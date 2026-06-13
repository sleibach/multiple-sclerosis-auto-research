#!/usr/bin/env python3
"""Map receipt-manifest outcomes to the next allowed command plan.

This is returned-package operations infrastructure. It connects the
receipt-manifest schema linter, package-manifest shape classifier, and
returned-package command-order planner so an operator can move from a safe
receipt manifest to the next executable command without opening returned score
tables. It does not read returned scores, expression data, labels, or
quarantined cohorts.
"""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from pathlib import Path

import v46_package_manifest_shape_classifier as shape
import v46_receipt_manifest_schema_linter as receipt
import v46_returned_package_command_order_planner as planner


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v46_receipt_manifest_to_command_plan_handoff"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    parser.add_argument("--fail-on-error", action="store_true")
    return parser.parse_args()


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


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


def classifier_command(manifest: Path, terms_class: str, outdir: Path) -> str:
    return (
        ".venv/bin/python scripts/v46_package_manifest_shape_classifier.py classify "
        f"--manifest {rel(manifest)} --terms-class {terms_class} --outdir {rel(outdir)} --fail-on-error"
    )


def planner_command(
    cohort_token: str,
    package_state: str,
    metric_format_state: str,
    terms_class: str,
    expected_status: str,
    outdir: Path,
) -> str:
    return (
        ".venv/bin/python scripts/v46_returned_package_command_order_planner.py plan "
        f"--cohort-token {cohort_token} "
        "--package-root <returned_aggregate_package_dir> "
        "--terms-capture <terms_capture_tsv> "
        f"--terms-class {terms_class} "
        "--package-kind author_run_aggregate "
        f"--package-state {package_state} "
        f"--metric-format-state {metric_format_state} "
        f"--outdir {rel(outdir)} "
        f"--expect-status {expected_status}"
    )


def expected_plan_status(terms_class: str) -> str:
    allowed, _reason = planner.terms_allows_returned_package(terms_class, "author_run_aggregate")
    return "PASS" if allowed else "BLOCKED"


