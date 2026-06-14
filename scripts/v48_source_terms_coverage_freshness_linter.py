#!/usr/bin/env python3
"""Check that the V48 source-terms coverage report matches current records."""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXTERNAL_ROOT = "knowledge_external"
DEFAULT_COVERAGE = ROOT / "knowledge_external/catalogs/indexes/source_terms_coverage_v48.tsv"
DEFAULT_OUTDIR = ROOT / "analysis/v48_source_terms_coverage_freshness_linter"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    lint = sub.add_parser("lint", help="Lint source-terms coverage freshness")
    lint.add_argument("--root", type=Path, default=ROOT)
    lint.add_argument("--coverage", type=Path, default=DEFAULT_COVERAGE)
    lint.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    lint.add_argument("--fail-on-error", action="store_true")
    synth = sub.add_parser("synthetic-check", help="Run synthetic source-terms coverage freshness fixtures")
    synth.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    synth.add_argument("--fail-on-error", action="store_true")
    return parser.parse_args()


def record_paths(root: Path) -> list[Path]:
    paths: list[Path] = []
    for subdir in ["records", "catalogs/resources"]:
        base = root / EXTERNAL_ROOT / subdir
        if base.exists():
            paths.extend(path for path in base.rglob("*.json") if not path.name.endswith(".schema.json"))
    return sorted(paths)


