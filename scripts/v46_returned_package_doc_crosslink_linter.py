#!/usr/bin/env python3
"""Lint returned-package documentation cross-links.

This is operator navigation infrastructure. It checks that each V46
returned-package guard script has:

1. a committed script file;
2. a committed documentation file;
3. a direct reference from that documentation file to the script;
4. at least one operator-facing reference from the returned-package handoff,
   operator checklist, regression suite, smoke bundle, or generated handoff
   manifest.

The linter does not read returned scores, expression data, labels, or
quarantined cohorts.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v46_returned_package_doc_crosslink_linter"

REQUIRED_SCRIPTS = [
    {
        "script": "scripts/v46_terms_governance_matrix.py",
        "doc": "docs/validation/TERMS_GOVERNANCE_MATRIX_V46.md",
        "role": "terms-governance route blocker",
    },
    {
        "script": "scripts/v46_author_run_metric_format_adapter.py",
        "doc": "docs/validation/AUTHOR_RUN_METRIC_FORMAT_ADAPTER_V46.md",
        "role": "noncanonical metric-format adapter",
    },
    {
        "script": "scripts/v46_partial_label_return_classifier.py",
        "doc": "docs/validation/PARTIAL_LABEL_RETURN_CLASSIFIER_V46.md",
        "role": "partial-label classifier",
    },
    {
        "script": "scripts/v46_receipt_manifest_schema_linter.py",
        "doc": "docs/validation/RECEIPT_MANIFEST_SCHEMA_LINTER_V46.md",
        "role": "receipt-manifest schema guard",
    },
    {
        "script": "scripts/v46_package_manifest_shape_classifier.py",
        "doc": "docs/validation/PACKAGE_MANIFEST_SHAPE_CLASSIFIER_V46.md",
        "role": "package-shape classifier",
    },
    {
        "script": "scripts/v46_receipt_manifest_to_command_plan_handoff.py",
        "doc": "docs/validation/RECEIPT_MANIFEST_TO_COMMAND_PLAN_HANDOFF_V46.md",
        "role": "receipt-manifest to command-plan handoff",
    },
    {
        "script": "scripts/v46_returned_package_command_order_planner.py",
        "doc": "docs/validation/RETURNED_PACKAGE_COMMAND_ORDER_PLANNER_V46.md",
        "role": "command-order planner",
    },
    {
        "script": "scripts/v46_returned_package_route_state_matrix.py",
        "doc": "docs/validation/RETURNED_PACKAGE_ROUTE_STATE_MATRIX_V46.md",
        "role": "route-state matrix",
    },
    {
        "script": "scripts/v46_aggregate_only_returned_package_composition_dryrun.py",
        "doc": "docs/validation/AGGREGATE_ONLY_RETURNED_PACKAGE_COMPOSITION_DRYRUN_V46.md",
        "role": "aggregate-only composition dry run",
    },
    {
        "script": "scripts/v46_unscoreable_return_composition_dryrun.py",
        "doc": "docs/validation/UNSCOREABLE_RETURN_COMPOSITION_DRYRUN_V46.md",
        "role": "unscoreable-return composition dry run",
    },
    {
        "script": "scripts/v46_returned_package_safe_interpretation.py",
        "doc": "docs/validation/RETURNED_PACKAGE_SAFE_INTERPRETATION_V46.md",
        "role": "safe-interpretation classifier",
    },
    {
        "script": "scripts/v46_safe_wording_fixture_linter.py",
        "doc": "docs/validation/SAFE_WORDING_FIXTURE_LINTER_V46.md",
        "role": "safe-wording fixture linter",
    },
    {
        "script": "scripts/v46_result_report_safe_class_linter.py",
        "doc": "docs/validation/RESULT_REPORT_SAFE_CLASS_LINTER_V46.md",
        "role": "result-report safe-class linter",
    },
    {
        "script": "scripts/v46_report_header_metadata_linter.py",
        "doc": "docs/validation/REPORT_HEADER_METADATA_LINTER_V46.md",
        "role": "report-header metadata linter",
    },
    {
        "script": "scripts/v46_report_header_repair_template_coverage.py",
        "doc": "docs/validation/REPORT_HEADER_REPAIR_TEMPLATE_COVERAGE_V46.md",
        "role": "report-header repair-template coverage",
    },
    {
        "script": "scripts/v46_safe_class_report_template_readiness.py",
        "doc": "docs/validation/SAFE_CLASS_REPORT_TEMPLATE_READINESS_V46.md",
        "role": "safe-class report-template readiness",
    },
    {
        "script": "scripts/v46_small_n_conclusion_language_table.py",
        "doc": "docs/validation/SMALL_N_CONCLUSION_LANGUAGE_V46.md",
        "role": "small-n conclusion language",
    },
    {
        "script": "scripts/v46_analyzable_pair_confidence_envelope.py",
        "doc": "docs/validation/ANALYZABLE_PAIR_CONFIDENCE_ENVELOPE_V46.md",
        "role": "analyzable-pair confidence envelope",
    },
    {
        "script": "scripts/v46_return_repair_request_templates.py",
        "doc": "docs/validation/RETURN_REPAIR_REQUEST_TEMPLATES_V46.md",
        "role": "repair-request templates",
    },
    {
        "script": "scripts/v46_partial_label_repair_prioritization.py",
        "doc": "docs/validation/PARTIAL_LABEL_REPAIR_PRIORITIZATION_V46.md",
        "role": "partial-label repair prioritization",
    },
    {
        "script": "scripts/v46_first30_returned_package_decision_table.py",
        "doc": "docs/validation/FIRST30_RETURNED_PACKAGE_DECISION_TABLE_V46.md",
        "role": "first-30 decision table",
    },
    {
        "script": "scripts/v46_first30_repair_template_coverage_linter.py",
        "doc": "docs/validation/FIRST30_REPAIR_TEMPLATE_COVERAGE_LINTER_V46.md",
        "role": "repair-template coverage linter",
    },
    {
        "script": "scripts/v46_first30_returned_package_status_board_dryrun.py",
        "doc": "docs/validation/FIRST30_RETURNED_PACKAGE_STATUS_BOARD_DRYRUN_V46.md",
        "role": "first-30 status-board dry run",
    },
    {
        "script": "scripts/v46_returned_package_status_board_schema_linter.py",
        "doc": "docs/validation/RETURNED_PACKAGE_STATUS_BOARD_SCHEMA_LINTER_V46.md",
        "role": "status-board schema linter",
    },
    {
        "script": "scripts/v46_status_board_markdown_roundtrip_renderer.py",
        "doc": "docs/validation/STATUS_BOARD_MARKDOWN_ROUNDTRIP_RENDERER_V46.md",
        "role": "status-board Markdown round-trip renderer",
    },
    {
        "script": "scripts/v46_returned_package_preflight_dryrun.py",
        "doc": "docs/validation/RETURNED_PACKAGE_PREFLIGHT_DRYRUN_V46.md",
        "role": "one-command preflight dry run",
    },
    {
        "script": "scripts/v46_returned_package_state_transition_validator.py",
        "doc": "docs/validation/RETURNED_PACKAGE_STATE_TRANSITION_VALIDATOR_V46.md",
        "role": "state-transition validator",
    },
    {
        "script": "scripts/v46_returned_package_handoff_bundle_manifest.py",
        "doc": "docs/validation/RETURNED_PACKAGE_HANDOFF_BUNDLE_MANIFEST_V46.md",
        "role": "handoff bundle manifest",
    },
    {
        "script": "scripts/v46_operator_transcript_fixture.py",
        "doc": "docs/validation/OPERATOR_TRANSCRIPT_FIXTURE_V46.md",
        "role": "operator transcript fixture",
    },
    {
        "script": "scripts/v46_returned_package_quickstart_readme.py",
        "doc": "docs/validation/RETURNED_PACKAGE_QUICKSTART_V46.md",
        "role": "returned-package generated quickstart",
    },
    {
        "script": "scripts/v46_returned_package_regression_suite.py",
        "doc": "docs/validation/RETURNED_PACKAGE_REGRESSION_SUITE_V46.md",
        "role": "returned-package regression suite",
    },
    {
        "script": "scripts/v46_operator_smoke_test_bundle.py",
        "doc": "docs/validation/OPERATOR_SMOKE_TEST_BUNDLE_V46.md",
        "role": "operator smoke-test bundle",
    },
    {
        "script": "scripts/v46_returned_package_doc_crosslink_linter.py",
        "doc": "docs/validation/RETURNED_PACKAGE_DOC_CROSSLINK_LINTER_V46.md",
        "role": "returned-package documentation cross-link linter",
    },
    {
        "script": "scripts/v46_returned_package_dependency_graph.py",
        "doc": "docs/validation/RETURNED_PACKAGE_DEPENDENCY_GRAPH_V46.md",
        "role": "returned-package dependency graph",
    },
]

OPERATOR_REFERENCE_FILES = [
    "docs/validation/AUTHOR_RUN_RETURN_OPERATOR_CHECKLIST_V45.md",
    "docs/validation/CURRENT_ACTION_CARD_V45.md",
    "docs/validation/COLD_START_OPERATOR_SEQUENCE_V45.md",
    "docs/validation/RETURNED_PACKAGE_HANDOFF_BUNDLE_MANIFEST_V46.md",
    "docs/validation/RETURNED_PACKAGE_REGRESSION_SUITE_V46.md",
    "docs/validation/OPERATOR_SMOKE_TEST_BUNDLE_V46.md",
    "docs/validation/RETURNED_PACKAGE_QUICKSTART_V46.md",
    "docs/validation/RETURNED_PACKAGE_DOC_CROSSLINK_LINTER_V46.md",
    "docs/validation/RETURNED_PACKAGE_DEPENDENCY_GRAPH_V46.md",
    "analysis/v46_returned_package_handoff_bundle_manifest/RETURNED_PACKAGE_HANDOFF_BUNDLE_MANIFEST.md",
    "analysis/v46_returned_package_quickstart_readme/RETURNED_PACKAGE_QUICKSTART.md",
    "analysis/v46_returned_package_handoff_bundle_manifest/returned_package_handoff_bundle_manifest.tsv",
    "analysis/v46_returned_package_regression_suite/returned_package_regression_steps.tsv",
    "analysis/v46_operator_smoke_test_bundle/operator_smoke_test_steps.tsv",
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


def read_text(path: Path) -> str:
    return path.read_text(errors="ignore") if path.exists() else ""


def write_tsv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def find_operator_refs(script: str) -> list[str]:
    refs: list[str] = []
    for candidate in OPERATOR_REFERENCE_FILES:
        path = ROOT / candidate
        if script in read_text(path):
            refs.append(candidate)
    return refs


def build_rows() -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    rows: list[dict[str, object]] = []
    lint_rows: list[dict[str, object]] = []
    for item in REQUIRED_SCRIPTS:
        script_path = ROOT / item["script"]
        doc_path = ROOT / item["doc"]
        script_name = script_path.name
        doc_text = read_text(doc_path)
        operator_refs = find_operator_refs(item["script"])
        checks = {
            "script_exists": script_path.exists(),
            "doc_exists": doc_path.exists(),
            "doc_mentions_script": script_name in doc_text or item["script"] in doc_text,
            "operator_reference_exists": bool(operator_refs),
        }
        status = "PASS" if all(checks.values()) else "FAIL"
        row = {
            "script": item["script"],
            "role": item["role"],
            "doc": item["doc"],
            "script_exists": str(checks["script_exists"]).lower(),
            "doc_exists": str(checks["doc_exists"]).lower(),
            "doc_mentions_script": str(checks["doc_mentions_script"]).lower(),
            "n_operator_refs": len(operator_refs),
            "operator_refs": ";".join(operator_refs),
            "score_values_read": "false",
            "status": status,
        }
        rows.append(row)
        for check, ok in checks.items():
            lint_rows.append(
                {
                    "script": item["script"],
                    "check": check,
                    "status": "PASS" if ok else "FAIL",
                    "detail": row["doc"] if check.startswith("doc") else row["operator_refs"],
                    "score_values_read": "false",
                }
            )
    return rows, lint_rows


def write_markdown(path: Path, summary: dict[str, object], rows: list[dict[str, object]]) -> None:
    lines = [
        "# Returned-Package Documentation Cross-Link Linter V46",
        "",
        "Status: operator navigation infrastructure. No validation result and no biological claim.",
        "",
        "This generated report verifies that V46 returned-package scripts are linked",
        "from both their committed documentation files and at least one operator-facing",
        "returned-package route reference.",
        "",
        f"Overall status: `{summary['overall_status']}`; scripts checked: `{summary['n_scripts']}`; failures: `{summary['n_fail']}`.",
        "",
        "| Script | Doc | Operator refs | Status |",
        "|---|---|---:|---|",
    ]
    for row in rows:
        lines.append(
            f"| `{row['script']}` | `{row['doc']}` | `{row['n_operator_refs']}` | `{row['status']}` |"
        )
    lines.extend(
        [
            "",
            "Boundary: this report checks navigation and documentation reachability only.",
            "It does not open returned score tables, expression matrices, labels, or quarantined cohorts.",
            "",
        ]
    )
    path.write_text("\n".join(lines))


def main() -> int:
    args = parse_args()
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    rows, lint_rows = build_rows()
    n_fail = sum(1 for row in rows if row["status"] != "PASS")
    n_lint_fail = sum(1 for row in lint_rows if row["status"] != "PASS")
    all_score_values_read_false = all(row["score_values_read"] == "false" for row in rows + lint_rows)

    table = outdir / "returned_package_doc_crosslink.tsv"
    lint = outdir / "returned_package_doc_crosslink_lint.tsv"
    report = outdir / "RETURNED_PACKAGE_DOC_CROSSLINK_LINTER.md"
    summary_path = outdir / "returned_package_doc_crosslink_summary.json"
    write_tsv(
        table,
        rows,
        [
            "script",
            "role",
            "doc",
            "script_exists",
            "doc_exists",
            "doc_mentions_script",
            "n_operator_refs",
            "operator_refs",
            "score_values_read",
            "status",
        ],
    )
    write_tsv(
        lint,
        lint_rows,
        ["script", "check", "status", "detail", "score_values_read"],
    )
    summary = {
        "synthetic": False,
        "purpose": "V46 returned-package documentation cross-link linter; no biological claim",
        "n_scripts": len(rows),
        "n_fail": n_fail,
        "n_lint_checks": len(lint_rows),
        "n_lint_fail": n_lint_fail,
        "all_score_values_read_false": all_score_values_read_false,
        "table": rel(table),
        "lint": rel(lint),
        "markdown": rel(report),
        "overall_status": "PASS" if n_fail == 0 and n_lint_fail == 0 and all_score_values_read_false else "FAIL",
    }
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    write_markdown(report, summary, rows)
    print(json.dumps(summary, indent=2, sort_keys=True))
    if args.fail_on_error and summary["overall_status"] != "PASS":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
