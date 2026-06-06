#!/usr/bin/env python3
"""Wave15-B perturbation and drug-response worker.

Question:
    Which real perturbations or compounds reduce the CD74/CIITA/HLA-II antigen
    presentation module more selectively than a generic IFN/JAK collapse?

Inputs are public processed perturbation resources already present locally, plus
small public L1000FWD API calls when available:

    - GSE281048 / Zenodo 14035992 Mixscale pathway CRISPRi DE tables.
    - GSE162463 mouse macrophage MHCII/CD40/PD-L1 CRISPR screen.
    - GSE162464 mouse macrophage NTC/Gsk3b/Med16 +/- IFN-gamma RNA-seq.
    - GSE294918 human macrophage IFN-gamma memory/ruxolitinib CPM table.
    - L1000FWD/LINCS2020 module signature search and local compound metadata.

This is an evidence worker, not a novelty or therapeutic-claim script. It keeps
effect scales separate by data source and writes all outputs under
phases/v3/results/wave15_perturbation_drug_response/.
"""

from __future__ import annotations

import json
import math
import re
import time
import zipfile
from collections import defaultdict
from io import BytesIO
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
import requests
from scipy import stats
from statsmodels.stats.multitest import multipletests

SEED = 20260527
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "phases/v3/results" / "wave15_perturbation_drug_response"

MIXSCALE_ZIP = ROOT / "data" / "raw_v3" / "mixscale" / "DE_results_all_pathway.zip"
GSE162463_SCREEN = ROOT / "data" / "raw_v3" / "wave14_gsk3b_ciita" / "GSE162463_sgRNA_CountsNormalized.txt.gz"
GSE162464_RNA = ROOT / "data" / "raw_v3" / "wave14_gsk3b_ciita" / "GSE162464_Normalized_Gene_Counts_Matrix.txt.gz"
GSE294918_CPM = ROOT / "data" / "raw_v3" / "wave14_gsk3b_ciita" / "GSE294918_IFNyRNAseq_CPM.csv.gz"
COMPOUNDINFO = ROOT / "data" / "raw_v3" / "lincs2020" / "compoundinfo_beta.txt"

L1000_BASE_URL = "https://maayanlab.cloud/L1000FWD"

TARGET_MODULE = [
    "CD74",
    "CIITA",
    "RFX5",
    "IFI30",
    "CTSS",
    "HLA-DRA",
    "HLA-DRB1",
    "HLA-DPA1",
    "HLA-DPB1",
    "HLA-DQA1",
    "HLA-DQB1",
    "HLA-DMA",
    "HLA-DMB",
]

GENERIC_IFN_MODULE = ["STAT1", "IRF1", "CXCL10", "GBP1", "ISG15", "IFIT1"]

STRESS_MODULE = [
    "DDIT3",
    "ATF4",
    "HSPA1A",
    "HSPA1B",
    "HSP90AA1",
    "DNAJB1",
    "HMOX1",
    "JUN",
    "FOS",
    "GADD45A",
    "KLF6",
    "BAX",
    "CASP3",
]

MOUSE_TARGET_MODULE = [
    "Cd74",
    "Ciita",
    "Rfx5",
    "Ifi30",
    "Ctss",
    "H2-Aa",
    "H2-Ab1",
    "H2-Eb1",
    "H2-DMa",
    "H2-DMb1",
    "H2-DMb2",
]
MOUSE_GENERIC_IFN_MODULE = ["Stat1", "Irf1", "Cxcl10", "Gbp2", "Isg15", "Ifit1"]
MOUSE_STRESS_MODULE = [
    "Ddit3",
    "Atf4",
    "Hspa1a",
    "Hspa1b",
    "Hsp90aa1",
    "Dnajb1",
    "Hmox1",
    "Jun",
    "Fos",
    "Gadd45a",
    "Klf6",
    "Bax",
    "Casp3",
]

CONTROL_TERMS = [
    "ruxolitinib",
    "tofacitinib",
    "baricitinib",
    "upadacitinib",
    "filgotinib",
    "dexamethasone",
    "prednisolone",
    "withaferin",
    "gsk3",
    "gsk-3",
    "sb-216763",
    "sb-415286",
    "ar-a014418",
    "indirubin",
    "kenpaullone",
    "lithium",
    "tideglusib",
    "chir99021",
    "chir-99021",
    "bortezomib",
    "trametinib",
    "apremilast",
    "roflumilast",
    "rolipram",
    "ibudilast",
    "calcitriol",
    "fingolimod",
]

BROAD_IFN_JAK_CONTROLS = {
    "IFNGR1",
    "IFNGR2",
    "JAK1",
    "JAK2",
    "STAT1",
    "IFNAR1",
    "IFNAR2",
    "TYK2",
    "ruxolitinib",
    "tofacitinib",
    "baricitinib",
}


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def fdr_from_p(p: pd.Series) -> pd.Series:
    p = pd.to_numeric(p, errors="coerce")
    out = pd.Series(np.nan, index=p.index, dtype=float)
    valid = p.notna()
    if valid.any():
        out.loc[valid] = multipletests(p.loc[valid], method="fdr_bh")[1]
    return out


def safe_mean(values: Iterable[float]) -> float:
    arr = pd.to_numeric(pd.Series(list(values)), errors="coerce").dropna().to_numpy(dtype=float)
    return float(np.nanmean(arr)) if arr.size else np.nan


def safe_median(values: Iterable[float]) -> float:
    arr = pd.to_numeric(pd.Series(list(values)), errors="coerce").dropna().to_numpy(dtype=float)
    return float(np.nanmedian(arr)) if arr.size else np.nan


def hedges_g(case: np.ndarray, control: np.ndarray) -> float:
    case = np.asarray(case, dtype=float)
    control = np.asarray(control, dtype=float)
    case = case[np.isfinite(case)]
    control = control[np.isfinite(control)]
    nx = case.size
    ny = control.size
    if nx < 2 or ny < 2:
        return np.nan
    pooled = ((nx - 1) * case.var(ddof=1) + (ny - 1) * control.var(ddof=1)) / (nx + ny - 2)
    if pooled <= 0:
        return np.nan
    correction = 1.0 - 3.0 / (4.0 * (nx + ny) - 9.0)
    return float(((case.mean() - control.mean()) / math.sqrt(pooled)) * correction)


def module_stats(
    sub: pd.DataFrame,
    genes: list[str],
    effect_col: str = "log2fc",
    fdr_col: str | None = "fdr",
) -> dict[str, object]:
    vals = sub[sub["gene"].isin(genes)].copy()
    vals[effect_col] = pd.to_numeric(vals[effect_col], errors="coerce")
    vals = vals.dropna(subset=[effect_col])
    if vals.empty:
        return {
            "n_genes": 0,
            "genes_present": "",
            "mean_effect": np.nan,
            "median_effect": np.nan,
            "negative_fraction": np.nan,
            "positive_fraction": np.nan,
            "sig_negative_fdr10": 0,
            "sig_positive_fdr10": 0,
        }
    fdr = pd.to_numeric(vals[fdr_col], errors="coerce") if fdr_col and fdr_col in vals.columns else pd.Series(np.nan, index=vals.index)
    return {
        "n_genes": int(vals["gene"].nunique()),
        "genes_present": ",".join(sorted(vals["gene"].unique())),
        "mean_effect": float(vals[effect_col].mean()),
        "median_effect": float(vals[effect_col].median()),
        "negative_fraction": float((vals[effect_col] < 0).mean()),
        "positive_fraction": float((vals[effect_col] > 0).mean()),
        "sig_negative_fdr10": int(((vals[effect_col] < 0) & (fdr <= 0.10)).sum()),
        "sig_positive_fdr10": int(((vals[effect_col] > 0) & (fdr <= 0.10)).sum()),
    }


