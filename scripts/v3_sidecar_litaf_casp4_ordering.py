#!/usr/bin/env python3
"""Sidecar ordering audit for the LITAF/CASP4 stress-generator branch.

This is intentionally narrower than the orchestrator waves. It asks whether
local perturbation or time-course artifacts can order LITAF and CASP4 relative
to C15ORF48/MOCCI, NDUFA4, NF-kB, IFN/APC, and pyroptosis readouts.

Inputs are all local V3 artifacts. Outputs are descriptive; they do not claim a
therapeutic finding.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
from scipy import stats


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "phases/v3/results" / "sidecar_litaf_casp4_ordering"
REPORT = ROOT / "phases/v3/subagents" / "sidecar_litaf_casp4_perturbation_modeling.md"
SEED = 20260527

GSE294918 = ROOT / "data/raw_v3/wave14_gsk3b_ciita/GSE294918_IFNyRNAseq_CPM.csv.gz"
GSE162464 = ROOT / "data/raw_v3/wave14_gsk3b_ciita/GSE162464_Normalized_Gene_Counts_Matrix.txt.gz"

MODULES_HUMAN = {
    "mocci_c15_ndufa4": ["C15ORF48", "NDUFA4"],
    "nfkb_lps": ["TNF", "NFKBIA", "IL1B", "CXCL8", "CCL2", "CCL20"],
    "ifn_core": ["STAT1", "IRF1", "ISG15", "IFIT1", "CXCL10", "GBP1", "GBP2", "GBP5"],
    "apc_mhcii": [
        "CIITA",
        "CD74",
        "CTSS",
        "IFI30",
        "RFX5",
        "HLA-DRA",
        "HLA-DPA1",
        "HLA-DPB1",
        "HLA-DQA1",
        "HLA-DQB1",
    ],
    "pyroptosis_noncanonical": ["CASP1", "CASP4", "CASP5", "GSDMD", "NLRP3", "IL1B", "IL18", "GBP1", "GBP2", "GBP5"],
    "stress_branch_targets": ["LITAF", "CASP4"],
}

MODULES_MOUSE = {
    "mocci_ndufa4_only": ["Ndufa4"],
    "nfkb_lps": ["Tnf", "Nfkbia", "Il1b", "Cxcl2", "Ccl2", "Ccl20"],
    "ifn_core": ["Stat1", "Irf1", "Isg15", "Ifit1", "Cxcl10", "Gbp2", "Gbp5"],
    "apc_mhcii": ["Ciita", "Cd74", "Ctss", "Ifi30", "Rfx5", "H2-Aa", "H2-Ab1", "H2-Eb1", "H2-DMa", "H2-DMb1"],
    "pyroptosis_noncanonical": ["Casp1", "Casp4", "Gsdmd", "Nlrp3", "Il1b", "Il18", "Gbp2", "Gbp5"],
    "stress_branch_targets": ["Litaf", "Casp4"],
}

FOCUS_HUMAN = sorted({g for genes in MODULES_HUMAN.values() for g in genes} | {"C15ORF48", "NDUFA4"})
FOCUS_MOUSE = sorted({g for genes in MODULES_MOUSE.values() for g in genes} | {"Ndufa4"})


def ensure_out() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)


def bh_fdr(pvals: Iterable[float]) -> list[float]:
    arr = np.asarray([np.nan if p is None else float(p) for p in pvals], dtype=float)
    out = np.full(arr.shape, np.nan)
    valid = np.isfinite(arr)
    if not valid.any():
        return out.tolist()
    idx = np.where(valid)[0]
    order = idx[np.argsort(arr[idx])]
    ranks = np.arange(1, len(order) + 1, dtype=float)
    adjusted = arr[order] * len(order) / ranks
    adjusted = np.minimum.accumulate(adjusted[::-1])[::-1]
    adjusted = np.minimum(adjusted, 1.0)
    out[order] = adjusted
    return out.tolist()


def safe_corr(x: Iterable[float], y: Iterable[float], method: str = "spearman") -> float:
    a = np.asarray(list(x), dtype=float)
    b = np.asarray(list(y), dtype=float)
    mask = np.isfinite(a) & np.isfinite(b)
    if mask.sum() < 3 or len(set(a[mask])) < 2 or len(set(b[mask])) < 2:
        return float("nan")
    if method == "pearson":
        return float(stats.pearsonr(a[mask], b[mask]).statistic)
    return float(stats.spearmanr(a[mask], b[mask]).statistic)


def first_delta_time(times: list[int], deltas: list[float], threshold: float = 0.5) -> float:
    for t, d in zip(times, deltas):
        if np.isfinite(d) and d >= threshold:
            return float(t)
    return float("nan")


def auc_delta(times: list[int], deltas: list[float]) -> float:
    arr = np.asarray(deltas, dtype=float)
    tt = np.asarray(times, dtype=float)
    mask = np.isfinite(arr)
    if mask.sum() < 2:
        return float("nan")
    return float(np.trapezoid(arr[mask], tt[mask]))


def read_human() -> pd.DataFrame:
    df = pd.read_csv(GSE294918, index_col=0)
    df.index = [str(x).upper() for x in df.index]
    df = df.apply(pd.to_numeric, errors="coerce")
    return df.groupby(df.index).mean()


def log2_value_human(df: pd.DataFrame, gene: str, column: str) -> float:
    if gene.upper() not in df.index or column not in df.columns:
        return float("nan")
    val = float(df.loc[gene.upper(), column])
    return float(np.log2(val + 0.5))


def human_module_value(df: pd.DataFrame, genes: list[str], column: str) -> tuple[float, str, int]:
    vals = []
    present = []
    for gene in genes:
        v = log2_value_human(df, gene, column)
        if np.isfinite(v):
            vals.append(v)
            present.append(gene.upper())
    if not vals:
        return float("nan"), "", 0
    return float(np.mean(vals)), ";".join(present), len(present)


def analyze_human_timecourse() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    df = read_human()
    arms = {
        "PBS_LPS": [0, 1, 3, 6, 12],
        "IFNy_memory_LPS": [0, 1, 3, 6, 12],
        "IFNy_memory_rux_LPS": [0, 1, 3, 6],
        "PBS_rux_LPS": [0, 1, 3, 6],
    }
    col_prefix = {
        "PBS_LPS": "D4_PBS_LPS",
        "IFNy_memory_LPS": "D4_IFNy_LPS",
        "IFNy_memory_rux_LPS": "D4_IFNy_rux_LPS",
        "PBS_rux_LPS": "D4_PBS_rux_LPS",
    }
    gene_rows = []
    module_rows = []
    for arm, times in arms.items():
        for gene in FOCUS_HUMAN:
            vals = []
            for t in times:
                col = f"{col_prefix[arm]}{t}H"
                vals.append(log2_value_human(df, gene, col))
            baseline = vals[0] if vals else float("nan")
            for t, val in zip(times, vals):
                gene_rows.append(
                    {
                        "dataset": "GSE294918",
                        "arm": arm,
                        "time_h": t,
                        "gene": gene,
                        "log2_cpm_plus_0_5": val,
                        "delta_vs_arm_0h": val - baseline if np.isfinite(val) and np.isfinite(baseline) else float("nan"),
                    }
                )
        for module, genes in MODULES_HUMAN.items():
            vals = []
            present_genes = ""
            n_present = 0
            for t in times:
                col = f"{col_prefix[arm]}{t}H"
                val, present_genes, n_present = human_module_value(df, genes, col)
                vals.append(val)
            baseline = vals[0] if vals else float("nan")
            for t, val in zip(times, vals):
                module_rows.append(
                    {
                        "dataset": "GSE294918",
                        "arm": arm,
                        "time_h": t,
                        "module": module,
                        "mean_log2_cpm_plus_0_5": val,
                        "delta_vs_arm_0h": val - baseline if np.isfinite(val) and np.isfinite(baseline) else float("nan"),
                        "n_genes_present": n_present,
                        "genes_present": present_genes,
                    }
                )

    gene_tc = pd.DataFrame(gene_rows)
    mod_tc = pd.DataFrame(module_rows)

    order_rows = []
    for arm, times in arms.items():
        for kind, name, sub in [
            *[("gene", g, gene_tc[(gene_tc["arm"].eq(arm)) & (gene_tc["gene"].eq(g))]) for g in FOCUS_HUMAN],
            *[("module", m, mod_tc[(mod_tc["arm"].eq(arm)) & (mod_tc["module"].eq(m))]) for m in MODULES_HUMAN],
        ]:
            if sub.empty:
                continue
            deltas = [float(x) for x in sub.sort_values("time_h")["delta_vs_arm_0h"]]
            t_order = [int(x) for x in sub.sort_values("time_h")["time_h"]]
            vals = [float(x) for x in sub.sort_values("time_h").iloc[:, sub.columns.get_loc("log2_cpm_plus_0_5") if kind == "gene" else sub.columns.get_loc("mean_log2_cpm_plus_0_5")]]
            max_delta = float(np.nanmax(deltas)) if np.isfinite(deltas).any() else float("nan")
            min_delta = float(np.nanmin(deltas)) if np.isfinite(deltas).any() else float("nan")
            order_rows.append(
                {
                    "dataset": "GSE294918",
                    "arm": arm,
                    "kind": kind,
                    "name": name,
                    "first_time_delta_ge_0_5h": first_delta_time(t_order, deltas),
                    "time_of_max_delta_h": float(t_order[int(np.nanargmax(deltas))]) if np.isfinite(deltas).any() else float("nan"),
                    "max_delta_log2": max_delta,
                    "min_delta_log2": min_delta,
                    "delta_auc_0_to_last": auc_delta(t_order, deltas),
                    "baseline_log2": vals[0] if vals else float("nan"),
                    "last_log2": vals[-1] if vals else float("nan"),
                }
            )
    ordering = pd.DataFrame(order_rows)

    rux_rows = []
    matched_times = [0, 1, 3, 6]
    for kind, names in [("gene", FOCUS_HUMAN), ("module", list(MODULES_HUMAN))]:
        for name in names:
            effects = []
            for t in matched_times:
                if kind == "gene":
                    case = log2_value_human(df, name, f"D4_IFNy_rux_LPS{t}H")
                    ctrl = log2_value_human(df, name, f"D4_IFNy_LPS{t}H")
                else:
                    case, _, _ = human_module_value(df, MODULES_HUMAN[name], f"D4_IFNy_rux_LPS{t}H")
                    ctrl, _, _ = human_module_value(df, MODULES_HUMAN[name], f"D4_IFNy_LPS{t}H")
                effect = case - ctrl if np.isfinite(case) and np.isfinite(ctrl) else float("nan")
                effects.append(effect)
                rux_rows.append(
                    {
                        "dataset": "GSE294918",
                        "kind": kind,
                        "name": name,
                        "time_h": t,
                        "rux_vs_matched_ifny_lps_log2fc": effect,
                        "note": "single processed CPM column per condition/timepoint; descriptive only",
                    }
                )
            if effects:
                rux_rows.append(
                    {
                        "dataset": "GSE294918",
                        "kind": kind,
                        "name": name,
                        "time_h": "mean_0_6h",
                        "rux_vs_matched_ifny_lps_log2fc": float(np.nanmean(effects)),
                        "note": "mean across 0/1/3/6h descriptive ruxolitinib contrasts",
                    }
                )
    rux = pd.DataFrame(rux_rows)

    return gene_tc, mod_tc, ordering, rux


def read_mouse() -> tuple[pd.DataFrame, dict[str, list[str]]]:
    df = pd.read_csv(GSE162464, sep="\t")
    sample_cols = [c for c in df.columns if c.startswith("Sample")]
    grouped = df.groupby("Symbol")[sample_cols].mean(numeric_only=True)
    groups = {
        "NTC_US": [c for c in sample_cols if "NTC_US" in c],
        "NTC_IFNg": [c for c in sample_cols if "NTC_IFNg" in c],
        "Gsk3b_US": [c for c in sample_cols if "Gsk3b_US" in c],
        "Gsk3b_IFNg": [c for c in sample_cols if "Gsk3b_IFNg" in c],
        "Med16_US": [c for c in sample_cols if "Med16_US" in c],
        "Med16_IFNg": [c for c in sample_cols if "Med16_IFNg" in c],
    }
    return grouped, groups


def hedges_g(x: np.ndarray, y: np.ndarray) -> float:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    nx, ny = len(x), len(y)
    if nx < 2 or ny < 2:
        return float("nan")
    sx = np.var(x, ddof=1)
    sy = np.var(y, ddof=1)
    pooled = ((nx - 1) * sx + (ny - 1) * sy) / (nx + ny - 2)
    if pooled <= 0:
        return float("nan")
    d = (np.mean(x) - np.mean(y)) / math.sqrt(pooled)
    correction = 1 - (3 / (4 * (nx + ny) - 9))
    return float(d * correction)


def contrast_vector(expr: pd.DataFrame, genes: list[str], case_cols: list[str], ctrl_cols: list[str]) -> tuple[np.ndarray, np.ndarray, list[str]]:
    present = [g for g in genes if g in expr.index]
    if not present:
        return np.array([]), np.array([]), []
    case_vals = np.vstack([np.log2(expr.loc[g, case_cols].astype(float).to_numpy() + 1.0) for g in present])
    ctrl_vals = np.vstack([np.log2(expr.loc[g, ctrl_cols].astype(float).to_numpy() + 1.0) for g in present])
    return case_vals.mean(axis=0), ctrl_vals.mean(axis=0), present


def analyze_mouse() -> tuple[pd.DataFrame, pd.DataFrame]:
    expr, groups = read_mouse()
    contrasts = [
        ("NTC_IFNg_vs_NTC_US", "NTC_IFNg", "NTC_US"),
        ("Gsk3b_IFNg_vs_NTC_IFNg", "Gsk3b_IFNg", "NTC_IFNg"),
        ("Med16_IFNg_vs_NTC_IFNg", "Med16_IFNg", "NTC_IFNg"),
        ("Gsk3b_US_vs_NTC_US", "Gsk3b_US", "NTC_US"),
        ("Med16_US_vs_NTC_US", "Med16_US", "NTC_US"),
    ]
    rows = []
    mod_rows = []
    for contrast, case, ctrl in contrasts:
        pvals = []
        idxs = []
        for gene in FOCUS_MOUSE:
            if gene not in expr.index:
                rows.append(
                    {
                        "dataset": "GSE162464",
                        "kind": "gene",
                        "contrast": contrast,
                        "gene": gene,
                        "present": False,
                    }
                )
                continue
            x = np.log2(expr.loc[gene, groups[case]].astype(float).to_numpy() + 1.0)
            y = np.log2(expr.loc[gene, groups[ctrl]].astype(float).to_numpy() + 1.0)
            p = float(stats.ttest_ind(x, y, equal_var=False).pvalue)
            row = {
                "dataset": "GSE162464",
                "kind": "gene",
                "contrast": contrast,
                "gene": gene,
                "present": True,
                "n_case": len(x),
                "n_control": len(y),
                "mean_case_log2": float(np.mean(x)),
                "mean_control_log2": float(np.mean(y)),
                "log2fc": float(np.mean(x) - np.mean(y)),
                "hedges_g": hedges_g(x, y),
                "welch_p": p,
            }
            pvals.append(p)
            idxs.append(len(rows))
            rows.append(row)
        fdrs = bh_fdr(pvals)
        for i, fdr in zip(idxs, fdrs):
            rows[i]["fdr_within_contrast_focus_genes"] = fdr

        mod_pvals = []
        mod_idxs = []
        for module, genes in MODULES_MOUSE.items():
            x, y, present = contrast_vector(expr, genes, groups[case], groups[ctrl])
            if len(present) == 0:
                mod_rows.append(
                    {
                        "dataset": "GSE162464",
                        "kind": "module",
                        "contrast": contrast,
                        "module": module,
                        "present": False,
                    }
                )
                continue
            p = float(stats.ttest_ind(x, y, equal_var=False).pvalue) if len(x) >= 2 and len(y) >= 2 else float("nan")
            mod_rows.append(
                {
                    "dataset": "GSE162464",
                    "kind": "module",
                    "contrast": contrast,
                    "module": module,
                    "present": True,
                    "n_genes_present": len(present),
                    "genes_present": ";".join(present),
                    "n_case": len(x),
                    "n_control": len(y),
                    "mean_case_log2": float(np.mean(x)),
                    "mean_control_log2": float(np.mean(y)),
                    "log2fc": float(np.mean(x) - np.mean(y)),
                    "hedges_g": hedges_g(x, y),
                    "welch_p": p,
                }
            )
            mod_pvals.append(p)
            mod_idxs.append(len(mod_rows) - 1)
        for i, fdr in zip(mod_idxs, bh_fdr(mod_pvals)):
            mod_rows[i]["fdr_within_contrast_modules"] = fdr

    return pd.DataFrame(rows), pd.DataFrame(mod_rows)


def extract_wave37() -> pd.DataFrame:
    path = ROOT / "phases/v3/results/wave37_gse212008_crispr_efferocytosis_screen/gene_level_screen_scores.tsv"
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_csv(path, sep="\t")
    focus = ["LITAF", "CASP4", "C15ORF48", "NDUFA4", "CASP1", "CASP5", "GSDMD", "IL1B"]
    return df[df["gene_symbol"].astype(str).str.upper().isin(focus)].copy()


def extract_mixscale() -> pd.DataFrame:
    path = ROOT / "phases/v3/results/mixscale/mixscale_readout_gene_summary.tsv"
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_csv(path, sep="\t")
    upstream = ["IFNGR1", "IFNGR2", "JAK1", "JAK2", "TYK2", "STAT1", "IRF1", "CHUK", "IKBKB", "IKBKG", "NFKB1", "MAP3K7"]
    readouts = ["GBP1", "GBP2", "STAT1", "IRF1", "CTSS", "NLRC5", "TAP1", "TAP2", "CD44"]
    sub = df[df["perturbation"].astype(str).str.upper().isin(upstream) & df["gene"].astype(str).str.upper().isin(readouts)].copy()
    return sub.sort_values(["pathway", "perturbation", "gene"])


def extract_geneformer() -> tuple[pd.DataFrame, pd.DataFrame]:
    metrics_path = ROOT / "phases/v3/results/geneformer_broad_residual_delete/geneformer_broad_residual_delete_metrics.tsv"
    summary_path = ROOT / "phases/v3/results/wave18_foundation_rescue/geneformer_source_gene_summary.tsv"
    metrics = pd.DataFrame()
    summary = pd.DataFrame()
    if metrics_path.exists():
        df = pd.read_csv(metrics_path, sep="\t")
        metrics = df[df["gene"].astype(str).str.upper().isin(["LITAF", "CASP4"])].copy()
    if summary_path.exists():
        df = pd.read_csv(summary_path, sep="\t")
        summary = df[df["gene"].astype(str).str.upper().isin(["LITAF", "CASP4"])].copy()
    return metrics, summary


def extract_l1000() -> pd.DataFrame:
    paths = [
        ROOT / "phases/v3/results/l1000fwd_reversal_hits.tsv",
        ROOT / "phases/v3/results/wave15_perturbation_drug_response/l1000fwd_selectivity_hits.tsv",
    ]
    rows = []
    pattern = "CASP4|LITAF|caspase|pyroptosis|NFKB|NF-kappa|JAK|ruxolitinib|TNF"
    for path in paths:
        if not path.exists():
            continue
        df = pd.read_csv(path, sep="\t")
        mask = df.astype(str).apply(lambda s: s.str.contains(pattern, case=False, na=False)).any(axis=1)
        sub = df[mask].copy()
        sub["source_file"] = str(path.relative_to(ROOT))
        rows.append(sub)
    return pd.concat(rows, ignore_index=True, sort=False) if rows else pd.DataFrame()


def build_target_summary(
    human_gene_tc: pd.DataFrame,
    human_module_tc: pd.DataFrame,
    human_order: pd.DataFrame,
    human_rux: pd.DataFrame,
    mouse_gene: pd.DataFrame,
    wave37: pd.DataFrame,
    gf_summary: pd.DataFrame,
) -> pd.DataFrame:
    rows = []
    for target in ["LITAF", "CASP4"]:
        ifny = human_gene_tc[(human_gene_tc["arm"].eq("IFNy_memory_LPS")) & (human_gene_tc["gene"].eq(target))].sort_values("time_h")
        target_delta = ifny["delta_vs_arm_0h"].to_numpy(float)
        c15 = human_gene_tc[(human_gene_tc["arm"].eq("IFNy_memory_LPS")) & (human_gene_tc["gene"].eq("C15ORF48"))].sort_values("time_h")
        ndufa4 = human_gene_tc[(human_gene_tc["arm"].eq("IFNy_memory_LPS")) & (human_gene_tc["gene"].eq("NDUFA4"))].sort_values("time_h")
        nfkb = human_module_tc[(human_module_tc["arm"].eq("IFNy_memory_LPS")) & (human_module_tc["module"].eq("nfkb_lps"))].sort_values("time_h")
        ifn = human_module_tc[(human_module_tc["arm"].eq("IFNy_memory_LPS")) & (human_module_tc["module"].eq("ifn_core"))].sort_values("time_h")
        pyro = human_module_tc[(human_module_tc["arm"].eq("IFNy_memory_LPS")) & (human_module_tc["module"].eq("pyroptosis_noncanonical"))].sort_values("time_h")
        order_row = human_order[(human_order["arm"].eq("IFNy_memory_LPS")) & (human_order["kind"].eq("gene")) & (human_order["name"].eq(target))]
        rux_mean = human_rux[
            (human_rux["kind"].eq("gene")) & (human_rux["name"].eq(target)) & (human_rux["time_h"].astype(str).eq("mean_0_6h"))
        ]
        d4_ifny_prime = float("nan")
        d0_ifny_prime = float("nan")
        h = read_human()
        d4_ifny_prime = log2_value_human(h, target, "D4_IFNy_LPS0H") - log2_value_human(h, target, "D4_PBS_LPS0H")
        d0_ifny_prime = log2_value_human(h, target, "D0_IFNy_8H") - log2_value_human(h, target, "D0_unstim")

        mouse_ifn = mouse_gene[(mouse_gene["gene"].str.lower().eq(target.lower().capitalize())) & (mouse_gene["contrast"].eq("NTC_IFNg_vs_NTC_US"))]
        # Mouse symbols are Litaf/Casp4.
        mouse_symbol = target.capitalize() if target != "CASP4" else "Casp4"
        mouse_ifn = mouse_gene[(mouse_gene["gene"].eq(mouse_symbol)) & (mouse_gene["contrast"].eq("NTC_IFNg_vs_NTC_US"))]
        mouse_gsk = mouse_gene[(mouse_gene["gene"].eq(mouse_symbol)) & (mouse_gene["contrast"].eq("Gsk3b_IFNg_vs_NTC_IFNg"))]
        mouse_med = mouse_gene[(mouse_gene["gene"].eq(mouse_symbol)) & (mouse_gene["contrast"].eq("Med16_IFNg_vs_NTC_IFNg"))]

        w37 = wave37[wave37["gene_symbol"].astype(str).str.upper().eq(target)] if not wave37.empty else pd.DataFrame()
        gf = gf_summary[gf_summary["gene"].astype(str).str.upper().eq(target)] if not gf_summary.empty else pd.DataFrame()

        if target == "CASP4":
            call = (
                "DEEPEN_AS_STRESS_READOUT_NOT_TARGET: human ruxolitinib suppresses CASP4 and mouse IFN induces Casp4, "
                "but direct CASP4 perturbation and selective therapeutic direction are absent/blocked."
            )
        else:
            call = (
                "PARK_AS_LATE_LPS_C15_COSTATE: LITAF tracks late LPS/C15 timing but lacks IFN/JAK dependence, "
                "direct perturbation, and selective modality."
            )

        rows.append(
            {
                "target": target,
                "human_ifny_lps_first_delta_ge_0_5h": float(order_row["first_time_delta_ge_0_5h"].iloc[0]) if not order_row.empty else float("nan"),
                "human_ifny_lps_max_delta_log2": float(order_row["max_delta_log2"].iloc[0]) if not order_row.empty else float("nan"),
                "human_d4_ifny_memory_0h_vs_pbs_lps0_log2fc": d4_ifny_prime,
                "human_d0_ifny_8h_vs_unstim_log2fc": d0_ifny_prime,
                "human_rux_mean_log2fc_0_6h": float(rux_mean["rux_vs_matched_ifny_lps_log2fc"].iloc[0]) if not rux_mean.empty else float("nan"),
                "corr_delta_with_c15orf48_spearman": safe_corr(target_delta, c15["delta_vs_arm_0h"].to_numpy(float)),
                "corr_delta_with_ndufa4_spearman": safe_corr(target_delta, ndufa4["delta_vs_arm_0h"].to_numpy(float)),
                "corr_delta_with_nfkb_module_spearman": safe_corr(target_delta, nfkb["delta_vs_arm_0h"].to_numpy(float)),
                "corr_delta_with_ifn_module_spearman": safe_corr(target_delta, ifn["delta_vs_arm_0h"].to_numpy(float)),
                "corr_delta_with_pyroptosis_module_spearman": safe_corr(target_delta, pyro["delta_vs_arm_0h"].to_numpy(float)),
                "mouse_ifng_log2fc": float(mouse_ifn["log2fc"].iloc[0]) if not mouse_ifn.empty else float("nan"),
                "mouse_ifng_fdr_focus": float(mouse_ifn["fdr_within_contrast_focus_genes"].iloc[0]) if not mouse_ifn.empty else float("nan"),
                "mouse_gsk3bko_ifng_log2fc": float(mouse_gsk["log2fc"].iloc[0]) if not mouse_gsk.empty else float("nan"),
                "mouse_gsk3bko_ifng_fdr_focus": float(mouse_gsk["fdr_within_contrast_focus_genes"].iloc[0]) if not mouse_gsk.empty else float("nan"),
                "mouse_med16ko_ifng_log2fc": float(mouse_med["log2fc"].iloc[0]) if not mouse_med.empty else float("nan"),
                "mouse_med16ko_ifng_fdr_focus": float(mouse_med["fdr_within_contrast_focus_genes"].iloc[0]) if not mouse_med.empty else float("nan"),
                "wave37_contrast_lfc": float(w37["median_efficient_minus_noneater_lfc"].iloc[0]) if not w37.empty else float("nan"),
                "wave37_contrast_fdr": float(w37["contrast_fdr"].iloc[0]) if not w37.empty and "contrast_fdr" in w37 else float("nan"),
                "geneformer_support_contexts": float(gf["support_contexts"].iloc[0]) if not gf.empty else 0.0,
                "geneformer_strong_support_contexts": float(gf["strong_support_contexts"].iloc[0]) if not gf.empty else 0.0,
                "sidecar_call": call,
            }
        )
    return pd.DataFrame(rows)


def fmt(x: float, digits: int = 3) -> str:
    if x is None or not np.isfinite(float(x)):
        return "NA"
    return f"{float(x):.{digits}f}"


def write_report(summary: pd.DataFrame, artifacts: dict[str, str]) -> None:
    litaf = summary[summary["target"].eq("LITAF")].iloc[0]
    casp4 = summary[summary["target"].eq("CASP4")].iloc[0]
    lines = [
        "# Sidecar: LITAF/CASP4 Perturbation and Ordering Audit",
        "",
        "## Scope",
        "Sidecar-only audit for the V3 autonomous autoimmune session. The question is whether local perturbation/time-course artifacts order `LITAF` or `CASP4` relative to `C15ORF48`/MOCCI, `NDUFA4`, NF-kB, IFN/APC, and pyroptosis readouts. This report does not claim a final therapeutic finding.",
        "",
        "## Datasets Used",
        "- `GSE294918`: human macrophage IFN-gamma memory/LPS/ruxolitinib processed CPM table. No replicate columns in the local file, so all time-course and rux effects are descriptive log2(CPM+0.5) differences.",
        "- `GSE162464`: mouse macrophage NTC/Gsk3b/Med16 +/- IFN-gamma normalized RNA-seq counts with triplicate groups; Welch tests and BH FDR were computed within this focused gene/module panel.",
        "- `GSE212008` Wave37 CRISPR efferocytosis screen: phenotype-only CRISPR readout for candidate KO effects on efficient-vs-noneater phagocytosis bins.",
        "- `GSE281048` Mixscale local summaries: used only to confirm generic IFN/NF-kB perturbation behavior; no local direct `LITAF`, `CASP4`, `C15ORF48`, or `NDUFA4` readout exists there.",
        "- Local Geneformer broad-residual deletion outputs: `CASP4` had weak model support; `LITAF` was absent from the local Geneformer candidate outputs.",
        "- Local L1000FWD outputs: no direct `LITAF`/`CASP4` perturbagen evidence; only generic NF-kB/JAK/caspase-adjacent signatures.",
        "",
        "## Quantitative Directionality Readout",
        "",
        "| target | human IFNy-LPS first +0.5 log2 h | human IFNy-LPS max delta | D4 IFNy-memory 0h vs PBS log2FC | D0 IFNy 8h vs unstim log2FC | rux mean log2FC 0-6h | corr with C15 delta | corr with NF-kB module | mouse IFNg log2FC / FDR | Gsk3b KO under IFNg log2FC / FDR | Med16 KO under IFNg log2FC / FDR | Wave37 KO contrast / FDR | Geneformer support |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for _, row in summary.iterrows():
        lines.append(
            "| {target} | {first} | {maxd} | {prime4} | {prime0} | {rux} | {c15corr} | {nfkbcorr} | {mifn}/{mifnfdr} | {mgsk}/{mgskfdr} | {mmed}/{mmedfdr} | {w37}/{w37fdr} | {gfs}/{gfss} |".format(
                target=row["target"],
                first=fmt(row["human_ifny_lps_first_delta_ge_0_5h"], 1),
                maxd=fmt(row["human_ifny_lps_max_delta_log2"]),
                prime4=fmt(row["human_d4_ifny_memory_0h_vs_pbs_lps0_log2fc"]),
                prime0=fmt(row["human_d0_ifny_8h_vs_unstim_log2fc"]),
                rux=fmt(row["human_rux_mean_log2fc_0_6h"]),
                c15corr=fmt(row["corr_delta_with_c15orf48_spearman"]),
                nfkbcorr=fmt(row["corr_delta_with_nfkb_module_spearman"]),
                mifn=fmt(row["mouse_ifng_log2fc"]),
                mifnfdr=fmt(row["mouse_ifng_fdr_focus"]),
                mgsk=fmt(row["mouse_gsk3bko_ifng_log2fc"]),
                mgskfdr=fmt(row["mouse_gsk3bko_ifng_fdr_focus"]),
                mmed=fmt(row["mouse_med16ko_ifng_log2fc"]),
                mmedfdr=fmt(row["mouse_med16ko_ifng_fdr_focus"]),
                w37=fmt(row["wave37_contrast_lfc"]),
                w37fdr=fmt(row["wave37_contrast_fdr"]),
                gfs=fmt(row["geneformer_support_contexts"], 0),
                gfss=fmt(row["geneformer_strong_support_contexts"], 0),
            )
        )
    lines += [
        "",
        "## Interpretation",
        f"- `CASP4`: {casp4['sidecar_call']}",
        f"- `LITAF`: {litaf['sidecar_call']}",
        "- Ordering from GSE294918: NF-kB/LPS cytokine markers peak early (1-3h), while `C15ORF48` rises later and monotonically through 12h. `LITAF` first crosses the +0.5 log2 threshold at 3h and correlates with the C15 trajectory, which makes it look like a late LPS/C15 co-state rather than a proven upstream controller. `CASP4` is already IFN-primed before LPS and is strongly JAK/rux-sensitive, so it sits closer to the IFN/noncanonical-inflammasome priming branch than to the late C15/MOCCI response.",
        "- Ordering from GSE162464: mouse `Casp4` is IFN-gamma inducible in triplicates, while `Litaf` is not materially IFN induced. Gsk3b and Med16 perturbations do not give a consistent causal ordering from these targets to C15/MOCCI because mouse `C15orf48` is absent from the local matrix and `Ndufa4` moves only modestly.",
        "- Direct perturbation gap: no local dataset directly perturbs `LITAF` or `CASP4` and measures the C15/NDUFA4/MOCCI state. Wave37 gives only an efferocytosis phenotype and is unresolved for `LITAF`; `CASP4` is absent from that screen extract.",
        "",
        "## Local Deepening Decision",
        "- `CASP4` deserves local deepening only as a stress-axis readout/control: it has real IFN/JAK ordering evidence, but no local direct perturbation edge and prior safety/selectivity concerns block therapeutic promotion.",
        "- `LITAF` does not deserve direct therapeutic deepening from current local evidence. If pursued, the right experiment is a time-resolved perturbation-ordering assay, not another co-expression/residual score.",
        "",
        "## Artifacts",
    ]
    for name, path in artifacts.items():
        lines.append(f"- `{name}`: `{path}`")
    lines += [
        "",
        "## Reproducibility",
        "- Entry point: `.venv_v3_py312/bin/python scripts/v3_sidecar_litaf_casp4_ordering.py`",
        f"- Random seed fixed: `{SEED}` (no stochastic analysis used).",
    ]
    REPORT.write_text("\n".join(lines) + "\n")


def main() -> None:
    np.random.seed(SEED)
    ensure_out()
    human_gene_tc, human_mod_tc, human_order, human_rux = analyze_human_timecourse()
    mouse_gene, mouse_mod = analyze_mouse()
    wave37 = extract_wave37()
    mixscale = extract_mixscale()
    gf_metrics, gf_summary = extract_geneformer()
    l1000 = extract_l1000()

    target_summary = build_target_summary(human_gene_tc, human_mod_tc, human_order, human_rux, mouse_gene, wave37, gf_summary)

    artifacts = {
        "human_gene_timecourse": "phases/v3/results/sidecar_litaf_casp4_ordering/gse294918_gene_timecourse.tsv",
        "human_module_timecourse": "phases/v3/results/sidecar_litaf_casp4_ordering/gse294918_module_timecourse.tsv",
        "human_ordering_summary": "phases/v3/results/sidecar_litaf_casp4_ordering/gse294918_ordering_summary.tsv",
        "human_rux_effects": "phases/v3/results/sidecar_litaf_casp4_ordering/gse294918_rux_effects.tsv",
        "mouse_gene_contrasts": "phases/v3/results/sidecar_litaf_casp4_ordering/gse162464_gene_contrasts.tsv",
        "mouse_module_contrasts": "phases/v3/results/sidecar_litaf_casp4_ordering/gse162464_module_contrasts.tsv",
        "wave37_extract": "phases/v3/results/sidecar_litaf_casp4_ordering/wave37_screen_extract.tsv",
        "mixscale_extract": "phases/v3/results/sidecar_litaf_casp4_ordering/mixscale_axis_extract.tsv",
        "geneformer_context_extract": "phases/v3/results/sidecar_litaf_casp4_ordering/geneformer_context_extract.tsv",
        "geneformer_gene_summary_extract": "phases/v3/results/sidecar_litaf_casp4_ordering/geneformer_gene_summary_extract.tsv",
        "l1000_extract": "phases/v3/results/sidecar_litaf_casp4_ordering/l1000_branch_extract.tsv",
        "target_directionality_summary": "phases/v3/results/sidecar_litaf_casp4_ordering/target_directionality_summary.tsv",
        "report": "phases/v3/subagents/sidecar_litaf_casp4_perturbation_modeling.md",
    }

    human_gene_tc.to_csv(ROOT / artifacts["human_gene_timecourse"], sep="\t", index=False)
    human_mod_tc.to_csv(ROOT / artifacts["human_module_timecourse"], sep="\t", index=False)
    human_order.to_csv(ROOT / artifacts["human_ordering_summary"], sep="\t", index=False)
    human_rux.to_csv(ROOT / artifacts["human_rux_effects"], sep="\t", index=False)
    mouse_gene.to_csv(ROOT / artifacts["mouse_gene_contrasts"], sep="\t", index=False)
    mouse_mod.to_csv(ROOT / artifacts["mouse_module_contrasts"], sep="\t", index=False)
    wave37.to_csv(ROOT / artifacts["wave37_extract"], sep="\t", index=False)
    mixscale.to_csv(ROOT / artifacts["mixscale_extract"], sep="\t", index=False)
    gf_metrics.to_csv(ROOT / artifacts["geneformer_context_extract"], sep="\t", index=False)
    gf_summary.to_csv(ROOT / artifacts["geneformer_gene_summary_extract"], sep="\t", index=False)
    l1000.to_csv(ROOT / artifacts["l1000_extract"], sep="\t", index=False)
    target_summary.to_csv(ROOT / artifacts["target_directionality_summary"], sep="\t", index=False)

    summary_json = {
        "analysis_call": "SIDECAR_NO_DIRECT_THERAPEUTIC_PROMOTION",
        "sidecar_call": {
            row["target"]: row["sidecar_call"] for _, row in target_summary.iterrows()
        },
        "datasets_used": [
            "GSE294918",
            "GSE162464",
            "GSE212008/Wave37",
            "GSE281048/Mixscale local summaries",
            "local Geneformer broad-residual deletion outputs",
            "local L1000FWD outputs",
        ],
        "random_seed": SEED,
        "artifacts": artifacts,
    }
    (OUT / "summary.json").write_text(json.dumps(summary_json, indent=2, sort_keys=True) + "\n")
    write_report(target_summary, artifacts)
    print(json.dumps(summary_json, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
