#!/usr/bin/env python3
"""Wave80 CD58/CD2 immune-synapse closure audit.

Question:
After Wave79 left CD58 as the only partial targetability survivor, is the
signal a specific cross-autoimmune intervention/stratification axis, or does it
collapse into immune-synapse/T-cell-mixture biology plus direct prior art?

This is a closure/falsification analysis. It does not promote CD58 as a target.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats

from v3_analyze_direct_h5ad_cell_states import MODULES as BASE_MODULES
from v3_analyze_direct_h5ad_cell_states import ROOT
from v3_wave68_gse282122_unrestricted_gene_screen import (
    aggregate_all_genes,
    build_primary_obs,
    load_inputs,
    logcpm as ibd_logcpm,
)


SEED = 20260527
OUT = ROOT / "phases/v3/results" / "wave80_cd58_synapse_closure"

RA_COUNTS = ROOT / "phases/v3/results" / "wave65_gse198520_ra_synovium_antitnf_audit" / "gse198520_counts_used.tsv"
RA_META = ROOT / "phases/v3/results" / "wave65_gse198520_ra_synovium_antitnf_audit" / "gse198520_sample_metadata.tsv"

GENE = "CD58"
MODULES = {
    "generic_nfkb": BASE_MODULES["inflammatory_nfkb"],
    "t_synapse": ["CD2", "CD3D", "CD3E", "TRAC", "LCK", "LAT", "CD4", "CD8A", "CD28", "ICOS"],
    "apc_hla": ["CD74", "HLA-DRA", "HLA-DPA1", "HLA-DPB1", "HLA-DRB1", "CIITA"],
    "myeloid": ["CD14", "ITGAM", "LST1", "AIF1", "CSF1R", "FCGR3A", "FCGR1A"],
    "b_cell": ["MS4A1", "CD79A", "CD79B", "CD19", "CD37"],
    "stromal_injury": ["COL1A1", "COL1A2", "DCN", "LUM", "VIM"],
}
ALL_GENES = sorted({GENE, *[gene for genes in MODULES.values() for gene in genes]})


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True) + "\n", encoding="utf-8")


def read_tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", low_memory=False)


def markdown_table(df: pd.DataFrame, max_rows: int = 40) -> str:
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


def log_cpm_gene_x_sample(counts: pd.DataFrame) -> pd.DataFrame:
    lib = counts.sum(axis=0).replace(0, np.nan)
    return np.log2(counts.div(lib, axis=1) * 1_000_000.0 + 1.0)


def zscore_by_gene(expr: pd.DataFrame) -> pd.DataFrame:
    """Input gene x sample; output gene x sample z-scored across samples."""
    return expr.sub(expr.mean(axis=1), axis=0).div(expr.std(axis=1, ddof=1).replace(0, np.nan), axis=0)


def zscore_by_column(expr: pd.DataFrame) -> pd.DataFrame:
    """Input sample x gene; output sample x gene z-scored across samples."""
    return expr.sub(expr.mean(axis=0), axis=1).div(expr.std(axis=0, ddof=1).replace(0, np.nan), axis=1)


def score_modules_sample_x_gene(expr: pd.DataFrame) -> pd.DataFrame:
    z = zscore_by_column(expr)
    out = pd.DataFrame(index=expr.index)
    out["cd58"] = z[GENE] if GENE in z.columns else np.nan
    for name, genes in MODULES.items():
        present = [gene for gene in genes if gene in z.columns]
        out[f"{name}_score"] = z[present].mean(axis=1, skipna=True) if present else np.nan
        out[f"{name}_genes_present"] = len(present)
    return out


def fit_ols(data: pd.DataFrame, formula: str, coef_name: str, label: dict[str, Any]) -> dict[str, Any]:
    needed = [coef_name]
    lhs, rhs = formula.split("~", 1)
    needed.append(lhs.strip())
    for token in rhs.replace("+", " ").replace("C(", " ").replace(")", " ").split():
        token = token.strip()
        if token and token in data.columns:
            needed.append(token)
    model_df = data.dropna(subset=sorted(set(needed))).copy()
    if model_df.shape[0] < 12 or model_df[coef_name].nunique() < 2:
        return {
            **label,
            "n": int(model_df.shape[0]),
            "coef": np.nan,
            "p": np.nan,
            "r2": np.nan,
            "status": "insufficient_rows_or_response_levels",
            "formula": formula,
        }
    try:
        model = smf.ols(formula, data=model_df).fit()
        return {
            **label,
            "n": int(model_df.shape[0]),
            "coef": float(model.params.get(coef_name, np.nan)),
            "p": float(model.pvalues.get(coef_name, np.nan)),
            "r2": float(model.rsquared),
            "status": "ok",
            "formula": formula,
        }
    except Exception as exc:  # pragma: no cover - retained for audit logging
        return {
            **label,
            "n": int(model_df.shape[0]),
            "coef": np.nan,
            "p": np.nan,
            "r2": np.nan,
            "status": f"model_error:{type(exc).__name__}:{exc}",
            "formula": formula,
        }


def attenuation(models: pd.DataFrame, dataset: str, endpoint: str, raw_model: str, adjusted_model: str) -> dict[str, Any]:
    rows = models[(models["dataset"].eq(dataset)) & (models["endpoint"].eq(endpoint))]
    raw = rows[rows["model"].eq(raw_model)]
    adj = rows[rows["model"].eq(adjusted_model)]
    if raw.empty or adj.empty:
        return {
            "dataset": dataset,
            "endpoint": endpoint,
            "raw_model": raw_model,
            "adjusted_model": adjusted_model,
            "raw_coef": np.nan,
            "adjusted_coef": np.nan,
            "abs_coef_ratio": np.nan,
            "attenuation_fraction": np.nan,
            "raw_p": np.nan,
            "adjusted_p": np.nan,
        }
    raw_row = raw.iloc[0]
    adj_row = adj.iloc[0]
    raw_coef = float(raw_row["coef"])
    adj_coef = float(adj_row["coef"])
    ratio = abs(adj_coef) / abs(raw_coef) if raw_coef and np.isfinite(raw_coef) else np.nan
    return {
        "dataset": dataset,
        "endpoint": endpoint,
        "raw_model": raw_model,
        "adjusted_model": adjusted_model,
        "raw_coef": raw_coef,
        "adjusted_coef": adj_coef,
        "abs_coef_ratio": ratio,
        "attenuation_fraction": 1.0 - ratio if np.isfinite(ratio) else np.nan,
        "raw_p": float(raw_row["p"]),
        "adjusted_p": float(adj_row["p"]),
    }


def spearman_rows(df: pd.DataFrame, dataset: str, group_cols: list[str]) -> pd.DataFrame:
    rows = []
    covariates = [
        "generic_nfkb_score",
        "t_synapse_score",
        "apc_hla_score",
        "myeloid_score",
        "b_cell_score",
        "stromal_injury_score",
    ]
    for key, sub in df.groupby(group_cols, observed=True, dropna=False):
        label = key if isinstance(key, tuple) else (key,)
        for cov in covariates:
            tmp = sub[["cd58", cov]].dropna()
            if tmp.shape[0] < 8:
                rho = np.nan
                p = np.nan
            else:
                rho, p = stats.spearmanr(tmp["cd58"], tmp[cov])
            rows.append(
                {
                    "dataset": dataset,
                    **{col: val for col, val in zip(group_cols, label, strict=True)},
                    "covariate": cov,
                    "n": int(tmp.shape[0]),
                    "spearman_rho": float(rho) if np.isfinite(rho) else np.nan,
                    "p": float(p) if np.isfinite(p) else np.nan,
                }
            )
    return pd.DataFrame(rows)


def build_ra_pairs() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    counts = read_tsv(RA_COUNTS).set_index("GeneSymbol")
    counts.index = counts.index.astype(str).str.upper()
    counts = counts.groupby(level=0).sum()
    expr_all = log_cpm_gene_x_sample(counts)
    present = [gene for gene in ALL_GENES if gene in expr_all.index]
    expr = expr_all.loc[present]
    scores = score_modules_sample_x_gene(expr.T)
    meta = read_tsv(RA_META).set_index("count_column")
    sample = meta.join(scores, how="left")
    rows = []
    for patient, sub in sample.groupby("patient", observed=True):
        pre = sub[sub["timepoint"].eq("pre")]
        post = sub[sub["timepoint"].eq("post")]
        if len(pre) != 1 or len(post) != 1:
            continue
        p = pre.iloc[0]
        q = post.iloc[0]
        row = {
            "patient": patient,
            "response_code": p.get("response_code"),
            "response_class": p.get("response_class"),
            "good_response": int(bool(p.get("responder_good_only"))),
            "moderate_good_response": int(bool(p.get("responder_moderate_or_good"))),
            "pathotype": p.get("pathotype"),
            "biologic": p.get("biologic"),
            "inflammatory_score": pd.to_numeric(p.get("inflammatory_score"), errors="coerce"),
            "das28_score": pd.to_numeric(p.get("das28_score"), errors="coerce"),
        }
        for col in ["cd58", *[f"{name}_score" for name in MODULES]]:
            row[f"{col}_pre"] = p.get(col)
            row[f"{col}_post"] = q.get(col)
            row[f"{col}_delta"] = q.get(col) - p.get(col)
        rows.append(row)
    pair_df = pd.DataFrame(rows)
    corr = spearman_rows(sample.reset_index(), "GSE198520_RA_synovium_antiTNF", ["timepoint"])
    return sample.reset_index(), pair_df, corr


def build_ibd_pairs() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    adata, paired, obs = load_inputs()
    primary = build_primary_obs(obs, paired)
    meta, counts = aggregate_all_genes(adata, primary)
    present = [gene for gene in ALL_GENES if gene in counts.columns]
    expr = ibd_logcpm(meta, counts[present])
    scores = score_modules_sample_x_gene(expr)
    sample = pd.concat([meta.reset_index(drop=True), scores.reset_index(drop=True)], axis=1)
    rows = []
    for key, sub in sample.groupby(["Patient", "Disease", "Site", "Remission_status", "cell_state"], observed=True, dropna=False):
        pre = sub[sub["Treatment"].eq("Pre")]
        post = sub[sub["Treatment"].eq("Post")]
        if len(pre) != 1 or len(post) != 1:
            continue
        p = pre.iloc[0]
        q = post.iloc[0]
        min_cells = int(min(p["n_cells"], q["n_cells"]))
        if min_cells < 20:
            continue
        row = {
            "Patient": key[0],
            "Disease": key[1],
            "Site": key[2],
            "Remission_status": key[3],
            "remission": int(key[3] == "Remission"),
            "cell_state": key[4],
            "n_sites": 1,
            "min_n_cells": min_cells,
            "baseline_inflammation_score": float(p["mean_inflammation_score"]),
        }
        for col in ["cd58", *[f"{name}_score" for name in MODULES]]:
            row[f"{col}_pre"] = p.get(col)
            row[f"{col}_post"] = q.get(col)
            row[f"{col}_delta"] = q.get(col) - p.get(col)
        rows.append(row)
    site_pair = pd.DataFrame(rows)
    patient_rows = []
    for key, sub in site_pair.groupby(["Patient", "Disease", "Remission_status", "cell_state"], observed=True, dropna=False):
        row = {
            "Patient": key[0],
            "Disease": key[1],
            "Remission_status": key[2],
            "remission": int(key[2] == "Remission"),
            "cell_state": key[3],
            "n_sites": int(sub["Site"].nunique()),
            "min_n_cells": int(sub["min_n_cells"].min()),
            "baseline_inflammation_score": float(sub["baseline_inflammation_score"].mean()),
        }
        score_cols = [col for col in site_pair.columns if col.endswith("_pre") or col.endswith("_post") or col.endswith("_delta")]
        for col in score_cols:
            row[col] = float(sub[col].mean())
        patient_rows.append(row)
    patient_pair = pd.DataFrame(patient_rows)
    corr = spearman_rows(sample.reset_index(), "GSE282122_IBD_myeloid_antiTNF", ["Treatment", "cell_state"])
    return sample, patient_pair, corr


def fit_ra_models(pair_df: pd.DataFrame) -> pd.DataFrame:
    specs = [
        (
            "baseline",
            "M0_clinical",
            "cd58_pre ~ good_response + generic_nfkb_score_pre + C(pathotype) + C(biologic) + inflammatory_score + das28_score",
        ),
        (
            "baseline",
            "M1_t_synapse",
            "cd58_pre ~ good_response + generic_nfkb_score_pre + t_synapse_score_pre + C(pathotype) + C(biologic) + inflammatory_score + das28_score",
        ),
        (
            "baseline",
            "M2_full_mixture",
            "cd58_pre ~ good_response + generic_nfkb_score_pre + t_synapse_score_pre + apc_hla_score_pre + myeloid_score_pre + b_cell_score_pre + stromal_injury_score_pre + C(pathotype) + C(biologic) + inflammatory_score + das28_score",
        ),
        (
            "delta",
            "M0_clinical",
            "cd58_delta ~ good_response + cd58_pre + generic_nfkb_score_pre + generic_nfkb_score_delta + C(pathotype) + C(biologic) + inflammatory_score + das28_score",
        ),
        (
            "delta",
            "M1_t_synapse",
            "cd58_delta ~ good_response + cd58_pre + generic_nfkb_score_pre + generic_nfkb_score_delta + t_synapse_score_pre + t_synapse_score_delta + C(pathotype) + C(biologic) + inflammatory_score + das28_score",
        ),
        (
            "delta",
            "M2_full_mixture",
            "cd58_delta ~ good_response + cd58_pre + generic_nfkb_score_pre + generic_nfkb_score_delta + t_synapse_score_pre + t_synapse_score_delta + apc_hla_score_pre + apc_hla_score_delta + myeloid_score_pre + myeloid_score_delta + b_cell_score_pre + b_cell_score_delta + stromal_injury_score_pre + C(pathotype) + C(biologic) + inflammatory_score + das28_score",
        ),
    ]
    rows = []
    for endpoint, model_name, formula in specs:
        rows.append(
            fit_ols(
                pair_df,
                formula,
                "good_response",
                {
                    "dataset": "GSE198520_RA_synovium_antiTNF",
                    "cell_state": "bulk_synovium",
                    "endpoint": endpoint,
                    "model": model_name,
                },
            )
        )
    return pd.DataFrame(rows)


def fit_ibd_models(pair_df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    specs = [
        (
            "baseline",
            "M0_clinical",
            "cd58_pre ~ remission + generic_nfkb_score_pre + C(Disease) + baseline_inflammation_score",
        ),
        (
            "baseline",
            "M1_t_synapse",
            "cd58_pre ~ remission + generic_nfkb_score_pre + t_synapse_score_pre + C(Disease) + baseline_inflammation_score",
        ),
        (
            "baseline",
            "M2_full_mixture",
            "cd58_pre ~ remission + generic_nfkb_score_pre + t_synapse_score_pre + apc_hla_score_pre + myeloid_score_pre + b_cell_score_pre + stromal_injury_score_pre + C(Disease) + baseline_inflammation_score",
        ),
        (
            "delta",
            "M0_clinical",
            "cd58_delta ~ remission + cd58_pre + generic_nfkb_score_pre + generic_nfkb_score_delta + C(Disease) + baseline_inflammation_score",
        ),
        (
            "delta",
            "M1_t_synapse",
            "cd58_delta ~ remission + cd58_pre + generic_nfkb_score_pre + generic_nfkb_score_delta + t_synapse_score_pre + t_synapse_score_delta + C(Disease) + baseline_inflammation_score",
        ),
        (
            "delta",
            "M2_full_mixture",
            "cd58_delta ~ remission + cd58_pre + generic_nfkb_score_pre + generic_nfkb_score_delta + t_synapse_score_pre + t_synapse_score_delta + apc_hla_score_pre + apc_hla_score_delta + myeloid_score_pre + myeloid_score_delta + b_cell_score_pre + b_cell_score_delta + stromal_injury_score_pre + C(Disease) + baseline_inflammation_score",
        ),
    ]
    for state, sub in pair_df.groupby("cell_state", observed=True):
        for endpoint, model_name, formula in specs:
            rows.append(
                fit_ols(
                    sub,
                    formula,
                    "remission",
                    {
                        "dataset": "GSE282122_IBD_myeloid_antiTNF",
                        "cell_state": state,
                        "endpoint": endpoint,
                        "model": model_name,
                    },
                )
            )
    return pd.DataFrame(rows)


def write_report(
    ra_models: pd.DataFrame,
    ibd_models: pd.DataFrame,
    atten: pd.DataFrame,
    corr: pd.DataFrame,
    decision: dict[str, Any],
) -> None:
    report = f"""# Wave80 CD58/CD2 Immune-Synapse Closure

