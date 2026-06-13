# Quickstart Command Coverage Matrix V46

Status: quickstart command-governance matrix. No validation result and no
biological claim.

## Purpose

`scripts/v46_quickstart_command_coverage_matrix.py` maps every generated
quickstart command row to README presence, regression/smoke script reachability,
and quickstart drift-fixture parity coverage.

## Command

```bash
.venv/bin/python scripts/v46_quickstart_command_coverage_matrix.py \
  --outdir analysis/v46_quickstart_command_coverage_matrix \
  --fail-on-error
```

## Current Result

- command rows: `34`
- lint failures: `0`
- all `score_values_read`: `false`
- overall status: `PASS`

## Outputs

- `analysis/v46_quickstart_command_coverage_matrix/quickstart_command_coverage_summary.json`
- `analysis/v46_quickstart_command_coverage_matrix/quickstart_command_coverage_matrix.tsv`
- `analysis/v46_quickstart_command_coverage_matrix/quickstart_command_coverage_lint.tsv`
- `analysis/v46_quickstart_command_coverage_matrix/QUICKSTART_COMMAND_COVERAGE_MATRIX.md`

## Boundary

This matrix checks operator-command coverage only. It does not run validation or
inspect returned data.
