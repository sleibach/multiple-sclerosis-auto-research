#!/usr/bin/env python3
"""Check that V37 uncovered-finding rationale matches the coverage map."""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_COVERAGE = ROOT / "knowledge_external/synthesis/v37_finding_external_coverage_v48.tsv"
DEFAULT_RATIONALE = ROOT / "knowledge_external/synthesis/v37_uncovered_finding_rationale_v48.tsv"
DEFAULT_OUTDIR = ROOT / "analysis/v48_v37_uncovered_rationale_freshness_linter"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    lint = sub.add_parser("lint", help="Lint uncovered-rationale freshness")
    lint.add_argument("--coverage", type=Path, default=DEFAULT_COVERAGE)
    lint.add_argument("--rationale", type=Path, default=DEFAULT_RATIONALE)
    lint.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    lint.add_argument("--fail-on-error", action="store_true")
    synth = sub.add_parser("synthetic-check", help="Run synthetic uncovered-rationale freshness fixtures")
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


def lint_paths(coverage: Path, rationale: Path, outdir: Path, fail_on_error: bool) -> int:
    coverage_rows = read_tsv(coverage)
    rationale_rows = read_tsv(rationale)
    expected = {row.get("item", "") for row in coverage_rows if row.get("v48_coverage") == "no_v48_external_relationship_row"}
    actual = {row.get("item", "") for row in rationale_rows}
    rows = [
        {
            "check": "rationale_row_count_matches_uncovered_coverage_rows",
            "status": "PASS" if len(expected) == len(actual) else "FAIL",
            "detail": f"expected={len(expected)} actual={len(actual)}",
        },
        {
            "check": "rationale_items_match_uncovered_coverage_items",
            "status": "PASS" if expected == actual else "FAIL",
            "detail": f"missing={sorted(expected - actual)} extra={sorted(actual - expected)}",
        },
        {
            "check": "all_rationale_rows_have_rationale_class",
            "status": "PASS" if all(row.get("rationale_class") for row in rationale_rows) else "FAIL",
            "detail": "rationale_class required for every row",
        },
    ]
    n_fail = sum(1 for row in rows if row["status"] == "FAIL")
    write_tsv(outdir / "v37_uncovered_rationale_freshness_lint.tsv", rows, ["check", "status", "detail"])
    summary = {
        "synthetic": False,
        "purpose": "V48 V37 uncovered-rationale freshness lint; synthesis/navigation only; no biological claim",
        "n_uncovered_expected": len(expected),
        "n_rationale_rows": len(actual),
        "n_checks": len(rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
    }
    (outdir / "v37_uncovered_rationale_freshness_lint_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if n_fail == 0 or not fail_on_error else 2


def synthetic_root(outdir: Path) -> tuple[Path, Path]:
    root = outdir / "synthetic_root"
    if root.exists():
        shutil.rmtree(root)
    coverage = root / "knowledge_external/synthesis/v37_finding_external_coverage_v48.tsv"
    rationale = root / "knowledge_external/synthesis/v37_uncovered_finding_rationale_v48.tsv"
    write_tsv(
        coverage,
        [
            {"item": "Covered", "v48_coverage": "has_external_convergence"},
            {"item": "Missing rationale", "v48_coverage": "no_v48_external_relationship_row"},
            {"item": "Good", "v48_coverage": "no_v48_external_relationship_row"},
        ],
        ["item", "v48_coverage"],
    )
    write_tsv(
        rationale,
        [
            {"item": "Good", "rationale_class": "targeted_external_record_needed"},
            {"item": "Extra", "rationale_class": "targeted_external_record_needed"},
        ],
        ["item", "rationale_class"],
    )
    return coverage, rationale


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else ROOT / outdir
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    coverage, rationale = synthetic_root(outdir)
    lint_out = outdir / "synthetic_lint"
    lint_paths(coverage, rationale, lint_out, fail_on_error=False)
    rows = list(csv.DictReader((lint_out / "v37_uncovered_rationale_freshness_lint.tsv").open(), delimiter="\t"))
    checks = {
        "item_mismatch_fails": any(row["check"] == "rationale_items_match_uncovered_coverage_items" and row["status"] == "FAIL" for row in rows),
        "row_count_can_match_but_identity_fail": any("Missing rationale" in row["detail"] and "Extra" in row["detail"] for row in rows),
    }
    check_rows = [{"check": key, "status": "PASS" if value else "FAIL"} for key, value in checks.items()]
    write_tsv(outdir / "synthetic_v37_uncovered_rationale_freshness_checks.tsv", check_rows, ["check", "status"])
    summary = {
        "synthetic": True,
        "purpose": "V48 V37 uncovered-rationale freshness synthetic fixture; no biological claim",
        "n_checks": len(check_rows),
        "n_fail": sum(1 for row in check_rows if row["status"] != "PASS"),
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
    }
    (outdir / "synthetic_v37_uncovered_rationale_freshness_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["overall_status"] == "PASS" or not fail_on_error else 2


def main() -> int:
    args = parse_args()
    if args.command == "lint":
        return lint_paths(args.coverage, args.rationale, args.outdir, args.fail_on_error)
    if args.command == "synthetic-check":
        return synthetic_check(args.outdir, args.fail_on_error)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
