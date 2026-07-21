# V54 Foamy Morphology Donor-Estimand Audit

Status: frozen after the two-lineage critique and metadata-only coverage check,
before score analysis. This post-result audit can only bound or downgrade the
already exploratory morphology coefficients.

## Problem

GSE279972 contains repeated samples and multiple lesion classes per donor.
Testing donor ID against lesion class with Fisher's exact test would treat
repeated categorical observations as independent and does not answer whether
the foamy coefficient is identified within donors. The relevant question is
how much morphology variation remains within donor and within donor-by-lesion
blocks.

The metadata-only check found 21 donors and 43 donor-by-lesion blocks. Six
donors contain both morphology labels (23 samples), but only three
donor-by-lesion blocks contain both labels (six samples). These counts are
design facts and fixed the sensitivity below.

## Frozen Checks

1. Publish the complete donor-by-lesion morphology coverage table.
2. For OXPHOS and lysosomal scores, fit a donor-fixed-effect model over the 23
   samples from the six morphology-varying donors with lesion-class fixed
   effects, B/APC composition,
   resident-microglia identity, de-overlapped MIMS state, and the other module
   as a mutual covariate. This coefficient is identified only by within-donor
   morphology variation after the measured adjustments.
3. Use HC3 confidence intervals and a donor-level Rademacher wild residual
   null under the reduced no-morphology model. Use seeds `54801`, `54802`, and
   `54803`, 100,000 replicates each, with max-T control across two endpoints.
4. Report leave-one-informative-donor-out coefficient ranges. A sign change is
   an influence warning, not proof of a donor-specific biological effect.
5. Report unadjusted foamy-minus-nonfoamy differences in the three
   donor-by-lesion blocks that contain both labels. With three blocks, the
   smallest exact two-sided sign p-value is 0.25; these are descriptive only.
6. Re-express the prior lesion-class interaction LODO results as standardized
   donor-deletion changes using the committed full-model standard error. This
   tests influence language only and cannot turn a null interaction into
   donor-specific heterogeneity.

## Interpretation

- A within-donor endpoint is `direction_retained_but_underpowered` if its
  coefficient retains the pooled sign but fails any inferential gate.
- It is `within_donor_supported_exploratory` only if the HC3 interval excludes
  zero, donor-wild p is at most 0.05, two-endpoint max-T p is at most 0.10, and
  every informative-donor deletion retains direction.
- Otherwise the pooled result is `substantially_between_donor_or_unresolved`.

No outcome can restore global post-result family support, identify temporal
progression, establish flux or causality, or produce an intervention direction.

## Fail-Closed Execution Amendment

The initially specified all-54-sample HC3 fit stopped before either endpoint
was estimated because non-varying singleton donor strata produced leverage
exactly equal to one, making HC3 undefined. The six morphology-varying donors
are the only donors that identify a within-donor coefficient. Before inspecting
an endpoint result, the executable model was therefore restricted to their 23
samples. The revised 23 x 13 full design is full rank, has condition number
`31.46`, and maximum leverage `0.763`. This amendment is driven by the design
matrix failure, not by score direction or significance.
