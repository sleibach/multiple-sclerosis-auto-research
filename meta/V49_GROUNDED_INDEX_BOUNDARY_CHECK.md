# V49 Grounded Index Boundary Check

Status: operational check. This document records whether V49 external-knowledge
artifacts entered the grounded TF-IDF/RAG index.

## Check

Current index manifest:

- path: `knowledge/.index/manifest.json`
- document count: `728`
- configured globs:
  - `knowledge/**/*.md`
  - `docs/**/*.md`
  - `meta/*.md`
  - `subagents/*.md`
  - `phases/v3/subagents/*.md`

Inspection command used `.venv_v3_py312/bin/python` because system Python and
`.venv/bin/python` lacked scikit-learn needed to unpickle the TF-IDF object.

## Result

- indexed `knowledge_external/` paths: `0`
- indexed V49 paths: `meta/V49_QUEUE.md`
- accidental V49 external-content indexing: `no`

`meta/V49_QUEUE.md` is operational resume state included by the existing
`meta/*.md` glob. The V49 external synthesis/catalog artifacts are under
`knowledge_external/` and remain structurally excluded by the index script.

## Decision

No RAG rebuild is required for V49 external content. Rebuilding now would index
additional operational `meta/V49_*.md` files but would still exclude
`knowledge_external/`. Future rebuilds should continue to treat
`knowledge_external/` as outside grounded evidence retrieval unless the project
intentionally builds a separate class-aware external index.

## Late V49 Recheck

Rechecked at `2026-06-14T21:46:55Z` after later V49 meta/navigation additions.
The TF-IDF object still contains `728` docs, `0` indexed `knowledge_external/`
paths, and only `meta/V49_QUEUE.md` among indexed V49 paths. Raw string scans of
the pickle can find the text `knowledge_external` because indexed meta documents
discuss the external boundary; the path-level check is the relevant guard.

Decision unchanged: do not rebuild the grounded index for V49 external content.
If a future session rebuilds the grounded index, it should separately verify
that indexed paths still exclude `knowledge_external/`.
