# Quickstart Drift Fixture V46

Status: synthetic documentation-regression infrastructure. No validation result
and no biological claim.

## Purpose

`scripts/v46_quickstart_drift_fixture.py` copies the generated returned-package
quickstart into synthetic fixtures and proves that command edits in the copied
Markdown are detected against the machine-readable quickstart command table.

The fixture exists because the quickstart is useful only if operator-facing
commands remain exact derivatives of the source tables.

## Command

```bash
.venv/bin/python scripts/v46_quickstart_drift_fixture.py \
  --outdir analysis/v46_quickstart_drift_fixture \
  --fail-on-error
```

## Current Result

- cases: `4`
- expected fail cases: `3`
- expectation failures: `0`
- command rows checked: `34`
- all `score_values_read`: `false`
- overall status: `PASS`

## Outputs

- `analysis/v46_quickstart_drift_fixture/quickstart_drift_summary.json`
- `analysis/v46_quickstart_drift_fixture/quickstart_drift_cases.tsv`
- `analysis/v46_quickstart_drift_fixture/quickstart_drift_lint.tsv`
- `analysis/v46_quickstart_drift_fixture/QUICKSTART_DRIFT_FIXTURE.md`
- synthetic mutated Markdown fixtures under `analysis/v46_quickstart_drift_fixture/fixtures/`

## Boundary

These fixtures mutate copied Markdown only. They do not read returned score
tables, labels, expression matrices, or quarantined cohorts, and they do not
change the generated quickstart source tables.
