# V45 Data-Use and Terms-Capture Template

Status: acquisition governance artifact. No data received or analyzed.

## Purpose

When Gafson, Karolinska, GSE228330 labels, or another low-barrier cohort arrives,
the project must record the terms of use before any validation harness runs. The
goal is to keep legal/access constraints auditable without committing
credentials, bearer tokens, private emails, or restricted agreement text.

Machine-readable blank template:

`docs/validation/input_schemas/V45_data_use_terms_capture_template.tsv`

Recommended per-cohort output location after receipt:

`data/quarantine/<cohort>/governance/data_use_terms_summary.tsv`

Only a non-sensitive summary should be committed. Restricted PDFs, signed
agreements, private messages, or access tokens must stay outside git.

## Required Fields

| Field | Purpose |
|---|---|
| `cohort_id` | stable local cohort identifier |
| `source_name` | study/publication/repository label |
| `source_url_or_accession` | public accession or non-sensitive source URL |
| `access_tier` | open, low_barrier, controlled, author_shared, collaborator |
| `received_date_utc` | date files were received |
| `data_provider_contact_non_sensitive` | public contact or role; no private content |
| `agreement_location_non_git` | local/private path or record ID outside git |
| `redistribution_allowed` | yes/no/unclear |
| `derived_metrics_allowed` | yes/no/unclear |
| `aggregate_publication_allowed` | yes/no/unclear |
| `individual_level_publication_allowed` | yes/no/unclear |
| `commercial_use_allowed` | yes/no/unclear/not_applicable |
| `data_retention_limit` | retention period or unclear |
| `requires_acknowledgement` | yes/no/unclear |
| `requires_provider_review_before_publication` | yes/no/unclear |
| `contains_personal_data_or_sensitive_clinical_data` | yes/no/unclear |
| `approved_internal_use` | exact permitted project use, short summary |
| `forbidden_use` | uses explicitly not allowed |
| `commit_allowed_files` | what may be committed, e.g. aggregate summaries only |
| `non_git_storage_path` | local restricted-data path outside git if applicable |
| `notes_non_sensitive` | concise non-sensitive notes |
| `reviewer` | person/agent who captured the terms |
| `review_date_utc` | date terms were reviewed |
| `status` | pending_review, approved_for_preflight, blocked_terms_unclear |

## Gate

A received cohort may proceed to intake preflight only if:

1. `status=approved_for_preflight`;
2. `derived_metrics_allowed` is `yes` or explicitly compatible with the planned
   validation outputs;
3. `aggregate_publication_allowed` is `yes` or the analysis is internal only;
4. `commit_allowed_files` clearly permits committing derived non-identifying
   artifacts, or the output plan is adjusted before any run;
5. no raw individual-level data, credentials, signed agreements, or private
   correspondence are committed.

If terms are unclear, the cohort is an acquisition blocker, not a data-analysis
blocker. Do not run the harness until the permitted use is clear.

## Example Non-Sensitive Summary

| Field | Example |
|---|---|
| `cohort_id` | `karolinska_dmf_ros_2019` |
| `access_tier` | `author_shared_low_barrier` |
| `redistribution_allowed` | `no` |
| `derived_metrics_allowed` | `yes` |
| `aggregate_publication_allowed` | `unclear` |
| `commit_allowed_files` | `aggregate QC/preflight summaries only; no raw expression or labels` |
| `status` | `pending_review` |

## Relationship To Existing Guards

This template runs before:

1. checksum manifesting;
2. `scripts/v45_validation_intake_preflight.py`;
3. `scripts/v45_subject_map_sanity_check.py`;
4. any cohort-specific preregistration addendum;
5. any frozen validation or context harness.

It is additive and does not change locked rules, pre-registered thresholds, or
the V42/V44/V45 harness logic.
