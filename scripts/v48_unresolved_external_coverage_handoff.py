#!/usr/bin/env python3
"""Generate V48 unresolved external coverage handoff grouped by action type."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PRIORITY = ROOT / "knowledge_external/synthesis/v37_external_coverage_gap_priority_v48.tsv"
DEFAULT_PLAN = ROOT / "knowledge_external/synthesis/high_priority_external_sourcing_plan_v48.tsv"
DEFAULT_QUERIES = ROOT / "knowledge_external/synthesis/high_priority_source_search_queries_v48.tsv"
DEFAULT_FUTURE = ROOT / "knowledge_external/synthesis/future_grounding_queue_v48.tsv"
DEFAULT_SURVEILLANCE = ROOT / "knowledge_external/synthesis/contradiction_surveillance_checklist_v48.tsv"
OUTDIR = ROOT / "knowledge_external/synthesis"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--priority", type=Path, default=DEFAULT_PRIORITY)
    parser.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    parser.add_argument("--queries", type=Path, default=DEFAULT_QUERIES)
    parser.add_argument("--future", type=Path, default=DEFAULT_FUTURE)
    parser.add_argument("--surveillance", type=Path, default=DEFAULT_SURVEILLANCE)
    parser.add_argument("--outdir", type=Path, default=OUTDIR)
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


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def query_counts(rows: list[dict[str, str]]) -> dict[str, dict[str, object]]:
    grouped: dict[str, dict[str, object]] = {}
    targets: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        item = row.get("item", "")
        targets[item].add(row.get("search_target", ""))
    for item, target_set in targets.items():
        grouped[item] = {"n_queries": sum(1 for row in rows if row.get("item", "") == item), "targets": ";".join(sorted(target_set))}
    return grouped


def build(priority: Path, plan: Path, queries: Path, future: Path, surveillance: Path, outdir: Path) -> dict[str, object]:
    priority_rows = read_tsv(priority)
    plan_rows = read_tsv(plan)
    query_info = query_counts(read_tsv(queries))
    future_rows = read_tsv(future)
    surveillance_rows = read_tsv(surveillance)
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
        priority_value = row.get("priority", "low")
        rows.append(
            {
                "action_id": f"V48_HO_{action_index:03d}",
                "action_type": "future_grounding_queue",
                "priority": priority_value,
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
    fields = ["action_id", "action_type", "priority", "item", "source_artifact", "input_rows", "next_step", "boundary"]
    outdir.mkdir(parents=True, exist_ok=True)
    write_tsv(outdir / "unresolved_external_coverage_handoff_v48.tsv", rows, fields)
    action_counts = Counter(str(row["action_type"]) for row in rows)
    priority_counts = Counter(str(row["priority"]) for row in rows)
    summary = {
        "purpose": "V48 unresolved external coverage handoff; work-queue/navigation only; no biological claim",
        "n_actions": len(rows),
        "action_type_counts": dict(sorted(action_counts.items())),
        "priority_counts": dict(sorted(priority_counts.items())),
        "overall_status": "PASS",
        "markdown": "knowledge_external/synthesis/UNRESOLVED_EXTERNAL_COVERAGE_HANDOFF_V48.md",
        "tsv": "knowledge_external/synthesis/unresolved_external_coverage_handoff_v48.tsv",
    }
    (ROOT / "knowledge_external/catalogs/indexes/unresolved_external_coverage_handoff_v48_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    lines = [
        "# V48 Unresolved External Coverage Handoff",
        "",
        "Status: work-queue/navigation only. This handoff consolidates unresolved source-search, source-acceptance, future-grounding, and surveillance actions; it does not add external records, assert convergence, or change grounded findings.",
        "",
        f"- total actions: `{summary['n_actions']}`",
        "",
        "## Action Counts",
        "",
        "| action type | count |",
        "|---|---:|",
    ]
    for action_type, count in sorted(action_counts.items()):
        lines.append(f"| {md_escape(action_type)} | {count} |")
    lines.extend(
        [
            "",
            "## Priority Counts",
            "",
            "| priority | count |",
            "|---|---:|",
        ]
    )
    for priority_key, count in sorted(priority_counts.items()):
        lines.append(f"| {md_escape(priority_key)} | {count} |")
    lines.extend(
        [
            "",
            "## Handoff Actions",
            "",
            "| id | action type | priority | item | next step | boundary |",
            "|---|---|---|---|---|---|",
        ]
    )
    for row in rows:
        lines.append(
            "| "
            f"`{md_escape(row['action_id'])}` | "
            f"{md_escape(row['action_type'])} | "
            f"`{md_escape(row['priority'])}` | "
            f"{md_escape(row['item'])} | "
            f"{md_escape(row['next_step'])} | "
            f"{md_escape(row['boundary'])} |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- This is an unresolved-work handoff, not a conclusion list.",
            "- A future source hit must still pass V47 segregated-record intake and V48 overlap review before it can enter a relationship matrix.",
            "- A future-grounding queue item remains ungrounded until a real data-backed test is run.",
            "",
        ]
    )
    (outdir / "UNRESOLVED_EXTERNAL_COVERAGE_HANDOFF_V48.md").write_text("\n".join(lines))
    print(json.dumps(summary, indent=2, sort_keys=True))
    return summary


def main() -> int:
    args = parse_args()
    summary = build(args.priority, args.plan, args.queries, args.future, args.surveillance, args.outdir if args.outdir.is_absolute() else ROOT / args.outdir)
    return 0 if summary["overall_status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
