# V45 Collaborator Validation Package README

Status: external handoff/readiness artifact. No data received or analyzed.

## Purpose

This README bundles the files a collaborator or medical-team coordinator needs
to request, receive, and stage a validation cohort without changing the locked
analysis plan.

It is intentionally operational. It does not change `LOCKED_RULE_V22.md`, the
V42 preregistration, secondary preregistrations, or any threshold.

## Start Here

| Need | File |
|---|---|
| V45 readiness changelog / reviewer route | `docs/validation/V45_READINESS_CHANGELOG.md` |
| One-page clinical/data package checklist | `docs/validation/CLINICAL_DATA_DICTIONARY_CRF_V45.md` |
| Machine-readable CRF checklist | `docs/validation/input_schemas/V45_clinical_crf_checklist.tsv` |
| Data-use/terms capture template | `docs/validation/DATA_USE_TERMS_CAPTURE_V45.md` |
| Data-use machine-readable template | `docs/validation/input_schemas/V45_data_use_terms_capture_template.tsv` |
| Live cohort acquisition index | `docs/validation/LIVE_COHORT_ACQUISITION_PACKET_INDEX_V45.md` |
| Outbound data request tracker | `docs/validation/OUTBOUND_DATA_REQUEST_TRACKER_V45.md` |
| Intake preflight instructions | `docs/validation/VALIDATION_INTAKE_PREFLIGHT_V45.md` |
| Validation harness command README | `docs/validation/VALIDATION_HARNESS_README_V45.md` |
| Subject-map sanity checker | `docs/validation/SUBJECT_MAP_SANITY_CHECKER_V45.md` |
| Response-column audit | `docs/validation/RESPONSE_COLUMN_AUDIT_V45.md` |
| Checksum manifest validator | `docs/validation/CHECKSUM_MANIFEST_VALIDATOR_V45.md` |
| First-24h received-data checklist | `docs/validation/FIRST_24H_RECEIVED_DATA_OPERATOR_CHECKLIST_V45.md` |
| Received-status updater | `docs/validation/RECEIVED_STATUS_UPDATER_V45.md` |
| Package receipt manifest | `docs/validation/PACKAGE_RECEIPT_MANIFEST_TEMPLATE_V45.md` |
| Preflight failure taxonomy | `docs/validation/PREFLIGHT_FAILURE_TAXONOMY_V45.md` |
| Outcome-label dictionary validator | `docs/validation/OUTCOME_LABEL_DICTIONARY_VALIDATOR_V45.md` |
| Module-coverage precheck | `docs/validation/MODULE_COVERAGE_PRECHECK_V45.md` |
| Harness-ready decision template | `docs/validation/HARNESS_READY_DECISION_TEMPLATE_V45.md` |
| Batch/QC/steroid missingness rubric | `docs/validation/BATCH_QC_STEROID_MISSINGNESS_RUBRIC_V45.md` |
| Validation result report template | `docs/validation/VALIDATION_RESULT_REPORT_TEMPLATE_V45.md` |
| Handoff bundle template | `docs/validation/VALIDATION_HANDOFF_BUNDLE_TEMPLATE_V45.md` |
| Handoff completeness checker | `docs/validation/HANDOFF_COMPLETENESS_CHECK_V45.md` |
| Sensitive-data redaction checklist | `docs/validation/SENSITIVE_DATA_REDACTION_CHECKLIST_V45.md` |
| Author-run frozen harness packet | `docs/validation/AUTHOR_RUN_FROZEN_HARNESS_PACKET_V45.md` |
| Author-run packet bundle index | `docs/validation/AUTHOR_RUN_PACKET_BUNDLE_INDEX_V45.md` |
| Author-run output completeness check | `docs/validation/AUTHOR_RUN_OUTPUT_COMPLETENESS_CHECK_V45.md` |

## Ready-To-Send Request Packets

| Cohort | Packet | Role |
|---|---|---|
| Gafson DMF PBMC / NEDA-4 | `docs/validation/outbound_requests/gafson_dmf_ready_to_send_V45.md` | primary V22/V42 validation target |
| Karolinska DMF ROS | `docs/validation/outbound_requests/karolinska_dmf_ready_to_send_V45.md` | parallel MS DMF secondary label path |
| GSE228330 ocrelizumab PBMC | `docs/validation/outbound_requests/gse228330_ocrelizumab_ready_to_send_V45.md` | optional outcome-label request; otherwise context-only |
| Author-run fallback | `docs/validation/outbound_requests/author_run_fallback_ready_to_send_V45.md` | use if individual-level data cannot be transferred |

After a request is sent, save the exact sent text as:

```text
docs/validation/outbound_requests/<cohort>_sent_YYYY-MM-DD.md
```

