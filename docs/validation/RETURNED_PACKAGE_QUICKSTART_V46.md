# Returned-Package Quickstart V46

Status: generated operator navigation. No validation result and no biological
claim.

## Purpose

`scripts/v46_returned_package_quickstart_readme.py` generates a compact
operator README from the machine-readable returned-package handoff manifest and
the receipt-manifest-to-command-plan handoff. The goal is drift prevention:
operator instructions should come from runnable commands and recorded stop
conditions, not from manually maintained prose.

## Command

```bash
.venv/bin/python scripts/v46_returned_package_quickstart_readme.py \
  --outdir analysis/v46_returned_package_quickstart_readme \
  --fail-on-error
```

## Current Result

The committed run passed:

- handoff commands: `26`
- receipt branch examples: `8`
- total command rows: `34`
- regression-suite steps observed: `36`
- smoke-bundle steps observed: `40`
- lint checks: `13`
- lint failures: `0`
- all `score_values_read`: `false`
- overall status: `PASS`

## Outputs

- `analysis/v46_returned_package_quickstart_readme/returned_package_quickstart_summary.json`
- `analysis/v46_returned_package_quickstart_readme/returned_package_quickstart_commands.tsv`
- `analysis/v46_returned_package_quickstart_readme/returned_package_quickstart_lint.tsv`
- `analysis/v46_returned_package_quickstart_readme/RETURNED_PACKAGE_QUICKSTART.md`

## Boundary

This artifact is operator navigation only. It does not open returned score
tables, expression matrices, labels, or quarantined cohorts. It does not
authorize result wording; the V46 safe class, report-header linter, and frozen
V42 pre-registration remain the interpretation boundary.
