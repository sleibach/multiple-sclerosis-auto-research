#!/usr/bin/env python3
"""Audit route-specific external blocker age and next action.

This is operational infrastructure only. It combines the external blocker board,
follow-up due board, escalation matrix, and sent-log entries to show whether each
route's external clock has started, is waiting, is due, or should escalate. It
does not read cohort data or run validation.
"""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v46_external_blocker_aging_audit"
DEFAULT_BLOCKER = ROOT / "analysis/v45_external_blocker_board/external_blocker_board.tsv"
DEFAULT_FOLLOWUP = ROOT / "analysis/v45_followup_due_board/live_template/followup_due_board.tsv"
DEFAULT_ESCALATION = ROOT / "analysis/v45_external_blocker_escalation_matrix/external_blocker_escalation_matrix.tsv"
DEFAULT_SENT_LOG = ROOT / "docs/validation/input_schemas/V45_request_sent_log_template.tsv"

TRACKER_TO_COHORT_ID = {
    "Gafson_2018_DMF_PBMC_PMID30283812": "gafson_dmf_2018",
    "Karolinska_DMF_ROS_GSE130478_GSE130491_GSE130494": "karolinska_dmf_ros_2019",
    "GSE228330_ocrelizumab_PBMC": "gse228330_ocrelizumab_pbmc",
    "Any_author_run_fallback": "any_author_run_fallback",
}
SHORT_TO_TRACKER = {
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
    sub = parser.add_subparsers(dest="cmd", required=True)

    audit_cmd = sub.add_parser("audit")
    audit_cmd.add_argument("--blocker-board", type=Path, default=DEFAULT_BLOCKER)
    audit_cmd.add_argument("--followup-board", type=Path, default=DEFAULT_FOLLOWUP)
    audit_cmd.add_argument("--escalation-matrix", type=Path, default=DEFAULT_ESCALATION)
    audit_cmd.add_argument("--sent-log", type=Path, default=DEFAULT_SENT_LOG)
    audit_cmd.add_argument("--as-of-utc", default="")
    audit_cmd.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)

    syn = sub.add_parser("synthetic-check")
    syn.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
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


def write_tsv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def norm(value: object) -> str:
    return str(value or "").strip().lower()


def parse_utc(value: str) -> datetime | None:
    text = str(value or "").strip()
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
    return parse_utc(value) or datetime.now(timezone.utc)


