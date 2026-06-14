#!/usr/bin/env python3
"""Check V48 convergence matrix coverage for priority grounded findings."""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MATRIX = ROOT / "knowledge_external/synthesis/convergence_contradiction_v48.tsv"
DEFAULT_OUTDIR = ROOT / "analysis/v48_convergence_matrix_coverage_linter"

REQUIRED_FINDINGS = [
    "Bounded APC/HLA-II early treatment-response monitoring scalar",
    "V22 scalar is immune-tone bounded, not steroid/composition artifact",
    "MS-UC is strongest tested genome-wide genetics comparator",
    "Coupled APC remodeling architecture",
    "Layer-specific autoimmune transfer-validity map",
    "ZMIZ1 opposite-direction MS/Crohn decoupling",
    "chr1 KIF21B/GPR25 locus resolves to real biology but hard target",
    "PTGER4 mixed shared/distinct signal closes naive transfer",
    "No validated broad immune-state simulator from held data",
    "Coupled-axis successor rule does not beat scalar",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    lint = sub.add_parser("lint", help="Lint real V48 matrix coverage")
    lint.add_argument("--matrix", type=Path, default=DEFAULT_MATRIX)
    lint.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    lint.add_argument("--fail-on-error", action="store_true")
    synth = sub.add_parser("synthetic-check", help="Run synthetic coverage fixtures")
    synth.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    synth.add_argument("--fail-on-error", action="store_true")
    return parser.parse_args()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def lint_matrix(matrix: Path, outdir: Path, fail_on_error: bool) -> int:
    outdir.mkdir(parents=True, exist_ok=True)
    rows = read_tsv(matrix) if matrix.exists() else []
    represented = {row.get("grounded_finding_id", "") for row in rows}
    lint_rows = [
        {
            "grounded_finding_id": finding,
            "check": "priority_finding_represented",
            "status": "PASS" if finding in represented else "FAIL",
            "detail": "present" if finding in represented else "missing",
        }
        for finding in REQUIRED_FINDINGS
    ]
    n_fail = sum(1 for row in lint_rows if row["status"] != "PASS")
    write_tsv(outdir / "convergence_matrix_coverage_lint.tsv", lint_rows, ["grounded_finding_id", "check", "status", "detail"])
    summary = {
        "synthetic": False,
        "purpose": "V48 convergence matrix coverage lint; no biological claim",
        "n_required_findings": len(REQUIRED_FINDINGS),
        "n_matrix_rows": len(rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
        "lint": str(outdir / "convergence_matrix_coverage_lint.tsv"),
    }
    (outdir / "convergence_matrix_coverage_lint_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["overall_status"] == "PASS" or not fail_on_error else 2


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else ROOT / outdir
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True)
    matrix = outdir / "synthetic_matrix.tsv"
    write_tsv(matrix, [{"grounded_finding_id": REQUIRED_FINDINGS[0]}], ["grounded_finding_id"])
    lint_out = outdir / "synthetic_lint"
    lint_matrix(matrix, lint_out, fail_on_error=False)
    rows = read_tsv(lint_out / "convergence_matrix_coverage_lint.tsv")
    checks = {
        "present_required_finding_passes": any(row["grounded_finding_id"] == REQUIRED_FINDINGS[0] and row["status"] == "PASS" for row in rows),
        "missing_required_finding_fails": any(row["grounded_finding_id"] == REQUIRED_FINDINGS[1] and row["status"] == "FAIL" for row in rows),
    }
    check_rows = [{"check": key, "status": "PASS" if value else "FAIL"} for key, value in checks.items()]
    write_tsv(outdir / "synthetic_convergence_matrix_coverage_checks.tsv", check_rows, ["check", "status"])
    summary = {
        "synthetic": True,
        "purpose": "V48 convergence matrix coverage synthetic fixture; no biological claim",
        "n_checks": len(check_rows),
        "n_fail": sum(1 for row in check_rows if row["status"] != "PASS"),
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
    }
    (outdir / "synthetic_convergence_matrix_coverage_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["overall_status"] == "PASS" or not fail_on_error else 2


def main() -> int:
    args = parse_args()
    if args.command == "lint":
        return lint_matrix(args.matrix, args.outdir, args.fail_on_error)
    if args.command == "synthetic-check":
        return synthetic_check(args.outdir, args.fail_on_error)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
