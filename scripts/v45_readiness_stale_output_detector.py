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
        "artifact": "current_action_card",
        "sources": [
            "analysis/v45_external_blocker_board/external_blocker_board.tsv",
            "analysis/v45_followup_due_board/live_template/followup_due_board.tsv",
            "analysis/v45_readiness_status_dashboard/readiness_status_dashboard_summary.json",
            "analysis/v45_state_machine_validator/live/state_machine_validator_summary.json",
            "analysis/v45_route_packet_integrity_manifest/live/route_packet_integrity_summary.json",
            "analysis/v45_precommit_readiness/precommit_readiness_summary.json",
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
