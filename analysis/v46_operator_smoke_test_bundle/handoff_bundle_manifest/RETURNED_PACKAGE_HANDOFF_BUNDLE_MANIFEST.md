# Returned-Package Handoff Bundle Manifest V46

Status: operator navigation infrastructure. No validation result and no biological claim.

This manifest lists the returned-package artifacts in deterministic operator order.
Overall status: `PASS`; rows: `14`; lint failures: `0`.

| Order | Phase | Artifact | Role | Doc |
|---:|---|---|---|---|
| 1 | `cold_start` | `current_action_card` | Confirm the operator is still blocked only on external data and local guards are green. | `docs/validation/CURRENT_ACTION_CARD_V45.md` |
| 2 | `cold_start` | `cold_start_operator_sequence` | Run the cold-start sequence before touching a received or returned package. | `docs/validation/COLD_START_OPERATOR_SEQUENCE_V45.md` |
| 3 | `pre_touch_guard` | `receipt_manifest_schema_linter` | Verify the receipt manifest has safe non-sensitive columns and aggregate paths before classification. | `docs/validation/RECEIPT_MANIFEST_SCHEMA_LINTER_V46.md` |
| 4 | `pre_touch_guard` | `package_manifest_shape_classifier` | Classify the returned package from receipt manifest filenames and terms only. | `docs/validation/PACKAGE_MANIFEST_SHAPE_CLASSIFIER_V46.md` |
| 5 | `first_30_minutes` | `first30_decision_table` | Follow the first 30 minutes of package handling without reading score values. | `docs/validation/FIRST30_RETURNED_PACKAGE_DECISION_TABLE_V46.md` |
| 6 | `first_30_minutes` | `first30_status_board` | Summarize route, blocker, next command, and safe team wording without reading score values. | `docs/validation/FIRST30_RETURNED_PACKAGE_STATUS_BOARD_DRYRUN_V46.md` |
| 7 | `command_order` | `command_order_planner` | Generate the route-specific command order using package-state and metric-format state. | `docs/validation/RETURNED_PACKAGE_COMMAND_ORDER_PLANNER_V46.md` |
| 8 | `state_guard` | `state_transition_validator` | Verify no report/score state is reachable before required gates and safe class. | `docs/validation/RETURNED_PACKAGE_STATE_TRANSITION_VALIDATOR_V46.md` |
| 9 | `interpretation_boundary` | `safe_interpretation_classifier` | Assign the V46 safe class after all prerequisite gate summaries exist. | `docs/validation/RETURNED_PACKAGE_SAFE_INTERPRETATION_V46.md` |
| 10 | `underpowered_language` | `small_n_language` | Constrain wording for underpowered or partial-label returns. | `docs/validation/SMALL_N_CONCLUSION_LANGUAGE_V46.md` |
| 11 | `underpowered_language` | `analyzable_pair_confidence_envelope` | Map analyzable-pair counts to pass/fail/inconclusive wording constraints. | `docs/validation/ANALYZABLE_PAIR_CONFIDENCE_ENVELOPE_V46.md` |
| 12 | `repair_handoff` | `repair_request_templates` | Draft safe author-facing repair requests for blocked returned-package states. | `docs/validation/RETURN_REPAIR_REQUEST_TEMPLATES_V46.md` |
| 13 | `repair_handoff` | `first30_repair_template_coverage` | Prove every first-30 stop route has local repair or a safe author-facing template. | `docs/validation/FIRST30_REPAIR_TEMPLATE_COVERAGE_LINTER_V46.md` |
| 14 | `report_guard` | `result_report_safe_class_linter` | Ensure any report cites a safe class and avoids forbidden score language when blocked. | `docs/validation/RESULT_REPORT_SAFE_CLASS_LINTER_V46.md` |

Every row is a pre-score navigation or guard artifact. The manifest does not
authorize result interpretation; the V46 safe class and V42 pre-registration
remain the interpretation boundary.
