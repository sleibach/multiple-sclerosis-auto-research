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
4. V46 receipt-manifest schema linter synthetic check.
5. V46 package-manifest shape classifier synthetic check.
6. V46 returned-package command-order planner synthetic check.
7. V46 returned-package route-state matrix.
8. V46 aggregate-only returned-package composition dry run.
9. V46 unscoreable-return composition dry run.
10. V46 safe-interpretation classifier synthetic check.
11. V46 safe-wording fixture linter.
12. V46 result-report safe-class linter.
13. V46 small-n conclusion language table.
14. V46 analyzable-pair confidence envelope.
15. V46 return repair-request templates.
16. V46 partial-label repair prioritization.
17. V46 first-30-minute returned-package decision table.
18. V46 first-30 repair-template coverage linter.
19. V46 first-30 returned-package status-board dry run.
20. V46 returned-package status-board schema linter.
21. V46 returned-package preflight dry run.
22. V46 returned-package state-transition validator.
23. V46 returned-package handoff bundle manifest.
24. V46 returned-package documentation cross-link linter.
25. V45/V46 readiness stale-output detector.
26. V46 returned-package dependency graph.
27. V45 no-raw-data git scanner.

## Current Result

The committed run passed:

- steps: `27`
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
