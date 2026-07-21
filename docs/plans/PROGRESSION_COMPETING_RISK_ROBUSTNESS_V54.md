# V54 Progression Competing-Risk Robustness Plan

Status: frozen before simulation on 2026-07-21T23:31:53Z.

## Boundary

This is a seeded synthetic method audit, not an empirical estimate of death,
disability progression, or MS biology. It does not change the frozen P1
endpoint. It asks when treating death as censoring preserves or invalidates the
source-by-treatment-stratified cause-specific Cox score route.

## Generator

Each cohort has a latent molecular state, an independent latent progression
frailty, a reliability-0.70 observed molecular score, source/treatment
assignment correlated with molecular state, source HR 1.6, treatment HR 0.7,
10% score missingness, and administrative horizon 1.0.

Progression event probability before competing death is calibrated to `0.15`
or `0.30`. Molecular progression HR is `1.0` (null) or `1.7` per latent SD.
Competing-death probability by the horizon is calibrated to `0.10` or `0.25`.
Sample sizes are `120, 240, 320`; three fixed seeds and 400 replicates per seed
are used.

Five competing-event mechanisms are fixed:

1. `none`: no competing event;
2. `independent`: death independent of score and progression frailty;
3. `score_dependent`: death depends on molecular state but not latent
   progression frailty;
4. `progression_risk_dependent`: death depends on latent progression frailty
   but not molecular state;
5. `joint_score_progression_risk`: death depends on molecular state,
   progression frailty, and their interaction, deliberately creating adverse
   dependent selection in the progression risk set.

The first four distinguish ordinary competing risk from the joint mechanism;
they are not assumed valid in advance.

## Frozen Analysis And Decisions

The primary route is the existing source-by-treatment-stratified Cox score test
for progression, with competing death censored at its observed time. Report
progression events, competing deaths, valid fits, signed one-step effects, and
three-seed false-call/power probabilities.

- A mechanism is null-calibrated only if no aggregate null cell has a Wilson
  95% lower bound above 0.05 and its family maximum is compatible with a
  Binomial(aggregate replicates, 0.05) maximum reference.
- A reproducible significant direction under molecular HR 1.0 is a false
  progression association, regardless of whether that direction appears
  clinically plausible.
- Power is interpreted only in null-calibrated mechanisms and requires at least
  80% aggregate detection and 75% in every seed.
- If joint score/progression-risk death is anti-conservative, future packages
  with outcome-related mortality require a competing-risk sensitivity fixed
  before score access; a standard cause-specific Cox result cannot arbitrate
  alone.

A death-composite endpoint is not substituted post hoc. Any future composite or
subdistribution estimand requires its own clinical justification and frozen
interpretation.
