# V54 Progression Endpoint-Confirmation Error Plan

Status: frozen before simulation on 2026-07-22T01:29:01Z.

## Boundary

This seeded synthetic audit tests method behavior when true progression is not
confirmed or a non-confirmable trajectory is falsely labeled confirmed. Error
rates and dependencies are stress-test assumptions, not estimates from MS
cohorts. The audit changes no endpoint definition or pre-registration.

## Frozen Generator

- analyzable N: `450`, `900`, `1,500`;
- event probability before confirmation: `0.15`, `0.30`;
- molecular HR per latent SD: `1.0` or `1.5`;
- three seeds and `800` cohorts per cell;
- one normalized follow-up unit and confirmation lag `0.25`;
- latent events after `0.75` cannot be confirmed by the horizon;
- balanced random three-site assignment, site baseline HRs
  `1.50/1.00/0.67`, assay scales `0.50/1.00/2.00` plus fixed offsets;
- score reliability `0.70` and 10% independent score missingness;
- guarded within-site standardized, site-stratified Cox route only.

## Frozen Error Families

1. complete confirmation;
2. 10% independent missed confirmation;
3. 10% score-dependent missed confirmation;
4. 10% latent-risk-dependent missed confirmation;
5. 10% joint score/risk missed confirmation;
6. 2% independent false confirmation among non-confirmable subjects;
7. 2% score-dependent false confirmation;
8. joint missed confirmation plus score-dependent false confirmation.

Score/risk logits use fixed coefficients. Rates are calibrated within the
eligible true-event or non-confirmable set in every synthetic cohort.

## Frozen Adjudication

Null calibration uses the strict-cell plus six-cell family-maximum rule at
alpha `0.05`. Invalid families are excluded from positive-performance and
minimum-N summaries. For calibrated families, a non-null call must be
significant in the positive direction; minimum N requires aggregate probability
at least `0.80` and every seed at least `0.75`.

An invalid mechanism is an interpretation failure, not “lost power.” A
calibrated mechanism bounds only the frozen generator and does not prove a real
cohort free of confirmation bias.
