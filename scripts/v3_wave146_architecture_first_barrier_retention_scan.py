#!/usr/bin/env python3
"""Wave146: architecture-first barrier/retention forcing scan.

This wave follows the post-Wave145 sidecar recommendation. It does not reuse
the lipid/APC intervention catalog as the candidate source. Instead it scores
predefined tissue-interface modules in local h5ad atlases, tests whether source
compartment module activity is disease-up, and asks whether it predicts paired
myeloid/APC target states after generic covariate adjustment.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import anndata as ad
import numpy as np
import pandas as pd
from scipy import sparse, stats
from statsmodels.stats.multitest import multipletests

from v3_analyze_direct_h5ad_cell_states import CONFIGS, MODULES as TARGET_MODULES, ROOT, hedges_g


SEED = 20260527
OUT = ROOT / "results_v3" / "wave146_architecture_first_barrier_retention_scan"
MS_SIG = ROOT / "results_v3" / "gse111972_full_ms_wm_signature.tsv"

ARCH_MODULES = {
    "endothelial_entry": ["ANGPT2", "ICAM1", "VCAM1", "SELE", "MADCAM1"],
    "stromal_retention_fibrosis": ["ITGAV", "ITGB1", "TGFB1", "TGFB2", "TGFB3", "SERPINE1", "PDPN", "COL1A1"],
    "epithelial_chemokine_entry": ["CCL20", "CXCL1", "CXCL2", "CXCL3"],
    "tls_lymphoid_niche": ["CXCL13", "CCL19", "CCL21", "LTB", "LTBR", "TNFSF14"],
    "tl1a_comparator": ["TNFSF15", "TNFRSF25"],
}

TARGET_READOUTS = ["inflammatory_nfkb", "lysosomal_apc", "ifn_apc", "hla_ii_apc"]
SOURCE_ROLE = {
    "ibd_crohn_myeloid": "target",
    "ibd_uc_myeloid": "target",
    "psoriasis_skin_apc": "target",
    "sjogren_gland_apc": "target",
    "ra_blood_myeloid": "target",
}
MIN_DONORS = 6


def gene_symbols(a: ad.AnnData, col: str) -> pd.Series:
    if col in a.var.columns:
        return a.var[col].astype(str)
    if "feature_name" in a.var.columns:
        return a.var["feature_name"].astype(str)
    return pd.Series(a.var_names.astype(str), index=a.var.index)


def read_counts(path: Path):
    a = ad.read_h5ad(path)
    x = a.X.tocsr() if sparse.issparse(a.X) else sparse.csr_matrix(a.X)
    return a, x


def score_config(config, a, x) -> tuple[pd.DataFrame, pd.DataFrame]:
    obs = a.obs.copy()
    mask = obs["disease"].isin([config.disease_label, config.control_label]) & obs["cell_type"].isin(config.cell_types)
    obs_sub = obs.loc[mask].copy()
    cell_idx = np.flatnonzero(mask.to_numpy())
    wanted = sorted({g for genes in ARCH_MODULES.values() for g in genes} | {g for genes in TARGET_MODULES.values() for g in genes})
    symbols = gene_symbols(a, config.gene_symbol_column)
    gene_idx = {}
    for idx, symbol in enumerate(symbols):
        if symbol in wanted and symbol not in gene_idx:
            gene_idx[symbol] = idx
    present = sorted(gene_idx)
    if len(obs_sub) == 0 or not present:
        return pd.DataFrame(), pd.DataFrame()
    target_x = x[cell_idx][:, [gene_idx[g] for g in present]].astype(float)
    lib = np.asarray(x[cell_idx].sum(axis=1)).ravel().astype(float)
    lib[~np.isfinite(lib) | (lib <= 0)] = np.nan
    normalized = target_x.multiply(np.divide(1.0, lib, out=np.zeros_like(lib), where=np.isfinite(lib))[:, None]).multiply(1e4)
    log_expr = np.log1p(normalized.toarray())
    normal = obs_sub["disease"].eq(config.control_label).to_numpy()
    means = np.nanmean(log_expr[normal], axis=0)
    sds = np.nanstd(log_expr[normal], axis=0, ddof=1)
    sds[~np.isfinite(sds) | (sds < 1e-6)] = 1.0
    z = (log_expr - means) / sds
    local = {g: i for i, g in enumerate(present)}

    module_defs = {**ARCH_MODULES, **{f"target_{k}": v for k, v in TARGET_MODULES.items()}}
    cell_scores = obs_sub[["donor_id", "disease", "cell_type"]].reset_index(drop=True).copy()
    gene_rows = []
    for module, genes in module_defs.items():
        genes_present = [g for g in genes if g in local]
        gene_rows.append(
            {
                "analysis": config.name,
                "module": module,
                "n_genes_present": len(genes_present),
                "genes_present": ",".join(genes_present),
            }
        )
        if genes_present:
            cell_scores[module] = np.nanmean(z[:, [local[g] for g in genes_present]], axis=1)
        else:
            cell_scores[module] = np.nan

    rows = []
    role = SOURCE_ROLE.get(config.name, "source")
    for (donor, disease), sub in cell_scores.groupby(["donor_id", "disease"], observed=True):
        if len(sub) < 10:
            continue
        base = {
            "analysis": config.name,
            "dataset_path": str(config.path.relative_to(ROOT)),
            "disease_name": config.disease_label,
            "compartment": config.compartment,
            "donor_id": donor,
            "disease": disease,
            "group": "case" if disease == config.disease_label else "control",
            "role": role,
            "n_cells": int(len(sub)),
            "cell_types": ",".join(sorted(sub["cell_type"].astype(str).unique())),
        }
        for module in module_defs:
            rows.append({**base, "module": module, "mean_score": float(np.nanmean(sub[module]))})
    return pd.DataFrame(rows), pd.DataFrame(gene_rows)


def compare_modules(scores: pd.DataFrame) -> pd.DataFrame:
    rows = []
    source = scores[scores["role"].eq("source") & scores["module"].isin(ARCH_MODULES)].copy()
    for (analysis, module), sub in source.groupby(["analysis", "module"], observed=True):
        case = sub.loc[sub["group"].eq("case"), "mean_score"].to_numpy(float)
        control = sub.loc[sub["group"].eq("control"), "mean_score"].to_numpy(float)
        t, p = (np.nan, np.nan)
        if len(case) >= 2 and len(control) >= 2:
            t, p = stats.ttest_ind(case, control, equal_var=False, nan_policy="omit")
        first = sub.iloc[0]
        rows.append(
            {
                "analysis": analysis,
                "disease_name": first["disease_name"],
                "compartment": first["compartment"],
                "module": module,
                "n_case_donors": len(case),
                "n_control_donors": len(control),
                "delta_case_minus_control": float(np.nanmean(case) - np.nanmean(control)) if len(case) and len(control) else np.nan,
                "hedges_g": hedges_g(case, control),
                "p": float(p) if np.isfinite(p) else np.nan,
            }
        )
    out = pd.DataFrame(rows)
    if not out.empty:
        out["fdr"] = multipletests(out["p"].fillna(1), method="fdr_bh")[1]
    return out


def paired_tests(scores: pd.DataFrame) -> pd.DataFrame:
    wide = scores.pivot_table(
        index=["dataset_path", "disease_name", "donor_id", "group", "analysis", "compartment", "role"],
        columns="module",
        values="mean_score",
        aggfunc="mean",
    ).reset_index()
    wide.columns.name = None
    sources = wide[wide["role"].eq("source")].copy()
    targets = wide[wide["role"].eq("target")].copy()
    rows = []
    for _, s_meta in sources[["dataset_path", "disease_name", "analysis", "compartment"]].drop_duplicates().iterrows():
        source_sub = sources[
            sources["dataset_path"].eq(s_meta["dataset_path"])
            & sources["disease_name"].eq(s_meta["disease_name"])
            & sources["analysis"].eq(s_meta["analysis"])
        ]
        target_sub = targets[targets["dataset_path"].eq(s_meta["dataset_path"]) & targets["disease_name"].eq(s_meta["disease_name"])]
        for _, t_meta in target_sub[["analysis", "compartment"]].drop_duplicates().iterrows():
            t_sub = target_sub[target_sub["analysis"].eq(t_meta["analysis"])]
            merged = source_sub.merge(
                t_sub,
                on=["dataset_path", "disease_name", "donor_id", "group"],
                suffixes=("_source", "_target"),
            )
            if len(merged) < MIN_DONORS:
                continue
            merged["case_indicator"] = merged["group"].eq("case").astype(float)
            for arch in ARCH_MODULES:
                x_col = f"{arch}_source" if f"{arch}_source" in merged.columns else arch
                x = pd.to_numeric(merged[x_col], errors="coerce").to_numpy(float)
                for readout in TARGET_READOUTS:
                    ycol = f"target_{readout}"
                    y_col = f"{ycol}_target" if f"{ycol}_target" in merged.columns else ycol
                    y = pd.to_numeric(merged[y_col], errors="coerce").to_numpy(float)
                    covars = ["case_indicator"]
                    for cov in ["target_inflammatory_nfkb", "target_hif_nampt_metabolic", "target_ifn_apc", "target_hla_ii_apc"]:
                        cov_col = f"{cov}_target" if f"{cov}_target" in merged.columns else cov
                        if cov != ycol and cov_col in merged.columns:
                            covars.append(cov_col)
                    for cov in ["target_lipid_loader_repair", "target_lysosomal_apc"]:
                        cov_col = f"{cov}_target" if f"{cov}_target" in merged.columns else cov
                        if cov != ycol and cov_col in merged.columns:
                            covars.append(cov_col)
                    design_cols = [np.ones(len(merged)), x]
                    covar_used = []
                    for cov in covars:
                        vals = pd.to_numeric(merged[cov], errors="coerce").to_numpy(float)
                        if np.isfinite(vals).sum() >= MIN_DONORS and np.nanstd(vals[np.isfinite(vals)]) > 1e-8:
                            design_cols.append(vals)
                            covar_used.append(cov)
                    design = np.column_stack(design_cols)
                    mask = np.isfinite(y) & np.all(np.isfinite(design), axis=1)
                    n = int(mask.sum())
                    p = slope = r2 = math.nan
                    if n >= max(MIN_DONORS, design.shape[1] + 3) and np.nanstd(x[mask]) > 1e-8 and np.nanstd(y[mask]) > 1e-8:
                        beta, *_ = np.linalg.lstsq(design[mask], y[mask], rcond=None)
                        resid = y[mask] - design[mask] @ beta
                        df = n - design.shape[1]
                        sigma2 = float(np.sum(resid**2) / df) if df > 0 else math.nan
                        xtx_inv = np.linalg.pinv(design[mask].T @ design[mask])
                        se = math.sqrt(max(0.0, sigma2 * xtx_inv[1, 1])) if np.isfinite(sigma2) else math.nan
                        slope = float(beta[1])
                        t = slope / se if se and se > 0 else math.nan
                        p = float(2 * stats.t.sf(abs(t), df)) if np.isfinite(t) and df > 0 else math.nan
                        ss_res = float(np.sum(resid**2))
                        ss_tot = float(np.sum((y[mask] - np.mean(y[mask])) ** 2))
                        r2 = 1 - ss_res / ss_tot if ss_tot > 0 else math.nan
                    rows.append(
                        {
                            "source_analysis": s_meta["analysis"],
                            "target_analysis": t_meta["analysis"],
                            "disease_name": s_meta["disease_name"],
                            "source_compartment": s_meta["compartment"],
                            "target_compartment": t_meta["compartment"],
                            "architecture_module": arch,
                            "target_readout": readout,
                            "n_pairs": n,
                            "slope": slope,
                            "p": p,
                            "partial_model_r2": r2,
                            "covariates": ";".join(covar_used),
                        }
                    )
    out = pd.DataFrame(rows)
    if not out.empty:
        out["fdr"] = multipletests(out["p"].fillna(1), method="fdr_bh")[1]
    return out


def ms_anchor() -> pd.DataFrame:
    sig = pd.read_csv(MS_SIG, sep="\t") if MS_SIG.exists() else pd.DataFrame()
    rows = []
    for module, genes in ARCH_MODULES.items():
        sub = sig[sig["gene"].isin(genes)].copy() if not sig.empty else pd.DataFrame()
        rows.append(
            {
                "module": module,
                "n_genes_in_ms_signature": int(len(sub)),
                "mean_delta_log2": float(sub["delta_log2"].mean()) if len(sub) else math.nan,
                "min_p": float(sub["p"].min()) if len(sub) else math.nan,
                "n_nominal_positive_genes": int(((sub["delta_log2"] > 0) & (sub["p"] < 0.05)).sum()) if len(sub) else 0,
                "n_fdr_positive_genes": int(((sub["delta_log2"] > 0) & (sub["fdr"] < 0.1)).sum()) if len(sub) else 0,
                "genes_seen": ",".join(sub["gene"].astype(str).tolist()) if len(sub) else "",
            }
        )
    return pd.DataFrame(rows)


def markdown_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "_No rows._"
    cols = list(df.columns)
    lines = [
        "| " + " | ".join(cols) + " |",
        "| " + " | ".join(["---"] * len(cols)) + " |",
    ]
    for _, row in df.iterrows():
        vals = []
        for col in cols:
            val = row[col]
            if isinstance(val, float):
                vals.append(f"{val:.4g}" if np.isfinite(val) else "")
            else:
                vals.append(str(val))
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines)


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    cache = {}
    score_tables = []
    gene_tables = []
    run_log = []
    for config in CONFIGS:
        try:
            if config.path not in cache:
                cache[config.path] = read_counts(config.path)
            scores, genes = score_config(config, *cache[config.path])
            score_tables.append(scores)
            gene_tables.append(genes)
            run_log.append({"analysis": config.name, "status": "completed", "n_rows": int(len(scores))})
        except Exception as exc:
            run_log.append({"analysis": config.name, "status": "failed", "error": f"{type(exc).__name__}: {exc}"})
    scores = pd.concat(score_tables, ignore_index=True) if score_tables else pd.DataFrame()
    genes = pd.concat(gene_tables, ignore_index=True) if gene_tables else pd.DataFrame()
    disease = compare_modules(scores)
    paired = paired_tests(scores)
    ms = ms_anchor()

    disease_pass = disease[(disease["delta_case_minus_control"] > 0) & (disease["p"] < 0.05)].groupby("module")["disease_name"].nunique()
    paired_pass = paired[(paired["slope"] > 0) & (paired["p"] < 0.05)].groupby("architecture_module")["disease_name"].nunique()
    ms_pass = ms.set_index("module")["n_fdr_positive_genes"].gt(0) | (
        ms.set_index("module")["n_nominal_positive_genes"].ge(2) & ms.set_index("module")["mean_delta_log2"].gt(0)
    )
    decisions = []
    for module in ARCH_MODULES:
        dp = int(disease_pass.get(module, 0))
        pp = int(paired_pass.get(module, 0))
        mp = bool(ms_pass.get(module, False))
        direct_prior_block = module in {"epithelial_chemokine_entry", "tl1a_comparator"}
        decisions.append(
            {
                "module": module,
                "source_disease_positive_count": dp,
                "paired_receiver_positive_count": pp,
                "ms_anchor_pass": mp,
                "direct_prior_or_comparator_block": direct_prior_block,
                "passes_architecture_gate": dp >= 3 and pp >= 2 and mp and not direct_prior_block,
            }
        )
    decision_df = pd.DataFrame(decisions)
    branch = (
        "ARCHITECTURE_FIRST_MODULE_REQUIRES_TARGET_RESOLUTION"
        if decision_df["passes_architecture_gate"].any()
        else "NO_ARCHITECTURE_FIRST_BARRIER_RETENTION_TARGET"
    )

    scores.to_csv(OUT / "architecture_module_donor_scores.tsv", sep="\t", index=False)
    genes.to_csv(OUT / "architecture_module_gene_coverage.tsv", sep="\t", index=False)
    disease.to_csv(OUT / "architecture_source_disease_tests.tsv", sep="\t", index=False)
    paired.to_csv(OUT / "architecture_sender_receiver_tests.tsv", sep="\t", index=False)
    ms.to_csv(OUT / "architecture_ms_anchor.tsv", sep="\t", index=False)
    decision_df.to_csv(OUT / "architecture_gate_decision.tsv", sep="\t", index=False)
    summary = {
        "branch_call": branch,
        "random_seed": SEED,
        "run_log": run_log,
        "n_donor_score_rows": int(len(scores)),
        "n_source_tests": int(len(disease)),
        "n_sender_receiver_tests": int(len(paired)),
        "n_passing_modules": int(decision_df["passes_architecture_gate"].sum()),
        "top_source_tests": disease.sort_values(["p", "delta_case_minus_control"], ascending=[True, False]).head(10).to_dict(orient="records") if not disease.empty else [],
        "top_sender_receiver_tests": paired.sort_values(["p", "slope"], ascending=[True, False]).head(10).to_dict(orient="records") if not paired.empty else [],
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    report = [
        "# Wave146 Architecture-First Barrier/Retention Scan",
        "",
        f"Branch call: `{branch}`.",
        "",
        "Decision table:",
        "",
        markdown_table(decision_df),
        "",
        "Interpretation:",
        "- This scan is architecture-first: predefined tissue-interface modules, not lipid/APC target rows.",
        "- A module must be disease-up in at least three source compartments, predict paired myeloid/APC receiver state in at least two diseases, and have an MS white-matter anchor.",
        "- Comparator modules with direct crowded prior art are not promotable even if biologically recurrent.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n")


if __name__ == "__main__":
    main()
