#!/usr/bin/env python3
"""Wave 14 GSK3B / CIITA perturbation scout.

Question: do public macrophage IFN-gamma perturbation data support GSK3B as an
intervention controller upstream of the CIITA/RFX5/MHC-II/CD74 state, without
collapsing generic IFN signaling?

Inputs are small processed public tables only:

- GSE162463: murine macrophage genome-wide CRISPR screen, normalized sgRNA
  counts from MHCII/CD40/PD-L1 sorted gates.
- GSE162464: matching murine macrophage RNA-seq normalized gene counts from
  NTC, Gsk3b KO, and Med16 KO cells +/- IFN-gamma.
- GSE294918: human macrophage IFN-gamma memory RNA-seq CPM table with a
  ruxolitinib arm.

Raw FASTQ/SRA data are intentionally not downloaded.
"""

from __future__ import annotations

import hashlib
import json
import math
import urllib.request
import warnings
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests

SEED = 20260527
ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw_v3" / "wave14_gsk3b_ciita"
OUT = ROOT / "phases/v3/results" / "wave14_gsk3b_ciita_perturbation"

DOWNLOADS = [
    {
        "accession": "GSE162463",
        "description": "murine macrophage IFN-gamma MHCII/CD40/PD-L1 CRISPR screen normalized sgRNA counts",
        "url": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE162nnn/GSE162463/suppl/GSE162463_sgRNA_CountsNormalized.txt.gz",
        "filename": "GSE162463_sgRNA_CountsNormalized.txt.gz",
    },
    {
        "accession": "GSE162464",
        "description": "murine macrophage NTC/Gsk3b/Med16 +/- IFN-gamma normalized RNA-seq counts",
        "url": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE162nnn/GSE162464/suppl/GSE162464_Normalized_Gene_Counts_Matrix.txt.gz",
        "filename": "GSE162464_Normalized_Gene_Counts_Matrix.txt.gz",
    },
    {
        "accession": "GSE294918",
        "description": "human macrophage IFN-gamma memory/ruxolitinib RNA-seq CPM",
        "url": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE294nnn/GSE294918/suppl/GSE294918_IFNyRNAseq_CPM.csv.gz",
        "filename": "GSE294918_IFNyRNAseq_CPM.csv.gz",
    },
]

MOUSE_MODULES = {
    "ciita_mhc2_cd74": [
        "Ciita",
        "Rfx5",
        "Cd74",
        "H2-Aa",
        "H2-Ab1",
        "H2-Eb1",
        "H2-DMa",
        "H2-DMb1",
        "H2-DMb2",
    ],
    "mhc2_surface_core": ["Cd74", "H2-Aa", "H2-Ab1", "H2-Eb1", "H2-DMa", "H2-DMb1", "H2-DMb2"],
    "generic_ifn_core": [
        "Stat1",
        "Irf1",
        "Cxcl9",
        "Cxcl10",
        "Gbp2",
        "Gbp5",
        "Ifit1",
        "Ifit2",
        "Ifit3",
        "Isg15",
        "Irf7",
        "Oasl2",
        "Tap1",
        "Tap2",
        "B2m",
        "Nlrc5",
        "Igtp",
        "Irgm1",
    ],
    "lysosomal_antigen_processing": ["Ifi30", "Ctss", "Ctsb", "Ctsd", "Ctsl", "Lamp1", "Lamp2", "Lamp3"],
}

