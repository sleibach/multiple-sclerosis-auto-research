#!/usr/bin/env python3
"""Check that the V37 external coverage gap priority map is fresh."""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_COVERAGE = ROOT / "knowledge_external/synthesis/v37_finding_external_coverage_v48.tsv"
DEFAULT_RATIONALE = ROOT / "knowledge_external/synthesis/v37_uncovered_finding_rationale_v48.tsv"
DEFAULT_PRIORITY = ROOT / "knowledge_external/synthesis/v37_external_coverage_gap_priority_v48.tsv"
DEFAULT_SUMMARY = ROOT / "knowledge_external/catalogs/indexes/v37_external_coverage_gap_priority_v48_summary.json"
DEFAULT_OUTDIR = ROOT / "analysis/v48_v37_gap_priority_freshness_linter"

FIELDS = [
    "rank",
    "item",
    "category",
    "relevance",
    "novelty",
    "evidence_grade",
    "rationale_class",
    "priority_score",
    "priority_tier",
    "priority_reason",
    "safe_source_requirement",
    "supporting_artifact",
    "status",
    "next_action",
]

EVIDENCE_WEIGHTS = {
    "robust": 3,
    "supported": 2,
    "negative-established": 2,
    "provisional": 1,
    "speculative": 0,
}

RATIONALE_WEIGHTS = {
    "no_relevant_external_record_imported": 3,
    "targeted_external_record_needed": 2,
    "method_specific_external_context_absent": 1,
    "avoid_false_corroboration": 0,
}

