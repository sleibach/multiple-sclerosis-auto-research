#!/usr/bin/env python3
"""Check that the V48 source-domain relationship rollup is current."""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
EXTERNAL_ROOT = ROOT / "knowledge_external"
DEFAULT_MATRIX = ROOT / "knowledge_external/synthesis/convergence_contradiction_v48.tsv"
DEFAULT_ROLLUP = ROOT / "knowledge_external/catalogs/indexes/source_domain_relationship_rollup_v48.tsv"
DEFAULT_OUTDIR = ROOT / "analysis/v48_source_domain_relationship_freshness_linter"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    lint = sub.add_parser("lint", help="Lint source-domain relationship rollup freshness")
    lint.add_argument("--matrix", type=Path, default=DEFAULT_MATRIX)
    lint.add_argument("--rollup", type=Path, default=DEFAULT_ROLLUP)
    lint.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    lint.add_argument("--fail-on-error", action="store_true")
    synth = sub.add_parser("synthetic-check", help="Run synthetic rollup freshness fixtures")
    synth.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    synth.add_argument("--fail-on-error", action="store_true")
    return parser.parse_args()


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


def domain_for_url(url: str) -> str:
    if not url:
        return "NO_URL"
    host = urlparse(url).netloc.lower()
    return host[4:] if host.startswith("www.") else host


def source_url(data: dict[str, object]) -> str:
    source = data.get("source")
    if isinstance(source, dict):
        return str(source.get("url", "")).strip()
    return ""


def record_paths(root: Path) -> list[Path]:
    paths: list[Path] = []
    for subdir in ["records", "catalogs/resources"]:
        base = root / "knowledge_external" / subdir
        if base.exists():
            paths.extend(path for path in base.rglob("*.json") if not path.name.endswith(".schema.json"))
    return sorted(paths)


def expected_rows(root: Path, matrix: Path) -> dict[str, dict[str, str]]:
    records: dict[str, dict[str, str]] = {}
    record_counts: dict[str, Counter[str]] = defaultdict(Counter)
    matrix_counts: dict[str, Counter[str]] = defaultdict(Counter)
    for path in record_paths(root):
        data = json.loads(path.read_text())
        record_id = str(data.get("record_id", ""))
        domain = domain_for_url(source_url(data))
        records[record_id] = {"domain": domain}
        record_counts[domain][str(data.get("relationship_to_project_findings", ""))] += 1
    for row in read_tsv(matrix):
        domain = records.get(row.get("external_record_id", ""), {}).get("domain", "missing_record")
        matrix_counts[domain][row.get("relationship_class", "")] += 1
    expected: dict[str, dict[str, str]] = {}
    for domain in sorted(set(record_counts) | set(matrix_counts)):
        rc = record_counts[domain]
        mc = matrix_counts[domain]
        expected[domain] = {
            "source_domain": domain,
            "n_records": str(sum(rc.values())),
            "record_relationship_counts": ";".join(f"{key}:{value}" for key, value in sorted(rc.items()) if key),
            "n_matrix_rows": str(sum(mc.values())),
            "matrix_relationship_counts": ";".join(f"{key}:{value}" for key, value in sorted(mc.items()) if key),
            "has_convergence": "yes" if mc.get("converges", 0) else "no",
            "has_contradiction": "yes" if mc.get("contradicts", 0) else "no",
        }
    return expected


