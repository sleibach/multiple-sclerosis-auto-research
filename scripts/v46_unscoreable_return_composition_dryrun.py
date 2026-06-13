#!/usr/bin/env python3
"""Dry-run an unscoreable aggregate returned package.

This is validation-readiness infrastructure only. It creates a seeded synthetic
author-run aggregate package that is valid to receive but missing score-bearing
outputs, includes a failure-taxonomy code, and verifies that the V45/V46 gates
stop before schema validation, scoring, or result interpretation.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v46_unscoreable_return_composition_dryrun"
COMPLETE_PACKAGE = ROOT / "analysis/v45_author_run_output_check/synthetic_complete_author_run_package"
SCORE_BEARING_FILES = [
    "locked_rule_metrics.tsv",
    "confounder_adjustment_metrics.tsv",
    "joint_confounder_metrics.tsv",
    "batch_diagnostic_metrics.tsv",
    "validation_result_report.md",
]
FORBIDDEN_WORDING = [
    r"\bAUC\b",
    r"\bHedges\b",
    r"\beffect[- ]size\b",
    r"\bp[- ]?value\b",
    r"\bpermutation\b",
    r"\bconfidence interval\b",
    r"\bvalidation (?:pass|fail|passed|failed)\b",
    r"\b(?:pass|fail|passed|failed) validation\b",
]


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


def read_json(path: Path) -> dict[str, object]:
    try:
        return json.loads(path.read_text())
    except Exception:
        return {}


def run_step(name: str, command: list[str], expected_rc: int = 0) -> dict[str, object]:
    start = time.time()
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    elapsed = round(time.time() - start, 3)
    return {
        "step": name,
        "command": " ".join(command),
        "expected_returncode": expected_rc,
        "returncode": result.returncode,
        "elapsed_seconds": elapsed,
        "status": "PASS" if result.returncode == expected_rc else "FAIL",
        "stdout_tail": result.stdout[-2000:] or "(empty)",
        "stderr_tail": result.stderr[-2000:] or "(empty)",
    }


def write_terms(path: Path) -> Path:
    row = {
        "cohort_id": "synthetic_unscoreable_return",
        "source_name": "synthetic unscoreable aggregate returned package dry run",
        "source_url_or_accession": "synthetic_fixture",
        "access_tier": "collaborator",
        "received_date_utc": "2026-06-13",
        "redistribution_allowed": "no",
        "derived_metrics_allowed": "yes",
        "aggregate_publication_allowed": "yes",
        "individual_level_publication_allowed": "no",
        "approved_internal_use": "local preflight and aggregate repair triage",
        "forbidden_use": "commit raw data or individual-level labels",
        "commit_allowed_files": "aggregate summaries only",
        "status": "approved_for_preflight",
        "reviewer": "synthetic_v46",
        "review_date_utc": "2026-06-13",
        "notes_non_sensitive": "synthetic unscoreable aggregate return; method behavior only",
    }
    write_tsv(path, [row], list(row.keys()))
    return path


def build_unscoreable_package(path: Path) -> Path:
    if path.exists():
        shutil.rmtree(path)
    shutil.copytree(COMPLETE_PACKAGE, path)
    for filename in SCORE_BEARING_FILES:
        target = path / filename
        if target.exists():
            target.unlink()
    (path / "failure_taxonomy_code.txt").write_text(
        "synthetic: true\n"
        "failure_code: UNSCOREABLE_MISSING_LOCKED_RULE_METRICS\n"
        "failed_gate: author_run_output_completeness\n"
        "allowed_repair: rerun frozen author-run harness and return the missing aggregate score tables\n"
    )
    summary = read_json(path / "validation_summary.json")
    summary.update(
        {
            "synthetic": True,
            "primary_status": "UNSCOREABLE",
            "result_class": "UNSCOREABLE_MISSING_LOCKED_RULE_METRICS",
            "warnings": ["synthetic unscoreable fixture; no score-bearing outputs present"],
        }
    )
    (path / "validation_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    return path


def write_safe_wording(path: Path) -> None:
    path.write_text(
        "# Synthetic Unscoreable Return Wording\n\n"
        "synthetic: true\n\n"
        "Status: package received, but score-bearing aggregate outputs are missing.\n\n"
        "Allowed wording: report the failure taxonomy code, failed gate, and requested repair only. "
        "No biological claim is made, the locked rule is unchanged, and no post-hoc interpretation is permitted.\n"
    )


def row_check(name: str, observed: object, expected: object, detail: str) -> dict[str, object]:
    return {
        "check": name,
        "expected": expected,
        "observed": observed,
        "status": "PASS" if observed == expected else "FAIL",
        "detail": detail,
    }


def wording_leak_count(path: Path) -> int:
    text = path.read_text(errors="ignore")
    return sum(1 for pattern in FORBIDDEN_WORDING if re.search(pattern, text, flags=re.IGNORECASE))


def main() -> int:
    args = parse_args()
    outdir = resolve(args.outdir)
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    py = sys.executable
    synthetic_dir = outdir / "synthetic"
    terms_path = write_terms(synthetic_dir / "unscoreable_terms.tsv")
    package = build_unscoreable_package(synthetic_dir / "unscoreable_aggregate_package")
    safe_wording = outdir / "unscoreable_safe_wording.md"
    write_safe_wording(safe_wording)

    steps = [
        run_step(
            "terms_governance",
            [
                py,
                "scripts/v46_terms_governance_matrix.py",
                "classify",
                "--terms",
                rel(terms_path),
                "--outdir",
                rel(outdir / "terms_governance"),
                "--expect-class",
                "AGGREGATE_ONLY_LOCAL_PREFLIGHT",
            ],
        ),
        run_step(
            "command_order_plan",
            [
                py,
                "scripts/v46_returned_package_command_order_planner.py",
                "plan",
                "--cohort-token",
                "synthetic_unscoreable_return",
                "--package-root",
                rel(package),
                "--terms-capture",
                rel(terms_path),
                "--terms-class",
                "AGGREGATE_ONLY_LOCAL_PREFLIGHT",
                "--package-kind",
                "author_run_aggregate",
                "--package-state",
                "unscoreable",
                "--metric-format-state",
                "canonical",
                "--outdir",
                rel(outdir / "command_order_plan"),
                "--expect-status",
                "PASS",
            ],
        ),
        run_step(
            "route_state_matrix",
            [
                py,
                "scripts/v46_returned_package_route_state_matrix.py",
                "--outdir",
                rel(outdir / "route_state_matrix"),
                "--fail-on-error",
            ],
        ),
        run_step(
            "author_run_return_gate_expected_fail",
            [
                py,
                "scripts/v45_author_run_return_gate_runner.py",
                "run",
                "--root",
                rel(package),
                "--package-state",
                "unscoreable",
                "--outdir",
                rel(outdir / "author_run_return_gate"),
                "--fail-on-error",
            ],
            expected_rc=1,
        ),
        run_step(
            "author_run_output_check_expected_fail",
            [
                py,
                "scripts/v45_author_run_output_check.py",
                "check",
                "--root",
                rel(package),
                "--package-state",
                "unscoreable",
                "--outdir",
                rel(outdir / "author_run_output_check"),
                "--fail-on-error",
            ],
            expected_rc=1,
        ),
    ]
    write_tsv(
        outdir / "unscoreable_composition_steps.tsv",
        steps,
        ["step", "command", "expected_returncode", "returncode", "elapsed_seconds", "status", "stdout_tail", "stderr_tail"],
    )

    terms = read_json(outdir / "terms_governance/terms_governance_summary.json")
    planner = read_json(outdir / "command_order_plan/returned_package_command_plan_summary.json")
    gate = read_json(outdir / "author_run_return_gate/author_run_return_gate_summary.json")
    output = read_json(outdir / "author_run_output_check/author_run_output_check_summary.json")
    output_rows = list(csv.DictReader((outdir / "author_run_output_check/author_run_output_check.tsv").open(), delimiter="\t"))
    missing_score_files = sorted(row["output_file"] for row in output_rows if row["output_file"] in SCORE_BEARING_FILES and row["check_status"] == "MISSING")
    taxonomy_rows = [row for row in output_rows if row["output_file"] == "failure_taxonomy_code.txt"]
    route_rows = list(csv.DictReader((outdir / "route_state_matrix/returned_package_route_state_matrix.tsv").open(), delimiter="\t"))
    matching_route = [
        row for row in route_rows
        if row["terms_class"] == "AGGREGATE_ONLY_LOCAL_PREFLIGHT"
        and row["package_state"] == "unscoreable"
        and row["metric_format_state"] == "canonical"
    ]
    route_class = matching_route[0]["route_class"] if matching_route else "MISSING"
    leak_count = wording_leak_count(safe_wording)

    checks = [
        row_check("all_subcommands_return_expected_code", sum(1 for step in steps if step["status"] != "PASS"), 0, "expected failures are explicit and counted as pass when they fail safely"),
        row_check("terms_class", terms.get("result_class"), "AGGREGATE_ONLY_LOCAL_PREFLIGHT", "aggregate-only local preflight route"),
        row_check("command_order_plan_status", planner.get("plan_status"), "PASS", "unscoreable package has a route plan but not interpretation permission"),
        row_check("route_class", route_class, "UNSCOREABLE_AGGREGATE_PREFLIGHT_ONLY", "route matrix forces repair-only wording"),
        row_check("return_gate_status", gate.get("overall_status"), "FAIL", "completeness gate must block missing score outputs"),
        row_check("output_check_status", output.get("overall_status"), "FAIL", "direct output check must block missing score outputs"),
        row_check("failure_taxonomy_present", taxonomy_rows[0]["check_status"] if taxonomy_rows else "MISSING", "PRESENT", "unscoreable return must name failure taxonomy"),
        row_check("missing_score_bearing_files", ";".join(missing_score_files), ";".join(sorted(SCORE_BEARING_FILES)), "all score-bearing outputs are absent by design"),
        row_check("schema_validator_not_run", (outdir / "aggregate_schema_validator").exists(), False, "schema validation is not reached after completeness block"),
        row_check("safe_interpretation_not_run", (outdir / "safe_interpretation_classifier").exists(), False, "safe interpretation is not reached after completeness block"),
        row_check("safe_wording_metric_leaks", leak_count, 0, "repair-only wording must not mention score/effect language"),
    ]
    write_tsv(outdir / "unscoreable_composition_checks.tsv", checks, ["check", "expected", "observed", "status", "detail"])
    n_fail = sum(1 for check in checks if check["status"] != "PASS")
    summary = {
        "synthetic": True,
        "purpose": "V46 unscoreable returned-package composition dry run; no biological claim",
        "n_steps": len(steps),
        "n_step_fail": sum(1 for step in steps if step["status"] != "PASS"),
        "n_checks": len(checks),
        "n_check_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
        "sample_level_data_read": False,
        "score_values_interpreted": False,
        "route_class": route_class,
        "failure_taxonomy_code": "UNSCOREABLE_MISSING_LOCKED_RULE_METRICS",
        "missing_score_bearing_files": missing_score_files,
        "safe_wording": rel(safe_wording),
        "steps": rel(outdir / "unscoreable_composition_steps.tsv"),
        "checks": rel(outdir / "unscoreable_composition_checks.tsv"),
    }
    (outdir / "unscoreable_composition_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 1 if args.fail_on_error and n_fail else (0 if n_fail == 0 else 2)


if __name__ == "__main__":
    raise SystemExit(main())
