# Returned-Package Preflight Dry Run V46

Status: validation-readiness infrastructure. No validation result and no
biological claim.

## Purpose

This one-command dry run composes the V46 returned-package pre-score route:
receipt-manifest schema linting, package-shape classification, first-30 route
lookup, state-transition validation, and repair-template coverage. It is meant
to prove that a returned package can be routed mechanically before any returned
result values are opened.

## Command

```bash
.venv/bin/python scripts/v46_returned_package_preflight_dryrun.py \
  --outdir analysis/v46_returned_package_preflight_dryrun \
  --fail-on-error
```

## Current Result

- synthetic cases: `6`
- composed steps: `13`
- case failures: `0`
- step failures: `0`
- state-transition status: `PASS`
- repair-template coverage status: `PASS`
- all `score_values_read`: `false`
- overall status: `PASS`

Synthetic routes exercised:

- canonical scored aggregate;
- noncanonical scored aggregate;
- unknown score-like alias blocked by schema linter before classification;
- unscoreable aggregate;
- terms-blocked aggregate;
- unsafe raw-expression manifest blocked by schema linter before classification.

Outputs:

- `analysis/v46_returned_package_preflight_dryrun/returned_package_preflight_dryrun_summary.json`
- `analysis/v46_returned_package_preflight_dryrun/returned_package_preflight_dryrun_cases.tsv`
- `analysis/v46_returned_package_preflight_dryrun/returned_package_preflight_dryrun_steps.tsv`
- per-case outputs under `analysis/v46_returned_package_preflight_dryrun/<case>/`

## Boundary

This dry run uses synthetic receipt manifests and method-only guard outputs. It
does not read real returned metric tables, expression matrices, labels, or
quarantined cohorts. A `PASS` means the pre-score routing machinery composes
correctly; it does not mean any real package is valid or interpretable.
