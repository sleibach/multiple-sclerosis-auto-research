# External Record Schema Linter V47

Status: dependency-free external-record governance. No biological claim.

Script:

`scripts/v47_external_record_schema_linter.py`

Purpose: lint records under `knowledge_external/records/` and
`knowledge_external/catalogs/resources/` without relying on an optional
`jsonschema` installation. The linter checks required fields, source presence,
epistemic class, relationship tags, access-tier values for resource records,
and the not-grounded marker.

## Commands

Synthetic fixtures:

```bash
.venv/bin/python scripts/v47_external_record_schema_linter.py synthetic-check \
  --outdir analysis/v47_external_record_schema_linter \
  --fail-on-error
```

Real external records:

```bash
.venv/bin/python scripts/v47_external_record_schema_linter.py lint \
  --outdir analysis/v47_external_record_schema_linter \
  --fail-on-error
```

The linter is stricter than navigation: a record can appear in the index only if
the provenance gate and this linter are both pass-clean.

