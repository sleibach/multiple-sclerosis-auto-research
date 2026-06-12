#!/usr/bin/env python3
"""Merge V45 acquisition, outbound, follow-up, and triage state.

This board is operational only. It makes external blockers explicit and keeps
them separate from internal readiness work.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v45_external_blocker_board"
DEFAULT_ACQ = ROOT / "analysis/v45_live_cohort_acquisition_index/live_cohort_acquisition_index.tsv"
DEFAULT_TRACKER = ROOT / "analysis/v45_outbound_data_requests/request_tracker.tsv"
DEFAULT_TRIAGE = ROOT / "analysis/v45_received_data_triage/received_data_triage_status.tsv"
DEFAULT_FOLLOWUP = ROOT / "analysis/v45_followup_due_board/live_template/followup_due_board.tsv"

TRACKER_TO_COHORT_ID = {
    "Gafson_2018_DMF_PBMC_PMID30283812": "gafson_dmf_2018",
    "Karolinska_DMF_ROS_GSE130478_GSE130491_GSE130494": "karolinska_dmf_ros_2019",
    "GSE228330_ocrelizumab_PBMC": "gse228330_ocrelizumab_pbmc",
    "Any_author_run_fallback": "any_author_run_fallback",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    return parser.parse_args()


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return [{key: (value or "") for key, value in row.items()} for row in reader]


def index(rows: list[dict[str, str]], key: str) -> dict[str, dict[str, str]]:
    return {row.get(key, ""): row for row in rows}


def blocker_type(row: dict[str, str]) -> str:
    if row.get("harness_ready") == "yes":
        return "none_harness_ready_review"
    if row.get("request_sent") != "yes":
        return "external_send_or_author_approval"
    if row.get("data_received") in {"no", "public_partial", "public_partial_labels_absent", ""}:
        return "external_data_or_label_response"
    return "internal_receipt_or_preflight_repair"


def recommended_action(row: dict[str, str]) -> str:
    btype = blocker_type(row)
    if btype == "external_send_or_author_approval":
        return row.get("followup_recommended_action") or "send_request_when_human_approves_contact"
    if btype == "external_data_or_label_response":
        return row.get("followup_recommended_action") or "wait_for_response_or_send_followup"
    if btype == "internal_receipt_or_preflight_repair":
        return row.get("triage_next_action") or "complete_received_data_gates"
    return "review_harness_ready_state_before_any_scoring"


def main() -> int:
    args = parse_args()
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    acq_by_id = index(read_tsv(DEFAULT_ACQ), "cohort_id")
    tracker = read_tsv(DEFAULT_TRACKER)
    triage_by_id = index(read_tsv(DEFAULT_TRIAGE), "cohort_id")
    followup_by_tracker = index(read_tsv(DEFAULT_FOLLOWUP), "cohort")

    rows: list[dict[str, str]] = []
    for tracker_row in tracker:
        tracker_cohort = tracker_row.get("cohort", "")
        cohort_id = TRACKER_TO_COHORT_ID.get(tracker_cohort, tracker_cohort)
        acq = acq_by_id.get(cohort_id, {})
        triage = triage_by_id.get(cohort_id, {})
        followup = followup_by_tracker.get(tracker_cohort, {})
        merged = {
            "cohort_id": cohort_id,
            "tracker_cohort": tracker_cohort,
            "role": acq.get("role") or tracker_row.get("role", ""),
            "access_tier": acq.get("access_tier") or tracker_row.get("access_tier", ""),
            "acquisition_status": acq.get("current_status", ""),
            "tracker_status": tracker_row.get("status", ""),
            "request_sent": followup.get("request_sent") or triage.get("request_sent", "no"),
            "followup_due_status": followup.get("due_status", ""),
            "data_received": triage.get("data_received", "not_applicable_for_fallback" if cohort_id == "any_author_run_fallback" else ""),
            "harness_ready": triage.get("harness_ready", "no"),
            "external_blocker": acq.get("blocker") or tracker_row.get("minimum_external_blocker", ""),
            "required_external_items": acq.get("required_external_items") or tracker_row.get("minimum_external_blocker", ""),
            "triage_current_blocker": triage.get("current_blocker", ""),
            "triage_next_action": triage.get("next_action", ""),
            "followup_recommended_action": followup.get("recommended_action", ""),
            "target_raw_path": acq.get("target_raw_path") or tracker_row.get("target_raw_path", ""),
            "request_packet": acq.get("request_packet") or tracker_row.get("prepared_request", ""),
        }
        merged["blocker_type"] = blocker_type(merged)
        merged["recommended_action"] = recommended_action(merged)
        rows.append(merged)

    rows.sort(key=lambda row: (row["blocker_type"], row["cohort_id"]))
    board_path = outdir / "external_blocker_board.tsv"
    fieldnames = [
        "cohort_id",
        "tracker_cohort",
        "role",
        "access_tier",
        "acquisition_status",
        "tracker_status",
        "request_sent",
        "followup_due_status",
        "data_received",
        "harness_ready",
        "blocker_type",
        "external_blocker",
        "required_external_items",
        "triage_current_blocker",
        "triage_next_action",
        "followup_recommended_action",
        "recommended_action",
        "target_raw_path",
        "request_packet",
    ]
    with board_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    counts: dict[str, int] = {}
    for row in rows:
        counts[row["blocker_type"]] = counts.get(row["blocker_type"], 0) + 1
    summary = {
        "synthetic": False,
        "purpose": "external blocker board; no biological claim",
        "board": rel(board_path),
        "n_rows": len(rows),
        "blocker_type_counts": counts,
        "n_harness_ready": sum(1 for row in rows if row["harness_ready"] == "yes"),
        "sources": {
            "acquisition_index": rel(DEFAULT_ACQ),
            "tracker": rel(DEFAULT_TRACKER),
            "triage": rel(DEFAULT_TRIAGE),
            "followup_board": rel(DEFAULT_FOLLOWUP),
        },
    }
    (outdir / "external_blocker_board_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
