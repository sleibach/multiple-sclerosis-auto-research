# V54 Progression Visit-Schedule And Interval-Observation Robustness Plan

Status: frozen before simulation on 2026-07-21T23:41:26Z.

## Boundary

This is a seeded synthetic method audit, not an empirical estimate of MS
progression, visit attendance, or a molecular effect. It does not modify the
frozen P1 endpoint or analysis. It asks when observing an irreversible latent
disability onset only through scheduled assessments and later confirmation
preserves calibration, loses power, or creates ascertainment bias.

## Fixed Generator

Each synthetic cohort has a latent molecular state, independent progression
frailty, reliability-0.70 observed molecular score, 10% score missingness, and
source/treatment assignments correlated with latent state. Source HR is 1.6,
treatment HR is 0.7, and source-by-treatment defines four analysis strata.
Latent progression time follows a proportional exponential model over a
two-year horizon, calibrated to cumulative event probability `0.15` or `0.30`.
The molecular progression HR is `1.0` or `1.7` per latent SD.

Sample sizes are `120, 240, 320`. Three fixed seeds and 400 replicates per seed
are used. Assessment intervals are `0.25`, `0.50`, and `1.00` years. Baseline
is always observed. A latent event is irreversible for this method audit. It is
detected at the first attended scheduled visit after onset and confirmed only
at a later attended visit at least `0.25` years after detection. Without valid
confirmation by year 2, the outcome remains censored/inconclusive rather than
being converted to a negative.

Four attendance mechanisms are fixed:

1. `complete`: every scheduled visit is observed;
2. `independent_20pct`: each post-baseline visit is missed independently with
   target probability 0.20;
3. `score_dependent_20pct`: missingness depends on latent molecular state but
   not progression frailty, calibrated to 0.20;
4. `joint_score_progression_risk_20pct`: missingness depends on molecular
   state, progression frailty, and their interaction, calibrated to 0.20.

The latter two are adverse diagnostic mechanisms, not empirical attendance
models.

## Frozen Analysis

The primary observed-data route assigns a confirmed event to its first
detection visit. A fixed sensitivity assigns it to the midpoint between the
last attended event-free visit and first detection. Two audit-only oracles are
reported: exact latent event time for all latent events, and exact latent time
restricted to events that the visit/confirmation process ascertained. Oracles
cannot replace the observed route in real data.

Because scheduled visits induce event-time ties, all observed routes use a
Breslow tie-aware, source-by-treatment-stratified Cox score test. The
implementation must pass independent `statsmodels.PHReg(ties="breslow")`
fixtures before interpretation. Report valid fits, confirmed events,
unconfirmed latent events, median detection delay, signed one-step effects,
and three-seed rejection probabilities.

## Frozen Decisions

- A route/mechanism family is calibrated only if no aggregate null cell has a
  Wilson 95% lower bound above 0.05 and its maximum is compatible with the
  Binomial maximum reference across that fixed family.
- Reproducible signed rejection under molecular HR 1.0 is ascertainment bias,
  regardless of clinical plausibility.
- Power is reported only for calibrated observed-data families and requires
  at least 80% aggregate rejection, at least 75% in every seed, and exclusively
  positive calls.
- Schedule-induced loss is measured against the full latent-time oracle at the
  same sample size and event setting. A null caused by sparse assessment or
  absent confirmation cannot be interpreted as absence of association.
- Detection-time and midpoint routes are not selected by whichever performs
  better. Detection time remains primary; midpoint is a fixed sensitivity.
- No interval-censoring model, visit window, confirmation lag, or endpoint is
  selected post hoc. A future interval-censored model requires a separately
  frozen implementation and interpretation.

Every output must state that it is synthetic method behavior and not evidence
about MS biology, disability progression, attendance, or treatment efficacy.
