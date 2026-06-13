#!/usr/bin/env python3
"""Build a first-30-minute returned-package status-board dry run.

This is operator infrastructure only. It composes existing V46 returned-package
guardrail artifacts into a status-board view that can be shared with the team
before any result values are inspected. It does not read real returned scores,
expression data, labels, or quarantined cohorts.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v46_first30_returned_package_status_board_dryrun"
FIRST30_TABLE = ROOT / "analysis/v46_first30_returned_package_decision_table/first30_returned_package_decision_table.tsv"
REPAIR_TEMPLATE_INDEX = ROOT / "analysis/v46_return_repair_request_templates/repair_request_template_index.tsv"


STATUS_CASES = [
    {
        "scenario": "scored_canonical_aggregate",
        "board_status": "ROUTE_READY_FOR_GATED_REVIEW",
        "status_summary": "Canonical aggregate return is ready for the frozen gate sequence.",
        "blocker": "none",
        "next_step_order": "4",
        "repair_template_id": "",
        "allowed_language": "Returned package is in pre-result gated review; no validation interpretation is available yet.",
    },
    {
        "scenario": "scored_noncanonical_aggregate",
        "board_status": "FORMAT_NORMALIZATION_REQUIRED",
        "status_summary": "Noncanonical aggregate aliases must be normalized before gate and schema checks.",
        "blocker": "noncanonical aggregate aliases",
        "next_step_order": "5",
        "repair_template_id": "schema_or_metric_format_mismatch",
        "allowed_language": "Returned package requires format normalization before any result interpretation is available.",
    },
    {
        "scenario": "scored_unknown_alias_aggregate",
        "board_status": "FORMAT_ALIAS_TRIAGE_REQUIRED",
        "status_summary": "Metric format is unknown; run the adapter branch and stop if required tables remain unmapped.",
        "blocker": "unknown aggregate alias state",
        "next_step_order": "5",
        "repair_template_id": "schema_or_metric_format_mismatch",
        "allowed_language": "Returned package is in format triage; no validation interpretation is available yet.",
    },
    {
        "scenario": "unscoreable_aggregate",
        "board_status": "UNSCOREABLE_AGGREGATE_PREFLIGHT",
        "status_summary": "Package may contain context only or incomplete aggregate outputs; completeness must block before reporting.",
        "blocker": "missing or unscoreable aggregate outputs",
        "next_step_order": "5",
        "repair_template_id": "missing_score_bearing_aggregate_outputs",
        "allowed_language": "Returned package is not result-reviewable unless required aggregate outputs are supplied.",
    },
    {
        "scenario": "partial_label_scored_aggregate",
        "board_status": "PARTIAL_LABEL_PAIR_COUNT_REQUIRED",
        "status_summary": "Labeled analyzable-pair count must be computed before any bounded wording is selected.",
        "blocker": "partial or unmapped response labels",
        "next_step_order": "7",
        "repair_template_id": "response_labels_absent_or_unmapped",
        "allowed_language": "Returned package needs response-label coverage classification before any validation interpretation is available.",
    },
    {
        "scenario": "terms_blocked_return",
        "board_status": "BLOCKED_TERMS_OR_RECEIPT",
        "status_summary": "Data-use terms or receipt metadata block package handling.",
        "blocker": "terms or receipt clearance missing",
        "next_step_order": "4",
        "repair_template_id": "terms_or_receipt_not_cleared",
        "allowed_language": "Returned package is blocked at terms or receipt clearance; no package review is permitted yet.",
    },
]

FORBIDDEN_LANGUAGE = [
    "auc",
    "validated",
    "validation result",
    "clinical",
    "kill",
    "passed",
    "failed",
    "breakthrough",
    "effect size",
    "response-predictive",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    parser.add_argument("--fail-on-error", action="store_true")
    return parser.parse_args()


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return [{key: value or "" for key, value in row.items()} for row in csv.DictReader(handle, delimiter="\t")]


def write_tsv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def first30_by_scenario_step() -> dict[tuple[str, str], dict[str, str]]:
    return {(row["scenario"], row["step_order"]): row for row in read_tsv(FIRST30_TABLE)}


def repair_templates() -> dict[str, dict[str, str]]:
    return {row["template_id"]: row for row in read_tsv(REPAIR_TEMPLATE_INDEX)}


def build_board() -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    first30 = first30_by_scenario_step()
    templates = repair_templates()
    rows: list[dict[str, object]] = []
    checks: list[dict[str, object]] = []

    for case in STATUS_CASES:
        key = (case["scenario"], case["next_step_order"])
        first30_row = first30.get(key, {})
        template_id = case["repair_template_id"]
        template = templates.get(template_id, {}) if template_id else {}
        next_command = first30_row.get("command_or_artifact", "")
        row = {
            "scenario": case["scenario"],
            "board_status": case["board_status"],
            "status_summary": case["status_summary"],
            "blocker": case["blocker"],
            "next_minute_window": first30_row.get("minute_window", ""),
            "next_step_order": case["next_step_order"],
            "next_action": first30_row.get("action", ""),
            "next_command_or_artifact": next_command,
            "stop_route_if_next_step_fails": first30_row.get("route_to_if_stopped", ""),
            "repair_template_id": template_id,
            "repair_template_path": template.get("template_path", ""),
            "allowed_language": case["allowed_language"],
            "team_status_sentence": f"{case['status_summary']} {case['allowed_language']}",
            "score_values_read": "false",
        }
        rows.append(row)

        checks.extend(
            [
                {
                    "scenario": case["scenario"],
                    "check": "first30_step_exists",
                    "status": "PASS" if first30_row else "FAIL",
                    "detail": f"{case['scenario']} step {case['next_step_order']}",
                },
                {
                    "scenario": case["scenario"],
                    "check": "next_command_present",
                    "status": "PASS" if next_command else "FAIL",
                    "detail": next_command,
                },
                {
                    "scenario": case["scenario"],
                    "check": "repair_template_exists_or_not_needed",
                    "status": "PASS" if (not template_id or template) else "FAIL",
                    "detail": template_id or "not_needed",
                },
                {
                    "scenario": case["scenario"],
                    "check": "score_values_read_false",
                    "status": "PASS" if row["score_values_read"] == "false" else "FAIL",
                    "detail": str(row["score_values_read"]),
                },
            ]
        )
        text = f"{row['allowed_language']} {row['team_status_sentence']}".lower()
        forbidden_hits = [term for term in FORBIDDEN_LANGUAGE if term in text]
        checks.append(
            {
                "scenario": case["scenario"],
                "check": "allowed_language_pre_result",
                "status": "FAIL" if forbidden_hits else "PASS",
                "detail": ";".join(forbidden_hits) if forbidden_hits else row["allowed_language"],
            }
        )

    scenario_set = {row["scenario"] for row in read_tsv(FIRST30_TABLE)}
    status_set = {case["scenario"] for case in STATUS_CASES}
    checks.append(
        {
            "scenario": "all",
            "check": "all_first30_scenarios_represented",
            "status": "PASS" if scenario_set == status_set else "FAIL",
            "detail": f"first30={sorted(scenario_set)} status_board={sorted(status_set)}",
        }
    )
    return rows, checks


def write_markdown(path: Path, rows: list[dict[str, object]], summary: dict[str, object]) -> None:
    lines = [
        "# First-30 Returned-Package Status Board Dry Run V46",
        "",
        "Status: operator infrastructure. No validation result and no biological claim.",
        "",
        "This dry-run board summarizes the first-30-minute returned-package route",
        "status without reading result values. It is intended for team status updates",
        "before the V46 safe-interpretation classifier and V42 grid permit any result",
        "language.",
        "",
        f"Rows: `{summary['n_board_rows']}`; lint checks: `{summary['n_lint_checks']}`; failures: `{summary['n_lint_fail']}`.",
        "",
        "| Scenario | Status | Blocker | Next action | Repair template |",
        "|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| `{row['scenario']}` | `{row['board_status']}` | {row['blocker']} | "
            f"{row['next_action']} | `{row['repair_template_id'] or 'not_needed'}` |"
        )
    lines.extend(
        [
            "",
            "Every row has `score_values_read=false`. Status sentences are deliberately",
            "pre-result and cannot be used as validation interpretation.",
            "",
        ]
    )
    path.write_text("\n".join(lines))


def main() -> int:
    args = parse_args()
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    outdir.mkdir(parents=True, exist_ok=True)
    rows, checks = build_board()
    n_fail = sum(1 for row in checks if row["status"] != "PASS")

    board_path = outdir / "first30_status_board_dryrun.tsv"
    lint_path = outdir / "first30_status_board_dryrun_lint.tsv"
    markdown_path = outdir / "FIRST30_STATUS_BOARD_DRYRUN.md"
    write_tsv(
        board_path,
        rows,
        [
            "scenario",
            "board_status",
            "status_summary",
            "blocker",
            "next_minute_window",
            "next_step_order",
            "next_action",
            "next_command_or_artifact",
            "stop_route_if_next_step_fails",
            "repair_template_id",
            "repair_template_path",
            "allowed_language",
            "team_status_sentence",
            "score_values_read",
        ],
    )
    write_tsv(lint_path, checks, ["scenario", "check", "status", "detail"])
    summary = {
        "synthetic": False,
        "purpose": "V46 first-30 returned-package status-board dry run; no biological claim",
        "n_board_rows": len(rows),
        "n_lint_checks": len(checks),
        "n_lint_fail": n_fail,
        "all_score_values_read_false": all(row["score_values_read"] == "false" for row in rows),
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
        "board": rel(board_path),
        "lint": rel(lint_path),
        "markdown": rel(markdown_path),
    }
    write_markdown(markdown_path, rows, summary)
    (outdir / "first30_status_board_dryrun_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    if args.fail_on_error and n_fail:
        return 1
    return 0 if n_fail == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
