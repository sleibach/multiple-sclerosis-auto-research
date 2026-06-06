#!/usr/bin/env python3
"""Wave23 treatment-response stratification scout.

This consolidates local Wave18 treatment-response outputs and adds lightweight
public GEO matrix analyses where processed data and response labels are
available. The purpose is not discovery; it is a guardrailed scout for whether
the shared lipid-lysosomal/APC module is more useful as a baseline
stratification biomarker than as a therapeutic target.

Outputs are written under:
phases/v3/results/wave23_treatment_response_stratification/
"""

from __future__ import annotations

import csv
import gzip
import io
import json
import math
import re
import urllib.request
from collections import defaultdict
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.metrics import roc_auc_score
from statsmodels.formula.api import ols
from statsmodels.stats.multitest import multipletests

from v3_analyze_direct_h5ad_cell_states import MODULES, ROOT

SEED = 20260527
OUT = ROOT / "phases/v3/results" / "wave23_treatment_response_stratification"

GENERIC_MODULES = ["inflammatory_nfkb", "ifn_apc"]
SHARED_MODULES = [
    "ifn_apc",
    "hla_ii_apc",
    "lysosomal_apc",
    "mif_cd74_receptor_state",
    "mixscale_validated_ifng_readout",
    "lipid_loader_repair",
    "complement_phagocytosis",
    "hif_nampt_metabolic",
    "inflammatory_nfkb",
]
TARGET_GENES = sorted({gene for module in SHARED_MODULES for gene in MODULES[module]})

GEO_URLS = {
    "GSE73661_matrix": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE73nnn/GSE73661/matrix/GSE73661_series_matrix.txt.gz",
    "GSE106992_matrix": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE106nnn/GSE106992/matrix/GSE106992_series_matrix.txt.gz",
    "GSE24742_matrix": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE24nnn/GSE24742/matrix/GSE24742_series_matrix.txt.gz",
    "GPL570_annot": "https://ftp.ncbi.nlm.nih.gov/geo/platforms/GPLnnn/GPL570/annot/GPL570.annot.gz",
    "GPL6244_annot": "https://ftp.ncbi.nlm.nih.gov/geo/platforms/GPL6nnn/GPL6244/annot/GPL6244.annot.gz",
    "GSE250453_counts": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE250nnn/GSE250453/suppl/GSE250453_fingo_RNAseq_all.tsv.gz",
    "GSE235357_norm": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE235nnn/GSE235357/suppl/GSE235357_normalized_annotated.csv.gz",
}


def download_bytes(url: str, timeout: int = 180) -> bytes:
    with urllib.request.urlopen(url, timeout=timeout) as handle:
        return handle.read()


def read_remote_gzip_text(url: str) -> str:
    return gzip.decompress(download_bytes(url)).decode("utf-8", errors="replace")


def split_geo_values(line: str) -> list[str]:
    return [part.strip().strip('"') for part in line.rstrip("\n").split("\t")[1:]]


