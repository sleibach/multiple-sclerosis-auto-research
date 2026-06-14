#!/usr/bin/env python3
"""Check that the V48 source-domain independence rollup is fresh."""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INDEPENDENCE = ROOT / "knowledge_external/synthesis/convergence_source_independence_v48.tsv"
DEFAULT_ROLLUP = ROOT / "knowledge_external/catalogs/indexes/source_domain_independence_rollup_v48.tsv"
DEFAULT_SUMMARY = ROOT / "knowledge_external/catalogs/indexes/source_domain_independence_rollup_v48_summary.json"
DEFAULT_OUTDIR = ROOT / "analysis/v48_source_domain_independence_freshness_linter"

FIELDS = [
    "source_domain",
    "matrix_rows",
    "canonical_source_clusters",
    "decision_relationship_rows",
    "convergence_rows",
    "contradiction_rows",
    "insufficient_overlap_rows",
    "relationship_counts",
    "synthesis_status_counts",
    "source_independence_classes",
    "canonical_source_urls",
    "grounded_findings",
    "interpretation_boundary",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    lint = sub.add_parser("lint", help="Lint source-domain independence rollup freshness")
    lint.add_argument("--independence", type=Path, default=DEFAULT_INDEPENDENCE)
    lint.add_argument("--rollup", type=Path, default=DEFAULT_ROLLUP)
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


def relationship_counts(rows: list[dict[str, str]], field: str) -> str:
    counts = Counter(row.get(field, "") for row in rows if row.get(field, ""))
    return ";".join(f"{key}:{value}" for key, value in sorted(counts.items()))


def interpretation_boundary(rows: list[dict[str, str]], canonical_count: int) -> str:
    has_decision = any(row.get("relationship_class") in {"converges", "contradicts"} for row in rows)
    has_convergence = any(row.get("relationship_class") == "converges" for row in rows)
    if has_decision and canonical_count == 1:
        if has_convergence:
            return "Decision-relevant convergence is present, but the domain contributes one canonical source cluster; do not count multiple rows as independent corroborations."
        return "Decision-relevant relationship is present, but the domain contributes one canonical source cluster."
    if has_decision:
        return "Decision-relevant relationship is spread across multiple canonical source clusters; still external context, not project evidence."
    return "Insufficient-overlap/resource context only; not external corroboration or contradiction."


def expected_rows(independence_path: Path) -> list[dict[str, object]]:
    rows = read_tsv(independence_path)
    by_domain: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_domain[row.get("source_domain", "")].append(row)
    expected: list[dict[str, object]] = []
    for domain, domain_rows in sorted(by_domain.items()):
        canonical_urls = sorted({row.get("canonical_source_url", "") for row in domain_rows if row.get("canonical_source_url")})
        grounded_findings = sorted({row.get("grounded_finding_id", "") for row in domain_rows if row.get("grounded_finding_id")})
        decision_rows = [row for row in domain_rows if row.get("relationship_class") in {"converges", "contradicts"}]
        convergence_rows = [row for row in domain_rows if row.get("relationship_class") == "converges"]
        contradiction_rows = [row for row in domain_rows if row.get("relationship_class") == "contradicts"]
        insufficient_rows = [row for row in domain_rows if row.get("relationship_class") == "insufficient-overlap"]
        expected.append(
            {
                "source_domain": domain,
                "matrix_rows": len(domain_rows),
                "canonical_source_clusters": len(canonical_urls),
                "decision_relationship_rows": len(decision_rows),
                "convergence_rows": len(convergence_rows),
                "contradiction_rows": len(contradiction_rows),
                "insufficient_overlap_rows": len(insufficient_rows),
                "relationship_counts": relationship_counts(domain_rows, "relationship_class"),
                "synthesis_status_counts": relationship_counts(domain_rows, "synthesis_status"),
                "source_independence_classes": relationship_counts(domain_rows, "source_independence_class"),
                "canonical_source_urls": ";".join(canonical_urls),
                "grounded_findings": ";".join(grounded_findings),
                "interpretation_boundary": interpretation_boundary(domain_rows, len(canonical_urls)),
            }
        )
    expected.sort(
        key=lambda row: (
            -int(row["decision_relationship_rows"]),
            -int(row["convergence_rows"]),
            -int(row["matrix_rows"]),
            str(row["source_domain"]),
        )
    )
    return expected


def add(rows: list[dict[str, object]], domain: str, check: str, status: str, detail: str) -> None:
    rows.append({"source_domain": domain, "check": check, "status": status, "detail": detail})


def lint_rollup(independence: Path, rollup: Path, summary_path: Path, outdir: Path, fail_on_error: bool) -> int:
    expected = {str(row["source_domain"]): row for row in expected_rows(independence)}
    observed = {row.get("source_domain", ""): row for row in read_tsv(rollup)}
    rows: list[dict[str, object]] = []
    for domain, expected_row in sorted(expected.items()):
        observed_row = observed.get(domain)
        add(rows, domain, "domain_present_in_rollup", "PASS" if observed_row else "FAIL", str(rollup))
        if not observed_row:
            continue
        for field in FIELDS:
            add(
                rows,
                domain,
                f"field_matches.{field}",
                "PASS" if str(expected_row.get(field, "")) == observed_row.get(field, "") else "FAIL",
                f"expected={expected_row.get(field, '')} observed={observed_row.get(field, '')}",
            )
    for domain in sorted(set(observed) - set(expected)):
        add(rows, domain, "no_extra_domain_rollup_row", "FAIL", "domain not present in current source-independence matrix")

    summary = read_json(summary_path)
    all_source_clusters = {
        row.get("canonical_source_url", "")
        for row in read_tsv(independence)
        if row.get("canonical_source_url")
    }
    decision_source_clusters = {
        row.get("canonical_source_url", "")
        for row in read_tsv(independence)
        if row.get("relationship_class") in {"converges", "contradicts"} and row.get("canonical_source_url")
    }
    summary_expectations = {
        "n_source_domains": len(expected),
        "n_matrix_rows": sum(int(row["matrix_rows"]) for row in expected.values()),
        "n_canonical_source_clusters": len(all_source_clusters),
        "n_decision_relationship_rows": sum(int(row["decision_relationship_rows"]) for row in expected.values()),
        "n_decision_canonical_source_clusters": len(decision_source_clusters),
        "n_domains_with_convergence": sum(1 for row in expected.values() if int(row["convergence_rows"]) > 0),
        "n_domains_with_contradiction": sum(1 for row in expected.values() if int(row["contradiction_rows"]) > 0),
    }
    for field, expected_value in summary_expectations.items():
        add(
            rows,
            "summary",
            f"summary_matches.{field}",
            "PASS" if str(summary.get(field, "")) == str(expected_value) else "FAIL",
            f"expected={expected_value} observed={summary.get(field, '')}",
        )

    n_fail = sum(1 for row in rows if row["status"] != "PASS")
    outdir.mkdir(parents=True, exist_ok=True)
    write_tsv(outdir / "source_domain_independence_freshness_lint.tsv", rows, ["source_domain", "check", "status", "detail"])
    result = {
        "synthetic": False,
        "purpose": "V48 source-domain independence rollup freshness lint; provenance/navigation only; no biological claim",
        "n_expected_domains": len(expected),
        "n_observed_domains": len(observed),
        "n_checks": len(rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
    }
    (outdir / "source_domain_independence_freshness_lint_summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if n_fail == 0 or not fail_on_error else 2


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else ROOT / outdir
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    independence = outdir / "synthetic_independence.tsv"
    rollup = outdir / "synthetic_rollup.tsv"
    summary = outdir / "synthetic_summary.json"
    write_tsv(
        independence,
        [
            {"source_domain": "example.org", "canonical_source_url": "https://example.org/a", "grounded_finding_id": "Finding A", "relationship_class": "converges", "synthesis_status": "OK", "source_independence_class": "single_row_source"},
            {"source_domain": "missing.example.org", "canonical_source_url": "https://missing.example.org/b", "grounded_finding_id": "Finding B", "relationship_class": "insufficient-overlap", "synthesis_status": "NO", "source_independence_class": "not_decision_relationship"},
        ],
        ["source_domain", "canonical_source_url", "grounded_finding_id", "relationship_class", "synthesis_status", "source_independence_class"],
    )
    expected = expected_rows(independence)
    stale_rows = [dict(expected[0])]
    stale_rows[0]["canonical_source_clusters"] = int(stale_rows[0]["canonical_source_clusters"]) + 1
    stale_rows.append(
        {
            "source_domain": "extra.example.org",
            "matrix_rows": 1,
            "canonical_source_clusters": 1,
            "decision_relationship_rows": 0,
            "convergence_rows": 0,
            "contradiction_rows": 0,
            "insufficient_overlap_rows": 1,
            "relationship_counts": "insufficient-overlap:1",
            "synthesis_status_counts": "NO:1",
            "source_independence_classes": "not_decision_relationship:1",
            "canonical_source_urls": "https://extra.example.org/x",
            "grounded_findings": "Extra",
            "interpretation_boundary": "stale",
        }
    )
    write_tsv(rollup, stale_rows, FIELDS)
    summary.write_text(json.dumps({"n_source_domains": 99, "n_matrix_rows": 99, "n_canonical_source_clusters": 99}) + "\n")
    lint_out = outdir / "synthetic_lint"
    lint_rollup(independence, rollup, summary, lint_out, fail_on_error=False)
    rows = read_tsv(lint_out / "source_domain_independence_freshness_lint.tsv")
    checks = {
        "missing_domain_fails": any(row["source_domain"] == "missing.example.org" and row["check"] == "domain_present_in_rollup" and row["status"] == "FAIL" for row in rows),
        "stale_canonical_cluster_count_fails": any(row["source_domain"] == "example.org" and row["check"] == "field_matches.canonical_source_clusters" and row["status"] == "FAIL" for row in rows),
        "extra_domain_fails": any(row["source_domain"] == "extra.example.org" and row["check"] == "no_extra_domain_rollup_row" and row["status"] == "FAIL" for row in rows),
        "bad_summary_count_fails": any(row["source_domain"] == "summary" and row["check"] == "summary_matches.n_source_domains" and row["status"] == "FAIL" for row in rows),
    }
    check_rows = [{"check": check, "status": "PASS" if ok else "FAIL"} for check, ok in checks.items()]
    write_tsv(outdir / "synthetic_source_domain_independence_freshness_checks.tsv", check_rows, ["check", "status"])
    synth_summary = {
        "synthetic": True,
        "purpose": "V48 source-domain independence freshness synthetic fixture; no biological claim",
        "n_checks": len(check_rows),
        "n_fail": sum(1 for row in check_rows if row["status"] != "PASS"),
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
    }
    (outdir / "synthetic_source_domain_independence_freshness_summary.json").write_text(json.dumps(synth_summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(synth_summary, indent=2, sort_keys=True))
    return 0 if synth_summary["overall_status"] == "PASS" or not fail_on_error else 2


def main() -> int:
    args = parse_args()
    if args.command == "lint":
        return lint_rollup(args.independence, args.rollup, args.summary, args.outdir, args.fail_on_error)
    if args.command == "synthetic-check":
        return synthetic_check(args.outdir, args.fail_on_error)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
