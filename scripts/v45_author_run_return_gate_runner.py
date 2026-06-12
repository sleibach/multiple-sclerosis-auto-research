#!/usr/bin/env python3
"""Run the author-run aggregate return gates in the required order.

This runner is validation-readiness infrastructure only. It does not inspect raw
expression, does not interpret biology, and does not run the frozen validation
harness. It enforces the order: redaction precheck first, completeness second.
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
DEFAULT_OUTDIR = ROOT / "analysis/v45_author_run_return_gate_runner"
COMPLETE_ROOT = ROOT / "analysis/v45_author_run_output_check/synthetic_complete_author_run_package"
RISKY_ROOT = ROOT / "analysis/v45_author_run_redaction_precheck/synthetic_risky_aggregate_package"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    run = sub.add_parser("run")
    run.add_argument("--root", type=Path, required=True, help="Returned aggregate package directory.")
    run.add_argument("--package-state", choices=["scored", "unscoreable"], default="scored")
    run.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    run.add_argument("--fail-on-error", action="store_true")

    syn = sub.add_parser("synthetic-check")
    syn.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    return parser.parse_args()


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def run_command(name: str, command: list[str]) -> dict[str, object]:
    start = time.time()
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    elapsed = round(time.time() - start, 3)
    return {
        "step": name,
        "command": " ".join(command),
        "returncode": result.returncode,
        "elapsed_seconds": elapsed,
        "status": "PASS" if result.returncode == 0 else "FAIL",
        "stdout_tail": result.stdout[-2000:],
        "stderr_tail": result.stderr[-2000:],
    }


def write_steps(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        fieldnames = ["step", "command", "returncode", "elapsed_seconds", "status", "stdout_tail", "stderr_tail"]
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_json(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError:
        return {}


def run_gate(root: Path, package_state: str, outdir: Path, fail_on_error: bool) -> int:
    outdir.mkdir(parents=True, exist_ok=True)
    py = sys.executable
    root = resolve(root)
    redaction_out = outdir / "redaction_precheck"
    completeness_out = outdir / "output_completeness"
    steps: list[dict[str, object]] = []

    redaction = run_command(
        "author_run_redaction_precheck",
        [
            py,
            "scripts/v45_author_run_redaction_precheck.py",
            "check",
            "--root",
            rel(root),
            "--outdir",
            rel(redaction_out),
            "--fail-on-error",
        ],
    )
    steps.append(redaction)

    completeness_status = "SKIPPED"
    if redaction["status"] == "PASS":
        completeness = run_command(
            "author_run_output_completeness",
            [
                py,
                "scripts/v45_author_run_output_check.py",
                "check",
                "--root",
                rel(root),
                "--package-state",
                package_state,
                "--outdir",
                rel(completeness_out),
                "--fail-on-error",
            ],
        )
        steps.append(completeness)
        completeness_status = str(completeness["status"])
    else:
        steps.append(
            {
                "step": "author_run_output_completeness",
                "command": "SKIPPED because redaction precheck failed",
                "returncode": "",
                "elapsed_seconds": 0.0,
                "status": "SKIPPED",
                "stdout_tail": "",
                "stderr_tail": "",
            }
        )

    write_steps(outdir / "author_run_return_gate_steps.tsv", steps)

    redaction_summary = read_json(redaction_out / "author_run_redaction_precheck_summary.json")
    completeness_summary = read_json(completeness_out / "author_run_output_check_summary.json")
    overall = "PASS" if redaction["status"] == "PASS" and completeness_status == "PASS" else "FAIL"
    summary = {
        "synthetic": "synthetic" in str(root).lower() or "v42_harness_validation" in str(root).lower(),
        "purpose": "author-run aggregate return gate runner; no biological claim",
        "root": rel(root),
        "package_state": package_state,
        "redaction_status": redaction["status"],
        "redaction_summary": redaction_summary,
        "completeness_status": completeness_status,
        "completeness_summary": completeness_summary,
        "overall_status": overall,
        "steps": rel(outdir / "author_run_return_gate_steps.tsv"),
    }
    (outdir / "author_run_return_gate_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 1 if fail_on_error and overall != "PASS" else 0


def synthetic_check(outdir: Path) -> int:
    clean_incomplete = outdir / "synthetic_clean_incomplete_package"
    if clean_incomplete.exists():
        shutil.rmtree(clean_incomplete)
    shutil.copytree(COMPLETE_ROOT, clean_incomplete)
    for filename in ["RUN_METADATA.txt", "batch_diagnostic_metrics.tsv", "validation_result_report.md"]:
        path = clean_incomplete / filename
        if path.exists():
            path.unlink()
    cases = [
        ("complete_pass", COMPLETE_ROOT, "scored", "PASS"),
        ("incomplete_completeness_fail", clean_incomplete, "scored", "FAIL"),
        ("risky_redaction_fail", RISKY_ROOT, "scored", "FAIL"),
    ]
    rows = []
    for name, root, package_state, expected in cases:
        case_out = outdir / name
        rc = run_gate(root, package_state, case_out, False)
        summary = read_json(case_out / "author_run_return_gate_summary.json")
        rows.append(
            {
                "case": name,
                "root": rel(root),
                "expected": expected,
                "observed": summary.get("overall_status", "MISSING"),
                "redaction_status": summary.get("redaction_status", "MISSING"),
                "completeness_status": summary.get("completeness_status", "MISSING"),
                "returncode_without_fail_on_error": rc,
            }
        )
    outdir.mkdir(parents=True, exist_ok=True)
    with (outdir / "synthetic_case_summary.tsv").open("w", newline="") as handle:
        fieldnames = [
            "case",
            "root",
            "expected",
            "observed",
            "redaction_status",
            "completeness_status",
            "returncode_without_fail_on_error",
        ]
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    n_mismatch = sum(1 for row in rows if row["expected"] != row["observed"])
    summary = {
        "synthetic": True,
        "purpose": "author-run return gate runner synthetic regression; no biological claim",
        "n_cases": len(rows),
        "n_mismatch": n_mismatch,
        "overall_status": "PASS" if n_mismatch == 0 else "FAIL",
        "cases": rows,
    }
    (outdir / "synthetic_check_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if n_mismatch == 0 else 2


def main() -> int:
    args = parse_args()
    if args.cmd == "synthetic-check":
        return synthetic_check(resolve(args.outdir))
    return run_gate(resolve(args.root), args.package_state, resolve(args.outdir), args.fail_on_error)


if __name__ == "__main__":
    raise SystemExit(main())