def parse_geo_series_matrix(url: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return sample metadata and expression matrix from a GEO series matrix."""
    text = read_remote_gzip_text(url)
    metadata_rows: list[dict[str, str]] = []
    table_lines: list[str] = []
    in_table = False

    for line in text.splitlines():
        if line.startswith("!series_matrix_table_begin"):
            in_table = True
            continue
        if line.startswith("!series_matrix_table_end"):
            break
        if in_table:
            table_lines.append(line)
            continue
        if line.startswith("!Sample_"):
            parts = line.rstrip("\n").split("\t")
            key = parts[0][1:]
            values = [part.strip().strip('"') for part in parts[1:]]
            if not metadata_rows:
                metadata_rows = [{} for _ in values]
            for idx, value in enumerate(values):
                if key == "Sample_characteristics_ch1" and ": " in value:
                    sub_key, sub_value = value.split(": ", 1)
                    metadata_rows[idx][sub_key.lower()] = sub_value
                else:
                    metadata_rows[idx][key] = value

    if not table_lines:
        raise ValueError(f"no series matrix table found at {url}")
    expr = pd.read_csv(io.StringIO("\n".join(table_lines)), sep="\t", index_col=0)
    expr.index = expr.index.astype(str).str.strip('"')
    expr.columns = expr.columns.astype(str).str.strip('"')
    meta = pd.DataFrame(metadata_rows)
    return meta, expr.apply(pd.to_numeric, errors="coerce")


def parse_geo_annotation(url: str, target_genes: set[str]) -> pd.DataFrame:
    text = read_remote_gzip_text(url)
    header: list[str] | None = None
    rows: list[dict[str, str]] = []
    for line in text.splitlines():
        if not line or line.startswith(("^", "!", "#")):
            continue
        parts = line.rstrip("\n").split("\t")
        if header is None:
            if parts[0] == "ID":
                header = parts
            continue
        if len(parts) < len(header):
            parts.extend([""] * (len(header) - len(parts)))
        record = dict(zip(header, parts, strict=False))
        symbols = split_symbols(record.get("Gene symbol", ""))
        for symbol in symbols:
            if symbol in target_genes:
                rows.append({"probe_id": record["ID"], "gene_symbol": symbol})
    return pd.DataFrame(rows).drop_duplicates()


def split_symbols(value: str) -> list[str]:
    if not isinstance(value, str) or not value.strip():
        return []
    value = value.replace('"', "")
    pieces = re.split(r"\s*///\s*|\s*//\s*|\s*;\s*|,\s*", value)
    return sorted({piece.strip() for piece in pieces if piece.strip()})


def collapse_probes_to_genes(expr: pd.DataFrame, annot: pd.DataFrame) -> pd.DataFrame:
    if annot.empty:
        return pd.DataFrame(index=expr.columns)
    present = annot[annot["probe_id"].isin(expr.index)].copy()
    rows = []
    for gene, sub in present.groupby("gene_symbol", observed=True):
        rows.append(pd.Series(expr.loc[sub["probe_id"].unique()].mean(axis=0), name=gene))
    if not rows:
        return pd.DataFrame(index=expr.columns)
    return pd.DataFrame(rows).T


def ensembl_symbol_map() -> dict[str, str]:
    path = ROOT / "phases/v3/results" / "wave18_treatment_response" / "wave18_gse138746_ra_gene_map.tsv"
    if not path.exists():
        return {}
    df = pd.read_csv(path, sep="\t")
    df = df[df["ensembl_gene_id"].notna() & df["ensembl_gene_id"].ne("")]
    return {str(row.ensembl_gene_id).split(".")[0]: row.gene_symbol for row in df.itertuples()}


def log_cpm(counts: pd.DataFrame) -> pd.DataFrame:
    lib = counts.sum(axis=0).replace(0, np.nan)
    return np.log1p(counts.divide(lib, axis=1) * 1e6).T


def log1p_transpose(values: pd.DataFrame) -> pd.DataFrame:
    return np.log1p(values.clip(lower=0)).T


def module_scores(
    sample_gene: pd.DataFrame,
    metadata: pd.DataFrame,
    reference_mask: pd.Series | np.ndarray | None = None,
) -> pd.DataFrame:
    if reference_mask is None:
        reference_values = np.ones(len(sample_gene), dtype=bool)
    elif isinstance(reference_mask, pd.Series):
        if reference_mask.index.equals(sample_gene.index):
            reference_values = reference_mask.reindex(sample_gene.index).fillna(False).to_numpy(bool)
        elif len(reference_mask) == len(sample_gene):
            reference_values = reference_mask.to_numpy(bool)
        else:
            raise ValueError("reference_mask Series must align by sample index or by row order")
    else:
        reference_values = np.asarray(reference_mask, dtype=bool)
        if len(reference_values) != len(sample_gene):
            raise ValueError("reference_mask length must match sample_gene rows")
    rows = []
    for module in SHARED_MODULES:
        genes = [gene for gene in MODULES[module] if gene in sample_gene.columns]
        if not genes:
            continue
        ref = sample_gene.loc[reference_values, genes]
        if ref.empty:
            continue
        mean = ref.mean(axis=0)
        sd = ref.std(axis=0, ddof=1).replace(0, np.nan).fillna(1.0)
        scores = ((sample_gene[genes] - mean) / sd).mean(axis=1)
        row = metadata.copy()
        row["module"] = module
        row["n_genes_present"] = len(genes)
        row["genes_present"] = ",".join(genes)
        row["score"] = scores.to_numpy(float)
        rows.append(row)
    return pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()


def hedges_g(a: Iterable[float], b: Iterable[float]) -> float:
    a = np.asarray(list(a), dtype=float)
    b = np.asarray(list(b), dtype=float)
    a = a[np.isfinite(a)]
    b = b[np.isfinite(b)]
    if len(a) < 2 or len(b) < 2:
        return np.nan
    pooled = ((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) / (len(a) + len(b) - 2)
    if pooled <= 0 or not np.isfinite(pooled):
        return np.nan
    correction = 1.0 - 3.0 / (4.0 * (len(a) + len(b)) - 9.0)
    return float(((a.mean() - b.mean()) / math.sqrt(pooled)) * correction)


def auc_safe(labels: Iterable[int], scores: Iterable[float]) -> float:
    labels = np.asarray(list(labels), dtype=int)
    scores = np.asarray(list(scores), dtype=float)
    mask = np.isfinite(scores)
    if mask.sum() < 4 or len(set(labels[mask])) < 2:
        return np.nan
    return float(roc_auc_score(labels[mask], scores[mask]))


def ttest_safe(a: Iterable[float], b: Iterable[float]) -> tuple[float, float]:
    a = np.asarray(list(a), dtype=float)
    b = np.asarray(list(b), dtype=float)
    a = a[np.isfinite(a)]
    b = b[np.isfinite(b)]
    if len(a) < 2 or len(b) < 2:
        return np.nan, np.nan
    stat, p_value = stats.ttest_ind(a, b, equal_var=False, nan_policy="omit")
    return float(stat), float(p_value)


def one_sample_ttest(values: Iterable[float]) -> tuple[float, float]:
    values = np.asarray(list(values), dtype=float)
    values = values[np.isfinite(values)]
    if len(values) < 2:
        return np.nan, np.nan
    stat, p_value = stats.ttest_1samp(values, 0.0, nan_policy="omit")
    return float(stat), float(p_value)


def fdr_column(df: pd.DataFrame, group_cols: list[str] | None = None) -> pd.DataFrame:
    if df.empty:
        return df
    df = df.copy()
    df["fdr"] = np.nan
    if group_cols:
        for _, idx in df.groupby(group_cols, observed=True).groups.items():
            p = df.loc[idx, "p"].fillna(1.0).to_numpy(float)
            df.loc[idx, "fdr"] = multipletests(p, method="fdr_bh")[1]
    else:
        df["fdr"] = multipletests(df["p"].fillna(1.0), method="fdr_bh")[1]
    return df


def wide_scores(scores: pd.DataFrame, index_cols: list[str]) -> pd.DataFrame:
    return (
        scores.pivot_table(index=index_cols, columns="module", values="score", aggfunc="mean")
        .reset_index()
        .rename_axis(None, axis=1)
    )


def residualized_response_test(
    wide: pd.DataFrame,
    module: str,
    responder_col: str,
    covariates: list[str],
) -> dict[str, float | str]:
    usable_covs = [cov for cov in covariates if cov in wide.columns and cov != module]
    if module not in wide.columns or not usable_covs:
        return {
            "generic_adjusted_delta": np.nan,
            "generic_adjusted_p": np.nan,
            "generic_adjusted_hedges_g": np.nan,
            "generic_adjustment_covariates": "",
            "module_generic_max_abs_r": np.nan,
        }
    cols = [module, responder_col] + usable_covs
    df = wide[cols].dropna().copy()
    if df[responder_col].nunique() < 2 or len(df) < 6:
        return {
            "generic_adjusted_delta": np.nan,
            "generic_adjusted_p": np.nan,
            "generic_adjusted_hedges_g": np.nan,
            "generic_adjustment_covariates": ",".join(usable_covs),
            "module_generic_max_abs_r": np.nan,
        }
    max_abs_r = np.nan
    corrs = []
    for cov in usable_covs:
        if df[module].std(ddof=1) > 0 and df[cov].std(ddof=1) > 0:
            corrs.append(abs(float(df[[module, cov]].corr().iloc[0, 1])))
    if corrs:
        max_abs_r = max(corrs)
    formula = f"Q('{module}') ~ " + " + ".join(f"Q('{cov}')" for cov in usable_covs)
    try:
        fit = ols(formula, data=df).fit()
        residual = fit.resid
    except Exception:  # noqa: BLE001
        residual = df[module] - df[module].mean()
    yes = residual[df[responder_col].astype(bool).to_numpy()]
    no = residual[~df[responder_col].astype(bool).to_numpy()]
    _, p_value = ttest_safe(yes, no)
    return {
        "generic_adjusted_delta": float(np.nanmean(yes) - np.nanmean(no)) if len(yes) and len(no) else np.nan,
        "generic_adjusted_p": p_value,
        "generic_adjusted_hedges_g": hedges_g(yes, no),
        "generic_adjustment_covariates": ",".join(usable_covs),
        "module_generic_max_abs_r": max_abs_r,
    }


def compare_baseline(
    scores: pd.DataFrame,
    index_cols: list[str],
    group_cols: list[str],
    responder_col: str,
    dataset: str,
    therapy_class: str,
    therapy: str,
    disease: str,
    tissue: str,
    design: str,
    confounders: str,
) -> pd.DataFrame:
    if scores.empty:
        return pd.DataFrame()
    wide = wide_scores(scores, index_cols)
    rows = []
    for keys, sub in wide.groupby(group_cols, observed=True):
        key_dict = dict(zip(group_cols, keys if isinstance(keys, tuple) else (keys,), strict=True))
        if sub[responder_col].nunique() < 2:
            continue
        for module in SHARED_MODULES:
            if module not in sub.columns:
                continue
            yes = sub.loc[sub[responder_col].astype(bool), module]
            no = sub.loc[~sub[responder_col].astype(bool), module]
            if len(yes.dropna()) < 2 or len(no.dropna()) < 2:
                continue
            t_stat, p_value = ttest_safe(yes, no)
            row = {
                "dataset": dataset,
                "therapy_class": key_dict.get("therapy_class", therapy_class),
                "therapy": key_dict.get("therapy", therapy),
                "disease": disease,
                "tissue_or_compartment": tissue,
                "design": design,
                "analysis_scope": ";".join(f"{k}={v}" for k, v in key_dict.items()),
                "module": module,
                "n_responder": int(yes.notna().sum()),
                "n_nonresponder": int(no.notna().sum()),
                "mean_responder": float(np.nanmean(yes)),
                "mean_nonresponder": float(np.nanmean(no)),
                "delta_responder_minus_nonresponder": float(np.nanmean(yes) - np.nanmean(no)),
                "hedges_g": hedges_g(yes, no),
                "welch_t": t_stat,
                "p": p_value,
                "auc_responder_high": auc_safe(sub[responder_col].astype(int), sub[module]),
                "confounders": confounders,
            }
            row.update(residualized_response_test(sub, module, responder_col, GENERIC_MODULES))
            rows.append(row)
    out = pd.DataFrame(rows)
    return fdr_column(out, ["dataset", "analysis_scope"]) if not out.empty else out


def compare_prepost(
    scores: pd.DataFrame,
    patient_col: str,
    time_col: str,
    baseline_value: str,
    post_order_col: str,
    group_cols: list[str],
    dataset: str,
    therapy_class: str,
    therapy: str,
    disease: str,
    tissue: str,
    design: str,
    confounders: str,
) -> pd.DataFrame:
    if scores.empty:
        return pd.DataFrame()
    wide = wide_scores(scores, [patient_col, time_col, post_order_col] + group_cols)
    rows = []
    for keys, sub in wide.groupby(group_cols, observed=True):
        key_dict = dict(zip(group_cols, keys if isinstance(keys, tuple) else (keys,), strict=True))
        base = sub[sub[time_col].eq(baseline_value)].drop_duplicates(patient_col).set_index(patient_col)
        post = (
            sub[~sub[time_col].eq(baseline_value)]
            .sort_values(post_order_col)
            .drop_duplicates(patient_col)
            .set_index(patient_col)
        )
        common = sorted(set(base.index) & set(post.index))
        if len(common) < 2:
            continue
        for module in SHARED_MODULES:
            if module not in sub.columns:
                continue
            delta = post.loc[common, module].to_numpy(float) - base.loc[common, module].to_numpy(float)
            t_stat, p_value = one_sample_ttest(delta)
            rows.append(
                {
                    "dataset": dataset,
                    "therapy_class": key_dict.get("therapy_class", therapy_class),
                    "therapy": key_dict.get("therapy", therapy),
                    "disease": disease,
                    "tissue_or_compartment": tissue,
                    "design": design,
                    "analysis_scope": ";".join(f"{k}={v}" for k, v in key_dict.items()),
                    "module": module,
                    "n_pairs": int(np.isfinite(delta).sum()),
                    "mean_post_minus_pre": float(np.nanmean(delta)),
                    "median_post_minus_pre": float(np.nanmedian(delta)),
                    "one_sample_t": t_stat,
                    "p": p_value,
                    "confounders": confounders,
                }
            )
    out = pd.DataFrame(rows)
    return fdr_column(out, ["dataset", "analysis_scope"]) if not out.empty else out


def analyze_local_wave18() -> tuple[pd.DataFrame, pd.DataFrame, list[dict[str, object]]]:
    baseline_tables = []
    pd_tables = []
    inventory: list[dict[str, object]] = []

    ra_path = ROOT / "phases/v3/results" / "wave18_treatment_response" / "wave18_gse138746_ra_sample_module_scores.tsv"
    if ra_path.exists():
        ra = pd.read_csv(ra_path, sep="\t")
        index_cols = ["patient", "sample", "compartment", "drug", "response_code", "eular_responder", "good_responder"]
        for endpoint, responder_col, label in [
            ("eular_moderate_good_vs_none", "eular_responder", "moderate/good vs none"),
            ("eular_good_vs_none", "good_responder", "good vs none"),
        ]:
            keep = ra.copy()
            if responder_col == "good_responder":
                keep = keep[keep["response_code"].isin(["g", "n"])].copy()
            baseline_tables.append(
                compare_baseline(
                    keep,
                    index_cols,
                    ["compartment", "drug"],
                    responder_col,
                    "GSE138746",
                    "anti-TNF",
                    "adalimumab/etanercept",
                    "rheumatoid arthritis",
                    "sorted PBMC/CD14/CD4",
                    f"baseline sorted RNA-seq; {label}",
                    "drug, compartment, response-class encoding, baseline disease activity; generic inflammation tested by inflammatory_nfkb/ifn_apc residualization",
                )
            )
            pooled = keep.copy()
            pooled["drug_scope"] = "all_anti_tnf"
            baseline_tables.append(
                compare_baseline(
                    pooled,
                    index_cols + ["drug_scope"],
                    ["compartment", "drug_scope"],
                    responder_col,
                    "GSE138746",
                    "anti-TNF",
                    "adalimumab/etanercept",
                    "rheumatoid arthritis",
                    "sorted PBMC/CD14/CD4",
                    f"baseline sorted RNA-seq pooled anti-TNF; {label}",
                    "drug mix, compartment, response-class encoding, baseline disease activity; generic inflammation tested by inflammatory_nfkb/ifn_apc residualization",
                )
            )
        inventory.append(
            {
                "accession": "GSE138746",
                "therapy_class": "anti-TNF",
                "therapy": "adalimumab/etanercept",
                "status": "analyzed_local_wave18_extended",
                "response_labels": "EULAR response after 6 months; encoded in sample names",
                "modality": "sorted PBMC/CD14/CD4 bulk RNA-seq",
                "url": "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE138746",
            }
        )

    uc_path = ROOT / "phases/v3/results" / "gse253006_tofacitinib_marker" / "gse253006_marker_donor_module_scores.tsv"
    if uc_path.exists():
        uc = pd.read_csv(uc_path, sep="\t").rename(columns={"mean_score": "score"})
        baseline = uc[uc["timepoint_norm"].eq("W0")].copy()
        baseline_tables.append(
            compare_baseline(
                baseline,
                ["patient", "gsm", "marker_compartment", "responder", "timepoint_norm"],
                ["marker_compartment"],
                "responder",
                "GSE253006",
                "JAK/TYK",
                "tofacitinib",
                "ulcerative colitis",
                "marker-derived rectal single-cell compartments",
                "baseline responder vs non-responder marker-compartment scRNA score",
                "n=11 baseline, marker-derived compartments, concomitant UC severity/cell-composition; generic inflammation tested by inflammatory_nfkb/ifn_apc residualization",
            )
        )
        uc_prepost = uc.copy()
        order = {"W0": 0, "W8": 8, "W16": 16, "W24": 24, "W48": 48}
        uc_prepost["time_order"] = uc_prepost["timepoint_norm"].map(order).fillna(999)
        pd_tables.append(
            compare_prepost(
                uc_prepost,
                "patient",
                "timepoint_norm",
                "W0",
                "time_order",
                ["group", "marker_compartment"],
                "GSE253006",
                "JAK/TYK",
                "tofacitinib",
                "ulcerative colitis",
                "marker-derived rectal single-cell compartments",
                "earliest post-treatment minus baseline",
                "post-treatment only for PD; n small, marker-derived compartments, cell-composition shifts",
            )
        )
        inventory.append(
            {
                "accession": "GSE253006",
                "therapy_class": "JAK/TYK",
                "therapy": "tofacitinib",
                "status": "analyzed_local_marker_compartment",
                "response_labels": "5 responders, 6 non-responders at baseline in local Wave18/V3 parsing",
                "modality": "10x scRNA, marker-derived compartments",
                "url": "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE253006",
            }
        )

    pso_path = ROOT / "phases/v3/results" / "wave18_treatment_response" / "wave18_gse183047_psoriasis_sample_module_scores.tsv"
    if pso_path.exists():
        pso = pd.read_csv(pso_path, sep="\t").rename(columns={"mean_score": "score"})
        pso = pso[pso["group"].eq("psoriasis") & pso["lesion"].eq("LS")].copy()
        pd_tables.append(
            compare_prepost(
                pso,
                "patient",
                "timepoint",
                "preTx",
                "time_order",
                ["marker_compartment"],
                "GSE183047",
                "IL-17/IL-23",
                "secukinumab",
                "psoriasis",
                "marker-derived lesional skin single-cell compartments",
                "earliest post-secukinumab minus pretreatment",
                "no responder labels; n=4 paired for analyzable lesional compartments; marker-derived compartments",
            )
        )
        inventory.append(
            {
                "accession": "GSE183047",
                "therapy_class": "IL-17/IL-23",
                "therapy": "secukinumab",
                "status": "analyzed_local_wave18_pd_only",
                "response_labels": "none in GEO/local parsing",
                "modality": "immune-enriched scRNA, marker-derived compartments",
                "url": "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE183047",
            }
        )

    return (
        pd.concat([df for df in baseline_tables if not df.empty], ignore_index=True) if baseline_tables else pd.DataFrame(),
        pd.concat([df for df in pd_tables if not df.empty], ignore_index=True) if pd_tables else pd.DataFrame(),
        inventory,
    )


def analyze_gse250453_fingolimod() -> tuple[pd.DataFrame, pd.DataFrame, list[dict[str, object]]]:
    symbol_by_ens = ensembl_symbol_map()
    raw = pd.read_csv(io.BytesIO(download_bytes(GEO_URLS["GSE250453_counts"])), sep="\t", compression="gzip")
    raw["ensembl_base"] = raw["ensembl_gene_id"].astype(str).str.split(".").str[0]
    raw["gene_symbol"] = raw["ensembl_base"].map(symbol_by_ens)
    expr = raw[raw["gene_symbol"].isin(TARGET_GENES)].copy()
    counts = expr.set_index("gene_symbol").drop(columns=["ensembl_gene_id", "ensembl_base"], errors="ignore")
    counts = counts.groupby(level=0).sum()
    sample_gene = log_cpm(counts)
    meta_rows = []
    for sample in sample_gene.index:
        fixed = sample.replace("Res4_treat", "R_treat_4")
        match = re.match(r"^(NR|R)_(basal|treat)_(\d+)$", fixed)
        if not match:
            continue
        response, time, patient = match.groups()
        meta_rows.append(
            {
                "sample": sample,
                "patient": f"{response}_{patient}",
                "response": response,
                "responder": response == "R",
                "timepoint": "baseline" if time == "basal" else "12m",
                "time_order": 0 if time == "basal" else 12,
            }
        )
    meta = (
        pd.DataFrame(meta_rows)
        .set_index("sample")
        .loc[sample_gene.index.intersection([r["sample"] for r in meta_rows])]
        .rename_axis("sample")
        .reset_index()
    )
    sample_gene = sample_gene.loc[meta["sample"]]
    ref = meta["timepoint"].eq("baseline")
    scores = module_scores(sample_gene, meta, ref)
    baseline = scores[scores["timepoint"].eq("baseline")]
    baseline = baseline.copy()
    baseline["contrast"] = "R_vs_NR"
    base_tests = compare_baseline(
        baseline,
        ["patient", "sample", "responder", "response", "timepoint", "contrast"],
        ["contrast"],
        "responder",
        "GSE250453",
        "S1P",
        "fingolimod",
        "multiple sclerosis",
        "PBMC bulk",
        "baseline R vs NR; NEDA-3 at 2 years; public processed counts",
        "n=5/5, all-PBMC bulk composition, lymphocyte-trafficking pharmacology, no compartment resolution; generic inflammation tested by inflammatory_nfkb/ifn_apc residualization",
    )
    pd_tests = compare_prepost(
        scores,
        "patient",
        "timepoint",
        "baseline",
        "time_order",
        ["response"],
        "GSE250453",
        "S1P",
        "fingolimod",
        "multiple sclerosis",
        "PBMC bulk",
        "12m minus baseline by responder group",
        "post-treatment PBMC composition dominated by S1P lymphocyte sequestration; not a baseline stratum claim",
    )
    inv = [
        {
            "accession": "GSE250453",
            "therapy_class": "S1P",
            "therapy": "fingolimod",
            "status": "analyzed_public_processed_bulk",
            "response_labels": "5 responders and 5 non-responders; NEDA-3 at 2 years",
            "modality": "PBMC RNA-seq bulk",
            "url": "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE250453",
        }
    ]
    return base_tests, pd_tests, inv


def analyze_gse235357_dmf() -> tuple[pd.DataFrame, pd.DataFrame, list[dict[str, object]]]:
    raw = pd.read_csv(io.BytesIO(download_bytes(GEO_URLS["GSE235357_norm"])), compression="gzip")
    symbol_col = "SYMBOL"
    sample_cols = [col for col in raw.columns if col.startswith("SM002604_")]
    expr = raw[raw[symbol_col].isin(TARGET_GENES)].copy()
    values = expr.groupby(symbol_col)[sample_cols].mean()
    sample_gene = log1p_transpose(values)
    meta_rows = []
    for idx, sample in enumerate(sample_cols, start=1):
        if idx <= 10:
            meta_rows.append({"sample": sample, "patient": f"HC_{idx}", "response": "healthy", "responder": False, "timepoint": "healthy", "time_order": -1})
        elif idx <= 20:
            patient_num = (idx - 11) // 2 + 1
            is_baseline = (idx - 11) % 2 == 0
            meta_rows.append(
                {
                    "sample": sample,
                    "patient": f"R_{patient_num}",
                    "response": "R",
                    "responder": True,
                    "timepoint": "baseline" if is_baseline else "12m",
                    "time_order": 0 if is_baseline else 12,
                }
            )
        else:
            patient_num = (idx - 21) // 2 + 1
            is_baseline = (idx - 21) % 2 == 0
            meta_rows.append(
                {
                    "sample": sample,
                    "patient": f"NR_{patient_num}",
                    "response": "NR",
                    "responder": False,
                    "timepoint": "baseline" if is_baseline else "12m",
                    "time_order": 0 if is_baseline else 12,
                }
            )
    meta = pd.DataFrame(meta_rows).set_index("sample").loc[sample_gene.index].rename_axis("sample").reset_index()
    ref = meta["timepoint"].eq("baseline")
    scores = module_scores(sample_gene, meta, ref)
    scores = scores[scores["response"].isin(["R", "NR"])].copy()
    baseline = scores[scores["timepoint"].eq("baseline")]
    baseline = baseline.copy()
    baseline["contrast"] = "R_vs_NR"
    base_tests = compare_baseline(
        baseline,
        ["patient", "sample", "responder", "response", "timepoint", "contrast"],
        ["contrast"],
        "responder",
        "GSE235357",
        "fumarate",
        "dimethyl fumarate",
        "multiple sclerosis",
        "PBMC bulk",
        "baseline R vs NR; public normalized annotated matrix",
        "n=5/5, all-PBMC bulk composition, published no baseline DEGs between R/NR; generic inflammation tested by inflammatory_nfkb/ifn_apc residualization",
    )
    pd_tests = compare_prepost(
        scores,
        "patient",
        "timepoint",
        "baseline",
        "time_order",
        ["response"],
        "GSE235357",
        "fumarate",
        "dimethyl fumarate",
        "multiple sclerosis",
        "PBMC bulk",
        "12m minus baseline by responder group",
        "post-treatment PBMC composition and NF-kB pharmacology; not a baseline stratum claim",
    )
    inv = [
        {
            "accession": "GSE235357",
            "therapy_class": "fumarate",
            "therapy": "dimethyl fumarate",
            "status": "analyzed_public_processed_bulk",
            "response_labels": "5 responders and 5 non-responders",
            "modality": "PBMC RNA-seq bulk",
            "url": "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE235357",
        }
    ]
    return base_tests, pd_tests, inv


def parse_gse73661_meta(meta: pd.DataFrame) -> pd.DataFrame:
    out = meta.copy()
    out["sample"] = out["Sample_geo_accession"]
    out["patient"] = out["study individual number"].astype(str)
    out["title"] = out["Sample_title"]
    out["therapy_raw"] = out["induction therapy_maintenance therapy"].fillna("")
    out["therapy"] = np.select(
        [
            out["therapy_raw"].str.contains("IFX", case=False, na=False),
            out["therapy_raw"].str.contains("vdz", case=False, na=False),
            out["therapy_raw"].str.contains("plac", case=False, na=False),
            out["therapy_raw"].eq("CO"),
        ],
        ["infliximab", "vedolizumab", "placebo", "control"],
        default="other",
    )
    out["therapy_class"] = out["therapy"].map({"infliximab": "anti-TNF", "vedolizumab": "integrin"}).fillna("other")
    title = out["title"].fillna("")
    out["timepoint"] = np.select(
        [
            title.str.contains("W0", case=False, na=False),
            title.str.contains("W4/6", case=False, na=False),
            title.str.contains("W6", case=False, na=False),
            title.str.contains("W12", case=False, na=False),
            title.str.contains("W52", case=False, na=False),
        ],
        ["W0", "W4_6", "W6", "W12", "W52"],
        default="control",
    )
    order = {"control": -1, "W0": 0, "W4_6": 5, "W6": 6, "W12": 12, "W52": 52}
    out["time_order"] = out["timepoint"].map(order).fillna(999)
    out["post_response"] = title.str.extract(r"UC\s+(R|NR)\s+", flags=re.IGNORECASE)[0].str.upper().fillna("")
    response_map: dict[tuple[str, str], str] = {}
    for _, row in out[out["post_response"].isin(["R", "NR"])].sort_values("time_order").iterrows():
        key = (row["patient"], row["therapy"])
        response_map.setdefault(key, row["post_response"])
    out["response"] = [response_map.get((row.patient, row.therapy), row.post_response) for row in out.itertuples()]
    out["responder"] = out["response"].eq("R")
    out["mayo"] = pd.to_numeric(out["mayo endoscopic subscore"], errors="coerce")
    return out


def analyze_gse73661_uc() -> tuple[pd.DataFrame, pd.DataFrame, list[dict[str, object]]]:
    meta, expr = parse_geo_series_matrix(GEO_URLS["GSE73661_matrix"])
    annot = parse_geo_annotation(GEO_URLS["GPL6244_annot"], set(TARGET_GENES))
    sample_gene = collapse_probes_to_genes(expr, annot)
    parsed = parse_gse73661_meta(meta)
    parsed = parsed.set_index("sample").loc[sample_gene.index].rename_axis("sample").reset_index()
    ref = parsed["timepoint"].eq("W0") & parsed["therapy"].isin(["infliximab", "vedolizumab"])
    scores = module_scores(sample_gene.loc[parsed["sample"]], parsed, ref)
    baseline = scores[
        scores["timepoint"].eq("W0")
        & scores["therapy"].isin(["infliximab", "vedolizumab"])
        & scores["response"].isin(["R", "NR"])
    ].copy()
    base_tests = compare_baseline(
        baseline,
        ["patient", "sample", "therapy_class", "therapy", "responder", "response", "timepoint", "mayo"],
        ["therapy_class", "therapy"],
        "responder",
        "GSE73661",
        "anti-TNF/integrin",
        "infliximab/vedolizumab",
        "ulcerative colitis",
        "colonic mucosal bulk biopsy",
        "baseline response assigned from earliest post-treatment mucosal-healing label",
        "bulk mucosa, Mayo endoscopic severity, treatment arm timing, cell composition; generic inflammation tested by inflammatory_nfkb/ifn_apc residualization",
    )
    pd_scores = scores[
        scores["therapy"].isin(["infliximab", "vedolizumab"])
        & scores["response"].isin(["R", "NR"])
        & scores["timepoint"].isin(["W0", "W4_6", "W6", "W12"])
    ].copy()
    pd_tests = compare_prepost(
        pd_scores,
        "patient",
        "timepoint",
        "W0",
        "time_order",
        ["therapy_class", "therapy", "response"],
        "GSE73661",
        "anti-TNF/integrin",
        "infliximab/vedolizumab",
        "ulcerative colitis",
        "colonic mucosal bulk biopsy",
        "earliest post-treatment minus baseline",
        "post-treatment mucosal-healing/severity and epithelial/immune composition shifts; not independent stratification",
    )
    inv = [
        {
            "accession": "GSE73661",
            "therapy_class": "anti-TNF",
            "therapy": "infliximab",
            "status": "analyzed_public_bulk",
            "response_labels": "mucosal healing at W4-6",
            "modality": "colonic biopsy Affymetrix bulk",
            "url": "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE73661",
        },
        {
            "accession": "GSE73661",
            "therapy_class": "integrin",
            "therapy": "vedolizumab",
            "status": "analyzed_public_bulk",
            "response_labels": "mucosal healing at W6/W12/W52; earliest label used for baseline scout",
            "modality": "colonic biopsy Affymetrix bulk",
            "url": "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE73661",
        },
    ]
    return base_tests, pd_tests, inv


def parse_gse106992_meta(meta: pd.DataFrame) -> pd.DataFrame:
    out = meta.copy()
    out["sample"] = out["Sample_geo_accession"]
    out["patient"] = out["subject id"]
    out["therapy"] = out["treatment"].replace({"Ustekinumab 90 mg": "ustekinumab", "Etanercept": "etanercept"})
    out["therapy_class"] = out["therapy"].map({"etanercept": "anti-TNF", "ustekinumab": "IL-17/IL-23"}).fillna("other")
    out["response"] = out["pasi75resp"].map({"Yes": "R", "No": "NR"}).fillna("")
    out["responder"] = out["response"].eq("R")
    out["timepoint"] = out["time"].str.replace("Week ", "W", regex=False)
    out["time_order"] = out["timepoint"].map({"W0": 0, "W12": 12}).fillna(999)
    out["skin_type"] = np.where(out["skin type"].str.contains("LS", na=False), "LS", "NL")
    return out


def analyze_gse106992_psoriasis() -> tuple[pd.DataFrame, pd.DataFrame, list[dict[str, object]]]:
    meta, expr = parse_geo_series_matrix(GEO_URLS["GSE106992_matrix"])
    annot = parse_geo_annotation(GEO_URLS["GPL570_annot"], set(TARGET_GENES))
    sample_gene = collapse_probes_to_genes(expr, annot)
    parsed = parse_gse106992_meta(meta)
    parsed = parsed.set_index("sample").loc[sample_gene.index].rename_axis("sample").reset_index()
    ref = parsed["skin_type"].eq("LS") & parsed["timepoint"].eq("W0")
    scores = module_scores(sample_gene.loc[parsed["sample"]], parsed, ref)
    baseline = scores[
        scores["skin_type"].eq("LS") & scores["timepoint"].eq("W0") & scores["response"].isin(["R", "NR"])
    ].copy()
    base_tests = compare_baseline(
        baseline,
        ["patient", "sample", "therapy_class", "therapy", "responder", "response", "timepoint", "skin_type"],
        ["therapy_class", "therapy"],
        "responder",
        "GSE106992",
        "anti-TNF/IL-17/IL-23",
        "etanercept/ustekinumab",
        "psoriasis",
        "lesional skin bulk biopsy",
        "baseline PASI75 responder vs non-responder",
        "bulk lesional skin, baseline PASI/severity unavailable in GEO matrix, treatment arm, cell composition; generic inflammation tested by inflammatory_nfkb/ifn_apc residualization",
    )
    pd_scores = scores[
        scores["skin_type"].eq("LS")
        & scores["timepoint"].isin(["W0", "W12"])
        & scores["response"].isin(["R", "NR"])
    ].copy()
    pd_tests = compare_prepost(
        pd_scores,
        "patient",
        "timepoint",
        "W0",
        "time_order",
        ["therapy_class", "therapy", "response"],
        "GSE106992",
        "anti-TNF/IL-17/IL-23",
        "etanercept/ustekinumab",
        "psoriasis",
        "lesional skin bulk biopsy",
        "W12 minus baseline",
        "post-treatment clinical response and lesion resolution; bulk-cell composition and generic inflammation dominate",
    )
    inv = [
        {
            "accession": "GSE106992",
            "therapy_class": "anti-TNF",
            "therapy": "etanercept",
            "status": "analyzed_public_bulk",
            "response_labels": "PASI75 responder/non-responder",
            "modality": "skin biopsy Affymetrix bulk",
            "url": "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE106992",
        },
        {
            "accession": "GSE106992",
            "therapy_class": "IL-17/IL-23",
            "therapy": "ustekinumab",
            "status": "analyzed_public_bulk",
            "response_labels": "PASI75 responder/non-responder",
            "modality": "skin biopsy Affymetrix bulk",
            "url": "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE106992",
        },
    ]
    return base_tests, pd_tests, inv


def parse_gse24742_meta(meta: pd.DataFrame) -> pd.DataFrame:
    out = meta.copy()
    out["sample"] = out["Sample_geo_accession"]
    out["patient"] = out["Sample_title"].str.extract(r"^(RTX\d+)")[0]
    out["response"] = out["response"].str.extract(r"EULAR (.+?)-responder")[0].str.lower()
    out["responder"] = out["response"].isin(["good", "moderate"])
    out["timepoint"] = np.where(out["treatment"].str.contains("baseline", case=False, na=False), "baseline", "W12")
    out["time_order"] = np.where(out["timepoint"].eq("baseline"), 0, 12)
    return out


def analyze_gse24742_rituximab() -> tuple[pd.DataFrame, pd.DataFrame, list[dict[str, object]]]:
    meta, expr = parse_geo_series_matrix(GEO_URLS["GSE24742_matrix"])
    annot = parse_geo_annotation(GEO_URLS["GPL570_annot"], set(TARGET_GENES))
    sample_gene = collapse_probes_to_genes(expr, annot)
    parsed = parse_gse24742_meta(meta)
    parsed = parsed.set_index("sample").loc[sample_gene.index].rename_axis("sample").reset_index()
    ref = parsed["timepoint"].eq("baseline")
    scores = module_scores(sample_gene.loc[parsed["sample"]], parsed, ref)
    baseline = scores[scores["timepoint"].eq("baseline")].copy()
    baseline["response_scope"] = "good_moderate_vs_poor"
    base_tests = compare_baseline(
        baseline,
        ["patient", "sample", "responder", "response", "timepoint", "response_scope"],
        ["response_scope"],
        "responder",
        "GSE24742",
        "anti-CD20",
        "rituximab",
        "rheumatoid arthritis",
        "synovial biopsy bulk",
        "baseline EULAR good/moderate vs poor response",
        "n=12 paired synovium, anti-TNF-resistant RA, synovial B-cell/immune aggregates, steroid coadministration; generic inflammation tested by inflammatory_nfkb/ifn_apc residualization",
    )
    pd_tests = compare_prepost(
        scores,
        "patient",
        "timepoint",
        "baseline",
        "time_order",
        ["response"],
        "GSE24742",
        "anti-CD20",
        "rituximab",
        "rheumatoid arthritis",
        "synovial biopsy bulk",
        "W12 minus baseline by EULAR response class",
        "post-treatment only, synovial composition, B-cell depletion and steroid coadministration",
    )
    inv = [
        {
            "accession": "GSE24742",
            "therapy_class": "anti-CD20",
            "therapy": "rituximab",
            "status": "analyzed_public_bulk",
            "response_labels": "EULAR good/moderate/poor",
            "modality": "synovial biopsy Affymetrix bulk",
            "url": "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE24742",
        },
        {
            "accession": "GSE228330",
            "therapy_class": "anti-CD20",
            "therapy": "ocrelizumab",
            "status": "public_metadata_pd_only_not_analyzed",
            "response_labels": "none; clinically stable MS before/0.5m/6m",
            "modality": "PBMC Clariom microarray",
            "url": "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE228330",
        },
    ]
    return base_tests, pd_tests, inv


def add_public_metadata_inventory() -> list[dict[str, object]]:
    return [
        {
            "accession": "GSE261334",
            "therapy_class": "integrin",
            "therapy": "vedolizumab",
            "status": "public_metadata_parked",
            "response_labels": "series says 5 R/5 NR at W0/W6, but donor-response crosswalk not in local SOFT parse",
            "modality": "PBMC scRNA",
            "url": "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE261334",
        },
        {
            "accession": "GSE171012",
            "therapy_class": "IL-17/IL-23",
            "therapy": "secukinumab",
            "status": "public_metadata_pd_only_not_analyzed",
            "response_labels": "no responder labels in GEO; longitudinal skin/T-cell RNA-seq",
            "modality": "bulk skin and sorted cutaneous T-cell RNA-seq",
            "url": "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE171012",
        },
        {
            "accession": "GSE296117",
            "therapy_class": "anti-TNF/JAK",
            "therapy": "TNF-alpha/JAK inhibitor",
            "status": "public_metadata_heavy_controlled_parked",
            "response_labels": "pre/post synovial-fluid scRNA; response labels not quickly extractable from GEO",
            "modality": "single-cell RDS, controlled raw data",
            "url": "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE296117",
        },
    ]


def interpretation_flags(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    df = df.copy()
    df["min_group_n"] = df[["n_responder", "n_nonresponder"]].min(axis=1)
    df["non_generic_module"] = ~df["module"].isin(GENERIC_MODULES)
    df["generic_independent"] = (
        df["generic_adjusted_p"].fillna(1.0).le(0.01)
        & df["module_generic_max_abs_r"].fillna(1.0).lt(0.50)
        & (np.sign(df["generic_adjusted_delta"].fillna(0)) == np.sign(df["delta_responder_minus_nonresponder"].fillna(0)))
    )
    df["effect_claim_allowed"] = (
        (df["fdr"] <= 0.05)
        & (df["min_group_n"] >= 10)
        & df["non_generic_module"]
        & df["generic_independent"]
        & df["design"].str.contains("single-cell|sorted", case=False, na=False)
    )
    df["kill_reason"] = ""
    df.loc[df["min_group_n"] < 5, "kill_reason"] = "too_underpowered_for_effect_size_claim"
    df.loc[(df["fdr"] > 0.10) & df["kill_reason"].eq(""), "kill_reason"] = "not_corrected_significant"
    df.loc[
        df["module"].isin(GENERIC_MODULES)
        & df["kill_reason"].eq("")
        & df["fdr"].le(0.10),
        "kill_reason",
    ] = "generic_inflammation_module_not_stratum_specific"
    df.loc[
        (~df["generic_independent"])
        & df["kill_reason"].eq("")
        & df["generic_adjustment_covariates"].fillna("").ne(""),
        "kill_reason",
    ] = "not_independent_of_generic_inflammation"
    df.loc[df["effect_claim_allowed"], "kill_reason"] = "not_killed_by_current_filters"
    return df


def ranked_calls(baseline: pd.DataFrame, pd_evidence: pd.DataFrame, inventory: pd.DataFrame) -> pd.DataFrame:
    rows = []
    if not baseline.empty:
        base = baseline.copy()
        base["sort_fdr"] = base["fdr"].fillna(1.0)
        base["sort_p"] = base["p"].fillna(1.0)
        for (dataset, therapy_class, therapy), sub in base.groupby(["dataset", "therapy_class", "therapy"], observed=True):
            best = sub.sort_values(["effect_claim_allowed", "sort_fdr", "sort_p", "min_group_n"], ascending=[False, True, True, False]).iloc[0]
            if bool(best["effect_claim_allowed"]):
                call = "GO"
                reason = "baseline module association survives correction and generic-inflammation residual check"
            elif best["p"] <= 0.05 and best["min_group_n"] >= 5:
                call = "PARK"
                reason = f"nominal baseline association only; {best['kill_reason']}"
            else:
                call = "NO_GO"
                reason = f"no usable baseline stratification signal; {best['kill_reason']}"
            rows.append(
                {
                    "rank": np.nan,
                    "call": call,
                    "dataset": dataset,
                    "therapy_class": therapy_class,
                    "therapy": therapy,
                    "evidence_type": "baseline_response",
                    "best_module": best["module"],
                    "best_scope": best["analysis_scope"],
                    "effect_size": best["hedges_g"],
                    "delta": best["delta_responder_minus_nonresponder"],
                    "p": best["p"],
                    "fdr": best["fdr"],
                    "n": f"{int(best['n_responder'])}R/{int(best['n_nonresponder'])}NR",
                    "generic_adjusted_p": best["generic_adjusted_p"],
                    "generic_max_abs_r": best["module_generic_max_abs_r"],
                    "reason": reason,
                }
            )
    if not pd_evidence.empty:
        for (dataset, therapy_class, therapy), sub in pd_evidence.groupby(["dataset", "therapy_class", "therapy"], observed=True):
            if baseline.empty or not ((baseline["dataset"].eq(dataset)) & (baseline["therapy"].eq(therapy))).any():
                best = sub.sort_values(["fdr", "p"], ascending=[True, True]).iloc[0]
                rows.append(
                    {
                        "rank": np.nan,
                        "call": "PARK" if best["p"] <= 0.05 else "NO_GO",
                        "dataset": dataset,
                        "therapy_class": therapy_class,
                        "therapy": therapy,
                        "evidence_type": "pharmacodynamic_only",
                        "best_module": best["module"],
                        "best_scope": best["analysis_scope"],
                        "effect_size": np.nan,
                        "delta": best["mean_post_minus_pre"],
                        "p": best["p"],
                        "fdr": best["fdr"],
                        "n": f"{int(best['n_pairs'])} pairs",
                        "generic_adjusted_p": np.nan,
                        "generic_max_abs_r": np.nan,
                        "reason": "post-treatment-only signal; cannot support baseline patient stratification",
                    }
                )
    analyzed = {(row["dataset"], row["therapy"]) for row in rows}
    for row in inventory.to_dict(orient="records"):
        key = (row["accession"], row["therapy"])
        if key in analyzed:
            continue
        call = "PARK" if "park" in str(row["status"]) or "pd_only" in str(row["status"]) else "NO_GO"
        rows.append(
            {
                "rank": np.nan,
                "call": call,
                "dataset": row["accession"],
                "therapy_class": row["therapy_class"],
                "therapy": row["therapy"],
                "evidence_type": "metadata_only",
                "best_module": "",
                "best_scope": "",
                "effect_size": np.nan,
                "delta": np.nan,
                "p": np.nan,
                "fdr": np.nan,
                "n": "",
                "generic_adjusted_p": np.nan,
                "generic_max_abs_r": np.nan,
                "reason": row["status"],
            }
        )
    out = pd.DataFrame(rows)
    if out.empty:
        return out
    call_rank = {"GO": 0, "PARK": 1, "NO_GO": 2}
    out["call_order"] = out["call"].map(call_rank).fillna(9)
    out["p_order"] = out["p"].fillna(1.0)
    out = out.sort_values(["call_order", "p_order", "dataset", "therapy"]).drop(columns=["call_order", "p_order"])
    out["rank"] = range(1, len(out) + 1)
    return out


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)

    baseline_parts = []
    pd_parts = []
    inventory_rows = []

    local_base, local_pd, local_inv = analyze_local_wave18()
    baseline_parts.append(local_base)
    pd_parts.append(local_pd)
    inventory_rows.extend(local_inv)

    analyzers = [
        analyze_gse73661_uc,
        analyze_gse106992_psoriasis,
        analyze_gse24742_rituximab,
        analyze_gse250453_fingolimod,
        analyze_gse235357_dmf,
    ]
    run_log = []
    for analyzer in analyzers:
        try:
            base, pd_evidence, inv = analyzer()
            baseline_parts.append(base)
            pd_parts.append(pd_evidence)
            inventory_rows.extend(inv)
            run_log.append({"analyzer": analyzer.__name__, "status": "completed", "baseline_rows": len(base), "pd_rows": len(pd_evidence)})
        except Exception as exc:  # noqa: BLE001
            run_log.append({"analyzer": analyzer.__name__, "status": "failed", "error": f"{type(exc).__name__}: {exc}"})

    inventory_rows.extend(add_public_metadata_inventory())
    inventory = pd.DataFrame(inventory_rows).drop_duplicates()
    baseline = pd.concat([df for df in baseline_parts if not df.empty], ignore_index=True) if baseline_parts else pd.DataFrame()
    pd_evidence = pd.concat([df for df in pd_parts if not df.empty], ignore_index=True) if pd_parts else pd.DataFrame()
    baseline = interpretation_flags(baseline)
    calls = ranked_calls(baseline, pd_evidence, inventory)

    inventory.to_csv(OUT / "public_and_local_dataset_inventory.tsv", sep="\t", index=False, quoting=csv.QUOTE_MINIMAL)
    baseline.to_csv(OUT / "baseline_module_response_evidence.tsv", sep="\t", index=False)
    pd_evidence.to_csv(OUT / "pharmacodynamic_module_evidence.tsv", sep="\t", index=False)
    calls.to_csv(OUT / "ranked_go_park_no_go.tsv", sep="\t", index=False)
    pd.DataFrame(run_log).to_csv(OUT / "run_log.tsv", sep="\t", index=False)

    summary = {
        "random_seed": SEED,
        "n_inventory_rows": int(len(inventory)),
        "n_baseline_rows": int(len(baseline)),
        "n_pharmacodynamic_rows": int(len(pd_evidence)),
        "n_ranked_calls": int(len(calls)),
        "n_go_calls": int(calls["call"].eq("GO").sum()) if not calls.empty else 0,
        "n_park_calls": int(calls["call"].eq("PARK").sum()) if not calls.empty else 0,
        "n_no_go_calls": int(calls["call"].eq("NO_GO").sum()) if not calls.empty else 0,
        "run_log": run_log,
        "guardrail": "No final finding is claimed. Baseline associations must survive multiplicity, minimum group size, and generic-inflammation residual checks before any GO call.",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