HUMAN_MODULES = {
    "ciita_hla2_cd74": [
        "CIITA",
        "RFX5",
        "CD74",
        "HLA-DRA",
        "HLA-DRB1",
        "HLA-DPA1",
        "HLA-DPB1",
        "HLA-DMA",
        "HLA-DMB",
    ],
    "hla2_surface_core": ["CD74", "HLA-DRA", "HLA-DRB1", "HLA-DPA1", "HLA-DPB1", "HLA-DMA", "HLA-DMB"],
    "generic_ifn_core": [
        "STAT1",
        "IRF1",
        "CXCL9",
        "CXCL10",
        "GBP1",
        "GBP2",
        "ISG15",
        "IFIT1",
        "IFIT2",
        "TAP1",
        "TAP2",
        "B2M",
        "NLRC5",
    ],
    "lysosomal_antigen_processing": ["IFI30", "CTSS", "CTSB", "CTSD", "CTSL", "LAMP1", "LAMP2", "LAMP3"],
}

SCREEN_TARGET_GENES = [
    "Gsk3b",
    "Gsk3a",
    "Med16",
    "Ifngr1",
    "Ifngr2",
    "Jak1",
    "Jak2",
    "Stat1",
    "Irf1",
    "Ciita",
    "Rfx5",
    "Cd74",
    "H2-Aa",
    "H2-Ab1",
    "H2-Eb1",
    "Ndufa10",
    "Ndufs1",
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def download_file(url: str, path: Path) -> str:
    if path.exists() and path.stat().st_size > 0:
        return "reused_existing"
    tmp = path.with_suffix(path.suffix + ".tmp")
    req = urllib.request.Request(url, headers={"User-Agent": "ms-auto-research-wave14/1.0"})
    with urllib.request.urlopen(req, timeout=60) as response, tmp.open("wb") as handle:
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            handle.write(chunk)
    tmp.replace(path)
    return "downloaded"


def prepare_inputs() -> pd.DataFrame:
    RAW.mkdir(parents=True, exist_ok=True)
    rows = []
    for item in DOWNLOADS:
        path = RAW / item["filename"]
        status = download_file(item["url"], path)
        rows.append(
            {
                **item,
                "local_path": str(path.relative_to(ROOT)),
                "status": status,
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
                "geo_record": f"https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={item['accession']}",
            }
        )
    return pd.DataFrame(rows)


def adjust_fdr(df: pd.DataFrame, p_col: str = "p") -> pd.DataFrame:
    out = df.copy()
    if p_col not in out.columns or out.empty:
        return out
    valid = pd.to_numeric(out[p_col], errors="coerce").notna()
    out["fdr"] = np.nan
    if valid.any():
        out.loc[valid, "fdr"] = multipletests(out.loc[valid, p_col].astype(float), method="fdr_bh")[1]
    return out


def log2_values(df: pd.DataFrame, gene: str, cols: list[str]) -> np.ndarray:
    if gene not in df.index:
        return np.array([], dtype=float)
    return np.log2(pd.to_numeric(df.loc[gene, cols], errors="coerce").to_numpy(dtype=float) + 1.0)


def log2_mean(df: pd.DataFrame, gene: str, cols: list[str]) -> float:
    vals = log2_values(df, gene, cols)
    return float(np.nanmean(vals)) if vals.size else np.nan


def contrast_row(
    df: pd.DataFrame,
    gene: str,
    contrast: str,
    case_cols: list[str],
    control_cols: list[str],
    p_value: bool = True,
) -> dict[str, object]:
    case = log2_values(df, gene, case_cols)
    control = log2_values(df, gene, control_cols)
    case = case[np.isfinite(case)]
    control = control[np.isfinite(control)]
    if p_value and case.size >= 2 and control.size >= 2:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)
            t_stat, p = stats.ttest_ind(case, control, equal_var=False, nan_policy="omit")
    else:
        t_stat, p = np.nan, np.nan
    return {
        "gene": gene,
        "contrast": contrast,
        "n_case": int(case.size),
        "n_control": int(control.size),
        "mean_case_log2": float(np.nanmean(case)) if case.size else np.nan,
        "mean_control_log2": float(np.nanmean(control)) if control.size else np.nan,
        "log2fc": float(np.nanmean(case) - np.nanmean(control)) if case.size and control.size else np.nan,
        "welch_t": float(t_stat) if pd.notna(t_stat) else np.nan,
        "p": float(p) if pd.notna(p) else np.nan,
    }


