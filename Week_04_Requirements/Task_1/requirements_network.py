# LangGraph network that turns a folder of loose project texts (emails, minutes, interviews,
# drafts, surveys) into one structured requirements document in Markdown.
#
#   load (code) -> extract (LLM) -> merge (LLM) -> check_coverage (code) -> write (LLM) -> review (LLM)
#                                     ^                  |                                     |
#                                     +-- missed items --+                                     |
#                                     +------------------ review found issues -----------------+
#   review OK -> render (code)
#
# Usage: python3 requirements_network.py <input_dir> [--output requirements.md]
# Needs OPENAI_API_KEY in the environment or in a .env file in this folder or any parent.

from __future__ import annotations

import argparse
import json
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path
from typing import Literal, TypedDict

from dotenv import find_dotenv, load_dotenv
from langgraph.graph import END, START, StateGraph
from openai import OpenAI
from pydantic import BaseModel, Field


MODELS = {
    "extract": "gpt-5-mini",  # many calls, needs to read carefully and miss nothing
    "merge": "gpt-6-luna",  # one big reasoning step over all candidates
    "review": "gpt-5.6-luna",  # a different model than the one it checks
    "write": "gpt-5.4-nano",  # plain prose from facts it is given
}
MAX_CHUNK_CHARS = 8000
MAX_COVERAGE_ROUNDS = 2
MAX_REVIEW_ROUNDS = 5
WRITE_BATCH = 10
WORKERS = 8
MAX_ATTEMPTS = 3

PRIORITY_SCALE = {
    "High": "Agreed in a decision (a thread summary or ratified meeting minutes) or asked for in at "
    "least three different source documents.",
    "Medium": "Asked for in one or two source documents (for example only in the draft specification), "
    "with no later decision.",
    "Low": "Suggested by one person in a discussion and not confirmed by anyone, or an optional convenience.",
}
CATEGORIES = {
    "functional": ("FR", "Functional requirements"),
    "non_functional": ("NFR", "Non-functional requirements"),
    "constraint": ("CON", "Constraints"),
}

client: OpenAI | None = None


# ---------- structured outputs ----------

class Candidate(BaseModel):
    statement: str = Field(description="One atomic need, phrased as 'The system shall ...'")
    quote: str = Field(description="Short verbatim evidence from the text, at most 25 words")
    kind: Literal["functional", "non_functional", "constraint"]
    status: Literal["decision", "proposal", "existing_feature", "background"]
    date: str = Field(description="Date of the message or document it came from, YYYY-MM-DD, or 'unknown'")


class Extraction(BaseModel):
    candidates: list[Candidate]


class MergedRequirement(BaseModel):
    name: str
    statement: str
    kind: Literal["functional", "non_functional", "constraint"]
    candidate_ids: list[str]


class DiscardedItem(BaseModel):
    name: str
    statement: str
    reason: str
    candidate_ids: list[str]


class MergeResult(BaseModel):
    requirements: list[MergedRequirement]
    discarded: list[DiscardedItem]


class Assignment(BaseModel):
    candidate_id: str
    target: str = Field(description="Existing key, R# or D#")


class Combine(BaseModel):
    keep: str
    absorb: list[str]


class Update(BaseModel):
    key: str
    name: str
    statement: str
    kind: Literal["functional", "non_functional", "constraint"]


class Move(BaseModel):
    key: str
    reason: str = Field(description="Why it is discarded; empty when restoring")


class MergePatch(BaseModel):
    assign: list[Assignment]
    combine: list[Combine]
    update: list[Update]
    discard: list[Move]
    restore: list[Move]
    new_requirements: list[MergedRequirement]
    new_discarded: list[DiscardedItem]


class ReviewIssue(BaseModel):
    kind: Literal["duplicate", "conflict", "vocabulary", "unclear", "wrong_discard", "not_a_requirement"]
    items: list[str] = Field(description="Keys of the affected entries, e.g. R12, D3")
    problem: str
    fix: str