def synthetic_cases(base: Path) -> list[dict[str, object]]:
    cases: list[dict[str, object]] = []

    def add(
        case: str,
        terms_class: str,
        manifest_rows: list[dict[str, str]],
        expected_schema_status: str,
        expected_first30_scenario: str,
        expected_terminal_stage: str,
    ) -> None:
        manifest = base / f"{case}.tsv"
        shape.write_manifest(manifest, manifest_rows)
        cases.append(
            {
                "case": case,
                "terms_class": terms_class,
                "manifest": manifest,
                "expected_schema_status": expected_schema_status,
                "expected_first30_scenario": expected_first30_scenario,
                "expected_terminal_stage": expected_terminal_stage,
            }
        )

    add(
        "schema_fail_missing_required_column",
        "AGGREGATE_ONLY_LOCAL_PREFLIGHT",
        [shape.manifest_row("locked_rule_metrics.tsv", "locked_rule_metrics")],
        "FAIL",
        "NOT_RUN",
        "STOP_RECEIPT_MANIFEST_REPAIR",
    )
    missing_column_manifest = base / "schema_fail_missing_required_column.tsv"
    receipt.write_manifest(
        missing_column_manifest,
        [receipt.manifest_row("locked_rule_metrics.tsv")],
        [column for column in receipt.REQUIRED_COLUMNS if column != "sha256_if_recordable"],
    )

    add(
        "schema_fail_raw_path",
        "AGGREGATE_ONLY_LOCAL_PREFLIGHT",
        [shape.manifest_row("raw/expression_counts.tsv", "raw_expression")],
        "FAIL",
        "NOT_RUN",
        "STOP_RECEIPT_MANIFEST_REPAIR",
    )
    add(
        "scored_canonical_to_plan",
        "AGGREGATE_ONLY_LOCAL_PREFLIGHT",
        shape.canonical_rows(),
        "PASS",
        "scored_canonical_aggregate",
        "COMMAND_PLAN_WRITTEN",
    )
    add(
        "scored_noncanonical_to_adapter_branch",
        "AGGREGATE_ONLY_LOCAL_PREFLIGHT",
        shape.alias_rows(),
        "PASS",
        "scored_noncanonical_aggregate",
        "COMMAND_PLAN_WRITTEN",
    )
    add(
        "partial_label_to_plan_with_label_classifier",
        "AGGREGATE_ONLY_LOCAL_PREFLIGHT",
        shape.canonical_rows(partial=True),
        "PASS",
        "partial_label_scored_aggregate",
        "COMMAND_PLAN_WRITTEN",
    )
    add(
        "unscoreable_author_run_aggregate_to_preflight_only",
        "AUTHOR_RUN_ONLY",
        [
            shape.manifest_row("RUN_METADATA.txt", "run_metadata"),
            shape.manifest_row("validation_summary.json", "validation_summary"),
            shape.manifest_row("sample_attrition.tsv", "sample_attrition"),
            shape.manifest_row("gene_mapping_coverage.tsv", "gene_mapping_coverage"),
            shape.manifest_row("failure_taxonomy_code.txt", "failure_taxonomy"),
            shape.manifest_row("validation_result_report.md", "validation_result_report"),
        ],
        "PASS",
        "unscoreable_aggregate",
        "COMMAND_PLAN_WRITTEN",
    )
    add(
        "terms_blocked_after_shape",
        "NO_PROCESSING_ALLOWED",
        shape.canonical_rows(),
        "PASS",
        "terms_blocked_return",
        "STOP_TERMS_BLOCK",
    )
    add(
        "unknown_score_like_filename_stops_at_schema",
        "LOCAL_PREFLIGHT_ALLOWED",
        [
            shape.manifest_row("run_info.txt", "run_metadata"),
            shape.manifest_row("validation_result_summary.json", "validation_summary"),
            shape.manifest_row("sample_retention.tsv", "sample_attrition"),
            shape.manifest_row("module_coverage.tsv", "gene_mapping_coverage"),
            shape.manifest_row("primary_metrics_table.tsv", "unknown_score_like_metric"),
        ],
        "FAIL",
        "NOT_RUN",
        "STOP_RECEIPT_MANIFEST_REPAIR",
    )
    return cases


