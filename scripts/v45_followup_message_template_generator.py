#!/usr/bin/env python3
"""Generate unsent acquisition message drafts from a follow-up due board.

The drafts are operational templates only. Generating a draft does not mark a
request sent, followed up, received, or validated.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BOARD = ROOT / "analysis/v45_followup_due_board/live_template/followup_due_board.tsv"
DEFAULT_OUTDIR = ROOT / "analysis/v45_followup_message_templates"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--board", type=Path, default=DEFAULT_BOARD)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
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


def slug(value: str) -> str:
    return value.lower().replace("/", "_").replace(" ", "_")


def subject_for(status: str, cohort: str) -> str:
    if status == "overdue":
        return f"Follow-up on MS validation data request: {cohort}"
    if status == "due_soon":
        return f"Upcoming follow-up on MS validation data request: {cohort}"
    if status == "sent_due_unknown":
        return f"Follow-up date clarification for MS validation data request: {cohort}"
    return f"MS validation data request packet: {cohort}"


def body_for(row: dict[str, str]) -> str:
    status = row.get("due_status", "")
    cohort = row.get("cohort", "")
    packet = row.get("prepared_request", "")
    blocker = row.get("minimum_external_blocker", "")
    if status in {"overdue", "due_soon"}:
        opener = "I am following up on the prior request" if status == "overdue" else "I am preparing a scheduled follow-up"
        return (
            f"Dear [recipient],\n\n"
            f"{opener} for the {cohort} validation data route. The current external blocker is:\n\n"
            f"{blocker}\n\n"
            "If individual-level data transfer is not possible, the author-run aggregate-output fallback remains available. "
            "Any returned package should follow the frozen harness and aggregate-output specification without changing modules, endpoints, thresholds, or timepoints.\n\n"
            "Kind regards,\n[Name / affiliation]\n"
        )
    if status == "sent_due_unknown":
        return (
            f"Dear [operator],\n\n"
            f"The sent-log row for {cohort} does not include a usable follow-up due date. "
            "Repair the request-sent log before sending any follow-up.\n"
        )
    return (
        f"Dear [recipient],\n\n"
        f"We are preparing the request packet for the {cohort} route. The prepared request is:\n\n"
        f"{packet}\n\n"
        f"The minimum external blocker to resolve is:\n\n{blocker}\n\n"
        "Please send only after the human contact/recipient decision is approved, then record the exact sent copy and follow-up date in the request-sent log.\n\n"
        "Kind regards,\n[Name / affiliation]\n"
    )


def main() -> int:
    args = parse_args()
    board_path = resolve(args.board)
    outdir = resolve(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    rows = read_tsv(board_path)
    index_rows = []
    counts: dict[str, int] = {}
    for row in rows:
        status = row.get("due_status", "unknown")
        counts[status] = counts.get(status, 0) + 1
        draft = outdir / f"{slug(row.get('cohort', 'unknown'))}_{status}_draft.md"
        draft.write_text(
            f"# Unsent Draft: {row.get('cohort', '')}\n\n"
            "Status: unsent operational draft. Creating this file does not mark any request sent.\n\n"
            f"Due status: `{status}`\n\n"
            f"Recommended action: `{row.get('recommended_action', '')}`\n\n"
            f"Subject: {subject_for(status, row.get('cohort', ''))}\n\n"
            "```text\n"
            f"{body_for(row)}"
            "```\n"
        )
        index_rows.append(
            {
                "cohort": row.get("cohort", ""),
                "due_status": status,
                "recommended_action": row.get("recommended_action", ""),
                "draft": rel(draft),
            }
        )
    index_path = outdir / "followup_message_template_index.tsv"
    with index_path.open("w", newline="") as handle:
        fieldnames = ["cohort", "due_status", "recommended_action", "draft"]
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(index_rows)
    summary = {
        "synthetic": "synthetic" in rel(board_path).lower(),
        "purpose": "unsent acquisition follow-up message templates; no biological claim",
        "board": rel(board_path),
        "n_drafts": len(index_rows),
        "due_status_counts": counts,
        "index": rel(index_path),
    }
    (outdir / "followup_message_template_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
