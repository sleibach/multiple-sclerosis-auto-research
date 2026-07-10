#!/usr/bin/env python3
"""Build a segregated structural-feasibility map for APC-axis proteins.

The map combines project-status references with AlphaFold DB confidence and
RCSB coverage metadata. Structural availability is external context and cannot
promote a target through a failed causal, directional, or selectivity gate.
"""

from __future__ import annotations

import csv
import json
import statistics
import urllib.error
import urllib.request
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "knowledge_external/synthesis/v53_apc_structure_scout"
ALPHAFOLD_API = "https://alphafold.ebi.ac.uk/api/prediction/{accession}"
RCSB_SEARCH = "https://search.rcsb.org/rcsbsearch/v2/query"


TARGETS: tuple[dict[str, str], ...] = (
    {
        "gene": "MIF",
        "accession": "P14174",
        "axis_role": "ligand/context arm",
        "project_status": "not_promoted",
        "primary_blocker": "no MIF-specific adjusted support or stable therapy direction",
        "project_artifact": "analysis/v53_mif_cd74_grounded_audit/REPORT.md",
    },
    {
        "gene": "CD74",
        "accession": "P04233",
        "axis_role": "MHC-II chaperone/receptor-state readout",
        "project_status": "not_promoted",
        "primary_blocker": "tone-loaded state readout; no receptor-specific adjusted support",
        "project_artifact": "analysis/v53_mif_cd74_grounded_audit/REPORT.md",
    },
    {
        "gene": "CTSS",
        "accession": "P25774",
        "axis_role": "lysosomal antigen-processing effector",
        "project_status": "demoted",
        "primary_blocker": "downstream, weak causal specificity, prior systemic route underwhelming",
        "project_artifact": "knowledge/candidates/CTSS.md",
    },
    {
        "gene": "IFI30",
        "accession": "P13284",
        "axis_role": "lysosomal thiol-reductase/readout",
        "project_status": "demoted",
        "primary_blocker": "no MS expression/perturbation/modality chain; host-defense risk",
        "project_artifact": "knowledge/candidates/IFI30_GILT.md",
    },
    {
        "gene": "CIITA",
        "accession": "P33076",
        "axis_role": "MHC-II transcriptional gate",
        "project_status": "parked",
        "primary_blocker": "direct modality impractical and broad loss immunologically unsafe",
        "project_artifact": "knowledge/candidates/CIITA_SELECTIVE.md",
    },
    {
        "gene": "RFX5",
        "accession": "P48382",
        "axis_role": "selective MHC-II transcriptional controller",
        "project_status": "parked",
        "primary_blocker": "target-selective perturbation but no practical direct modality",
        "project_artifact": "knowledge/candidates/CIITA_SELECTIVE.md",
    },
    {
        "gene": "GSK3B",
        "accession": "P49841",
        "axis_role": "partial CIITA/MHC-II decoupling controller",
        "project_status": "parked_partial",
        "primary_blocker": "partial selectivity and pleiotropy",
        "project_artifact": "analysis/tier_0_triage/ciita_mediator_selectivity/decision.json",
    },
    {
        "gene": "CDK8",
        "accession": "P49336",
        "axis_role": "Mediator-kinase surrogate",
        "project_status": "parked_translation_blocked",
        "primary_blocker": "drug inhibition has not phenocopied MED16 APC selectivity",
        "project_artifact": "knowledge/candidates/CDK8_CDK19_MEDIATOR.md",
    },
    {
        "gene": "CDK19",
        "accession": "Q9BWU1",
        "axis_role": "Mediator-kinase surrogate",
        "project_status": "parked_translation_blocked",
        "primary_blocker": "drug inhibition has not phenocopied MED16 APC selectivity",
        "project_artifact": "knowledge/candidates/CDK8_CDK19_MEDIATOR.md",
    },
    {
        "gene": "IFNGR1",
        "accession": "P15260",
        "axis_role": "upstream IFN-gamma controller",
        "project_status": "broad_control_only",
        "primary_blocker": "strong module movement is broad IFN/APC collapse, not selective decoupling",
        "project_artifact": "analysis/v26_deep_structure/perturbation_module_matrix.tsv",
    },
    {
        "gene": "JAK1",
        "accession": "P23458",
        "axis_role": "upstream IFN controller",
        "project_status": "broad_control_only",
        "primary_blocker": "broad IFN/APC suppression and existing pathway-level immunosuppression",
        "project_artifact": "analysis/v26_deep_structure/perturbation_module_matrix.tsv",
    },
    {
        "gene": "STAT1",
        "accession": "P42224",
        "axis_role": "IFN/APC transcriptional controller",
        "project_status": "broad_control_only",
        "primary_blocker": "immune-tone confounder/controller rather than selective therapeutic node",
        "project_artifact": "docs/workups/treatment_response/CONFOUNDER_AUDIT_V32.md",
    },
    {
        "gene": "HLA-DRA",
        "accession": "P01903",
        "axis_role": "MHC-II output/readout",
        "project_status": "monitoring_readout",
        "primary_blocker": "direct intervention direction and safety are not established",
        "project_artifact": "docs/locked_rules/LOCKED_RULE_V22.md",
    },
)


def fetch_bytes(url: str, payload: dict[str, Any] | None = None) -> bytes:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8") if payload is not None else None,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "ms-auto-research-v53-structure-scout/1.0",
        },
        method="POST" if payload is not None else "GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:  # noqa: S310 - fixed HTTPS APIs.
            return response.read()
    except urllib.error.HTTPError as exc:
        if exc.code == 204:
            return b""
        raise RuntimeError(f"HTTP {exc.code} fetching {url}") from exc


