#!/usr/bin/env python3
"""Build a machine-readable, artifact-backed ledger of V53 outcomes."""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis/v53_outcome_ledger"
LEDGER = ROOT / "knowledge_external/synthesis/V53_OUTCOME_LEDGER.tsv"


ENTRIES = [
    ("B", "MIF/CD74 target audit", "agent", "grounded-real-data", "not-supported", "analysis/v53_mif_cd74_grounded_audit/summary.json", "No adjusted receptor-specific therapeutic signal or consistent direction."),
    ("A/B", "MIF/CD74 structure context", "AlphaFold/PDB", "external-unverifiable-prediction-context", "inconclusive", "knowledge_external/synthesis/v53_mif_cd74_structure_context/record.json", "Structure adds context but cannot repair causal or directional gaps."),
    ("A", "APC-axis structure-first target scout", "AlphaFold", "external-unverifiable-prediction-context", "not-supported", "knowledge_external/synthesis/v53_apc_structure_scout/record.json", "No target gate changed across 13 proteins."),
    ("C", "Additive two-node intervention probe", "agent", "grounded-real-data", "not-supported", "analysis/v53_combinatorial_intervention_probe/summary.json", "No pair survived BH plus max-T correction."),
    ("D", "Association-network control-node probe", "agent", "grounded-real-data", "not-supported", "analysis/v53_network_control_probe/summary.json", "No corrected cross-context control node; RFX5 remains nominal only."),
    ("E", "Claude/Gemini divergent proposals", "Claude/Gemini", "model-proposal-only", "triaged", "analysis/v53_model_proposal_grounding/summary.json", "One methodological negative supported; no biological lead promoted."),
    ("E", "RPT feasibility lens", "SAP RPT", "model-proposal-only", "consistency-only", "knowledge_external/model_outputs/v53_rpt_proposal_lens/record.json", "Matched encoded schema feasibility; no independent biology."),
    ("D", "Causal-equivalence orientation", "agent", "grounded-method", "supported-boundary", "analysis/v53_model_proposal_grounding/causal_identifiability_summary.json", "Current three-edge summaries identify no consensus direction."),
    ("D", "Causal-identifiability skeleton sensitivity", "agent", "grounded-method", "supported-boundary", "analysis/v53_causal_identifiability_sensitivity/summary.json", "Zero consensus-oriented edges across all 10 skeleton variants."),
    ("D", "Matrix semantic contract", "agent", "grounded-method", "supported-boundary", "analysis/v53_matrix_semantic_contract/contract_audit_summary.json", "72 real checks pass; unsupported patient/temporal requests fail closed."),
    ("D", "RFX5 replication boundary", "agent", "grounded-real-plus-synthetic-method", "needs-data", "analysis/v53_rfx5_replication_boundary/summary.json", "Single-context nominal signal fails corrected network gates."),
    ("D/E", "Multi-lineage identifiability critique", "Claude/Gemini+agent", "model-proposal-grounded-method", "supported-boundary", "analysis/v53_identifiability_critique/summary.json", "Objections tightened wording; no verdict changed."),
    ("D", "Orientation acquisition design", "agent", "synthetic-method-only", "needs-data", "analysis/v53_causal_orientation_design/summary.json", "Selective instruments and powered intervention cohorts are absent."),
    ("D", "Cross-environment invariance feasibility", "agent", "grounded-schema-audit", "needs-data", "analysis/v53_invariance_feasibility_audit/summary.json", "Zero of five routes meet the harmonized environment contract."),
    ("D", "Perturbation module de-overlap", "agent", "grounded-real-data", "not-supported", "analysis/v53_deoverlapped_module_sensitivity/summary.json", "HLA/receptor edge fails the disjoint context-stratified gate."),
    ("D", "Cell-state module de-overlap", "agent", "grounded-real-data", "not-supported", "analysis/v53_cell_state_deoverlap_sensitivity/summary.json", "HLA/receptor edge collapses after globally unique scoring."),
    ("D", "Treatment-response module de-overlap", "agent", "grounded-real-data", "not-supported", "analysis/v53_treatment_response_deoverlap_sensitivity/summary.json", "HLA/receptor edge collapses after globally unique scoring."),
    ("D", "Pharmacodynamic module de-overlap", "agent", "grounded-real-data", "supported-within-layer", "analysis/v53_pharmacodynamic_deoverlap_sensitivity/summary.json", "Disjoint rank edge persists in this layer only."),
    ("D", "Pharmacodynamic portability stress", "agent", "grounded-real-data", "not-supported", "analysis/v53_pharmacodynamic_edge_robustness/summary.json", "Centered, cluster-bootstrap, and LODO tests reject a portable common effect."),
    ("D", "Cross-disease summary lineage audit", "agent", "grounded-source-audit", "supported-boundary", "analysis/v53_cross_disease_summary_lineage_audit/summary.json", "Derived matrix retired as an independent fifth modality."),
    ("D", "Physical-dataset APC recurrence", "agent", "grounded-real-data", "supported", "analysis/v53_additional_atlas_disjoint_rescoring/summary.json", "IFN/APC and CD44/CXCR4 each recur positively in 7/8 datasets; HLA does not."),
    ("D", "Pharmacodynamic response semantics", "agent", "grounded-real-data", "not-supported", "analysis/v53_pharmacodynamic_context_decomposition/summary.json", "The surviving rank edge is not response-structured."),
    ("D", "GSE111972 CD44/CXCR4 association", "agent", "grounded-real-data", "supported-provisional", "analysis/v53_ms_microglia_receptor_decoupling/summary.json", "State association passes; decoupling does not."),
    ("D", "GSE111972 age/region robustness", "agent", "grounded-real-data", "supported", "analysis/v53_ms_microglia_age_region_robustness/summary.json", "Association survives age, region, and influence gates within cohort."),
    ("D", "GSE111972 component specificity", "agent", "grounded-real-data", "not-supported", "analysis/v53_ms_microglia_component_specificity/summary.json", "Joint APC-state adjustment defeats receptor-specific interpretation."),
    ("F", "CD44/CXCR4 prior-art audit", "literature", "external-unverifiable-context", "low-novelty", "knowledge_external/synthesis/V53_CD44_CXCR4_MS_MICROGLIA_PRIOR_ART.md", "Biology is low novelty; exact adjusted analysis is moderate novelty at most."),
    ("F", "Frozen microglia replication specification", "agent", "grounded-method", "ready", "analysis/v53_ms_microglia_replication_spec/summary.json", "Independent-cohort score, model, null, and interpretation are frozen."),
    ("D/F", "Macnair frozen-score replication", "agent", "grounded-real-data", "supported-quality-qualified", "analysis/v53_ms_microglia_independent_cohort_scout/summary.json", "Both partitions pass the frozen primary; discovery is depth-sensitive."),
    ("D", "Macnair lesion/stage localization", "agent", "grounded-real-data", "supported-partial", "analysis/v53_macnair_stage_lesion_heterogeneity/summary.json", "White-matter state supported; stage specificity and lesion amplification are not."),
    ("D", "Microglia source-lineage audit", "agent", "grounded-source-audit", "supported-boundary", "analysis/v53_microglia_source_lineage_audit/summary.json", "Macnair is one package with two partitions; person-level independence is not provable."),
    ("D", "Macnair source-family influence", "agent", "grounded-real-data", "not-supported", "analysis/v53_macnair_source_influence/summary.json", "Discovery attenuates after brain-bank adjustment; validation remains robust."),
    ("D", "Package-aware cross-cohort synthesis", "agent", "grounded-real-data", "supported-quality-qualified", "analysis/v53_microglia_cross_cohort_meta/summary.json", "Positive effects are heterogeneous and limited to two package families."),
    ("D", "GSE301908 low-control sensitivity", "agent", "grounded-real-data", "not-supported", "analysis/v53_gse301908_low_control_sensitivity/summary.json", "Positive point estimate is unsupported with three controls and normalized-data-only input."),
    ("F", "V22 interpretation boundary", "agent", "grounded-method", "unchanged", "analysis/v53_v22_interpretation_boundary/summary.json", "V53 changes no locked score, threshold, confounder list, or harness behavior."),
]


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def artifact_verdict(path: Path) -> str:
    if path.suffix != ".json":
        return ""
    payload = json.loads(path.read_text())
    for key in ("verdict", "overall_status", "status"):
        if key in payload and not isinstance(payload[key], (dict, list)):
            return str(payload[key])
    return ""


