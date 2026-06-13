# small_clean_full_labels

Status: safe wording example. No validation result and no biological claim.

Scenario: Both response classes are mapped, but the cohort remains too small for a definitive V42 result.
Safe class: `INCONCLUSIVE_SMALL_COHORT`.
Report mode: `RESULT_SKELETON_ALLOWED_AFTER_GATES`.
Planning band: `gafson_sized_effect_estimate_only` (`10-14`).
Allowed sentence: This small cohort supplies an effect-size and uncertainty estimate; it does not validate or project-ending claim the rule.
Report boundary: Use the generated report skeleton only after all gates pass.
Next action: Use observed AUC/g/CI to update the powered-cohort request and seek an independent cohort with at least 30+30 clean labeled pairs, preferably 60-80/group.
Skeleton: `analysis/v46_safe_class_report_template_readiness/fixtures/inconclusive_small_cohort.md`.
