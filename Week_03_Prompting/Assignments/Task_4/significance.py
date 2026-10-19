# Statistical comparison of the three prompts from Task 2, using exact match (Task 2)
# and the Diner Score (Task 3). All tests are paired: the same 155 questions were
# answered by every prompt.
#   - Wilson 95 % confidence interval for each prompt's accuracy
#   - Cochran's Q over all three prompts (exact match)
#   - exact McNemar test for each pair of prompts (exact match)
#   - Wilcoxon signed-rank test for each pair (Diner Score, inference time, output tokens)
#   - paired bootstrap 95 % interval for the Diner Score difference
# Only standard library; prints results, writes no files.
#
# Usage: python3 significance.py

import csv
import importlib.util
import itertools
import json
import math
import random
import statistics
from pathlib import Path


ASSIGNMENTS = Path(__file__).resolve().parent.parent
LABELS_PATH = ASSIGNMENTS / "Task_2" / "data" / "restaurants_dataset.csv"
PREDICTIONS_DIR = ASSIGNMENTS / "Task_2" / "predictions"
DINER_PATH = ASSIGNMENTS / "Task_3" / "diner_score.py"
PROMPT_IDS = ["P1_CO_STAR", "P2_CHAIN_OF_THOUGHT", "P3_FEW_SHOT"]
SHORT = {"P1_CO_STAR": "P1", "P2_CHAIN_OF_THOUGHT": "P2", "P3_FEW_SHOT": "P3"}


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def wilson(successes, n, z=1.96):
    p = successes / n
    centre = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return centre - half, centre + half


def binomial_two_sided(k, n):
    """Exact two-sided sign/McNemar p-value for k of n discordant pairs."""
    if n == 0:
        return 1.0
    tail = sum(math.comb(n, i) for i in range(0, min(k, n - k) + 1)) / 2**n
    return min(1.0, 2 * tail)


def cochran_q(matrix):
    """matrix: rows = questions, columns = prompts, values 0/1."""
    k = len(matrix[0])
    columns = [sum(row[j] for row in matrix) for j in range(k)]
    rows = [sum(row) for row in matrix]
    total = sum(rows)
    denominator = k * total - sum(r * r for r in rows)
    if denominator == 0:
        return 0.0, 1.0
    q = (k - 1) * (k * sum(c * c for c in columns) - total * total) / denominator
    return q, math.exp(-q / 2)  # chi-square survival function, df = 2


def ranks(values):
    order = sorted(range(len(values)), key=lambda i: values[i])
    result = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        for position in range(i, j + 1):
            result[order[position]] = (i + j) / 2 + 1
        i = j + 1
    return result


def wilcoxon(first, second):
    """Two-sided Wilcoxon signed-rank test. Exact for up to 20 non-zero differences."""
    differences = [a - b for a, b in zip(first, second) if a != b]
    n = len(differences)
    if n == 0:
        return 0, 1.0
    rank_values = ranks([abs(d) for d in differences])
    w_plus = sum(r for r, d in zip(rank_values, differences) if d > 0)
    if n <= 20:
        observed = min(w_plus, sum(rank_values) - w_plus)
        extreme = 0
        for signs in itertools.product((0, 1), repeat=n):
            w = sum(r for r, s in zip(rank_values, signs) if s)
            extreme += min(w, sum(rank_values) - w) <= observed + 1e-9
        return n, extreme / 2**n
    mean = n * (n + 1) / 4
    variance = sum(r * r for r in rank_values) / 4
    z = (w_plus - mean) / math.sqrt(variance)
    return n, math.erfc(abs(z) / math.sqrt(2))


def bootstrap_difference(first, second, rounds=10_000, seed=0):
    rng = random.Random(seed)
    n = len(first)
    means = []
    for _ in range(rounds):
        sample = [rng.randrange(n) for _ in range(n)]
        means.append(sum(first[i] - second[i] for i in sample) / n)
    means.sort()
    return means[int(0.025 * rounds)], means[int(0.975 * rounds)]


