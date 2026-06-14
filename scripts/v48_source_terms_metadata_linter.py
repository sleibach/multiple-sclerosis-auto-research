#!/usr/bin/env python3
"""Report source license/terms metadata coverage on external records.

Missing terms metadata is a warning for existing V47 records, not a failure.
If a record provides source_terms, the object must be syntactically complete.
This is provenance/navigation infrastructure only.
"""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EXTERNAL_ROOT = "knowledge_external"
DEFAULT_OUTDIR = ROOT / "analysis/v48_source_terms_metadata_linter"
ALLOWED_REDISTRIBUTION = {"unknown", "yes", "no", "metadata_only"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    lint = sub.add_parser("lint", help="Lint source terms metadata coverage")
    lint.add_argument("--root", type=Path, default=ROOT)
    lint.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    lint.add_argument("--fail-on-error", action="store_true")
    synth = sub.add_parser("synthetic-check", help="Run synthetic source-terms fixtures")
    synth.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    synth.add_argument("--fail-on-error", action="store_true")
    return parser.parse_args()


def record_paths(root: Path) -> list[Path]:
    paths: list[Path] = []
    for base in [root / EXTERNAL_ROOT / "records", root / EXTERNAL_ROOT / "catalogs/resources"]:
        if base.exists():
            paths.extend(path for path in base.rglob("*.json") if not path.name.endswith(".schema.json"))
    return sorted(paths)


def rel(root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def write_tsv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def add(rows: list[dict[str, object]], path: str, record_id: str, check: str, status: str, detail: str) -> None:
    rows.append({"path": path, "record_id": record_id, "check": check, "status": status, "detail": detail})


def lint_record(root: Path, path: Path) -> list[dict[str, object]]:
    rel_path = rel(root, path)
    rows: list[dict[str, object]] = []
    try:
        data = json.loads(path.read_text())
    except Exception as exc:  # noqa: BLE001
        return [{"path": rel_path, "record_id": "", "check": "json_parse", "status": "FAIL", "detail": str(exc)}]
    if not isinstance(data, dict):
        return [{"path": rel_path, "record_id": "", "check": "json_object", "status": "FAIL", "detail": "not an object"}]
    record_id = str(data.get("record_id", ""))
    terms = data.get("source_terms")
    if terms is None:
        add(rows, rel_path, record_id, "source_terms_present", "WARN", "missing optional source_terms metadata")
        return rows
    if not isinstance(terms, dict):
        add(rows, rel_path, record_id, "source_terms_object", "FAIL", "source_terms is not an object")
        return rows
    label = str(terms.get("license_or_terms_label", "")).strip()
    terms_url = str(terms.get("terms_url", "")).strip()
    checked_date = str(terms.get("checked_date", "")).strip()
    reuse_notes = str(terms.get("reuse_notes", "")).strip()
    redistribution = str(terms.get("redistribution_allowed", "")).strip()
    add(rows, rel_path, record_id, "license_or_terms_label_present", "PASS" if label else "FAIL", label)
    add(rows, rel_path, record_id, "terms_url_http_or_empty", "PASS" if (not terms_url or terms_url.startswith(("https://", "http://"))) else "FAIL", terms_url)
    add(rows, rel_path, record_id, "checked_date_present", "PASS" if checked_date else "FAIL", checked_date)
    add(rows, rel_path, record_id, "reuse_notes_present", "PASS" if reuse_notes else "FAIL", reuse_notes[:120])
    add(rows, rel_path, record_id, "redistribution_value_allowed", "PASS" if redistribution in ALLOWED_REDISTRIBUTION else "FAIL", redistribution)
    return rows


def lint_root(root: Path, outdir: Path, fail_on_error: bool) -> int:
    root = root.resolve()
    outdir = outdir if outdir.is_absolute() else root / outdir
    rows: list[dict[str, object]] = []
    paths = record_paths(root)
    for path in paths:
        rows.extend(lint_record(root, path))
    n_fail = sum(1 for row in rows if row["status"] == "FAIL")
    n_warn = sum(1 for row in rows if row["status"] == "WARN")
    n_with_terms = sum(1 for path in paths if isinstance(json.loads(path.read_text()).get("source_terms"), dict))
    write_tsv(outdir / "source_terms_metadata_lint.tsv", rows, ["path", "record_id", "check", "status", "detail"])
    summary = {
        "synthetic": False,
        "purpose": "V48 source license/terms metadata lint; coverage report only unless malformed metadata is present",
        "n_records": len(paths),
        "n_records_with_source_terms": n_with_terms,
        "n_checks": len(rows),
        "n_warn": n_warn,
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
        "lint": rel(root, outdir / "source_terms_metadata_lint.tsv") if root == ROOT else str(outdir / "source_terms_metadata_lint.tsv"),
    }
    (outdir / "source_terms_metadata_lint_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
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
        "claim": "Synthetic source terms claim.",
        "epistemic_class": "external-unverifiable",
        "source": {"label": "Synthetic", "url": "https://example.invalid"},
        "date_accessed": "2026-06-14",
        "relationship_to_project_findings": "orthogonal",
        "not_project_grounded_marker": "NOT_PROJECT_GROUNDED",
        "why_unverifiable": "Synthetic fixture.",
    }
    write_record(base / "missing_terms.json", **common, record_id="SYNTH_MISSING_TERMS")
    write_record(
        base / "good_terms.json",
        **common,
        record_id="SYNTH_GOOD_TERMS",
        source_terms={
            "license_or_terms_label": "Synthetic permissive",
            "terms_url": "https://example.invalid/terms",
            "checked_date": "2026-06-14",
            "reuse_notes": "Synthetic metadata only.",
            "redistribution_allowed": "metadata_only",
        },
    )
    write_record(
        base / "bad_terms.json",
        **common,
        record_id="SYNTH_BAD_TERMS",
        source_terms={
            "license_or_terms_label": "",
            "terms_url": "example.invalid/terms",
            "checked_date": "",
            "reuse_notes": "",
            "redistribution_allowed": "maybe",
        },
    )
    return root


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else ROOT / outdir
    outdir.mkdir(parents=True, exist_ok=True)
    root = synthetic_root(outdir)
    lint_out = outdir / "synthetic_lint"
    lint_root(root, lint_out, fail_on_error=False)
    rows = list(csv.DictReader((lint_out / "source_terms_metadata_lint.tsv").open(), delimiter="\t"))
    checks = {
        "missing_terms_warns": any(row["record_id"] == "SYNTH_MISSING_TERMS" and row["status"] == "WARN" for row in rows),
        "good_terms_no_fail": not any(row["record_id"] == "SYNTH_GOOD_TERMS" and row["status"] == "FAIL" for row in rows),
        "bad_terms_fail": any(row["record_id"] == "SYNTH_BAD_TERMS" and row["status"] == "FAIL" for row in rows),
    }
    check_rows = [{"check": key, "status": "PASS" if value else "FAIL"} for key, value in checks.items()]
    write_tsv(outdir / "synthetic_source_terms_checks.tsv", check_rows, ["check", "status"])
    summary = {
        "synthetic": True,
        "purpose": "V48 source license/terms metadata synthetic fixture; no biological claim",
        "n_checks": len(check_rows),
        "n_fail": sum(1 for row in check_rows if row["status"] != "PASS"),
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
    }
    (outdir / "synthetic_source_terms_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
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
