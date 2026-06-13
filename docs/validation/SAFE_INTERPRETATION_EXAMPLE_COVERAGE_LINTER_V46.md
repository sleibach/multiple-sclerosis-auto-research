# Safe-Interpretation Example Coverage Linter V46

Status: safe-class coverage governance. No validation result and no biological
claim.

## Purpose

`scripts/v46_safe_interpretation_example_coverage_linter.py` verifies that every
V46 safe class either has a safe-interpretation example card or an explicit
reason it is intentionally not represented by an example.

## Command

```bash
.venv/bin/python scripts/v46_safe_interpretation_example_coverage_linter.py \
  --outdir analysis/v46_safe_interpretation_example_coverage_linter \
  --fail-on-error
```

## Current Result

- safe classes: `12`
- represented by example: `6`
- explicit non-example reasons: `6`
- lint failures: `0`
- all `score_values_read`: `false`
- overall status: `PASS`

## Outputs

- `analysis/v46_safe_interpretation_example_coverage_linter/safe_interpretation_example_coverage_summary.json`
- `analysis/v46_safe_interpretation_example_coverage_linter/safe_interpretation_example_coverage.tsv`
- `analysis/v46_safe_interpretation_example_coverage_linter/safe_interpretation_example_coverage_lint.tsv`
- `analysis/v46_safe_interpretation_example_coverage_linter/SAFE_INTERPRETATION_EXAMPLE_COVERAGE.md`

## Boundary

This linter does not make blocked safe classes interpretable. It only prevents
the examples bundle from silently omitting a safe class without accounting for
the omission.
