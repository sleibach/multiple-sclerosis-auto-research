#!/usr/bin/env python3
"""Generate a compact V48 convergence/contradiction executive card."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "knowledge_external/synthesis"
SUMMARIES = {
    "matrix": ROOT / "knowledge_external/catalogs/indexes/convergence_contradiction_v48_summary.json",
    "source_independence": ROOT / "knowledge_external/catalogs/indexes/convergence_source_independence_v48_summary.json",
    "domain_independence": ROOT / "knowledge_external/catalogs/indexes/source_domain_independence_rollup_v48_summary.json",
    "gap_priority": ROOT / "knowledge_external/catalogs/indexes/v37_external_coverage_gap_priority_v48_summary.json",
    "preflight": ROOT / "analysis/v48_governance_preflight/v48_governance_preflight_summary.json",
}
DECISION_TSV = ROOT / "knowledge_external/synthesis/decision_relevant_convergences_v48.tsv"
GAP_TSV = ROOT / "knowledge_external/synthesis/v37_external_coverage_gap_priority_v48.tsv"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
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


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def build(outdir: Path) -> dict[str, object]:
    summaries = {name: read_json(path) for name, path in SUMMARIES.items()}
    decision_rows = read_tsv(DECISION_TSV)
    high_gap_rows = [row for row in read_tsv(GAP_TSV) if row.get("priority_tier") == "high"]
    high_gap_rows.sort(key=lambda row: int(row.get("rank", "999")))
    card_rows = [
        {
            "section": "relationship_counts",
            "metric": "V48 matrix rows",
            "value": summaries["matrix"].get("n_rows", ""),
            "boundary": "External relationship rows are context, not evidence.",
        },
        {
            "section": "relationship_counts",
            "metric": "convergence rows",
            "value": summaries["matrix"].get("n_converges", ""),
            "boundary": "Convergence corroborates context; grounded artifacts remain evidence.",
        },
        {
            "section": "relationship_counts",
            "metric": "contradiction rows",
            "value": summaries["matrix"].get("n_contradicts", ""),
            "boundary": "Contradictions would flag future grounding, not override grounded findings.",
        },
        {
            "section": "source_independence",
            "metric": "decision canonical source clusters",
            "value": summaries["source_independence"].get("n_decision_canonical_sources", ""),
            "boundary": "Same canonical source cluster is not multiple independent corroborations.",
        },
        {
            "section": "source_independence",
            "metric": "domains with convergence",
            "value": summaries["domain_independence"].get("n_domains_with_convergence", ""),
            "boundary": "Domain concentration limits external-source independence.",
        },
        {
            "section": "coverage_gaps",
            "metric": "V37 uncovered priority rows",
            "value": summaries["gap_priority"].get("n_priority_rows", ""),
            "boundary": "Sourcing priority is not validation or convergence.",
        },
        {
            "section": "coverage_gaps",
            "metric": "high-priority V37 sourcing gaps",
            "value": summaries["gap_priority"].get("n_high_priority", ""),
            "boundary": "Only same-definition external sources should be added.",
        },
        {
            "section": "governance",
            "metric": "preflight checks",
            "value": summaries["preflight"].get("n_checks", ""),
            "boundary": "Preflight checks provenance/navigation controls only.",
        },
        {
            "section": "governance",
            "metric": "preflight failures",
            "value": summaries["preflight"].get("n_fail", ""),
            "boundary": "Zero failures means the segregation controls passed.",
        },
    ]
    outdir.mkdir(parents=True, exist_ok=True)
    write_tsv(outdir / "convergence_contradiction_executive_card_v48.tsv", card_rows, ["section", "metric", "value", "boundary"])

    summary = {
        "purpose": "V48 convergence/contradiction executive card; synthesis/navigation only; no biological claim",
        "n_card_metrics": len(card_rows),
        "n_decision_rows": len(decision_rows),
        "n_high_priority_gap_rows": len(high_gap_rows),
        "n_convergence_rows": summaries["matrix"].get("n_converges", 0),
        "n_contradiction_rows": summaries["matrix"].get("n_contradicts", 0),
        "n_decision_canonical_source_clusters": summaries["source_independence"].get("n_decision_canonical_sources", 0),
        "governance_preflight_status": summaries["preflight"].get("overall_status", ""),
        "overall_status": "PASS",
        "markdown": "knowledge_external/synthesis/CONVERGENCE_CONTRADICTION_EXECUTIVE_CARD_V48.md",
        "tsv": "knowledge_external/synthesis/convergence_contradiction_executive_card_v48.tsv",
    }
    (ROOT / "knowledge_external/catalogs/indexes/convergence_contradiction_executive_card_v48_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")

    lines = [
        "# V48 Convergence/Contradiction Executive Card",
        "",
        "Status: synthesis/navigation only. This card summarizes V48 external-context relationships; it does not validate external claims or change grounded findings.",
        "",
        "## Headline",
        "",
        f"- V48 currently has `{summary['n_convergence_rows']}` convergence rows and `{summary['n_contradiction_rows']}` contradiction rows.",
        f"- The decision-relevant rows collapse to `{summary['n_decision_canonical_source_clusters']}` canonical external source cluster, so row count must not be treated as independent-source count.",
        f"- The high-priority uncovered V37 sourcing backlog has `{summary['n_high_priority_gap_rows']}` rows.",
        f"- Governance preflight status: `{summary['governance_preflight_status']}`.",
        "",
        "## Metrics",
        "",
        "| section | metric | value | boundary |",
        "|---|---|---:|---|",
    ]
    for row in card_rows:
        lines.append(f"| `{row['section']}` | {md_escape(row['metric'])} | {row['value']} | {md_escape(row['boundary'])} |")
    lines.extend(
        [
            "",
            "## Current Decision-Relevant Rows",
            "",
            "| finding | evidence grade | relationship | source | boundary |",
            "|---|---|---|---|---|",
        ]
    )
    for row in decision_rows:
        lines.append(
            "| "
            f"{md_escape(row.get('grounded_finding_id', ''))} | "
            f"`{md_escape(row.get('grounded_evidence_grade', ''))}` | "
            f"`{md_escape(row.get('relationship_class', ''))}` | "
            f"{md_escape(row.get('external_source', ''))} | "
            f"{md_escape(row.get('evidence_boundary', ''))} |"
        )
    lines.extend(
        [
            "",
            "## Top High-Priority Sourcing Gaps",
            "",
            "| rank | finding | score | safe source requirement |",
            "|---:|---|---:|---|",
        ]
    )
    for row in high_gap_rows[:5]:
        lines.append(
            "| "
            f"{md_escape(row.get('rank', ''))} | "
            f"{md_escape(row.get('item', ''))} | "
            f"{md_escape(row.get('priority_score', ''))} | "
            f"{md_escape(row.get('safe_source_requirement', ''))} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation Boundary",
            "",
            "- External convergence is corroborating context only; project artifacts remain the evidence.",
            "- Current convergence is source-cluster concentrated and should be described that way.",
            "- Current zero contradictions means no imported external record directly conflicts with a grounded finding under V48 rules; it is not proof that no contradiction exists in the wider literature.",
            "- Sourcing gaps are a future external-intake plan, not findings.",
            "",
        ]
    )
    (outdir / "CONVERGENCE_CONTRADICTION_EXECUTIVE_CARD_V48.md").write_text("\n".join(lines))
    print(json.dumps(summary, indent=2, sort_keys=True))
    return summary


def main() -> int:
    args = parse_args()
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    summary = build(outdir)
    return 0 if summary["overall_status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
