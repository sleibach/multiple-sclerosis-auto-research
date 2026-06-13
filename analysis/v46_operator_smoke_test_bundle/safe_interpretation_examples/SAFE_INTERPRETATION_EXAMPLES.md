# Safe-Interpretation Examples V46

Status: operator wording examples. No validation result and no biological claim.

Overall status: `PASS`; examples: `7`; lint failures: `0`.

| Example | Safe class | Band | Report mode | Next action |
|---|---|---|---|---|
| `aggregate_only_no_labels` | `CONTEXT_ONLY_OR_LABELS_NEEDED` | `no_mapped_response_groups` | `STOP_ONLY` | Request sample-mapped response labels or a valid aggregate author-run return containing the locked-rule metrics. |
| `aggregate_only_below_floor` | `BELOW_V45_PLANNING_FLOOR` | `below_planning_floor` | `STOP_ONLY` | Request additional labeled paired subjects or combine only under a separately pre-specified external meta-analysis plan. |
| `partial_labels_effect_size_only` | `INCONCLUSIVE_SMALL_COHORT` | `gafson_sized_effect_estimate_only` | `RESULT_SKELETON_ALLOWED_AFTER_GATES` | Use observed AUC/g/CI to update the powered-cohort request and seek an independent cohort with at least 30+30 clean labeled pairs, preferably 60-80/group. |
| `small_clean_full_labels` | `INCONCLUSIVE_SMALL_COHORT` | `gafson_sized_effect_estimate_only` | `RESULT_SKELETON_ALLOWED_AFTER_GATES` | Use observed AUC/g/CI to update the powered-cohort request and seek an independent cohort with at least 30+30 clean labeled pairs, preferably 60-80/group. |
| `minimum_decision_grade_clean` | `MINIMUM_DECISION_GRADE_CAUTION` | `minimum_decision_grade` | `RESULT_SKELETON_ALLOWED_AFTER_GATES` | Seek a replication cohort and preserve the batch/confounder diagnostic appendix with the report. |
| `batch_or_confounder_caution` | `CAUTION_BATCH_OR_CONFOUNDER` | `minimum_decision_grade` | `RESULT_SKELETON_ALLOWED_AFTER_GATES` | Seek a replication cohort and preserve the batch/confounder diagnostic appendix with the report. |
| `preferred_decision_grade_clean` | `ELIGIBLE_FOR_PREREGISTERED_INTERPRETATION` | `preferred_decision_grade` | `RESULT_SKELETON_ALLOWED_AFTER_GATES` | If positive, pursue prospective validation/utility; if negative, update the V22/V23 ledger under the pre-specified failure rules. |

Boundary: these examples are generated from existing V46 safe-class,
small-n, analyzable-pair, and repair-prioritization tables. They do not
authorize reading returned score values or changing the frozen V42/V22 rules.
