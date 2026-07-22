# V54 Progression Combined-Ascertainment Audit Plan

Status: frozen before simulation on 2026-07-22T01:04:27Z.

## Boundary

This seeded synthetic audit asks whether attendance loss, competing death,
treatment-switch censoring, and site structure that are bounded alone can
compound into invalid progression inference. It tests method behavior only. It
does not estimate any MS effect, dropout/death/switch process, or progression
mechanism and changes no locked rule or pre-registration.

## Fixed Generator

- sample sizes: `180`, `320`, and `450`;
- event probabilities before ascertainment: `0.15` and `0.30`;
- molecular progression HR: `1.0` and `1.5` per latent SD;
- three fixed seeds and `800` cohorts per cell;
- observed-score reliability `0.70`, with 10% independent score missingness;
- latent progression frailty log-HR `0.70`;
- three site baseline HRs: `1.50`, `1.00`, and `0.67`;
- site assay scales `0.50`, `1.00`, and `2.00`, with fixed offsets;
- each active attendance-loss, death, or switch-censoring process targets a
  10% marginal event probability within follow-up.

Score-only censoring uses log-rate `0.8z`; risk-only censoring uses `0.8u`;
weak-joint censoring uses `0.2z + 0.2u + 0.35zu`, where `z` is latent molecular
state and `u` is independent progression frailty. Process times are generated
independently conditional on `z,u` and observed follow-up ends at the first
progression event, attendance loss, death, switch, or administrative horizon.

## Frozen Stacks

1. clean balanced reference;
2. attendance score-only;
3. death risk-only;
4. switch score-only;
5. all three separable processes;
6. attendance weak-joint;
7. death weak-joint;
8. switch weak-joint;
9. all three weak-joint processes;
10. all three weak-joint processes plus score-linked 60/30/10 site allocation.

The site-linked stack is a positive-control challenge for pooled inference, not
an empirical cohort model.

## Frozen Analysis Routes

1. `guarded_within_site_stratified`: standardize the observed score within
   predeclared site and use a site-stratified Cox score test;
2. `naive_global_pooled`: globally standardize the assay-scaled score and omit
   site strata.

The guarded route is the only candidate progression route. The naive route is
retained to verify that the site guard detects the known confounding path.

## Null And Compounding Rules

For each stack and route, null calibration is assessed jointly across six
sample-size/event-probability cells. A cell flags when its 95% Wilson lower
bound exceeds `0.05`. A family is invalid only when a strict cell flag is
accompanied by a fixed-family maximum binomial tail below `0.05`. Strict but
family-compatible flags are reported and excluded.

Compounded invalidity is called only when a combined stack is invalid under the
guarded route while every named constituent single-process family under that
same route is calibrated. No post-result mechanism or route substitution is
allowed. Non-null performance is summarized only for calibrated families and
is not biological power evidence.

## Interpretation

An invalid combined stack establishes a synthetic design boundary and adds a
mandatory combined sensitivity; it does not show that a real cohort has that
mechanism. A calibrated combined stack bounds only the frozen generator and
does not prove robustness to every joint process.
