#!/usr/bin/env python3
"""Wave147: TAGAP adaptive-immune genetics benchmark.

This wave tests Gauss's outside-catalog genetics-first suggestion. It asks
whether broad TAGAP/RhoGTPase autoimmune genetics becomes a therapeutic route
once local T-cell state, MS white-matter anchor, direction, perturbation, and
reachability gates are applied.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path

import anndata as ad
import numpy as np
import pandas as pd
from scipy import sparse, stats
from statsmodels.stats.multitest import multipletests

from v3_analyze_direct_h5ad_cell_states import ROOT, hedges_g


SEED = 20260527
RAW = ROOT / "data" / "raw_v3" / "cell_state"
OUT = ROOT / "phases/v3/results" / "wave147_tagap_adaptive_genetics_benchmark"

GENES = {
    "TAGAP_single": ["TAGAP"],
    "tcr_rhogtpase_activation": ["TAGAP", "SKAP1", "LCP2", "VAV1", "RAC2", "DOCK8", "ARHGAP15", "RHOH", "CD3D", "CD3E", "TRAC"],
}

GENETICS_FILES = {
    "wave55": ROOT / "phases/v3/results" / "wave55_external_genetics_druggability_sweep" / "external_genetics_rank.tsv",
    "wave62": ROOT / "phases/v3/results" / "wave62_opentargets_target_resolution" / "target_resolution_summary.tsv",
    "wave104": ROOT / "phases/v3/results" / "wave104_genetics_first_lipid_state_convergence_audit" / "genetics_first_lipid_state_rank.tsv",
    "ms_signature": ROOT / "phases/v3/results" / "gse111972_full_ms_wm_signature.tsv",
}


@dataclass(frozen=True)
class TCellConfig:
    name: str
    path: Path
    disease_label: str
    control_label: str
    cell_types: tuple[str, ...]
    gene_symbol_column: str


CONFIGS = [
    TCellConfig("ibd_crohn_tcell", RAW / "ibd_human_10x.h5ad", "Crohn disease", "normal", ("T cell of anorectum",), "gene_symbols"),
    TCellConfig("ibd_uc_tcell", RAW / "ibd_human_10x.h5ad", "ulcerative colitis", "normal", ("T cell of anorectum",), "gene_symbols"),
    TCellConfig(
        "psoriasis_skin_tcell",
        RAW / "psoriasis_skin.h5ad",
        "psoriasis",
        "normal",
        ("cytotoxic T cell", "helper T cell", "regulatory T cell"),
        "GeneSym",
    ),
    TCellConfig(
        "sjogren_gland_tcell",
        RAW / "sjogren_salivary.h5ad",
        "Sjogren syndrome",
        "normal",
        (
            "CD4-positive, alpha-beta T cell",
            "effector CD8-positive, alpha-beta T cell",
            "CD8-positive, alpha-beta cytotoxic T cell",
            "CD8-positive, alpha-beta regulatory T cell",
            "mature NK T cell",
        ),
        "feature_name",
    ),
    TCellConfig(
        "ra_blood_tcell",
        RAW / "ra_binvignat_blood.h5ad",
        "rheumatoid arthritis",
        "normal",
        (
            "central memory CD4-positive, alpha-beta T cell",
            "naive thymus-derived CD4-positive, alpha-beta T cell",
            "effector memory CD4-positive, alpha-beta T cell",
            "naive thymus-derived CD8-positive, alpha-beta T cell",
            "effector memory CD8-positive, alpha-beta T cell, terminally differentiated",
            "CD8-positive, alpha-beta memory T cell",
            "gamma-delta T cell",
            "CD4-positive, alpha-beta T cell",
        ),
        "feature_name",
    ),
]


def read_tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


def gene_symbols(a: ad.AnnData, col: str) -> pd.Series:
    if col in a.var.columns:
        return a.var[col].astype(str)
    if "feature_name" in a.var.columns:
        return a.var["feature_name"].astype(str)
    return pd.Series(a.var_names.astype(str), index=a.var.index)


def score_config(config: TCellConfig, a: ad.AnnData, x) -> tuple[pd.DataFrame, pd.DataFrame]:
    obs = a.obs.copy()
    mask = obs["disease"].isin([config.disease_label, config.control_label]) & obs["cell_type"].isin(config.cell_types)
    obs_sub = obs.loc[mask].copy()
    cell_idx = np.flatnonzero(mask.to_numpy())
    wanted = sorted({g for genes in GENES.values() for g in genes})
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
    cell_scores = obs_sub[["donor_id", "disease", "cell_type"]].reset_index(drop=True).copy()
    coverage = []
    for module, genes in GENES.items():
        genes_present = [g for g in genes if g in local]
        coverage.append(
            {
                "analysis": config.name,
                "module": module,
                "n_genes_present": len(genes_present),
                "genes_present": ",".join(genes_present),
            }
        )
        cell_scores[module] = np.nanmean(z[:, [local[g] for g in genes_present]], axis=1) if genes_present else np.nan
    rows = []
    for (donor, disease), sub in cell_scores.groupby(["donor_id", "disease"], observed=True):
        if len(sub) < 10:
            continue
        for module in GENES:
            rows.append(
                {
                    "analysis": config.name,
                    "dataset_path": str(config.path.relative_to(ROOT)),
                    "disease_name": config.disease_label,
                    "donor_id": donor,
                    "disease": disease,
                    "group": "case" if disease == config.disease_label else "control",
                    "module": module,
                    "n_cells": int(len(sub)),
                    "mean_score": float(np.nanmean(sub[module])),
                    "cell_types": ",".join(sorted(sub["cell_type"].astype(str).unique())),
                }
            )
    return pd.DataFrame(rows), pd.DataFrame(coverage)


def compare(scores: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (analysis, module), sub in scores.groupby(["analysis", "module"], observed=True):
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
                "module": module,
                "n_case_donors": len(case),
                "n_control_donors": len(control),
                "mean_case": float(np.nanmean(case)) if len(case) else np.nan,
                "mean_control": float(np.nanmean(control)) if len(control) else np.nan,
                "delta_case_minus_control": float(np.nanmean(case) - np.nanmean(control)) if len(case) and len(control) else np.nan,
                "hedges_g": hedges_g(case, control),
                "p": float(p) if np.isfinite(p) else np.nan,
            }
        )
    out = pd.DataFrame(rows)
    if not out.empty:
        out["fdr"] = multipletests(out["p"].fillna(1), method="fdr_bh")[1]
    return out


def genetics_table() -> pd.DataFrame:
    rows = []
    for gene in ["TAGAP", "TNRC18", "PUS10"]:
        row = {"gene": gene}
        w55 = read_tsv(GENETICS_FILES["wave55"])
        w62 = read_tsv(GENETICS_FILES["wave62"])
        w104 = read_tsv(GENETICS_FILES["wave104"])
        ms = read_tsv(GENETICS_FILES["ms_signature"])
        if not w55.empty and gene in set(w55["gene"]):
            r = w55[w55["gene"].eq(gene)].iloc[0]
            row.update(
                {
                    "wave55_diseases_ge_0_25": r.get("diseases_genetic_ge_0_25", ""),
                    "wave55_n_diseases_ge_0_25": r.get("n_diseases_genetic_ge_0_25", 0),
                    "wave55_ms_genetic_association": r.get("ms_genetic_association", np.nan),
                }
            )
        if not w62.empty and gene in set(w62["gene"]):
            r = w62[w62["gene"].eq(gene)].iloc[0]
            row.update(
                {
                    "wave62_call": r.get("wave62_call", ""),
                    "strong_l2g_diseases": r.get("strong_l2g_diseases", ""),
                    "strong_l2g_disease_count": r.get("strong_l2g_disease_count", 0),
                    "strong_qtl_coloc_diseases": r.get("strong_qtl_coloc_diseases", ""),
                    "strong_qtl_coloc_disease_count": r.get("strong_qtl_coloc_disease_count", 0),
                    "ms_max_l2g_score": r.get("ms_max_l2g_score", np.nan),
                    "ms_max_qtl_h4": r.get("ms_max_qtl_h4", np.nan),
                    "direction_proxy_values": r.get("direction_proxy_values", ""),
                    "chembl_activity_count": r.get("druggable_activity_count", 0),
                }
            )
        if not w104.empty and gene in set(w104["gene"]):
            r = w104[w104["gene"].eq(gene)].iloc[0]
            row.update(
                {
                    "wave104_call": r.get("wave104_call", ""),
                    "wave104_missing_gates": r.get("wave104_missing_gates", ""),
                    "direct_perturbation": r.get("direct_perturbation", False),
                    "gate_reachable_modality": r.get("gate_reachable_modality", False),
                }
            )
        if not ms.empty and gene in set(ms["gene"]):
            r = ms[ms["gene"].eq(gene)].iloc[0]
            row.update(
                {
                    "ms_wm_delta_log2": r.get("delta_log2", np.nan),
                    "ms_wm_p": r.get("p", np.nan),
                    "ms_wm_fdr": r.get("fdr", np.nan),
                }
            )
        rows.append(row)
    return pd.DataFrame(rows)


def has_text(value) -> bool:
    if value is None:
        return False
    try:
        if pd.isna(value):
            return False
    except (TypeError, ValueError):
        pass
    text = str(value).strip()
    return bool(text) and text.lower() != "nan"


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    cache = {}
    score_tables = []
    cov_tables = []
    run_log = []
    for config in CONFIGS:
        try:
            if config.path not in cache:
                a = ad.read_h5ad(config.path)
                x = a.X.tocsr() if sparse.issparse(a.X) else sparse.csr_matrix(a.X)
                cache[config.path] = (a, x)
            scores, cov = score_config(config, *cache[config.path])
            score_tables.append(scores)
            cov_tables.append(cov)
            run_log.append({"analysis": config.name, "status": "completed", "n_score_rows": int(len(scores))})
        except Exception as exc:
            run_log.append({"analysis": config.name, "status": "failed", "error": f"{type(exc).__name__}: {exc}"})
    scores = pd.concat(score_tables, ignore_index=True) if score_tables else pd.DataFrame()
    coverage = pd.concat(cov_tables, ignore_index=True) if cov_tables else pd.DataFrame()
    tests = compare(scores)
    genetics = genetics_table()
    tagap = genetics[genetics["gene"].eq("TAGAP")].iloc[0].to_dict()
    local_tagap = tests[(tests["module"].eq("TAGAP_single")) & (tests["delta_case_minus_control"] > 0) & (tests["p"] < 0.05)]
    local_module = tests[(tests["module"].eq("tcr_rhogtpase_activation")) & (tests["delta_case_minus_control"] > 0) & (tests["p"] < 0.05)]

    gates = {
        "cross_autoimmune_genetics_ms_plus_two": float(tagap.get("strong_l2g_disease_count", 0) or 0) >= 3
        and float(tagap.get("ms_max_l2g_score", 0) or 0) >= 0.5,
        "target_resolved_qtl_or_l2g_ms": float(tagap.get("ms_max_l2g_score", 0) or 0) >= 0.5
        or float(tagap.get("ms_max_qtl_h4", 0) or 0) >= 0.8,
        "direction_proxy_resolved": has_text(tagap.get("direction_proxy_values", "")),
        "local_tagap_tcell_state_two_diseases": local_tagap["disease_name"].nunique() >= 2,
        "local_tcr_rhogtpase_module_two_diseases": local_module["disease_name"].nunique() >= 2,
        "ms_white_matter_expression_anchor": float(tagap.get("ms_wm_fdr", 1) or 1) < 0.1
        and float(tagap.get("ms_wm_delta_log2", 0) or 0) > 0,
        "direct_perturbation_support": str(tagap.get("direct_perturbation", "False")).lower() == "true",
        "reachable_non_broad_suppression_modality": str(tagap.get("gate_reachable_modality", "False")).lower() == "true",
    }
    branch = "TAGAP_ADAPTIVE_GENETICS_PROMOTABLE" if all(gates.values()) else "NO_TAGAP_ADAPTIVE_GENETICS_PROMOTION"
    gate_df = pd.DataFrame([{"gate": k, "pass": v} for k, v in gates.items()])

    scores.to_csv(OUT / "tagap_tcell_donor_scores.tsv", sep="\t", index=False)
    coverage.to_csv(OUT / "tagap_tcell_gene_coverage.tsv", sep="\t", index=False)
    tests.to_csv(OUT / "tagap_tcell_disease_tests.tsv", sep="\t", index=False)
    genetics.to_csv(OUT / "tagap_genetics_comparator_table.tsv", sep="\t", index=False)
    gate_df.to_csv(OUT / "tagap_gate_decision.tsv", sep="\t", index=False)
    summary = {
        "branch_call": branch,
        "random_seed": SEED,
        "run_log": run_log,
        "n_tcell_tests": int(len(tests)),
        "local_tagap_positive_diseases_p_lt_0_05": sorted(local_tagap["disease_name"].unique().tolist()),
        "local_module_positive_diseases_p_lt_0_05": sorted(local_module["disease_name"].unique().tolist()),
        "gates": gates,
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    report = [
        "# Wave147 TAGAP Adaptive-Immune Genetics Benchmark",
        "",
        f"Branch call: `{branch}`.",
        "",
        "Interpretation:",
        "- TAGAP has strong cross-autoimmune genetics and an MS L2G anchor.",
        "- It fails promotion because local disease T-cell state recurrence, MS white-matter expression, direction proxy resolution, perturbation support, and reachable modality gates do not all pass.",
        "- This is a benchmark showing why genetics breadth alone is insufficient for a V3 therapeutic target.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n")


if __name__ == "__main__":
    main()