def main() -> int:
    rows = []
    for workstream, probe, source, evidence_class, outcome, artifact_name, boundary in ENTRIES:
        artifact = ROOT / artifact_name
        if not artifact.is_file():
            raise FileNotFoundError(artifact)
        rows.append(
            {
                "workstream": workstream,
                "probe": probe,
                "proposal_source": source,
                "epistemic_class": evidence_class,
                "grounded_outcome": outcome,
                "artifact": artifact_name,
                "artifact_sha256": digest(artifact),
                "artifact_verdict": artifact_verdict(artifact),
                "interpretation_boundary": boundary,
            }
        )
    OUT.mkdir(parents=True, exist_ok=True)
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    counts = Counter(row["grounded_outcome"] for row in rows)
    summary = {
        "purpose": "Machine-readable V53 outcome index; no new claim",
        "n_entries": len(rows),
        "n_artifacts_missing": 0,
        "outcome_counts": dict(sorted(counts.items())),
        "ledger": str(LEDGER.relative_to(ROOT)),
        "overall_status": "PASS",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    (OUT / "REPORT.md").write_text(
        "# V53 Outcome Ledger\n\n"
        f"Status: **PASS**. `{len(rows)}` V53 probes/boundaries are indexed with "
        "source, epistemic class, current outcome, artifact path, SHA-256, and an "
        "interpretation boundary. This is navigation metadata and adds no claim.\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
