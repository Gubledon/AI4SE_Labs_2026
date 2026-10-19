# Runs every question from the dataset through each Task 1 prompt with the Claude Code CLI
# (`claude -p`). Every call is a fresh, isolated session: the prompt is the system prompt,
# the question is the only user message, and no tools, settings, hooks or MCP servers load.
# Calls run in parallel. Results are saved after each call, so the script can be resumed.
#
# Usage: python3 run_predictions.py [--workers 8] [--model claude-sonnet-5-5] [--prompts P1 P2 P3] [--limit N]

import argparse
import csv
import json
import random
import re
import subprocess
import tempfile
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


TASK_DIR = Path(__file__).resolve().parent
LABELS_PATH = TASK_DIR / "data" / "restaurants_dataset.csv"
PROMPTS_DIR = TASK_DIR.parent / "Task_1" / "prompts"
OUTPUT_DIR = TASK_DIR / "predictions"

PROMPTS = {
    "P1": ("P1_CO_STAR", "CO-STAR", "p1_co_star.txt"),
    "P2": ("P2_CHAIN_OF_THOUGHT", "Chain of Thought", "p2_chain_of_thought.txt"),
    "P3": ("P3_FEW_SHOT", "Few-Shot", "p3_few_shot.txt"),
}

FIELDS = [
    "row",
    "question",
    "predicted_sql",
    "prompt_id",
    "framework",
    "model",
    "inference_ms",
    "wall_ms",
    "input_tokens",
    "output_tokens",
    "cost_usd",
    "session_id",
    "raw_response",
]

SQL_PATTERN = re.compile(r"<sql>(.*?)</sql>", re.S | re.I)
MAX_ATTEMPTS = 3


def load_questions():
    csv.field_size_limit(1_000_000_000)
    with LABELS_PATH.open(encoding="utf-8", newline="") as source:
        return [row["question"] for row in csv.DictReader(source)]


def extract_sql(text):
    matches = SQL_PATTERN.findall(text or "")
    return " ".join(matches[-1].split()) if matches else ""


def call_model(system_prompt, question, model, workdir):
    command = [
        "claude", "-p",
        "--model", model,
        "--system-prompt", system_prompt,
        "--tools", "",
        "--setting-sources", "",
        "--strict-mcp-config",
        "--no-session-persistence",
        "--output-format", "json",
    ]
    for attempt in range(1, MAX_ATTEMPTS + 1):
        started = time.perf_counter()
        process = subprocess.run(
            command, input=question, capture_output=True, text=True, cwd=workdir, timeout=600
        )
        wall_ms = round((time.perf_counter() - started) * 1000)
        try:
            payload = json.loads(process.stdout)
        except json.JSONDecodeError:
            payload = None
        if process.returncode == 0 and payload and not payload.get("is_error"):
            return payload, wall_ms
        if attempt == MAX_ATTEMPTS:
            raise RuntimeError(f"claude -p failed: {process.stderr.strip() or process.stdout[:300]}")
        time.sleep(5 * attempt)


def output_path(prompt_id):
    return OUTPUT_DIR / f"{prompt_id}_predictions.csv"


def load_done(prompt_id):
    path = output_path(prompt_id)
    if not path.exists():
        return {}
    with path.open(encoding="utf-8", newline="") as source:
        return {int(row["row"]): row for row in csv.DictReader(source)}


def save(prompt_id, rows):
    path = output_path(prompt_id)
    temporary = path.with_suffix(".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as target:
        writer = csv.DictWriter(target, fieldnames=FIELDS)
        writer.writeheader()
        for index in sorted(rows):
            writer.writerow(rows[index])
    temporary.replace(path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--model", default="claude-sonnet-5-5")
    parser.add_argument("--prompts", nargs="+", default=list(PROMPTS))
    parser.add_argument("--limit", type=int, help="only the first N questions (for a quick test)")
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(exist_ok=True)
    questions = load_questions()[: args.limit]
    workdir = tempfile.mkdtemp(prefix="task2_clean_")

    system_prompts, results, jobs = {}, {}, []
    for key in args.prompts:
        prompt_id, _framework, filename = PROMPTS[key]
        system_prompts[key] = (PROMPTS_DIR / filename).read_text(encoding="utf-8")
        results[key] = load_done(prompt_id)
        jobs += [(key, index) for index in range(len(questions)) if index not in results[key]]

    # Interleave prompts so they share the same load conditions during the run.
    random.Random(0).shuffle(jobs)
    print(f"{len(jobs)} calls to make with {args.workers} workers", flush=True)

    lock = threading.Lock()

    def run(job):
        key, index = job
        payload, wall_ms = call_model(system_prompts[key], questions[index], args.model, workdir)
        usage = payload.get("usage", {})
        prompt_id, framework, _filename = PROMPTS[key]
        return key, index, {
            "row": index,
            "question": questions[index],
            "predicted_sql": extract_sql(payload.get("result", "")),
            "prompt_id": prompt_id,
            "framework": framework,
            "model": args.model,
            "inference_ms": payload.get("duration_api_ms"),
            "wall_ms": wall_ms,
            "input_tokens": usage.get("input_tokens", 0)
            + usage.get("cache_creation_input_tokens", 0)
            + usage.get("cache_read_input_tokens", 0),
            "output_tokens": usage.get("output_tokens"),
            "cost_usd": payload.get("total_cost_usd"),
            "session_id": payload.get("session_id"),
            "raw_response": payload.get("result", ""),
        }

    finished = 0
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(run, job) for job in jobs]
        for future in as_completed(futures):
            try:
                key, index, row = future.result()
            except Exception as error:  # keep going; a rerun picks up the missing rows
                print(f"FAILED: {error}", flush=True)
                continue
            with lock:
                results[key][index] = row
                save(PROMPTS[key][0], results[key])
                finished += 1
            if finished % 20 == 0 or finished == len(jobs):
                print(f"{finished}/{len(jobs)} done", flush=True)


if __name__ == "__main__":
    main()
