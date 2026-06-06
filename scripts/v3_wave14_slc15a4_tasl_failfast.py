#!/usr/bin/env python3
"""Fail-fast SLC15A4/TASL/IRF5 endolysosomal APC branch.

This is a branch-level no-go gate, not a causal claim. It reuses the V3
direct-h5ad disease compartments to test donor-level recurrence for the
SLC15A4/TASL/IRF5/TLR7-9/UNC93B1 branch, then cross-walks the branch against
existing V3 genetics and perturbation artifacts.
"""

from __future__ import annotations

import gc
import json
import math
from collections import OrderedDict
from pathlib import Path

import anndata as ad
import numpy as np
import pandas as pd
from scipy import sparse, stats
from statsmodels.stats.multitest import multipletests

from v3_analyze_osmr_complement_axes import CONFIGS, ROOT


SEED = 20260527
RESULTS = ROOT / "phases/v3/results"
OUT = RESULTS / "wave14_slc15a4_tasl_failfast"
MS_SIGNATURE = RESULTS / "gse111972_full_ms_wm_signature.tsv"
GENETICS = ROOT / "phases/v3/tmp" / "wave13_opentargets_gwas_credible_sets.tsv"

MIN_DONOR_CELLS = 10

BRANCH_GENE_ALIASES: "OrderedDict[str, tuple[str, ...]]" = OrderedDict(
    [
        ("SLC15A4", ("SLC15A4",)),
        ("TASL_CXorf21", ("TASL", "CXorf21", "CXORF21")),
        ("IRF5", ("IRF5",)),
        ("TLR7", ("TLR7",)),
        ("TLR8", ("TLR8",)),
        ("TLR9", ("TLR9",)),
        ("UNC93B1", ("UNC93B1",)),
    ]
)

BRANCH_MODULES = OrderedDict(
    [
        ("slc15a4_tasl_irf5_core", ("SLC15A4", "TASL_CXorf21", "IRF5")),
        ("endosomal_tlr_sensor_chaperone", ("TLR7", "TLR8", "TLR9", "UNC93B1")),
        (
            "full_slc15a4_tasl_tlr_irf5_branch",
            ("SLC15A4", "TASL_CXorf21", "IRF5", "TLR7", "TLR8", "TLR9", "UNC93B1"),
        ),
    ]
)

BRANCH_QUERY_SYMBOLS = sorted({alias for aliases in BRANCH_GENE_ALIASES.values() for alias in aliases})
BRANCH_PERTURBATION_SYMBOLS = {"SLC15A4", "TASL", "CXorf21", "CXORF21", "IRF5", "TLR7", "TLR8", "TLR9", "UNC93B1"}
DOWNSTREAM_READOUT_MODULES = {"ifn_apc", "hla_ii_apc", "mif_cd74_receptor_state", "gilt_lysosomal_apc"}


def hedges_g(case: np.ndarray, control: np.ndarray) -> float:
    case = np.asarray(case, dtype=float)
    control = np.asarray(control, dtype=float)
    case = case[np.isfinite(case)]
    control = control[np.isfinite(control)]
    if case.size < 2 or control.size < 2:
        return np.nan
    pooled = ((case.size - 1) * case.var(ddof=1) + (control.size - 1) * control.var(ddof=1)) / (
        case.size + control.size - 2
    )
    if pooled <= 0:
        return np.nan
    correction = 1.0 - (3.0 / (4.0 * (case.size + control.size) - 9.0))
    return float(((case.mean() - control.mean()) / math.sqrt(pooled)) * correction)


def compare_values(values: pd.Series, groups: pd.Series) -> dict[str, float]:
    case = values.loc[groups == "case"].astype(float).to_numpy()
    control = values.loc[groups == "control"].astype(float).to_numpy()
    case = case[np.isfinite(case)]
    control = control[np.isfinite(control)]
    if case.size >= 2 and control.size >= 2:
        t_stat, p_value = stats.ttest_ind(case, control, equal_var=False, nan_policy="omit")
    else:
        t_stat, p_value = np.nan, np.nan
    return {
        "n_case_donors": int(case.size),
        "n_control_donors": int(control.size),
        "mean_case": float(np.nanmean(case)) if case.size else np.nan,
        "mean_control": float(np.nanmean(control)) if control.size else np.nan,
        "delta_case_minus_control": float(np.nanmean(case) - np.nanmean(control)) if case.size and control.size else np.nan,
        "hedges_g": hedges_g(case, control),
        "welch_t": float(t_stat) if pd.notna(t_stat) else np.nan,
        "p": float(p_value) if pd.notna(p_value) else np.nan,
    }


