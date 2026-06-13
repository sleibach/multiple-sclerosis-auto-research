# Returned-Package Quickstart V46

Status: generated operator quickstart. No validation result and no biological claim.

This quickstart is generated from the returned-package handoff manifest and
the receipt-manifest-to-command-plan handoff. Edit those machine-readable
sources, not this Markdown, when the route changes.

## Start Here

Run these guards before touching a returned package:

```bash
.venv/bin/python scripts/v46_returned_package_regression_suite.py --outdir analysis/v46_returned_package_regression_suite --fail-on-error
.venv/bin/python scripts/v46_operator_smoke_test_bundle.py --outdir analysis/v46_operator_smoke_test_bundle --fail-on-error
.venv/bin/python scripts/v46_returned_package_handoff_bundle_manifest.py --outdir analysis/v46_returned_package_handoff_bundle_manifest --fail-on-error
```

If these commands do not pass, stop at readiness repair. Do not inspect
returned score-bearing files, labels, expression matrices, or quarantined
cohorts while resolving navigation failures.

## Operator Order

### cold_start

| Order | Artifact | Command | Primary output |
|---:|---|---|---|
| 1 | `current_action_card` | `.venv/bin/python scripts/v45_current_action_card.py --outdir analysis/manual_edit_current_action_card` | `analysis/v45_current_action_card/current_action_card_summary.json` |
| 2 | `cold_start_operator_sequence` | `.venv/bin/python scripts/v45_cold_start_operator_sequence.py --outdir analysis/v45_cold_start_operator_sequence` | `analysis/v45_cold_start_operator_sequence/cold_start_operator_sequence_summary.json` |

### pre_touch_guard

| Order | Artifact | Command | Primary output |
|---:|---|---|---|
| 3 | `receipt_manifest_schema_linter` | `.venv/bin/python scripts/v46_receipt_manifest_schema_linter.py lint --manifest <receipt_manifest.tsv> --outdir analysis/v46_receipt_manifest_schema_linter/<cohort>_<date> --fail-on-error` | `analysis/v46_receipt_manifest_schema_linter/receipt_manifest_schema_synthetic_summary.json` |
| 4 | `package_manifest_shape_classifier` | `.venv/bin/python scripts/v46_package_manifest_shape_classifier.py classify --manifest <receipt_manifest.tsv> --terms-class <TERMS_CLASS> --outdir analysis/v46_package_manifest_shape_classifier/<cohort>_<date> --fail-on-error` | `analysis/v46_package_manifest_shape_classifier/package_manifest_shape_synthetic_summary.json` |
| 5 | `receipt_manifest_to_command_plan_handoff` | `.venv/bin/python scripts/v46_receipt_manifest_to_command_plan_handoff.py --outdir analysis/v46_receipt_manifest_to_command_plan_handoff --fail-on-error` | `analysis/v46_receipt_manifest_to_command_plan_handoff/receipt_manifest_to_command_plan_handoff_summary.json` |

### first_30_minutes

| Order | Artifact | Command | Primary output |
|---:|---|---|---|
| 6 | `first30_decision_table` | `.venv/bin/python scripts/v46_first30_returned_package_decision_table.py --outdir analysis/v46_first30_returned_package_decision_table --fail-on-error` | `analysis/v46_first30_returned_package_decision_table/first30_returned_package_decision_summary.json` |
| 7 | `first30_status_board` | `.venv/bin/python scripts/v46_first30_returned_package_status_board_dryrun.py --outdir analysis/v46_first30_returned_package_status_board_dryrun --fail-on-error` | `analysis/v46_first30_returned_package_status_board_dryrun/first30_status_board_dryrun_summary.json` |
| 8 | `status_board_schema_linter` | `.venv/bin/python scripts/v46_returned_package_status_board_schema_linter.py --outdir analysis/v46_returned_package_status_board_schema_linter --fail-on-error` | `analysis/v46_returned_package_status_board_schema_linter/status_board_schema_linter_summary.json` |
| 9 | `status_board_markdown_roundtrip_renderer` | `.venv/bin/python scripts/v46_status_board_markdown_roundtrip_renderer.py --outdir analysis/v46_status_board_markdown_roundtrip_renderer --fail-on-error` | `analysis/v46_status_board_markdown_roundtrip_renderer/status_board_markdown_roundtrip_summary.json` |

