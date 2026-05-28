#!/usr/bin/env python3
"""Wave78 LILRB-family target-level audit.

This wave tests the least-broad inhibitory-receptor route left by Wave70/75:
LILRB-family myeloid receptors. The central question is not whether LILRB
genes mark inflammatory myeloid cells; they do. The stricter question is
whether any family member has enough target-level, directionally coherent,
MS-compatible, and receptor-specific evidence to become a V3 intervention
claim.
"""

from __future__ import annotations

import json
import math
import warnings
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats
from statsmodels.stats.multitest import multipletests

from v3_analyze_direct_h5ad_cell_states import ROOT


SEED = 20260527
OUT = ROOT / "results_v3" / "wave78_lilrb_family_target_audit"

LILRB_GENES = ["LILRB1", "LILRB2", "LILRB3", "LILRB4", "LILRB5"]
ACTIVATING_PARALOGS = ["LILRA1", "LILRA2", "LILRA3", "LILRA4", "LILRA5", "LILRA6"]
ADJACENT_INHIBITORY = ["LAIR1", "SIGLEC10", "CD300A", "CD300LF", "FCGR2B"]
CANDIDATE_GENES = LILRB_GENES + ACTIVATING_PARALOGS + ADJACENT_INHIBITORY

BROAD = ROOT / "results_v3" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_contrasts.tsv"
MS_SIG = ROOT / "results_v3" / "gse111972_full_ms_wm_signature.tsv"
W34 = ROOT / "results_v3" / "wave34_genetics_expression_druggability_scan" / "wave34_genetics_expression_druggability_rank.tsv"
W55 = ROOT / "results_v3" / "wave55_external_genetics_druggability_sweep" / "external_genetics_rank.tsv"
W62 = ROOT / "results_v3" / "wave62_opentargets_target_resolution" / "target_resolution_summary.tsv"
W68 = ROOT / "results_v3" / "wave68_gse282122_unrestricted_gene_screen" / "integrated_gene_target_rank.tsv"
W70C = ROOT / "results_v3" / "wave70c_inhibitory_receptor_geneformer_direction" / "geneformer_direction_candidate_calls.tsv"
RA_COUNTS = ROOT / "results_v3" / "wave65_gse198520_ra_synovium_antitnf_audit" / "gse198520_counts_used.tsv"
RA_META = ROOT / "results_v3" / "wave65_gse198520_ra_synovium_antitnf_audit" / "gse198520_sample_metadata.tsv"
RA_MODULES = ROOT / "results_v3" / "wave65_gse198520_ra_synovium_antitnf_audit" / "gse198520_module_scores.tsv"


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
    correction = 1.0 - 3.0 / (4.0 * (len(a) + len(b)) - 9.0)
    return float(((a.mean() - b.mean()) / math.sqrt(pooled)) * correction)


def zscore(series: pd.Series) -> pd.Series:
    sd = series.std(ddof=1)
    if not math.isfinite(sd) or sd == 0:
        return series * np.nan
    return (series - series.mean()) / sd


