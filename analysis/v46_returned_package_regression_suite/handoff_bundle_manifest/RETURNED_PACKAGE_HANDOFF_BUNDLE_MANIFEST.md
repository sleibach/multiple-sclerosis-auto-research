# Returned-Package Handoff Bundle Manifest V46

Status: operator navigation infrastructure. No validation result and no biological claim.

This manifest lists the returned-package artifacts in deterministic operator order.
Overall status: `PASS`; rows: `24`; lint failures: `0`.

| Order | Phase | Artifact | Role | Doc |
|---:|---|---|---|---|
| 1 | `cold_start` | `current_action_card` | Confirm the operator is still blocked only on external data and local guards are green. | `docs/validation/CURRENT_ACTION_CARD_V45.md` |
| 2 | `cold_start` | `cold_start_operator_sequence` | Run the cold-start sequence before touching a received or returned package. | `docs/validation/COLD_START_OPERATOR_SEQUENCE_V45.md` |
| 3 | `pre_touch_guard` | `receipt_manifest_schema_linter` | Verify the receipt manifest has safe non-sensitive columns and aggregate paths before classification. | `docs/validation/RECEIPT_MANIFEST_SCHEMA_LINTER_V46.md` |
| 4 | `pre_touch_guard` | `package_manifest_shape_classifier` | Classify the returned package from receipt manifest filenames and terms only. | `docs/validation/PACKAGE_MANIFEST_SHAPE_CLASSIFIER_V46.md` |
| 5 | `pre_touch_guard` | `receipt_manifest_to_command_plan_handoff` | Map receipt-manifest lint outcomes to the next allowed classifier/planner command and hard stop. | `docs/validation/RECEIPT_MANIFEST_TO_COMMAND_PLAN_HANDOFF_V46.md` |
| 6 | `first_30_minutes` | `first30_decision_table` | Follow the first 30 minutes of package handling without reading score values. | `docs/validation/FIRST30_RETURNED_PACKAGE_DECISION_TABLE_V46.md` |
| 7 | `first_30_minutes` | `first30_status_board` | Summarize route, blocker, next command, and safe team wording without reading score values. | `docs/validation/FIRST30_RETURNED_PACKAGE_STATUS_BOARD_DRYRUN_V46.md` |
| 8 | `first_30_minutes` | `status_board_schema_linter` | Verify team-update TSV/Markdown status-board outputs stay parseable and pre-result safe. | `docs/validation/RETURNED_PACKAGE_STATUS_BOARD_SCHEMA_LINTER_V46.md` |
| 9 | `first_30_minutes` | `status_board_markdown_roundtrip_renderer` | Regenerate first-30 status-board Markdown from TSV and fail on manual Markdown drift. | `docs/validation/STATUS_BOARD_MARKDOWN_ROUNDTRIP_RENDERER_V46.md` |
| 10 | `preflight_composition` | `returned_package_preflight_dryrun` | Run one synthetic-safe command that composes schema lint, shape classification, first-30 routing, state validation, and repair coverage. | `docs/validation/RETURNED_PACKAGE_PREFLIGHT_DRYRUN_V46.md` |
| 11 | `command_order` | `command_order_planner` | Generate the route-specific command order using package-state and metric-format state. | `docs/validation/RETURNED_PACKAGE_COMMAND_ORDER_PLANNER_V46.md` |
| 12 | `state_guard` | `state_transition_validator` | Verify no report/score state is reachable before required gates and safe class. | `docs/validation/RETURNED_PACKAGE_STATE_TRANSITION_VALIDATOR_V46.md` |
| 13 | `interpretation_boundary` | `safe_interpretation_classifier` | Assign the V46 safe class after all prerequisite gate summaries exist. | `docs/validation/RETURNED_PACKAGE_SAFE_INTERPRETATION_V46.md` |
| 14 | `underpowered_language` | `small_n_language` | Constrain wording for underpowered or partial-label returns. | `docs/validation/SMALL_N_CONCLUSION_LANGUAGE_V46.md` |
| 15 | `underpowered_language` | `analyzable_pair_confidence_envelope` | Map analyzable-pair counts to pass/fail/inconclusive wording constraints. | `docs/validation/ANALYZABLE_PAIR_CONFIDENCE_ENVELOPE_V46.md` |
| 16 | `repair_handoff` | `repair_request_templates` | Draft safe author-facing repair requests for blocked returned-package states. | `docs/validation/RETURN_REPAIR_REQUEST_TEMPLATES_V46.md` |
| 17 | `repair_handoff` | `partial_label_repair_prioritization` | Map partial-label classes to repair priority, confidence band, template, and next action. | `docs/validation/PARTIAL_LABEL_REPAIR_PRIORITIZATION_V46.md` |
| 18 | `repair_handoff` | `first30_repair_template_coverage` | Prove every first-30 stop route has local repair or a safe author-facing template. | `docs/validation/FIRST30_REPAIR_TEMPLATE_COVERAGE_LINTER_V46.md` |
| 19 | `report_guard` | `result_report_safe_class_linter` | Ensure any report cites a safe class and avoids forbidden score language when blocked. | `docs/validation/RESULT_REPORT_SAFE_CLASS_LINTER_V46.md` |
| 20 | `report_guard` | `report_header_metadata_linter` | Ensure result reports include cohort token, route, terms class, safe class, and locked-rule hash before result text. | `docs/validation/REPORT_HEADER_METADATA_LINTER_V46.md` |
| 21 | `report_guard` | `report_header_repair_template_coverage` | Map every report-header metadata failure to a safe repair request before score text. | `docs/validation/REPORT_HEADER_REPAIR_TEMPLATE_COVERAGE_V46.md` |
| 22 | `report_guard` | `safe_class_report_template_readiness` | Prove every V46 safe class has an allowed report skeleton or explicit stop wording. | `docs/validation/SAFE_CLASS_REPORT_TEMPLATE_READINESS_V46.md` |
| 23 | `operator_navigation` | `returned_package_doc_crosslink_linter` | Verify every returned-package script has direct documentation and operator-route reachability. | `docs/validation/RETURNED_PACKAGE_DOC_CROSSLINK_LINTER_V46.md` |
| 24 | `operator_navigation` | `returned_package_dependency_graph` | Map dependencies across handoff, regression, smoke, and stale-output readiness artifacts. | `docs/validation/RETURNED_PACKAGE_DEPENDENCY_GRAPH_V46.md` |

Every row is a pre-score navigation or guard artifact. The manifest does not
authorize result interpretation; the V46 safe class and V42 pre-registration
remain the interpretation boundary.