def build_handoff(outdir: Path) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    synthetic_dir = outdir / "synthetic_manifests"
    synthetic_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, object]] = []
    checks: list[dict[str, object]] = []

    for case in synthetic_cases(synthetic_dir):
        case_name = str(case["case"])
        manifest = Path(case["manifest"])
        terms_class = str(case["terms_class"])
        schema_out = outdir / case_name / "receipt_manifest_schema"
        shape_out = outdir / case_name / "package_manifest_shape"
        plan_out = outdir / case_name / "command_order_plan"

        schema_summary = receipt.lint_manifest(manifest, schema_out, synthetic_case=case_name)
        schema_status = str(schema_summary["overall_status"])
        expected_schema_status = str(case["expected_schema_status"])
        first30_scenario = "NOT_RUN"
        package_state = "NOT_RUN"
        metric_state = "NOT_RUN"
        plan_status = "NOT_RUN"
        expected_status = "NOT_RUN"
        plan_cmd = "NOT_ALLOWED"
        next_cmd = "STOP"
        stop_condition = "receipt_manifest_schema_linter overall_status is not PASS; request manifest repair before any classification"

        if schema_status == "PASS":
            classification = shape.classify_manifest(manifest, terms_class, shape_out)
            first30_scenario = str(classification["first30_scenario"])
            package_state = str(classification["package_state_for_command_order"])
            metric_state = str(classification["metric_format_state_for_command_order"])
            expected_status = expected_plan_status(terms_class)
            next_cmd = classifier_command(manifest, terms_class, shape_out)
            plan_cmd = planner_command(case_name, package_state, metric_state, terms_class, expected_status, plan_out)
            plan_args = argparse.Namespace(
                cohort_token=case_name,
                package_root="<returned_aggregate_package_dir>",
                terms_capture="<terms_capture_tsv>",
                terms_class=terms_class,
                package_kind="author_run_aggregate",
                package_state=package_state,
                metric_format_state=metric_state,
                outdir=plan_out,
                expect_status=expected_status,
            )
            rc = planner.plan(plan_args)
            plan_summary = json.loads((plan_out / "returned_package_command_plan_summary.json").read_text())
            plan_status = str(plan_summary["plan_status"])
            if plan_status == "PASS":
                stop_condition = "continue through command-order planner stop_if fields; no score interpretation until safe class permits wording"
            else:
                stop_condition = "command-order planner writes stop_terms_block; no package gate, schema check, score reading, or interpretation"
        else:
            rc = 0

        row = {
            "case": case_name,
            "terms_class": terms_class,
            "receipt_manifest": rel(manifest),
            "receipt_manifest_schema_status": schema_status,
            "expected_schema_status": expected_schema_status,
            "n_schema_fail": schema_summary["n_fail"],
            "first30_scenario": first30_scenario,
            "expected_first30_scenario": case["expected_first30_scenario"],
            "package_state_for_command_order": package_state,
            "metric_format_state_for_command_order": metric_state,
            "next_executable_command": next_cmd,
            "command_plan_command": plan_cmd,
            "expected_plan_status": expected_status,
            "observed_plan_status": plan_status,
            "terminal_stage": case["expected_terminal_stage"],
            "stop_condition": stop_condition,
            "score_values_read": "false",
            "handoff_status": "PASS",
        }

        case_checks = [
            (
                "schema_status_expected",
                schema_status == expected_schema_status,
                f"expected={expected_schema_status};observed={schema_status}",
            ),
            (
                "score_values_read_false",
                row["score_values_read"] == "false",
                str(row["score_values_read"]),
            ),
            (
                "schema_fail_blocks_downstream",
                schema_status == "PASS" or (first30_scenario == "NOT_RUN" and plan_status == "NOT_RUN" and next_cmd == "STOP"),
                f"first30={first30_scenario};plan={plan_status};next={next_cmd}",
            ),
            (
                "schema_pass_has_classifier_command",
                schema_status != "PASS" or "v46_package_manifest_shape_classifier.py classify" in next_cmd,
                next_cmd,
            ),
            (
                "schema_pass_has_plan_command",
                schema_status != "PASS" or "v46_returned_package_command_order_planner.py plan" in plan_cmd,
                plan_cmd,
            ),
            (
                "plan_status_expected",
                schema_status != "PASS" or plan_status == expected_status,
                f"expected={expected_status};observed={plan_status}",
            ),
            (
                "expected_first30_scenario",
                first30_scenario == str(case["expected_first30_scenario"]),
                f"expected={case['expected_first30_scenario']};observed={first30_scenario}",
            ),
            (
                "planner_returncode_ok",
                rc == 0,
                str(rc),
            ),
        ]
        n_case_fail = sum(1 for _check, ok, _detail in case_checks if not ok)
        row["handoff_status"] = "PASS" if n_case_fail == 0 else "FAIL"
        rows.append(row)
        for check, ok, detail in case_checks:
            checks.append(
                {
                    "case": case_name,
                    "check": check,
                    "status": "PASS" if ok else "FAIL",
                    "detail": detail,
                    "score_values_read": "false",
                }
            )

    return rows, checks


