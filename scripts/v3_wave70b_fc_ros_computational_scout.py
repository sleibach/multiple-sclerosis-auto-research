#!/usr/bin/env python3
"""Wave70-B Fc/ROS-resolution candidate scout.

Local-only computational scout over the Fc inhibitory receptor / phosphatase /
TAM-resolution neighborhood requested in Wave70-B. This script intentionally
does not promote a therapeutic finding. It aggregates exact candidate-level
effect sizes from local V3 artifacts and the local GSE282122 myeloid object.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import anndata as ad
import numpy as np
import pandas as pd
from scipy import sparse, stats
from statsmodels.formula.api import ols
from statsmodels.stats.multitest import multipletests


SEED = 20260527
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "phases/v3/results" / "wave70b_fc_ros_computational_scout"

CANDIDATES = [
    "INPP5D",
    "PTPN6",
    "LILRB1",
    "LILRB2",
    "LILRB4",
    "LAIR1",
    "SIGLEC10",
    "CD300A",
    "BTK",
    "PIK3CD",
    "PIK3CG",
    "MERTK",
    "AXL",
    "TYRO3",
    "GAS6",
    "PROS1",
    "CD300LF",
    "PTPN11",
    "SH2D1B",
]
CANDIDATE_SET = set(CANDIDATES)

RAW_GSE282122 = ROOT / "data" / "raw_v3" / "wave67_gse282122_myeloid"
GSE282122_H5AD = RAW_GSE282122 / "myeloid_final.h5ad"
GSE282122_PAIRS = RAW_GSE282122 / "paired_sample_list.csv"
WAVE68_INTEGRATED = ROOT / "phases/v3/results" / "wave68_gse282122_unrestricted_gene_screen" / "integrated_gene_target_rank.tsv"
WAVE69B = ROOT / "phases/v3/results" / "wave69b_independent_validation_scout"
MS_SIGNATURE = ROOT / "phases/v3/results" / "gse111972_full_ms_wm_signature.tsv"
BROAD_SUMMARY = ROOT / "phases/v3/results" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_summary.tsv"
BROAD_CONTRASTS = ROOT / "phases/v3/results" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_contrasts.tsv"
WAVE37_EFFERO = ROOT / "phases/v3/results" / "wave37_gse212008_crispr_efferocytosis_screen" / "gene_level_screen_scores.tsv"
WAVE57_CALLS = (
    ROOT / "phases/v3/results" / "wave57_intervention_first_geneformer_screen" / "wave57_intervention_first_candidate_calls.tsv"
)
WAVE69D_CALLS = (
    ROOT
    / "phases/v3/results"
    / "wave69d_gse282122_geneformer_remission_centroid"
    / "geneformer_remission_candidate_calls.tsv"
)
GENEFORMER_SOURCE_SUMMARY = ROOT / "phases/v3/results" / "wave18_foundation_rescue" / "geneformer_source_gene_summary.tsv"
GENEFORMER_PIVOT_SUMMARY = (
    ROOT / "phases/v3/results" / "geneformer_pivot_panel_delete" / "geneformer_pivot_panel_gene_summary.tsv"
)
RA_COUNTS = ROOT / "phases/v3/results" / "wave65_gse198520_ra_synovium_antitnf_audit" / "gse198520_counts_used.tsv"
RA_META = ROOT / "phases/v3/results" / "wave65_gse198520_ra_synovium_antitnf_audit" / "gse198520_sample_metadata.tsv"

PRIMARY_STATES = ["Mono_macro", "DC"]
MIN_CELLS_PER_SIDE = 20

MANUAL_DIRECTION_BLOCKERS = {
    "BTK": "BTK inhibitors are direct MS/autoimmune prior-art comparators and broad B-cell/myeloid immunosuppression, not a new Fc-resolution node.",
    "PIK3CD": "PI3K-delta inhibitors are immunosuppressive and infection/colitis-risk comparators; autoimmune direction is not a selective resolution claim.",
    "PIK3CG": "PI3K-gamma inhibitors are broad myeloid inflammatory pharmacology with oncology/inflammation prior art and host-defense risk.",
    "PTPN11": "SHP2 modulation is pleiotropic growth-factor/oncology biology; inhibition is unlikely to be a clean autoimmune-resolution intervention.",
    "MERTK": "TAM biology likely requires agonism/restoration, while available small-molecule pharmacology is mostly kinase inhibition.",
    "AXL": "TAM biology likely requires agonism/restoration, while available small-molecule pharmacology is mostly kinase inhibition.",
    "TYRO3": "TAM biology likely requires agonism/restoration, while available small-molecule pharmacology is mostly kinase inhibition.",
    "GAS6": "Ligand restoration is modality-immature and pro-thrombotic/TAM-pleiotropy concerns remain unresolved.",
    "PROS1": "Protein S biology is anticoagulation/TAM-pleiotropic; autoimmune delivery and directionality are unresolved.",
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def save_tsv(df: pd.DataFrame, name: str) -> None:
    df.to_csv(OUT / name, sep="\t", index=False)


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True) + "\n", encoding="utf-8")


def bh(values: pd.Series | np.ndarray) -> np.ndarray:
    vals = pd.Series(values).fillna(1.0).to_numpy(float)
    return multipletests(vals, method="fdr_bh")[1]


def hedges_g(a: np.ndarray, b: np.ndarray) -> float:
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    a = a[np.isfinite(a)]
    b = b[np.isfinite(b)]
    if len(a) < 2 or len(b) < 2:
        return np.nan
    pooled = ((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) / (len(a) + len(b) - 2)
    if pooled <= 0 or not np.isfinite(pooled):
        return np.nan
    correction = 1.0 - (3.0 / (4.0 * (len(a) + len(b)) - 9.0))
    return float(((a.mean() - b.mean()) / math.sqrt(pooled)) * correction)


def gene_symbols(adata: ad.AnnData) -> list[str]:
    for col in ["gene_symbols", "gene_symbol", "feature_name", "GeneSym", "symbol", "gene_name"]:
        if col in adata.var.columns:
            vals = adata.var[col].astype(str).str.upper().tolist()
            if len(set(vals) & CANDIDATE_SET) >= 5:
                return vals
    return [str(x).upper() for x in adata.var_names]


def gse282122_direct_candidate_pairs() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Compute candidate-only GSE282122 pseudobulk from the local h5ad object."""
    adata = ad.read_h5ad(GSE282122_H5AD)
    paired = pd.read_csv(GSE282122_PAIRS, sep=None, engine="python")
    paired_samples = set(paired["sample_id"].astype(str))
    obs = adata.obs.copy().reset_index(names="obs_index")
    for col in ["sample_id", "Patient", "Disease", "Site", "Treatment", "Remission_status", "major", "Batch"]:
        if col in obs.columns:
            obs[col] = obs[col].astype(str).str.strip()
    obs["Inflammation_score_numeric"] = pd.to_numeric(obs.get("Inflammation_score", np.nan), errors="coerce")
    filt = obs[
        obs["sample_id"].astype(str).isin(paired_samples)
        & obs["Disease"].isin(["CD", "UC"])
        & obs["Treatment"].isin(["Pre", "Post"])
        & obs["Remission_status"].isin(["Remission", "Non_Remission"])
        & obs["major"].isin(PRIMARY_STATES)
    ].copy()
    filt["cell_state"] = filt["major"]
    filt["row_position"] = filt.index.to_numpy()

    X = adata.X.tocsr() if sparse.issparse(adata.X) else sparse.csr_matrix(adata.X)
    totals = np.asarray(X.sum(axis=1)).ravel()
    filt["cell_total_counts"] = totals[filt["row_position"].to_numpy(int)]
    symbols = pd.Series(gene_symbols(adata))
    gene_to_cols: dict[str, list[int]] = {}
    for gene in CANDIDATES:
        idx = np.flatnonzero(symbols.eq(gene).to_numpy())
        if len(idx):
            gene_to_cols[gene] = [int(x) for x in idx]

    group_cols = ["Patient", "Disease", "Site", "Treatment", "Remission_status", "sample_id", "Batch", "cell_state"]
    meta_rows: list[dict[str, object]] = []
    expr_rows: list[dict[str, float]] = []
    detect_rows: list[dict[str, float]] = []
    for key, sub in filt.groupby(group_cols, observed=True, dropna=False):
        idx = sub["row_position"].to_numpy(int)
        total_counts = float(sub["cell_total_counts"].sum())
        meta = dict(zip(group_cols, key, strict=True))
        meta.update(
            {
                "n_cells": int(len(idx)),
                "total_counts_all_genes": total_counts,
                "mean_inflammation_score": float(sub["Inflammation_score_numeric"].mean()),
            }
        )
        expr: dict[str, float] = {}
        detect: dict[str, float] = {}
        for gene in CANDIDATES:
            cols = gene_to_cols.get(gene, [])
            if not cols:
                expr[gene] = np.nan
                detect[gene] = np.nan
                continue
            block = X[idx, :][:, cols]
            per_cell = np.asarray(block.sum(axis=1)).ravel()
            summed = float(per_cell.sum())
            expr[gene] = float(np.log2((summed / total_counts) * 1_000_000.0 + 1.0)) if total_counts else np.nan
            detect[gene] = float(np.mean(per_cell > 0)) if len(per_cell) else np.nan
        meta_rows.append(meta)
        expr_rows.append(expr)
        detect_rows.append(detect)

    meta_df = pd.DataFrame(meta_rows)
    expr_df = pd.DataFrame(expr_rows)
    detect_df = pd.DataFrame(detect_rows)
    expr_df.index = meta_df.index
    detect_df.index = meta_df.index

    pair_rows: list[dict[str, object]] = []
    delta_rows: list[dict[str, float]] = []
    detect_pair_rows: list[dict[str, float]] = []
    pair_cols = ["Patient", "Disease", "Site", "Remission_status", "cell_state"]
    for key, sub in meta_df.groupby(pair_cols, observed=True, dropna=False):
        pre = sub[sub["Treatment"].eq("Pre")]
        post = sub[sub["Treatment"].eq("Post")]
        if len(pre) != 1 or len(post) != 1:
            continue
        pidx = pre.index[0]
        qidx = post.index[0]
        p = pre.iloc[0]
        q = post.iloc[0]
        min_cells = int(min(p["n_cells"], q["n_cells"]))
        pair_rows.append(
            {
                **dict(zip(pair_cols, key, strict=True)),
                "pre_sample_id": p["sample_id"],
                "post_sample_id": q["sample_id"],
                "pre_n_cells": int(p["n_cells"]),
                "post_n_cells": int(q["n_cells"]),
                "min_n_cells": min_cells,
                "passes_cell_threshold": bool(min_cells >= MIN_CELLS_PER_SIDE),
                "baseline_inflammation_score": float(p["mean_inflammation_score"]),
                "post_inflammation_score": float(q["mean_inflammation_score"]),
            }
        )
        delta_rows.append((expr_df.loc[qidx] - expr_df.loc[pidx]).to_dict())
        detect_pair_rows.append(detect_df.loc[pidx].add_prefix("baseline_detection_").to_dict())
    pair_meta = pd.DataFrame(pair_rows)
    deltas = pd.DataFrame(delta_rows)
    baseline_detect = pd.DataFrame(detect_pair_rows)
    deltas.index = pair_meta.index
    baseline_detect.index = pair_meta.index

    paired_rows: list[dict[str, object]] = []
    response_rows: list[dict[str, object]] = []
    for state, idx0 in pair_meta[pair_meta["passes_cell_threshold"]].groupby("cell_state", observed=True).groups.items():
        idx = list(idx0)
        state_meta = pair_meta.loc[idx]
        for gene in CANDIDATES:
            vals = deltas.loc[idx, gene].to_numpy(float)
            vals = vals[np.isfinite(vals)]
            if len(vals) >= 4:
                t_stat, p_value = stats.ttest_1samp(vals, 0.0, nan_policy="omit")
            else:
                t_stat, p_value = np.nan, np.nan
            paired_rows.append(
                {
                    "dataset": "GSE282122",
                    "system": "local h5ad candidate pseudobulk, paired anti-TNF IBD myeloid",
                    "cell_state": state,
                    "gene": gene,
                    "n_pairs": int(len(vals)),
                    "n_patients": int(state_meta["Patient"].nunique()),
                    "mean_post_minus_pre_log2cpm": float(np.nanmean(vals)) if len(vals) else np.nan,
                    "sd_post_minus_pre_log2cpm": float(np.nanstd(vals, ddof=1)) if len(vals) > 1 else np.nan,
                    "one_sample_t": float(t_stat) if np.isfinite(t_stat) else np.nan,
                    "one_sample_p": float(p_value) if np.isfinite(p_value) else np.nan,
                    "mean_baseline_detection_fraction": float(
                        np.nanmean(baseline_detect.loc[idx, f"baseline_detection_{gene}"].to_numpy(float))
                    ),
                }
            )
            rem = state_meta["Remission_status"].eq("Remission").to_numpy()
            non = state_meta["Remission_status"].eq("Non_Remission").to_numpy()
            a = deltas.loc[idx, gene].to_numpy(float)[rem]
            b = deltas.loc[idx, gene].to_numpy(float)[non]
            if np.isfinite(a).sum() >= 2 and np.isfinite(b).sum() >= 2:
                t2, p2 = stats.ttest_ind(a, b, equal_var=False, nan_policy="omit")
            else:
                t2, p2 = np.nan, np.nan
            adjusted_beta = np.nan
            adjusted_p = np.nan
            try:
                tmp = state_meta.copy()
                tmp["target_delta"] = deltas.loc[idx, gene].to_numpy(float)
                tmp["remission_binary"] = tmp["Remission_status"].eq("Remission").astype(int)
                model = ols("target_delta ~ remission_binary + baseline_inflammation_score + C(Disease)", data=tmp).fit()
                adjusted_beta = float(model.params.get("remission_binary", np.nan))
                adjusted_p = float(model.pvalues.get("remission_binary", np.nan))
            except Exception:
                pass
            response_rows.append(
                {
                    "dataset": "GSE282122",
                    "system": "local h5ad candidate pseudobulk, remission vs non-remission post-pre delta",
                    "cell_state": state,
                    "gene": gene,
                    "n_remission_pairs": int(np.isfinite(a).sum()),
                    "n_non_remission_pairs": int(np.isfinite(b).sum()),
                    "mean_delta_remission": float(np.nanmean(a)) if np.isfinite(a).any() else np.nan,
                    "mean_delta_non_remission": float(np.nanmean(b)) if np.isfinite(b).any() else np.nan,
                    "raw_delta_remission_minus_non": (
                        float(np.nanmean(a) - np.nanmean(b)) if np.isfinite(a).any() and np.isfinite(b).any() else np.nan
                    ),
                    "hedges_g_remission_vs_non": hedges_g(a, b),
                    "raw_t": float(t2) if np.isfinite(t2) else np.nan,
                    "raw_p": float(p2) if np.isfinite(p2) else np.nan,
                    "adjusted_beta_remission": adjusted_beta,
                    "adjusted_p": adjusted_p,
                }
            )
    paired = pd.DataFrame(paired_rows)
    response = pd.DataFrame(response_rows)
    if not paired.empty:
        paired["one_sample_fdr"] = bh(paired["one_sample_p"])
        paired["paired_call"] = np.select(
            [
                paired["one_sample_fdr"].le(0.10) & paired["mean_post_minus_pre_log2cpm"].gt(0),
                paired["one_sample_fdr"].le(0.10) & paired["mean_post_minus_pre_log2cpm"].lt(0),
                paired["one_sample_p"].lt(0.05) & paired["mean_post_minus_pre_log2cpm"].gt(0),
                paired["one_sample_p"].lt(0.05) & paired["mean_post_minus_pre_log2cpm"].lt(0),
            ],
            ["post_pre_up_fdr10", "post_pre_down_fdr10", "post_pre_up_nominal", "post_pre_down_nominal"],
            default="null_or_weak",
        )
    if not response.empty:
        response["raw_fdr"] = bh(response["raw_p"])
        response["adjusted_fdr"] = bh(response["adjusted_p"])
        response["response_call"] = np.select(
            [
                response["adjusted_fdr"].le(0.10) & response["adjusted_beta_remission"].gt(0),
                response["adjusted_fdr"].le(0.10) & response["adjusted_beta_remission"].lt(0),
                response["raw_fdr"].le(0.10) & response["raw_delta_remission_minus_non"].gt(0),
                response["raw_fdr"].le(0.10) & response["raw_delta_remission_minus_non"].lt(0),
                response["raw_p"].lt(0.05) & response["raw_delta_remission_minus_non"].gt(0),
                response["raw_p"].lt(0.05) & response["raw_delta_remission_minus_non"].lt(0),
            ],
            [
                "remission_adjusted_up_fdr10",
                "remission_adjusted_down_fdr10",
                "remission_raw_up_fdr10",
                "remission_raw_down_fdr10",
                "remission_raw_up_nominal",
                "remission_raw_down_nominal",
            ],
            default="null_or_weak",
        )
    return meta_df, pair_meta.join(deltas.add_prefix("delta_")), paired, response


