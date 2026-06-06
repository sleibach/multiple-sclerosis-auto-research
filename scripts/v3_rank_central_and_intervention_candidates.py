#!/usr/bin/env python3
"""Rank V3 central-mechanism and intervention candidates.

This is an explicit triage score, not a causal estimator. It integrates only
V3 traceable outputs:

- direct h5ad donor-level module replication;
- MS GSE111972 module replication;
- Mixscale IFN-gamma CRISPRi perturbation effects;
- OpenTargets candidate-disease evidence;
- EuropePMC/ClinicalTrials prior-art audit counts.

The goal is to prevent narrative drift by separating two scores:

- centrality_score: how well the candidate explains the recurring state;
- intervention_score: how tractable/novel the candidate is as a therapeutic
  handle after prior-art and druggability penalties.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "phases/v3/results"


@dataclass(frozen=True)
class Candidate:
    name: str
    genes: tuple[str, ...]
    modules: tuple[str, ...]
    mixscale_perturbations: tuple[str, ...]
    prior_art_key: str
    druggability: float
    selectivity: float
    notes: str


CANDIDATES = [
    Candidate(
        name="IFNGR_JAK_STAT1_upstream_control",
        genes=("IFNGR1", "IFNGR2", "JAK1", "JAK2", "STAT1"),
        modules=("ifn_apc", "mixscale_validated_ifng_readout", "hla_ii_apc"),
        mixscale_perturbations=("IFNGR1", "IFNGR2", "JAK1", "JAK2", "STAT1"),
        prior_art_key="IFNG_IFNGR_axis",
        druggability=0.80,
        selectivity=0.25,
        notes="Strong controller; broad immunosuppression and heavy prior art.",
    ),
    Candidate(
        name="CIITA_RFX5_HLAII_transcriptional_gate",
        genes=("CIITA", "RFX5", "NLRC5"),
        modules=("hla_ii_apc", "mif_cd74_receptor_state"),
        mixscale_perturbations=("RFX5",),
        prior_art_key="CIITA_RFX5_HLAII_gate",
        druggability=0.25,
        selectivity=0.45,
        notes="Mechanistically narrow HLA-II gate; transcription-factor druggability weak.",
    ),
    Candidate(
        name="IFI30_GILT_lysosomal_feedback_effector",
        genes=("IFI30",),
        modules=("lysosomal_apc", "mixscale_validated_ifng_readout"),
        mixscale_perturbations=(),
        prior_art_key="IFI30_GILT",
        druggability=0.55,
        selectivity=0.60,
        notes="Enzymatic lysosomal effector; low clinical prior art but chemical matter uncertain.",
    ),
    Candidate(
        name="CTSS_cathepsinS_lysosomal_effector",
        genes=("CTSS",),
        modules=("lysosomal_apc", "mixscale_validated_ifng_readout"),
        mixscale_perturbations=(),
        prior_art_key="CTSS_cathepsin_S",
        druggability=0.85,
        selectivity=0.55,
        notes="Druggable enzyme; autoimmune clinical history and prior art are unfavorable.",
    ),
    Candidate(
        name="CD74_HLAII_receptor_APC_state_biomarker",
        genes=("CD74", "HLA-DRA", "HLA-DRB1", "HLA-DPA1", "HLA-DPB1", "CD44", "CXCR4"),
        modules=("mif_cd74_receptor_state", "hla_ii_apc"),
        mixscale_perturbations=("RFX5", "IFNGR1", "IFNGR2", "JAK1", "JAK2", "STAT1"),
        prior_art_key="CD74_MIF",
        druggability=0.45,
        selectivity=0.35,
        notes="Strong state/biomarker; direct CD74/MIF therapeutic claim is prior-art blocked.",
    ),
]


def load_tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t") if path.exists() else pd.DataFrame()


def clipped_log_count(x: float) -> float:
    if not np.isfinite(x) or x <= 0:
        return 0.0
    return min(4.0, math.log10(x + 1.0))


def direct_h5ad_score(candidate: Candidate) -> tuple[float, list[str]]:
    df = load_tsv(OUT / "direct_h5ad_cell_state" / "direct_h5ad_donor_module_comparisons.tsv")
    if df.empty:
        return 0.0, []
    sub = df[
        (df["metric"] == "mean_score")
        & (df["module"].isin(candidate.modules))
        & (df["delta_case_minus_control"] > 0)
        & (df["fdr"] <= 0.10)
    ].copy()
    details = []
    score = 0.0
    for _, row in sub.iterrows():
        disease = str(row["disease_name"])
        compartment = str(row["compartment"])
        effect = float(row["hedges_g"]) if pd.notna(row["hedges_g"]) else 0.0
        fdr = float(row["fdr"])
        score += min(3.0, max(0.0, effect)) * (1.0 if fdr <= 0.05 else 0.75)
        details.append(f"{row['analysis']}:{row['module']}:g={effect:.3f}:FDR={fdr:.3g}:{disease}:{compartment}")
    return score, details


def ms_gse111972_score(candidate: Candidate) -> tuple[float, list[str]]:
    df = load_tsv(OUT / "gse111972_module_contrasts.tsv")
    if df.empty:
        return 0.0, []
    feature_to_module = {
        "interferon_apc": "ifn_apc",
        "lysosome_antigen_processing": "lysosomal_apc",
    }
    df = df.copy()
    df["module"] = df["feature"].map(feature_to_module).fillna(df["feature"])
    sub = df[
        (df["module"].isin(candidate.modules))
        & (df["contrast"] == "MS_WM_vs_CON_WM")
        & (df["delta_log2"] > 0)
        & (df["fdr"] <= 0.10)
    ].copy()
    score = 0.0
    details = []
    for _, row in sub.iterrows():
        effect = float(row["hedges_g"]) if pd.notna(row["hedges_g"]) else 0.0
        fdr = float(row["fdr"])
        score += min(3.0, max(0.0, effect)) * (1.0 if fdr <= 0.05 else 0.75)
        details.append(f"{row['module']}:g={effect:.3f}:FDR={fdr:.3g}")
    return score, details


def thyroid_spatial_score(candidate: Candidate) -> tuple[float, list[str]]:
    df = load_tsv(OUT / "gse248205_thyroid_spatial" / "gse248205_module_gene_contrasts.tsv")
    if df.empty:
        return 0.0, []
    sub = df[
        (df["contrast"] == "Hashimoto thyroiditis_vs_control")
        & (df["feature_type"] == "module")
        & (df["feature"].isin(candidate.modules))
        & (df["delta_case_minus_control"] > 0)
        & (df["fdr"] <= 0.10)
    ].copy()
    score = 0.0
    details = []
    for _, row in sub.iterrows():
        effect = float(row["hedges_g"]) if pd.notna(row["hedges_g"]) else 0.0
        fdr = float(row["fdr"])
        # Spatial sample-level n is only 2 controls and 3 Hashimoto cases.
        # Cap each module heavily so the route-around dataset cannot dominate
        # the cross-disease rank despite its very large standardized effects.
        score += min(1.5, max(0.0, effect)) * (1.0 if fdr <= 0.05 else 0.75)
        details.append(f"{row['feature']}:g={effect:.3f}:FDR={fdr:.3g}:Hashimoto thyroid spatial")
    return score, details


def celiac_marker_score(candidate: Candidate) -> tuple[float, list[str]]:
    df = load_tsv(OUT / "gse315138_celiac_marker" / "gse315138_donor_module_comparisons.tsv")
    if df.empty:
        return 0.0, []
    sub = df[
        (df["metric"] == "mean_score")
        & (df["module"].isin(candidate.modules))
        & (df["delta_case_minus_control"] > 0)
        & (df["p"] <= 0.10)
    ].copy()
    score = 0.0
    details = []
    for _, row in sub.iterrows():
        effect = float(row["hedges_g"]) if pd.notna(row["hedges_g"]) else 0.0
        p = float(row["p"])
        # GSE315138 lacks curated cell labels and has only two controls.
        # Cap each marker-compartment contribution so it informs breadth
        # without dominating validated h5ad/spatial/perturbation evidence.
        score += min(0.75, max(0.0, effect)) * (1.0 if p <= 0.05 else 0.65)
        details.append(f"{row['compartment']}:{row['module']}:g={effect:.3f}:p={p:.3g}:marker-compartment")
    return score, details


def mixscale_controller_score(candidate: Candidate) -> tuple[float, list[str]]:
    df = load_tsv(OUT / "mixscale" / "mixscale_module_summary.tsv")
    if df.empty:
        return 0.0, []
    modules = set(candidate.modules) | {"ifn_apc", "hla_ii_apc", "gilt_lysosomal_apc"}
    sub = df[
        (df["pathway"] == "IFNG")
        & (df["perturbation"].isin(candidate.mixscale_perturbations))
        & (df["module"].isin(modules))
    ].copy()
    score = 0.0
    details = []
    for _, row in sub.iterrows():
        effect = float(row["mean_module_log2fc_across_cell_types"])
        neg_fraction = float(row["cell_type_negative_fraction"])
        if effect < 0:
            score += min(2.0, abs(effect)) * neg_fraction
        details.append(f"{row['perturbation']}->{row['module']}:{effect:.3f}:negFrac={neg_fraction:.2f}")
    return score, details


def mixscale_readout_score(candidate: Candidate) -> tuple[float, list[str]]:
    df = load_tsv(OUT / "mixscale" / "mixscale_readout_gene_summary.tsv")
    if df.empty:
        return 0.0, []
    upstream = ("IFNGR1", "IFNGR2", "JAK1", "JAK2", "STAT1")
    sub = df[
        (df["pathway"] == "IFNG")
        & (df["perturbation"].isin(upstream))
        & (df["gene"].isin(candidate.genes))
    ].copy()
    score = 0.0
    details = []
    for _, row in sub.iterrows():
        effect = float(row["mean_log2fc"])
        neg_fraction = float(row["negative_fraction"])
        if effect < 0:
            score += min(1.5, abs(effect)) * neg_fraction
        details.append(f"{row['perturbation']}->{row['gene']}:{effect:.3f}:negFrac={neg_fraction:.2f}")
    return score, details


def genetics_score(candidate: Candidate) -> tuple[float, list[str]]:
    df = load_tsv(OUT / "opentargets_candidate_disease_hits.tsv")
    if df.empty:
        return 0.0, []
    sub = df[df["target"].isin(candidate.genes)].copy()
    details = []
    score = 0.0
    for _, row in sub.iterrows():
        genetic = row.get("datatype_genetic_association")
        genetic = 0.0 if pd.isna(genetic) else float(genetic)
        overall = row.get("overall_score")
        overall = 0.0 if pd.isna(overall) else float(overall)
        increment = max(genetic, 0.25 * overall)
        score += increment
        details.append(f"{row['disease']}:{row['target']}:genetic={genetic:.3f}:overall={overall:.3f}")
    return score, details


def prior_art_penalty(candidate: Candidate) -> tuple[float, list[str]]:
    df = load_tsv(OUT / "intervention_prior_art_audit.tsv")
    if df.empty:
        return 0.0, []
    sub = df[df["candidate"] == candidate.prior_art_key]
    lit = sub[sub["source"].eq("EuropePMC")]["hit_count"].dropna().astype(float)
    trials = sub[sub["source"].eq("ClinicalTrials.gov")]["hit_count"].dropna().astype(float)
    lit_penalty = float(lit.map(clipped_log_count).sum()) * 0.35
    trial_penalty = float(trials.sum()) * 0.18
    details = [
        f"EuropePMC_log_penalty={lit_penalty:.3f}",
        f"ClinicalTrials_penalty={trial_penalty:.3f}",
        f"queries={len(sub)}",
    ]
    return lit_penalty + trial_penalty, details


def main() -> None:
    rows = []
    detail = {}
    for cand in CANDIDATES:
        direct_score, direct_detail = direct_h5ad_score(cand)
        ms_score, ms_detail = ms_gse111972_score(cand)
        thyroid_score, thyroid_detail = thyroid_spatial_score(cand)
        celiac_score, celiac_detail = celiac_marker_score(cand)
        controller_score, controller_detail = mixscale_controller_score(cand)
        readout_score, readout_detail = mixscale_readout_score(cand)
        genetic_score, genetic_detail = genetics_score(cand)
        prior_penalty, prior_detail = prior_art_penalty(cand)
        centrality = direct_score + ms_score + thyroid_score + celiac_score + controller_score + 0.75 * readout_score + 1.5 * genetic_score
        intervention = centrality + 4.0 * cand.druggability + 3.0 * cand.selectivity - prior_penalty
        rows.append(
            {
                "candidate": cand.name,
                "centrality_score": centrality,
                "intervention_score": intervention,
                "direct_h5ad_score": direct_score,
                "ms_gse111972_score": ms_score,
                "thyroid_spatial_score": thyroid_score,
                "celiac_marker_score": celiac_score,
                "mixscale_controller_score": controller_score,
                "mixscale_readout_score": readout_score,
                "opentargets_genetics_score": genetic_score,
                "druggability_assumption": cand.druggability,
                "selectivity_assumption": cand.selectivity,
                "prior_art_penalty": prior_penalty,
                "genes": ",".join(cand.genes),
                "modules": ",".join(cand.modules),
                "notes": cand.notes,
            }
        )
        detail[cand.name] = {
            "direct_h5ad": direct_detail,
            "ms_gse111972": ms_detail,
            "thyroid_spatial": thyroid_detail,
            "celiac_marker": celiac_detail,
            "mixscale_controller": controller_detail,
            "mixscale_readout": readout_detail,
            "opentargets": genetic_detail,
            "prior_art": prior_detail,
            "scoring_caveat": (
                "Scores are rank-aggregation heuristics. They are designed to force transparent "
                "tradeoffs, not to estimate causal effect sizes."
            ),
        }
    out = pd.DataFrame(rows).sort_values(["centrality_score", "intervention_score"], ascending=False)
    out.to_csv(OUT / "central_and_intervention_candidate_rank.tsv", sep="\t", index=False)
    (OUT / "central_and_intervention_candidate_rank_detail.json").write_text(json.dumps(detail, indent=2) + "\n")
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
