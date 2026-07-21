# V54 Lysosomal Morphology Specificity Sensitivity

Status: post-result sensitivity frozen before execution. This plan follows the
family-wise GSE279972 lysosomal/foamy association observed in the frozen V54
lesion-state analysis. It cannot promote that result to progression evidence.

## Question

Does the GSE279972 lysosomal module's foamy-morphology coefficient survive
additional adjustment for broad microglial identity and foamy lipid/complement
state, or is it a non-specific restatement of the deposited morphology label?

## Frozen Additional Covariates

- `resident_microglia_identity`: `P2RY12`, `TMEM119`, `CX3CR1`, `SALL1`.
  This exact resident-myeloid marker set already appears in the project corpus.
- `mims_deoverlapped`: `GPNMB`, `APOE`, `LPL`, `TREM2`, `SPP1`, `C1QA`,
  `C1QB`, `C1QC`. This is the pre-existing MIMS lipid/complement program with
  `CTSB` removed to prevent direct overlap with the tested lysosomal module.

These are imperfect state proxies, not measured cell fractions. Resident
markers can themselves fall during microglial activation, so attenuation is a
specificity warning and persistence is not proof of cell-composition control.

## Frozen Models

All models retain deposited broad lesion class and `b_apc_composition`:

1. base model from the frozen lesion analysis;
2. plus resident microglia identity;
3. plus de-overlapped MIMS state;
4. plus both added covariates.

For every model report donor-clustered confidence intervals, three-seed 300,000
donor-wild nulls, leave-one-donor coefficient ranges, and max-variant control
across all four sensitivity models.

## Interpretation Rule

The association is `specificity_survives_tested_state_adjustment` only if all
four coefficients remain positive, every donor-wild p is at most 0.05, the
four-model max-variant p for the fully adjusted model is at most 0.10, its
clustered interval excludes zero, and every fully-adjusted leave-one-donor
coefficient is positive.

Otherwise it is `state_or_composition_sensitive`. Either result remains a
cross-sectional morphology association, not clinical progression, causality,
direction-matched druggability, or therapeutic evidence.
