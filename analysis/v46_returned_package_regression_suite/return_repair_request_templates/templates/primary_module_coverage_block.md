# Repair Request: primary_module_coverage_block

Status: draft request template. No validation result and no biological claim.

Subject: Processed matrix or gene mapping needed for primary module coverage

Dear <collaborator_or_data_provider>,

Thank you for the returned package for `<cohort_id>`. Our pre-registered intake
checks cannot proceed to interpretation in its current form.

Blocked state:

- V46 safe class: `UNSCOREABLE_DATA`
- failure code: `PRIMARY_MODULE_COVERAGE_FAIL`
- trigger: V22 primary modules fail coverage precheck
- allowed repair: repair gene mapping under V42 rules or request processed matrix

Requested repair:

- The primary locked modules cannot be scored with the current feature identifiers or processed matrix.
- Please provide the feature annotation/gene-symbol mapping used for the expression matrix, or a processed matrix with standard gene identifiers.

Please return:

- feature annotation
- gene identifier mapping
- processed expression matrix if terms allow local preflight
- or aggregate author-run outputs

Please do not send:

- changed module genes
- lower module coverage threshold
- post-hoc replacement modules

This request does not ask for any new analysis, changed rule, changed endpoint,
changed threshold, or interpretation. Once the repaired package is received, we
will rerun the same frozen intake and returned-package gates before any result
wording is drafted.
