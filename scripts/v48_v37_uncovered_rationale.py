#!/usr/bin/env python3
"""Generate rationale table for V37 findings without V48 external rows."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_COVERAGE = ROOT / "knowledge_external/synthesis/v37_finding_external_coverage_v48.tsv"
DEFAULT_OUTDIR = ROOT / "knowledge_external/synthesis"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--coverage", type=Path, default=DEFAULT_COVERAGE)
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


def rationale_for(row: dict[str, str]) -> tuple[str, str, str]:
    category = row.get("category", "")
    grade = row.get("evidence_grade", "")
    if category in {"kills_closed", "decoupling_negative"}:
        return (
            "targeted_external_record_needed",
            "This is a project-specific negative, kill, or decoupling result; V48 should not force a generic external context row without a source that addresses the same direction/definition.",
            "Only add external context if a source directly discusses the same locus/lead/failure mode and can be classed without changing the grounded result.",
        )
    if grade in {"provisional", "speculative"}:
        return (
            "avoid_false_corroboration",
            "The project finding is not robust enough to benefit from broad external context; generic literature agreement would risk overstating a provisional result.",
            "Queue a future external-verifiable task only if a source points to a concrete dataset or predefined test.",
        )
    if category == "methodological":
        return (
            "method_specific_external_context_absent",
            "The item is a project-method or governance result; external literature rarely maps one-to-one to the exact project procedure.",
            "Add only method-specific external context, not broad biological context.",
        )
    return (
        "no_relevant_external_record_imported",
        "No imported external record overlaps the finding closely enough to assert convergence or contradiction under V47/V48 provenance rules.",
        "Future V47-style intake can add a sourced external record if it directly overlaps the finding.",
    )


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def build(coverage_path: Path, outdir: Path) -> dict[str, object]:
    coverage_rows = read_tsv(coverage_path)
    rows: list[dict[str, object]] = []
    for row in coverage_rows:
        if row.get("v48_coverage") != "no_v48_external_relationship_row":
            continue
        rationale_class, rationale, next_action = rationale_for(row)
        rows.append(
            {
                "item": row.get("item", ""),
                "category": row.get("category", ""),
                "evidence_grade": row.get("evidence_grade", ""),
                "supporting_artifact": row.get("supporting_artifact", ""),
                "rationale_class": rationale_class,
                "rationale": rationale,
                "next_action": next_action,
            }
        )
    outdir.mkdir(parents=True, exist_ok=True)
    fields = ["item", "category", "evidence_grade", "supporting_artifact", "rationale_class", "rationale", "next_action"]
    write_tsv(outdir / "v37_uncovered_finding_rationale_v48.tsv", rows, fields)
    rationale_counts = Counter(str(row["rationale_class"]) for row in rows)
    category_counts = Counter(str(row["category"]) for row in rows)
    summary = {
        "purpose": "V48 rationale for V37 findings without external relationship rows; synthesis/navigation only",
        "n_uncovered_findings": len(rows),
        "rationale_counts": dict(sorted(rationale_counts.items())),
        "category_counts": dict(sorted(category_counts.items())),
        "overall_status": "PASS",
        "markdown": "knowledge_external/synthesis/V37_UNCOVERED_FINDING_RATIONALE_V48.md",
        "tsv": "knowledge_external/synthesis/v37_uncovered_finding_rationale_v48.tsv",
    }
    (ROOT / "knowledge_external/catalogs/indexes/v37_uncovered_finding_rationale_v48_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    lines = [
        "# V37 Uncovered Finding Rationale V48",
        "",
        "Status: synthesis/navigation only. Absence of a V48 external relationship row is not a biological negative and not external contradiction.",
        "",
        f"- uncovered V37 findings: `{summary['n_uncovered_findings']}`",
        "",
        "## Rationale Counts",
        "",
        "| rationale class | count |",
        "|---|---:|",
    ]
    for key, value in sorted(rationale_counts.items()):
        lines.append(f"| `{key}` | {value} |")
    lines.extend(
        [
            "",
            "## Findings",
            "",
            "| finding | category | evidence | rationale class | rationale | next action |",
            "|---|---|---|---|---|---|",
        ]
    )
    for row in rows:
        lines.append(
            "| "
            f"{md_escape(row['item'])} | "
            f"`{md_escape(row['category'])}` | "
            f"`{md_escape(row['evidence_grade'])}` | "
            f"`{md_escape(row['rationale_class'])}` | "
            f"{md_escape(row['rationale'])} | "
            f"{md_escape(row['next_action'])} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- This table explains non-coverage; it does not demote, validate, or contradict any finding.",
            "- External context should be added only when source overlap is specific enough to preserve provenance discipline.",
            "- Grounded project artifacts remain the evidence for every V37 item.",
            "",
        ]
    )
    (outdir / "V37_UNCOVERED_FINDING_RATIONALE_V48.md").write_text("\n".join(lines))
    print(json.dumps(summary, indent=2, sort_keys=True))
    return summary


def main() -> int:
    args = parse_args()
    coverage = args.coverage if args.coverage.is_absolute() else ROOT / args.coverage
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    summary = build(coverage, outdir)
    return 0 if summary["overall_status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
