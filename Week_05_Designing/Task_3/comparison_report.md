# Comparison: Tasks 1 and 2 on CDC without and with the skill

| | Without skill | With skill |
|---|---|---|
| My turns in the notes (Task 1 / Task 2) | 22 / 6 | 21 / 6 |
| Process corrections | 6 | 0 |
| Questions asked in Task 1 | 18 | 19 |
| Question rounds (Task 1 / Task 2) | not visible in the notes | 8 / 3 |
| ADR drafts until I was satisfied | 4 | 3 |
| Quizzes answered correctly | 1 of 3 | 3 of 3 |

The process corrections disappeared. In the first run I corrected the notes format three times, objected that architecture 2 came with its choices already made, asked for a more thorough discussion, and got the table and diagram only after asking in draft 2. With the skill, the notes had the right format from the first line, each architecture was an outline, one question round and a quiz, and draft 1 already had the table and the Mermaid diagram. The rerun took 26 minutes for Task 1 and 24 for Task 2. The first run has no recorded times, so I can't say if it was faster.

Both ADRs choose the monolith and share the payment rules: raw-body signature check, unique event ID, provider call after commit, double-click guard, price snapshots, the 24 h expiry and flagged late payments. This time I chose stock and the carrier API instead of no stock and manual status. The new ADR also decides sessions but drops module boundary enforcement. Both caught the provider call under the cart lock; the new one also made "unchanged cart" compare prices.

This rerun prompt restated the process rules from the earlier session, so the comparison measures the skill plus this prompt. Also, `pitfalls.md` carries conclusions from the first run, I took the recommended option in all 20 design questions, and I had seen these scenarios before. Part of the gain is that this was my second time.
