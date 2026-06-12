#!/usr/bin/env python3
"""Generate a V45 request-sent intake log template from current actions.

The generated template is a draft-only operational aid. It does not mark any
request as sent and does not update receipt, triage, or harness readiness.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ACTIONS = ROOT / "analysis/v45_current_action_card/current_action_card.tsv"
DEFAULT_OUTDIR = ROOT / "analysis/v45_send_log_intake_template"

COHORT_ALIASES = {
    "gafson_dmf_2018": "gafson_dmf_neda",
    "karolinska_dmf_ros_2019": "karolinska_dmf_ros",
    "gse228330_ocrelizumab_pbmc": "gse228330_ocrelizumab",
    "any_author_run_fallback": "author_run_fallback",
}

SENT_COPY_STEMS = {
    "gafson_dmf_neda": "gafson_dmf_sent",
    "karolinska_dmf_ros": "karolinska_dmf_sent",
    "gse228330_ocrelizumab": "gse228330_ocrelizumab_sent",
    "author_run_fallback": "author_run_fallback_sent",
}

FIELDNAMES = [
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--actions", type=Path, default=DEFAULT_ACTIONS)
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


def recipient_role(recipient_or_path: str) -> str:
    if "@" in recipient_or_path:
        return "corresponding_author"
    if "data_controller" in recipient_or_path or "cohort_owner" in recipient_or_path:
        return "cohort_owner_or_data_controller"
    if recipient_or_path.startswith("authors_from_"):
        return "publication_authors"
    return "recipient_role_to_fill"


def template_rows(actions: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for action in actions:
        if action.get("action_type") != "send_or_approve_external_request":
            continue
        alias = COHORT_ALIASES.get(action.get("cohort_id", ""), action.get("cohort_id", ""))
        stem = SENT_COPY_STEMS.get(alias, f"{alias}_sent")
        rows.append(
            {
                "cohort": alias,
                "request_packet_path": action.get("request_or_packet", ""),
                "exact_sent_copy_path": f"docs/validation/outbound_requests/{stem}_<YYYY-MM-DD>.md",
                "sent_timestamp_utc": "<YYYY-MM-DDTHH:MM:SSZ>",
                "sender_or_owner": "<owner>",
                "recipient_role": recipient_role(action.get("recipient_or_path", "")),
                "recipient_private_details_committed": "no",
                "next_followup_due_utc": "<YYYY-MM-DDTHH:MM:SSZ>",
                "escalation_due_utc": "<YYYY-MM-DDTHH:MM:SSZ>",
                "request_tracker_updated": "no",
                "triage_board_updated": "no",
                "status": "draft",
                "notes": "generated_from_current_action_card; fill only after a request is actually sent",
            }
        )
    return rows


def write_tsv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    args = parse_args()
    actions_path = args.actions if args.actions.is_absolute() else ROOT / args.actions
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    rows = template_rows(read_tsv(actions_path))
    template_path = outdir / "send_log_intake_template.tsv"
    write_tsv(template_path, rows)
    summary = {
        "synthetic": False,
        "purpose": "V45 request-sent intake template; no biological claim",
        "actions_source": rel(actions_path),
        "template": rel(template_path),
        "n_rows": len(rows),
        "n_draft_rows": sum(1 for row in rows if row["status"] == "draft"),
        "n_sent_rows": sum(1 for row in rows if row["status"] != "draft"),
        "allowed_effect": "draft_template_only_no_tracker_or_triage_update",
    }
    (outdir / "send_log_intake_template_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
