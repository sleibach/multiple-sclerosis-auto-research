# Returned-Package Route-State Matrix V46

Status: validation-readiness infrastructure. No validation result and no
biological claim.

## Purpose

`scripts/v46_returned_package_route_state_matrix.py` enumerates plausible
returned aggregate-package states before a real package arrives. It crosses:

- terms class: `LOCAL_PREFLIGHT_ALLOWED`, `AGGREGATE_ONLY_LOCAL_PREFLIGHT`,
  `AUTHOR_RUN_ONLY`, `NO_PROCESSING_ALLOWED`, `AMBIGUOUS_TERMS_BLOCK`,
  `UNKNOWN`;
- package state: `scored` or `unscoreable`;
- metric-format state: `canonical`, `noncanonical`, or `unknown`.

The output is a route matrix that says whether handling is blocked before
package gates, allowed only for unscoreable aggregate preflight/repair, requires
metric-format normalization, or can proceed to the V46 safe-interpretation
classifier. It does not read score values, expression data, labels, or any
quarantined cohort.

## Command

```bash
.venv/bin/python scripts/v46_returned_package_route_state_matrix.py \
  --outdir analysis/v46_returned_package_route_state_matrix \
  --fail-on-error
```

## Verified Synthetic Result

The committed run passed:

- route states: `36`;
- check rows: `144`;
- blocked routes: `18`;
- unscoreable preflight-only routes: `9`;
- score-reading paths: `0`;
- failures: `0`;
- overall status: `PASS`.

Machine-readable outputs:

- `analysis/v46_returned_package_route_state_matrix/returned_package_route_state_matrix_summary.json`
- `analysis/v46_returned_package_route_state_matrix/returned_package_route_state_matrix.tsv`
- `analysis/v46_returned_package_route_state_matrix/returned_package_route_state_checks.tsv`

## Interpretation Boundary

This matrix is route planning only. It can tell an operator which branch is safe
for a returned package shape, including when to stop before package handling or
when only repair/logistics wording is allowed. It cannot establish validation,
cannot make a biological claim, and cannot override the locked V22 rule, V42
pre-registration, or V46 safe-interpretation class.
