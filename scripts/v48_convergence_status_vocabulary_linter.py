#!/usr/bin/env python3
"""Lint V48 convergence relationship/status vocabulary."""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MATRIX = ROOT / "knowledge_external/synthesis/convergence_contradiction_v48.tsv"
DEFAULT_OUTDIR = ROOT / "analysis/v48_convergence_status_vocabulary_linter"

ALLOWED_RELATIONSHIPS = {"converges", "contradicts", "insufficient-overlap"}
ALLOWED_STATUSES = {
    "CORROBORATION_FROM_INDEPENDENT_SOURCE",
    "NO_DIRECT_EXTERNAL_CORROBORATION",
    "RESOURCE_CAN_QUEUE_FUTURE_CHECK",
    "GENERAL_CONTEXT_NOT_LOCUS_CORROBORATION",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    lint = sub.add_parser("lint", help="Lint real convergence status vocabulary")
    lint.add_argument("--matrix", type=Path, default=DEFAULT_MATRIX)
    lint.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    lint.add_argument("--fail-on-error", action="store_true")
    synth = sub.add_parser("synthetic-check", help="Run synthetic vocabulary fixture")
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
    rows: list[dict[str, object]] = []
    matrix_rows = read_tsv(matrix) if matrix.exists() else []
    for index, row in enumerate(matrix_rows, start=1):
        relationship = row.get("relationship_class", "")
        status = row.get("synthesis_status", "")
        rows.append({"row": index, "field": "relationship_class", "value": relationship, "status": "PASS" if relationship in ALLOWED_RELATIONSHIPS else "FAIL"})
        rows.append({"row": index, "field": "synthesis_status", "value": status, "status": "PASS" if status in ALLOWED_STATUSES else "FAIL"})
        if relationship == "converges":
            rows.append({"row": index, "field": "converges_requires_corroboration_status", "value": status, "status": "PASS" if status == "CORROBORATION_FROM_INDEPENDENT_SOURCE" else "FAIL"})
        if relationship == "contradicts":
            rows.append({"row": index, "field": "contradiction_status_present", "value": status, "status": "PASS" if "CONTRADICTION" in status else "FAIL"})
    n_fail = sum(1 for row in rows if row["status"] != "PASS")
    write_tsv(outdir / "convergence_status_vocabulary_lint.tsv", rows, ["row", "field", "value", "status"])
    summary = {
        "synthetic": False,
        "purpose": "V48 convergence status vocabulary lint; no biological claim",
        "n_matrix_rows": len(matrix_rows),
        "n_checks": len(rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
        "lint": str(outdir / "convergence_status_vocabulary_lint.tsv"),
    }
    (outdir / "convergence_status_vocabulary_lint_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["overall_status"] == "PASS" or not fail_on_error else 2


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else ROOT / outdir
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    matrix = outdir / "synthetic_matrix.tsv"
    write_tsv(
        matrix,
        [
            {"relationship_class": "converges", "synthesis_status": "CORROBORATION_FROM_INDEPENDENT_SOURCE"},
            {"relationship_class": "made-up", "synthesis_status": "BAD_STATUS"},
            {"relationship_class": "converges", "synthesis_status": "NO_DIRECT_EXTERNAL_CORROBORATION"},
        ],
        ["relationship_class", "synthesis_status"],
    )
    lint_out = outdir / "synthetic_lint"
    lint_matrix(matrix, lint_out, fail_on_error=False)
    rows = read_tsv(lint_out / "convergence_status_vocabulary_lint.tsv")
    checks = {
        "valid_convergence_passes": any(row["row"] == "1" and row["field"] == "relationship_class" and row["status"] == "PASS" for row in rows),
        "bad_relationship_fails": any(row["row"] == "2" and row["field"] == "relationship_class" and row["status"] == "FAIL" for row in rows),
        "bad_status_fails": any(row["row"] == "2" and row["field"] == "synthesis_status" and row["status"] == "FAIL" for row in rows),
        "bad_convergence_status_fails": any(row["row"] == "3" and row["field"] == "converges_requires_corroboration_status" and row["status"] == "FAIL" for row in rows),
    }
    check_rows = [{"check": key, "status": "PASS" if value else "FAIL"} for key, value in checks.items()]
    write_tsv(outdir / "synthetic_convergence_status_vocabulary_checks.tsv", check_rows, ["check", "status"])
    summary = {
        "synthetic": True,
        "purpose": "V48 convergence status vocabulary synthetic fixture; no biological claim",
        "n_checks": len(check_rows),
        "n_fail": sum(1 for row in check_rows if row["status"] != "PASS"),
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
    }
    (outdir / "synthetic_convergence_status_vocabulary_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
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
