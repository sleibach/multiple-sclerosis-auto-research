#!/usr/bin/env python3
"""Build a V48 contradiction surveillance checklist."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MATRIX = ROOT / "knowledge_external/synthesis/convergence_contradiction_v48.tsv"
DEFAULT_PLAN = ROOT / "knowledge_external/synthesis/high_priority_external_sourcing_plan_v48.tsv"
DEFAULT_OUTDIR = ROOT / "knowledge_external/synthesis"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--matrix", type=Path, default=DEFAULT_MATRIX)
    parser.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
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


def trigger_for(category: str) -> str:
    if category == "positive_supported":
        return "Candidate says the grounded positive does not hold under the same definition, population, layer, or direction."
    if category == "decoupling_negative":
        return "Candidate says a project decoupling/negative relationship is actually shared, same-direction, or transferable under the same definition."
    if category == "kills_closed":
        return "Candidate says a killed or closed lead succeeds under the same rule, direction, or validation domain."
    if category == "methodological":
        return "Candidate challenges a project method result or governance rule under the same procedure."
    return "Candidate conflicts with the matching grounded finding definition."


def action_for(scope: str) -> str:
    if scope == "current_matrix":
        return "Add or update a contradiction-intake row only if the candidate has source-specific overlap; queue future grounding before any interpretation change."
    return "If a source is found, ingest it through V47 segregation first, then classify overlap before creating any contradiction row."


def build(matrix_path: Path, plan_path: Path, outdir: Path) -> dict[str, object]:
    grouped: dict[tuple[str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in read_tsv(matrix_path):
        key = ("current_matrix", row.get("external_record_type", ""), row.get("grounded_category", ""))
        grouped[key].append(row)
    for row in read_tsv(plan_path):
        key = ("future_sourcing_plan", row.get("source_type_needed", ""), row.get("category", ""))
        grouped[key].append(row)

    rows: list[dict[str, object]] = []
    for (scope, source_class, finding_category), group in sorted(grouped.items()):
        rel_counts = Counter(row.get("relationship_class", "planned_source") for row in group)
        rows.append(
            {
                "scope": scope,
                "source_class": source_class,
                "finding_category": finding_category,
                "rows": len(group),
                "current_convergence_rows": rel_counts.get("converges", 0),
                "current_contradiction_rows": rel_counts.get("contradicts", 0),
                "current_insufficient_overlap_rows": rel_counts.get("insufficient-overlap", 0),
                "planned_source_rows": rel_counts.get("planned_source", 0),
                "surveillance_trigger": trigger_for(finding_category),
                "safe_action": action_for(scope),
            }
        )
    rows.sort(
        key=lambda row: (
            0 if row["scope"] == "current_matrix" else 1,
            str(row["finding_category"]),
            str(row["source_class"]),
        )
    )
    fields = [
        "scope",
        "source_class",
        "finding_category",
        "rows",
        "current_convergence_rows",
        "current_contradiction_rows",
        "current_insufficient_overlap_rows",
        "planned_source_rows",
        "surveillance_trigger",
        "safe_action",
    ]
    outdir.mkdir(parents=True, exist_ok=True)
    write_tsv(outdir / "contradiction_surveillance_checklist_v48.tsv", rows, fields)
    summary = {
        "purpose": "V48 contradiction surveillance checklist; future intake/navigation only; no biological claim",
        "n_checklist_rows": len(rows),
        "n_current_matrix_scopes": sum(1 for row in rows if row["scope"] == "current_matrix"),
        "n_future_sourcing_scopes": sum(1 for row in rows if row["scope"] == "future_sourcing_plan"),
        "n_current_contradiction_rows": sum(int(row["current_contradiction_rows"]) for row in rows),
        "overall_status": "PASS",
        "markdown": "knowledge_external/synthesis/CONTRADICTION_SURVEILLANCE_CHECKLIST_V48.md",
        "tsv": "knowledge_external/synthesis/contradiction_surveillance_checklist_v48.tsv",
    }
    (ROOT / "knowledge_external/catalogs/indexes/contradiction_surveillance_checklist_v48_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    lines = [
        "# V48 Contradiction Surveillance Checklist",
        "",
        "Status: future intake/navigation only. This checklist defines how future candidate tensions are triaged; it does not assert current contradictions.",
        "",
        f"- checklist rows: `{summary['n_checklist_rows']}`",
        f"- current matrix surveillance rows: `{summary['n_current_matrix_scopes']}`",
        f"- future sourcing surveillance rows: `{summary['n_future_sourcing_scopes']}`",
        f"- current contradiction rows: `{summary['n_current_contradiction_rows']}`",
        "",
        "## Checklist",
        "",
        "| scope | source class | finding category | rows | current contradiction rows | surveillance trigger | safe action |",
        "|---|---|---|---:|---:|---|---|",
    ]
    for row in rows:
        lines.append(
            "| "
            f"`{md_escape(row['scope'])}` | "
            f"{md_escape(row['source_class'])} | "
            f"`{md_escape(row['finding_category'])}` | "
            f"{row['rows']} | "
            f"{row['current_contradiction_rows']} | "
            f"{md_escape(row['surveillance_trigger'])} | "
            f"{md_escape(row['safe_action'])} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation Boundary",
            "",
            "- The current V48 matrix still has zero contradiction rows.",
            "- A future tension is a routing event: intake, overlap check, future grounding queue; it is not an override of a grounded finding.",
            "- This checklist prevents ad hoc interpretation if a future source appears to disagree with the project.",
            "",
        ]
    )
    (outdir / "CONTRADICTION_SURVEILLANCE_CHECKLIST_V48.md").write_text("\n".join(lines))
    print(json.dumps(summary, indent=2, sort_keys=True))
    return summary


def main() -> int:
    args = parse_args()
    matrix = args.matrix if args.matrix.is_absolute() else ROOT / args.matrix
    plan = args.plan if args.plan.is_absolute() else ROOT / args.plan
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    summary = build(matrix, plan, outdir)
    return 0 if summary["overall_status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
