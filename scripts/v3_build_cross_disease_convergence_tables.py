#!/usr/bin/env python3
"""Build explicit cross-disease convergence tables for the V3 synthesis.

This script aggregates only locally produced, traceable outputs. It keeps
sample-level statistics from each dataset rather than reusing narrative labels.
The tables are designed for milestone decisions, not for causal estimation.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results_v3"

MODULE_MAP_GSE111972 = {
    "interferon_apc": "ifn_apc",
    "lysosome_antigen_processing": "lysosomal_apc",
}

TRANSITION_MODULES = {
    "IFNG_HLAII_CD74_GILT_TAP_transition": [
        "ifn_apc",
        "hla_ii_apc",
        "mif_cd74_receptor_state",
        "mixscale_validated_ifng_readout",
        "lysosomal_apc",
    ],
}


def load_tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t") if path.exists() else pd.DataFrame()


def support_level(delta: float, effect: float, p: float, fdr: float) -> str:
    if not np.isfinite(delta):
        return "missing"
    if delta < 0 and np.isfinite(p) and p <= 0.10:
        return "negative_trend"
    if delta <= 0:
        return "null_or_negative"
    if np.isfinite(fdr) and fdr <= 0.05 and np.isfinite(effect) and effect >= 1.0:
        return "strong"
    if np.isfinite(fdr) and fdr <= 0.10:
        return "supportive"
    if np.isfinite(p) and p <= 0.10:
        return "trend"
    return "positive_null"


def support_score(level: str) -> float:
    return {
        "strong": 3.0,
        "supportive": 2.0,
        "trend": 1.0,
        "positive_null": 0.25,
        "null_or_negative": 0.0,
        "negative_trend": -1.0,
    }.get(level, 0.0)


def module_rows() -> pd.DataFrame:
    rows: list[dict[str, object]] = []

    gse = load_tsv(OUT / "gse111972_module_contrasts.tsv")
    if not gse.empty:
        for _, row in gse[gse["contrast"].eq("MS_WM_vs_CON_WM")].iterrows():
            module = MODULE_MAP_GSE111972.get(str(row["feature"]), str(row["feature"]))
            rows.append(
                {
                    "disease": "MS",
                    "dataset": "GSE111972",
                    "modality": "sorted_bulk_microglia",
                    "compartment": "white matter microglia",
                    "module": module,
                    "metric": "log2_module_score",
                    "n_case": int(row["n_case"]),
                    "n_control": int(row["n_control"]),
                    "delta": float(row["delta_log2"]),
                    "hedges_g": float(row["hedges_g"]),
                    "p": float(row["p"]),
                    "fdr": float(row["fdr"]),
                }
            )

    h5 = load_tsv(OUT / "direct_h5ad_cell_state" / "direct_h5ad_donor_module_comparisons.tsv")
    if not h5.empty:
        sub = h5[h5["metric"].eq("mean_score")]
        for _, row in sub.iterrows():
            rows.append(
                {
                    "disease": str(row["disease_name"]),
                    "dataset": str(row["analysis"]),
                    "modality": "single_cell_or_single_nucleus_h5ad",
                    "compartment": str(row["compartment"]),
                    "module": str(row["module"]),
                    "metric": "donor_mean_z_score",
                    "n_case": int(row["n_case_donors"]),
                    "n_control": int(row["n_control_donors"]),
                    "delta": float(row["delta_case_minus_control"]),
                    "hedges_g": float(row["hedges_g"]),
                    "p": float(row["p"]),
                    "fdr": float(row["fdr"]),
                }
            )

    thyroid = load_tsv(OUT / "gse248205_thyroid_spatial" / "gse248205_module_gene_contrasts.tsv")
    if not thyroid.empty:
        sub = thyroid[thyroid["feature_type"].eq("module")]
        for _, row in sub.iterrows():
            disease = str(row["contrast"]).replace("_vs_control", "")
            rows.append(
                {
                    "disease": disease,
                    "dataset": "GSE248205",
                    "modality": "spatial_visium",
                    "compartment": "thyroid tissue spots",
                    "module": str(row["feature"]),
                    "metric": "sample_mean_log1p_cpm_module",
                    "n_case": int(row["n_case_samples"]),
                    "n_control": int(row["n_control_samples"]),
                    "delta": float(row["delta_case_minus_control"]),
                    "hedges_g": float(row["hedges_g"]),
                    "p": float(row["p"]),
                    "fdr": float(row["fdr"]),
                }
            )

    celiac = load_tsv(OUT / "gse315138_celiac_marker" / "gse315138_donor_module_comparisons.tsv")
    if not celiac.empty:
        sub = celiac[celiac["metric"].eq("mean_score")]
        for _, row in sub.iterrows():
            rows.append(
                {
                    "disease": str(row["disease_name"]),
                    "dataset": "GSE315138",
                    "modality": "single_cell_marker_compartment",
                    "compartment": f"{row['compartment']} marker-classified duodenum",
                    "module": str(row["module"]),
                    "metric": "donor_mean_z_score_marker_compartment",
                    "n_case": int(row["n_case_donors"]),
                    "n_control": int(row["n_control_donors"]),
                    "delta": float(row["delta_case_minus_control"]),
                    "hedges_g": float(row["hedges_g"]),
                    "p": float(row["p"]),
                    "fdr": float(row["fdr"]),
                }
            )

    out = pd.DataFrame(rows)
    if out.empty:
        return out
    out["support_level"] = [
        support_level(d, g, p, f) for d, g, p, f in zip(out["delta"], out["hedges_g"], out["p"], out["fdr"])
    ]
    out["support_score"] = out["support_level"].map(support_score)
    return out.sort_values(["disease", "module", "support_score"], ascending=[True, True, False])


def summarize_modules(modules: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    if modules.empty:
        return pd.DataFrame(rows)
    for module, sub in modules.groupby("module"):
        by_disease = (
            sub.sort_values("support_score", ascending=False)
            .groupby("disease", as_index=False)
            .first()
        )
        pos = by_disease[by_disease["support_level"].isin(["strong", "supportive", "trend"])]
        rows.append(
            {
                "module": module,
                "n_diseases_tested": int(by_disease["disease"].nunique()),
                "n_strong_diseases": int((by_disease["support_level"] == "strong").sum()),
                "n_supportive_or_strong_diseases": int(by_disease["support_level"].isin(["strong", "supportive"]).sum()),
                "n_trend_or_better_diseases": int(by_disease["support_level"].isin(["strong", "supportive", "trend"]).sum()),
                "n_negative_trend_diseases": int((by_disease["support_level"] == "negative_trend").sum()),
                "mean_positive_delta": float(pos["delta"].mean()) if not pos.empty else np.nan,
                "median_positive_hedges_g": float(pos["hedges_g"].median()) if not pos.empty else np.nan,
                "supporting_diseases": ";".join(pos["disease"].tolist()),
            }
        )
    return pd.DataFrame(rows).sort_values(
        ["n_supportive_or_strong_diseases", "n_trend_or_better_diseases", "n_negative_trend_diseases"],
        ascending=[False, False, True],
    )


def summarize_transitions(modules: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    if modules.empty:
        return pd.DataFrame(rows)
    for transition, transition_modules in TRANSITION_MODULES.items():
        sub = modules[modules["module"].isin(transition_modules)].copy()
        by_disease = sub.sort_values("support_score", ascending=False).groupby("disease", as_index=False).first()
        pos = by_disease[by_disease["support_level"].isin(["strong", "supportive", "trend"])]
        rows.append(
            {
                "transition": transition,
                "modules_considered": ",".join(transition_modules),
                "n_diseases_tested": int(by_disease["disease"].nunique()),
                "n_strong_diseases": int((by_disease["support_level"] == "strong").sum()),
                "n_supportive_or_strong_diseases": int(by_disease["support_level"].isin(["strong", "supportive"]).sum()),
                "n_trend_or_better_diseases": int(by_disease["support_level"].isin(["strong", "supportive", "trend"]).sum()),
                "n_negative_trend_diseases": int((by_disease["support_level"] == "negative_trend").sum()),
                "supporting_diseases": ";".join(pos["disease"].tolist()),
                "top_per_disease": json.dumps(
                    by_disease[
                        ["disease", "dataset", "compartment", "module", "delta", "hedges_g", "p", "fdr", "support_level"]
                    ].to_dict(orient="records")
                ),
            }
        )
    return pd.DataFrame(rows)


def gene_rows() -> pd.DataFrame:
    rows: list[dict[str, object]] = []

    ms = load_tsv(OUT / "gse111972_target_contrasts.tsv")
    if not ms.empty:
        for _, row in ms[ms["contrast"].eq("MS_WM_vs_CON_WM")].iterrows():
            rows.append(
                {
                    "disease": "MS",
                    "dataset": "GSE111972",
                    "modality": "sorted_bulk_microglia",
                    "compartment": "white matter microglia",
                    "gene": str(row["feature"]),
                    "metric": "log2_expression",
                    "n_case": int(row["n_case"]),
                    "n_control": int(row["n_control"]),
                    "delta": float(row["delta_log2"]),
                    "hedges_g": float(row["hedges_g"]),
                    "p": float(row["p"]),
                    "fdr": float(row["fdr"]),
                }
            )

    direct = load_tsv(OUT / "direct_h5ad_gene_replication" / "direct_h5ad_gene_donor_comparisons.tsv")
    if not direct.empty:
        sub = direct[direct["metric"].eq("mean_z_vs_controls")]
        for _, row in sub.iterrows():
            rows.append(
                {
                    "disease": str(row["disease_name"]),
                    "dataset": str(row["analysis"]),
                    "modality": "single_cell_or_single_nucleus_h5ad",
                    "compartment": str(row["compartment"]),
                    "gene": str(row["gene"]),
                    "metric": "donor_mean_z_score",
                    "n_case": int(row["n_case_donors"]),
                    "n_control": int(row["n_control_donors"]),
                    "delta": float(row["delta_case_minus_control"]),
                    "hedges_g": float(row["hedges_g"]),
                    "p": float(row["p"]),
                    "fdr": float(row["fdr"]),
                }
            )

    thyroid = load_tsv(OUT / "gse248205_thyroid_spatial" / "gse248205_module_gene_contrasts.tsv")
    if not thyroid.empty:
        sub = thyroid[thyroid["feature_type"].eq("gene")]
        for _, row in sub.iterrows():
            disease = str(row["contrast"]).replace("_vs_control", "")
            rows.append(
                {
                    "disease": disease,
                    "dataset": "GSE248205",
                    "modality": "spatial_visium",
                    "compartment": "thyroid tissue spots",
                    "gene": str(row["feature"]),
                    "metric": "sample_mean_log1p_cpm_gene",
                    "n_case": int(row["n_case_samples"]),
                    "n_control": int(row["n_control_samples"]),
                    "delta": float(row["delta_case_minus_control"]),
                    "hedges_g": float(row["hedges_g"]),
                    "p": float(row["p"]),
                    "fdr": float(row["fdr"]),
                }
            )

    out = pd.DataFrame(rows)
    if out.empty:
        return out
    out["support_level"] = [
        support_level(d, g, p, f) for d, g, p, f in zip(out["delta"], out["hedges_g"], out["p"], out["fdr"])
    ]
    out["support_score"] = out["support_level"].map(support_score)
    return out.sort_values(["gene", "disease", "support_score"], ascending=[True, True, False])


def summarize_genes(genes: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    if genes.empty:
        return pd.DataFrame(rows)
    for gene, sub in genes.groupby("gene"):
        by_disease = sub.sort_values("support_score", ascending=False).groupby("disease", as_index=False).first()
        pos = by_disease[by_disease["support_level"].isin(["strong", "supportive", "trend"])]
        rows.append(
            {
                "gene": gene,
                "n_diseases_tested": int(by_disease["disease"].nunique()),
                "n_strong_diseases": int((by_disease["support_level"] == "strong").sum()),
                "n_supportive_or_strong_diseases": int(by_disease["support_level"].isin(["strong", "supportive"]).sum()),
                "n_trend_or_better_diseases": int(by_disease["support_level"].isin(["strong", "supportive", "trend"]).sum()),
                "n_negative_trend_diseases": int((by_disease["support_level"] == "negative_trend").sum()),
                "median_positive_hedges_g": float(pos["hedges_g"].median()) if not pos.empty else np.nan,
                "supporting_diseases": ";".join(pos["disease"].tolist()),
            }
        )
    return pd.DataFrame(rows).sort_values(
        ["n_supportive_or_strong_diseases", "n_trend_or_better_diseases", "n_negative_trend_diseases", "median_positive_hedges_g"],
        ascending=[False, False, True, False],
    )


def main() -> None:
    OUT.mkdir(exist_ok=True)
    modules = module_rows()
    genes = gene_rows()
    module_summary = summarize_modules(modules)
    transition_summary = summarize_transitions(modules)
    gene_summary = summarize_genes(genes)

    modules.to_csv(OUT / "cross_disease_cell_state_convergence.tsv", sep="\t", index=False)
    module_summary.to_csv(OUT / "cross_disease_module_summary.tsv", sep="\t", index=False)
    transition_summary.to_csv(OUT / "cross_disease_transition_summary.tsv", sep="\t", index=False)
    genes.to_csv(OUT / "cross_disease_gene_convergence.tsv", sep="\t", index=False)
    gene_summary.to_csv(OUT / "cross_disease_gene_summary.tsv", sep="\t", index=False)

    summary = {
        "module_rows": int(len(modules)),
        "gene_rows": int(len(genes)),
        "top_modules": module_summary.head(10).to_dict(orient="records") if not module_summary.empty else [],
        "transition_summary": transition_summary.to_dict(orient="records") if not transition_summary.empty else [],
        "top_genes": gene_summary.head(20).to_dict(orient="records") if not gene_summary.empty else [],
        "support_level_rule": (
            "strong: delta>0, FDR<=0.05, Hedges g>=1; supportive: delta>0 and FDR<=0.10; "
            "trend: delta>0 and p<=0.10; negative_trend: delta<0 and p<=0.10."
        ),
    }
    (OUT / "cross_disease_convergence_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
