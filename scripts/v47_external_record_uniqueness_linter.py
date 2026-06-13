#!/usr/bin/env python3
"""Lint V47 external records for uniqueness of identifiers and source locators.

Duplicate record IDs are hard failures. Duplicate source locators are review
failures because they can indicate accidental copy/paste records. This linter
does not validate source content or external claims.
"""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from collections import defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v47_external_record_uniqueness_linter"
EXTERNAL_ROOT = "knowledge_external"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    lint = sub.add_parser("lint", help="Lint real external records for duplicate IDs/source locators")
    lint.add_argument("--root", type=Path, default=ROOT)
    lint.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    lint.add_argument("--fail-on-error", action="store_true")
    synth = sub.add_parser("synthetic-check", help="Run synthetic duplicate-record fixtures")
    synth.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    synth.add_argument("--fail-on-error", action="store_true")
    return parser.parse_args()


def rel(root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def write_tsv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def record_paths(root: Path) -> list[Path]:
    paths: list[Path] = []
    for directory in [root / EXTERNAL_ROOT / "records", root / EXTERNAL_ROOT / "catalogs/resources"]:
        if directory.exists():
            paths.extend(path for path in directory.rglob("*.json") if not path.name.endswith(".schema.json"))
    return sorted(paths)


def load_record(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text())
    if not isinstance(data, dict):
        raise ValueError(f"External record is not a JSON object: {path}")
    return data


def source_locator(data: dict[str, Any]) -> str:
    source = data.get("source")
    if not isinstance(source, dict):
        return ""
    for field in ["url", "doi", "pmid", "citation"]:
        value = str(source.get(field, "")).strip()
        if value:
            return f"{field}:{value.lower()}"
    return ""


def lint_root(root: Path, outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else root / outdir
    outdir.mkdir(parents=True, exist_ok=True)
    paths = record_paths(root)
    records: list[dict[str, object]] = []
    by_id: dict[str, list[str]] = defaultdict(list)
    by_locator: dict[str, list[str]] = defaultdict(list)
    for path in paths:
        data = load_record(path)
        record_id = str(data.get("record_id", "")).strip()
        locator = source_locator(data)
        rel_path = rel(root, path)
        records.append({"path": rel_path, "record_id": record_id, "source_locator": locator})
        by_id[record_id].append(rel_path)
        if locator:
            by_locator[locator].append(rel_path)

    rows: list[dict[str, object]] = []
    for record in records:
        duplicate_id_paths = by_id[str(record["record_id"])]
        duplicate_locator_paths = by_locator.get(str(record["source_locator"]), [])
        rows.append(
            {
                "path": record["path"],
                "record_id": record["record_id"],
                "check": "record_id_unique",
                "status": "PASS" if len(duplicate_id_paths) == 1 else "FAIL",
                "detail": ";".join(duplicate_id_paths) if len(duplicate_id_paths) > 1 else "-",
            }
        )
        rows.append(
            {
                "path": record["path"],
                "record_id": record["record_id"],
                "check": "source_locator_unique",
                "status": "PASS" if len(duplicate_locator_paths) <= 1 else "FAIL",
                "detail": ";".join(duplicate_locator_paths) if len(duplicate_locator_paths) > 1 else "-",
            }
        )
    n_fail = sum(1 for row in rows if row["status"] != "PASS")
    write_tsv(outdir / "external_record_uniqueness_lint.tsv", rows, ["path", "record_id", "check", "status", "detail"])
    summary = {
        "synthetic": False,
        "purpose": "V47 external-record uniqueness lint; no biological claim",
        "n_records": len(paths),
        "n_checks": len(rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
        "lint": rel(root, outdir / "external_record_uniqueness_lint.tsv") if root == ROOT else str(outdir / "external_record_uniqueness_lint.tsv"),
    }
    (outdir / "external_record_uniqueness_lint_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["overall_status"] == "PASS" or not fail_on_error else 2


def write_record(path: Path, **kwargs: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(kwargs, indent=2, sort_keys=True) + "\n")


def build_synthetic_root(outdir: Path) -> Path:
    root = outdir / "synthetic_root"
    if root.exists():
        shutil.rmtree(root)
    records = root / EXTERNAL_ROOT / "records"
    records.mkdir(parents=True, exist_ok=True)
    base = {
        "claim": "Synthetic uniqueness record.",
        "epistemic_class": "external-unverifiable",
        "date_accessed": "2026-06-13",
        "relationship_to_project_findings": "orthogonal",
        "not_project_grounded_marker": "NOT_PROJECT_GROUNDED",
        "why_unverifiable": "Synthetic fixture.",
        "future_grounding_route": "Synthetic route.",
    }
    write_record(records / "unique_a.json", **base, record_id="SYNTH_UNIQUE_A", source={"label": "A", "url": "https://example.invalid/a"})
    write_record(records / "unique_b.json", **base, record_id="SYNTH_UNIQUE_B", source={"label": "B", "url": "https://example.invalid/b"})
    write_record(records / "duplicate_id_1.json", **base, record_id="SYNTH_DUP_ID", source={"label": "C", "url": "https://example.invalid/c"})
    write_record(records / "duplicate_id_2.json", **base, record_id="SYNTH_DUP_ID", source={"label": "D", "url": "https://example.invalid/d"})
    write_record(records / "duplicate_source_1.json", **base, record_id="SYNTH_DUP_SOURCE_1", source={"label": "E", "url": "https://example.invalid/e"})
    write_record(records / "duplicate_source_2.json", **base, record_id="SYNTH_DUP_SOURCE_2", source={"label": "E copy", "url": "https://example.invalid/e"})
    return root


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else ROOT / outdir
    outdir.mkdir(parents=True, exist_ok=True)
    root = build_synthetic_root(outdir)
    lint_out = outdir / "synthetic_lint"
    lint_root(root, lint_out, fail_on_error=False)
    rows = list(csv.DictReader((lint_out / "external_record_uniqueness_lint.tsv").open(), delimiter="\t"))
    checks = {
        "unique_records_pass": not any(row["record_id"] in {"SYNTH_UNIQUE_A", "SYNTH_UNIQUE_B"} and row["status"] == "FAIL" for row in rows),
        "duplicate_id_fails": any(row["record_id"] == "SYNTH_DUP_ID" and row["check"] == "record_id_unique" and row["status"] == "FAIL" for row in rows),
        "duplicate_source_fails": any(row["record_id"] == "SYNTH_DUP_SOURCE_1" and row["check"] == "source_locator_unique" and row["status"] == "FAIL" for row in rows),
    }
    check_rows = [{"check": key, "status": "PASS" if value else "FAIL"} for key, value in checks.items()]
    write_tsv(outdir / "synthetic_uniqueness_checks.tsv", check_rows, ["check", "status"])
    summary = {
        "synthetic": True,
        "purpose": "V47 external-record uniqueness linter synthetic fixture; no biological claim",
        "n_checks": len(check_rows),
        "n_fail": sum(1 for row in check_rows if row["status"] != "PASS"),
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
    }
    (outdir / "synthetic_uniqueness_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["overall_status"] == "PASS" or not fail_on_error else 2


def main() -> int:
    args = parse_args()
    if args.command == "lint":
        return lint_root(args.root.resolve(), args.outdir, args.fail_on_error)
    if args.command == "synthetic-check":
        return synthetic_check(args.outdir, args.fail_on_error)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
