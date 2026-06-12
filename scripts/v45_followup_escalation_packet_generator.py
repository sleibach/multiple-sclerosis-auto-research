#!/usr/bin/env python3
"""Generate V45 follow-up/escalation packets from live blocker state.

Operations only. This script creates draft packets and does not send messages,
update trackers, inspect data, or authorize validation.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v45_followup_escalation_packets/live"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    return parser.parse_args()


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def slug(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")


def route_key(value: str) -> str:
    lowered = value.lower()
    if "gafson" in lowered:
        return "gafson_dmf_2018"
    if "karolinska" in lowered:
        return "karolinska_dmf_ros_2019"
    if "gse228330" in lowered:
        return "gse228330_ocrelizumab_pbmc"
    if "author_run" in lowered:
        return "any_author_run_fallback"
    return slug(value)


def read_tsv(path: str) -> pd.DataFrame:
    return pd.read_csv(ROOT / path, sep="\t", dtype=str).fillna("")


def escalation_action(due_status: str, current_action: str) -> str:
    if due_status == "overdue_followup":
        return "send_overdue_followup"
    if due_status == "followup_due_now":
        return "send_due_followup"
    if due_status == "not_sent_ready":
        return current_action or "send_request_when_human_approves_contact"
    return current_action or "monitor"


def main() -> int:
    args = parse_args()
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    due = read_tsv("analysis/v45_followup_due_board/live_template/followup_due_board.tsv")
    escalation = read_tsv("analysis/v45_external_blocker_escalation_matrix/external_blocker_escalation_matrix.tsv")

    due_by_route = {route_key(row["cohort"]): row for row in due.to_dict(orient="records")}
    rows: list[dict[str, str]] = []

    for record in escalation.sort_values("priority", key=lambda col: col.astype(int)).to_dict(orient="records"):
        due_row = due_by_route.get(record["cohort_id"], {})
        action = escalation_action(due_row.get("due_status", ""), record.get("current_recommended_action", ""))
        filename = outdir / f"{record['priority']}_{slug(record['cohort_id'])}_{action}.md"
        packet_lines = [
            f"# V45 Escalation Packet: {record['cohort_id']}",
            "",
            "Status: draft operations packet. No message has been sent by this file.",
            "",
            f"- Route role: `{record['role']}`",
            f"- Owner / recipient: `{record['owner_or_recipient']}`",
            f"- Current blocker: `{record['current_blocker']}`",
            f"- Blocker type: `{record['blocker_type']}`",
            f"- Due status: `{due_row.get('due_status', 'unknown')}`",
            f"- Recommended action: `{action}`",
            f"- Request artifact: `{record['request_artifact']}`",
            f"- Required external items: `{record['required_external_items']}`",
            f"- Exact unblocking event: {record['exact_unblocking_event']}",
            "",
            "## Guardrail",
            "",
            "Sending or following up on this packet does not mean data have been received, preflighted, scored, or validated.",
        ]
        filename.write_text("\n".join(packet_lines) + "\n")
        rows.append(
            {
                "priority": record["priority"],
                "cohort_id": record["cohort_id"],
                "owner_or_recipient": record["owner_or_recipient"],
                "due_status": due_row.get("due_status", "unknown"),
                "recommended_action": action,
                "request_artifact": record["request_artifact"],
                "packet": rel(filename),
                "exact_unblocking_event": record["exact_unblocking_event"],
            }
        )

    index = outdir / "followup_escalation_packet_index.tsv"
    with index.open("w", newline="") as handle:
        fieldnames = list(rows[0].keys()) if rows else []
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    n_overdue = sum(1 for row in rows if row["due_status"] in {"overdue_followup", "followup_due_now"})
    summary = {
        "synthetic": False,
        "purpose": "V45 follow-up escalation packets; draft operations only, no biological claim",
        "n_routes": len(rows),
        "n_overdue_or_due_now": n_overdue,
        "n_not_sent_ready": sum(1 for row in rows if row["due_status"] == "not_sent_ready"),
        "overall_status": "PASS",
        "index": rel(index),
    }
    (outdir / "followup_escalation_packet_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
