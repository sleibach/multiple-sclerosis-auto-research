# RAG Status

Last updated: 2026-07-10 15:05 CEST

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
- Current document count after V52 package refresh: `798`.
- V52 therapeutic smoke test query
  `V52 therapeutic path monitoring chr1 OpenGWAS` returned V52-relevant
  artifacts in the prior V52 refresh, including:
  1. `docs/reports/THERAPEUTIC_ROUTE_RISK_REGISTER_V52.md`;
  2. `docs/reports/THERAPEUTIC_CLAIM_HIERARCHY_V52.md`;
  3. `meta/V52_QUEUE.md`;
  4. `docs/reports/THERAPEUTIC_PATH_V52.md`;
  5. `docs/workups/genetics/OPENGWAS_PRE_EXPIRY_BOUNDED_POLISH_COMMANDS_V52.md`.
- V52 package-layer smoke test query
  `V52 package route classifier handoff bundle data owner README` returned
  package-handoff artifacts, including:
  1. `docs/validation/THERAPEUTIC_PACKAGE_HANDOFF_LINK_AUDIT_V52.md`;
  2. `docs/validation/THERAPEUTIC_PACKAGE_HANDOFF_BUNDLE_INDEX_V52.md`;
  3. `docs/validation/DATA_OWNER_PACKAGE_README_V52.md`;
  4. `meta/V52_QUEUE.md`;
  5. `docs/validation/VALIDATION_PACKAGE_ROUTE_CLASSIFIER_SCHEMA_CHECK_V52.md`.

This is not a semantic embedding index. It is a continuity aid until the proper
vector stack is installed.

## Upgrade Criteria

Install a vector stack only when:

- dependency installation is permitted,
- model weights can be documented,
- indexing is fast enough for routine use,
- and the sparse fallback proves insufficient.
