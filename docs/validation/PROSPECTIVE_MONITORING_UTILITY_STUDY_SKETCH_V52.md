# Prospective Monitoring Utility Study Sketch V52

Date: 2026-07-10

Status: future-study design sketch. This document adds no evidence, changes no
locked rule, and does not alter the V42/V44 validation plan. It defines what
would be needed after external validation to test whether the bounded
APC/HLA-II monitoring signal is clinically useful.

## Purpose

The V52 therapeutic-path synthesis concludes that the most defensible near-term
impact is monitoring / stratification, not a direct target. If the frozen
validation harness later passes on an external paired PBMC treatment-response
cohort, the next question is not whether the score exists. The next question is
whether acting on the score improves patient management.

This sketch pre-defines that next step so a positive validation is not
overinterpreted as immediate clinical utility.

## Entry Condition

Start a prospective utility study only after one of these external-validation
outcomes:

| validation outcome | utility-study eligibility |
|---|---|
| Clean pass under the frozen V42/V44 harness | eligible |
| Raw pass with pre-specified immune-tone-bounded attenuation | eligible only as an immune-tone-aware monitoring study |
| Inconclusive but directionally consistent with informative confidence interval | design-only; do not start an action study without a powered replication plan |
| Fail, unscoreable package, or batch-invalidated result | not eligible |

No post-hoc threshold tuning, feature selection, or refitting on the validation
cohort is allowed to create eligibility.

## Study Type

The first prospective step should be an observational decision-impact study,
not an immediate treatment-switching intervention.

| phase | purpose | why this order |
|---|---|---|
| Prospective observational utility | Test feasibility, calibration, incremental value, and clinician decision impact while treatment decisions remain standard of care | Avoids exposing patients to score-guided actions before clinical utility is demonstrated |
| Prospective action trial | Test whether score-informed escalation or monitoring changes outcomes | Only justified after prospective calibration and decision-impact evidence |

## Population And Sampling

| element | pre-specified requirement |
|---|---|
| disease | relapsing MS or clinically comparable inflammatory MS cohort receiving a DMF-like immune-remodeling treatment |
| samples | paired baseline and early on-treatment PBMC, with the early timepoint pre-specified before enrollment |
| timing | baseline before treatment start; early on-treatment window consistent with the frozen validation plan; record exact days from start |
| labels | NEDA-4 or pre-specified equivalent outcome, recorded independently of the score |
| metadata | batch, site, steroid exposure, relapse/infection timing, DMT timing, lymphocyte counts, monocyte/B/T cell fractions where available |
| exclusions | missing baseline, missing early timepoint, unresolvable gene identifiers, missing response label, or batch structure that prevents interpretation under V44 rules |

The study should aim for at least `30` responders and `30` nonresponders if it
is intended to estimate utility with interpretable precision rather than only
feasibility.

## Frozen Score Handling

The bounded V22/V42 score is used exactly as frozen:

1. Ingest paired baseline and early on-treatment expression.
2. Apply the locked module definitions and early-change feature.
3. Run the V42/V44 batch and confounder reporting.
4. Report the raw score, pre-specified adjusted outputs, confidence intervals,
   and calibration metrics.

The score is not refit, reweighted, threshold-tuned, or replaced by a successor
feature in the prospective utility study.

## Primary Utility Questions

| question | required analysis |
|---|---|
| Feasibility | fraction of enrolled subjects producing a scoreable result within the required time window |
| Calibration | observed response rate by pre-specified score strata with confidence intervals |
| Incremental value | score added to standard baseline clinical variables, with cross-validated or optimism-corrected performance where sample size allows |
| Decision impact | whether the score would change clinician risk assessment or monitoring intensity under a pre-specified decision grid |
| Safety boundary | count cases where the score would have suggested reassurance but clinical disease activity occurred |

Decision-impact analysis may be simulated from observed outcomes in the first
prospective study, but any score-guided treatment change requires a later action
trial.

## What Would Count As Progress

| result | interpretation |
|---|---|
| High scoreability plus calibrated risk strata | supports prospective monitoring feasibility |
| Additive value over baseline clinical variables | supports clinical utility workup |
| Clean decision-curve or net-benefit signal | supports designing a score-informed action trial |
| Immune-tone-bounded but reproducible calibration | supports a narrower pharmacodynamic-state monitor, not a pure APC/HLA-II-specific rule |

## What Would Not Count

These results do not establish clinical utility:

- post-hoc threshold selection;
- validation only after dropping inconvenient samples;
- a raw pass that becomes batch-invalidated under the V44 diagnostics;
- a directionally favorable but underpowered estimate without a planned powered
  replication;
- replacement of the locked scalar with a more complex successor;
- use of the score as a baseline treatment-selection rule without prospective
  evidence.

## Next Data Ask

If external validation passes, the medical team should seek a prospective
cohort with:

1. paired baseline and early on-treatment PBMC expression;
2. independently adjudicated NEDA-4 or equivalent outcome;
3. site, batch, steroid, infection, relapse, DMT timing, and cell-count
   metadata;
4. enough responders and nonresponders to estimate calibration and incremental
   value;
5. a pre-specified plan for how clinicians would see and act on score strata in
   a later action trial.

## Source Artifacts

- `docs/reports/THERAPEUTIC_PATH_V52.md`
- `docs/validation/THERAPEUTIC_VALIDATION_HANDOFF_V52.md`
- `docs/validation/MONITORING_VALIDATION_DECISION_TREE_V52.md`
- `docs/validation/MONITORING_VALIDATION_COMMAND_MANIFEST_V52.md`
- `docs/validation/PREREGISTRATION_V42.md`
- `docs/validation/OUTCOME_INTERPRETATION_GRID_V42.md`
- `docs/validation/POWER_MAP_V43.md`
- `docs/validation/BATCH_GUARD_V44.md`
