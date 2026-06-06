#!/usr/bin/env python3
"""Wave68 unrestricted GSE282122 myeloid/DC perturbation gene screen.

Purpose:
- After Wave67 failed the pre-specified lipid-lysosomal target modules, screen
  individual genes in the same cell-resolved paired anti-TNF dataset.
- Intersect perturbation signals with Wave62 cross-autoimmune target-resolution
  genetics to find any gene-level successor worth reopening.

This is still a gate. It does not claim a therapeutic target without further
druggability, prior-art, and cross-dataset validation.
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

from v3_analyze_direct_h5ad_cell_states import ROOT


SEED = 20260527
RAW = ROOT / "data" / "raw_v3" / "wave67_gse282122_myeloid"
OUT = ROOT / "phases/v3/results" / "wave68_gse282122_unrestricted_gene_screen"
MYELOID_FILE = RAW / "myeloid_final.h5ad"
PAIRED_FILE = RAW / "paired_sample_list.csv"
WAVE62_TARGETS = ROOT / "phases/v3/results" / "wave62_opentargets_target_resolution" / "target_resolution_summary.tsv"
WAVE67_DELTAS = ROOT / "phases/v3/results" / "wave67_gse282122_myeloid_pseudobulk" / "paired_module_deltas.tsv"

PRIMARY_STATES = ["Mono_macro", "DC"]
MIN_CELLS_PER_SIDE = 20
TOP_OLS_PER_STATE = 750
GENERIC_MODULES = ["ifn_apc", "inflammatory_nfkb", "tnf_autocrine_nfkb"]
V3_POSTHOC_BLOCKERS = {
    # Wave56/63 already audited SP140 directly: the biology is real in Crohn,
    # but therapeutic promotion is blocked by direct prior art, direction
    # conflict for SP140-low risk alleles, weak CNS lead-likeness, and null
    # local MS white-matter signal. Keep it visible as a comparator, not a
    # reopened target.
    "SP140": "v3_sp140_prior_art_direction_conflict_ms_local_null",
}
PRIORITY_GENES = {
    "CD74",
    "HLA-DRA",
    "HLA-DRB1",
    "HLA-DPA1",
    "HLA-DPB1",
    "CIITA",
    "IFI30",
    "CTSS",
    "CTSB",
    "CTSD",
    "LIPA",
    "NPC2",
    "RGS1",
    "INAVA",
    "SP140",
    "IL7R",
    "TNFSF14",
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True) + "\n", encoding="utf-8")


def bh(values: pd.Series | np.ndarray) -> np.ndarray:
    return multipletests(pd.Series(values).fillna(1.0).to_numpy(float), method="fdr_bh")[1]


def gene_symbols(adata: ad.AnnData) -> list[str]:
    for col in ["gene_symbols", "gene_symbol", "feature_name", "GeneSym", "symbol", "gene_name"]:
        if col in adata.var.columns:
            vals = adata.var[col].astype(str).str.upper().tolist()
            if len(set(vals) & PRIORITY_GENES) >= 3:
                return vals
    return [str(x).upper() for x in adata.var_names]


def load_inputs() -> tuple[ad.AnnData, pd.DataFrame, pd.DataFrame]:
    if not MYELOID_FILE.exists():
        raise RuntimeError(f"missing {MYELOID_FILE}; run Wave67 first")
    if not PAIRED_FILE.exists():
        raise RuntimeError(f"missing {PAIRED_FILE}; run Wave67 first")
    adata = ad.read_h5ad(MYELOID_FILE)
    paired = pd.read_csv(PAIRED_FILE, sep=None, engine="python")
    obs = adata.obs.copy().reset_index(names="obs_index")
    for col in ["sample_id", "Patient", "Disease", "Site", "Treatment", "Remission_status", "major", "Batch"]:
        if col in obs.columns:
            obs[col] = obs[col].astype(str).str.strip()
    obs["Inflammation_score_numeric"] = pd.to_numeric(obs.get("Inflammation_score", np.nan), errors="coerce")
    return adata, paired, obs


def build_primary_obs(obs: pd.DataFrame, paired: pd.DataFrame) -> pd.DataFrame:
    paired_samples = set(paired["sample_id"].astype(str))
    filt = obs[
        obs["sample_id"].astype(str).isin(paired_samples)
        & obs["Disease"].isin(["CD", "UC"])
        & obs["Treatment"].isin(["Pre", "Post"])
        & obs["Remission_status"].isin(["Remission", "Non_Remission"])
        & obs["major"].isin(PRIMARY_STATES)
    ].copy()
    filt["cell_state"] = filt["major"]
    return filt.sort_index()


def aggregate_all_genes(adata: ad.AnnData, obs: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    X = adata.X.tocsr() if sparse.issparse(adata.X) else sparse.csr_matrix(adata.X)
    totals = np.asarray(X.sum(axis=1)).ravel()
    symbols = gene_symbols(adata)
    obs = obs.copy()
    obs["row_position"] = obs.index.to_numpy()
    obs["cell_total_counts"] = totals[obs["row_position"].to_numpy(int)]
    group_cols = ["Patient", "Disease", "Site", "Treatment", "Remission_status", "sample_id", "Batch", "cell_state"]
    meta_rows = []
    count_blocks = []
    for key, sub in obs.groupby(group_cols, observed=True, dropna=False):
        idx = sub["row_position"].to_numpy(int)
        summed = np.asarray(X[idx, :].sum(axis=0)).ravel()
        meta = dict(zip(group_cols, key, strict=True))
        meta.update(
            {
                "n_cells": int(len(idx)),
                "total_counts_all_genes": float(sub["cell_total_counts"].sum()),
                "mean_inflammation_score": float(sub["Inflammation_score_numeric"].mean()),
            }
        )
        meta_rows.append(meta)
        count_blocks.append(summed)
    meta_df = pd.DataFrame(meta_rows)
    counts = pd.DataFrame(np.vstack(count_blocks), columns=symbols)
    # Collapse duplicate symbols if present.
    counts = counts.T.groupby(level=0).sum().T
    counts.index = meta_df.index
    return meta_df, counts


def logcpm(meta: pd.DataFrame, counts: pd.DataFrame) -> pd.DataFrame:
    denom = pd.to_numeric(meta["total_counts_all_genes"], errors="coerce").replace(0, np.nan)
    return np.log2(counts.div(denom, axis=0) * 1_000_000.0 + 1.0)


def paired_gene_deltas(meta: pd.DataFrame, expr: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows = []
    delta_blocks = []
    pair_cols = ["Patient", "Disease", "Site", "Remission_status", "cell_state"]
    for key, sub in meta.groupby(pair_cols, observed=True, dropna=False):
        pre = sub[sub["Treatment"].eq("Pre")]
        post = sub[sub["Treatment"].eq("Post")]
        if len(pre) != 1 or len(post) != 1:
            continue
        pidx = pre.index[0]
        qidx = post.index[0]
        p = pre.iloc[0]
        q = post.iloc[0]
        min_cells = int(min(p["n_cells"], q["n_cells"]))
        row = {
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
        rows.append(row)
        delta_blocks.append((expr.loc[qidx] - expr.loc[pidx]).to_numpy(float))
    pair_meta = pd.DataFrame(rows)
    deltas = pd.DataFrame(np.vstack(delta_blocks), columns=expr.columns) if delta_blocks else pd.DataFrame()
    deltas.index = pair_meta.index
    return pair_meta, deltas


def one_sample_gene_tests(pair_meta: pd.DataFrame, deltas: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for state, idx in pair_meta[pair_meta["passes_cell_threshold"]].groupby("cell_state", observed=True).groups.items():
        idx = list(idx)
        block = deltas.loc[idx]
        n = block.notna().sum(axis=0).to_numpy(float)
        mean = block.mean(axis=0).to_numpy(float)
        sd = block.std(axis=0, ddof=1).replace(0, np.nan).to_numpy(float)
        se = sd / np.sqrt(n)
        t_stat = mean / se
        p = np.full_like(mean, np.nan, dtype=float)
        valid = (n >= 4) & np.isfinite(t_stat)
        p[valid] = stats.t.sf(np.abs(t_stat[valid]), df=n[valid] - 1) * 2.0
        out = pd.DataFrame(
            {
                "cell_state": state,
                "gene": block.columns,
                "n_pairs": n.astype(int),
                "n_patients": pair_meta.loc[idx, "Patient"].nunique(),
                "mean_delta": mean,
                "sd_delta": sd,
                "t": t_stat,
                "paired_p": p,
            }
        )
        out["paired_fdr"] = bh(out["paired_p"])
        rows.append(out)
    return pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()


def patient_collapsed(pair_meta: pd.DataFrame, deltas: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    filt = pair_meta[pair_meta["passes_cell_threshold"]].copy()
    meta_rows = []
    delta_rows = []
    for key, sub in filt.groupby(["Patient", "Disease", "Remission_status", "cell_state"], observed=True, dropna=False):
        idx = list(sub.index)
        meta_rows.append(
            {
                "Patient": key[0],
                "Disease": key[1],
                "Remission_status": key[2],
                "cell_state": key[3],
                "n_sites": int(sub["Site"].nunique()),
                "min_n_cells": int(sub["min_n_cells"].min()),
                "baseline_inflammation_score": float(sub["baseline_inflammation_score"].mean()),
            }
        )
        delta_rows.append(deltas.loc[idx].mean(axis=0).to_numpy(float))
    meta = pd.DataFrame(meta_rows)
    dmat = pd.DataFrame(np.vstack(delta_rows), columns=deltas.columns) if delta_rows else pd.DataFrame()
    dmat.index = meta.index
    return meta, dmat


def response_gene_tests(pair_meta: pd.DataFrame, deltas: pd.DataFrame) -> pd.DataFrame:
    meta, dmat = patient_collapsed(pair_meta, deltas)
    rows = []
    for state, idx0 in meta.groupby("cell_state", observed=True).groups.items():
        idx = list(idx0)
        block = dmat.loc[idx]
        submeta = meta.loc[idx]
        rem_mask = submeta["Remission_status"].eq("Remission").to_numpy()
        non_mask = submeta["Remission_status"].eq("Non_Remission").to_numpy()
        rem = block.loc[rem_mask]
        non = block.loc[non_mask]
        n_rem = rem.notna().sum(axis=0).to_numpy(float)
        n_non = non.notna().sum(axis=0).to_numpy(float)
        mean_rem = rem.mean(axis=0).to_numpy(float)
        mean_non = non.mean(axis=0).to_numpy(float)
        var_rem = rem.var(axis=0, ddof=1).replace(0, np.nan).to_numpy(float)
        var_non = non.var(axis=0, ddof=1).replace(0, np.nan).to_numpy(float)
        diff = mean_rem - mean_non
        se = np.sqrt(var_rem / n_rem + var_non / n_non)
        t_stat = diff / se
        df_num = (var_rem / n_rem + var_non / n_non) ** 2
        df_den = (var_rem**2 / ((n_rem**2) * (n_rem - 1))) + (var_non**2 / ((n_non**2) * (n_non - 1)))
        df = df_num / df_den
        p = np.full_like(diff, np.nan, dtype=float)
        valid = (n_rem >= 4) & (n_non >= 4) & np.isfinite(t_stat) & np.isfinite(df)
        p[valid] = stats.t.sf(np.abs(t_stat[valid]), df=df[valid]) * 2.0
        out = pd.DataFrame(
            {
                "cell_state": state,
                "gene": block.columns,
                "n_patient_units": len(block),
                "n_remission": n_rem.astype(int),
                "n_non_remission": n_non.astype(int),
                "mean_delta_remission": mean_rem,
                "mean_delta_non_remission": mean_non,
                "raw_delta_remission_minus_non": diff,
                "raw_t": t_stat,
                "raw_p": p,
            }
        )
        out["raw_fdr"] = bh(out["raw_p"])
        rows.append(out)
    return pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()


def generic_patient_covariates() -> pd.DataFrame:
    if not WAVE67_DELTAS.exists():
        return pd.DataFrame()
    d = pd.read_csv(WAVE67_DELTAS, sep="\t")
    d = d[d["passes_cell_threshold"] & d["state_level"].eq("major") & d["module"].isin(GENERIC_MODULES)].copy()
    collapsed = (
        d.groupby(["Patient", "Disease", "Remission_status", "cell_state", "module"], observed=True)
        .agg(delta=("delta_post_minus_pre", "mean"), pre_score=("pre_score", "mean"))
        .reset_index()
    )
    wide = collapsed.pivot_table(
        index=["Patient", "Disease", "Remission_status", "cell_state"],
        columns="module",
        values="delta",
        aggfunc="first",
    ).reset_index()
    generic_cols = [c for c in GENERIC_MODULES if c in wide.columns]
    wide["generic_delta"] = wide[generic_cols].mean(axis=1)
    return wide[["Patient", "Disease", "Remission_status", "cell_state", "generic_delta"]]


def adjusted_top_ols(
    response: pd.DataFrame,
    pair_meta: pd.DataFrame,
    deltas: pd.DataFrame,
    expr_baseline: pd.DataFrame,
) -> pd.DataFrame:
    meta, dmat = patient_collapsed(pair_meta, deltas)
    generic = generic_patient_covariates()
    meta2 = meta.merge(generic, on=["Patient", "Disease", "Remission_status", "cell_state"], how="left")
    # Baseline expression collapsed by patient/state from pre pseudobulk is
    # approximated by subtracting delta from post-pre impossible here; instead
    # use no baseline gene term in OLS to avoid reconstructing site-level pre
    # matrices for every gene. Baseline inflammation and generic delta remain.
    rows = []
    for state, subresp in response.groupby("cell_state", observed=True):
        genes = set(
            subresp.sort_values(["raw_p", "raw_fdr"]).head(TOP_OLS_PER_STATE)["gene"].astype(str)
        ) | PRIORITY_GENES
        submeta = meta2[meta2["cell_state"].eq(state)].copy()
        if submeta.empty:
            continue
        for gene in sorted(g for g in genes if g in dmat.columns):
            df = submeta.copy()
            df["target_delta"] = dmat.loc[df.index, gene].to_numpy(float)
            df["remission_binary"] = df["Remission_status"].eq("Remission").astype(int)
            df = df.replace([np.inf, -np.inf], np.nan).dropna(subset=["target_delta", "remission_binary"])
            if len(df) < 12 or df["remission_binary"].nunique() < 2 or df["remission_binary"].value_counts().min() < 4:
                continue
            formula = "target_delta ~ remission_binary"
            if df["generic_delta"].notna().sum() >= 10:
                formula += " + generic_delta"
            if df["baseline_inflammation_score"].notna().sum() >= 10:
                formula += " + baseline_inflammation_score"
            if df["Disease"].nunique() > 1:
                formula += " + C(Disease)"
            try:
                fit = ols(formula, data=df).fit()
                rows.append(
                    {
                        "cell_state": state,
                        "gene": gene,
                        "n": int(len(df)),
                        "remission_adjusted_delta": float(fit.params.get("remission_binary", np.nan)),
                        "remission_adjusted_p": float(fit.pvalues.get("remission_binary", np.nan)),
                        "formula": formula,
                    }
                )
            except Exception:  # noqa: BLE001
                continue
    out = pd.DataFrame(rows)
    if not out.empty:
        out["remission_adjusted_fdr"] = bh(out["remission_adjusted_p"])
    return out


def load_wave62() -> pd.DataFrame:
    if not WAVE62_TARGETS.exists():
        return pd.DataFrame(columns=["gene"])
    cols = [
        "gene",
        "approved_name",
        "wave62_score",
        "wave62_call",
        "manual_blocker",
        "prior_context_blocker",
        "max_l2g_score",
        "best_l2g_disease",
        "strong_l2g_disease_count",
        "strong_l2g_diseases",
        "strong_qtl_coloc_disease_count",
        "strong_qtl_coloc_diseases",
        "myeloid_qtl_coloc_disease_count",
        "max_qtl_h4",
        "ms_max_l2g_score",
        "ms_max_relevant_qtl_h4",
        "gwas_catalog_trait_count",
        "chembl_target_id",
        "druggable_activity_count",
        "wave55_score",
        "wave55_genetic_diseases_ge_0_25",
    ]
    d = pd.read_csv(WAVE62_TARGETS, sep="\t", usecols=lambda c: c in cols)
    d["gene"] = d["gene"].astype(str).str.upper()
    return d


def integrate(
    paired_tests: pd.DataFrame,
    response_tests: pd.DataFrame,
    adjusted: pd.DataFrame,
) -> pd.DataFrame:
    wave62 = load_wave62()
    merged = response_tests.merge(
        paired_tests[["cell_state", "gene", "mean_delta", "paired_p", "paired_fdr"]],
        on=["cell_state", "gene"],
        how="left",
    ).merge(adjusted, on=["cell_state", "gene"], how="left")
    merged["gene"] = merged["gene"].astype(str).str.upper()
    merged = merged.merge(wave62, on="gene", how="left")
    for col in ["wave62_score", "strong_l2g_disease_count", "strong_qtl_coloc_disease_count", "myeloid_qtl_coloc_disease_count", "druggable_activity_count", "wave55_score"]:
        if col not in merged.columns:
            merged[col] = 0.0
        merged[col] = pd.to_numeric(merged[col], errors="coerce").fillna(0.0)
    merged["has_cross_autoimmune_genetics"] = (
        (merged["strong_l2g_disease_count"] >= 3)
        | (merged["strong_qtl_coloc_disease_count"] >= 3)
        | (merged["wave62_score"] >= 4.0)
    )
    merged["has_any_druggability_flag"] = (
        merged.get("chembl_target_id", pd.Series("", index=merged.index)).fillna("").astype(str).ne("")
        | (merged["druggable_activity_count"] > 0)
    )
    merged["manual_or_prior_blocked"] = (
        merged.get("manual_blocker", pd.Series("", index=merged.index)).fillna("").astype(str).ne("")
        | merged.get("prior_context_blocker", pd.Series("", index=merged.index)).fillna("").astype(str).ne("")
    )
    merged["wave68_posthoc_blocker"] = merged["gene"].map(V3_POSTHOC_BLOCKERS).fillna("")
    merged["manual_or_prior_blocked"] = merged["manual_or_prior_blocked"] | merged["wave68_posthoc_blocker"].ne("")
    merged["perturbation_strength"] = (
        -np.log10(pd.to_numeric(merged["raw_p"], errors="coerce").clip(lower=1e-300).fillna(1.0))
        + -np.log10(pd.to_numeric(merged["paired_p"], errors="coerce").clip(lower=1e-300).fillna(1.0))
    )
    merged["integrated_score"] = (
        merged["perturbation_strength"]
        + merged["wave62_score"].clip(upper=8.0) / 2.0
        + merged["has_any_druggability_flag"].astype(float)
        - merged["manual_or_prior_blocked"].astype(float) * 2.0
    )
    calls = []
    for row in merged.itertuples(index=False):
        if (
            bool(row.has_cross_autoimmune_genetics)
            and bool(row.has_any_druggability_flag)
            and not bool(row.manual_or_prior_blocked)
            and (
                (np.isfinite(row.raw_fdr) and row.raw_fdr <= 0.10)
                or (np.isfinite(getattr(row, "remission_adjusted_fdr", np.nan)) and getattr(row, "remission_adjusted_fdr") <= 0.10)
                or (np.isfinite(row.paired_fdr) and row.paired_fdr <= 0.10)
            )
        ):
            calls.append("REOPEN_GENE_LEVEL_TARGET_CANDIDATE")
        elif bool(row.has_cross_autoimmune_genetics) and row.perturbation_strength >= 3:
            calls.append("PARK_GENETIC_PERTURBATION_INTERSECTION")
        else:
            calls.append("DESCRIPTIVE_GENE_SIGNAL")
    merged["wave68_call"] = calls
    call_priority = {
        "REOPEN_GENE_LEVEL_TARGET_CANDIDATE": 0,
        "PARK_GENETIC_PERTURBATION_INTERSECTION": 1,
        "DESCRIPTIVE_GENE_SIGNAL": 2,
    }
    merged["wave68_call_priority"] = merged["wave68_call"].map(call_priority).fillna(9).astype(int)
    return merged.sort_values(["wave68_call_priority", "integrated_score"], ascending=[True, False])


def write_report(
    pair_meta: pd.DataFrame,
    paired_tests: pd.DataFrame,
    response_tests: pd.DataFrame,
    adjusted: pd.DataFrame,
    integrated: pd.DataFrame,
) -> None:
    top_integrated = integrated.head(40)
    top_response = response_tests.sort_values(["raw_fdr", "raw_p"]).head(30)
    top_paired = paired_tests.sort_values(["paired_fdr", "paired_p"]).head(30)
    calls = integrated["wave68_call"].value_counts().to_dict()
    lines = [
        "# Wave68 GSE282122 Unrestricted Myeloid Gene Screen",
        "",
        f"Random seed: `{SEED}`.",
        "",
        "## Data",
        "",
        f"- Input h5ad: `{rel(MYELOID_FILE)}`.",
        f"- Paired major-state units: `{len(pair_meta)}` site/state rows before threshold filtering.",
        f"- Thresholded rows: `{int(pair_meta['passes_cell_threshold'].sum())}`.",
        f"- Genes tested: `{paired_tests['gene'].nunique()}`.",
        "",
        "## Verdict",
        "",
        f"- Calls: `{calls}`.",
        "- This is an unrestricted discovery screen. Any candidate must still pass druggability, prior-art, and independent cross-dataset validation.",
        "",
        "## Top Integrated Rows",
        "",
        "| state | gene | call | score | raw response FDR | adjusted FDR | paired FDR | wave62 score | genetics | druggable | blocker | posthoc blocker |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- | --- | --- |",
    ]
    for row in top_integrated.itertuples(index=False):
        lines.append(
            f"| {row.cell_state} | {row.gene} | {row.wave68_call} | {row.integrated_score:.3g} | "
            f"{row.raw_fdr:.3g} | {getattr(row, 'remission_adjusted_fdr', np.nan):.3g} | "
            f"{row.paired_fdr:.3g} | {row.wave62_score:.3g} | "
            f"{bool(row.has_cross_autoimmune_genetics)} | {bool(row.has_any_druggability_flag)} | "
            f"{bool(row.manual_or_prior_blocked)} | {getattr(row, 'wave68_posthoc_blocker', '')} |"
        )
    lines.extend(["", "## Top Raw Remission-Response Rows", ""])
    lines.extend(
        [
            "| state | gene | n | remission mean | nonremission mean | raw delta | raw p | raw FDR |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in top_response.itertuples(index=False):
        lines.append(
            f"| {row.cell_state} | {row.gene} | {row.n_patient_units} | {row.mean_delta_remission:.3g} | "
            f"{row.mean_delta_non_remission:.3g} | {row.raw_delta_remission_minus_non:.3g} | "
            f"{row.raw_p:.3g} | {row.raw_fdr:.3g} |"
        )
    lines.extend(["", "## Top Paired Pharmacodynamic Rows", ""])
    lines.extend(["| state | gene | n pairs | mean delta | p | FDR |", "| --- | --- | ---: | ---: | ---: | ---: |"])
    for row in top_paired.itertuples(index=False):
        lines.append(
            f"| {row.cell_state} | {row.gene} | {row.n_pairs} | {row.mean_delta:.3g} | "
            f"{row.paired_p:.3g} | {row.paired_fdr:.3g} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation Guardrails",
            "",
            "- Remission-response tests are associative and post-treatment outcome-linked, not randomized target perturbations.",
            "- Wave68 post-hoc blockers encode already-completed V3 audits so the unrestricted screen does not reopen candidates previously rejected on stronger evidence.",
            "- Genes with HLA/MHC symbols are not straightforward drug targets even when statistically strong.",
            "- Wave62 genetics intersection is target-resolution triage, not proof that changing the gene changes disease.",
        ]
    )
    (OUT / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    adata, paired, obs = load_inputs()
    primary_obs = build_primary_obs(obs, paired)
    meta, counts = aggregate_all_genes(adata, primary_obs)
    expr = logcpm(meta, counts)
    pair_meta, deltas = paired_gene_deltas(meta, expr)
    paired_tests = one_sample_gene_tests(pair_meta, deltas)
    response_tests = response_gene_tests(pair_meta, deltas)
    adjusted = adjusted_top_ols(response_tests, pair_meta, deltas, expr)
    integrated = integrate(paired_tests, response_tests, adjusted)

    primary_obs.to_csv(OUT / "primary_cell_obs_used.tsv", sep="\t", index=False)
    meta.to_csv(OUT / "all_gene_pseudobulk_metadata.tsv", sep="\t", index=False)
    pair_meta.to_csv(OUT / "all_gene_pair_metadata.tsv", sep="\t", index=False)
    paired_tests.to_csv(OUT / "paired_gene_delta_tests.tsv", sep="\t", index=False)
    response_tests.to_csv(OUT / "raw_remission_response_gene_tests.tsv", sep="\t", index=False)
    adjusted.to_csv(OUT / "adjusted_top_gene_ols.tsv", sep="\t", index=False)
    integrated.to_csv(OUT / "integrated_gene_target_rank.tsv", sep="\t", index=False)

    summary = {
        "seed": SEED,
        "input_files": {
            "myeloid_h5ad": rel(MYELOID_FILE),
            "paired_manifest": rel(PAIRED_FILE),
            "wave62_targets": rel(WAVE62_TARGETS),
        },
        "n_primary_cells": int(len(primary_obs)),
        "n_pseudobulk_strata": int(len(meta)),
        "n_pair_rows": int(len(pair_meta)),
        "n_threshold_pair_rows": int(pair_meta["passes_cell_threshold"].sum()),
        "n_genes_tested": int(paired_tests["gene"].nunique()) if not paired_tests.empty else 0,
        "calls": integrated["wave68_call"].value_counts().to_dict() if not integrated.empty else {},
        "top_integrated": integrated.head(30).replace({np.nan: None}).to_dict(orient="records")
        if not integrated.empty
        else [],
        "interpretation": "Unrestricted gene screen; candidates require further validation before any therapeutic claim.",
    }
    write_json(OUT / "summary.json", summary)
    write_report(pair_meta, paired_tests, response_tests, adjusted, integrated)


if __name__ == "__main__":
    main()
