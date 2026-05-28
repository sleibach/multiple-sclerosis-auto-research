#!/usr/bin/env python3
"""Wave78 LILRB inhibitory-receptor family audit.

Rationale:
Wave75-A nominated the LILRB inhibitory-receptor family as the only bounded
target class worth a response-direction audit after generic macrophage and
lipid-mediator routes repeatedly failed. This script tests that nomination
against local V3 data with explicit anti-proxy gates.

The audit is target-level: it asks whether a named receptor has cross-disease
cell-state recurrence, MS guardrail support, adjusted treatment-response
specificity in RA and IBD, genetic anchoring, foundation-model/perturbation
direction support, and a plausible non-blocked intervention route.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from statsmodels.stats.multitest import multipletests

from v3_analyze_direct_h5ad_cell_states import MODULES as BASE_MODULES
from v3_analyze_direct_h5ad_cell_states import ROOT
from v3_wave68_gse282122_unrestricted_gene_screen import (
    aggregate_all_genes,
    build_primary_obs,
    load_inputs,
    logcpm as ibd_logcpm,
)


SEED = 20260527
OUT = ROOT / "results_v3" / "wave78_lilrb_inhibitory_receptor_audit"

BROAD = ROOT / "results_v3" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_contrasts.tsv"
MS_SIG = ROOT / "results_v3" / "gse111972_full_ms_wm_signature.tsv"
W62 = ROOT / "results_v3" / "wave62_opentargets_target_resolution" / "target_resolution_summary.tsv"
W62_QTL = ROOT / "results_v3" / "wave62_opentargets_target_resolution" / "opentargets_qtl_coloc_rows.tsv"
W70B = ROOT / "results_v3" / "wave70b_fc_ros_computational_scout" / "integrated_fc_ros_candidate_scout.tsv"
W70C = ROOT / "results_v3" / "wave70c_inhibitory_receptor_geneformer_direction" / "geneformer_direction_candidate_calls.tsv"
W37 = ROOT / "results_v3" / "wave37_gse212008_crispr_efferocytosis_screen" / "gene_level_screen_scores.tsv"
RA_COUNTS = ROOT / "results_v3" / "wave65_gse198520_ra_synovium_antitnf_audit" / "gse198520_counts_used.tsv"
RA_META = ROOT / "results_v3" / "wave65_gse198520_ra_synovium_antitnf_audit" / "gse198520_sample_metadata.tsv"
IBD_PAIR_META = ROOT / "results_v3" / "wave68_gse282122_unrestricted_gene_screen" / "all_gene_pair_metadata.tsv"

TARGET_GENES = ["LILRB1", "LILRB2", "LILRB3", "LILRB4", "LILRB5"]
COMPARATOR_GENES = ["LAIR1", "CD300A", "CD300LF", "FCGR2B", "INPP5D"]
GENES = TARGET_GENES + COMPARATOR_GENES
GENERIC_MODULE = "inflammatory_nfkb"
GENERIC_GENES = BASE_MODULES[GENERIC_MODULE]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def read_tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True) + "\n", encoding="utf-8")


def markdown_table(df: pd.DataFrame, max_rows: int = 30) -> str:
    if df.empty:
        return "_No rows._"
    view = df.head(max_rows).copy()
    cols = list(view.columns)
    lines = ["| " + " | ".join(cols) + " |", "| " + " | ".join(["---"] * len(cols)) + " |"]
    for _, row in view.iterrows():
        vals = []
        for col in cols:
            value = row[col]
            if isinstance(value, float):
                vals.append("" if math.isnan(value) else f"{value:.4g}")
            else:
                vals.append(str(value).replace("|", "\\|"))
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines)


def bh(values: pd.Series | np.ndarray) -> np.ndarray:
    return multipletests(pd.Series(values).fillna(1.0).to_numpy(float), method="fdr_bh")[1]


def numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series.replace("NA", np.nan), errors="coerce")


def log_cpm(counts: pd.DataFrame) -> pd.DataFrame:
    lib = counts.sum(axis=0).replace(0, np.nan)
    return np.log2(counts.div(lib, axis=1) * 1_000_000.0 + 1.0)


def zscore_columns(expr: pd.DataFrame) -> pd.DataFrame:
    return expr.sub(expr.mean(axis=0), axis=1).div(expr.std(axis=0, ddof=1).replace(0, np.nan), axis=1)


def zscore_rows(expr: pd.DataFrame) -> pd.DataFrame:
    return expr.sub(expr.mean(axis=1), axis=0).div(expr.std(axis=1, ddof=1).replace(0, np.nan), axis=0)


def broad_summary() -> tuple[pd.DataFrame, pd.DataFrame]:
    df = read_tsv(BROAD)
    if df.empty:
        return pd.DataFrame(), pd.DataFrame()
    sub = df[df["gene"].astype(str).str.upper().isin(GENES)].copy()
    if sub.empty:
        return sub, pd.DataFrame()
    sub["gene"] = sub["gene"].astype(str).str.upper()
    sub["nominal_positive"] = (sub["delta_log2_cpm"] >= 0.35) & (sub["p"] <= 0.05)
    sub["nominal_negative"] = (sub["delta_log2_cpm"] <= -0.35) & (sub["p"] <= 0.05)
    rows = []
    for gene, gdf in sub.groupby("gene", observed=True):
        pos = sorted(gdf.loc[gdf["nominal_positive"], "disease_name"].astype(str).unique())
        neg = sorted(gdf.loc[gdf["nominal_negative"], "disease_name"].astype(str).unique())
        best = gdf.iloc[int(np.nanargmin(gdf["p"].fillna(1.0).to_numpy(float)))]
        rows.append(
            {
                "gene": gene,
                "contexts_tested": int(gdf["analysis"].nunique()),
                "positive_contexts": int(gdf["nominal_positive"].sum()),
                "negative_contexts": int(gdf["nominal_negative"].sum()),
                "positive_disease_count": len(pos),
                "positive_diseases": ";".join(pos),
                "negative_disease_count": len(neg),
                "negative_diseases": ";".join(neg),
                "best_context": best["analysis"],
                "best_disease": best["disease_name"],
                "best_delta_log2_cpm": float(best["delta_log2_cpm"]),
                "best_p": float(best["p"]),
                "best_fdr": float(best["fdr"]),
            }
        )
    out = pd.DataFrame(rows).sort_values(["positive_disease_count", "best_p"], ascending=[False, True])
    return sub.sort_values(["gene", "p"]), out


def ms_rows() -> pd.DataFrame:
    df = read_tsv(MS_SIG)
    if df.empty:
        return pd.DataFrame()
    sub = df[df["gene"].astype(str).str.upper().isin(GENES)].copy()
    if sub.empty:
        return sub
    sub["gene"] = sub["gene"].astype(str).str.upper()
    sub["ms_positive_anchor"] = (sub["delta_log2"] >= 0.35) & (sub["p"] <= 0.05)
    sub["ms_nominal_down"] = (sub["delta_log2"] <= -0.35) & (sub["p"] <= 0.05)
    sub["ms_nonnegative_guardrail"] = ~sub["ms_nominal_down"]
    return sub.sort_values("p")


def wave62_rows() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    summary = read_tsv(W62)
    qtl = read_tsv(W62_QTL)
    sum_sub = pd.DataFrame()
    qtl_sub = pd.DataFrame()
    qtl_summary = pd.DataFrame()
    if not summary.empty:
        sum_sub = summary[summary["gene"].astype(str).str.upper().isin(GENES)].copy()
        if not sum_sub.empty:
            sum_sub["gene"] = sum_sub["gene"].astype(str).str.upper()
    if not qtl.empty:
        qtl_sub = qtl[qtl["gene"].astype(str).str.upper().isin(GENES)].copy()
        if not qtl_sub.empty:
            qtl_sub["gene"] = qtl_sub["gene"].astype(str).str.upper()
            rows = []
            for gene, gdf in qtl_sub.groupby("gene", observed=True):
                strong = gdf[gdf["h4"] >= 0.8]
                rows.append(
                    {
                        "gene": gene,
                        "qtl_coloc_rows": int(gdf.shape[0]),
                        "max_h4": float(gdf["h4"].max()),
                        "strong_h4_disease_count": int(strong["disease"].nunique()),
                        "strong_h4_diseases": ";".join(sorted(strong["disease"].astype(str).unique())),
                        "ms_max_h4": float(gdf.loc[gdf["disease"].eq("MS"), "h4"].max())
                        if (gdf["disease"].eq("MS")).any()
                        else 0.0,
                        "myeloid_relevant_rows": int(gdf["biosample_myeloid"].fillna(False).astype(bool).sum())
                        if "biosample_myeloid" in gdf.columns
                        else 0,
                    }
                )
            qtl_summary = pd.DataFrame(rows).sort_values(["strong_h4_disease_count", "max_h4"], ascending=[False, False])
    return sum_sub, qtl_sub, qtl_summary


def module_score_from_gene_x_sample(expr_gene_x_sample: pd.DataFrame) -> pd.Series:
    z = zscore_rows(expr_gene_x_sample)
    present = [gene for gene in GENERIC_GENES if gene in z.index]
    if not present:
        return pd.Series(index=expr_gene_x_sample.columns, dtype=float)
    return z.loc[present].mean(axis=0, skipna=True)


def fit_model(
    data: pd.DataFrame,
    y_col: str,
    response_col: str,
    rhs: str,
    dataset: str,
    gene: str,
    cell_state: str,
    endpoint: str,
    comparison: str,
) -> dict[str, Any]:
    needed = [y_col, response_col]
    for col in [
        "pre_generic",
        "delta_generic",
        "pre_score",
        "baseline_inflammation_score",
        "inflammatory_score",
        "das28_score",
    ]:
        if col in rhs and col in data.columns:
            needed.append(col)
    needed = [c for c in needed if c in data.columns]
    model_df = data.dropna(subset=needed).copy()
    if model_df.shape[0] < 12 or model_df[response_col].nunique() < 2:
        return {
            "dataset": dataset,
            "gene": gene,
            "cell_state": cell_state,
            "endpoint": endpoint,
            "comparison": comparison,
            "n": int(model_df.shape[0]),
            "response_coef": np.nan,
            "response_p": np.nan,
            "model_status": "insufficient_rows_or_response_levels",
            "formula": "",
        }
    model_df = model_df.rename(columns={y_col: "y"})
    formula = f"y ~ {rhs}"
    try:
        model = smf.ols(formula, data=model_df).fit()
        coef = float(model.params.get(response_col, np.nan))
        pval = float(model.pvalues.get(response_col, np.nan))
        status = "ok"
    except Exception as exc:  # noqa: BLE001
        coef = np.nan
        pval = np.nan
        status = f"fit_failed:{type(exc).__name__}:{exc}"
    return {
        "dataset": dataset,
        "gene": gene,
        "cell_state": cell_state,
        "endpoint": endpoint,
        "comparison": comparison,
        "n": int(model_df.shape[0]),
        "response_coef": coef,
        "response_p": pval,
        "model_status": status,
        "formula": formula,
    }


def ra_pairs_and_models() -> tuple[pd.DataFrame, pd.DataFrame]:
    counts = read_tsv(RA_COUNTS)
    meta = read_tsv(RA_META)
    if counts.empty or meta.empty:
        return pd.DataFrame(), pd.DataFrame()
    counts = counts.set_index("GeneSymbol")
    counts.index = counts.index.astype(str).str.upper()
    expr = log_cpm(counts.astype(float))
    z = zscore_rows(expr)
    generic = module_score_from_gene_x_sample(expr)
    present = [gene for gene in GENES if gene in z.index]

    sample = meta[
        [
            "count_column",
            "patient",
            "response_code",
            "response_class",
            "timepoint",
            "pathotype",
            "biologic",
            "inflammatory_score",
            "das28_score",
        ]
    ].copy()
    sample["inflammatory_score"] = numeric(sample["inflammatory_score"])
    sample["das28_score"] = numeric(sample["das28_score"])
    sample["generic_inflammatory_nfkb"] = sample["count_column"].map(generic.to_dict()).astype(float)
    for gene in present:
        sample[f"score_{gene}"] = sample["count_column"].map(z.loc[gene].to_dict()).astype(float)

    pair_rows = []
    for patient, sub in sample.groupby("patient", observed=True):
        pre = sub[sub["timepoint"].eq("pre")]
        post = sub[sub["timepoint"].eq("post")]
        if len(pre) != 1 or len(post) != 1:
            continue
        p = pre.iloc[0]
        q = post.iloc[0]
        for gene in present:
            pair_rows.append(
                {
                    "patient": patient,
                    "gene": gene,
                    "response_code": p["response_code"],
                    "response_class": p["response_class"],
                    "good_response": int(p["response_code"] == "r"),
                    "moderate_good_response": int(p["response_code"] in {"r", "mr"}),
                    "pathotype": p.get("pathotype", ""),
                    "biologic": p.get("biologic", ""),
                    "inflammatory_score": p.get("inflammatory_score", np.nan),
                    "das28_score": p.get("das28_score", np.nan),
                    "pre_score": float(p[f"score_{gene}"]),
                    "post_score": float(q[f"score_{gene}"]),
                    "post_minus_pre": float(q[f"score_{gene}"] - p[f"score_{gene}"]),
                    "pre_generic": float(p["generic_inflammatory_nfkb"]),
                    "post_generic": float(q["generic_inflammatory_nfkb"]),
                    "delta_generic": float(q["generic_inflammatory_nfkb"] - p["generic_inflammatory_nfkb"]),
                }
            )
    pairs = pd.DataFrame(pair_rows)
    rows = []
    for gene, sub in pairs.groupby("gene", observed=True):
        for comparison, response_col in [
            ("good_vs_moderate_none", "good_response"),
            ("moderate_good_vs_none", "moderate_good_response"),
        ]:
            rows.append(
                fit_model(
                    sub,
                    "pre_score",
                    response_col,
                    f"{response_col} + pre_generic + C(pathotype) + C(biologic) + inflammatory_score + das28_score",
                    "GSE198520_RA_synovium_antiTNF",
                    gene,
                    "bulk_synovium",
                    "baseline_pre",
                    comparison,
                )
            )
            rows.append(
                fit_model(
                    sub,
                    "post_minus_pre",
                    response_col,
                    f"{response_col} + pre_score + pre_generic + delta_generic + C(pathotype) + C(biologic) + inflammatory_score + das28_score",
                    "GSE198520_RA_synovium_antiTNF",
                    gene,
                    "bulk_synovium",
                    "delta_post_minus_pre",
                    comparison,
                )
            )
    models = pd.DataFrame(rows)
    models["response_fdr"] = bh(models["response_p"]) if not models.empty else []
    return pairs, models


def ibd_pairs_and_models() -> tuple[pd.DataFrame, pd.DataFrame]:
    adata, paired_samples, obs = load_inputs()
    primary_obs = build_primary_obs(obs, paired_samples)
    meta, counts = aggregate_all_genes(adata, primary_obs)
    expr = ibd_logcpm(meta, counts)
    z = zscore_columns(expr)
    present = [gene for gene in GENES if gene in z.columns]
    generic_present = [gene for gene in GENERIC_GENES if gene in z.columns]
    sample = meta.copy()
    if generic_present:
        sample["generic_inflammatory_nfkb"] = z[generic_present].mean(axis=1, skipna=True)
    else:
        sample["generic_inflammatory_nfkb"] = np.nan
    for gene in present:
        sample[f"score_{gene}"] = z[gene].to_numpy(float)

    pair_meta = read_tsv(IBD_PAIR_META)
    pair_meta = pair_meta[pair_meta["passes_cell_threshold"].astype(bool)].copy()
    score_by_key = sample.set_index(["sample_id", "cell_state"])
    site_rows = []
    for _, pair in pair_meta.iterrows():
        pre_key = (pair["pre_sample_id"], pair["cell_state"])
        post_key = (pair["post_sample_id"], pair["cell_state"])
        if pre_key not in score_by_key.index or post_key not in score_by_key.index:
            continue
        p = score_by_key.loc[pre_key]
        q = score_by_key.loc[post_key]
        if isinstance(p, pd.DataFrame):
            p = p.iloc[0]
        if isinstance(q, pd.DataFrame):
            q = q.iloc[0]
        for gene in present:
            site_rows.append(
                {
                    "Patient": pair["Patient"],
                    "Disease": pair["Disease"],
                    "Site": pair["Site"],
                    "Remission_status": pair["Remission_status"],
                    "remission": int(pair["Remission_status"] == "Remission"),
                    "cell_state": pair["cell_state"],
                    "gene": gene,
                    "baseline_inflammation_score": pair["baseline_inflammation_score"],
                    "pre_score": float(p[f"score_{gene}"]),
                    "post_score": float(q[f"score_{gene}"]),
                    "post_minus_pre": float(q[f"score_{gene}"] - p[f"score_{gene}"]),
                    "pre_generic": float(p["generic_inflammatory_nfkb"]),
                    "post_generic": float(q["generic_inflammatory_nfkb"]),
                    "delta_generic": float(q["generic_inflammatory_nfkb"] - p["generic_inflammatory_nfkb"]),
                }
            )
    site_pairs = pd.DataFrame(site_rows)
    collapsed = []
    if not site_pairs.empty:
        for keys, sub in site_pairs.groupby(["Patient", "Disease", "Remission_status", "cell_state", "gene"], observed=True):
            collapsed.append(
                {
                    "Patient": keys[0],
                    "Disease": keys[1],
                    "Remission_status": keys[2],
                    "remission": int(keys[2] == "Remission"),
                    "cell_state": keys[3],
                    "gene": keys[4],
                    "n_sites": int(sub["Site"].nunique()),
                    "baseline_inflammation_score": float(pd.to_numeric(sub["baseline_inflammation_score"], errors="coerce").mean()),
                    "pre_score": float(sub["pre_score"].mean()),
                    "post_score": float(sub["post_score"].mean()),
                    "post_minus_pre": float(sub["post_minus_pre"].mean()),
                    "pre_generic": float(sub["pre_generic"].mean()),
                    "post_generic": float(sub["post_generic"].mean()),
                    "delta_generic": float(sub["delta_generic"].mean()),
                }
            )
    pairs = pd.DataFrame(collapsed)
    rows = []
    for (gene, cell_state), sub in pairs.groupby(["gene", "cell_state"], observed=True):
        rows.append(
            fit_model(
                sub,
                "pre_score",
                "remission",
                "remission + pre_generic + C(Disease) + baseline_inflammation_score",
                "GSE282122_IBD_myeloid_antiTNF",
                gene,
                str(cell_state),
                "baseline_pre",
                "remission_vs_nonremission",
            )
        )
        rows.append(
            fit_model(
                sub,
                "post_minus_pre",
                "remission",
                "remission + pre_score + pre_generic + delta_generic + C(Disease) + baseline_inflammation_score",
                "GSE282122_IBD_myeloid_antiTNF",
                gene,
                str(cell_state),
                "delta_post_minus_pre",
                "remission_vs_nonremission",
            )
        )
    models = pd.DataFrame(rows)
    models["response_fdr"] = bh(models["response_p"]) if not models.empty else []
    return pairs, models


def generic_reference_coefficients(ra_pairs: pd.DataFrame, ibd_pairs: pd.DataFrame) -> pd.DataFrame:
    rows = []
    if not ra_pairs.empty:
        base = ra_pairs.drop_duplicates("patient").copy()
        for comparison, response_col in [
            ("good_vs_moderate_none", "good_response"),
            ("moderate_good_vs_none", "moderate_good_response"),
        ]:
            rows.append(
                fit_model(
                    base,
                    "pre_generic",
                    response_col,
                    f"{response_col} + C(pathotype) + C(biologic) + inflammatory_score + das28_score",
                    "GSE198520_RA_synovium_antiTNF",
                    "__GENERIC__",
                    "bulk_synovium",
                    "baseline_pre",
                    comparison,
                )
            )
            rows.append(
                fit_model(
                    base,
                    "delta_generic",
                    response_col,
                    f"{response_col} + pre_generic + C(pathotype) + C(biologic) + inflammatory_score + das28_score",
                    "GSE198520_RA_synovium_antiTNF",
                    "__GENERIC__",
                    "bulk_synovium",
                    "delta_post_minus_pre",
                    comparison,
                )
            )
    if not ibd_pairs.empty:
        base = ibd_pairs.drop_duplicates(["Patient", "cell_state"]).copy()
        for cell_state, sub in base.groupby("cell_state", observed=True):
            rows.append(
                fit_model(
                    sub,
                    "pre_generic",
                    "remission",
                    "remission + C(Disease) + baseline_inflammation_score",
                    "GSE282122_IBD_myeloid_antiTNF",
                    "__GENERIC__",
                    str(cell_state),
                    "baseline_pre",
                    "remission_vs_nonremission",
                )
            )
            rows.append(
                fit_model(
                    sub,
                    "delta_generic",
                    "remission",
                    "remission + pre_generic + C(Disease) + baseline_inflammation_score",
                    "GSE282122_IBD_myeloid_antiTNF",
                    "__GENERIC__",
                    str(cell_state),
                    "delta_post_minus_pre",
                    "remission_vs_nonremission",
                )
            )
    out = pd.DataFrame(rows)
    if not out.empty:
        out = out.rename(columns={"response_coef": "generic_response_coef", "response_p": "generic_response_p"})
    return out


def add_generic_ratios(models: pd.DataFrame, generic: pd.DataFrame) -> pd.DataFrame:
    if models.empty or generic.empty:
        return models
    g = generic[
        [
            "dataset",
            "cell_state",
            "endpoint",
            "comparison",
            "generic_response_coef",
            "generic_response_p",
        ]
    ].copy()
    out = models.merge(g, on=["dataset", "cell_state", "endpoint", "comparison"], how="left")
    out["target_generic_abs_ratio"] = np.where(
        out["generic_response_coef"].abs() > 1e-9,
        out["response_coef"].abs() / out["generic_response_coef"].abs(),
        np.inf,
    )
    return out


def response_convergence(ra: pd.DataFrame, ibd: pd.DataFrame) -> pd.DataFrame:
    rows = []
    if ra.empty or ibd.empty:
        return pd.DataFrame()
    for gene in sorted(set(ra["gene"]) & set(ibd["gene"])):
        for endpoint in ["baseline_pre", "delta_post_minus_pre"]:
            rsub = ra[(ra["gene"].eq(gene)) & (ra["endpoint"].eq(endpoint)) & ra["model_status"].eq("ok")]
            isub = ibd[(ibd["gene"].eq(gene)) & (ibd["endpoint"].eq(endpoint)) & ibd["model_status"].eq("ok")]
            if rsub.empty or isub.empty:
                continue
            rbest = rsub.sort_values("response_p").iloc[0]
            ibest = isub.sort_values("response_p").iloc[0]
            rcoef = float(rbest["response_coef"])
            icoef = float(ibest["response_coef"])
            sign_stable = math.isfinite(rcoef) and math.isfinite(icoef) and np.sign(rcoef) == np.sign(icoef)
            rows.append(
                {
                    "gene": gene,
                    "endpoint": endpoint,
                    "ra_comparison": rbest["comparison"],
                    "ra_coef": rcoef,
                    "ra_p": float(rbest["response_p"]),
                    "ra_fdr": float(rbest["response_fdr"]),
                    "ra_generic_coef": float(rbest.get("generic_response_coef", np.nan)),
                    "ra_target_generic_abs_ratio": float(rbest.get("target_generic_abs_ratio", np.nan)),
                    "ibd_cell_state": ibest["cell_state"],
                    "ibd_coef": icoef,
                    "ibd_p": float(ibest["response_p"]),
                    "ibd_fdr": float(ibest["response_fdr"]),
                    "ibd_generic_coef": float(ibest.get("generic_response_coef", np.nan)),
                    "ibd_target_generic_abs_ratio": float(ibest.get("target_generic_abs_ratio", np.nan)),
                    "sign_stable": bool(sign_stable),
                    "both_p10": bool(sign_stable and rbest["response_p"] <= 0.10 and ibest["response_p"] <= 0.10),
                    "both_ratio_ge2": bool(
                        sign_stable
                        and rbest.get("target_generic_abs_ratio", 0.0) >= 2.0
                        and ibest.get("target_generic_abs_ratio", 0.0) >= 2.0
                    ),
                }
            )
    out = pd.DataFrame(rows)
    if not out.empty:
        out["response_specificity_pass"] = out["both_p10"] & out["both_ratio_ge2"]
        out["priority"] = (
            4 * out["response_specificity_pass"].astype(int)
            + 2 * out["both_p10"].astype(int)
            + out["sign_stable"].astype(int)
        )
        out = out.sort_values(["priority", "ra_p", "ibd_p"], ascending=[False, True, True])
    return out


def rows_for_genes(path: Path) -> pd.DataFrame:
    df = read_tsv(path)
    if df.empty:
        return df
    gene_col = "gene" if "gene" in df.columns else "candidate" if "candidate" in df.columns else None
    if gene_col is None:
        return pd.DataFrame()
    out = df[df[gene_col].astype(str).str.upper().isin(GENES)].copy()
    if not out.empty:
        out[gene_col] = out[gene_col].astype(str).str.upper()
    return out


def integrated_decision(
    broad: pd.DataFrame,
    ms: pd.DataFrame,
    w62_summary: pd.DataFrame,
    qtl_summary: pd.DataFrame,
    conv: pd.DataFrame,
    w70b: pd.DataFrame,
    w70c: pd.DataFrame,
    w37: pd.DataFrame,
) -> pd.DataFrame:
    broad_by_gene = broad.set_index("gene").to_dict(orient="index") if not broad.empty else {}
    ms_by_gene = ms.set_index("gene").to_dict(orient="index") if not ms.empty else {}
    w62_by_gene = w62_summary.set_index("gene").to_dict(orient="index") if not w62_summary.empty else {}
    qtl_by_gene = qtl_summary.set_index("gene").to_dict(orient="index") if not qtl_summary.empty else {}
    conv_by_gene = {}
    if not conv.empty:
        for gene, gdf in conv.groupby("gene", observed=True):
            conv_by_gene[gene] = gdf.sort_values(["priority", "ra_p", "ibd_p"], ascending=[False, True, True]).iloc[0].to_dict()
    w70c_by_gene = w70c.set_index("gene").to_dict(orient="index") if not w70c.empty and "gene" in w70c.columns else {}
    w70b_by_gene = w70b.set_index("gene").to_dict(orient="index") if not w70b.empty and "gene" in w70b.columns else {}
    w37_gene_col = "gene_symbol" if "gene_symbol" in w37.columns else "gene" if "gene" in w37.columns else None
    w37_by_gene = w37.set_index(w37_gene_col).to_dict(orient="index") if w37_gene_col and not w37.empty else {}

    rows = []
    for gene in GENES:
        b = broad_by_gene.get(gene, {})
        m = ms_by_gene.get(gene, {})
        s = w62_by_gene.get(gene, {})
        q = qtl_by_gene.get(gene, {})
        c = conv_by_gene.get(gene, {})
        model_call = str(w70c_by_gene.get(gene, {}).get("direction_model_call", ""))
        wave70_call = str(w70c_by_gene.get(gene, {}).get("wave70_call", w70b_by_gene.get(gene, {}).get("integrated_call", "")))
        wave37_call = str(w37_by_gene.get(gene, {}).get("screen_call", w37_by_gene.get(gene, {}).get("wave37_screen_call", "")))

        gate_breadth = int(b.get("positive_disease_count", 0) >= 3)
        gate_local_response = int(bool(c.get("response_specificity_pass", False)))
        gate_ms_anchor = int(bool(m.get("ms_positive_anchor", False)))
        gate_ms_guardrail = int(bool(m.get("ms_nonnegative_guardrail", True)))
        gate_genetics = int(q.get("strong_h4_disease_count", 0) >= 2 or not str(s.get("wave62_call", "NO_GO")).startswith("NO_GO"))
        gate_model = int("MODEL_SUPPORT" in model_call and "BLOCKED" not in model_call and "NO_GO" not in model_call)
        gate_perturbation = int(wave37_call not in {"", "UNRESOLVED", "not_present_in_wave37_mouse_screen", "null_or_weak"})
        surface_modality = gene.startswith("LILRB") or gene in {"LAIR1", "CD300A", "CD300LF", "FCGR2B"}
        direction_blocked = (
            "NO_GO" in model_call
            or "NO_GO" in wave70_call
            or "BLOCKED" in wave70_call
            or gene in {"FCGR2B", "INPP5D"}
        )
        gate_intervention = int(surface_modality and not direction_blocked)
        gate_count = sum(
            [
                gate_breadth,
                gate_local_response,
                gate_ms_anchor,
                gate_ms_guardrail,
                gate_genetics,
                gate_model,
                gate_perturbation,
                gate_intervention,
            ]
        )
        if gene in TARGET_GENES and gate_count >= 6 and gate_ms_anchor and gate_local_response and gate_intervention:
            call = "REOPEN_LILRB_TARGET"
            reason = "LILRB target passes strict Wave78 gates"
        elif gene in TARGET_GENES and (gate_local_response or gate_genetics or b.get("positive_disease_count", 0) >= 2):
            call = "PARK_LILRB_DIRECTIONALLY_UNRESOLVED"
            reason = "some target-level signal exists but MS, specificity, model direction, or intervention route is insufficient"
        else:
            call = "NO_GO_LILRB_LOCAL_AUDIT"
            reason = "does not pass target-level local gates"
        rows.append(
            {
                "gene": gene,
                "wave78_call": call,
                "gate_count": gate_count,
                "gate_breadth_ge3_diseases": gate_breadth,
                "gate_adjusted_ra_ibd_response_specific": gate_local_response,
                "gate_ms_positive_anchor": gate_ms_anchor,
                "gate_ms_nonnegative_guardrail": gate_ms_guardrail,
                "gate_cross_disease_genetics": gate_genetics,
                "gate_foundation_model_direction": gate_model,
                "gate_direct_perturbation": gate_perturbation,
                "gate_nonblocked_intervention_route": gate_intervention,
                "positive_disease_count": b.get("positive_disease_count", 0),
                "positive_diseases": b.get("positive_diseases", ""),
                "ms_delta_log2": m.get("delta_log2", np.nan),
                "ms_p": m.get("p", np.nan),
                "ms_fdr": m.get("fdr", np.nan),
                "qtl_strong_h4_disease_count": q.get("strong_h4_disease_count", 0),
                "qtl_strong_h4_diseases": q.get("strong_h4_diseases", ""),
                "wave62_call": s.get("wave62_call", ""),
                "best_response_endpoint": c.get("endpoint", ""),
                "ra_response_p": c.get("ra_p", np.nan),
                "ibd_response_p": c.get("ibd_p", np.nan),
                "ra_target_generic_abs_ratio": c.get("ra_target_generic_abs_ratio", np.nan),
                "ibd_target_generic_abs_ratio": c.get("ibd_target_generic_abs_ratio", np.nan),
                "direction_model_call": model_call,
                "wave70_call": wave70_call,
                "wave37_call": wave37_call,
                "decision_reason": reason,
            }
        )
    out = pd.DataFrame(rows)
    out["is_lilrb_target"] = out["gene"].isin(TARGET_GENES)
    return out.sort_values(["is_lilrb_target", "gate_count", "positive_disease_count"], ascending=[False, False, False])


def write_report(
    decision: pd.DataFrame,
    broad_sum: pd.DataFrame,
    ms: pd.DataFrame,
    qtl_summary: pd.DataFrame,
    conv: pd.DataFrame,
    ra_models: pd.DataFrame,
    ibd_models: pd.DataFrame,
    w70b: pd.DataFrame,
    w70c: pd.DataFrame,
) -> None:
    lines = [
        "# Wave78 LILRB Inhibitory-Receptor Family Audit",
        "",
        "## Question",
        "",
        "Does any LILRB-family inhibitory receptor survive as a target-level",
        "cross-autoimmune/MS intervention point after adjusted treatment-response",
        "specificity, MS guardrails, genetics, model-direction, and intervention",
        "route checks?",
        "",
        "## Verdict",
        "",
        str(decision.iloc[0]["wave78_call"]) if not decision.empty else "NO_GO_NO_DECISION_ROWS",
        "",
        "## Integrated Decision",
        "",
        markdown_table(decision, max_rows=20),
        "",
        "## Broad Disease Cell-State Summary",
        "",
        markdown_table(broad_sum, max_rows=20),
        "",
        "## MS White-Matter Rows",
        "",
        markdown_table(ms, max_rows=20),
        "",
        "## QTL Colocalization Summary",
        "",
        markdown_table(qtl_summary, max_rows=20),
        "",
        "## Adjusted RA/IBD Response Convergence",
        "",
        markdown_table(conv, max_rows=40),
        "",
        "## RA Adjusted Models",
        "",
        markdown_table(
            ra_models.sort_values("response_p")[
                [
                    "gene",
                    "endpoint",
                    "comparison",
                    "n",
                    "response_coef",
                    "response_p",
                    "response_fdr",
                    "generic_response_coef",
                    "target_generic_abs_ratio",
                    "model_status",
                ]
            ]
            if not ra_models.empty
            else ra_models,
            max_rows=50,
        ),
        "",
        "## IBD Adjusted Models",
        "",
        markdown_table(
            ibd_models.sort_values("response_p")[
                [
                    "gene",
                    "cell_state",
                    "endpoint",
                    "n",
                    "response_coef",
                    "response_p",
                    "response_fdr",
                    "generic_response_coef",
                    "target_generic_abs_ratio",
                    "model_status",
                ]
            ]
            if not ibd_models.empty
            else ibd_models,
            max_rows=60,
        ),
        "",
        "## Wave70B Integrated Scout Rows",
        "",
        markdown_table(w70b, max_rows=20),
        "",
        "## Wave70C Geneformer Direction Rows",
        "",
        markdown_table(w70c, max_rows=20),
        "",
        "## Interpretation",
        "",
        "A LILRB target can only be promoted if the target-level signal is not just",
        "myeloid abundance or generic inflammation. The hard blockers are absent MS",
        "anchor, inconsistent adjusted RA/IBD response specificity, no model-backed",
        "direction, and uncertainty over whether agonism or inhibition would improve",
        "the pathogenic state.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)

    broad_rows, broad_sum = broad_summary()
    ms = ms_rows()
    w62_summary, qtl_rows, qtl_summary = wave62_rows()
    ra_pairs, ra_models_raw = ra_pairs_and_models()
    ibd_pairs, ibd_models_raw = ibd_pairs_and_models()
    generic = generic_reference_coefficients(ra_pairs, ibd_pairs)
    ra_models = add_generic_ratios(ra_models_raw, generic)
    ibd_models = add_generic_ratios(ibd_models_raw, generic)
    conv = response_convergence(ra_models, ibd_models)
    w70b = rows_for_genes(W70B)
    w70c = rows_for_genes(W70C)
    w37 = rows_for_genes(W37)
    decision = integrated_decision(broad_sum, ms, w62_summary, qtl_summary, conv, w70b, w70c, w37)

    broad_rows.to_csv(OUT / "lilrb_broad_context_rows.tsv", sep="\t", index=False)
    broad_sum.to_csv(OUT / "lilrb_broad_gene_summary.tsv", sep="\t", index=False)
    ms.to_csv(OUT / "lilrb_ms_white_matter_rows.tsv", sep="\t", index=False)
    w62_summary.to_csv(OUT / "lilrb_wave62_summary_rows.tsv", sep="\t", index=False)
    qtl_rows.to_csv(OUT / "lilrb_qtl_coloc_rows.tsv", sep="\t", index=False)
    qtl_summary.to_csv(OUT / "lilrb_qtl_coloc_summary.tsv", sep="\t", index=False)
    ra_pairs.to_csv(OUT / "lilrb_ra_patient_pairs.tsv", sep="\t", index=False)
    ibd_pairs.to_csv(OUT / "lilrb_ibd_patient_pairs.tsv", sep="\t", index=False)
    generic.to_csv(OUT / "generic_reference_models.tsv", sep="\t", index=False)
    ra_models.to_csv(OUT / "lilrb_ra_adjusted_models.tsv", sep="\t", index=False)
    ibd_models.to_csv(OUT / "lilrb_ibd_adjusted_models.tsv", sep="\t", index=False)
    conv.to_csv(OUT / "lilrb_adjusted_response_convergence.tsv", sep="\t", index=False)
    w70b.to_csv(OUT / "lilrb_wave70b_rows.tsv", sep="\t", index=False)
    w70c.to_csv(OUT / "lilrb_wave70c_rows.tsv", sep="\t", index=False)
    w37.to_csv(OUT / "lilrb_wave37_rows.tsv", sep="\t", index=False)
    decision.to_csv(OUT / "lilrb_integrated_decision.tsv", sep="\t", index=False)

    summary = {
        "random_seed": SEED,
        "inputs": {
            "broad": rel(BROAD),
            "ms_signature": rel(MS_SIG),
            "wave62_summary": rel(W62),
            "wave62_qtl": rel(W62_QTL),
            "wave70b": rel(W70B),
            "wave70c": rel(W70C),
            "wave37": rel(W37),
            "ra_counts": rel(RA_COUNTS),
            "ra_meta": rel(RA_META),
            "ibd_h5ad_loader": "v3_wave68_gse282122_unrestricted_gene_screen.load_inputs",
            "ibd_pair_meta": rel(IBD_PAIR_META),
        },
        "targets": TARGET_GENES,
        "comparators": COMPARATOR_GENES,
        "decision": decision.replace({np.nan: None}).to_dict(orient="records"),
    }
    write_json(OUT / "summary.json", summary)
    write_report(decision, broad_sum, ms, qtl_summary, conv, ra_models, ibd_models, w70b, w70c)


if __name__ == "__main__":
    main()
