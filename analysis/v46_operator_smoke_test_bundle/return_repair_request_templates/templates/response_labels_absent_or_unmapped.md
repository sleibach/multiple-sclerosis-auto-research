# Repair Request: response_labels_absent_or_unmapped

Status: draft request template. No validation result and no biological claim.

Subject: Mapped response labels or aggregate rerun needed

Dear <collaborator_or_data_provider>,

Thank you for the returned package for `<cohort_id>`. Our pre-registered intake
checks cannot proceed to interpretation in its current form.

Blocked state:

- V46 safe class: `CONTEXT_ONLY_OR_LABELS_NEEDED`
- failure code: `OUTCOME_DICTIONARY_MISSING`
- trigger: outcome labels exist but no frozen mapping/orientation
- allowed repair: ask provider; freeze dictionary before scoring

Requested repair:

- The package cannot support response-validation wording because responder/nonresponder labels are absent or not mapped to paired subjects.
- Please provide an approved response-label dictionary and sample-to-subject mapping, or rerun the frozen author-run harness locally and return the aggregate outputs.

Please return:

- approved response-label dictionary
- sample-to-subject and timepoint mapping
- aggregate author-run outputs if labels cannot be shared

Please do not send:

- unapproved private labels
- inferred endpoint orientation
- performance-based label mapping

This request does not ask for any new analysis, changed rule, changed endpoint,
changed threshold, or interpretation. Once the repaired package is received, we
will rerun the same frozen intake and returned-package gates before any result
wording is drafted.
