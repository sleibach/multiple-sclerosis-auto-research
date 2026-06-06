#!/usr/bin/env python3
"""Wave75 ETS2 inflammatory macrophage program audit.

The branch asks whether the ETS2 macrophage/gene-desert axis is a promotable
cross-autoimmune intervention point, or whether local data only recapitulate a
published/generic inflammatory macrophage program.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "phases/v3/results" / "wave75_ets2_macrophage_program_audit"
SEED = 20260527

BROAD_SUMMARY = ROOT / "phases/v3/results" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_summary.tsv"
BROAD_CONTRASTS = ROOT / "phases/v3/results" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_contrasts.tsv"
MS_SIG = ROOT / "phases/v3/results" / "gse111972_full_ms_wm_signature.tsv"
WAVE62 = ROOT / "phases/v3/results" / "wave62_opentargets_target_resolution" / "target_resolution_summary.tsv"
WAVE55 = ROOT / "phases/v3/results" / "wave55_external_genetics_druggability_sweep" / "external_genetics_rank.tsv"
GSE282122_RAW = ROOT / "phases/v3/results" / "wave68_gse282122_unrestricted_gene_screen" / "raw_remission_response_gene_tests.tsv"
GSE282122_PAIRED = ROOT / "phases/v3/results" / "wave68_gse282122_unrestricted_gene_screen" / "paired_gene_delta_tests.tsv"
GSE282122_INTEGRATED = ROOT / "phases/v3/results" / "wave68_gse282122_unrestricted_gene_screen" / "integrated_gene_target_rank.tsv"
RA_COUNTS = ROOT / "phases/v3/results" / "wave65_gse198520_ra_synovium_antitnf_audit" / "gse198520_counts_used.tsv"
RA_META = ROOT / "phases/v3/results" / "wave65_gse198520_ra_synovium_antitnf_audit" / "gse198520_sample_metadata.tsv"
WAVE57 = ROOT / "phases/v3/results" / "wave57_intervention_first_geneformer_screen" / "wave57_geneformer_gene_summary.tsv"
WAVE69D = ROOT / "phases/v3/results" / "wave69d_gse282122_geneformer_remission_centroid" / "geneformer_remission_gene_summary.tsv"

TARGET = "ETS2"

MODULES: dict[str, list[str]] = {
    "ets2_direct": ["ETS2"],
    "ets2_macrophage_program": [
        "ETS2",
        "IL1B",
        "IL6",
        "TNF",
        "PTGS2",
        "CCL2",
        "CCL3",
        "CCL4",
        "CXCL8",
        "TNFAIP3",
        "NFKBIA",
        "ICAM1",
        "MMP9",
    ],
    "ap1_ets_immediate_early": ["ETS2", "FOS", "FOSB", "JUN", "JUNB", "JUND", "EGR1", "DUSP1", "DUSP2"],
    "generic_nfkb_tnf": ["TNF", "IL6", "CXCL8", "NFKBIA", "TNFAIP3", "CCL2", "CCL3", "CCL4", "IL1B"],
    "interferon_apc": ["STAT1", "IRF1", "CXCL10", "IFI30", "HLA-DRA", "HLA-DRB1", "CD74", "GBP1", "ISG15"],
    "lysosome_apc": ["IFI30", "CTSD", "CTSB", "CTSS", "CTSL", "LAMP1", "LAMP2", "TPP1", "CD74", "HLA-DRA"],
}

PROMOTION_MODULES = {"ets2_direct", "ets2_macrophage_program", "ap1_ets_immediate_early"}
COMPARATOR_MODULES = {"generic_nfkb_tnf", "interferon_apc", "lysosome_apc"}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def read_tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True) + "\n", encoding="utf-8")


def f(value: Any) -> float:
    try:
        out = float(value)
    except (TypeError, ValueError):
        return math.nan
    return out


def s(value: Any) -> str:
    if value is None or pd.isna(value):
        return ""
    return str(value)


def markdown_table(df: pd.DataFrame, max_rows: int = 20) -> str:
    if df.empty:
        return "_No rows._"
    view = df.head(max_rows).copy()
    cols = list(view.columns)
    lines = ["| " + " | ".join(cols) + " |", "| " + " | ".join(["---"] * len(cols)) + " |"]
    for _, row in view.iterrows():
        vals: list[str] = []
        for col in cols:
            val = row[col]
            if isinstance(val, (float, np.floating)):
                vals.append("" if math.isnan(float(val)) else f"{float(val):.4g}")
            else:
                vals.append(str(val).replace("|", "\\|"))
        lines.append("| " + " | ".join(vals) + " |")
    if len(df) > max_rows:
        lines.append(f"\n_Showing {max_rows} of {len(df)} rows._")
    return "\n".join(lines)


def signed_z(effect: float, p: float) -> float:
    if not math.isfinite(effect) or not math.isfinite(p) or p <= 0:
        return math.nan
    p = min(max(p, 1e-300), 1.0)
    return math.copysign(stats.norm.isf(p / 2.0), effect)


def combine_effects(rows: pd.DataFrame, gene_col: str, effect_col: str, p_col: str) -> dict[str, Any]:
    if rows.empty:
        return {
            "n_genes_present": 0,
            "genes_present": "",
            "mean_effect": math.nan,
            "median_effect": math.nan,
            "combined_z": math.nan,
            "combined_p": math.nan,
        }
    clean = rows.dropna(subset=[effect_col]).copy()
    if clean.empty:
        return {
            "n_genes_present": 0,
            "genes_present": "",
            "mean_effect": math.nan,
            "median_effect": math.nan,
            "combined_z": math.nan,
            "combined_p": math.nan,
        }
    clean["z"] = [signed_z(f(e), f(p)) for e, p in zip(clean[effect_col], clean[p_col])]
    zvals = clean["z"].replace([np.inf, -np.inf], np.nan).dropna().to_numpy(float)
    combined_z = float(np.nansum(zvals) / math.sqrt(len(zvals))) if len(zvals) else math.nan
    combined_p = float(2 * stats.norm.sf(abs(combined_z))) if math.isfinite(combined_z) else math.nan
    genes = sorted(set(clean[gene_col].astype(str)))
    return {
        "n_genes_present": int(len(genes)),
        "genes_present": ";".join(genes),
        "mean_effect": float(np.nanmean(clean[effect_col].astype(float))),
        "median_effect": float(np.nanmedian(clean[effect_col].astype(float))),
        "combined_z": combined_z,
        "combined_p": combined_p,
    }


def fdr_column(df: pd.DataFrame, p_col: str, out_col: str) -> pd.DataFrame:
    if df.empty:
        return df
    df[out_col] = multipletests(df[p_col].fillna(1.0), method="fdr_bh")[1]
    return df


def module_definitions() -> pd.DataFrame:
    rows = []
    for module, genes in MODULES.items():
        rows.append(
            {
                "module": module,
                "class": "candidate" if module in PROMOTION_MODULES else "specificity_comparator",
                "genes": ";".join(genes),
                "n_genes": len(genes),
            }
        )
    return pd.DataFrame(rows)


def direct_gene_evidence() -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    broad = read_tsv(BROAD_SUMMARY)
    if not broad.empty:
        hit = broad[broad["gene"].astype(str).eq(TARGET)]
        for _, row in hit.iterrows():
            rows.append(
                {
                    "source": "broad_h5ad_gene_summary",
                    "metric": "cross_disease_expression",
                    "effect": f(row.get("max_positive_delta_log2_cpm")),
                    "p": f(row.get("best_positive_p")),
                    "fdr": f(row.get("best_positive_fdr")),
                    "support": bool(f(row.get("positive_disease_count")) >= 2 and f(row.get("negative_disease_count")) == 0),
                    "details": f"positive_diseases={s(row.get('positive_diseases'))}; negative_diseases={s(row.get('negative_diseases'))}; fdr10_contexts={s(row.get('positive_fdr10_compartment_count'))}",
                }
            )
    ms = read_tsv(MS_SIG)
    if not ms.empty:
        hit = ms[ms["gene"].astype(str).eq(TARGET)]
        for _, row in hit.iterrows():
            rows.append(
                {
                    "source": "GSE111972_MS_white_matter",
                    "metric": "MS_case_minus_control_expression",
                    "effect": f(row.get("delta_log2")),
                    "p": f(row.get("p")),
                    "fdr": f(row.get("fdr")),
                    "support": bool(f(row.get("delta_log2")) >= 0.35 and f(row.get("p")) <= 0.05),
                    "details": "direct ETS2 in MS white matter signature",
                }
            )
    wave62 = read_tsv(WAVE62)
    if not wave62.empty:
        hit = wave62[wave62["gene"].astype(str).eq(TARGET)]
        for _, row in hit.iterrows():
            rows.append(
                {
                    "source": "wave62_opentargets_target_resolution",
                    "metric": "target_resolved_genetics",
                    "effect": f(row.get("wave62_score")),
                    "p": math.nan,
                    "fdr": math.nan,
                    "support": bool("NO_GO" not in s(row.get("wave62_call"))),
                    "details": f"call={s(row.get('wave62_call'))}; strong_l2g={s(row.get('strong_l2g_diseases'))}; relevant_qtl={s(row.get('relevant_qtl_coloc_diseases'))}; ms_l2g={s(row.get('ms_max_l2g_score'))}",
                }
            )
    wave55 = read_tsv(WAVE55)
    if not wave55.empty and "gene" in wave55.columns:
        hit = wave55[wave55["gene"].astype(str).eq(TARGET)]
        for _, row in hit.iterrows():
            rows.append(
                {
                    "source": "wave55_external_genetics",
                    "metric": "external_genetics_breadth",
                    "effect": f(row.get("wave55_score")),
                    "p": math.nan,
                    "fdr": math.nan,
                    "support": bool(f(row.get("genetic_disease_count_ge_0_25")) >= 4),
                    "details": "; ".join(f"{c}={s(row.get(c))}" for c in row.index if c in {"genetic_diseases_ge_0_25", "approved_name", "wave55_call"}),
                }
            )
    for path, source, score_col in [
        (WAVE57, "wave57_geneformer_intervention", "wave57_model_priority_score"),
        (WAVE69D, "wave69d_geneformer_remission_centroid", "geneformer_remission_priority_score"),
    ]:
        df = read_tsv(path)
        if not df.empty and "gene" in df.columns:
            hit = df[df["gene"].astype(str).eq(TARGET)]
            if not hit.empty:
                for _, row in hit.iterrows():
                    rows.append(
                        {
                            "source": source,
                            "metric": "foundation_model_perturbation",
                            "effect": f(row.get(score_col)),
                            "p": math.nan,
                            "fdr": math.nan,
                            "support": bool(f(row.get("strong_support_contexts")) >= 1 or f(row.get("support_contexts")) >= 2),
                            "details": f"support_contexts={s(row.get('support_contexts'))}; strong={s(row.get('strong_support_contexts'))}; best_context={s(row.get('best_context'))}",
                        }
                    )
            else:
                rows.append(
                    {
                        "source": source,
                        "metric": "foundation_model_perturbation",
                        "effect": math.nan,
                        "p": math.nan,
                        "fdr": math.nan,
                        "support": False,
                        "details": "ETS2 absent from output or below token/support threshold",
                    }
                )
    raw = read_tsv(GSE282122_RAW)
    if not raw.empty:
        for _, row in raw[raw["gene"].astype(str).eq(TARGET)].iterrows():
            rows.append(
                {
                    "source": f"GSE282122_raw_{s(row.get('cell_state'))}",
                    "metric": "IBD_antiTNF_remission_delta",
                    "effect": f(row.get("raw_delta_remission_minus_non")),
                    "p": f(row.get("raw_p")),
                    "fdr": f(row.get("raw_fdr")),
                    "support": bool(f(row.get("raw_delta_remission_minus_non")) <= -0.35 and f(row.get("raw_p")) <= 0.05),
                    "details": "negative effect means remission moves down relative to non-remission",
                }
            )
    paired = read_tsv(GSE282122_PAIRED)
    if not paired.empty:
        for _, row in paired[paired["gene"].astype(str).eq(TARGET)].iterrows():
            rows.append(
                {
                    "source": f"GSE282122_paired_{s(row.get('cell_state'))}",
                    "metric": "IBD_antiTNF_paired_post_minus_pre",
                    "effect": f(row.get("mean_delta")),
                    "p": f(row.get("paired_p")),
                    "fdr": f(row.get("paired_fdr")),
                    "support": bool(f(row.get("mean_delta")) <= -0.35 and f(row.get("paired_p")) <= 0.05),
                    "details": "negative effect means treatment pharmacodynamically lowers ETS2",
                }
            )
    integrated = read_tsv(GSE282122_INTEGRATED)
    if not integrated.empty and "gene" in integrated.columns:
        for _, row in integrated[integrated["gene"].astype(str).eq(TARGET)].iterrows():
            rows.append(
                {
                    "source": f"GSE282122_integrated_{s(row.get('state'))}",
                    "metric": "IBD_integrated_gene_rank",
                    "effect": f(row.get("integrated_score")),
                    "p": f(row.get("raw_fdr")),
                    "fdr": f(row.get("remission_adjusted_fdr")),
                    "support": bool(s(row.get("wave68_call")).startswith("PARK")),
                    "details": f"cell_state={s(row.get('cell_state'))}; call={s(row.get('wave68_call'))}; paired_fdr={s(row.get('paired_fdr'))}",
                }
            )
    return pd.DataFrame(rows)


def broad_module_contrasts() -> pd.DataFrame:
    df = read_tsv(BROAD_CONTRASTS)
    rows: list[dict[str, Any]] = []
    if df.empty:
        return pd.DataFrame(rows)
    for keys, sub in df.groupby(["analysis", "dataset_path", "disease_name", "compartment", "role"], dropna=False):
        for module, genes in MODULES.items():
            m = sub[sub["gene"].astype(str).isin(genes)]
            min_genes = 1 if module == "ets2_direct" else 3
            result = combine_effects(m, "gene", "delta_log2_cpm", "p")
            if result["n_genes_present"] < min_genes:
                continue
            rows.append(
                {
                    "analysis": keys[0],
                    "dataset_path": keys[1],
                    "disease_name": keys[2],
                    "compartment": keys[3],
                    "role": keys[4],
                    "module": module,
                    **result,
                }
            )
    out = pd.DataFrame(rows)
    if not out.empty:
        fdr_column(out, "combined_p", "fdr")
        out["positive_nominal"] = (out["mean_effect"] >= 0.35) & (out["combined_p"] <= 0.05)
        out["negative_nominal"] = (out["mean_effect"] <= -0.35) & (out["combined_p"] <= 0.05)
        out["positive_fdr10"] = (out["mean_effect"] >= 0.35) & (out["fdr"] <= 0.10)
        out["negative_fdr10"] = (out["mean_effect"] <= -0.35) & (out["fdr"] <= 0.10)
    return out


def module_summary(mods: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for module in MODULES:
        sub = mods[mods["module"].eq(module)] if not mods.empty else pd.DataFrame()
        pos = sub[sub.get("positive_nominal", False)] if not sub.empty else pd.DataFrame()
        neg = sub[sub.get("negative_nominal", False)] if not sub.empty else pd.DataFrame()
        fdrpos = sub[sub.get("positive_fdr10", False)] if not sub.empty else pd.DataFrame()
        rows.append(
            {
                "module": module,
                "module_class": "candidate" if module in PROMOTION_MODULES else "specificity_comparator",
                "tested_context_count": int(len(sub)),
                "positive_context_count": int(len(pos)),
                "negative_context_count": int(len(neg)),
                "positive_fdr10_context_count": int(len(fdrpos)),
                "positive_disease_count": int(pos["disease_name"].nunique()) if not pos.empty else 0,
                "negative_disease_count": int(neg["disease_name"].nunique()) if not neg.empty else 0,
                "positive_diseases": ";".join(sorted(map(str, pos["disease_name"].dropna().unique()))) if not pos.empty else "",
                "negative_diseases": ";".join(sorted(map(str, neg["disease_name"].dropna().unique()))) if not neg.empty else "",
                "best_positive_context": (
                    pos.sort_values("mean_effect", ascending=False)
                    .head(1)
                    .apply(lambda r: f"{r['analysis']}|{r['disease_name']}|{r['compartment']}|effect={r['mean_effect']:.3g}|p={r['combined_p']:.3g}|fdr={r['fdr']:.3g}", axis=1)
                    .iloc[0]
                    if not pos.empty
                    else ""
                ),
            }
        )
    return pd.DataFrame(rows)


def specificity_vs_comparators(mods: pd.DataFrame) -> pd.DataFrame:
    if mods.empty:
        return pd.DataFrame()
    pivot = mods.pivot_table(
        index=["analysis", "disease_name", "compartment", "role"],
        columns="module",
        values="mean_effect",
        aggfunc="first",
    ).reset_index()
    rows: list[dict[str, Any]] = []
    for _, row in pivot.iterrows():
        comparator_max = max([f(row.get(c)) for c in COMPARATOR_MODULES if math.isfinite(f(row.get(c)))] or [math.nan])
        for module in PROMOTION_MODULES:
            eff = f(row.get(module))
            if not math.isfinite(eff):
                continue
            rows.append(
                {
                    "analysis": row["analysis"],
                    "disease_name": row["disease_name"],
                    "compartment": row["compartment"],
                    "role": row["role"],
                    "candidate_module": module,
                    "candidate_effect": eff,
                    "max_generic_comparator_effect": comparator_max,
                    "specificity_margin": eff - comparator_max if math.isfinite(comparator_max) else math.nan,
                    "specificity_pass": bool(math.isfinite(comparator_max) and eff >= 0.35 and (eff - comparator_max) >= 0.25),
                }
            )
    return pd.DataFrame(rows)


def ms_module_tests() -> pd.DataFrame:
    df = read_tsv(MS_SIG)
    rows: list[dict[str, Any]] = []
    if df.empty:
        return pd.DataFrame(rows)
    for module, genes in MODULES.items():
        sub = df[df["gene"].astype(str).isin(genes)]
        result = combine_effects(sub, "gene", "delta_log2", "p")
        rows.append({"dataset": "GSE111972_MS_white_matter", "module": module, **result})
    out = pd.DataFrame(rows)
    if not out.empty:
        fdr_column(out, "combined_p", "fdr")
        out["support_call"] = np.where(
            (out["mean_effect"] >= 0.35) & (out["combined_p"] <= 0.05),
            "MS_NOMINAL_POSITIVE",
            "NO_MS_MODULE_SUPPORT",
        )
    return out


def gse282122_module_tests() -> pd.DataFrame:
    raw = read_tsv(GSE282122_RAW)
    paired = read_tsv(GSE282122_PAIRED)
    rows: list[dict[str, Any]] = []
    if not raw.empty:
        for cell_state, sub in raw.groupby("cell_state", dropna=False):
            for module, genes in MODULES.items():
                m = sub[sub["gene"].astype(str).isin(genes)]
                min_genes = 1 if module == "ets2_direct" else 3
                result = combine_effects(m, "gene", "raw_delta_remission_minus_non", "raw_p")
                if result["n_genes_present"] < min_genes:
                    continue
                rows.append(
                    {
                        "dataset": "GSE282122",
                        "test": "remission_delta_difference",
                        "cell_state": cell_state,
                        "module": module,
                        **result,
                        "expected_direction_support": bool(result["mean_effect"] <= -0.35 and result["combined_p"] <= 0.05),
                    }
                )
    if not paired.empty:
        for cell_state, sub in paired.groupby("cell_state", dropna=False):
            for module, genes in MODULES.items():
                m = sub[sub["gene"].astype(str).isin(genes)]
                min_genes = 1 if module == "ets2_direct" else 3
                result = combine_effects(m, "gene", "mean_delta", "paired_p")
                if result["n_genes_present"] < min_genes:
                    continue
                rows.append(
                    {
                        "dataset": "GSE282122",
                        "test": "paired_post_minus_pre_all",
                        "cell_state": cell_state,
                        "module": module,
                        **result,
                        "expected_direction_support": bool(result["mean_effect"] <= -0.35 and result["combined_p"] <= 0.05),
                    }
                )
    out = pd.DataFrame(rows)
    if not out.empty:
        fdr_column(out, "combined_p", "fdr")
    return out


def logcpm(counts: pd.DataFrame) -> pd.DataFrame:
    genes = counts["GeneSymbol"].astype(str)
    mat = counts.drop(columns=["GeneSymbol"]).astype(float)
    lib = mat.sum(axis=0).replace(0, np.nan)
    cpm = mat.div(lib, axis=1) * 1e6
    out = np.log2(cpm + 1)
    out.insert(0, "GeneSymbol", genes)
    return out


def ra_module_tests() -> tuple[pd.DataFrame, pd.DataFrame]:
    counts = read_tsv(RA_COUNTS)
    meta = read_tsv(RA_META)
    if counts.empty or meta.empty:
        return pd.DataFrame(), pd.DataFrame()
    expr = logcpm(counts)
    sample_cols = [c for c in expr.columns if c != "GeneSymbol"]
    sample_scores: list[dict[str, Any]] = []
    for module, genes in MODULES.items():
        sub = expr[expr["GeneSymbol"].astype(str).isin(genes)]
        min_genes = 1 if module == "ets2_direct" else 3
        present = sorted(set(sub["GeneSymbol"].astype(str)))
        if len(present) < min_genes:
            continue
        scores = sub[sample_cols].astype(float).mean(axis=0)
        for sample, score in scores.items():
            sample_scores.append(
                {
                    "count_column": sample,
                    "module": module,
                    "score": float(score),
                    "n_genes_present": len(present),
                    "genes_present": ";".join(present),
                }
            )
    score_df = pd.DataFrame(sample_scores).merge(meta, on="count_column", how="left")
    tests: list[dict[str, Any]] = []
    for module, sub in score_df.groupby("module"):
        wide = sub.pivot_table(index="patient", columns="timepoint", values="score", aggfunc="mean")
        pats = wide.dropna(subset=["pre", "post"]).index
        vals = wide.loc[pats, "post"] - wide.loc[pats, "pre"]
        t, p = stats.ttest_1samp(vals, 0.0, nan_policy="omit") if len(vals) >= 3 else (math.nan, math.nan)
        response = sub.drop_duplicates("patient").set_index("patient")
        rows = []
        for pat, delta in vals.items():
            rows.append(
                {
                    "patient": pat,
                    "module": module,
                    "delta_post_minus_pre": float(delta),
                    "response_class": response.loc[pat, "response_class"] if pat in response.index else "",
                    "responder_good_only": bool(response.loc[pat, "responder_good_only"]) if pat in response.index else False,
                    "responder_moderate_or_good": bool(response.loc[pat, "responder_moderate_or_good"]) if pat in response.index else False,
                }
            )
        delta_df = pd.DataFrame(rows)
        good = delta_df[delta_df["responder_good_only"]]["delta_post_minus_pre"].astype(float)
        other = delta_df[~delta_df["responder_good_only"]]["delta_post_minus_pre"].astype(float)
        go_t, go_p = stats.ttest_ind(good, other, equal_var=False, nan_policy="omit") if len(good) >= 3 and len(other) >= 3 else (math.nan, math.nan)
        mg = delta_df[delta_df["responder_moderate_or_good"]]["delta_post_minus_pre"].astype(float)
        none = delta_df[~delta_df["responder_moderate_or_good"]]["delta_post_minus_pre"].astype(float)
        mn_t, mn_p = stats.ttest_ind(mg, none, equal_var=False, nan_policy="omit") if len(mg) >= 3 and len(none) >= 3 else (math.nan, math.nan)
        tests.append(
            {
                "dataset": "GSE198520_RA_synovium_antiTNF",
                "module": module,
                "n_patients": int(len(vals)),
                "mean_post_minus_pre": float(np.nanmean(vals)) if len(vals) else math.nan,
                "paired_t": float(t) if math.isfinite(t) else math.nan,
                "paired_p": float(p) if math.isfinite(p) else math.nan,
                "good_vs_other_delta": float(np.nanmean(good) - np.nanmean(other)) if len(good) and len(other) else math.nan,
                "good_vs_other_p": float(go_p) if math.isfinite(go_p) else math.nan,
                "modgood_vs_none_delta": float(np.nanmean(mg) - np.nanmean(none)) if len(mg) and len(none) else math.nan,
                "modgood_vs_none_p": float(mn_p) if math.isfinite(mn_p) else math.nan,
                "expected_direction_support": bool(
                    len(good) >= 3
                    and len(other) >= 3
                    and math.isfinite(go_p)
                    and go_p <= 0.05
                    and (float(np.nanmean(good) - np.nanmean(other)) <= -0.35)
                ),
            }
        )
    test_df = pd.DataFrame(tests)
    if not test_df.empty:
        test_df["paired_fdr"] = multipletests(test_df["paired_p"].fillna(1.0), method="fdr_bh")[1]
        test_df["good_vs_other_fdr"] = multipletests(test_df["good_vs_other_p"].fillna(1.0), method="fdr_bh")[1]
        test_df["modgood_vs_none_fdr"] = multipletests(test_df["modgood_vs_none_p"].fillna(1.0), method="fdr_bh")[1]
    return score_df, test_df


def decision(
    direct: pd.DataFrame,
    broad_summary_df: pd.DataFrame,
    specificity: pd.DataFrame,
    ms: pd.DataFrame,
    gse282122: pd.DataFrame,
    ra_tests: pd.DataFrame,
) -> pd.DataFrame:
    broad_ets2 = broad_summary_df[broad_summary_df["module"].eq("ets2_direct")]
    broad_program = broad_summary_df[broad_summary_df["module"].eq("ets2_macrophage_program")]
    ms_candidate = ms[ms["module"].isin(PROMOTION_MODULES)] if not ms.empty else pd.DataFrame()
    gse_candidate = gse282122[gse282122["module"].isin(PROMOTION_MODULES)] if not gse282122.empty else pd.DataFrame()
    ra_candidate = ra_tests[ra_tests["module"].isin(PROMOTION_MODULES)] if not ra_tests.empty else pd.DataFrame()
    specificity_candidate = specificity[specificity["candidate_module"].isin(PROMOTION_MODULES)] if not specificity.empty else pd.DataFrame()

    target_sources = int(direct["support"].sum()) if not direct.empty else 0
    broad_direct_diseases = int(broad_ets2["positive_disease_count"].max()) if not broad_ets2.empty else 0
    broad_program_diseases = int(broad_program["positive_disease_count"].max()) if not broad_program.empty else 0
    specificity_pass = int(specificity_candidate["specificity_pass"].sum()) if not specificity_candidate.empty else 0
    ms_support = int(((ms_candidate["mean_effect"] >= 0.35) & (ms_candidate["combined_p"] <= 0.05)).sum()) if not ms_candidate.empty else 0
    ibd_response = int((gse_candidate["expected_direction_support"] & (gse_candidate["fdr"] <= 0.10)).sum()) if not gse_candidate.empty else 0
    ra_response = int((ra_candidate["expected_direction_support"] & (ra_candidate["good_vs_other_fdr"] <= 0.10)).sum()) if not ra_candidate.empty else 0
    genetics_support = int(
        any(
            direct["source"].eq("wave62_opentargets_target_resolution")
            & direct["support"].astype(bool)
        )
    ) if not direct.empty else 0
    foundation_support = int(
        any(
            direct["source"].isin(["wave57_geneformer_intervention", "wave69d_geneformer_remission_centroid"])
            & direct["support"].astype(bool)
        )
    ) if not direct.empty else 0

    gates = {
        "broad_direct_ets2_support": int(broad_direct_diseases >= 2),
        "broad_program_support": int(broad_program_diseases >= 3),
        "specificity_vs_generic_modules": int(specificity_pass >= 2),
        "ms_support": int(ms_support >= 1),
        "ibd_response_support": int(ibd_response >= 1),
        "ra_response_support": int(ra_response >= 1),
        "target_resolved_genetics": genetics_support,
        "foundation_model_support": foundation_support,
    }
    gate_count = int(sum(gates.values()))
    blockers = []
    if not gates["specificity_vs_generic_modules"]:
        blockers.append("ETS2-labeled program does not beat generic inflammatory/APC comparators")
    if not gates["ms_support"]:
        blockers.append("no MS white-matter ETS2/program support")
    if not gates["target_resolved_genetics"]:
        blockers.append("Wave62 target-resolution remains no-go")
    if not gates["ibd_response_support"] and not gates["ra_response_support"]:
        blockers.append("no replicated treatment-response support")
    if not gates["foundation_model_support"]:
        blockers.append("no Geneformer/foundation reopener")

    call = "NO_GO_ETS2_LOCAL_AUDIT"
    if gate_count >= 6 and gates["specificity_vs_generic_modules"] and gates["ms_support"] and gates["target_resolved_genetics"]:
        call = "PARK_ETS2_NEEDS_PRIOR_ART_AND_MODALITY"
    elif gates["broad_direct_ets2_support"] or gates["broad_program_support"]:
        call = "PARK_IBD_MYELOID_PROGRAM_NOT_PROMOTABLE"

    row = {
        "candidate": "ETS2_inflammatory_macrophage_program",
        "wave75_call": call,
        "gate_count": gate_count,
        **gates,
        "broad_direct_positive_disease_count": broad_direct_diseases,
        "broad_program_positive_disease_count": broad_program_diseases,
        "specificity_pass_context_count": specificity_pass,
        "target_support_source_count": target_sources,
        "decision_blockers": "; ".join(blockers),
    }
    return pd.DataFrame([row])


def write_report(
    decision_df: pd.DataFrame,
    direct: pd.DataFrame,
    module_defs: pd.DataFrame,
    broad_summary_df: pd.DataFrame,
    specificity: pd.DataFrame,
    ms: pd.DataFrame,
    gse282122: pd.DataFrame,
    ra_tests: pd.DataFrame,
) -> None:
    lines = [
        "# Wave75 ETS2 Inflammatory Macrophage Program Audit",
        "",
        "## Question",
        "",
        "Does local V3 evidence support `ETS2` as a promotable cross-autoimmune inflammatory macrophage intervention point rather than a generic/published inflammatory macrophage program?",
        "",
        "## Verdict",
        "",
        str(decision_df.iloc[0]["wave75_call"]),
        "",
        "## Integrated Decision",
        "",
        markdown_table(decision_df),
        "",
        "## Direct ETS2 Evidence",
        "",
        markdown_table(direct, 30),
        "",
        "## Module Definitions",
        "",
        markdown_table(module_defs),
        "",
        "## Broad h5ad Module Summary",
        "",
        markdown_table(broad_summary_df),
        "",
        "## Specificity Versus Generic Modules",
        "",
        markdown_table(specificity.sort_values("specificity_margin", ascending=False) if not specificity.empty else specificity, 20),
        "",
        "## MS White-Matter Module Tests",
        "",
        markdown_table(ms),
        "",
        "## IBD GSE282122 Anti-TNF Module Tests",
        "",
        markdown_table(gse282122.sort_values(["expected_direction_support", "fdr"], ascending=[False, True]) if not gse282122.empty else gse282122, 20),
        "",
        "## RA GSE198520 Anti-TNF Module Tests",
        "",
        markdown_table(ra_tests),
        "",
        "## Interpretation",
        "",
        "- ETS2 direct expression is strongest in IBD myeloid contexts, especially UC and Crohn myeloid compartments.",
        "- The ETS2-labeled macrophage program is intentionally compared against generic NF-kB/TNF, IFN/APC, and lysosomal/APC modules; specificity failure blocks promotion.",
        "- Direct ETS2 modulation remains a transcription-factor modality problem even before prior-art review.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)

    defs = module_definitions()
    direct = direct_gene_evidence()
    broad = broad_module_contrasts()
    broad_summary_df = module_summary(broad)
    specificity = specificity_vs_comparators(broad)
    ms = ms_module_tests()
    gse282122 = gse282122_module_tests()
    ra_scores, ra_tests = ra_module_tests()
    decision_df = decision(direct, broad_summary_df, specificity, ms, gse282122, ra_tests)

    defs.to_csv(OUT / "module_definitions.tsv", sep="\t", index=False)
    direct.to_csv(OUT / "direct_ets2_evidence.tsv", sep="\t", index=False)
    broad.to_csv(OUT / "broad_h5ad_module_contrasts.tsv", sep="\t", index=False)
    broad_summary_df.to_csv(OUT / "broad_h5ad_module_summary.tsv", sep="\t", index=False)
    specificity.to_csv(OUT / "specificity_vs_generic_modules.tsv", sep="\t", index=False)
    ms.to_csv(OUT / "ms_gse111972_module_tests.tsv", sep="\t", index=False)
    gse282122.to_csv(OUT / "gse282122_module_response_tests.tsv", sep="\t", index=False)
    ra_scores.to_csv(OUT / "ra_gse198520_module_scores.tsv", sep="\t", index=False)
    ra_tests.to_csv(OUT / "ra_gse198520_module_tests.tsv", sep="\t", index=False)
    decision_df.to_csv(OUT / "ets2_program_decision.tsv", sep="\t", index=False)
    write_json(
        OUT / "summary.json",
        {
            "random_seed": SEED,
            "inputs": {
                "broad_summary": rel(BROAD_SUMMARY),
                "broad_contrasts": rel(BROAD_CONTRASTS),
                "ms_signature": rel(MS_SIG),
                "wave62": rel(WAVE62),
                "wave55": rel(WAVE55),
                "gse282122_raw": rel(GSE282122_RAW),
                "gse282122_paired": rel(GSE282122_PAIRED),
                "gse282122_integrated": rel(GSE282122_INTEGRATED),
                "ra_counts": rel(RA_COUNTS),
                "ra_meta": rel(RA_META),
                "wave57": rel(WAVE57),
                "wave69d": rel(WAVE69D),
            },
            "decision": decision_df.iloc[0].to_dict(),
        },
    )
    write_report(decision_df, direct, defs, broad_summary_df, specificity, ms, gse282122, ra_tests)


if __name__ == "__main__":
    main()
