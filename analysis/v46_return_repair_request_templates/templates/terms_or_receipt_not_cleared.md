# Repair Request: terms_or_receipt_not_cleared

Status: draft request template. No validation result and no biological claim.

Subject: Clarification needed before returned validation package can be reviewed

Dear <collaborator_or_data_provider>,

Thank you for the returned package for `<cohort_id>`. Our pre-registered intake
checks cannot proceed to interpretation in its current form.

Blocked state:

- V46 safe class: `BLOCKED_TERMS_OR_RECEIPT_GATES`
- failure code: `TERMS_NOT_APPROVED`
- trigger: data-use capture is missing or not approved for preflight
- allowed repair: request clarification or approval; keep files quarantined

Requested repair:

- Please confirm the data-use terms that permit us to inspect this returned package.
- If package review is not permitted, please either approve aggregate-only review or run the frozen author-run harness locally and return only non-sensitive aggregate outputs.

Please return:

- terms approval or no-processing instruction
- permitted package handling scope

Please do not send:

- raw expression
- private clinical tables
- credentials
- private URLs

This request does not ask for any new analysis, changed rule, changed endpoint,
changed threshold, or interpretation. Once the repaired package is received, we
will rerun the same frozen intake and returned-package gates before any result
wording is drafted.
