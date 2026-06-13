# Safe-Interpretation Examples V46

Status: operator wording examples. No validation result and no biological
claim.

## Purpose

`scripts/v46_safe_interpretation_examples.py` generates example cards for
returned-package interpretation states by joining existing V46 readiness tables:

- safe-class report-template readiness;
- small-n conclusion language;
- analyzable-pair confidence envelope;
- partial-label repair prioritization.

The examples show what an operator may say for aggregate-only, partial-label,
underpowered, diagnostic-caution, and preferred-decision scenarios without
reading returned score values or altering locked rules.

## Command

```bash
.venv/bin/python scripts/v46_safe_interpretation_examples.py \
  --outdir analysis/v46_safe_interpretation_examples \
  --fail-on-error
```

## Current Result

- examples: `7`
- lint checks: `56`
- lint failures: `0`
- all `score_values_read`: `false`
- overall status: `PASS`

## Outputs

- `analysis/v46_safe_interpretation_examples/safe_interpretation_examples_summary.json`
- `analysis/v46_safe_interpretation_examples/safe_interpretation_examples.tsv`
- `analysis/v46_safe_interpretation_examples/safe_interpretation_examples_lint.tsv`
- `analysis/v46_safe_interpretation_examples/SAFE_INTERPRETATION_EXAMPLES.md`
- per-example cards under `analysis/v46_safe_interpretation_examples/cards/`

## Boundary

These are wording examples only. They do not run validation, read returned
score-bearing files, inspect labels or expression matrices, or authorize any
post-hoc change to the V42/V22 validation plan.
