# Repair Request: missing_score_bearing_aggregate_outputs

Status: draft request template. No validation result and no biological claim.

Subject: Missing aggregate output files needed for mechanical review

Dear <collaborator_or_data_provider>,

Thank you for the returned package for `<cohort_id>`. Our pre-registered intake
checks cannot proceed to interpretation in its current form.

Blocked state:

- V46 safe class: `BLOCKED_COMPLETENESS`
- failure code: `UNSCOREABLE_MISSING_LOCKED_RULE_METRICS`
- trigger: see linked V46 returned-package gate output
- allowed repair: request a corrected aggregate return before interpretation

Requested repair:

- The aggregate return is incomplete under the V45 minimum-output specification.
- Please rerun the frozen author-run command or resend the missing aggregate outputs without changing thresholds, modules, labels, or timepoints.

Please return:

- locked_rule_metrics.tsv
- confounder_adjustment_metrics.tsv
- joint_confounder_metrics.tsv
- batch_diagnostic_metrics.tsv
- validation_result_report.md

Please do not send:

- interpretive prose in place of tables
- screenshots
- raw data
- post-hoc recalculated thresholds

This request does not ask for any new analysis, changed rule, changed endpoint,
changed threshold, or interpretation. Once the repaired package is received, we
will rerun the same frozen intake and returned-package gates before any result
wording is drafted.
