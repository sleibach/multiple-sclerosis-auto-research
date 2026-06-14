#!/usr/bin/env python3
"""Check that the V48 source URL duplicate review matches current records."""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from collections import defaultdict
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


ROOT = Path(__file__).resolve().parents[1]
EXTERNAL_DIRS = [
    ROOT / "knowledge_external/records",
    ROOT / "knowledge_external/catalogs/resources",
]
DEFAULT_REVIEW = ROOT / "knowledge_external/catalogs/indexes/source_url_duplicate_review_v48.tsv"
DEFAULT_SUMMARY = ROOT / "knowledge_external/catalogs/indexes/source_url_duplicate_review_v48_summary.json"
DEFAULT_OUTDIR = ROOT / "analysis/v48_source_url_duplicate_freshness_linter"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    lint = sub.add_parser("lint", help="Lint source URL duplicate review freshness")
    lint.add_argument("--review", type=Path, default=DEFAULT_REVIEW)
    lint.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    lint.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    lint.add_argument("--fail-on-error", action="store_true")
    synth = sub.add_parser("synthetic-check", help="Run synthetic duplicate-review freshness fixtures")
    synth.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    synth.add_argument("--fail-on-error", action="store_true")
    return parser.parse_args()


def canonical_url(url: str) -> str:
    if not url:
        return ""
    parts = urlsplit(url)
    scheme = parts.scheme.lower() or "https"
    netloc = parts.netloc.lower()
    path = parts.path.rstrip("/") or "/"
    query = urlencode(sorted(parse_qsl(parts.query, keep_blank_values=True)))
    return urlunsplit((scheme, netloc, path, query, ""))


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


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


def source_url(data: dict[str, object]) -> str:
    source = data.get("source")
    if isinstance(source, dict):
        return str(source.get("url", "")).strip()
    return ""


def current_duplicate_rows(paths: list[Path] | None = None) -> list[dict[str, object]]:
    if paths is None:
        paths = []
        for base in EXTERNAL_DIRS:
            if base.exists():
                paths.extend(path for path in base.rglob("*.json") if not path.name.endswith(".schema.json"))
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for path in sorted(paths):
        data = read_json(path)
        canonical = canonical_url(source_url(data))
        groups[canonical].append({"record_id": str(data.get("record_id", "")), "record_path": rel(path)})
    rows: list[dict[str, object]] = []
    for canonical, grouped in sorted(groups.items()):
        if len(grouped) < 2:
            continue
        rows.append(
            {
                "canonical_url": canonical,
                "n_records": len(grouped),
                "record_ids": ";".join(row["record_id"] for row in grouped),
                "record_paths": ";".join(row["record_path"] for row in grouped),
            }
        )
    return rows


def add(rows: list[dict[str, object]], canonical: str, check: str, status: str, detail: str) -> None:
    rows.append({"canonical_url": canonical, "check": check, "status": status, "detail": detail})