def main():
    diner = load_module(DINER_PATH, "diner_score")
    csv.field_size_limit(1_000_000_000)
    with LABELS_PATH.open(encoding="utf-8", newline="") as source:
        labels = [json.loads(row["result"]) for row in csv.DictReader(source)]

    connection = diner.load_database()
    exact, scores, times, tokens = {}, {}, {}, {}
    for prompt_id in PROMPT_IDS:
        with (PREDICTIONS_DIR / f"{prompt_id}_predictions.csv").open(encoding="utf-8", newline="") as source:
            predictions = {int(row["row"]): row for row in csv.DictReader(source)}
        exact[prompt_id], scores[prompt_id], times[prompt_id], tokens[prompt_id] = [], [], [], []
        for index, expected in enumerate(labels):
            row = predictions[index]
            rows = diner.run_query(connection, row["predicted_sql"])
            score, _wasted, _missed = diner.diner_score(rows, expected)
            same = sorted(map(tuple, rows)) == sorted(map(tuple, expected))
            exact[prompt_id].append(int(same))
            scores[prompt_id].append(score)
            times[prompt_id].append(float(row["inference_ms"]) / 1000)
            tokens[prompt_id].append(float(row["output_tokens"]))
    connection.close()
    n = len(labels)

    print(f"Per prompt ({n} questions)")
    print(f"{'prompt':<4}{'correct':>8}{'accuracy':>10}{'95% CI':>18}{'diner':>8}"
          f"{'time med':>10}{'time IQR':>16}{'tokens med':>12}")
    for p in PROMPT_IDS:
        low, high = wilson(sum(exact[p]), n)
        quart = statistics.quantiles(times[p], n=4)
        print(f"{SHORT[p]:<4}{sum(exact[p]):>8}{sum(exact[p]) / n:>10.3f}"
              f"{f'[{low:.3f}, {high:.3f}]':>18}{statistics.mean(scores[p]):>8.3f}"
              f"{statistics.median(times[p]):>9.2f}s{f'{quart[0]:.2f}-{quart[2]:.2f}s':>16}"
              f"{statistics.median(tokens[p]):>12.0f}")

    matrix = [[exact[p][i] for p in PROMPT_IDS] for i in range(n)]
    q, p_value = cochran_q(matrix)
    print(f"\nCochran's Q (exact match, all three): Q = {q:.2f}, df = 2, p = {p_value:.3f}")
    always_wrong = sum(1 for row in matrix if sum(row) == 0)
    print(f"Questions wrong for all three prompts: {always_wrong}")

    print("\nPairwise tests (a vs b)")
    print(f"{'pair':<8}{'a only':>7}{'b only':>7}{'McNemar p':>11}"
          f"{'diner diff':>12}{'bootstrap 95%':>20}{'diner n':>9}{'diner p':>9}"
          f"{'time n':>8}{'time p':>11}{'a slower':>10}")
    for a, b in itertools.combinations(PROMPT_IDS, 2):
        a_only = sum(1 for x, y in zip(exact[a], exact[b]) if x and not y)
        b_only = sum(1 for x, y in zip(exact[a], exact[b]) if y and not x)
        mcnemar = binomial_two_sided(a_only, a_only + b_only)
        diff = statistics.mean(scores[a]) - statistics.mean(scores[b])
        low, high = bootstrap_difference(scores[a], scores[b])
        diner_n, diner_p = wilcoxon(scores[a], scores[b])
        time_n, time_p = wilcoxon(times[a], times[b])
        slower = sum(1 for x, y in zip(times[a], times[b]) if x > y)
        print(f"{SHORT[a] + '-' + SHORT[b]:<8}{a_only:>7}{b_only:>7}{mcnemar:>11.3f}"
              f"{diff:>12.4f}{f'[{low:.4f}, {high:.4f}]':>20}{diner_n:>9}{diner_p:>9.3f}"
              f"{time_n:>8}{time_p:>11.2e}{slower:>10}")

    smallest = math.ceil(math.log2(1 / 0.05)) + 1
    print(f"\nFor McNemar to reach p < 0.05, the discordant pairs must all go one way and number at least {smallest}.")


if __name__ == "__main__":
    main()
