# External Markdown Index Linter V47

This linter checks generated external Markdown navigation files. It does not
validate external claims. It verifies a narrower display invariant: when a
generated Markdown table has a `source` column and a row carries an external
epistemic class or `NOT_PROJECT_GROUNDED` marker, the row must also contain a
source locator such as a URL, DOI, or PMID.

Aggregate count tables without a source column are ignored.

## Commands

```bash
.venv/bin/python scripts/v47_external_markdown_index_linter.py synthetic-check --outdir analysis/v47_external_markdown_index_linter --fail-on-error
.venv/bin/python scripts/v47_external_markdown_index_linter.py lint --outdir analysis/v47_external_markdown_index_linter --fail-on-error
```

The synthetic fixture verifies that a source-bearing row passes, an aggregate
count row is ignored, and a source-bearing external row without a source locator
fails.
