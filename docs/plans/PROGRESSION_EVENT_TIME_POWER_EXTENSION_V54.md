# V54 Progression Event-Time Power Extension

Status: frozen synthetic method plan, committed before execution. This plan
does not use received or held biological values and cannot establish an MS
effect size, event rate, or progression mechanism.

## Question

How much do right censoring and source/treatment confounding change the ability
of a future longitudinal cohort to test one frozen molecular state against a
confirmed disability event, and does pre-specified stratification restore null
calibration when the score is imbalanced across those covariates?

## Synthetic Design

Each cohort contains one latent standardized molecular state, one noisy
observed measurement, binary source and treatment strata, a continuous event
time, and independent administrative/dropout censoring. Event times follow an
exponential proportional-hazards generator. The baseline hazard is calibrated
within each simulated cohort to the declared event probability before dropout.

Frozen defaults:

- sample sizes: `80, 120, 160, 240, 320`;
- pre-dropout event probabilities by the fixed horizon: `0.15, 0.30`;
- molecular hazard ratios per latent SD: `1.0, 1.5, 2.0`;
- dropout probabilities: `0.00, 0.25`;
- score-to-source/treatment assignment strengths: `0.0, 0.8`;
- source hazard ratio: `1.6`;
- treatment hazard ratio: `0.7`;
- observed-score reliability: `0.70`;
- molecular missingness: `0.10`;
- three seeds, 250 cohorts per seed and grid cell;
- two-sided alpha `0.05`, with positive score direction additionally required
  under non-null simulations.

The `0.8` assignment-strength regime deliberately creates a method stress test:
larger latent scores are more likely in the higher-hazard source and less likely
to receive the protective treatment. It is not an estimate of real cohort
confounding.

## Frozen Analyses

The same cohort is analyzed twice:

1. an unadjusted Cox score test for the observed molecular state;
2. a Cox score test stratified by the four source-by-treatment combinations.

The implementation uses continuous generated times, so event ties are expected
to be negligible. A fit is eligible only with at least 20 observed molecular
values, at least 10 observed events, at least 10 censored/event-free subjects,
and positive efficient information. Fewer events is inconclusive, consistent
with the V54 acquisition contract.

## Frozen Evaluation

- Null behavior is summarized by route, confounding, event probability,
  dropout, and N with Wilson intervals across the three seeds.
- A non-null cell is conclusive only when `p <= 0.05` and the score statistic is
  positive.
- A scenario reaches the planning threshold at the first N with aggregate
  conclusive probability at least `0.80` and every seed at least `0.75`.
- The adjusted route is considered acceptably calibrated only if no systematic
  null inflation appears across the grid. An isolated finite-simulation maximum
  is reported with its interval and is not interpreted from a point estimate
  alone.
- Adjusted and unadjusted routes are compared on the same simulation cells; a
  difference is method behavior, not biological evidence.

## Interpretation Boundary

The generator assumes proportional hazards, measured binary source/treatment,
independent dropout, and a correctly specified stratification. Real PIRA/CDP
data can violate every assumption. Therefore the output can set expectations
and force a cohort-specific pre-score simulation, but it cannot provide a
universal N, infer an MS hazard ratio, or make a progression claim.
