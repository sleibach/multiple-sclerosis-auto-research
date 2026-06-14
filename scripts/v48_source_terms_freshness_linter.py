#!/usr/bin/env python3
"""Lint source_terms checked_date freshness for external records.

If a record has source_terms metadata, the checked_date must parse and must not
predate the record date_accessed. Records without source_terms are warnings,
not failures, because source_terms remains optional coverage metadata.
"""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EXTERNAL_ROOT = "knowledge_external"
DEFAULT_OUTDIR = ROOT / "analysis/v48_source_terms_freshness_linter"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    lint = sub.add_parser("lint", help="Lint source_terms checked_date freshness")
    lint.add_argument("--root", type=Path, default=ROOT)
    lint.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    lint.add_argument("--fail-on-error", action="store_true")
    synth = sub.add_parser("synthetic-check", help="Run synthetic source_terms freshness fixtures")
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


def parse_date(value: object) -> date | None:
    text = str(value or "").strip()
    if not text:
        return None
    try:
        return date.fromisoformat(text)
    except ValueError:
        return None


def add(rows: list[dict[str, object]], path: str, record_id: str, check: str, status: str, detail: str) -> None:
    rows.append({"path": path, "record_id": record_id, "check": check, "status": status, "detail": detail})


def lint_record(root: Path, path: Path) -> list[dict[str, object]]:
    rel_path = rel(root, path)
    try:
        data = json.loads(path.read_text())
    except Exception as exc:  # noqa: BLE001
        return [{"path": rel_path, "record_id": "", "check": "json_parse", "status": "FAIL", "detail": str(exc)}]
    record_id = str(data.get("record_id", ""))
    rows: list[dict[str, object]] = []
    terms = data.get("source_terms")
    if not isinstance(terms, dict):
        add(rows, rel_path, record_id, "source_terms_present_for_freshness", "WARN", "missing optional source_terms metadata")
        return rows
    accessed = parse_date(data.get("date_accessed"))
    checked = parse_date(terms.get("checked_date"))
    add(rows, rel_path, record_id, "date_accessed_parseable", "PASS" if accessed else "FAIL", str(data.get("date_accessed", "")))
    add(rows, rel_path, record_id, "source_terms_checked_date_parseable", "PASS" if checked else "FAIL", str(terms.get("checked_date", "")))
    if accessed and checked:
        add(
            rows,
            rel_path,
            record_id,
            "source_terms_checked_not_older_than_accessed",
            "PASS" if checked >= accessed else "FAIL",
            f"checked={checked.isoformat()} accessed={accessed.isoformat()}",
        )
    return rows


def write_tsv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def lint_root(root: Path, outdir: Path, fail_on_error: bool) -> int:
    root = root.resolve()
    outdir = outdir if outdir.is_absolute() else root / outdir
    paths = record_paths(root)
    rows: list[dict[str, object]] = []
    for path in paths:
        rows.extend(lint_record(root, path))
    n_fail = sum(1 for row in rows if row["status"] == "FAIL")
    n_warn = sum(1 for row in rows if row["status"] == "WARN")
    write_tsv(outdir / "source_terms_freshness_lint.tsv", rows, ["path", "record_id", "check", "status", "detail"])
    summary = {
        "synthetic": False,
        "purpose": "V48 source_terms freshness lint; provenance/navigation only; no biological claim",
        "n_records": len(paths),
        "n_checks": len(rows),
        "n_warn": n_warn,
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
        "lint": rel(root, outdir / "source_terms_freshness_lint.tsv") if root == ROOT else str(outdir / "source_terms_freshness_lint.tsv"),
    }
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "source_terms_freshness_lint_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["overall_status"] == "PASS" or not fail_on_error else 2


def write_record(path: Path, **kwargs: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(kwargs, indent=2, sort_keys=True) + "\n")


def synthetic_root(outdir: Path) -> Path:
    root = outdir / "synthetic_root"
    if root.exists():
        shutil.rmtree(root)
    base = root / EXTERNAL_ROOT / "records"
    common = {
        "claim": "Synthetic source_terms freshness claim.",
        "epistemic_class": "external-unverifiable",
        "source": {"label": "Synthetic", "url": "https://example.invalid"},
        "relationship_to_project_findings": "orthogonal",
        "not_project_grounded_marker": "NOT_PROJECT_GROUNDED",
        "why_unverifiable": "Synthetic fixture.",
    }
    write_record(base / "good.json", **common, record_id="SYNTH_FRESH_GOOD", date_accessed="2026-06-13", source_terms={"checked_date": "2026-06-14"})
    write_record(base / "stale.json", **common, record_id="SYNTH_FRESH_STALE", date_accessed="2026-06-14", source_terms={"checked_date": "2026-06-13"})
    write_record(base / "bad_date.json", **common, record_id="SYNTH_FRESH_BAD_DATE", date_accessed="not-a-date", source_terms={"checked_date": "also-bad"})
    write_record(base / "missing.json", **common, record_id="SYNTH_FRESH_MISSING", date_accessed="2026-06-14")
    return root


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else ROOT / outdir
    outdir.mkdir(parents=True, exist_ok=True)
    root = synthetic_root(outdir)
    lint_out = outdir / "synthetic_lint"
    lint_root(root, lint_out, fail_on_error=False)
    rows = list(csv.DictReader((lint_out / "source_terms_freshness_lint.tsv").open(), delimiter="\t"))
    checks = {
        "good_passes": any(row["record_id"] == "SYNTH_FRESH_GOOD" and row["check"] == "source_terms_checked_not_older_than_accessed" and row["status"] == "PASS" for row in rows),
        "stale_fails": any(row["record_id"] == "SYNTH_FRESH_STALE" and row["check"] == "source_terms_checked_not_older_than_accessed" and row["status"] == "FAIL" for row in rows),
        "bad_dates_fail": any(row["record_id"] == "SYNTH_FRESH_BAD_DATE" and row["status"] == "FAIL" for row in rows),
        "missing_warns": any(row["record_id"] == "SYNTH_FRESH_MISSING" and row["status"] == "WARN" for row in rows),
    }
    check_rows = [{"check": key, "status": "PASS" if value else "FAIL"} for key, value in checks.items()]
    write_tsv(outdir / "synthetic_source_terms_freshness_checks.tsv", check_rows, ["check", "status"])
    summary = {
        "synthetic": True,
        "purpose": "V48 source_terms freshness synthetic fixture; no biological claim",
        "n_checks": len(check_rows),
        "n_fail": sum(1 for row in check_rows if row["status"] != "PASS"),
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
    }
    (outdir / "synthetic_source_terms_freshness_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["overall_status"] == "PASS" or not fail_on_error else 2


def main() -> int:
    args = parse_args()
    if args.command == "lint":
        return lint_root(args.root, args.outdir, args.fail_on_error)
    if args.command == "synthetic-check":
        return synthetic_check(args.outdir, args.fail_on_error)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
