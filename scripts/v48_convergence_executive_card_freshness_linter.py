#!/usr/bin/env python3
"""Check that the V48 convergence/contradiction executive card is fresh."""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CARD = ROOT / "knowledge_external/synthesis/convergence_contradiction_executive_card_v48.tsv"
DEFAULT_SUMMARY = ROOT / "knowledge_external/catalogs/indexes/convergence_contradiction_executive_card_v48_summary.json"
DEFAULT_OUTDIR = ROOT / "analysis/v48_convergence_executive_card_freshness_linter"
SUMMARIES = {
    "matrix": ROOT / "knowledge_external/catalogs/indexes/convergence_contradiction_v48_summary.json",
    "source_independence": ROOT / "knowledge_external/catalogs/indexes/convergence_source_independence_v48_summary.json",
    "domain_independence": ROOT / "knowledge_external/catalogs/indexes/source_domain_independence_rollup_v48_summary.json",
    "gap_priority": ROOT / "knowledge_external/catalogs/indexes/v37_external_coverage_gap_priority_v48_summary.json",
    "preflight": ROOT / "analysis/v48_governance_preflight/v48_governance_preflight_summary.json",
}
DECISION_TSV = ROOT / "knowledge_external/synthesis/decision_relevant_convergences_v48.tsv"
GAP_TSV = ROOT / "knowledge_external/synthesis/v37_external_coverage_gap_priority_v48.tsv"