def fetch_json(url: str, payload: dict[str, Any] | None = None) -> Any:
    body = fetch_bytes(url, payload)
    return json.loads(body.decode("utf-8")) if body else {}


def alphafold_summary(target: dict[str, str]) -> dict[str, Any]:
    api_url = ALPHAFOLD_API.format(accession=target["accession"])
    entries = fetch_json(api_url)
    if not isinstance(entries, list) or not entries:
        return {
            "alphafold_entry": "",
            "alphafold_model_version": "",
            "sequence_length": 0,
            "mean_plddt": "",
            "fraction_plddt_ge_70": "",
            "fraction_plddt_lt_50": "",
            "alphafold_source_url": api_url,
            "alphafold_status": "not_found",
        }
    entry = next(
        (row for row in entries if str(row.get("gene", "")).upper() == target["gene"].upper()),
        entries[0],
    )
    confidence_url = str(entry.get("plddtDocUrl") or "")
    confidence = fetch_json(confidence_url)
    scores = [float(value) for value in confidence.get("confidenceScore", [])]
    if not scores:
        raise RuntimeError(f"No pLDDT scores for {target['gene']} at {confidence_url}")
    return {
        "alphafold_entry": str(entry.get("modelEntityId") or entry.get("entryId") or ""),
        "alphafold_model_version": str(entry.get("latestVersion") or ""),
        "sequence_length": len(str(entry.get("uniprotSequence") or entry.get("sequence") or "")),
        "mean_plddt": round(statistics.fmean(scores), 4),
        "fraction_plddt_ge_70": round(sum(value >= 70 for value in scores) / len(scores), 6),
        "fraction_plddt_lt_50": round(sum(value < 50 for value in scores) / len(scores), 6),
        "alphafold_source_url": api_url,
        "alphafold_status": "available",
    }


def rcsb_summary(accession: str) -> dict[str, Any]:
    payload = {
        "query": {
            "type": "terminal",
            "service": "text",
            "parameters": {
                "attribute": (
                    "rcsb_polymer_entity_container_identifiers."
                    "reference_sequence_identifiers.database_accession"
                ),
                "operator": "exact_match",
                "value": accession,
            },
        },
        "return_type": "polymer_entity",
        "request_options": {"paginate": {"start": 0, "rows": 1}},
    }
    result = fetch_json(RCSB_SEARCH, payload)
    hits = [str(row["identifier"]) for row in result.get("result_set", [])]
    return {
        "rcsb_exact_uniprot_polymer_count": int(result.get("total_count") or 0),
        "rcsb_representative_polymer_entity": hits[0] if hits else "",
        "rcsb_source_url": RCSB_SEARCH,
    }


def structure_context_grade(row: dict[str, Any]) -> str:
    if row["alphafold_status"] != "available":
        return "unavailable"
    mean_plddt = float(row["mean_plddt"])
    rcsb_count = int(row["rcsb_exact_uniprot_polymer_count"])
    if mean_plddt >= 80 and rcsb_count > 0:
        return "high_context_availability"
    if mean_plddt >= 70 or rcsb_count > 0:
        return "moderate_context_availability"
    return "low_context_availability"


def write_tsv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(rows[0]),
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    rows: list[dict[str, Any]] = []
    for target in TARGETS:
        row = {**target, **alphafold_summary(target), **rcsb_summary(target["accession"])}
        row["structure_context_grade"] = structure_context_grade(row)
        row["therapeutic_gate_after_structure"] = "unchanged"
        rows.append(row)
    rows.sort(
        key=lambda row: (
            {"high_context_availability": 0, "moderate_context_availability": 1}.get(
                str(row["structure_context_grade"]), 2
            ),
            row["gene"],
        )
    )

    OUT.mkdir(parents=True, exist_ok=True)
    table_path = OUT / "apc_structure_scout.tsv"
    write_tsv(table_path, rows)
    counts = {
        grade: sum(row["structure_context_grade"] == grade for row in rows)
        for grade in (
            "high_context_availability",
            "moderate_context_availability",
            "low_context_availability",
            "unavailable",
        )
    }
    record = {
        "record_id": "V53_APC_STRUCTURE_SCOUT",
        "record_type": "external_structural_scout",
        "claim": (
            "APC-axis proteins have uneven but often substantial structural coverage; structural "
            "availability did not remove any project-defined causal, directional, selectivity, or "
            "modality blocker in this target-gated scout."
        ),
        "epistemic_class": "external-unverifiable",
        "not_project_grounded_marker": "NOT_PROJECT_GROUNDED",
        "source": {
            "label": "AlphaFold DB and RCSB PDB public APIs",
            "url": "https://alphafold.ebi.ac.uk/",
            "citation": "AlphaFold DB confidence metadata and RCSB exact-UniProt structure metadata.",
        },
        "date_accessed": datetime.now(UTC).date().isoformat(),
        "why_unverifiable": (
            "The structure predictions and experimental metadata are external records that the "
            "project did not experimentally produce or validate."
        ),
        "relationship_to_project_findings": "orthogonal",
        "relationship_note": (
            "The map tests physical context availability only; project target gates remain defined "
            "by separately cited rerunnable analyses."
        ),
        "project_use": "Structure-first triage with an explicit no-rescue rule.",
        "n_targets": len(rows),
        "structure_context_grade_counts": counts,
        "n_target_status_changes": 0,
        "table_path": str(table_path.relative_to(ROOT)),
        "limitations": [
            "Whole-chain pLDDT does not establish a druggable pocket or biologically relevant interface.",
            "RCSB entry counts measure coverage, not therapeutic suitability.",
            "No target can advance without its project-defined causal, direction, selectivity, and modality gates.",
        ],
    }
    (OUT / "record.json").write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    print(json.dumps(record, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