class Review(BaseModel):
    approved: bool
    issues: list[ReviewIssue]


class WrittenRequirement(BaseModel):
    key: str
    name: str = Field(description="Short descriptive name, at most 8 words")
    description: str = Field(description="One paragraph, 3 to 5 sentences")
    priority: Literal["High", "Medium", "Low"]


class WrittenBatch(BaseModel):
    requirements: list[WrittenRequirement]


class State(TypedDict, total=False):
    input_dir: str
    chunks: list[dict]
    candidates: list[dict]
    merged: dict
    feedback: str
    review_notes: str
    missing_ids: list[str]
    coverage_rounds: int
    review_rounds: int
    written: dict
    document: str


# ---------- helpers ----------

def ask(step, system, user, schema):
    for attempt in range(1, MAX_ATTEMPTS + 1):
        started = time.perf_counter()
        try:
            response = client.chat.completions.parse(
                model=MODELS[step],
                messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
                response_format=schema,
            )
            parsed = response.choices[0].message.parsed
            if parsed is None:
                raise ValueError("model returned no parsable output")
            usage = response.usage
            print(f"  [{step}] {MODELS[step]} {time.perf_counter() - started:.0f}s "
                  f"in={usage.prompt_tokens} out={usage.completion_tokens}", flush=True)
            return parsed
        except Exception as error:
            if attempt == MAX_ATTEMPTS:
                raise
            print(f"  [{step}] attempt {attempt} failed: {error}; retrying", flush=True)
            time.sleep(5 * attempt)


def split_into_chunks(text, limit):
    chunks, current = [], ""
    for paragraph in text.split("\n\n"):
        if current and len(current) + len(paragraph) > limit:
            chunks.append(current)
            current = ""
        current += paragraph + "\n\n"
    if current.strip():
        chunks.append(current)
    return chunks


FACT_STATUSES = ("existing_feature", "background")


def needs(state):
    return [c for c in state["candidates"] if c["status"] not in FACT_STATUSES]


def facts_as_text(state):
    return "\n".join(f"- {c['statement']} ({c['source']})" for c in state["candidates"]
                     if c["status"] in FACT_STATUSES)


def candidate_line(candidate):
    return (f"{candidate['id']} [{candidate['source']} | {candidate['date']} | {candidate['status']} | "
            f"{candidate['kind']}] {candidate['statement']}")


def merged_as_text(merged):
    lines = ["REQUIREMENTS:"]
    for index, item in enumerate(merged["requirements"], 1):
        lines.append(f"R{index} ({item['kind']}) {item['name']}: {item['statement']} "
                     f"<- {', '.join(item['candidate_ids'])}")
    lines.append("\nDISCARDED:")
    for index, item in enumerate(merged["discarded"], 1):
        lines.append(f"D{index} {item['name']}: {item['statement']} | reason: {item['reason']} "
                     f"<- {', '.join(item['candidate_ids'])}")
    return "\n".join(lines)


# ---------- nodes ----------

def load(state: State):
    """Deterministic: read every text file under the input folder and cut it into chunks."""
    root = Path(state["input_dir"])
    chunks = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or any(part.startswith(".") for part in path.relative_to(root).parts):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            print(f"  skipping non-text file {path}", flush=True)
            continue
        lines = [line.rstrip() for line in text.replace("\r\n", "\n").split("\n")]
        text = "\n".join(lines)
        while "\n\n\n" in text:
            text = text.replace("\n\n\n", "\n\n")
        source = path.relative_to(root).as_posix()
        parts = split_into_chunks(text, MAX_CHUNK_CHARS)
        for number, part in enumerate(parts, 1):
            chunks.append({"source": source, "part": f"{number}/{len(parts)}", "text": part})
    if not chunks:
        raise SystemExit(f"No text files found in {root}")
    print(f"load: {len({c['source'] for c in chunks})} files, {len(chunks)} chunks", flush=True)
    return {"chunks": chunks}


