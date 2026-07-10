# Therapeutic Package Handoff Bundle Index V52

Date: 2026-07-10

Status: operational navigation aid. This document adds no evidence, changes no
validation rule, and authorizes no new analysis. It groups V52 operator-facing
artifacts into handoff bundles so a package recipient or operator can use the
right documents without mixing routes.

## Bundle 1: Universal Intake

Use for every incoming package before route-specific work.

| artifact | purpose |
|---|---|
| `docs/validation/PACKAGE_CHECKSUM_INTAKE_CHECKLIST_V52.md` | access terms, quarantine, checksum, and no-large-file intake |
| `docs/validation/INCOMING_PACKAGE_PREFLIGHT_CHECKLIST_V52.md` | ordered pre-analysis path from terms to route decision |
| `docs/validation/VALIDATION_PACKAGE_ROUTE_CLASSIFIER_V52.tsv` | route incoming package to validation, chr1, secondary, context, or reject |
| `docs/validation/VALIDATION_PACKAGE_ROUTE_CLASSIFIER_EXAMPLES_V52.tsv` | worked package-route examples |
| `docs/validation/VALIDATION_PACKAGE_FIELD_DICTIONARY_V52.tsv` | required and optional fields by route |
| `docs/validation/TARGET_PACKAGE_ACCEPTANCE_CRITERIA_V52.tsv` | accept, partial, reject, or unscoreable criteria |

## Bundle 2: Monitoring Validation

Use only after the classifier returns `monitoring_validation`.

| artifact | purpose |
|---|---|
| `docs/validation/MONITORING_MINIMUM_VIABLE_PACKAGE_CHECKLIST_V52.md` | required versus strongly preferred fields for paired PBMC response packages |
| `docs/validation/MONITORING_OPERATOR_ONE_PAGE_CARD_V52.md` | operator quick card from receipt to result class |
| `docs/validation/MONITORING_VALIDATION_COMMAND_MANIFEST_V52.md` | exact frozen command order |
| `docs/validation/MONITORING_VALIDATION_DECISION_TREE_V52.md` | mechanical pass, fail, inconclusive, or unscoreable routing |
| `docs/validation/MONITORING_VALIDATION_RESULT_REPORT_TEMPLATE_V52.md` | blank result-report shell selected before outputs are known |
| `docs/validation/MONITORING_PUBLIC_WORDING_TABLE_V52.tsv` | safe public wording by result class |

## Bundle 3: Chr1 Target-Resolution Handoff

Use only after the classifier returns `chr1_target_resolution` or
`chr1_modality_workup`.

| artifact | purpose |
|---|---|
| `docs/workups/genetics/CHR1_GENOTYPE_LINKED_DATA_SPEC_V52.md` | future data package needed to resolve candidate gene, cell state, and direction |
| `docs/workups/genetics/CHR1_DIRECTION_MATCHED_EXPERIMENT_BLUEPRINT_V52.md` | staged target-resolution and perturbation flow |
| `docs/workups/genetics/CHR1_TARGET_RESOLUTION_DECISION_COMPACT_V52.tsv` | compact no-go, ambiguous, direction-supported, and reopen states |
| `docs/workups/genetics/CHR1_WRONG_DIRECTION_CONTROL_CHECKLIST_V52.md` | labels and interpretation for wrong-direction controls |
| `docs/workups/genetics/CHR1_OPERATOR_ONE_PAGE_CARD_V52.md` | operator quick card for chr1 packages |
| `docs/workups/genetics/CHR1_PACKAGE_RESULT_REPORT_TEMPLATE_V52.md` | blank chr1 package result shell |
| `docs/workups/genetics/CHR1_NO_GO_COMMUNICATION_APPENDIX_V52.md` | collaborator-safe no-go wording |

## Bundle 4: Route Governance And Drift Checks

Use before external handoff or route-status update.

| artifact | purpose |
|---|---|
| `docs/reports/THERAPEUTIC_PATH_SUMMARY_CARD_V52.md` | medical-team bottom line |
| `docs/reports/THERAPEUTIC_PATH_V52.md` | full therapeutic-path synthesis |
| `docs/reports/THERAPEUTIC_ROUTE_STATUS_DASHBOARD_V52.tsv` | compact route status table |
| `docs/reports/THERAPEUTIC_ROUTE_DECISION_LOG_TEMPLATE_V52.md` | future route-status change shell |
| `docs/reports/POST_VALIDATION_ROUTE_UPDATE_PLAYBOOK_V52.md` | route-status transition rules after future outcomes |
| `docs/reports/V52_OPERATOR_ARTIFACT_HASH_SNAPSHOT.tsv` | stable operator artifact hash snapshot |
| `docs/reports/V52_OPERATOR_ARTIFACT_HASH_VERIFY_COMMANDS.md` | command to check the hash snapshot |

## Non-Bundle Context

AlphaFold DB records and external literature context stay in their segregated
context layer. They may be referenced when explaining tractability limits, but
they are not part of a validation package and do not replace any required
genetics, response, or perturbation evidence.

## Handoff Rule

Send only the bundle matching the package route plus the universal intake bundle.
Do not send route-specific artifacts for a route the package did not qualify for,
because that invites post-hoc reinterpretation.
