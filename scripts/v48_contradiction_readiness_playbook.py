#!/usr/bin/env python3
"""Generate the V48 contradiction readiness playbook."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MATRIX = ROOT / "knowledge_external/synthesis/convergence_contradiction_v48.tsv"
OUTDIR = ROOT / "knowledge_external/synthesis"
SUMMARY_PATH = ROOT / "knowledge_external/catalogs/indexes/contradiction_readiness_playbook_v48_summary.json"


STEPS = [
    {
        "stage": "intake",
        "trigger": "external source appears to disagree with a grounded project finding",
        "required_artifact": "knowledge_external/templates/contradiction_intake_template.json.template",
        "safe_action": "create a segregated external-verifiable intake record with source, class, project-finding reference, relationship note, and future grounding route",
        "forbidden_action": "do not edit the grounded finding, locked rule, or validation pre-registration",
    },
    {
        "stage": "triage",
        "trigger": "intake record exists",
        "required_artifact": "scripts/v48_contradiction_intake_linter.py",
        "safe_action": "classify likely explanation: population, phenotype definition, modality, directionality, date/version, or true discrepancy",
        "forbidden_action": "do not resolve by deferring to the external source",
    },
    {
        "stage": "future_grounding",
        "trigger": "concrete project data or reachable public data can test the tension",
        "required_artifact": "knowledge_external/synthesis/FUTURE_GROUNDING_QUEUE_V48.md",
        "safe_action": "queue the exact test and required data; keep the contradiction as a flag until grounded",
        "forbidden_action": "do not report model or literature agreement as evidence",
    },
    {
        "stage": "grounded_resolution",
        "trigger": "a future rerunnable project analysis tests the contradiction",
        "required_artifact": "normal grounded project artifact outside knowledge_external",
        "safe_action": "update the grounded project state only through rerunnable analysis with evidence grade and artifact reference",
        "forbidden_action": "do not let an external record directly change project scores or conclusions",
    },
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--matrix", type=Path, default=DEFAULT_MATRIX)
    parser.add_argument("--outdir", type=Path, default=OUTDIR)
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


def build(matrix: Path, outdir: Path) -> dict[str, object]:
    matrix_rows = read_tsv(matrix)
    current_contradictions = [row for row in matrix_rows if row.get("relationship_class") == "contradicts"]
    outdir.mkdir(parents=True, exist_ok=True)
    fields = ["stage", "trigger", "required_artifact", "safe_action", "forbidden_action"]
    write_tsv(outdir / "contradiction_readiness_playbook_v48.tsv", STEPS, fields)
    summary = {
        "purpose": "V48 contradiction readiness playbook; governance/navigation only; no biological claim",
        "n_current_matrix_rows": len(matrix_rows),
        "n_current_contradictions": len(current_contradictions),
        "n_playbook_steps": len(STEPS),
        "overall_status": "PASS",
        "markdown": "knowledge_external/synthesis/CONTRADICTION_READINESS_PLAYBOOK_V48.md",
        "tsv": "knowledge_external/synthesis/contradiction_readiness_playbook_v48.tsv",
    }
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    lines = [
        "# V48 Contradiction Readiness Playbook",
        "",
        "Status: governance/navigation only. This playbook defines what to do if future external context conflicts with a grounded project finding.",
        "",
        f"- current matrix rows: `{summary['n_current_matrix_rows']}`",
        f"- current contradictions: `{summary['n_current_contradictions']}`",
        f"- playbook steps: `{summary['n_playbook_steps']}`",
        "",
        "## Current State",
        "",
    ]
    if current_contradictions:
        lines.extend(["| grounded finding | external record | source | future grounding action |", "|---|---|---|---|"])
        for row in current_contradictions:
            lines.append(
                "| "
                f"{md_escape(row.get('grounded_finding_id', ''))} | "
                f"`{md_escape(row.get('external_record_id', ''))}` | "
                f"{md_escape(row.get('external_source', ''))} | "
                f"{md_escape(row.get('future_grounding_action', ''))} |"
            )
    else:
        lines.append("- No contradictions are currently flagged in the V48 matrix.")
    lines.extend(
        [
            "",
            "## Playbook",
            "",
            "| stage | trigger | required artifact | safe action | forbidden action |",
            "|---|---|---|---|---|",
        ]
    )
    for row in STEPS:
        lines.append(
            "| "
            f"`{md_escape(row['stage'])}` | "
            f"{md_escape(row['trigger'])} | "
            f"`{md_escape(row['required_artifact'])}` | "
            f"{md_escape(row['safe_action'])} | "
            f"{md_escape(row['forbidden_action'])} |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- External disagreement raises a flag; it does not override a rerunnable project finding.",
            "- Any resolution must be produced by a future grounded analysis artifact.",
            "- Locked rules and validation pre-registrations are unchanged by this playbook.",
            "",
        ]
    )
    (outdir / "CONTRADICTION_READINESS_PLAYBOOK_V48.md").write_text("\n".join(lines))
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
