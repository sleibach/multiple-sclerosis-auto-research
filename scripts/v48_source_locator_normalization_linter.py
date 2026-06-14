#!/usr/bin/env python3
"""Lint source locators on segregated external records.

This is provenance infrastructure only. It checks whether source URL/DOI/PMID
fields are syntactically normalized enough for later review; it does not fetch
or validate external content.
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
DEFAULT_OUTDIR = ROOT / "analysis/v48_source_locator_normalization_linter"
NOT_GROUNDED = "NOT_PROJECT_GROUNDED"
DOI_RE = re.compile(r"^10\.\d{4,9}/\S+$")
PMID_RE = re.compile(r"^\d{1,9}$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    lint = sub.add_parser("lint", help="Lint real external source locators")
    lint.add_argument("--root", type=Path, default=ROOT)
    lint.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    lint.add_argument("--fail-on-error", action="store_true")
    synth = sub.add_parser("synthetic-check", help="Run synthetic source-locator fixtures")
    synth.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    synth.add_argument("--fail-on-error", action="store_true")
    return parser.parse_args()


def rel(root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def external_record_paths(root: Path) -> list[Path]:
    paths: list[Path] = []
    for base in [root / EXTERNAL_ROOT / "records", root / EXTERNAL_ROOT / "catalogs/resources"]:
        if base.exists():
            paths.extend(path for path in base.rglob("*.json") if not path.name.endswith(".schema.json"))
    return sorted(paths)


def write_tsv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def source_value(source: Any, key: str) -> str:
    if not isinstance(source, dict):
        return ""
    return str(source.get(key, "")).strip()


def add(rows: list[dict[str, object]], path: str, record_id: str, check: str, ok: bool, detail: str) -> None:
    rows.append(
        {
            "path": path,
            "record_id": record_id,
            "check": check,
            "status": "PASS" if ok else "FAIL",
            "detail": detail,
        }
    )


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
    source = data.get("source")
    label = source_value(source, "label")
    url = source_value(source, "url")
    doi = source_value(source, "doi")
    pmid = source_value(source, "pmid")
    citation = source_value(source, "citation")
    locator_count = sum(bool(value) for value in [url, doi, pmid, citation])
    add(rows, rel_path, record_id, "source_label_present", bool(label), label)
    add(rows, rel_path, record_id, "at_least_one_locator_present", locator_count >= 1, f"locators={locator_count}")
    if url:
        add(rows, rel_path, record_id, "url_has_http_scheme", url.startswith(("https://", "http://")), url)
        add(rows, rel_path, record_id, "url_has_no_whitespace", not any(char.isspace() for char in url), url)
        add(rows, rel_path, record_id, "url_is_trimmed", url == source.get("url", ""), url)
    if doi:
        add(rows, rel_path, record_id, "doi_format", bool(DOI_RE.match(doi)), doi)
        add(rows, rel_path, record_id, "doi_has_no_url_prefix", not doi.lower().startswith(("https://", "http://", "doi:")), doi)
    if pmid:
        add(rows, rel_path, record_id, "pmid_numeric", bool(PMID_RE.match(pmid)), pmid)
    add(rows, rel_path, record_id, "not_grounded_marker_present", data.get("not_project_grounded_marker") == NOT_GROUNDED, str(data.get("not_project_grounded_marker", "")))
    return rows


def lint_root(root: Path, outdir: Path, fail_on_error: bool) -> int:
    root = root.resolve()
    outdir = outdir if outdir.is_absolute() else root / outdir
    rows: list[dict[str, object]] = []
    for path in external_record_paths(root):
        rows.extend(lint_record(root, path))
    n_fail = sum(1 for row in rows if row["status"] != "PASS")
    write_tsv(outdir / "source_locator_normalization_lint.tsv", rows, ["path", "record_id", "check", "status", "detail"])
    summary = {
        "synthetic": False,
        "purpose": "V48 source-locator normalization lint; no biological claim",
        "n_records": len(external_record_paths(root)),
        "n_checks": len(rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
        "lint": rel(root, outdir / "source_locator_normalization_lint.tsv") if root == ROOT else str(outdir / "source_locator_normalization_lint.tsv"),
    }
    (outdir / "source_locator_normalization_lint_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
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
    base.mkdir(parents=True)
    common = {
        "claim": "Synthetic source locator claim.",
        "epistemic_class": "external-unverifiable",
        "date_accessed": "2026-06-14",
        "relationship_to_project_findings": "orthogonal",
        "not_project_grounded_marker": NOT_GROUNDED,
        "why_unverifiable": "Synthetic fixture.",
    }
    write_record(base / "good.json", **common, record_id="SYNTH_GOOD", source={"label": "Good", "url": "https://example.invalid/a", "doi": "10.1234/example"})
    write_record(base / "bad_url.json", **common, record_id="SYNTH_BAD_URL", source={"label": "Bad URL", "url": "example.invalid/a b"})
    write_record(base / "bad_doi.json", **common, record_id="SYNTH_BAD_DOI", source={"label": "Bad DOI", "doi": "https://doi.org/10.1234/example"})
    return root


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else ROOT / outdir
    outdir.mkdir(parents=True, exist_ok=True)
    root = synthetic_root(outdir)
    lint_out = outdir / "synthetic_lint"
    lint_root(root, lint_out, fail_on_error=False)
    rows = list(csv.DictReader((lint_out / "source_locator_normalization_lint.tsv").open(), delimiter="\t"))
    checks = {
        "good_passes": not any(row["record_id"] == "SYNTH_GOOD" and row["status"] == "FAIL" for row in rows),
        "bad_url_fails_scheme": any(row["record_id"] == "SYNTH_BAD_URL" and row["check"] == "url_has_http_scheme" and row["status"] == "FAIL" for row in rows),
        "bad_url_fails_whitespace": any(row["record_id"] == "SYNTH_BAD_URL" and row["check"] == "url_has_no_whitespace" and row["status"] == "FAIL" for row in rows),
        "bad_doi_fails_prefix": any(row["record_id"] == "SYNTH_BAD_DOI" and row["check"] == "doi_has_no_url_prefix" and row["status"] == "FAIL" for row in rows),
    }
    check_rows = [{"check": key, "status": "PASS" if value else "FAIL"} for key, value in checks.items()]
    write_tsv(outdir / "synthetic_source_locator_checks.tsv", check_rows, ["check", "status"])
    summary = {
        "synthetic": True,
        "purpose": "V48 source-locator normalization synthetic fixture; no biological claim",
        "n_checks": len(check_rows),
        "n_fail": sum(1 for row in check_rows if row["status"] != "PASS"),
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
    }
    (outdir / "synthetic_source_locator_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
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