def wave68_rows() -> pd.DataFrame:
    if not WAVE68_INTEGRATED.exists():
        return pd.DataFrame()
    df = pd.read_csv(WAVE68_INTEGRATED, sep="\t", low_memory=False)
    out = df[df["gene"].isin(CANDIDATES)].copy()
    keep = [
        "cell_state",
        "gene",
        "n_patient_units",
        "raw_delta_remission_minus_non",
        "raw_p",
        "raw_fdr",
        "mean_delta",
        "paired_p",
        "paired_fdr",
        "remission_adjusted_delta",
        "remission_adjusted_p",
        "remission_adjusted_fdr",
        "wave62_score",
        "wave62_call",
        "strong_l2g_disease_count",
        "strong_l2g_diseases",
        "strong_qtl_coloc_disease_count",
        "strong_qtl_coloc_diseases",
        "myeloid_qtl_coloc_disease_count",
        "ms_max_l2g_score",
        "ms_max_relevant_qtl_h4",
        "has_cross_autoimmune_genetics",
        "has_any_druggability_flag",
        "manual_or_prior_blocked",
        "perturbation_strength",
        "integrated_score",
        "wave68_call",
    ]
    keep = [c for c in keep if c in out.columns]
    out = out[keep].sort_values(["gene", "cell_state"])
    return out


