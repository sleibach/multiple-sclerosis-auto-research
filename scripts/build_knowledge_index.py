#!/usr/bin/env python3
"""Build a lightweight local retrieval index over V4 knowledge files.

This is a sparse TF-IDF fallback because sentence-transformer/vector-store
packages are not installed in the current environment. It is intentionally
simple and reproducible.
"""

from __future__ import annotations

import json
import pickle
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "knowledge" / ".index"
OUT.mkdir(parents=True, exist_ok=True)

GLOBS = [
    "knowledge/**/*.md",
    "docs/**/*.md",
    "meta/*.md",
    "subagents/*.md",
    "phases/v3/subagents/*.md",
]


def collect_docs() -> list[dict]:
    docs: list[dict] = []
    for pat in GLOBS:
        for p in ROOT.glob(pat):
            if not p.is_file():
                continue
            try:
                text = p.read_text(errors="ignore")
            except Exception:
                continue
            if not text.strip():
                continue
            docs.append({"path": str(p.relative_to(ROOT)), "text": text})
    return docs


def main() -> None:
    docs = collect_docs()
    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        ngram_range=(1, 2),
        max_features=100_000,
        min_df=1,
    )
    matrix = vectorizer.fit_transform([d["text"] for d in docs]) if docs else None
    with (OUT / "tfidf_index.pkl").open("wb") as fh:
        pickle.dump({"vectorizer": vectorizer, "matrix": matrix, "docs": docs}, fh)
    (OUT / "manifest.json").write_text(
        json.dumps(
            {
                "index_type": "sklearn_tfidf_sparse_fallback",
                "document_count": len(docs),
                "globs": GLOBS,
                "note": "Fallback index until sentence-transformer/vector-store stack is installed.",
            },
            indent=2,
        )
        + "\n"
    )
    print(json.dumps({"document_count": len(docs), "out": str(OUT)}, indent=2))


if __name__ == "__main__":
    main()