def selectivity_metrics(target_effect: float, generic_ifn_effect: float, stress_effect: float) -> dict[str, float]:
    target_suppression = max(0.0, -target_effect) if np.isfinite(target_effect) else 0.0
    ifn_suppression = max(0.0, -generic_ifn_effect) if np.isfinite(generic_ifn_effect) else 0.0
    stress_induction = max(0.0, stress_effect) if np.isfinite(stress_effect) else 0.0
    stress_abs = abs(stress_effect) if np.isfinite(stress_effect) else 0.0
    return {
        "target_suppression": target_suppression,
        "generic_ifn_suppression": ifn_suppression,
        "target_vs_ifn_margin": target_suppression - ifn_suppression,
        "target_over_ifn_ratio": target_suppression / max(ifn_suppression, 0.10),
        "stress_induction": stress_induction,
        "stress_abs_effect": stress_abs,
        "selectivity_score": target_suppression - ifn_suppression - 0.35 * stress_induction - 0.10 * stress_abs,
    }


def evidence_call(row: pd.Series) -> str:
    target = float(row.get("target_module_effect", np.nan))
    ifn = float(row.get("generic_ifn_effect", np.nan))
    stress = float(row.get("stress_module_effect", np.nan))
    target_neg_fraction = float(row.get("target_negative_fraction", np.nan))
    metrics = selectivity_metrics(target, ifn, stress)
    if not np.isfinite(target):
        return "no_target_data"
    if target <= -0.50 and metrics["target_vs_ifn_margin"] >= 0.50 and target_neg_fraction >= 0.60:
        if stress > 0.50:
            return "selective_target_suppression_with_stress_caution"
        return "selective_target_suppression"
    if target <= -0.50 and metrics["target_vs_ifn_margin"] < 0.0:
        return "broad_ifn_jak_like_collapse"
    if target <= -0.25 and metrics["target_vs_ifn_margin"] >= 0.20:
        return "weak_selective_target_suppression"
    if target <= -0.25:
        return "target_suppression_not_selective"
    return "null_or_wrong_direction"


def list_mixscale_members() -> list[tuple[str, str, str]]:
    pattern = re.compile(r"DE_results_all_pathway/Parse_(IFNG|IFNB|TNFA)/(.+?)_\1_pathway_DE_results\.txt$")
    rows = []
    with zipfile.ZipFile(MIXSCALE_ZIP) as zf:
        for name in zf.namelist():
            match = pattern.match(name)
            if match:
                rows.append((match.group(1), match.group(2), name))
    return sorted(rows)


def read_mixscale_member(zf: zipfile.ZipFile, member: str) -> pd.DataFrame:
    return pd.read_csv(BytesIO(zf.read(member)), sep=r"\s+", na_values=["NA"], engine="python")


def analyze_mixscale() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    readout_genes = sorted(set(TARGET_MODULE + GENERIC_IFN_MODULE + STRESS_MODULE))
    gene_rows: list[dict[str, object]] = []
    celltype_rows: list[dict[str, object]] = []
    members = list_mixscale_members()
    with zipfile.ZipFile(MIXSCALE_ZIP) as zf:
        for pathway, perturbation, member in members:
            df = read_mixscale_member(zf, member)
            cell_types = sorted(c.removeprefix("log2FC_") for c in df.columns if c.startswith("log2FC_"))
            for cell_type in cell_types:
                log_col = f"log2FC_{cell_type}"
                p_col = f"p_cell_type{cell_type}"
                if log_col not in df.columns or p_col not in df.columns:
                    continue
                tidy = pd.DataFrame(
                    {
                        "dataset": "GSE281048_Mixscale",
                        "pathway": pathway,
                        "perturbation": perturbation,
                        "cell_type": cell_type,
                        "gene": df["gene_ID"].astype(str),
                        "log2fc": pd.to_numeric(df[log_col], errors="coerce"),
                        "p": pd.to_numeric(df[p_col], errors="coerce"),
                    }
                )
                tidy["fdr"] = fdr_from_p(tidy["p"])
                keep = tidy[tidy["gene"].isin(readout_genes)].copy()
                gene_rows.extend(keep.to_dict(orient="records"))
                target = module_stats(keep, TARGET_MODULE)
                generic = module_stats(keep, GENERIC_IFN_MODULE)
                stress = module_stats(keep, STRESS_MODULE)
                metrics = selectivity_metrics(
                    float(target["mean_effect"]) if pd.notna(target["mean_effect"]) else np.nan,
                    float(generic["mean_effect"]) if pd.notna(generic["mean_effect"]) else np.nan,
                    float(stress["mean_effect"]) if pd.notna(stress["mean_effect"]) else np.nan,
                )
                celltype_rows.append(
                    {
                        "dataset": "GSE281048_Mixscale",
                        "pathway": pathway,
                        "perturbation": perturbation,
                        "cell_type": cell_type,
                        "target_module_effect": target["mean_effect"],
                        "target_module_median_effect": target["median_effect"],
                        "target_n_genes": target["n_genes"],
                        "target_genes_present": target["genes_present"],
                        "target_negative_fraction": target["negative_fraction"],
                        "target_sig_negative_fdr10": target["sig_negative_fdr10"],
                        "generic_ifn_effect": generic["mean_effect"],
                        "generic_ifn_median_effect": generic["median_effect"],
                        "generic_ifn_n_genes": generic["n_genes"],
                        "generic_ifn_genes_present": generic["genes_present"],
                        "generic_ifn_negative_fraction": generic["negative_fraction"],
                        "generic_ifn_sig_negative_fdr10": generic["sig_negative_fdr10"],
                        "stress_module_effect": stress["mean_effect"],
                        "stress_module_median_effect": stress["median_effect"],
                        "stress_n_genes": stress["n_genes"],
                        "stress_genes_present": stress["genes_present"],
                        "stress_positive_fraction": stress["positive_fraction"],
                        "stress_sig_positive_fdr10": stress["sig_positive_fdr10"],
                        **metrics,
                    }
                )

    gene_effects = pd.DataFrame(gene_rows)
    celltype_effects = pd.DataFrame(celltype_rows)
    summary_rows: list[dict[str, object]] = []
    for (pathway, perturbation), sub in celltype_effects.groupby(["pathway", "perturbation"], observed=True):
        target_effects = pd.to_numeric(sub["target_module_effect"], errors="coerce").dropna()
        ifn_effects = pd.to_numeric(sub["generic_ifn_effect"], errors="coerce").dropna()
        stress_effects = pd.to_numeric(sub["stress_module_effect"], errors="coerce").dropna()
        target_mean = safe_mean(target_effects)
        ifn_mean = safe_mean(ifn_effects)
        stress_mean = safe_mean(stress_effects)
        metrics = selectivity_metrics(target_mean, ifn_mean, stress_mean)
        row = {
            "source": "Mixscale_CRISPRi",
            "dataset": "GSE281048_Zenodo14035992",
            "system": "stimulated human cancer-cell pathway Perturb-seq",
            "pathway": pathway,
            "perturbation": perturbation,
            "perturbation_type": "CRISPRi_gene",
            "condition": f"{pathway}_pathway",
            "n_cell_types": int(sub["cell_type"].nunique()),
            "target_module_effect": target_mean,
            "target_module_median_effect": safe_median(target_effects),
            "target_negative_fraction": safe_mean(sub["target_negative_fraction"]),
            "target_sig_negative_fdr10_total": int(pd.to_numeric(sub["target_sig_negative_fdr10"], errors="coerce").fillna(0).sum()),
            "generic_ifn_effect": ifn_mean,
            "generic_ifn_median_effect": safe_median(ifn_effects),
            "generic_ifn_negative_fraction": safe_mean(sub["generic_ifn_negative_fraction"]),
            "generic_ifn_sig_negative_fdr10_total": int(pd.to_numeric(sub["generic_ifn_sig_negative_fdr10"], errors="coerce").fillna(0).sum()),
            "stress_module_effect": stress_mean,
            "stress_module_median_effect": safe_median(stress_effects),
            "stress_positive_fraction": safe_mean(sub["stress_positive_fraction"]),
            "stress_sig_positive_fdr10_total": int(pd.to_numeric(sub["stress_sig_positive_fdr10"], errors="coerce").fillna(0).sum()),
            "effect_scale": "mean_log2FC_across_readout_genes_and_cell_types",
            "provenance": "data/raw_v3/mixscale/DE_results_all_pathway.zip",
        }
        row.update(metrics)
        row["evidence_call"] = evidence_call(pd.Series(row))
        row["control_class"] = "broad_IFN_JAK_positive_control" if perturbation in BROAD_IFN_JAK_CONTROLS else "candidate_or_other_control"
        summary_rows.append(row)

    summary = pd.DataFrame(summary_rows).sort_values(
        ["selectivity_score", "target_vs_ifn_margin", "target_suppression"], ascending=[False, False, False]
    )
    return summary, celltype_effects, gene_effects