def read_mouse_rna() -> pd.DataFrame:
    path = RAW / "GSE162464_Normalized_Gene_Counts_Matrix.txt.gz"
    df = pd.read_csv(path, sep="\t")
    numeric = [c for c in df.columns if c not in {"Ensemble_Number", "Symbol"}]
    df[numeric] = df[numeric].apply(pd.to_numeric, errors="coerce")
    # Target genes are unique here; grouping is defensive for alias/annotation duplicates.
    return df.groupby("Symbol", dropna=True)[numeric].sum(min_count=1)


def mouse_rna_contrasts() -> tuple[pd.DataFrame, pd.DataFrame]:
    df = read_mouse_rna()
    groups = {
        "NTC_US": ["Sample1_NTC_US", "Sample2_NTC_US", "Sample3_NTC_US"],
        "NTC_IFNg": ["Sample4_NTC_IFNg", "Sample5_NTC_IFNg", "Sample6_NTC_IFNg"],
        "Gsk3b_US": ["Sample7_Gsk3b_US", "Sample8_Gsk3b_US", "Sample9_Gsk3b_US"],
        "Gsk3b_IFNg": ["Sample10_Gsk3b_IFNg", "Sample11_Gsk3b_IFNg", "Sample12_Gsk3b_IFNg"],
        "Med16_US": ["Sample13_Med16_US", "Sample14_Med16_US", "Sample15_Med16_US"],
        "Med16_IFNg": ["Sample_16_Med16_IFNg", "Sample17_Med16_IFNg", "Sample18_Med16_IFNg"],
    }
    wanted = sorted({gene for genes in MOUSE_MODULES.values() for gene in genes} | {"Gsk3b", "Med16", "Il6", "Tnf"})
    genes = [gene for gene in wanted if gene in df.index]
    contrasts = [
        ("NTC_IFNg_vs_NTC_US", groups["NTC_IFNg"], groups["NTC_US"], True),
        ("Gsk3b_IFNg_vs_NTC_IFNg", groups["Gsk3b_IFNg"], groups["NTC_IFNg"], True),
        ("Gsk3b_US_vs_NTC_US", groups["Gsk3b_US"], groups["NTC_US"], True),
        ("Med16_IFNg_vs_NTC_IFNg", groups["Med16_IFNg"], groups["NTC_IFNg"], True),
        ("Med16_US_vs_NTC_US", groups["Med16_US"], groups["NTC_US"], True),
    ]
    rows = []
    for gene in genes:
        for contrast, case_cols, control_cols, p_value in contrasts:
            rows.append(contrast_row(df, gene, contrast, case_cols, control_cols, p_value=p_value))
        gsk_interaction = (
            log2_mean(df, gene, groups["Gsk3b_IFNg"])
            - log2_mean(df, gene, groups["Gsk3b_US"])
            - (log2_mean(df, gene, groups["NTC_IFNg"]) - log2_mean(df, gene, groups["NTC_US"]))
        )
        med_interaction = (
            log2_mean(df, gene, groups["Med16_IFNg"])
            - log2_mean(df, gene, groups["Med16_US"])
            - (log2_mean(df, gene, groups["NTC_IFNg"]) - log2_mean(df, gene, groups["NTC_US"]))
        )
        rows.extend(
            [
                {
                    "gene": gene,
                    "contrast": "Gsk3b_IFNg_induction_interaction",
                    "n_case": 3,
                    "n_control": 3,
                    "mean_case_log2": np.nan,
                    "mean_control_log2": np.nan,
                    "log2fc": float(gsk_interaction) if np.isfinite(gsk_interaction) else np.nan,
                    "welch_t": np.nan,
                    "p": np.nan,
                },
                {
                    "gene": gene,
                    "contrast": "Med16_IFNg_induction_interaction",
                    "n_case": 3,
                    "n_control": 3,
                    "mean_case_log2": np.nan,
                    "mean_control_log2": np.nan,
                    "log2fc": float(med_interaction) if np.isfinite(med_interaction) else np.nan,
                    "welch_t": np.nan,
                    "p": np.nan,
                },
            ]
        )
    gene_contrasts = adjust_fdr(pd.DataFrame(rows))

    module_rows = []
    for contrast, sub in gene_contrasts.groupby("contrast", observed=True):
        for module, module_genes in MOUSE_MODULES.items():
            vals = sub[sub["gene"].isin(module_genes)].dropna(subset=["log2fc"]).copy()
            module_rows.append(
                {
                    "dataset": "GSE162464",
                    "organism": "Mus musculus",
                    "contrast": contrast,
                    "module": module,
                    "n_genes": int(vals["gene"].nunique()),
                    "genes_present": ",".join(sorted(vals["gene"].unique())),
                    "mean_log2fc": float(vals["log2fc"].mean()) if not vals.empty else np.nan,
                    "median_log2fc": float(vals["log2fc"].median()) if not vals.empty else np.nan,
                    "negative_fraction": float((vals["log2fc"] < 0).mean()) if not vals.empty else np.nan,
                    "sig_negative_fdr10": int(((vals["log2fc"] < 0) & (vals["fdr"] <= 0.10)).sum())
                    if "fdr" in vals
                    else 0,
                    "sig_positive_fdr10": int(((vals["log2fc"] > 0) & (vals["fdr"] <= 0.10)).sum())
                    if "fdr" in vals
                    else 0,
                }
            )
    return gene_contrasts.sort_values(["contrast", "gene"]), pd.DataFrame(module_rows)