def lint_review(review_path: Path, summary_path: Path, outdir: Path, fail_on_error: bool, expected_rows: list[dict[str, object]] | None = None) -> int:
    expected = {str(row["canonical_url"]): row for row in (expected_rows if expected_rows is not None else current_duplicate_rows())}
    observed = {row.get("canonical_url", ""): row for row in read_tsv(review_path)}
    rows: list[dict[str, object]] = []
    for canonical, expected_row in sorted(expected.items()):
        observed_row = observed.get(canonical)
        add(rows, canonical, "present_in_review", "PASS" if observed_row else "FAIL", str(review_path))
        if not observed_row:
            continue
        for field in ["n_records", "record_ids", "record_paths"]:
            add(
                rows,
                canonical,
                f"field_matches.{field}",
                "PASS" if str(expected_row.get(field, "")) == observed_row.get(field, "") else "FAIL",
                f"expected={expected_row.get(field, '')} observed={observed_row.get(field, '')}",
            )
    for canonical in sorted(set(observed) - set(expected)):
        add(rows, canonical, "no_extra_duplicate_group", "FAIL", "review row is not duplicated in current external records")
    summary = read_json(summary_path)
    add(
        rows,
        "summary",
        "summary_duplicate_count_matches_rows",
        "PASS" if int(summary.get("n_duplicate_canonical_urls", -1)) == len(observed) else "FAIL",
        f"summary={summary.get('n_duplicate_canonical_urls', '')} rows={len(observed)}",
    )
    n_fail = sum(1 for row in rows if row["status"] != "PASS")
    outdir.mkdir(parents=True, exist_ok=True)
    write_tsv(outdir / "source_url_duplicate_freshness_lint.tsv", rows, ["canonical_url", "check", "status", "detail"])
    result = {
        "synthetic": False,
        "purpose": "V48 source URL duplicate review freshness lint; source maintenance only; no claim validation",
        "n_expected_duplicate_urls": len(expected),
        "n_review_duplicate_urls": len(observed),
        "n_checks": len(rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
    }
    (outdir / "source_url_duplicate_freshness_lint_summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if n_fail == 0 or not fail_on_error else 2


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else ROOT / outdir
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    review = outdir / "synthetic_review.tsv"
    summary = outdir / "synthetic_summary.json"
    expected = [
        {"canonical_url": "https://example.org/a", "n_records": 2, "record_ids": "A;B", "record_paths": "a.json;b.json"},
        {"canonical_url": "https://example.org/b", "n_records": 2, "record_ids": "C;D", "record_paths": "c.json;d.json"},
    ]
    write_tsv(
        review,
        [
            {"canonical_url": "https://example.org/a", "n_records": 99, "record_ids": "A;B", "record_paths": "a.json;b.json", "review_reason": "synthetic", "boundary": "synthetic"},
            {"canonical_url": "https://example.org/extra", "n_records": 2, "record_ids": "X;Y", "record_paths": "x.json;y.json", "review_reason": "synthetic", "boundary": "synthetic"},
        ],
        ["canonical_url", "n_records", "record_ids", "record_paths", "review_reason", "boundary"],
    )
    summary.write_text(json.dumps({"n_duplicate_canonical_urls": 99}) + "\n")
    lint_out = outdir / "synthetic_lint"
    lint_review(review, summary, lint_out, fail_on_error=False, expected_rows=expected)
    rows = read_tsv(lint_out / "source_url_duplicate_freshness_lint.tsv")
    checks = {
        "missing_duplicate_group_fails": any(row["canonical_url"] == "https://example.org/b" and row["check"] == "present_in_review" and row["status"] == "FAIL" for row in rows),
        "stale_count_fails": any(row["canonical_url"] == "https://example.org/a" and row["check"] == "field_matches.n_records" and row["status"] == "FAIL" for row in rows),
        "extra_group_fails": any(row["canonical_url"] == "https://example.org/extra" and row["check"] == "no_extra_duplicate_group" and row["status"] == "FAIL" for row in rows),
        "bad_summary_count_fails": any(row["canonical_url"] == "summary" and row["check"] == "summary_duplicate_count_matches_rows" and row["status"] == "FAIL" for row in rows),
    }
    check_rows = [{"check": key, "status": "PASS" if value else "FAIL"} for key, value in checks.items()]
    write_tsv(outdir / "synthetic_source_url_duplicate_freshness_checks.tsv", check_rows, ["check", "status"])
    synth_summary = {
        "synthetic": True,
        "purpose": "V48 source URL duplicate freshness synthetic fixture; no biological claim",
        "n_checks": len(check_rows),
        "n_fail": sum(1 for row in check_rows if row["status"] != "PASS"),
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
    }
    (outdir / "synthetic_source_url_duplicate_freshness_summary.json").write_text(json.dumps(synth_summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(synth_summary, indent=2, sort_keys=True))
    return 0 if synth_summary["overall_status"] == "PASS" or not fail_on_error else 2


def main() -> int:
    args = parse_args()
    if args.command == "lint":
        return lint_review(args.review, args.summary, args.outdir, args.fail_on_error)
    if args.command == "synthetic-check":
        return synthetic_check(args.outdir, args.fail_on_error)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
