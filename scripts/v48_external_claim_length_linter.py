#!/usr/bin/env python3
"""Lint external records for concise, non-excerpt-like claim text.

This is a copyright/provenance hygiene check. External records should contain
short sourced summaries, not long copied source passages.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EXTERNAL_ROOT = "knowledge_external"
DEFAULT_OUTDIR = ROOT / "analysis/v48_external_claim_length_linter"
FIELD_LIMITS = {
    "claim": 60,
    "relationship_note": 80,
    "project_use": 60,
    "future_grounding_route": 80,
    "why_unverifiable": 80,
}
SOURCE_TERMS_LIMITS = {
    "license_or_terms_label": 30,
    "reuse_notes": 80,
}
EXCERPT_FIELD_RE = re.compile(r"(quote|quoted|excerpt|verbatim)", re.IGNORECASE)
EXCERPT_FIELD_LIMIT = 25


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    lint = sub.add_parser("lint", help="Lint external record text lengths")
    lint.add_argument("--root", type=Path, default=ROOT)
    lint.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    lint.add_argument("--fail-on-error", action="store_true")
    synth = sub.add_parser("synthetic-check", help="Run synthetic claim-length fixtures")
    synth.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    synth.add_argument("--fail-on-error", action="store_true")
    return parser.parse_args()


def rel(root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def word_count(value: object) -> int:
    return len(re.findall(r"\b\w+\b", str(value or "")))


def record_paths(root: Path) -> list[Path]:
    paths: list[Path] = []
    for subdir in ["records", "catalogs/resources"]:
        base = root / EXTERNAL_ROOT / subdir
        if base.exists():
            paths.extend(path for path in base.rglob("*.json") if not path.name.endswith(".schema.json"))
    return sorted(paths)


def write_tsv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def add(
    rows: list[dict[str, object]],
    path: str,
    record_id: str,
    field: str,
    limit: int,
    count: int,
    detail: str = "short sourced summary required; do not paste long source passages",
) -> None:
    rows.append(
        {
            "path": path,
            "record_id": record_id,
            "field": field,
            "word_limit": limit,
            "word_count": count,
            "status": "PASS" if count <= limit else "FAIL",
            "detail": detail,
        }
    )


def iter_excerpt_fields(value: Any, prefix: str = "") -> list[tuple[str, object]]:
    hits: list[tuple[str, object]] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            field = f"{prefix}.{key}" if prefix else str(key)
            if EXCERPT_FIELD_RE.search(str(key)):
                hits.append((field, nested))
            hits.extend(iter_excerpt_fields(nested, field))
    elif isinstance(value, list):
        for idx, nested in enumerate(value):
            hits.extend(iter_excerpt_fields(nested, f"{prefix}[{idx}]"))
    return hits


def lint_root(root: Path, outdir: Path, fail_on_error: bool) -> int:
    root = root.resolve()
    outdir = outdir if outdir.is_absolute() else root / outdir
    rows: list[dict[str, object]] = []
    for path in record_paths(root):
        data = json.loads(path.read_text())
        record_id = str(data.get("record_id", ""))
        rel_path = rel(root, path)
        for field, limit in FIELD_LIMITS.items():
            if field in data:
                add(rows, rel_path, record_id, field, limit, word_count(data.get(field)))
        terms = data.get("source_terms")
        if isinstance(terms, dict):
            for field, limit in SOURCE_TERMS_LIMITS.items():
                if field in terms:
                    add(rows, rel_path, record_id, f"source_terms.{field}", limit, word_count(terms.get(field)))
        for field, value in iter_excerpt_fields(data):
            add(
                rows,
                rel_path,
                record_id,
                field,
                EXCERPT_FIELD_LIMIT,
                word_count(value),
                "excerpt/quote/verbatim-like fields must stay below the short-quote limit and remain source-bound",
            )
    n_fail = sum(1 for row in rows if row["status"] == "FAIL")
    write_tsv(outdir / "external_claim_length_lint.tsv", rows, ["path", "record_id", "field", "word_limit", "word_count", "status", "detail"])
    summary = {
        "synthetic": False,
        "purpose": "V48 external claim-length safety lint; copyright/provenance hygiene only; no claim validation",
        "n_records": len(record_paths(root)),
        "n_checks": len(rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
    }
    (outdir / "external_claim_length_lint_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if n_fail == 0 or not fail_on_error else 2


def write_record(path: Path, **kwargs: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(kwargs, indent=2, sort_keys=True) + "\n")


def synthetic_root(outdir: Path) -> Path:
    root = outdir / "synthetic_root"
    if root.exists():
        shutil.rmtree(root)
    base = {
        "record_type": "external_claim",
        "epistemic_class": "external-unverifiable",
        "source": {"label": "Synthetic", "url": "https://example.invalid"},
        "date_accessed": "2026-06-14",
        "relationship_to_project_findings": "orthogonal",
        "not_project_grounded_marker": "NOT_PROJECT_GROUNDED",
        "why_unverifiable": "Synthetic fixture.",
    }
    write_record(root / EXTERNAL_ROOT / "records/good.json", **base, record_id="SYNTH_LENGTH_GOOD", claim="Short synthetic summary.")
    long_claim = " ".join(["word"] * 70)
    write_record(root / EXTERNAL_ROOT / "records/bad.json", **base, record_id="SYNTH_LENGTH_BAD", claim=long_claim)
    long_excerpt = " ".join(["quoted"] * 30)
    write_record(
        root / EXTERNAL_ROOT / "records/bad_excerpt.json",
        **base,
        record_id="SYNTH_EXCERPT_BAD",
        claim="Short synthetic summary.",
        source_excerpt=long_excerpt,
    )
    return root


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else ROOT / outdir
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    root = synthetic_root(outdir)
    lint_out = outdir / "synthetic_lint"
    lint_root(root, lint_out, fail_on_error=False)
    rows = list(csv.DictReader((lint_out / "external_claim_length_lint.tsv").open(), delimiter="\t"))
    checks = {
        "short_claim_passes": any(row["record_id"] == "SYNTH_LENGTH_GOOD" and row["field"] == "claim" and row["status"] == "PASS" for row in rows),
        "long_claim_fails": any(row["record_id"] == "SYNTH_LENGTH_BAD" and row["field"] == "claim" and row["status"] == "FAIL" for row in rows),
        "long_excerpt_field_fails": any(row["record_id"] == "SYNTH_EXCERPT_BAD" and row["field"] == "source_excerpt" and row["status"] == "FAIL" for row in rows),
    }
    check_rows = [{"check": key, "status": "PASS" if value else "FAIL"} for key, value in checks.items()]
    write_tsv(outdir / "synthetic_external_claim_length_checks.tsv", check_rows, ["check", "status"])
    summary = {
        "synthetic": True,
        "purpose": "V48 external claim-length synthetic fixture; no biological claim",
        "n_checks": len(check_rows),
        "n_fail": sum(1 for row in check_rows if row["status"] != "PASS"),
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
    }
    (outdir / "synthetic_external_claim_length_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
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