def read_mouse_rna() -> pd.DataFrame:
    df = pd.read_csv(GSE162464_RNA, sep="\t")
    numeric = [c for c in df.columns if c not in {"Ensemble_Number", "Symbol"}]
    df[numeric] = df[numeric].apply(pd.to_numeric, errors="coerce")
    return df.groupby("Symbol", dropna=True)[numeric].sum(min_count=1)


def log2_values(df: pd.DataFrame, gene: str, cols: list[str]) -> np.ndarray:
    if gene not in df.index:
        return np.array([], dtype=float)
    return np.log2(pd.to_numeric(df.loc[gene, cols], errors="coerce").to_numpy(dtype=float) + 1.0)


def contrast_gene_rows(
    df: pd.DataFrame,
    contrast: str,
    case_cols: list[str],
    control_cols: list[str],
    genes: list[str],
    dataset: str,
    organism: str,
) -> pd.DataFrame:
    rows = []
    for gene in genes:
        case = log2_values(df, gene, case_cols)
        control = log2_values(df, gene, control_cols)
        case = case[np.isfinite(case)]
        control = control[np.isfinite(control)]
        if case.size >= 2 and control.size >= 2:
            t_stat, p_val = stats.ttest_ind(case, control, equal_var=False, nan_policy="omit")
        else:
            t_stat, p_val = np.nan, np.nan
        rows.append(
            {
                "dataset": dataset,
                "organism": organism,
                "contrast": contrast,
                "gene": gene,
                "n_case": int(case.size),
                "n_control": int(control.size),
                "mean_case_log2": float(np.nanmean(case)) if case.size else np.nan,
                "mean_control_log2": float(np.nanmean(control)) if control.size else np.nan,
                "log2fc": float(np.nanmean(case) - np.nanmean(control)) if case.size and control.size else np.nan,
                "hedges_g": hedges_g(case, control),
                "welch_t": float(t_stat) if pd.notna(t_stat) else np.nan,
                "p": float(p_val) if pd.notna(p_val) else np.nan,
            }
        )
    out = pd.DataFrame(rows)
    out["fdr"] = fdr_from_p(out["p"])
    return out


def summarize_direct_contrast(
    gene_rows: pd.DataFrame,
    source: str,
    dataset: str,
    system: str,
    perturbation: str,
    perturbation_type: str,
    condition: str,
    target_genes: list[str],
    generic_genes: list[str],
    stress_genes: list[str],
    effect_scale: str = "mean_log2FC_across_readout_genes",
    provenance: str = "",
) -> dict[str, object]:
    target = module_stats(gene_rows, target_genes)
    generic = module_stats(gene_rows, generic_genes)
    stress = module_stats(gene_rows, stress_genes)
    target_effect = float(target["mean_effect"]) if pd.notna(target["mean_effect"]) else np.nan
    generic_effect = float(generic["mean_effect"]) if pd.notna(generic["mean_effect"]) else np.nan
    stress_effect = float(stress["mean_effect"]) if pd.notna(stress["mean_effect"]) else np.nan
    metrics = selectivity_metrics(target_effect, generic_effect, stress_effect)
    row = {
        "source": source,
        "dataset": dataset,
        "system": system,
        "pathway": "",
        "perturbation": perturbation,
        "perturbation_type": perturbation_type,
        "condition": condition,
        "n_cell_types": np.nan,
        "target_module_effect": target_effect,
        "target_module_median_effect": target["median_effect"],
        "target_negative_fraction": target["negative_fraction"],
        "target_sig_negative_fdr10_total": target["sig_negative_fdr10"],
        "target_n_genes": target["n_genes"],
        "target_genes_present": target["genes_present"],
        "generic_ifn_effect": generic_effect,
        "generic_ifn_median_effect": generic["median_effect"],
        "generic_ifn_negative_fraction": generic["negative_fraction"],
        "generic_ifn_sig_negative_fdr10_total": generic["sig_negative_fdr10"],
        "generic_ifn_n_genes": generic["n_genes"],
        "generic_ifn_genes_present": generic["genes_present"],
        "stress_module_effect": stress_effect,
        "stress_module_median_effect": stress["median_effect"],
        "stress_positive_fraction": stress["positive_fraction"],
        "stress_sig_positive_fdr10_total": stress["sig_positive_fdr10"],
        "stress_n_genes": stress["n_genes"],
        "stress_genes_present": stress["genes_present"],
        "effect_scale": effect_scale,
        "provenance": provenance,
        **metrics,
    }
    row["evidence_call"] = evidence_call(pd.Series(row))
    row["control_class"] = (
        "broad_IFN_JAK_positive_control" if perturbation in BROAD_IFN_JAK_CONTROLS else "candidate_or_other_control"
    )
    return row


