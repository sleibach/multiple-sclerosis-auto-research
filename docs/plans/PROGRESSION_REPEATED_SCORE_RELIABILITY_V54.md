# V54 Progression Repeated Molecular-Score Reliability Plan

Status: frozen before simulation on 2026-07-21T23:49:12Z.

## Boundary

This is a seeded synthetic study-design audit. It characterizes when repeated
baseline molecular measurement can improve a progression-association study;
it is not empirical evidence about biomarker stability, an MS hazard ratio, or
treatment efficacy. It does not modify a locked rule or pre-registration.

## Fixed Generator

Each cohort has a stable latent molecular state, independent progression
frailty, source and treatment assignments correlated with state, source HR
1.6, treatment HR 0.7, and a proportional exponential progression time over a
unit horizon. Source-by-treatment defines four Cox strata. Cumulative event
probability is `0.15` or `0.30`; molecular HR per latent SD is `1.0`, `1.5`, or
`1.7`; sample size is `120, 240, 320`.

The single-measurement reliability is `0.40` or `0.70`. Acquisition plans use
one, two, or three baseline measurements. Each measurement has 10% independent
missingness; the pre-specified score is the arithmetic mean of every available
measurement, requiring at least one. Measurement error is either independent
across repeats or has within-person correlation `0.50`. For one measurement,
error correlation is not applicable and is represented once. The stable latent
state and error model are fixed; no outcome-informed weighting or timepoint
selection is allowed.

Three fixed seeds and 400 replicates per seed are used per cell. Empirical
squared correlation between the averaged observed score and latent state is
reported alongside retained sample size.

## Frozen Analysis And Decisions

Run the source-by-treatment-stratified Cox score test on the standardized
pre-specified average. Report signed one-step effects, valid fits, empirical
reliability, retained sample size, and three-seed rejection probabilities.

- A measurement plan is calibrated only if no aggregate null cell has a Wilson
  95% lower bound above 0.05 and its fixed-family maximum is compatible with a
  Binomial maximum reference.
- Power is interpreted only for calibrated plans and requires at least 80%
  aggregate detection, at least 75% in every seed, and exclusively positive
  calls.
- A repeat plan is **materially useful** only if, at the same event rate,
  effect, sample size, and starting reliability, it improves power by at least
  0.10 over one measurement and that gain is present in every seed. Effective
  reliability gain is reported but cannot substitute for power gain.
- A repeat plan with correlated error is compared with both one measurement
  and the same repeat count under independent error. Diminishing returns are a
  design result, not evidence that a biological state is unstable.
- No result supplies an empirical effect size or a reason to collect repeated
  molecular samples without a progression-qualified endpoint and the existing
  receipt gates.

All artifacts must state that they contain synthetic method behavior only.
