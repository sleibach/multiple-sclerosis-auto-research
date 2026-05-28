#!/usr/bin/env python3
"""Query the local sparse V4 knowledge index."""

from __future__ import annotations

import pickle
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "knowledge" / ".index" / "tfidf_index.pkl"


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("usage: query_knowledge_index.py QUERY [k]")
    query = sys.argv[1]
    k = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    with INDEX.open("rb") as fh:
        idx = pickle.load(fh)
    q = idx["vectorizer"].transform([query])
    scores = (idx["matrix"] @ q.T).toarray().ravel()
    order = scores.argsort()[::-1][:k]
    for i in order:
        if scores[i] <= 0:
            continue
        print(f"{scores[i]:.4f}\t{idx['docs'][i]['path']}")


if __name__ == "__main__":
    main()