def screen_summary() -> tuple[pd.DataFrame, pd.DataFrame]:
    path = RAW / "GSE162463_sgRNA_CountsNormalized.txt.gz"
    df = pd.read_csv(path, sep="\t")
    gates = {
        "MHCII": (["MHC_pos1", "MHC_pos2"], ["MHC_neg1", "MHC_neg2"]),
        "CD40": (["CD40_pos1", "CD40_pos2"], ["CD40_neg1", "CD40_neg2"]),
        "PDL1": (["PDL1_pos1", "PDL1_pos2"], ["PDL1_neg1", "PDL1_neg2"]),
    }
    for gate, (high_cols, low_cols) in gates.items():
        high = df[high_cols].apply(pd.to_numeric, errors="coerce").mean(axis=1)
        low = df[low_cols].apply(pd.to_numeric, errors="coerce").mean(axis=1)
        df[f"{gate}_low_vs_high_log2"] = np.log2((low + 1.0) / (high + 1.0))

    rows = []
    for gene, sub in df.groupby("Gene", dropna=True):
        row: dict[str, object] = {"gene": gene, "n_sgrna": int(sub["sgRNA"].nunique())}
        for gate in gates:
            vals = pd.to_numeric(sub[f"{gate}_low_vs_high_log2"], errors="coerce").dropna().to_numpy(dtype=float)
            if vals.size >= 2:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", RuntimeWarning)
                    t_stat, p = stats.ttest_1samp(vals, 0.0, nan_policy="omit")
            else:
                t_stat, p = np.nan, np.nan
            row.update(
                {
                    f"{gate}_mean_low_vs_high_log2": float(np.nanmean(vals)) if vals.size else np.nan,
                    f"{gate}_median_low_vs_high_log2": float(np.nanmedian(vals)) if vals.size else np.nan,
                    f"{gate}_positive_sgrna_fraction": float((vals > 0).mean()) if vals.size else np.nan,
                    f"{gate}_one_sample_t": float(t_stat) if pd.notna(t_stat) else np.nan,
                    f"{gate}_p": float(p) if pd.notna(p) else np.nan,
                }
            )
        rows.append(row)
    gene_summary = pd.DataFrame(rows)

    valid = gene_summary["n_sgrna"] >= 3
    for gate in gates:
        rank_col = f"{gate}_rank_required_low_vs_high"
        gene_summary[rank_col] = np.nan
        gene_summary.loc[valid, rank_col] = gene_summary.loc[valid, f"{gate}_median_low_vs_high_log2"].rank(
            ascending=False, method="min"
        )
        p_col = f"{gate}_p"
        fdr_col = f"{gate}_fdr"
        gene_summary[fdr_col] = np.nan
        p_valid = valid & pd.to_numeric(gene_summary[p_col], errors="coerce").notna()
        if p_valid.any():
            gene_summary.loc[p_valid, fdr_col] = multipletests(
                gene_summary.loc[p_valid, p_col].astype(float), method="fdr_bh"
            )[1]

    gene_summary = gene_summary.sort_values("MHCII_median_low_vs_high_log2", ascending=False)
    target_summary = gene_summary[gene_summary["gene"].isin(SCREEN_TARGET_GENES)].copy()
    target_summary = target_summary.sort_values("MHCII_rank_required_low_vs_high", na_position="last")
    return gene_summary, target_summary