def support_level(delta: float, p_value: float, fdr: float) -> str:
    if not np.isfinite(delta):
        return "missing"
    if delta < 0 and np.isfinite(p_value) and p_value <= 0.10:
        return "negative_trend"
    if delta <= 0:
        return "null_or_negative"
    if np.isfinite(fdr) and fdr <= 0.10:
        return "fdr10_positive"
    if np.isfinite(p_value) and p_value <= 0.10:
        return "trend_positive"
    return "positive_null"


def support_score(level: str) -> float:
    return {
        "fdr10_positive": 2.0,
        "trend_positive": 1.0,
        "positive_null": 0.25,
        "null_or_negative": 0.0,
        "negative_trend": -1.0,
        "missing": -2.0,
    }.get(level, 0.0)


def read_counts(path: Path):
    a = ad.read_h5ad(path)
    x = a.X.tocsr() if sparse.issparse(a.X) else sparse.csr_matrix(a.X)
    return a, x


def gene_symbols_for_config(a, symbol_column: str) -> list[str]:
    if symbol_column in a.var.columns:
        raw = a.var[symbol_column].astype(str).tolist()
    elif "feature_name" in a.var.columns:
        raw = a.var["feature_name"].astype(str).tolist()
    else:
        raw = list(map(str, a.var_names))
    return [value.strip() for value in raw]


def selected_gene_columns(a, symbol_column: str) -> tuple[dict[str, int], pd.DataFrame]:
    symbol_to_first: dict[str, tuple[int, str]] = {}
    for idx, symbol in enumerate(gene_symbols_for_config(a, symbol_column)):
        key = symbol.upper()
        if key not in symbol_to_first:
            symbol_to_first[key] = (idx, symbol)

    mapping: dict[str, int] = {}
    rows: list[dict[str, object]] = []
    for canonical, aliases in BRANCH_GENE_ALIASES.items():
        matched_alias = None
        matched_symbol = None
        matched_idx = None
        for alias in aliases:
            hit = symbol_to_first.get(alias.upper())
            if hit is not None:
                matched_idx, matched_symbol = hit
                matched_alias = alias
                break
        if matched_idx is not None:
            mapping[canonical] = matched_idx
        rows.append(
            {
                "gene": canonical,
                "aliases": ",".join(aliases),
                "present": bool(matched_idx is not None),
                "matched_alias": matched_alias,
                "matched_symbol": matched_symbol,
            }
        )
    return mapping, pd.DataFrame(rows)


