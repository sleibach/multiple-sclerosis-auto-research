# Aggregate-Only Returned-Package Composition Dry Run V46

Status: synthetic validation-readiness infrastructure. No validation result and
no biological claim.

## Purpose

`scripts/v46_aggregate_only_returned_package_composition_dryrun.py` proves that
the V46 returned-package pieces compose safely on a synthetic aggregate-only
author-run return. It exercises:

1. aggregate-only terms classification;
2. returned-package command-order planning;
3. noncanonical metric-format adaptation;
4. author-run redaction/completeness gate on the normalized package;
5. aggregate schema validation;
6. partial-label classification;
7. safe-interpretation classification.

The dry run uses seeded synthetic aggregate outputs only. It reads no real cohort
data and no sample-level private data. It does not change the locked V22 rule or
the V42 pre-registration.

## Command

```bash
.venv/bin/python scripts/v46_aggregate_only_returned_package_composition_dryrun.py \
  --outdir analysis/v46_aggregate_only_returned_package_composition_dryrun \
  --fail-on-error
```

## Current Result

The committed run passed:

- composed steps: `8`
- checks: `10`
- step failures: `0`
- check failures: `0`
- final safe-interpretation class: `BELOW_V45_PLANNING_FLOOR`
- sample-level data read: `false`
- score values interpreted: `false`

Machine-readable outputs:

- `analysis/v46_aggregate_only_returned_package_composition_dryrun/aggregate_only_composition_summary.json`
- `analysis/v46_aggregate_only_returned_package_composition_dryrun/aggregate_only_composition_steps.tsv`
- `analysis/v46_aggregate_only_returned_package_composition_dryrun/aggregate_only_composition_checks.tsv`

## Interpretation

This dry run demonstrates a realistic safe outcome: a collaborator aggregate
package can pass terms, alias normalization, return gates, and schema validation
while still being restricted to non-decisive wording because the labeled subset
is below the V45 planning floor. That is correct behavior. It prevents a
structurally valid but under-labeled package from being promoted into a
validation result.

The result is method behavior only. It is not evidence for MS biology,
treatment response, or clinical validity.
