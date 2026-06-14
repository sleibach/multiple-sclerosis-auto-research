#!/usr/bin/env python3
"""Generate a V48 decision-relevant convergence/contradiction shortlist."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MATRIX = ROOT / "knowledge_external/synthesis/convergence_contradiction_v48.tsv"
DEFAULT_OUTDIR = ROOT / "knowledge_external/synthesis"
SUMMARY_PATH = ROOT / "knowledge_external/catalogs/indexes/decision_relevant_convergences_v48_summary.json"


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


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def relevance(row: dict[str, str]) -> str:
    if row.get("relationship_class") == "converges":
        return "corroborated_grounded_context"
    if row.get("relationship_class") == "contradicts":
        return "external_tension_to_ground"
    return "not_shortlisted"


def sort_key(row: dict[str, object]) -> tuple[int, str]:
    order = {"external_tension_to_ground": 0, "corroborated_grounded_context": 1}
    return (order.get(str(row["shortlist_class"]), 9), str(row["grounded_finding_id"]))


def build(matrix: Path, outdir: Path) -> dict[str, object]:
    matrix_rows = read_tsv(matrix)
    rows: list[dict[str, object]] = []
    for row in matrix_rows:
        shortlist_class = relevance(row)
        if shortlist_class == "not_shortlisted":
            continue
        rows.append(
            {
                "shortlist_class": shortlist_class,
                "grounded_finding_id": row.get("grounded_finding_id", ""),
                "grounded_evidence_grade": row.get("grounded_evidence_grade", ""),
                "grounded_artifact": row.get("grounded_artifact", ""),
                "external_record_id": row.get("external_record_id", ""),
                "epistemic_class": row.get("epistemic_class", ""),
                "external_source": row.get("external_source", ""),
                "relationship_class": row.get("relationship_class", ""),
                "synthesis_status": row.get("synthesis_status", ""),
                "interpretation": row.get("interpretation", ""),
                "future_grounding_action": row.get("future_grounding_action", ""),
                "evidence_boundary": "Grounded artifact remains the evidence; external source is context/corroboration or tension flag only.",
            }
        )
    rows.sort(key=sort_key)
    outdir.mkdir(parents=True, exist_ok=True)
    fields = [
        "shortlist_class",
        "grounded_finding_id",
        "grounded_evidence_grade",
        "grounded_artifact",
        "external_record_id",
        "epistemic_class",
        "external_source",
        "relationship_class",
        "synthesis_status",
        "interpretation",
        "future_grounding_action",
        "evidence_boundary",
    ]
    write_tsv(outdir / "decision_relevant_convergences_v48.tsv", rows, fields)
    relationship_counts = Counter(row.get("relationship_class", "") for row in matrix_rows)
    shortlist_counts = Counter(str(row["shortlist_class"]) for row in rows)
    summary = {
        "purpose": "V48 decision-relevant convergence/contradiction shortlist; synthesis/navigation only; no biological claim",
        "n_matrix_rows": len(matrix_rows),
        "n_shortlist_rows": len(rows),
        "n_converges_in_matrix": relationship_counts.get("converges", 0),
        "n_contradicts_in_matrix": relationship_counts.get("contradicts", 0),
        "shortlist_counts": dict(sorted(shortlist_counts.items())),
        "overall_status": "PASS",
        "markdown": "knowledge_external/synthesis/DECISION_RELEVANT_CONVERGENCES_V48.md",
        "tsv": "knowledge_external/synthesis/decision_relevant_convergences_v48.tsv",
    }
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    lines = [
        "# V48 Decision-Relevant Convergences And Contradictions",
        "",
        "Status: synthesis/navigation only. This shortlist does not add evidence, change V37 scores, or alter any grounded finding.",
        "",
        f"- source matrix rows: `{summary['n_matrix_rows']}`",
        f"- shortlist rows: `{summary['n_shortlist_rows']}`",
        f"- convergences in matrix: `{summary['n_converges_in_matrix']}`",
        f"- contradictions in matrix: `{summary['n_contradicts_in_matrix']}`",
        "",
        "## Corroborated Grounded Context",
        "",
        "| grounded finding | evidence | external record | class | source | operational meaning |",
        "|---|---|---|---|---|---|",
    ]
    for row in rows:
        if row["shortlist_class"] != "corroborated_grounded_context":
            continue
        lines.append(
            "| "
            f"{md_escape(row['grounded_finding_id'])} | "
            f"`{md_escape(row['grounded_evidence_grade'])}` / `{md_escape(row['grounded_artifact'])}` | "
            f"`{md_escape(row['external_record_id'])}` | "
            f"`{md_escape(row['epistemic_class'])}` / `NOT_PROJECT_GROUNDED` | "
            f"{md_escape(row['external_source'])} | "
            f"{md_escape(row['interpretation'])} |"
        )
    lines.extend(
        [
            "",
            "## Contradictions Or Tensions",
            "",
        ]
    )
    contradiction_rows = [row for row in rows if row["shortlist_class"] == "external_tension_to_ground"]
    if not contradiction_rows:
        lines.append("- None flagged in the current V48 matrix.")
    else:
        lines.extend(["| grounded finding | external record | source | future grounding action |", "|---|---|---|---|"])
        for row in contradiction_rows:
            lines.append(
                "| "
                f"{md_escape(row['grounded_finding_id'])} | "
                f"`{md_escape(row['external_record_id'])}` | "
                f"{md_escape(row['external_source'])} | "
                f"{md_escape(row['future_grounding_action'])} |"
            )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- `corroborated_grounded_context` raises confidence as independent context, but the project artifact remains the evidence.",
            "- `external_tension_to_ground` would create a future grounding task, not an override of a grounded result.",
            "- Rows above retain the external/not-grounded boundary in their class/source columns.",
            "",
        ]
    )
    (outdir / "DECISION_RELEVANT_CONVERGENCES_V48.md").write_text("\n".join(lines))
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
