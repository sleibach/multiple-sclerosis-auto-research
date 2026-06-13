# External Record Uniqueness Linter V47

This linter checks external records for duplicate `record_id` values and
duplicate source locators. It is governance only: it does not validate source
content and does not make biological or clinical claims.

Duplicate record IDs are hard failures. Duplicate source locators are also
failures because they usually indicate accidental copy/paste records or an
unclear split between two records.

## Commands

```bash
.venv/bin/python scripts/v47_external_record_uniqueness_linter.py synthetic-check --outdir analysis/v47_external_record_uniqueness_linter --fail-on-error
.venv/bin/python scripts/v47_external_record_uniqueness_linter.py lint --outdir analysis/v47_external_record_uniqueness_linter --fail-on-error
```

The synthetic fixture verifies that unique records pass, duplicate IDs fail,
and duplicate source URLs fail.
