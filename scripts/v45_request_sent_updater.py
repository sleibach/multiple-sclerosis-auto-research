#!/usr/bin/env python3
"""Propose outbound tracker updates from an explicitly filled request-sent log.

This script is acquisition-operations only. It does not infer that a request
was sent from a ready-to-send packet. A row updates the proposed tracker only
when the request-sent log records a sent status and concrete sent metadata.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LOG = ROOT / "docs/validation/input_schemas/V45_request_sent_log_template.tsv"
DEFAULT_TRACKER = ROOT / "analysis/v45_outbound_data_requests/request_tracker.tsv"
DEFAULT_TRIAGE = ROOT / "analysis/v45_received_data_triage/received_data_triage_status.tsv"
DEFAULT_OUTDIR = ROOT / "analysis/v45_request_sent_updater"

REQUIRED_LOG_COLUMNS = [
    "cohort",
    "request_packet_path",
    "exact_sent_copy_path",
    "sent_timestamp_utc",
    "sender_or_owner",
    "recipient_role",
    "recipient_private_details_committed",
    "next_followup_due_utc",
    "escalation_due_utc",
    "request_tracker_updated",
    "triage_board_updated",
    "status",
    "notes",
]

SENT_STATUSES = {
    "sent",
    "sent_logged",
    "sent_waiting_response",
    "sent_no_response_yet",
    "sent_followup_pending",
}
DRAFT_STATUSES = {"draft", "todo", "not_sent", "ready_unsent", "optional_ready_unsent", ""}

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

TRIAGE_ALIASES = {
    "gafson_dmf_neda": "gafson_dmf_2018",
    "gafson_dmf_2018": "gafson_dmf_2018",
    "karolinska_dmf_ros": "karolinska_dmf_ros_2019",
    "karolinska_dmf_ros_2019": "karolinska_dmf_ros_2019",
    "gse228330_ocrelizumab": "gse228330_ocrelizumab_pbmc",
    "gse228330_ocrelizumab_pbmc": "gse228330_ocrelizumab_pbmc",
}

TRACKER_EXTRA_COLUMNS = [
    "request_sent",
    "sent_timestamp_utc",
    "sent_copy_path",
    "sender_or_owner",
    "recipient_role_logged",
    "next_followup_due_utc",
    "escalation_due_utc",
    "request_sent_log_status",
    "request_sent_log_notes",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sent-log", type=Path, default=DEFAULT_LOG)
    parser.add_argument("--tracker", type=Path, default=DEFAULT_TRACKER)
    parser.add_argument("--triage-board", type=Path, default=DEFAULT_TRIAGE)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    parser.add_argument(
        "--write-tracker",
        action="store_true",
        help="Overwrite the canonical outbound tracker with the proposed tracker.",
    )
    parser.add_argument(
        "--write-triage-board",
        action="store_true",
        help="Overwrite the canonical triage board with the proposed triage request_sent values.",
    )
    return parser.parse_args()


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def read_tsv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if reader.fieldnames is None:
            raise ValueError(f"{path} has no header")
        rows = [{key: (value or "") for key, value in row.items()} for row in reader]
        return list(reader.fieldnames), rows


def write_tsv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def norm(value: object) -> str:
    return str(value).strip().lower()


def has_placeholder(value: str) -> bool:
    stripped = value.strip()
    return not stripped or "<" in stripped or ">" in stripped


def valid_utc(value: str) -> bool:
    if has_placeholder(value):
        return False
    candidate = value.strip()
    if candidate.endswith("Z"):
        candidate = candidate[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(candidate)
    except ValueError:
        return False
    return parsed.tzinfo is not None and parsed.astimezone(timezone.utc) is not None


def sent_date(timestamp: str) -> str:
    return timestamp.strip()[:10]


def audit_log_row(row: dict[str, str]) -> dict[str, str]:
    status = norm(row.get("status", ""))
    audit = {
        "cohort": row.get("cohort", ""),
        "status": row.get("status", ""),
        "action": "ignored",
        "tracker_cohort": TRACKER_ALIASES.get(norm(row.get("cohort", "")), ""),
        "triage_cohort": TRIAGE_ALIASES.get(norm(row.get("cohort", "")), ""),
        "hard_failure": "no",
        "failure_reason": "",
    }
    if status in DRAFT_STATUSES:
        audit["failure_reason"] = "not_sent_status"
        return audit
    if status not in SENT_STATUSES:
        audit["hard_failure"] = "yes"
        audit["failure_reason"] = "unknown_status"
        return audit
    failures: list[str] = []
    for column in [
        "cohort",
        "request_packet_path",
        "exact_sent_copy_path",
        "sent_timestamp_utc",
        "sender_or_owner",
        "recipient_role",
        "next_followup_due_utc",
    ]:
        if has_placeholder(row.get(column, "")):
            failures.append(f"{column}_missing_or_placeholder")
    if norm(row.get("recipient_private_details_committed", "")) not in {"no", "not_applicable", "n/a"}:
        failures.append("private_recipient_details_marked_committed")
    if not valid_utc(row.get("sent_timestamp_utc", "")):
        failures.append("sent_timestamp_not_utc_iso")
    if not valid_utc(row.get("next_followup_due_utc", "")):
        failures.append("next_followup_due_not_utc_iso")
    if row.get("escalation_due_utc", "").strip() and not has_placeholder(row.get("escalation_due_utc", "")):
        if not valid_utc(row.get("escalation_due_utc", "")):
            failures.append("escalation_due_not_utc_iso")
    sent_copy = resolve(Path(row.get("exact_sent_copy_path", "")))
    if not sent_copy.exists():
        failures.append("exact_sent_copy_path_not_found")
    if not audit["tracker_cohort"]:
        failures.append("cohort_not_mapped_to_tracker")
    if failures:
        audit["hard_failure"] = "yes"
        audit["failure_reason"] = ";".join(failures)
    else:
        audit["action"] = "propose_sent_update"
    return audit


def ensure_columns(fieldnames: list[str], extra: list[str]) -> list[str]:
    out = list(fieldnames)
    for field in extra:
        if field not in out:
            out.append(field)
    return out


def update_tracker(
    fieldnames: list[str],
    rows: list[dict[str, str]],
    log_rows: list[dict[str, str]],
    audits: list[dict[str, str]],
) -> tuple[list[str], list[dict[str, str]], int]:
    fields = ensure_columns(fieldnames, TRACKER_EXTRA_COLUMNS)
    by_cohort = {row.get("cohort", ""): row for row in rows}
    updates = 0
    for log_row, audit in zip(log_rows, audits):
        if audit["action"] != "propose_sent_update":
            continue
        tracker_cohort = audit["tracker_cohort"]
        row = by_cohort.get(tracker_cohort)
        if row is None:
            audit["hard_failure"] = "yes"
            audit["failure_reason"] = "tracker_row_not_found"
            audit["action"] = "blocked"
            continue
        row["status"] = "request_sent_waiting_response"
        row["request_sent"] = "yes"
        row["sent_timestamp_utc"] = log_row["sent_timestamp_utc"].strip()
        row["sent_copy_path"] = log_row["exact_sent_copy_path"].strip()
        row["sender_or_owner"] = log_row["sender_or_owner"].strip()
        row["recipient_role_logged"] = log_row["recipient_role"].strip()
        row["next_followup_due_utc"] = log_row["next_followup_due_utc"].strip()
        row["escalation_due_utc"] = log_row["escalation_due_utc"].strip()
        row["request_sent_log_status"] = log_row["status"].strip()
        row["request_sent_log_notes"] = log_row.get("notes", "").strip()
        row["next_internal_action"] = "await_response_then_receipt_checksum_and_preflight"
        row["followup_rule"] = f"follow_up_due_{sent_date(log_row['next_followup_due_utc'])}"
        updates += 1
    return fields, rows, updates


def update_triage(
    fieldnames: list[str],
    rows: list[dict[str, str]],
    log_rows: list[dict[str, str]],
    audits: list[dict[str, str]],
) -> tuple[list[str], list[dict[str, str]], int]:
    by_cohort = {row.get("cohort_id", ""): row for row in rows}
    updates = 0
    for log_row, audit in zip(log_rows, audits):
        if audit["action"] != "propose_sent_update":
            continue
        triage_cohort = audit["triage_cohort"]
        if not triage_cohort:
            continue
        row = by_cohort.get(triage_cohort)
        if row is None:
            continue
        row["request_sent"] = "yes"
        row["harness_ready"] = "no"
        if norm(row.get("data_received", "")) in {"no", "public_partial", "public_partial_labels_absent", ""}:
            row["current_blocker"] = "awaiting_external_response_or_data_package"
            row["next_action"] = "wait_for_response_then_quarantine_checksum_preflight"
        updates += 1
    return fieldnames, rows, updates


def main() -> int:
    args = parse_args()
    sent_log_path = resolve(args.sent_log)
    tracker_path = resolve(args.tracker)
    triage_path = resolve(args.triage_board)
    outdir = resolve(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    log_fields, log_rows = read_tsv(sent_log_path)
    missing = [field for field in REQUIRED_LOG_COLUMNS if field not in log_fields]
    if missing:
        raise SystemExit(f"sent log missing required columns: {', '.join(missing)}")

    tracker_fields, tracker_rows = read_tsv(tracker_path)
    triage_fields, triage_rows = read_tsv(triage_path)

    audits = [audit_log_row(row) for row in log_rows]
    tracker_fields, proposed_tracker, tracker_updates = update_tracker(tracker_fields, tracker_rows, log_rows, audits)
    triage_fields, proposed_triage, triage_updates = update_triage(triage_fields, triage_rows, log_rows, audits)

    tracker_out = outdir / "request_tracker.proposed.tsv"
    triage_out = outdir / "received_data_triage_status.proposed.tsv"
    audit_out = outdir / "request_sent_log_audit.tsv"
    write_tsv(tracker_out, tracker_fields, proposed_tracker)
    write_tsv(triage_out, triage_fields, proposed_triage)
    write_tsv(
        audit_out,
        ["cohort", "status", "action", "tracker_cohort", "triage_cohort", "hard_failure", "failure_reason"],
        audits,
    )

    hard_failures = [row for row in audits if row["hard_failure"] == "yes"]
    if args.write_tracker:
        write_tsv(tracker_path, tracker_fields, proposed_tracker)
    if args.write_triage_board:
        write_tsv(triage_path, triage_fields, proposed_triage)

    summary = {
        "synthetic": "synthetic" in rel(sent_log_path).lower(),
        "purpose": "request-sent operations updater; no biological claim",
        "sent_log": rel(sent_log_path),
        "tracker": rel(tracker_path),
        "triage_board": rel(triage_path),
        "proposed_tracker": rel(tracker_out),
        "proposed_triage_board": rel(triage_out),
        "audit": rel(audit_out),
        "n_log_rows": len(log_rows),
        "n_sent_rows_accepted": sum(1 for row in audits if row["action"] == "propose_sent_update"),
        "n_draft_or_ignored_rows": sum(1 for row in audits if row["failure_reason"] == "not_sent_status"),
        "n_hard_failures": len(hard_failures),
        "tracker_updates_proposed": tracker_updates,
        "triage_updates_proposed": triage_updates,
        "write_tracker": bool(args.write_tracker),
        "write_triage_board": bool(args.write_triage_board),
    }
    (outdir / "request_sent_update_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 1 if hard_failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
