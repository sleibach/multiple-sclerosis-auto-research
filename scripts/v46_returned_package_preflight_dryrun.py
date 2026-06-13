#!/usr/bin/env python3
"""Run a one-command returned-package preflight dry run.

This is validation-readiness infrastructure. It composes receipt-manifest schema
linting, package-shape classification, first-30 route lookup, state-transition
validation, and repair-template coverage on synthetic receipt manifests. It
does not open returned result tables, inspect expression data, read labels, or
access quarantined cohorts.
"""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
import time
from pathlib import Path

import v46_author_run_metric_format_adapter as adapter


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v46_returned_package_preflight_dryrun"
FIRST30_TABLE = ROOT / "analysis/v46_first30_returned_package_decision_table/first30_returned_package_decision_table.tsv"
REPAIR_COVERAGE = ROOT / "analysis/v46_first30_repair_template_coverage_linter/first30_repair_template_coverage.tsv"

CANONICAL_FILES = [name for name in adapter.FILE_ALIASES if name != "failure_taxonomy_code.txt"]


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


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return [{key: value or "" for key, value in row.items()} for row in csv.DictReader(handle, delimiter="\t")]


def write_tsv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def run_step(case: str, step: str, command: list[str], expected_rc: int = 0) -> dict[str, object]:
    start = time.time()
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    elapsed = round(time.time() - start, 3)
    return {
        "case": case,
        "step": step,
        "command": " ".join(command),
        "expected_returncode": expected_rc,
        "returncode": result.returncode,
        "elapsed_seconds": elapsed,
        "status": "PASS" if result.returncode == expected_rc else "FAIL",
        "stdout_tail": result.stdout[-2000:] or "(empty)",
        "stderr_tail": result.stderr[-2000:] or "(empty)",
        "score_values_read": "false",
    }


def manifest_row(filename: str, notes: str = "") -> dict[str, str]:
    return {
        "cohort_id": "synthetic_preflight",
        "receipt_timestamp_utc": "2026-06-13T00:00:00Z",
        "received_from": "synthetic_fixture",
        "relative_path_or_external_location": filename,
        "file_role": Path(filename).name.removesuffix(".tsv").removesuffix(".json").removesuffix(".txt").removesuffix(".md"),
        "bytes": "123",
        "sha256_if_recordable": "synthetic",
        "sensitivity_class": "derived_non_sensitive_summary",
        "terms_status": "synthetic",
        "commit_allowed": "yes",
        "next_gate": "manifest_shape_classifier",
        "notes": notes,
    }


def write_manifest(path: Path, rows: list[dict[str, str]]) -> Path:
    write_tsv(
        path,
        rows,
        [
            "cohort_id",
            "receipt_timestamp_utc",
            "received_from",
            "relative_path_or_external_location",
            "file_role",
            "bytes",
            "sha256_if_recordable",
            "sensitivity_class",
            "terms_status",
            "commit_allowed",
            "next_gate",
            "notes",
        ],
    )
    return path


def canonical_rows() -> list[dict[str, str]]:
    return [manifest_row(name) for name in CANONICAL_FILES]


def alias_rows() -> list[dict[str, str]]:
    rows = []
    for canonical in CANONICAL_FILES:
        aliases = adapter.FILE_ALIASES[canonical]
        rows.append(manifest_row(aliases[1] if len(aliases) > 1 else aliases[0]))
    return rows


