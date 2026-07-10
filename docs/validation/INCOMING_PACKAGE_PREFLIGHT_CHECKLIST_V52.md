# Incoming Package Preflight Checklist V52

Date: 2026-07-10

Status: operational checklist. This document adds no evidence and runs no
analysis. It orders the package-receipt checks that must happen before any
monitoring, chr1, secondary-biology, context-only, or rejection decision.

## Rule

Do not run analysis on any incoming package until this preflight is complete.
If a step fails, stop at the listed action and do not reinterpret the package
post hoc.

## Ordered Preflight

| step | check | pass condition | fail action | artifact |
|---|---|---|---|---|
| 1 | access terms | package terms allow local analysis under the project constraints | stop; request permitted package or terms clarification | `docs/validation/PACKAGE_CHECKSUM_INTAKE_CHECKLIST_V52.md` |
| 2 | quarantine and checksum | raw or received files are quarantined, checksummed, and not committed if large or restricted | stop; record receipt blocker | `docs/validation/PACKAGE_CHECKSUM_INTAKE_CHECKLIST_V52.md`; `docs/validation/MANIFEST_METADATA_VS_RAW_DATA_GIT_POLICY_V52.md` |
| 3 | route classification | package maps to exactly one primary route or a context/reject class | stop; classify as unscoreable if no route fits | `docs/validation/VALIDATION_PACKAGE_ROUTE_CLASSIFIER_V52.tsv`; `docs/validation/PACKAGE_ROUTE_CLASSIFIER_OPERATOR_NOTE_V52.md`; `docs/validation/PACKAGE_ROUTE_CLASSIFIER_STATUS_DECISION_TABLE_V52.tsv` |
| 4 | route example sanity check | package resembles a known route example or the difference is documented | document difference before proceeding | `docs/validation/VALIDATION_PACKAGE_ROUTE_CLASSIFIER_EXAMPLES_V52.tsv` |
| 5 | field dictionary | required route fields are present or the missing fields are allowed partial-context fields | reject, context-only, or request missing fields | `docs/validation/VALIDATION_PACKAGE_FIELD_DICTIONARY_V52.tsv` |
| 6 | acceptance criteria | package meets accept or pre-defined partial criteria for its route | reject or context-only | `docs/validation/TARGET_PACKAGE_ACCEPTANCE_CRITERIA_V52.tsv` |
| 7 | stable artifact hash check | operator packet has not drifted unexpectedly before external use | review mismatch before handoff | `docs/reports/V52_OPERATOR_ARTIFACT_HASH_VERIFY_COMMANDS.md` |
| 8 | route-specific operator card | operator follows the route card rather than inventing a path | stop and assign route owner if no card exists | `docs/validation/MONITORING_OPERATOR_ONE_PAGE_CARD_V52.md`; `docs/workups/genetics/CHR1_OPERATOR_ONE_PAGE_CARD_V52.md` |
| 9 | result-report shell | correct blank result template is selected before outputs are known | create no ad hoc result report | `docs/validation/MONITORING_VALIDATION_RESULT_REPORT_TEMPLATE_V52.md`; `docs/workups/genetics/CHR1_PACKAGE_RESULT_REPORT_TEMPLATE_V52.md` |
| 10 | final pre-analysis decision | package status is accept, partial/context, access-blocked, reject, or unscoreable | do not analyze until status is recorded | `docs/reports/THERAPEUTIC_ROUTE_DECISION_LOG_TEMPLATE_V52.md` |

## Route-Specific Next Step

| route class | next step |
|---|---|
| `monitoring_validation` | run the frozen monitoring command manifest only after V42/V44 preflight passes |
| `chr1_target_resolution` | apply the chr1 genotype-linked data spec and direction-matched blueprint |
| `chr1_modality_workup` | apply the wrong-direction control checklist before any target interpretation |
| `postpartum_secondary_biology` | run only the pre-registered postpartum harness if the package is scoreable |
| `TB_secondary_monitoring` | run only the pre-registered T/B harness if composition can be handled |
| `pharmacodynamic_context_only` | record context; do not count as response validation |
| `structure_context_only` | store as feasibility context; do not override genetics or direction blockers |
| `access_or_terms_blocked` | request allowed-use clarification; do not inspect restricted content |
| `metadata_only_or_aggregate_only` | request sample-level package or record acquisition gap |

## Stop Conditions

Stop package handling and do not analyze if:

1. access terms are unclear or restrictive;
2. raw data would need to be committed to git;
3. required fields for the chosen route are absent;
4. the package route is ambiguous after the classifier and examples;
5. the package only supports context but is being used as validation;
6. route-specific operator artifacts are missing.

## Source Artifacts

- `docs/validation/PACKAGE_CHECKSUM_INTAKE_CHECKLIST_V52.md`
- `docs/validation/MANIFEST_METADATA_VS_RAW_DATA_GIT_POLICY_V52.md`
- `docs/validation/RECEIVED_PACKAGE_FILE_NAMING_POLICY_V52.md`
- `docs/validation/VALIDATION_PACKAGE_ROUTE_CLASSIFIER_V52.tsv`
- `docs/validation/PACKAGE_ROUTE_CLASSIFIER_OPERATOR_NOTE_V52.md`
- `docs/validation/PACKAGE_ROUTE_CLASSIFIER_STATUS_DECISION_TABLE_V52.tsv`
- `docs/validation/VALIDATION_PACKAGE_ROUTE_CLASSIFIER_EXAMPLES_V52.tsv`
- `docs/validation/VALIDATION_PACKAGE_FIELD_DICTIONARY_V52.tsv`
- `docs/validation/TARGET_PACKAGE_ACCEPTANCE_CRITERIA_V52.tsv`
- `docs/reports/V52_OPERATOR_ARTIFACT_HASH_VERIFY_COMMANDS.md`
