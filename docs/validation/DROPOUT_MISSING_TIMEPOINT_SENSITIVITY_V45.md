# V45 Dropout and Missing-Timepoint Sensitivity Table

Status: synthetic method-planning artifact. This is not biological evidence.

## Purpose

The V45 power table used analyzable paired subjects per response group. In real
cohorts, enrollment or public sample count is larger than the number of subjects
with:

1. a usable baseline sample;
2. a usable early on-treatment sample;
3. a sample-mapped response label;
4. enough metadata to pass intake and batch/confounder guards.

This artifact translates nominal enrollment into expected analyzable paired
subjects under dropout/missing-timepoint rates, then maps that analyzable count
back onto the committed V45 synthetic power bands.

Generator:

`scripts/v45_dropout_sensitivity_table.py`

Machine-readable outputs:

- `analysis/v45_dropout_sensitivity_table/dropout_enrollment_targets.tsv`
- `analysis/v45_dropout_sensitivity_table/nominal_attrition_power_impact.tsv`
- `analysis/v45_dropout_sensitivity_table/summary.json`

## Headline

Dropout and missing early timepoints materially weaken the already conservative
cohort-size guidance:

- to retain `30` analyzable paired responders and `30` analyzable paired
  nonresponders, enroll about `38+38` if `20%` are missing and `50+50` if `40%`
  are missing;
- to retain `60+60`, enroll about `75+75` at `20%` missing and `100+100` at
  `40%` missing;
- to retain `80+80`, enroll about `100+100` at `20%` missing and `134+134` at
  `40%` missing;
- a nominal `30+30` cohort is decision-grade only in the clean large-effect
  synthetic scenario with no missing paired samples; at `20%` missing it maps to
  about `24+24`, using the `20+20` simulated planning band, which is no longer
  decision-grade.

## Enrollment Required To Retain Analyzable Pairs

| Target analyzable per group | Missing/dropout | Enroll per group | Total enrollment |
|---:|---:|---:|---:|
| 30 | 10% | 34 | 68 |
| 30 | 20% | 38 | 76 |
| 30 | 30% | 43 | 86 |
| 30 | 40% | 50 | 100 |
| 60 | 10% | 67 | 134 |
| 60 | 20% | 75 | 150 |
| 60 | 30% | 86 | 172 |
| 60 | 40% | 100 | 200 |
| 80 | 10% | 89 | 178 |
| 80 | 20% | 100 | 200 |
| 80 | 30% | 115 | 230 |
| 80 | 40% | 134 | 268 |

## Nominal Cohort Impact Examples

The table below maps nominal enrollment to expected analyzable paired subjects
and then to the nearest lower simulated V45 planning grid. Exact pass rates are
planning bands, not precision estimates; the V43 selected cells are small and
non-monotone in places.

| Nominal per group | Missing/dropout | Expected analyzable per group | Scenario | Nearest grid n | Synthetic pass rate | Decision band |
|---:|---:|---:|---|---:|---:|---|
| 15 | 0% | 15 | large clean | 15 | 0.542 | directional / often inconclusive |
| 15 | 20% | 12 | large clean | 10 | 0.542 | directional / often inconclusive |
| 15 | 40% | 9 | large clean | below grid | NA | below simulated grid |
| 30 | 0% | 30 | large clean | 30 | 0.917 | decision-grade pass probability |
| 30 | 20% | 24 | large clean | 20 | 0.625 | promising but not decision-grade |
| 30 | 40% | 18 | large clean | 15 | 0.542 | directional / often inconclusive |
| 60 | 20% | 48 | large clean | 45 | 0.708 | promising but not decision-grade |
| 80 | 20% | 64 | large clean | 60 | 0.833 | decision-grade pass probability |
| 100 | 20% | 80 | large clean | 80 | 0.833 | decision-grade pass probability |
| 100 | 40% | 60 | large clean | 60 | 0.833 | decision-grade pass probability |
| 30 | 20% | 24 | moderate noisy immune-tone | 20 | 0.333 | directional / often inconclusive |
| 80 | 20% | 64 | moderate noisy immune-tone | 60 | 0.083 | mostly inconclusive |
| 100 | 20% | 80 | moderate noisy immune-tone | 80 | 0.042 | mostly inconclusive |

## Practical Acquisition Rule

For a collaborator/prospective cohort, request enough enrollment to survive
missing paired samples:

1. If the medical team wants a minimum `30+30` analyzable clean large-effect
   test, request at least `38+38` when `20%` attrition is plausible and `50+50`
   when `40%` attrition is plausible.
2. If the medical team wants the preferred `60-80/group` analyzable range from
   `MEDICAL_TEAM_COHORT_SPEC_V45.md`, request `75-100/group` at `20%` attrition
   and `100-134/group` at `40%` attrition.
3. If a public or collaborator cohort starts around `10-15/group`, any missing
   early timepoints can push it below the simulated planning grid; treat it as
   effect-size and CI information unless the diagnostics and effect are unusually
   clean.

## Guardrail

Nominal sample count is not sufficient for validation-readiness. The project
should always report:

- nominal subjects per response group;
- analyzable paired subjects per response group;
- number excluded for missing baseline;
- number excluded for missing early on-treatment;
- number excluded for missing or unmappable outcome labels;
- number downgraded by batch/confounder or module-coverage guards.

This is an additive planning artifact. It does not change `LOCKED_RULE_V22.md`,
`PREREGISTRATION_V42.md`, or the frozen success/failure thresholds.
