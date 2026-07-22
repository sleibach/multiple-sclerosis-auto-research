# V54 Progression Enrollment-Inflation Audit

Status: **CONDITIONAL_ENROLLMENT_LOOKUP_COMPLETE_NO_UNIVERSAL_N**.

This is seeded synthetic study-planning behavior only. It is not an empirical
MS event rate, loss rate, effect size, or universal sample-size recommendation.

## Equal-Quota Results

Across 54 fixed loss/event scenarios, all
54 reach the frozen count
targets within the searched total-enrollment range of 450-2,400. Each selected
minimum requires the 95% Wilson lower bound for joint target attainment to be
at least 0.90 in every one of three seeds.

- Reference planning scenario (10% follow-up loss, 10% score missingness, 10%
  confirmation loss, event probability 0.30): gross `690`
  (`230` per site; inflation
  `1.53x`), minimum-seed assurance
  `0.928`.
- Severe-loss scenario (20% in all three loss channels, event probability
  0.30): gross `990` (`330` per
  site; `2.20x`).
- Lower-event scenario (10% in all loss channels, event probability 0.15):
  gross `1380` (`460` per site;
  `3.07x`).

The event target, not merely participant retention, drives inflation in the
lower-event setting. These numbers are conditional on the generator and are a
planning lookup, not a guarantee.

## Passive Recruitment Stress

With all three loss channels fixed at 10% and event probability 0.30:

- `balanced_in_expectation`: gross total `690`, minimum-seed assurance `0.931` (Wilson lower `0.923`), `BALANCED_IN_EXPECTATION_NOT_FIXED_QUOTA`.
- `moderate_45_35_20`: gross total `1035`, minimum-seed assurance `0.933` (Wilson lower `0.925`), `OUTSIDE_TESTED_BALANCED_REFERENCE`.
- `severe_60_30_10`: gross total `2055`, minimum-seed assurance `0.913` (Wilson lower `0.904`), `OUTSIDE_TESTED_BALANCED_REFERENCE`.

Clearing participant/event arithmetic by enrolling more does not validate an
unequal site allocation. Only explicit equal site quotas align with the fixed
balanced design that previously passed transport; all passive strategies need
the full site transport gate on realized data.

## Boundary

The generator assumes independent loss channels. Any score/risk-dependent
attendance, censoring, death, or confirmation mechanism invokes the separate
V54 invalidity and sensitivity boundaries. Enrollment inflation cannot repair
informative missingness, endpoint misclassification, unknown site scale, or a
nonportable site effect.
