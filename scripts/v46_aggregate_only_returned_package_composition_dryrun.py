#!/usr/bin/env python3
"""Run an aggregate-only returned-package composition dry run.

This is validation-readiness infrastructure only. It composes existing V45/V46
returned-package gates on seeded synthetic aggregate outputs. It does not read
real cohort data, run discovery, change locked rules, or make biological claims.
"""

from __future__ import annotations

import argparse
import csv
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v46_aggregate_only_returned_package_composition_dryrun"
PARTIAL_PAIR = ROOT / "analysis/v45_route_analyzable_pair_calculator/gafson_partial_return/analyzable_pair_summary.json"
METADATA_CLEAN = ROOT / "analysis/v45_metadata_contradiction_stress/clean_pass/metadata_contradiction_summary.json"


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
        "cohort_id": "synthetic_aggregate_only_composition",
        "source_name": "synthetic aggregate-only returned package composition dry run",
        "source_url_or_accession": "synthetic_fixture",
        "access_tier": "collaborator",
        "received_date_utc": "2026-06-13",
        "redistribution_allowed": "no",
        "derived_metrics_allowed": "yes",
        "aggregate_publication_allowed": "yes",
        "individual_level_publication_allowed": "no",
        "approved_internal_use": "local preflight and frozen harness aggregate review",
        "forbidden_use": "commit raw data or individual-level labels",
        "commit_allowed_files": "aggregate summaries only",
        "status": "approved_for_preflight",
        "reviewer": "synthetic_v46",
        "review_date_utc": "2026-06-13",
        "notes_non_sensitive": "synthetic aggregate-only composition dry run; method behavior only",
    }
    write_tsv(path, [row], list(row.keys()))
    return path


