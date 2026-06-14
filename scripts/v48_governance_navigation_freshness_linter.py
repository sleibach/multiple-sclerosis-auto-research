#!/usr/bin/env python3
"""Check that V48 governance navigation covers the current preflight suite."""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PREFLIGHT = ROOT / "analysis/v48_governance_preflight/v48_governance_preflight_plan.tsv"
DEFAULT_NAV = ROOT / "knowledge_external/catalogs/indexes/v48_governance_navigation.tsv"
DEFAULT_SUMMARY = ROOT / "knowledge_external/catalogs/indexes/v48_governance_navigation_summary.json"
DEFAULT_OUTDIR = ROOT / "analysis/v48_governance_navigation_freshness_linter"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    lint = sub.add_parser("lint", help="Lint governance-navigation freshness")
    lint.add_argument("--preflight", type=Path, default=DEFAULT_PREFLIGHT)
    lint.add_argument("--navigation", type=Path, default=DEFAULT_NAV)
    lint.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    lint.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    lint.add_argument("--fail-on-error", action="store_true")
    synth = sub.add_parser("synthetic-check", help="Run synthetic governance-navigation freshness fixtures")
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


def preflight_script_paths(preflight_rows: list[dict[str, str]]) -> set[str]:
    paths: set[str] = set()
    for row in preflight_rows:
        command = row.get("command", "")
        first = command.split(" ", 1)[0].strip()
        if first:
            paths.add(first)
    return paths


def lint_paths(preflight: Path, navigation: Path, summary_path: Path, outdir: Path, fail_on_error: bool) -> int:
    preflight_rows = read_tsv(preflight)
    nav_rows = read_tsv(navigation)
    summary = read_json(summary_path)
    preflight_paths = preflight_script_paths(preflight_rows)
    nav_paths = {row.get("path", "") for row in nav_rows}
    rows: list[dict[str, object]] = []
    missing = sorted(preflight_paths - nav_paths)
    extra_scripts = sorted(path for path in nav_paths - preflight_paths if path.startswith("scripts/"))
    rows.append(
        {
            "check": "all_preflight_scripts_in_navigation",
            "status": "PASS" if not missing else "FAIL",
            "detail": ";".join(missing) if missing else "all covered",
        }
    )
    rows.append(
        {
            "check": "navigation_summary_artifact_count_matches_rows",
            "status": "PASS" if int(summary.get("n_artifacts", -1)) == len(nav_rows) else "FAIL",
            "detail": f"summary={summary.get('n_artifacts', '')} rows={len(nav_rows)}",
        }
    )
    rows.append(
        {
            "check": "navigation_has_no_stale_script_rows",
            "status": "PASS" if not extra_scripts else "FAIL",
            "detail": ";".join(extra_scripts) if extra_scripts else "no stale script rows",
        }
    )
    n_fail = sum(1 for row in rows if row["status"] == "FAIL")
    write_tsv(outdir / "governance_navigation_freshness_lint.tsv", rows, ["check", "status", "detail"])
    result = {
        "synthetic": False,
        "purpose": "V48 governance-navigation freshness lint; navigation control only; no biological claim",
        "n_preflight_checks": len(preflight_rows),
        "n_navigation_rows": len(nav_rows),
        "n_checks": len(rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
    }
    (outdir / "governance_navigation_freshness_lint_summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if n_fail == 0 or not fail_on_error else 2


def synthetic_root(outdir: Path) -> tuple[Path, Path, Path]:
    root = outdir / "synthetic_root"
    if root.exists():
        shutil.rmtree(root)
    preflight = root / "analysis/v48_governance_preflight/v48_governance_preflight.tsv"
    nav = root / "knowledge_external/catalogs/indexes/v48_governance_navigation.tsv"
    summary = root / "knowledge_external/catalogs/indexes/v48_governance_navigation_summary.json"
    write_tsv(
        preflight,
        [
            {"check": "a", "command": "scripts/a.py lint"},
            {"check": "b", "command": "scripts/b.py lint"},
        ],
        ["check", "command"],
    )
    write_tsv(
        nav,
        [
            {"artifact": "A", "path": "scripts/a.py"},
            {"artifact": "Stale", "path": "scripts/stale.py"},
        ],
        ["artifact", "path"],
    )
    summary.parent.mkdir(parents=True, exist_ok=True)
    summary.write_text(json.dumps({"n_artifacts": 3}) + "\n")
    return preflight, nav, summary


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else ROOT / outdir
    outdir.mkdir(parents=True, exist_ok=True)
    preflight, nav, summary = synthetic_root(outdir)
    lint_out = outdir / "synthetic_lint"
    lint_paths(preflight, nav, summary, lint_out, fail_on_error=False)
    rows = list(csv.DictReader((lint_out / "governance_navigation_freshness_lint.tsv").open(), delimiter="\t"))
    checks = {
        "missing_preflight_script_fails": any(row["check"] == "all_preflight_scripts_in_navigation" and row["status"] == "FAIL" for row in rows),
        "bad_count_fails": any(row["check"] == "navigation_summary_artifact_count_matches_rows" and row["status"] == "FAIL" for row in rows),
        "stale_script_fails": any(row["check"] == "navigation_has_no_stale_script_rows" and row["status"] == "FAIL" for row in rows),
    }
    check_rows = [{"check": key, "status": "PASS" if value else "FAIL"} for key, value in checks.items()]
    write_tsv(outdir / "synthetic_governance_navigation_freshness_checks.tsv", check_rows, ["check", "status"])
    result = {
        "synthetic": True,
        "purpose": "V48 governance-navigation freshness synthetic fixture; no biological claim",
        "n_checks": len(check_rows),
        "n_fail": sum(1 for row in check_rows if row["status"] != "PASS"),
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
    }
    (outdir / "synthetic_governance_navigation_freshness_summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["overall_status"] == "PASS" or not fail_on_error else 2


def main() -> int:
    args = parse_args()
    if args.command == "lint":
        return lint_paths(args.preflight, args.navigation, args.summary, args.outdir, args.fail_on_error)
    if args.command == "synthetic-check":
        return synthetic_check(args.outdir, args.fail_on_error)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
