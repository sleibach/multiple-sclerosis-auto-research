#!/usr/bin/env python3
"""Check that the V48 source-domain review matches current external records."""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
EXTERNAL_ROOT = "knowledge_external"
DEFAULT_OUTDIR = ROOT / "analysis/v48_source_domain_review_freshness_linter"
DEFAULT_REVIEW = ROOT / "knowledge_external/catalogs/indexes/source_domain_review_v48.tsv"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    lint = sub.add_parser("lint", help="Lint source-domain review freshness")
    lint.add_argument("--root", type=Path, default=ROOT)
    lint.add_argument("--review", type=Path, default=DEFAULT_REVIEW)
    lint.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    lint.add_argument("--fail-on-error", action="store_true")
    synth = sub.add_parser("synthetic-check", help="Run synthetic source-domain freshness fixtures")
    synth.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    synth.add_argument("--fail-on-error", action="store_true")
    return parser.parse_args()


def rel(root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def record_paths(root: Path) -> list[Path]:
    paths: list[Path] = []
    for subdir in ["records", "catalogs/resources"]:
        base = root / EXTERNAL_ROOT / subdir
        if base.exists():
            paths.extend(path for path in base.rglob("*.json") if not path.name.endswith(".schema.json"))
    return sorted(paths)


def source_url(data: dict[str, object]) -> str:
    source = data.get("source")
    if isinstance(source, dict):
        return str(source.get("url", "")).strip()
    return ""


def domain_for_url(url: str) -> str:
    if not url:
        return "NO_URL"
    host = urlparse(url).netloc.lower()
    return host[4:] if host.startswith("www.") else host


def current_rows(root: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path in record_paths(root):
        data = json.loads(path.read_text())
        url = source_url(data)
        rows.append(
            {
                "record_id": str(data.get("record_id", "")),
                "domain": domain_for_url(url),
                "source_url": url,
                "path": rel(root, path),
            }
        )
    return rows


def read_review(path: Path) -> list[dict[str, str]]:
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


def lint_root(root: Path, review: Path, outdir: Path, fail_on_error: bool) -> int:
    root = root.resolve()
    review = review if review.is_absolute() else root / review
    outdir = outdir if outdir.is_absolute() else root / outdir
    current = current_rows(root)
    reviewed = read_review(review)
    current_by_id = {row["record_id"]: row for row in current}
    reviewed_by_id = {row.get("record_id", ""): row for row in reviewed}
    rows: list[dict[str, object]] = []
    for record_id, row in sorted(current_by_id.items()):
        reviewed_row = reviewed_by_id.get(record_id)
        rows.append(
            {
                "record_id": record_id,
                "check": "record_present_in_source_domain_review",
                "status": "PASS" if reviewed_row else "FAIL",
                "detail": row["path"],
            }
        )
        if reviewed_row:
            rows.append(
                {
                    "record_id": record_id,
                    "check": "review_domain_matches_current_source_url",
                    "status": "PASS" if reviewed_row.get("domain") == row["domain"] else "FAIL",
                    "detail": f"current={row['domain']} reviewed={reviewed_row.get('domain', '')}",
                }
            )
            rows.append(
                {
                    "record_id": record_id,
                    "check": "review_source_url_matches_current",
                    "status": "PASS" if reviewed_row.get("source_url") == row["source_url"] else "FAIL",
                    "detail": row["source_url"],
                }
            )
    stale_ids = sorted(set(reviewed_by_id) - set(current_by_id))
    for record_id in stale_ids:
        rows.append(
            {
                "record_id": record_id,
                "check": "stale_review_record_removed_from_current_records",
                "status": "FAIL",
                "detail": "review row has no current external record",
            }
        )
    n_fail = sum(1 for row in rows if row["status"] == "FAIL")
    summary = {
        "synthetic": False,
        "purpose": "V48 source-domain review freshness lint; maintenance/navigation only; no biological claim",
        "n_current_records": len(current),
        "n_review_rows": len(reviewed),
        "n_checks": len(rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
        "lint": rel(root, outdir / "source_domain_review_freshness_lint.tsv") if root == ROOT else str(outdir / "source_domain_review_freshness_lint.tsv"),
    }
    write_tsv(outdir / "source_domain_review_freshness_lint.tsv", rows, ["record_id", "check", "status", "detail"])
    (outdir / "source_domain_review_freshness_lint_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["overall_status"] == "PASS" or not fail_on_error else 2


def write_record(path: Path, record_id: str, url: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "record_id": record_id,
                "record_type": "external_claim",
                "claim": "Synthetic domain freshness claim.",
                "epistemic_class": "external-unverifiable",
                "source": {"label": "Synthetic", "url": url},
                "date_accessed": "2026-06-14",
                "relationship_to_project_findings": "orthogonal",
                "not_project_grounded_marker": "NOT_PROJECT_GROUNDED",
                "why_unverifiable": "Synthetic fixture.",
            },
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )


def synthetic_root(outdir: Path) -> tuple[Path, Path]:
    root = outdir / "synthetic_root"
    if root.exists():
        shutil.rmtree(root)
    write_record(root / EXTERNAL_ROOT / "records/good.json", "SYNTH_DOMAIN_GOOD", "https://example.invalid/good")
    write_record(root / EXTERNAL_ROOT / "records/missing.json", "SYNTH_DOMAIN_MISSING", "https://missing.example.invalid/")
    write_record(root / EXTERNAL_ROOT / "records/changed.json", "SYNTH_DOMAIN_CHANGED", "https://current.example.invalid/")
    review = root / EXTERNAL_ROOT / "catalogs/indexes/source_domain_review_v48.tsv"
    review.parent.mkdir(parents=True, exist_ok=True)
    with review.open("w", newline="") as handle:
        fields = ["domain", "review_class", "record_id", "record_type", "source_url", "access_tier", "path"]
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerow({"domain": "example.invalid", "review_class": "manual_review_domain", "record_id": "SYNTH_DOMAIN_GOOD", "record_type": "external_claim", "source_url": "https://example.invalid/good", "access_tier": "", "path": "knowledge_external/records/good.json"})
        writer.writerow({"domain": "old.example.invalid", "review_class": "manual_review_domain", "record_id": "SYNTH_DOMAIN_CHANGED", "record_type": "external_claim", "source_url": "https://old.example.invalid/", "access_tier": "", "path": "knowledge_external/records/changed.json"})
        writer.writerow({"domain": "stale.example.invalid", "review_class": "manual_review_domain", "record_id": "SYNTH_DOMAIN_STALE", "record_type": "external_claim", "source_url": "https://stale.example.invalid/", "access_tier": "", "path": "knowledge_external/records/stale.json"})
    return root, review.relative_to(root)


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else ROOT / outdir
    outdir.mkdir(parents=True, exist_ok=True)
    root, review = synthetic_root(outdir)
    lint_out = outdir / "synthetic_lint"
    lint_root(root, root / review, lint_out, fail_on_error=False)
    rows = list(csv.DictReader((lint_out / "source_domain_review_freshness_lint.tsv").open(), delimiter="\t"))
    checks = {
        "good_record_passes": any(row["record_id"] == "SYNTH_DOMAIN_GOOD" and row["status"] == "PASS" for row in rows),
        "missing_record_fails": any(row["record_id"] == "SYNTH_DOMAIN_MISSING" and row["check"] == "record_present_in_source_domain_review" and row["status"] == "FAIL" for row in rows),
        "changed_domain_fails": any(row["record_id"] == "SYNTH_DOMAIN_CHANGED" and row["check"] == "review_domain_matches_current_source_url" and row["status"] == "FAIL" for row in rows),
        "stale_review_fails": any(row["record_id"] == "SYNTH_DOMAIN_STALE" and row["check"] == "stale_review_record_removed_from_current_records" and row["status"] == "FAIL" for row in rows),
    }
    check_rows = [{"check": key, "status": "PASS" if value else "FAIL"} for key, value in checks.items()]
    write_tsv(outdir / "synthetic_source_domain_review_freshness_checks.tsv", check_rows, ["check", "status"])
    summary = {
        "synthetic": True,
        "purpose": "V48 source-domain review freshness synthetic fixture; no biological claim",
        "n_checks": len(check_rows),
        "n_fail": sum(1 for row in check_rows if row["status"] != "PASS"),
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
    }
    (outdir / "synthetic_source_domain_review_freshness_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["overall_status"] == "PASS" or not fail_on_error else 2


def main() -> int:
    args = parse_args()
    if args.command == "lint":
        return lint_root(args.root, args.review, args.outdir, args.fail_on_error)
    if args.command == "synthetic-check":
        return synthetic_check(args.outdir, args.fail_on_error)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
