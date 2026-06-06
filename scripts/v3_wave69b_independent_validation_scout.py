#!/usr/bin/env python3
"""Wave69-B independent validation scout for Wave68 parked genes.

This is deliberately a scout, not a target-promoting analysis. It extracts
candidate-level recurrence from local independent autoimmune datasets and adds a
small RA synovium bulk gene-level audit that Wave65 had not run.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.formula.api import ols
from statsmodels.stats.multitest import multipletests

SEED = 20260527
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "phases/v3/results" / "wave69b_independent_validation_scout"

CANDIDATES = ["RGS14", "CD274", "TNFSF15", "CD80", "FCGR2B", "NCF1", "IL7R", "STAT4", "SP140"]

WAVE68 = ROOT / "phases/v3/results" / "wave68_gse282122_unrestricted_gene_screen" / "integrated_gene_target_rank.tsv"
MS_SIGNATURE = ROOT / "phases/v3/results" / "gse111972_full_ms_wm_signature.tsv"
BROAD_CONTRASTS = ROOT / "phases/v3/results" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_contrasts.tsv"
BROAD_SUMMARY = ROOT / "phases/v3/results" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_summary.tsv"
RA_COUNTS = ROOT / "phases/v3/results" / "wave65_gse198520_ra_synovium_antitnf_audit" / "gse198520_counts_used.tsv"
RA_META = ROOT / "phases/v3/results" / "wave65_gse198520_ra_synovium_antitnf_audit" / "gse198520_sample_metadata.tsv"


def hedges_g(a: np.ndarray, b: np.ndarray) -> float:
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    a = a[np.isfinite(a)]
    b = b[np.isfinite(b)]
    if len(a) < 2 or len(b) < 2:
        return np.nan
    pooled = ((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) / (len(a) + len(b) - 2)
    if pooled <= 0:
        return np.nan
    correction = 1.0 - (3.0 / (4.0 * (len(a) + len(b)) - 9.0))
    return float(((a.mean() - b.mean()) / math.sqrt(pooled)) * correction)


def save_tsv(df: pd.DataFrame, name: str) -> None:
    df.to_csv(OUT / name, sep="\t", index=False)


def wave68_origin() -> pd.DataFrame:
    df = pd.read_csv(WAVE68, sep="\t", low_memory=False)
    cols = [
        "gene",
        "cell_state",
        "wave68_call",
        "integrated_score",
        "paired_mean_delta",
        "paired_p",
        "paired_fdr",
        "raw_delta_remission_minus_non",
        "raw_p",
        "raw_fdr",
        "remission_adjusted_delta",
        "remission_adjusted_p",
        "remission_adjusted_fdr",
        "wave62_score",
        "wave62_call",
        "strong_l2g_diseases",
        "strong_qtl_diseases",
        "has_any_druggability_flag",
        "has_manual_blocker",
        "has_prior_art_blocker",
        "posthoc_blocker",
        "blockers",
    ]
    cols = [c for c in cols if c in df.columns]
    out = df[df["gene"].isin(CANDIDATES)][cols].copy()
    return out.sort_values(["wave68_call", "integrated_score"], ascending=[True, False])


def ms_local() -> pd.DataFrame:
    df = pd.read_csv(MS_SIGNATURE, sep="\t")
    out = df[df["gene"].isin(CANDIDATES)].copy()
    out["dataset"] = "GSE111972"
    out["system"] = "sorted human microglia, MS white matter vs control white matter"
    out["status"] = np.select(
        [
            (out["fdr"] <= 0.10) & (out["delta_log2"] > 0),
            (out["p"] < 0.05) & (out["delta_log2"] > 0),
            (out["p"] < 0.05) & (out["delta_log2"] < 0),
        ],
        ["positive_fdr10", "positive_nominal", "negative_nominal"],
        default="null_or_weak",
    )
    cols = ["dataset", "system", "gene", "delta_log2", "hedges_g", "p", "fdr", "status"]
    return out[cols].sort_values(["status", "p"])


def broad_h5ad() -> tuple[pd.DataFrame, pd.DataFrame]:
    contrasts = pd.read_csv(BROAD_CONTRASTS, sep="\t")
    contrasts = contrasts[contrasts["gene"].isin(CANDIDATES)].copy()
    contrasts["support_status"] = np.select(
        [
            contrasts["positive_fdr10"],
            contrasts["negative_fdr10"],
            contrasts["positive_nominal"],
            contrasts["negative_nominal"],
        ],
        ["positive_fdr10", "negative_fdr10", "positive_nominal", "negative_nominal"],
        default="null_or_weak",
    )
    priority = contrasts[
        contrasts["analysis"].str.startswith(("ibd_", "psoriasis_", "ra_blood_"), na=False)
    ].copy()

    summary = pd.read_csv(BROAD_SUMMARY, sep="\t")
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
    summary = summary[[c for c in keep if c in summary.columns]].sort_values(
        ["positive_fdr10_compartment_count", "positive_compartment_count", "best_positive_p"],
        ascending=[False, False, True],
    )
    return priority, summary


def ra_synovium_gene_audit() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
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

    paired_rows = []
    response_rows = []
    for gene, sub in deltas.groupby("gene", observed=True):
        vals = sub["post_minus_pre"].to_numpy(float)
        t_stat, p_value = stats.ttest_1samp(vals, 0.0, nan_policy="omit") if len(vals) >= 3 else (np.nan, np.nan)
        paired_rows.append(
            {
                "gene": gene,
                "n_patients": int(len(vals)),
                "mean_post_minus_pre": float(np.nanmean(vals)),
                "sd_post_minus_pre": float(np.nanstd(vals, ddof=1)),
                "t": float(t_stat) if np.isfinite(t_stat) else np.nan,
                "p": float(p_value) if np.isfinite(p_value) else np.nan,
            }
        )
        for contrast, column in [
            ("good_vs_moderate_none", "responder_good_only"),
            ("moderate_good_vs_none", "responder_moderate_or_good"),
        ]:
            a = sub.loc[sub[column].astype(bool), "post_minus_pre"].to_numpy(float)
            b = sub.loc[~sub[column].astype(bool), "post_minus_pre"].to_numpy(float)
            if len(a) >= 2 and len(b) >= 2:
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
                    "gene": gene,
                    "contrast": contrast,
                    "n_true": int(len(a)),
                    "n_false": int(len(b)),
                    "mean_true": float(np.nanmean(a)) if len(a) else np.nan,
                    "mean_false": float(np.nanmean(b)) if len(b) else np.nan,
                    "raw_delta_true_minus_false": float(np.nanmean(a) - np.nanmean(b)) if len(a) and len(b) else np.nan,
                    "hedges_g": hedges_g(a, b),
                    "raw_p": float(p2) if np.isfinite(p2) else np.nan,
                    "pathotype_adjusted_beta": adjusted_beta,
                    "pathotype_adjusted_p": adjusted_p,
                }
            )
    paired = pd.DataFrame(paired_rows)
    response = pd.DataFrame(response_rows)
    if not paired.empty:
        paired["fdr"] = multipletests(paired["p"].fillna(1.0), method="fdr_bh")[1]
        paired["status"] = np.select(
            [(paired["fdr"] <= 0.10), (paired["p"] < 0.05)],
            ["paired_pharmacodynamic_fdr10", "paired_pharmacodynamic_nominal"],
            default="null_or_weak",
        )
    if not response.empty:
        response["raw_fdr"] = multipletests(response["raw_p"].fillna(1.0), method="fdr_bh")[1]
        response["adjusted_fdr"] = multipletests(response["pathotype_adjusted_p"].fillna(1.0), method="fdr_bh")[1]
        response["status"] = np.select(
            [(response["adjusted_fdr"] <= 0.10), (response["raw_fdr"] <= 0.10), (response["raw_p"] < 0.05)],
            ["response_pathotype_adjusted_fdr10", "response_raw_fdr10", "response_raw_nominal"],
            default="null_or_weak",
        )
    return deltas, paired.sort_values("p"), response.sort_values(["adjusted_fdr", "raw_p"])


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)

    origin = wave68_origin()
    ms = ms_local()
    broad_priority, broad_summary = broad_h5ad()
    ra_delta, ra_paired, ra_response = ra_synovium_gene_audit()

    save_tsv(origin, "wave68_origin_candidate_rows.tsv")
    save_tsv(ms, "ms_gse111972_candidate_rows.tsv")
    save_tsv(broad_priority, "broad_h5ad_priority_candidate_rows.tsv")
    save_tsv(broad_summary, "broad_h5ad_candidate_summary.tsv")
    save_tsv(ra_delta, "ra_gse198520_candidate_patient_deltas.tsv")
    save_tsv(ra_paired, "ra_gse198520_candidate_paired_tests.tsv")
    save_tsv(ra_response, "ra_gse198520_candidate_response_tests.tsv")

    summary = {
        "random_seed": SEED,
        "candidate_genes": CANDIDATES,
        "origin_rows": int(len(origin)),
        "ms_candidate_rows": int(len(ms)),
        "broad_priority_rows": int(len(broad_priority)),
        "ra_synovium_delta_rows": int(len(ra_delta)),
        "ra_synovium_patient_count": int(ra_delta["patient"].nunique()) if not ra_delta.empty else 0,
        "strongest_broad_h5ad": broad_summary.head(9).to_dict(orient="records"),
        "strongest_ra_synovium_paired": ra_paired.head(9).to_dict(orient="records"),
        "strongest_ra_synovium_response": ra_response.head(9).to_dict(orient="records"),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, allow_nan=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, allow_nan=True))


if __name__ == "__main__":
    main()