and update:

- `analysis/v45_outbound_data_requests/request_tracker.tsv`
- `docs/validation/OUTBOUND_DATA_REQUEST_TRACKER_V45.md`

## Received Data: Required Order Of Operations

1. **Do not score anything.**
2. Place files under the agreed raw/quarantine path.
3. Capture non-sensitive data-use terms using
   `docs/validation/input_schemas/V45_data_use_terms_capture_template.tsv`.
4. Write or verify a checksum manifest.
5. Freeze the outcome-label dictionary before any response scoring.
6. Run response-column audit if the cohort is pharmacodynamic/context-only.
7. Run full intake preflight.
8. Run module-coverage precheck for expression-matrix packages.
9. Run subject-map sanity if paired deltas are required.
10. Finalize any cohort-specific preregistration addendum before outcome labels
   are scored.
11. Run locked-artifact hash audit and pre-commit readiness checks.
12. Run only the matching frozen harness.
13. Fill the validation result report and handoff bundle templates.
14. Run the handoff completeness checker for the declared lifecycle state.

## Minimal Commands

### Checksum Manifest

```bash
.venv/bin/python scripts/v45_checksum_manifest_validator.py write \
  --root data/quarantine/<cohort> \
  --manifest data/quarantine/<cohort>/SHA256_MANIFEST.tsv

.venv/bin/python scripts/v45_checksum_manifest_validator.py verify \
  --root data/quarantine/<cohort> \
  --manifest data/quarantine/<cohort>/SHA256_MANIFEST.tsv \
  --outdir analysis/checksum_manifest/<cohort> \
  --fail-on-error
```

### Primary Treatment-Response Intake

```bash
.venv/bin/python scripts/v45_validation_intake_preflight.py check \
  --root data/quarantine/<cohort> \
  --mode primary \
  --metadata data/quarantine/<cohort>/metadata/sample_metadata.tsv \
  --expression data/quarantine/<cohort>/processed/expression.tsv \
  --outdir analysis/intake_preflight/<cohort> \
  --write-checksums
```

### Paired Subject-Map Sanity

```bash
.venv/bin/python scripts/v45_subject_map_sanity_check.py check \
  --metadata data/quarantine/<cohort>/metadata/sample_metadata.tsv \
  --outdir analysis/subject_map_sanity/<cohort> \
  --min-paired-subjects 2 \
  --fail-on-error
```

### Module-Coverage Precheck

```bash
.venv/bin/python scripts/v45_module_coverage_precheck.py check \
  --expression data/quarantine/<cohort>/processed/expression.tsv \
  --outdir analysis/module_coverage_precheck/<cohort> \
  --fail-on-error
```

### Integrity/Regression Checks

```bash
.venv/bin/python scripts/v45_locked_artifact_hash_audit.py audit \
  --baseline docs/validation/LOCKED_ARTIFACT_HASH_BASELINE_V45.tsv \
  --outdir analysis/v45_locked_artifact_hash_audit \
  --fail-on-drift

.venv/bin/python scripts/v45_precommit_readiness_check.py
```

### Pharmacodynamic-Only Response-Column Audit

```bash
.venv/bin/python scripts/v45_response_column_audit.py audit \
  --metadata data/quarantine/<cohort>/metadata/sample_metadata.tsv \
  --outdir analysis/response_column_audit/<cohort> \
  --fail-on-response-like
```

## Cohort-Specific Notes

### Gafson

Use the V42 primary preregistration if the received cohort matches the planned
Gafson DMF PBMC/NEDA structure. If fields differ materially, document the
deviation before scoring; do not alter the locked V22 rule.

### Karolinska

Do not score outcomes until `KAROLINSKA_PREREGISTRATION_TEMPLATE_V45.md` is
finalized as a cohort-specific addendum, blind to module scores and outcome
performance.

### GSE228330

Current public metadata are context-only:

- no public response labels;
- current subject map is inferred/unverified;
- array reprocessing is still required for expression.

Run context-only analyses only after verified subject/timepoint mapping and
processed expression are available. If outcome labels are obtained, write a new
cohort-specific preregistration addendum before scoring.

## What Not To Commit

Never commit:

- raw individual-level expression or clinical data unless terms explicitly allow;
- credentials, API tokens, signed agreements, private email content, or private
  access URLs;
- restricted data-use agreement text;
- identifiable clinical data.

Commit only non-sensitive aggregate summaries, schemas, checksums if permitted,
and derived artifacts allowed by the captured terms.

## Validation Principle

Receiving data is not the same as being ready to analyze. A cohort is
harness-ready only after terms, checksums, intake schema, subject-map sanity,
and preregistration gates have all passed.
