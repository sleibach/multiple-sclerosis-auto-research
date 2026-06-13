# Returned-Package Status-Board Schema Linter V46

Status: operator infrastructure. No validation result and no biological claim.

## Purpose

`scripts/v46_returned_package_status_board_schema_linter.py` verifies that the
first-30 returned-package status-board TSV and Markdown outputs remain parseable
for team updates. It checks required columns, scenario coverage, status
vocabulary, Markdown table shape, TSV/Markdown consistency, pre-result wording,
and `score_values_read=false`.

The linter does not open returned score tables, expression matrices, labels, or
quarantined cohorts.

## Command

```bash
.venv/bin/python scripts/v46_returned_package_status_board_schema_linter.py \
  --outdir analysis/v46_returned_package_status_board_schema_linter \
  --fail-on-error
```

## Current Result

- live checks: `91`
- live failures: `0`
- synthetic fixture cases: `4`
- fixture expectation failures: `0`
- all `score_values_read`: `false`
- overall status: `PASS`

Machine-readable outputs:

- `analysis/v46_returned_package_status_board_schema_linter/status_board_schema_linter_summary.json`
- `analysis/v46_returned_package_status_board_schema_linter/status_board_schema_lint.tsv`
- `analysis/v46_returned_package_status_board_schema_linter/status_board_schema_fixture_results.tsv`
- `analysis/v46_returned_package_status_board_schema_linter/RETURNED_PACKAGE_STATUS_BOARD_SCHEMA_LINTER.md`

## Boundary

A `PASS` means the operator-facing status-board TSV and Markdown are structurally
parseable and pre-result safe. It does not mean a package is scoreable, terms
permit processing, or any validation result can be interpreted.
