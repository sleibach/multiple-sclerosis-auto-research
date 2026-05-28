#!/usr/bin/env python3
"""Wave67 GSE282122 myeloid anti-TNF pseudobulk perturbation audit.

Purpose:
- Move beyond bulk tissue signatures by testing V3 modules inside annotated
  human IBD myeloid/APC states under paired anti-TNF exposure.
- Use only the public Zenodo myeloid object, not full atlas reintegration.
- Treat this as a perturbation-direction gate, not a therapeutic claim.
"""

from __future__ import annotations

import hashlib
import json
import math
import urllib.request
from pathlib import Path
from typing import Any

import anndata as ad
import numpy as np
import pandas as pd
from scipy import sparse, stats
from statsmodels.formula.api import ols
from statsmodels.stats.multitest import multipletests

from v3_analyze_direct_h5ad_cell_states import MODULES, ROOT


SEED = 20260527
RAW = ROOT / "data" / "raw_v3" / "wave67_gse282122_myeloid"
OUT = ROOT / "results_v3" / "wave67_gse282122_myeloid_pseudobulk"

MYELOID_URL = "https://zenodo.org/api/records/14007626/files/myeloid_final.h5ad/content"
PAIRED_URL = "https://zenodo.org/api/records/14007626/files/paired_sample_list.csv/content"
MYELOID_FILE = RAW / "myeloid_final.h5ad"
PAIRED_FILE = RAW / "paired_sample_list.csv"
MYELOID_MD5 = "bdfe50345a11abdb1a72b2439bf9950e"
PAIRED_MD5 = "3300a53889bb4b70c48ec66dbb66beea"

PRIMARY_STATES = {"Mono_macro", "DC"}
SECONDARY_FINE_STATES = {
    "C1Qhi IL1Blo macro",
    "C1Qhi IL1Bhi macro",
    "S100A8 A9hi mono",
    "S100A8 A9hi TNFhi IL6pos mono",
    "CD1Chi DC",
}
MIN_CELLS_PER_SIDE_PRIMARY = 20
MIN_CELLS_PER_SIDE_FINE = 20
TARGET_MODULES = ["lipid_loader_repair", "lysosomal_apc", "complement_phagocytosis"]
GENERIC_MODULES = ["ifn_apc", "inflammatory_nfkb", "tnf_autocrine_nfkb"]

EXPANDED_MODULES = {
    **MODULES,
    "lipid_loader_repair": [
        "APOE",
        "APOC1",
        "TREM2",
        "GPNMB",
        "LPL",
        "SPP1",
        "LGALS3",
        "FABP5",
        "CD9",
        "AXL",
        "MERTK",
        "LIPA",
        "LAMP1",
        "CTSD",
    ],
    "lysosomal_apc": [
        "LAMP1",
        "LAMP2",
        "CTSB",
        "CTSD",
        "CTSS",
        "LIPA",
        "IFI30",
        "HLA-DRA",
        "HLA-DRB1",
        "HLA-DPA1",
        "HLA-DPB1",
        "CD74",
        "PSAP",
        "NPC2",
    ],
    "complement_phagocytosis": [
        "C1QA",
        "C1QB",
        "C1QC",
        "C3",
        "TYROBP",
        "FCGR3A",
        "FCGR2A",
        "ITGAM",
        "ITGB2",
        "AIF1",
        "VSIG4",
        "MRC1",
    ],
    "tnf_autocrine_nfkb": [
        "TNF",
        "TNFAIP3",
        "NFKBIA",
        "NFKBIZ",
        "RELB",
        "IL1B",
        "IL6",
        "CCL2",
        "CCL3",
        "CCL4",
        "CXCL8",
        "PTGS2",
    ],
    "host_defense_cost": ["IL1B", "TNF", "IL6", "CXCL8", "NOS2", "PTGS2", "TLR2", "TLR4"],
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True) + "\n", encoding="utf-8")


