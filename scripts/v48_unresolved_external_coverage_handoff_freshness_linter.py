#!/usr/bin/env python3
"""Check that the V48 unresolved external coverage handoff is fresh."""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import shutil
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PRIORITY = ROOT / "knowledge_external/synthesis/v37_external_coverage_gap_priority_v48.tsv"
DEFAULT_PLAN = ROOT / "knowledge_external/synthesis/high_priority_external_sourcing_plan_v48.tsv"
DEFAULT_QUERIES = ROOT / "knowledge_external/synthesis/high_priority_source_search_queries_v48.tsv"
DEFAULT_FUTURE = ROOT / "knowledge_external/synthesis/future_grounding_queue_v48.tsv"
DEFAULT_SURVEILLANCE = ROOT / "knowledge_external/synthesis/contradiction_surveillance_checklist_v48.tsv"
DEFAULT_HANDOFF = ROOT / "knowledge_external/synthesis/unresolved_external_coverage_handoff_v48.tsv"
DEFAULT_SUMMARY = ROOT / "knowledge_external/catalogs/indexes/unresolved_external_coverage_handoff_v48_summary.json"
DEFAULT_OUTDIR = ROOT / "analysis/v48_unresolved_external_coverage_handoff_freshness_linter"
GENERATOR = ROOT / "scripts/v48_unresolved_external_coverage_handoff.py"

