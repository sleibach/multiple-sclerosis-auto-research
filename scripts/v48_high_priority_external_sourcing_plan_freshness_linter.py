#!/usr/bin/env python3
"""Check that the V48 high-priority external sourcing plan is fresh."""

from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PRIORITY = ROOT / "knowledge_external/synthesis/v37_external_coverage_gap_priority_v48.tsv"
DEFAULT_PLAN = ROOT / "knowledge_external/synthesis/high_priority_external_sourcing_plan_v48.tsv"
DEFAULT_SUMMARY = ROOT / "knowledge_external/catalogs/indexes/high_priority_external_sourcing_plan_v48_summary.json"
DEFAULT_OUTDIR = ROOT / "analysis/v48_high_priority_external_sourcing_plan_freshness_linter"

FIELDS = [
    "rank",
    "item",
    "priority_score",
    "category",
    "evidence_grade",
    "source_type_needed",
    "search_route",
    "acceptance_criteria",
    "forbidden_shortcut",
    "safe_source_requirement",
    "source_integration_action",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    lint = sub.add_parser("lint", help="Lint high-priority external sourcing plan freshness")
    lint.add_argument("--priority", type=Path, default=DEFAULT_PRIORITY)
    lint.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
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


def route_for(row: dict[str, str]) -> tuple[str, str, str, str]:
    item = row.get("item", "").lower()
    category = row.get("category", "")
    rationale = row.get("rationale_class", "")
    if rationale == "method_specific_external_context_absent":
        return (
            "method/governance literature",
            "Search for methods papers, validation guidance, or target-interpretation standards matching the project procedure.",
            "Source must address the same methodological question, not broad MS biology.",
            "Do not use general disease-mechanism context as method corroboration.",
        )
    if "ibd" in item or "crohn" in item or "uc" in item:
        return (
            "IBD/MS transfer-specific literature or datasets",
            "Search for MS-IBD treatment-response, IFN/APC dynamics, or layer-specific transfer studies with matching definitions.",
            "Source must address the same disease-pair layer and direction, or provide a dataset route for future grounding.",
            "Do not count generic MS-IBD comorbidity or genetics context as response-layer corroboration.",
        )
    if "ebv" in item:
        return (
            "EBV-stratified immune-data source",
            "Search for EBV-stratified MS/control immune transcriptomic sources with specificity controls.",
            "Source must support a specificity-aware test route, not merely EBV-MS association context.",
            "Do not use broad EBV-risk literature to reopen a specificity-failed imprint.",
        )
    if "pregnancy" in item or "postpartum" in item or re.search(r"\bra\b", item) or "rheumatoid" in item:
        return (
            "pregnancy/postpartum comparator literature or datasets",
            "Search for pregnancy/postpartum immune-trajectory sources with APC-arm or treatment-response transfer information.",
            "Source must include matching timing, compartment, and disease-comparator definition.",
            "Do not use general relapse-course context as APC-arm corroboration.",
        )
    if "gpr25" in item or "mhc" in item:
        return (
            "locus/signal-specific genetics source",
            "Search for fine-mapping, colocalization, QTL, or signal-specific records matching the locus and direction.",
            "Source must address the same variant/gene/direction or provide importable summary-statistic/QTL data.",
            "Do not use catalog-level association existence as causal-direction corroboration.",
        )
    if category == "kills_closed" or category == "decoupling_negative":
        return (
            "same-failure-mode source",
            "Search for sources directly addressing the same negative result, direction conflict, or failed transfer mode.",
            "Source must match the project failure definition closely enough for convergence/contradiction classification.",
            "Do not add generic biological context to a closed/negative finding.",
        )
    return (
        "same-definition external source",
        "Search for a source or dataset directly overlapping the grounded finding definition.",
        "Source must overlap the same finding definition and preserve epistemic class labels.",
        "Do not infer convergence from broad adjacent context.",
    )


def expected_rows(priority: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for row in sorted([row for row in read_tsv(priority) if row.get("priority_tier") == "high"], key=lambda row: int(row.get("rank", "999"))):
        source_type, search_route, acceptance_criteria, forbidden_shortcut = route_for(row)
        rows.append(
            {
                "rank": row.get("rank", ""),
                "item": row.get("item", ""),
                "priority_score": row.get("priority_score", ""),
                "category": row.get("category", ""),
                "evidence_grade": row.get("evidence_grade", ""),
                "source_type_needed": source_type,
                "search_route": search_route,
                "acceptance_criteria": acceptance_criteria,
                "forbidden_shortcut": forbidden_shortcut,
                "safe_source_requirement": row.get("safe_source_requirement", ""),
                "source_integration_action": "If found, add as a segregated external record first; classify relationship in V48 matrix only after source-specific overlap review.",
            }
        )
    return rows


def key(row: dict[str, object]) -> str:
    return str(row.get("item", ""))


def add(rows: list[dict[str, object]], row_key: str, check: str, status: str, detail: str) -> None:
    rows.append({"row_key": row_key, "check": check, "status": status, "detail": detail})


def lint_plan(priority: Path, plan: Path, summary_path: Path, outdir: Path, fail_on_error: bool) -> int:
    expected = {key(row): row for row in expected_rows(priority)}
    observed = {key(row): row for row in read_tsv(plan)}
    rows: list[dict[str, object]] = []
    for row_key, expected_row in sorted(expected.items(), key=lambda item: int(item[1]["rank"])):
        observed_row = observed.get(row_key)
        add(rows, row_key, "present_in_sourcing_plan", "PASS" if observed_row else "FAIL", str(plan))
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
        add(rows, row_key, "no_extra_sourcing_plan_row", "FAIL", "row is not currently high priority")
    summary = read_json(summary_path)
    source_type_counts: dict[str, int] = {}
    for row in expected.values():
        source_type_counts[str(row["source_type_needed"])] = source_type_counts.get(str(row["source_type_needed"]), 0) + 1
    add(
        rows,
        "summary",
        "summary_plan_row_count_matches",
        "PASS" if int(summary.get("n_plan_rows", -1)) == len(expected) else "FAIL",
        f"expected={len(expected)} observed={summary.get('n_plan_rows', '')}",
    )
    add(
        rows,
        "summary",
        "summary_source_type_counts_match",
        "PASS" if summary.get("source_type_counts", {}) == dict(sorted(source_type_counts.items())) else "FAIL",
        f"expected={dict(sorted(source_type_counts.items()))} observed={summary.get('source_type_counts', {})}",
    )
    n_fail = sum(1 for row in rows if row["status"] != "PASS")
    outdir.mkdir(parents=True, exist_ok=True)
    write_tsv(outdir / "high_priority_external_sourcing_plan_freshness_lint.tsv", rows, ["row_key", "check", "status", "detail"])
    result = {
        "synthetic": False,
        "purpose": "V48 high-priority external sourcing plan freshness lint; future intake/navigation only; no biological claim",
        "n_expected_rows": len(expected),
        "n_observed_rows": len(observed),
        "n_checks": len(rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
    }
    (outdir / "high_priority_external_sourcing_plan_freshness_lint_summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if n_fail == 0 or not fail_on_error else 2


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else ROOT / outdir
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    priority = outdir / "synthetic_priority.tsv"
    plan = outdir / "synthetic_plan.tsv"
    summary = outdir / "synthetic_summary.json"
    priority_fields = ["rank", "item", "priority_score", "category", "evidence_grade", "rationale_class", "priority_tier", "safe_source_requirement"]
    write_tsv(
        priority,
        [
            {"rank": "1", "item": "EBV/IFN APC imprint downgraded by specificity control", "priority_score": "14", "category": "kills_closed", "evidence_grade": "negative-established", "rationale_class": "targeted_external_record_needed", "priority_tier": "high", "safe_source_requirement": "safe"},
            {"rank": "2", "item": "GPR25 demoted from protected favorite", "priority_score": "14", "category": "kills_closed", "evidence_grade": "negative-established", "rationale_class": "targeted_external_record_needed", "priority_tier": "high", "safe_source_requirement": "safe"},
        ],
        priority_fields,
    )
    expected = expected_rows(priority)
    stale = [dict(expected[0])]
    stale[0]["source_type_needed"] = "stale"
    stale.append({field: "extra" for field in FIELDS})
    stale[-1]["item"] = "Extra"
    write_tsv(plan, stale, FIELDS)
    summary.write_text(json.dumps({"n_plan_rows": 99, "source_type_counts": {"stale": 99}}) + "\n")
    lint_out = outdir / "synthetic_lint"
    lint_plan(priority, plan, summary, lint_out, fail_on_error=False)
    rows = read_tsv(lint_out / "high_priority_external_sourcing_plan_freshness_lint.tsv")
    checks = {
        "missing_row_fails": any(row["row_key"] == "GPR25 demoted from protected favorite" and row["check"] == "present_in_sourcing_plan" and row["status"] == "FAIL" for row in rows),
        "stale_route_fails": any(row["row_key"] == "EBV/IFN APC imprint downgraded by specificity control" and row["check"] == "field_matches.source_type_needed" and row["status"] == "FAIL" for row in rows),
        "extra_row_fails": any(row["row_key"] == "Extra" and row["check"] == "no_extra_sourcing_plan_row" and row["status"] == "FAIL" for row in rows),
        "bad_summary_count_fails": any(row["row_key"] == "summary" and row["check"] == "summary_plan_row_count_matches" and row["status"] == "FAIL" for row in rows),
    }
    check_rows = [{"check": check, "status": "PASS" if ok else "FAIL"} for check, ok in checks.items()]
    write_tsv(outdir / "synthetic_high_priority_external_sourcing_plan_freshness_checks.tsv", check_rows, ["check", "status"])
    synth_summary = {
        "synthetic": True,
        "purpose": "V48 high-priority external sourcing plan freshness synthetic fixture; no biological claim",
        "n_checks": len(check_rows),
        "n_fail": sum(1 for row in check_rows if row["status"] != "PASS"),
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
    }
    (outdir / "synthetic_high_priority_external_sourcing_plan_freshness_summary.json").write_text(json.dumps(synth_summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(synth_summary, indent=2, sort_keys=True))
    return 0 if synth_summary["overall_status"] == "PASS" or not fail_on_error else 2


def main() -> int:
    args = parse_args()
    if args.command == "lint":
        return lint_plan(args.priority, args.plan, args.summary, args.outdir, args.fail_on_error)
    if args.command == "synthetic-check":
        return synthetic_check(args.outdir, args.fail_on_error)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