def ms_gse111972_rows() -> pd.DataFrame:
    df = pd.read_csv(MS_SIGNATURE, sep="\t")
    out = df[df["gene"].isin(CANDIDATES)].copy()
    out["dataset"] = "GSE111972"
    out["system"] = "sorted human microglia, MS white matter vs control white matter"
    out["ms_call"] = np.select(
        [
            out["fdr"].le(0.10) & out["delta_log2"].gt(0),
            out["fdr"].le(0.10) & out["delta_log2"].lt(0),
            out["p"].lt(0.05) & out["delta_log2"].gt(0),
            out["p"].lt(0.05) & out["delta_log2"].lt(0),
        ],
        ["ms_up_fdr10", "ms_down_fdr10", "ms_up_nominal", "ms_down_nominal"],
        default="null_or_weak",
    )
    cols = ["dataset", "system", "gene", "delta_log2", "hedges_g", "p", "fdr", "ms_call"]
    return out[cols].sort_values(["ms_call", "p"])


def broad_rows() -> tuple[pd.DataFrame, pd.DataFrame]:
    summary = pd.read_csv(BROAD_SUMMARY, sep="\t", low_memory=False)
    summary = summary[summary["gene"].isin(CANDIDATES)].copy()
    keep = [
        "gene",
        "tested_compartment_count",
        "positive_compartment_count",
        "negative_compartment_count",
        "positive_fdr10_compartment_count",
        "negative_fdr10_compartment_count",
        "positive_disease_count",
        "negative_disease_count",
        "positive_diseases",
        "negative_diseases",
        "best_positive_p",
        "best_positive_fdr",
        "max_positive_delta_log2_cpm",
        "median_positive_hedges_g",
        "best_negative_p",
        "min_negative_delta_log2_cpm",
        "top_positive_compartments",
    ]
    summary = summary[[c for c in keep if c in summary.columns]]
    summary["broad_call"] = np.select(
        [
            summary["positive_fdr10_compartment_count"].ge(2) & summary["negative_fdr10_compartment_count"].eq(0),
            summary["positive_compartment_count"].ge(3) & summary["negative_compartment_count"].eq(0),
            summary["negative_fdr10_compartment_count"].ge(1),
            summary["positive_compartment_count"].ge(1),
        ],
        ["broad_positive_fdr10_recurrent", "broad_positive_nominal_recurrent", "contradictory_or_negative", "single_context_hint"],
        default="null_or_weak",
    )

    contrasts = pd.read_csv(BROAD_CONTRASTS, sep="\t", low_memory=False)
    contrasts = contrasts[contrasts["gene"].isin(CANDIDATES)].copy()
    contrasts["contrast_call"] = np.select(
        [
            contrasts["positive_fdr10"],
            contrasts["negative_fdr10"],
            contrasts["positive_nominal"],
            contrasts["negative_nominal"],
        ],
        ["positive_fdr10", "negative_fdr10", "positive_nominal", "negative_nominal"],
        default="null_or_weak",
    )
    contrasts = contrasts.sort_values(["gene", "p"])
    return summary.sort_values(["broad_call", "positive_fdr10_compartment_count", "positive_compartment_count"]), contrasts


