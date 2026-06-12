#!/usr/bin/env python3
"""Build an acquisition follow-up due board from tracker and sent-log state.

This is operations infrastructure only. It does not imply data receipt,
preflight readiness, or validation. It only surfaces which request/follow-up
action is due based on explicitly logged sends and tracker rows.
"""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TRACKER = ROOT / "analysis/v45_outbound_data_requests/request_tracker.tsv"
DEFAULT_SENT_LOG = ROOT / "docs/validation/input_schemas/V45_request_sent_log_template.tsv"
DEFAULT_OUTDIR = ROOT / "analysis/v45_followup_due_board"

SENT_STATUSES = {
    "sent",
    "sent_logged",
    "sent_waiting_response",
    "sent_no_response_yet",
    "sent_followup_pending",
}

TRACKER_ALIASES = {
    "gafson_dmf_neda": "Gafson_2018_DMF_PBMC_PMID30283812",
    "gafson_dmf_2018": "Gafson_2018_DMF_PBMC_PMID30283812",
    "karolinska_dmf_ros": "Karolinska_DMF_ROS_GSE130478_GSE130491_GSE130494",
    "karolinska_dmf_ros_2019": "Karolinska_DMF_ROS_GSE130478_GSE130491_GSE130494",
    "gse228330_ocrelizumab": "GSE228330_ocrelizumab_PBMC",
    "gse228330_ocrelizumab_pbmc": "GSE228330_ocrelizumab_PBMC",
    "author_run_fallback": "Any_author_run_fallback",
    "any_author_run_fallback": "Any_author_run_fallback",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tracker", type=Path, default=DEFAULT_TRACKER)
    parser.add_argument("--sent-log", type=Path, default=DEFAULT_SENT_LOG)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    parser.add_argument("--as-of-utc", default="", help="ISO UTC timestamp. Defaults to current UTC.")
    return parser.parse_args()


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return [{key: (value or "") for key, value in row.items()} for row in reader]


def write_tsv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "priority",
        "cohort",
        "tracker_status",
        "request_sent",
        "sent_timestamp_utc",
        "next_followup_due_utc",
        "days_until_due",
        "due_status",
        "recommended_action",
        "recipient_or_path",
        "prepared_request",
        "minimum_external_blocker",
        "target_raw_path",
    ]
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def norm(value: object) -> str:
    return str(value).strip().lower()


def parse_utc(value: str) -> datetime | None:
    text = value.strip()
    if not text or "<" in text or ">" in text:
        return None
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return None
    return parsed.astimezone(timezone.utc)


def parse_as_of(value: str) -> datetime:
    parsed = parse_utc(value) if value else None
    return parsed or datetime.now(timezone.utc)


def sent_events(sent_rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    events: dict[str, dict[str, str]] = {}
    for row in sent_rows:
        status = norm(row.get("status", ""))
        if status not in SENT_STATUSES:
            continue
        tracker_cohort = TRACKER_ALIASES.get(norm(row.get("cohort", "")))
        if not tracker_cohort:
            continue
        existing = events.get(tracker_cohort)
        if existing is None:
            events[tracker_cohort] = row
            continue
        old_ts = parse_utc(existing.get("sent_timestamp_utc", ""))
        new_ts = parse_utc(row.get("sent_timestamp_utc", ""))
        if new_ts and (old_ts is None or new_ts > old_ts):
            events[tracker_cohort] = row
    return events


def board_row(tracker_row: dict[str, str], event: dict[str, str] | None, as_of: datetime) -> dict[str, object]:
    request_sent = "yes" if event else norm(tracker_row.get("request_sent", "no")) if tracker_row.get("request_sent") else "no"
    sent_ts = event.get("sent_timestamp_utc", "") if event else tracker_row.get("sent_timestamp_utc", "")
    due_ts = event.get("next_followup_due_utc", "") if event else tracker_row.get("next_followup_due_utc", "")
    due_dt = parse_utc(due_ts)
    if request_sent == "yes" and due_dt:
        days_until = round((due_dt - as_of).total_seconds() / 86400, 2)
        if days_until < 0:
            due_status = "overdue"
            action = "send_followup_or_escalate_if_terms_allow"
        elif days_until <= 2:
            due_status = "due_soon"
            action = "prepare_followup"
        else:
            due_status = "waiting"
            action = "wait_until_followup_due"
    elif request_sent == "yes":
        days_until = ""
        due_status = "sent_due_unknown"
        action = "repair_sent_log_followup_due_date"
    else:
        days_until = ""
        status = norm(tracker_row.get("status", ""))
        if "ready" in status:
            due_status = "not_sent_ready"
            action = "send_request_when_human_approves_contact"
        else:
            due_status = "not_sent_not_ready"
            action = "resolve_pre_send_blocker"
    return {
        "priority": tracker_row.get("priority", ""),
        "cohort": tracker_row.get("cohort", ""),
        "tracker_status": tracker_row.get("status", ""),
        "request_sent": request_sent,
        "sent_timestamp_utc": sent_ts,
        "next_followup_due_utc": due_ts,
        "days_until_due": days_until,
        "due_status": due_status,
        "recommended_action": action,
        "recipient_or_path": tracker_row.get("recipient_or_path", ""),
        "prepared_request": tracker_row.get("prepared_request", ""),
        "minimum_external_blocker": tracker_row.get("minimum_external_blocker", ""),
        "target_raw_path": tracker_row.get("target_raw_path", ""),
    }


def main() -> int:
    args = parse_args()
    tracker_path = resolve(args.tracker)
    sent_log_path = resolve(args.sent_log)
    outdir = resolve(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    as_of = parse_as_of(args.as_of_utc)

    tracker_rows = read_tsv(tracker_path)
    sent_rows = read_tsv(sent_log_path)
    events = sent_events(sent_rows)
    board = [board_row(row, events.get(row.get("cohort", "")), as_of) for row in tracker_rows]
    board.sort(key=lambda row: (str(row["due_status"]) not in {"overdue", "due_soon", "not_sent_ready"}, int(row["priority"] or 999)))

    board_path = outdir / "followup_due_board.tsv"
    write_tsv(board_path, board)
    status_counts: dict[str, int] = {}
    for row in board:
        status_counts[str(row["due_status"])] = status_counts.get(str(row["due_status"]), 0) + 1
    summary = {
        "synthetic": "synthetic" in rel(sent_log_path).lower(),
        "purpose": "acquisition follow-up due board; no biological claim",
        "as_of_utc": as_of.isoformat().replace("+00:00", "Z"),
        "tracker": rel(tracker_path),
        "sent_log": rel(sent_log_path),
        "board": rel(board_path),
        "n_tracker_rows": len(tracker_rows),
        "n_sent_events": len(events),
        "due_status_counts": status_counts,
    }
    (outdir / "followup_due_board_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
