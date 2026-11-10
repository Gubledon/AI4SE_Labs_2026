"""Turn repository chunks into embeddings with TF-IDF + truncated SVD (LSA).

Run as a script to build the storage from ../Task_2/chunks.json:
    chunks.json     the chunks, in the same order as the matrix rows
    embeddings.npy  N x DIMS float32 matrix, rows L2-normalised
    model.npz       vocabulary, idf weights and SVD components

Import embed() to turn any new text (a chunk or a task description) into a
vector in the same space.
"""

import json
import keyword
import math
import re
from collections import Counter
from pathlib import Path

import numpy as np
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer

HERE = Path(__file__).resolve().parent
CHUNKS_IN = HERE.parent / "Task_2" / "chunks.json"
CHUNKS_OUT = HERE / "chunks.json"
EMBEDDINGS = HERE / "embeddings.npy"
MODEL = HERE / "model.npz"
DIMS = 256

# Words that appear in almost every chunk and say nothing about its topic.
STOP = set(keyword.kwlist) | {"self", "cls", "file", "class", "py", "playground", "none", "true", "false"}


def code_tokens(text):
    """Split code into lower-case words; identifiers are kept whole and split.

    "can_afford" -> ["can_afford", "can", "afford"]
    "OutOfStockError" -> ["outofstockerror", "out", "of", "stock", "error"]
    """
    tokens = []
    for ident in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", text):
        parts = [p for p in re.split(r"_|(?<=[a-z0-9])(?=[A-Z])", ident) if p]
        words = [p.lower() for p in parts]
        whole = ident.strip("_").lower()
        if len(words) > 1:
            words.append(whole)
        tokens.extend(w for w in words if len(w) > 1 and w not in STOP)
    return tokens


def _normalise(matrix):
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return matrix / norms


_model = None


def embed(texts):
    """Return an (len(texts) x DIMS) array of unit vectors for ``texts``."""
    global _model
    if _model is None:
        data = np.load(MODEL)
        vocab = {w: i for i, w in enumerate(data["vocabulary"])}
        _model = vocab, data["idf"], data["components"]
    vocab, idf, components = _model

    tfidf = np.zeros((len(texts), len(vocab)), dtype=np.float64)
    for row, text in enumerate(texts):
        for word, count in Counter(code_tokens(text)).items():
            if word in vocab:
                tfidf[row, vocab[word]] = (1 + math.log(count)) * idf[vocab[word]]
    tfidf = _normalise(tfidf)
    return _normalise(tfidf @ components.T).astype(np.float32)


def build():
    chunks = json.loads(CHUNKS_IN.read_text(encoding="utf-8"))
    texts = [c["text"] for c in chunks]

    vectorizer = TfidfVectorizer(tokenizer=code_tokens, lowercase=False,
                                 token_pattern=None, sublinear_tf=True)
    tfidf = vectorizer.fit_transform(texts)
    svd = TruncatedSVD(n_components=DIMS, random_state=0)
    vectors = _normalise(svd.fit_transform(tfidf)).astype(np.float32)

    np.savez(MODEL, vocabulary=vectorizer.get_feature_names_out().astype(str),
             idf=vectorizer.idf_, components=svd.components_)
    np.save(EMBEDDINGS, vectors)
    CHUNKS_OUT.write_text(json.dumps(chunks, indent=2), encoding="utf-8")

    # embed() must reproduce the build-time vectors, or queries land elsewhere.
    drift = np.abs(embed(texts) - vectors).max()
    print(f"{len(chunks)} chunks, vocabulary {tfidf.shape[1]} words -> {DIMS} dims")
    print(f"variance kept by SVD: {svd.explained_variance_ratio_.sum():.1%}")
    print(f"max difference embed() vs stored: {drift:.2e}")


if __name__ == "__main__":
    build()