def wave37_efferocytosis_rows() -> pd.DataFrame:
    df = pd.read_csv(WAVE37_EFFERO, sep="\t", low_memory=False)
    out = df[df["gene_symbol"].isin(CANDIDATES)].copy()
    missing = [gene for gene in CANDIDATES if gene not in set(out["gene_symbol"])]
    if missing:
        out = pd.concat(
            [
                out,
                pd.DataFrame(
                    {
                        "gene_symbol": missing,
                        "screen_call": "not_present_in_wave37_mouse_screen",
                    }
                ),
            ],
            ignore_index=True,
            sort=False,
        )
    out["efferocytosis_direction"] = np.select(
        [
            out["screen_call"].eq("KO_ENHANCES_EFFEROCYTOSIS_NEGATIVE_REGULATOR"),
            out["screen_call"].eq("KO_IMPAIRS_EFFEROCYTOSIS_POSITIVE_REGULATOR"),
            out["median_efficient_minus_noneater_lfc"].gt(0.25),
            out["median_efficient_minus_noneater_lfc"].lt(-0.25),
        ],
        [
            "ko_enhances_efferocytosis_gate",
            "ko_impairs_efferocytosis_gate",
            "ko_enhancement_trend",
            "ko_impairment_trend",
        ],
        default="null_or_weak",
    )
    keep = [
        "gene_symbol",
        "n_sgrna",
        "median_efficient_lfc",
        "median_noneater_lfc",
        "median_efficient_minus_noneater_lfc",
        "efficient_p_wilcoxon",
        "noneater_p_wilcoxon",
        "contrast_p_wilcoxon",
        "efficient_fdr",
        "noneater_fdr",
        "contrast_fdr",
        "screen_call",
        "efferocytosis_direction",
        "modules",
    ]
    return out[[c for c in keep if c in out.columns]].sort_values("gene_symbol")


def ra_synovium_rows() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    counts = pd.read_csv(RA_COUNTS, sep="\t")
    counts["GeneSymbol"] = counts["GeneSymbol"].astype(str).str.upper()
    gene_counts = counts.groupby("GeneSymbol").sum(numeric_only=True)
    present = [g for g in CANDIDATES if g in gene_counts.index]
    lib = gene_counts.sum(axis=0).replace(0, np.nan)
    log_cpm = np.log2(gene_counts.div(lib, axis=1) * 1_000_000.0 + 1.0)

    meta = pd.read_csv(RA_META, sep="\t")
    meta["timepoint"] = meta["timepoint"].astype(str).str.lower()
    meta = meta[meta["count_column"].isin(log_cpm.columns)].copy()

    delta_rows: list[dict[str, object]] = []
    for patient, sub in meta.groupby("patient", observed=True):
        pre = sub[sub["timepoint"].eq("pre")]
        post = sub[sub["timepoint"].eq("post")]
        if pre.empty or post.empty:
            continue
        pre_col = str(pre.iloc[0]["count_column"])
        post_col = str(post.iloc[0]["count_column"])
        row_meta = pre.iloc[0]
        for gene in present:
            delta_rows.append(
                {
                    "dataset": "GSE198520",
                    "system": "RA paired synovium bulk RNA-seq anti-TNF",
                    "patient": patient,
                    "gene": gene,
                    "response_class": row_meta["response_class"],
                    "responder_good_only": bool(row_meta["responder_good_only"]),
                    "responder_moderate_or_good": bool(row_meta["responder_moderate_or_good"]),
                    "pathotype": row_meta.get("pathotype", np.nan),
                    "pre_log2_cpm": float(log_cpm.loc[gene, pre_col]),
                    "post_log2_cpm": float(log_cpm.loc[gene, post_col]),
                    "post_minus_pre": float(log_cpm.loc[gene, post_col] - log_cpm.loc[gene, pre_col]),
                }
            )
    deltas = pd.DataFrame(delta_rows)

    paired_rows: list[dict[str, object]] = []
    response_rows: list[dict[str, object]] = []
    for gene in CANDIDATES:
        sub = deltas[deltas["gene"].eq(gene)] if not deltas.empty else pd.DataFrame()
        vals = sub["post_minus_pre"].to_numpy(float) if not sub.empty else np.array([])
        vals = vals[np.isfinite(vals)]
        if len(vals) >= 3:
            t_stat, p_value = stats.ttest_1samp(vals, 0.0, nan_policy="omit")
        else:
            t_stat, p_value = np.nan, np.nan
        paired_rows.append(
            {
                "dataset": "GSE198520",
                "system": "RA paired synovium bulk RNA-seq anti-TNF",
                "gene": gene,
                "n_patients": int(len(vals)),
                "mean_post_minus_pre": float(np.nanmean(vals)) if len(vals) else np.nan,
                "sd_post_minus_pre": float(np.nanstd(vals, ddof=1)) if len(vals) > 1 else np.nan,
                "t": float(t_stat) if np.isfinite(t_stat) else np.nan,
                "p": float(p_value) if np.isfinite(p_value) else np.nan,
            }
        )
        for contrast, column in [
            ("good_vs_moderate_none", "responder_good_only"),
            ("moderate_good_vs_none", "responder_moderate_or_good"),
        ]:
            if sub.empty:
                a = np.array([])
                b = np.array([])
            else:
                a = sub.loc[sub[column].astype(bool), "post_minus_pre"].to_numpy(float)
                b = sub.loc[~sub[column].astype(bool), "post_minus_pre"].to_numpy(float)
            if np.isfinite(a).sum() >= 2 and np.isfinite(b).sum() >= 2:
                t2, p2 = stats.ttest_ind(a, b, equal_var=False, nan_policy="omit")
            else:
                t2, p2 = np.nan, np.nan
            adjusted_beta = np.nan
            adjusted_p = np.nan
            try:
                tmp = sub.copy()
                tmp["response_binary"] = tmp[column].astype(bool).astype(int)
                model = ols("post_minus_pre ~ response_binary + C(pathotype)", data=tmp).fit()
                adjusted_beta = float(model.params.get("response_binary", np.nan))
                adjusted_p = float(model.pvalues.get("response_binary", np.nan))
            except Exception:
                pass
            response_rows.append(
                {
                    "dataset": "GSE198520",
                    "system": "RA paired synovium bulk RNA-seq anti-TNF",
                    "gene": gene,
                    "contrast": contrast,
                    "n_true": int(np.isfinite(a).sum()),
                    "n_false": int(np.isfinite(b).sum()),
                    "mean_true": float(np.nanmean(a)) if np.isfinite(a).any() else np.nan,
                    "mean_false": float(np.nanmean(b)) if np.isfinite(b).any() else np.nan,
                    "raw_delta_true_minus_false": (
                        float(np.nanmean(a) - np.nanmean(b)) if np.isfinite(a).any() and np.isfinite(b).any() else np.nan
                    ),
                    "hedges_g": hedges_g(a, b),
                    "raw_p": float(p2) if np.isfinite(p2) else np.nan,
                    "pathotype_adjusted_beta": adjusted_beta,
                    "pathotype_adjusted_p": adjusted_p,
                }
            )
    paired = pd.DataFrame(paired_rows)
    response = pd.DataFrame(response_rows)
    paired["fdr"] = bh(paired["p"])
    paired["ra_paired_call"] = np.select(
        [
            paired["fdr"].le(0.10) & paired["mean_post_minus_pre"].gt(0),
            paired["fdr"].le(0.10) & paired["mean_post_minus_pre"].lt(0),
            paired["p"].lt(0.05) & paired["mean_post_minus_pre"].gt(0),
            paired["p"].lt(0.05) & paired["mean_post_minus_pre"].lt(0),
        ],
        ["ra_antitnf_up_fdr10", "ra_antitnf_down_fdr10", "ra_antitnf_up_nominal", "ra_antitnf_down_nominal"],
        default="null_or_weak",
    )
    response["raw_fdr"] = bh(response["raw_p"])
    response["adjusted_fdr"] = bh(response["pathotype_adjusted_p"])
    response["ra_response_call"] = np.select(
        [
            response["adjusted_fdr"].le(0.10),
            response["raw_fdr"].le(0.10),
            response["raw_p"].lt(0.05),
        ],
        ["ra_response_pathotype_adjusted_fdr10", "ra_response_raw_fdr10", "ra_response_raw_nominal"],
        default="null_or_weak",
    )
    return deltas, paired.sort_values(["ra_paired_call", "p"]), response.sort_values(["ra_response_call", "raw_p"])


