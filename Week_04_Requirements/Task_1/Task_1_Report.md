# Task 1 Report: Requirements Refinement Network

The network is `requirements_network.py`. It takes only an input folder (`python3 requirements_network.py data/corpus`) and writes `requirements.md`.

```
load (code) -> extract (LLM) -> merge (LLM) -> check_coverage (code) -> write (LLM) -> review (LLM) -> render (code)
                                  ^                  |                                     |
                                  +-- unplaced ------+                                     |
                                  +----------------- review found issues ------------------+
```

| Node | Kind | Model | Job |
|---|---|---|---|
| load | code | none | reads every text file in the folder, splits long ones into ~8000-character chunks |
| extract | LLM | gpt-5-mini | lists every requirement-like statement per chunk, with status (decision, proposal, existing feature, background) and date |
| merge | LLM | gpt-6-luna | merges duplicates into one requirement per feature, resolves conflicts, writes the blacklist |
| check_coverage | code | none | every candidate must sit in a requirement or in the blacklist; missing ones go back to merge |
| write | LLM | gpt-5.4-nano | name, paragraph and priority for each requirement |
| review | LLM | gpt-5.6-luna | checks the written document; issues go back to merge and write |
| render | code | none | IDs, sources, priority scale, blacklist |

I gave each step the model that fits its load. Extraction runs 26 times, so it uses a cheap model. Merge is one large reasoning call over all candidates, so it gets the strongest one. The reviewer is a different model from the one it checks.

Tracing is done in code. Extraction attaches the file name to each candidate, merge returns only candidate IDs, and render looks up the files from those IDs. The model cannot invent a source. When review finds problems, merge returns a list of edits (assign, combine, update, discard, restore) and code applies them. Merge never rewrites the whole set.

Conflicts are settled by authority: a decision beats a proposal, and a later date beats an earlier one. Statements about the existing system (94 of 908) go to merge and review as facts, not candidates. A request that the facts contradict is discarded. The High priority rule (a decision or at least three source documents) is applied in code after write. The model only picks between Medium and Low.

The final run produced 150 requirements (130 functional, 11 non-functional, 9 constraints) and 27 discarded items. Review issues fell from 22 to 15, 7, 6, 2 and 2 over six rounds. The last two were not fixed because the loop allows five revisions. One nonsensical detail got through: the in-transit report in FR-008 is "sortable by due date", but transits have no due date. One global merge handles about 40k tokens of candidates here, but it would not scale to a much larger corpus.

| Spec | Where it is handled |
|---|---|
| ANS1 | extract, merge, write, review |
| ANS2 | load, check_coverage, render |
| ANS3 | check_coverage -> merge, review -> merge/write |
| ANS4 | gpt-5-mini, gpt-6-luna, gpt-5.4-nano, gpt-5.6-luna |
| ANS5 | LangGraph `StateGraph` with conditional edges |
| OS1 | render writes one Markdown file |
| OS2 | render assigns FR-/NFR-/CON-/DR- numbers |
| OS3 | merge prompt, review rules 1 and 9 |
| OS4 | candidate IDs to source files, computed in code |
| OS5 | write prompt (name of at most 8 words, one paragraph) |
| OS6 | `PRIORITY_SCALE` printed in the document, High rule in code |
| OS7 | merge and write prompts (one term per concept), review rules 2, 3 and 10 |
| OS8 | check_coverage loop, "Unplaced candidates" section as fallback |
| OS9 | merge discards with reasons, review rules 6 to 8, blacklist section |