def lint_paths(root: Path, matrix: Path, rollup: Path, outdir: Path, fail_on_error: bool) -> int:
    expected = expected_rows(root, matrix)
    actual = {row.get("source_domain", ""): row for row in read_tsv(rollup)}
    rows: list[dict[str, object]] = []
    for domain, expected_row in expected.items():
        actual_row = actual.get(domain)
        rows.append({"source_domain": domain, "check": "domain_present_in_rollup", "status": "PASS" if actual_row else "FAIL", "detail": domain})
        if actual_row:
            for field in ["n_records", "record_relationship_counts", "n_matrix_rows", "matrix_relationship_counts", "has_convergence", "has_contradiction"]:
                rows.append(
                    {
                        "source_domain": domain,
                        "check": f"{field}_matches_expected",
                        "status": "PASS" if actual_row.get(field, "") == expected_row[field] else "FAIL",
                        "detail": f"expected={expected_row[field]} actual={actual_row.get(field, '')}",
                    }
                )
    for domain in sorted(set(actual) - set(expected)):
        rows.append({"source_domain": domain, "check": "stale_rollup_domain_removed_from_current_records", "status": "FAIL", "detail": domain})
    n_fail = sum(1 for row in rows if row["status"] == "FAIL")
    write_tsv(outdir / "source_domain_relationship_freshness_lint.tsv", rows, ["source_domain", "check", "status", "detail"])
    summary = {
        "synthetic": False,
        "purpose": "V48 source-domain relationship rollup freshness lint; navigation/synthesis only; no biological claim",
        "n_expected_domains": len(expected),
        "n_rollup_domains": len(actual),
        "n_checks": len(rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
    }
    (outdir / "source_domain_relationship_freshness_lint_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if n_fail == 0 or not fail_on_error else 2


def write_record(path: Path, record_id: str, url: str, relationship: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "record_id": record_id,
                "record_type": "external_claim",
                "claim": "Synthetic source-domain relationship freshness claim.",
                "epistemic_class": "external-unverifiable",
                "source": {"label": "Synthetic", "url": url},
                "date_accessed": "2026-06-14",
                "relationship_to_project_findings": relationship,
                "not_project_grounded_marker": "NOT_PROJECT_GROUNDED",
                "why_unverifiable": "Synthetic fixture.",
            },
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )


def synthetic_root(outdir: Path) -> tuple[Path, Path, Path]:
    root = outdir / "synthetic_root"
    if root.exists():
        shutil.rmtree(root)
    write_record(root / "knowledge_external/records/good.json", "SYNTH_DOMAIN_REL_GOOD", "https://example.invalid/good", "supports")
    write_record(root / "knowledge_external/records/missing.json", "SYNTH_DOMAIN_REL_MISSING", "https://missing.example.invalid/", "orthogonal")
    matrix = root / "knowledge_external/synthesis/convergence_contradiction_v48.tsv"
    write_tsv(matrix, [{"external_record_id": "SYNTH_DOMAIN_REL_GOOD", "relationship_class": "converges"}], ["external_record_id", "relationship_class"])
    rollup = root / "knowledge_external/catalogs/indexes/source_domain_relationship_rollup_v48.tsv"
    write_tsv(
        rollup,
        [
            {"source_domain": "example.invalid", "n_records": "1", "record_relationship_counts": "supports:1", "n_matrix_rows": "1", "matrix_relationship_counts": "converges:1", "has_convergence": "yes", "has_contradiction": "no"},
            {"source_domain": "stale.example.invalid", "n_records": "1", "record_relationship_counts": "orthogonal:1", "n_matrix_rows": "0", "matrix_relationship_counts": "", "has_convergence": "no", "has_contradiction": "no"},
        ],
        ["source_domain", "n_records", "record_relationship_counts", "n_matrix_rows", "matrix_relationship_counts", "has_convergence", "has_contradiction"],
    )
    return root, matrix, rollup


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else ROOT / outdir
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    root, matrix, rollup = synthetic_root(outdir)
    lint_out = outdir / "synthetic_lint"
    lint_paths(root, matrix, rollup, lint_out, fail_on_error=False)
    rows = list(csv.DictReader((lint_out / "source_domain_relationship_freshness_lint.tsv").open(), delimiter="\t"))
    checks = {
        "good_domain_passes": any(row["source_domain"] == "example.invalid" and row["status"] == "PASS" for row in rows),
        "missing_domain_fails": any(row["source_domain"] == "missing.example.invalid" and row["check"] == "domain_present_in_rollup" and row["status"] == "FAIL" for row in rows),
        "stale_domain_fails": any(row["source_domain"] == "stale.example.invalid" and row["check"] == "stale_rollup_domain_removed_from_current_records" and row["status"] == "FAIL" for row in rows),
    }
    check_rows = [{"check": key, "status": "PASS" if value else "FAIL"} for key, value in checks.items()]
    write_tsv(outdir / "synthetic_source_domain_relationship_freshness_checks.tsv", check_rows, ["check", "status"])
    summary = {
        "synthetic": True,
        "purpose": "V48 source-domain relationship freshness synthetic fixture; no biological claim",
        "n_checks": len(check_rows),
        "n_fail": sum(1 for row in check_rows if row["status"] != "PASS"),
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
    }
    (outdir / "synthetic_source_domain_relationship_freshness_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["overall_status"] == "PASS" or not fail_on_error else 2


def main() -> int:
    args = parse_args()
    if args.command == "lint":
        return lint_paths(ROOT, args.matrix, args.rollup, args.outdir, args.fail_on_error)
    if args.command == "synthetic-check":
        return synthetic_check(args.outdir, args.fail_on_error)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