def read_human_cpm() -> pd.DataFrame:
    path = RAW / "GSE294918_IFNyRNAseq_CPM.csv.gz"
    df = pd.read_csv(path, index_col=0)
    df = df.apply(pd.to_numeric, errors="coerce")
    return df.groupby(df.index).sum(min_count=1)


def human_gene_and_module_contrasts() -> tuple[pd.DataFrame, pd.DataFrame]:
    df = read_human_cpm()
    wanted = sorted({gene for genes in HUMAN_MODULES.values() for gene in genes})
    genes = [gene for gene in wanted if gene in df.index]
    rows = []

    def value(gene: str, col: str) -> float:
        return float(np.log2(df.loc[gene, col] + 1.0)) if gene in df.index and col in df.columns else np.nan

    scalar_contrasts = [
        ("D0_IFNy_8H_vs_D0_unstim", "D0_IFNy_8H", "D0_unstim"),
        ("D4_IFNy_memory_vs_D4_PBS_LPS0H", "D4_IFNy_LPS0H", "D4_PBS_LPS0H"),
        ("D4_IFNy_rux_vs_D4_IFNy_LPS0H", "D4_IFNy_rux_LPS0H", "D4_IFNy_LPS0H"),
    ]
    for gene in genes:
        for contrast, case_col, control_col in scalar_contrasts:
            rows.append(
                {
                    "gene": gene,
                    "contrast": contrast,
                    "timepoint": contrast.rsplit("_", 1)[-1],
                    "case": case_col,
                    "control": control_col,
                    "log2fc": value(gene, case_col) - value(gene, control_col),
                    "note": "single CPM column per condition; descriptive only",
                }
            )
        for hour in ["0H", "1H", "3H", "6H"]:
            case_col = f"D4_IFNy_rux_LPS{hour}"
            control_col = f"D4_IFNy_LPS{hour}"
            rows.append(
                {
                    "gene": gene,
                    "contrast": "D4_IFNy_rux_vs_D4_IFNy_matched_LPS",
                    "timepoint": hour,
                    "case": case_col,
                    "control": control_col,
                    "log2fc": value(gene, case_col) - value(gene, control_col),
                    "note": "single CPM column per condition; descriptive only",
                }
            )
            rows.append(
                {
                    "gene": gene,
                    "contrast": "D4_IFNy_memory_vs_D4_PBS_matched_LPS",
                    "timepoint": hour,
                    "case": f"D4_IFNy_LPS{hour}",
                    "control": f"D4_PBS_LPS{hour}",
                    "log2fc": value(gene, f"D4_IFNy_LPS{hour}") - value(gene, f"D4_PBS_LPS{hour}"),
                    "note": "single CPM column per condition; descriptive only",
                }
            )
    gene_contrasts = pd.DataFrame(rows)

    module_rows = []
    for (contrast, timepoint), sub in gene_contrasts.groupby(["contrast", "timepoint"], observed=True):
        for module, module_genes in HUMAN_MODULES.items():
            vals = sub[sub["gene"].isin(module_genes)].dropna(subset=["log2fc"])
            module_rows.append(
                {
                    "dataset": "GSE294918",
                    "organism": "Homo sapiens",
                    "contrast": contrast,
                    "timepoint": timepoint,
                    "module": module,
                    "n_genes": int(vals["gene"].nunique()),
                    "genes_present": ",".join(sorted(vals["gene"].unique())),
                    "mean_log2fc": float(vals["log2fc"].mean()) if not vals.empty else np.nan,
                    "median_log2fc": float(vals["log2fc"].median()) if not vals.empty else np.nan,
                    "negative_fraction": float((vals["log2fc"] < 0).mean()) if not vals.empty else np.nan,
                    "note": "single CPM column per condition; descriptive only",
                }
            )
    return gene_contrasts.sort_values(["contrast", "timepoint", "gene"]), pd.DataFrame(module_rows)


