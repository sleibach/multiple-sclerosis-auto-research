# Preflight Regression Tests V45

Status: infrastructure regression. Synthetic data only; no biological evidence.

## Purpose

`scripts/v45_validation_intake_preflight.py` is the gate before any received
cohort enters a frozen harness. This checkpoint turns its core synthetic checks
into an executable regression test so future edits cannot silently weaken:

- checksum coverage;
- metadata schema checking;
- pharmacodynamic no-response-label guardrails;
- the rule that preflight computes no module scores or validation metrics.

## Command

```bash
.venv/bin/python scripts/v45_preflight_regression_tests.py
```

The script invokes:

```bash
.venv/bin/python scripts/v45_validation_intake_preflight.py synthetic-check \
  --outdir analysis/v45_preflight_regression_tests/synthetic_check
```

and then asserts the generated JSON summaries.

## Result

Committed output:

- `analysis/v45_preflight_regression_tests/regression_summary.json`

Summary:

| Check | Result |
|---|---|
| Primary synthetic preflight passes | pass |
| Pharmacodynamic synthetic preflight passes | pass |
| Pharmacodynamic synthetic package with response-like column fails | pass |
| Missing checksum count is zero for valid synthetic packages | pass |
| Bad pharmacodynamic package has fail count >= 1 | pass |
| Synthetic assertions match detailed summaries | pass |
| No module scores computed | pass |

Overall status: `PASS`.

## Interpretation

This regression protects the intake boundary. If it fails in a future session,
no newly received validation or context cohort should be opened by any frozen
harness until the preflight behavior is fixed.
