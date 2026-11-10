# Task 5: Unit test results

`rag_solve.py` ran all 10 tasks with gpt-6-luna. The prompt held only the task text and the top 5 chunks. Every reply parsed on the first attempt and was written over its stub.

| Run | Passed | Failed |
|---|---|---|
| Before (stubs) | 429 | 52 |
| After RAG | 463 | 18 |

Seven of the ten methods pass all their tests. The 18 failures come from three methods:

- `BulkDiscountPricing.price` (10 failures): all five retrieved chunks were tests, so the model never saw `__init__` and invented `self.base`, `self.min_quantity` and `self.discount_percent`, which don't exist (`_base`, `_threshold`, `_percent_off` do).
- `OrderStateMachine.transition` (5): it raises `ValueError`, but the tests expect `InvalidTransitionError`. That exception wasn't among the chunks.
- `InventoryLedger.__contains__` (3): it raises on a non-string or malformed SKU instead of returning False, and it reports a SKU with zero on-hand stock as missing, which the tests don't accept.

For the first two, the code that would have helped wasn't among the five retrieved chunks. So I think better retrieval would fix more than a stronger model would. The third one also comes down to the task description: it says "positive on-hand stock", while the tests count a SKU with zero on-hand stock as present.