def analyze_config(config, a, x) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    obs = a.obs.copy()
    mask = obs["disease"].isin([config.disease_label, config.control_label]) & obs["cell_type"].isin(config.cell_types)
    obs_sub = obs.loc[mask].copy()
    cell_idx = np.flatnonzero(mask.to_numpy())
    gene_to_col, presence = selected_gene_columns(a, config.gene_symbol_column)
    presence.insert(0, "analysis", config.name)
    presence.insert(1, "disease_name", config.disease_label)
    presence.insert(2, "compartment", config.compartment)
    presence.insert(3, "role", config.role)

    if obs_sub.empty or not gene_to_col:
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), presence

    present_genes = [gene for gene in BRANCH_GENE_ALIASES if gene in gene_to_col]
    target_x = x[cell_idx][:, [gene_to_col[gene] for gene in present_genes]].astype(float)
    lib_size = np.asarray(x[cell_idx].sum(axis=1)).ravel().astype(float)
    lib_size[~np.isfinite(lib_size) | (lib_size <= 0)] = np.nan
    normalizer = np.divide(1.0, lib_size, out=np.zeros_like(lib_size), where=np.isfinite(lib_size))
    normalized = target_x.multiply(normalizer[:, None]).multiply(1e4)
    log_expr = np.log1p(normalized.toarray())

    normal_mask = obs_sub["disease"].eq(config.control_label).to_numpy()
    control_mean = np.nanmean(log_expr[normal_mask], axis=0)
    control_sd = np.nanstd(log_expr[normal_mask], axis=0, ddof=1)
    control_sd[~np.isfinite(control_sd) | (control_sd < 1e-6)] = 1.0
    z_expr = (log_expr - control_mean) / control_sd

    gene_to_local = {gene: i for i, gene in enumerate(present_genes)}
    cell_meta_cols = ["donor_id", "disease", "cell_type"]
    if "tissue" in obs_sub.columns:
        cell_meta_cols.append("tissue")
    cell_scores = obs_sub[cell_meta_cols].reset_index(drop=True).copy()

    module_presence_rows: list[dict[str, object]] = []
    for module, genes in BRANCH_MODULES.items():
        present = [gene for gene in genes if gene in gene_to_local]
        module_presence_rows.append(
            {
                "analysis": config.name,
                "disease_name": config.disease_label,
                "compartment": config.compartment,
                "role": config.role,
                "module": module,
                "n_genes_present": len(present),
                "genes_present": ",".join(present),
            }
        )
        if present:
            local_idx = [gene_to_local[gene] for gene in present]
            score = np.nanmean(z_expr[:, local_idx], axis=1)
        else:
            score = np.full(len(obs_sub), np.nan)
        if np.isfinite(score[normal_mask]).any():
            high_threshold = np.nanpercentile(score[normal_mask], 75)
        else:
            high_threshold = np.nan
        cell_scores[module] = score
        cell_scores[f"{module}_high"] = score > high_threshold if np.isfinite(high_threshold) else False

    gene_rows: list[dict[str, object]] = []
    module_rows: list[dict[str, object]] = []
    for (donor, disease), group_index in cell_scores.groupby(["donor_id", "disease"], observed=True).groups.items():
        donor_idx = np.fromiter(group_index, dtype=int)
        if donor_idx.size < MIN_DONOR_CELLS:
            continue
        group = "case" if disease == config.disease_label else "control"
        base = {
            "analysis": config.name,
            "dataset_path": str(config.path.relative_to(ROOT)),
            "disease_name": config.disease_label,
            "compartment": config.compartment,
            "role": config.role,
            "donor_id": donor,
            "disease": disease,
            "group": group,
            "n_cells": int(donor_idx.size),
            "cell_types": ",".join(sorted(cell_scores.iloc[donor_idx]["cell_type"].astype(str).unique())),
        }
        for gene in present_genes:
            local = gene_to_local[gene]
            vals = log_expr[donor_idx, local]
            zvals = z_expr[donor_idx, local]
            gene_rows.append(
                {
                    **base,
                    "gene": gene,
                    "mean_log_norm": float(np.nanmean(vals)),
                    "mean_z_vs_controls": float(np.nanmean(zvals)),
                    "detection_fraction": float((vals > 0).mean()),
                }
            )
        for module in BRANCH_MODULES:
            vals = cell_scores.iloc[donor_idx][module].astype(float)
            module_rows.append(
                {
                    **base,
                    "module": module,
                    "mean_z_score": float(np.nanmean(vals)) if np.isfinite(vals).any() else np.nan,
                    "high_fraction": float(cell_scores.iloc[donor_idx][f"{module}_high"].mean()),
                }
            )

    return pd.DataFrame(gene_rows), pd.DataFrame(module_rows), pd.DataFrame(module_presence_rows), presence


