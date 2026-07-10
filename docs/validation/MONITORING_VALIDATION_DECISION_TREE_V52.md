# Monitoring Validation Decision Tree V52

Date: 2026-07-10

Status: additive interpretation aid. This document does not change
`docs/locked_rules/LOCKED_RULE_V22.md`,
`docs/validation/PREREGISTRATION_V42.md`,
`docs/validation/OUTCOME_INTERPRETATION_GRID_V42.md`, or the V44 batch guard.
It restates the pre-registered validation path as a mechanical if/then tree.

## Entry Condition

Use this tree only for a Gafson/Karolinska-style package or equivalent
DMF-like MS treatment-response cohort.

If the package is for target development, chr1 genetics, postpartum relapse
biology, or T/B compartment biology, do not use this tree. Use the relevant
V44/V52 handoff instead.

## Step 1: Package Eligibility

| if | then |
|---|---|
| Paired baseline and early on-treatment PBMC expression are present | Continue to Step 2 |
| Baseline sample is missing | `UNSCOREABLE_DATA`; record missing baseline |
| Early on-treatment sample is missing or outside pre-specified timing | `UNSCOREABLE_DATA`; record missing eligible treatment sample |
| Subject-level NEDA-4 or pre-specified equivalent response label is missing | `UNSCOREABLE_DATA`; do not reconstruct endpoint post hoc |
| Feature annotation cannot map enough V22 module genes | `UNSCOREABLE_DATA`; record failed module coverage |
| Batch/QC metadata are absent | Continue only if expression and labels are scoreable; flag reduced trust envelope |

## Step 2: Frozen Scoring

Apply exactly:

1. V42 feature mapping and preprocessing.
2. V22 frozen Class C score:
   `delta_HLAII - delta_IFN_APC`.
3. Fixed responder-higher orientation.
4. No sign flip, endpoint substitution, timepoint tuning, feature tuning, or
   threshold revision.

If scoring fails mechanically, classify as `UNSCOREABLE_DATA`.

## Step 3: Primary Result Class

| if | primary class |
|---|---|
| Adequate powered clean pass under V42 thresholds and no specificity/batch guard issue | `PASS_CLEAN` |
| Raw V42 pass but immune-tone, confounder, or batch diagnostics bound interpretation | `PASS_IMMUNE_TONE_BOUNDED` or `PASS_NON_SPECIFIC`, depending on V42/V44 outputs |
| Directional signal in small or underpowered cohort | `INCONCLUSIVE_UNDERPOWERED` with effect size and CI |
| Adequate powered fail under V42 thresholds | `FAIL_ADEQUATE_POWER` |
| Score points opposite to locked direction strongly enough under V42 criteria | `FAIL_ADEQUATE_POWER` and flag direction reversal |
| Receptor-only or nonspecific control outperforms the locked score by the V42 rule | downgrade to non-specific interpretation |

## Step 4: Confounder And Batch Interpretation

Run and report the pre-specified V32/V44 panels:

| diagnostic result | interpretation |
|---|---|
| Locked score survives steroid, composition, metabolic/STAT1, baseline APC/HLA-II, and batch diagnostics | Cleanest monitoring interpretation |
| Locked score survives only with broad immune-tone context | Immune-tone-bounded monitor; useful only with confounder reporting |
| Locked score is explained by response-correlated batch | No clean validation; batch-bound result only |
| Locked score is explained by simple cell composition | Do not treat as within-cell APC/HLA-II monitoring |
| Locked score is explained by steroid exposure | Do not treat as treatment-response biology without steroid-aware replication |

## Step 5: Therapeutic Interpretation

| final class | what it means for impact | what remains unproven |
|---|---|---|
| `PASS_CLEAN` | The scalar becomes externally supported as an early pharmacodynamic monitoring / stratification readout in that context | Not a clinical treatment-switching threshold, baseline selector, durable response guarantee, or drug target |
| `PASS_IMMUNE_TONE_BOUNDED` | The scalar may be useful as an immune-remodeling monitor with mandatory confounder/batch reporting | Not a clean APC/HLA-II-specific mechanism claim |
| `PASS_NON_SPECIFIC` | A dynamic immune-state signal exists, but the intended V22 biology is not specifically validated | Does not validate the locked scalar as intended |
| `INCONCLUSIVE_UNDERPOWERED` | Provides effect size and CI for the next cohort design | Neither pass nor kill |
| `FAIL_ADEQUATE_POWER` | Materially weakens the DMF/MS Class C monitoring route | Does not authorize post-hoc score revision or broad therapy-class claims |
| `UNSCOREABLE_DATA` | Package cannot test the rule | No biological inference |

## Step 6: Next Action

| final class | next action |
|---|---|
| `PASS_CLEAN` | Seek independent replication and prospective utility study; keep rule frozen |
| `PASS_IMMUNE_TONE_BOUNDED` | Replicate with confounder-rich cohort; report as bounded monitor |
| `PASS_NON_SPECIFIC` | Do not promote V22 biology; use result only for mechanism audit |
| `INCONCLUSIVE_UNDERPOWERED` | Use effect size and CI for powered sample-size planning |
| `FAIL_ADEQUATE_POWER` | Demote monitoring route in V52/V37 successor report; do not tune rescue rule on same data |
| `UNSCOREABLE_DATA` | Request missing fields or move to another complete validation package |

## Source Artifacts

- `docs/locked_rules/LOCKED_RULE_V22.md`
- `docs/validation/PREREGISTRATION_V42.md`
- `docs/validation/OUTCOME_INTERPRETATION_GRID_V42.md`
- `docs/validation/MONITORING_VALIDATION_COMMAND_MANIFEST_V52.md`
- `docs/validation/THERAPEUTIC_VALIDATION_HANDOFF_V52.md`
- `docs/validation/MEDICAL_TEAM_THERAPEUTIC_DATA_REQUEST_V52.md`
- `docs/validation/POWER_MAP_V43.md`
- `docs/reports/THERAPEUTIC_PATH_V52.md`
