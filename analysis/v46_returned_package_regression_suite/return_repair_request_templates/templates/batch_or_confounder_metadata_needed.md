# Repair Request: batch_or_confounder_metadata_needed

Status: draft request template. No validation result and no biological claim.

Subject: Batch/QC/steroid metadata needed to interpret aggregate result

Dear <collaborator_or_data_provider>,

Thank you for the returned package for `<cohort_id>`. Our pre-registered intake
checks cannot proceed to interpretation in its current form.

Blocked state:

- V46 safe class: `CAUTION_BATCH_OR_CONFOUNDER`
- failure code: `BATCH_DIAGNOSTIC_WARNING`
- trigger: response-correlated batch/QC metadata detected
- allowed repair: report through V42/V44 interpretation grid

Requested repair:

- The returned result requires the pre-specified batch and confounder context to avoid over-interpreting a technical or immune-tone signal.
- Please provide aggregate batch/QC/steroid diagnostic outputs from the frozen harness, or the metadata fields needed to run those diagnostics under approved terms.

Please return:

- batch_diagnostic_metrics.tsv
- confounder_adjustment_metrics.tsv
- joint_confounder_metrics.tsv
- metadata dictionary if diagnostics cannot be returned

Please do not send:

- post-hoc batch correction of the primary score
- new confounder panels
- clean-pass wording without diagnostics

This request does not ask for any new analysis, changed rule, changed endpoint,
changed threshold, or interpretation. Once the repaired package is received, we
will rerun the same frozen intake and returned-package gates before any result
wording is drafted.
