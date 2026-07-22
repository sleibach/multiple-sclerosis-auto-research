# V54 Progression Treatment-Switch Estimand Audit

Status: frozen before simulation on 2026-07-22T00:34:12Z.

## Boundary

This seeded synthetic audit tests method behavior when treatment changes during
progression follow-up. It does not estimate an MS treatment effect, switching
rate, molecular effect, or clinical estimand. It changes no locked rule or
pre-registration.

## Fixed Generator

- total sample size: `180` and `320`;
- administrative horizon: one normalized follow-up unit;
- progression event probability before switching: `0.30`;
- switch probability: `0.25` when a switch mechanism is active;
- molecular progression HR: `1.0` (null) or `1.7` per latent SD;
- observed-score reliability: `0.70`, with 10% independent score missingness;
- post-switch progression HR: `0.5`, `1.0`, or `1.5`;
- switch mechanisms: none, independent, score-dependent,
  progression-risk-dependent, and joint score/progression-risk-dependent;
- three fixed seeds and 400 cohorts per cell.

Continuous switch and event times are generated from calibrated exponential
rates. If switching occurs first, the event rate changes by the fixed
post-switch HR. Independent latent progression frailty affects event risk;
mechanism-specific switch rates may depend on molecular state, frailty, or
their interaction.

## Frozen Estimands

1. `treatment_policy`: retain follow-up and observed post-switch events. This
   estimates association under the realized treatment policy, not untreated
   natural history. Score-adaptive treatment can induce an association even
   when the direct molecular event HR is one.
2. `censor_at_switch`: censor at first switch. This targets the pre-switch
   association only when switch censoring is adequately independent; joint
   score/risk switching can create informative selection.

Both are always reported. Neither may replace the other after inspecting
direction or significance. A future cohort must declare the primary estimand
before score access and retain the other as the frozen sensitivity.

## Calibration And Verdicts

Null families are evaluated by mechanism and estimand across sample sizes and
post-switch effects. A cell is strictly flagged when its 95% Wilson lower bound
exceeds 0.05. Consistent with the other V54 multi-cell audits, a family is
method-invalid only when it has a strict flag **and** the fixed-family maximum
binomial tail is below 0.05. A strict but family-compatible family is reported
and excluded from positive-performance summaries rather than called valid or
invalid. Power is summarized only for cleanly calibrated families and is not
an empirical MS effect estimate.

Correction note: the first code pass implemented strict-cell invalidity alone,
which conflicts with the family-maximum sentence above and with the established
V54 calibration rule. It overcalled two independent-switch families whose
family tails were 0.170 and 0.130. The implementation was corrected before any
scientific interpretation or commit; the flags remain visible and excluded.

All artifacts must state that this is synthetic method behavior only.
