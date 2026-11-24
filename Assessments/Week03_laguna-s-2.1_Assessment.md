# Assessment by laguna-s-2.1

# Week 03 Prompting
- Awarded: 5b out of 5b
- Commentary: This is a strong, internally consistent submission across all four tasks. The three prompts (CO-STAR, Chain-of-Thought, Few-shot) are well-crafted for the text-to-SQL problem and each is justified by source and expected behaviour. Task 2 runs all 155 questions per prompt with measured inference times and a real SVG chart, Task 3 introduces an original F0.5 "Diner Score" with clean implementation, and Task 4 wraps it in proper paired statistics (Wilson CIs, Cochran's Q, exact McNemar, Wilcoxon, bootstrap) while explaining the model, prompt and coding-agent factors. Code is reproducible, reports are clear, and the statistical conclusion (accuracy flat and non-significant; speed a real difference) is well argued.

## Task 1
- Awarded: 1b   (max 1b)
- Commentary: Three frameworks chosen from frompting.com (CO-STAR, Chain of Thought, Few-shot), excluding ROSES and zero-shot as instructed. The three prompt files under Task_1/prompts/ are properly formulated for the restaurants text-to-SQL task (same schema, single `<sql>` line output). The report explains the source/URL of each framework, why it was picked, and what each is expected to deliver. Output is complete: prompt data files plus a justification report.

## Task 2
- Awarded: 1b   (max 1b)
- Commentary: run_predictions.py executes all 155 questions through each prompt with a fresh `claude -p` session, stores predictions with metadata (model, framework, inference_ms, wall_ms, tokens, cost), and evaluate_predictions.py computes exact accuracy and emits summary.csv, per_question.csv, failures.csv, accuracy_by_category.csv and comparison.svg. Inference times are measured (median/p90 and per-call). The report compares accuracy, median time, output tokens and cost for all three prompts. The SVG is an inline text chart with three panels (accuracy, inference time with p90 whisker, accuracy by question type), which is readable directly.

## Task 3
- Awarded: 1b   (max 1b)
- Commentary: Original "Diner Score" = F0.5 over returned restaurants, weighting precision twice as much as recall (a wrong recommendation wastes a trip, a missing one just loses an option). The report argues why it is applicable and states it complements rather than replaces exact match. diner_score.py implements it on the Task 2 predictions and prints per-prompt tables, and the report shows a comparison table (92.9%/0.966, 91.0%/0.948, 92.3%/0.961) with discussion of where the misses differ.

## Task 4
- Awarded: 2b   (max 2b)
- Commentary: significance.py computes Wilson 95% CIs, Cochran's Q, exact McNemar per pair, Wilcoxon signed-rank, and a paired bootstrap 95% interval for the Diner Score, all on the same 155 questions. The report presents tables (per-prompt correct/accuracy/CI/Diner/median time/IQR/tokens, a pairwise table with McNemar p, bootstrap 95%, Wilcoxon p, and a time-difference Wilcoxon p) plus two Mermaid charts. It concludes accuracy differences are not significant (only 4 discordant pairs; McNemar underpowered; Cochran Q p=0.17) while the speed difference is overwhelmingly significant (CoT slower on all 155 questions). The explanation correctly accounts for prompt factors (CoT emits ~1000 tokens of analysis and "tidies" values like `ave.`->`ave`), model factors (Sonnet 5.5 handles the simple schema well; 11 shared fails are reference/model issues), and coding-agent factors (Claude Code wrote all three prompts in one style and added ~7s startup excluded from timings).
