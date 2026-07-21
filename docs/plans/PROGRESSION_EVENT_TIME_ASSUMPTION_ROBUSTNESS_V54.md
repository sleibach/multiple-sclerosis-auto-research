# V54 Progression Event-Time Assumption Robustness Plan

Status: frozen before simulation on 2026-07-21T22:59:53Z.

## Boundary

This is a seeded synthetic method audit of the already frozen
source-by-treatment-stratified Cox score route. It is not biological evidence,
does not estimate an MS hazard ratio, and does not modify the V54 P1/P2 blinded
pre-registration. Its purpose is to identify conditions under which one Cox
coefficient is calibrated, merely underpowered, or scientifically
misleading.

## Fixed Generator

Each synthetic cohort contains a latent molecular state, a reliability-0.70
observed score, binary source and treatment assignments correlated with latent
state, source hazard ratio 1.6, treatment hazard ratio 0.7, 10% score
missingness, and a horizon of 1.0. Source-by-treatment defines the four Cox
strata. Baseline hazard is calibrated within each replicate to a pre-censoring
event probability of 0.15 or 0.30.

Event times arise from a two-period piecewise exponential model with a fixed
cut at time 0.5. The molecular log-hazard patterns are:

| pattern | early HR | late HR | interpretation |
|---|---:|---:|---|
| null | 1.0 | 1.0 | calibration |
| proportional | 1.7 | 1.7 | correctly specified positive effect |
| early_only | 2.2 | 1.0 | early effect diluted by one coefficient |
| late_only | 1.0 | 2.2 | late effect diluted by one coefficient |
| crossing | 2.0 | 0.5 | genuine time-varying effect that may cancel |

The sample sizes are 120, 240, and 320. Three fixed seeds and 500 replicates
per seed are used for every cell.

## Fixed Censoring Mechanisms

All dropout mechanisms target 25% dropout before the horizon unless named
administrative-only:

1. `administrative_only`: no dropout before time 1.0.
2. `independent`: dropout assignment and time independent of score and latent
   event time.
3. `score_dependent`: dropout probability depends on latent molecular state,
   but is conditionally independent of event time given state. This tests
   covariate-dependent censoring without violating the conditional censoring
   assumption.
4. `event_risk_dependent`: dropout preferentially censors subjects whose latent
   event would occur early, without depending on molecular state.
5. `joint_score_event_risk`: dropout depends on the interaction between latent
   molecular state and latent early-event risk and occurs before that event.
   This deliberately violates conditional independent censoring and is the
   adverse informative-dropout case.

Dropout probabilities are calibrated numerically within replicate. The exact
mechanism and achieved dropout fraction must be written to output.

## Frozen Analyses

For every replicate, run:

1. the existing source-by-treatment-stratified whole-follow-up Cox score test;
2. an early-window diagnostic, administratively censoring at 0.5;
3. a late-window diagnostic among subjects event-free and observed at 0.5,
   resetting time at the landmark.

The whole-follow-up route is the frozen inferential route under audit. Window
tests are diagnostics only and cannot replace it post hoc. Report two-sided
alpha 0.05 results, signed one-step coefficients, valid-fit rates, observed
events, dropout, and three-seed stability. Do not call a comparison of window
p-values an interaction. A separate direct early-versus-late coefficient
contrast is outside this fast audit and must be pre-registered if later used.

## Decision Rules

- **Calibrated:** for a null family, no aggregate cell has a Wilson 95% lower
  bound above 0.05, and the family maximum is compatible with its binomial
  maximum reference.
- **Anti-conservative / invalid:** a null cell's Wilson lower bound exceeds
  0.05, or a censoring family shows reproducible directional false calls across
  all seeds. Such a route cannot adjudicate progression without a censoring
  model or sensitivity analysis fixed before score access.
- **Power loss:** a same-direction non-null pattern has lower whole-follow-up
  detection than the corresponding correctly specified proportional pattern.
  This is not type-I invalidity.
- **Cancellation boundary:** the crossing pattern yields low whole-follow-up
  detection while early and late diagnostics recover opposing signs. A null
  whole-follow-up coefficient then cannot be interpreted as absence of a
  time-varying association.
- **Planning threshold:** at least 80% aggregate detection and at least 75% in
  every seed. Only null-calibrated censoring regimes are eligible for power
  interpretation.

All output must state that these are synthetic assumptions and method behavior,
not empirical MS progression or dropout estimates.