FIELDS = ["action_id", "action_type", "priority", "item", "source_artifact", "input_rows", "next_step", "boundary"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    lint = sub.add_parser("lint", help="Lint unresolved external coverage handoff freshness")
    lint.add_argument("--priority", type=Path, default=DEFAULT_PRIORITY)
    lint.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    lint.add_argument("--queries", type=Path, default=DEFAULT_QUERIES)
    lint.add_argument("--future", type=Path, default=DEFAULT_FUTURE)
    lint.add_argument("--surveillance", type=Path, default=DEFAULT_SURVEILLANCE)
    lint.add_argument("--handoff", type=Path, default=DEFAULT_HANDOFF)
    lint.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    lint.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    lint.add_argument("--fail-on-error", action="store_true")
    synth = sub.add_parser("synthetic-check", help="Run synthetic handoff freshness fixtures")
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
    spec = importlib.util.spec_from_file_location("v48_unresolved_external_coverage_handoff", GENERATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not import unresolved handoff generator from {GENERATOR}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def expected_rows(priority: Path, plan: Path, queries: Path, future: Path, surveillance: Path) -> list[dict[str, object]]:
    generator = load_generator()
    priority_rows = generator.read_tsv(priority)
    plan_rows = generator.read_tsv(plan)
    query_info = generator.query_counts(generator.read_tsv(queries))
    future_rows = generator.read_tsv(future)
    surveillance_rows = generator.read_tsv(surveillance)
    rows: list[dict[str, object]] = []
    action_index = 1
    for row in sorted(priority_rows, key=lambda row: int(row.get("rank", "999"))):
        if row.get("priority_tier", "") != "high":
            continue
        info = query_info.get(row.get("item", ""), {"n_queries": 0, "targets": ""})
        rows.append(
            {
                "action_id": f"V48_HO_{action_index:03d}",
                "action_type": "run_targeted_source_search",
                "priority": row.get("priority_tier", ""),
                "item": row.get("item", ""),
                "source_artifact": "knowledge_external/synthesis/HIGH_PRIORITY_SOURCE_SEARCH_QUERIES_V48.md",
                "input_rows": f"{info['n_queries']} query rows; targets={info['targets']}",
                "next_step": "Run the query packet outside this artifact, then ingest any usable hit through V47 segregated records before relationship classification.",
                "boundary": "search handoff only; query hits are not findings",
            }
        )
        action_index += 1
    plan_by_item = {row.get("item", ""): row for row in plan_rows}
    for item, row in sorted(plan_by_item.items(), key=lambda item_row: int(item_row[1].get("rank", "999"))):
        rows.append(
            {
                "action_id": f"V48_HO_{action_index:03d}",
                "action_type": "apply_source_acceptance_criteria",
                "priority": "high",
                "item": item,
                "source_artifact": "knowledge_external/synthesis/HIGH_PRIORITY_EXTERNAL_SOURCING_PLAN_V48.md",
                "input_rows": row.get("source_type_needed", ""),
                "next_step": row.get("acceptance_criteria", ""),
                "boundary": "source-acceptance handoff only; generic adjacent context remains insufficient",
            }
        )
        action_index += 1
    for row in future_rows:
        rows.append(
            {
                "action_id": f"V48_HO_{action_index:03d}",
                "action_type": "future_grounding_queue",
                "priority": row.get("priority", "low"),
                "item": row.get("grounded_finding_id", ""),
                "source_artifact": "knowledge_external/synthesis/FUTURE_GROUNDING_QUEUE_V48.md",
                "input_rows": row.get("queue_id", ""),
                "next_step": row.get("future_grounding_action", ""),
                "boundary": "future-grounding handoff only; queued items are not findings",
            }
        )
        action_index += 1
    for row in surveillance_rows:
        if row.get("scope", "") != "future_sourcing_plan":
            continue
        rows.append(
            {
                "action_id": f"V48_HO_{action_index:03d}",
                "action_type": "contradiction_surveillance",
                "priority": "medium",
                "item": f"{row.get('finding_category', '')} / {row.get('source_class', '')}",
                "source_artifact": "knowledge_external/synthesis/CONTRADICTION_SURVEILLANCE_CHECKLIST_V48.md",
                "input_rows": f"{row.get('rows', '')} planned rows",
                "next_step": row.get("safe_action", ""),
                "boundary": "surveillance handoff only; tensions require source-specific overlap and future grounding",
            }
        )
        action_index += 1
    return rows


def row_key(row: dict[str, object]) -> str:
    return str(row.get("action_id", ""))


def add(rows: list[dict[str, object]], key: str, check: str, status: str, detail: str) -> None:
    rows.append({"row_key": key, "check": check, "status": status, "detail": detail})


def lint_handoff(priority: Path, plan: Path, queries: Path, future: Path, surveillance: Path, handoff: Path, summary_path: Path, outdir: Path, fail_on_error: bool) -> int:
    expected_list = expected_rows(priority, plan, queries, future, surveillance)
    expected = {row_key(row): row for row in expected_list}
    observed = {row_key(row): row for row in read_tsv(handoff)}
    rows: list[dict[str, object]] = []
    for key, expected_row in sorted(expected.items()):
        observed_row = observed.get(key)
        add(rows, key, "action_present", "PASS" if observed_row else "FAIL", str(handoff))
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
        add(rows, key, "no_extra_action", "FAIL", "action is not expected from current handoff inputs")
    summary = read_json(summary_path)
    action_counts = Counter(str(row["action_type"]) for row in expected_list)
    priority_counts = Counter(str(row["priority"]) for row in expected_list)
    summary_expectations = {
        "n_actions": len(expected_list),
        "action_type_counts": dict(sorted(action_counts.items())),
        "priority_counts": dict(sorted(priority_counts.items())),
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
    write_tsv(outdir / "unresolved_external_coverage_handoff_freshness_lint.tsv", rows, ["row_key", "check", "status", "detail"])
    result = {
        "synthetic": False,
        "purpose": "V48 unresolved external coverage handoff freshness lint; work-queue/navigation only; no biological claim",
        "n_expected_actions": len(expected_list),
        "n_checks": len(rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
    }
    (outdir / "unresolved_external_coverage_handoff_freshness_lint_summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if n_fail == 0 or not fail_on_error else 2


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else ROOT / outdir
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    expected = expected_rows(DEFAULT_PRIORITY, DEFAULT_PLAN, DEFAULT_QUERIES, DEFAULT_FUTURE, DEFAULT_SURVEILLANCE)
    handoff = outdir / "synthetic_handoff.tsv"
    summary = outdir / "synthetic_summary.json"
    stale = [dict(expected[0])]
    stale[0]["priority"] = "stale"
    stale.append({field: "extra" for field in FIELDS})
    stale[-1]["action_id"] = "EXTRA"
    write_tsv(handoff, stale, FIELDS)
    summary.write_text(json.dumps({"n_actions": 999, "action_type_counts": {"stale": 999}, "priority_counts": {"stale": 999}}) + "\n")
    lint_out = outdir / "synthetic_lint"
    lint_handoff(DEFAULT_PRIORITY, DEFAULT_PLAN, DEFAULT_QUERIES, DEFAULT_FUTURE, DEFAULT_SURVEILLANCE, handoff, summary, lint_out, fail_on_error=False)
    rows = read_tsv(lint_out / "unresolved_external_coverage_handoff_freshness_lint.tsv")
    first_key = row_key(expected[0])
    checks = {
        "missing_action_fails": any(row["check"] == "action_present" and row["status"] == "FAIL" for row in rows),
        "stale_action_field_fails": any(row["row_key"] == first_key and row["check"] == "field_matches.priority" and row["status"] == "FAIL" for row in rows),
        "extra_action_fails": any(row["row_key"] == "EXTRA" and row["check"] == "no_extra_action" and row["status"] == "FAIL" for row in rows),
        "bad_summary_count_fails": any(row["row_key"] == "summary" and row["check"] == "summary_matches.n_actions" and row["status"] == "FAIL" for row in rows),
    }
    check_rows = [{"check": check, "status": "PASS" if ok else "FAIL"} for check, ok in checks.items()]
    write_tsv(outdir / "synthetic_unresolved_external_coverage_handoff_freshness_checks.tsv", check_rows, ["check", "status"])
    result = {
        "synthetic": True,
        "purpose": "V48 unresolved external coverage handoff freshness synthetic fixture; no biological claim",
        "n_checks": len(check_rows),
        "n_fail": sum(1 for row in check_rows if row["status"] != "PASS"),
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
    }
    (outdir / "synthetic_unresolved_external_coverage_handoff_freshness_summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["overall_status"] == "PASS" or not fail_on_error else 2


def main() -> int:
    args = parse_args()
    if args.command == "lint":
        return lint_handoff(args.priority, args.plan, args.queries, args.future, args.surveillance, args.handoff, args.summary, args.outdir, args.fail_on_error)
    if args.command == "synthetic-check":
        return synthetic_check(args.outdir, args.fail_on_error)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
