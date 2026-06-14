#!/usr/bin/env python3
"""Check that the public external index links all required V48 artifacts."""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INDEX = ROOT / "knowledge_external/INDEX.md"
DEFAULT_OUTDIR = ROOT / "analysis/v48_public_index_freshness_linter"


REQUIRED_TARGETS = [
    "catalogs/indexes/EXTERNAL_KNOWLEDGE_INDEX.md",
    "catalogs/indexes/EXTERNAL_RESOURCE_COMPARATOR_MATRIX_V48.md",
    "catalogs/indexes/SOURCE_DOMAIN_REVIEW_V48.md",
    "catalogs/indexes/SOURCE_DOMAIN_RELATIONSHIP_ROLLUP_V48.md",
    "catalogs/indexes/SOURCE_TERMS_COVERAGE_V48.md",
    "catalogs/indexes/SOURCE_TERMS_REVIEW_QUEUE_V48.md",
    "catalogs/indexes/V48_GOVERNANCE_NAVIGATION.md",
    "catalogs/indexes/V48_EXTERNAL_GOVERNANCE_HANDOFF.md",
    "synthesis/CONVERGENCE_CONTRADICTION_V48.md",
    "synthesis/CONVERGENCE_DECISION_TABLE_V48.md",
    "synthesis/V37_FINDING_EXTERNAL_COVERAGE_V48.md",
    "synthesis/V37_UNCOVERED_FINDING_RATIONALE_V48.md",
    "synthesis/FUTURE_GROUNDING_QUEUE_V48.md",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    lint = sub.add_parser("lint", help="Lint public-index required artifacts")
    lint.add_argument("--index", type=Path, default=DEFAULT_INDEX)
    lint.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    lint.add_argument("--fail-on-error", action="store_true")
    synth = sub.add_parser("synthetic-check", help="Run synthetic public-index freshness fixtures")
    synth.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    synth.add_argument("--fail-on-error", action="store_true")
    return parser.parse_args()


def write_tsv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def lint_index(index: Path, outdir: Path, fail_on_error: bool) -> int:
    text = index.read_text(errors="ignore") if index.exists() else ""
    rows: list[dict[str, object]] = []
    for target in REQUIRED_TARGETS:
        rows.append(
            {
                "required_target": target,
                "check": "linked_from_public_external_index",
                "status": "PASS" if target in text else "FAIL",
                "detail": str(index),
            }
        )
    n_fail = sum(1 for row in rows if row["status"] == "FAIL")
    write_tsv(outdir / "public_index_freshness_lint.tsv", rows, ["required_target", "check", "status", "detail"])
    summary = {
        "synthetic": False,
        "purpose": "V48 public external index freshness lint; navigation only; no biological claim",
        "n_required_targets": len(REQUIRED_TARGETS),
        "n_checks": len(rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
    }
    (outdir / "public_index_freshness_lint_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if n_fail == 0 or not fail_on_error else 2


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else ROOT / outdir
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    index = outdir / "synthetic_INDEX.md"
    index.write_text("\n".join(REQUIRED_TARGETS[:-1]) + "\n")
    lint_out = outdir / "synthetic_lint"
    lint_index(index, lint_out, fail_on_error=False)
    rows = list(csv.DictReader((lint_out / "public_index_freshness_lint.tsv").open(), delimiter="\t"))
    checks = {
        "linked_required_targets_pass": any(row["status"] == "PASS" for row in rows),
        "missing_required_target_fails": any(row["required_target"] == REQUIRED_TARGETS[-1] and row["status"] == "FAIL" for row in rows),
    }
    check_rows = [{"check": key, "status": "PASS" if value else "FAIL"} for key, value in checks.items()]
    write_tsv(outdir / "synthetic_public_index_freshness_checks.tsv", check_rows, ["check", "status"])
    summary = {
        "synthetic": True,
        "purpose": "V48 public-index freshness synthetic fixture; no biological claim",
        "n_checks": len(check_rows),
        "n_fail": sum(1 for row in check_rows if row["status"] != "PASS"),
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
    }
    (outdir / "synthetic_public_index_freshness_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["overall_status"] == "PASS" or not fail_on_error else 2


def main() -> int:
    args = parse_args()
    if args.command == "lint":
        return lint_index(args.index, args.outdir, args.fail_on_error)
    if args.command == "synthetic-check":
        return synthetic_check(args.outdir, args.fail_on_error)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
