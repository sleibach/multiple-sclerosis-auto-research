#!/usr/bin/env python3
"""Triage V48 insufficient-overlap rows into actionable future routes.

This is synthesis/navigation only. It does not validate any external claim and
does not change grounded findings. The goal is to prevent all insufficient
overlap rows from being treated the same: some are ready for a frozen future
test, some require source-specific import first, and some are context-only
closures unless new data arrive.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MATRIX = ROOT / "knowledge_external/synthesis/convergence_contradiction_v48.tsv"
DEFAULT_QUEUE = ROOT / "knowledge_external/synthesis/future_grounding_queue_v48.tsv"
DEFAULT_OUTDIR = ROOT / "knowledge_external/synthesis"
SUMMARY_PATH = ROOT / "knowledge_external/catalogs/indexes/v49_insufficient_overlap_triage_summary.json"


TRIAGE: dict[str, dict[str, str]] = {
    "Bounded APC/HLA-II early treatment-response monitoring scalar": {
        "triage_class": "ready_when_blind_validation_data_arrive",
        "actionability": "high",
        "next_test": "Run the frozen V42/V44 validation harness on paired labeled DMF or immune-remodeling/JAK-STAT response data.",
        "required_input": "Paired baseline/early-treatment transcriptomes, response labels, module genes, and predeclared batch/confounder metadata.",
        "reason": "The external treatment label is not validation, but the project already has a frozen harness for the exact future test.",
    },
    "V22 scalar is immune-tone bounded, not steroid/composition artifact": {
        "triage_class": "validation_guardrail_already_preregistered",
        "actionability": "high",
        "next_test": "Apply the V42/V44 confounder and batch diagnostics alongside the frozen scalar in the validation cohort.",
        "required_input": "Validation cohort with enough expression coverage to score steroid, cell-composition, metabolic, STAT1/immune-tone, and batch diagnostics.",
        "reason": "This row is not externally corroborated, but it is already converted into a mechanical validation guardrail.",
    },
    "Coupled APC remodeling architecture": {
        "triage_class": "source_specific_import_before_comparison",
        "actionability": "medium",
        "next_test": "Import source-specific CD74, MIF, HLA, IFN/APC, and APC-axis records before comparing against V26.",
        "required_input": "Specific external records or datasets with source snapshots, not resource-level metadata.",
        "reason": "Resource metadata cannot corroborate architecture; only source-specific axis records can be compared.",
    },
    "T/B-readable early IFN/APC/STAT1 monitoring state": {
        "triage_class": "needs_compartment_resolved_response_data",
        "actionability": "medium",
        "next_test": "Run the pre-registered T/B-compartment monitoring harness on paired response data with compartment-resolved or deconvolved readouts.",
        "required_input": "Paired treatment-response data with T/B compartment signal or defensible deconvolution.",
        "reason": "A CD20 therapy label is not a monitoring-state validation; the row becomes testable only with compartment-resolved response data.",
    },
    "Postpartum HLA-II/CD64 APC-arm imbalance": {
        "triage_class": "needs_true_postpartum_ms_trajectory",
        "actionability": "medium",
        "next_test": "Test HLA-II-minus-CD64 APC-arm trajectory against postpartum relapse-window timing in MS.",
        "required_input": "MS pregnancy/postpartum immune trajectory data with relapse-window timing and APC readouts.",
        "reason": "General RRMS course context is not postpartum APC evidence; the missing data type is specific and already defined.",
    },
    "ZMIZ1 opposite-direction MS/Crohn decoupling": {
        "triage_class": "source_specific_import_before_comparison",
        "actionability": "high",
        "next_test": "Import specific ZMIZ1 disease-gene, variant, QTL, or direction records, then compare to the project's MS/Crohn directionality.",
        "required_input": "Source-specific ZMIZ1 records with disease, direction, variant/gene mapping, and source snapshots.",
        "reason": "The current DisGeNET row is only resource metadata; source-specific ZMIZ1 direction records are readily definable.",
    },
    "chr1 KIF21B/GPR25 locus resolves to real biology but hard target": {
        "triage_class": "source_specific_import_before_comparison",
        "actionability": "high",
        "next_test": "Import specific GWAS Catalog or fine-mapping association records for KIF21B/GPR25 and compare direction/tractability to V19.",
        "required_input": "Signal-specific associations or fine-mapping/QTL records with variant, effect, trait, and date/version.",
        "reason": "Catalog-level existence is insufficient, but the source-specific import path is concrete.",
    },
    "PTGER4 mixed shared/distinct signal closes naive transfer": {
        "triage_class": "closed_unless_signal_specific_data_arrive",
        "actionability": "low",
        "next_test": "Only reopen if PTGER4-specific fine-mapping, QTL, or treatment-transfer data directly address the mixed-signal failure mode.",
        "required_input": "PTGER4 signal-specific external data with direction and disease-layer definitions.",
        "reason": "General treatment-transfer caution is context only; the project finding is already negative-established for naive transfer.",
    },
    "No validated broad immune-state simulator from held data": {
        "triage_class": "closed_unless_new_perturbation_validation_data_arrive",
        "actionability": "low",
        "next_test": "Do not reopen simulator claims without a held-out perturbation dataset and frozen split.",
        "required_input": "Held-out perturbation or response dataset suitable for simulator validation.",
        "reason": "External resource metadata cannot address the simulator validation failure.",
    },
    "Coupled-axis successor rule does not beat scalar": {
        "triage_class": "closed_unless_preregistered_external_comparison_arrives",
        "actionability": "low",
        "next_test": "Retest only under a preregistered external scalar-versus-successor comparison.",
        "required_input": "External cohort with frozen scalar and any pre-locked successor evaluated under the V27/V42 comparison rules.",
        "reason": "A treatment label cannot evaluate the predictive comparison; current project result remains negative-established.",
    },
    "Locked V7 general cross-disease baseline fallback killed": {
        "triage_class": "closed_unless_same_failure_mode_dataset_arrives",
        "actionability": "low",
        "next_test": "Only retest the baseline fallback in a predefined external dataset directly matching the cross-disease baseline-fallback rule.",
        "required_input": "Dataset with baseline-only cross-disease transfer structure and predefined failure-mode comparison.",
        "reason": "Generic prediction-model guidance supports discipline but not the specific kill.",
    },
    "Crohn downstream IFN/APC convergence exceeds genetic proximity": {
        "triage_class": "needs_crohn_response_data",
        "actionability": "medium",
        "next_test": "Test downstream IFN/APC response convergence in Crohn paired response data before using Crohn as a monitoring comparator.",
        "required_input": "Crohn paired treatment-response transcriptomic data with IFN/APC module coverage.",
        "reason": "MS-UC/MS-CD genetic proximity context does not test downstream response convergence.",
    },
    "RA pregnancy comparator but blood APC treatment-response nontransfer": {
        "triage_class": "context_only_until_ms_or_ra_response_transfer_data",
        "actionability": "low",
        "next_test": "Use RA/SLE pregnancy data for timing context only unless paired MS/RA treatment-response transfer data are acquired.",
        "required_input": "Paired treatment-response transfer data, not pregnancy transcriptome context alone.",
        "reason": "Pregnancy transcriptomes help postpartum timing questions but do not test blood APC treatment-response nontransfer.",
    },
    "EBV/IFN APC imprint downgraded by specificity control": {
        "triage_class": "needs_ebv_stratified_expression_with_specificity_controls",
        "actionability": "medium",
        "next_test": "Rerun the imprint test only with EBV-stratified expression and predefined autoimmune/control specificity panels.",
        "required_input": "EBV-stratified MS/control/comparator transcriptomes with enough APC/IFN module coverage.",
        "reason": "EBV-MS risk context does not rescue a specificity-failed APC/IFN imprint.",
    },
    "GPR25 demoted from protected favorite": {
        "triage_class": "closed_unless_direction_and_tractability_evidence_arrive",
        "actionability": "low",
        "next_test": "Only reconsider if signal-specific direction and tractability evidence directly resolves the V19 demotion reason.",
        "required_input": "GPR25-specific direction, QTL, fine-mapping, and tractability evidence.",
        "reason": "External nomination of GPR25 as a putative gene is not direction-matched target evidence.",
    },
    "No load-bearing invariant found in V26": {
        "triage_class": "closed_until_null_tested_invariant_candidate_exists",
        "actionability": "low",
        "next_test": "Do not promote an invariant unless a new candidate passes cross-modality null-tested invariant gates.",
        "required_input": "A predefined invariant candidate and cross-modality data sufficient for null/permutation testing.",
        "reason": "General biomarker heterogeneity context is not an invariant-search replication.",
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--matrix", type=Path, default=DEFAULT_MATRIX)
    parser.add_argument("--queue", type=Path, default=DEFAULT_QUEUE)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    return parser.parse_args()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def md(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def build_rows(matrix_rows: list[dict[str, str]], queue_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    queue_by_pair = {(row["grounded_finding_id"], row["external_record_id"]): row for row in queue_rows}
    rows: list[dict[str, str]] = []
    for row in matrix_rows:
        if row.get("relationship_class") != "insufficient-overlap":
            continue
        finding = row["grounded_finding_id"]
        triage = TRIAGE[finding]
        queue_row = queue_by_pair.get((finding, row["external_record_id"]), {})
        rows.append(
            {
                "grounded_finding_id": finding,
                "external_record_id": row["external_record_id"],
                "synthesis_status": row["synthesis_status"],
                "queue_priority": queue_row.get("priority", ""),
                **triage,
                "future_grounding_action": row["future_grounding_action"],
            }
        )
    return rows


def write_markdown(path: Path, rows: list[dict[str, str]], summary: dict[str, Any]) -> None:
    lines = [
        "# V49 Insufficient-Overlap Triage",
        "",
        "Status: synthesis/navigation only. This document classifies existing insufficient-overlap rows so future work does not mistake context for corroboration.",
        "",
        "Boundary: rows here remain not corroborated by the paired external source. A listed next test is a future route, not a finding, and no grounded project conclusion is changed.",
        "",
        "## Summary",
        "",
        f"- insufficient-overlap rows triaged: `{summary['n_rows']}`",
        f"- high actionability rows: `{summary['actionability_counts'].get('high', 0)}`",
        f"- medium actionability rows: `{summary['actionability_counts'].get('medium', 0)}`",
        f"- low actionability rows: `{summary['actionability_counts'].get('low', 0)}`",
        "",
        "## Actionability Classes",
        "",
        "| actionability | class | count |",
        "|---|---|---:|",
    ]
    for triage_class, count in sorted(summary["triage_class_counts"].items()):  # type: ignore[index, union-attr]
        actionability = next(row["actionability"] for row in rows if row["triage_class"] == triage_class)
        lines.append(f"| `{actionability}` | `{triage_class}` | {count} |")
    lines.extend(
        [
            "",
            "## Rows",
            "",
            "| finding | external record | actionability | triage class | next test | required input | reason |",
            "|---|---|---|---|---|---|---|",
        ]
    )
    for row in rows:
        lines.append(
            "| "
            f"{md(row['grounded_finding_id'])} | "
            f"`{md(row['external_record_id'])}` | "
            f"`{md(row['actionability'])}` | "
            f"`{md(row['triage_class'])}` | "
            f"{md(row['next_test'])} | "
            f"{md(row['required_input'])} | "
            f"{md(row['reason'])} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `high` means the row has a concrete frozen-harness or source-specific import route already defined.",
            "- `medium` means the row is scientifically testable but needs a specific data type not currently in hand.",
            "- `low` means the row should stay closed or context-only unless a narrowly matching future source arrives.",
            "- No row in this file is evidence for or against the underlying grounded finding; the V37/V48 grounded artifacts remain authoritative.",
            "",
        ]
    )
    path.write_text("\n".join(lines))


def main() -> int:
    args = parse_args()
    matrix_rows = read_tsv(args.matrix)
    queue_rows = read_tsv(args.queue)
    rows = build_rows(matrix_rows, queue_rows)
    action_counts: dict[str, int] = {}
    class_counts: dict[str, int] = {}
    for row in rows:
        action_counts[row["actionability"]] = action_counts.get(row["actionability"], 0) + 1
        class_counts[row["triage_class"]] = class_counts.get(row["triage_class"], 0) + 1
    summary = {
        "purpose": "V49 insufficient-overlap triage; synthesis/navigation only; no biological claim",
        "n_rows": len(rows),
        "actionability_counts": dict(sorted(action_counts.items())),
        "triage_class_counts": dict(sorted(class_counts.items())),
        "overall_status": "PASS" if len(rows) == 16 else "REVIEW_NEEDED",
        "markdown": "knowledge_external/synthesis/V49_INSUFFICIENT_OVERLAP_TRIAGE.md",
        "tsv": "knowledge_external/synthesis/v49_insufficient_overlap_triage.tsv",
    }
    fields = [
        "grounded_finding_id",
        "external_record_id",
        "synthesis_status",
        "queue_priority",
        "triage_class",
        "actionability",
        "next_test",
        "required_input",
        "reason",
        "future_grounding_action",
    ]
    args.outdir.mkdir(parents=True, exist_ok=True)
    write_tsv(args.outdir / "v49_insufficient_overlap_triage.tsv", rows, fields)
    write_markdown(args.outdir / "V49_INSUFFICIENT_OVERLAP_TRIAGE.md", rows, summary)
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["overall_status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
