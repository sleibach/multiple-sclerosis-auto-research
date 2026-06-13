#!/usr/bin/env python3
"""Build the V46 returned-package handoff bundle manifest.

This is operator navigation infrastructure. It links the returned-package
guardrail artifacts in deterministic order and checks that each referenced
script, doc, and generated output exists. It does not read returned scores,
expression data, labels, or quarantined cohorts.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v46_returned_package_handoff_bundle_manifest"

ARTIFACTS = [
    {
        "sequence": 1,
        "phase": "cold_start",
        "artifact_id": "current_action_card",
        "role": "Confirm the operator is still blocked only on external data and local guards are green.",
        "command": ".venv/bin/python scripts/v45_current_action_card.py --outdir analysis/v45_current_action_card",
        "doc": "docs/validation/CURRENT_ACTION_CARD_V45.md",
        "primary_output": "analysis/v45_current_action_card/current_action_card_summary.json",
    },
    {
        "sequence": 2,
        "phase": "cold_start",
        "artifact_id": "cold_start_operator_sequence",
        "role": "Run the cold-start sequence before touching a received or returned package.",
        "command": ".venv/bin/python scripts/v45_cold_start_operator_sequence.py --outdir analysis/v45_cold_start_operator_sequence",
        "doc": "docs/validation/COLD_START_OPERATOR_SEQUENCE_V45.md",
        "primary_output": "analysis/v45_cold_start_operator_sequence/cold_start_operator_sequence_summary.json",
    },
    {
        "sequence": 3,
        "phase": "pre_touch_guard",
        "artifact_id": "receipt_manifest_schema_linter",
        "role": "Verify the receipt manifest has safe non-sensitive columns and aggregate paths before classification.",
        "command": ".venv/bin/python scripts/v46_receipt_manifest_schema_linter.py lint --manifest <receipt_manifest.tsv> --outdir analysis/v46_receipt_manifest_schema_linter/<cohort>_<date> --fail-on-error",
        "doc": "docs/validation/RECEIPT_MANIFEST_SCHEMA_LINTER_V46.md",
        "primary_output": "analysis/v46_receipt_manifest_schema_linter/receipt_manifest_schema_synthetic_summary.json",
    },
    {
        "sequence": 4,
        "phase": "pre_touch_guard",
        "artifact_id": "package_manifest_shape_classifier",
        "role": "Classify the returned package from receipt manifest filenames and terms only.",
        "command": ".venv/bin/python scripts/v46_package_manifest_shape_classifier.py classify --manifest <receipt_manifest.tsv> --terms-class <TERMS_CLASS> --outdir analysis/v46_package_manifest_shape_classifier/<cohort>_<date> --fail-on-error",
        "doc": "docs/validation/PACKAGE_MANIFEST_SHAPE_CLASSIFIER_V46.md",
        "primary_output": "analysis/v46_package_manifest_shape_classifier/package_manifest_shape_synthetic_summary.json",
    },
    {
        "sequence": 5,
        "phase": "first_30_minutes",
        "artifact_id": "first30_decision_table",
        "role": "Follow the first 30 minutes of package handling without reading score values.",
        "command": ".venv/bin/python scripts/v46_first30_returned_package_decision_table.py --outdir analysis/v46_first30_returned_package_decision_table --fail-on-error",
        "doc": "docs/validation/FIRST30_RETURNED_PACKAGE_DECISION_TABLE_V46.md",
        "primary_output": "analysis/v46_first30_returned_package_decision_table/first30_returned_package_decision_summary.json",
    },
    {
        "sequence": 6,
        "phase": "first_30_minutes",
        "artifact_id": "first30_status_board",
        "role": "Summarize route, blocker, next command, and safe team wording without reading score values.",
        "command": ".venv/bin/python scripts/v46_first30_returned_package_status_board_dryrun.py --outdir analysis/v46_first30_returned_package_status_board_dryrun --fail-on-error",
        "doc": "docs/validation/FIRST30_RETURNED_PACKAGE_STATUS_BOARD_DRYRUN_V46.md",
        "primary_output": "analysis/v46_first30_returned_package_status_board_dryrun/first30_status_board_dryrun_summary.json",
    },
    {
        "sequence": 7,
        "phase": "preflight_composition",
        "artifact_id": "returned_package_preflight_dryrun",
        "role": "Run one synthetic-safe command that composes schema lint, shape classification, first-30 routing, state validation, and repair coverage.",
        "command": ".venv/bin/python scripts/v46_returned_package_preflight_dryrun.py --outdir analysis/v46_returned_package_preflight_dryrun --fail-on-error",
        "doc": "docs/validation/RETURNED_PACKAGE_PREFLIGHT_DRYRUN_V46.md",
        "primary_output": "analysis/v46_returned_package_preflight_dryrun/returned_package_preflight_dryrun_summary.json",
    },
    {
        "sequence": 8,
        "phase": "command_order",
        "artifact_id": "command_order_planner",
        "role": "Generate the route-specific command order using package-state and metric-format state.",
        "command": ".venv/bin/python scripts/v46_returned_package_command_order_planner.py plan --cohort-token <cohort>_<date> --package-root <returned_package_dir> --terms-capture <terms_capture_tsv> --terms-class <TERMS_CLASS> --package-kind author_run_aggregate --package-state <package_state> --metric-format-state <metric_format_state> --outdir analysis/v46_returned_package_command_order_planner/<cohort>_<date> --expect-status <PASS_or_BLOCKED>",
        "doc": "docs/validation/RETURNED_PACKAGE_COMMAND_ORDER_PLANNER_V46.md",
        "primary_output": "analysis/v46_returned_package_command_order_planner/returned_package_command_order_synthetic_summary.json",
    },
    {
        "sequence": 9,
        "phase": "state_guard",
        "artifact_id": "state_transition_validator",
        "role": "Verify no report/score state is reachable before required gates and safe class.",
        "command": ".venv/bin/python scripts/v46_returned_package_state_transition_validator.py --outdir analysis/v46_returned_package_state_transition_validator --fail-on-error",
        "doc": "docs/validation/RETURNED_PACKAGE_STATE_TRANSITION_VALIDATOR_V46.md",
        "primary_output": "analysis/v46_returned_package_state_transition_validator/returned_package_state_transition_summary.json",
    },
    {
        "sequence": 10,
        "phase": "interpretation_boundary",
        "artifact_id": "safe_interpretation_classifier",
        "role": "Assign the V46 safe class after all prerequisite gate summaries exist.",
        "command": ".venv/bin/python scripts/v46_returned_package_safe_interpretation.py classify --gate-summary <gate_summary> --schema-summary <schema_summary> --analyzable-summary <analyzable_summary> --metadata-summary <metadata_summary> --batch-confounder-summary <batch_summary> --terms-status PASS --outdir analysis/v46_returned_package_safe_interpretation/<cohort>_<date>",
        "doc": "docs/validation/RETURNED_PACKAGE_SAFE_INTERPRETATION_V46.md",
        "primary_output": "analysis/v46_returned_package_safe_interpretation/safe_interpretation_synthetic_summary.json",
    },
    {
        "sequence": 11,
        "phase": "underpowered_language",
        "artifact_id": "small_n_language",
        "role": "Constrain wording for underpowered or partial-label returns.",
        "command": ".venv/bin/python scripts/v46_small_n_conclusion_language_table.py --outdir analysis/v46_small_n_conclusion_language",
        "doc": "docs/validation/SMALL_N_CONCLUSION_LANGUAGE_V46.md",
        "primary_output": "analysis/v46_small_n_conclusion_language/small_n_conclusion_language_summary.json",
    },
    {
        "sequence": 12,
        "phase": "underpowered_language",
        "artifact_id": "analyzable_pair_confidence_envelope",
        "role": "Map analyzable-pair counts to pass/fail/inconclusive wording constraints.",
        "command": ".venv/bin/python scripts/v46_analyzable_pair_confidence_envelope.py --outdir analysis/v46_analyzable_pair_confidence_envelope --fail-on-error",
        "doc": "docs/validation/ANALYZABLE_PAIR_CONFIDENCE_ENVELOPE_V46.md",
        "primary_output": "analysis/v46_analyzable_pair_confidence_envelope/analyzable_pair_confidence_envelope_summary.json",
    },
    {
        "sequence": 13,
        "phase": "repair_handoff",
        "artifact_id": "repair_request_templates",
        "role": "Draft safe author-facing repair requests for blocked returned-package states.",
        "command": ".venv/bin/python scripts/v46_return_repair_request_templates.py --outdir analysis/v46_return_repair_request_templates --fail-on-error",
        "doc": "docs/validation/RETURN_REPAIR_REQUEST_TEMPLATES_V46.md",
        "primary_output": "analysis/v46_return_repair_request_templates/return_repair_request_templates_summary.json",
    },
    {
        "sequence": 14,
        "phase": "repair_handoff",
        "artifact_id": "first30_repair_template_coverage",
        "role": "Prove every first-30 stop route has local repair or a safe author-facing template.",
        "command": ".venv/bin/python scripts/v46_first30_repair_template_coverage_linter.py --outdir analysis/v46_first30_repair_template_coverage_linter --fail-on-error",
        "doc": "docs/validation/FIRST30_REPAIR_TEMPLATE_COVERAGE_LINTER_V46.md",
        "primary_output": "analysis/v46_first30_repair_template_coverage_linter/first30_repair_template_coverage_summary.json",
    },
    {
        "sequence": 15,
        "phase": "report_guard",
        "artifact_id": "result_report_safe_class_linter",
        "role": "Ensure any report cites a safe class and avoids forbidden score language when blocked.",
        "command": ".venv/bin/python scripts/v46_result_report_safe_class_linter.py synthetic-check --outdir analysis/v46_result_report_safe_class_linter --fail-on-error",
        "doc": "docs/validation/RESULT_REPORT_SAFE_CLASS_LINTER_V46.md",
        "primary_output": "analysis/v46_result_report_safe_class_linter/result_report_safe_class_synthetic_summary.json",
    },
    {
        "sequence": 16,
        "phase": "operator_navigation",
        "artifact_id": "returned_package_doc_crosslink_linter",
        "role": "Verify every returned-package script has direct documentation and operator-route reachability.",
        "command": ".venv/bin/python scripts/v46_returned_package_doc_crosslink_linter.py --outdir analysis/v46_returned_package_doc_crosslink_linter --fail-on-error",
        "doc": "docs/validation/RETURNED_PACKAGE_DOC_CROSSLINK_LINTER_V46.md",
        "primary_output": "analysis/v46_returned_package_doc_crosslink_linter/returned_package_doc_crosslink_summary.json",
    },
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


def write_tsv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def status_from_json(path: Path) -> str:
    if not path.exists() or path.suffix != ".json":
        return ""
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError:
        return "UNREADABLE_JSON"
    return str(data.get("overall_status") or data.get("headline_status") or data.get("observed_status") or "")


def build_rows() -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    rows: list[dict[str, object]] = []
    checks: list[dict[str, object]] = []
    for item in ARTIFACTS:
        doc_path = ROOT / item["doc"]
        output_path = ROOT / item["primary_output"]
        command_script = item["command"].split()[1] if item["command"].startswith(".venv/bin/python ") else ""
        script_path = ROOT / command_script if command_script else None
        row = {
            **item,
            "doc_exists": str(doc_path.exists()).lower(),
            "primary_output_exists": str(output_path.exists()).lower(),
            "script_exists": str(script_path.exists() if script_path else True).lower(),
            "observed_status": status_from_json(output_path),
            "score_values_read": "false",
        }
        rows.append(row)
        for check, ok, detail in [
            ("doc_exists", doc_path.exists(), item["doc"]),
            ("primary_output_exists", output_path.exists(), item["primary_output"]),
            ("script_exists", script_path.exists() if script_path else True, command_script),
            ("score_values_read_false", row["score_values_read"] == "false", item["artifact_id"]),
        ]:
            checks.append(
                {
                    "artifact_id": item["artifact_id"],
                    "check": check,
                    "status": "PASS" if ok else "FAIL",
                    "detail": detail,
                }
            )
    return rows, checks


def write_markdown(path: Path, rows: list[dict[str, object]], summary: dict[str, object]) -> None:
    lines = [
        "# Returned-Package Handoff Bundle Manifest V46",
        "",
        "Status: operator navigation infrastructure. No validation result and no biological claim.",
        "",
        "This manifest lists the returned-package artifacts in deterministic operator order.",
        f"Overall status: `{summary['overall_status']}`; rows: `{summary['n_manifest_rows']}`; lint failures: `{summary['n_lint_fail']}`.",
        "",
        "| Order | Phase | Artifact | Role | Doc |",
        "|---:|---|---|---|---|",
    ]
    for row in rows:
        lines.append(f"| {row['sequence']} | `{row['phase']}` | `{row['artifact_id']}` | {row['role']} | `{row['doc']}` |")
    lines.extend(
        [
            "",
            "Every row is a pre-score navigation or guard artifact. The manifest does not",
            "authorize result interpretation; the V46 safe class and V42 pre-registration",
            "remain the interpretation boundary.",
            "",
        ]
    )
    path.write_text("\n".join(lines))


def main() -> int:
    args = parse_args()
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    outdir.mkdir(parents=True, exist_ok=True)
    rows, checks = build_rows()
    n_fail = sum(1 for row in checks if row["status"] != "PASS")

    manifest_path = outdir / "returned_package_handoff_bundle_manifest.tsv"
    lint_path = outdir / "returned_package_handoff_bundle_lint.tsv"
    markdown_path = outdir / "RETURNED_PACKAGE_HANDOFF_BUNDLE_MANIFEST.md"

    write_tsv(
        manifest_path,
        rows,
        [
            "sequence",
            "phase",
            "artifact_id",
            "role",
            "command",
            "doc",
            "primary_output",
            "doc_exists",
            "primary_output_exists",
            "script_exists",
            "observed_status",
            "score_values_read",
        ],
    )
    write_tsv(lint_path, checks, ["artifact_id", "check", "status", "detail"])
    summary = {
        "synthetic": False,
        "purpose": "V46 returned-package handoff bundle manifest; no biological claim",
        "n_manifest_rows": len(rows),
        "n_lint_checks": len(checks),
        "n_lint_fail": n_fail,
        "all_score_values_read_false": all(row["score_values_read"] == "false" for row in rows),
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
        "manifest": rel(manifest_path),
        "lint": rel(lint_path),
        "markdown": rel(markdown_path),
    }
    write_markdown(markdown_path, rows, summary)
    (outdir / "returned_package_handoff_bundle_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    if args.fail_on_error and n_fail:
        return 1
    return 0 if n_fail == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