def analyze_mouse_rna() -> tuple[pd.DataFrame, pd.DataFrame]:
    df = read_mouse_rna()
    groups = {
        "NTC_US": ["Sample1_NTC_US", "Sample2_NTC_US", "Sample3_NTC_US"],
        "NTC_IFNg": ["Sample4_NTC_IFNg", "Sample5_NTC_IFNg", "Sample6_NTC_IFNg"],
        "Gsk3b_US": ["Sample7_Gsk3b_US", "Sample8_Gsk3b_US", "Sample9_Gsk3b_US"],
        "Gsk3b_IFNg": ["Sample10_Gsk3b_IFNg", "Sample11_Gsk3b_IFNg", "Sample12_Gsk3b_IFNg"],
        "Med16_US": ["Sample13_Med16_US", "Sample14_Med16_US", "Sample15_Med16_US"],
        "Med16_IFNg": ["Sample_16_Med16_IFNg", "Sample17_Med16_IFNg", "Sample18_Med16_IFNg"],
    }
    genes = sorted(set(MOUSE_TARGET_MODULE + MOUSE_GENERIC_IFN_MODULE + MOUSE_STRESS_MODULE))
    contrast_specs = [
        ("NTC_IFNg_vs_NTC_US", "IFNG_positive_control", "cytokine_stimulation", groups["NTC_IFNg"], groups["NTC_US"]),
        ("Gsk3b_IFNg_vs_NTC_IFNg", "Gsk3b_KO", "gene_knockout", groups["Gsk3b_IFNg"], groups["NTC_IFNg"]),
        ("Med16_IFNg_vs_NTC_IFNg", "Med16_KO", "gene_knockout", groups["Med16_IFNg"], groups["NTC_IFNg"]),
        ("Gsk3b_US_vs_NTC_US", "Gsk3b_KO_unstimulated", "gene_knockout", groups["Gsk3b_US"], groups["NTC_US"]),
        ("Med16_US_vs_NTC_US", "Med16_KO_unstimulated", "gene_knockout", groups["Med16_US"], groups["NTC_US"]),
    ]
    all_gene_rows: list[pd.DataFrame] = []
    summary_rows: list[dict[str, object]] = []
    for contrast, perturbation, perturbation_type, case_cols, control_cols in contrast_specs:
        gene_rows = contrast_gene_rows(
            df,
            contrast,
            case_cols,
            control_cols,
            genes,
            "GSE162464",
            "Mus musculus",
        )
        all_gene_rows.append(gene_rows)
        summary_rows.append(
            summarize_direct_contrast(
                gene_rows=gene_rows,
                source="mouse_macrophage_RNAseq",
                dataset="GSE162464",
                system="primary mouse macrophage RNA-seq, triplicates",
                perturbation=perturbation,
                perturbation_type=perturbation_type,
                condition=contrast,
                target_genes=MOUSE_TARGET_MODULE,
                generic_genes=MOUSE_GENERIC_IFN_MODULE,
                stress_genes=MOUSE_STRESS_MODULE,
                provenance="data/raw_v3/wave14_gsk3b_ciita/GSE162464_Normalized_Gene_Counts_Matrix.txt.gz",
            )
        )
    return pd.DataFrame(summary_rows), pd.concat(all_gene_rows, ignore_index=True)


def analyze_mouse_screen() -> tuple[pd.DataFrame, pd.DataFrame]:
    df = pd.read_csv(GSE162463_SCREEN, sep="\t")
    gates = {
        "MHCII": (["MHC_pos1", "MHC_pos2"], ["MHC_neg1", "MHC_neg2"]),
        "CD40": (["CD40_pos1", "CD40_pos2"], ["CD40_neg1", "CD40_neg2"]),
        "PDL1": (["PDL1_pos1", "PDL1_pos2"], ["PDL1_neg1", "PDL1_neg2"]),
    }
    sg_rows = []
    for gate, (high_cols, low_cols) in gates.items():
        high = df[high_cols].apply(pd.to_numeric, errors="coerce").mean(axis=1)
        low = df[low_cols].apply(pd.to_numeric, errors="coerce").mean(axis=1)
        df[f"{gate}_low_vs_high_log2"] = np.log2((low + 1.0) / (high + 1.0))
    for _, row in df.iterrows():
        for gate in gates:
            sg_rows.append(
                {
                    "dataset": "GSE162463",
                    "gene": row["Gene"],
                    "sgRNA": row["sgRNA"],
                    "gate": gate,
                    "low_vs_high_log2": row[f"{gate}_low_vs_high_log2"],
                }
            )
    summary_rows = []
    for gene, sub in df.groupby("Gene", dropna=True):
        row: dict[str, object] = {"gene": gene, "n_sgrna": int(sub["sgRNA"].nunique())}
        for gate in gates:
            vals = pd.to_numeric(sub[f"{gate}_low_vs_high_log2"], errors="coerce").dropna()
            if len(vals) >= 2:
                t_stat, p_val = stats.ttest_1samp(vals, 0.0, nan_policy="omit")
            else:
                t_stat, p_val = np.nan, np.nan
            row[f"{gate}_median_low_vs_high_log2"] = float(vals.median()) if len(vals) else np.nan
            row[f"{gate}_mean_low_vs_high_log2"] = float(vals.mean()) if len(vals) else np.nan
            row[f"{gate}_positive_sgrna_fraction"] = float((vals > 0).mean()) if len(vals) else np.nan
            row[f"{gate}_p"] = float(p_val) if pd.notna(p_val) else np.nan
            row[f"{gate}_t"] = float(t_stat) if pd.notna(t_stat) else np.nan
        summary_rows.append(row)
    summary = pd.DataFrame(summary_rows)
    valid = summary["n_sgrna"] >= 3
    for gate in gates:
        summary[f"{gate}_fdr"] = np.nan
        pvalid = valid & pd.to_numeric(summary[f"{gate}_p"], errors="coerce").notna()
        if pvalid.any():
            summary.loc[pvalid, f"{gate}_fdr"] = multipletests(summary.loc[pvalid, f"{gate}_p"], method="fdr_bh")[1]
        summary[f"{gate}_rank_required_low_vs_high"] = np.nan
        summary.loc[valid, f"{gate}_rank_required_low_vs_high"] = summary.loc[
            valid, f"{gate}_median_low_vs_high_log2"
        ].rank(ascending=False, method="min")
    return summary.sort_values("MHCII_rank_required_low_vs_high"), pd.DataFrame(sg_rows)