### preflight_composition

| Order | Artifact | Command | Primary output |
|---:|---|---|---|
| 10 | `returned_package_preflight_dryrun` | `.venv/bin/python scripts/v46_returned_package_preflight_dryrun.py --outdir analysis/v46_returned_package_preflight_dryrun --fail-on-error` | `analysis/v46_returned_package_preflight_dryrun/returned_package_preflight_dryrun_summary.json` |

### command_order

| Order | Artifact | Command | Primary output |
|---:|---|---|---|
| 11 | `command_order_planner` | `.venv/bin/python scripts/v46_returned_package_command_order_planner.py plan --cohort-token <cohort>_<date> --package-root <returned_package_dir> --terms-capture <terms_capture_tsv> --terms-class <TERMS_CLASS> --package-kind author_run_aggregate --package-state <package_state> --metric-format-state <metric_format_state> --outdir analysis/v46_returned_package_command_order_planner/<cohort>_<date> --expect-status <PASS_or_BLOCKED>` | `analysis/v46_returned_package_command_order_planner/returned_package_command_order_synthetic_summary.json` |

### state_guard

| Order | Artifact | Command | Primary output |
|---:|---|---|---|
| 12 | `state_transition_validator` | `.venv/bin/python scripts/v46_returned_package_state_transition_validator.py --outdir analysis/v46_returned_package_state_transition_validator --fail-on-error` | `analysis/v46_returned_package_state_transition_validator/returned_package_state_transition_summary.json` |

### interpretation_boundary

| Order | Artifact | Command | Primary output |
|---:|---|---|---|
| 13 | `safe_interpretation_classifier` | `.venv/bin/python scripts/v46_returned_package_safe_interpretation.py classify --gate-summary <gate_summary> --schema-summary <schema_summary> --analyzable-summary <analyzable_summary> --metadata-summary <metadata_summary> --batch-confounder-summary <batch_summary> --terms-status PASS --outdir analysis/v46_returned_package_safe_interpretation/<cohort>_<date>` | `analysis/v46_returned_package_safe_interpretation/safe_interpretation_synthetic_summary.json` |

### underpowered_language

| Order | Artifact | Command | Primary output |
|---:|---|---|---|
| 14 | `small_n_language` | `.venv/bin/python scripts/v46_small_n_conclusion_language_table.py --outdir analysis/v46_small_n_conclusion_language` | `analysis/v46_small_n_conclusion_language/small_n_conclusion_language_summary.json` |
| 15 | `analyzable_pair_confidence_envelope` | `.venv/bin/python scripts/v46_analyzable_pair_confidence_envelope.py --outdir analysis/v46_analyzable_pair_confidence_envelope --fail-on-error` | `analysis/v46_analyzable_pair_confidence_envelope/analyzable_pair_confidence_envelope_summary.json` |

### repair_handoff

| Order | Artifact | Command | Primary output |
|---:|---|---|---|
| 16 | `repair_request_templates` | `.venv/bin/python scripts/v46_return_repair_request_templates.py --outdir analysis/v46_return_repair_request_templates --fail-on-error` | `analysis/v46_return_repair_request_templates/return_repair_request_templates_summary.json` |
| 17 | `partial_label_repair_prioritization` | `.venv/bin/python scripts/v46_partial_label_repair_prioritization.py --outdir analysis/v46_partial_label_repair_prioritization --fail-on-error` | `analysis/v46_partial_label_repair_prioritization/partial_label_repair_prioritization_summary.json` |
| 18 | `first30_repair_template_coverage` | `.venv/bin/python scripts/v46_first30_repair_template_coverage_linter.py --outdir analysis/v46_first30_repair_template_coverage_linter --fail-on-error` | `analysis/v46_first30_repair_template_coverage_linter/first30_repair_template_coverage_summary.json` |

