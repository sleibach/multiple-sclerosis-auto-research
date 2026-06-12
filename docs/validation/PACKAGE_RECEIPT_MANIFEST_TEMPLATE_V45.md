# Package Receipt Manifest Template V45

Status: receipt-stage operations template. No data received or analyzed.

Purpose: capture a non-sensitive inventory of a received validation package
before checksum/preflight/harness execution.

Machine-readable template:

`docs/validation/input_schemas/V45_package_receipt_manifest_template.tsv`

## Use

For each received file, fill one row before running preflight:

- `cohort_id`
- `receipt_timestamp_utc`
- `relative_path_or_external_location`
- `file_role`
- `bytes`
- `sha256_if_recordable`
- `sensitivity_class`
- `terms_status`
- `commit_allowed`
- `next_gate`

If terms do not permit committing path details or checksums, record the manifest
outside git and commit only a non-sensitive summary stating that the manifest
exists and passed local review.

## Sensitivity Classes

| Class | Meaning | Commit allowed |
|---|---|---|
| `public_metadata` | public accession metadata, non-identifying file lists | usually yes |
| `derived_non_sensitive_summary` | aggregate/receipt summary without private values | yes if terms allow |
| `restricted_expression` | individual/sample-level expression matrix | no unless terms explicitly permit |
| `restricted_clinical` | sample-level outcomes, NEDA/relapse/EDSS labels | no unless terms explicitly permit |
| `restricted_agreement` | signed terms, contracts, private correspondence | no |
| `credential_or_private_url` | access keys, private links, bearer tokens | no |

## Required Receipt Rule

Do not proceed to checksum validation until every row has:

- a file role;
- a sensitivity class;
- terms status;
- commit eligibility;
- next gate.

## Link To Later Gates

The receipt manifest feeds:

- checksum manifest validation;
- data-use terms capture;
- received-data triage board;
- no-raw-data git scanner;
- first-24h operator status template.

It is not a validation result.
