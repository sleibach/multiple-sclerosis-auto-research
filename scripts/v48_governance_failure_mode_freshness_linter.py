#!/usr/bin/env python3
"""Check that the V48 governance failure-mode matrix matches navigation."""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_NAV = ROOT / "knowledge_external/catalogs/indexes/v48_governance_navigation.tsv"
DEFAULT_MATRIX = ROOT / "knowledge_external/catalogs/indexes/governance_failure_mode_matrix_v48.tsv"
DEFAULT_SUMMARY = ROOT / "knowledge_external/catalogs/indexes/governance_failure_mode_matrix_v48_summary.json"
DEFAULT_OUTDIR = ROOT / "analysis/v48_governance_failure_mode_freshness_linter"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    lint = sub.add_parser("lint", help="Lint governance failure-mode matrix freshness")
    lint.add_argument("--navigation", type=Path, default=DEFAULT_NAV)
    lint.add_argument("--matrix", type=Path, default=DEFAULT_MATRIX)
    lint.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
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


def read_json(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text())
    return data if isinstance(data, dict) else {}


def write_tsv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def key(row: dict[str, str]) -> str:
    return f"{row.get('artifact', '')}||{row.get('path', '')}"


def add(rows: list[dict[str, object]], row_key: str, check: str, status: str, detail: str) -> None:
    rows.append({"row_key": row_key, "check": check, "status": status, "detail": detail})


def lint_matrix(navigation: Path, matrix: Path, summary_path: Path, outdir: Path, fail_on_error: bool) -> int:
    nav_rows = {key(row): row for row in read_tsv(navigation)}
    matrix_rows = {key(row): row for row in read_tsv(matrix)}
    rows: list[dict[str, object]] = []
    for row_key, nav_row in sorted(nav_rows.items()):
        matrix_row = matrix_rows.get(row_key)
        add(rows, row_key, "present_in_matrix", "PASS" if matrix_row else "FAIL", str(matrix))
        if not matrix_row:
            continue
        for field in ["boundary", "purpose", "overall_status"]:
            matrix_field = "control_status" if field == "overall_status" else field
            add(
                rows,
                row_key,
                f"field_matches.{field}",
                "PASS" if nav_row.get(field, "") == matrix_row.get(matrix_field, "") else "FAIL",
                f"navigation={nav_row.get(field, '')} matrix={matrix_row.get(matrix_field, '')}",
            )
        add(
            rows,
            row_key,
            "failure_mode_mapped",
            "PASS" if matrix_row.get("failure_mode_prevented", "") and not matrix_row.get("failure_mode_prevented", "").startswith("manual review needed") else "FAIL",
            matrix_row.get("failure_mode_prevented", ""),
        )
    for row_key in sorted(set(matrix_rows) - set(nav_rows)):
        add(rows, row_key, "no_extra_matrix_row", "FAIL", "matrix row is not present in current governance navigation")
    summary = read_json(summary_path)
    add(
        rows,
        "summary",
        "summary_control_count_matches_matrix",
        "PASS" if int(summary.get("n_controls", -1)) == len(matrix_rows) else "FAIL",
        f"summary={summary.get('n_controls', '')} matrix={len(matrix_rows)}",
    )
    n_fail = sum(1 for row in rows if row["status"] != "PASS")
    outdir.mkdir(parents=True, exist_ok=True)
    write_tsv(outdir / "governance_failure_mode_freshness_lint.tsv", rows, ["row_key", "check", "status", "detail"])
    result = {
        "synthetic": False,
        "purpose": "V48 governance failure-mode matrix freshness lint; governance/navigation only; no biological claim",
        "n_navigation_rows": len(nav_rows),
        "n_matrix_rows": len(matrix_rows),
        "n_checks": len(rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
    }
    (outdir / "governance_failure_mode_freshness_lint_summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if n_fail == 0 or not fail_on_error else 2


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else ROOT / outdir
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    nav = outdir / "synthetic_nav.tsv"
    matrix = outdir / "synthetic_matrix.tsv"
    summary = outdir / "synthetic_summary.json"
    write_tsv(
        nav,
        [
            {"artifact": "A", "path": "scripts/a.py", "boundary": "schema control", "purpose": "schema", "overall_status": "PASS"},
            {"artifact": "B", "path": "scripts/b.py", "boundary": "navigation control", "purpose": "nav", "overall_status": "PASS"},
        ],
        ["artifact", "path", "boundary", "purpose", "overall_status"],
    )
    write_tsv(
        matrix,
        [
            {"artifact": "A", "path": "scripts/a.py", "boundary": "stale", "purpose": "schema", "failure_mode_prevented": "manual review needed", "control_status": "PASS", "summary": "a.json"},
            {"artifact": "EXTRA", "path": "scripts/extra.py", "boundary": "schema control", "purpose": "extra", "failure_mode_prevented": "ok", "control_status": "PASS", "summary": "extra.json"},
        ],
        ["artifact", "path", "boundary", "purpose", "failure_mode_prevented", "control_status", "summary"],
    )
    summary.write_text(json.dumps({"n_controls": 99}) + "\n")
    lint_out = outdir / "synthetic_lint"
    lint_matrix(nav, matrix, summary, lint_out, fail_on_error=False)
    rows = read_tsv(lint_out / "governance_failure_mode_freshness_lint.tsv")
    checks = {
        "missing_matrix_row_fails": any(row["row_key"] == "B||scripts/b.py" and row["check"] == "present_in_matrix" and row["status"] == "FAIL" for row in rows),
        "stale_boundary_fails": any(row["row_key"] == "A||scripts/a.py" and row["check"] == "field_matches.boundary" and row["status"] == "FAIL" for row in rows),
        "unmapped_failure_mode_fails": any(row["row_key"] == "A||scripts/a.py" and row["check"] == "failure_mode_mapped" and row["status"] == "FAIL" for row in rows),
        "extra_row_fails": any(row["row_key"] == "EXTRA||scripts/extra.py" and row["check"] == "no_extra_matrix_row" and row["status"] == "FAIL" for row in rows),
        "bad_summary_count_fails": any(row["row_key"] == "summary" and row["check"] == "summary_control_count_matches_matrix" and row["status"] == "FAIL" for row in rows),
    }
    check_rows = [{"check": check, "status": "PASS" if ok else "FAIL"} for check, ok in checks.items()]
    write_tsv(outdir / "synthetic_governance_failure_mode_freshness_checks.tsv", check_rows, ["check", "status"])
    synth_summary = {
        "synthetic": True,
        "purpose": "V48 governance failure-mode freshness synthetic fixture; no biological claim",
        "n_checks": len(check_rows),
        "n_fail": sum(1 for row in check_rows if row["status"] != "PASS"),
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
    }
    (outdir / "synthetic_governance_failure_mode_freshness_summary.json").write_text(json.dumps(synth_summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(synth_summary, indent=2, sort_keys=True))
    return 0 if synth_summary["overall_status"] == "PASS" or not fail_on_error else 2


def main() -> int:
    args = parse_args()
    if args.command == "lint":
        return lint_matrix(args.navigation, args.matrix, args.summary, args.outdir, args.fail_on_error)
    if args.command == "synthetic-check":
        return synthetic_check(args.outdir, args.fail_on_error)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
