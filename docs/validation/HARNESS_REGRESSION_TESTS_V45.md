# Harness Regression Tests V45

Status: infrastructure regression. Synthetic data only; no biological evidence.

## Purpose

V45 now has multiple validation/context harnesses. This regression checkpoint
adds a single command that verifies the guardrail behavior most likely to be
broken by future edits:

- secondary postpartum APC-arm synthetic null must not clean-pass;
- secondary postpartum APC-arm planted signal must clean-pass;
- secondary T/B compartment synthetic null must not clean-pass;
- secondary T/B compartment planted signal must clean-pass;
- pharmacodynamic-only harness must remain context-only and must not perform
  response validation.

## Command

```bash
.venv/bin/python scripts/v45_harness_regression_tests.py
```

The script runs:

```bash
.venv/bin/python scripts/v45_secondary_real_cohort_harness.py synthetic-check \
  --outdir analysis/v45_harness_regression_tests/secondary_real_ingest \
  --n-boot 120

.venv/bin/python scripts/v45_pharmacodynamic_only_harness.py synthetic-check \
  --outdir analysis/v45_harness_regression_tests/pharmacodynamic_only
```

It then reads the generated JSON outputs and fails if any invariant is broken.

## Result

Committed regression result:

- `analysis/v45_harness_regression_tests/regression_summary.json`

Summary:

| Check | Result |
|---|---|
| Postpartum null expected fail | pass |
| Postpartum planted expected pass | pass |
| T/B null expected fail | pass |
| T/B planted expected pass | pass |
| Pharmacodynamic context-only flag | pass |
| Pharmacodynamic response-validation flag false | pass |
| Pharmacodynamic paired synthetic deltas | `24` |

Overall status: `PASS`.

## Interpretation

This is a software guard, not a research result. It makes future changes safer by
turning the V45 synthetic mechanics expectations into an executable regression
test. If this script fails in a future session, the affected harness should be
fixed before any real quarantined cohort is opened.
