#!/usr/bin/env python3
"""Build a read-only V45 validation-readiness status dashboard.

This dashboard aggregates existing operations and governance outputs. It does
not run validation, score data, or change any tracker.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v45_readiness_status_dashboard"

DEFAULTS = {
    "tracker": ROOT / "analysis/v45_outbound_data_requests/request_tracker.tsv",
    "triage": ROOT / "analysis/v45_received_data_triage/received_data_triage_status.tsv",
    "precommit": ROOT / "analysis/v45_precommit_readiness/precommit_readiness_summary.json",
    "path_resolver": ROOT / "analysis/v45_collaborator_path_resolver/live_sources/collaborator_package_path_resolution_summary.json",
    "followup": ROOT / "analysis/v45_followup_due_board/live_template/followup_due_board_summary.json",
    "external_blocker": ROOT / "analysis/v45_external_blocker_board/external_blocker_board_summary.json",
    "handoff_not_received": ROOT / "analysis/v45_handoff_completeness/handoff_completeness_summary.json",
    "handoff_scored_missing": ROOT / "analysis/v45_handoff_completeness_scored_missing/handoff_completeness_summary.json",
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


def read_json(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError:
        return {}


def read_tsv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return [{key: (value or "") for key, value in row.items()} for row in reader]


def count(rows: list[dict[str, str]], column: str, value: str) -> int:
    return sum(1 for row in rows if str(row.get(column, "")).strip().lower() == value)


def dashboard_rows() -> tuple[list[dict[str, str]], dict[str, object]]:
    tracker = read_tsv(DEFAULTS["tracker"])
    triage = read_tsv(DEFAULTS["triage"])
    precommit = read_json(DEFAULTS["precommit"])
    path_resolver = read_json(DEFAULTS["path_resolver"])
    followup = read_json(DEFAULTS["followup"])
    external_blocker = read_json(DEFAULTS["external_blocker"])
    handoff_not_received = read_json(DEFAULTS["handoff_not_received"])
    handoff_scored_missing = read_json(DEFAULTS["handoff_scored_missing"])

    tracker_ready = sum(1 for row in tracker if "ready" in row.get("status", "").lower())
    tracker_sent = count(tracker, "request_sent", "yes")
    triage_harness_ready = count(triage, "harness_ready", "yes")
    triage_request_sent = count(triage, "request_sent", "yes")

    rows = [
        {
            "area": "outbound_requests",
            "status": "ACTION_NEEDED",
            "metric": f"{tracker_ready}/{len(tracker)} tracker rows ready; {tracker_sent} marked sent",
            "source": rel(DEFAULTS["tracker"]),
            "interpretation": "send/author-run requests remain external acquisition actions, not validation",
        },
        {
            "area": "received_data_triage",
            "status": "AWAITING_EXTERNAL_DATA" if triage_harness_ready == 0 else "HARNESS_READY_EXISTS",
            "metric": f"{triage_harness_ready}/{len(triage)} cohorts harness-ready; {triage_request_sent} requests sent on board",
            "source": rel(DEFAULTS["triage"]),
            "interpretation": "no frozen harness should run until a cohort is harness-ready",
        },
        {
            "area": "precommit_readiness",
            "status": str(precommit.get("overall_status", "MISSING")),
            "metric": f"{precommit.get('n_pass', 0)}/{precommit.get('n_steps', 0)} checks pass; {precommit.get('total_elapsed_seconds', 'na')} seconds",
            "source": rel(DEFAULTS["precommit"]),
            "interpretation": "repository/readiness guard status only",
        },
        {
            "area": "collaborator_path_resolution",
            "status": str(path_resolver.get("overall_status", "MISSING")),
            "metric": f"{path_resolver.get('n_pass', 0)} resolved; {path_resolver.get('n_missing', 'na')} missing",
            "source": rel(DEFAULTS["path_resolver"]),
            "interpretation": "handoff links resolve; no validation claim",
        },
        {
            "area": "followup_due_board",
            "status": "ACTION_NEEDED",
            "metric": json.dumps(followup.get("due_status_counts", {}), sort_keys=True),
            "source": rel(DEFAULTS["followup"]),
            "interpretation": "acquisition action status only",
        },
        {
            "area": "external_blocker_board",
            "status": "ACTION_NEEDED" if external_blocker.get("n_harness_ready", 0) == 0 else "REVIEW",
            "metric": json.dumps(external_blocker.get("blocker_type_counts", {}), sort_keys=True),
            "source": rel(DEFAULTS["external_blocker"]),
            "interpretation": "external blockers remain separate from internal readiness work",
        },
        {
            "area": "handoff_not_received_lifecycle",
            "status": str(handoff_not_received.get("overall_status", "MISSING")),
            "metric": f"{handoff_not_received.get('n_present', 0)}/{handoff_not_received.get('n_required_now', 0)} required-now artifacts present",
            "source": rel(DEFAULTS["handoff_not_received"]),
            "interpretation": "pre-receipt handoff state should pass with only currently required artifacts",
        },
        {
            "area": "handoff_scored_lifecycle_negative_control",
            "status": "EXPECTED_FAIL" if handoff_scored_missing.get("overall_status") == "FAIL" else str(handoff_scored_missing.get("overall_status", "MISSING")),
            "metric": f"{handoff_scored_missing.get('n_hard_fail', 'na')} hard missing scored-state outputs",
            "source": rel(DEFAULTS["handoff_scored_missing"]),
            "interpretation": "scored-state failure is expected before data/harness outputs exist",
        },
    ]

    internal_ok = (
        precommit.get("overall_status") == "PASS"
        and path_resolver.get("overall_status") == "PASS"
        and handoff_not_received.get("overall_status") == "PASS"
    )
    if internal_ok and triage_harness_ready == 0:
        headline = "READY_AWAITING_EXTERNAL_DATA"
    elif not internal_ok:
        headline = "INTERNAL_GUARD_REPAIR_NEEDED"
    else:
        headline = "HARNESS_READY_REVIEW_REQUIRED"
    summary = {
        "synthetic": False,
        "purpose": "V45 readiness status dashboard; no biological claim",
        "headline_status": headline,
        "n_tracker_rows": len(tracker),
        "n_tracker_ready": tracker_ready,
        "n_tracker_sent": tracker_sent,
        "n_triage_rows": len(triage),
        "n_harness_ready": triage_harness_ready,
        "precommit_status": precommit.get("overall_status", "MISSING"),
        "path_resolver_status": path_resolver.get("overall_status", "MISSING"),
        "external_blocker_counts": external_blocker.get("blocker_type_counts", {}),
        "handoff_not_received_status": handoff_not_received.get("overall_status", "MISSING"),
        "handoff_scored_negative_control_status": rows[-1]["status"],
    }
    return rows, summary


def write_markdown(path: Path, rows: list[dict[str, str]], summary: dict[str, object]) -> None:
    lines = [
        "# V45 Readiness Status Dashboard",
        "",
        "Status: generated dashboard. No biological claim.",
        "",
        f"Headline status: `{summary['headline_status']}`",
        "",
        "| Area | Status | Metric | Interpretation |",
        "|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['area']} | `{row['status']}` | {row['metric']} | {row['interpretation']} |"
        )
    lines.extend(
        [
            "",
            "A ready dashboard means internal operational guards are in place. It does not",
            "mean any cohort has been received, scored, or validated.",
            "",
        ]
    )
    path.write_text("\n".join(lines))


def main() -> int:
    args = parse_args()
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    outdir.mkdir(parents=True, exist_ok=True)
    rows, summary = dashboard_rows()

    table_path = outdir / "readiness_status_dashboard.tsv"
    with table_path.open("w", newline="") as handle:
        fieldnames = ["area", "status", "metric", "source", "interpretation"]
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    summary["dashboard_table"] = rel(table_path)
    (outdir / "readiness_status_dashboard_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    write_markdown(outdir / "READINESS_STATUS_DASHBOARD.md", rows, summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
