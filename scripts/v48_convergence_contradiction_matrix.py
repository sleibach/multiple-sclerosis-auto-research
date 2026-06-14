#!/usr/bin/env python3
"""Build the V48 convergence/contradiction relationship matrix.

This script is intentionally conservative. External records can corroborate a
grounded finding only when they point to a specific V37 finding reference.
Resource metadata and broad context records are classified as insufficient
overlap unless the curated mapping below says otherwise. The output is a
synthesis artifact, not a grounded-project evidence artifact.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCORES = ROOT / "docs/reports/FINDINGS_SCORES_V37.tsv"
DEFAULT_INDEX = ROOT / "knowledge_external/catalogs/indexes/external_knowledge_index.tsv"
DEFAULT_OUTDIR = ROOT / "knowledge_external/synthesis"
DEFAULT_SUMMARY = ROOT / "knowledge_external/catalogs/indexes/convergence_contradiction_v48_summary.json"
NOT_GROUNDED = "NOT_PROJECT_GROUNDED"


GROUNDING_MAP: list[dict[str, str]] = [
    {
        "grounded_finding_id": "MS-UC is strongest tested genome-wide genetics comparator",
        "external_record_id": "claim.nature.ms_uc_greater_genetic_correlation_context.2026-06-14",
        "relationship_class": "converges",
        "synthesis_status": "CORROBORATION_FROM_INDEPENDENT_SOURCE",
        "interpretation": (
            "The external literature claim independently reports stronger MS-UC than MS-CD genetic correlation. "
            "This aligns with the project's rerunnable MS-UC genetics backdrop; the project artifact remains the evidence."
        ),
        "future_grounding_action": "No action needed for current interpretation; future refresh should hash and rerun the external summary-statistic inputs if imported.",
    },
    {
        "grounded_finding_id": "Layer-specific autoimmune transfer-validity map",
        "external_record_id": "claim.ms_ibd.treatment_transfer_caution_context.2026-06-14",
        "relationship_class": "converges",
        "synthesis_status": "CORROBORATION_FROM_INDEPENDENT_SOURCE",
        "interpretation": (
            "The external literature context warns that treatment effects do not transfer naively between MS and IBD. "
            "This aligns with the project's axis-specific transfer-validity map; the project artifact remains the evidence."
        ),
        "future_grounding_action": "If pursued clinically, ground specific treatment-transfer claims in predefined patient-level or pharmacovigilance data.",
    },
    {
        "grounded_finding_id": "Bounded APC/HLA-II early treatment-response monitoring scalar",
        "external_record_id": "claim.dailymed.dimethyl_fumarate_mechanism_context.2026-06-13",
        "relationship_class": "insufficient-overlap",
        "synthesis_status": "NO_DIRECT_EXTERNAL_CORROBORATION",
        "interpretation": (
            "The DMF label provides treatment-context and mechanism-uncertainty context, but it does not independently assert an APC/HLA-II early-response monitoring rule."
        ),
        "future_grounding_action": "Validate with the frozen V42/V44 harness on a paired labeled DMF cohort; do not use label context as validation.",
    },
    {
        "grounded_finding_id": "V22 scalar is immune-tone bounded, not steroid/composition artifact",
        "external_record_id": "claim.dailymed.dimethyl_fumarate_mechanism_context.2026-06-13",
        "relationship_class": "insufficient-overlap",
        "synthesis_status": "NO_DIRECT_EXTERNAL_CORROBORATION",
        "interpretation": (
            "The label context does not test glucocorticoid, composition, metabolic, or STAT1 confounding of the project score."
        ),
        "future_grounding_action": "Use the V42/V44 confounder and batch diagnostics when real validation data arrive.",
    },
    {
        "grounded_finding_id": "Coupled APC remodeling architecture",
        "external_record_id": "resource.msgd.database_commons.2026-06-13",
        "relationship_class": "insufficient-overlap",
        "synthesis_status": "NO_DIRECT_EXTERNAL_CORROBORATION",
        "interpretation": (
            "A curated MS gene database can provide gene-level context, but the current resource metadata does not independently assert the project's coupled HLA/IFN-APC and MIF-CD74 architecture."
        ),
        "future_grounding_action": "Import specific CD74, MIF, HLA, and APC-axis external records only as segregated future-grounding context before comparing them to V26.",
    },
    {
        "grounded_finding_id": "T/B-readable early IFN/APC/STAT1 monitoring state",
        "external_record_id": "claim.dailymed.ocrelizumab_mechanism_context.2026-06-13",
        "relationship_class": "insufficient-overlap",
        "synthesis_status": "NO_DIRECT_EXTERNAL_CORROBORATION",
        "interpretation": (
            "The ocrelizumab label contextualizes CD20-directed therapy, but it does not corroborate the project's early IFN/APC/STAT1 monitoring-state readout."
        ),
        "future_grounding_action": "Ground only in paired response data with compartment-resolved or deconvolved readouts.",
    },
    {
        "grounded_finding_id": "Postpartum HLA-II/CD64 APC-arm imbalance",
        "external_record_id": "claim.national_ms_society.rrms_course_context.2026-06-13",
        "relationship_class": "insufficient-overlap",
        "synthesis_status": "NO_DIRECT_EXTERNAL_CORROBORATION",
        "interpretation": (
            "The disease-course context is relevant to relapse/remission terminology, but it does not address postpartum APC-arm trajectories."
        ),
        "future_grounding_action": "Acquire true postpartum MS immune trajectory data with relapse-window timing.",
    },
    {
        "grounded_finding_id": "ZMIZ1 opposite-direction MS/Crohn decoupling",
        "external_record_id": "resource.disgenet.platform.2026-06-13",
        "relationship_class": "insufficient-overlap",
        "synthesis_status": "RESOURCE_CAN_QUEUE_FUTURE_CHECK",
        "interpretation": (
            "The resource may contain disease-gene assertions, but the current resource metadata record does not contain a ZMIZ1 directionality claim."
        ),
        "future_grounding_action": "Create a future-grounding task only after importing specific ZMIZ1 records with source snapshots and hashes.",
    },
    {
        "grounded_finding_id": "chr1 KIF21B/GPR25 locus resolves to real biology but hard target",
        "external_record_id": "resource.gwas_catalog.ms.2026-06-13",
        "relationship_class": "insufficient-overlap",
        "synthesis_status": "RESOURCE_CAN_QUEUE_FUTURE_CHECK",
        "interpretation": (
            "The resource metadata confirms a public association catalog exists, but it does not itself confirm the project's chr1 causal-gene/direction assessment."
        ),
        "future_grounding_action": "Import specific GWAS Catalog associations only as future-grounding records before comparison.",
    },
    {
        "grounded_finding_id": "PTGER4 mixed shared/distinct signal closes naive transfer",
        "external_record_id": "claim.ms_ibd.treatment_transfer_caution_context.2026-06-14",
        "relationship_class": "insufficient-overlap",
        "synthesis_status": "GENERAL_CONTEXT_NOT_LOCUS_CORROBORATION",
        "interpretation": (
            "The treatment-transfer caution supports the general need for mechanism-specific transfer, but it does not speak to PTGER4 fine-mapping or signal conflict."
        ),
        "future_grounding_action": "Leave PTGER4 closed unless signal-specific external data are imported and grounded.",
    },
    {
        "grounded_finding_id": "No validated broad immune-state simulator from held data",
        "external_record_id": "resource.msgd.database_commons.2026-06-13",
        "relationship_class": "insufficient-overlap",
        "synthesis_status": "NO_DIRECT_EXTERNAL_CORROBORATION",
        "interpretation": (
            "A curated MS gene database is a useful external resource, but it does not validate the project's held-out simulator negative or supply perturbation validation."
        ),
        "future_grounding_action": "Do not reopen simulator claims without a held-out perturbation dataset and frozen split.",
    },
    {
        "grounded_finding_id": "Coupled-axis successor rule does not beat scalar",
        "external_record_id": "claim.dailymed.dimethyl_fumarate_mechanism_context.2026-06-13",
        "relationship_class": "insufficient-overlap",
        "synthesis_status": "NO_DIRECT_EXTERNAL_CORROBORATION",
        "interpretation": (
            "The DMF label offers treatment context but does not evaluate whether a coupled-axis response rule improves over the locked scalar."
        ),
        "future_grounding_action": "Keep V27 negative-established unless a future external cohort is tested with the frozen scalar and any pre-locked successor under a preregistered comparison.",
    },
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scores", type=Path, default=DEFAULT_SCORES)
    parser.add_argument("--index", type=Path, default=DEFAULT_INDEX)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    return parser.parse_args()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def source_locator(row: dict[str, str]) -> str:
    return row.get("source_url") or row.get("source_doi") or row.get("source_pmid") or row.get("source_label", "")


def build_rows(scores: list[dict[str, str]], external: list[dict[str, str]]) -> list[dict[str, Any]]:
    score_by_item = {row["item"]: row for row in scores}
    external_by_id = {row["record_id"]: row for row in external}
    rows: list[dict[str, Any]] = []
    for mapping in GROUNDING_MAP:
        finding = score_by_item.get(mapping["grounded_finding_id"])
        ext = external_by_id.get(mapping["external_record_id"])
        if finding is None or ext is None:
            rows.append(
                {
                    **mapping,
                    "grounded_category": finding.get("category", "") if finding else "",
                    "grounded_evidence_grade": finding.get("evidence_grade", "") if finding else "",
                    "grounded_artifact": finding.get("supporting_artifact", "") if finding else "",
                    "external_record_type": ext.get("record_type", "") if ext else "",
                    "external_record_path": ext.get("path", "") if ext else "",
                    "epistemic_class": ext.get("epistemic_class", "") if ext else "",
                    "external_source": source_locator(ext) if ext else "",
                    "not_project_grounded_marker": ext.get("not_project_grounded_marker", "") if ext else "",
                    "row_status": "MISSING_INPUT",
                }
            )
            continue
        rows.append(
            {
                "grounded_finding_id": mapping["grounded_finding_id"],
                "grounded_category": finding.get("category", ""),
                "grounded_evidence_grade": finding.get("evidence_grade", ""),
                "grounded_artifact": finding.get("supporting_artifact", ""),
                "external_record_id": mapping["external_record_id"],
                "external_record_type": ext.get("record_type", ""),
                "external_record_path": ext.get("path", ""),
                "epistemic_class": ext.get("epistemic_class", ""),
                "external_source": source_locator(ext),
                "not_project_grounded_marker": ext.get("not_project_grounded_marker", ""),
                "relationship_class": mapping["relationship_class"],
                "synthesis_status": mapping["synthesis_status"],
                "interpretation": mapping["interpretation"],
                "future_grounding_action": mapping["future_grounding_action"],
                "row_status": "PASS",
            }
        )
    return rows


def write_markdown(path: Path, rows: list[dict[str, Any]], summary: dict[str, Any]) -> None:
    lines = [
        "# V48 Convergence / Contradiction Analysis",
        "",
        "Status: class-aware synthesis. This document compares project-grounded findings to segregated external records.",
        "",
        "Boundary rule: each external row is marked with its epistemic class, source, and explicit not-grounded marker. External agreement is corroboration context only; project artifacts remain the evidence. External disagreement would flag a future-grounding task, not override the grounded result.",
        "",
        "## Summary",
        "",
        f"- relationship rows: `{summary['n_rows']}`",
        f"- convergences asserted: `{summary['n_converges']}`",
        f"- contradictions flagged: `{summary['n_contradicts']}`",
        f"- insufficient-overlap/context rows: `{summary['n_insufficient_overlap']}`",
        f"- missing-input rows: `{summary['n_missing_input']}`",
        "",
        "## Decision-Relevant Convergences",
        "",
    ]
    convergences = [row for row in rows if row["relationship_class"] == "converges"]
    if not convergences:
        lines.append("- None.")
    for row in convergences:
        lines.append(
            f"- Grounded: `{row['grounded_finding_id']}` ({row['grounded_evidence_grade']}; source artifact: `{row['grounded_artifact']}`). "
            f"External: `{row['external_record_id']}` ({row['epistemic_class']}; source: {row['external_source']}; marker: `{row['not_project_grounded_marker']}`). "
            f"Status: `{row['synthesis_status']}`. {row['interpretation']}"
        )
    lines.extend(["", "## Contradictions Flagged", ""])
    contradictions = [row for row in rows if row["relationship_class"] == "contradicts"]
    if not contradictions:
        lines.append("- None in this pass. No external record currently overrides or directly contradicts a grounded finding.")
    for row in contradictions:
        lines.append(
            f"- Grounded: `{row['grounded_finding_id']}`. External: `{row['external_record_id']}` ({row['epistemic_class']}; source: {row['external_source']}; marker: `{row['not_project_grounded_marker']}`). {row['interpretation']}"
        )
    lines.extend(["", "## Relationship Matrix", ""])
    lines.append("| grounded finding | external record | class | source | relationship | status | interpretation |")
    lines.append("|---|---|---|---|---|---|---|")
    for row in rows:
        lines.append(
            f"| {row['grounded_finding_id']} | `{row['external_record_id']}` | `{row['epistemic_class']}` / `{row['not_project_grounded_marker']}` | {row['external_source']} | `{row['relationship_class']}` | `{row['synthesis_status']}` | {row['interpretation']} |"
        )
    lines.extend(["", "## Follow-Up Queue", ""])
    for row in rows:
        if row["future_grounding_action"]:
            lines.append(f"- `{row['grounded_finding_id']}` x `{row['external_record_id']}`: {row['future_grounding_action']}")
    path.write_text("\n".join(lines) + "\n")


def main() -> int:
    args = parse_args()
    scores = read_tsv(args.scores)
    external = read_tsv(args.index)
    rows = build_rows(scores, external)
    fields = [
        "grounded_finding_id",
        "grounded_category",
        "grounded_evidence_grade",
        "grounded_artifact",
        "external_record_id",
        "external_record_type",
        "external_record_path",
        "epistemic_class",
        "external_source",
        "not_project_grounded_marker",
        "relationship_class",
        "synthesis_status",
        "interpretation",
        "future_grounding_action",
        "row_status",
    ]
    args.outdir.mkdir(parents=True, exist_ok=True)
    write_tsv(args.outdir / "convergence_contradiction_v48.tsv", rows, fields)
    summary = {
        "purpose": "V48 convergence/contradiction synthesis; external rows are not project evidence",
        "n_rows": len(rows),
        "n_converges": sum(1 for row in rows if row["relationship_class"] == "converges"),
        "n_contradicts": sum(1 for row in rows if row["relationship_class"] == "contradicts"),
        "n_insufficient_overlap": sum(1 for row in rows if row["relationship_class"] == "insufficient-overlap"),
        "n_missing_input": sum(1 for row in rows if row["row_status"] != "PASS"),
        "overall_status": "PASS" if all(row["row_status"] == "PASS" for row in rows) else "REVIEW_NEEDED",
        "not_project_grounded_marker_required": NOT_GROUNDED,
    }
    DEFAULT_SUMMARY.parent.mkdir(parents=True, exist_ok=True)
    DEFAULT_SUMMARY.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    write_markdown(args.outdir / "CONVERGENCE_CONTRADICTION_V48.md", rows, summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["overall_status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
