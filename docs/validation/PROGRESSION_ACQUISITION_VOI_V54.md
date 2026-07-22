# V54 Progression Acquisition Value of Information

Status: artifact-bound operational ranking. “Value” means which documented
decision and gate a data bundle unlocks. It is not a probability of biological
success, a monetary VOI estimate, or a new finding.

## Immediate Priority

| rank | acquisition bundle | decision unlocked | why it cannot be substituted |
|---:|---|---|---|
| 1 | verified subject-sample-visit link plus repeated molecular and confirmed disability components | first P1 test that state precedes accumulation | relapse, stage, NEDA response, and postmortem morphology are not progression trajectories |
| 2 | expected/actual visits, attendance and censoring reasons, death metadata | interpretable event-time inference | 10% weak joint score/risk attendance was method-invalid in independent simulation |
| 3 | site, batch, platform, quality, and blinded scale metadata | within-site inference and transport audit | pooled site-aligned signal was anti-conservative |
| 4 | balanced site enrollment and confirmed-event yield | transport-informative rather than descriptive P1 | the 450/30%-event reference is conditional; imbalanced or sparse designs failed transport |
| 5 | PIRA definition plus relapse, steroid, infection, and full treatment-switch history | relapse-independent and switch-estimand interpretation | CDP cannot be relabeled PIRA; switch routes can change or invalidate interpretation |

Five living molecular candidates could potentially be clarified by the first
and fifth requests, but none is currently eligible and no off-record field is
assumed to exist. The exact first action remains source-owner clarification plus
a prospective request if those fields were never collected.

## Conditional Priority

| rank | acquisition bundle | prerequisite |
|---:|---|---|
| 6 | blinded molecular reliability and repeat-error audit | P1 core receipt |
| 7 | paired CSF/blood and direct composition | a P1 association worth localizing |
| 8 | longitudinal chronic-active lesion imaging | P1 core receipt; adjunct, not endpoint replacement |
| 9 | direction-resolved multi-donor functional perturbation | P1 association and P2 localization/justified context |

P3 has the largest eventual therapeutic meaning but is not the next rational
acquisition: without a progression association and direction, it would repeat
the project's context-dependent target failures.

## Machine Artifact

Run:

```bash
.venv/bin/python scripts/v54_progression_acquisition_voi.py
```

The script validates every named schema field, gate identifier, candidate, and
supporting artifact, then writes
`analysis/v54_progression_acquisition_voi/acquisition_priority.tsv`.

## Medical-Team Ask

First seek a de-identified, verified sample-subject-visit map linking expression
to raw repeated EDSS/T25FW/9HPT, confirmed CDP/PIRA protocol fields, every
expected and observed visit, attendance/censoring/death reasons, relapse and
steroid dates, complete DMT switching, site/platform/batch/QC, and cell counts.
If no existing source has that link, the rational next resource is a
prospective balanced longitudinal cohort, not another cross-sectional omics
dataset.

## Boundary

This ranking identifies information bottlenecks. It does not imply that the
requested data will confirm a molecular state, establish a target, or halt MS
progression.
