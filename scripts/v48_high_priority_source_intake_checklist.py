#!/usr/bin/env python3
"""Generate a V48 high-priority source intake checklist."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PLAN = ROOT / "knowledge_external/synthesis/high_priority_external_sourcing_plan_v48.tsv"
DEFAULT_QUERIES = ROOT / "knowledge_external/synthesis/high_priority_source_search_queries_v48.tsv"
OUTDIR = ROOT / "knowledge_external/templates"


CHECKLIST_STEPS = [
    "source_locator_recorded",
    "source_terms_reviewed",
    "source_snapshot_or_access_date_recorded",
    "epistemic_class_assigned",
    "not_project_grounded_marker_present",
    "same_definition_overlap_reviewed",
    "forbidden_shortcut_checked",
    "relationship_matrix_candidate_prepared",
    "future_grounding_route_recorded_if_verifiable",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    parser.add_argument("--queries", type=Path, default=DEFAULT_QUERIES)
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


def query_targets(queries: list[dict[str, str]]) -> dict[str, str]:
    targets: dict[str, set[str]] = defaultdict(set)
    for row in queries:
        targets[row.get("item", "")].add(row.get("search_target", ""))
    return {item: ";".join(sorted(target_set)) for item, target_set in targets.items()}


def build(plan: Path, queries: Path, outdir: Path) -> dict[str, object]:
    plan_rows = read_tsv(plan)
    targets_by_item = query_targets(read_tsv(queries))
    rows: list[dict[str, object]] = []
    for plan_row in sorted(plan_rows, key=lambda row: int(row.get("rank", "999"))):
        item = plan_row.get("item", "")
        for step_order, step in enumerate(CHECKLIST_STEPS, start=1):
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
    outdir.mkdir(parents=True, exist_ok=True)
    write_tsv(outdir / "high_priority_source_intake_checklist_v48.tsv", rows, ["rank", "item", "source_type_needed", "query_targets", "check_order", "check_id", "acceptance_criteria", "forbidden_shortcut", "required_before_matrix_entry", "boundary"])
    source_type_counts = Counter(row.get("source_type_needed", "") for row in plan_rows)
    summary = {
        "purpose": "V48 high-priority source intake checklist; template/navigation only; no biological claim",
        "n_plan_rows": len(plan_rows),
        "n_checklist_steps": len(CHECKLIST_STEPS),
        "n_checklist_rows": len(rows),
        "source_type_counts": dict(sorted(source_type_counts.items())),
        "overall_status": "PASS",
        "markdown": "knowledge_external/templates/HIGH_PRIORITY_SOURCE_INTAKE_CHECKLIST_V48.md",
        "tsv": "knowledge_external/templates/high_priority_source_intake_checklist_v48.tsv",
    }
    (ROOT / "knowledge_external/catalogs/indexes/high_priority_source_intake_checklist_v48_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    lines = [
        "# V48 High-Priority Source Intake Checklist",
        "",
        "Status: template/navigation only. This checklist tells future sessions how to intake a source found from the high-priority search packet; it does not add external records, assert convergence, or change grounded findings.",
        "",
        f"- source-plan rows: `{summary['n_plan_rows']}`",
        f"- required checklist steps per item: `{summary['n_checklist_steps']}`",
        f"- checklist rows: `{summary['n_checklist_rows']}`",
        "",
        "## Required Steps",
        "",
        "| order | check | meaning |",
        "|---:|---|---|",
    ]
    meanings = {
        "source_locator_recorded": "Record URL, DOI, accession, or stable locator.",
        "source_terms_reviewed": "Check source terms/reuse metadata before storing summaries.",
        "source_snapshot_or_access_date_recorded": "Record access date and, where possible, a source snapshot/hash.",
        "epistemic_class_assigned": "Assign external-verifiable or external-unverifiable before use.",
        "not_project_grounded_marker_present": "Preserve the explicit not-grounded marker.",
        "same_definition_overlap_reviewed": "Confirm the source overlaps the same finding definition before relationship classification.",
        "forbidden_shortcut_checked": "Reject generic adjacent context when the source plan forbids it.",
        "relationship_matrix_candidate_prepared": "Prepare a candidate relationship row only after source-specific overlap review.",
        "future_grounding_route_recorded_if_verifiable": "If the claim can be grounded later, queue the exact future test.",
    }
    for order, step in enumerate(CHECKLIST_STEPS, start=1):
        lines.append(f"| {order} | `{step}` | {md_escape(meanings[step])} |")
    lines.extend(
        [
            "",
            "## High-Priority Items",
            "",
            "| rank | item | source type needed | query targets | acceptance criteria | forbidden shortcut |",
            "|---:|---|---|---|---|---|",
        ]
    )
    for plan_row in sorted(plan_rows, key=lambda row: int(row.get("rank", "999"))):
        item = plan_row.get("item", "")
        lines.append(
            "| "
            f"{md_escape(plan_row.get('rank', ''))} | "
            f"{md_escape(item)} | "
            f"{md_escape(plan_row.get('source_type_needed', ''))} | "
            f"{md_escape(targets_by_item.get(item, ''))} | "
            f"{md_escape(plan_row.get('acceptance_criteria', ''))} | "
            f"{md_escape(plan_row.get('forbidden_shortcut', ''))} |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- Passing this checklist does not make a source a project finding.",
            "- Any source must still be stored as a segregated external record with class, source, access date, and not-grounded marker.",
            "- The grounded project artifact remains the evidence unless a future project run regrounds the claim on real data.",
            "",
        ]
    )
    (outdir / "HIGH_PRIORITY_SOURCE_INTAKE_CHECKLIST_V48.md").write_text("\n".join(lines))
    print(json.dumps(summary, indent=2, sort_keys=True))
    return summary


def main() -> int:
    args = parse_args()
    summary = build(args.plan, args.queries, args.outdir if args.outdir.is_absolute() else ROOT / args.outdir)
    return 0 if summary["overall_status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