def wave69b_local_rows() -> dict[str, pd.DataFrame]:
    outputs = {}
    for name in [
        "ms_gse111972_candidate_rows.tsv",
        "broad_h5ad_candidate_summary.tsv",
        "ra_gse198520_candidate_paired_tests.tsv",
        "ra_gse198520_candidate_response_tests.tsv",
    ]:
        path = WAVE69B / name
        if not path.exists():
            continue
        df = pd.read_csv(path, sep="\t", low_memory=False)
        gene_col = "gene" if "gene" in df.columns else "gene_symbol" if "gene_symbol" in df.columns else None
        if gene_col:
            df = df[df[gene_col].isin(CANDIDATES)].copy()
        outputs[name] = df
    return outputs


def geneformer_rows() -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    sources = [
        ("wave57_intervention_first", WAVE57_CALLS),
        ("wave69d_gse282122_remission_centroid", WAVE69D_CALLS),
        ("wave18_foundation_rescue_source", GENEFORMER_SOURCE_SUMMARY),
        ("geneformer_pivot_panel", GENEFORMER_PIVOT_SUMMARY),
    ]
    for source, path in sources:
        if not path.exists():
            continue
        df = pd.read_csv(path, sep="\t", low_memory=False)
        gene_col = "gene" if "gene" in df.columns else "target_gene" if "target_gene" in df.columns else None
        if not gene_col:
            continue
        df[gene_col] = df[gene_col].astype(str).str.upper()
        out = df[df[gene_col].isin(CANDIDATES)].copy()
        if out.empty:
            continue
        out = out.rename(columns={gene_col: "gene"})
        out.insert(0, "geneformer_source", source)
        keep = [
            "geneformer_source",
            "gene",
            "contexts_tested",
            "contexts_with_token_ge_3_cells",
            "contexts_with_token",
            "disease_cells_with_token",
            "support_contexts",
            "strong_support_contexts",
            "positive_projection_contexts",
            "negative_projection_contexts",
            "best_context",
            "best_n_disease_cells_with_token",
            "best_n_nonremission_cells_with_token",
            "best_context_cells_with_token",
            "best_cosine_shift_z_vs_random",
            "best_context_cosine_z",
            "best_projection_minus_random",
            "best_context_projection_minus_random",
            "wave57_model_priority_score",
            "geneformer_remission_priority_score",
            "wave57_call",
            "wave69d_call",
        ]
        frames.append(out[[c for c in keep if c in out.columns]])
    if not frames:
        return pd.DataFrame(columns=["geneformer_source", "gene"])
    return pd.concat(frames, ignore_index=True, sort=False).sort_values(["gene", "geneformer_source"])


