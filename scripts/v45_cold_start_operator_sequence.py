#!/usr/bin/env python3
"""Generate cold-start operator sequence from current V45 route state.

Plan-only infrastructure. This script reads committed status/route tables and
writes an operator sequence; it does not inspect data or run validation.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v45_cold_start_operator_sequence"

COMMAND_PLAN = {
    "gafson_dmf_2018": "analysis/v45_validation_command_runner/gafson_primary_plan/command_plan.md",
    "karolinska_dmf_ros_2019": "analysis/v45_validation_command_runner/karolinska_primary_plan/command_plan.md",
    "gse228330_ocrelizumab_pbmc": "analysis/v45_validation_command_runner/gse228330_pharmacodynamic_plan/command_plan.md",
    "any_author_run_fallback": "docs/validation/AUTHOR_RUN_RETURN_OPERATOR_CHECKLIST_V45.md",
}
RETURNED_PACKAGE_REGRESSION_COMMAND = ".venv/bin/python scripts/v46_returned_package_regression_suite.py --outdir analysis/v46_returned_package_regression_suite --fail-on-error"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    return parser.parse_args()


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def read_tsv(path: str) -> pd.DataFrame:
    return pd.read_csv(ROOT / path, sep="\t", dtype=str).fillna("")


def write_tsv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="") as handle:
        fieldnames = list(rows[0].keys()) if rows else []
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    args = parse_args()
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    actions = read_tsv("analysis/v45_current_action_card/current_action_card.tsv")
    decision = read_tsv("analysis/v45_received_package_decision_tree/live/received_package_decision_tree.tsv")
    packets = read_tsv("analysis/v45_route_arrival_packets/route_arrival_packet_index.tsv")

    action_by_route = {row["cohort_id"]: row for row in actions.to_dict(orient="records")}
    decision_by_route = {row["cohort_id"]: row for row in decision.to_dict(orient="records")}
    packet_by_route = {row["cohort_id"]: row for row in packets.to_dict(orient="records")}

    rows: list[dict[str, str]] = []
    for priority, cohort_id in enumerate(sorted(action_by_route, key=lambda cid: int(action_by_route[cid]["priority"])), start=1):
        action = action_by_route[cohort_id]
        dec = decision_by_route.get(cohort_id, {})
        packet = packet_by_route.get(cohort_id, {})
        plan = COMMAND_PLAN.get(cohort_id, "")
        rows.append(
            {
                "priority": str(priority),
                "cohort_id": cohort_id,
                "current_state": dec.get("derived_state", ""),
                "current_blocker": action.get("blocker", ""),
                "operator_now": action.get("recommended_action", ""),
                "request_or_packet": action.get("request_or_packet", ""),
                "recipient_or_path": action.get("recipient_or_path", ""),
                "if_package_arrives": dec.get("if_package_arrives", ""),
                "arrival_packet": packet.get("packet", dec.get("arrival_packet", "")),
                "status_template": dec.get("operator_status_template", ""),
                "status_updater_or_gate": dec.get("status_updater_or_gate", ""),
                "pre_return_package_regression": RETURNED_PACKAGE_REGRESSION_COMMAND,
                "command_plan_or_return_gate": plan,
                "may_score_now": dec.get("may_score_now", "no"),
                "hard_stop": dec.get("hard_stop", "no module scoring, outcome scoring, or interpretation until gates pass"),
            }
        )

    table = outdir / "cold_start_operator_sequence.tsv"
    write_tsv(table, rows)

    md = outdir / "COLD_START_OPERATOR_SEQUENCE.md"
    lines = [
        "# V45 Cold-Start Operator Sequence",
        "",
        "Status: generated operational plan. No biological claim and no scoring authorization.",
        "",
        "Use this when resuming from a clean checkout or when a package arrives. It is derived from the current action card, route-arrival packet index, received-package decision tree, and command-plan outputs.",
        "",
        "Hard rule: if `may_score_now` is `no`, do not run module scoring, outcome scoring, or interpretation.",
        "",
        "| Priority | Cohort | Current blocker | Operator now | If package arrives | Gate / command plan | May score now |",
        "|---:|---|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['priority']} | `{row['cohort_id']}` | `{row['current_blocker']}` | "
            f"{row['operator_now']} | {row['if_package_arrives']} | "
            f"`{row['pre_return_package_regression']}` then `{row['command_plan_or_return_gate']}` | `{row['may_score_now']}` |"
        )
    lines.extend(
        [
            "",
            "## Required Source Artifacts",
            "",
            "- `analysis/v45_current_action_card/current_action_card.tsv`",
            "- `analysis/v45_received_package_decision_tree/live/received_package_decision_tree.tsv`",
            "- `analysis/v45_route_arrival_packets/route_arrival_packet_index.tsv`",
            "- `analysis/v46_returned_package_regression_suite/returned_package_regression_summary.json`",
            "",
            "This generated sequence is an operator convenience layer. The linked route packet and frozen preregistration remain authoritative.",
        ]
    )
    md.write_text("\n".join(lines) + "\n")

    n_may_score = sum(1 for row in rows if row["may_score_now"].lower() == "yes")
    summary = {
        "synthetic": False,
        "purpose": "V45 cold-start operator sequence; no biological claim",
        "n_routes": len(rows),
        "n_may_score_now": n_may_score,
        "overall_status": "PASS" if n_may_score == 0 else "CHECK_SCORE_AUTHORIZATION",
        "table": rel(table),
        "markdown": rel(md),
    }
    (outdir / "cold_start_operator_sequence_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
