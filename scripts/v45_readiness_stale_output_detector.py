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
        stale = bool(missing_outputs or missing_sources or latest_source > oldest_output)
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