def integrate(
    gse282122_response: pd.DataFrame,
    wave68: pd.DataFrame,
    ms: pd.DataFrame,
    broad_summary: pd.DataFrame,
    effero: pd.DataFrame,
    ra_paired: pd.DataFrame,
    ra_response: pd.DataFrame,
    geneformer: pd.DataFrame,
) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for gene in CANDIDATES:
        w68 = wave68[wave68["gene"].eq(gene)] if not wave68.empty else pd.DataFrame()
        gse_resp = gse282122_response[gse282122_response["gene"].eq(gene)] if not gse282122_response.empty else pd.DataFrame()
        ms_row = ms[ms["gene"].eq(gene)] if not ms.empty else pd.DataFrame()
        broad = broad_summary[broad_summary["gene"].eq(gene)] if not broad_summary.empty else pd.DataFrame()
        eff = effero[effero["gene_symbol"].eq(gene)] if not effero.empty and "gene_symbol" in effero.columns else pd.DataFrame()
        ra_p = ra_paired[ra_paired["gene"].eq(gene)] if not ra_paired.empty else pd.DataFrame()
        ra_r = ra_response[ra_response["gene"].eq(gene)] if not ra_response.empty else pd.DataFrame()
        gf = geneformer[geneformer["gene"].eq(gene)] if not geneformer.empty else pd.DataFrame()

        best_gse = gse_resp.sort_values(["adjusted_fdr", "raw_p"], na_position="last").head(1)
        best_w68 = w68.sort_values(["remission_adjusted_fdr", "raw_p"], na_position="last").head(1)
        best_ra_p = ra_p.sort_values("fdr", na_position="last").head(1)
        best_ra_r = ra_r.sort_values(["adjusted_fdr", "raw_p"], na_position="last").head(1)

        broad_positive_fdr10 = int(broad["positive_fdr10_compartment_count"].iloc[0]) if not broad.empty else 0
        broad_positive = int(broad["positive_compartment_count"].iloc[0]) if not broad.empty else 0
        broad_negative_fdr10 = int(broad["negative_fdr10_compartment_count"].iloc[0]) if not broad.empty else 0
        positive_disease_count = int(broad["positive_disease_count"].iloc[0]) if not broad.empty else 0
        negative_disease_count = int(broad["negative_disease_count"].iloc[0]) if not broad.empty else 0

        ms_delta = float(ms_row["delta_log2"].iloc[0]) if not ms_row.empty else np.nan
        ms_p = float(ms_row["p"].iloc[0]) if not ms_row.empty else np.nan
        ms_fdr = float(ms_row["fdr"].iloc[0]) if not ms_row.empty else np.nan
        ms_call = str(ms_row["ms_call"].iloc[0]) if not ms_row.empty else "missing"

        eff_delta = (
            float(eff["median_efficient_minus_noneater_lfc"].iloc[0])
            if not eff.empty and "median_efficient_minus_noneater_lfc" in eff.columns
            else np.nan
        )
        eff_call = str(eff["efferocytosis_direction"].iloc[0]) if not eff.empty else "missing"
        eff_screen_call = str(eff["screen_call"].iloc[0]) if not eff.empty and "screen_call" in eff.columns else "missing"

        max_l2g = float(w68["ms_max_l2g_score"].max()) if not w68.empty and "ms_max_l2g_score" in w68.columns else np.nan
        qtl_count = (
            float(w68["strong_qtl_coloc_disease_count"].max())
            if not w68.empty and "strong_qtl_coloc_disease_count" in w68.columns
            else np.nan
        )
        has_cross_genetics = (
            bool(w68["has_cross_autoimmune_genetics"].fillna(False).astype(bool).any())
            if not w68.empty and "has_cross_autoimmune_genetics" in w68.columns
            else False
        )
        has_druggability = (
            bool(w68["has_any_druggability_flag"].fillna(False).astype(bool).any())
            if not w68.empty and "has_any_druggability_flag" in w68.columns
            else False
        )
        wave68_best_call = ";".join(sorted(set(w68["wave68_call"].dropna().astype(str)))) if not w68.empty else ""

        geneformer_sources = ";".join(sorted(set(gf["geneformer_source"].astype(str)))) if not gf.empty else ""
        geneformer_support = (
            int(pd.to_numeric(gf.get("support_contexts", pd.Series(dtype=float)), errors="coerce").fillna(0).max())
            if not gf.empty and "support_contexts" in gf.columns
            else 0
        )
        geneformer_strong = (
            int(pd.to_numeric(gf.get("strong_support_contexts", pd.Series(dtype=float)), errors="coerce").fillna(0).max())
            if not gf.empty and "strong_support_contexts" in gf.columns
            else 0
        )

        gse_adj_fdr = float(best_gse["adjusted_fdr"].iloc[0]) if not best_gse.empty else np.nan
        gse_adj_beta = float(best_gse["adjusted_beta_remission"].iloc[0]) if not best_gse.empty else np.nan
        gse_response_call = str(best_gse["response_call"].iloc[0]) if not best_gse.empty else "missing"
        gse_best_state = str(best_gse["cell_state"].iloc[0]) if not best_gse.empty else ""

        w68_adj_fdr = float(best_w68["remission_adjusted_fdr"].iloc[0]) if not best_w68.empty else np.nan
        w68_adj_delta = float(best_w68["remission_adjusted_delta"].iloc[0]) if not best_w68.empty else np.nan

        ra_paired_fdr = float(best_ra_p["fdr"].iloc[0]) if not best_ra_p.empty else np.nan
        ra_paired_delta = float(best_ra_p["mean_post_minus_pre"].iloc[0]) if not best_ra_p.empty else np.nan
        ra_paired_call = str(best_ra_p["ra_paired_call"].iloc[0]) if not best_ra_p.empty else "missing"
        ra_response_fdr = float(best_ra_r["adjusted_fdr"].iloc[0]) if not best_ra_r.empty else np.nan
        ra_response_beta = float(best_ra_r["pathotype_adjusted_beta"].iloc[0]) if not best_ra_r.empty else np.nan
        ra_response_call = str(best_ra_r["ra_response_call"].iloc[0]) if not best_ra_r.empty else "missing"

        support_score = 0
        support_score += int(gse_response_call != "null_or_weak" and gse_response_call != "missing")
        support_score += int(w68_adj_fdr <= 0.10) if np.isfinite(w68_adj_fdr) else 0
        support_score += int(ms_call.endswith("fdr10") or ms_call.endswith("nominal"))
        support_score += int(broad_positive_fdr10 >= 1 or broad_positive >= 3)
        support_score += int(ra_paired_call != "null_or_weak" and ra_paired_call != "missing")
        support_score += int(ra_response_call != "null_or_weak" and ra_response_call != "missing")
        support_score += int(eff_call in {"ko_enhancement_trend", "ko_impairment_trend", "ko_enhances_efferocytosis_gate", "ko_impairs_efferocytosis_gate"})
        support_score += int(geneformer_support >= 1)
        support_score += int(has_cross_genetics)

        blocker = MANUAL_DIRECTION_BLOCKERS.get(gene, "")
        if broad_negative_fdr10 > 0 or negative_disease_count > positive_disease_count + 1:
            blocker = (blocker + " " if blocker else "") + "Local broad h5ad recurrence is negative/contradictory."
        if gene in {"LILRB1", "LILRB2", "LILRB4", "LAIR1", "SIGLEC10", "CD300A", "CD300LF"} and not has_cross_genetics:
            blocker = (blocker + " " if blocker else "") + "No local Wave68/Wave62 cross-autoimmune genetic anchor in this scout."

        if blocker:
            integrated_call = "PARK_BLOCKED_OR_DIRECTIONALLY_UNRESOLVED"
        elif support_score >= 6 and has_cross_genetics and (gse_response_call != "null_or_weak" or ra_paired_call != "null_or_weak"):
            integrated_call = "REOPEN_CONTROLLER_SCOUT_NEEDS_REAL_PERTURBATION"
        elif support_score >= 4:
            integrated_call = "PARK_MULTI_MODAL_HINT"
        elif support_score >= 2:
            integrated_call = "DESCRIPTIVE_SIGNAL_ONLY"
        else:
            integrated_call = "NO_GO_LOCAL_SUPPORT_WEAK"

        rows.append(
            {
                "gene": gene,
                "integrated_call": integrated_call,
                "support_score_0_9": support_score,
                "manual_or_empirical_blocker": blocker,
                "gse282122_best_cell_state": gse_best_state,
                "gse282122_adjusted_beta_remission": gse_adj_beta,
                "gse282122_adjusted_fdr": gse_adj_fdr,
                "gse282122_response_call": gse_response_call,
                "wave68_adjusted_delta": w68_adj_delta,
                "wave68_adjusted_fdr": w68_adj_fdr,
                "wave68_best_call": wave68_best_call,
                "ms_gse111972_delta_log2": ms_delta,
                "ms_gse111972_p": ms_p,
                "ms_gse111972_fdr": ms_fdr,
                "ms_gse111972_call": ms_call,
                "broad_positive_compartments": broad_positive,
                "broad_positive_fdr10_compartments": broad_positive_fdr10,
                "broad_negative_compartments": int(broad["negative_compartment_count"].iloc[0]) if not broad.empty else 0,
                "broad_negative_fdr10_compartments": broad_negative_fdr10,
                "positive_disease_count": positive_disease_count,
                "positive_diseases": str(broad["positive_diseases"].iloc[0]) if not broad.empty else "",
                "negative_disease_count": negative_disease_count,
                "negative_diseases": str(broad["negative_diseases"].iloc[0]) if not broad.empty else "",
                "ra_antitnf_mean_post_minus_pre": ra_paired_delta,
                "ra_antitnf_fdr": ra_paired_fdr,
                "ra_antitnf_call": ra_paired_call,
                "ra_response_adjusted_beta": ra_response_beta,
                "ra_response_adjusted_fdr": ra_response_fdr,
                "ra_response_call": ra_response_call,
                "wave37_median_efficient_minus_noneater_lfc": eff_delta,
                "wave37_screen_call": eff_screen_call,
                "wave37_efferocytosis_direction": eff_call,
                "geneformer_sources": geneformer_sources,
                "geneformer_support_contexts_max": geneformer_support,
                "geneformer_strong_support_contexts_max": geneformer_strong,
                "ms_max_l2g_score": max_l2g,
                "strong_qtl_coloc_disease_count": qtl_count,
                "has_cross_autoimmune_genetics": has_cross_genetics,
                "has_any_druggability_flag_wave68": has_druggability,
            }
        )
    order = {
        "REOPEN_CONTROLLER_SCOUT_NEEDS_REAL_PERTURBATION": 0,
        "PARK_MULTI_MODAL_HINT": 1,
        "PARK_BLOCKED_OR_DIRECTIONALLY_UNRESOLVED": 2,
        "DESCRIPTIVE_SIGNAL_ONLY": 3,
        "NO_GO_LOCAL_SUPPORT_WEAK": 4,
    }
    out = pd.DataFrame(rows)
    out["call_priority"] = out["integrated_call"].map(order).fillna(9).astype(int)
    return out.sort_values(["call_priority", "support_score_0_9", "gene"], ascending=[True, False, True])


