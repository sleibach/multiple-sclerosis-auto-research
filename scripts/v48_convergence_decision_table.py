#!/usr/bin/env python3
"""Generate a compact decision table from the V48 convergence matrix."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MATRIX = ROOT / "knowledge_external/synthesis/convergence_contradiction_v48.tsv"
DEFAULT_OUTDIR = ROOT / "knowledge_external/synthesis"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--matrix", type=Path, default=DEFAULT_MATRIX)
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


def decision(row: dict[str, str]) -> tuple[str, str]:
    relationship = row.get("relationship_class", "")
    status = row.get("synthesis_status", "")
    if relationship == "converges":
        return (
            "corroborated_context",
            "Independent external context aligns with the grounded project finding; use as confidence-raising context, not evidence.",
        )
    if relationship == "contradicts":
        return (
            "tension_flag",
            "External context conflicts with a grounded finding; queue future grounding, do not override the project finding.",
        )
    if status == "NO_DIRECT_EXTERNAL_CORROBORATION":
        return (
            "no_direct_external_corroboration",
            "Related external context exists, but it does not validate or contradict the grounded finding.",
        )
    return (
        "insufficient_overlap",
        "External record does not overlap enough with the grounded finding to support a relationship claim.",
    )


def priority_key(row: dict[str, object]) -> tuple[int, str]:
    priority = {
        "tension_flag": 0,
        "corroborated_context": 1,
        "no_direct_external_corroboration": 2,
        "insufficient_overlap": 3,
    }
    return (priority.get(str(row["decision_class"]), 9), str(row["grounded_finding_id"]))


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def build(matrix: Path, outdir: Path) -> dict[str, object]:
    rows: list[dict[str, object]] = []
    for row in read_tsv(matrix):
        decision_class, decision_text = decision(row)
        rows.append(
            {
                "grounded_finding_id": row.get("grounded_finding_id", ""),
                "grounded_category": row.get("grounded_category", ""),
                "grounded_evidence_grade": row.get("grounded_evidence_grade", ""),
                "external_record_id": row.get("external_record_id", ""),
                "epistemic_class": row.get("epistemic_class", ""),
                "external_source": row.get("external_source", ""),
                "relationship_class": row.get("relationship_class", ""),
                "synthesis_status": row.get("synthesis_status", ""),
                "decision_class": decision_class,
                "decision_text": decision_text,
                "future_grounding_action": row.get("future_grounding_action", ""),
            }
        )
    rows.sort(key=priority_key)
    outdir.mkdir(parents=True, exist_ok=True)
    fields = [
        "grounded_finding_id",
        "grounded_category",
        "grounded_evidence_grade",
        "external_record_id",
        "epistemic_class",
        "external_source",
        "relationship_class",
        "synthesis_status",
        "decision_class",
        "decision_text",
        "future_grounding_action",
    ]
    write_tsv(outdir / "convergence_decision_table_v48.tsv", rows, fields)
    decision_counts = Counter(str(row["decision_class"]) for row in rows)
    relationship_counts = Counter(str(row["relationship_class"]) for row in rows)
    summary = {
        "purpose": "V48 compact convergence decision table; synthesis/navigation only; no biological claim",
        "n_rows": len(rows),
        "decision_counts": dict(sorted(decision_counts.items())),
        "relationship_counts": dict(sorted(relationship_counts.items())),
        "overall_status": "PASS",
        "markdown": "knowledge_external/synthesis/CONVERGENCE_DECISION_TABLE_V48.md",
        "tsv": "knowledge_external/synthesis/convergence_decision_table_v48.tsv",
    }
    (ROOT / "knowledge_external/catalogs/indexes/convergence_decision_table_v48_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    lines = [
        "# V48 Convergence Decision Table",
        "",
        "Status: synthesis/navigation only. External context is never project evidence; relationship classes only guide interpretation and future grounding.",
        "",
        f"- rows: `{summary['n_rows']}`",
        "",
        "## Decision Counts",
        "",
        "| decision class | count |",
        "|---|---:|",
    ]
    for key, value in sorted(decision_counts.items()):
        lines.append(f"| `{md_escape(key)}` | {value} |")
    lines.extend(
        [
            "",
            "## Decision Rows",
            "",
            "| decision | grounded finding | evidence | relationship | external class | source | operational meaning |",
            "|---|---|---|---|---|---|---|",
        ]
    )
    for row in rows:
        lines.append(
            "| "
            f"`{md_escape(row['decision_class'])}` | "
            f"{md_escape(row['grounded_finding_id'])} | "
            f"`{md_escape(row['grounded_evidence_grade'])}` | "
            f"`{md_escape(row['relationship_class'])}` | "
            f"`{md_escape(row['epistemic_class'])}` | "
            f"{md_escape(row['external_source'])} | "
            f"{md_escape(row['decision_text'])} |"
        )
    lines.extend(
        [
            "",
            "## Rules",
            "",
            "- `corroborated_context`: confidence-raising context only; grounded artifact remains the evidence.",
            "- `tension_flag`: future-grounding priority only; external context does not override a grounded finding.",
            "- `no_direct_external_corroboration`: related context exists but does not validate the finding.",
            "- This table does not change V37 scores, locked rules, or validation plans.",
            "",
        ]
    )
    (outdir / "CONVERGENCE_DECISION_TABLE_V48.md").write_text("\n".join(lines))
    print(json.dumps(summary, indent=2, sort_keys=True))
    return summary


def main() -> int:
    args = parse_args()
    matrix = args.matrix if args.matrix.is_absolute() else ROOT / args.matrix
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    summary = build(matrix, outdir)
    return 0 if summary["overall_status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