def load_broad() -> tuple[pd.DataFrame, pd.DataFrame]:
    df = read_tsv(BROAD)
    if df.empty:
        return pd.DataFrame(), pd.DataFrame()
    sub = df[df["gene"].astype(str).str.upper().isin(CANDIDATE_GENES)].copy()
    if sub.empty:
        return sub, pd.DataFrame()

    sub["route_class"] = np.select(
        [
            sub["gene"].isin(LILRB_GENES),
            sub["gene"].isin(ACTIVATING_PARALOGS),
            sub["gene"].isin(ADJACENT_INHIBITORY),
        ],
        ["LILRB_inhibitory", "LILRA_activating_paralog", "adjacent_inhibitory"],
        default="other",
    )
    sub["nominal_positive"] = (sub["delta_log2_cpm"] >= 0.35) & (sub["p"] <= 0.05)
    sub["nominal_negative"] = (sub["delta_log2_cpm"] <= -0.35) & (sub["p"] <= 0.05)

    ctx_cols = ["disease_name", "compartment"]
    activating_max = (
        sub[sub["gene"].isin(ACTIVATING_PARALOGS)]
        .groupby(ctx_cols, observed=True)["delta_log2_cpm"]
        .max()
        .rename("max_activating_paralog_delta")
        .reset_index()
    )
    sub = sub.merge(activating_max, on=ctx_cols, how="left")
    sub["beats_activating_paralog"] = (
        sub["gene"].isin(LILRB_GENES)
        & sub["nominal_positive"]
        & (
            sub["max_activating_paralog_delta"].isna()
            | (sub["delta_log2_cpm"] >= sub["max_activating_paralog_delta"] + 0.25)
        )
    )

    summary_rows = []
    for gene, gdf in sub.groupby("gene", observed=True):
        positive = gdf[gdf["nominal_positive"]]
        negative = gdf[gdf["nominal_negative"]]
        specific = gdf[gdf["beats_activating_paralog"]]
        best_idx = gdf["p"].astype(float).idxmin() if not gdf.empty else None
        summary_rows.append(
            {
                "gene": gene,
                "broad_tested_contexts": int(gdf.shape[0]),
                "broad_positive_contexts": int(positive.shape[0]),
                "broad_positive_disease_count": int(positive["disease_name"].nunique()),
                "broad_positive_diseases": ";".join(sorted(positive["disease_name"].dropna().astype(str).unique())),
                "broad_negative_contexts": int(negative.shape[0]),
                "broad_negative_disease_count": int(negative["disease_name"].nunique()),
                "broad_specific_positive_contexts": int(specific.shape[0]),
                "broad_specific_positive_disease_count": int(specific["disease_name"].nunique()),
                "best_broad_context": ""
                if best_idx is None
                else f"{gdf.loc[best_idx, 'disease_name']}|{gdf.loc[best_idx, 'compartment']}",
                "best_broad_delta": np.nan if best_idx is None else float(gdf.loc[best_idx, "delta_log2_cpm"]),
                "best_broad_p": np.nan if best_idx is None else float(gdf.loc[best_idx, "p"]),
                "best_broad_fdr": np.nan if best_idx is None else float(gdf.loc[best_idx, "fdr"]),
            }
        )
    summary = pd.DataFrame(summary_rows).sort_values(
        ["broad_positive_disease_count", "broad_specific_positive_disease_count", "best_broad_p"],
        ascending=[False, False, True],
    )
    return sub.sort_values(["gene", "p"]), summary


def ms_rows() -> pd.DataFrame:
    df = read_tsv(MS_SIG)
    if df.empty:
        return pd.DataFrame()
    sub = df[df["gene"].astype(str).str.upper().isin(CANDIDATE_GENES)].copy()
    sub["ms_wrong_for_suppression_route"] = (sub["delta_log2"] <= -0.35) & (sub["p"] <= 0.05)
    sub["ms_positive_for_suppression_route"] = (sub["delta_log2"] >= 0.35) & (sub["p"] <= 0.05)
    return sub.sort_values("p")


def ibd_response_rows() -> pd.DataFrame:
    df = read_tsv(W68)
    if df.empty:
        return pd.DataFrame()
    sub = df[df["gene"].astype(str).str.upper().isin(CANDIDATE_GENES)].copy()
    sub["ibd_suppression_response_support"] = (
        (sub["remission_adjusted_delta"] <= -0.30)
        & (sub["remission_adjusted_p"] <= 0.05)
        & (sub["remission_adjusted_fdr"] <= 0.10)
    )
    sub["ibd_restoration_response_support"] = (
        (sub["remission_adjusted_delta"] >= 0.30)
        & (sub["remission_adjusted_p"] <= 0.05)
        & (sub["remission_adjusted_fdr"] <= 0.10)
    )
    keep = [
        "gene",
        "cell_state",
        "remission_adjusted_delta",
        "remission_adjusted_p",
        "remission_adjusted_fdr",
        "wave68_call",
        "ibd_suppression_response_support",
        "ibd_restoration_response_support",
    ]
    return sub[[c for c in keep if c in sub.columns]].sort_values(
        ["ibd_suppression_response_support", "remission_adjusted_p"], ascending=[False, True]
    )


