# Secondary-Route No-Degrees-Of-Freedom Checklist V45

Status: preregistration guardrail for secondary/context routes. No scoring is
authorized by this document.

Machine-readable checklist:

`docs/validation/input_schemas/V45_secondary_route_no_dof_checklist.tsv`

Purpose: prevent Karolinska DMF ROS or GSE228330 from becoming post-hoc
analyses. Before either route is scored against outcomes, every field below must
be filled, frozen, and committed in a route-specific addendum.

## Applies To

- `docs/validation/KAROLINSKA_PREREGISTRATION_TEMPLATE_V45.md`
- `docs/validation/GSE228330_OUTCOME_LABEL_ADDENDUM_TEMPLATE_V45.md`

## Required Frozen Choices

| Area | Must Be Frozen Before Scoring |
|---|---|
| cohort role | primary/secondary/context-only role and what the route can and cannot prove |
| subject map | sample-to-subject/timepoint/cell-type map and handling of missing pairs |
| outcome dictionary | label names, orientation, missingness, endpoint window, and positive/negative class definitions |
| expression provenance | raw/reprocessed/author-processed expression source and gene ID mapping |
| timepoint eligibility | which baseline and on-treatment timepoints are eligible for locked delta features |
| module/rule use | V22 module/rule unchanged, or context-only analysis if rule prerequisites fail |
| confounder diagnostics | which V32/V44/V45 batch, steroid, immune-tone, composition checks are scoreable |
| analysis budget | exact analyses to run and explicit analyses not run |
| success/failure wording | what a pass, fail, or inconclusive result can and cannot mean for the primary DMF lead |
| unscoreable conditions | missing labels, missing pairs, poor module coverage, or unresolved provenance states that stop scoring |

## Forbidden

Do not:

- choose a response endpoint after seeing module scores;
- switch timepoints after seeing performance;
- tune thresholds, signs, modules, or confounder sets;
- reinterpret GSE228330 as a primary DMF validation;
- reinterpret Karolinska as a clean early PBMC validation unless the finalized
  addendum documents eligible PBMC-equivalent early paired data.

## Current State

Both routes remain unscoreable for outcome validation until external labels/maps
arrive and the route-specific addendum is finalized blind to module scores and
performance.
