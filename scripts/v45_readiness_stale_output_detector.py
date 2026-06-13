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
        "artifact": "v47_provenance_gate",
        "sources": [
            "docs/knowledge/EPISTEMIC_CLASSES.md",
            "knowledge_external/README.md",
            "knowledge_external/records",
            "knowledge_external/catalogs/resources",
            "knowledge_external/schema/external_claim_record.schema.json",
            "scripts/v47_provenance_gate.py",
        ],
        "outputs": [
            "analysis/v47_provenance_gate/synthetic_provenance_gate_summary.json",
            "analysis/v47_provenance_gate/synthetic_provenance_gate_cases.tsv",
            "analysis/v47_provenance_gate/provenance_gate_summary.json",
            "analysis/v47_provenance_gate/provenance_gate_issues.tsv",
        ],
        "refresh_command": ".venv/bin/python scripts/v47_provenance_gate.py synthetic-check --outdir analysis/v47_provenance_gate --fail-on-error && .venv/bin/python scripts/v47_provenance_gate.py audit --outdir analysis/v47_provenance_gate --fail-on-error",
    },
    {
        "artifact": "v47_external_knowledge_index",
        "sources": [
            "docs/knowledge/EXTERNAL_KNOWLEDGE_INDEX_V47.md",
            "knowledge_external/README.md",
            "knowledge_external/catalogs/README.md",
            "knowledge_external/records",
            "knowledge_external/catalogs/resources",
            "knowledge_external/schema/external_claim_record.schema.json",
            "knowledge_external/catalogs/resource_record.schema.json",
            "scripts/v47_external_knowledge_index.py",
        ],
        "outputs": [
            "analysis/v47_external_knowledge_index/synthetic_index_summary.json",
            "analysis/v47_external_knowledge_index/synthetic_index_checks.tsv",
            "knowledge_external/catalogs/indexes/external_knowledge_index.tsv",
            "knowledge_external/catalogs/indexes/external_knowledge_index_counts.tsv",
            "knowledge_external/catalogs/indexes/EXTERNAL_KNOWLEDGE_INDEX.md",
        ],
        "refresh_command": ".venv/bin/python scripts/v47_external_knowledge_index.py synthetic-check --outdir analysis/v47_external_knowledge_index --fail-on-error && .venv/bin/python scripts/v47_external_knowledge_index.py index --outdir knowledge_external/catalogs/indexes",
    },
    {
        "artifact": "v47_external_record_schema_linter",
        "sources": [
            "docs/knowledge/EXTERNAL_RECORD_SCHEMA_LINTER_V47.md",
            "knowledge_external/records",
            "knowledge_external/catalogs/resources",
            "scripts/v47_external_record_schema_linter.py",
        ],
        "outputs": [
            "analysis/v47_external_record_schema_linter/synthetic_schema_lint_summary.json",
            "analysis/v47_external_record_schema_linter/synthetic_schema_lint_checks.tsv",
            "analysis/v47_external_record_schema_linter/external_record_schema_lint_summary.json",
            "analysis/v47_external_record_schema_linter/external_record_schema_lint.tsv",
        ],
        "refresh_command": ".venv/bin/python scripts/v47_external_record_schema_linter.py synthetic-check --outdir analysis/v47_external_record_schema_linter --fail-on-error && .venv/bin/python scripts/v47_external_record_schema_linter.py lint --outdir analysis/v47_external_record_schema_linter --fail-on-error",
    },
    {
        "artifact": "v47_external_resource_category_rollup",
        "sources": [
            "docs/knowledge/EXTERNAL_RESOURCE_CATEGORY_ROLLUP_V47.md",
            "knowledge_external/catalogs/resources",
            "scripts/v47_external_resource_category_rollup.py",
        ],
        "outputs": [
            "analysis/v47_external_resource_category_rollup/synthetic_category_rollup_summary.json",
            "analysis/v47_external_resource_category_rollup/synthetic_category_rollup_checks.tsv",
            "knowledge_external/catalogs/indexes/external_resource_category_rollup.tsv",
            "knowledge_external/catalogs/indexes/external_resource_category_counts.tsv",
            "knowledge_external/catalogs/indexes/EXTERNAL_RESOURCE_CATEGORY_ROLLUP.md",
        ],
        "refresh_command": ".venv/bin/python scripts/v47_external_resource_category_rollup.py synthetic-check --outdir analysis/v47_external_resource_category_rollup --fail-on-error && .venv/bin/python scripts/v47_external_resource_category_rollup.py rollup --outdir knowledge_external/catalogs/indexes",
    },
    {
        "artifact": "v47_external_resource_access_tier_rollup",
        "sources": [
            "docs/knowledge/EXTERNAL_RESOURCE_ACCESS_TIER_ROLLUP_V47.md",
            "knowledge_external/catalogs/resources",
            "scripts/v47_external_resource_access_tier_rollup.py",
        ],
        "outputs": [
            "analysis/v47_external_resource_access_tier_rollup/synthetic_access_tier_rollup_summary.json",
            "analysis/v47_external_resource_access_tier_rollup/synthetic_access_tier_rollup_checks.tsv",
            "knowledge_external/catalogs/indexes/external_resource_access_tier_rollup.tsv",
            "knowledge_external/catalogs/indexes/external_resource_access_tier_counts.tsv",
            "knowledge_external/catalogs/indexes/EXTERNAL_RESOURCE_ACCESS_TIER_ROLLUP.md",
        ],
        "refresh_command": ".venv/bin/python scripts/v47_external_resource_access_tier_rollup.py synthetic-check --outdir analysis/v47_external_resource_access_tier_rollup --fail-on-error && .venv/bin/python scripts/v47_external_resource_access_tier_rollup.py rollup --outdir knowledge_external/catalogs/indexes",
    },
    {
        "artifact": "v47_external_markdown_index_linter",
        "sources": [
            "docs/knowledge/EXTERNAL_MARKDOWN_INDEX_LINTER_V47.md",
            "knowledge_external/catalogs/indexes",
            "knowledge_external/synthesis",
            "scripts/v47_external_markdown_index_linter.py",
        ],
        "outputs": [
            "analysis/v47_external_markdown_index_linter/synthetic_external_markdown_index_lint_summary.json",
            "analysis/v47_external_markdown_index_linter/synthetic_external_markdown_index_lint_checks.tsv",
            "analysis/v47_external_markdown_index_linter/external_markdown_index_lint_summary.json",
            "analysis/v47_external_markdown_index_linter/external_markdown_index_lint.tsv",
        ],
        "refresh_command": ".venv/bin/python scripts/v47_external_markdown_index_linter.py synthetic-check --outdir analysis/v47_external_markdown_index_linter --fail-on-error && .venv/bin/python scripts/v47_external_markdown_index_linter.py lint --outdir analysis/v47_external_markdown_index_linter --fail-on-error",
    },
    {
        "artifact": "v47_external_record_uniqueness_linter",
        "sources": [
            "docs/knowledge/EXTERNAL_RECORD_UNIQUENESS_LINTER_V47.md",
            "knowledge_external/records",
            "knowledge_external/catalogs/resources",
            "scripts/v47_external_record_uniqueness_linter.py",
        ],
        "outputs": [
            "analysis/v47_external_record_uniqueness_linter/synthetic_uniqueness_summary.json",
            "analysis/v47_external_record_uniqueness_linter/synthetic_uniqueness_checks.tsv",
            "analysis/v47_external_record_uniqueness_linter/external_record_uniqueness_lint_summary.json",
            "analysis/v47_external_record_uniqueness_linter/external_record_uniqueness_lint.tsv",
        ],
        "refresh_command": ".venv/bin/python scripts/v47_external_record_uniqueness_linter.py synthetic-check --outdir analysis/v47_external_record_uniqueness_linter --fail-on-error && .venv/bin/python scripts/v47_external_record_uniqueness_linter.py lint --outdir analysis/v47_external_record_uniqueness_linter --fail-on-error",
    },
    {
        "artifact": "v47_external_source_domain_rollup",
        "sources": [
            "docs/knowledge/EXTERNAL_SOURCE_DOMAIN_ROLLUP_V47.md",
            "knowledge_external/records",
            "knowledge_external/catalogs/resources",
            "scripts/v47_external_source_domain_rollup.py",
        ],
        "outputs": [
            "analysis/v47_external_source_domain_rollup/synthetic_source_domain_rollup_summary.json",
            "analysis/v47_external_source_domain_rollup/synthetic_source_domain_rollup_checks.tsv",
            "knowledge_external/catalogs/indexes/external_source_domain_rollup.tsv",
            "knowledge_external/catalogs/indexes/external_source_domain_counts.tsv",
            "knowledge_external/catalogs/indexes/EXTERNAL_SOURCE_DOMAIN_ROLLUP.md",
            "knowledge_external/catalogs/indexes/external_source_domain_rollup_summary.json",
        ],
        "refresh_command": ".venv/bin/python scripts/v47_external_source_domain_rollup.py synthetic-check --outdir analysis/v47_external_source_domain_rollup --fail-on-error && .venv/bin/python scripts/v47_external_source_domain_rollup.py rollup --outdir knowledge_external/catalogs/indexes",
    },
    {
        "artifact": "v47_convergence_contradiction_skeleton",
        "sources": [
            "docs/knowledge/CONVERGENCE_CONTRADICTION_SKELETON_V47.md",
            "knowledge_external/catalogs/indexes/external_knowledge_index.tsv",
            "scripts/v47_convergence_contradiction_skeleton.py",
        ],
        "outputs": [
            "analysis/v47_convergence_contradiction_skeleton/synthetic_skeleton_summary.json",
            "analysis/v47_convergence_contradiction_skeleton/synthetic_skeleton_checks.tsv",
            "analysis/v47_convergence_contradiction_skeleton/convergence_contradiction_skeleton_summary.json",
            "knowledge_external/synthesis/convergence_contradiction_skeleton.tsv",
            "knowledge_external/synthesis/CONVERGENCE_CONTRADICTION_SKELETON.md",
        ],
        "refresh_command": ".venv/bin/python scripts/v47_convergence_contradiction_skeleton.py synthetic-check --outdir analysis/v47_convergence_contradiction_skeleton --fail-on-error && .venv/bin/python scripts/v47_convergence_contradiction_skeleton.py build --index knowledge_external/catalogs/indexes/external_knowledge_index.tsv --outdir knowledge_external/synthesis --analysis-outdir analysis/v47_convergence_contradiction_skeleton",
    },
    {
        "artifact": "v47_relationship_vocabulary_linter",
        "sources": [
            "docs/knowledge/RELATIONSHIP_TO_PROJECT_FINDINGS_V47.md",
            "knowledge_external/records",
            "knowledge_external/catalogs/resources",
            "scripts/v47_relationship_vocabulary_linter.py",
        ],
        "outputs": [
            "analysis/v47_relationship_vocabulary_linter/synthetic_relationship_vocabulary_summary.json",
            "analysis/v47_relationship_vocabulary_linter/synthetic_relationship_vocabulary_checks.tsv",
            "analysis/v47_relationship_vocabulary_linter/relationship_vocabulary_lint_summary.json",
            "analysis/v47_relationship_vocabulary_linter/relationship_vocabulary_lint.tsv",
        ],
        "refresh_command": ".venv/bin/python scripts/v47_relationship_vocabulary_linter.py synthetic-check --outdir analysis/v47_relationship_vocabulary_linter --fail-on-error && .venv/bin/python scripts/v47_relationship_vocabulary_linter.py lint --outdir analysis/v47_relationship_vocabulary_linter --fail-on-error",
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
        "artifact": "v46_receipt_manifest_schema_linter",
        "sources": [
            "docs/validation/RECEIPT_MANIFEST_SCHEMA_LINTER_V46.md",
            "docs/validation/input_schemas/V45_package_receipt_manifest_template.tsv",
            "scripts/v46_receipt_manifest_schema_linter.py",
        ],
        "outputs": [
            "analysis/v46_receipt_manifest_schema_linter/receipt_manifest_schema_synthetic_summary.json",
            "analysis/v46_receipt_manifest_schema_linter/receipt_manifest_schema_synthetic_cases.tsv",
            "analysis/v46_receipt_manifest_schema_linter/receipt_manifest_schema_synthetic_lint.tsv",
        ],
        "refresh_command": ".venv/bin/python scripts/v46_receipt_manifest_schema_linter.py synthetic-check --outdir analysis/v46_receipt_manifest_schema_linter",
    },
    {
        "artifact": "v46_package_manifest_shape_classifier",
        "sources": [
            "docs/validation/PACKAGE_MANIFEST_SHAPE_CLASSIFIER_V46.md",
            "docs/validation/input_schemas/V45_package_receipt_manifest_template.tsv",
            "docs/validation/input_schemas/V45_author_run_minimum_output_spec.tsv",
            "docs/validation/FIRST30_RETURNED_PACKAGE_DECISION_TABLE_V46.md",
            "scripts/v46_package_manifest_shape_classifier.py",
            "scripts/v46_author_run_metric_format_adapter.py",
        ],
        "outputs": [
            "analysis/v46_package_manifest_shape_classifier/package_manifest_shape_synthetic_summary.json",
            "analysis/v46_package_manifest_shape_classifier/package_manifest_shape_synthetic_cases.tsv",
            "analysis/v46_package_manifest_shape_classifier/package_manifest_shape_synthetic_lint.tsv",
        ],
        "refresh_command": ".venv/bin/python scripts/v46_package_manifest_shape_classifier.py synthetic-check --outdir analysis/v46_package_manifest_shape_classifier",
    },
    {
        "artifact": "v46_receipt_manifest_to_command_plan_handoff",
        "sources": [
            "docs/validation/RECEIPT_MANIFEST_TO_COMMAND_PLAN_HANDOFF_V46.md",
            "docs/validation/RECEIPT_MANIFEST_SCHEMA_LINTER_V46.md",
            "docs/validation/PACKAGE_MANIFEST_SHAPE_CLASSIFIER_V46.md",
            "docs/validation/RETURNED_PACKAGE_COMMAND_ORDER_PLANNER_V46.md",
            "scripts/v46_receipt_manifest_to_command_plan_handoff.py",
            "scripts/v46_receipt_manifest_schema_linter.py",
            "scripts/v46_package_manifest_shape_classifier.py",
            "scripts/v46_returned_package_command_order_planner.py",
        ],
        "outputs": [
            "analysis/v46_receipt_manifest_to_command_plan_handoff/receipt_manifest_to_command_plan_handoff_summary.json",
            "analysis/v46_receipt_manifest_to_command_plan_handoff/receipt_manifest_to_command_plan_handoff.tsv",
            "analysis/v46_receipt_manifest_to_command_plan_handoff/receipt_manifest_to_command_plan_handoff_lint.tsv",
            "analysis/v46_receipt_manifest_to_command_plan_handoff/RECEIPT_MANIFEST_TO_COMMAND_PLAN_HANDOFF.md",
        ],
        "refresh_command": ".venv/bin/python scripts/v46_receipt_manifest_to_command_plan_handoff.py --outdir analysis/v46_receipt_manifest_to_command_plan_handoff --fail-on-error",
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
            "docs/validation/RECEIPT_MANIFEST_SCHEMA_LINTER_V46.md",
            "scripts/v46_receipt_manifest_schema_linter.py",
            "docs/validation/PACKAGE_MANIFEST_SHAPE_CLASSIFIER_V46.md",
            "scripts/v46_package_manifest_shape_classifier.py",
            "docs/validation/RECEIPT_MANIFEST_TO_COMMAND_PLAN_HANDOFF_V46.md",
            "scripts/v46_receipt_manifest_to_command_plan_handoff.py",
            "scripts/v46_returned_package_command_order_planner.py",
            "scripts/v46_returned_package_route_state_matrix.py",
            "scripts/v46_aggregate_only_returned_package_composition_dryrun.py",
            "scripts/v46_unscoreable_return_composition_dryrun.py",
            "scripts/v46_returned_package_safe_interpretation.py",
            "scripts/v46_safe_wording_fixture_linter.py",
            "docs/validation/RESULT_REPORT_SAFE_CLASS_LINTER_V46.md",
            "scripts/v46_result_report_safe_class_linter.py",
            "docs/validation/REPORT_HEADER_METADATA_LINTER_V46.md",
            "scripts/v46_report_header_metadata_linter.py",
            "docs/validation/REPORT_HEADER_REPAIR_TEMPLATE_COVERAGE_V46.md",
            "scripts/v46_report_header_repair_template_coverage.py",
            "docs/validation/SAFE_CLASS_REPORT_TEMPLATE_READINESS_V46.md",
            "scripts/v46_safe_class_report_template_readiness.py",
            "docs/validation/OPERATOR_TRANSCRIPT_FIXTURE_V46.md",
            "scripts/v46_operator_transcript_fixture.py",
            "docs/validation/RETURNED_PACKAGE_QUICKSTART_V46.md",
            "scripts/v46_returned_package_quickstart_readme.py",
            "docs/validation/ANALYZABLE_PAIR_CONFIDENCE_ENVELOPE_V46.md",
            "scripts/v46_analyzable_pair_confidence_envelope.py",
            "docs/validation/RETURN_REPAIR_REQUEST_TEMPLATES_V46.md",
            "scripts/v46_return_repair_request_templates.py",
            "docs/validation/PARTIAL_LABEL_REPAIR_PRIORITIZATION_V46.md",
            "scripts/v46_partial_label_repair_prioritization.py",
            "docs/validation/FIRST30_RETURNED_PACKAGE_DECISION_TABLE_V46.md",
            "scripts/v46_first30_returned_package_decision_table.py",
            "docs/validation/FIRST30_REPAIR_TEMPLATE_COVERAGE_LINTER_V46.md",
            "scripts/v46_first30_repair_template_coverage_linter.py",
            "docs/validation/FIRST30_RETURNED_PACKAGE_STATUS_BOARD_DRYRUN_V46.md",
            "scripts/v46_first30_returned_package_status_board_dryrun.py",
            "docs/validation/RETURNED_PACKAGE_STATUS_BOARD_SCHEMA_LINTER_V46.md",
            "scripts/v46_returned_package_status_board_schema_linter.py",
            "docs/validation/STATUS_BOARD_MARKDOWN_ROUNDTRIP_RENDERER_V46.md",
            "scripts/v46_status_board_markdown_roundtrip_renderer.py",
            "docs/validation/RETURNED_PACKAGE_PREFLIGHT_DRYRUN_V46.md",
            "scripts/v46_returned_package_preflight_dryrun.py",
            "docs/validation/RETURNED_PACKAGE_STATE_TRANSITION_VALIDATOR_V46.md",
            "scripts/v46_returned_package_state_transition_validator.py",
            "docs/validation/RETURNED_PACKAGE_HANDOFF_BUNDLE_MANIFEST_V46.md",
            "scripts/v46_returned_package_handoff_bundle_manifest.py",
            "docs/validation/RETURNED_PACKAGE_DOC_CROSSLINK_LINTER_V46.md",
            "scripts/v46_returned_package_doc_crosslink_linter.py",
            "docs/validation/RETURNED_PACKAGE_DEPENDENCY_GRAPH_V46.md",
            "scripts/v46_returned_package_dependency_graph.py",
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
        "artifact": "v46_report_header_metadata_linter",
        "sources": [
            "docs/validation/REPORT_HEADER_METADATA_LINTER_V46.md",
            "docs/validation/LOCKED_ARTIFACT_HASH_BASELINE_V45.tsv",
            "docs/validation/RESULT_REPORT_SAFE_CLASS_LINTER_V46.md",
            "scripts/v46_report_header_metadata_linter.py",
        ],
        "outputs": [
            "analysis/v46_report_header_metadata_linter/report_header_metadata_synthetic_summary.json",
            "analysis/v46_report_header_metadata_linter/report_header_metadata_synthetic_cases.tsv",
        ],
        "refresh_command": ".venv/bin/python scripts/v46_report_header_metadata_linter.py synthetic-check --outdir analysis/v46_report_header_metadata_linter --fail-on-error",
    },
    {
        "artifact": "v46_report_header_repair_template_coverage",
        "sources": [
            "docs/validation/REPORT_HEADER_REPAIR_TEMPLATE_COVERAGE_V46.md",
            "docs/validation/REPORT_HEADER_METADATA_LINTER_V46.md",
            "scripts/v46_report_header_repair_template_coverage.py",
            "scripts/v46_report_header_metadata_linter.py",
        ],
        "outputs": [
            "analysis/v46_report_header_repair_template_coverage/report_header_repair_template_coverage_summary.json",
            "analysis/v46_report_header_repair_template_coverage/report_header_repair_template_coverage.tsv",
            "analysis/v46_report_header_repair_template_coverage/report_header_required_field_coverage.tsv",
            "analysis/v46_report_header_repair_template_coverage/report_header_repair_template_lint.tsv",
            "analysis/v46_report_header_repair_template_coverage/REPORT_HEADER_REPAIR_TEMPLATE_COVERAGE.md",
        ],
        "refresh_command": ".venv/bin/python scripts/v46_report_header_repair_template_coverage.py --outdir analysis/v46_report_header_repair_template_coverage --fail-on-error",
    },
    {
        "artifact": "v46_safe_class_report_template_readiness",
        "sources": [
            "docs/validation/SAFE_CLASS_REPORT_TEMPLATE_READINESS_V46.md",
            "docs/validation/RETURNED_PACKAGE_SAFE_INTERPRETATION_V46.md",
            "docs/validation/RESULT_REPORT_SAFE_CLASS_LINTER_V46.md",
            "analysis/v46_returned_package_safe_interpretation/safe_interpretation_synthetic_cases.tsv",
            "scripts/v46_safe_class_report_template_readiness.py",
            "scripts/v46_result_report_safe_class_linter.py",
        ],
        "outputs": [
            "analysis/v46_safe_class_report_template_readiness/safe_class_report_template_readiness_summary.json",
            "analysis/v46_safe_class_report_template_readiness/safe_class_report_template_map.tsv",
            "analysis/v46_safe_class_report_template_readiness/safe_class_report_template_linter_results.tsv",
            "analysis/v46_safe_class_report_template_readiness/safe_class_report_template_lint.tsv",
            "analysis/v46_safe_class_report_template_readiness/SAFE_CLASS_REPORT_TEMPLATE_READINESS.md",
        ],
        "refresh_command": ".venv/bin/python scripts/v46_safe_class_report_template_readiness.py --outdir analysis/v46_safe_class_report_template_readiness --fail-on-error",
    },
    {
        "artifact": "v46_operator_transcript_fixture",
        "sources": [
            "docs/validation/OPERATOR_TRANSCRIPT_FIXTURE_V46.md",
            "docs/validation/LOCKED_ARTIFACT_HASH_BASELINE_V45.tsv",
            "analysis/v46_receipt_manifest_to_command_plan_handoff/receipt_manifest_to_command_plan_handoff.tsv",
            "analysis/v46_first30_returned_package_status_board_dryrun/first30_status_board_dryrun.tsv",
            "analysis/v46_safe_class_report_template_readiness/safe_class_report_template_map.tsv",
            "analysis/v46_report_header_repair_template_coverage/report_header_repair_template_coverage.tsv",
            "scripts/v46_operator_transcript_fixture.py",
        ],
        "outputs": [
            "analysis/v46_operator_transcript_fixture/operator_transcript_fixture_summary.json",
            "analysis/v46_operator_transcript_fixture/operator_transcript_cases.tsv",
            "analysis/v46_operator_transcript_fixture/operator_transcript_steps.tsv",
            "analysis/v46_operator_transcript_fixture/operator_transcript_lint.tsv",
            "analysis/v46_operator_transcript_fixture/OPERATOR_TRANSCRIPT_FIXTURE.md",
        ],
        "refresh_command": ".venv/bin/python scripts/v46_operator_transcript_fixture.py --outdir analysis/v46_operator_transcript_fixture --fail-on-error",
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
        "artifact": "v46_analyzable_pair_confidence_envelope",
        "sources": [
            "docs/validation/ANALYZABLE_PAIR_CONFIDENCE_ENVELOPE_V46.md",
            "docs/validation/POWER_MAP_V43.md",
            "docs/validation/VALIDATION_POWER_DECISION_TABLE_V45.md",
            "docs/validation/ROUTE_ANALYZABLE_PAIR_CALCULATOR_V45.md",
            "analysis/v43_method_validation/power_map_summary.tsv",
            "analysis/v45_route_analyzable_pair_calculator/route_analyzable_pair_synthetic_cases.tsv",
            "scripts/v46_analyzable_pair_confidence_envelope.py",
        ],
        "outputs": [
            "analysis/v46_analyzable_pair_confidence_envelope/analyzable_pair_confidence_envelope_summary.json",
            "analysis/v46_analyzable_pair_confidence_envelope/analyzable_pair_confidence_envelope.tsv",
            "analysis/v46_analyzable_pair_confidence_envelope/representative_power_cells.tsv",
            "analysis/v46_analyzable_pair_confidence_envelope/partial_label_example_envelopes.tsv",
            "analysis/v46_analyzable_pair_confidence_envelope/analyzable_pair_confidence_envelope_lint.tsv",
            "analysis/v46_analyzable_pair_confidence_envelope/ANALYZABLE_PAIR_CONFIDENCE_ENVELOPE.md",
        ],
        "refresh_command": ".venv/bin/python scripts/v46_analyzable_pair_confidence_envelope.py --outdir analysis/v46_analyzable_pair_confidence_envelope --fail-on-error",
    },
    {
        "artifact": "v46_safe_interpretation_examples",
        "sources": [
            "docs/validation/SAFE_INTERPRETATION_EXAMPLES_V46.md",
            "analysis/v46_safe_class_report_template_readiness/safe_class_report_template_map.tsv",
            "analysis/v46_small_n_conclusion_language/small_n_conclusion_language.tsv",
            "analysis/v46_analyzable_pair_confidence_envelope/analyzable_pair_confidence_envelope.tsv",
            "analysis/v46_partial_label_repair_prioritization/partial_label_repair_prioritization.tsv",
            "scripts/v46_safe_interpretation_examples.py",
        ],
        "outputs": [
            "analysis/v46_safe_interpretation_examples/safe_interpretation_examples_summary.json",
            "analysis/v46_safe_interpretation_examples/safe_interpretation_examples.tsv",
            "analysis/v46_safe_interpretation_examples/safe_interpretation_examples_lint.tsv",
            "analysis/v46_safe_interpretation_examples/SAFE_INTERPRETATION_EXAMPLES.md",
        ],
        "refresh_command": ".venv/bin/python scripts/v46_safe_interpretation_examples.py --outdir analysis/v46_safe_interpretation_examples --fail-on-error",
    },
    {
        "artifact": "v46_safe_interpretation_example_coverage_linter",
        "sources": [
            "docs/validation/SAFE_INTERPRETATION_EXAMPLE_COVERAGE_LINTER_V46.md",
            "analysis/v46_safe_class_report_template_readiness/safe_class_report_template_map.tsv",
            "analysis/v46_safe_interpretation_examples/safe_interpretation_examples.tsv",
            "scripts/v46_safe_interpretation_example_coverage_linter.py",
        ],
        "outputs": [
            "analysis/v46_safe_interpretation_example_coverage_linter/safe_interpretation_example_coverage_summary.json",
            "analysis/v46_safe_interpretation_example_coverage_linter/safe_interpretation_example_coverage.tsv",
            "analysis/v46_safe_interpretation_example_coverage_linter/safe_interpretation_example_coverage_lint.tsv",
            "analysis/v46_safe_interpretation_example_coverage_linter/SAFE_INTERPRETATION_EXAMPLE_COVERAGE.md",
        ],
        "refresh_command": ".venv/bin/python scripts/v46_safe_interpretation_example_coverage_linter.py --outdir analysis/v46_safe_interpretation_example_coverage_linter --fail-on-error",
    },
    {
        "artifact": "v46_return_repair_request_templates",
        "sources": [
            "docs/validation/RETURN_REPAIR_REQUEST_TEMPLATES_V46.md",
            "docs/validation/input_schemas/V45_preflight_failure_taxonomy.tsv",
            "docs/validation/input_schemas/V45_author_run_minimum_output_spec.tsv",
            "docs/validation/AUTHOR_RUN_RETURN_OPERATOR_CHECKLIST_V45.md",
            "docs/validation/RETURNED_PACKAGE_SAFE_INTERPRETATION_V46.md",
            "analysis/v46_small_n_conclusion_language/small_n_conclusion_language.tsv",
            "scripts/v46_return_repair_request_templates.py",
        ],
        "outputs": [
            "analysis/v46_return_repair_request_templates/return_repair_request_templates_summary.json",
            "analysis/v46_return_repair_request_templates/repair_request_template_index.tsv",
            "analysis/v46_return_repair_request_templates/repair_request_template_lint.tsv",
            "analysis/v46_return_repair_request_templates/RETURN_REPAIR_REQUEST_TEMPLATES.md",
        ],
        "refresh_command": ".venv/bin/python scripts/v46_return_repair_request_templates.py --outdir analysis/v46_return_repair_request_templates --fail-on-error",
    },
    {
        "artifact": "v46_first30_returned_package_decision_table",
        "sources": [
            "docs/validation/FIRST30_RETURNED_PACKAGE_DECISION_TABLE_V46.md",
            "docs/validation/FIRST_24H_RECEIVED_DATA_OPERATOR_CHECKLIST_V45.md",
            "docs/validation/RETURNED_PACKAGE_COMMAND_ORDER_PLANNER_V46.md",
            "analysis/v46_returned_package_route_state_matrix/returned_package_route_state_matrix.tsv",
            "scripts/v46_first30_returned_package_decision_table.py",
        ],
        "outputs": [
            "analysis/v46_first30_returned_package_decision_table/first30_returned_package_decision_summary.json",
            "analysis/v46_first30_returned_package_decision_table/first30_returned_package_decision_table.tsv",
            "analysis/v46_first30_returned_package_decision_table/first30_returned_package_decision_lint.tsv",
            "analysis/v46_first30_returned_package_decision_table/FIRST30_RETURNED_PACKAGE_DECISION_TABLE.md",
        ],
        "refresh_command": ".venv/bin/python scripts/v46_first30_returned_package_decision_table.py --outdir analysis/v46_first30_returned_package_decision_table --fail-on-error",
    },
    {
        "artifact": "v46_first30_repair_template_coverage_linter",
        "sources": [
            "docs/validation/FIRST30_REPAIR_TEMPLATE_COVERAGE_LINTER_V46.md",
            "analysis/v46_first30_returned_package_decision_table/first30_returned_package_decision_table.tsv",
            "analysis/v46_return_repair_request_templates/repair_request_template_index.tsv",
            "analysis/v46_return_repair_request_templates/repair_request_template_lint.tsv",
            "scripts/v46_first30_repair_template_coverage_linter.py",
        ],
        "outputs": [
            "analysis/v46_first30_repair_template_coverage_linter/first30_repair_template_coverage_summary.json",
            "analysis/v46_first30_repair_template_coverage_linter/first30_repair_template_coverage.tsv",
            "analysis/v46_first30_repair_template_coverage_linter/repair_template_safe_class_coverage.tsv",
            "analysis/v46_first30_repair_template_coverage_linter/first30_repair_template_coverage_lint.tsv",
            "analysis/v46_first30_repair_template_coverage_linter/FIRST30_REPAIR_TEMPLATE_COVERAGE.md",
        ],
        "refresh_command": ".venv/bin/python scripts/v46_first30_repair_template_coverage_linter.py --outdir analysis/v46_first30_repair_template_coverage_linter --fail-on-error",
    },
    {
        "artifact": "v46_first30_status_board_dryrun",
        "sources": [
            "docs/validation/FIRST30_RETURNED_PACKAGE_STATUS_BOARD_DRYRUN_V46.md",
            "analysis/v46_first30_returned_package_decision_table/first30_returned_package_decision_table.tsv",
            "analysis/v46_return_repair_request_templates/repair_request_template_index.tsv",
            "scripts/v46_first30_returned_package_status_board_dryrun.py",
        ],
        "outputs": [
            "analysis/v46_first30_returned_package_status_board_dryrun/first30_status_board_dryrun_summary.json",
            "analysis/v46_first30_returned_package_status_board_dryrun/first30_status_board_dryrun.tsv",
            "analysis/v46_first30_returned_package_status_board_dryrun/first30_status_board_dryrun_lint.tsv",
            "analysis/v46_first30_returned_package_status_board_dryrun/FIRST30_STATUS_BOARD_DRYRUN.md",
        ],
        "refresh_command": ".venv/bin/python scripts/v46_first30_returned_package_status_board_dryrun.py --outdir analysis/v46_first30_returned_package_status_board_dryrun --fail-on-error",
    },
    {
        "artifact": "v46_returned_package_status_board_schema_linter",
        "sources": [
            "docs/validation/RETURNED_PACKAGE_STATUS_BOARD_SCHEMA_LINTER_V46.md",
            "analysis/v46_first30_returned_package_status_board_dryrun/first30_status_board_dryrun.tsv",
            "analysis/v46_first30_returned_package_status_board_dryrun/FIRST30_STATUS_BOARD_DRYRUN.md",
            "scripts/v46_returned_package_status_board_schema_linter.py",
        ],
        "outputs": [
            "analysis/v46_returned_package_status_board_schema_linter/status_board_schema_linter_summary.json",
            "analysis/v46_returned_package_status_board_schema_linter/status_board_schema_lint.tsv",
            "analysis/v46_returned_package_status_board_schema_linter/status_board_schema_fixture_results.tsv",
            "analysis/v46_returned_package_status_board_schema_linter/RETURNED_PACKAGE_STATUS_BOARD_SCHEMA_LINTER.md",
        ],
        "refresh_command": ".venv/bin/python scripts/v46_returned_package_status_board_schema_linter.py --outdir analysis/v46_returned_package_status_board_schema_linter --fail-on-error",
    },
    {
        "artifact": "v46_status_board_markdown_roundtrip_renderer",
        "sources": [
            "docs/validation/STATUS_BOARD_MARKDOWN_ROUNDTRIP_RENDERER_V46.md",
            "analysis/v46_first30_returned_package_status_board_dryrun/first30_status_board_dryrun.tsv",
            "analysis/v46_first30_returned_package_status_board_dryrun/FIRST30_STATUS_BOARD_DRYRUN.md",
            "analysis/v46_first30_returned_package_status_board_dryrun/first30_status_board_dryrun_summary.json",
            "scripts/v46_status_board_markdown_roundtrip_renderer.py",
            "scripts/v46_returned_package_status_board_schema_linter.py",
        ],
        "outputs": [
            "analysis/v46_status_board_markdown_roundtrip_renderer/status_board_markdown_roundtrip_summary.json",
            "analysis/v46_status_board_markdown_roundtrip_renderer/status_board_markdown_roundtrip_lint.tsv",
            "analysis/v46_status_board_markdown_roundtrip_renderer/FIRST30_STATUS_BOARD_DRYRUN.roundtrip.md",
            "analysis/v46_status_board_markdown_roundtrip_renderer/synthetic_manual_drift.md",
            "analysis/v46_status_board_markdown_roundtrip_renderer/first30_status_board_roundtrip.diff",
        ],
        "refresh_command": ".venv/bin/python scripts/v46_status_board_markdown_roundtrip_renderer.py --outdir analysis/v46_status_board_markdown_roundtrip_renderer --fail-on-error",
    },
    {
        "artifact": "v46_returned_package_preflight_dryrun",
        "sources": [
            "docs/validation/RETURNED_PACKAGE_PREFLIGHT_DRYRUN_V46.md",
            "analysis/v46_first30_returned_package_decision_table/first30_returned_package_decision_table.tsv",
            "analysis/v46_first30_repair_template_coverage_linter/first30_repair_template_coverage.tsv",
            "scripts/v46_returned_package_preflight_dryrun.py",
            "scripts/v46_receipt_manifest_schema_linter.py",
            "scripts/v46_package_manifest_shape_classifier.py",
            "scripts/v46_first30_returned_package_decision_table.py",
            "scripts/v46_returned_package_state_transition_validator.py",
            "scripts/v46_first30_repair_template_coverage_linter.py",
        ],
        "outputs": [
            "analysis/v46_returned_package_preflight_dryrun/returned_package_preflight_dryrun_summary.json",
            "analysis/v46_returned_package_preflight_dryrun/returned_package_preflight_dryrun_cases.tsv",
            "analysis/v46_returned_package_preflight_dryrun/returned_package_preflight_dryrun_steps.tsv",
        ],
        "refresh_command": ".venv/bin/python scripts/v46_returned_package_preflight_dryrun.py --outdir analysis/v46_returned_package_preflight_dryrun --fail-on-error",
    },
    {
        "artifact": "v46_returned_package_state_transition_validator",
        "sources": [
            "docs/validation/RETURNED_PACKAGE_STATE_TRANSITION_VALIDATOR_V46.md",
            "docs/validation/RETURNED_PACKAGE_COMMAND_ORDER_PLANNER_V46.md",
            "docs/validation/RETURNED_PACKAGE_ROUTE_STATE_MATRIX_V46.md",
            "docs/validation/RETURNED_PACKAGE_SAFE_INTERPRETATION_V46.md",
            "docs/validation/RESULT_REPORT_SAFE_CLASS_LINTER_V46.md",
            "scripts/v46_returned_package_state_transition_validator.py",
        ],
        "outputs": [
            "analysis/v46_returned_package_state_transition_validator/returned_package_state_transition_summary.json",
            "analysis/v46_returned_package_state_transition_validator/returned_package_states.tsv",
            "analysis/v46_returned_package_state_transition_validator/returned_package_allowed_transitions.tsv",
            "analysis/v46_returned_package_state_transition_validator/returned_package_state_transition_scenarios.tsv",
            "analysis/v46_returned_package_state_transition_validator/returned_package_state_transition_lint.tsv",
            "analysis/v46_returned_package_state_transition_validator/RETURNED_PACKAGE_STATE_TRANSITION_VALIDATOR.md",
        ],
        "refresh_command": ".venv/bin/python scripts/v46_returned_package_state_transition_validator.py --outdir analysis/v46_returned_package_state_transition_validator --fail-on-error",
    },
    {
        "artifact": "v46_returned_package_handoff_bundle_manifest",
        "sources": [
            "docs/validation/RETURNED_PACKAGE_HANDOFF_BUNDLE_MANIFEST_V46.md",
            "analysis/v45_current_action_card/current_action_card_summary.json",
            "analysis/v45_cold_start_operator_sequence/cold_start_operator_sequence_summary.json",
            "analysis/v46_receipt_manifest_schema_linter/receipt_manifest_schema_synthetic_summary.json",
            "analysis/v46_package_manifest_shape_classifier/package_manifest_shape_synthetic_summary.json",
            "analysis/v46_receipt_manifest_to_command_plan_handoff/receipt_manifest_to_command_plan_handoff_summary.json",
            "analysis/v46_first30_returned_package_decision_table/first30_returned_package_decision_summary.json",
            "analysis/v46_first30_returned_package_status_board_dryrun/first30_status_board_dryrun_summary.json",
            "analysis/v46_returned_package_status_board_schema_linter/status_board_schema_linter_summary.json",
            "analysis/v46_status_board_markdown_roundtrip_renderer/status_board_markdown_roundtrip_summary.json",
            "analysis/v46_returned_package_preflight_dryrun/returned_package_preflight_dryrun_summary.json",
            "analysis/v46_returned_package_state_transition_validator/returned_package_state_transition_summary.json",
            "analysis/v46_report_header_metadata_linter/report_header_metadata_synthetic_summary.json",
            "analysis/v46_report_header_repair_template_coverage/report_header_repair_template_coverage_summary.json",
            "analysis/v46_safe_class_report_template_readiness/safe_class_report_template_readiness_summary.json",
            "analysis/v46_operator_transcript_fixture/operator_transcript_fixture_summary.json",
            "analysis/v46_first30_repair_template_coverage_linter/first30_repair_template_coverage_summary.json",
            "analysis/v46_partial_label_repair_prioritization/partial_label_repair_prioritization_summary.json",
            "scripts/v46_returned_package_handoff_bundle_manifest.py",
        ],
        "outputs": [
            "analysis/v46_returned_package_handoff_bundle_manifest/returned_package_handoff_bundle_summary.json",
            "analysis/v46_returned_package_handoff_bundle_manifest/returned_package_handoff_bundle_manifest.tsv",
            "analysis/v46_returned_package_handoff_bundle_manifest/returned_package_handoff_bundle_lint.tsv",
            "analysis/v46_returned_package_handoff_bundle_manifest/RETURNED_PACKAGE_HANDOFF_BUNDLE_MANIFEST.md",
        ],
        "refresh_command": ".venv/bin/python scripts/v46_returned_package_handoff_bundle_manifest.py --outdir analysis/v46_returned_package_handoff_bundle_manifest --fail-on-error",
    },
    {
        "artifact": "v46_returned_package_quickstart_readme",
        "sources": [
            "docs/validation/RETURNED_PACKAGE_QUICKSTART_V46.md",
            "analysis/v46_returned_package_handoff_bundle_manifest/returned_package_handoff_bundle_manifest.tsv",
            "analysis/v46_receipt_manifest_to_command_plan_handoff/receipt_manifest_to_command_plan_handoff.tsv",
            "analysis/v46_returned_package_regression_suite/returned_package_regression_steps.tsv",
            "analysis/v46_operator_smoke_test_bundle/operator_smoke_test_steps.tsv",
            "scripts/v46_returned_package_quickstart_readme.py",
        ],
        "outputs": [
            "analysis/v46_returned_package_quickstart_readme/returned_package_quickstart_summary.json",
            "analysis/v46_returned_package_quickstart_readme/returned_package_quickstart_commands.tsv",
            "analysis/v46_returned_package_quickstart_readme/returned_package_quickstart_lint.tsv",
            "analysis/v46_returned_package_quickstart_readme/RETURNED_PACKAGE_QUICKSTART.md",
        ],
        "refresh_command": ".venv/bin/python scripts/v46_returned_package_quickstart_readme.py --outdir analysis/v46_returned_package_quickstart_readme --fail-on-error",
    },
    {
        "artifact": "v46_quickstart_drift_fixture",
        "sources": [
            "docs/validation/QUICKSTART_DRIFT_FIXTURE_V46.md",
            "analysis/v46_returned_package_quickstart_readme/RETURNED_PACKAGE_QUICKSTART.md",
            "analysis/v46_returned_package_quickstart_readme/returned_package_quickstart_commands.tsv",
            "scripts/v46_quickstart_drift_fixture.py",
        ],
        "outputs": [
            "analysis/v46_quickstart_drift_fixture/quickstart_drift_summary.json",
            "analysis/v46_quickstart_drift_fixture/quickstart_drift_cases.tsv",
            "analysis/v46_quickstart_drift_fixture/quickstart_drift_lint.tsv",
            "analysis/v46_quickstart_drift_fixture/QUICKSTART_DRIFT_FIXTURE.md",
        ],
        "refresh_command": ".venv/bin/python scripts/v46_quickstart_drift_fixture.py --outdir analysis/v46_quickstart_drift_fixture --fail-on-error",
    },
    {
        "artifact": "v46_quickstart_command_coverage_matrix",
        "sources": [
            "docs/validation/QUICKSTART_COMMAND_COVERAGE_MATRIX_V46.md",
            "analysis/v46_returned_package_quickstart_readme/RETURNED_PACKAGE_QUICKSTART.md",
            "analysis/v46_returned_package_quickstart_readme/returned_package_quickstart_commands.tsv",
            "analysis/v46_returned_package_regression_suite/returned_package_regression_steps.tsv",
            "analysis/v46_operator_smoke_test_bundle/operator_smoke_test_steps.tsv",
            "analysis/v46_quickstart_drift_fixture/quickstart_drift_summary.json",
            "scripts/v46_quickstart_command_coverage_matrix.py",
        ],
        "outputs": [
            "analysis/v46_quickstart_command_coverage_matrix/quickstart_command_coverage_summary.json",
            "analysis/v46_quickstart_command_coverage_matrix/quickstart_command_coverage_matrix.tsv",
            "analysis/v46_quickstart_command_coverage_matrix/quickstart_command_coverage_lint.tsv",
            "analysis/v46_quickstart_command_coverage_matrix/QUICKSTART_COMMAND_COVERAGE_MATRIX.md",
        ],
        "refresh_command": ".venv/bin/python scripts/v46_quickstart_command_coverage_matrix.py --outdir analysis/v46_quickstart_command_coverage_matrix --fail-on-error",
    },
    {
        "artifact": "v46_returned_package_operator_pocket_card",
        "sources": [
            "docs/validation/RETURNED_PACKAGE_OPERATOR_POCKET_CARD_V46.md",
            "analysis/v46_returned_package_quickstart_readme/returned_package_quickstart_commands.tsv",
            "analysis/v46_first30_returned_package_status_board_dryrun/first30_status_board_dryrun.tsv",
            "analysis/v46_safe_class_report_template_readiness/safe_class_report_template_map.tsv",
            "scripts/v46_returned_package_operator_pocket_card.py",
        ],
        "outputs": [
            "analysis/v46_returned_package_operator_pocket_card/pocket_card_summary.json",
            "analysis/v46_returned_package_operator_pocket_card/RETURNED_PACKAGE_OPERATOR_POCKET_CARD.md",
            "analysis/v46_returned_package_operator_pocket_card/pocket_card_commands.tsv",
            "analysis/v46_returned_package_operator_pocket_card/pocket_card_first30.tsv",
            "analysis/v46_returned_package_operator_pocket_card/pocket_card_safe_classes.tsv",
            "analysis/v46_returned_package_operator_pocket_card/pocket_card_lint.tsv",
        ],
        "refresh_command": ".venv/bin/python scripts/v46_returned_package_operator_pocket_card.py --outdir analysis/v46_returned_package_operator_pocket_card --fail-on-error",
    },
    {
        "artifact": "v46_partial_label_repair_prioritization",
        "sources": [
            "docs/validation/PARTIAL_LABEL_REPAIR_PRIORITIZATION_V46.md",
            "analysis/v46_partial_label_return_classifier/partial_label_synthetic_cases.tsv",
            "analysis/v46_analyzable_pair_confidence_envelope/analyzable_pair_confidence_envelope.tsv",
            "analysis/v46_return_repair_request_templates/repair_request_template_index.tsv",
            "scripts/v46_partial_label_repair_prioritization.py",
        ],
        "outputs": [
            "analysis/v46_partial_label_repair_prioritization/partial_label_repair_prioritization_summary.json",
            "analysis/v46_partial_label_repair_prioritization/partial_label_repair_prioritization.tsv",
            "analysis/v46_partial_label_repair_prioritization/partial_label_repair_prioritization_lint.tsv",
            "analysis/v46_partial_label_repair_prioritization/PARTIAL_LABEL_REPAIR_PRIORITIZATION.md",
        ],
        "refresh_command": ".venv/bin/python scripts/v46_partial_label_repair_prioritization.py --outdir analysis/v46_partial_label_repair_prioritization --fail-on-error",
    },
    {
        "artifact": "v46_returned_package_doc_crosslink_linter",
        "sources": [
            "docs/validation/RETURNED_PACKAGE_DOC_CROSSLINK_LINTER_V46.md",
            "docs/validation/AUTHOR_RUN_RETURN_OPERATOR_CHECKLIST_V45.md",
            "docs/validation/CURRENT_ACTION_CARD_V45.md",
            "docs/validation/COLD_START_OPERATOR_SEQUENCE_V45.md",
            "docs/validation/RETURNED_PACKAGE_HANDOFF_BUNDLE_MANIFEST_V46.md",
            "docs/validation/RETURNED_PACKAGE_REGRESSION_SUITE_V46.md",
            "docs/validation/OPERATOR_SMOKE_TEST_BUNDLE_V46.md",
            "docs/validation/PARTIAL_LABEL_REPAIR_PRIORITIZATION_V46.md",
            "docs/validation/RETURNED_PACKAGE_DEPENDENCY_GRAPH_V46.md",
            "docs/validation/RETURNED_PACKAGE_STATUS_BOARD_SCHEMA_LINTER_V46.md",
            "docs/validation/STATUS_BOARD_MARKDOWN_ROUNDTRIP_RENDERER_V46.md",
            "docs/validation/SAFE_CLASS_REPORT_TEMPLATE_READINESS_V46.md",
            "docs/validation/OPERATOR_TRANSCRIPT_FIXTURE_V46.md",
            "docs/validation/RETURNED_PACKAGE_QUICKSTART_V46.md",
            "analysis/v46_returned_package_quickstart_readme/RETURNED_PACKAGE_QUICKSTART.md",
            "analysis/v46_returned_package_handoff_bundle_manifest/returned_package_handoff_bundle_manifest.tsv",
            "analysis/v46_returned_package_regression_suite/returned_package_regression_steps.tsv",
            "analysis/v46_operator_smoke_test_bundle/operator_smoke_test_steps.tsv",
            "scripts/v46_returned_package_doc_crosslink_linter.py",
        ],
        "outputs": [
            "analysis/v46_returned_package_doc_crosslink_linter/returned_package_doc_crosslink_summary.json",
            "analysis/v46_returned_package_doc_crosslink_linter/returned_package_doc_crosslink.tsv",
            "analysis/v46_returned_package_doc_crosslink_linter/returned_package_doc_crosslink_lint.tsv",
            "analysis/v46_returned_package_doc_crosslink_linter/RETURNED_PACKAGE_DOC_CROSSLINK_LINTER.md",
        ],
        "refresh_command": ".venv/bin/python scripts/v46_returned_package_doc_crosslink_linter.py --outdir analysis/v46_returned_package_doc_crosslink_linter --fail-on-error",
    },
    {
        "artifact": "v46_returned_package_dependency_graph",
        "sources": [
            "docs/validation/RETURNED_PACKAGE_DEPENDENCY_GRAPH_V46.md",
            "analysis/v46_returned_package_handoff_bundle_manifest/returned_package_handoff_bundle_manifest.tsv",
            "analysis/v46_returned_package_regression_suite/returned_package_regression_steps.tsv",
            "analysis/v46_operator_smoke_test_bundle/operator_smoke_test_steps.tsv",
            "scripts/v46_returned_package_dependency_graph.py",
        ],
        "outputs": [
            "analysis/v46_returned_package_dependency_graph/returned_package_dependency_summary.json",
            "analysis/v46_returned_package_dependency_graph/returned_package_dependency_nodes.tsv",
            "analysis/v46_returned_package_dependency_graph/returned_package_dependency_edges.tsv",
            "analysis/v46_returned_package_dependency_graph/returned_package_dependency_lint.tsv",
            "analysis/v46_returned_package_dependency_graph/returned_package_dependency_graph.dot",
            "analysis/v46_returned_package_dependency_graph/RETURNED_PACKAGE_DEPENDENCY_GRAPH.md",
        ],
        "refresh_command": ".venv/bin/python scripts/v46_returned_package_dependency_graph.py --outdir analysis/v46_returned_package_dependency_graph --fail-on-error",
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
            "docs/validation/RECEIPT_MANIFEST_SCHEMA_LINTER_V46.md",
            "scripts/v46_receipt_manifest_schema_linter.py",
            "docs/validation/PACKAGE_MANIFEST_SHAPE_CLASSIFIER_V46.md",
            "scripts/v46_package_manifest_shape_classifier.py",
            "docs/validation/RECEIPT_MANIFEST_TO_COMMAND_PLAN_HANDOFF_V46.md",
            "scripts/v46_receipt_manifest_to_command_plan_handoff.py",
            "scripts/v46_returned_package_command_order_planner.py",
            "scripts/v46_returned_package_route_state_matrix.py",
            "scripts/v46_aggregate_only_returned_package_composition_dryrun.py",
            "scripts/v46_unscoreable_return_composition_dryrun.py",
            "scripts/v46_returned_package_safe_interpretation.py",
            "scripts/v46_safe_wording_fixture_linter.py",
            "docs/validation/RESULT_REPORT_SAFE_CLASS_LINTER_V46.md",
            "scripts/v46_result_report_safe_class_linter.py",
            "docs/validation/REPORT_HEADER_METADATA_LINTER_V46.md",
            "scripts/v46_report_header_metadata_linter.py",
            "docs/validation/REPORT_HEADER_REPAIR_TEMPLATE_COVERAGE_V46.md",
            "scripts/v46_report_header_repair_template_coverage.py",
            "docs/validation/SAFE_CLASS_REPORT_TEMPLATE_READINESS_V46.md",
            "scripts/v46_safe_class_report_template_readiness.py",
            "docs/validation/OPERATOR_TRANSCRIPT_FIXTURE_V46.md",
            "scripts/v46_operator_transcript_fixture.py",
            "docs/validation/RETURNED_PACKAGE_QUICKSTART_V46.md",
            "scripts/v46_returned_package_quickstart_readme.py",
            "docs/validation/ANALYZABLE_PAIR_CONFIDENCE_ENVELOPE_V46.md",
            "scripts/v46_analyzable_pair_confidence_envelope.py",
            "docs/validation/RETURN_REPAIR_REQUEST_TEMPLATES_V46.md",
            "scripts/v46_return_repair_request_templates.py",
            "docs/validation/PARTIAL_LABEL_REPAIR_PRIORITIZATION_V46.md",
            "scripts/v46_partial_label_repair_prioritization.py",
            "docs/validation/FIRST30_RETURNED_PACKAGE_DECISION_TABLE_V46.md",
            "scripts/v46_first30_returned_package_decision_table.py",
            "docs/validation/FIRST30_REPAIR_TEMPLATE_COVERAGE_LINTER_V46.md",
            "scripts/v46_first30_repair_template_coverage_linter.py",
            "docs/validation/FIRST30_RETURNED_PACKAGE_STATUS_BOARD_DRYRUN_V46.md",
            "scripts/v46_first30_returned_package_status_board_dryrun.py",
            "docs/validation/RETURNED_PACKAGE_STATUS_BOARD_SCHEMA_LINTER_V46.md",
            "scripts/v46_returned_package_status_board_schema_linter.py",
            "docs/validation/STATUS_BOARD_MARKDOWN_ROUNDTRIP_RENDERER_V46.md",
            "scripts/v46_status_board_markdown_roundtrip_renderer.py",
            "docs/validation/RETURNED_PACKAGE_PREFLIGHT_DRYRUN_V46.md",
            "scripts/v46_returned_package_preflight_dryrun.py",
            "docs/validation/RETURNED_PACKAGE_STATE_TRANSITION_VALIDATOR_V46.md",
            "scripts/v46_returned_package_state_transition_validator.py",
            "docs/validation/RETURNED_PACKAGE_HANDOFF_BUNDLE_MANIFEST_V46.md",
            "scripts/v46_returned_package_handoff_bundle_manifest.py",
            "docs/validation/RETURNED_PACKAGE_DOC_CROSSLINK_LINTER_V46.md",
            "scripts/v46_returned_package_doc_crosslink_linter.py",
            "docs/validation/RETURNED_PACKAGE_DEPENDENCY_GRAPH_V46.md",
            "scripts/v46_returned_package_dependency_graph.py",
            "scripts/v46_external_blocker_aging_audit.py",
        ],
        "outputs": [
            "analysis/v46_operator_smoke_test_bundle/operator_smoke_test_summary.json",
            "analysis/v46_operator_smoke_test_bundle/operator_smoke_test_steps.tsv",
        ],
        "refresh_command": ".venv/bin/python scripts/v46_operator_smoke_test_bundle.py --outdir analysis/v46_operator_smoke_test_bundle --fail-on-error",
    },
    {
        "artifact": "v46_sap_ai_core_health_check",
        "sources": [
            "docs/validation/SAP_AI_CORE_HEALTH_CHECK_V46.md",
            "scripts/v46_sap_ai_core_health_check.py",
            "scripts/sap_ai_core_client.py",
            "meta/SAP_AI_CORE_ACCESS_V30.md",
        ],
        "outputs": [
            "analysis/v46_sap_ai_core_health_check/sap_ai_core_health_summary.json",
            "analysis/v46_sap_ai_core_health_check/sap_ai_core_health_checks.tsv",
        ],
        "refresh_command": ".venv/bin/python scripts/v46_sap_ai_core_health_check.py --outdir analysis/v46_sap_ai_core_health_check --fail-on-error",
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
    if not path.exists():
        return -1.0
    if path.is_dir():
        child_mtimes = [child.stat().st_mtime for child in path.rglob("*") if child.is_file()]
        return max([path.stat().st_mtime] + child_mtimes)
    return path.stat().st_mtime


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
