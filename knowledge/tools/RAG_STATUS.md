# RAG Status

Last updated: 2026-06-12 16:45 CEST

## Desired V4 Layer 2

Preferred stack:
- sentence-transformer embeddings,
- Chroma, LanceDB, or sqlite-vec vector store.

## Current Feasibility Probe

Checked in `.venv_v3_py312`:

- `chromadb`: not installed.
- `lancedb`: not installed.
- `sqlite_vec`: not installed.
- `sentence_transformers`: not installed.
- `sklearn`: installed.

## Provisioned Fallback

Sparse local retrieval:

- Build: `./.venv_v3_py312/bin/python scripts/build_knowledge_index.py`
- Query: `./.venv_v3_py312/bin/python scripts/query_knowledge_index.py "candidate prior art" 10`
- Index path: `knowledge/.index/tfidf_index.pkl`
- Current document count: `538`.
- Smoke test query `V43 power map robustness synthetic null Gafson`
  returned:
  1. `meta/V43_QUEUE.md`;
  2. `docs/history/PIPELINE_SELF_AUDIT_V43.md`;
  3. `docs/validation/POWER_MAP_V43.md`;
  4. `meta/V42_QUEUE.md`;
  5. `meta/CURRENT_STATUS.md`.

This is not a semantic embedding index. It is a continuity aid until the proper
vector stack is installed.

## Upgrade Criteria

Install a vector stack only when:

- dependency installation is permitted,
- model weights can be documented,
- indexing is fast enough for routine use,
- and the sparse fallback proves insufficient.