def sent_events(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    events: dict[str, dict[str, str]] = {}
    for row in rows:
        status = norm(row.get("status"))
        if status not in {"sent", "sent_logged", "sent_waiting_response", "sent_no_response_yet", "sent_followup_pending"}:
            continue
        tracker = SHORT_TO_TRACKER.get(norm(row.get("cohort")), row.get("cohort", ""))
        cohort_id = TRACKER_TO_COHORT_ID.get(tracker, tracker)
        if not cohort_id:
            continue
        old = events.get(cohort_id)
        old_ts = parse_utc(old.get("sent_timestamp_utc", "")) if old else None
        new_ts = parse_utc(row.get("sent_timestamp_utc", ""))
        if old is None or (new_ts and (old_ts is None or new_ts > old_ts)):
            events[cohort_id] = row
    return events


def days_between(later: datetime, earlier: datetime | None) -> str:
    if earlier is None:
        return ""
    return str(round((later - earlier).total_seconds() / 86400, 2))


def due_delta(due: datetime | None, as_of: datetime) -> str:
    if due is None:
        return ""
    return str(round((due - as_of).total_seconds() / 86400, 2))


def aging_band(sent: datetime | None, followup_due: datetime | None, escalation_due: datetime | None, as_of: datetime, request_sent: str) -> str:
    if request_sent != "yes" or sent is None:
        return "clock_not_started"
    if escalation_due and as_of >= escalation_due:
        return "escalation_overdue"
    if followup_due and as_of >= followup_due:
        return "followup_overdue"
    if followup_due and (followup_due - as_of).total_seconds() <= 2 * 86400:
        return "followup_due_soon"
    if followup_due:
        return "waiting"
    return "sent_due_unknown"


def action_for_band(band: str, fallback: str) -> str:
    if band == "clock_not_started":
        return fallback or "send_request_when_human_approves_contact"
    if band == "escalation_overdue":
        return "escalate_to_alternate_contact_or_author_run_route_if_terms_allow"
    if band == "followup_overdue":
        return "send_followup_now_or_escalate_if_already_followed_up"
    if band == "followup_due_soon":
        return "prepare_followup_and_send_on_due_date"
    if band == "waiting":
        return "wait_until_followup_due_date"
    return "repair_sent_log_due_dates"


def audit(
    blocker_board: Path,
    followup_board: Path,
    escalation_matrix: Path,
    sent_log: Path,
    as_of: datetime,
    outdir: Path,
) -> int:
    blocker_rows = read_tsv(resolve(blocker_board))
    followup_by_tracker = {row["cohort"]: row for row in read_tsv(resolve(followup_board))}
    escalation_by_id = {row["cohort_id"]: row for row in read_tsv(resolve(escalation_matrix))}
    sent_by_id = sent_events(read_tsv(resolve(sent_log)))
    outdir = resolve(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, object]] = []
    for blocker in blocker_rows:
        cohort_id = blocker["cohort_id"]
        tracker = blocker.get("tracker_cohort", "")
        followup = followup_by_tracker.get(tracker, {})
        escalation = escalation_by_id.get(cohort_id, {})
        sent = sent_by_id.get(cohort_id, {})
        request_sent = "yes" if sent else blocker.get("request_sent", followup.get("request_sent", "no"))
        sent_ts = parse_utc(sent.get("sent_timestamp_utc", followup.get("sent_timestamp_utc", "")))
        followup_due = parse_utc(sent.get("next_followup_due_utc", followup.get("next_followup_due_utc", "")))
        escalation_due = parse_utc(sent.get("escalation_due_utc", ""))
        band = aging_band(sent_ts, followup_due, escalation_due, as_of, request_sent)
        rows.append(
            {
                "cohort_id": cohort_id,
                "tracker_cohort": tracker,
                "blocker_type": blocker.get("blocker_type", ""),
                "request_sent": request_sent,
                "aging_band": band,
                "days_since_sent": days_between(as_of, sent_ts),
                "days_until_followup_due": due_delta(followup_due, as_of),
                "days_until_escalation_due": due_delta(escalation_due, as_of),
                "sent_timestamp_utc": sent.get("sent_timestamp_utc", followup.get("sent_timestamp_utc", "")),
                "next_followup_due_utc": sent.get("next_followup_due_utc", followup.get("next_followup_due_utc", "")),
                "escalation_due_utc": sent.get("escalation_due_utc", ""),
                "exact_unblocking_event": escalation.get("exact_unblocking_event", blocker.get("required_external_items", "")),
                "next_action": action_for_band(band, blocker.get("recommended_action", "")),
                "request_packet": blocker.get("request_packet", ""),
                "current_blocker": blocker.get("external_blocker", ""),
            }
        )
    rows.sort(key=lambda row: (str(row["aging_band"]), str(row["cohort_id"])))
    audit_path = outdir / "external_blocker_aging_audit.tsv"
    write_tsv(
        audit_path,
        rows,
        [
            "cohort_id",
            "tracker_cohort",
            "blocker_type",
            "request_sent",
            "aging_band",
            "days_since_sent",
            "days_until_followup_due",
            "days_until_escalation_due",
            "sent_timestamp_utc",
            "next_followup_due_utc",
            "escalation_due_utc",
            "exact_unblocking_event",
            "next_action",
            "request_packet",
            "current_blocker",
        ],
    )
    counts: dict[str, int] = {}
    for row in rows:
        counts[str(row["aging_band"])] = counts.get(str(row["aging_band"]), 0) + 1
    summary = {
        "synthetic": "synthetic" in rel(resolve(sent_log)).lower() or "synthetic" in rel(outdir).lower(),
        "purpose": "V46 external blocker aging audit; no biological claim",
        "as_of_utc": as_of.isoformat().replace("+00:00", "Z"),
        "n_routes": len(rows),
        "aging_band_counts": counts,
        "audit": rel(audit_path),
        "sources": {
            "blocker_board": rel(resolve(blocker_board)),
            "followup_board": rel(resolve(followup_board)),
            "escalation_matrix": rel(resolve(escalation_matrix)),
            "sent_log": rel(resolve(sent_log)),
        },
    }
    (outdir / "external_blocker_aging_audit_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


def write_synthetic_sent_log(path: Path) -> Path:
    rows = [
        {
            "cohort": "gafson_dmf_neda",
            "request_packet_path": "docs/validation/outbound_requests/gafson_dmf_ready_to_send_V45.md",
            "exact_sent_copy_path": "synthetic_sent",
            "sent_timestamp_utc": "2026-06-01T00:00:00Z",
            "sender_or_owner": "synthetic",
            "recipient_role": "corresponding_author",
            "recipient_private_details_committed": "no",
            "next_followup_due_utc": "2026-06-10T00:00:00Z",
            "escalation_due_utc": "2026-06-20T00:00:00Z",
            "request_tracker_updated": "yes",
            "triage_board_updated": "yes",
            "status": "sent_no_response_yet",
            "notes": "synthetic followup overdue",
        },
        {
            "cohort": "karolinska_dmf_ros",
            "request_packet_path": "docs/validation/outbound_requests/karolinska_dmf_ready_to_send_V45.md",
            "exact_sent_copy_path": "synthetic_sent",
            "sent_timestamp_utc": "2026-06-01T00:00:00Z",
            "sender_or_owner": "synthetic",
            "recipient_role": "corresponding_author",
            "recipient_private_details_committed": "no",
            "next_followup_due_utc": "2026-06-10T00:00:00Z",
            "escalation_due_utc": "2026-06-12T00:00:00Z",
            "request_tracker_updated": "yes",
            "triage_board_updated": "yes",
            "status": "sent_no_response_yet",
            "notes": "synthetic escalation overdue",
        },
        {
            "cohort": "gse228330_ocrelizumab",
            "request_packet_path": "docs/validation/outbound_requests/gse228330_ocrelizumab_ready_to_send_V45.md",
            "exact_sent_copy_path": "synthetic_sent",
            "sent_timestamp_utc": "2026-06-10T00:00:00Z",
            "sender_or_owner": "synthetic",
            "recipient_role": "corresponding_author",
            "recipient_private_details_committed": "no",
            "next_followup_due_utc": "2026-06-14T00:00:00Z",
            "escalation_due_utc": "2026-06-30T00:00:00Z",
            "request_tracker_updated": "yes",
            "triage_board_updated": "yes",
            "status": "sent_no_response_yet",
            "notes": "synthetic due soon",
        },
    ]
    fieldnames = list(rows[0])
    write_tsv(path, rows, fieldnames)
    return path


def synthetic_check(outdir: Path) -> int:
    outdir = resolve(outdir)
    if outdir.exists():
        shutil.rmtree(outdir)
    sent_log = write_synthetic_sent_log(outdir / "synthetic" / "synthetic_sent_log.tsv")
    as_of = parse_as_of("2026-06-13T00:00:00Z")
    audit(DEFAULT_BLOCKER, DEFAULT_FOLLOWUP, DEFAULT_ESCALATION, sent_log, as_of, outdir / "synthetic_audit")
    summary = json.loads((outdir / "synthetic_audit" / "external_blocker_aging_audit_summary.json").read_text())
    expected = {"escalation_overdue": 1, "followup_overdue": 1, "followup_due_soon": 1, "clock_not_started": 1}
    observed = summary["aging_band_counts"]
    rows = [
        {
            "expected_band": key,
            "expected_count": value,
            "observed_count": observed.get(key, 0),
            "expectation_met": str(observed.get(key, 0) == value).lower(),
        }
        for key, value in expected.items()
    ]
    write_tsv(outdir / "external_blocker_aging_synthetic_expectations.tsv", rows, ["expected_band", "expected_count", "observed_count", "expectation_met"])
    n_fail = sum(1 for row in rows if row["expectation_met"] != "true")
    final = {
        "synthetic": True,
        "purpose": "V46 external blocker aging audit synthetic verification; no biological claim",
        "n_expectation_failures": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
        "synthetic_audit_summary": rel(outdir / "synthetic_audit" / "external_blocker_aging_audit_summary.json"),
        "expectations": rel(outdir / "external_blocker_aging_synthetic_expectations.tsv"),
    }
    (outdir / "external_blocker_aging_synthetic_summary.json").write_text(json.dumps(final, indent=2, sort_keys=True) + "\n")
    print(json.dumps(final, indent=2, sort_keys=True))
    return 0 if n_fail == 0 else 2


def main() -> int:
    args = parse_args()
    if args.cmd == "synthetic-check":
        return synthetic_check(args.outdir)
    return audit(
        args.blocker_board,
        args.followup_board,
        args.escalation_matrix,
        args.sent_log,
        parse_as_of(args.as_of_utc),
        args.outdir,
    )


if __name__ == "__main__":
    raise SystemExit(main())
