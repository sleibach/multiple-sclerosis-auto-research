#!/usr/bin/env python3
"""Run the compact V45/V46 validation-readiness smoke-test bundle.

This is operator infrastructure only. It runs synthetic/readiness checks in a
fixed order and writes one machine-readable summary. It does not read real
cohort data, run validation, or make biological claims.
"""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v46_operator_smoke_test_bundle"


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


def command_plan(outdir: Path) -> list[tuple[str, str, list[str]]]:
    py = sys.executable
    return [
        (
            "opengwas_expiry_sentinel",
            "credential_status",
            [py, "scripts/v45_opengwas_token_expiry_sentinel.py", "--outdir", rel(outdir / "opengwas_token_expiry_sentinel")],
        ),
        (
            "locked_artifact_hash_audit",
            "integrity",
            [
                py,
                "scripts/v45_locked_artifact_hash_audit.py",
                "audit",
                "--baseline",
                "docs/validation/LOCKED_ARTIFACT_HASH_BASELINE_V45.tsv",
                "--outdir",
                rel(outdir / "locked_artifact_hash_audit"),
                "--fail-on-drift",
            ],
        ),
        (
            "author_run_return_gate_synthetic",
            "returned_package",
            [py, "scripts/v45_author_run_return_gate_runner.py", "synthetic-check", "--outdir", rel(outdir / "author_run_return_gate")],
        ),
        (
            "author_run_schema_validator_synthetic",
            "returned_package",
            [py, "scripts/v45_author_run_schema_validator.py", "synthetic-check", "--outdir", rel(outdir / "author_run_schema_validator")],
        ),
        (
            "route_analyzable_pair_synthetic",
            "returned_package",
            [py, "scripts/v45_route_analyzable_pair_calculator.py", "synthetic-check", "--outdir", rel(outdir / "route_analyzable_pair_calculator")],
        ),
        (
            "terms_governance_matrix_synthetic",
            "terms_governance",
            [py, "scripts/v46_terms_governance_matrix.py", "synthetic-check", "--outdir", rel(outdir / "terms_governance_matrix")],
        ),
        (
            "metric_format_adapter_synthetic",
            "returned_package",
            [py, "scripts/v46_author_run_metric_format_adapter.py", "synthetic-check", "--outdir", rel(outdir / "metric_format_adapter")],
        ),
        (
            "partial_label_classifier_synthetic",
            "returned_package",
            [py, "scripts/v46_partial_label_return_classifier.py", "synthetic-check", "--outdir", rel(outdir / "partial_label_return_classifier")],
        ),
        (
            "receipt_manifest_schema_linter_synthetic",
            "returned_package",
            [py, "scripts/v46_receipt_manifest_schema_linter.py", "synthetic-check", "--outdir", rel(outdir / "receipt_manifest_schema_linter")],
        ),
        (
            "package_manifest_shape_classifier_synthetic",
            "returned_package",
            [py, "scripts/v46_package_manifest_shape_classifier.py", "synthetic-check", "--outdir", rel(outdir / "package_manifest_shape_classifier")],
        ),
        (
            "receipt_manifest_to_command_plan_handoff",
            "returned_package",
            [py, "scripts/v46_receipt_manifest_to_command_plan_handoff.py", "--outdir", rel(outdir / "receipt_manifest_to_command_plan_handoff"), "--fail-on-error"],
        ),
        (
            "returned_package_command_order_planner_synthetic",
            "returned_package",
            [py, "scripts/v46_returned_package_command_order_planner.py", "synthetic-check", "--outdir", rel(outdir / "returned_package_command_order_planner")],
        ),
        (
            "returned_package_route_state_matrix",
            "returned_package",
            [py, "scripts/v46_returned_package_route_state_matrix.py", "--outdir", rel(outdir / "returned_package_route_state_matrix"), "--fail-on-error"],
        ),
        (
            "aggregate_only_returned_package_composition_dryrun",
            "returned_package",
            [py, "scripts/v46_aggregate_only_returned_package_composition_dryrun.py", "--outdir", rel(outdir / "aggregate_only_composition_dryrun"), "--fail-on-error"],
        ),
        (
            "unscoreable_return_composition_dryrun",
            "returned_package",
            [py, "scripts/v46_unscoreable_return_composition_dryrun.py", "--outdir", rel(outdir / "unscoreable_return_composition_dryrun"), "--fail-on-error"],
        ),
        (
            "safe_interpretation_classifier_synthetic",
            "returned_package",
            [py, "scripts/v46_returned_package_safe_interpretation.py", "synthetic-check", "--outdir", rel(outdir / "safe_interpretation_classifier")],
        ),
        (
            "safe_wording_fixture_linter",
            "returned_package",
            [py, "scripts/v46_safe_wording_fixture_linter.py", "--outdir", rel(outdir / "safe_wording_fixture_linter"), "--fail-on-error"],
        ),
        (
            "result_report_safe_class_linter",
            "returned_package",
            [py, "scripts/v46_result_report_safe_class_linter.py", "synthetic-check", "--outdir", rel(outdir / "result_report_safe_class_linter"), "--fail-on-error"],
        ),
        (
            "report_header_metadata_linter",
            "returned_package",
            [py, "scripts/v46_report_header_metadata_linter.py", "synthetic-check", "--outdir", rel(outdir / "report_header_metadata_linter"), "--fail-on-error"],
        ),
        (
            "report_header_repair_template_coverage",
            "returned_package",
            [py, "scripts/v46_report_header_repair_template_coverage.py", "--outdir", rel(outdir / "report_header_repair_template_coverage"), "--fail-on-error"],
        ),
        (
            "safe_class_report_template_readiness",
            "returned_package",
            [py, "scripts/v46_safe_class_report_template_readiness.py", "--outdir", rel(outdir / "safe_class_report_template_readiness"), "--fail-on-error"],
        ),
        (
            "small_n_conclusion_language",
            "power_design",
            [py, "scripts/v46_small_n_conclusion_language_table.py", "--outdir", rel(outdir / "small_n_conclusion_language")],
        ),
        (
            "analyzable_pair_confidence_envelope",
            "power_design",
            [py, "scripts/v46_analyzable_pair_confidence_envelope.py", "--outdir", rel(outdir / "analyzable_pair_confidence_envelope"), "--fail-on-error"],
        ),
        (
            "safe_interpretation_examples",
            "power_design",
            [py, "scripts/v46_safe_interpretation_examples.py", "--outdir", rel(outdir / "safe_interpretation_examples"), "--fail-on-error"],
        ),
        (
            "return_repair_request_templates",
            "returned_package",
            [py, "scripts/v46_return_repair_request_templates.py", "--outdir", rel(outdir / "return_repair_request_templates"), "--fail-on-error"],
        ),
        (
            "partial_label_repair_prioritization",
            "returned_package",
            [py, "scripts/v46_partial_label_repair_prioritization.py", "--outdir", rel(outdir / "partial_label_repair_prioritization"), "--fail-on-error"],
        ),
        (
            "first30_returned_package_decision_table",
            "returned_package",
            [py, "scripts/v46_first30_returned_package_decision_table.py", "--outdir", rel(outdir / "first30_returned_package_decision_table"), "--fail-on-error"],
        ),
        (
            "first30_repair_template_coverage_linter",
            "returned_package",
            [py, "scripts/v46_first30_repair_template_coverage_linter.py", "--outdir", rel(outdir / "first30_repair_template_coverage_linter"), "--fail-on-error"],
        ),
        (
            "first30_status_board_dryrun",
            "returned_package",
            [py, "scripts/v46_first30_returned_package_status_board_dryrun.py", "--outdir", rel(outdir / "first30_status_board_dryrun"), "--fail-on-error"],
        ),
        (
            "status_board_schema_linter",
            "returned_package",
            [py, "scripts/v46_returned_package_status_board_schema_linter.py", "--outdir", rel(outdir / "status_board_schema_linter"), "--fail-on-error"],
        ),
        (
            "status_board_markdown_roundtrip_renderer",
            "returned_package",
            [py, "scripts/v46_status_board_markdown_roundtrip_renderer.py", "--outdir", rel(outdir / "status_board_markdown_roundtrip_renderer"), "--fail-on-error"],
        ),
        (
            "returned_package_preflight_dryrun",
            "returned_package",
            [py, "scripts/v46_returned_package_preflight_dryrun.py", "--outdir", rel(outdir / "returned_package_preflight_dryrun"), "--fail-on-error"],
        ),
        (
            "returned_package_state_transition_validator",
            "returned_package",
            [py, "scripts/v46_returned_package_state_transition_validator.py", "--outdir", rel(outdir / "state_transition_validator"), "--fail-on-error"],
        ),
        (
            "operator_transcript_fixture",
            "returned_package",
            [py, "scripts/v46_operator_transcript_fixture.py", "--outdir", rel(outdir / "operator_transcript_fixture"), "--fail-on-error"],
        ),
        (
            "returned_package_handoff_bundle_manifest",
            "returned_package",
            [py, "scripts/v46_returned_package_handoff_bundle_manifest.py", "--outdir", rel(outdir / "handoff_bundle_manifest"), "--fail-on-error"],
        ),
        (
            "returned_package_quickstart_readme",
            "returned_package",
            [py, "scripts/v46_returned_package_quickstart_readme.py", "--outdir", rel(outdir / "quickstart_readme"), "--fail-on-error"],
        ),
        (
            "returned_package_doc_crosslink_linter",
            "returned_package",
            [py, "scripts/v46_returned_package_doc_crosslink_linter.py", "--outdir", rel(outdir / "doc_crosslink_linter"), "--fail-on-error"],
        ),
        (
            "returned_package_dependency_graph",
            "returned_package",
            [
                py,
                "scripts/v46_returned_package_dependency_graph.py",
                "--outdir",
                rel(outdir / "dependency_graph"),
                "--stale-status-mode",
                "warn",
                "--suite-status-mode",
                "warn",
                "--fail-on-error",
            ],
        ),
        (
            "no_raw_git_scanner",
            "repository_safety",
            [py, "scripts/v45_no_raw_git_scanner.py", "--outdir", rel(outdir / "no_raw_git_scanner")],
        ),
    ]


