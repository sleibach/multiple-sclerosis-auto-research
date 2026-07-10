# V52 Package Artifact Hash Coverage Audit

Date: 2026-07-10

Status: operational audit. This document adds no evidence, changes no locked
rule, and does not alter any validation or target verdict. It checks whether
artifacts in the V52 therapeutic package handoff bundle are covered by the
stable operator SHA256 snapshot.

## Inputs

- Handoff bundle:
  `docs/validation/THERAPEUTIC_PACKAGE_HANDOFF_BUNDLE_INDEX_V52.md`
- Hash snapshot:
  `docs/reports/V52_OPERATOR_ARTIFACT_HASH_SNAPSHOT.tsv`

## Result

The handoff bundle lists 36 unique artifacts. The current hash snapshot lists
54 artifacts. Thirty handoff artifacts are hash-covered by the snapshot. Six
handoff artifacts are not hash-covered.

This is not automatically an error. Some handoff artifacts are mutable
navigation or status documents, and the snapshot cannot safely hash itself. The
audit separates intentional exclusions from context or governance artifacts
where freezing is a policy choice rather than a correctness requirement. The
only clear stable operator-control gap identified by the first audit pass,
`docs/workups/genetics/CHR1_WRONG_DIRECTION_CONTROL_CHECKLIST_V52.md`, has now
been added to the snapshot.

## Handoff Artifacts Not Hash-Covered

| artifact | coverage assessment | action |
|---|---|---|
| `docs/reports/THERAPEUTIC_PATH_SUMMARY_CARD_V52.md` | high-level summary; useful context but not a package-execution control | leave out unless the project decides summary cards should be frozen |
| `docs/reports/THERAPEUTIC_PATH_V52.md` | synthesis report; reference context rather than operator control | leave out unless synthesis reports become frozen package controls |
| `docs/reports/THERAPEUTIC_ROUTE_STATUS_DASHBOARD_V52.tsv` | live status/dashboard artifact expected to change after future outcomes | intentionally mutable; do not freeze as a stable hash target |
| `docs/reports/THERAPEUTIC_ROUTE_DECISION_LOG_TEMPLATE_V52.md` | future route-update shell; stable enough to freeze, but lower priority than route execution artifacts | optional snapshot addition if the operator bundle wants full template drift checks |
| `docs/reports/POST_VALIDATION_ROUTE_UPDATE_PLAYBOOK_V52.md` | route-update governance; stable but expected to evolve if validation classes are extended | optional snapshot addition if governance drift checks are desired |
| `docs/reports/V52_OPERATOR_ARTIFACT_HASH_SNAPSHOT.tsv` | self-referential snapshot; hashing itself would create unstable drift | intentionally excluded |

## Snapshot Artifacts Not In The Handoff Bundle

The snapshot also covers twenty-four stable artifacts that are not listed in the handoff
bundle:

- `docs/validation/HANDOFF_ORDERED_FLOW_AUDIT_V52.md`
- `docs/validation/MANIFEST_README_CONSISTENCY_RECHECK_V52.md`
- `docs/validation/MEDICAL_TEAM_THERAPEUTIC_DATA_REQUEST_V52.md`
- `docs/validation/PACKAGE_INTAKE_GENERATED_OUTPUT_INVENTORY_V52.md`
- `docs/validation/PACKAGE_ID_VALIDATOR_REGRESSION_FIXTURE_V52.md`
- `docs/validation/PACKAGE_INTAKE_CLI_HELP_SNAPSHOT_V52.md`
- `docs/validation/PACKAGE_INTAKE_COMBINED_SMOKE_SUITE_V52.md`
- `docs/validation/PACKAGE_INTAKE_CROSS_REFERENCE_AUDIT_V52.md`
- `docs/validation/PACKAGE_INTAKE_RAW_TERM_SCAN_V52.md`
- `docs/validation/PACKAGE_ROUTE_CLASSIFIER_DUPLICATE_ID_GUARD_V52.md`
- `docs/validation/PACKAGE_ROUTE_CLASSIFIER_EMPTY_FIELDS_REGRESSION_V52.md`
- `docs/validation/PACKAGE_ROUTE_OUTPUT_SCHEMA_AUDIT_V52.md`
- `docs/validation/PACKAGE_ROUTE_OUTPUT_SCHEMA_NEGATIVE_FIXTURE_V52.md`
- `docs/validation/PACKAGE_ROUTE_OUTPUT_SCHEMA_NO_OUTPUT_FIXTURE_V52.md`
- `docs/validation/RECEIVED_PACKAGE_INTAKE_SAFETY_AUDIT_REGRESSION_FIXTURE_V52.md`
- `docs/validation/RECEIVED_PACKAGE_INTAKE_SAFETY_NEGATIVE_EMAIL_FIXTURE_V52.md`
- `docs/validation/RECEIVED_PACKAGE_DRY_RUN_REPLAY_AUDIT_V52.md`
- `docs/validation/ROUTE_CLASSIFIER_EXAMPLES_REGRESSION_V52.md`
- `docs/validation/VALIDATION_PACKAGE_ROUTE_CLASSIFIER_SCHEMA_CHECK_V52.md`
- `docs/validation/THERAPEUTIC_PACKAGE_HANDOFF_BUNDLE_INDEX_V52.md`
- `docs/reports/V52_OPERATOR_ARTIFACT_HASH_REFRESH_COMMANDS.md`
- `docs/reports/V52_OPERATOR_ARTIFACT_STABILITY_POLICY.md`
- `docs/workups/genetics/CHR1_COLLABORATOR_ASSAY_REQUEST_APPENDIX_V52.md`
- `docs/workups/genetics/OPENGWAS_PRE_EXPIRY_BOUNDED_POLISH_COMMANDS_V52.md`

These are legitimate snapshot targets: they are stable operator, schema,
handoff, collaborator-request, or bounded-command artifacts even if they are not
part of the minimal package bundle sent to every data owner.

## Verdict

Coverage is coherent after remediation. The stable chr1 operator-control
checklist is now hash-covered. The remaining uncovered artifacts are either
intentionally mutable, self-referential, or context/governance artifacts where
freezing is a project policy choice rather than a correctness requirement.