EXTRACT_PROMPT = """You extract software requirements from project documents for a requirements engineer.
You get one excerpt of one document. List EVERY requirement-like statement in it: features, reports,
data the system must show, filters, permissions, quality attributes (performance, security, usability,
privacy), technical and legal constraints, and concrete wishes made in discussions, even if someone
else disagrees later. A later step resolves duplicates and conflicts, so do not drop anything because
it seems repeated or disputed. Completeness matters more than brevity.

Rules:
- One atomic need per candidate. Split sentences that ask for several things.
- Within this excerpt, list each need once, even if it is repeated (e.g. quoted replies).
- Write each as "The system shall ..." in plain, specific words. Keep numbers, names and limits.
- status: "decision" if agreed or ratified (a summary of a discussion, minutes that approve it),
  "proposal" if one person suggests or asks for it or it is only in a draft, "existing_feature" if it describes what the current software
  already does, "background" if it is context rather than a need.
- date: the date of the message or document the statement is in, if the excerpt shows it.
- Ignore personal chatter, greetings, signatures, jokes, scheduling and action items about people.
- If the excerpt has no requirements, return an empty list."""


def extract(state: State):
    """LLM: pull candidate requirements out of every chunk, in parallel."""
    def run(chunk):
        user = f"Document: {chunk['source']} (part {chunk['part']})\n\n{chunk['text']}"
        return chunk, ask("extract", EXTRACT_PROMPT, user, Extraction).candidates

    candidates = []
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        for chunk, found in pool.map(run, state["chunks"]):
            for item in found:
                candidates.append({"source": chunk["source"], **item.model_dump()})
    for number, candidate in enumerate(candidates, 1):
        candidate["id"] = f"C{number:03d}"
    print(f"extract: {len(candidates)} candidates", flush=True)
    return {"candidates": candidates}


MERGE_PROMPT = """You are a senior requirements engineer. You get candidate requirements extracted from
many project documents. Each line is: ID [source file | date | status | kind] statement.
Turn them into one clean, consistent set of requirements.

Rules:
- Merge semantic duplicates (same need, different words or sources) into ONE requirement and list
  all their candidate IDs. Keep the most specific details (numbers, filters, levels) from the group.
- One requirement per feature: a report or function together with its own filters, columns,
  grouping levels, sorting and export options is ONE requirement; put those details in its
  statement. Keep different reports or features separate.
- Conflicts: when candidates contradict each other, keep the one with more authority: a decision
  beats a proposal, a later date beats an earlier one, a ratified summary or minutes beat a draft.
  Put the losing version in "discarded" and name the winning version in the reason.
- Look actively for conflicts: the same setting, term or behaviour given different values in
  different sources (periods, limits, definitions, allowed methods, whether something exists).
  Every conflict ends with one winner; the others are discarded.
- A need agreed in a decision can only be discarded by a newer decision or by a fact that
  contradicts it, never by a broad scope argument.
- Discard nonsensical, technically impossible or explicitly out-of-scope items, with the reason
  (e.g. a request that relies on data or a status the sources say does not exist).
- Never invent numbers, limits, technologies or details that are not in the candidates.
- Reasons must read on their own: refer to other requirements by name, never by candidate ID.
- After the candidates you get FACTS: what the sources say about the existing system and data.
  They are context, not candidates. A candidate that a fact contradicts (it relies on data, a
  status or a field the facts say does not exist or works differently) is nonsensical and must be
  discarded, naming the fact. A field the facts simply do not mention is not a contradiction.
- Project process is not a system requirement: how the specification is written or reviewed,
  who contributes input, development method, meetings. Discard it with that reason.
- Use one vocabulary: the same term for the same thing everywhere (pick the term of the latest
  authoritative source). Every statement starts with "The system shall".
- name: short descriptive name, at most 8 words.
- EVERY candidate ID must appear in exactly one requirement or one discarded item. Do not drop any.
- kind: functional, non_functional or constraint."""


