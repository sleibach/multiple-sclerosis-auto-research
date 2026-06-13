#!/usr/bin/env python3
"""Run the V46 returned-package synthetic/readiness regression suite.

This is software and validation-readiness infrastructure only. It runs
synthetic or governance checks for returned-package handling. It does not read
real cohort data, run validation, change locked rules, or make biological
claims.
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
DEFAULT_OUTDIR = ROOT / "analysis/v46_returned_package_regression_suite"


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


def command_plan(outdir: Path) -> list[tuple[str, str, list[str]]]:
    py = sys.executable
    return [
        (
            "terms_governance_matrix_synthetic",
            "route_terms",
            [py, "scripts/v46_terms_governance_matrix.py", "synthetic-check", "--outdir", rel(outdir / "terms_governance_matrix")],
        ),
        (
            "metric_format_adapter_synthetic",
            "aggregate_format",
            [py, "scripts/v46_author_run_metric_format_adapter.py", "synthetic-check", "--outdir", rel(outdir / "metric_format_adapter")],
        ),
        (
            "partial_label_classifier_synthetic",
            "label_coverage",
            [py, "scripts/v46_partial_label_return_classifier.py", "synthetic-check", "--outdir", rel(outdir / "partial_label_classifier")],
        ),
        (
            "returned_package_command_order_planner_synthetic",
            "command_order",
            [py, "scripts/v46_returned_package_command_order_planner.py", "synthetic-check", "--outdir", rel(outdir / "command_order_planner")],
        ),
        (
            "returned_package_route_state_matrix",
            "route_state",
            [py, "scripts/v46_returned_package_route_state_matrix.py", "--outdir", rel(outdir / "route_state_matrix"), "--fail-on-error"],
        ),
        (
            "aggregate_only_composition_dryrun",
            "composition",
            [py, "scripts/v46_aggregate_only_returned_package_composition_dryrun.py", "--outdir", rel(outdir / "aggregate_only_composition"), "--fail-on-error"],
        ),
        (
            "unscoreable_return_composition_dryrun",
            "composition",
            [py, "scripts/v46_unscoreable_return_composition_dryrun.py", "--outdir", rel(outdir / "unscoreable_return_composition"), "--fail-on-error"],
        ),
        (
            "safe_interpretation_classifier_synthetic",
            "safe_wording",
            [py, "scripts/v46_returned_package_safe_interpretation.py", "synthetic-check", "--outdir", rel(outdir / "safe_interpretation_classifier")],
        ),
        (
            "safe_wording_fixture_linter",
            "safe_wording",
            [py, "scripts/v46_safe_wording_fixture_linter.py", "--outdir", rel(outdir / "safe_wording_fixture_linter"), "--fail-on-error"],
        ),
        (
            "readiness_stale_output_detector",
            "governance",
            [py, "scripts/v45_readiness_stale_output_detector.py", "--outdir", rel(outdir / "readiness_stale_output_detector")],
        ),
        (
            "no_raw_git_scanner",
            "repository_safety",
            [py, "scripts/v45_no_raw_git_scanner.py", "--outdir", rel(outdir / "no_raw_git_scanner")],
        ),
    ]


def main() -> int:
    args = parse_args()
    outdir = resolve(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    rows = [run_step(name, group, command) for name, group, command in command_plan(outdir)]
    steps_path = outdir / "returned_package_regression_steps.tsv"
    write_tsv(
        steps_path,
        rows,
        ["step", "group", "command", "returncode", "elapsed_seconds", "status", "stdout_tail", "stderr_tail"],
    )
    n_fail = sum(1 for row in rows if row["status"] != "PASS")
    summary = {
        "synthetic": True,
        "purpose": "V46 returned-package regression suite; no biological claim",
        "n_steps": len(rows),
        "n_fail": n_fail,
        "total_elapsed_seconds": round(sum(float(row["elapsed_seconds"]) for row in rows), 3),
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
        "steps": rel(steps_path),
        "output_dir": rel(outdir),
    }
    (outdir / "returned_package_regression_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 1 if args.fail_on_error and n_fail else (0 if n_fail == 0 else 2)


if __name__ == "__main__":
    raise SystemExit(main())
