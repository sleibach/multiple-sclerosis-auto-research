# Repair Request: metadata_or_pairing_contradiction

Status: draft request template. No validation result and no biological claim.

Subject: Metadata or sample-pairing repair needed

Dear <collaborator_or_data_provider>,

Thank you for the returned package for `<cohort_id>`. Our pre-registered intake
checks cannot proceed to interpretation in its current form.

Blocked state:

- V46 safe class: `BLOCKED_METADATA_CONTRADICTION`
- failure code: `EXPRESSION_SAMPLE_MISMATCH`
- trigger: expression columns and metadata sample IDs disagree
- allowed repair: repair sample IDs from source documentation

Requested repair:

- The metadata, sample IDs, subject IDs, or timepoints are contradictory under the frozen pairing rules.
- Please provide a corrected sample manifest or pairing table derived from source metadata, not from expression-score behavior.

Please return:

- sample manifest
- subject ID map
- baseline and early-treatment timepoint map
- correction provenance

Please do not send:

- score-informed sample ordering
- manual reassignment based on outcomes
- changed timepoint window

This request does not ask for any new analysis, changed rule, changed endpoint,
changed threshold, or interpretation. Once the repaired package is received, we
will rerun the same frozen intake and returned-package gates before any result
wording is drafted.