def write_batch_clean(path: Path) -> Path:
    data = {
        "synthetic": True,
        "purpose": "synthetic clean batch/confounder warning fixture for V46 composition dry run; no biological claim",
        "overall_status": "PASS",
        "n_warn": 0,
        "n_fail": 0,
        "diagnostic_status": "PASS",
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    return path


def row_check(name: str, observed: object, expected: object, detail: str) -> dict[str, object]:
    return {
        "check": name,
        "expected": expected,
        "observed": observed,
        "status": "PASS" if observed == expected else "FAIL",
        "detail": detail,
    }


def main() -> int:
    args = parse_args()
    outdir = resolve(args.outdir)
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    py = sys.executable
    synthetic_dir = outdir / "synthetic"
    terms_path = write_terms(synthetic_dir / "aggregate_only_terms.tsv")
    batch_clean = write_batch_clean(synthetic_dir / "batch_confounder_clean.json")

    steps: list[dict[str, object]] = []
    steps.append(
        run_step(
            "build_noncanonical_variant",
            [py, "scripts/v46_author_run_metric_format_adapter.py", "synthetic-check", "--outdir", rel(outdir / "metric_adapter_seed")],
        )
    )
    variant_package = outdir / "metric_adapter_seed/synthetic_variant_package"
    normalized_package = outdir / "metric_adapter/normalized_package"
    steps.append(
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
        )
    )
    steps.append(
        run_step(
            "command_order_plan",
            [
                py,
                "scripts/v46_returned_package_command_order_planner.py",
                "plan",
                "--cohort-token",
                "synthetic_aggregate_only",
                "--package-root",
                rel(variant_package),
                "--terms-capture",
                rel(terms_path),
                "--terms-class",
                "AGGREGATE_ONLY_LOCAL_PREFLIGHT",
                "--package-kind",
                "author_run_aggregate",
                "--package-state",
                "scored",
                "--metric-format-state",
                "noncanonical",
                "--outdir",
                rel(outdir / "command_order_plan"),
                "--expect-status",
                "PASS",
            ],
        )
    )
    steps.append(
        run_step(
            "metric_format_adapter",
            [
                py,
                "scripts/v46_author_run_metric_format_adapter.py",
                "adapt",
                "--root",
                rel(variant_package),
                "--outdir",
                rel(outdir / "metric_adapter"),
                "--fail-on-error",
            ],
        )
    )
    steps.append(
        run_step(
            "author_run_return_gate",
            [
                py,
                "scripts/v45_author_run_return_gate_runner.py",
                "run",
                "--root",
                rel(normalized_package),
                "--package-state",
                "scored",
                "--outdir",
                rel(outdir / "author_run_return_gate"),
                "--fail-on-error",
            ],
        )
    )
    steps.append(
        run_step(
            "aggregate_schema_validator",
            [
                py,
                "scripts/v45_author_run_schema_validator.py",
                "run",
                "--root",
                rel(normalized_package),
                "--package-state",
                "scored",
                "--outdir",
                rel(outdir / "aggregate_schema_validator"),
                "--fail-on-error",
            ],
        )
    )
    steps.append(
        run_step(
            "partial_label_classifier",
            [
                py,
                "scripts/v46_partial_label_return_classifier.py",
                "classify",
                "--analyzable-summary",
                rel(PARTIAL_PAIR),
                "--outdir",
                rel(outdir / "partial_label_classifier"),
                "--expect-class",
                "PARTIAL_LABELS_BELOW_PLANNING_FLOOR",
            ],
        )
    )
    steps.append(
        run_step(
            "safe_interpretation_classifier",
            [
                py,
                "scripts/v46_returned_package_safe_interpretation.py",
                "classify",
                "--gate-summary",
                rel(outdir / "author_run_return_gate/author_run_return_gate_summary.json"),
                "--schema-summary",
                rel(outdir / "aggregate_schema_validator/author_run_schema_validation_summary.json"),
                "--analyzable-summary",
                rel(PARTIAL_PAIR),
                "--metadata-summary",
                rel(METADATA_CLEAN),
                "--batch-confounder-summary",
                rel(batch_clean),
                "--terms-status",
                "PASS",
                "--outdir",
                rel(outdir / "safe_interpretation_classifier"),
                "--expect-class",
                "BELOW_V45_PLANNING_FLOOR",
            ],
        )
    )
    write_tsv(
        outdir / "aggregate_only_composition_steps.tsv",
        steps,
        ["step", "command", "expected_returncode", "returncode", "elapsed_seconds", "status", "stdout_tail", "stderr_tail"],
    )

    terms = read_json(outdir / "terms_governance/terms_governance_summary.json")
    planner = read_json(outdir / "command_order_plan/returned_package_command_plan_summary.json")
    adapter = read_json(outdir / "metric_adapter/metric_format_adapter_summary.json")
    gate = read_json(outdir / "author_run_return_gate/author_run_return_gate_summary.json")
    schema = read_json(outdir / "aggregate_schema_validator/author_run_schema_validation_summary.json")
    partial = read_json(outdir / "partial_label_classifier/partial_label_classification_summary.json")
    safe = read_json(outdir / "safe_interpretation_classifier/safe_interpretation_summary.json")
    plan_rows = list(csv.DictReader((outdir / "command_order_plan/returned_package_command_plan.tsv").open(), delimiter="\t"))

    checks = [
        row_check("all_subcommands_return_expected_code", sum(1 for step in steps if step["status"] != "PASS"), 0, "all composed scripts completed as expected"),
        row_check("terms_class", terms.get("result_class"), "AGGREGATE_ONLY_LOCAL_PREFLIGHT", "aggregate-only local preflight route"),
        row_check("command_order_plan_status", planner.get("plan_status"), "PASS", "noncanonical package has a valid ordered plan"),
        row_check("metric_adapter_status", adapter.get("overall_status"), "PASS", "alias package normalized"),
        row_check("return_gate_status", gate.get("overall_status"), "PASS", "redaction and completeness passed on normalized aggregate package"),
        row_check("schema_status", schema.get("overall_status"), "PASS", "aggregate values passed schema validation"),
        row_check("partial_label_class", partial.get("result_class"), "PARTIAL_LABELS_BELOW_PLANNING_FLOOR", "partial labels force below-floor wording"),
        row_check("safe_interpretation_class", safe.get("result_class"), "BELOW_V45_PLANNING_FLOOR", "final wording blocks pass/fail interpretation"),
        row_check(
            "command_plan_no_score_values_read",
            str(all(row.get("score_values_read") == "false" for row in plan_rows)).lower(),
            "true",
            "planner rows preserve no-score-before-gates boundary",
        ),
        row_check("safe_classifier_no_score_values_read", str(safe.get("score_values_read")).lower(), "false", "safe classifier reads no returned score values"),
    ]
    write_tsv(outdir / "aggregate_only_composition_checks.tsv", checks, ["check", "expected", "observed", "status", "detail"])
    n_fail = sum(1 for check in checks if check["status"] != "PASS")
    summary = {
        "synthetic": True,
        "purpose": "V46 aggregate-only returned-package composition dry run; no biological claim",
        "n_steps": len(steps),
        "n_step_fail": sum(1 for step in steps if step["status"] != "PASS"),
        "n_checks": len(checks),
        "n_check_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
        "sample_level_data_read": False,
        "score_values_interpreted": False,
        "final_safe_interpretation_class": safe.get("result_class", "MISSING"),
        "steps": rel(outdir / "aggregate_only_composition_steps.tsv"),
        "checks": rel(outdir / "aggregate_only_composition_checks.tsv"),
    }
    (outdir / "aggregate_only_composition_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 1 if args.fail_on_error and n_fail else (0 if n_fail == 0 else 2)


if __name__ == "__main__":
    raise SystemExit(main())
