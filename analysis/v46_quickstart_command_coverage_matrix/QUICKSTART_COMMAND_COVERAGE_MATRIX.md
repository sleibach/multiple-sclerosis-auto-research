# Quickstart Command Coverage Matrix V46

Status: quickstart command-governance matrix. No validation result and no biological claim.

Overall status: `PASS`; command rows: `34`; lint failures: `0`.

| Sequence | Artifact | README | Regression script | Smoke script | Drift parity |
|---:|---|---|---|---|---|
| 1 | `current_action_card` | `true` | `false` | `false` | `true` |
| 2 | `cold_start_operator_sequence` | `true` | `false` | `false` | `true` |
| 3 | `receipt_manifest_schema_linter` | `true` | `true` | `true` | `true` |
| 4 | `package_manifest_shape_classifier` | `true` | `true` | `true` | `true` |
| 5 | `receipt_manifest_to_command_plan_handoff` | `true` | `true` | `true` | `true` |
| 6 | `first30_decision_table` | `true` | `true` | `true` | `true` |
| 7 | `first30_status_board` | `true` | `true` | `true` | `true` |
| 8 | `status_board_schema_linter` | `true` | `true` | `true` | `true` |
| 9 | `status_board_markdown_roundtrip_renderer` | `true` | `true` | `true` | `true` |
| 10 | `returned_package_preflight_dryrun` | `true` | `true` | `true` | `true` |
| 11 | `command_order_planner` | `true` | `true` | `true` | `true` |
| 12 | `state_transition_validator` | `true` | `true` | `true` | `true` |
| 13 | `safe_interpretation_classifier` | `true` | `true` | `true` | `true` |
| 14 | `small_n_language` | `true` | `true` | `true` | `true` |
| 15 | `analyzable_pair_confidence_envelope` | `true` | `true` | `true` | `true` |
| 16 | `repair_request_templates` | `true` | `true` | `true` | `true` |
| 17 | `partial_label_repair_prioritization` | `true` | `true` | `true` | `true` |
| 18 | `first30_repair_template_coverage` | `true` | `true` | `true` | `true` |
| 19 | `result_report_safe_class_linter` | `true` | `true` | `true` | `true` |
| 20 | `report_header_metadata_linter` | `true` | `true` | `true` | `true` |
| 21 | `report_header_repair_template_coverage` | `true` | `true` | `true` | `true` |
| 22 | `safe_class_report_template_readiness` | `true` | `true` | `true` | `true` |
| 23 | `operator_transcript_fixture` | `true` | `true` | `true` | `true` |
| 24 | `returned_package_quickstart_readme` | `true` | `true` | `true` | `true` |
| 25 | `returned_package_doc_crosslink_linter` | `true` | `true` | `true` | `true` |
| 26 | `returned_package_dependency_graph` | `true` | `true` | `true` | `true` |
| 27 | `schema_fail_missing_required_column` | `true` | `true` | `true` | `true` |
| 28 | `schema_fail_raw_path` | `true` | `true` | `true` | `true` |
| 29 | `scored_canonical_to_plan` | `true` | `true` | `true` | `true` |
| 30 | `scored_noncanonical_to_adapter_branch` | `true` | `true` | `true` | `true` |
| 31 | `partial_label_to_plan_with_label_classifier` | `true` | `true` | `true` | `true` |
| 32 | `unscoreable_author_run_aggregate_to_preflight_only` | `true` | `true` | `true` | `true` |
| 33 | `terms_blocked_after_shape` | `true` | `true` | `true` | `true` |
| 34 | `unknown_score_like_filename_stops_at_schema` | `true` | `true` | `true` | `true` |

Boundary: this matrix checks command coverage only. It does not run a
validation and does not inspect returned data.