def markdown_table(df: pd.DataFrame, cols: list[str], n: int = 20) -> str:
    if df.empty:
        return "_No rows._"
    use = df[[c for c in cols if c in df.columns]].head(n).copy()
    if use.empty:
        return "_No columns._"
    display = use.replace({np.nan: ""})
    display = display.astype(str)
    header = "| " + " | ".join(display.columns) + " |"
    sep = "| " + " | ".join(["---"] * len(display.columns)) + " |"
    body = ["| " + " | ".join(row) + " |" for row in display.to_numpy()]
    return "\n".join([header, sep, *body])


def write_report(
    integrated: pd.DataFrame,
    gse_paired: pd.DataFrame,
    gse_response: pd.DataFrame,
    ms: pd.DataFrame,
    broad_summary: pd.DataFrame,
    effero: pd.DataFrame,
    ra_paired: pd.DataFrame,
    ra_response: pd.DataFrame,
    geneformer: pd.DataFrame,
) -> None:
    top_cols = [
        "gene",
        "integrated_call",
        "support_score_0_9",
        "manual_or_empirical_blocker",
        "gse282122_best_cell_state",
        "gse282122_adjusted_beta_remission",
        "gse282122_adjusted_fdr",
        "ms_gse111972_delta_log2",
        "ms_gse111972_p",
        "broad_positive_compartments",
        "broad_negative_compartments",
        "ra_antitnf_mean_post_minus_pre",
        "ra_antitnf_fdr",
        "wave37_median_efficient_minus_noneater_lfc",
        "geneformer_support_contexts_max",
        "has_cross_autoimmune_genetics",
    ]
    gse_cols = [
        "cell_state",
        "gene",
        "n_remission_pairs",
        "n_non_remission_pairs",
        "raw_delta_remission_minus_non",
        "hedges_g_remission_vs_non",
        "raw_p",
        "raw_fdr",
        "adjusted_beta_remission",
        "adjusted_p",
        "adjusted_fdr",
        "response_call",
    ]
    paired_cols = [
        "cell_state",
        "gene",
        "n_pairs",
        "mean_post_minus_pre_log2cpm",
        "sd_post_minus_pre_log2cpm",
        "one_sample_p",
        "one_sample_fdr",
        "mean_baseline_detection_fraction",
        "paired_call",
    ]
    lines = [
        "# Wave70-B Fc/ROS-Resolution Computational Scout",
        "",
        "## Verdict",
        "",
        "No Fc/ROS-resolution candidate is promoted as a finding. The strongest local signal is the LILRB inhibitory-receptor group, led by `LILRB2` in the integrated scout and by `LILRB1`/`LILRB4` in Mono_macro GSE282122 remission-response rows, but this does not replicate as a RA anti-TNF response signal and lacks a local Wave68/Wave62 cross-autoimmune genetic anchor. `INPP5D`, `PTPN6`, and `CD300A` show useful efferocytosis or post-treatment hints, not enough convergent disease evidence. TAM nodes (`MERTK`, `AXL`, `GAS6`, `PROS1`, `TYRO3`) remain directionally blocked because the plausible intervention is agonism/restoration while available pharmacology and local recurrence do not solve the delivery/safety problem.",
        "",
        "## Scope",
        "",
        f"- Candidate genes: `{', '.join(CANDIDATES)}`.",
        "- Data used: local GSE282122 myeloid h5ad, Wave68 integrated GSE282122 gene screen, MS GSE111972 microglia signature, broad h5ad recurrence, local RA GSE198520 synovium counts, Wave37 GSE212008 CRISPR efferocytosis screen, and existing Geneformer outputs.",
        "- This is a scout only. It ranks candidates for follow-up; it does not claim a therapeutic mechanism.",
        "",
        "## Integrated Calls",
        "",
        markdown_table(integrated, top_cols, n=len(integrated)),
        "",
        "## GSE282122 Direct h5ad Remission-Response Signal",
        "",
        markdown_table(gse_response.sort_values(["adjusted_fdr", "raw_p"], na_position="last"), gse_cols, n=20),
        "",
        "## GSE282122 Direct h5ad Paired Pharmacodynamic Signal",
        "",
        markdown_table(gse_paired.sort_values(["one_sample_fdr", "one_sample_p"], na_position="last"), paired_cols, n=20),
        "",
        "## MS GSE111972",
        "",
        markdown_table(ms.sort_values("p"), ["gene", "delta_log2", "hedges_g", "p", "fdr", "ms_call"], n=len(ms)),
        "",
        "## Broad h5ad Recurrence",
        "",
        markdown_table(
            broad_summary.sort_values(
                ["positive_fdr10_compartment_count", "positive_compartment_count", "best_positive_p"],
                ascending=[False, False, True],
            ),
            [
                "gene",
                "positive_compartment_count",
                "negative_compartment_count",
                "positive_fdr10_compartment_count",
                "negative_fdr10_compartment_count",
                "positive_disease_count",
                "positive_diseases",
                "negative_disease_count",
                "negative_diseases",
                "best_positive_p",
                "best_positive_fdr",
                "max_positive_delta_log2_cpm",
                "broad_call",
            ],
            n=len(broad_summary),
        ),
        "",
        "## RA GSE198520 Anti-TNF Synovium",
        "",
        markdown_table(
            ra_paired.sort_values(["fdr", "p"], na_position="last"),
            ["gene", "n_patients", "mean_post_minus_pre", "sd_post_minus_pre", "p", "fdr", "ra_paired_call"],
            n=len(ra_paired),
        ),
        "",
        "### RA Response Association",
        "",
        markdown_table(
            ra_response.sort_values(["adjusted_fdr", "raw_p"], na_position="last"),
            [
                "gene",
                "contrast",
                "raw_delta_true_minus_false",
                "hedges_g",
                "raw_p",
                "raw_fdr",
                "pathotype_adjusted_beta",
                "pathotype_adjusted_p",
                "adjusted_fdr",
                "ra_response_call",
            ],
            n=30,
        ),
        "",
        "## Wave37 Efferocytosis",
        "",
        markdown_table(
            effero.sort_values("median_efficient_minus_noneater_lfc", ascending=False, na_position="last"),
            [
                "gene_symbol",
                "n_sgrna",
                "median_efficient_lfc",
                "median_noneater_lfc",
                "median_efficient_minus_noneater_lfc",
                "contrast_p_wilcoxon",
                "contrast_fdr",
                "screen_call",
                "efferocytosis_direction",
            ],
            n=len(effero),
        ),
        "",
        "## Geneformer Evidence",
        "",
        markdown_table(geneformer, list(geneformer.columns), n=20),
        "",
        "## Interpretation Guardrails",
        "",
        "- The GSE282122 remission-response analysis is cell-resolved and paired, but it is anti-TNF-treated IBD myeloid tissue, not MS CNS tissue.",
        "- RA GSE198520 is bulk synovium; PD movement may reflect cell-composition or treatment-class effects.",
        "- Wave37 is murine BMDM CRISPR efferocytosis only; it does not test autoimmune tissue repair or inflammation guardrails.",
        "- Geneformer rows are retained as weak triage. For this candidate set, existing local model evidence covers only `CD300LF`.",
        "- No candidate here should be used as the V3 finding without fresh target-specific perturbation and novelty/prior-art work.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)

    gse_meta, gse_pairs, gse_paired, gse_response = gse282122_direct_candidate_pairs()
    wave68 = wave68_rows()
    ms = ms_gse111972_rows()
    broad_summary, broad_contrasts = broad_rows()
    effero = wave37_efferocytosis_rows()
    ra_delta, ra_paired, ra_response = ra_synovium_rows()
    wave69b = wave69b_local_rows()
    geneformer = geneformer_rows()

    integrated = integrate(gse_response, wave68, ms, broad_summary, effero, ra_paired, ra_response, geneformer)

    save_tsv(gse_meta, "gse282122_candidate_pseudobulk_metadata.tsv")
    save_tsv(gse_pairs, "gse282122_candidate_pair_deltas.tsv")
    save_tsv(gse_paired, "gse282122_candidate_paired_tests.tsv")
    save_tsv(gse_response, "gse282122_candidate_remission_response_tests.tsv")
    save_tsv(wave68, "wave68_candidate_rows.tsv")
    save_tsv(ms, "ms_gse111972_candidate_rows.tsv")
    save_tsv(broad_summary, "broad_h5ad_candidate_summary.tsv")
    save_tsv(broad_contrasts, "broad_h5ad_candidate_contrasts.tsv")
    save_tsv(effero, "wave37_efferocytosis_candidate_rows.tsv")
    save_tsv(ra_delta, "ra_gse198520_candidate_patient_deltas.tsv")
    save_tsv(ra_paired, "ra_gse198520_candidate_paired_tests.tsv")
    save_tsv(ra_response, "ra_gse198520_candidate_response_tests.tsv")
    save_tsv(geneformer, "geneformer_candidate_rows.tsv")
    save_tsv(integrated, "integrated_fc_ros_candidate_scout.tsv")
    for name, df in wave69b.items():
        save_tsv(df, "wave69b_overlap_" + name)

    summary = {
        "random_seed": SEED,
        "candidate_genes": CANDIDATES,
        "data_sources": {
            "gse282122_h5ad": rel(GSE282122_H5AD),
            "gse282122_pairs": rel(GSE282122_PAIRS),
            "wave68_integrated": rel(WAVE68_INTEGRATED),
            "ms_gse111972": rel(MS_SIGNATURE),
            "broad_h5ad_summary": rel(BROAD_SUMMARY),
            "broad_h5ad_contrasts": rel(BROAD_CONTRASTS),
            "ra_gse198520_counts": rel(RA_COUNTS),
            "ra_gse198520_meta": rel(RA_META),
            "wave37_efferocytosis": rel(WAVE37_EFFERO),
            "wave57_geneformer": rel(WAVE57_CALLS),
            "wave69d_geneformer": rel(WAVE69D_CALLS),
        },
        "n_gse282122_pseudobulk_strata": int(len(gse_meta)),
        "n_gse282122_pair_rows": int(len(gse_pairs)),
        "n_ra_delta_rows": int(len(ra_delta)),
        "integrated_call_counts": integrated["integrated_call"].value_counts().to_dict(),
        "top_integrated_rows": integrated.head(10).to_dict(orient="records"),
    }
    write_json(OUT / "summary.json", summary)
    write_report(integrated, gse_paired, gse_response, ms, broad_summary, effero, ra_paired, ra_response, geneformer)
    print(json.dumps(summary, indent=2, allow_nan=True))


if __name__ == "__main__":
    main()
