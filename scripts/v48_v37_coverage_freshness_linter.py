#!/usr/bin/env python3
"""Check that the V37-to-V48 external coverage map is current."""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_V37 = ROOT / "docs/reports/FINDINGS_SCORES_V37.tsv"
DEFAULT_MATRIX = ROOT / "knowledge_external/synthesis/convergence_contradiction_v48.tsv"
DEFAULT_COVERAGE = ROOT / "knowledge_external/synthesis/v37_finding_external_coverage_v48.tsv"
DEFAULT_OUTDIR = ROOT / "analysis/v48_v37_coverage_freshness_linter"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    lint = sub.add_parser("lint", help="Lint V37 coverage-map freshness")
    lint.add_argument("--root", type=Path, default=ROOT)
    lint.add_argument("--v37", type=Path, default=DEFAULT_V37)
    lint.add_argument("--matrix", type=Path, default=DEFAULT_MATRIX)
    lint.add_argument("--coverage", type=Path, default=DEFAULT_COVERAGE)
    lint.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    lint.add_argument("--fail-on-error", action="store_true")
    synth = sub.add_parser("synthetic-check", help="Run synthetic freshness fixtures")
    synth.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    synth.add_argument("--fail-on-error", action="store_true")
    return parser.parse_args()


def read_tsv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def lint_root(root: Path, v37: Path, matrix: Path, coverage: Path, outdir: Path, fail_on_error: bool) -> int:
    root = root.resolve()
    v37 = v37 if v37.is_absolute() else root / v37
    matrix = matrix if matrix.is_absolute() else root / matrix
    coverage = coverage if coverage.is_absolute() else root / coverage
    outdir = outdir if outdir.is_absolute() else root / outdir
    v37_rows = read_tsv(v37)
    matrix_rows = read_tsv(matrix)
    coverage_rows = read_tsv(coverage)
    v37_items = {row.get("item", "") for row in v37_rows}
    coverage_items = {row.get("item", "") for row in coverage_rows}
    matrix_findings = {row.get("grounded_finding_id", "") for row in matrix_rows}
    coverage_linked = {row.get("item", "") for row in coverage_rows if row.get("v48_coverage") != "no_v48_external_relationship_row"}
    rows: list[dict[str, object]] = [
        {
            "check": "coverage_row_count_matches_v37",
            "status": "PASS" if len(v37_rows) == len(coverage_rows) else "FAIL",
            "detail": f"v37={len(v37_rows)} coverage={len(coverage_rows)}",
        },
        {
            "check": "coverage_items_match_v37_items",
            "status": "PASS" if v37_items == coverage_items else "FAIL",
            "detail": f"missing={sorted(v37_items - coverage_items)} extra={sorted(coverage_items - v37_items)}",
        },
        {
            "check": "matrix_findings_covered_by_nonempty_coverage_rows",
            "status": "PASS" if matrix_findings <= coverage_linked else "FAIL",
            "detail": f"missing={sorted(matrix_findings - coverage_linked)}",
        },
    ]
    n_fail = sum(1 for row in rows if row["status"] == "FAIL")
    write_tsv(outdir / "v37_coverage_freshness_lint.tsv", rows, ["check", "status", "detail"])
    summary = {
        "synthetic": False,
        "purpose": "V48 V37 coverage freshness lint; navigation/synthesis only; no biological claim",
        "n_v37_rows": len(v37_rows),
        "n_matrix_rows": len(matrix_rows),
        "n_coverage_rows": len(coverage_rows),
        "n_checks": len(rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
    }
    (outdir / "v37_coverage_freshness_lint_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if n_fail == 0 or not fail_on_error else 2


def write_rows(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def synthetic_root(outdir: Path) -> tuple[Path, Path, Path, Path]:
    root = outdir / "synthetic_root"
    if root.exists():
        shutil.rmtree(root)
    v37 = root / "docs/reports/FINDINGS_SCORES_V37.tsv"
    matrix = root / "knowledge_external/synthesis/convergence_contradiction_v48.tsv"
    coverage = root / "knowledge_external/synthesis/v37_finding_external_coverage_v48.tsv"
    write_rows(v37, [{"item": "Finding A"}, {"item": "Finding B"}], ["item"])
    write_rows(matrix, [{"grounded_finding_id": "Finding A"}], ["grounded_finding_id"])
    write_rows(
        coverage,
        [
            {"item": "Finding A", "v48_coverage": "has_external_convergence"},
            {"item": "Finding C", "v48_coverage": "no_v48_external_relationship_row"},
        ],
        ["item", "v48_coverage"],
    )
    return root, v37.relative_to(root), matrix.relative_to(root), coverage.relative_to(root)


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else ROOT / outdir
    outdir.mkdir(parents=True, exist_ok=True)
    root, v37, matrix, coverage = synthetic_root(outdir)
    lint_out = outdir / "synthetic_lint"
    lint_root(root, root / v37, root / matrix, root / coverage, lint_out, fail_on_error=False)
    rows = list(csv.DictReader((lint_out / "v37_coverage_freshness_lint.tsv").open(), delimiter="\t"))
    checks = {
        "item_mismatch_fails": any(row["check"] == "coverage_items_match_v37_items" and row["status"] == "FAIL" for row in rows),
        "row_count_same_can_still_fail_by_identity": any("Finding B" in row["detail"] and "Finding C" in row["detail"] for row in rows),
        "matrix_linked_finding_passes": any(row["check"] == "matrix_findings_covered_by_nonempty_coverage_rows" and row["status"] == "PASS" for row in rows),
    }
    check_rows = [{"check": key, "status": "PASS" if value else "FAIL"} for key, value in checks.items()]
    write_tsv(outdir / "synthetic_v37_coverage_freshness_checks.tsv", check_rows, ["check", "status"])
    summary = {
        "synthetic": True,
        "purpose": "V48 V37 coverage freshness synthetic fixture; no biological claim",
        "n_checks": len(check_rows),
        "n_fail": sum(1 for row in check_rows if row["status"] != "PASS"),
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
    }
    (outdir / "synthetic_v37_coverage_freshness_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["overall_status"] == "PASS" or not fail_on_error else 2


def main() -> int:
    args = parse_args()
    if args.command == "lint":
        return lint_root(args.root, args.v37, args.matrix, args.coverage, args.outdir, args.fail_on_error)
    if args.command == "synthetic-check":
        return synthetic_check(args.outdir, args.fail_on_error)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
