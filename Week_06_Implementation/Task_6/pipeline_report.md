# Task 6: A better pipeline

For "implement method X in class Y", embedding matching alone isn't the best strategy. The most useful context is fixed by the code structure: the class's `__init__` and attributes, the file's imports, and whatever those imports define. My two worst failures in Task 5 came from missing exactly that: how `Money` does arithmetic, and `InvalidTransitionError`.

The pipeline I would build:

1. Structural context from the AST: the target file with the stub, plus the definitions of every name it imports.
2. Tests found by searching for the method name, since they act as the spec.
3. Embedding or BM25 search only to fill the remaining space with similar code.
4. Generate, run the related tests, and send failures back to the model for up to 3 rounds.

The number of chunks should follow a token budget, not a fixed 5. Five chunks of about 7 lines is far too little. This package has only 13 small modules, so for a repo this small I would skip retrieval and put all the source code in the prompt. The AST chunking itself is fine. Each method chunk should just carry its class skeleton.
