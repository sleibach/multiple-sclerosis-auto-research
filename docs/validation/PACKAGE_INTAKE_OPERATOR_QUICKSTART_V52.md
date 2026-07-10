# Package Intake Operator Quickstart V52

Date: 2026-07-10

Status: operational quickstart. This document adds no biological evidence,
changes no locked rule, and does not inspect real package data.

## Scope

Use this quickstart when a data owner returns any monitoring, chr1,
postpartum, compartment, metadata-only, or aggregate-only package.

The goal is to decide mechanically whether the package can proceed to a frozen
route-specific harness, must remain blocked, or needs a safe redacted manifest
before classification.

## Intake Sequence

1. Choose a package ID.
   - Shape: `YYYYMMDD_lowercase_alnum_underscore_segments`
   - Check:
     `python3 scripts/v52_validate_package_id.py <package_id>`
   - Do not include human names, emails, tokens, signed URLs, or patient
     identifiers.

2. Confirm package access terms before touching file content.
   - Use `docs/validation/PACKAGE_CHECKSUM_INTAKE_CHECKLIST_V52.md`.
   - If terms are absent, conflicting, or prohibit local analysis, stop.

3. Keep raw or restricted files out of git.
   - Use `docs/validation/RECEIVED_PACKAGE_FILE_NAMING_POLICY_V52.md`.
   - Raw package files belong only under the ignored quarantine path.
   - Safe metadata and classifier outputs may live under
     `analysis/received_package_intake/<package_id>/`.

4. Capture safe metadata.
   - Start from `docs/validation/INCOMING_PACKAGE_MANIFEST_TEMPLATE_V52.tsv`.
   - If sample-level labels or file names are restricted, create a redacted
     manifest instead of committing the original.

5. Classify the route.
   - Command:
     ```bash
     python3 scripts/v52_package_route_classifier.py \
       --manifests analysis/received_package_intake/<package_id>/manifest.tsv \
       --out analysis/received_package_intake/<package_id>/route_classification.tsv
     ```
   - Interpret with
     `docs/validation/PACKAGE_ROUTE_CLASSIFIER_STATUS_DECISION_TABLE_V52.tsv`.

6. Run the intake safety audit before commit.
   - Command:
     ```bash
     python3 scripts/v52_received_intake_safety_audit.py --fail-on-error
     ```
   - Any failure blocks commit until reviewed.

7. If blocked, write the blocker note.
   - Use `docs/validation/RECEIPT_BLOCKER_TEMPLATE_V52.md`.
   - State the specific blocker: terms, missing labels, unsafe metadata,
     missing timepoints, route mismatch, or unusable format.

## Proceed / Block Rule

Proceed only when all of the following are true:

- package ID validates
- access terms permit the intended local analysis
- raw or restricted content is quarantined outside git
- a safe manifest exists
- route classification is `matched` or explicitly acceptable under the
  preflight table
- the intake safety audit passes

Otherwise stop before analysis and record the blocker.
