#!/usr/bin/env python3
"""Prioritize V37 findings that still lack V48 external relationship rows."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_COVERAGE = ROOT / "knowledge_external/synthesis/v37_finding_external_coverage_v48.tsv"
DEFAULT_RATIONALE = ROOT / "knowledge_external/synthesis/v37_uncovered_finding_rationale_v48.tsv"
DEFAULT_OUTDIR = ROOT / "knowledge_external/synthesis"
DEFAULT_SUMMARY = ROOT / "knowledge_external/catalogs/indexes/v37_external_coverage_gap_priority_v48_summary.json"


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
    parser.add_argument("--coverage", type=Path, default=DEFAULT_COVERAGE)
    parser.add_argument("--rationale", type=Path, default=DEFAULT_RATIONALE)
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
    parts = [
        f"relevance {row['relevance']}",
        f"novelty {row['novelty']}",
        f"evidence {row['evidence_grade']}",
        f"rationale {row['rationale_class']}",
    ]
    return "; ".join(parts)


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


def build(coverage_path: Path, rationale_path: Path, outdir: Path) -> dict[str, object]:
    coverage_rows = read_tsv(coverage_path)
    rationale_rows = read_tsv(rationale_path)
    rationale_by_item = {row["item"]: row for row in rationale_rows}

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

    fields = [
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
    outdir.mkdir(parents=True, exist_ok=True)
    write_tsv(outdir / "v37_external_coverage_gap_priority_v48.tsv", rows, fields)

    tier_counts = Counter(str(row["priority_tier"]) for row in rows)
    rationale_counts = Counter(str(row["rationale_class"]) for row in rows)
    category_counts = Counter(str(row["category"]) for row in rows)
    high_priority = [row["item"] for row in rows if row["priority_tier"] == "high"]
    summary = {
        "purpose": "V48 priority map for V37 scored findings still lacking external relationship rows; sourcing/navigation only, not evidence",
        "n_priority_rows": len(rows),
        "n_high_priority": len(high_priority),
        "high_priority_items": high_priority,
        "tier_counts": dict(sorted(tier_counts.items())),
        "rationale_counts": dict(sorted(rationale_counts.items())),
        "category_counts": dict(sorted(category_counts.items())),
        "score_formula": "2*relevance + novelty + evidence_weight + rationale_weight + category_weight",
        "overall_status": "PASS",
        "markdown": "knowledge_external/synthesis/V37_EXTERNAL_COVERAGE_GAP_PRIORITY_V48.md",
        "tsv": "knowledge_external/synthesis/v37_external_coverage_gap_priority_v48.tsv",
    }
    DEFAULT_SUMMARY.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")

    lines = [
        "# V37 External Coverage Gap Priority V48",
        "",
        "Status: sourcing/navigation only. This table prioritizes external-record hunting for V37 findings that currently lack a V48 relationship row; it does not change any V37 score or grounded finding.",
        "",
        f"- uncovered V37 findings prioritized: `{summary['n_priority_rows']}`",
        f"- high-priority sourcing gaps: `{summary['n_high_priority']}`",
        f"- score formula: `{summary['score_formula']}`",
        "",
        "## Priority Counts",
        "",
        "| tier | count |",
        "|---|---:|",
    ]
    for key, value in sorted(tier_counts.items()):
        lines.append(f"| `{md_escape(key)}` | {value} |")
    lines.extend(
        [
            "",
            "## Prioritized Gaps",
            "",
            "| rank | finding | tier | score | relevance | novelty | evidence | rationale | safe source requirement | next action |",
            "|---:|---|---|---:|---:|---:|---|---|---|---|",
        ]
    )
    for row in rows:
        lines.append(
            "| "
            f"{row['rank']} | "
            f"{md_escape(row['item'])} | "
            f"`{md_escape(row['priority_tier'])}` | "
            f"{row['priority_score']} | "
            f"{row['relevance']} | "
            f"{row['novelty']} | "
            f"`{md_escape(row['evidence_grade'])}` | "
            f"`{md_escape(row['rationale_class'])}` | "
            f"{md_escape(row['safe_source_requirement'])} | "
            f"{md_escape(row['next_action'])} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- High priority means the next external-knowledge pass should look first for specific, source-backed context for that grounded V37 item.",
            "- A priority row is not convergence, contradiction, validation, or biological evidence.",
            "- Generic external context must not be added when the safe source requirement demands a same-definition source.",
            "- Grounded project artifacts remain the evidence for every V37 item.",
            "",
        ]
    )
    (outdir / "V37_EXTERNAL_COVERAGE_GAP_PRIORITY_V48.md").write_text("\n".join(lines))
    print(json.dumps(summary, indent=2, sort_keys=True))
    return summary


def main() -> int:
    args = parse_args()
    coverage = args.coverage if args.coverage.is_absolute() else ROOT / args.coverage
    rationale = args.rationale if args.rationale.is_absolute() else ROOT / args.rationale
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    summary = build(coverage, rationale, outdir)
    return 0 if summary["overall_status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
