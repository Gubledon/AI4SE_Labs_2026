# Scores the predictions of every prompt and draws the comparison chart.
# Correctness uses the official evaluator's own database loader and row comparison
# (data/evaluate_retrieval_predictions.py). Unlike the official script, a query that
# fails to run is counted as wrong instead of stopping the evaluation.
#
# Usage: python3 evaluate_predictions.py

import csv
import importlib.util
import json
import re
import sqlite3
import statistics
from pathlib import Path


TASK_DIR = Path(__file__).resolve().parent
PREDICTIONS_DIR = TASK_DIR / "predictions"
RESULTS_DIR = TASK_DIR / "results"
LABELS_PATH = TASK_DIR / "data" / "restaurants_dataset.csv"
EVALUATOR_PATH = TASK_DIR / "data" / "evaluate_retrieval_predictions.py"

PROMPT_IDS = ["P1_CO_STAR", "P2_CHAIN_OF_THOUGHT", "P3_FEW_SHOT"]
COLORS = {"P1_CO_STAR": "#3b6fd4", "P2_CHAIN_OF_THOUGHT": "#e07b28", "P3_FEW_SHOT": "#1f9e74"}
CATEGORIES = ["city", "street", "region", "best", "name", "other", "noisy"]

CORE_PATTERN = re.compile(
    r"(what is|what are|where is|where are|where can i eat|where can (?:i|we) find|give me)[^,?]*", re.I
)


