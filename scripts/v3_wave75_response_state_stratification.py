#!/usr/bin/env python3
"""Wave75 response-state stratification audit.

Question:
Does the recurrent IFN/APC plus lysosomal/APC state predict treatment response
across independent autoimmune anti-TNF datasets, beyond generic inflammatory
module movement?

This is a biomarker/intervention-point gate, not a finding generator. A claim
requires directionally stable response association in RA synovium and IBD
myeloid/DC data after generic-inflammation residualization.
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

from v3_analyze_direct_h5ad_cell_states import MODULES as BASE_MODULES
from v3_analyze_direct_h5ad_cell_states import ROOT
from v3_wave68_gse282122_unrestricted_gene_screen import (
    aggregate_all_genes,
    build_primary_obs,
    load_inputs,
    logcpm as ibd_logcpm,
)


SEED = 20260527
OUT = ROOT / "phases/v3/results" / "wave75_response_state_stratification"

RA_COUNTS = ROOT / "phases/v3/results" / "wave65_gse198520_ra_synovium_antitnf_audit" / "gse198520_counts_used.tsv"
RA_META = ROOT / "phases/v3/results" / "wave65_gse198520_ra_synovium_antitnf_audit" / "gse198520_sample_metadata.tsv"
IBD_PAIR_META = ROOT / "phases/v3/results" / "wave68_gse282122_unrestricted_gene_screen" / "all_gene_pair_metadata.tsv"

MODULES: dict[str, list[str]] = {
    "ifn_apc": BASE_MODULES["ifn_apc"],
    "hla_ii_apc": BASE_MODULES["hla_ii_apc"],
    "lysosomal_apc": BASE_MODULES["lysosomal_apc"],
    "mif_cd74_receptor_state": BASE_MODULES["mif_cd74_receptor_state"],
    "lipid_loader_repair": BASE_MODULES["lipid_loader_repair"],
    "inflammatory_nfkb": BASE_MODULES["inflammatory_nfkb"],
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


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


def log_cpm(counts: pd.DataFrame) -> pd.DataFrame:
    lib = counts.sum(axis=0).replace(0, np.nan)
    return np.log2(counts.div(lib, axis=1) * 1_000_000.0 + 1.0)


def zscore_rows(expr: pd.DataFrame) -> pd.DataFrame:
    mean = expr.mean(axis=1)
    sd = expr.std(axis=1, ddof=1).replace(0, np.nan)
    return expr.sub(mean, axis=0).div(sd, axis=0).replace([np.inf, -np.inf], np.nan)


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


def module_score_wide(expr: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    z = zscore_rows(expr)
    score_rows = {}
    gene_rows = []
    for module, genes in MODULES.items():
        present = [gene for gene in genes if gene in z.index]
        gene_rows.append(
            {
                "module": module,
                "n_defined": len(genes),
                "n_present": len(present),
                "genes_present": ";".join(present),
                "genes_missing": ";".join([g for g in genes if g not in z.index]),
            }
        )
        if present:
            score_rows[module] = z.loc[present].mean(axis=0, skipna=True)
    scores = pd.DataFrame(score_rows)
    scores["ifn_lysosomal_apc_composite"] = scores[["ifn_apc", "lysosomal_apc"]].mean(axis=1)
    return scores, pd.DataFrame(gene_rows)


def add_residual_scores(scores: pd.DataFrame) -> pd.DataFrame:
    out = scores.copy()
    if "inflammatory_nfkb" in scores.columns:
        x = scores[["inflammatory_nfkb"]].copy()
        x.insert(0, "intercept", 1.0)
        for module in [
            "ifn_apc",
            "hla_ii_apc",
            "lysosomal_apc",
            "mif_cd74_receptor_state",
            "lipid_loader_repair",
            "ifn_lysosomal_apc_composite",
        ]:
            if module not in scores.columns:
                continue
            joined = pd.concat([scores[module], x], axis=1).dropna()
            if joined.shape[0] < 6:
                continue
            y = joined[module].to_numpy(float)
            X = joined[["intercept", "inflammatory_nfkb"]].to_numpy(float)
            beta = np.linalg.lstsq(X, y, rcond=None)[0]
            pred = x.to_numpy(float) @ beta
            out[f"{module}__resid_inflammatory_nfkb"] = scores[module] - pred
    if {"ifn_apc", "inflammatory_nfkb"}.issubset(scores.columns):
        x2 = scores[["ifn_apc", "inflammatory_nfkb"]].copy()
        x2.insert(0, "intercept", 1.0)
        for module in ["lysosomal_apc", "hla_ii_apc", "mif_cd74_receptor_state", "lipid_loader_repair"]:
            if module not in scores.columns:
                continue
            joined = pd.concat([scores[module], x2], axis=1).dropna()
            if joined.shape[0] < 6:
                continue
            y = joined[module].to_numpy(float)
            X = joined[["intercept", "ifn_apc", "inflammatory_nfkb"]].to_numpy(float)
            beta = np.linalg.lstsq(X, y, rcond=None)[0]
            pred = x2.to_numpy(float) @ beta
            out[f"{module}__resid_ifn_apc_inflammatory_nfkb"] = scores[module] - pred
    return out


def two_group_test(a: np.ndarray, b: np.ndarray) -> dict[str, Any]:
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    a = a[np.isfinite(a)]
    b = b[np.isfinite(b)]
    if len(a) >= 3 and len(b) >= 3:
        t_stat, p_value = stats.ttest_ind(a, b, equal_var=False, nan_policy="omit")
    else:
        t_stat, p_value = np.nan, np.nan
    return {
        "n_group_a": int(len(a)),
        "n_group_b": int(len(b)),
        "mean_group_a": float(np.nanmean(a)) if len(a) else np.nan,
        "mean_group_b": float(np.nanmean(b)) if len(b) else np.nan,
        "effect_group_a_minus_b": hedges_g(a, b),
        "t": float(t_stat) if np.isfinite(t_stat) else np.nan,
        "p": float(p_value) if np.isfinite(p_value) else np.nan,
    }


def paired_test(values: np.ndarray) -> dict[str, Any]:
    values = np.asarray(values, dtype=float)
    values = values[np.isfinite(values)]
    if len(values) >= 3:
        t_stat, p_value = stats.ttest_1samp(values, 0.0, nan_policy="omit")
    else:
        t_stat, p_value = np.nan, np.nan
    return {
        "n_pairs": int(len(values)),
        "mean_delta": float(np.nanmean(values)) if len(values) else np.nan,
        "median_delta": float(np.nanmedian(values)) if len(values) else np.nan,
        "paired_t": float(t_stat) if np.isfinite(t_stat) else np.nan,
        "paired_p": float(p_value) if np.isfinite(p_value) else np.nan,
    }


def spearman_test(x: np.ndarray, y: np.ndarray) -> dict[str, Any]:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    mask = np.isfinite(x) & np.isfinite(y)
    if mask.sum() >= 6 and len(np.unique(x[mask])) > 2 and len(np.unique(y[mask])) > 2:
        rho, p_value = stats.spearmanr(x[mask], y[mask])
    else:
        rho, p_value = np.nan, np.nan
    return {"n_corr": int(mask.sum()), "spearman_rho": float(rho) if np.isfinite(rho) else np.nan, "spearman_p": float(p_value) if np.isfinite(p_value) else np.nan}


def ra_tables() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    counts = pd.read_csv(RA_COUNTS, sep="\t").set_index("GeneSymbol")
    counts.index = counts.index.astype(str).str.upper()
    meta = pd.read_csv(RA_META, sep="\t")
    expr = log_cpm(counts.astype(float))
    scores, genes = module_score_wide(expr)
    scores = add_residual_scores(scores)

    sample_scores = meta[["count_column", "patient", "response_code", "response_class", "timepoint", "pathotype", "delta_das28"]].copy()
    for col in scores.columns:
        sample_scores[col] = sample_scores["count_column"].map(scores[col].to_dict())

    rows = []
    for patient, sub in sample_scores.groupby("patient", observed=True):
        pre = sub[sub["timepoint"].eq("pre")]
        post = sub[sub["timepoint"].eq("post")]
        if len(pre) != 1 or len(post) != 1:
            continue
        p = pre.iloc[0]
        q = post.iloc[0]
        for module in scores.columns:
            rows.append(
                {
                    "dataset": "GSE198520_RA_synovium_antiTNF",
                    "patient": patient,
                    "response_code": p["response_code"],
                    "response_class": p["response_class"],
                    "responder_good_only": p["response_code"] == "r",
                    "responder_moderate_or_good": p["response_code"] in {"r", "mr"},
                    "pathotype": p.get("pathotype", ""),
                    "delta_das28": pd.to_numeric(p.get("delta_das28"), errors="coerce"),
                    "module": module,
                    "pre_score": float(p[module]),
                    "post_score": float(q[module]),
                    "post_minus_pre": float(q[module] - p[module]),
                }
            )
    paired = pd.DataFrame(rows)
    return sample_scores, paired, genes.assign(dataset="GSE198520_RA_synovium_antiTNF")


def ra_tests(paired: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for module, sub in paired.groupby("module", observed=True):
        for endpoint, value_col in [("baseline_pre", "pre_score"), ("delta_post_minus_pre", "post_minus_pre")]:
            good = sub.loc[sub["responder_good_only"], value_col].to_numpy(float)
            other = sub.loc[~sub["responder_good_only"], value_col].to_numpy(float)
            res = two_group_test(good, other)
            rows.append(
                {
                    "dataset": "GSE198520_RA_synovium_antiTNF",
                    "cell_state": "bulk_synovium",
                    "endpoint": endpoint,
                    "comparison": "good_vs_moderate_none",
                    "module": module,
                    **res,
                }
            )
            mg = sub.loc[sub["responder_moderate_or_good"], value_col].to_numpy(float)
            none = sub.loc[~sub["responder_moderate_or_good"], value_col].to_numpy(float)
            res = two_group_test(mg, none)
            rows.append(
                {
                    "dataset": "GSE198520_RA_synovium_antiTNF",
                    "cell_state": "bulk_synovium",
                    "endpoint": endpoint,
                    "comparison": "moderate_good_vs_none",
                    "module": module,
                    **res,
                }
            )
            corr = spearman_test(sub[value_col].to_numpy(float), pd.to_numeric(sub["delta_das28"], errors="coerce").to_numpy(float))
            rows.append(
                {
                    "dataset": "GSE198520_RA_synovium_antiTNF",
                    "cell_state": "bulk_synovium",
                    "endpoint": endpoint,
                    "comparison": "spearman_vs_delta_das28",
                    "module": module,
                    "n_group_a": corr["n_corr"],
                    "n_group_b": 0,
                    "mean_group_a": np.nan,
                    "mean_group_b": np.nan,
                    "effect_group_a_minus_b": corr["spearman_rho"],
                    "t": np.nan,
                    "p": corr["spearman_p"],
                }
            )
        for scope, scope_df in [
            ("all_patients", sub),
            ("good_responders", sub[sub["responder_good_only"]]),
            ("moderate_good_responders", sub[sub["responder_moderate_or_good"]]),
            ("nonresponders", sub[~sub["responder_moderate_or_good"]]),
        ]:
            res = paired_test(scope_df["post_minus_pre"].to_numpy(float))
            rows.append(
                {
                    "dataset": "GSE198520_RA_synovium_antiTNF",
                    "cell_state": "bulk_synovium",
                    "endpoint": "paired_change",
                    "comparison": scope,
                    "module": module,
                    "n_group_a": res["n_pairs"],
                    "n_group_b": 0,
                    "mean_group_a": res["mean_delta"],
                    "mean_group_b": 0.0,
                    "effect_group_a_minus_b": res["mean_delta"],
                    "t": res["paired_t"],
                    "p": res["paired_p"],
                }
            )
    out = pd.DataFrame(rows)
    out["fdr"] = bh(out["p"])
    return out


def ibd_scores_and_pairs() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    adata, paired_samples, obs = load_inputs()
    primary_obs = build_primary_obs(obs, paired_samples)
    meta, counts = aggregate_all_genes(adata, primary_obs)
    expr = ibd_logcpm(meta, counts).T
    scores, genes = module_score_wide(expr)
    scores = add_residual_scores(scores)
    sample_scores = meta.copy()
    for col in scores.columns:
        sample_scores[col] = scores[col].to_numpy(float)

    pair_meta = pd.read_csv(IBD_PAIR_META, sep="\t")
    pair_meta = pair_meta[pair_meta["passes_cell_threshold"].astype(bool)].copy()
    key_cols = ["sample_id", "cell_state"]
    score_by_key = sample_scores.set_index(key_cols)
    rows = []
    for _, pair in pair_meta.iterrows():
        pre_key = (pair["pre_sample_id"], pair["cell_state"])
        post_key = (pair["post_sample_id"], pair["cell_state"])
        if pre_key not in score_by_key.index or post_key not in score_by_key.index:
            continue
        p = score_by_key.loc[pre_key]
        q = score_by_key.loc[post_key]
        # loc can return a frame if keys duplicate; the aggregation should not,
        # but take the first row defensively.
        if isinstance(p, pd.DataFrame):
            p = p.iloc[0]
        if isinstance(q, pd.DataFrame):
            q = q.iloc[0]
        for module in scores.columns:
            rows.append(
                {
                    "dataset": "GSE282122_IBD_myeloid_antiTNF",
                    "Patient": pair["Patient"],
                    "Disease": pair["Disease"],
                    "Site": pair["Site"],
                    "Remission_status": pair["Remission_status"],
                    "cell_state": pair["cell_state"],
                    "baseline_inflammation_score": pair["baseline_inflammation_score"],
                    "post_inflammation_score": pair["post_inflammation_score"],
                    "module": module,
                    "pre_score": float(p[module]),
                    "post_score": float(q[module]),
                    "post_minus_pre": float(q[module] - p[module]),
                }
            )
    site_pairs = pd.DataFrame(rows)
    collapsed_rows = []
    for keys, sub in site_pairs.groupby(["Patient", "Disease", "Remission_status", "cell_state", "module"], observed=True):
        collapsed_rows.append(
            {
                "dataset": "GSE282122_IBD_myeloid_antiTNF",
                "Patient": keys[0],
                "Disease": keys[1],
                "Remission_status": keys[2],
                "cell_state": keys[3],
                "module": keys[4],
                "n_sites": int(sub["Site"].nunique()),
                "baseline_inflammation_score": float(sub["baseline_inflammation_score"].mean()),
                "pre_score": float(sub["pre_score"].mean()),
                "post_score": float(sub["post_score"].mean()),
                "post_minus_pre": float(sub["post_minus_pre"].mean()),
            }
        )
    patient_pairs = pd.DataFrame(collapsed_rows)
    return sample_scores, patient_pairs, genes.assign(dataset="GSE282122_IBD_myeloid_antiTNF")


def ibd_tests(patient_pairs: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (cell_state, module), sub in patient_pairs.groupby(["cell_state", "module"], observed=True):
        for endpoint, value_col in [("baseline_pre", "pre_score"), ("delta_post_minus_pre", "post_minus_pre")]:
            rem = sub.loc[sub["Remission_status"].eq("Remission"), value_col].to_numpy(float)
            non = sub.loc[sub["Remission_status"].eq("Non_Remission"), value_col].to_numpy(float)
            res = two_group_test(rem, non)
            rows.append(
                {
                    "dataset": "GSE282122_IBD_myeloid_antiTNF",
                    "cell_state": cell_state,
                    "endpoint": endpoint,
                    "comparison": "remission_vs_nonremission",
                    "module": module,
                    **res,
                }
            )
        for scope, scope_df in [
            ("all_patients", sub),
            ("remission", sub[sub["Remission_status"].eq("Remission")]),
            ("nonremission", sub[sub["Remission_status"].eq("Non_Remission")]),
        ]:
            res = paired_test(scope_df["post_minus_pre"].to_numpy(float))
            rows.append(
                {
                    "dataset": "GSE282122_IBD_myeloid_antiTNF",
                    "cell_state": cell_state,
                    "endpoint": "paired_change",
                    "comparison": scope,
                    "module": module,
                    "n_group_a": res["n_pairs"],
                    "n_group_b": 0,
                    "mean_group_a": res["mean_delta"],
                    "mean_group_b": 0.0,
                    "effect_group_a_minus_b": res["mean_delta"],
                    "t": res["paired_t"],
                    "p": res["paired_p"],
                }
            )
    out = pd.DataFrame(rows)
    out["fdr"] = bh(out["p"])
    return out


def convergence(ra: pd.DataFrame, ibd: pd.DataFrame) -> pd.DataFrame:
    ra_focus = ra[
        ra["comparison"].isin(["good_vs_moderate_none", "moderate_good_vs_none"])
        & ra["endpoint"].isin(["baseline_pre", "delta_post_minus_pre"])
    ].copy()
    ibd_focus = ibd[
        ibd["comparison"].eq("remission_vs_nonremission")
        & ibd["endpoint"].isin(["baseline_pre", "delta_post_minus_pre"])
    ].copy()
    rows = []
    for module in sorted(set(ra_focus["module"]) & set(ibd_focus["module"])):
        for endpoint in ["baseline_pre", "delta_post_minus_pre"]:
            rsub = ra_focus[(ra_focus["module"].eq(module)) & (ra_focus["endpoint"].eq(endpoint))]
            isub = ibd_focus[(ibd_focus["module"].eq(module)) & (ibd_focus["endpoint"].eq(endpoint))]
            if rsub.empty or isub.empty:
                continue
            # Choose the strongest RA response comparison and strongest IBD cell
            # state by nominal p, then check direction stability.
            rbest = rsub.sort_values("p").iloc[0]
            ibest = isub.sort_values("p").iloc[0]
            r_eff = float(rbest["effect_group_a_minus_b"])
            i_eff = float(ibest["effect_group_a_minus_b"])
            direction_stable = math.isfinite(r_eff) and math.isfinite(i_eff) and np.sign(r_eff) == np.sign(i_eff)
            rows.append(
                {
                    "module": module,
                    "endpoint": endpoint,
                    "ra_best_comparison": rbest["comparison"],
                    "ra_effect": r_eff,
                    "ra_p": float(rbest["p"]),
                    "ra_fdr": float(rbest["fdr"]),
                    "ibd_best_cell_state": ibest["cell_state"],
                    "ibd_effect": i_eff,
                    "ibd_p": float(ibest["p"]),
                    "ibd_fdr": float(ibest["fdr"]),
                    "direction_stable": bool(direction_stable),
                    "both_nominal_p10": bool(direction_stable and rbest["p"] <= 0.10 and ibest["p"] <= 0.10),
                    "one_nominal_other_trend": bool(direction_stable and min(rbest["p"], ibest["p"]) <= 0.05 and max(rbest["p"], ibest["p"]) <= 0.20),
                }
            )
    out = pd.DataFrame(rows)
    if not out.empty:
        out["priority"] = (
            3 * out["both_nominal_p10"].astype(int)
            + 2 * out["one_nominal_other_trend"].astype(int)
            + out["direction_stable"].astype(int)
            + out["module"].str.contains("ifn|lysosomal|hla", regex=True).astype(int)
        )
        out = out.sort_values(["priority", "ra_p", "ibd_p"], ascending=[False, True, True])
    return out


def make_decision(conv: pd.DataFrame) -> pd.DataFrame:
    if conv.empty:
        call = "NO_GO_RESPONSE_STRATIFICATION_NO_COMPARABLE_TESTS"
        reason = "no comparable RA and IBD response tests"
        best = {}
    else:
        best_row = conv.iloc[0].to_dict()
        best = best_row
        if bool(best_row.get("both_nominal_p10")):
            call = "REOPEN_RESPONSE_STRATIFICATION"
            reason = "RA and IBD response associations are directionally stable and nominal in both datasets"
        elif bool(best_row.get("one_nominal_other_trend")):
            call = "PARK_RESPONSE_STRATIFICATION_TREND_ONLY"
            reason = "cross-dataset direction is stable but one dataset is only a trend"
        elif bool(best_row.get("direction_stable")):
            call = "PARK_RESPONSE_STRATIFICATION_DIRECTION_ONLY"
            reason = "direction is stable for at least one module but statistical support is weak"
        else:
            call = "NO_GO_RESPONSE_STRATIFICATION_NOT_REPLICATED"
            reason = "available RA and IBD response datasets do not support a stable module-response association"
    return pd.DataFrame(
        [
            {
                "candidate": "IFN_APC_lysosomal_APC_response_stratification",
                "wave75_call": call,
                "decision_reason": reason,
                "best_module": best.get("module", ""),
                "best_endpoint": best.get("endpoint", ""),
                "ra_effect": best.get("ra_effect", np.nan),
                "ra_p": best.get("ra_p", np.nan),
                "ibd_effect": best.get("ibd_effect", np.nan),
                "ibd_p": best.get("ibd_p", np.nan),
                "direction_stable": best.get("direction_stable", False),
                "both_nominal_p10": best.get("both_nominal_p10", False),
                "one_nominal_other_trend": best.get("one_nominal_other_trend", False),
            }
        ]
    )


def write_report(decision: pd.DataFrame, conv: pd.DataFrame, ra_tests_df: pd.DataFrame, ibd_tests_df: pd.DataFrame, genes: pd.DataFrame) -> None:
    lines = [
        "# Wave75 Response-State Stratification Audit",
        "",
        "## Question",
        "",
        "Does the recurrent IFN/APC plus lysosomal/APC state predict anti-TNF",
        "response across RA synovium and IBD myeloid/DC datasets better than a",
        "generic inflammatory module?",
        "",
        "## Verdict",
        "",
        str(decision.iloc[0]["wave75_call"]),
        "",
        "## Integrated Decision",
        "",
        markdown_table(decision),
        "",
        "## Cross-Dataset Convergence",
        "",
        markdown_table(conv, max_rows=40),
        "",
        "## RA Response Tests",
        "",
        markdown_table(
            ra_tests_df.sort_values("p")[
                [
                    "dataset",
                    "cell_state",
                    "endpoint",
                    "comparison",
                    "module",
                    "n_group_a",
                    "n_group_b",
                    "effect_group_a_minus_b",
                    "p",
                    "fdr",
                ]
            ],
            max_rows=50,
        ),
        "",
        "## IBD Response Tests",
        "",
        markdown_table(
            ibd_tests_df.sort_values("p")[
                [
                    "dataset",
                    "cell_state",
                    "endpoint",
                    "comparison",
                    "module",
                    "n_group_a",
                    "n_group_b",
                    "effect_group_a_minus_b",
                    "p",
                    "fdr",
                ]
            ],
            max_rows=60,
        ),
        "",
        "## Module Gene Coverage",
        "",
        markdown_table(genes, max_rows=80),
        "",
        "## Interpretation Guardrails",
        "",
        "- RA GSE198520 is bulk synovium, not cell-resolved myeloid data.",
        "- IBD GSE282122 is cell-resolved, but this analysis uses patient-collapsed",
        "  pseudobulk module scores, not causal perturbation.",
        "- Directionally unstable RA/IBD effects block a stratification claim even if",
        "  one dataset has nominal p-values.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)

    ra_sample_scores, ra_pairs, ra_genes = ra_tables()
    ra_tests_df = ra_tests(ra_pairs)
    ibd_sample_scores, ibd_pairs, ibd_genes = ibd_scores_and_pairs()
    ibd_tests_df = ibd_tests(ibd_pairs)
    conv = convergence(ra_tests_df, ibd_tests_df)
    decision = make_decision(conv)
    genes = pd.concat([ra_genes, ibd_genes], ignore_index=True)

    ra_sample_scores.to_csv(OUT / "ra_sample_module_scores.tsv", sep="\t", index=False)
    ra_pairs.to_csv(OUT / "ra_patient_module_pairs.tsv", sep="\t", index=False)
    ra_tests_df.to_csv(OUT / "ra_response_module_tests.tsv", sep="\t", index=False)
    ibd_sample_scores.to_csv(OUT / "ibd_sample_module_scores.tsv", sep="\t", index=False)
    ibd_pairs.to_csv(OUT / "ibd_patient_module_pairs.tsv", sep="\t", index=False)
    ibd_tests_df.to_csv(OUT / "ibd_response_module_tests.tsv", sep="\t", index=False)
    conv.to_csv(OUT / "cross_dataset_response_convergence.tsv", sep="\t", index=False)
    decision.to_csv(OUT / "response_state_stratification_decision.tsv", sep="\t", index=False)
    genes.to_csv(OUT / "module_gene_coverage.tsv", sep="\t", index=False)

    summary = {
        "random_seed": SEED,
        "inputs": {
            "ra_counts": rel(RA_COUNTS),
            "ra_meta": rel(RA_META),
            "ibd_h5ad": rel(ROOT / "data" / "raw_v3" / "wave67_gse282122_myeloid" / "myeloid_final.h5ad"),
            "ibd_pair_meta": rel(IBD_PAIR_META),
        },
        "ra_patient_count": int(ra_pairs["patient"].nunique()) if not ra_pairs.empty else 0,
        "ibd_patient_count": int(ibd_pairs["Patient"].nunique()) if not ibd_pairs.empty else 0,
        "decision": decision.replace({np.nan: None}).to_dict(orient="records")[0],
        "top_convergence": conv.head(20).replace({np.nan: None}).to_dict(orient="records") if not conv.empty else [],
    }
    write_json(OUT / "summary.json", summary)
    write_report(decision, conv, ra_tests_df, ibd_tests_df, genes)


if __name__ == "__main__":
    main()