def run_step(name: str, group: str, command: list[str]) -> dict[str, object]:
    start = time.time()
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    elapsed = round(time.time() - start, 3)
    return {
        "step": name,
        "group": group,
        "command": " ".join(command),
        "returncode": result.returncode,
        "elapsed_seconds": elapsed,
        "status": "PASS" if result.returncode == 0 else "FAIL",
        "stdout_tail": result.stdout[-3000:] or "(empty)",
        "stderr_tail": result.stderr[-3000:] or "(empty)",
    }


def write_tsv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    args = parse_args()
    outdir = resolve(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    rows = [run_step(name, group, command) for name, group, command in command_plan(outdir)]
    steps_path = outdir / "operator_smoke_test_steps.tsv"
    write_tsv(
        steps_path,
        rows,
        ["step", "group", "command", "returncode", "elapsed_seconds", "status", "stdout_tail", "stderr_tail"],
    )
    n_fail = sum(1 for row in rows if row["status"] != "PASS")
    summary = {
        "synthetic": True,
        "purpose": "V46 compact operator smoke-test bundle; no biological claim",
        "n_steps": len(rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
        "steps": rel(steps_path),
        "output_dir": rel(outdir),
    }
    (outdir / "operator_smoke_test_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 1 if args.fail_on_error and n_fail else (0 if n_fail == 0 else 2)


if __name__ == "__main__":
    raise SystemExit(main())
