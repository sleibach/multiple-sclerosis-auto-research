#!/usr/bin/env python3
"""Check that the V48 high-priority source-search query packet is fresh."""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PLAN = ROOT / "knowledge_external/synthesis/high_priority_external_sourcing_plan_v48.tsv"
DEFAULT_QUERIES = ROOT / "knowledge_external/synthesis/high_priority_source_search_queries_v48.tsv"
DEFAULT_SUMMARY = ROOT / "knowledge_external/catalogs/indexes/high_priority_source_search_queries_v48_summary.json"
DEFAULT_OUTDIR = ROOT / "analysis/v48_high_priority_source_search_query_freshness_linter"
QUERY_BUILDER = ROOT / "scripts/v48_high_priority_source_search_queries.py"

FIELDS = [
    "rank",
    "item",
    "source_type_needed",
    "search_target",
    "query",
    "acceptance_criteria",
    "forbidden_shortcut",
    "integration_boundary",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    lint = sub.add_parser("lint", help="Lint high-priority source-search query freshness")
    lint.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    lint.add_argument("--queries", type=Path, default=DEFAULT_QUERIES)
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


def load_query_builder():
    spec = importlib.util.spec_from_file_location("v48_high_priority_source_search_queries", QUERY_BUILDER)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not import query builder from {QUERY_BUILDER}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def expected_rows(plan_path: Path) -> list[dict[str, object]]:
    builder = load_query_builder()
    rows: list[dict[str, object]] = []
    for plan in read_tsv(plan_path):
        for target in builder.target_repositories(plan.get("source_type_needed", "")):
            rows.append(
                {
                    "rank": plan.get("rank", ""),
                    "item": plan.get("item", ""),
                    "source_type_needed": plan.get("source_type_needed", ""),
                    "search_target": target,
                    "query": builder.query_for(plan, target),
                    "acceptance_criteria": plan.get("acceptance_criteria", ""),
                    "forbidden_shortcut": plan.get("forbidden_shortcut", ""),
                    "integration_boundary": "Search results are candidates only; no claim enters the project without V47 segregated-record intake and V48 overlap review.",
                }
            )
    return rows


def row_key(row: dict[str, object]) -> str:
    return f"{row.get('rank', '')}||{row.get('item', '')}||{row.get('search_target', '')}"


def add(rows: list[dict[str, object]], key: str, check: str, status: str, detail: str) -> None:
    rows.append({"row_key": key, "check": check, "status": status, "detail": detail})


def lint_queries(plan: Path, queries: Path, summary_path: Path, outdir: Path, fail_on_error: bool) -> int:
    expected = {row_key(row): row for row in expected_rows(plan)}
    observed = {row_key(row): row for row in read_tsv(queries)}
    rows: list[dict[str, object]] = []
    for key, expected_row in sorted(expected.items(), key=lambda item: (int(item[1]["rank"] or 999), str(item[1]["search_target"]))):
        observed_row = observed.get(key)
        add(rows, key, "present_in_query_packet", "PASS" if observed_row else "FAIL", str(queries))
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
        add(rows, key, "no_extra_query_row", "FAIL", "row is not expected from the current sourcing plan")
    summary = read_json(summary_path)
    target_counts: dict[str, int] = {}
    for row in expected.values():
        target = str(row["search_target"])
        target_counts[target] = target_counts.get(target, 0) + 1
    summary_expectations = {
        "n_plan_rows": len(read_tsv(plan)),
        "n_query_rows": len(expected),
        "target_counts": dict(sorted(target_counts.items())),
    }
    for field, expected_value in summary_expectations.items():
        add(
            rows,
            "summary",
            f"summary_matches.{field}",
            "PASS" if summary.get(field, "") == expected_value else "FAIL",
            f"expected={expected_value} observed={summary.get(field, '')}",
        )
    n_fail = sum(1 for row in rows if row["status"] != "PASS")
    outdir.mkdir(parents=True, exist_ok=True)
    write_tsv(outdir / "high_priority_source_search_query_freshness_lint.tsv", rows, ["row_key", "check", "status", "detail"])
    result = {
        "synthetic": False,
        "purpose": "V48 high-priority source-search query freshness lint; future search/navigation only; no biological claim",
        "n_expected_rows": len(expected),
        "n_observed_rows": len(observed),
        "n_checks": len(rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
    }
    (outdir / "high_priority_source_search_query_freshness_lint_summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if n_fail == 0 or not fail_on_error else 2


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else ROOT / outdir
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    plan = outdir / "synthetic_plan.tsv"
    queries = outdir / "synthetic_queries.tsv"
    summary = outdir / "synthetic_summary.json"
    write_tsv(
        plan,
        [
            {
                "rank": "1",
                "item": "Tool-robust but simple V22 scalar",
                "source_type_needed": "method/governance literature",
                "acceptance_criteria": "method-specific",
                "forbidden_shortcut": "no broad context",
            },
            {
                "rank": "2",
                "item": "GPR25 demoted from protected favorite",
                "source_type_needed": "locus/signal-specific genetics source",
                "acceptance_criteria": "same locus/direction",
                "forbidden_shortcut": "no broad association",
            },
        ],
        ["rank", "item", "source_type_needed", "acceptance_criteria", "forbidden_shortcut"],
    )
    expected = expected_rows(plan)
    stale = [dict(expected[0])]
    stale[0]["query"] = "V22 stale internal label"
    stale.append({field: "extra" for field in FIELDS})
    stale[-1]["rank"] = "99"
    stale[-1]["item"] = "Extra"
    stale[-1]["search_target"] = "PubMed/EuropePMC"
    write_tsv(queries, stale, FIELDS)
    summary.write_text(json.dumps({"n_plan_rows": 99, "n_query_rows": 99, "target_counts": {"stale": 99}}) + "\n")
    lint_out = outdir / "synthetic_lint"
    lint_queries(plan, queries, summary, lint_out, fail_on_error=False)
    rows = read_tsv(lint_out / "high_priority_source_search_query_freshness_lint.tsv")
    checks = {
        "missing_row_fails": any(row["row_key"].startswith("2||GPR25 demoted") and row["check"] == "present_in_query_packet" and row["status"] == "FAIL" for row in rows),
        "stale_query_fails": any(row["row_key"].startswith("1||Tool-robust") and row["check"] == "field_matches.query" and row["status"] == "FAIL" for row in rows),
        "extra_row_fails": any(row["row_key"] == "99||Extra||PubMed/EuropePMC" and row["check"] == "no_extra_query_row" and row["status"] == "FAIL" for row in rows),
        "bad_summary_count_fails": any(row["row_key"] == "summary" and row["check"] == "summary_matches.n_query_rows" and row["status"] == "FAIL" for row in rows),
    }
    check_rows = [{"check": check, "status": "PASS" if ok else "FAIL"} for check, ok in checks.items()]
    write_tsv(outdir / "synthetic_high_priority_source_search_query_freshness_checks.tsv", check_rows, ["check", "status"])
    result = {
        "synthetic": True,
        "purpose": "V48 high-priority source-search query freshness synthetic fixture; no biological claim",
        "n_checks": len(check_rows),
        "n_fail": sum(1 for row in check_rows if row["status"] != "PASS"),
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
    }
    (outdir / "synthetic_high_priority_source_search_query_freshness_summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["overall_status"] == "PASS" or not fail_on_error else 2


def main() -> int:
    args = parse_args()
    if args.command == "lint":
        return lint_queries(args.plan, args.queries, args.summary, args.outdir, args.fail_on_error)
    if args.command == "synthetic-check":
        return synthetic_check(args.outdir, args.fail_on_error)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