PATCH_PROMPT = MERGE_PROMPT + """

You already built a requirements set (below, keys R# and D#). Now fix the listed problems. Do NOT
return the whole set again; return only the edits, and leave every list empty that you do not need:
- assign: put a candidate into an existing requirement (R#) or discarded item (D#).
- combine: duplicate requirements; "keep" one key, the "absorb" keys are folded into it.
- update: new name, statement or kind for an existing requirement (wording, vocabulary, conflicts).
- discard: move a requirement to the discarded list, with the reason.
- restore: move a discarded item (D#) back to the requirements.
- new_requirements / new_discarded: for candidates that fit nowhere existing."""


def apply_patch(merged, patch):
    requirements = {f"R{i}": r for i, r in enumerate(merged["requirements"], 1)}
    discarded = {f"D{i}": d for i, d in enumerate(merged["discarded"], 1)}
    for item in patch.assign:
        target = requirements.get(item.target) or discarded.get(item.target)
        if target is not None:
            target["candidate_ids"].append(item.candidate_id)
    for item in patch.combine:
        keep = requirements.get(item.keep)
        for key in item.absorb:
            if keep is not None and key != item.keep and key in requirements:
                keep["candidate_ids"] += requirements.pop(key)["candidate_ids"]
    for item in patch.update:
        if item.key in requirements:
            requirements[item.key].update(name=item.name, statement=item.statement, kind=item.kind)
    for item in patch.discard:
        if item.key in requirements:
            moved = requirements.pop(item.key)
            discarded["new" + item.key] = {"name": moved["name"], "statement": moved["statement"],
                                           "reason": item.reason, "candidate_ids": moved["candidate_ids"]}
    for item in patch.restore:
        if item.key in discarded:
            moved = discarded.pop(item.key)
            requirements["new" + item.key] = {"name": moved["name"], "statement": moved["statement"],
                                              "kind": "functional", "candidate_ids": moved["candidate_ids"]}
    return {"requirements": list(requirements.values()) + [r.model_dump() for r in patch.new_requirements],
            "discarded": list(discarded.values()) + [d.model_dump() for d in patch.new_discarded]}


def merge(state: State):
    """LLM: deduplicate, resolve conflicts and blacklist. On feedback it returns edits, not a new set."""
    candidates = "\n".join(candidate_line(c) for c in needs(state))
    user = f"CANDIDATES ({len(needs(state))}):\n{candidates}\n\nFACTS:\n{facts_as_text(state)}"
    if state.get("feedback"):
        user += ("\n\nCURRENT SET:\n" + merged_as_text(state["merged"]) +
                 "\n\nPROBLEMS TO FIX:\n" + state["feedback"])
        merged = apply_patch(state["merged"], ask("merge", PATCH_PROMPT, user, MergePatch))
    else:
        merged = ask("merge", MERGE_PROMPT, user, MergeResult).model_dump()
    print(f"merge: {len(merged['requirements'])} requirements, {len(merged['discarded'])} discarded",
          flush=True)
    return {"merged": merged, "feedback": ""}


def check_coverage(state: State):
    """Deterministic: every candidate must end up in a requirement or in the blacklist."""
    known = {c["id"] for c in needs(state)}
    used = set()
    for item in state["merged"]["requirements"] + state["merged"]["discarded"]:
        item["candidate_ids"] = [i for i in dict.fromkeys(item["candidate_ids"]) if i in known]
        used.update(item["candidate_ids"])
    # Entries without a valid candidate cannot be traced to a source, so they are dropped.
    state["merged"]["requirements"] = [r for r in state["merged"]["requirements"] if r["candidate_ids"]]
    discarded = {}
    for item in state["merged"]["discarded"]:
        if not item["candidate_ids"]:
            continue
        key = (item["name"].lower(), item["statement"].lower())
        if key in discarded:
            discarded[key]["candidate_ids"] += [i for i in item["candidate_ids"]
                                                if i not in discarded[key]["candidate_ids"]]
        else:
            discarded[key] = item
    state["merged"]["discarded"] = list(discarded.values())
    missing = sorted(known - used)
    rounds = state.get("coverage_rounds", 0)
    print(f"check_coverage: {len(missing)} candidates not placed", flush=True)
    update = {"merged": state["merged"], "missing_ids": missing}
    if missing and rounds < MAX_COVERAGE_ROUNDS:
        by_id = {c["id"]: c for c in state["candidates"]}
        update["feedback"] = ("These candidates are not in any requirement or discarded item. "
                              "Place each one:\n" + "\n".join(candidate_line(by_id[i]) for i in missing))
        update["coverage_rounds"] = rounds + 1
    return update


