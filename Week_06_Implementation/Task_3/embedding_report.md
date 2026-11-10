# Task 3: Embeddings and storage

I embed chunks locally with TF-IDF followed by truncated SVD (LSA), using scikit-learn. Code search mostly comes down to shared names. A task like "Order.__len__: Return the number of line items" shares `order`, `len`, `line` and `items` with the code it needs, so word overlap goes a long way. The tokenizer splits identifiers (`can_afford` becomes `can`, `afford` and `can_afford`) and drops Python keywords and `self`. SVD compresses the 1461-word vocabulary into 256 dimensions and keeps 88% of the variance. It also groups words that tend to appear together, so related code can match even when the exact word differs.

I embed the full chunk text, header included, so the file and class names count as well.

Storage is `embeddings.npy` (729 × 256, unit-length rows), with row i matching entry i in `chunks.json`. `model.npz` holds the vocabulary, idf weights and SVD components, so `embed()` puts a new query in the same space. Because the rows are unit length, cosine similarity is one matrix product. That is exact and instant at 729 rows, so I didn't need a vector database.
