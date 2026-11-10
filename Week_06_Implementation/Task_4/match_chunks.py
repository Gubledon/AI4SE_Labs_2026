"""Retrieve the n chunks most similar to a query embedding (cosine similarity).

Uses the storage built in Task 3. Run as a script to print the top 5 chunks
for every task in missing_code.json.
"""

import json
import sys
from pathlib import Path

import numpy as np

WEEK = Path(__file__).resolve().parent.parent
STORE = WEEK / "Task_3"
sys.path.insert(0, str(STORE))
from embed_chunks import embed  # noqa: E402

EMBEDDINGS = np.load(STORE / "embeddings.npy")
CHUNKS = json.loads((STORE / "chunks.json").read_text(encoding="utf-8"))


def ids_for(file, cls, name):
    """Ids of chunks for one method, e.g. the stub that Task 5 is replacing."""
    return {c["id"] for c in CHUNKS
            if c["file"] == file and c["class"] == cls and c["name"] == name}


def match(query_vector, n=5, exclude=(), max_tests=None):
    """Return [(score, chunk), ...] for the n best chunks, best first.

    query_vector must be unit length (embed() returns that), so the dot
    product with the unit-length stored rows is the cosine similarity.
    max_tests caps how many test chunks may be returned, so tests (512 of
    729 chunks) can't push all source code out of the result.
    """
    scores = EMBEDDINGS @ np.asarray(query_vector, dtype=np.float32).ravel()
    picked, tests = [], 0
    for i in np.argsort(-scores):
        if i in exclude:
            continue
        if CHUNKS[i]["role"] == "test":
            if max_tests is not None and tests >= max_tests:
                continue
            tests += 1
        picked.append((float(scores[i]), CHUNKS[i]))
        if len(picked) == n:
            break
    return picked


def main():
    tasks = json.loads((WEEK / "Assignments" / "missing_code.json").read_text(encoding="utf-8"))
    for task in tasks:
        doc = task["docstring"].strip().strip('"').strip()
        query = f'{task["file"]} {task["class"]}.{task["method"]}: {doc}'
        skip = ids_for(task["file"], task["class"], task["method"])
        print(f"\n{task['class']}.{task['method']}  (excluded stub ids: {sorted(skip)})")
        for score, chunk in match(embed([query])[0], n=5, exclude=skip, max_tests=2):
            where = f'{chunk["class"]}.{chunk["name"]}' if chunk["class"] else chunk["name"]
            print(f"  {score:.3f}  {chunk['role']:6}  {chunk['file']}  {where}")


if __name__ == "__main__":
    main()
