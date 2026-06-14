#!/usr/bin/env python3
"""Build a sourcing plan for high-priority V37 external coverage gaps."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PRIORITY = ROOT / "knowledge_external/synthesis/v37_external_coverage_gap_priority_v48.tsv"
DEFAULT_OUTDIR = ROOT / "knowledge_external/synthesis"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--priority", type=Path, default=DEFAULT_PRIORITY)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    return parser.parse_args()


def read_tsv(path: Path) -> list[dict[str, str]]:
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


def build(priority_path: Path, outdir: Path) -> dict[str, object]:
    priority_rows = [row for row in read_tsv(priority_path) if row.get("priority_tier") == "high"]
    priority_rows.sort(key=lambda row: int(row.get("rank", "999")))
    rows: list[dict[str, object]] = []
    for row in priority_rows:
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
    fields = [
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
    outdir.mkdir(parents=True, exist_ok=True)
    write_tsv(outdir / "high_priority_external_sourcing_plan_v48.tsv", rows, fields)
    source_type_counts: dict[str, int] = {}
    for row in rows:
        key = str(row["source_type_needed"])
        source_type_counts[key] = source_type_counts.get(key, 0) + 1
    summary = {
        "purpose": "V48 high-priority external sourcing plan; future intake/navigation only; no external claims added and no biological claim",
        "n_plan_rows": len(rows),
        "source_type_counts": dict(sorted(source_type_counts.items())),
        "overall_status": "PASS",
        "markdown": "knowledge_external/synthesis/HIGH_PRIORITY_EXTERNAL_SOURCING_PLAN_V48.md",
        "tsv": "knowledge_external/synthesis/high_priority_external_sourcing_plan_v48.tsv",
    }
    (ROOT / "knowledge_external/catalogs/indexes/high_priority_external_sourcing_plan_v48_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    lines = [
        "# V48 High-Priority External Sourcing Plan",
        "",
        "Status: future intake/navigation only. This plan does not add external claims, assert convergence, or change any grounded finding.",
        "",
        f"- high-priority sourcing rows: `{summary['n_plan_rows']}`",
        "",
        "## Source-Type Counts",
        "",
        "| source type needed | count |",
        "|---|---:|",
    ]
    for key, value in sorted(source_type_counts.items()):
        lines.append(f"| {md_escape(key)} | {value} |")
    lines.extend(
        [
            "",
            "## Plan",
            "",
            "| rank | finding | source type needed | acceptance criteria | forbidden shortcut |",
            "|---:|---|---|---|---|",
        ]
    )
    for row in rows:
        lines.append(
            "| "
            f"{md_escape(row['rank'])} | "
            f"{md_escape(row['item'])} | "
            f"{md_escape(row['source_type_needed'])} | "
            f"{md_escape(row['acceptance_criteria'])} | "
            f"{md_escape(row['forbidden_shortcut'])} |"
        )
    lines.extend(
        [
            "",
            "## Integration Boundary",
            "",
            "- Any located candidate must go through the V47 segregated-record intake workflow before matrix comparison.",
            "- The candidate remains external context until a separate grounded analysis is run.",
            "- Convergence or contradiction can be asserted only after source-specific overlap review under the V48 matrix rules.",
            "",
        ]
    )
    (outdir / "HIGH_PRIORITY_EXTERNAL_SOURCING_PLAN_V48.md").write_text("\n".join(lines))
    print(json.dumps(summary, indent=2, sort_keys=True))
    return summary


def main() -> int:
    args = parse_args()
    priority = args.priority if args.priority.is_absolute() else ROOT / args.priority
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    summary = build(priority, outdir)
    return 0 if summary["overall_status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