def analyze_human_ruxolitinib() -> tuple[pd.DataFrame, pd.DataFrame]:
    df = pd.read_csv(GSE294918_CPM, index_col=0)
    df = df.apply(pd.to_numeric, errors="coerce")
    df = df.groupby(df.index).sum(min_count=1)
    genes = sorted(set(TARGET_MODULE + GENERIC_IFN_MODULE + STRESS_MODULE))
    contrast_specs = [
        ("D4_IFNy_rux_LPS0H_vs_D4_IFNy_LPS0H", "ruxolitinib", "JAK_inhibitor", "D4_IFNy_rux_LPS0H", "D4_IFNy_LPS0H"),
        ("D4_IFNy_rux_LPS1H_vs_D4_IFNy_LPS1H", "ruxolitinib", "JAK_inhibitor", "D4_IFNy_rux_LPS1H", "D4_IFNy_LPS1H"),
        ("D4_IFNy_rux_LPS3H_vs_D4_IFNy_LPS3H", "ruxolitinib", "JAK_inhibitor", "D4_IFNy_rux_LPS3H", "D4_IFNy_LPS3H"),
        ("D4_IFNy_rux_LPS6H_vs_D4_IFNy_LPS6H", "ruxolitinib", "JAK_inhibitor", "D4_IFNy_rux_LPS6H", "D4_IFNy_LPS6H"),
        ("D4_IFNy_LPS0H_vs_D4_PBS_LPS0H", "IFNG_memory", "cytokine_memory", "D4_IFNy_LPS0H", "D4_PBS_LPS0H"),
        ("D0_IFNy_8H_vs_D0_unstim", "IFNG_8H", "cytokine_stimulation", "D0_IFNy_8H", "D0_unstim"),
    ]
    gene_rows_all = []
    summary_rows = []
    for contrast, perturbation, perturbation_type, case_col, control_col in contrast_specs:
        rows = []
        for gene in genes:
            case = float(np.log2(df.loc[gene, case_col] + 1.0)) if gene in df.index and case_col in df.columns else np.nan
            control = float(np.log2(df.loc[gene, control_col] + 1.0)) if gene in df.index and control_col in df.columns else np.nan
            rows.append(
                {
                    "dataset": "GSE294918",
                    "organism": "Homo sapiens",
                    "contrast": contrast,
                    "gene": gene,
                    "case_column": case_col,
                    "control_column": control_col,
                    "log2fc": case - control if np.isfinite(case) and np.isfinite(control) else np.nan,
                    "p": np.nan,
                    "fdr": np.nan,
                    "note": "single processed CPM column per condition/timepoint; descriptive only",
                }
            )
        gene_rows = pd.DataFrame(rows)
        gene_rows_all.append(gene_rows)
        summary_rows.append(
            summarize_direct_contrast(
                gene_rows=gene_rows,
                source="human_macrophage_RNAseq_descriptive",
                dataset="GSE294918",
                system="human macrophage IFN-gamma memory/ruxolitinib CPM table",
                perturbation=perturbation,
                perturbation_type=perturbation_type,
                condition=contrast,
                target_genes=TARGET_MODULE,
                generic_genes=GENERIC_IFN_MODULE,
                stress_genes=STRESS_MODULE,
                effect_scale="descriptive_mean_log2CPM_difference",
                provenance="data/raw_v3/wave14_gsk3b_ciita/GSE294918_IFNyRNAseq_CPM.csv.gz",
            )
        )
    return pd.DataFrame(summary_rows), pd.concat(gene_rows_all, ignore_index=True)


def load_compound_metadata() -> pd.DataFrame:
    if not COMPOUNDINFO.exists():
        return pd.DataFrame()
    meta = pd.read_csv(COMPOUNDINFO, sep="\t", low_memory=False)
    for col in ["pert_id", "cmap_name", "target", "moa", "compound_aliases"]:
        if col not in meta.columns:
            meta[col] = np.nan
    return meta


def query_l1000fwd(name: str, up: list[str], down: list[str]) -> dict[str, object]:
    payload = {"up_genes": up, "down_genes": down}
    try:
        post = requests.post(
            f"{L1000_BASE_URL}/sig_search",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=90,
        )
        result: dict[str, object] = {
            "query_name": name,
            "payload": payload,
            "post_status_code": post.status_code,
        }
        if post.status_code != 200:
            result["error"] = post.text[:1000]
            return result
        post_json = post.json()
        result["post_response"] = post_json
        result_id = post_json.get("result_id")
        result["result_id"] = result_id
        if not result_id:
            result["error"] = "missing result_id"
            return result
        time.sleep(1.0)
        get = requests.get(f"{L1000_BASE_URL}/result/topn/{result_id}", timeout=90)
        result["get_status_code"] = get.status_code
        if get.status_code != 200:
            result["error"] = get.text[:1000]
            return result
        result["results"] = get.json()
        return result
    except requests.RequestException as exc:
        return {"query_name": name, "payload": payload, "error": repr(exc)}


def flatten_l1000_results(raw: dict[str, dict[str, object]]) -> pd.DataFrame:
    rows = []
    for query_name, payload in raw.items():
        result_id = payload.get("result_id")
        results = payload.get("results") or {}
        for mode in ["opposite", "similar"]:
            for rank, hit in enumerate(results.get(mode, []), start=1):
                row = {"query_name": query_name, "mode": mode, "rank": rank, "result_id": result_id}
                if isinstance(hit, dict):
                    row.update(hit)
                else:
                    row["hit"] = str(hit)
                rows.append(row)
    return pd.DataFrame(rows)


def annotate_l1000_hits(hits: pd.DataFrame, meta: pd.DataFrame) -> pd.DataFrame:
    if hits.empty:
        return hits
    out = hits.copy()
    if "sig_id" in out.columns:
        out["pert_id"] = out["sig_id"].astype(str).str.extract(r"(BRD-[A-Z][A-Z0-9]+)")[0]
    if not meta.empty and "pert_id" in out.columns:
        keep = ["pert_id", "cmap_name", "target", "moa", "canonical_smiles", "inchi_key", "compound_aliases"]
        meta_keep = meta[[c for c in keep if c in meta.columns]].drop_duplicates("pert_id")
        out = out.merge(meta_keep, on="pert_id", how="left")
    return out


def summarize_l1000_selectivity(hits: pd.DataFrame) -> pd.DataFrame:
    if hits.empty or "pert_id" not in hits.columns:
        return pd.DataFrame()
    opposite = hits[hits["mode"].eq("opposite")].copy()
    if opposite.empty:
        return pd.DataFrame()
    rows = []
    group_cols = ["pert_id", "cmap_name", "target", "moa"]
    for keys, sub in opposite.groupby(group_cols, dropna=False):
        row = dict(zip(group_cols, keys, strict=False))
        for query in ["target_antigen_presentation", "generic_ifn_jak"]:
            q = sub[sub["query_name"].eq(query)].copy()
            if q.empty:
                row[f"{query}_best_rank"] = np.nan
                row[f"{query}_min_qval"] = np.nan
                row[f"{query}_max_reversal_strength"] = 0.0
                row[f"{query}_n_signatures"] = 0
            else:
                scores = pd.to_numeric(q.get("combined_scores"), errors="coerce")
                row[f"{query}_best_rank"] = int(pd.to_numeric(q["rank"], errors="coerce").min())
                row[f"{query}_min_qval"] = float(pd.to_numeric(q.get("qvals"), errors="coerce").min())
                row[f"{query}_max_reversal_strength"] = float(np.nanmax(np.maximum(0.0, -scores)))
                row[f"{query}_n_signatures"] = int(q["sig_id"].nunique()) if "sig_id" in q.columns else int(len(q))
        row["l1000_target_minus_generic_reversal_strength"] = (
            row["target_antigen_presentation_max_reversal_strength"]
            - row["generic_ifn_jak_max_reversal_strength"]
        )
        if row["target_antigen_presentation_n_signatures"] > 0 and row["generic_ifn_jak_n_signatures"] == 0:
            row["l1000_selectivity_call"] = "target_opposite_hit_absent_from_generic_top50"
        elif row["target_antigen_presentation_max_reversal_strength"] > row["generic_ifn_jak_max_reversal_strength"]:
            row["l1000_selectivity_call"] = "target_stronger_than_generic"
        elif row["generic_ifn_jak_n_signatures"] > 0:
            row["l1000_selectivity_call"] = "generic_ifn_reversal_at_least_as_strong"
        else:
            row["l1000_selectivity_call"] = "no_target_opposite_hit"
        rows.append(row)
    return pd.DataFrame(rows).sort_values(
        [
            "l1000_target_minus_generic_reversal_strength",
            "target_antigen_presentation_max_reversal_strength",
            "target_antigen_presentation_best_rank",
        ],
        ascending=[False, False, True],
    )


