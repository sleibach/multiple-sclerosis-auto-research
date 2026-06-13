# Returned-Package Regression Suite V46

Status: synthetic/software regression infrastructure. No validation result and
no biological claim.

## Purpose

`scripts/v46_returned_package_regression_suite.py` runs the V46 returned-package
guardrails from one command. It is narrower than the operator smoke bundle and
focused on aggregate author-run returns and safe interpretation.

The suite runs only synthetic or governance checks. It does not read real cohort
data, run validation, change locked rules, or interpret biological results.

## Command

```bash
.venv/bin/python scripts/v46_returned_package_regression_suite.py \
  --outdir analysis/v46_returned_package_regression_suite \
  --fail-on-error
```

## Included Checks

1. V46 terms-governance matrix synthetic check.
2. V46 metric-format adapter synthetic check.
3. V46 partial-label classifier synthetic check.
4. V46 returned-package command-order planner synthetic check.
5. V46 aggregate-only returned-package composition dry run.
6. V46 safe-interpretation classifier synthetic check.
7. V46 safe-wording fixture linter.
8. V45/V46 readiness stale-output detector.
9. V45 no-raw-data git scanner.

## Current Result

The committed run passed:

- steps: `9`
- failures: `0`
- runtime: recorded in `returned_package_regression_summary.json`
- overall status: `PASS`

Machine-readable outputs:

- `analysis/v46_returned_package_regression_suite/returned_package_regression_summary.json`
- `analysis/v46_returned_package_regression_suite/returned_package_regression_steps.tsv`
- isolated per-check subdirectories under `analysis/v46_returned_package_regression_suite/`

## Boundary

This suite supports software and method-readiness claims only. A passing suite
means returned-package guards still execute mechanically on synthetic fixtures.
It does not mean any real returned package is valid, scoreable, or clinically
interpretable.
