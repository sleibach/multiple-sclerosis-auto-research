#!/usr/bin/env python3
"""Build end-to-end returned-package operator transcript fixtures.

This is operator-navigation infrastructure only. It stitches existing V46
receipt-manifest, first-30 status-board, repair-template, and report-template
readiness outputs into readable synthetic operator transcripts. It does not
open returned score tables, expression matrices, labels, or quarantined cohort
data.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v46_operator_transcript_fixture"

HANDOFF = ROOT / "analysis/v46_receipt_manifest_to_command_plan_handoff/receipt_manifest_to_command_plan_handoff.tsv"
STATUS_BOARD = ROOT / "analysis/v46_first30_returned_package_status_board_dryrun/first30_status_board_dryrun.tsv"
SAFE_CLASS_MAP = ROOT / "analysis/v46_safe_class_report_template_readiness/safe_class_report_template_map.tsv"
HEADER_REPAIR = ROOT / "analysis/v46_report_header_repair_template_coverage/report_header_repair_template_coverage.tsv"
LOCKED_HASH_BASELINE = ROOT / "docs/validation/LOCKED_ARTIFACT_HASH_BASELINE_V45.tsv"

LOCKED_RULE_PATH = "docs/locked_rules/LOCKED_RULE_V22.md"

SCENARIOS = [
    {
        "scenario": "scoreable_canonical_pre_result",
        "cohort_token": "synthetic_scoreable_v46",
        "handoff_case": "scored_canonical_to_plan",
        "status_board_scenario": "scored_canonical_aggregate",
        "route_class": "SCORED_CANONICAL_AGGREGATE",
        "safe_class": "ELIGIBLE_FOR_PREREGISTERED_INTERPRETATION",
        "terms_class": "AGGREGATE_ONLY_LOCAL_PREFLIGHT",
        "final_operator_state": "REPORT_SKELETON_READY_NO_VALUES",
        "report_boundary": "A locked-rule report skeleton can be prepared after gates, but this transcript fixture does not populate any result fields.",
        "repair_issue_id": "",
    },
    {
        "scenario": "unscoreable_aggregate_repair_path",
        "cohort_token": "synthetic_unscoreable_v46",
        "handoff_case": "unscoreable_author_run_aggregate_to_preflight_only",
        "status_board_scenario": "unscoreable_aggregate",
        "route_class": "UNSCOREABLE_AGGREGATE_PREFLIGHT_ONLY",
        "safe_class": "BLOCKED_COMPLETENESS",
        "terms_class": "AUTHOR_RUN_ONLY",
        "final_operator_state": "REPORT_STOP_SKELETON_READY",
        "report_boundary": "A stop-only report skeleton can be prepared; missing aggregate outputs must be repaired before interpretation.",
        "repair_issue_id": "",
    },
    {
        "scenario": "terms_blocked_no_package_review",
        "cohort_token": "synthetic_terms_blocked_v46",
        "handoff_case": "terms_blocked_after_shape",
        "status_board_scenario": "terms_blocked_return",
        "route_class": "TERMS_BLOCKED_RETURN",
        "safe_class": "BLOCKED_TERMS_OR_RECEIPT_GATES",
        "terms_class": "NO_PROCESSING_ALLOWED",
        "final_operator_state": "REPORT_STOP_SKELETON_READY",
        "report_boundary": "A stop-only report skeleton can be prepared; package review remains blocked by terms or receipt gates.",
        "repair_issue_id": "missing_terms_class",
    },
]

FORBIDDEN_PATTERNS = [
    re.compile(r"\bAUC\s*[=:]", re.I),
    re.compile(r"\bp\s*[=:]", re.I),
    re.compile(r"\beffect[- ]size\s*[=:]", re.I),
    re.compile(r"\bsensitivity\s*[=:]", re.I),
    re.compile(r"\bspecificity\s*[=:]", re.I),
    re.compile(r"\bpassed\b", re.I),
    re.compile(r"\bfailed\b", re.I),
    re.compile(r"\bconfirmed\b", re.I),
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
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def index_by(rows: list[dict[str, str]], key: str) -> dict[str, dict[str, str]]:
    return {row[key]: row for row in rows}


def locked_rule_hash() -> str:
    for row in read_tsv(LOCKED_HASH_BASELINE):
        if row["path"] == LOCKED_RULE_PATH:
            return row["sha256"]
    raise RuntimeError(f"Missing locked-rule hash baseline for {LOCKED_RULE_PATH}")


def report_skeleton_text(
    scenario: dict[str, str],
    safe_row: dict[str, str],
    status_row: dict[str, str],
    locked_hash: str,
    repair_template_path: str,
) -> str:
    lines = [
        f"# Returned-Package Report Skeleton: {scenario['scenario']}",
        "",
        "Status: synthetic operator transcript fixture. No validation result and no biological claim.",
        "",
        "## Required Provenance Header",
        "",
        f"- cohort_token: `{scenario['cohort_token']}`",
        f"- route_class: `{scenario['route_class']}`",
        f"- terms_class: `{scenario['terms_class']}`",
        f"- safe_class: `{scenario['safe_class']}`",
        f"- locked_rule_path: `{LOCKED_RULE_PATH}`",
        f"- locked_rule_sha256: `{locked_hash}`",
        "- score_values_read: `false`",
        "",
        "## Pre-Result Boundary",
        "",
        scenario["report_boundary"],
        "",
        "## Source Navigation",
        "",
        f"- first30_board_status: `{status_row['board_status']}`",
        f"- safe_report_mode: `{safe_row['report_mode']}`",
        f"- safe_skeleton_id: `{safe_row['skeleton_id']}`",
    ]
    if repair_template_path:
        lines.append(f"- repair_template_path: `{repair_template_path}`")
    lines.extend(
        [
            "",
            "## Report Body Placeholder",
            "",
            "No result wording is populated by this transcript fixture. The eventual real",
            "report must pass the V46 report-header metadata linter, the V46 safe-class",
            "report linter, and the frozen V42 interpretation grid before any result",
            "fields are written.",
            "",
        ]
    )
    return "\n".join(lines)


def transcript_markdown(
    scenario: dict[str, str],
    steps: list[dict[str, object]],
    report_path: str,
) -> str:
    lines = [
        f"# Operator Transcript Fixture: {scenario['scenario']}",
        "",
        "Status: synthetic operator-navigation fixture. No validation result and no biological claim.",
        "",
        f"Cohort token: `{scenario['cohort_token']}`",
        f"Final operator state: `{scenario['final_operator_state']}`",
        f"Report skeleton: `{report_path}`",
        "",
        "| Step | Phase | Observation | Next action |",
        "|---:|---|---|---|",
    ]
    for row in steps:
        lines.append(
            f"| {row['step_order']} | `{row['phase']}` | {row['operator_observation']} | {row['allowed_next_action']} |"
        )
    lines.extend(
        [
            "",
            "Boundary: every step in this transcript is pre-score or stop-only. The",
            "fixture does not open returned score values, labels, expression matrices,",
            "or quarantined real cohort data.",
            "",
        ]
    )
    return "\n".join(lines)


def build_case(
    scenario: dict[str, str],
    handoff_rows: dict[str, dict[str, str]],
    board_rows: dict[str, dict[str, str]],
    safe_rows: dict[str, dict[str, str]],
    header_repairs: dict[str, dict[str, str]],
    outdir: Path,
    locked_hash: str,
) -> tuple[list[dict[str, object]], dict[str, object], str, str]:
    handoff = handoff_rows[scenario["handoff_case"]]
    board = board_rows[scenario["status_board_scenario"]]
    safe_row = safe_rows[scenario["safe_class"]]
    repair_template_path = board.get("repair_template_path") or ""
    if scenario["repair_issue_id"]:
        repair_template_path = header_repairs[scenario["repair_issue_id"]]["template_path"]

    report_dir = outdir / "report_skeletons"
    transcript_dir = outdir / "transcripts"
    report_dir.mkdir(parents=True, exist_ok=True)
    transcript_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / f"{scenario['scenario']}.md"

    steps = [
        {
            "scenario": scenario["scenario"],
            "step_order": 1,
            "phase": "receipt_manifest",
            "source_artifact": rel(HANDOFF),
            "operator_observation": f"Receipt manifest schema status is `{handoff['receipt_manifest_schema_status']}` with `{handoff['n_schema_fail']}` schema failures.",
            "allowed_next_action": "Stop for manifest repair if schema failed; otherwise continue to package-shape and command-plan branch.",
            "command_or_artifact": handoff.get("next_executable_command") or "STOP",
            "safe_class": "",
            "report_skeleton_path": "",
            "score_values_read": "false",
            "status": "PASS" if handoff["score_values_read"] == "false" else "FAIL",
        },
        {
            "scenario": scenario["scenario"],
            "step_order": 2,
            "phase": "first30_status_board",
            "source_artifact": rel(STATUS_BOARD),
            "operator_observation": f"Status board route is `{board['board_status']}`; blocker is `{board['blocker']}`.",
            "allowed_next_action": board["allowed_language"],
            "command_or_artifact": board["next_command_or_artifact"],
            "safe_class": "",
            "report_skeleton_path": "",
            "score_values_read": "false",
            "status": "PASS" if board["score_values_read"] == "false" else "FAIL",
        },
        {
            "scenario": scenario["scenario"],
            "step_order": 3,
            "phase": "safe_class_report_readiness",
            "source_artifact": rel(SAFE_CLASS_MAP),
            "operator_observation": f"Safe class `{scenario['safe_class']}` maps to report mode `{safe_row['report_mode']}`.",
            "allowed_next_action": safe_row["allowed_interpretation"],
            "command_or_artifact": safe_row["skeleton_path"],
            "safe_class": scenario["safe_class"],
            "report_skeleton_path": "",
            "score_values_read": "false",
            "status": "PASS" if safe_row["score_values_read"] == "false" else "FAIL",
        },
        {
            "scenario": scenario["scenario"],
            "step_order": 4,
            "phase": "report_skeleton",
            "source_artifact": rel(report_path),
            "operator_observation": "Report skeleton contains the required locked-rule provenance header before any body text.",
            "allowed_next_action": scenario["report_boundary"],
            "command_or_artifact": rel(report_path),
            "safe_class": scenario["safe_class"],
            "report_skeleton_path": rel(report_path),
            "score_values_read": "false",
            "status": "PASS",
        },
    ]

    report_text = report_skeleton_text(scenario, safe_row, board, locked_hash, repair_template_path)
    report_path.write_text(report_text)
    transcript_path = transcript_dir / f"{scenario['scenario']}.md"
    transcript_path.write_text(transcript_markdown(scenario, steps, rel(report_path)))

    summary = {
        "scenario": scenario["scenario"],
        "cohort_token": scenario["cohort_token"],
        "route_class": scenario["route_class"],
        "terms_class": scenario["terms_class"],
        "safe_class": scenario["safe_class"],
        "handoff_case": scenario["handoff_case"],
        "status_board_scenario": scenario["status_board_scenario"],
        "first30_board_status": board["board_status"],
        "final_operator_state": scenario["final_operator_state"],
        "repair_template_path": repair_template_path,
        "report_skeleton_path": rel(report_path),
        "transcript_path": rel(transcript_path),
        "score_values_read": "false",
        "status": "PASS" if all(row["status"] == "PASS" for row in steps) else "FAIL",
    }
    return steps, summary, rel(report_path), rel(transcript_path)


def lint_outputs(
    step_rows: list[dict[str, object]],
    case_rows: list[dict[str, object]],
    report_paths: list[str],
    transcript_paths: list[str],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for row in step_rows:
        rows.append(
            {
                "scope": "step",
                "scenario": row["scenario"],
                "check": f"score_values_read_false_step_{row['step_order']}",
                "status": "PASS" if row["score_values_read"] == "false" else "FAIL",
                "detail": row["phase"],
                "score_values_read": "false",
            }
        )
    for row in case_rows:
        report_text = (ROOT / row["report_skeleton_path"]).read_text(errors="ignore")
        before_body = report_text.split("## Report Body Placeholder", 1)[0]
        required_header = [
            "cohort_token:",
            "route_class:",
            "terms_class:",
            "safe_class:",
            "locked_rule_path:",
            "locked_rule_sha256:",
            "score_values_read:",
        ]
        for token in required_header:
            rows.append(
                {
                    "scope": "report_skeleton",
                    "scenario": row["scenario"],
                    "check": f"required_header_before_body:{token}",
                    "status": "PASS" if token in before_body else "FAIL",
                    "detail": row["report_skeleton_path"],
                    "score_values_read": "false",
                }
            )
        for pattern in FORBIDDEN_PATTERNS:
            rows.append(
                {
                    "scope": "report_skeleton",
                    "scenario": row["scenario"],
                    "check": f"forbidden_pattern:{pattern.pattern}",
                    "status": "FAIL" if pattern.search(report_text) else "PASS",
                    "detail": row["report_skeleton_path"],
                    "score_values_read": "false",
                }
            )
    for path in report_paths + transcript_paths:
        text = (ROOT / path).read_text(errors="ignore")
        rows.append(
            {
                "scope": "generated_markdown",
                "scenario": Path(path).stem,
                "check": "contains_synthetic_boundary",
                "status": "PASS" if "No validation result and no biological claim" in text else "FAIL",
                "detail": path,
                "score_values_read": "false",
            }
        )
        rows.append(
            {
                "scope": "generated_markdown",
                "scenario": Path(path).stem,
                "check": "contains_no_score_values_read_true",
                "status": "FAIL" if "score_values_read: `true`" in text or "\ttrue" in text else "PASS",
                "detail": path,
                "score_values_read": "false",
            }
        )
    return rows


def write_markdown(path: Path, case_rows: list[dict[str, object]], summary: dict[str, object]) -> None:
    lines = [
        "# Operator Transcript Fixture V46",
        "",
        "Status: synthetic operator-navigation infrastructure. No validation result and no biological claim.",
        "",
        "This generated fixture demonstrates the mechanical route from receipt",
        "manifest state through the first-30 status board and into a report",
        "skeleton, without opening returned score-bearing values.",
        "",
        f"Overall status: `{summary['overall_status']}`; scenarios: `{summary['n_scenarios']}`; lint failures: `{summary['n_lint_fail']}`.",
        "",
        "| Scenario | Route | Safe class | Report skeleton | Transcript |",
        "|---|---|---|---|---|",
    ]
    for row in case_rows:
        lines.append(
            f"| `{row['scenario']}` | `{row['route_class']}` | `{row['safe_class']}` | `{row['report_skeleton_path']}` | `{row['transcript_path']}` |"
        )
    lines.extend(
        [
            "",
            "Boundary: these are synthetic transcript fixtures for operator training and",
            "regression testing. They do not authorize interpretation of any real returned",
            "package, do not change the V22 locked rule, and do not alter the V42 frozen",
            "pre-registration.",
            "",
        ]
    )
    path.write_text("\n".join(lines))


def main() -> int:
    args = parse_args()
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    handoff_rows = index_by(read_tsv(HANDOFF), "case")
    board_rows = index_by(read_tsv(STATUS_BOARD), "scenario")
    safe_rows = index_by(read_tsv(SAFE_CLASS_MAP), "safe_class")
    header_repairs = index_by(read_tsv(HEADER_REPAIR), "issue_id")
    locked_hash = locked_rule_hash()

    all_steps: list[dict[str, object]] = []
    case_rows: list[dict[str, object]] = []
    report_paths: list[str] = []
    transcript_paths: list[str] = []
    for scenario in SCENARIOS:
        steps, case_summary, report_path, transcript_path = build_case(
            scenario,
            handoff_rows,
            board_rows,
            safe_rows,
            header_repairs,
            outdir,
            locked_hash,
        )
        all_steps.extend(steps)
        case_rows.append(case_summary)
        report_paths.append(report_path)
        transcript_paths.append(transcript_path)

    lint_rows = lint_outputs(all_steps, case_rows, report_paths, transcript_paths)
    n_lint_fail = sum(1 for row in lint_rows if row["status"] != "PASS")
    n_case_fail = sum(1 for row in case_rows if row["status"] != "PASS")
    all_score_values_read_false = all(row["score_values_read"] == "false" for row in all_steps + case_rows + lint_rows)

    steps_path = outdir / "operator_transcript_steps.tsv"
    cases_path = outdir / "operator_transcript_cases.tsv"
    lint_path = outdir / "operator_transcript_lint.tsv"
    report_path = outdir / "OPERATOR_TRANSCRIPT_FIXTURE.md"
    summary_path = outdir / "operator_transcript_fixture_summary.json"

    write_tsv(
        steps_path,
        all_steps,
        [
            "scenario",
            "step_order",
            "phase",
            "source_artifact",
            "operator_observation",
            "allowed_next_action",
            "command_or_artifact",
            "safe_class",
            "report_skeleton_path",
            "score_values_read",
            "status",
        ],
    )
    write_tsv(
        cases_path,
        case_rows,
        [
            "scenario",
            "cohort_token",
            "route_class",
            "terms_class",
            "safe_class",
            "handoff_case",
            "status_board_scenario",
            "first30_board_status",
            "final_operator_state",
            "repair_template_path",
            "report_skeleton_path",
            "transcript_path",
            "score_values_read",
            "status",
        ],
    )
    write_tsv(
        lint_path,
        lint_rows,
        ["scope", "scenario", "check", "status", "detail", "score_values_read"],
    )
    summary = {
        "synthetic": True,
        "purpose": "V46 returned-package operator transcript fixture; no biological claim",
        "n_scenarios": len(case_rows),
        "n_steps": len(all_steps),
        "n_case_fail": n_case_fail,
        "n_lint_checks": len(lint_rows),
        "n_lint_fail": n_lint_fail,
        "all_score_values_read_false": all_score_values_read_false,
        "steps": rel(steps_path),
        "cases": rel(cases_path),
        "lint": rel(lint_path),
        "markdown": rel(report_path),
        "overall_status": "PASS" if n_case_fail == 0 and n_lint_fail == 0 and all_score_values_read_false else "FAIL",
    }
    write_markdown(report_path, case_rows, summary)
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    if args.fail_on_error and summary["overall_status"] != "PASS":
        return 1
    return 0 if summary["overall_status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
