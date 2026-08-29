# V57 Sequential Cohort-Evidence Accumulator: Frozen Plan

Status: **frozen before simulation outcomes**

## Purpose and Boundary

Test whether an anytime-valid evidence process can reduce dependence on one
small validation cohort by accumulating independent, pre-specified
cohort-level p-values as data packages arrive.

This is method characterization. Synthetic p-values are never biological
evidence. The four held cohorts have different diseases/therapies and are used
only as a contextual dry run, not as a confirmatory combined MS result.

## Fixed E-Process

For each valid one-sided cohort p-value `p`, use three fixed p-to-e
calibrators:

```text
e_k(p) = k * p^(k - 1), for k in {0.25, 0.50, 0.75}
```

Maintain the product separately for each calibrator and average the three
products at every cohort arrival. The mixture starts at one. Evidence crosses
the alpha=0.05 boundary at mixture e-value >=20.

No calibrator, order, threshold, or cohort is selected from observed evidence.
Future confirmatory use requires independent cohorts testing the same frozen
estimand with valid p-values.

## Simulation

- 200,000 sequences per scenario and seed;
- 20 possible cohort arrivals per sequence;
- seeds 57081, 57082, 57083;
- null: Uniform(0,1) valid p-values;
- moderate alternative: Beta(0.50,1) p-values;
- strong alternative: Beta(0.25,1) p-values.

Record probability of crossing by arrivals 5, 10, and 20 plus first-crossing
time. Do not store individual synthetic sequences.

## Method-Behavior Gate

The implementation is verified only if, under every seed:

1. null probability of ever crossing by 20 is <=0.055; and
2. strong-alternative probability of crossing by 20 is >=0.80.

Moderate-alternative performance is descriptive. A method pass does not make
the V22 signal externally validated; it supplies a disciplined future
accumulation rule.
