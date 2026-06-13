# External Knowledge Index V47

Status: navigation infrastructure only. No biological claim and no
project-grounded finding is made here.

Script:

`scripts/v47_external_knowledge_index.py`

Purpose: generate class-aware indexes over records stored in
`knowledge_external/records/` and `knowledge_external/catalogs/resources/`.
The index preserves epistemic class, source, access date, relationship tags,
and the not-grounded marker. It does not validate external claims, does not
move them into grounded trees, and does not change any locked rule or
pre-registration.

## Commands

Synthetic aggregation fixture:

```bash
.venv/bin/python scripts/v47_external_knowledge_index.py synthetic-check \
  --outdir analysis/v47_external_knowledge_index \
  --fail-on-error
```

Real external index:

```bash
.venv/bin/python scripts/v47_external_knowledge_index.py index \
  --outdir knowledge_external/catalogs/indexes
```

Provenance gate:

```bash
.venv/bin/python scripts/v47_provenance_gate.py audit \
  --outdir analysis/v47_provenance_gate \
  --fail-on-error
```

## Outputs

Real index outputs remain inside `knowledge_external/`:

- `knowledge_external/catalogs/indexes/external_knowledge_index.tsv`
- `knowledge_external/catalogs/indexes/external_knowledge_index_counts.tsv`
- `knowledge_external/catalogs/indexes/EXTERNAL_KNOWLEDGE_INDEX.md`

Synthetic fixture outputs remain under `analysis/v47_external_knowledge_index/`
and are allowlisted only as software-governance artifacts. They are not
biological evidence.

