# minimum_decision_grade_clean

Status: safe wording example. No validation result and no biological claim.

Scenario: The return reaches the minimum decision-grade band only if diagnostics are clean.
Safe class: `MINIMUM_DECISION_GRADE_CAUTION`.
Report mode: `RESULT_SKELETON_ALLOWED_AFTER_GATES`.
Planning band: `minimum_decision_grade` (`30-59`).
Allowed sentence: This cohort reaches the minimum decision-grade planning band only under clean-effect assumptions; the V42 grid and diagnostics determine interpretation.
Report boundary: Use the generated report skeleton only after all gates pass.
Next action: Seek a replication cohort and preserve the batch/confounder diagnostic appendix with the report.
Skeleton: `analysis/v46_safe_class_report_template_readiness/fixtures/minimum_decision_grade_caution.md`.
