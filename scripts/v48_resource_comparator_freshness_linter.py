#!/usr/bin/env python3
"""Check that the V48 resource comparator matrix covers all resource records."""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RESOURCE_DIR = ROOT / "knowledge_external/catalogs/resources"
DEFAULT_MATRIX = ROOT / "knowledge_external/catalogs/indexes/external_resource_comparator_matrix_v48.tsv"
DEFAULT_OUTDIR = ROOT / "analysis/v48_resource_comparator_freshness_linter"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    lint = sub.add_parser("lint", help="Lint comparator matrix freshness")
    lint.add_argument("--resource-dir", type=Path, default=DEFAULT_RESOURCE_DIR)
    lint.add_argument("--matrix", type=Path, default=DEFAULT_MATRIX)
    lint.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    lint.add_argument("--fail-on-error", action="store_true")
    synth = sub.add_parser("synthetic-check", help="Run synthetic freshness fixture")
    synth.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    synth.add_argument("--fail-on-error", action="store_true")
    return parser.parse_args()


def write_tsv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def resource_ids(resource_dir: Path) -> set[str]:
    ids: set[str] = set()
    for path in sorted(resource_dir.glob("*.json")):
        if path.name.endswith(".schema.json"):
            continue
        data = json.loads(path.read_text())
        if isinstance(data, dict):
            ids.add(str(data.get("record_id", "")))
    return ids


def lint_freshness(resource_dir: Path, matrix: Path, outdir: Path, fail_on_error: bool) -> int:
    outdir.mkdir(parents=True, exist_ok=True)
    resources = resource_ids(resource_dir)
    matrix_rows = read_tsv(matrix) if matrix.exists() else []
    matrix_ids = {row.get("resource_id", "") for row in matrix_rows}
    lint_rows: list[dict[str, object]] = []
    for record_id in sorted(resources):
        lint_rows.append(
            {
                "record_id": record_id,
                "check": "resource_has_matrix_row",
                "status": "PASS" if record_id in matrix_ids else "FAIL",
                "detail": "",
            }
        )
    for record_id in sorted(matrix_ids - resources):
        lint_rows.append(
            {
                "record_id": record_id,
                "check": "matrix_row_has_resource_record",
                "status": "FAIL",
                "detail": "stale matrix row",
            }
        )
    n_fail = sum(1 for row in lint_rows if row["status"] != "PASS")
    write_tsv(outdir / "resource_comparator_freshness_lint.tsv", lint_rows, ["record_id", "check", "status", "detail"])
    summary = {
        "synthetic": False,
        "purpose": "V48 resource comparator freshness lint; navigation only",
        "n_resource_records": len(resources),
        "n_matrix_rows": len(matrix_ids),
        "n_checks": len(lint_rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
        "lint": str(outdir / "resource_comparator_freshness_lint.tsv"),
    }
    (outdir / "resource_comparator_freshness_lint_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["overall_status"] == "PASS" or not fail_on_error else 2


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else ROOT / outdir
    if outdir.exists():
        shutil.rmtree(outdir)
    resource_dir = outdir / "resources"
    resource_dir.mkdir(parents=True)
    (resource_dir / "a.json").write_text(json.dumps({"record_id": "A"}) + "\n")
    (resource_dir / "b.json").write_text(json.dumps({"record_id": "B"}) + "\n")
    matrix = outdir / "matrix.tsv"
    write_tsv(matrix, [{"resource_id": "A"}, {"resource_id": "STALE"}], ["resource_id"])
    lint_out = outdir / "synthetic_lint"
    lint_freshness(resource_dir, matrix, lint_out, fail_on_error=False)
    rows = read_tsv(lint_out / "resource_comparator_freshness_lint.tsv")
    checks = {
        "covered_resource_passes": any(row["record_id"] == "A" and row["status"] == "PASS" for row in rows),
        "missing_resource_fails": any(row["record_id"] == "B" and row["status"] == "FAIL" for row in rows),
        "stale_matrix_row_fails": any(row["record_id"] == "STALE" and row["status"] == "FAIL" for row in rows),
    }
    check_rows = [{"check": key, "status": "PASS" if value else "FAIL"} for key, value in checks.items()]
    write_tsv(outdir / "synthetic_resource_comparator_freshness_checks.tsv", check_rows, ["check", "status"])
    summary = {
        "synthetic": True,
        "purpose": "V48 resource comparator freshness synthetic fixture; navigation only",
        "n_checks": len(check_rows),
        "n_fail": sum(1 for row in check_rows if row["status"] != "PASS"),
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
    }
    (outdir / "synthetic_resource_comparator_freshness_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["overall_status"] == "PASS" or not fail_on_error else 2


def main() -> int:
    args = parse_args()
    if args.command == "lint":
        return lint_freshness(args.resource_dir, args.matrix, args.outdir, args.fail_on_error)
    if args.command == "synthetic-check":
        return synthetic_check(args.outdir, args.fail_on_error)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