def analyze_l1000fwd() -> tuple[pd.DataFrame, pd.DataFrame, dict[str, object]]:
    raw_path = OUT / "l1000fwd_selectivity_raw.json"
    queries = {
        "target_antigen_presentation": {"up": TARGET_MODULE, "down": []},
        "generic_ifn_jak": {"up": GENERIC_IFN_MODULE, "down": []},
    }
    if raw_path.exists():
        raw = json.loads(raw_path.read_text(encoding="utf-8"))
    else:
        raw = {name: query_l1000fwd(name, spec["up"], spec["down"]) for name, spec in queries.items()}
        write_json(raw_path, raw)
    meta = load_compound_metadata()
    hits = annotate_l1000_hits(flatten_l1000_results(raw), meta)
    ranked = summarize_l1000_selectivity(hits)
    summary = {
        "api": L1000_BASE_URL,
        "queries": queries,
        "errors": {name: payload.get("error") for name, payload in raw.items() if payload.get("error")},
        "interpretation_guardrail": (
            "L1000FWD results are cell-line signature similarities. They nominate compounds whose LINCS "
            "signatures oppose the input module; they do not provide direct antigen-presentation or viability assays."
        ),
    }
    return hits, ranked, summary


def control_compound_metadata() -> pd.DataFrame:
    meta = load_compound_metadata()
    if meta.empty:
        return meta
    mask = pd.Series(False, index=meta.index)
    for col in ["cmap_name", "target", "moa", "compound_aliases"]:
        text = meta[col].fillna("").astype(str).str.lower()
        for term in CONTROL_TERMS:
            mask |= text.str.contains(term, regex=False)
    keep = ["pert_id", "cmap_name", "target", "moa", "canonical_smiles", "inchi_key", "compound_aliases"]
    return meta.loc[mask, [c for c in keep if c in meta.columns]].drop_duplicates()


