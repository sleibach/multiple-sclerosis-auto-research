#!/usr/bin/env python3
"""Check that the V48 convergence source-independence matrix is fresh."""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MATRIX = ROOT / "knowledge_external/synthesis/convergence_contradiction_v48.tsv"
DEFAULT_INDEPENDENCE = ROOT / "knowledge_external/synthesis/convergence_source_independence_v48.tsv"
DEFAULT_SUMMARY = ROOT / "knowledge_external/catalogs/indexes/convergence_source_independence_v48_summary.json"
DEFAULT_OUTDIR = ROOT / "analysis/v48_convergence_source_independence_freshness_linter"
FIELDS = [
    "grounded_finding_id",
    "external_record_id",
    "relationship_class",
    "synthesis_status",
    "external_source",
    "canonical_source_url",
    "source_domain",
    "canonical_source_row_count",
    "source_independence_class",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    lint = sub.add_parser("lint", help="Lint convergence source-independence freshness")
    lint.add_argument("--matrix", type=Path, default=DEFAULT_MATRIX)
    lint.add_argument("--independence", type=Path, default=DEFAULT_INDEPENDENCE)
    lint.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    lint.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    lint.add_argument("--fail-on-error", action="store_true")
    synth = sub.add_parser("synthetic-check", help="Run synthetic freshness fixtures")
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


def canonical_url(url: str) -> str:
    if not url:
        return ""
    parts = urlsplit(url)
    scheme = parts.scheme.lower() or "https"
    netloc = parts.netloc.lower()
    path = parts.path.rstrip("/") or "/"
    query = urlencode(sorted(parse_qsl(parts.query, keep_blank_values=True)))
    return urlunsplit((scheme, netloc, path, query, ""))


def source_domain(url: str) -> str:
    return urlsplit(url).netloc.lower()


def independence_class(relationship: str, group_size: int) -> str:
    if relationship not in {"converges", "contradicts"}:
        return "not_decision_relationship"
    return "single_row_source" if group_size == 1 else "shared_source_cluster"


def expected_rows(matrix: Path) -> list[dict[str, object]]:
    matrix_rows = read_tsv(matrix)
    groups: dict[str, int] = {}
    for row in matrix_rows:
        canonical = canonical_url(row.get("external_source", ""))
        groups[canonical] = groups.get(canonical, 0) + 1
    rows: list[dict[str, object]] = []
    for row in matrix_rows:
        canonical = canonical_url(row.get("external_source", ""))
        relationship = row.get("relationship_class", "")
        rows.append(
            {
                "grounded_finding_id": row.get("grounded_finding_id", ""),
                "external_record_id": row.get("external_record_id", ""),
                "relationship_class": relationship,
                "synthesis_status": row.get("synthesis_status", ""),
                "external_source": row.get("external_source", ""),
                "canonical_source_url": canonical,
                "source_domain": source_domain(canonical),
                "canonical_source_row_count": groups[canonical],
                "source_independence_class": independence_class(relationship, groups[canonical]),
            }
        )
    return rows


def key(row: dict[str, object]) -> str:
    return f"{row.get('grounded_finding_id', '')}||{row.get('external_record_id', '')}"


def add(rows: list[dict[str, object]], row_key: str, check: str, status: str, detail: str) -> None:
    rows.append({"row_key": row_key, "check": check, "status": status, "detail": detail})


def lint_independence(matrix: Path, independence: Path, summary_path: Path, outdir: Path, fail_on_error: bool) -> int:
    expected = {key(row): row for row in expected_rows(matrix)}
    observed = {key(row): row for row in read_tsv(independence)}
    rows: list[dict[str, object]] = []
    for row_key, expected_row in sorted(expected.items()):
        observed_row = observed.get(row_key)
        add(rows, row_key, "present_in_independence_matrix", "PASS" if observed_row else "FAIL", str(independence))
        if not observed_row:
            continue
        for field in FIELDS:
            add(
                rows,
                row_key,
                f"field_matches.{field}",
                "PASS" if str(expected_row.get(field, "")) == observed_row.get(field, "") else "FAIL",
                f"expected={expected_row.get(field, '')} observed={observed_row.get(field, '')}",
            )
    for row_key in sorted(set(observed) - set(expected)):
        add(rows, row_key, "no_extra_independence_row", "FAIL", "row is not present in current convergence matrix")
    summary = read_json(summary_path)
    add(
        rows,
        "summary",
        "summary_matrix_row_count_matches",
        "PASS" if int(summary.get("n_matrix_rows", -1)) == len(expected) else "FAIL",
        f"summary={summary.get('n_matrix_rows', '')} expected={len(expected)}",
    )
    n_fail = sum(1 for row in rows if row["status"] != "PASS")
    outdir.mkdir(parents=True, exist_ok=True)
    write_tsv(outdir / "convergence_source_independence_freshness_lint.tsv", rows, ["row_key", "check", "status", "detail"])
    result = {
        "synthetic": False,
        "purpose": "V48 convergence source-independence freshness lint; synthesis/navigation only; no biological claim",
        "n_expected_rows": len(expected),
        "n_observed_rows": len(observed),
        "n_checks": len(rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
    }
    (outdir / "convergence_source_independence_freshness_lint_summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if n_fail == 0 or not fail_on_error else 2


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else ROOT / outdir
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    matrix = outdir / "synthetic_matrix.tsv"
    independence = outdir / "synthetic_independence.tsv"
    summary = outdir / "synthetic_summary.json"
    matrix_fields = ["grounded_finding_id", "external_record_id", "relationship_class", "synthesis_status", "external_source"]
    write_tsv(
        matrix,
        [
            {"grounded_finding_id": "A", "external_record_id": "E1", "relationship_class": "converges", "synthesis_status": "OK", "external_source": "https://example.org/source"},
            {"grounded_finding_id": "B", "external_record_id": "E2", "relationship_class": "converges", "synthesis_status": "OK", "external_source": "https://example.org/source/"},
        ],
        matrix_fields,
    )
    write_tsv(
        independence,
        [
            {"grounded_finding_id": "A", "external_record_id": "E1", "relationship_class": "converges", "synthesis_status": "OK", "external_source": "https://example.org/source", "canonical_source_url": "stale", "source_domain": "example.org", "canonical_source_row_count": "1", "source_independence_class": "single_row_source"},
            {"grounded_finding_id": "EXTRA", "external_record_id": "E3", "relationship_class": "converges", "synthesis_status": "OK", "external_source": "https://example.org/extra", "canonical_source_url": "https://example.org/extra", "source_domain": "example.org", "canonical_source_row_count": "1", "source_independence_class": "single_row_source"},
        ],
        FIELDS,
    )
    summary.write_text(json.dumps({"n_matrix_rows": 99}) + "\n")
    lint_out = outdir / "synthetic_lint"
    lint_independence(matrix, independence, summary, lint_out, fail_on_error=False)
    rows = read_tsv(lint_out / "convergence_source_independence_freshness_lint.tsv")
    checks = {
        "missing_row_fails": any(row["row_key"] == "B||E2" and row["check"] == "present_in_independence_matrix" and row["status"] == "FAIL" for row in rows),
        "stale_canonical_fails": any(row["row_key"] == "A||E1" and row["check"] == "field_matches.canonical_source_url" and row["status"] == "FAIL" for row in rows),
        "stale_group_count_fails": any(row["row_key"] == "A||E1" and row["check"] == "field_matches.canonical_source_row_count" and row["status"] == "FAIL" for row in rows),
        "extra_row_fails": any(row["row_key"] == "EXTRA||E3" and row["check"] == "no_extra_independence_row" and row["status"] == "FAIL" for row in rows),
        "bad_summary_count_fails": any(row["row_key"] == "summary" and row["check"] == "summary_matrix_row_count_matches" and row["status"] == "FAIL" for row in rows),
    }
    check_rows = [{"check": check, "status": "PASS" if ok else "FAIL"} for check, ok in checks.items()]
    write_tsv(outdir / "synthetic_convergence_source_independence_freshness_checks.tsv", check_rows, ["check", "status"])
    synth_summary = {
        "synthetic": True,
        "purpose": "V48 convergence source-independence freshness synthetic fixture; no biological claim",
        "n_checks": len(check_rows),
        "n_fail": sum(1 for row in check_rows if row["status"] != "PASS"),
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
    }
    (outdir / "synthetic_convergence_source_independence_freshness_summary.json").write_text(json.dumps(synth_summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(synth_summary, indent=2, sort_keys=True))
    return 0 if synth_summary["overall_status"] == "PASS" or not fail_on_error else 2


def main() -> int:
    args = parse_args()
    if args.command == "lint":
        return lint_independence(args.matrix, args.independence, args.summary, args.outdir, args.fail_on_error)
    if args.command == "synthetic-check":
        return synthetic_check(args.outdir, args.fail_on_error)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
