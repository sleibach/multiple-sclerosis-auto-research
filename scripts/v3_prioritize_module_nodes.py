#!/usr/bin/env python3
"""First-pass V3 central-node ranking from existing reproducible outputs.

This is a triage script, not a causal analysis. It integrates the V2
cross-autoimmune screens with the existing MS proteome/snRNA/spatial outputs,
splits the old lipid-lysosomal module into mechanistic axes, and ranks genes
for follow-up by breadth, consistency, MS anchoring, and prior demotion flags.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20260526
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "phases/v3/results"


AXES: dict[str, list[str]] = {
    "lipid_droplet_efflux": [
        "ACSL1",
        "APOE",
        "GPNMB",
        "LPL",
        "TREM2",
        "PLIN2",
        "CD36",
        "FABP5",
        "LIPA",
        "MERTK",
        "MSR1",
        "MARCO",
        "ASAH1",
    ],
    "lysosome_antigen_processing": ["IFI30", "CTSD", "CTSB", "CTSL", "TPP1", "LAMP1", "LIPA", "ASAH1"],
    "complement_phagocytosis": ["C1QA", "C1QB", "C1QC", "CD68", "TREM2", "MERTK", "MSR1", "MARCO"],
    "interferon_chemokine": ["CXCL10", "STAT1", "IRF1", "IRF7", "IFI30", "TNF", "IL1B", "NFKBIA", "CCL2", "CCL3", "CCL4"],
    "metabolic_licensing": ["NAMPT", "HIF1A", "SLC2A1", "LDHA", "NFKBIA", "TNF", "IL1B"],
    "tissue_remodeling": ["SPP1", "GPNMB", "MERTK", "TREM2", "APOE", "LPL", "MARCO"],
}

PRIOR_FLAGS: dict[str, str] = {
    "ACSL1": "demoted_v2_marker_after_module_adjustment_and_simulation",
    "NAMPT": "strong_v2_successor_but_broad_prior_art_and_direction_ambiguity",
}


def neglog10(p: float | int | None) -> float:
    if p is None or pd.isna(p):
        return 0.0
    return min(12.0, -math.log10(max(float(p), 1e-300)))


def signed_score(effect: float | int | None, p: float | int | None, quality: float) -> float:
    if effect is None or pd.isna(effect):
        return 0.0
    sign = 1.0 if float(effect) > 0 else -1.0 if float(effect) < 0 else 0.0
    return sign * quality * (0.5 + min(3.0, abs(float(effect))) / 2.0) * (1.0 + neglog10(p) / 6.0)


def disease_from_comparison(comparison: str, dataset: str) -> str:
    if dataset == "GSE97779":
        return "RA"
    if dataset == "GSE13355":
        return "psoriasis"
    if comparison.startswith("UC_"):
        return "UC"
    if comparison.startswith("CD_"):
        return "Crohn"
    if comparison.startswith("LN_"):
        return "lupus_nephritis"
    if comparison.startswith("SLE_myeloid"):
        return "SLE_myeloid"
    if comparison.startswith("SLE_CD4"):
        return "SLE_CD4_T"
    if comparison.startswith("SLE_CD19"):
        return "SLE_B"
    if comparison.startswith("Sjogren"):
        return "Sjogren"
    return dataset


def quality_weight(row: pd.Series) -> float:
    dataset = str(row.get("dataset", ""))
    comparison = str(row.get("comparison", ""))
    limitation = str(row.get("limitation", "")).lower()
    if dataset == "MS":
        return float(row.get("quality", 1.0))
    if dataset == "GSE10325" and "myeloid" in comparison:
        return 0.85
    if dataset == "GSE97779":
        # Macrophage-specific but biologically confounded against cultured controls.
        return 0.65
    if dataset == "GSE13355" and "paired" in comparison:
        return 0.65
    if dataset == "GSE75214" and ("inactive" in comparison):
        return 0.60
    if dataset == "GSE32591":
        return 0.45
    if dataset == "GSE23117" and "advanced" in comparison:
        return 0.25
    if "bulk" in limitation:
        return 0.40
    return 0.50


def load_existing_evidence() -> pd.DataFrame:
    rows: list[dict[str, object]] = []

    # Non-MS target screens.
    for path in [
        ROOT / "phases/v2/results" / "cross_autoimmune_target_gene_contrasts.tsv",
        ROOT / "phases/v2/results" / "extended_autoimmune_target_gene_contrasts.tsv",
    ]:
        if not path.exists():
            continue
        df = pd.read_csv(path, sep="\t")
        for _, r in df.iterrows():
            disease = disease_from_comparison(str(r["comparison"]), str(r["dataset"]))
            q = quality_weight(r)
            rows.append(
                {
                    "gene": r["feature"],
                    "disease": disease,
                    "dataset": r["dataset"],
                    "channel": "expression_screen",
                    "comparison": r["comparison"],
                    "effect": r["hedges_g"] if pd.notna(r.get("hedges_g")) else r.get("delta"),
                    "p": r["p"],
                    "quality": q,
                    "score": signed_score(r.get("hedges_g"), r["p"], q),
                    "limitation": r.get("limitation", ""),
                }
            )

    # MS foamy proteomics and snRNA convergence.
    conv_path = ROOT / "results" / "mims2_proteome_convergent_targets.tsv"
    if conv_path.exists():
        conv = pd.read_csv(conv_path, sep="\t")
        for _, r in conv.iterrows():
            gene = r["gene"]
            if pd.notna(r.get("gee_coef_foamy")):
                rows.append(
                    {
                        "gene": gene,
                        "disease": "MS",
                        "dataset": "GSE279972",
                        "channel": "foamy_lesion_proteomics",
                        "comparison": "foamy_vs_nonfoamy_lesion",
                        "effect": r["gee_coef_foamy"],
                        "p": r["gee_p"],
                        "quality": 0.90 if bool(r.get("adequate_reporting_coverage")) else 0.35,
                        "score": signed_score(
                            r["gee_coef_foamy"],
                            r["gee_p"],
                            0.90 if bool(r.get("adequate_reporting_coverage")) else 0.35,
                        ),
                        "limitation": "bulk lesion proteomics, donor-aware but not cell-specific",
                    }
                )
            rows.append(
                {
                    "gene": gene,
                    "disease": "MS",
                    "dataset": "GSE301908",
                    "channel": "snRNA_MIMS2_like_microglia",
                    "comparison": "MIMS2_like_vs_HMG_like",
                    "effect": r["dz"],
                    "p": r["wilcoxon_p"],
                    "quality": 0.80,
                    "score": signed_score(r["dz"], r["wilcoxon_p"], 0.80),
                    "limitation": "reconstructed state from snRNA markers; donor-paired but marker-defined",
                }
            )

    # MS spatial MERFISH, low-powered but compartmental.
    spatial_path = ROOT / "results" / "spatial_convergent_candidate_statistics.tsv"
    if spatial_path.exists():
        sp = pd.read_csv(spatial_path, sep="\t")
        for _, r in sp.iterrows():
            rows.append(
                {
                    "gene": r["gene"],
                    "disease": "MS",
                    "dataset": "GSE284005",
                    "channel": "spatial_MERFISH",
                    "comparison": r["analysis"],
                    "effect": r["paired_dz"],
                    "p": r["wilcoxon_p"],
                    "quality": 0.55,
                    "score": signed_score(r["paired_dz"], r["wilcoxon_p"], 0.55),
                    "limitation": "spatial but n=6 donors and limited gene panel",
                }
            )

    evidence = pd.DataFrame(rows)
    if evidence.empty:
        return evidence
    evidence["axis"] = evidence["gene"].map(axis_for_gene)
    evidence["positive_nominal"] = (evidence["effect"] > 0) & (evidence["p"] < 0.05)
    evidence["negative_nominal"] = (evidence["effect"] < 0) & (evidence["p"] < 0.05)
    return evidence


def axis_for_gene(gene: str) -> str:
    hits = [axis for axis, genes in AXES.items() if gene in genes]
    return ",".join(hits) if hits else "unassigned"


def summarize_genes(evidence: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for gene, sub in evidence.groupby("gene"):
        disease_scores = sub.groupby("disease")["score"].sum()
        disease_pos = sub.groupby("disease")["positive_nominal"].any()
        disease_neg = sub.groupby("disease")["negative_nominal"].any()
        ms_sub = sub[sub["disease"] == "MS"]
        non_ms_sub = sub[sub["disease"] != "MS"]
        pos_diseases = sorted(disease_pos.index[disease_pos].tolist())
        neg_diseases = sorted(disease_neg.index[disease_neg].tolist())
        positive_non_ms = sorted(non_ms_sub.groupby("disease")["positive_nominal"].any().pipe(lambda x: x.index[x].tolist()))
        negative_non_ms = sorted(non_ms_sub.groupby("disease")["negative_nominal"].any().pipe(lambda x: x.index[x].tolist()))
        n_channels_ms = ms_sub["channel"].nunique()
        n_datasets_ms = ms_sub["dataset"].nunique()
        breadth_score = len(positive_non_ms) - 0.75 * len(negative_non_ms)
        ms_anchor = max(0.0, ms_sub["score"].sum()) + 0.5 * n_channels_ms + 0.25 * n_datasets_ms
        weighted_total = disease_scores.sum()
        contradiction_penalty = max(0, len(negative_non_ms) - 1) * 1.25
        prior_penalty = 1.5 if gene in PRIOR_FLAGS else 0.0
        priority = weighted_total + 1.75 * breadth_score + ms_anchor - contradiction_penalty - prior_penalty
        rows.append(
            {
                "gene": gene,
                "axis": axis_for_gene(gene),
                "priority_score": priority,
                "weighted_evidence_score": weighted_total,
                "ms_anchor_score": ms_anchor,
                "positive_disease_count": len(pos_diseases),
                "negative_disease_count": len(neg_diseases),
                "positive_non_ms_disease_count": len(positive_non_ms),
                "negative_non_ms_disease_count": len(negative_non_ms),
                "ms_channels": n_channels_ms,
                "ms_datasets": n_datasets_ms,
                "positive_diseases": ",".join(pos_diseases),
                "negative_diseases": ",".join(neg_diseases),
                "prior_flag": PRIOR_FLAGS.get(gene, ""),
            }
        )
    return pd.DataFrame(rows).sort_values("priority_score", ascending=False)


def summarize_axes(evidence: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for axis, genes in AXES.items():
        sub = evidence[evidence["gene"].isin(genes)].copy()
        if sub.empty:
            continue
        disease_axis = sub.groupby("disease").agg(
            score=("score", "sum"),
            any_positive=("positive_nominal", "any"),
            any_negative=("negative_nominal", "any"),
            n_genes=("gene", "nunique"),
            n_channels=("channel", "nunique"),
        )
        rows.append(
            {
                "axis": axis,
                "genes_in_axis": ",".join(genes),
                "weighted_score": float(disease_axis["score"].sum()),
                "positive_disease_count": int(disease_axis["any_positive"].sum()),
                "negative_disease_count": int(disease_axis["any_negative"].sum()),
                "positive_diseases": ",".join(sorted(disease_axis.index[disease_axis["any_positive"]].tolist())),
                "negative_diseases": ",".join(sorted(disease_axis.index[disease_axis["any_negative"]].tolist())),
                "mean_genes_per_disease": float(disease_axis["n_genes"].mean()),
                "mean_channels_per_disease": float(disease_axis["n_channels"].mean()),
            }
        )
    return pd.DataFrame(rows).sort_values("weighted_score", ascending=False)


def main() -> None:
    OUT.mkdir(exist_ok=True)
    evidence = load_existing_evidence()
    evidence.to_csv(OUT / "existing_evidence_candidate_matrix.tsv", sep="\t", index=False)
    genes = summarize_genes(evidence)
    axes = summarize_axes(evidence)
    genes.to_csv(OUT / "central_node_first_pass_rank.tsv", sep="\t", index=False)
    axes.to_csv(OUT / "axis_level_convergence.tsv", sep="\t", index=False)
    summary = {
        "seed": SEED,
        "n_evidence_rows": int(len(evidence)),
        "n_genes": int(evidence["gene"].nunique()) if not evidence.empty else 0,
        "top_genes": genes.head(10)["gene"].tolist(),
        "top_axes": axes.head(6)["axis"].tolist(),
        "interpretation": (
            "Heuristic breadth ranking for triage. Promotion requires cell-state, genetics, "
            "foundation-model/perturbation, druggability, and prior-art validation."
        ),
    }
    (OUT / "central_node_first_pass_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    print("\nTop genes:")
    print(genes.head(20).to_string(index=False))
    print("\nAxes:")
    print(axes.to_string(index=False))


if __name__ == "__main__":
    main()
