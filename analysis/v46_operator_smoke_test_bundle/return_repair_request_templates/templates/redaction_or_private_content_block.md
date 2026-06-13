# Repair Request: redaction_or_private_content_block

Status: draft request template. No validation result and no biological claim.

Subject: Redacted aggregate-only return needed

Dear <collaborator_or_data_provider>,

Thank you for the returned package for `<cohort_id>`. Our pre-registered intake
checks cannot proceed to interpretation in its current form.

Blocked state:

- V46 safe class: `BLOCKED_REDACTION`
- failure code: `RAW_DATA_GIT_HARD_FAIL`
- trigger: no-raw scanner finds restricted/private data staged for git
- allowed repair: unstage/remove from git; keep in quarantine

Requested repair:

- The returned package cannot be reviewed because it appears to contain content outside the aggregate-return boundary.
- Please resend only aggregate output files from the frozen harness, with private sample identifiers removed or pseudonymized as your terms permit.

Please return:

- RUN_METADATA.txt
- validation_summary.json
- sample_attrition.tsv
- gene_mapping_coverage.tsv
- locked_rule_metrics.tsv
- confounder_adjustment_metrics.tsv
- joint_confounder_metrics.tsv
- batch_diagnostic_metrics.tsv
- validation_result_report.md
- failure_taxonomy_code.txt

Please do not send:

- raw expression matrix
- sample-level clinical labels unless separately approved
- unredacted agreements
- credentials

This request does not ask for any new analysis, changed rule, changed endpoint,
changed threshold, or interpretation. Once the repaired package is received, we
will rerun the same frozen intake and returned-package gates before any result
wording is drafted.