def ra_response_rows() -> pd.DataFrame:
    counts = read_tsv(RA_COUNTS)
    meta = read_tsv(RA_META)
    modules = read_tsv(RA_MODULES)
    if counts.empty or meta.empty or modules.empty:
        return pd.DataFrame()

    counts = counts.set_index("GeneSymbol")
    genes = [g for g in CANDIDATE_GENES if g in counts.index]
    if not genes:
        return pd.DataFrame()
    expr = log_cpm(counts.loc[genes].astype(float)).T.reset_index().rename(columns={"index": "count_column"})
    long = expr.merge(meta, on="count_column", how="left")
    generic = modules[modules["module"].eq("inflammatory_nfkb")][["count_column", "score"]].rename(
        columns={"score": "generic_nfkb_score"}
    )
    long = long.merge(generic, on="count_column", how="left")
    for col in ["inflammatory_score", "das28_score", "generic_nfkb_score"]:
        if col in long.columns:
            long[col] = numeric(long[col])

    rows: list[dict[str, Any]] = []
    for gene in genes:
        g = long[
            [
                "patient",
                "timepoint",
                "response_code",
                "responder_good_only",
                "responder_moderate_or_good",
                "pathotype",
                "biologic",
                "inflammatory_score",
                "das28_score",
                "generic_nfkb_score",
                gene,
            ]
        ].dropna(subset=["patient", "timepoint", gene])
        wide = g.pivot_table(index="patient", columns="timepoint", values=[gene, "generic_nfkb_score"], aggfunc="first")
        wide.columns = [f"{a}_{b}" for a, b in wide.columns]
        wide = wide.reset_index()
        pre_meta = g[g["timepoint"].eq("pre")].drop_duplicates("patient")
        pre_keep = [
            "patient",
            "response_code",
            "responder_good_only",
            "responder_moderate_or_good",
            "pathotype",
            "biologic",
            "inflammatory_score",
            "das28_score",
        ]
        wide = wide.merge(pre_meta[pre_keep], on="patient", how="left")
        pre_col = f"{gene}_pre"
        post_col = f"{gene}_post"
        if pre_col not in wide.columns or post_col not in wide.columns:
            continue
        wide["target_pre"] = zscore(wide[pre_col])
        wide["target_delta"] = zscore(wide[post_col] - wide[pre_col])
        wide["generic_pre"] = zscore(wide.get("generic_nfkb_score_pre", pd.Series(np.nan, index=wide.index)))
        wide["generic_delta"] = zscore(
            wide.get("generic_nfkb_score_post", pd.Series(np.nan, index=wide.index))
            - wide.get("generic_nfkb_score_pre", pd.Series(np.nan, index=wide.index))
        )
        wide["good_response"] = wide["response_code"].eq("r").astype(int)
        wide["moderate_good_response"] = wide["response_code"].isin(["r", "mr"]).astype(int)
        wide["baseline_inflammatory_score"] = numeric(wide["inflammatory_score"])
        wide["baseline_das28"] = numeric(wide["das28_score"])

        for endpoint, y_col, base_rhs in [
            (
                "delta_post_minus_pre",
                "target_delta",
                "response + target_pre + generic_delta + generic_pre + baseline_inflammatory_score + baseline_das28",
            ),
            ("baseline_pre", "target_pre", "response + generic_pre + baseline_inflammatory_score + baseline_das28"),
        ]:
            for comparison, response_col in [
                ("good_vs_moderate_none", "good_response"),
                ("moderate_good_vs_none", "moderate_good_response"),
            ]:
                model_df = wide.rename(columns={response_col: "response"}).dropna(
                    subset=[y_col, "response", "generic_pre", "baseline_inflammatory_score"]
                )
                if endpoint == "delta_post_minus_pre":
                    model_df = model_df.dropna(subset=["target_pre", "generic_delta"])
                y_sd = model_df[y_col].std(ddof=1)
                if model_df.shape[0] < 20 or model_df["response"].nunique() < 2:
                    coef, pval, status = np.nan, np.nan, "insufficient"
                elif not math.isfinite(y_sd) or y_sd < 1e-8:
                    coef, pval, status = np.nan, np.nan, "insufficient_target_variance"
                else:
                    try:
                        model = smf.ols(f"{y_col} ~ {base_rhs}", data=model_df).fit()
                        coef = float(model.params.get("response", np.nan))
                        pval = float(model.pvalues.get("response", np.nan))
                        status = "ok"
                    except Exception as exc:  # noqa: BLE001
                        coef, pval, status = np.nan, np.nan, f"fit_failed:{type(exc).__name__}:{exc}"
                good = model_df[model_df["response"].eq(1)][y_col].to_numpy(float)
                other = model_df[model_df["response"].eq(0)][y_col].to_numpy(float)
                if len(good) >= 3 and len(other) >= 3 and (np.nanstd(good, ddof=1) + np.nanstd(other, ddof=1)) >= 1e-8:
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore", RuntimeWarning)
                        _, raw_p = stats.ttest_ind(good, other, equal_var=False, nan_policy="omit")
                    raw_g = hedges_g(good, other)
                else:
                    raw_p, raw_g = np.nan, np.nan
                rows.append(
                    {
                        "gene": gene,
                        "dataset": "GSE198520_RA_synovium_antiTNF",
                        "endpoint": endpoint,
                        "comparison": comparison,
                        "n": int(model_df.shape[0]),
                        "response_coef": coef,
                        "response_p": pval,
                        "raw_hedges_g_response_minus_other": raw_g,
                        "raw_p": float(raw_p) if np.isfinite(raw_p) else np.nan,
                        "model_status": status,
                    }
                )

    out = pd.DataFrame(rows)
    if out.empty:
        return out
    out["response_fdr"] = bh(out["response_p"])
    out["ra_suppression_response_support"] = (
        out["endpoint"].eq("delta_post_minus_pre")
        & out["comparison"].eq("good_vs_moderate_none")
        & (out["response_coef"] <= -0.25)
        & (out["response_p"] <= 0.10)
    )
    out["ra_restoration_response_support"] = (
        out["endpoint"].eq("delta_post_minus_pre")
        & out["comparison"].eq("good_vs_moderate_none")
        & (out["response_coef"] >= 0.25)
        & (out["response_p"] <= 0.10)
    )
    return out.sort_values(["ra_suppression_response_support", "response_p"], ascending=[False, True])


