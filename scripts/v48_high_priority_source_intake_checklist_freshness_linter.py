#!/usr/bin/env python3
"""Check that the V48 high-priority source intake checklist is fresh."""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import shutil
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PLAN = ROOT / "knowledge_external/synthesis/high_priority_external_sourcing_plan_v48.tsv"
DEFAULT_QUERIES = ROOT / "knowledge_external/synthesis/high_priority_source_search_queries_v48.tsv"
DEFAULT_CHECKLIST = ROOT / "knowledge_external/templates/high_priority_source_intake_checklist_v48.tsv"
DEFAULT_SUMMARY = ROOT / "knowledge_external/catalogs/indexes/high_priority_source_intake_checklist_v48_summary.json"
DEFAULT_OUTDIR = ROOT / "analysis/v48_high_priority_source_intake_checklist_freshness_linter"
GENERATOR = ROOT / "scripts/v48_high_priority_source_intake_checklist.py"

FIELDS = [
    "rank",
    "item",
    "source_type_needed",
    "query_targets",
    "check_order",
    "check_id",
    "acceptance_criteria",
    "forbidden_shortcut",
    "required_before_matrix_entry",
    "boundary",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    lint = sub.add_parser("lint", help="Lint high-priority source intake checklist freshness")
    lint.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    lint.add_argument("--queries", type=Path, default=DEFAULT_QUERIES)
    lint.add_argument("--checklist", type=Path, default=DEFAULT_CHECKLIST)
    lint.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    lint.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    lint.add_argument("--fail-on-error", action="store_true")
    synth = sub.add_parser("synthetic-check", help="Run synthetic intake-checklist freshness fixtures")
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


def load_generator():
    spec = importlib.util.spec_from_file_location("v48_high_priority_source_intake_checklist", GENERATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not import intake checklist generator from {GENERATOR}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def expected_rows(plan: Path, queries: Path) -> list[dict[str, object]]:
    generator = load_generator()
    plan_rows = read_tsv(plan)
    targets_by_item = generator.query_targets(read_tsv(queries))
    rows: list[dict[str, object]] = []
    for plan_row in sorted(plan_rows, key=lambda row: int(row.get("rank", "999"))):
        item = plan_row.get("item", "")
        for step_order, step in enumerate(generator.CHECKLIST_STEPS, start=1):
            rows.append(
                {
                    "rank": plan_row.get("rank", ""),
                    "item": item,
                    "source_type_needed": plan_row.get("source_type_needed", ""),
                    "query_targets": targets_by_item.get(item, ""),
                    "check_order": step_order,
                    "check_id": step,
                    "acceptance_criteria": plan_row.get("acceptance_criteria", ""),
                    "forbidden_shortcut": plan_row.get("forbidden_shortcut", ""),
                    "required_before_matrix_entry": "yes",
                    "boundary": "intake checklist only; a checked source is still external until separately grounded",
                }
            )
    return rows


def row_key(row: dict[str, object]) -> str:
    return f"{row.get('rank', '')}||{row.get('item', '')}||{row.get('check_order', '')}||{row.get('check_id', '')}"


def add(rows: list[dict[str, object]], key: str, check: str, status: str, detail: str) -> None:
    rows.append({"row_key": key, "check": check, "status": status, "detail": detail})


def lint_checklist(plan: Path, queries: Path, checklist: Path, summary_path: Path, outdir: Path, fail_on_error: bool) -> int:
    expected_list = expected_rows(plan, queries)
    expected = {row_key(row): row for row in expected_list}
    observed = {row_key(row): row for row in read_tsv(checklist)}
    rows: list[dict[str, object]] = []
    for key, expected_row in sorted(expected.items(), key=lambda item: (int(item[1]["rank"] or 999), int(item[1]["check_order"] or 999))):
        observed_row = observed.get(key)
        add(rows, key, "checklist_row_present", "PASS" if observed_row else "FAIL", str(checklist))
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
        add(rows, key, "no_extra_checklist_row", "FAIL", "row is not expected from the current source plan and query packet")

    generator = load_generator()
    plan_rows = read_tsv(plan)
    source_type_counts = Counter(row.get("source_type_needed", "") for row in plan_rows)
    summary = read_json(summary_path)
    summary_expectations = {
        "n_plan_rows": len(plan_rows),
        "n_checklist_steps": len(generator.CHECKLIST_STEPS),
        "n_checklist_rows": len(expected_list),
        "source_type_counts": dict(sorted(source_type_counts.items())),
        "markdown": "knowledge_external/templates/HIGH_PRIORITY_SOURCE_INTAKE_CHECKLIST_V48.md",
        "tsv": "knowledge_external/templates/high_priority_source_intake_checklist_v48.tsv",
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
    write_tsv(outdir / "high_priority_source_intake_checklist_freshness_lint.tsv", rows, ["row_key", "check", "status", "detail"])
    result = {
        "synthetic": False,
        "purpose": "V48 high-priority source intake checklist freshness lint; template/navigation only; no biological claim",
        "n_expected_rows": len(expected_list),
        "n_observed_rows": len(observed),
        "n_checks": len(rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
    }
    (outdir / "high_priority_source_intake_checklist_freshness_lint_summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if n_fail == 0 or not fail_on_error else 2


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else ROOT / outdir
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    plan = outdir / "synthetic_plan.tsv"
    queries = outdir / "synthetic_queries.tsv"
    checklist = outdir / "synthetic_checklist.tsv"
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
    write_tsv(
        queries,
        [
            {"item": "Tool-robust but simple V22 scalar", "search_target": "PubMed/EuropePMC"},
            {"item": "Tool-robust but simple V22 scalar", "search_target": "GEO/ArrayExpress"},
            {"item": "GPR25 demoted from protected favorite", "search_target": "GWAS Catalog/OpenGWAS"},
        ],
        ["item", "search_target"],
    )
    expected = expected_rows(plan, queries)
    stale = [dict(expected[0])]
    stale[0]["query_targets"] = "stale"
    stale.append({field: "extra" for field in FIELDS})
    stale[-1]["rank"] = "99"
    stale[-1]["item"] = "Extra source item"
    stale[-1]["check_order"] = "99"
    stale[-1]["check_id"] = "extra_check"
    write_tsv(checklist, stale, FIELDS)
    summary.write_text(json.dumps({"n_plan_rows": 99, "n_checklist_steps": 99, "n_checklist_rows": 99, "source_type_counts": {"stale": 99}}) + "\n")
    lint_out = outdir / "synthetic_lint"
    lint_checklist(plan, queries, checklist, summary, lint_out, fail_on_error=False)
    rows = read_tsv(lint_out / "high_priority_source_intake_checklist_freshness_lint.tsv")
    first_key = row_key(expected[0])
    checks = {
        "missing_row_fails": any(row["check"] == "checklist_row_present" and row["status"] == "FAIL" for row in rows),
        "stale_query_targets_fails": any(row["row_key"] == first_key and row["check"] == "field_matches.query_targets" and row["status"] == "FAIL" for row in rows),
        "extra_row_fails": any(row["row_key"] == "99||Extra source item||99||extra_check" and row["check"] == "no_extra_checklist_row" and row["status"] == "FAIL" for row in rows),
        "bad_summary_count_fails": any(row["row_key"] == "summary" and row["check"] == "summary_matches.n_checklist_rows" and row["status"] == "FAIL" for row in rows),
    }
    check_rows = [{"check": check, "status": "PASS" if ok else "FAIL"} for check, ok in checks.items()]
    write_tsv(outdir / "synthetic_high_priority_source_intake_checklist_freshness_checks.tsv", check_rows, ["check", "status"])
    result = {
        "synthetic": True,
        "purpose": "V48 high-priority source intake checklist freshness synthetic fixture; no biological claim",
        "n_checks": len(check_rows),
        "n_fail": sum(1 for row in check_rows if row["status"] != "PASS"),
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
    }
    (outdir / "synthetic_high_priority_source_intake_checklist_freshness_summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["overall_status"] == "PASS" or not fail_on_error else 2


def main() -> int:
    args = parse_args()
    if args.command == "lint":
        return lint_checklist(args.plan, args.queries, args.checklist, args.summary, args.outdir, args.fail_on_error)
    if args.command == "synthetic-check":
        return synthetic_check(args.outdir, args.fail_on_error)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