def case_definitions(outdir: Path) -> list[dict[str, object]]:
    synthetic = outdir / "synthetic"
    cases: list[dict[str, object]] = []

    def add(case: str, terms_class: str, expected_schema: str, expected_scenario: str, rows: list[dict[str, str]]) -> None:
        manifest = write_manifest(synthetic / case / "receipt_manifest.tsv", rows)
        cases.append(
            {
                "case": case,
                "terms_class": terms_class,
                "expected_schema_status": expected_schema,
                "expected_first30_scenario": expected_scenario,
                "manifest": manifest,
            }
        )

    add("canonical_scored_preflight", "AGGREGATE_ONLY_LOCAL_PREFLIGHT", "PASS", "scored_canonical_aggregate", canonical_rows())
    add("noncanonical_scored_preflight", "AGGREGATE_ONLY_LOCAL_PREFLIGHT", "PASS", "scored_noncanonical_aggregate", alias_rows())
    unknown = canonical_rows()
    unknown[0]["relative_path_or_external_location"] = "mystery_score_summary.tsv"
    add("unknown_alias_preflight", "LOCAL_PREFLIGHT_ALLOWED", "FAIL", "schema_block_before_classification", unknown)
    unscoreable = [manifest_row("failure_taxonomy_code.txt")]
    add("unscoreable_preflight", "AUTHOR_RUN_ONLY", "PASS", "unscoreable_aggregate", unscoreable)
    add("terms_blocked_preflight", "NO_PROCESSING_ALLOWED", "PASS", "terms_blocked_return", canonical_rows())
    add("unsafe_raw_manifest", "AGGREGATE_ONLY_LOCAL_PREFLIGHT", "FAIL", "schema_block_before_classification", [manifest_row("raw/expression_counts.tsv")])
    return cases


def json_summary(path: Path) -> dict[str, object]:
    try:
        return json.loads(path.read_text())
    except Exception:
        return {}


def first30_counts() -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in read_tsv(FIRST30_TABLE):
        counts[row["scenario"]] = counts.get(row["scenario"], 0) + 1
    return counts


def repair_coverage_status_by_scenario() -> dict[str, str]:
    rows = read_tsv(REPAIR_COVERAGE)
    status: dict[str, str] = {}
    for row in rows:
        scenario = row["scenario"]
        if scenario not in status:
            status[scenario] = "PASS"
        if row["coverage_status"] != "PASS":
            status[scenario] = "FAIL"
    return status