def genetics_rows() -> pd.DataFrame:
    frames = []
    for label, path in [("wave34", W34), ("wave55", W55), ("wave62", W62)]:
        df = read_tsv(path)
        if df.empty or "gene" not in df.columns:
            continue
        sub = df[df["gene"].astype(str).str.upper().isin(CANDIDATE_GENES)].copy()
        if not sub.empty:
            sub.insert(0, "source", label)
            frames.append(sub)
    return pd.concat(frames, ignore_index=True, sort=False) if frames else pd.DataFrame()


def foundation_rows() -> pd.DataFrame:
    df = read_tsv(W70C)
    if df.empty:
        return pd.DataFrame()
    sub = df[df["gene"].astype(str).str.upper().isin(CANDIDATE_GENES)].copy()
    sub["foundation_suppression_support"] = sub["directional_interpretation"].astype(str).str.contains(
        "suppression_or_antagonism", na=False
    ) & (sub["support_contexts"].fillna(0) >= 2)
    sub["foundation_restoration_support"] = sub["directional_interpretation"].astype(str).str.contains(
        "restoration_or_agonism", na=False
    ) & (sub["opposing_contexts"].fillna(0) >= 1)
    return sub.sort_values("geneformer_direction_priority_score", ascending=False)


def build_candidate_matrix(
    broad_summary: pd.DataFrame,
    ms: pd.DataFrame,
    ibd: pd.DataFrame,
    ra: pd.DataFrame,
    genetics: pd.DataFrame,
    foundation: pd.DataFrame,
) -> pd.DataFrame:
    genes = sorted(set(LILRB_GENES + ADJACENT_INHIBITORY) & set(CANDIDATE_GENES))
    rows: list[dict[str, Any]] = []
    for gene in genes:
        b = broad_summary[broad_summary["gene"].eq(gene)]
        m = ms[ms["gene"].eq(gene)]
        i = ibd[ibd["gene"].eq(gene)]
        r = ra[ra["gene"].eq(gene)]
        g = genetics[genetics["gene"].eq(gene)] if not genetics.empty else pd.DataFrame()
        f = foundation[foundation["gene"].eq(gene)] if not foundation.empty else pd.DataFrame()

        best_ibd = i.sort_values("remission_adjusted_p").head(1) if not i.empty else pd.DataFrame()
        best_ra = r.sort_values("response_p").head(1) if not r.empty else pd.DataFrame()
        wave34 = g[g["source"].eq("wave34")].head(1) if not g.empty and "source" in g.columns else pd.DataFrame()
        wave55 = g[g["source"].eq("wave55")].head(1) if not g.empty and "source" in g.columns else pd.DataFrame()
        foundation_row = f.head(1)

        broad_positive_disease_count = int(b["broad_positive_disease_count"].iloc[0]) if not b.empty else 0
        broad_specific_positive_disease_count = (
            int(b["broad_specific_positive_disease_count"].iloc[0]) if not b.empty else 0
        )
        ms_wrong = bool(m["ms_wrong_for_suppression_route"].iloc[0]) if not m.empty else False
        ms_positive = bool(m["ms_positive_for_suppression_route"].iloc[0]) if not m.empty else False
        ms_delta = float(m["delta_log2"].iloc[0]) if not m.empty else np.nan
        ms_p = float(m["p"].iloc[0]) if not m.empty else np.nan
        ibd_suppression = bool(i["ibd_suppression_response_support"].any()) if not i.empty else False
        ibd_restoration = bool(i["ibd_restoration_response_support"].any()) if not i.empty else False
        ra_suppression = bool(r["ra_suppression_response_support"].any()) if not r.empty else False
        ra_restoration = bool(r["ra_restoration_response_support"].any()) if not r.empty else False
        foundation_suppression = (
            bool(f["foundation_suppression_support"].any()) if not f.empty and "foundation_suppression_support" in f else False
        )
        foundation_restoration = (
            bool(f["foundation_restoration_support"].any()) if not f.empty and "foundation_restoration_support" in f else False
        )

        genetic_disease_count = 0
        if not wave55.empty and "n_diseases_genetic_ge_0_25" in wave55.columns:
            genetic_disease_count = max(genetic_disease_count, int(float(wave55["n_diseases_genetic_ge_0_25"].fillna(0).iloc[0])))
        if not wave34.empty and "gwas_catalog_trait_count" in wave34.columns:
            genetic_disease_count = max(genetic_disease_count, int(float(wave34["gwas_catalog_trait_count"].fillna(0).iloc[0])))

        suppression_gate_count = sum(
            [
                broad_positive_disease_count >= 2,
                broad_specific_positive_disease_count >= 2,
                not ms_wrong,
                ibd_suppression,
                ra_suppression,
                foundation_suppression,
                genetic_disease_count >= 2,
            ]
        )
        restoration_gate_count = sum(
            [
                broad_positive_disease_count >= 2,
                broad_specific_positive_disease_count >= 2,
                bool(ms_positive or not ms_wrong),
                ibd_restoration,
                ra_restoration,
                foundation_restoration,
                genetic_disease_count >= 2,
            ]
        )

        if suppression_gate_count >= 6:
            call = "PARK_LILRB_SUPPRESSION_ROUTE_NEEDS_PRIOR_ART_AND_SAFETY"
        elif restoration_gate_count >= 6:
            call = "PARK_LILRB_RESTORATION_ROUTE_NEEDS_PRIOR_ART_AND_SAFETY"
        else:
            call = "NO_GO_LILRB_TARGET_LEVEL_CONVERGENCE"

        reason_bits = []
        if broad_positive_disease_count < 2:
            reason_bits.append("insufficient cross-disease expression breadth")
        if broad_specific_positive_disease_count < 2:
            reason_bits.append("LILRB signal does not beat LILRA/myeloid-family paralog specificity")
        if ms_wrong:
            reason_bits.append("MS white matter is nominally lower, opposite a suppression route")
        if not ibd_suppression and not ibd_restoration:
            reason_bits.append("IBD response direction insufficient or cell-state-limited")
        if not ra_suppression and not ra_restoration:
            reason_bits.append("RA response direction does not replicate")
        if not foundation_suppression and not foundation_restoration:
            reason_bits.append("foundation directionality does not support a clear route")
        if genetic_disease_count < 2:
            reason_bits.append("target-level genetic breadth absent")

        rows.append(
            {
                "gene": gene,
                "call": call,
                "suppression_gate_count": suppression_gate_count,
                "restoration_gate_count": restoration_gate_count,
                "broad_positive_disease_count": broad_positive_disease_count,
                "broad_positive_diseases": "" if b.empty else b["broad_positive_diseases"].iloc[0],
                "broad_specific_positive_disease_count": broad_specific_positive_disease_count,
                "ms_delta_log2": ms_delta,
                "ms_p": ms_p,
                "ms_wrong_for_suppression_route": ms_wrong,
                "ibd_best_cell_state": "" if best_ibd.empty else best_ibd["cell_state"].iloc[0],
                "ibd_best_adjusted_delta": np.nan
                if best_ibd.empty
                else float(best_ibd["remission_adjusted_delta"].iloc[0]),
                "ibd_best_adjusted_p": np.nan if best_ibd.empty else float(best_ibd["remission_adjusted_p"].iloc[0]),
                "ibd_best_adjusted_fdr": np.nan
                if best_ibd.empty
                else float(best_ibd["remission_adjusted_fdr"].iloc[0]),
                "ibd_suppression_support": ibd_suppression,
                "ibd_restoration_support": ibd_restoration,
                "ra_best_endpoint": "" if best_ra.empty else best_ra["endpoint"].iloc[0],
                "ra_best_comparison": "" if best_ra.empty else best_ra["comparison"].iloc[0],
                "ra_best_response_coef": np.nan if best_ra.empty else float(best_ra["response_coef"].iloc[0]),
                "ra_best_response_p": np.nan if best_ra.empty else float(best_ra["response_p"].iloc[0]),
                "ra_suppression_support": ra_suppression,
                "ra_restoration_support": ra_restoration,
                "foundation_priority": np.nan
                if foundation_row.empty
                else float(foundation_row["geneformer_direction_priority_score"].iloc[0]),
                "foundation_suppression_support": foundation_suppression,
                "foundation_restoration_support": foundation_restoration,
                "genetic_disease_count_proxy": genetic_disease_count,
                "wave34_call": "" if wave34.empty else str(wave34["wave34_call"].iloc[0]),
                "wave55_score": np.nan if wave55.empty else float(wave55["wave55_score"].iloc[0]),
                "decision_reason": "; ".join(reason_bits) if reason_bits else "all local gates pass pending prior-art scout",
            }
        )

    out = pd.DataFrame(rows)
    return out.sort_values(
        ["suppression_gate_count", "restoration_gate_count", "broad_positive_disease_count"],
        ascending=[False, False, False],
    )


