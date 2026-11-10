# Task 5: Unit test results

`rag_solve.py` ran all 10 tasks with gpt-6-luna. The prompt held only the task text and the top 5 chunks (at most 2 of them tests), with a system prompt that tells the model to use only names that appear in the chunks. Every reply parsed on the first attempt and was written over its stub.

| Run | Passed | Failed |
|---|---|---|
| Before (stubs) | 429 | 52 |
| After RAG | 463 | 18 |

Five of the ten methods pass all their tests. The 18 failures come from five methods:

- `BulkDiscountPricing.price` (8 failures): it uses the right attributes, but divides `Money` by an int, which `Money` doesn't support. No chunk showed how `Money` does arithmetic.
- `OrderStateMachine.transition` (5): it raises `ValueError`, but the tests expect `InvalidTransitionError`. That exception wasn't among the chunks.
- `InventoryLedger.__contains__` (3): it raises on a non-string or malformed SKU instead of returning False, and it reports a SKU with zero on-hand stock as missing. Here the task description says "positive on-hand stock", while the tests count a zero stock SKU as present.
- `OrderLog.by_status` (1): it doesn't reject a non-`OrderStatus` argument. The test that expects the `TypeError` wasn't one of the two retrieved tests.
- `EventBus.__contains__` (1): it raises on a non-`EventType` argument instead of returning False.

Most failures trace back to something missing from the five chunks, so the retrieval limits the result more than the model does. The LLM also varies between runs: an earlier run of this exact setup had 17 failures, because `EventBus.__contains__` passed that time.