FIELDS = ["section", "metric", "value", "boundary"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    lint = sub.add_parser("lint", help="Lint executive-card freshness")
    lint.add_argument("--card", type=Path, default=DEFAULT_CARD)
    lint.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    lint.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    lint.add_argument("--fail-on-error", action="store_true")
    synth = sub.add_parser("synthetic-check", help="Run synthetic freshness fixtures")
    synth.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    synth.add_argument("--fail-on-error", action="store_true")
    return parser.parse_args()


def read_json(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text())
    return data if isinstance(data, dict) else {}


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


def expected_card_rows(summaries: dict[str, dict[str, object]]) -> list[dict[str, object]]:
    return [
        {"section": "relationship_counts", "metric": "V48 matrix rows", "value": summaries["matrix"].get("n_rows", ""), "boundary": "External relationship rows are context, not evidence."},
        {"section": "relationship_counts", "metric": "convergence rows", "value": summaries["matrix"].get("n_converges", ""), "boundary": "Convergence corroborates context; grounded artifacts remain evidence."},
        {"section": "relationship_counts", "metric": "contradiction rows", "value": summaries["matrix"].get("n_contradicts", ""), "boundary": "Contradictions would flag future grounding, not override grounded findings."},
        {"section": "source_independence", "metric": "decision canonical source clusters", "value": summaries["source_independence"].get("n_decision_canonical_sources", ""), "boundary": "Same canonical source cluster is not multiple independent corroborations."},
        {"section": "source_independence", "metric": "domains with convergence", "value": summaries["domain_independence"].get("n_domains_with_convergence", ""), "boundary": "Domain concentration limits external-source independence."},
        {"section": "coverage_gaps", "metric": "V37 uncovered priority rows", "value": summaries["gap_priority"].get("n_priority_rows", ""), "boundary": "Sourcing priority is not validation or convergence."},
        {"section": "coverage_gaps", "metric": "high-priority V37 sourcing gaps", "value": summaries["gap_priority"].get("n_high_priority", ""), "boundary": "Only same-definition external sources should be added."},
        {"section": "governance", "metric": "preflight checks", "value": summaries["preflight"].get("n_checks", ""), "boundary": "Preflight checks provenance/navigation controls only."},
        {"section": "governance", "metric": "preflight failures", "value": summaries["preflight"].get("n_fail", ""), "boundary": "Zero failures means the segregation controls passed."},
    ]


def row_key(row: dict[str, object]) -> str:
    return f"{row.get('section', '')}||{row.get('metric', '')}"


def add(rows: list[dict[str, object]], row_key_value: str, check: str, status: str, detail: str) -> None:
    rows.append({"row_key": row_key_value, "check": check, "status": status, "detail": detail})


def lint_card(card: Path, summary_path: Path, outdir: Path, fail_on_error: bool) -> int:
    summaries = {name: read_json(path) for name, path in SUMMARIES.items()}
    expected = {row_key(row): row for row in expected_card_rows(summaries)}
    observed = {row_key(row): row for row in read_tsv(card)}
    rows: list[dict[str, object]] = []
    for key, expected_row in sorted(expected.items()):
        observed_row = observed.get(key)
        add(rows, key, "metric_present_in_card", "PASS" if observed_row else "FAIL", str(card))
        if not observed_row:
            continue
        for field in FIELDS:
            add(
                rows,
                key,
                f"field_matches.{field}",
                "PASS" if str(expected_row.get(field, "")) == observed_row.get(field, "") else "FAIL",
                f"expected={expected_row.get(field, '')} observed={observed_row.get(field, '')}",
            )
    for key in sorted(set(observed) - set(expected)):
        add(rows, key, "no_extra_card_metric", "FAIL", "metric is not expected from current summaries")

    summary = read_json(summary_path)
    high_gap_rows = [row for row in read_tsv(GAP_TSV) if row.get("priority_tier") == "high"]
    summary_expectations = {
        "n_card_metrics": len(expected),
        "n_decision_rows": len(read_tsv(DECISION_TSV)),
        "n_high_priority_gap_rows": len(high_gap_rows),
        "n_convergence_rows": summaries["matrix"].get("n_converges", 0),
        "n_contradiction_rows": summaries["matrix"].get("n_contradicts", 0),
        "n_decision_canonical_source_clusters": summaries["source_independence"].get("n_decision_canonical_sources", 0),
        "governance_preflight_status": summaries["preflight"].get("overall_status", ""),
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
    write_tsv(outdir / "convergence_executive_card_freshness_lint.tsv", rows, ["row_key", "check", "status", "detail"])
    result = {
        "synthetic": False,
        "purpose": "V48 convergence executive-card freshness lint; synthesis/navigation only; no biological claim",
        "n_expected_metrics": len(expected),
        "n_observed_metrics": len(observed),
        "n_checks": len(rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
    }
    (outdir / "convergence_executive_card_freshness_lint_summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if n_fail == 0 or not fail_on_error else 2


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else ROOT / outdir
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    card = outdir / "synthetic_card.tsv"
    summary = outdir / "synthetic_summary.json"
    observed = [{"section": "relationship_counts", "metric": "V48 matrix rows", "value": "stale", "boundary": "External relationship rows are context, not evidence."}]
    observed.append({"section": "extra", "metric": "extra", "value": "1", "boundary": "stale"})
    write_tsv(card, observed, FIELDS)
    summary.write_text(json.dumps({"n_card_metrics": 99, "n_decision_rows": 99, "governance_preflight_status": "STALE"}) + "\n")
    lint_out = outdir / "synthetic_lint"
    lint_card(card, summary, lint_out, fail_on_error=False)
    rows = read_tsv(lint_out / "convergence_executive_card_freshness_lint.tsv")
    checks = {
        "missing_metric_fails": any(row["check"] == "metric_present_in_card" and row["status"] == "FAIL" for row in rows),
        "stale_metric_value_fails": any(row["row_key"] == "relationship_counts||V48 matrix rows" and row["check"] == "field_matches.value" and row["status"] == "FAIL" for row in rows),
        "extra_metric_fails": any(row["row_key"] == "extra||extra" and row["check"] == "no_extra_card_metric" and row["status"] == "FAIL" for row in rows),
        "bad_summary_count_fails": any(row["row_key"] == "summary" and row["check"] == "summary_matches.n_card_metrics" and row["status"] == "FAIL" for row in rows),
    }
    check_rows = [{"check": check, "status": "PASS" if ok else "FAIL"} for check, ok in checks.items()]
    write_tsv(outdir / "synthetic_convergence_executive_card_freshness_checks.tsv", check_rows, ["check", "status"])
    synth_summary = {
        "synthetic": True,
        "purpose": "V48 convergence executive-card freshness synthetic fixture; no biological claim",
        "n_checks": len(check_rows),
        "n_fail": sum(1 for row in check_rows if row["status"] != "PASS"),
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
    }
    (outdir / "synthetic_convergence_executive_card_freshness_summary.json").write_text(json.dumps(synth_summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(synth_summary, indent=2, sort_keys=True))
    return 0 if synth_summary["overall_status"] == "PASS" or not fail_on_error else 2


def main() -> int:
    args = parse_args()
    if args.command == "lint":
        return lint_card(args.card, args.summary, args.outdir, args.fail_on_error)
    if args.command == "synthetic-check":
        return synthetic_check(args.outdir, args.fail_on_error)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
