# V54 Foamy-State Lesion-Stratum Transport Plan

Status: frozen before stratum-specific coefficients were inspected.

## Question

Do the mutually separable OXPHOS-low and lysosomal-high foamy-morphology
associations persist within adequately represented deposited lesion strata, or
are the pooled coefficients carried by transport across lesion classes?

This is a post-result sensitivity of one morphology cohort. Even a positive
result remains morphology-bounded and is not progression, flux, causal, or
intervention evidence.

## Frozen Inputs And Endpoints

Input:
`analysis/v54_progression_lesion_module_panel/gse279972_panel_scores.tsv`.

The two endpoints and expected pooled directions are fixed from the prior
mutual-adjustment result:

- OXPHOS: lower in foamy samples;
- lysosomal unique state: higher in foamy samples.

Each endpoint is adjusted for the other endpoint, B/APC composition,
resident-microglia identity, and de-overlapped MIMS state.

## Pre-Score Stratum Eligibility

A deposited `Lesion_type_6` stratum is inferentially eligible only if, before
endpoint coefficients are inspected, it has:

1. at least 12 independent donors total;
2. at least 5 donors represented in each morphology group;
3. full-rank reduced and full designs for both endpoints; and
4. design condition number at most 30.

Classes 2 and 3 satisfy these metadata/design rules. NAWM has only four foamy
donors and is recorded as ineligible; it is not used to rescue or veto the
transport verdict.

## Frozen Inference

For each of two endpoints in each of two eligible strata:

- estimate the mutually adjusted foamy coefficient;
- report donor-clustered 95% confidence intervals;
- run 300,000 donor-wild residual sign-flip nulls over three fixed seeds;
- preserve a donor's sign across strata within each null draw;
- control the maximum absolute statistic across all four tests;
- repeat after leaving out each donor.

An endpoint passes lesion-stratum transport only if every eligible stratum:

1. has the pre-specified pooled direction;
2. has a clustered confidence interval excluding zero;
3. has donor-wild `p <= 0.05`;
4. has four-test max-family `p <= 0.10`; and
5. retains direction in every estimable leave-one-donor fit.

Failure is `NOT_TRANSPORT_SUPPORTED`, not proof of no within-stratum effect.
Passing is `MORPHOLOGY_ASSOCIATION_TRANSPORTS_ACROSS_ELIGIBLE_LESION_STRATA`,
not evidence of progression or a treatment direction.

