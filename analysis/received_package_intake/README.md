# Received Package Intake Directory

Date: 2026-07-10

Status: operational boundary note. This directory is for safe, reviewable
metadata artifacts only. It is not a raw-data holding area and does not contain
biological evidence.

## Allowed Here

Allowed files are package-level artifacts that can be committed without exposing
restricted or identifying content:

- synthetic or redacted package manifests
- route-classifier outputs generated from safe manifests
- receipt blocker notes that explain why intake stopped before analysis
- checksum summaries only when filenames and hashes are allowed to be disclosed

## Not Allowed Here

Do not place the following under this directory:

- raw expression matrices or assay files
- per-sample clinical labels unless the data owner explicitly allows public
  release
- patient identifiers, dates of birth, emails, tokens, signed URLs, or access
  credentials
- restricted collaborator package files
- files copied from a package before access terms are checked

Raw or restricted files belong only under the ignored quarantine path described
in `docs/validation/RECEIVED_PACKAGE_FILE_NAMING_POLICY_V52.md`.

## Required Flow

Before creating a package subdirectory:

1. Validate the package ID with `scripts/v52_validate_package_id.py`.
2. Confirm access terms with
   `docs/validation/PACKAGE_CHECKSUM_INTAKE_CHECKLIST_V52.md`.
3. Use `docs/validation/INCOMING_PACKAGE_MANIFEST_TEMPLATE_V52.tsv` for safe
   metadata capture.
4. Run `scripts/v52_package_route_classifier.py` on the safe or redacted
   manifest.
5. Apply `docs/validation/PACKAGE_ROUTE_CLASSIFIER_STATUS_DECISION_TABLE_V52.tsv`
   before any route-specific analysis.

If any step fails because terms, labels, or safe metadata are missing, stop and
write a blocker using `docs/validation/RECEIPT_BLOCKER_TEMPLATE_V52.md`.

Before committing any files under this directory, run:

```bash
python3 scripts/v52_received_intake_safety_audit.py --fail-on-error
```

The current recorded smoke-audit output is
`analysis/v52_received_intake_safety_audit/intake_safety_audit.tsv`.