def after_coverage(state: State):
    return "merge" if state.get("feedback") else "write"


WRITE_PROMPT = """You write entries for a software requirements document. For each requirement you get
its key, a draft name, the statement and the source evidence it was derived from. Return for each:
- name: short descriptive name, at most 8 words, in Title Case.
- description: one paragraph of 2 to 4 sentences. Say what the system shall do, for whom and why,
  with the concrete details from the evidence (fields, filters, levels, numbers). Use only facts
  from the statement and evidence; never add numbers or details that are not there. Keep the
  wording "The system shall" for the core sentence. No filler about how important it is, and do not
  use: crucial, vital, essential, robust, seamless, enhance, leverage, pivotal, ensure. Do not
  write about the evidence or the sources in the paragraph; describe only the system.
  Leave out any detail that relies on data the evidence says does not exist.
- priority, on this scale (count the source documents and look at the status of the evidence):
{scale}
Return every key you were given, unchanged.
Use the same term for the same concept in every entry."""


def write(state: State):
    """LLM: write name, paragraph and priority for every requirement, in parallel batches."""
    by_id = {c["id"]: c for c in state["candidates"]}
    scale = "\n".join(f"  {level}: {meaning}" for level, meaning in PRIORITY_SCALE.items())
    system = WRITE_PROMPT.format(scale=scale)
    if state.get("review_notes"):
        system += ("\n\nA reviewer checked the previous version. Apply the notes about names, wording or "
                   "priority to the requirements they mention (matched by name):\n" + state["review_notes"])
    items = list(enumerate(state["merged"]["requirements"], 1))
    batches = [items[i:i + WRITE_BATCH] for i in range(0, len(items), WRITE_BATCH)]

    def run(batch):
        blocks = []
        for index, item in batch:
            evidence = "\n".join(f"  - ({by_id[i]['source']}, {by_id[i]['status']}) \"{by_id[i]['quote']}\""
                                 for i in item["candidate_ids"])
            documents = len({by_id[i]["source"] for i in item["candidate_ids"]})
            blocks.append(f"KEY R{index}\nName: {item['name']}\nStatement: {item['statement']}\n"
                          f"Source documents: {documents}\nEvidence:\n{evidence}")
        return ask("write", system, "\n\n".join(blocks), WrittenBatch).requirements

    written = {}
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        for result in pool.map(run, batches):
            for entry in result:
                written[entry.key] = entry.model_dump()
    # The High rule of the scale is mechanical, so code enforces it; Medium vs Low stays with the model.
    for index, item in items:
        entry = written.get(f"R{index}")
        if entry is None:
            continue
        evidence = [by_id[i] for i in item["candidate_ids"]]
        high = (any(c["status"] == "decision" for c in evidence)
                or len({c["source"] for c in evidence}) >= 3)
        if high:
            entry["priority"] = "High"
        elif entry["priority"] == "High":
            entry["priority"] = "Medium"
    print(f"write: {len(written)}/{len(items)} requirements written", flush=True)
    return {"written": written}