def md5sum(path: Path, chunk_size: int = 8 * 1024 * 1024) -> str:
    digest = hashlib.md5()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(chunk_size)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def download_if_missing(url: str, path: Path, expected_md5: str | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.stat().st_size > 0:
        if expected_md5 and md5sum(path) != expected_md5:
            path.unlink()
        else:
            return
    tmp = path.with_suffix(path.suffix + ".tmp")
    urllib.request.urlretrieve(url, tmp)
    tmp.replace(path)
    if expected_md5:
        observed = md5sum(path)
        if observed != expected_md5:
            raise RuntimeError(f"MD5 mismatch for {path}: observed {observed}, expected {expected_md5}")


def bh_fdr(values: pd.Series) -> np.ndarray:
    return multipletests(pd.to_numeric(values, errors="coerce").fillna(1.0).to_numpy(float), method="fdr_bh")[1]


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


def gene_symbol_series(adata: ad.AnnData) -> pd.Series:
    candidates = ["gene_symbols", "gene_symbol", "feature_name", "GeneSym", "symbol", "gene_name"]
    for column in candidates:
        if column in adata.var.columns:
            values = adata.var[column].astype(str)
            if values.str.upper().isin({g for genes in EXPANDED_MODULES.values() for g in genes}).any():
                return values
    return pd.Series(adata.var_names.astype(str), index=adata.var_names)


def build_gene_index(adata: ad.AnnData) -> tuple[list[str], list[int], pd.DataFrame]:
    symbols = gene_symbol_series(adata)
    upper_to_idx: dict[str, int] = {}
    for i, symbol in enumerate(symbols.astype(str)):
        upper_to_idx.setdefault(symbol.upper(), i)
    wanted = sorted({gene for genes in EXPANDED_MODULES.values() for gene in genes})
    present = [gene for gene in wanted if gene.upper() in upper_to_idx]
    indices = [upper_to_idx[gene.upper()] for gene in present]
    rows = []
    for module, genes in EXPANDED_MODULES.items():
        module_present = [gene for gene in genes if gene.upper() in upper_to_idx]
        rows.append(
            {
                "module": module,
                "n_genes_defined": len(genes),
                "n_genes_present": len(module_present),
                "genes_present": ",".join(module_present),
                "genes_missing": ",".join([gene for gene in genes if gene.upper() not in upper_to_idx]),
            }
        )
    return present, indices, pd.DataFrame(rows)


def normalize_obs(adata: ad.AnnData) -> pd.DataFrame:
    obs = adata.obs.copy()
    obs = obs.reset_index(names="obs_index")
    required = ["sample_id", "Patient", "Disease", "Site", "Treatment", "Remission_status", "major", "final_analysis"]
    missing = [col for col in required if col not in obs.columns]
    if missing:
        raise RuntimeError(f"myeloid h5ad missing required obs columns: {missing}")
    for col in required + ["Batch", "Inflammation_score", "Inflammation"]:
        if col in obs.columns:
            obs[col] = obs[col].astype(str).str.strip()
    obs["Inflammation_score_numeric"] = pd.to_numeric(obs.get("Inflammation_score", np.nan), errors="coerce")
    return obs


def load_paired_manifest() -> pd.DataFrame:
    download_if_missing(PAIRED_URL, PAIRED_FILE, PAIRED_MD5)
    manifest = pd.read_csv(PAIRED_FILE, sep=None, engine="python")
    manifest.columns = [c.strip() for c in manifest.columns]
    if "sample_id" not in manifest.columns:
        raise RuntimeError("paired manifest lacks sample_id column")
    return manifest


def build_stratified_obs(obs: pd.DataFrame, paired: pd.DataFrame) -> pd.DataFrame:
    paired_samples = set(paired["sample_id"].astype(str))
    base = obs[
        obs["sample_id"].astype(str).isin(paired_samples)
        & obs["Disease"].isin(["CD", "UC"])
        & obs["Treatment"].isin(["Pre", "Post"])
        & obs["Remission_status"].isin(["Remission", "Non_Remission"])
    ].copy()
    primary = base[base["major"].isin(PRIMARY_STATES)].copy()
    primary["state_level"] = "major"
    primary["cell_state"] = primary["major"]
    fine = base[base["final_analysis"].isin(SECONDARY_FINE_STATES)].copy()
    fine["state_level"] = "fine"
    fine["cell_state"] = fine["final_analysis"]
    return pd.concat([primary, fine], ignore_index=False).sort_index()


def aggregate_pseudobulk(
    adata: ad.AnnData,
    obs: pd.DataFrame,
    gene_names: list[str],
    gene_indices: list[int],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    selected = adata.X[:, gene_indices]
    if not sparse.issparse(selected):
        selected = sparse.csr_matrix(selected)
    else:
        selected = selected.tocsr()
    total_counts = np.asarray(adata.X.sum(axis=1)).ravel() if sparse.issparse(adata.X) else np.asarray(adata.X).sum(axis=1)
    obs = obs.copy()
    obs["row_position"] = obs.index.to_numpy()
    obs["cell_total_counts"] = total_counts[obs["row_position"].to_numpy(int)]

    group_cols = [
        "Patient",
        "Disease",
        "Site",
        "Treatment",
        "Remission_status",
        "sample_id",
        "Batch",
        "state_level",
        "cell_state",
    ]
    count_rows = []
    meta_rows = []
    for key, sub in obs.groupby(group_cols, observed=True, dropna=False):
        idx = sub["row_position"].to_numpy(int)
        summed = np.asarray(selected[idx, :].sum(axis=0)).ravel()
        group_total = float(sub["cell_total_counts"].sum())
        row = dict(zip(group_cols, key, strict=True))
        row.update(
            {
                "n_cells": int(len(idx)),
                "total_counts_all_genes": group_total,
                "mean_inflammation_score": float(pd.to_numeric(sub["Inflammation_score_numeric"], errors="coerce").mean()),
                "inflammation_label": ";".join(sorted(set(sub.get("Inflammation", pd.Series(dtype=str)).astype(str)))),
            }
        )
        meta_rows.append(row)
        count_row = {**row}
        count_row.update({gene: float(value) for gene, value in zip(gene_names, summed, strict=True)})
        count_rows.append(count_row)
    return pd.DataFrame(meta_rows), pd.DataFrame(count_rows)


def compute_module_scores(pseudobulk_counts: pd.DataFrame, gene_names: list[str]) -> tuple[pd.DataFrame, pd.DataFrame]:
    meta_cols = [col for col in pseudobulk_counts.columns if col not in set(gene_names)]
    gene_counts = pseudobulk_counts[gene_names].astype(float)
    denom = pd.to_numeric(pseudobulk_counts["total_counts_all_genes"], errors="coerce").replace(0, np.nan)
    logcpm = np.log2(gene_counts.div(denom, axis=0) * 1_000_000.0 + 1.0)
    logcpm.index = pseudobulk_counts.index
    rows = []
    for (state_level, cell_state), idx in pseudobulk_counts.groupby(["state_level", "cell_state"], observed=True).groups.items():
        idx = list(idx)
        block = logcpm.loc[idx]
        mean = block.mean(axis=0)
        sd = block.std(axis=0, ddof=1).replace(0, np.nan)
        z = block.sub(mean, axis=1).div(sd, axis=1).replace([np.inf, -np.inf], np.nan)
        meta = pseudobulk_counts.loc[idx, meta_cols].copy()
        for module, genes in EXPANDED_MODULES.items():
            present = [gene for gene in genes if gene in z.columns]
            if not present:
                continue
            tmp = meta.copy()
            tmp["module"] = module
            tmp["score"] = z[present].mean(axis=1, skipna=True).to_numpy(float)
            tmp["n_genes_present"] = len(present)
            rows.append(tmp)
    score_table = pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()
    return score_table, logcpm


def build_pair_deltas(scores: pd.DataFrame) -> pd.DataFrame:
    rows = []
    pair_cols = ["Patient", "Disease", "Site", "Remission_status", "state_level", "cell_state", "module"]
    for key, sub in scores.groupby(pair_cols, observed=True, dropna=False):
        pre = sub[sub["Treatment"].eq("Pre")]
        post = sub[sub["Treatment"].eq("Post")]
        if len(pre) != 1 or len(post) != 1:
            continue
        p = pre.iloc[0]
        q = post.iloc[0]
        min_required = MIN_CELLS_PER_SIDE_FINE if p["state_level"] == "fine" else MIN_CELLS_PER_SIDE_PRIMARY
        rows.append(
            {
                **dict(zip(pair_cols, key, strict=True)),
                "pre_sample_id": p["sample_id"],
                "post_sample_id": q["sample_id"],
                "pre_batch": p.get("Batch", ""),
                "post_batch": q.get("Batch", ""),
                "pre_score": float(p["score"]),
                "post_score": float(q["score"]),
                "delta_post_minus_pre": float(q["score"] - p["score"]),
                "pre_n_cells": int(p["n_cells"]),
                "post_n_cells": int(q["n_cells"]),
                "min_n_cells": int(min(p["n_cells"], q["n_cells"])),
                "passes_cell_threshold": bool(min(p["n_cells"], q["n_cells"]) >= min_required),
                "pre_total_counts_all_genes": float(p["total_counts_all_genes"]),
                "post_total_counts_all_genes": float(q["total_counts_all_genes"]),
                "baseline_inflammation_score": float(p["mean_inflammation_score"]),
                "post_inflammation_score": float(q["mean_inflammation_score"]),
                "baseline_inflammation_label": p.get("inflammation_label", ""),
                "post_inflammation_label": q.get("inflammation_label", ""),
            }
        )
    out = pd.DataFrame(rows)
    if out.empty:
        return out
    out["pair_id"] = (
        out["Patient"].astype(str)
        + "|"
        + out["Disease"].astype(str)
        + "|"
        + out["Site"].astype(str)
        + "|"
        + out["Remission_status"].astype(str)
        + "|"
        + out["state_level"].astype(str)
        + "|"
        + out["cell_state"].astype(str)
    )
    return out


def paired_delta_tests(deltas: pd.DataFrame) -> pd.DataFrame:
    filt = deltas[deltas["passes_cell_threshold"]].copy()
    rows = []
    scopes: list[tuple[str, pd.DataFrame]] = [("all", filt)]
    for disease, sub in filt.groupby("Disease", observed=True):
        scopes.append((f"disease_{disease}", sub))
    for remission, sub in filt.groupby("Remission_status", observed=True):
        scopes.append((f"outcome_{remission}", sub))
    for (disease, remission), sub in filt.groupby(["Disease", "Remission_status"], observed=True):
        scopes.append((f"{disease}_{remission}", sub))
    for scope, sub0 in scopes:
        for (state_level, cell_state, module), sub in sub0.groupby(["state_level", "cell_state", "module"], observed=True):
            vals = sub["delta_post_minus_pre"].to_numpy(float)
            vals = vals[np.isfinite(vals)]
            if len(vals) >= 4:
                t_stat, p_value = stats.ttest_1samp(vals, 0.0, nan_policy="omit")
            else:
                t_stat, p_value = np.nan, np.nan
            rows.append(
                {
                    "scope": scope,
                    "state_level": state_level,
                    "cell_state": cell_state,
                    "module": module,
                    "n_pairs": int(len(vals)),
                    "n_patients": int(sub["Patient"].nunique()),
                    "mean_delta": float(np.nanmean(vals)) if len(vals) else np.nan,
                    "median_delta": float(np.nanmedian(vals)) if len(vals) else np.nan,
                    "paired_t": float(t_stat) if np.isfinite(t_stat) else np.nan,
                    "p": float(p_value) if np.isfinite(p_value) else np.nan,
                    "all_same_positive": bool((vals > 0).all()) if len(vals) else False,
                    "all_same_negative": bool((vals < 0).all()) if len(vals) else False,
                }
            )
    out = pd.DataFrame(rows)
    if not out.empty:
        out["fdr"] = bh_fdr(out["p"])
    return out


def patient_collapsed_wide(deltas: pd.DataFrame) -> pd.DataFrame:
    filt = deltas[deltas["passes_cell_threshold"]].copy()
    collapse_cols = ["Patient", "Disease", "Remission_status", "state_level", "cell_state", "module"]
    collapsed = (
        filt.groupby(collapse_cols, observed=True, dropna=False)
        .agg(
            delta_post_minus_pre=("delta_post_minus_pre", "mean"),
            pre_score=("pre_score", "mean"),
            baseline_inflammation_score=("baseline_inflammation_score", "mean"),
            n_sites=("Site", "nunique"),
            min_n_cells=("min_n_cells", "min"),
        )
        .reset_index()
    )
    wide_delta = collapsed.pivot_table(
        index=["Patient", "Disease", "Remission_status", "state_level", "cell_state"],
        columns="module",
        values="delta_post_minus_pre",
        aggfunc="first",
    ).reset_index()
    wide_pre = collapsed.pivot_table(
        index=["Patient", "Disease", "Remission_status", "state_level", "cell_state"],
        columns="module",
        values="pre_score",
        aggfunc="first",
    ).reset_index()
    wide_pre = wide_pre.rename(columns={col: f"pre_{col}" for col in wide_pre.columns if col not in {"Patient", "Disease", "Remission_status", "state_level", "cell_state"}})
    meta = (
        collapsed.groupby(["Patient", "Disease", "Remission_status", "state_level", "cell_state"], observed=True)
        .agg(
            baseline_inflammation_score=("baseline_inflammation_score", "mean"),
            n_sites=("n_sites", "sum"),
            min_n_cells=("min_n_cells", "min"),
        )
        .reset_index()
    )
    return wide_delta.merge(wide_pre, on=["Patient", "Disease", "Remission_status", "state_level", "cell_state"]).merge(
        meta, on=["Patient", "Disease", "Remission_status", "state_level", "cell_state"]
    )


def response_interaction_tests(deltas: pd.DataFrame) -> pd.DataFrame:
    wide = patient_collapsed_wide(deltas)
    rows = []
    for (state_level, cell_state), sub0 in wide.groupby(["state_level", "cell_state"], observed=True):
        for module in [m for m in TARGET_MODULES + GENERIC_MODULES if m in sub0.columns]:
            sub = sub0.copy()
            if module not in sub.columns:
                continue
            sub["target_delta"] = pd.to_numeric(sub[module], errors="coerce")
            pre_col = f"pre_{module}"
            sub["baseline_target"] = pd.to_numeric(sub[pre_col], errors="coerce") if pre_col in sub.columns else np.nan
            generic_cols = [m for m in GENERIC_MODULES if m in sub.columns and m != module]
            sub["generic_delta"] = sub[generic_cols].apply(pd.to_numeric, errors="coerce").mean(axis=1) if generic_cols else np.nan
            sub["remission_binary"] = sub["Remission_status"].eq("Remission").astype(int)
            yes = sub.loc[sub["remission_binary"].eq(1), "target_delta"].to_numpy(float)
            no = sub.loc[sub["remission_binary"].eq(0), "target_delta"].to_numpy(float)
            yes = yes[np.isfinite(yes)]
            no = no[np.isfinite(no)]
            if len(yes) >= 4 and len(no) >= 4:
                t_stat, p_value = stats.ttest_ind(yes, no, equal_var=False, nan_policy="omit")
            else:
                t_stat, p_value = np.nan, np.nan
            adjusted_delta = np.nan
            adjusted_p = np.nan
            formula_used = ""
            df = sub[["target_delta", "remission_binary", "Disease", "baseline_target", "generic_delta", "baseline_inflammation_score"]].copy()
            df = df.replace([np.inf, -np.inf], np.nan).dropna(subset=["target_delta", "remission_binary"])
            if (
                len(df) >= 12
                and df["remission_binary"].nunique() == 2
                and df["remission_binary"].value_counts().min() >= 4
            ):
                formula = "target_delta ~ remission_binary"
                if df["baseline_target"].notna().sum() >= 10:
                    formula += " + baseline_target"
                if df["generic_delta"].notna().sum() >= 10:
                    formula += " + generic_delta"
                if df["baseline_inflammation_score"].notna().sum() >= 10:
                    formula += " + baseline_inflammation_score"
                if df["Disease"].nunique() > 1:
                    formula += " + C(Disease)"
                try:
                    fit = ols(formula, data=df).fit()
                    adjusted_delta = float(fit.params.get("remission_binary", np.nan))
                    adjusted_p = float(fit.pvalues.get("remission_binary", np.nan))
                    formula_used = formula
                except Exception:  # noqa: BLE001
                    formula_used = f"failed: {formula}"
            rows.append(
                {
                    "state_level": state_level,
                    "cell_state": cell_state,
                    "module": module,
                    "n_patient_units": int(len(sub)),
                    "n_remission": int(np.isfinite(yes).sum()),
                    "n_non_remission": int(np.isfinite(no).sum()),
                    "mean_delta_remission": float(np.nanmean(yes)) if len(yes) else np.nan,
                    "mean_delta_non_remission": float(np.nanmean(no)) if len(no) else np.nan,
                    "raw_delta_remission_minus_non": float(np.nanmean(yes) - np.nanmean(no)) if len(yes) and len(no) else np.nan,
                    "raw_hedges_g": hedges_g(yes, no),
                    "raw_t": float(t_stat) if np.isfinite(t_stat) else np.nan,
                    "raw_p": float(p_value) if np.isfinite(p_value) else np.nan,
                    "generic_adjusted_delta": adjusted_delta,
                    "generic_adjusted_p": adjusted_p,
                    "generic_covariates": ",".join(generic_cols),
                    "formula_used": formula_used,
                }
            )
    out = pd.DataFrame(rows)
    if not out.empty:
        out["raw_fdr"] = bh_fdr(out["raw_p"])
        out["generic_adjusted_fdr"] = bh_fdr(out["generic_adjusted_p"])
    return out


def gate_summary(pd_tests: pd.DataFrame, response_tests: pd.DataFrame) -> pd.DataFrame:
    rows = []
    all_pd = pd_tests[pd_tests["scope"].eq("all") & pd_tests["state_level"].eq("major")].copy()
    generic_effects = {
        state: float(sub.loc[sub["module"].isin(GENERIC_MODULES), "mean_delta"].abs().max())
        for state, sub in all_pd.groupby("cell_state", observed=True)
    }
    for state in sorted(PRIMARY_STATES):
        for module in TARGET_MODULES:
            pd_row = all_pd[all_pd["cell_state"].eq(state) & all_pd["module"].eq(module)]
            resp = response_tests[
                response_tests["state_level"].eq("major")
                & response_tests["cell_state"].eq(state)
                & response_tests["module"].eq(module)
            ]
            generic_max = generic_effects.get(state, np.nan)
            effect = float(pd_row["mean_delta"].iloc[0]) if not pd_row.empty else np.nan
            target_to_generic = abs(effect) / generic_max if np.isfinite(effect) and np.isfinite(generic_max) and generic_max > 0 else np.nan
            failed = []
            n_pairs = int(pd_row["n_pairs"].iloc[0]) if not pd_row.empty else 0
            n_patients = int(pd_row["n_patients"].iloc[0]) if not pd_row.empty else 0
            paired_fdr = float(pd_row["fdr"].iloc[0]) if not pd_row.empty else np.nan
            adjusted_fdr = float(resp["generic_adjusted_fdr"].iloc[0]) if not resp.empty else np.nan
            raw_response_fdr = float(resp["raw_fdr"].iloc[0]) if not resp.empty else np.nan
            if n_pairs < 20 or n_patients < 10:
                failed.append("insufficient_primary_pair_support")
            if not (np.isfinite(paired_fdr) and paired_fdr <= 0.10):
                failed.append("no_all_pair_fdr10_pharmacodynamic_delta")
            if not (np.isfinite(target_to_generic) and target_to_generic >= 2.0):
                failed.append("target_to_generic_delta_ratio_lt_2")
            if not (np.isfinite(adjusted_fdr) and adjusted_fdr <= 0.10):
                failed.append("no_remission_interaction_after_generic_adjustment")
            # Cross-disease stability from all-pair disease-specific rows.
            disease_rows = pd_tests[
                pd_tests["scope"].isin(["disease_CD", "disease_UC"])
                & pd_tests["state_level"].eq("major")
                & pd_tests["cell_state"].eq(state)
                & pd_tests["module"].eq(module)
            ]
            disease_effects = disease_rows.set_index("scope")["mean_delta"].to_dict()
            if len(disease_effects) < 2 or np.sign(disease_effects.get("disease_CD", np.nan)) != np.sign(
                disease_effects.get("disease_UC", np.nan)
            ):
                failed.append("cd_uc_effect_direction_not_stable")
            if failed:
                call = "PARK_CELL_RESOLVED_PD_SIGNAL_ONLY" if len(failed) <= 3 else "NO_GO_GSE282122_MYELOID"
            else:
                call = "REOPEN_CELL_RESOLVED_PERTURBATION_AXIS"
            rows.append(
                {
                    "cell_state": state,
                    "module": module,
                    "n_pairs": n_pairs,
                    "n_patients": n_patients,
                    "all_pair_mean_delta": effect,
                    "all_pair_fdr": paired_fdr,
                    "max_generic_all_pair_delta_abs": generic_max,
                    "target_to_generic_delta_ratio": target_to_generic,
                    "raw_remission_response_fdr": raw_response_fdr,
                    "generic_adjusted_remission_response_fdr": adjusted_fdr,
                    "cd_mean_delta": disease_effects.get("disease_CD", np.nan),
                    "uc_mean_delta": disease_effects.get("disease_UC", np.nan),
                    "wave67_call": call,
                    "failed_gates": ";".join(failed),
                }
            )
    return pd.DataFrame(rows).sort_values(["wave67_call", "all_pair_fdr", "generic_adjusted_remission_response_fdr"])


def write_report(
    obs: pd.DataFrame,
    paired: pd.DataFrame,
    gene_presence: pd.DataFrame,
    pseudobulk_meta: pd.DataFrame,
    deltas: pd.DataFrame,
    pd_tests: pd.DataFrame,
    response_tests: pd.DataFrame,
    gates: pd.DataFrame,
) -> None:
    top_pd = pd_tests.sort_values(["fdr", "scope", "cell_state", "module"]).head(30)
    top_resp = response_tests.sort_values(["generic_adjusted_fdr", "raw_fdr"]).head(20)
    lines = [
        "# Wave67 GSE282122 Myeloid Pseudobulk Audit",
        "",
        f"Random seed: `{SEED}`.",
        "",
        "## Data",
        "",
        "- Accession context: `GSE282122`; processed myeloid object from Zenodo record `14007626`.",
        f"- Myeloid h5ad: `{rel(MYELOID_FILE)}`.",
        f"- Paired manifest: `{rel(PAIRED_FILE)}`.",
        f"- Cells in paired myeloid analysis strata: `{len(obs)}`.",
        f"- Paired manifest samples: `{paired['sample_id'].nunique()}`.",
        f"- Pseudobulk strata: `{len(pseudobulk_meta)}`.",
        f"- Site/state/module deltas: `{len(deltas)}`.",
        "",
        "## Gate Summary",
        "",
        "| cell state | module | n pairs | n patients | all delta | all FDR | target/generic | adjusted response FDR | call | failed gates |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for row in gates.itertuples(index=False):
        lines.append(
            f"| {row.cell_state} | {row.module} | {row.n_pairs} | {row.n_patients} | "
            f"{row.all_pair_mean_delta:.4g} | {row.all_pair_fdr:.4g} | "
            f"{row.target_to_generic_delta_ratio:.4g} | {row.generic_adjusted_remission_response_fdr:.4g} | "
            f"{row.wave67_call} | {row.failed_gates} |"
        )
    lines.extend(["", "## Top Paired Pharmacodynamic Tests", ""])
    lines.extend(
        [
            "| scope | state | module | n pairs | n patients | mean delta | p | FDR |",
            "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in top_pd.itertuples(index=False):
        lines.append(
            f"| {row.scope} | {row.cell_state} | {row.module} | {row.n_pairs} | {row.n_patients} | "
            f"{row.mean_delta:.4g} | {row.p:.4g} | {row.fdr:.4g} |"
        )
    lines.extend(["", "## Top Remission-Interaction Tests", ""])
    lines.extend(
        [
            "| state | module | n | remission delta | nonremission delta | adjusted delta | adjusted FDR | formula |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for row in top_resp.itertuples(index=False):
        lines.append(
            f"| {row.cell_state} | {row.module} | {row.n_patient_units} | {row.mean_delta_remission:.4g} | "
            f"{row.mean_delta_non_remission:.4g} | {row.generic_adjusted_delta:.4g} | "
            f"{row.generic_adjusted_fdr:.4g} | {row.formula_used} |"
        )
    lines.extend(["", "## Gene Coverage", ""])
    for row in gene_presence.itertuples(index=False):
        lines.append(f"- `{row.module}`: {row.n_genes_present}/{row.n_genes_defined} genes present.")
    lines.extend(
        [
            "",
            "## Interpretation Guardrails",
            "",
            "- This is patient/site-level pseudobulk in annotated myeloid states, not single-cell causal perturbation.",
            "- Anti-TNF is a broad intervention. Module movement must exceed or survive generic TNF/NF-kB/IFN controls before a controller can be reopened.",
            "- Remission status is an outcome association and not randomized target perturbation.",
            "- Fine-state rows are secondary because many states lack enough paired cells.",
        ]
    )
    (OUT / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    download_if_missing(MYELOID_URL, MYELOID_FILE, MYELOID_MD5)
    paired = load_paired_manifest()
    adata = ad.read_h5ad(MYELOID_FILE)
    obs_all = normalize_obs(adata)
    obs = build_stratified_obs(obs_all, paired)
    gene_names, gene_indices, gene_presence = build_gene_index(adata)
    pseudobulk_meta, pseudobulk_counts = aggregate_pseudobulk(adata, obs, gene_names, gene_indices)
    scores, logcpm = compute_module_scores(pseudobulk_counts, gene_names)
    deltas = build_pair_deltas(scores)
    pd_tests = paired_delta_tests(deltas)
    response_tests = response_interaction_tests(deltas)
    gates = gate_summary(pd_tests, response_tests)

    paired.to_csv(OUT / "paired_sample_list_used.tsv", sep="\t", index=False)
    obs.to_csv(OUT / "cell_obs_used.tsv", sep="\t", index=False)
    gene_presence.to_csv(OUT / "module_gene_presence.tsv", sep="\t", index=False)
    pseudobulk_meta.to_csv(OUT / "pseudobulk_metadata.tsv", sep="\t", index=False)
    pseudobulk_counts.to_csv(OUT / "pseudobulk_module_gene_counts.tsv", sep="\t", index=False)
    logcpm.to_csv(OUT / "pseudobulk_module_gene_logcpm.tsv", sep="\t")
    scores.to_csv(OUT / "pseudobulk_module_scores.tsv", sep="\t", index=False)
    deltas.to_csv(OUT / "paired_module_deltas.tsv", sep="\t", index=False)
    pd_tests.to_csv(OUT / "paired_delta_tests.tsv", sep="\t", index=False)
    response_tests.to_csv(OUT / "remission_interaction_tests.tsv", sep="\t", index=False)
    gates.to_csv(OUT / "wave67_gate_summary.tsv", sep="\t", index=False)

    summary = {
        "seed": SEED,
        "input_accessions": ["GSE282122", "Zenodo 14007626"],
        "input_files": {
            "myeloid_h5ad": rel(MYELOID_FILE),
            "paired_manifest": rel(PAIRED_FILE),
        },
        "myeloid_md5": md5sum(MYELOID_FILE),
        "paired_manifest_md5": md5sum(PAIRED_FILE),
        "adata_shape": [int(adata.n_obs), int(adata.n_vars)],
        "n_cells_stratified": int(len(obs)),
        "n_pseudobulk_strata": int(len(pseudobulk_meta)),
        "n_delta_rows": int(len(deltas)),
        "gate_calls": gates["wave67_call"].value_counts().to_dict() if not gates.empty else {},
        "top_gates": gates.replace({np.nan: None}).to_dict(orient="records") if not gates.empty else [],
        "interpretation": (
            "Wave67 is a cell-resolved paired pseudobulk perturbation audit. "
            "It can reopen a direction only if target modules move beyond "
            "generic anti-TNF inflammatory contraction."
        ),
    }
    write_json(OUT / "summary.json", summary)
    write_report(obs, paired, gene_presence, pseudobulk_meta, deltas, pd_tests, response_tests, gates)


if __name__ == "__main__":
    main()
