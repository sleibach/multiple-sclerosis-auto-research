#!/usr/bin/env python3
"""Audit committed V52 route-classifier outputs for schema drift.

This is an operational guard. It does not inspect raw package data and does not
make biological claims.
"""

from __future__ import annotations

import argparse
import csv
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "analysis/v52_route_output_schema_audit/route_output_schema_audit.tsv"
DEFAULT_SCAN_ROOT = ROOT / "analysis"
EXPECTED_COLUMNS = [
    "package_id",
    "expected_route",
    "assigned_route",
    "status",
    "matched_required_count",
    "required_count",
    "missing_required_fields",
    "candidate_full_routes",
    "expected_matches_assigned",
]


def scan_tsvs(scan_root: Path, all_files: bool) -> list[Path]:
    if all_files:
        return sorted(path for path in scan_root.rglob("*.tsv") if path.is_file())
    rel_root = scan_root.relative_to(ROOT)
    output = subprocess.check_output(["git", "ls-files", str(rel_root)], cwd=ROOT, text=True)
    return sorted(ROOT / line for line in output.splitlines() if line.endswith(".tsv"))


def read_header(path: Path) -> list[str]:
    with path.open(newline="") as handle:
        reader = csv.reader(handle, delimiter="\t")
        return next(reader, [])


def count_data_rows(path: Path) -> int:
    with path.open(newline="") as handle:
        reader = csv.reader(handle, delimiter="\t")
        next(reader, None)
        return sum(1 for _ in reader)


def audit_outputs(scan_root: Path, all_files: bool) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path in scan_tsvs(scan_root, all_files):
        header = read_header(path)
        if "assigned_route" not in header:
            continue
        status = "PASS" if header == EXPECTED_COLUMNS else "FAIL"
        rows.append(
            {
                "path": str(path.relative_to(ROOT)),
                "status": status,
                "observed_column_count": str(len(header)),
                "expected_column_count": str(len(EXPECTED_COLUMNS)),
                "observed_columns": ";".join(header),
                "expected_columns": ";".join(EXPECTED_COLUMNS),
                "data_rows": str(count_data_rows(path)),
            }
        )
    return rows


def write_rows(rows: list[dict[str, str]], out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "path",
        "status",
        "observed_column_count",
        "expected_column_count",
        "observed_columns",
        "expected_columns",
        "data_rows",
    ]
    with out.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scan-root", type=Path, default=DEFAULT_SCAN_ROOT)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--all-files", action="store_true")
    parser.add_argument("--fail-on-error", action="store_true")
    args = parser.parse_args()

    scan_root = args.scan_root if args.scan_root.is_absolute() else ROOT / args.scan_root
    out = args.out if args.out.is_absolute() else ROOT / args.out
    rows = audit_outputs(scan_root.resolve(), args.all_files)
    write_rows(rows, out)
    failures = [row for row in rows if row["status"] != "PASS"]
    print({"outputs": len(rows), "failures": len(failures), "out": str(out)})
    if (not rows or failures) and args.fail_on_error:
        raise SystemExit({"outputs": len(rows), "failures": failures})


if __name__ == "__main__":
    main()