REVIEW_PROMPT = """You are a strict reviewer of a finished requirements document. Check it against these rules:
1. No two requirements describe the same need (semantic duplicates).
2. No two requirements contradict or conflict with each other.
3. Consistent language: the same term for the same concept in names and descriptions.
4. Each requirement is clear, testable and makes sense. Background facts are not requirements.
5. Each name is short and fits its description. Priorities are set by a fixed rule in code on
   this scale, so do not report priority problems:
{scale}
6. Discarded items were discarded for a good reason (real conflict, nonsense, out of scope), and no
   valid, non-conflicting need was wrongly discarded.
7. No requirement relies on data, a field or a status that the FACTS section (what the sources say
   about the existing system and data) says does not exist or works differently. Such a
   requirement is a "conflict" and must be discarded with the fact as the reason. A field the
   facts simply do not mention is NOT a conflict.
8. A need the sources agreed in a decision must not be discarded because of a broad scope
   statement; only a newer decision or a contradicting fact can remove it.
9. Requirements that are only a detail of another feature (a filter, column, export option of
   the same report) should be combined into that feature.
10. Check the details inside each requirement too (sort keys, fields, statuses), not only its
   main idea. A detail the FACTS contradict must be removed from the requirement.
Only report real problems. Do not report vague wording that cannot be fixed from the sources. For each, give the keys (R#, D#), the problem and a concrete fix.
A fix may only use facts already in the document: never ask to add numbers, limits or details
that the sources do not give, even to make a requirement testable.
Set approved=true if there are no problems that matter."""


def final_as_text(state):
    lines = ["REQUIREMENTS:"]
    for index, item in enumerate(state["merged"]["requirements"], 1):
        text = state["written"].get(f"R{index}", {})
        lines.append(f"R{index} ({item['kind']}, {text.get('priority', '?')}) {text.get('name', item['name'])}: "
                     f"{text.get('description', item['statement'])}")
    lines.append("\nDISCARDED:")
    for index, item in enumerate(state["merged"]["discarded"], 1):
        lines.append(f"D{index} {item['name']}: {item['statement']} | reason: {item['reason']}")
    lines.append("\nFACTS (what the sources say about the existing system and data):")
    lines.append(facts_as_text(state))
    return "\n".join(lines)


def review(state: State):
    """LLM: check the written document; on problems send it back to merge and write (feedback loop)."""
    scale = "\n".join(f"  {level}: {meaning}" for level, meaning in PRIORITY_SCALE.items())
    result = ask("review", REVIEW_PROMPT.format(scale=scale), final_as_text(state), Review)
    rounds = state.get("review_rounds", 0) + 1
    print(f"review: round {rounds}, approved={result.approved}, {len(result.issues)} issues", flush=True)
    for issue in result.issues:
        print(f"    - {issue.kind} {', '.join(issue.items)}: {issue.problem}", flush=True)
    update = {"review_rounds": rounds, "coverage_rounds": 0}
    if result.issues and not result.approved and rounds <= MAX_REVIEW_ROUNDS:
        names = {f"R{i}": state["written"].get(f"R{i}", r)["name"]
                 for i, r in enumerate(state["merged"]["requirements"], 1)}
        names.update({f"D{i}": d["name"] for i, d in enumerate(state["merged"]["discarded"], 1)})
        lines = [f"- {issue.kind} {', '.join(f'{k} ({names.get(k, k)})' for k in issue.items)}: "
                 f"{issue.problem} Fix: {issue.fix}" for issue in result.issues]
        update["feedback"] = "\n".join(lines)
        update["review_notes"] = "\n".join(lines)
    return update


def after_review(state: State):
    return "merge" if state.get("feedback") else "render"