CATEGORY_WEIGHTS = {
    "positive_supported": 2,
    "decoupling_negative": 2,
    "kills_closed": 1,
    "methodological": 1,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    lint = sub.add_parser("lint", help="Lint V37 gap-priority freshness")
    lint.add_argument("--coverage", type=Path, default=DEFAULT_COVERAGE)
    lint.add_argument("--rationale", type=Path, default=DEFAULT_RATIONALE)
    lint.add_argument("--priority", type=Path, default=DEFAULT_PRIORITY)
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


def to_int(value: str) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def priority_tier(score: int) -> str:
    if score >= 14:
        return "high"
    if score >= 10:
        return "medium"
    return "low"


def priority_reason(row: dict[str, object]) -> str:
    return "; ".join(
        [
            f"relevance {row['relevance']}",
            f"novelty {row['novelty']}",
            f"evidence {row['evidence_grade']}",
            f"rationale {row['rationale_class']}",
        ]
    )


def safe_source_requirement(row: dict[str, object]) -> str:
    category = str(row["category"])
    rationale = str(row["rationale_class"])
    if rationale == "avoid_false_corroboration":
        return "Do not add broad context; require a concrete predefined dataset/test source before queueing external-verifiable work."
    if category == "methodological":
        return "Require a method-specific source about the same procedure or governance issue; broad disease biology is not sufficient."
    if category in {"decoupling_negative", "kills_closed"}:
        return "Require a source that addresses the same direction, locus, failure mode, or definition; generic disease context is insufficient."
    return "Require a source directly overlapping the grounded finding before adding a V48 relationship row."


def expected_rows(coverage_path: Path, rationale_path: Path) -> list[dict[str, object]]:
    coverage_rows = read_tsv(coverage_path)
    rationale_by_item = {row.get("item", ""): row for row in read_tsv(rationale_path)}
    rows: list[dict[str, object]] = []
    for coverage in coverage_rows:
        if coverage.get("v48_coverage") != "no_v48_external_relationship_row":
            continue
        item = coverage.get("item", "")
        rationale = rationale_by_item.get(item, {})
        relevance = to_int(coverage.get("relevance", ""))
        novelty = to_int(coverage.get("novelty", ""))
        evidence = coverage.get("evidence_grade", "")
        category = coverage.get("category", "")
        rationale_class = rationale.get("rationale_class", "missing_rationale")
        score = (
            relevance * 2
            + novelty
            + EVIDENCE_WEIGHTS.get(evidence, 0)
            + RATIONALE_WEIGHTS.get(rationale_class, 0)
            + CATEGORY_WEIGHTS.get(category, 0)
        )
        row: dict[str, object] = {
            "rank": 0,
            "item": item,
            "category": category,
            "relevance": relevance,
            "novelty": novelty,
            "evidence_grade": evidence,
            "rationale_class": rationale_class,
            "priority_score": score,
            "priority_tier": priority_tier(score),
            "priority_reason": "",
            "safe_source_requirement": "",
            "supporting_artifact": coverage.get("supporting_artifact", ""),
            "status": coverage.get("status", ""),
            "next_action": rationale.get("next_action", ""),
        }
        row["priority_reason"] = priority_reason(row)
        row["safe_source_requirement"] = safe_source_requirement(row)
        rows.append(row)
    rows.sort(
        key=lambda row: (
            -int(row["priority_score"]),
            -int(row["relevance"]),
            -int(row["novelty"]),
            str(row["item"]),
        )
    )
    for index, row in enumerate(rows, start=1):
        row["rank"] = index
    return rows


def key(row: dict[str, object]) -> str:
    return str(row.get("item", ""))


def add(rows: list[dict[str, object]], row_key: str, check: str, status: str, detail: str) -> None:
    rows.append({"row_key": row_key, "check": check, "status": status, "detail": detail})


def lint_priority(coverage: Path, rationale: Path, priority: Path, summary_path: Path, outdir: Path, fail_on_error: bool) -> int:
    expected = {key(row): row for row in expected_rows(coverage, rationale)}
    observed = {key(row): row for row in read_tsv(priority)}
    rows: list[dict[str, object]] = []
    for row_key, expected_row in sorted(expected.items(), key=lambda item: int(item[1]["rank"])):
        observed_row = observed.get(row_key)
        add(rows, row_key, "present_in_priority_map", "PASS" if observed_row else "FAIL", str(priority))
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
        add(rows, row_key, "no_extra_priority_row", "FAIL", "row is not present in current uncovered V37 coverage set")

    summary = read_json(summary_path)
    tier_counts = Counter(str(row["priority_tier"]) for row in expected.values())
    high_priority = sorted(str(row["item"]) for row in expected.values() if row["priority_tier"] == "high")
    add(
        rows,
        "summary",
        "summary_priority_row_count_matches",
        "PASS" if int(summary.get("n_priority_rows", -1)) == len(expected) else "FAIL",
        f"summary={summary.get('n_priority_rows', '')} expected={len(expected)}",
    )
    add(
        rows,
        "summary",
        "summary_high_priority_count_matches",
        "PASS" if int(summary.get("n_high_priority", -1)) == len(high_priority) else "FAIL",
        f"summary={summary.get('n_high_priority', '')} expected={len(high_priority)}",
    )
    add(
        rows,
        "summary",
        "summary_tier_counts_match",
        "PASS" if summary.get("tier_counts", {}) == dict(sorted(tier_counts.items())) else "FAIL",
        f"summary={summary.get('tier_counts', {})} expected={dict(sorted(tier_counts.items()))}",
    )
    summary_items = sorted(str(item) for item in summary.get("high_priority_items", []))
    add(
        rows,
        "summary",
        "summary_high_priority_items_match",
        "PASS" if summary_items == high_priority else "FAIL",
        f"summary={summary_items} expected={high_priority}",
    )

    n_fail = sum(1 for row in rows if row["status"] != "PASS")
    outdir.mkdir(parents=True, exist_ok=True)
    write_tsv(outdir / "v37_gap_priority_freshness_lint.tsv", rows, ["row_key", "check", "status", "detail"])
    result = {
        "synthetic": False,
        "purpose": "V48 V37 external coverage gap priority freshness lint; sourcing/navigation only; no biological claim",
        "n_expected_rows": len(expected),
        "n_observed_rows": len(observed),
        "n_high_priority": len(high_priority),
        "n_checks": len(rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
    }
    (outdir / "v37_gap_priority_freshness_lint_summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if n_fail == 0 or not fail_on_error else 2


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else ROOT / outdir
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    coverage = outdir / "synthetic_coverage.tsv"
    rationale = outdir / "synthetic_rationale.tsv"
    priority = outdir / "synthetic_priority.tsv"
    summary = outdir / "synthetic_summary.json"
    write_tsv(
        coverage,
        [
            {"item": "High", "category": "positive_supported", "relevance": "5", "novelty": "4", "evidence_grade": "supported", "supporting_artifact": "artifact", "status": "status", "v48_coverage": "no_v48_external_relationship_row"},
            {"item": "Medium", "category": "kills_closed", "relevance": "2", "novelty": "2", "evidence_grade": "negative-established", "supporting_artifact": "artifact", "status": "status", "v48_coverage": "no_v48_external_relationship_row"},
        ],
        ["item", "category", "relevance", "novelty", "evidence_grade", "supporting_artifact", "status", "v48_coverage"],
    )
    write_tsv(
        rationale,
        [
            {"item": "High", "rationale_class": "no_relevant_external_record_imported", "next_action": "next"},
            {"item": "Medium", "rationale_class": "targeted_external_record_needed", "next_action": "next"},
        ],
        ["item", "rationale_class", "next_action"],
    )
    expected = expected_rows(coverage, rationale)
    stale_rows = [dict(row) for row in expected[:1]]
    stale_rows[0]["priority_score"] = int(stale_rows[0]["priority_score"]) - 1
    stale_rows.append(
        {
            "rank": 99,
            "item": "Extra",
            "category": "methodological",
            "relevance": 1,
            "novelty": 1,
            "evidence_grade": "supported",
            "rationale_class": "method_specific_external_context_absent",
            "priority_score": 99,
            "priority_tier": "high",
            "priority_reason": "stale",
            "safe_source_requirement": "stale",
            "supporting_artifact": "stale",
            "status": "stale",
            "next_action": "stale",
        }
    )
    write_tsv(priority, stale_rows, FIELDS)
    summary.write_text(json.dumps({"n_priority_rows": 99, "n_high_priority": 99, "tier_counts": {"high": 99}, "high_priority_items": ["Extra"]}) + "\n")
    lint_out = outdir / "synthetic_lint"
    lint_priority(coverage, rationale, priority, summary, lint_out, fail_on_error=False)
    rows = read_tsv(lint_out / "v37_gap_priority_freshness_lint.tsv")
    checks = {
        "missing_row_fails": any(row["row_key"] == "Medium" and row["check"] == "present_in_priority_map" and row["status"] == "FAIL" for row in rows),
        "stale_score_fails": any(row["row_key"] == "High" and row["check"] == "field_matches.priority_score" and row["status"] == "FAIL" for row in rows),
        "extra_row_fails": any(row["row_key"] == "Extra" and row["check"] == "no_extra_priority_row" and row["status"] == "FAIL" for row in rows),
        "bad_summary_count_fails": any(row["row_key"] == "summary" and row["check"] == "summary_priority_row_count_matches" and row["status"] == "FAIL" for row in rows),
        "bad_summary_high_items_fail": any(row["row_key"] == "summary" and row["check"] == "summary_high_priority_items_match" and row["status"] == "FAIL" for row in rows),
    }
    check_rows = [{"check": check, "status": "PASS" if ok else "FAIL"} for check, ok in checks.items()]
    write_tsv(outdir / "synthetic_v37_gap_priority_freshness_checks.tsv", check_rows, ["check", "status"])
    synth_summary = {
        "synthetic": True,
        "purpose": "V48 V37 external coverage gap priority freshness synthetic fixture; no biological claim",
        "n_checks": len(check_rows),
        "n_fail": sum(1 for row in check_rows if row["status"] != "PASS"),
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
    }
    (outdir / "synthetic_v37_gap_priority_freshness_summary.json").write_text(json.dumps(synth_summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(synth_summary, indent=2, sort_keys=True))
    return 0 if synth_summary["overall_status"] == "PASS" or not fail_on_error else 2


def main() -> int:
    args = parse_args()
    if args.command == "lint":
        return lint_priority(args.coverage, args.rationale, args.priority, args.summary, args.outdir, args.fail_on_error)
    if args.command == "synthetic-check":
        return synthetic_check(args.outdir, args.fail_on_error)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
