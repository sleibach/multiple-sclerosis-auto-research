# V57 Federated Effect-Size Schema

Status: **verified validation infrastructure; no external cohort evidence**

## Problem Found

The first operational federated record retained aggregate AUC and the frozen
permutation p-value, but it omitted the AUC confidence interval and Hedges' g
already produced by the owner-side V42 export. That did not invalidate the
e-process calibration, but it created an avoidable significance-only reporting
path and contradicted the stated requirement to retain site effect estimates.

## Fail-Closed Repair

Both independent and declared-cluster combiners now require:

- AUC in the locked positive direction;
- ordered AUC confidence limits containing that AUC;
- finite Hedges' g;
- the valid frozen one-sided permutation p-value;
- the existing estimand, harness, arrival, and dependence metadata.

The owner-export converter reads these values from the attested primary metric
row. Missing or inconsistent uncertainty is rejected before evidence is
accumulated. The e-process remains unchanged and consumes only the p-value;
effect size and uncertainty remain mandatory for interpretation rather than
being converted into additional evidence.

## Synthetic Verification

- The independent valid fixture passes.
- Duplicate independence and changed-harness fixtures still fail.
- A new record with a missing AUC confidence limit fails.
- The attested planted-signal export round-trips AUC `1.0`, CI `[1.0, 1.0]`,
  and Hedges' g `6.9794`; these are synthetic method-test values, not MS
  evidence.
- All seven clustered-combiner accept/refuse fixtures still pass their expected
  outcomes with the expanded record schema.

## Interpretation Boundary

No pooled effect estimate is inferred from these site summaries. Site
confidence intervals are not automatically simultaneous, and heterogeneous
site estimators must not be combined post hoc. The repair preserves effect
reporting; it does not create a new biological result or validate V22 in an
external cohort.
