#!/usr/bin/env python3
"""Detect stale V45 readiness outputs based on source/output mtimes.

This is infrastructure governance only. It does not rerun checks; it reports
which generated readiness artifacts should be refreshed.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v45_readiness_stale_output_detector"

CHECKS = [
    {
        "artifact": "collaborator_path_resolver",
        "sources": [
            "docs/validation/COLLABORATOR_VALIDATION_PACKAGE_README_V45.md",
            "docs/validation/AUTHOR_RUN_PACKET_BUNDLE_INDEX_V45.md",
            "analysis/v45_collaborator_package/collaborator_package_manifest.tsv",
            "analysis/v45_author_run_packet_bundle/author_run_packet_bundle_index.tsv",
            "scripts/v45_collaborator_package_path_resolver.py",
        ],
        "outputs": [
            "analysis/v45_collaborator_path_resolver/live_sources/collaborator_package_path_resolution_summary.json",
            "analysis/v45_collaborator_path_resolver/live_sources/collaborator_package_path_resolution.tsv",
        ],
        "refresh_command": ".venv/bin/python scripts/v45_collaborator_package_path_resolver.py synthetic-check --outdir analysis/v45_collaborator_path_resolver",
    },
    {
        "artifact": "followup_due_board",
        "sources": [
            "analysis/v45_outbound_data_requests/request_tracker.tsv",
            "docs/validation/input_schemas/V45_request_sent_log_template.tsv",
            "scripts/v45_followup_due_board.py",
        ],
        "outputs": [
            "analysis/v45_followup_due_board/live_template/followup_due_board_summary.json",
            "analysis/v45_followup_due_board/live_template/followup_due_board.tsv",
        ],
        "refresh_command": ".venv/bin/python scripts/v45_followup_due_board.py --outdir analysis/v45_followup_due_board/live_template",
    },
    {
        "artifact": "external_blocker_board",
        "sources": [
            "analysis/v45_live_cohort_acquisition_index/live_cohort_acquisition_index.tsv",
            "analysis/v45_outbound_data_requests/request_tracker.tsv",
            "analysis/v45_received_data_triage/received_data_triage_status.tsv",
            "analysis/v45_followup_due_board/live_template/followup_due_board.tsv",
            "scripts/v45_external_blocker_board.py",
        ],
        "outputs": [
            "analysis/v45_external_blocker_board/external_blocker_board_summary.json",
            "analysis/v45_external_blocker_board/external_blocker_board.tsv",
        ],
        "refresh_command": ".venv/bin/python scripts/v45_external_blocker_board.py --outdir analysis/v45_external_blocker_board",
    },
    {
        "artifact": "external_blocker_escalation_matrix",
        "sources": [
            "analysis/v45_external_blocker_board/external_blocker_board.tsv",
            "analysis/v45_current_action_card/current_action_card.tsv",
            "analysis/v45_followup_due_board/live_template/followup_due_board.tsv",
            "scripts/v45_external_blocker_escalation_matrix.py",
        ],
        "outputs": [
            "analysis/v45_external_blocker_escalation_matrix/external_blocker_escalation_summary.json",
            "analysis/v45_external_blocker_escalation_matrix/external_blocker_escalation_matrix.tsv",
        ],
        "refresh_command": ".venv/bin/python scripts/v45_external_blocker_escalation_matrix.py --outdir analysis/v45_external_blocker_escalation_matrix",
    },
    {
        "artifact": "followup_escalation_packets",
        "sources": [
            "analysis/v45_followup_due_board/live_template/followup_due_board.tsv",
            "analysis/v45_external_blocker_escalation_matrix/external_blocker_escalation_matrix.tsv",
            "scripts/v45_followup_escalation_packet_generator.py",
        ],
        "outputs": [
            "analysis/v45_followup_escalation_packets/live/followup_escalation_packet_summary.json",
            "analysis/v45_followup_escalation_packets/live/followup_escalation_packet_index.tsv",
        ],
        "refresh_command": ".venv/bin/python scripts/v45_followup_escalation_packet_generator.py --outdir analysis/v45_followup_escalation_packets/live",
    },
    {
        "artifact": "outbound_request_packet_integrity",
        "sources": [
            "analysis/v45_external_blocker_board/external_blocker_board.tsv",
            "scripts/v45_outbound_request_packet_integrity.py",
            "docs/validation/outbound_requests/author_run_fallback_ready_to_send_V45.md",
            "docs/validation/outbound_requests/gafson_dmf_ready_to_send_V45.md",
            "docs/validation/outbound_requests/gse228330_ocrelizumab_ready_to_send_V45.md",
            "docs/validation/outbound_requests/karolinska_dmf_ready_to_send_V45.md",
        ],
        "outputs": [
            "analysis/v45_outbound_request_packet_integrity/live/outbound_request_packet_integrity_summary.json",
            "analysis/v45_outbound_request_packet_integrity/live/outbound_request_packet_manifest.tsv",
            "analysis/v45_outbound_request_packet_integrity/live/outbound_request_packet_issues.tsv",
        ],
        "refresh_command": ".venv/bin/python scripts/v45_outbound_request_packet_integrity.py --outdir analysis/v45_outbound_request_packet_integrity/live --expect-status PASS",
    },
    {
        "artifact": "followup_message_templates",
        "sources": [
            "analysis/v45_followup_due_board/live_template/followup_due_board.tsv",
            "scripts/v45_followup_message_template_generator.py",
        ],
        "outputs": [
            "analysis/v45_followup_message_templates/live_template/followup_message_template_summary.json",
            "analysis/v45_followup_message_templates/live_template/followup_message_template_index.tsv",
        ],
        "refresh_command": ".venv/bin/python scripts/v45_followup_message_template_generator.py --board analysis/v45_followup_due_board/live_template/followup_due_board.tsv --outdir analysis/v45_followup_message_templates/live_template",
    },
    {
        "artifact": "send_log_intake_template",
        "sources": [
            "analysis/v45_current_action_card/current_action_card.tsv",
            "scripts/v45_send_log_intake_template.py",
        ],
        "outputs": [
            "analysis/v45_send_log_intake_template/send_log_intake_template_summary.json",
            "analysis/v45_send_log_intake_template/send_log_intake_template.tsv",
            "analysis/v45_send_log_intake_template/request_sent_updater_dryrun/request_sent_update_summary.json",
        ],
        "refresh_command": ".venv/bin/python scripts/v45_send_log_intake_template.py --outdir analysis/v45_send_log_intake_template && .venv/bin/python scripts/v45_request_sent_updater.py --sent-log analysis/v45_send_log_intake_template/send_log_intake_template.tsv --outdir analysis/v45_send_log_intake_template/request_sent_updater_dryrun",
    },
    {
        "artifact": "route_arrival_packets",
        "sources": [
            "analysis/v45_live_cohort_acquisition_index/live_cohort_acquisition_index.tsv",
            "analysis/v45_outbound_data_requests/request_tracker.tsv",
            "scripts/v45_route_arrival_packet_generator.py",
        ],
        "outputs": [
            "analysis/v45_route_arrival_packets/route_arrival_packet_summary.json",
            "analysis/v45_route_arrival_packets/route_arrival_packet_index.tsv",
        ],
        "refresh_command": ".venv/bin/python scripts/v45_route_arrival_packet_generator.py --outdir analysis/v45_route_arrival_packets",
    },
    {
        "artifact": "route_packet_integrity_manifest",
        "sources": [
            "analysis/v45_route_arrival_packets/route_arrival_packet_summary.json",
            "analysis/v45_route_arrival_packets/route_arrival_packet_index.tsv",
            "scripts/v45_route_packet_integrity_manifest.py",
        ],
        "outputs": [
            "analysis/v45_route_packet_integrity_manifest/live/route_packet_integrity_summary.json",
            "analysis/v45_route_packet_integrity_manifest/live/route_packet_integrity_manifest.tsv",
        ],
        "refresh_command": ".venv/bin/python scripts/v45_route_packet_integrity_manifest.py --outdir analysis/v45_route_packet_integrity_manifest/live --expect-status PASS",
    },
    {
        "artifact": "cross_route_readiness_linter",
        "sources": [
            "analysis/v45_external_blocker_board/external_blocker_board.tsv",
            "analysis/v45_route_arrival_packets/route_arrival_packet_index.tsv",
            "analysis/v45_validation_command_runner/gafson_primary_plan/command_plan_summary.json",
            "analysis/v45_validation_command_runner/karolinska_primary_plan/command_plan_summary.json",
            "analysis/v45_validation_command_runner/gse228330_pharmacodynamic_plan/command_plan_summary.json",
            "analysis/v45_author_run_return_gate_runner/synthetic_check_summary.json",
            "scripts/v45_cross_route_readiness_linter.py",
        ],
        "outputs": [
            "analysis/v45_cross_route_readiness_linter/live/cross_route_readiness_lint_summary.json",
            "analysis/v45_cross_route_readiness_linter/live/cross_route_readiness_lint.tsv",
            "analysis/v45_cross_route_readiness_linter/live/cross_route_readiness_issues.tsv",
        ],
        "refresh_command": ".venv/bin/python scripts/v45_cross_route_readiness_linter.py --outdir analysis/v45_cross_route_readiness_linter/live --expect-status PASS",
    },
    {
        "artifact": "state_machine_transition_validator",
        "sources": [
            "analysis/v45_received_data_triage/received_data_triage_status.tsv",
            "analysis/v45_external_blocker_board/external_blocker_board.tsv",
            "analysis/v45_followup_due_board/live_template/followup_due_board.tsv",
            "analysis/v45_readiness_status_dashboard/readiness_status_dashboard_summary.json",
            "scripts/v45_state_machine_validator.py",
        ],
        "outputs": [
            "analysis/v45_state_machine_validator/live/state_machine_validator_summary.json",
            "analysis/v45_state_machine_validator/live/route_state_validation.tsv",
        ],
        "refresh_command": ".venv/bin/python scripts/v45_state_machine_validator.py --outdir analysis/v45_state_machine_validator/live --expect-status PASS",
    },
    {
        "artifact": "received_package_decision_tree",
        "sources": [
            "analysis/v45_current_action_card/current_action_card.tsv",
            "analysis/v45_state_machine_validator/live/route_state_validation.tsv",
            "analysis/v45_state_machine_validator/live/state_machine_validator_summary.json",
            "scripts/v45_received_package_decision_tree.py",
        ],
        "outputs": [
            "analysis/v45_received_package_decision_tree/live/received_package_decision_tree_summary.json",
            "analysis/v45_received_package_decision_tree/live/received_package_decision_tree.tsv",
            "analysis/v45_received_package_decision_tree/live/received_package_decision_tree_issues.tsv",
        ],
        "refresh_command": ".venv/bin/python scripts/v45_received_package_decision_tree.py --outdir analysis/v45_received_package_decision_tree/live --expect-status PASS",
    },
    {
        "artifact": "current_action_card",
        "sources": [
            "analysis/v45_external_blocker_board/external_blocker_board.tsv",
            "analysis/v45_followup_due_board/live_template/followup_due_board.tsv",
            "analysis/v45_readiness_status_dashboard/readiness_status_dashboard_summary.json",
            "analysis/v45_state_machine_validator/live/state_machine_validator_summary.json",
            "analysis/v45_route_packet_integrity_manifest/live/route_packet_integrity_summary.json",
            "analysis/v45_precommit_readiness/precommit_readiness_summary.json",
            "analysis/v46_returned_package_regression_suite/returned_package_regression_summary.json",
            "analysis/v46_operator_smoke_test_bundle/operator_smoke_test_summary.json",
            "scripts/v45_current_action_card.py",
        ],
        "outputs": [
            "analysis/v45_current_action_card/current_action_card_summary.json",
            "analysis/v45_current_action_card/current_action_card.tsv",
            "analysis/v45_current_action_card/CURRENT_ACTION_CARD.md",
        ],
        "refresh_command": ".venv/bin/python scripts/v45_current_action_card.py --outdir analysis/v45_current_action_card",
    },
    {
        "artifact": "cold_start_operator_sequence",
        "sources": [
            "analysis/v45_current_action_card/current_action_card.tsv",
            "analysis/v45_received_package_decision_tree/live/received_package_decision_tree.tsv",
            "analysis/v45_route_arrival_packets/route_arrival_packet_index.tsv",
            "analysis/v45_validation_command_runner/gafson_primary_plan/command_plan.md",
            "analysis/v45_validation_command_runner/karolinska_primary_plan/command_plan.md",
            "analysis/v45_validation_command_runner/gse228330_pharmacodynamic_plan/command_plan.md",
            "analysis/v46_returned_package_regression_suite/returned_package_regression_summary.json",
            "scripts/v45_cold_start_operator_sequence.py",
        ],
        "outputs": [
            "analysis/v45_cold_start_operator_sequence/cold_start_operator_sequence_summary.json",
            "analysis/v45_cold_start_operator_sequence/cold_start_operator_sequence.tsv",
            "analysis/v45_cold_start_operator_sequence/COLD_START_OPERATOR_SEQUENCE.md",
        ],
        "refresh_command": ".venv/bin/python scripts/v45_cold_start_operator_sequence.py --outdir analysis/v45_cold_start_operator_sequence",
    },
    {
        "artifact": "author_run_bundle_dryrun_manifest",
        "sources": [
            "analysis/v45_author_run_packet_bundle/author_run_packet_bundle_index.tsv",
            "analysis/v45_author_run_packet_checksums/write/author_run_packet_sha256_manifest.tsv",
            "analysis/v45_author_run_packet_checksums/verify/author_run_packet_checksum_verify.tsv",
            "analysis/v45_command_plan_consistency/command_plan_consistency_summary.json",
            "analysis/v45_current_action_card/current_action_card.tsv",
            "scripts/v45_author_run_bundle_dryrun_manifest.py",
        ],
        "outputs": [
            "analysis/v45_author_run_bundle_dryrun_manifest/live/author_run_bundle_dryrun_summary.json",
            "analysis/v45_author_run_bundle_dryrun_manifest/live/author_run_bundle_dryrun_manifest.tsv",
        ],
        "refresh_command": ".venv/bin/python scripts/v45_author_run_bundle_dryrun_manifest.py --outdir analysis/v45_author_run_bundle_dryrun_manifest/live --expect-status PASS",
    },
    {
        "artifact": "generated_checker_registry",
        "sources": [
            "scripts/v45_generated_checker_registry.py",
            "docs/validation/GENERATED_CHECKER_REGISTRY_V45.md",
        ],
        "outputs": [
            "analysis/v45_generated_checker_registry/generated_checker_registry_summary.json",
            "analysis/v45_generated_checker_registry/generated_checker_registry.tsv",
        ],
        "refresh_command": ".venv/bin/python scripts/v45_generated_checker_registry.py --outdir analysis/v45_generated_checker_registry",
    },
    {
        "artifact": "operational_handoff_index",
        "sources": [
            "docs/validation/input_schemas/V45_operational_handoff_index.tsv",
        ],
        "outputs": [
            "docs/validation/V45_OPERATIONAL_HANDOFF_INDEX.md",
        ],
        "refresh_command": "update docs/validation/V45_OPERATIONAL_HANDOFF_INDEX.md to match docs/validation/input_schemas/V45_operational_handoff_index.tsv",
    },
    {
        "artifact": "readiness_status_dashboard",
        "sources": [
            "analysis/v45_outbound_data_requests/request_tracker.tsv",
            "analysis/v45_received_data_triage/received_data_triage_status.tsv",
            "analysis/v45_precommit_readiness/precommit_readiness_summary.json",
            "analysis/v45_collaborator_path_resolver/live_sources/collaborator_package_path_resolution_summary.json",
            "analysis/v45_followup_due_board/live_template/followup_due_board_summary.json",
            "analysis/v45_external_blocker_board/external_blocker_board_summary.json",
            "analysis/v45_handoff_completeness/handoff_completeness_summary.json",
            "analysis/v45_handoff_completeness_scored_missing/handoff_completeness_summary.json",
            "scripts/v45_readiness_status_dashboard.py",
        ],
        "outputs": [
            "analysis/v45_readiness_status_dashboard/readiness_status_dashboard_summary.json",
            "analysis/v45_readiness_status_dashboard/readiness_status_dashboard.tsv",
        ],
        "refresh_command": ".venv/bin/python scripts/v45_readiness_status_dashboard.py --outdir analysis/v45_readiness_status_dashboard",
    },
    {
        "artifact": "generated_doc_freshness_linter",
        "sources": [
            "analysis/v45_artifact_index/summary.json",
            "analysis/v45_compute_storage_summary/summary.json",
            "analysis/v45_synthetic_artifact_index/summary.json",
            "analysis/v45_precommit_readiness/precommit_readiness_summary.json",
            "analysis/v45_regression_aggregator/regression_aggregator_summary.json",
            "docs/validation/V45_GOVERNANCE_REFRESH.md",
            "docs/validation/V45_ARTIFACT_INDEX.md",
            "docs/validation/V45_COMPUTE_STORAGE_SUMMARY.md",
            "docs/validation/PRECOMMIT_READINESS_CHECKLIST_V45.md",
            "docs/validation/V45_READINESS_CHANGELOG.md",
            "docs/validation/SYNTHETIC_ARTIFACT_RETENTION_INDEX_V45.md",
            "docs/validation/SYNTHETIC_OUTPUT_RETENTION_POLICY_V45.md",
            "docs/validation/V45_REGRESSION_AGGREGATOR.md",
            "docs/validation/READINESS_STALE_OUTPUT_DETECTOR_V45.md",
            "scripts/v45_generated_doc_freshness_linter.py",
            "scripts/v45_readiness_stale_output_detector.py",
        ],
        "outputs": [
            "analysis/v45_generated_doc_freshness_linter/generated_doc_freshness_summary.json",
            "analysis/v45_generated_doc_freshness_linter/generated_doc_freshness_lint.tsv",
        ],
        "refresh_command": ".venv/bin/python scripts/v45_generated_doc_freshness_linter.py --outdir analysis/v45_generated_doc_freshness_linter",
    },
    {
        "artifact": "no_score_before_gates_linter",
        "sources": [
            "docs/validation/FIRST_24H_RECEIVED_DATA_OPERATOR_CHECKLIST_V45.md",
            "docs/validation/HARNESS_READY_DECISION_TEMPLATE_V45.md",
            "docs/validation/VALIDATION_COMMAND_RUNNER_V45.md",
            "docs/validation/COLLABORATOR_VALIDATION_PACKAGE_README_V45.md",
            "docs/validation/EXTERNAL_BLOCKER_BOARD_V45.md",
            "analysis/v45_route_arrival_packets/gafson_dmf_2018_arrival_packet.md",
            "analysis/v45_route_arrival_packets/karolinska_dmf_ros_2019_arrival_packet.md",
            "analysis/v45_route_arrival_packets/gse228330_ocrelizumab_pbmc_arrival_packet.md",
            "analysis/v45_route_arrival_packets/any_author_run_fallback_arrival_packet.md",
            "scripts/v45_no_score_before_gates_linter.py",
        ],
        "outputs": [
            "analysis/v45_no_score_before_gates_linter/live/no_score_before_gates_summary.json",
            "analysis/v45_no_score_before_gates_linter/live/no_score_before_gates_lint.tsv",
            "analysis/v45_no_score_before_gates_linter/synthetic_bad/no_score_before_gates_summary.json",
            "analysis/v45_no_score_before_gates_linter/synthetic_bad/no_score_before_gates_lint.tsv",
        ],
        "refresh_command": ".venv/bin/python scripts/v45_no_score_before_gates_linter.py --outdir analysis/v45_no_score_before_gates_linter/live --expect-status PASS && .venv/bin/python scripts/v45_no_score_before_gates_linter.py --outdir analysis/v45_no_score_before_gates_linter/synthetic_bad --synthetic-case bad --expect-status FAIL",
    },
    {
        "artifact": "synthetic_received_package_dryrun",
        "sources": [
            "docs/validation/input_schemas/V45_first_24h_operator_status_template.tsv",
            "scripts/v45_synthetic_received_package_dryrun.py",
            "scripts/v45_received_status_updater.py",
            "scripts/v45_state_machine_validator.py",
            "scripts/v45_received_package_decision_tree.py",
        ],
        "outputs": [
            "analysis/v45_synthetic_received_package_dryrun/synthetic_received_package_dryrun_summary.json",
            "analysis/v45_synthetic_received_package_dryrun/received_status_updater/received_data_triage_status.proposed.tsv",
            "analysis/v45_synthetic_received_package_dryrun/state_machine_validator/route_state_validation.tsv",
            "analysis/v45_synthetic_received_package_dryrun/received_package_decision_tree/received_package_decision_tree.tsv",
        ],
        "refresh_command": ".venv/bin/python scripts/v45_synthetic_received_package_dryrun.py --outdir analysis/v45_synthetic_received_package_dryrun",
    },
    {
        "artifact": "v46_terms_governance_matrix",
        "sources": [
            "docs/validation/input_schemas/V45_data_use_terms_capture_template.tsv",
            "docs/validation/TERMS_GOVERNANCE_MATRIX_V46.md",
            "scripts/v46_terms_governance_matrix.py",
        ],
        "outputs": [
            "analysis/v46_terms_governance_matrix/terms_governance_synthetic_summary.json",
            "analysis/v46_terms_governance_matrix/terms_governance_synthetic_cases.tsv",
        ],
        "refresh_command": ".venv/bin/python scripts/v46_terms_governance_matrix.py synthetic-check --outdir analysis/v46_terms_governance_matrix",
    },
    {
        "artifact": "v46_metric_format_adapter",
        "sources": [
            "analysis/v45_author_run_output_check/synthetic_complete_author_run_package/validation_summary.json",
            "docs/validation/AUTHOR_RUN_METRIC_FORMAT_ADAPTER_V46.md",
            "scripts/v46_author_run_metric_format_adapter.py",
        ],
        "outputs": [
            "analysis/v46_author_run_metric_format_adapter/metric_format_adapter_synthetic_summary.json",
            "analysis/v46_author_run_metric_format_adapter/metric_format_adapter_synthetic_checks.tsv",
        ],
        "refresh_command": ".venv/bin/python scripts/v46_author_run_metric_format_adapter.py synthetic-check --outdir analysis/v46_author_run_metric_format_adapter",
    },
    {
        "artifact": "v46_partial_label_return_classifier",
        "sources": [
            "analysis/v45_route_analyzable_pair_calculator/route_analyzable_pair_synthetic_summary.json",
            "docs/validation/PARTIAL_LABEL_RETURN_CLASSIFIER_V46.md",
            "scripts/v46_partial_label_return_classifier.py",
        ],
        "outputs": [
            "analysis/v46_partial_label_return_classifier/partial_label_synthetic_summary.json",
            "analysis/v46_partial_label_return_classifier/partial_label_synthetic_cases.tsv",
        ],
        "refresh_command": ".venv/bin/python scripts/v46_partial_label_return_classifier.py synthetic-check --outdir analysis/v46_partial_label_return_classifier",
    },
    {
        "artifact": "v46_safe_interpretation_classifier",
        "sources": [
            "analysis/v45_author_run_return_gate_runner/synthetic_check_summary.json",
            "analysis/v45_author_run_schema_validator/synthetic_author_run_schema_summary.json",
            "analysis/v45_route_analyzable_pair_calculator/route_analyzable_pair_synthetic_summary.json",
            "docs/validation/RETURNED_PACKAGE_SAFE_INTERPRETATION_V46.md",
            "scripts/v46_returned_package_safe_interpretation.py",
        ],
        "outputs": [
            "analysis/v46_returned_package_safe_interpretation/safe_interpretation_synthetic_summary.json",
            "analysis/v46_returned_package_safe_interpretation/safe_interpretation_synthetic_cases.tsv",
        ],
        "refresh_command": ".venv/bin/python scripts/v46_returned_package_safe_interpretation.py synthetic-check --outdir analysis/v46_returned_package_safe_interpretation",
    },
    {
        "artifact": "v46_returned_package_command_order_planner",
        "sources": [
            "docs/validation/RETURNED_PACKAGE_COMMAND_ORDER_PLANNER_V46.md",
            "docs/validation/AUTHOR_RUN_RETURN_OPERATOR_CHECKLIST_V45.md",
            "scripts/v46_returned_package_command_order_planner.py",
        ],
        "outputs": [
            "analysis/v46_returned_package_command_order_planner/returned_package_command_order_synthetic_summary.json",
            "analysis/v46_returned_package_command_order_planner/returned_package_command_order_synthetic_cases.tsv",
        ],
        "refresh_command": ".venv/bin/python scripts/v46_returned_package_command_order_planner.py synthetic-check --outdir analysis/v46_returned_package_command_order_planner",
    },
    {
        "artifact": "v46_returned_package_route_state_matrix",
        "sources": [
            "docs/validation/RETURNED_PACKAGE_ROUTE_STATE_MATRIX_V46.md",
            "scripts/v46_returned_package_route_state_matrix.py",
            "scripts/v46_returned_package_command_order_planner.py",
        ],
        "outputs": [
            "analysis/v46_returned_package_route_state_matrix/returned_package_route_state_matrix_summary.json",
            "analysis/v46_returned_package_route_state_matrix/returned_package_route_state_matrix.tsv",
            "analysis/v46_returned_package_route_state_matrix/returned_package_route_state_checks.tsv",
        ],
        "refresh_command": ".venv/bin/python scripts/v46_returned_package_route_state_matrix.py --outdir analysis/v46_returned_package_route_state_matrix --fail-on-error",
    },
    {
        "artifact": "v46_aggregate_only_returned_package_composition_dryrun",
        "sources": [
            "docs/validation/AGGREGATE_ONLY_RETURNED_PACKAGE_COMPOSITION_DRYRUN_V46.md",
            "docs/validation/AUTHOR_RUN_RETURN_OPERATOR_CHECKLIST_V45.md",
            "scripts/v46_aggregate_only_returned_package_composition_dryrun.py",
            "scripts/v46_returned_package_command_order_planner.py",
            "scripts/v46_returned_package_route_state_matrix.py",
            "scripts/v46_author_run_metric_format_adapter.py",
            "scripts/v46_partial_label_return_classifier.py",
            "scripts/v46_returned_package_safe_interpretation.py",
        ],
        "outputs": [
            "analysis/v46_aggregate_only_returned_package_composition_dryrun/aggregate_only_composition_summary.json",
            "analysis/v46_aggregate_only_returned_package_composition_dryrun/aggregate_only_composition_checks.tsv",
            "analysis/v46_aggregate_only_returned_package_composition_dryrun/aggregate_only_composition_steps.tsv",
        ],
        "refresh_command": ".venv/bin/python scripts/v46_aggregate_only_returned_package_composition_dryrun.py --outdir analysis/v46_aggregate_only_returned_package_composition_dryrun --fail-on-error",
    },
    {
        "artifact": "v46_unscoreable_return_composition_dryrun",
        "sources": [
            "docs/validation/UNSCOREABLE_RETURN_COMPOSITION_DRYRUN_V46.md",
            "docs/validation/AUTHOR_RUN_RETURN_OPERATOR_CHECKLIST_V45.md",
            "scripts/v46_unscoreable_return_composition_dryrun.py",
            "scripts/v46_returned_package_command_order_planner.py",
            "scripts/v46_returned_package_route_state_matrix.py",
            "scripts/v45_author_run_return_gate_runner.py",
            "scripts/v45_author_run_output_check.py",
        ],
        "outputs": [
            "analysis/v46_unscoreable_return_composition_dryrun/unscoreable_composition_summary.json",
            "analysis/v46_unscoreable_return_composition_dryrun/unscoreable_composition_steps.tsv",
            "analysis/v46_unscoreable_return_composition_dryrun/unscoreable_composition_checks.tsv",
        ],
        "refresh_command": ".venv/bin/python scripts/v46_unscoreable_return_composition_dryrun.py --outdir analysis/v46_unscoreable_return_composition_dryrun --fail-on-error",
    },
    {
        "artifact": "v46_returned_package_regression_suite",
        "sources": [
            "docs/validation/RETURNED_PACKAGE_REGRESSION_SUITE_V46.md",
            "scripts/v46_returned_package_regression_suite.py",
            "scripts/v46_terms_governance_matrix.py",
            "scripts/v46_author_run_metric_format_adapter.py",
            "scripts/v46_partial_label_return_classifier.py",
            "scripts/v46_returned_package_command_order_planner.py",
            "scripts/v46_returned_package_route_state_matrix.py",
            "scripts/v46_aggregate_only_returned_package_composition_dryrun.py",
            "scripts/v46_unscoreable_return_composition_dryrun.py",
            "scripts/v46_returned_package_safe_interpretation.py",
            "scripts/v46_safe_wording_fixture_linter.py",
            "scripts/v46_result_report_safe_class_linter.py",
        ],
        "outputs": [
            "analysis/v46_returned_package_regression_suite/returned_package_regression_summary.json",
            "analysis/v46_returned_package_regression_suite/returned_package_regression_steps.tsv",
        ],
        "refresh_command": ".venv/bin/python scripts/v46_returned_package_regression_suite.py --outdir analysis/v46_returned_package_regression_suite --fail-on-error",
    },
    {
        "artifact": "v46_safe_wording_fixture_linter",
        "sources": [
            "analysis/v46_returned_package_safe_interpretation/safe_interpretation_synthetic_cases.tsv",
            "docs/validation/SAFE_WORDING_FIXTURE_LINTER_V46.md",
            "scripts/v46_safe_wording_fixture_linter.py",
        ],
        "outputs": [
            "analysis/v46_safe_wording_fixture_linter/safe_wording_fixture_summary.json",
            "analysis/v46_safe_wording_fixture_linter/safe_wording_fixture_index.tsv",
            "analysis/v46_safe_wording_fixture_linter/safe_wording_fixture_lint.tsv",
        ],
        "refresh_command": ".venv/bin/python scripts/v46_safe_wording_fixture_linter.py --outdir analysis/v46_safe_wording_fixture_linter --fail-on-error",
    },
    {
        "artifact": "v46_result_report_safe_class_linter",
        "sources": [
            "docs/validation/RESULT_REPORT_SAFE_CLASS_LINTER_V46.md",
            "docs/validation/AUTHOR_RUN_RETURN_OPERATOR_CHECKLIST_V45.md",
            "scripts/v46_result_report_safe_class_linter.py",
        ],
        "outputs": [
            "analysis/v46_result_report_safe_class_linter/result_report_safe_class_synthetic_summary.json",
            "analysis/v46_result_report_safe_class_linter/result_report_safe_class_synthetic_cases.tsv",
        ],
        "refresh_command": ".venv/bin/python scripts/v46_result_report_safe_class_linter.py synthetic-check --outdir analysis/v46_result_report_safe_class_linter --fail-on-error",
    },
    {
        "artifact": "v46_small_n_conclusion_language",
        "sources": [
            "docs/validation/SMALL_N_CONCLUSION_LANGUAGE_V46.md",
            "docs/validation/PREREGISTRATION_V42.md",
            "docs/validation/OUTCOME_INTERPRETATION_GRID_V42.md",
            "docs/validation/VALIDATION_POWER_DECISION_TABLE_V45.md",
            "docs/validation/RETURNED_PACKAGE_SAFE_INTERPRETATION_V46.md",
            "analysis/v45_route_analyzable_pair_calculator/route_analyzable_pair_synthetic_cases.tsv",
            "analysis/v45_power_decision_table/stakeholder_power_decision_table.tsv",
            "analysis/v45_power_decision_table/selected_scenarios_by_n.tsv",
            "scripts/v46_small_n_conclusion_language_table.py",
        ],
        "outputs": [
            "analysis/v46_small_n_conclusion_language/small_n_conclusion_language_summary.json",
            "analysis/v46_small_n_conclusion_language/small_n_conclusion_language.tsv",
            "analysis/v46_small_n_conclusion_language/route_example_language.tsv",
            "analysis/v46_small_n_conclusion_language/SMALL_N_CONCLUSION_LANGUAGE.md",
        ],
        "refresh_command": ".venv/bin/python scripts/v46_small_n_conclusion_language_table.py --outdir analysis/v46_small_n_conclusion_language",
    },
    {
        "artifact": "v46_external_blocker_aging_audit",
        "sources": [
            "analysis/v45_external_blocker_board/external_blocker_board.tsv",
            "analysis/v45_followup_due_board/live_template/followup_due_board.tsv",
            "analysis/v45_external_blocker_escalation_matrix/external_blocker_escalation_matrix.tsv",
            "docs/validation/input_schemas/V45_request_sent_log_template.tsv",
            "docs/validation/EXTERNAL_BLOCKER_AGING_AUDIT_V46.md",
            "scripts/v46_external_blocker_aging_audit.py",
        ],
        "outputs": [
            "analysis/v46_external_blocker_aging_audit/live/external_blocker_aging_audit_summary.json",
            "analysis/v46_external_blocker_aging_audit/live/external_blocker_aging_audit.tsv",
            "analysis/v46_external_blocker_aging_audit/external_blocker_aging_synthetic_summary.json",
        ],
        "refresh_command": ".venv/bin/python scripts/v46_external_blocker_aging_audit.py synthetic-check --outdir analysis/v46_external_blocker_aging_audit && .venv/bin/python scripts/v46_external_blocker_aging_audit.py audit --outdir analysis/v46_external_blocker_aging_audit/live",
    },
    {
        "artifact": "v46_operator_smoke_test_bundle",
        "sources": [
            "docs/validation/OPERATOR_SMOKE_TEST_BUNDLE_V46.md",
            "scripts/v46_operator_smoke_test_bundle.py",
            "scripts/v46_terms_governance_matrix.py",
            "scripts/v46_author_run_metric_format_adapter.py",
            "scripts/v46_partial_label_return_classifier.py",
            "scripts/v46_returned_package_command_order_planner.py",
            "scripts/v46_returned_package_route_state_matrix.py",
            "scripts/v46_aggregate_only_returned_package_composition_dryrun.py",
            "scripts/v46_unscoreable_return_composition_dryrun.py",
            "scripts/v46_returned_package_safe_interpretation.py",
            "scripts/v46_safe_wording_fixture_linter.py",
            "scripts/v46_result_report_safe_class_linter.py",
            "scripts/v46_external_blocker_aging_audit.py",
        ],
        "outputs": [
            "analysis/v46_operator_smoke_test_bundle/operator_smoke_test_summary.json",
            "analysis/v46_operator_smoke_test_bundle/operator_smoke_test_steps.tsv",
        ],
        "refresh_command": ".venv/bin/python scripts/v46_operator_smoke_test_bundle.py --outdir analysis/v46_operator_smoke_test_bundle --fail-on-error",
    },
    {
        "artifact": "opengwas_token_expiry_sentinel",
        "sources": [
            "scripts/v45_opengwas_token_expiry_sentinel.py",
            "scripts/check_opengwas_access.py",
            "docs/validation/OPENGWAS_TOKEN_EXPIRY_SENTINEL_V45.md",
            "docs/validation/OPENGWAS_JWT_RENEWAL_RUNBOOK_V45.md",
        ],
        "outputs": [
            "analysis/v45_opengwas_token_expiry_sentinel/opengwas_token_expiry_sentinel_summary.json",
            "analysis/v45_opengwas_token_expiry_sentinel/opengwas_token_expiry_sentinel.tsv",
        ],
        "refresh_command": ".venv/bin/python scripts/v45_opengwas_token_expiry_sentinel.py --outdir analysis/v45_opengwas_token_expiry_sentinel",
    },
]

MTIME_EPSILON_SECONDS = 1.0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    return parser.parse_args()


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def mtime(path: Path) -> float:
    return path.stat().st_mtime if path.exists() else -1.0


def main() -> int:
    args = parse_args()
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    outdir.mkdir(parents=True, exist_ok=True)
    rows = []
    for spec in CHECKS:
        source_paths = [ROOT / value for value in spec["sources"]]
        output_paths = [ROOT / value for value in spec["outputs"]]
        missing_sources = [rel(path) for path in source_paths if not path.exists()]
        missing_outputs = [rel(path) for path in output_paths if not path.exists()]
        latest_source = max((mtime(path) for path in source_paths), default=-1.0)
        oldest_output = min((mtime(path) for path in output_paths), default=-1.0)
        stale = bool(missing_outputs or missing_sources or latest_source > oldest_output + MTIME_EPSILON_SECONDS)
        rows.append(
            {
                "artifact": spec["artifact"],
                "status": "STALE_OR_MISSING" if stale else "FRESH",
                "latest_source_mtime": latest_source,
                "oldest_output_mtime": oldest_output,
                "missing_sources": ";".join(missing_sources),
                "missing_outputs": ";".join(missing_outputs),
                "sources": ";".join(spec["sources"]),
                "outputs": ";".join(spec["outputs"]),
                "refresh_command": spec["refresh_command"],
            }
        )
    table = outdir / "readiness_stale_output_detector.tsv"
    with table.open("w", newline="") as handle:
        fieldnames = [
            "artifact",
            "status",
            "latest_source_mtime",
            "oldest_output_mtime",
            "missing_sources",
            "missing_outputs",
            "sources",
            "outputs",
            "refresh_command",
        ]
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    n_stale = sum(1 for row in rows if row["status"] != "FRESH")
    summary = {
        "synthetic": False,
        "purpose": "readiness generated-output freshness check; no biological claim",
        "n_artifacts_checked": len(rows),
        "n_stale_or_missing": n_stale,
        "overall_status": "PASS" if n_stale == 0 else "REFRESH_NEEDED",
        "table": rel(table),
    }
    (outdir / "readiness_stale_output_detector_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