def write_report(
    candidate_matrix: pd.DataFrame,
    broad_rows: pd.DataFrame,
    broad_summary: pd.DataFrame,
    ms: pd.DataFrame,
    ibd: pd.DataFrame,
    ra: pd.DataFrame,
    genetics: pd.DataFrame,
    foundation: pd.DataFrame,
) -> None:
    top_call = candidate_matrix["call"].iloc[0] if not candidate_matrix.empty else "NO_DATA"
    report = [
        "# Wave78 LILRB Family Target-Level Audit",
        "",
        "## Question",
        "",
        "Does any LILRB-family inhibitory myeloid receptor survive as a",
        "target-level, receptor-specific, MS-compatible intervention point after",
        "RA/IBD response, foundation-model directionality, and genetic breadth gates?",
        "",
        "## Verdict",
        "",
        top_call,
        "",
        "## Integrated Candidate Matrix",
        "",
        markdown_table(candidate_matrix, 20),
        "",
        "## Broad Cell-State Summary",
        "",
        markdown_table(broad_summary, 25),
        "",
        "## Top Broad Context Rows",
        "",
        markdown_table(broad_rows.sort_values(["p"]).head(35), 35),
        "",
        "## MS White-Matter Rows",
        "",
        markdown_table(ms, 25),
        "",
        "## IBD Anti-TNF Adjusted Response Rows",
        "",
        markdown_table(ibd, 35),
        "",
        "## RA Anti-TNF Direct Gene Response Rows",
        "",
        markdown_table(ra, 40),
        "",
        "## Foundation Directionality Rows",
        "",
        markdown_table(foundation, 25),
        "",
        "## Genetics/Druggability Rows",
        "",
        markdown_table(genetics, 35),
        "",
        "## Interpretation Guardrails",
        "",
        "- A positive LILRB disease-state signal is not enough; it must beat",
        "  activating LILRA paralogs in the same disease/compartment to avoid a",
        "  generic myeloid-abundance explanation.",
        "- For a suppression route, nominally lower MS white-matter expression is a",
        "  wrong-direction guardrail even if FDR is not genome-wide significant.",
        "- For an agonist/restoration route, remission-associated receptor decrease",
        "  in IBD and deletion-toward-remission foundation output are wrong-direction",
        "  evidence.",
        "- This script does not include the Wave78 prior-art sidecar; the local call",
        "  is therefore a biological convergence decision, not a final patent/trial",
        "  novelty decision.",
        "",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report), encoding="utf-8")


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)

    broad_rows, broad_summary = load_broad()
    ms = ms_rows()
    ibd = ibd_response_rows()
    ra = ra_response_rows()
    genetics = genetics_rows()
    foundation = foundation_rows()
    candidate_matrix = build_candidate_matrix(broad_summary, ms, ibd, ra, genetics, foundation)

    broad_rows.to_csv(OUT / "broad_family_context_rows.tsv", sep="\t", index=False)
    broad_summary.to_csv(OUT / "broad_family_summary.tsv", sep="\t", index=False)
    ms.to_csv(OUT / "ms_white_matter_family_rows.tsv", sep="\t", index=False)
    ibd.to_csv(OUT / "ibd_antitnf_adjusted_family_rows.tsv", sep="\t", index=False)
    ra.to_csv(OUT / "ra_antitnf_direct_gene_response_rows.tsv", sep="\t", index=False)
    genetics.to_csv(OUT / "genetics_druggability_family_rows.tsv", sep="\t", index=False)
    foundation.to_csv(OUT / "foundation_directionality_family_rows.tsv", sep="\t", index=False)
    candidate_matrix.to_csv(OUT / "lilrb_family_candidate_matrix.tsv", sep="\t", index=False)

    summary = {
        "seed": SEED,
        "candidate_genes": CANDIDATE_GENES,
        "top_call": candidate_matrix["call"].iloc[0] if not candidate_matrix.empty else "NO_DATA",
        "top_gene": candidate_matrix["gene"].iloc[0] if not candidate_matrix.empty else "",
        "inputs": {
            "broad": rel(BROAD),
            "ms_signature": rel(MS_SIG),
            "wave34": rel(W34),
            "wave55": rel(W55),
            "wave62": rel(W62),
            "wave68": rel(W68),
            "wave70c": rel(W70C),
            "ra_counts": rel(RA_COUNTS),
            "ra_meta": rel(RA_META),
            "ra_modules": rel(RA_MODULES),
        },
    }
    write_json(OUT / "summary.json", summary)
    write_report(candidate_matrix, broad_rows, broad_summary, ms, ibd, ra, genetics, foundation)


if __name__ == "__main__":
    main()
