# Diner Score: a graded metric for the restaurants text-to-SQL problem.
#
# Each answer is treated as a list of restaurants that a hungry person would act on.
# Per question, the predicted rows and the reference rows are compared as multisets:
#   overlap   = rows in both
#   precision = overlap / predicted rows   (how many recommended places are right)
#   recall    = overlap / reference rows   (how many right places were found)
#   score     = F0.5 of precision and recall, which weighs precision twice as much as
#               recall: sending someone to a wrong restaurant wastes a trip, while
#               missing one only leaves them with fewer options.
# Both empty counts as a perfect 1.0. A query that fails, or no query at all, returns
# no rows. Alongside the score, the script counts "wasted trips" (wrong restaurants
# returned) and "missed places" (right restaurants left out).
#
# Usage: python3 diner_score.py

import csv
import importlib.util
import json
import sqlite3
import statistics
from collections import Counter
from pathlib import Path


TASK2_DIR = Path(__file__).resolve().parent.parent / "Task_2"
LABELS_PATH = TASK2_DIR / "data" / "restaurants_dataset.csv"
EVALUATOR_PATH = TASK2_DIR / "data" / "evaluate_retrieval_predictions.py"
PREDICTIONS_DIR = TASK2_DIR / "predictions"
PROMPT_IDS = ["P1_CO_STAR", "P2_CHAIN_OF_THOUGHT", "P3_FEW_SHOT"]
BETA = 0.5


def diner_score(predicted_rows, expected_rows, beta=BETA):
    """Return (score, wasted_trips, missed_places) for one question."""
    predicted = Counter(tuple(row) for row in predicted_rows)
    expected = Counter(tuple(row) for row in expected_rows)
    overlap = sum((predicted & expected).values())
    wasted = sum(predicted.values()) - overlap
    missed = sum(expected.values()) - overlap
    if not predicted and not expected:
        return 1.0, 0, 0
    if overlap == 0:
        return 0.0, wasted, missed
    precision = overlap / sum(predicted.values())
    recall = overlap / sum(expected.values())
    score = (1 + beta**2) * precision * recall / (beta**2 * precision + recall)
    return score, wasted, missed


def load_database():
    spec = importlib.util.spec_from_file_location("official_evaluator", EVALUATOR_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.load_database()


def run_query(connection, sql):
    if not sql:
        return []
    try:
        return connection.execute(sql).fetchall()
    except sqlite3.Error:
        return []


def main():
    csv.field_size_limit(1_000_000_000)
    with LABELS_PATH.open(encoding="utf-8", newline="") as source:
        labels = [(row["question"], json.loads(row["result"])) for row in csv.DictReader(source)]

    connection = load_database()
    print(f"Diner Score (F{BETA} over returned restaurants), {len(labels)} questions\n")
    print(f"{'prompt':<22}{'exact match':>12}{'diner score':>13}{'on misses':>11}"
          f"{'wasted trips':>14}{'missed places':>15}")

    details = []
    for prompt_id in PROMPT_IDS:
        with (PREDICTIONS_DIR / f"{prompt_id}_predictions.csv").open(encoding="utf-8", newline="") as source:
            predictions = {int(row["row"]): row for row in csv.DictReader(source)}

        scores, exact, miss_scores, wasted_total, missed_total = [], 0, [], 0, 0
        for index, (question, expected) in enumerate(labels):
            sql = predictions[index]["predicted_sql"] if index in predictions else ""
            rows = run_query(connection, sql)
            score, wasted, missed = diner_score(rows, expected)
            is_exact = Counter(map(tuple, rows)) == Counter(map(tuple, expected))
            scores.append(score)
            exact += is_exact
            wasted_total += wasted
            missed_total += missed
            if not is_exact:
                miss_scores.append(score)
                details.append((prompt_id, index, score, wasted, missed, question))

        print(f"{prompt_id:<22}{exact / len(labels):>12.2%}{statistics.mean(scores):>13.4f}"
              f"{statistics.mean(miss_scores) if miss_scores else 1:>11.3f}"
              f"{wasted_total:>14}{missed_total:>15}")

    connection.close()
    print("\nQuestions that are not an exact match:")
    print(f"{'prompt':<22}{'row':>4}{'score':>8}{'wasted':>8}{'missed':>8}  question")
    for prompt_id, index, score, wasted, missed, question in details:
        print(f"{prompt_id:<22}{index:>4}{score:>8.3f}{wasted:>8}{missed:>8}  {question[:90]}")


if __name__ == "__main__":
    main()
