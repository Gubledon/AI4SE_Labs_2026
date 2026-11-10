# Task 2: Chunking the repository

`chunk_repo.py` uses Python's `ast` module and makes one chunk per function or method. The tasks in Task 5 are all "implement this method", so a whole method is the natural unit to retrieve. Fixed line windows would cut methods in half. Class attributes and docstrings go into a separate class chunk, and imports and constants into one module chunk per file. Every chunk starts with a `# file:` / `# class:` header, so a short method like `__len__` still says where it belongs.

The chunk size follows from the code itself rather than a fixed number: 729 chunks, 6.6 lines on average, 57 at most. Small chunks keep the top 5 in Task 5 focused. I included the tests (marked `"role": "test"`) because they show how each method is called and what it should return.

Chunks are stored in `chunks.json` as a list of objects with file, class, name, line range and text.