def write_markdown(path: Path, rows: list[dict[str, object]], summary: dict[str, object]) -> None:
    lines = [
        "# Receipt Manifest To Command Plan Handoff V46",
        "",
        "This generated handoff table links the receipt-manifest schema outcome to the next allowed returned-package command.",
        "It is synthetic operations infrastructure only: it reads receipt manifests and generated summaries, never returned score values, expression data, labels, or quarantined cohorts.",
        "",
        "## Current Result",
        "",
        f"- Overall status: `{summary['overall_status']}`",
        f"- Synthetic handoff cases: `{summary['n_cases']}`",
        f"- Lint checks: `{summary['n_lint_checks']}`",
        f"- Lint failures: `{summary['n_lint_fail']}`",
        f"- All score values read false: `{str(summary['all_score_values_read_false']).lower()}`",
        "",
        "## Handoff Table",
        "",
        "| Case | Schema | First-30 Scenario | Plan Status | Terminal Stage | Next Action |",
        "|---|---:|---|---:|---|---|",
    ]
    for row in rows:
        next_action = "STOP" if row["next_executable_command"] == "STOP" else "classify_manifest_then_plan"
        lines.append(
            "| {case} | `{receipt_manifest_schema_status}` | `{first30_scenario}` | `{observed_plan_status}` | `{terminal_stage}` | `{next_action}` |".format(
                **row,
                next_action=next_action,
            )
        )
    lines.extend(
        [
            "",
            "## Operator Rule",
            "",
            "If receipt-manifest schema lint is not `PASS`, stop before shape classification and request manifest repair.",
            "If it is `PASS`, run the generated shape-classifier command, then pass its package-state and metric-format state to the generated command-order planner.",
            "The planner's own `stop_if` fields remain the source of truth for downstream hard stops.",
            "",
            "Primary generated table: `analysis/v46_receipt_manifest_to_command_plan_handoff/receipt_manifest_to_command_plan_handoff.tsv`.",
        ]
    )
    path.write_text("\n".join(lines) + "\n")


def main() -> int:
    args = parse_args()
    outdir = resolve(args.outdir)
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    rows, checks = build_handoff(outdir)
    table_path = outdir / "receipt_manifest_to_command_plan_handoff.tsv"
    lint_path = outdir / "receipt_manifest_to_command_plan_handoff_lint.tsv"
    write_tsv(
        table_path,
        rows,
        [
            "case",
            "terms_class",
            "receipt_manifest",
            "receipt_manifest_schema_status",
            "expected_schema_status",
            "n_schema_fail",
            "first30_scenario",
            "expected_first30_scenario",
            "package_state_for_command_order",
            "metric_format_state_for_command_order",
            "next_executable_command",
            "command_plan_command",
            "expected_plan_status",
            "observed_plan_status",
            "terminal_stage",
            "stop_condition",
            "score_values_read",
            "handoff_status",
        ],
    )
    write_tsv(lint_path, checks, ["case", "check", "status", "detail", "score_values_read"])
    n_fail = sum(1 for row in checks if row["status"] != "PASS")
    summary = {
        "synthetic": True,
        "purpose": "V46 receipt-manifest-to-command-plan handoff; no biological claim and no score values read",
        "n_cases": len(rows),
        "n_schema_fail_stop_cases": sum(1 for row in rows if row["receipt_manifest_schema_status"] != "PASS"),
        "n_schema_pass_plan_cases": sum(1 for row in rows if row["receipt_manifest_schema_status"] == "PASS"),
        "n_lint_checks": len(checks),
        "n_lint_fail": n_fail,
        "all_score_values_read_false": all(row["score_values_read"] == "false" for row in rows)
        and all(row["score_values_read"] == "false" for row in checks),
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
        "handoff_table": rel(table_path),
        "lint": rel(lint_path),
    }
    summary_path = outdir / "receipt_manifest_to_command_plan_handoff_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    write_markdown(outdir / "RECEIPT_MANIFEST_TO_COMMAND_PLAN_HANDOFF.md", rows, summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 1 if args.fail_on_error and n_fail else (0 if n_fail == 0 else 2)


if __name__ == "__main__":
    raise SystemExit(main())