## Question

Can the `CD58` partial survivor from Wave79 be reframed as a coherent
cross-autoimmune immune-synapse intervention or stratification axis, or is it
explained by mixture/immune-synapse biology plus prior-art blockade?

## Verdict

`{decision['call']}`

## Decision

{decision['decision_text']}

## Attenuation Summary

{markdown_table(atten)}

## RA Models

{markdown_table(ra_models)}

## IBD Models

{markdown_table(ibd_models)}

## CD58 Correlations With Mixture/Synapse Scores

{markdown_table(corr.sort_values(['dataset', 'cell_state' if 'cell_state' in corr.columns else 'covariate', 'p']).head(60))}

## Interpretation

- RA uses bulk synovium, so `CD58` can reflect cell mixture, immune-synapse
  density, stromal/injury signal, or a true response-relevant state.
- IBD uses myeloid/DC pseudobulk, so T-cell markers are interpreted as ambient
  contamination, doublets, or sample-level lymphocyte proximity rather than
  true myeloid expression.
- A promotable target claim would require RA and IBD response coherence after
  these covariates, plus a non-prior-art intervention direction. That is not
  expected from Wave79 sidecar constraints.

## Output Files

- `{rel(OUT / 'ra_cd58_synapse_models.tsv')}`
- `{rel(OUT / 'ibd_cd58_synapse_models.tsv')}`
- `{rel(OUT / 'cd58_synapse_attenuation.tsv')}`
- `{rel(OUT / 'cd58_synapse_correlations.tsv')}`
- `{rel(OUT / 'ra_cd58_synapse_pairs.tsv')}`
- `{rel(OUT / 'ibd_cd58_synapse_pairs.tsv')}`
- `{rel(OUT / 'summary.json')}`
"""
    (OUT / "REPORT.md").write_text(report, encoding="utf-8")


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)

    ra_sample, ra_pairs, ra_corr = build_ra_pairs()
    ibd_sample, ibd_pairs, ibd_corr = build_ibd_pairs()
    ra_models = fit_ra_models(ra_pairs)
    ibd_models = fit_ibd_models(ibd_pairs)

    atten = pd.DataFrame(
        [
            attenuation(ra_models, "GSE198520_RA_synovium_antiTNF", "baseline", "M0_clinical", "M2_full_mixture"),
            attenuation(ra_models, "GSE198520_RA_synovium_antiTNF", "delta", "M0_clinical", "M2_full_mixture"),
            attenuation(ibd_models, "GSE282122_IBD_myeloid_antiTNF", "baseline", "M0_clinical", "M2_full_mixture"),
            attenuation(ibd_models, "GSE282122_IBD_myeloid_antiTNF", "delta", "M0_clinical", "M2_full_mixture"),
        ]
    )
    corr = pd.concat([ra_corr, ibd_corr], ignore_index=True, sort=False)

    ra_best = ra_models[
        ra_models["dataset"].eq("GSE198520_RA_synovium_antiTNF")
        & ra_models["endpoint"].eq("baseline")
        & ra_models["model"].eq("M2_full_mixture")
    ]
    ibd_best = ibd_models[
        ibd_models["dataset"].eq("GSE282122_IBD_myeloid_antiTNF")
        & ibd_models["endpoint"].eq("baseline")
        & ibd_models["model"].eq("M2_full_mixture")
    ]
    ibd_any = bool((ibd_best["p"] <= 0.10).any()) if not ibd_best.empty else False
    ra_survives = bool((not ra_best.empty) and float(ra_best.iloc[0]["p"]) <= 0.10)
    ra_atten = atten[
        atten["dataset"].eq("GSE198520_RA_synovium_antiTNF")
        & atten["endpoint"].eq("baseline")
    ]
    ra_ratio = float(ra_atten.iloc[0]["abs_coef_ratio"]) if not ra_atten.empty else np.nan

    if not ra_survives and not ibd_any:
        call = "CLOSE_CD58_RESPONSE_SIGNAL_MIXTURE_OR_WEAK_REPLICATION"
        decision_text = (
            "Close CD58 as a therapeutic or stratification candidate from this route: "
            "the response signal does not survive mixture/synapse adjustment in RA and "
            "does not replicate in IBD."
        )
    elif ra_survives and not ibd_any:
        call = "PARK_CD58_RA_ONLY_PRIOR_ART_BLOCKED"
        decision_text = (
            "Park CD58 as an RA-only response-state comparator: RA retains some signal "
            "after mixture/synapse adjustment, but IBD replication is absent and the "
            "intervention route is prior-art blocked."
        )
    elif ra_survives and ibd_any and np.isfinite(ra_ratio) and ra_ratio >= 0.5:
        call = "PARK_CD58_STRATIFICATION_ONLY_NOT_TARGET"
        decision_text = (
            "Retain CD58 only as a possible stratification biomarker. Even with "
            "cross-dataset response signal, alefacept/CD2-CD58 prior art and MS "
            "directionality conflict block target promotion."
        )
    else:
        call = "CLOSE_CD58_UNSTABLE_DIRECTIONALITY"
        decision_text = (
            "Close CD58 for V3 target promotion because the adjusted response evidence "
            "is unstable and therapeutic direction remains conflicted."
        )

    summary: dict[str, Any] = {
        "seed": SEED,
        "call": call,
        "decision_text": decision_text,
        "ra_n_patients": int(ra_pairs.shape[0]),
        "ibd_n_patient_cellstate_rows": int(ibd_pairs.shape[0]),
        "ibd_n_patients": int(ibd_pairs["Patient"].nunique()) if not ibd_pairs.empty else 0,
        "ra_baseline_full_p": float(ra_best.iloc[0]["p"]) if not ra_best.empty else np.nan,
        "ra_baseline_full_coef": float(ra_best.iloc[0]["coef"]) if not ra_best.empty else np.nan,
        "ra_baseline_full_abs_coef_ratio": ra_ratio,
        "ibd_baseline_full_min_p": float(ibd_best["p"].min()) if not ibd_best.empty else np.nan,
        "ibd_any_baseline_full_p10": ibd_any,
        "interpretation": "closure/falsification only; prior art blocks intervention novelty",
        "inputs": {
            "ra_counts": rel(RA_COUNTS),
            "ra_metadata": rel(RA_META),
            "ibd_h5ad": rel(ROOT / "data" / "raw_v3" / "wave67_gse282122_myeloid" / "myeloid_final.h5ad"),
        },
    }

    ra_sample.to_csv(OUT / "ra_cd58_synapse_sample_scores.tsv", sep="\t", index=False)
    ra_pairs.to_csv(OUT / "ra_cd58_synapse_pairs.tsv", sep="\t", index=False)
    ibd_sample.to_csv(OUT / "ibd_cd58_synapse_sample_scores.tsv", sep="\t", index=False)
    ibd_pairs.to_csv(OUT / "ibd_cd58_synapse_pairs.tsv", sep="\t", index=False)
    ra_models.to_csv(OUT / "ra_cd58_synapse_models.tsv", sep="\t", index=False)
    ibd_models.to_csv(OUT / "ibd_cd58_synapse_models.tsv", sep="\t", index=False)
    atten.to_csv(OUT / "cd58_synapse_attenuation.tsv", sep="\t", index=False)
    corr.to_csv(OUT / "cd58_synapse_correlations.tsv", sep="\t", index=False)
    write_json(OUT / "summary.json", summary)
    write_report(ra_models, ibd_models, atten, corr, summary)


if __name__ == "__main__":
    main()