def render(state: State):
    """Deterministic: assign IDs, attach sources and lay out the final document."""
    by_id = {c["id"]: c for c in state["candidates"]}
    sources_of = lambda ids: sorted({by_id[i]["source"] for i in ids})
    files = sorted({c["source"] for c in state["chunks"]})

    entries = {kind: [] for kind in CATEGORIES}
    for index, item in enumerate(state["merged"]["requirements"], 1):
        text = state["written"].get(f"R{index}") or {
            "name": item["name"], "description": item["statement"], "priority": "Medium"}
        entries[item["kind"]].append((item, text))

    out = ["# Software Requirements Specification", "",
           f"Generated on {date.today().isoformat()} by `requirements_network.py` from {len(files)} input "
           f"documents in `{state['input_dir']}`.", "",
           "Models: " + ", ".join(f"{step} = `{model}`" for step, model in MODELS.items()) + ".", "",
           f"{len(state['candidates'])} statements were extracted. {len(needs(state))} were requirement "
           f"candidates; the other {len(state['candidates']) - len(needs(state))} describe the existing "
           "system and were used as facts for spotting nonsensical requests, not as requirements.", "",
           "## Priority scale", "", "| Priority | Meaning |", "|---|---|"]
    out += [f"| {level} | {meaning} |" for level, meaning in PRIORITY_SCALE.items()]
    out += ["", "## Summary", "", "| ID | Name | Priority |", "|---|---|---|"]

    numbered = []
    order = {"High": 0, "Medium": 1, "Low": 2}
    for kind, (prefix, _title) in CATEGORIES.items():
        ranked = sorted(entries[kind], key=lambda pair: order.get(pair[1]["priority"], 1))
        for number, (item, text) in enumerate(ranked, 1):
            numbered.append((kind, f"{prefix}-{number:03d}", item, text))
    out += [f"| {rid} | {text['name']} | {text['priority']} |" for _kind, rid, _item, text in numbered]

    for kind, (_prefix, title) in CATEGORIES.items():
        out += ["", f"## {title}"]
        for _kind, rid, item, text in (n for n in numbered if n[0] == kind):
            out += ["", f"### {rid}: {text['name']}", "",
                    f"**Priority:** {text['priority']}  ",
                    f"**Sources:** {', '.join(f'`{s}`' for s in sources_of(item['candidate_ids']))}", "",
                    text["description"]]

    out += ["", "## Discarded requirements (blacklist)", "",
            "Candidates that were found in the inputs but left out of the specification, with the reason.", ""]
    for number, item in enumerate(state["merged"]["discarded"], 1):
        out += [f"### DR-{number:03d}: {item['name']}", "",
                f"**Sources:** {', '.join(f'`{s}`' for s in sources_of(item['candidate_ids']))}  ",
                f"**Statement:** {item['statement']}  ", f"**Reason:** {item['reason']}", ""]

    if state.get("missing_ids"):
        out += ["## Unplaced candidates", "",
                "The merge step did not place these extracted candidates; listed so nothing is lost.", ""]
        out += [f"- {by_id[i]['statement']} (`{by_id[i]['source']}`)" for i in state["missing_ids"]]

    print(f"render: {len(numbered)} requirements, {len(state['merged']['discarded'])} discarded", flush=True)
    return {"document": "\n".join(out) + "\n"}


def build_graph():
    graph = StateGraph(State)
    for name, node in [("load", load), ("extract", extract), ("merge", merge),
                       ("check_coverage", check_coverage), ("review", review),
                       ("write", write), ("render", render)]:
        graph.add_node(name, node)
    graph.add_edge(START, "load")
    graph.add_edge("load", "extract")
    graph.add_edge("extract", "merge")
    graph.add_edge("merge", "check_coverage")
    graph.add_conditional_edges("check_coverage", after_coverage, ["merge", "write"])
    graph.add_edge("write", "review")
    graph.add_conditional_edges("review", after_review, ["merge", "render"])
    graph.add_edge("render", END)
    return graph.compile()


def main():
    global client
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", help="folder with the input documents (read recursively)")
    parser.add_argument("--output", default="requirements.md")
    args = parser.parse_args()

    load_dotenv(find_dotenv(usecwd=True))
    client = OpenAI(timeout=1200)
    final = build_graph().invoke({"input_dir": args.input_dir}, {"recursion_limit": 50})
    Path(args.output).write_text(final["document"], encoding="utf-8")
    print(f"written {args.output}", flush=True)


if __name__ == "__main__":
    main()