### report_guard

| Order | Artifact | Command | Primary output |
|---:|---|---|---|
| 19 | `result_report_safe_class_linter` | `.venv/bin/python scripts/v46_result_report_safe_class_linter.py synthetic-check --outdir analysis/v46_result_report_safe_class_linter --fail-on-error` | `analysis/v46_result_report_safe_class_linter/result_report_safe_class_synthetic_summary.json` |
| 20 | `report_header_metadata_linter` | `.venv/bin/python scripts/v46_report_header_metadata_linter.py synthetic-check --outdir analysis/v46_report_header_metadata_linter --fail-on-error` | `analysis/v46_report_header_metadata_linter/report_header_metadata_synthetic_summary.json` |
| 21 | `report_header_repair_template_coverage` | `.venv/bin/python scripts/v46_report_header_repair_template_coverage.py --outdir analysis/v46_report_header_repair_template_coverage --fail-on-error` | `analysis/v46_report_header_repair_template_coverage/report_header_repair_template_coverage_summary.json` |
| 22 | `safe_class_report_template_readiness` | `.venv/bin/python scripts/v46_safe_class_report_template_readiness.py --outdir analysis/v46_safe_class_report_template_readiness --fail-on-error` | `analysis/v46_safe_class_report_template_readiness/safe_class_report_template_readiness_summary.json` |

### operator_navigation

| Order | Artifact | Command | Primary output |
|---:|---|---|---|
| 23 | `operator_transcript_fixture` | `.venv/bin/python scripts/v46_operator_transcript_fixture.py --outdir analysis/v46_operator_transcript_fixture --fail-on-error` | `analysis/v46_operator_transcript_fixture/operator_transcript_fixture_summary.json` |
| 24 | `returned_package_quickstart_readme` | `.venv/bin/python scripts/v46_returned_package_quickstart_readme.py --outdir analysis/v46_returned_package_quickstart_readme --fail-on-error` | `analysis/v46_returned_package_quickstart_readme/returned_package_quickstart_summary.json` |
| 25 | `returned_package_doc_crosslink_linter` | `.venv/bin/python scripts/v46_returned_package_doc_crosslink_linter.py --outdir analysis/v46_returned_package_doc_crosslink_linter --fail-on-error` | `analysis/v46_returned_package_doc_crosslink_linter/returned_package_doc_crosslink_summary.json` |
| 26 | `returned_package_dependency_graph` | `.venv/bin/python scripts/v46_returned_package_dependency_graph.py --outdir analysis/v46_returned_package_dependency_graph --fail-on-error` | `analysis/v46_returned_package_dependency_graph/returned_package_dependency_summary.json` |

## Receipt-Manifest Branch Examples

These examples are generated from the handoff table and show the next
command or stop condition without reading score values.

