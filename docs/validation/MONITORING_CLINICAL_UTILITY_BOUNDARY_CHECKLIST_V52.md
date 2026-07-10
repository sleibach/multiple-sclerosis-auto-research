# Monitoring Clinical Utility Boundary Checklist V52

Date: 2026-07-10

Status: operational boundary checklist. This document adds no evidence, changes
no locked rule, and does not alter the V42/V44 validation plan.

## Purpose

The bounded APC/HLA-II monitoring signal could become useful only through a
sequence of increasingly demanding claims. This checklist keeps those claims
separate so a validation pass is not over-read as immediate clinical utility or
treatment guidance.

## Claim Boundaries

| claim level | what it means | minimum evidence | what it does not mean |
|---|---|---|---|
| Technical scoreability | the cohort can be ingested and scored by the frozen harness | V42/V44 preflight passes; module genes/timepoints/labels/batch metadata adequate | no predictive or clinical claim |
| External predictive validation | the frozen score predicts the pre-specified response label in an external cohort | clean pass or pre-specified immune-tone-bounded pass with confidence intervals | no proof that acting on the score improves outcomes |
| Pharmacodynamic monitoring | score strata reflect an early treatment-response state under similar therapy context | replicated validation plus confounder/batch diagnostics consistent with V32/V44 | not a baseline treatment-selection rule |
| Clinical utility | the score improves decision quality beyond standard variables | prospective decision-impact study with pre-specified clinician action grid | not yet evidence that changing treatment based on the score is safe/effective |
| Treatment-action utility | score-guided monitoring/escalation improves patient outcomes | prospective action trial or equivalent pre-specified interventional evidence | not established by retrospective or observational validation alone |

## Pass / Do-Not-Pass Checklist

Before a V52 document or downstream report says the monitoring route has moved
forward, all applicable boundary checks below must be answered.

| check | yes condition | if no |
|---|---|---|
| Was the frozen V42/V44 rule applied without refitting? | exact locked modules, feature, and threshold/reporting plan used | do not call it validation |
| Was package eligibility decided before outcome interpretation? | accept/partial/reject status assigned by the command manifest and acceptance criteria | classify as unscoreable or partial-context only |
| Did batch diagnostics pass or give a pre-specified warning? | V44 batch guard reports no response-correlated invalidation | do not call it a clean pass |
| Were V32 confounders reported? | glucocorticoid, composition, metabolic/immune-tone, and STAT1 panels reported as specified | report as incomplete validation |
| Is the result externally replicated or only internally supported? | independent external cohort result exists | keep claim at provisional/internal level |
| Is there prospective decision-impact evidence? | clinicians' risk assessment/action grid tested prospectively | do not claim clinical utility |
| Is there score-guided action evidence? | outcome-improving action trial or equivalent pre-specified evidence | do not recommend treatment switching based on the score |

## Approved Wording

| evidence state | allowed wording |
|---|---|
| External clean pass | "The frozen score externally validated as an early treatment-response monitor in this cohort." |
| Immune-tone-bounded pass | "The score validated as an immune-tone-aware pharmacodynamic monitor, with bounded interpretation." |
| Inconclusive but informative | "The cohort estimates effect size and uncertainty but does not settle the rule." |
| Technical scoreable only | "The package is analyzable; no predictive claim follows from scoreability." |
| Prospective decision-impact evidence | "The score has evidence of clinical utility for decision support." |
| Action trial evidence | "Score-guided action has outcome evidence." |

## Forbidden Wording Without Additional Evidence

- Do not call a clean external pass a treatment-selection rule.
- Do not call a retrospective validation proof of clinical utility.
- Do not call an immune-tone-bounded pass a pure APC/HLA-II-specific marker.
- Do not call scoreability validation.
- Do not call calibration or decision-curve improvement a treatment-action
  mandate.
- Do not imply the score cures, prevents, or directly treats MS.

## Source Artifacts

- `docs/validation/PREREGISTRATION_V42.md`
- `docs/validation/OUTCOME_INTERPRETATION_GRID_V42.md`
- `docs/validation/BATCH_GUARD_V44.md`
- `docs/validation/THERAPEUTIC_VALIDATION_HANDOFF_V52.md`
- `docs/validation/MONITORING_VALIDATION_DECISION_TREE_V52.md`
- `docs/validation/MONITORING_VALIDATION_COMMAND_MANIFEST_V52.md`
- `docs/validation/PROSPECTIVE_MONITORING_UTILITY_STUDY_SKETCH_V52.md`