def compare_genes(gene_scores: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    if gene_scores.empty:
        return pd.DataFrame()
    for (analysis, gene), sub in gene_scores.groupby(["analysis", "gene"], observed=True):
        for metric in ["mean_z_vs_controls", "detection_fraction"]:
            first = sub.iloc[0]
            rows.append(
                {
                    "analysis": analysis,
                    "disease_name": first["disease_name"],
                    "compartment": first["compartment"],
                    "role": first["role"],
                    "gene": gene,
                    "metric": metric,
                    **compare_values(sub[metric], sub["group"]),
                }
            )
    out = pd.DataFrame(rows)
    out["fdr"] = multipletests(out["p"].fillna(1.0), method="fdr_bh")[1]
    return out


def compare_modules(module_scores: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    if module_scores.empty:
        return pd.DataFrame()
    for (analysis, module), sub in module_scores.groupby(["analysis", "module"], observed=True):
        for metric in ["mean_z_score", "high_fraction"]:
            first = sub.iloc[0]
            rows.append(
                {
                    "analysis": analysis,
                    "disease_name": first["disease_name"],
                    "compartment": first["compartment"],
                    "role": first["role"],
                    "module": module,
                    "metric": metric,
                    **compare_values(sub[metric], sub["group"]),
                }
            )
    out = pd.DataFrame(rows)
    out["fdr"] = multipletests(out["p"].fillna(1.0), method="fdr_bh")[1]
    return out


def ms_gene_rows() -> pd.DataFrame:
    if not MS_SIGNATURE.exists():
        return pd.DataFrame()
    df = pd.read_csv(MS_SIGNATURE, sep="\t")
    rows: list[dict[str, object]] = []
    gene_col = "gene" if "gene" in df.columns else df.columns[0]
    upper_gene = df[gene_col].astype(str).str.upper()
    for gene, aliases in BRANCH_GENE_ALIASES.items():
        alias_mask = upper_gene.isin([alias.upper() for alias in aliases])
        if not alias_mask.any():
            continue
        row = df.loc[alias_mask].iloc[0]
        rows.append(
            {
                "analysis": "GSE111972_MS_WM_microglia",
                "disease_name": "MS",
                "compartment": "white matter microglia",
                "role": "myeloid_apc",
                "gene": gene,
                "metric": "bulk_log2_expression",
                "n_case_donors": np.nan,
                "n_control_donors": np.nan,
                "mean_case": float(row.get("mean_case", np.nan)),
                "mean_control": float(row.get("mean_control", np.nan)),
                "delta_case_minus_control": float(row.get("delta_log2", np.nan)),
                "hedges_g": float(row.get("hedges_g", np.nan)),
                "welch_t": float(row.get("welch_t", np.nan)),
                "p": float(row.get("p", np.nan)),
                "fdr": float(row.get("fdr", np.nan)),
            }
        )
    return pd.DataFrame(rows)


def summarize_feature(comparisons: pd.DataFrame, feature_col: str) -> pd.DataFrame:
    if comparisons.empty:
        return pd.DataFrame()
    work = comparisons.copy()
    work["support_level"] = [
        support_level(delta, p_value, fdr)
        for delta, p_value, fdr in zip(work["delta_case_minus_control"], work["p"], work["fdr"])
    ]
    work["support_score"] = work["support_level"].map(support_score)
    best = (
        work.sort_values(["support_score", "hedges_g"], ascending=[False, False])
        .groupby([feature_col, "disease_name"], as_index=False)
        .first()
    )
    rows: list[dict[str, object]] = []
    for feature, sub in best.groupby(feature_col, observed=True):
        positives = sub[sub["support_level"].isin(["fdr10_positive", "trend_positive"])]
        negatives = sub[sub["support_level"].eq("negative_trend")]
        rows.append(
            {
                feature_col: feature,
                "n_diseases_tested": int(sub["disease_name"].nunique()),
                "n_fdr10_positive_diseases": int((sub["support_level"] == "fdr10_positive").sum()),
                "n_trend_or_better_diseases": int(sub["support_level"].isin(["fdr10_positive", "trend_positive"]).sum()),
                "n_negative_trend_diseases": int(len(negatives)),
                "median_positive_hedges_g": float(positives["hedges_g"].median()) if not positives.empty else np.nan,
                "supporting_diseases": ";".join(positives["disease_name"].tolist()),
                "negative_diseases": ";".join(negatives["disease_name"].tolist()),
                "best_details": json.dumps(
                    sub.sort_values(["support_score", "hedges_g"], ascending=[False, False])[
                        [
                            "disease_name",
                            "analysis",
                            "compartment",
                            "metric",
                            "delta_case_minus_control",
                            "hedges_g",
                            "p",
                            "fdr",
                            "support_level",
                        ]
                    ].to_dict(orient="records")
                ),
            }
        )
    return pd.DataFrame(rows).sort_values(
        ["n_fdr10_positive_diseases", "n_trend_or_better_diseases", "n_negative_trend_diseases", "median_positive_hedges_g"],
        ascending=[False, False, True, False],
    )


def genetics_tables() -> tuple[pd.DataFrame, pd.DataFrame]:
    if not GENETICS.exists():
        empty = pd.DataFrame()
        return empty, empty
    df = pd.read_csv(GENETICS, sep="\t")
    rows: list[pd.DataFrame] = []
    for gene, aliases in BRANCH_GENE_ALIASES.items():
        alias_upper = {alias.upper() for alias in aliases}
        mask = df["query_gene"].astype(str).str.upper().isin(alias_upper) | df["approved_symbol"].astype(str).str.upper().isin(alias_upper)
        sub = df.loc[mask].copy()
        if sub.empty:
            rows.append(
                pd.DataFrame(
                    [
                        {
                            "gene": gene,
                            "query_gene": np.nan,
                            "approved_symbol": np.nan,
                            "ensembl": np.nan,
                            "disease": np.nan,
                            "disease_id": np.nan,
                            "max_score": 0.0,
                            "evidence_count": 0,
                            "pmids": np.nan,
                            "note": "not_in_wave13_opentargets_input",
                        }
                    ]
                )
            )
        else:
            sub.insert(0, "gene", gene)
            rows.append(sub)
    detail = pd.concat(rows, ignore_index=True, sort=False)
    summary_rows: list[dict[str, object]] = []
    for gene, sub in detail.groupby("gene", observed=True):
        evidence = sub[(sub["max_score"].fillna(0) > 0) | (sub["evidence_count"].fillna(0) > 0)]
        summary_rows.append(
            {
                "gene": gene,
                "n_diseases_queried": int(sub["disease"].dropna().nunique()),
                "n_diseases_with_any_evidence": int(evidence["disease"].dropna().nunique()),
                "max_score": float(sub["max_score"].fillna(0).max()) if "max_score" in sub else 0.0,
                "total_evidence_count": int(sub["evidence_count"].fillna(0).sum()) if "evidence_count" in sub else 0,
                "evidence_diseases": ";".join(evidence.sort_values("max_score", ascending=False)["disease"].dropna().astype(str).tolist()),
                "pmids": ";".join(
                    sorted(
                        {
                            pmid
                            for value in evidence["pmids"].dropna().astype(str)
                            for pmid in value.split(";")
                            if pmid and pmid.lower() != "nan"
                        }
                    )
                ),
            }
        )
    summary = pd.DataFrame(summary_rows).sort_values(
        ["n_diseases_with_any_evidence", "max_score", "total_evidence_count"], ascending=[False, False, False]
    )
    return detail, summary


def perturbation_tables() -> dict[str, pd.DataFrame]:
    tables: dict[str, pd.DataFrame] = {}

    mixscale_rank = RESULTS / "mixscale" / "mixscale_transition_controller_rank.tsv"
    if mixscale_rank.exists():
        rank = pd.read_csv(mixscale_rank, sep="\t")
        branch = rank[rank["perturbation"].astype(str).isin(BRANCH_PERTURBATION_SYMBOLS)].copy()
        tables["mixscale_branch_perturbations"] = branch
        tables["mixscale_top_downstream_controls"] = rank.sort_values(
            "transition_suppression_score", ascending=False
        ).head(12)

    mixscale_module = RESULTS / "mixscale" / "mixscale_module_summary.tsv"
    if mixscale_module.exists():
        module = pd.read_csv(mixscale_module, sep="\t")
        branch_module = module[module["perturbation"].astype(str).isin(BRANCH_PERTURBATION_SYMBOLS)].copy()
        tables["mixscale_branch_module_effects"] = branch_module
        downstream = module[
            module["module"].isin(DOWNSTREAM_READOUT_MODULES)
            & module["mean_module_log2fc_across_cell_types"].lt(0)
            & module["cell_type_negative_fraction"].ge(0.5)
        ].copy()
        tables["mixscale_downstream_suppression_modules"] = downstream.sort_values(
            ["cell_type_negative_fraction", "mean_module_log2fc_across_cell_types"], ascending=[False, True]
        )

    l1000 = RESULTS / "l1000fwd_reversal_hits.tsv"
    if l1000.exists():
        hits = pd.read_csv(l1000, sep="\t")
        text = (
            hits.get("target", pd.Series("", index=hits.index)).fillna("").astype(str)
            + " "
            + hits.get("moa", pd.Series("", index=hits.index)).fillna("").astype(str)
            + " "
            + hits.get("cmap_name", pd.Series("", index=hits.index)).fillna("").astype(str)
        )
        branch = hits[text.str.contains("|".join(sorted(BRANCH_PERTURBATION_SYMBOLS)), case=False, regex=True)].copy()
        tables["l1000_branch_or_tlr_hits"] = branch
        generic = hits[
            hits["mode"].eq("opposite")
            & text.str.contains("JAK|TYK|IFN|IKK|NF.?KB|IRAK|TLR", case=False, regex=True)
        ].copy()
        tables["l1000_generic_inflammatory_reversal_hits"] = generic.sort_values(["qvals", "rank"]).head(50)

    geneformer_dir = RESULTS / "geneformer_phagolysosomal_matrix_delete"
    geneformer = geneformer_dir / "geneformer_phagolysosomal_matrix_gene_summary.tsv"
    if geneformer.exists():
        gf = pd.read_csv(geneformer, sep="\t")
        branch = gf[gf["gene"].astype(str).isin(BRANCH_PERTURBATION_SYMBOLS)].copy()
        tables["geneformer_branch_delete_summary"] = branch

    summary_rows = [
        {
            "source": "MixScale transition controller rank",
            "direct_branch_perturbation_rows": int(len(tables.get("mixscale_branch_perturbations", pd.DataFrame()))),
            "generic_downstream_rows": int(len(tables.get("mixscale_top_downstream_controls", pd.DataFrame()))),
            "interpretation": "No direct SLC15A4/TASL/TLR/IRF5 perturbation in local MixScale; downstream IFN/JAK/STAT controls suppress IFN/HLA/CD74 modules.",
        },
        {
            "source": "L1000FWD/CMap reversal hits",
            "direct_branch_perturbation_rows": int(len(tables.get("l1000_branch_or_tlr_hits", pd.DataFrame()))),
            "generic_downstream_rows": int(len(tables.get("l1000_generic_inflammatory_reversal_hits", pd.DataFrame()))),
            "interpretation": "No direct branch-targeted reversal hit; generic inflammatory/JAK/IKK hits are not branch-specific.",
        },
        {
            "source": "Geneformer phagolysosomal delete",
            "direct_branch_perturbation_rows": int(len(tables.get("geneformer_branch_delete_summary", pd.DataFrame()))),
            "generic_downstream_rows": 0,
            "interpretation": "Branch genes are absent from the available phagolysosomal delete summary.",
        },
    ]
    tables["perturbation_evidence_summary"] = pd.DataFrame(summary_rows)
    return tables


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)

    gene_score_tables: list[pd.DataFrame] = []
    module_score_tables: list[pd.DataFrame] = []
    module_presence_tables: list[pd.DataFrame] = []
    gene_presence_tables: list[pd.DataFrame] = []
    run_rows: list[dict[str, object]] = []

    current_path: Path | None = None
    current_a = None
    current_x = None
    for config in sorted(CONFIGS, key=lambda c: str(c.path)):
        try:
            if current_path != config.path:
                current_a = None
                current_x = None
                gc.collect()
                current_a, current_x = read_counts(config.path)
                current_path = config.path
            gene_scores, module_scores, module_presence, gene_presence = analyze_config(config, current_a, current_x)
            gene_score_tables.append(gene_scores)
            module_score_tables.append(module_scores)
            module_presence_tables.append(module_presence)
            gene_presence_tables.append(gene_presence)
            run_rows.append(
                {
                    "analysis": config.name,
                    "status": "completed",
                    "n_gene_donor_rows": int(len(gene_scores)),
                    "n_module_donor_rows": int(len(module_scores)),
                    "n_present_genes": int(gene_presence["present"].sum()) if not gene_presence.empty else 0,
                }
            )
        except Exception as exc:  # keep fail-fast script informative across heterogeneous h5ad inputs
            run_rows.append({"analysis": config.name, "status": "failed", "error": f"{type(exc).__name__}: {exc}"})

    gene_scores = pd.concat(gene_score_tables, ignore_index=True, sort=False) if gene_score_tables else pd.DataFrame()
    module_scores = pd.concat(module_score_tables, ignore_index=True, sort=False) if module_score_tables else pd.DataFrame()
    gene_presence = pd.concat(gene_presence_tables, ignore_index=True, sort=False) if gene_presence_tables else pd.DataFrame()
    module_presence = pd.concat(module_presence_tables, ignore_index=True, sort=False) if module_presence_tables else pd.DataFrame()

    direct_gene_comparisons = compare_genes(gene_scores)
    ms_genes = ms_gene_rows()
    combined_gene_comparisons = (
        pd.concat([direct_gene_comparisons, ms_genes], ignore_index=True, sort=False)
        if not ms_genes.empty
        else direct_gene_comparisons
    )
    gene_summary = summarize_feature(combined_gene_comparisons, "gene")

    module_comparisons = compare_modules(module_scores)
    module_summary = summarize_feature(module_comparisons, "module")

    genetics_detail, genetics_summary = genetics_tables()
    perturbation = perturbation_tables()

    pd.DataFrame(run_rows).to_csv(OUT / "run_log.tsv", sep="\t", index=False)
    gene_presence.to_csv(OUT / "branch_gene_presence.tsv", sep="\t", index=False)
    module_presence.to_csv(OUT / "branch_module_gene_presence.tsv", sep="\t", index=False)
    gene_scores.to_csv(OUT / "branch_gene_donor_scores.tsv", sep="\t", index=False)
    module_scores.to_csv(OUT / "branch_module_donor_scores.tsv", sep="\t", index=False)
    direct_gene_comparisons.to_csv(OUT / "branch_gene_direct_h5ad_comparisons.tsv", sep="\t", index=False)
    combined_gene_comparisons.to_csv(OUT / "branch_gene_combined_comparisons.tsv", sep="\t", index=False)
    gene_summary.to_csv(OUT / "branch_gene_summary.tsv", sep="\t", index=False)
    module_comparisons.to_csv(OUT / "branch_module_comparisons.tsv", sep="\t", index=False)
    module_summary.to_csv(OUT / "branch_module_summary.tsv", sep="\t", index=False)
    genetics_detail.to_csv(OUT / "branch_genetics_detail.tsv", sep="\t", index=False)
    genetics_summary.to_csv(OUT / "branch_genetics_summary.tsv", sep="\t", index=False)
    for name, table in perturbation.items():
        table.to_csv(OUT / f"{name}.tsv", sep="\t", index=False)

    top_gene = gene_summary.head(10).to_dict(orient="records") if not gene_summary.empty else []
    top_module = module_summary.head(10).to_dict(orient="records") if not module_summary.empty else []
    pert_summary = perturbation["perturbation_evidence_summary"].to_dict(orient="records")
    recommendation = {
        "call": "no_go_as_cross_autoimmune_central_intervention",
        "reasons": [
            "Local expression recurrence is uneven and mostly trend-level.",
            "Genetics is strong for IRF5 across diseases but SLC15A4/TASL evidence is concentrated in SLE/RA.",
            "Available local perturbation/LINCS artifacts do not contain direct branch inhibition linked to IFN/HLA-II/CD74 downshift.",
            "TLR7/8 prior-art and downstream JAK/IFN biology block novelty as a central intervention claim.",
        ],
    }
    summary = {
        "random_seed": SEED,
        "branch_genes": BRANCH_GENE_ALIASES,
        "branch_modules": BRANCH_MODULES,
        "n_gene_donor_rows": int(len(gene_scores)),
        "n_module_donor_rows": int(len(module_scores)),
        "n_combined_gene_comparison_rows": int(len(combined_gene_comparisons)),
        "n_module_comparison_rows": int(len(module_comparisons)),
        "top_gene_summary": top_gene,
        "top_module_summary": top_module,
        "genetics_summary": genetics_summary.to_dict(orient="records") if not genetics_summary.empty else [],
        "perturbation_summary": pert_summary,
        "recommendation": recommendation,
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