| Case | Expected plan status | Terminal stage | Stop condition | Command |
|---|---|---|---|---|
| `schema_fail_missing_required_column` | `NOT_RUN` | `STOP_RECEIPT_MANIFEST_REPAIR` | receipt_manifest_schema_linter overall_status is not PASS; request manifest repair before any classification | `NOT_ALLOWED` |
| `schema_fail_raw_path` | `NOT_RUN` | `STOP_RECEIPT_MANIFEST_REPAIR` | receipt_manifest_schema_linter overall_status is not PASS; request manifest repair before any classification | `NOT_ALLOWED` |
| `scored_canonical_to_plan` | `PASS` | `COMMAND_PLAN_WRITTEN` | continue through command-order planner stop_if fields; no score interpretation until safe class permits wording | `.venv/bin/python scripts/v46_returned_package_command_order_planner.py plan --cohort-token scored_canonical_to_plan --package-root <returned_aggregate_package_dir> --terms-capture <terms_capture_tsv> --terms-class AGGREGATE_ONLY_LOCAL_PREFLIGHT --package-kind author_run_aggregate --package-state scored --metric-format-state canonical --outdir analysis/v46_receipt_manifest_to_command_plan_handoff/scored_canonical_to_plan/command_order_plan --expect-status PASS` |
| `scored_noncanonical_to_adapter_branch` | `PASS` | `COMMAND_PLAN_WRITTEN` | continue through command-order planner stop_if fields; no score interpretation until safe class permits wording | `.venv/bin/python scripts/v46_returned_package_command_order_planner.py plan --cohort-token scored_noncanonical_to_adapter_branch --package-root <returned_aggregate_package_dir> --terms-capture <terms_capture_tsv> --terms-class AGGREGATE_ONLY_LOCAL_PREFLIGHT --package-kind author_run_aggregate --package-state scored --metric-format-state noncanonical --outdir analysis/v46_receipt_manifest_to_command_plan_handoff/scored_noncanonical_to_adapter_branch/command_order_plan --expect-status PASS` |
| `partial_label_to_plan_with_label_classifier` | `PASS` | `COMMAND_PLAN_WRITTEN` | continue through command-order planner stop_if fields; no score interpretation until safe class permits wording | `.venv/bin/python scripts/v46_returned_package_command_order_planner.py plan --cohort-token partial_label_to_plan_with_label_classifier --package-root <returned_aggregate_package_dir> --terms-capture <terms_capture_tsv> --terms-class AGGREGATE_ONLY_LOCAL_PREFLIGHT --package-kind author_run_aggregate --package-state scored --metric-format-state canonical --outdir analysis/v46_receipt_manifest_to_command_plan_handoff/partial_label_to_plan_with_label_classifier/command_order_plan --expect-status PASS` |
| `unscoreable_author_run_aggregate_to_preflight_only` | `PASS` | `COMMAND_PLAN_WRITTEN` | continue through command-order planner stop_if fields; no score interpretation until safe class permits wording | `.venv/bin/python scripts/v46_returned_package_command_order_planner.py plan --cohort-token unscoreable_author_run_aggregate_to_preflight_only --package-root <returned_aggregate_package_dir> --terms-capture <terms_capture_tsv> --terms-class AUTHOR_RUN_ONLY --package-kind author_run_aggregate --package-state unscoreable --metric-format-state canonical --outdir analysis/v46_receipt_manifest_to_command_plan_handoff/unscoreable_author_run_aggregate_to_preflight_only/command_order_plan --expect-status PASS` |
| `terms_blocked_after_shape` | `BLOCKED` | `STOP_TERMS_BLOCK` | command-order planner writes stop_terms_block; no package gate, schema check, score reading, or interpretation | `.venv/bin/python scripts/v46_returned_package_command_order_planner.py plan --cohort-token terms_blocked_after_shape --package-root <returned_aggregate_package_dir> --terms-capture <terms_capture_tsv> --terms-class NO_PROCESSING_ALLOWED --package-kind author_run_aggregate --package-state scored --metric-format-state canonical --outdir analysis/v46_receipt_manifest_to_command_plan_handoff/terms_blocked_after_shape/command_order_plan --expect-status BLOCKED` |
| `unknown_score_like_filename_stops_at_schema` | `NOT_RUN` | `STOP_RECEIPT_MANIFEST_REPAIR` | receipt_manifest_schema_linter overall_status is not PASS; request manifest repair before any classification | `NOT_ALLOWED` |

## Interpretation Boundary

This quickstart does not authorize any result wording. The V46 safe class,
the result-report header linter, and the frozen V42 pre-registration remain
the boundary before any result text can be drafted.
