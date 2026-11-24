# Assessment by mimo-2.6-flash

# Week 03 Prompting
- Awarded: 4.5b out of 5b
- Commentary: All four tasks are complete, reproducible and consistently above average, with a clean pipeline linking prompts (Task 1) to predictions (Task 2), a genuinely novel metric (Task 3) and a statistically rigorous comparison (Task 4). The work is held back only by Task 4 being somewhat compressed for a "detailed analysis" — the new metric is tabulated but not visualised, and per-category/distribution insights from Task 2 are not carried forward. Graphics (SVG and mermaid) could not be rendered in this review and were judged from their source code/text, which was sound and matched the reported numbers.

## Task 1
- Awarded: 1b   (max 1b)
- Commentary: Three frameworks (CO-STAR, Chain of Thought, Few-Shot) are taken from frompting.com with per-framework source URLs, honouring the exclusions of ROSES and zero-shot. The three prompt files are complete, mutually comparable (shared schema, shared `<sql>` contract, only the framework varies) and tailored to the Task 2 text-to-SQL problem. The report explains why each framework was chosen, where it was found, what was expected from it (including anticipated accuracy/speed trade-offs) and honestly notes the platform's own caveat that CoT suits machine-parsed output poorly.

## Task 2
- Awarded: 1b   (max 1b)
- Commentary: All 155 questions were run through each prompt with fresh, isolated `claude -p` sessions (stronger than the hint), and predictions CSVs carry full metadata (prompt_id, framework, model, tokens, cost, session id, raw response). Evaluation reuses the official row-multiset comparison; failure counts in the report (11/14/12) match failures.csv and summary.csv exactly. Inference times are measured and reported (mean/median/p90, token counts, cost), and the report contains a three-panel comparison chart (accuracy, time with p90 whiskers, accuracy by question type) plus a clear recommendation — a complete answer to the task.

## Task 3
- Awarded: 1b   (max 1b)
- Commentary: The invented "Diner Score" (F0.5 of multiset precision/recall, precision weighted 2×) is well motivated: it quantifies how useful a wrong answer remains, with a concrete justification (a wrong restaurant wastes a trip, a missing one only reduces options) and honest discussion of its limits and of the off-topic reference question. The report explicitly argues that it complements rather than replaces exact match. Implementation (diner_score.py) is correct (multiset overlap, both-empty = 1.0, failed queries score 0) and was run over the actual Task 2 predictions, producing the per-prompt comparison table (exact match vs Diner Score vs wasted trips).

## Task 4
- Awarded: 1.5b   (max 2b)
- Commentary: significance.py applies the right paired tests with only the standard library — Wilson CIs, Cochran's Q across all three prompts, exact McNemar per pair, Wilcoxon signed-rank and a paired bootstrap CI — and the conclusions are statistically correct (accuracy differences not significant; only four discordant questions; CoT slower on all 155 questions, p ≈ 3.5e-27). The report delivers tables, two mermaid bar charts (judged from text, not rendered), and an interpretation that explicitly covers the three requested factors: the prompt (CoT's ~1,000-token analysis causes both the delay and its extra `ave.`/`vietnamese` errors), the model (Sonnet 5.5 is insensitive to framework choice on this simple schema, with 11 shared failures implicating the references), and the coding agent (uniform prompt style, ~7 s CLI startup excluded). Deductions: for a "detailed" analysis the Diner Score only appears in a table with no graph or distribution/category-level exploration, the narrative is very brief, and its P1 Diner value (0.965) slightly disagrees with Task 3's (0.966).