def main() -> int:
    args = parse_args()
    outdir = resolve(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    py = sys.executable
    steps: list[dict[str, object]] = []
    cases_out: list[dict[str, object]] = []
    first30 = first30_counts()
    coverage = repair_coverage_status_by_scenario()

    global_steps = [
        (
            "global",
            "first30_decision_table",
            [py, "scripts/v46_first30_returned_package_decision_table.py", "--outdir", rel(outdir / "first30_decision_table"), "--fail-on-error"],
        ),
        (
            "global",
            "state_transition_validator",
            [py, "scripts/v46_returned_package_state_transition_validator.py", "--outdir", rel(outdir / "state_transition_validator"), "--fail-on-error"],
        ),
        (
            "global",
            "repair_template_coverage",
            [py, "scripts/v46_first30_repair_template_coverage_linter.py", "--outdir", rel(outdir / "repair_template_coverage"), "--fail-on-error"],
        ),
    ]
    for case, step, command in global_steps:
        steps.append(run_step(case, step, command))

    state_status = json_summary(outdir / "state_transition_validator/returned_package_state_transition_summary.json").get("overall_status", "")
    coverage_status = json_summary(outdir / "repair_template_coverage/first30_repair_template_coverage_summary.json").get("overall_status", "")

    for case in case_definitions(outdir):
        case_name = str(case["case"])
        case_dir = outdir / case_name
        manifest = Path(case["manifest"])
        schema_step = run_step(
            case_name,
            "receipt_manifest_schema_lint",
            [
                py,
                "scripts/v46_receipt_manifest_schema_linter.py",
                "lint",
                "--manifest",
                rel(manifest),
                "--outdir",
                rel(case_dir / "receipt_manifest_schema_lint"),
            ],
            expected_rc=0 if case["expected_schema_status"] == "PASS" else 2,
        )
        steps.append(schema_step)
        schema_summary = json_summary(case_dir / "receipt_manifest_schema_lint/receipt_manifest_schema_lint_summary.json")
        observed_schema = str(schema_summary.get("overall_status", ""))

        observed_scenario = "schema_block_before_classification"
        classifier_rc = "not_run"
        route_rows = 0
        scenario_repair_status = "not_applicable"
        if observed_schema == "PASS":
            classify_step = run_step(
                case_name,
                "package_manifest_shape_classification",
                [
                    py,
                    "scripts/v46_package_manifest_shape_classifier.py",
                    "classify",
                    "--manifest",
                    rel(manifest),
                    "--terms-class",
                    str(case["terms_class"]),
                    "--outdir",
                    rel(case_dir / "package_manifest_shape_classifier"),
                    "--fail-on-error",
                ],
            )
            steps.append(classify_step)
            classifier_rc = str(classify_step["returncode"])
            class_summary = json_summary(case_dir / "package_manifest_shape_classifier/package_manifest_shape_classification_summary.json")
            observed_scenario = str(class_summary.get("first30_scenario", ""))
            route_rows = first30.get(observed_scenario, 0)
            scenario_repair_status = coverage.get(observed_scenario, "MISSING")

        expected_scenario = str(case["expected_first30_scenario"])
        case_ok = (
            observed_schema == case["expected_schema_status"]
            and observed_scenario == expected_scenario
            and (observed_schema != "PASS" or (route_rows > 0 and scenario_repair_status == "PASS"))
            and state_status == "PASS"
            and coverage_status == "PASS"
        )
        cases_out.append(
            {
                "case": case_name,
                "terms_class": case["terms_class"],
                "expected_schema_status": case["expected_schema_status"],
                "observed_schema_status": observed_schema,
                "expected_first30_scenario": expected_scenario,
                "observed_first30_scenario": observed_scenario,
                "classifier_returncode": classifier_rc,
                "first30_route_rows": route_rows,
                "repair_coverage_status": scenario_repair_status,
                "state_transition_status": state_status,
                "case_status": "PASS" if case_ok else "FAIL",
                "score_values_read": "false",
            }
        )

    steps_path = outdir / "returned_package_preflight_dryrun_steps.tsv"
    cases_path = outdir / "returned_package_preflight_dryrun_cases.tsv"
    write_tsv(
        steps_path,
        steps,
        ["case", "step", "command", "expected_returncode", "returncode", "elapsed_seconds", "status", "stdout_tail", "stderr_tail", "score_values_read"],
    )
    write_tsv(
        cases_path,
        cases_out,
        [
            "case",
            "terms_class",
            "expected_schema_status",
            "observed_schema_status",
            "expected_first30_scenario",
            "observed_first30_scenario",
            "classifier_returncode",
            "first30_route_rows",
            "repair_coverage_status",
            "state_transition_status",
            "case_status",
            "score_values_read",
        ],
    )
    n_step_fail = sum(1 for row in steps if row["status"] != "PASS")
    n_case_fail = sum(1 for row in cases_out if row["case_status"] != "PASS")
    summary = {
        "synthetic": True,
        "purpose": "V46 one-command returned-package preflight dry run; no biological claim",
        "n_cases": len(cases_out),
        "n_case_fail": n_case_fail,
        "n_steps": len(steps),
        "n_step_fail": n_step_fail,
        "state_transition_status": state_status,
        "repair_coverage_status": coverage_status,
        "all_score_values_read_false": all(row["score_values_read"] == "false" for row in steps) and all(row["score_values_read"] == "false" for row in cases_out),
        "overall_status": "PASS" if n_case_fail == 0 and n_step_fail == 0 else "FAIL",
        "cases": rel(cases_path),
        "steps": rel(steps_path),
    }
    (outdir / "returned_package_preflight_dryrun_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    if args.fail_on_error and summary["overall_status"] != "PASS":
        return 1
    return 0 if summary["overall_status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
