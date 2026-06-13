#!/usr/bin/env python3
"""Generate the first-30-minute operator decision table for returned packages.

This is operations infrastructure only. It sequences already-frozen V45/V46
guards for plausible returned-package shapes and keeps all first-30-minute rows
before score interpretation. It does not read real cohort data or returned
scores.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v46_first30_returned_package_decision_table"

COMMANDS = {
    "regression": ".venv/bin/python scripts/v46_returned_package_regression_suite.py --outdir analysis/v46_returned_package_regression_suite --fail-on-error",
    "command_order": ".venv/bin/python scripts/v46_returned_package_command_order_planner.py plan --cohort-token <cohort>_<date> --package-root <returned_package_dir> --terms-capture <terms_capture_tsv> --terms-class <terms_class> --package-kind author_run_aggregate --package-state <package_state> --metric-format-state <metric_format_state> --outdir analysis/v46_returned_package_command_order_planner/<cohort>_<date> --expect-status <PASS_or_BLOCKED>",
    "metric_adapter": ".venv/bin/python scripts/v46_author_run_metric_format_adapter.py adapt --root <returned_package_dir> --outdir analysis/v46_author_run_metric_format_adapter/<cohort>_<date> --fail-on-error",
    "return_gate": ".venv/bin/python scripts/v45_author_run_return_gate_runner.py run --root <returned_or_normalized_package_dir> --package-state <package_state> --outdir analysis/v45_author_run_return_gate_runner/<cohort>_<date> --fail-on-error",
    "schema": ".venv/bin/python scripts/v45_author_run_schema_validator.py run --root <returned_or_normalized_package_dir> --package-state <package_state> --outdir analysis/v45_author_run_schema_validator/<cohort>_<date> --fail-on-error",
    "analyzable": ".venv/bin/python scripts/v45_route_analyzable_pair_calculator.py calculate --route <route> --metadata <metadata_tsv> --outdir analysis/v45_route_analyzable_pair_calculator/<cohort>_<date>",
    "partial_label": ".venv/bin/python scripts/v46_partial_label_return_classifier.py classify --analyzable-summary analysis/v45_route_analyzable_pair_calculator/<cohort>_<date>/analyzable_pair_summary.json --outdir analysis/v46_partial_label_return_classifier/<cohort>_<date>",
    "safe_interpretation": ".venv/bin/python scripts/v46_returned_package_safe_interpretation.py classify --gate-summary <gate_summary> --schema-summary <schema_summary> --analyzable-summary <analyzable_summary> --metadata-summary <metadata_summary> --batch-confounder-summary <batch_summary> --terms-status PASS --outdir analysis/v46_returned_package_safe_interpretation/<cohort>_<date>",
    "small_n_language": ".venv/bin/python scripts/v46_small_n_conclusion_language_table.py --outdir analysis/v46_small_n_conclusion_language",
    "repair_templates": ".venv/bin/python scripts/v46_return_repair_request_templates.py --outdir analysis/v46_return_repair_request_templates --fail-on-error",
}


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


def write_tsv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def add(rows: list[dict[str, object]], scenario: str, minute: str, step: int, action: str, command: str, continue_if: str, stop_if: str, route_to: str = "") -> None:
    rows.append(
        {
            "scenario": scenario,
            "minute_window": minute,
            "step_order": step,
            "action": action,
            "command_or_artifact": command,
            "continue_if": continue_if,
            "stop_if": stop_if,
            "route_to_if_stopped": route_to,
            "score_values_read": "false",
        }
    )


def common_receipt_rows(scenario: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    add(rows, scenario, "00-03", 1, "Run local returned-package regression guard before touching package content", COMMANDS["regression"], "overall_status=PASS", "any failure", "repair local software/readiness guard")
    add(rows, scenario, "03-06", 2, "Record non-sensitive receipt metadata and file listing only", "docs/validation/input_schemas/V45_package_receipt_manifest_template.tsv", "receipt manifest drafted", "raw/private content would need committing", "keep package outside git and run no-raw scanner")
    add(rows, scenario, "06-10", 3, "Capture or resolve data-use terms class", "docs/validation/input_schemas/V45_data_use_terms_capture_template.tsv", "terms_class permits this route", "terms UNKNOWN, AMBIGUOUS_TERMS_BLOCK, or NO_PROCESSING_ALLOWED", "repair template terms_or_receipt_not_cleared")
    return rows


def scenario_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    scenarios = {
        "scored_canonical_aggregate": ("scored", "canonical", False),
        "scored_noncanonical_aggregate": ("scored", "noncanonical", True),
        "scored_unknown_alias_aggregate": ("scored", "unknown", True),
        "unscoreable_aggregate": ("unscoreable", "canonical", False),
        "partial_label_scored_aggregate": ("scored", "canonical", False),
        "terms_blocked_return": ("scored", "canonical", False),
    }
    for scenario, (package_state, metric_format, needs_adapter) in scenarios.items():
        rows.extend(common_receipt_rows(scenario))
        if scenario == "terms_blocked_return":
            add(rows, scenario, "10-12", 4, "Stop at terms blocker; do not run package gates", COMMANDS["repair_templates"], "repair request template generated", "terms remain unresolved", "repair template terms_or_receipt_not_cleared")
            continue
        add(rows, scenario, "10-13", 4, "Generate route-specific command order", COMMANDS["command_order"], "plan status PASS", "plan status BLOCKED", "matching repair template from blocked safe class")
        next_step = 5
        if needs_adapter:
            add(rows, scenario, "13-17", next_step, "Normalize accepted noncanonical aggregate aliases if needed", COMMANDS["metric_adapter"], "adapter PASS", "adapter blocks or required canonical file absent", "repair template schema_or_metric_format_mismatch")
            next_step += 1
        add(rows, scenario, "17-21", next_step, "Run redaction and completeness return gate", COMMANDS["return_gate"], "return gate PASS", "redaction/completeness fail", "repair template redaction_or_private_content_block or missing_score_bearing_aggregate_outputs")
        next_step += 1
        add(rows, scenario, "21-24", next_step, "Run aggregate schema validator", COMMANDS["schema"], "schema PASS", "schema FAIL", "repair template schema_or_metric_format_mismatch")
        next_step += 1
        if scenario in {"partial_label_scored_aggregate", "scored_canonical_aggregate"}:
            add(rows, scenario, "24-27", next_step, "Count analyzable response pairs and classify partial-label state", f"{COMMANDS['analyzable']} && {COMMANDS['partial_label']}", "pair/label band computed", "labels absent or below floor", "small-n language table plus repair template response_labels_absent_or_unmapped or below_planning_floor_labeled_pairs")
            next_step += 1
        else:
            add(rows, scenario, "24-26", next_step, "Refresh small-n conclusion language constraints", COMMANDS["small_n_language"], "language table PASS", "language table unavailable", "repair local planning artifact before report drafting")
            next_step += 1
        add(rows, scenario, "27-30", next_step, "Run safe-interpretation classifier or route to repair template without reading score values", f"{COMMANDS['safe_interpretation']} || {COMMANDS['repair_templates']}", "safe class emitted", "blocked safe class or missing prerequisite", "matching repair template; no result report yet")
    return rows


def lint_rows(rows: list[dict[str, object]]) -> list[dict[str, str]]:
    checks: list[dict[str, str]] = []
    for row in rows:
        checks.append(
            {
                "scenario": str(row["scenario"]),
                "step_order": str(row["step_order"]),
                "check": "score_values_read_false",
                "status": "PASS" if row["score_values_read"] == "false" else "FAIL",
                "detail": str(row["action"]),
            }
        )
        action_lower = str(row["action"]).lower()
        forbidden = any(term in action_lower for term in ["interpret score", "read auc", "read p-value", "call pass", "call fail"])
        checks.append(
            {
                "scenario": str(row["scenario"]),
                "step_order": str(row["step_order"]),
                "check": "no_interpretation_action",
                "status": "FAIL" if forbidden else "PASS",
                "detail": str(row["action"]),
            }
        )
    return checks


def write_markdown(path: Path, rows: list[dict[str, object]], summary: dict[str, object]) -> None:
    lines = [
        "# First 30 Minutes Returned-Package Decision Table V46",
        "",
        "Status: operations infrastructure. No validation result and no biological claim.",
        "",
        "This table sequences the first 30 minutes after a returned aggregate package arrives.",
        "Every row is pre-interpretation and has `score_values_read=false`.",
        "",
        f"Scenarios: `{summary['n_scenarios']}`; rows: `{summary['n_rows']}`; lint failures: `{summary['n_lint_fail']}`.",
        "",
        "| Scenario | Window | Step | Action | Stop route |",
        "|---|---|---:|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| `{row['scenario']}` | `{row['minute_window']}` | {row['step_order']} | {row['action']} | {row['route_to_if_stopped']} |"
        )
    lines.extend(
        [
            "",
            "If any row stops, use the named repair template or local guard repair and rerun",
            "the same first-30-minute sequence from the beginning for the repaired package.",
            "",
        ]
    )
    path.write_text("\n".join(lines))


def main() -> int:
    args = parse_args()
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    outdir.mkdir(parents=True, exist_ok=True)
    rows = scenario_rows()
    checks = lint_rows(rows)
    table_path = outdir / "first30_returned_package_decision_table.tsv"
    lint_path = outdir / "first30_returned_package_decision_lint.tsv"
    markdown_path = outdir / "FIRST30_RETURNED_PACKAGE_DECISION_TABLE.md"
    write_tsv(
        table_path,
        rows,
        ["scenario", "minute_window", "step_order", "action", "command_or_artifact", "continue_if", "stop_if", "route_to_if_stopped", "score_values_read"],
    )
    write_tsv(lint_path, checks, ["scenario", "step_order", "check", "status", "detail"])
    n_fail = sum(1 for row in checks if row["status"] != "PASS")
    summary = {
        "synthetic": False,
        "purpose": "V46 first-30-minute returned-package operator decision table; no biological claim",
        "n_scenarios": len({row["scenario"] for row in rows}),
        "n_rows": len(rows),
        "n_lint_checks": len(checks),
        "n_lint_fail": n_fail,
        "all_score_values_read_false": all(row["score_values_read"] == "false" for row in rows),
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
        "table": rel(table_path),
        "lint": rel(lint_path),
        "markdown": rel(markdown_path),
    }
    write_markdown(markdown_path, rows, summary)
    (outdir / "first30_returned_package_decision_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    if args.fail_on_error and n_fail:
        return 1
    return 0 if n_fail == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