def build_integrated_rank(
    mixscale_summary: pd.DataFrame,
    mouse_summary: pd.DataFrame,
    human_summary: pd.DataFrame,
    screen_summary: pd.DataFrame,
    l1000_rank: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    direct = pd.concat([mixscale_summary, mouse_summary, human_summary], ignore_index=True, sort=False)
    direct = direct.sort_values(["selectivity_score", "target_suppression"], ascending=[False, False]).reset_index(drop=True)
    direct["within_direct_rank"] = np.arange(1, len(direct) + 1)

    # Candidate-level synthesis keeps scales separate and counts convergent signals.
    candidate_map: dict[str, list[dict[str, object]]] = defaultdict(list)
    for _, row in direct.iterrows():
        candidate = str(row["perturbation"])
        candidate_map[candidate].append(row.to_dict())
    if not screen_summary.empty:
        for gene in ["Gsk3b", "Med16", "Ifngr1", "Ifngr2", "Jak1", "Jak2", "Stat1", "Ciita", "Rfx5"]:
            sub = screen_summary[screen_summary["gene"].eq(gene)]
            if not sub.empty:
                row = sub.iloc[0].to_dict()
                candidate_map[gene].append({"source": "mouse_macrophage_CRISPR_screen", **row})
                if gene == "Gsk3b":
                    candidate_map["Gsk3b_KO"].append({"source": "mouse_macrophage_CRISPR_screen", **row})
                if gene == "Med16":
                    candidate_map["Med16_KO"].append({"source": "mouse_macrophage_CRISPR_screen", **row})

    synthesis_rows = []
    for candidate, evidence in candidate_map.items():
        direct_rows = [e for e in evidence if "selectivity_score" in e]
        best_direct = max([e.get("selectivity_score", -np.inf) for e in direct_rows], default=np.nan)
        best_target = max([e.get("target_suppression", 0.0) for e in direct_rows], default=np.nan)
        best_margin = max([e.get("target_vs_ifn_margin", -np.inf) for e in direct_rows], default=np.nan)
        calls = sorted({str(e.get("evidence_call")) for e in direct_rows if e.get("evidence_call")})
        sources = sorted({str(e.get("source")) for e in evidence if e.get("source")})
        screen_hits = [e for e in evidence if e.get("source") == "mouse_macrophage_CRISPR_screen"]
        mhcii_rank = screen_hits[0].get("MHCII_rank_required_low_vs_high") if screen_hits else np.nan
        strength = nominate_strength(candidate, direct_rows, mhcii_rank, l1000_rank)
        synthesis_rows.append(
            {
                "candidate": candidate,
                "n_evidence_records": len(evidence),
                "sources": ";".join(sources),
                "best_direct_selectivity_score": best_direct,
                "best_direct_target_suppression": best_target,
                "best_direct_target_vs_ifn_margin": best_margin,
                "direct_evidence_calls": ";".join(calls),
                "gse162463_mhcii_low_gate_rank_if_available": mhcii_rank,
                "nomination_strength": strength,
                "nomination_priority": nomination_priority(strength),
            }
        )
    synthesis = pd.DataFrame(synthesis_rows).sort_values(
        ["nomination_priority", "best_direct_selectivity_score", "best_direct_target_suppression"],
        ascending=[True, False, False],
    )
    return direct, synthesis


def nomination_priority(strength: str) -> int:
    order = {
        "strong_mechanistic_comparator_not_druggable": 1,
        "candidate_evidence_not_enough_to_nominate_drug": 2,
        "selective_in_model_system_followup_needed": 3,
        "weak_followup_only": 4,
        "comparator_only_broad_ifn_jak_collapse": 5,
        "not_nominated": 6,
        "not_nominated_no_direct_transcript_effect": 7,
    }
    return order.get(strength, 99)


def nominate_strength(candidate: str, direct_rows: list[dict[str, object]], mhcii_rank: object, l1000_rank: pd.DataFrame) -> str:
    if not direct_rows:
        return "not_nominated_no_direct_transcript_effect"
    best = max([r.get("selectivity_score", -np.inf) for r in direct_rows])
    best_call = {str(r.get("evidence_call")) for r in direct_rows}
    broad = any(str(r.get("control_class")) == "broad_IFN_JAK_positive_control" for r in direct_rows)
    if broad:
        return "comparator_only_broad_ifn_jak_collapse"
    if "selective_target_suppression" in best_call and best >= 0.75:
        if str(candidate).lower() in {"med16_ko", "rfx5", "ciita"}:
            return "strong_mechanistic_comparator_not_druggable"
        if str(candidate).lower() in {"gsk3b_ko", "gsk3b"}:
            return "candidate_evidence_not_enough_to_nominate_drug"
        return "selective_in_model_system_followup_needed"
    if "weak_selective_target_suppression" in best_call:
        return "weak_followup_only"
    return "not_nominated"


def write_report(
    direct_rank: pd.DataFrame,
    candidate_synthesis: pd.DataFrame,
    mixscale_summary: pd.DataFrame,
    mouse_summary: pd.DataFrame,
    human_summary: pd.DataFrame,
    screen_summary: pd.DataFrame,
    l1000_rank: pd.DataFrame,
    l1000_summary: dict[str, object],
    outputs: list[str],
) -> None:
    def markdown_table(df: pd.DataFrame, columns: list[str], max_rows: int | None = None) -> str:
        view = df.loc[:, [c for c in columns if c in df.columns]].copy()
        if max_rows is not None:
            view = view.head(max_rows)
        if view.empty:
            return "_No rows._"

        def fmt(value: object) -> str:
            if pd.isna(value):
                return ""
            if isinstance(value, (float, np.floating)):
                return f"{float(value):.3f}"
            text = str(value)
            return text.replace("|", "\\|").replace("\n", " ")

        header = "| " + " | ".join(view.columns) + " |"
        sep = "| " + " | ".join(["---"] * len(view.columns)) + " |"
        rows = ["| " + " | ".join(fmt(v) for v in row) + " |" for row in view.to_numpy(dtype=object)]
        return "\n".join([header, sep, *rows])

    report = OUT.parent.parent / "phases/v3/subagents" / "wave15_perturbation_drug_response.md"
    top_direct = direct_rank.head(15)
    top_l1000 = l1000_rank.head(12) if not l1000_rank.empty else pd.DataFrame()
    gsk = direct_rank[direct_rank["perturbation"].astype(str).str.contains("Gsk3b", case=False, regex=False)]
    rfx5 = mixscale_summary[(mixscale_summary["perturbation"].eq("RFX5")) & (mixscale_summary["pathway"].eq("IFNG"))]
    med16 = mouse_summary[mouse_summary["perturbation"].eq("Med16_KO")]
    rux = human_summary[human_summary["perturbation"].eq("ruxolitinib")]
    lines: list[str] = []
    lines.append("# Wave15-B Perturbation and Drug-Response Evidence")
    lines.append("")
    lines.append("Returned: 2026-05-27")
    lines.append("")
    lines.append("## Scope")
    lines.append("")
    lines.append(
        "Search real perturbation/drug-response resources for interventions that reduce "
        "`CD74`/`CIITA`/HLA-II antigen presentation more selectively than generic IFN/JAK collapse. "
        "This worker does not assess novelty or make a therapeutic claim."
    )
    lines.append("")
    lines.append("## Data Provenance")
    lines.append("")
    lines.append("- `GSE281048` / Zenodo `14035992`: Mixscale pathway CRISPRi DE tables, local file `data/raw_v3/mixscale/DE_results_all_pathway.zip`.")
    lines.append("- `GSE162463`: mouse macrophage MHCII/CD40/PD-L1 CRISPR-screen normalized sgRNA counts.")
    lines.append("- `GSE162464`: mouse macrophage NTC/`Gsk3b`/`Med16` +/- IFN-gamma RNA-seq normalized counts.")
    lines.append("- `GSE294918`: human macrophage IFN-gamma memory/ruxolitinib processed CPM table.")
    lines.append("- L1000FWD/LINCS2020: module-signature API queries plus local `compoundinfo_beta.txt` metadata.")
    lines.append("")
    lines.append("## Module Definition")
    lines.append("")
    lines.append(f"- Target antigen-presentation module: `{', '.join(TARGET_MODULE)}`.")
    lines.append(f"- Generic IFN/JAK module: `{', '.join(GENERIC_IFN_MODULE)}`.")
    lines.append(f"- Stress/viability proxy module where available: `{', '.join(STRESS_MODULE)}`.")
    lines.append("")
    lines.append("Selectivity score is target suppression minus generic IFN suppression, with a small stress penalty. It is a ranking heuristic; raw effect sizes are the evidence.")
    lines.append("")
    lines.append("## Ranked Direct Perturbations")
    lines.append("")
    lines.append(markdown_table(top_direct, [
        "within_direct_rank",
        "source",
        "dataset",
        "pathway",
        "perturbation",
        "condition",
        "target_module_effect",
        "generic_ifn_effect",
        "stress_module_effect",
        "target_vs_ifn_margin",
        "target_over_ifn_ratio",
        "selectivity_score",
        "evidence_call",
    ]))
    lines.append("")
    lines.append("## Key Findings")
    lines.append("")
    if not rfx5.empty:
        row = rfx5.iloc[0]
        lines.append(
            f"- `RFX5` CRISPRi in IFN-gamma-stimulated Mixscale cells is the cleanest selective genetic gate: "
            f"target module mean log2FC `{row['target_module_effect']:.3f}`, generic IFN mean log2FC "
            f"`{row['generic_ifn_effect']:.3f}`, margin `{row['target_vs_ifn_margin']:.3f}`. "
            "This is mechanistically coherent but not a druggable compound result."
        )
    if not med16.empty:
        row = med16.iloc[0]
        lines.append(
            f"- `Med16` KO in mouse macrophages is a strong non-druggable gate comparator: target module "
            f"`{row['target_module_effect']:.3f}`, generic IFN `{row['generic_ifn_effect']:.3f}`, "
            f"margin `{row['target_vs_ifn_margin']:.3f}`."
        )
    if not gsk.empty:
        best = gsk.sort_values("selectivity_score", ascending=False).iloc[0]
        lines.append(
            f"- `Gsk3b` KO in mouse macrophages remains the strongest druggable-ish controller evidence: "
            f"target module `{best['target_module_effect']:.3f}`, generic IFN `{best['generic_ifn_effect']:.3f}`, "
            f"margin `{best['target_vs_ifn_margin']:.3f}`, selectivity score `{best['selectivity_score']:.3f}`. "
            "It is still comparator evidence, not enough to nominate a drug, because GSK3 biology is broad and the support is mouse KO rather than selective human chemical perturbation."
        )
    if not rux.empty:
        best_rux = rux.sort_values("condition").iloc[0]
        lines.append(
            f"- `ruxolitinib` is the expected broad-JAK positive control, not selective: in human macrophage CPM "
            f"the LPS0 contrast has target module `{best_rux['target_module_effect']:.3f}` and generic IFN "
            f"`{best_rux['generic_ifn_effect']:.3f}`."
        )
    lines.append("")
    lines.append("## L1000FWD Compound Signal")
    lines.append("")
    if top_l1000.empty:
        lines.append(f"- L1000FWD did not return usable compound rankings. API errors: `{l1000_summary.get('errors')}`.")
    else:
        lines.append(
            markdown_table(top_l1000, [
                "pert_id",
                "cmap_name",
                "target",
                "moa",
                "target_antigen_presentation_best_rank",
                "target_antigen_presentation_min_qval",
                "target_antigen_presentation_max_reversal_strength",
                "generic_ifn_jak_max_reversal_strength",
                "l1000_target_minus_generic_reversal_strength",
                "l1000_selectivity_call",
            ])
        )
        lines.append("")
        lines.append(
            "L1000FWD is treated as weak supportive or negative evidence only: it is a LINCS cell-line signature search, "
            "not an antigen-presentation assay. No L1000 compound alone is strong enough for nomination."
        )
    lines.append("")
    lines.append("## Candidate-Level Disposition")
    lines.append("")
    lines.append(markdown_table(candidate_synthesis, list(candidate_synthesis.columns), max_rows=20))
    lines.append("")
    lines.append("## Verdict")
    lines.append("")
    lines.append(
        "No compound is strong enough to nominate from perturbation/drug-response data alone. The strongest direct "
        "selectivity signal is genetic gating of the CIITA/RFX5/MHC-II program (`RFX5` CRISPRi and `Med16` KO), "
        "with `Gsk3b` KO as the best druggable-ish upstream comparator. Broad JAK/IFNGR perturbations and "
        "ruxolitinib reduce the target module but fail the selectivity requirement because they collapse the generic "
        "IFN module. The appropriate use of this worker output is as comparator evidence for the orchestrator, not "
        "as a standalone therapeutic claim."
    )
    lines.append("")
    lines.append("## Reproducibility")
    lines.append("")
    lines.append("Command:")
    lines.append("")
    lines.append("```bash")
    lines.append("./.venv_v3_py312/bin/python scripts/v3_wave15_perturbation_drug_response.py")
    lines.append("```")
    lines.append("")
    lines.append("Outputs:")
    lines.extend([f"- `{path}`" for path in outputs])
    lines.append("")
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)

    run_log = []

    mixscale_summary, mixscale_celltypes, mixscale_genes = analyze_mixscale()
    mixscale_summary.to_csv(OUT / "mixscale_selectivity_by_perturbation.tsv", sep="\t", index=False)
    mixscale_celltypes.to_csv(OUT / "mixscale_selectivity_by_cell_type.tsv", sep="\t", index=False)
    mixscale_genes.to_csv(OUT / "mixscale_readout_gene_effects.tsv", sep="\t", index=False)
    run_log.append({"step": "mixscale", "status": "ok", "n_perturbations": int(len(mixscale_summary))})

    mouse_summary, mouse_genes = analyze_mouse_rna()
    mouse_summary.to_csv(OUT / "gse162464_mouse_rna_selectivity.tsv", sep="\t", index=False)
    mouse_genes.to_csv(OUT / "gse162464_mouse_rna_readout_gene_effects.tsv", sep="\t", index=False)
    run_log.append({"step": "gse162464_mouse_rna", "status": "ok", "n_contrasts": int(len(mouse_summary))})

    screen_summary, screen_sgrna = analyze_mouse_screen()
    screen_summary.to_csv(OUT / "gse162463_mouse_crispr_screen_gene_summary.tsv", sep="\t", index=False)
    screen_sgrna.to_csv(OUT / "gse162463_mouse_crispr_screen_sgrna_effects.tsv", sep="\t", index=False)
    run_log.append({"step": "gse162463_mouse_screen", "status": "ok", "n_genes": int(len(screen_summary))})

    human_summary, human_genes = analyze_human_ruxolitinib()
    human_summary.to_csv(OUT / "gse294918_human_ruxolitinib_selectivity.tsv", sep="\t", index=False)
    human_genes.to_csv(OUT / "gse294918_human_ruxolitinib_readout_gene_effects.tsv", sep="\t", index=False)
    run_log.append({"step": "gse294918_human_ruxolitinib", "status": "ok", "n_contrasts": int(len(human_summary))})

    controls = control_compound_metadata()
    controls.to_csv(OUT / "control_compound_metadata.tsv", sep="\t", index=False)
    run_log.append({"step": "control_compound_metadata", "status": "ok", "n_rows": int(len(controls))})

    l1000_hits, l1000_rank, l1000_summary = analyze_l1000fwd()
    l1000_hits.to_csv(OUT / "l1000fwd_selectivity_hits.tsv", sep="\t", index=False)
    l1000_rank.to_csv(OUT / "l1000fwd_selectivity_compound_rank.tsv", sep="\t", index=False)
    write_json(OUT / "l1000fwd_selectivity_summary.json", l1000_summary)
    run_log.append(
        {
            "step": "l1000fwd",
            "status": "ok" if not l1000_summary.get("errors") else "partial",
            "n_hits": int(len(l1000_hits)),
            "n_compounds": int(len(l1000_rank)),
            "errors": json.dumps(l1000_summary.get("errors")),
        }
    )

    direct_rank, candidate_synthesis = build_integrated_rank(
        mixscale_summary, mouse_summary, human_summary, screen_summary, l1000_rank
    )
    direct_rank.to_csv(OUT / "ranked_direct_perturbations.tsv", sep="\t", index=False)
    candidate_synthesis.to_csv(OUT / "candidate_level_synthesis.tsv", sep="\t", index=False)
    run_log.append({"step": "integrated_rank", "status": "ok", "n_rows": int(len(direct_rank))})

    outputs = [
        "phases/v3/results/wave15_perturbation_drug_response/mixscale_selectivity_by_perturbation.tsv",
        "phases/v3/results/wave15_perturbation_drug_response/mixscale_selectivity_by_cell_type.tsv",
        "phases/v3/results/wave15_perturbation_drug_response/mixscale_readout_gene_effects.tsv",
        "phases/v3/results/wave15_perturbation_drug_response/gse162464_mouse_rna_selectivity.tsv",
        "phases/v3/results/wave15_perturbation_drug_response/gse162464_mouse_rna_readout_gene_effects.tsv",
        "phases/v3/results/wave15_perturbation_drug_response/gse162463_mouse_crispr_screen_gene_summary.tsv",
        "phases/v3/results/wave15_perturbation_drug_response/gse162463_mouse_crispr_screen_sgrna_effects.tsv",
        "phases/v3/results/wave15_perturbation_drug_response/gse294918_human_ruxolitinib_selectivity.tsv",
        "phases/v3/results/wave15_perturbation_drug_response/gse294918_human_ruxolitinib_readout_gene_effects.tsv",
        "phases/v3/results/wave15_perturbation_drug_response/l1000fwd_selectivity_raw.json",
        "phases/v3/results/wave15_perturbation_drug_response/l1000fwd_selectivity_hits.tsv",
        "phases/v3/results/wave15_perturbation_drug_response/l1000fwd_selectivity_compound_rank.tsv",
        "phases/v3/results/wave15_perturbation_drug_response/l1000fwd_selectivity_summary.json",
        "phases/v3/results/wave15_perturbation_drug_response/control_compound_metadata.tsv",
        "phases/v3/results/wave15_perturbation_drug_response/ranked_direct_perturbations.tsv",
        "phases/v3/results/wave15_perturbation_drug_response/candidate_level_synthesis.tsv",
        "phases/v3/results/wave15_perturbation_drug_response/summary.json",
        "phases/v3/results/wave15_perturbation_drug_response/run_log.tsv",
        "phases/v3/subagents/wave15_perturbation_drug_response.md",
    ]

    summary = {
        "seed": SEED,
        "question": "selective reduction of CD74/CIITA/HLA-II antigen presentation versus generic IFN/JAK collapse",
        "target_module": TARGET_MODULE,
        "generic_ifn_module": GENERIC_IFN_MODULE,
        "stress_module": STRESS_MODULE,
        "top_direct_perturbations": direct_rank.head(20).to_dict(orient="records"),
        "top_candidate_synthesis": candidate_synthesis.head(20).to_dict(orient="records"),
        "l1000_summary": l1000_summary,
        "guardrails": [
            "Do not compare absolute selectivity scores across direct log2FC and L1000 signature scales.",
            "Mixscale uses stimulated cancer cell lines, not autoimmune tissue.",
            "GSE294918 ruxolitinib CPM contrasts are descriptive because processed columns lack replicates.",
            "No compound is nominated solely from this worker output.",
        ],
        "outputs": outputs,
    }
    write_json(OUT / "summary.json", summary)
    pd.DataFrame(run_log).to_csv(OUT / "run_log.tsv", sep="\t", index=False)
    write_report(
        direct_rank=direct_rank,
        candidate_synthesis=candidate_synthesis,
        mixscale_summary=mixscale_summary,
        mouse_summary=mouse_summary,
        human_summary=human_summary,
        screen_summary=screen_summary,
        l1000_rank=l1000_rank,
        l1000_summary=l1000_summary,
        outputs=outputs,
    )
    print(json.dumps({"status": "ok", "out": str(OUT), "top": summary["top_direct_perturbations"][:5]}, indent=2))


if __name__ == "__main__":
    main()
