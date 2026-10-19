# Task 3 Report: the Diner Score

Exact match gives 0 to any wrong answer, so 63 restaurants instead of 62 scores the same as an empty list. The Diner Score treats each answer as a list of places someone will actually drive to. It compares predicted and reference rows and takes F0.5 of precision and recall:

- precision = matching rows / predicted rows
- recall = matching rows / reference rows
- score = 1.25 · P · R / (0.25 · P + R), with 1 if both answers are empty

Precision counts double because a wrong restaurant is a wasted trip, while a missing one only means one fewer option. It complements exact match rather than replacing it. Exact match says whether the SQL is right, and the Diner Score says how useful a wrong answer still is.

| Prompt | Exact match | Diner Score | Score on misses | Wasted trips* |
|---|---|---|---|---|
| P1 CO-STAR | 92.9 % | 0.966 | 0.51 | 24 |
| P2 Chain of Thought | 91.0 % | 0.948 | 0.43 | 89 |
| P3 Few-Shot | 92.3 % | 0.961 | 0.50 | 24 |

\*Without the off-topic question, which has a 2,696-row reference.

The ranking doesn't change, but the misses look different. Chain of Thought's own errors are complete misses: `vietnamese/louisiana` alone sends the user to 65 wrong places. The errors all prompts share are mostly near-misses scoring 0.92 to 0.99, which suggests the reference answers use a slightly different rule.

The weak spot is that the metric is only as good as the reference. On the off-topic question, returning the whole database scores 0.33 and refusing scores 0.
