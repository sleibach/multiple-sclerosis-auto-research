# Repair Request: schema_or_metric_format_mismatch

Status: draft request template. No validation result and no biological claim.

Subject: Aggregate output table format needs repair

Dear <collaborator_or_data_provider>,

Thank you for the returned package for `<cohort_id>`. Our pre-registered intake
checks cannot proceed to interpretation in its current form.

Blocked state:

- V46 safe class: `BLOCKED_SCHEMA`
- failure code: `METADATA_REQUIRED_COLUMN_MISSING`
- trigger: intake preflight schema lacks required fields
- allowed repair: repair from source metadata or request corrected table

Requested repair:

- The returned aggregate tables are present but do not match the required schema or accepted aliases.
- Please resend the same frozen-run outputs with the canonical columns and files from the minimum-output specification.

Please return:

- canonical aggregate files and columns
- RUN_METADATA.txt with command and software versions

Please do not send:

- new analysis
- changed endpoint
- changed thresholds
- score interpretation

This request does not ask for any new analysis, changed rule, changed endpoint,
changed threshold, or interpretation. Once the repaired package is received, we
will rerun the same frozen intake and returned-package gates before any result
wording is drafted.