def rel(root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


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


def current_rows(root: Path) -> dict[str, dict[str, str]]:
    rows: dict[str, dict[str, str]] = {}
    for path in record_paths(root):
        data = json.loads(path.read_text())
        terms = data.get("source_terms")
        terms_obj = terms if isinstance(terms, dict) else {}
        record_id = str(data.get("record_id", ""))
        rows[record_id] = {
            "path": rel(root, path),
            "source_terms_status": "present" if terms_obj else "missing_optional",
            "checked_date": str(terms_obj.get("checked_date", "")).strip(),
            "redistribution_allowed": str(terms_obj.get("redistribution_allowed", "")).strip(),
        }
    return rows


def lint_root(root: Path, coverage: Path, outdir: Path, fail_on_error: bool) -> int:
    root = root.resolve()
    coverage = coverage if coverage.is_absolute() else root / coverage
    outdir = outdir if outdir.is_absolute() else root / outdir
    current = current_rows(root)
    coverage_rows = read_tsv(coverage)
    coverage_by_id = {row.get("record_id", ""): row for row in coverage_rows}
    rows: list[dict[str, object]] = []
    for record_id, current_row in sorted(current.items()):
        coverage_row = coverage_by_id.get(record_id)
        rows.append(
            {
                "record_id": record_id,
                "check": "record_present_in_source_terms_coverage",
                "status": "PASS" if coverage_row else "FAIL",
                "detail": current_row["path"],
            }
        )
        if coverage_row:
            for field in ["source_terms_status", "checked_date", "redistribution_allowed"]:
                rows.append(
                    {
                        "record_id": record_id,
                        "check": f"coverage_{field}_matches_current_record",
                        "status": "PASS" if coverage_row.get(field, "") == current_row[field] else "FAIL",
                        "detail": f"current={current_row[field]} coverage={coverage_row.get(field, '')}",
                    }
                )
    stale_ids = sorted(set(coverage_by_id) - set(current))
    for record_id in stale_ids:
        rows.append(
            {
                "record_id": record_id,
                "check": "stale_coverage_record_removed_from_current_records",
                "status": "FAIL",
                "detail": "coverage row has no current external record",
            }
        )
    n_fail = sum(1 for row in rows if row["status"] == "FAIL")
    write_tsv(outdir / "source_terms_coverage_freshness_lint.tsv", rows, ["record_id", "check", "status", "detail"])
    summary = {
        "synthetic": False,
        "purpose": "V48 source-terms coverage freshness lint; provenance/navigation only; no biological claim",
        "n_current_records": len(current),
        "n_coverage_rows": len(coverage_rows),
        "n_checks": len(rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
    }
    (outdir / "source_terms_coverage_freshness_lint_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if n_fail == 0 or not fail_on_error else 2


def write_record(path: Path, record_id: str, terms: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data: dict[str, object] = {
        "record_id": record_id,
        "record_type": "external_claim",
        "claim": "Synthetic source-terms coverage freshness claim.",
        "epistemic_class": "external-unverifiable",
        "source": {"label": "Synthetic", "url": "https://example.invalid"},
        "date_accessed": "2026-06-14",
        "relationship_to_project_findings": "orthogonal",
        "not_project_grounded_marker": "NOT_PROJECT_GROUNDED",
        "why_unverifiable": "Synthetic fixture.",
    }
    if terms:
        data["source_terms"] = {"checked_date": "2026-06-14", "redistribution_allowed": "metadata_only"}
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def synthetic_root(outdir: Path) -> tuple[Path, Path]:
    root = outdir / "synthetic_root"
    if root.exists():
        shutil.rmtree(root)
    write_record(root / EXTERNAL_ROOT / "records/good.json", "SYNTH_TERMS_COVERAGE_GOOD", True)
    write_record(root / EXTERNAL_ROOT / "records/missing.json", "SYNTH_TERMS_COVERAGE_MISSING", False)
    write_record(root / EXTERNAL_ROOT / "records/changed.json", "SYNTH_TERMS_COVERAGE_CHANGED", True)
    coverage = root / EXTERNAL_ROOT / "catalogs/indexes/source_terms_coverage_v48.tsv"
    rows = [
        {"record_id": "SYNTH_TERMS_COVERAGE_GOOD", "source_terms_status": "present", "checked_date": "2026-06-14", "redistribution_allowed": "metadata_only"},
        {"record_id": "SYNTH_TERMS_COVERAGE_CHANGED", "source_terms_status": "missing_optional", "checked_date": "", "redistribution_allowed": ""},
        {"record_id": "SYNTH_TERMS_COVERAGE_STALE", "source_terms_status": "present", "checked_date": "2026-06-14", "redistribution_allowed": "metadata_only"},
    ]
    write_tsv(coverage, rows, ["record_id", "source_terms_status", "checked_date", "redistribution_allowed"])
    return root, coverage.relative_to(root)


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else ROOT / outdir
    outdir.mkdir(parents=True, exist_ok=True)
    root, coverage = synthetic_root(outdir)
    lint_out = outdir / "synthetic_lint"
    lint_root(root, root / coverage, lint_out, fail_on_error=False)
    rows = list(csv.DictReader((lint_out / "source_terms_coverage_freshness_lint.tsv").open(), delimiter="\t"))
    checks = {
        "good_record_passes": any(row["record_id"] == "SYNTH_TERMS_COVERAGE_GOOD" and row["status"] == "PASS" for row in rows),
        "missing_record_fails": any(row["record_id"] == "SYNTH_TERMS_COVERAGE_MISSING" and row["check"] == "record_present_in_source_terms_coverage" and row["status"] == "FAIL" for row in rows),
        "changed_terms_fail": any(row["record_id"] == "SYNTH_TERMS_COVERAGE_CHANGED" and row["status"] == "FAIL" for row in rows),
        "stale_coverage_fails": any(row["record_id"] == "SYNTH_TERMS_COVERAGE_STALE" and row["check"] == "stale_coverage_record_removed_from_current_records" and row["status"] == "FAIL" for row in rows),
    }
    check_rows = [{"check": key, "status": "PASS" if value else "FAIL"} for key, value in checks.items()]
    write_tsv(outdir / "synthetic_source_terms_coverage_freshness_checks.tsv", check_rows, ["check", "status"])
    summary = {
        "synthetic": True,
        "purpose": "V48 source-terms coverage freshness synthetic fixture; no biological claim",
        "n_checks": len(check_rows),
        "n_fail": sum(1 for row in check_rows if row["status"] != "PASS"),
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
    }
    (outdir / "synthetic_source_terms_coverage_freshness_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["overall_status"] == "PASS" or not fail_on_error else 2


def main() -> int:
    args = parse_args()
    if args.command == "lint":
        return lint_root(args.root, args.coverage, args.outdir, args.fail_on_error)
    if args.command == "synthetic-check":
        return synthetic_check(args.outdir, args.fail_on_error)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
