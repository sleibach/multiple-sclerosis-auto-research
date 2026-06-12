#!/usr/bin/env python3
"""Generate a V45 external-blocker escalation matrix.

This matrix is acquisition operations only. It makes external blockers and
unblocking events explicit; it does not send requests, receive data, or run
validation.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v45_external_blocker_escalation_matrix"
DEFAULTS = {
    "external": ROOT / "analysis/v45_external_blocker_board/external_blocker_board.tsv",
    "actions": ROOT / "analysis/v45_current_action_card/current_action_card.tsv",
    "followup": ROOT / "analysis/v45_followup_due_board/live_template/followup_due_board.tsv",
}

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


def write_tsv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def unblocking_event(row: dict[str, str]) -> str:
    cohort_id = row.get("cohort_id", "")
    if cohort_id == "gafson_dmf_2018":
        return "receive expression matrix, sample-patient map, baseline/early timepoints, NEDA-4 labels, gene IDs, batch/QC, steroid, and cell-covariate metadata; then quarantine/checksum/preflight before V42 harness"
    if cohort_id == "karolinska_dmf_ros_2019":
        return "receive beneficial-response labels plus GSM-to-patient/timepoint/cell-type map and outcome definition; then finalize blind Karolinska addendum before scoring"
    if cohort_id == "gse228330_ocrelizumab_pbmc":
        return "receive or reconstruct processed expression with verified subject map; optional response labels require a frozen addendum before any response analysis"
    if cohort_id == "any_author_run_fallback":
        return "receive non-sensitive aggregate author-run output package that passes redaction, completeness, checksum, and result-report gates"
    return row.get("required_external_items", "")


def escalation_trigger(row: dict[str, str], followup: dict[str, str]) -> str:
    if row.get("request_sent") != "yes":
        return "human approval to send initial request or author-run fallback packet"
    due = followup.get("next_followup_due_utc", "")
    if due:
        return f"follow up on or after {due}"
    return "wait for external response or define follow-up date"


def main() -> int:
    args = parse_args()
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    external_rows = read_tsv(DEFAULTS["external"])
    action_by_id = {row.get("cohort_id", ""): row for row in read_tsv(DEFAULTS["actions"])}
    followup_by_id = {
        TRACKER_TO_COHORT_ID.get(row.get("cohort", ""), row.get("cohort", "")): row
        for row in read_tsv(DEFAULTS["followup"])
    }

    rows: list[dict[str, str]] = []
    for row in external_rows:
        cohort_id = row.get("cohort_id", "")
        action = action_by_id.get(cohort_id, {})
        followup = followup_by_id.get(cohort_id, {})
        rows.append(
            {
                "priority": action.get("priority") or followup.get("priority", "99"),
                "cohort_id": cohort_id,
                "role": row.get("role", ""),
                "owner_or_recipient": action.get("recipient_or_path") or followup.get("recipient_or_path", ""),
                "request_artifact": action.get("request_or_packet") or row.get("request_packet", ""),
                "blocker_type": row.get("blocker_type", ""),
                "current_blocker": row.get("external_blocker") or row.get("triage_current_blocker", ""),
                "required_external_items": row.get("required_external_items", ""),
                "exact_unblocking_event": unblocking_event(row),
                "escalation_trigger": escalation_trigger(row, followup),
                "current_recommended_action": row.get("recommended_action", ""),
                "harness_ready": row.get("harness_ready", ""),
                "data_received": row.get("data_received", ""),
            }
        )
    rows.sort(key=lambda row: (int(row["priority"]) if row["priority"].isdigit() else 99, row["cohort_id"]))

    matrix_path = outdir / "external_blocker_escalation_matrix.tsv"
    write_tsv(
        matrix_path,
        rows,
        [
            "priority",
            "cohort_id",
            "role",
            "owner_or_recipient",
            "request_artifact",
            "blocker_type",
            "current_blocker",
            "required_external_items",
            "exact_unblocking_event",
            "escalation_trigger",
            "current_recommended_action",
            "harness_ready",
            "data_received",
        ],
    )
    summary = {
        "synthetic": False,
        "purpose": "V45 external-blocker escalation matrix; no biological claim",
        "matrix": rel(matrix_path),
        "n_routes": len(rows),
        "n_external_blocked": sum(1 for row in rows if row["blocker_type"] != "none_harness_ready_review"),
        "n_harness_ready": sum(1 for row in rows if row["harness_ready"] == "yes"),
        "sources": {name: rel(path) for name, path in DEFAULTS.items()},
    }
    (outdir / "external_blocker_escalation_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