def get_value(df: pd.DataFrame, **filters: object) -> float:
    mask = pd.Series(True, index=df.index)
    for col, val in filters.items():
        mask &= df[col].eq(val)
    sub = df.loc[mask]
    if sub.empty:
        return np.nan
    return float(sub.iloc[0]["mean_log2fc"])


def build_verdict(
    screen_targets: pd.DataFrame,
    mouse_modules: pd.DataFrame,
    mouse_genes: pd.DataFrame,
    human_modules: pd.DataFrame,
) -> dict[str, object]:
    gsk3b_screen = screen_targets[screen_targets["gene"].eq("Gsk3b")].iloc[0].to_dict()
    gsk_mhc = get_value(
        mouse_modules,
        dataset="GSE162464",
        contrast="Gsk3b_IFNg_vs_NTC_IFNg",
        module="ciita_mhc2_cd74",
    )
    gsk_ifn = get_value(
        mouse_modules,
        dataset="GSE162464",
        contrast="Gsk3b_IFNg_vs_NTC_IFNg",
        module="generic_ifn_core",
    )
    gsk_surface = get_value(
        mouse_modules,
        dataset="GSE162464",
        contrast="Gsk3b_IFNg_vs_NTC_IFNg",
        module="mhc2_surface_core",
    )
    rux_hla = get_value(
        human_modules,
        dataset="GSE294918",
        contrast="D4_IFNy_rux_vs_D4_IFNy_matched_LPS",
        timepoint="0H",
        module="ciita_hla2_cd74",
    )
    rux_ifn = get_value(
        human_modules,
        dataset="GSE294918",
        contrast="D4_IFNy_rux_vs_D4_IFNy_matched_LPS",
        timepoint="0H",
        module="generic_ifn_core",
    )
    gene_lookup = mouse_genes.set_index(["gene", "contrast"])["log2fc"]
    ciita_gsk = float(gene_lookup.get(("Ciita", "Gsk3b_IFNg_vs_NTC_IFNg"), np.nan))
    cd74_gsk = float(gene_lookup.get(("Cd74", "Gsk3b_IFNg_vs_NTC_IFNg"), np.nan))
    stat1_gsk = float(gene_lookup.get(("Stat1", "Gsk3b_IFNg_vs_NTC_IFNg"), np.nan))
    irf1_gsk = float(gene_lookup.get(("Irf1", "Gsk3b_IFNg_vs_NTC_IFNg"), np.nan))

    selectivity_ratio = abs(gsk_mhc) / abs(gsk_ifn) if np.isfinite(gsk_mhc) and np.isfinite(gsk_ifn) and gsk_ifn != 0 else np.nan
    verdict = (
        "supports_GSK3B_as_testable_CIITA_MHCII_controller_not_final_therapeutic_claim"
        if gsk_mhc < -1.0 and gsk_ifn > -1.0 and gsk3b_screen["MHCII_rank_required_low_vs_high"] <= 100
        else "mixed_or_null_for_selective_GSK3B_controller"
    )
    caveat = (
        "GSK3B KO preferentially reduces CIITA/MHC-II/CD74 versus the averaged generic IFN module, "
        "but it is not IFN-neutral: CXCL10 and some inflammatory genes also drop. Ruxolitinib remains "
        "the broad IFN/JAK positive-control pattern, not the desired selectivity profile."
    )
    return {
        "verdict": verdict,
        "interpretation": caveat,
        "gse162463_gsk3b_mhcii_low_vs_high_median_log2": gsk3b_screen["MHCII_median_low_vs_high_log2"],
        "gse162463_gsk3b_mhcii_required_rank": gsk3b_screen["MHCII_rank_required_low_vs_high"],
        "gse162464_gsk3b_ciita_mhc2_cd74_mean_log2fc": gsk_mhc,
        "gse162464_gsk3b_mhc2_surface_core_mean_log2fc": gsk_surface,
        "gse162464_gsk3b_generic_ifn_core_mean_log2fc": gsk_ifn,
        "gse162464_selectivity_ratio_abs_mhc_over_ifn": selectivity_ratio,
        "gse162464_gsk3b_ciita_log2fc": ciita_gsk,
        "gse162464_gsk3b_cd74_log2fc": cd74_gsk,
        "gse162464_gsk3b_stat1_log2fc": stat1_gsk,
        "gse162464_gsk3b_irf1_log2fc": irf1_gsk,
        "gse294918_rux_ciita_hla2_cd74_lps0_mean_log2fc": rux_hla,
        "gse294918_rux_generic_ifn_core_lps0_mean_log2fc": rux_ifn,
    }


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = prepare_inputs()
    manifest.to_csv(OUT / "download_manifest.tsv", sep="\t", index=False)

    screen_all, screen_targets = screen_summary()
    screen_all.to_csv(OUT / "gse162463_screen_gene_summary.tsv", sep="\t", index=False)
    screen_targets.to_csv(OUT / "gse162463_target_gene_summary.tsv", sep="\t", index=False)

    mouse_genes, mouse_modules = mouse_rna_contrasts()
    mouse_genes.to_csv(OUT / "gse162464_mouse_rna_gene_contrasts.tsv", sep="\t", index=False)
    mouse_modules.to_csv(OUT / "gse162464_mouse_rna_module_summary.tsv", sep="\t", index=False)

    human_genes, human_modules = human_gene_and_module_contrasts()
    human_genes.to_csv(OUT / "gse294918_human_rux_gene_contrasts.tsv", sep="\t", index=False)
    human_modules.to_csv(OUT / "gse294918_human_rux_module_summary.tsv", sep="\t", index=False)

    verdict = build_verdict(screen_targets, mouse_modules, mouse_genes, human_modules)
    summary = {
        "seed": SEED,
        "inputs": manifest.to_dict(orient="records"),
        "outputs": [
            "download_manifest.tsv",
            "gse162463_screen_gene_summary.tsv",
            "gse162463_target_gene_summary.tsv",
            "gse162464_mouse_rna_gene_contrasts.tsv",
            "gse162464_mouse_rna_module_summary.tsv",
            "gse294918_human_rux_gene_contrasts.tsv",
            "gse294918_human_rux_module_summary.tsv",
            "wave14_verdict.json",
            "wave14_summary.json",
        ],
        "verdict": verdict,
    }
    write_json(OUT / "wave14_verdict.json", verdict)
    write_json(OUT / "wave14_summary.json", summary)
    print(json.dumps(verdict, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