def load_evaluator():
    spec = importlib.util.spec_from_file_location("official_evaluator", EVALUATOR_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def classify(question):
    """Question template, judged on the request clause only, plus whether filler text surrounds it."""
    match = CORE_PATTERN.search(question)
    core = match.group(0).lower() if match else question.lower()
    noisy = core.strip() != question.lower().rstrip(" ?").strip()
    if " in " not in core:
        kind = "other"
    elif re.search(r"\bbest\b", core):
        kind = "best"
    elif re.match(r"where is (?!a |an |some )", core) and "rating" not in core:
        kind = "name"
    elif re.search(r" in the |northern california", core):
        kind = "region"
    elif " on " in core:
        kind = "street"
    else:
        kind = "city"
    return kind, noisy


def percentile(values, share):
    ordered = sorted(values)
    return ordered[min(len(ordered) - 1, int(round(share * (len(ordered) - 1))))]


def main():
    evaluator = load_evaluator()
    csv.field_size_limit(1_000_000_000)
    with LABELS_PATH.open(encoding="utf-8", newline="") as source:
        labels = [(row["question"], json.loads(row["result"])) for row in csv.DictReader(source)]

    connection = evaluator.load_database()
    RESULTS_DIR.mkdir(exist_ok=True)
    per_question, summary, failures = [], [], []

    for prompt_id in PROMPT_IDS:
        path = PREDICTIONS_DIR / f"{prompt_id}_predictions.csv"
        if not path.exists():
            continue
        with path.open(encoding="utf-8", newline="") as source:
            predictions = {int(row["row"]): row for row in csv.DictReader(source)}

        times, walls, out_tokens, costs = [], [], [], []
        correct = errors = missing = 0
        meta = next(iter(predictions.values()))
        for index, (question, expected) in enumerate(labels):
            row = predictions.get(index)
            kind, noisy = classify(question)
            status = "missing"
            if row is not None:
                assert row["question"] == question, f"row {index} question mismatch in {path.name}"
                times.append(float(row["inference_ms"]))
                walls.append(float(row["wall_ms"]))
                out_tokens.append(float(row["output_tokens"]))
                costs.append(float(row["cost_usd"]))
                rows = []
                if not row["predicted_sql"]:
                    status = "no_sql"
                else:
                    try:
                        rows = connection.execute(row["predicted_sql"]).fetchall()
                        same = evaluator.row_multiset(rows) == evaluator.row_multiset(expected)
                        status = "correct" if same else "wrong_rows"
                    except sqlite3.Error:
                        status = "sql_error"
                if status != "correct":
                    failures.append({
                        "row": index,
                        "prompt_id": prompt_id,
                        "status": status,
                        "expected_rows": len(expected),
                        "predicted_rows": len(rows),
                        "question": question,
                        "predicted_sql": row["predicted_sql"],
                        "raw_response": row["raw_response"] if status == "no_sql" else "",
                    })
            correct += status == "correct"
            errors += status == "sql_error"
            missing += status in ("missing", "no_sql")
            per_question.append({
                "row": index,
                "prompt_id": prompt_id,
                "category": kind,
                "noisy": noisy,
                "status": status,
                "correct": status == "correct",
                "inference_ms": row["inference_ms"] if row else "",
                "question": question,
            })

        summary.append({
            "prompt_id": prompt_id,
            "framework": meta["framework"],
            "model": meta["model"],
            "questions": len(labels),
            "correct": correct,
            "accuracy": round(correct / len(labels), 4),
            "sql_errors": errors,
            "missing_or_no_sql": missing,
            "mean_inference_ms": round(statistics.mean(times)),
            "median_inference_ms": round(statistics.median(times)),
            "p90_inference_ms": round(percentile(times, 0.9)),
            "mean_wall_ms": round(statistics.mean(walls)),
            "mean_output_tokens": round(statistics.mean(out_tokens)),
            "total_cost_usd": round(sum(costs), 4),
        })

    connection.close()
    write_csv(RESULTS_DIR / "per_question.csv", per_question)
    write_csv(RESULTS_DIR / "summary.csv", summary)
    write_csv(RESULTS_DIR / "failures.csv", failures)
    by_category = category_accuracy(per_question)
    write_csv(RESULTS_DIR / "accuracy_by_category.csv", by_category)
    (RESULTS_DIR / "comparison.svg").write_text(draw_chart(summary, by_category), encoding="utf-8")

    for item in summary:
        print(
            f"{item['prompt_id']:<22} accuracy {item['accuracy']:.2%} ({item['correct']}/{item['questions']})"
            f"  sql errors {item['sql_errors']}  median {item['median_inference_ms']} ms"
            f"  mean {item['mean_inference_ms']} ms"
        )


def category_accuracy(per_question):
    table = []
    for category in CATEGORIES:
        entry = {"category": category}
        for prompt_id in PROMPT_IDS:
            rows = [
                r for r in per_question
                if r["prompt_id"] == prompt_id and (r["noisy"] if category == "noisy" else r["category"] == category)
            ]
            entry["n"] = len(rows) or entry.get("n", 0)
            entry[prompt_id] = round(sum(r["correct"] for r in rows) / len(rows), 4) if rows else ""
        table.append(entry)
    return table


def write_csv(path, rows):
    with path.open("w", encoding="utf-8", newline="") as target:
        writer = csv.DictWriter(target, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def draw_chart(summary, by_category):
    """Three panels as a standalone SVG: accuracy, inference time, and accuracy per question type."""
    width, parts = 860, []
    font = "font-family='Segoe UI, Helvetica, Arial, sans-serif'"

    def text(x, y, value, size=12, anchor="start", weight="normal", fill="#2b2b2b"):
        parts.append(
            f"<text x='{x}' y='{y}' {font} font-size='{size}' text-anchor='{anchor}' "
            f"font-weight='{weight}' fill='{fill}'>{value}</text>"
        )

    def short(prompt_id):
        return {"P1_CO_STAR": "P1 CO-STAR", "P2_CHAIN_OF_THOUGHT": "P2 Chain of Thought", "P3_FEW_SHOT": "P3 Few-Shot"}[prompt_id]

    model = summary[0]["model"] if summary else ""
    text(30, 34, f"Text-to-SQL on restaurants dataset: 3 prompts, {model}", 17, weight="bold")
    count = summary[0]["questions"] if summary else 0
    text(30, 54, f"{count} questions per prompt, each question in a fresh claude -p session", 12, fill="#666")

    # Panel 1: accuracy. Panel 2: median inference time with p90 whisker.
    panels = [
        ("Accuracy (exact row match)", "accuracy", lambda v: f"{v * 100:.1f}%", 1.0, 30),
        ("Inference time per question (median, whisker = p90)", "median_inference_ms",
         lambda v: f"{v / 1000:.1f} s", max([s["p90_inference_ms"] for s in summary] + [1]) * 1.15, 450),
    ]
    for title, key, label, top, left in panels:
        base, height, bar = 260, 160, 70
        text(left, 90, title, 13, weight="bold")
        parts.append(f"<line x1='{left}' y1='{base}' x2='{left + 380}' y2='{base}' stroke='#bbb'/>")
        for i, item in enumerate(summary):
            x = left + 25 + i * 120
            value = item[key]
            h = height * value / top
            parts.append(f"<rect x='{x}' y='{base - h}' width='{bar}' height='{h}' rx='3' fill='{COLORS[item['prompt_id']]}'/>")
            if key == "median_inference_ms":
                p90 = base - height * item["p90_inference_ms"] / top
                cx = x + bar / 2
                parts.append(f"<line x1='{cx}' y1='{base - h}' x2='{cx}' y2='{p90}' stroke='#444'/>")
                parts.append(f"<line x1='{cx - 8}' y1='{p90}' x2='{cx + 8}' y2='{p90}' stroke='#444'/>")
                text(cx, p90 - 6, label(item["p90_inference_ms"]), 10, "middle", fill="#666")
                text(cx, base - h + 16, label(value), 12, "middle", "bold", "#fff")
            else:
                text(x + bar / 2, base - h - 6, label(value), 12, "middle", "bold")
            text(x + bar / 2, base + 18, short(item["prompt_id"]).split(" ", 1)[0], 12, "middle", "bold")
            text(x + bar / 2, base + 33, short(item["prompt_id"]).split(" ", 1)[1], 10, "middle", fill="#666")

    # Panel 3: accuracy per question type, grouped bars.
    top_y, base, height = 330, 520, 160
    text(30, top_y, "Accuracy by question type", 13, weight="bold")
    parts.append(f"<line x1='30' y1='{base}' x2='{width - 30}' y2='{base}' stroke='#bbb'/>")
    group_width = (width - 60) / len(by_category)
    for g, entry in enumerate(by_category):
        gx = 30 + g * group_width + 10
        for i, prompt_id in enumerate(PROMPT_IDS):
            value = entry.get(prompt_id)
            if value == "":
                continue
            h = height * value
            x = gx + i * 30
            parts.append(f"<rect x='{x}' y='{base - h}' width='26' height='{h}' rx='2' fill='{COLORS[prompt_id]}'/>")
            text(x + 13, base - h - 4, f"{value * 100:.0f}", 10, "middle", fill="#444")
        label = "with filler" if entry["category"] == "noisy" else entry["category"]
        text(gx + 43, base + 18, label, 12, "middle", "bold")
        text(gx + 43, base + 33, f"n = {entry['n']}", 10, "middle", fill="#666")

    for i, prompt_id in enumerate(PROMPT_IDS):
        x = 30 + i * 220
        parts.append(f"<rect x='{x}' y='575' width='14' height='14' rx='2' fill='{COLORS[prompt_id]}'/>")
        text(x + 20, 587, short(prompt_id), 12)

    return (
        f"<svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='610' viewBox='0 0 {width} 610'>"
        f"<rect width='100%' height='100%' fill='#ffffff'/>{''.join(parts)}</svg>"
    )


if __name__ == "__main__":
    main()
