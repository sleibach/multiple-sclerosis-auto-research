#!/usr/bin/env python3
"""Wave18 treatment-response scout for V3 autoimmune modules.

The script keeps analysis in compartments where public metadata allow it:

* GSE138746: RA anti-TNF baseline RNA-seq in PBMC, CD14 monocyte, and CD4 T
  cell compartments. Sample names encode drug and EULAR response class.
* GSE183047: psoriasis lesional skin immune-enriched scRNA-seq before/after
  secukinumab. GEO provides MTX matrices but no cell annotations, so cells are
  assigned to transparent marker-derived compartments.
* GSE253006: UC tofacitinib marker-compartment analysis already exists in V3;
  this script copies the relevant summary into the Wave18 output tree.

Outputs are written under results_v3/wave18_treatment_response/.
"""

from __future__ import annotations

import gzip
import json
import math
import re
import tarfile
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd
import requests
from scipy import io, sparse, stats
from sklearn.metrics import roc_auc_score
from statsmodels.formula.api import ols
from statsmodels.stats.multitest import multipletests

from v3_analyze_direct_h5ad_cell_states import MODULES, ROOT

SEED = 20260527
RAW = ROOT / "data" / "raw_v3"
OUT = ROOT / "results_v3" / "wave18_treatment_response"

GSE138746_RAW = RAW / "wave18_gse138746"
GSE183047_RAW = RAW / "wave18_gse183047"
GSE183047_MTX = GSE183047_RAW / "raw"

RA_FILES = {
    "PBMC": "GSE138746_Counts_Normalization_PBMC.csv.gz",
    "CD14_monocyte": "GSE138746_Counts_Normalization_cd14.csv.gz",
    "CD4_T_cell": "GSE138746_Counts_Normalization_cd4.csv.gz",
}

RA_URL_BASE = "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE138nnn/GSE138746/suppl"
PSO_TAR_URL = "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE183nnn/GSE183047/suppl/GSE183047_RAW.tar"
PSO_SOFT_URL = "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE183nnn/GSE183047/soft/GSE183047_family.soft.gz"

TARGET_GENES = sorted({gene for genes in MODULES.values() for gene in genes})

MARKER_SETS = {
    "myeloid_apc_like": [
        "LYZ",
        "LST1",
        "CST3",
        "CD14",
        "FCGR3A",
        "MS4A7",
        "ITGAX",
        "FCER1A",
        "CLEC10A",
        "LILRA4",
        "IL3RA",
        "HLA-DRA",
        "CD74",
    ],
    "t_cell_like": ["CD3D", "CD3E", "CD3G", "TRAC", "CD4", "CD8A", "CD8B", "NKG7", "GZMA"],
    "b_plasma_like": ["MS4A1", "CD79A", "CD79B", "CD74", "MZB1", "JCHAIN", "IGHG1"],
    "keratinocyte_like": ["KRT5", "KRT14", "KRT1", "KRT10", "KRT16", "KRT17", "S100A7", "S100A8", "S100A9"],
    "stromal_endothelial_like": ["COL1A1", "COL1A2", "DCN", "LUM", "PECAM1", "VWF", "CLDN5", "ACTA2"],
}

PSO_EXTRA_MODULES = {
    "il17_keratinocyte_inflammation": ["IL36G", "S100A7", "S100A8", "S100A9", "DEFB4A", "KRT16", "KRT17"],
    "regulatory_dc_markers": ["THBD", "CLEC4A", "CD1C", "CD14", "LILRB4"],
}

ALL_PSO_MODULES = {**MODULES, **PSO_EXTRA_MODULES}
PSO_GENES = sorted(
    {gene for genes in ALL_PSO_MODULES.values() for gene in genes}
    | {gene for genes in MARKER_SETS.values() for gene in genes}
)


def download_if_missing(url: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.stat().st_size > 0:
        return
    tmp = path.with_suffix(path.suffix + ".tmp")
    urllib.request.urlretrieve(url, tmp)
    tmp.replace(path)


def hedges_g(a: np.ndarray, b: np.ndarray) -> float:
    a = a[np.isfinite(a)]
    b = b[np.isfinite(b)]
    if len(a) < 2 or len(b) < 2:
        return np.nan
    pooled = ((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) / (len(a) + len(b) - 2)
    if pooled <= 0:
        return np.nan
    correction = 1.0 - 3.0 / (4.0 * (len(a) + len(b)) - 9.0)
    return float(((a.mean() - b.mean()) / math.sqrt(pooled)) * correction)


def auc_safe(labels: np.ndarray, scores: np.ndarray) -> float:
    labels = np.asarray(labels)
    scores = np.asarray(scores, dtype=float)
    mask = np.isfinite(scores)
    if mask.sum() < 4 or len(set(labels[mask])) < 2:
        return np.nan
    return float(roc_auc_score(labels[mask], scores[mask]))


def parse_ra_sample(sample: str, compartment: str) -> dict[str, object]:
    match = re.match(r"^(?:PBMC|cd14|cd4)_([AE])_([nmg])_(\d+)$", sample, flags=re.IGNORECASE)
    if not match:
        raise ValueError(f"cannot parse GSE138746 sample name: {sample}")
    drug_code, response_code, patient_id = match.groups()
    return {
        "sample": sample,
        "patient": f"RA_{int(patient_id):02d}",
        "compartment": compartment,
        "drug": {"A": "adalimumab", "E": "etanercept"}[drug_code.upper()],
        "response_code": response_code,
        "response_class": {"g": "good", "m": "moderate", "n": "none"}[response_code],
        "eular_responder": response_code in {"g", "m"},
        "good_responder": response_code == "g",
    }


def load_or_build_gene_map() -> pd.DataFrame:
    path = OUT / "wave18_gse138746_ra_gene_map.tsv"
    if path.exists() and path.stat().st_size > 0:
        return pd.read_csv(path, sep="\t")

    rows = []
    for symbol in TARGET_GENES:
        url = f"https://rest.ensembl.org/xrefs/symbol/homo_sapiens/{symbol}"
        try:
            response = requests.get(url, headers={"Content-Type": "application/json"}, timeout=20)
            response.raise_for_status()
            payload = response.json()
            ids = sorted({item["id"] for item in payload if item.get("type") == "gene" and item.get("id", "").startswith("ENSG")})
        except Exception as exc:  # noqa: BLE001
            ids = []
            rows.append({"gene_symbol": symbol, "ensembl_gene_id": "", "status": f"lookup_failed:{type(exc).__name__}"})
            continue
        if ids:
            for ens in ids:
                rows.append({"gene_symbol": symbol, "ensembl_gene_id": ens, "status": "mapped"})
        else:
            rows.append({"gene_symbol": symbol, "ensembl_gene_id": "", "status": "unmapped"})
    out = pd.DataFrame(rows)
    out.to_csv(path, sep="\t", index=False)
    return out


def ensure_ra_inputs() -> None:
    GSE138746_RAW.mkdir(parents=True, exist_ok=True)
    for filename in RA_FILES.values():
        download_if_missing(f"{RA_URL_BASE}/{filename}", GSE138746_RAW / filename)


def analyze_gse138746_ra() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    ensure_ra_inputs()
    gene_map = load_or_build_gene_map()
    ens_by_symbol = (
        gene_map[gene_map["ensembl_gene_id"].notna() & gene_map["ensembl_gene_id"].ne("")]
        .groupby("gene_symbol")["ensembl_gene_id"]
        .apply(list)
        .to_dict()
    )
    score_rows = []
    presence_rows = []

    for compartment, filename in RA_FILES.items():
        expr = pd.read_csv(GSE138746_RAW / filename, index_col=0)
        expr.index = expr.index.astype(str)
        log_expr = np.log1p(expr.astype(float))
        gene_values: dict[str, np.ndarray] = {}
        for symbol in TARGET_GENES:
            ids = [ens for ens in ens_by_symbol.get(symbol, []) if ens in log_expr.index]
            presence_rows.append(
                {
                    "dataset": "GSE138746",
                    "compartment": compartment,
                    "gene_symbol": symbol,
                    "n_ensembl_ids_present": len(ids),
                    "ensembl_ids_present": ",".join(ids),
                }
            )
            if ids:
                gene_values[symbol] = log_expr.loc[ids].mean(axis=0).to_numpy(float)

        sample_meta = pd.DataFrame([parse_ra_sample(col, compartment) for col in log_expr.columns])
        for module, genes in MODULES.items():
            present = [gene for gene in genes if gene in gene_values]
            if not present:
                continue
            mat = np.vstack([gene_values[gene] for gene in present])
            means = np.nanmean(mat, axis=1)
            sds = np.nanstd(mat, axis=1, ddof=1)
            sds[~np.isfinite(sds) | (sds < 1e-6)] = 1.0
            z = (mat - means[:, None]) / sds[:, None]
            scores = np.nanmean(z, axis=0)
            for idx, sample in enumerate(log_expr.columns):
                row = sample_meta.iloc[idx].to_dict()
                row.update(
                    {
                        "dataset": "GSE138746",
                        "module": module,
                        "n_genes_present": len(present),
                        "genes_present": ",".join(present),
                        "score": float(scores[idx]),
                    }
                )
                score_rows.append(row)

    scores = pd.DataFrame(score_rows)
    presence = pd.DataFrame(presence_rows)
    tests = compare_ra_response(scores)
    scores.to_csv(OUT / "wave18_gse138746_ra_sample_module_scores.tsv", sep="\t", index=False)
    presence.to_csv(OUT / "wave18_gse138746_ra_gene_presence.tsv", sep="\t", index=False)
    tests.to_csv(OUT / "wave18_gse138746_ra_baseline_response_tests.tsv", sep="\t", index=False)
    return scores, tests, presence


def compare_ra_response(scores: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for endpoint, label_col, include_codes in [
        ("eular_responder_moderate_or_good_vs_none", "eular_responder", {"n", "m", "g"}),
        ("good_responder_vs_none", "good_responder", {"n", "g"}),
    ]:
        endpoint_scores = scores[scores["response_code"].isin(include_codes)].copy()
        for (compartment, drug, module), sub in endpoint_scores.groupby(["compartment", "drug", "module"], observed=True):
            labels = sub[label_col].astype(bool)
            yes = sub.loc[labels, "score"].to_numpy(float)
            no = sub.loc[~labels, "score"].to_numpy(float)
            if len(yes) >= 2 and len(no) >= 2:
                t_stat, p_value = stats.ttest_ind(yes, no, equal_var=False, nan_policy="omit")
            else:
                t_stat, p_value = np.nan, np.nan
            rows.append(
                {
                    "dataset": "GSE138746",
                    "test": endpoint,
                    "compartment": compartment,
                    "drug_scope": drug,
                    "module": module,
                    "n_responder": int(len(yes)),
                    "n_nonresponder": int(len(no)),
                    "mean_responder": float(np.nanmean(yes)) if len(yes) else np.nan,
                    "mean_nonresponder": float(np.nanmean(no)) if len(no) else np.nan,
                    "delta_responder_minus_nonresponder": float(np.nanmean(yes) - np.nanmean(no)) if len(yes) and len(no) else np.nan,
                    "hedges_g": hedges_g(yes, no),
                    "welch_t": float(t_stat) if pd.notna(t_stat) else np.nan,
                    "p": float(p_value) if pd.notna(p_value) else np.nan,
                    "auc_responder_high": auc_safe(labels.astype(int).to_numpy(), sub["score"].to_numpy(float)),
                    "drug_adjusted_beta": np.nan,
                    "drug_adjusted_p": np.nan,
                }
            )
        for (compartment, module), sub in endpoint_scores.groupby(["compartment", "module"], observed=True):
            labels = sub[label_col].astype(bool)
            yes = sub.loc[labels, "score"].to_numpy(float)
            no = sub.loc[~labels, "score"].to_numpy(float)
            if len(yes) >= 2 and len(no) >= 2:
                t_stat, p_value = stats.ttest_ind(yes, no, equal_var=False, nan_policy="omit")
            else:
                t_stat, p_value = np.nan, np.nan
            adj_beta = np.nan
            adj_p = np.nan
            if labels.nunique() == 2 and sub["drug"].nunique() == 2:
                model_df = sub[["score", "drug"]].copy()
                model_df["responder"] = labels.astype(int).to_numpy()
                try:
                    fit = ols("score ~ responder + C(drug)", data=model_df).fit()
                    adj_beta = float(fit.params.get("responder", np.nan))
                    adj_p = float(fit.pvalues.get("responder", np.nan))
                except Exception:  # noqa: BLE001
                    pass
            rows.append(
                {
                    "dataset": "GSE138746",
                    "test": endpoint,
                    "compartment": compartment,
                    "drug_scope": "all_anti_tnf_drug_adjusted",
                    "module": module,
                    "n_responder": int(len(yes)),
                    "n_nonresponder": int(len(no)),
                    "mean_responder": float(np.nanmean(yes)) if len(yes) else np.nan,
                    "mean_nonresponder": float(np.nanmean(no)) if len(no) else np.nan,
                    "delta_responder_minus_nonresponder": float(np.nanmean(yes) - np.nanmean(no)) if len(yes) and len(no) else np.nan,
                    "hedges_g": hedges_g(yes, no),
                    "welch_t": float(t_stat) if pd.notna(t_stat) else np.nan,
                    "p": float(p_value) if pd.notna(p_value) else np.nan,
                    "auc_responder_high": auc_safe(labels.astype(int).to_numpy(), sub["score"].to_numpy(float)),
                    "drug_adjusted_beta": adj_beta,
                    "drug_adjusted_p": adj_p,
                }
            )
    out = pd.DataFrame(rows)
    if not out.empty:
        out["fdr"] = multipletests(out["p"].fillna(1.0), method="fdr_bh")[1]
        out["drug_adjusted_fdr"] = multipletests(out["drug_adjusted_p"].fillna(1.0), method="fdr_bh")[1]
    return out


def parse_pso_soft() -> pd.DataFrame:
    soft_path = GSE183047_RAW / "GSE183047_family.soft.gz"
    download_if_missing(PSO_SOFT_URL, soft_path)
    rows = []
    current: dict[str, str] = {}
    with gzip.open(soft_path, "rt", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            line = line.rstrip("\n")
            if line.startswith("^SAMPLE"):
                if current:
                    rows.append(current)
                current = {"gsm": line.split("=", 1)[1].strip()}
            elif current and line.startswith("!Sample_title"):
                current["title"] = line.split("=", 1)[1].strip()
            elif current and line.startswith("!Sample_supplementary_file"):
                value = line.split("=", 1)[1].strip()
                if "matrix.mtx.gz" in value:
                    current["matrix_url"] = value
        if current:
            rows.append(current)
    meta = pd.DataFrame(rows)
    meta = meta[meta["title"].fillna("").str.contains("Psoriasis|Control", case=False)].copy()
    parsed = meta["title"].apply(parse_pso_title).apply(pd.Series)
    return pd.concat([meta, parsed], axis=1)


def parse_pso_title(title: str) -> dict[str, object]:
    if title.startswith("Control"):
        return {"patient": title, "group": "control", "lesion": "control", "timepoint": "control", "time_order": -1}
    match = re.match(r"^(Psoriasis\d+)_(preTx|postTx_week\d+)_(LS|NL)(?:_\d+)?$", title)
    if not match:
        return {"patient": title, "group": "unknown", "lesion": "unknown", "timepoint": "unknown", "time_order": np.nan}
    patient, timepoint, lesion = match.groups()
    order = 0 if timepoint == "preTx" else int(re.search(r"week(\d+)", timepoint).group(1))
    return {"patient": patient, "group": "psoriasis", "lesion": lesion, "timepoint": timepoint, "time_order": order}


def ensure_pso_inputs() -> None:
    GSE183047_MTX.mkdir(parents=True, exist_ok=True)
    if list(GSE183047_MTX.glob("*_matrix.mtx.gz")):
        return
    tar_path = GSE183047_RAW / "GSE183047_RAW.tar"
    download_if_missing(PSO_TAR_URL, tar_path)
    with tarfile.open(tar_path, "r") as tar:
        tar.extractall(GSE183047_MTX)


def read_features(path: Path) -> pd.DataFrame:
    rows = []
    with gzip.open(path, "rt") as handle:
        for line in handle:
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 2:
                rows.append({"gene_id": parts[0], "gene_symbol": parts[1]})
    out = pd.DataFrame(rows)
    out["row_index"] = np.arange(out.shape[0])
    return out


def pso_selected_log_expression(prefix: str) -> tuple[pd.DataFrame, np.ndarray, list[str]]:
    features_path = GSE183047_MTX / f"{prefix}_features.tsv.gz"
    matrix_path = GSE183047_MTX / f"{prefix}_matrix.mtx.gz"
    barcodes_path = GSE183047_MTX / f"{prefix}_barcodes.tsv.gz"
    missing = [p for p in [features_path, matrix_path, barcodes_path] if not p.exists() or p.stat().st_size == 0]
    if missing:
        raise FileNotFoundError("missing psoriasis sample files: " + ", ".join(str(p) for p in missing))

    features = read_features(features_path)
    row_to_gene: dict[int, str] = {}
    for gene in PSO_GENES:
        hits = features.loc[features["gene_symbol"].eq(gene), "row_index"]
        if not hits.empty:
            row_to_gene[int(hits.iloc[0])] = gene
    rows = sorted(row_to_gene)
    genes = [row_to_gene[i] for i in rows]
    with gzip.open(barcodes_path, "rt") as handle:
        barcodes = [line.strip() for line in handle if line.strip()]

    mat = io.mmread(str(matrix_path)).tocsc().astype(float)
    if mat.shape[0] != len(features) and mat.shape[1] == len(features):
        mat = mat.T.tocsc()
    if mat.shape[0] != len(features):
        raise ValueError(f"unexpected matrix/features shape for {prefix}: {mat.shape}, {len(features)}")
    lib = np.asarray(mat.sum(axis=0)).ravel()
    lib_safe = lib.copy()
    lib_safe[~np.isfinite(lib_safe) | (lib_safe <= 0)] = np.nan
    selected = mat[rows, :].T.tocsr()
    norm = selected.multiply(np.divide(1.0, lib_safe, out=np.zeros_like(lib_safe), where=np.isfinite(lib_safe))[:, None]).multiply(1e4)
    log_expr = np.log1p(norm.toarray()).astype(np.float32)
    obs = pd.DataFrame({"sample_prefix": prefix, "barcode": barcodes, "n_counts": lib})
    return obs, log_expr, genes


def classify_marker_compartments(obs: pd.DataFrame, expr: np.ndarray, genes: list[str]) -> pd.DataFrame:
    gene_to_idx = {gene: i for i, gene in enumerate(genes)}
    scores = {}
    for compartment, markers in MARKER_SETS.items():
        present = [gene for gene in markers if gene in gene_to_idx]
        scores[compartment] = (
            np.nanmean(expr[:, [gene_to_idx[gene] for gene in present]], axis=1)
            if present
            else np.full(expr.shape[0], np.nan)
        )
    score_df = pd.DataFrame(scores)
    vals = score_df.to_numpy(float)
    order = np.argsort(np.nan_to_num(vals, nan=-np.inf), axis=1)
    top = order[:, -1]
    second = order[:, -2]
    top_score = vals[np.arange(vals.shape[0]), top]
    second_score = vals[np.arange(vals.shape[0]), second]
    compartments = np.array(score_df.columns)[top].astype(object)
    ambiguous = (~np.isfinite(top_score)) | (top_score < 0.20) | ((top_score - second_score) < 0.05)
    compartments[ambiguous] = "ambiguous"
    out = obs.copy()
    for col in score_df.columns:
        out[f"marker_{col}"] = score_df[col].to_numpy(float)
    out["marker_compartment"] = compartments
    out["marker_top_score"] = top_score
    out["marker_margin"] = top_score - second_score
    return out


def analyze_gse183047_psoriasis() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    ensure_pso_inputs()
    meta = parse_pso_soft()
    meta = meta[meta["title"].notna()].copy()
    meta["sample_prefix"] = meta["gsm"] + "_" + meta["title"]

    obs_tables = []
    expr_tables = []
    gene_sets = []
    run_log = []
    for _, sample in meta.iterrows():
        prefix = sample["sample_prefix"]
        try:
            obs, expr, genes = pso_selected_log_expression(prefix)
            obs = classify_marker_compartments(obs, expr, genes)
            for col in ["gsm", "title", "patient", "group", "lesion", "timepoint", "time_order"]:
                obs[col] = sample[col]
            obs_tables.append(obs)
            expr_tables.append(pd.DataFrame(expr, columns=genes))
            gene_sets.append(set(genes))
            run_log.append({"sample_prefix": prefix, "status": "completed", "n_cells": int(len(obs)), "n_genes_selected": int(len(genes))})
        except Exception as exc:  # noqa: BLE001
            run_log.append({"sample_prefix": prefix, "status": "failed", "error": f"{type(exc).__name__}: {exc}"})
    if not obs_tables:
        raise RuntimeError("No GSE183047 psoriasis samples analyzed")

    obs_all = pd.concat(obs_tables, ignore_index=True)
    common_genes = sorted(set.intersection(*gene_sets))
    expr_all = pd.concat([df.reindex(columns=common_genes) for df in expr_tables], ignore_index=True).to_numpy(dtype=float)
    gene_to_idx = {gene: i for i, gene in enumerate(common_genes)}

    cell_rows = []
    module_gene_rows = []
    for compartment, comp_obs in obs_all.groupby("marker_compartment", observed=True):
        if compartment == "ambiguous":
            continue
        comp_idx = comp_obs.index.to_numpy()
        baseline_mask = comp_obs["group"].eq("psoriasis").to_numpy() & comp_obs["lesion"].eq("LS").to_numpy() & comp_obs["timepoint"].eq("preTx").to_numpy()
        if baseline_mask.sum() < 100:
            continue
        comp_expr = expr_all[comp_idx, :]
        baseline_expr = comp_expr[baseline_mask, :]
        mean = np.nanmean(baseline_expr, axis=0)
        sd = np.nanstd(baseline_expr, axis=0, ddof=1)
        sd[~np.isfinite(sd) | (sd < 1e-6)] = 1.0
        z = (comp_expr - mean) / sd
        for module, genes in ALL_PSO_MODULES.items():
            present = [gene for gene in genes if gene in gene_to_idx]
            module_gene_rows.append(
                {
                    "dataset": "GSE183047",
                    "marker_compartment": compartment,
                    "module": module,
                    "n_genes_present": len(present),
                    "genes_present": ",".join(present),
                }
            )
            if not present:
                continue
            vals = np.nanmean(z[:, [gene_to_idx[gene] for gene in present]], axis=1)
            threshold = np.nanpercentile(vals[baseline_mask], 75)
            tmp = comp_obs[["gsm", "title", "patient", "group", "lesion", "timepoint", "time_order", "marker_compartment"]].copy()
            tmp["module"] = module
            tmp["score"] = vals
            tmp["high"] = vals > threshold
            cell_rows.append(tmp)

    cell_scores = pd.concat(cell_rows, ignore_index=True) if cell_rows else pd.DataFrame()
    sample_rows = []
    if not cell_scores.empty:
        group_cols = ["gsm", "title", "patient", "group", "lesion", "timepoint", "time_order", "marker_compartment", "module"]
        for keys, sub in cell_scores.groupby(group_cols, observed=True):
            if len(sub) < 25:
                continue
            row = dict(zip(group_cols, keys, strict=True))
            row.update({"dataset": "GSE183047", "n_cells": int(len(sub)), "mean_score": float(np.nanmean(sub["score"])), "high_fraction": float(np.nanmean(sub["high"]))})
            sample_rows.append(row)
    sample_scores = pd.DataFrame(sample_rows)
    prepost = compare_pso_prepost(sample_scores) if not sample_scores.empty else pd.DataFrame()
    counts = (
        obs_all.groupby(["gsm", "title", "patient", "group", "lesion", "timepoint", "marker_compartment"], observed=True)
        .size()
        .reset_index(name="n_cells")
    )
    counts.to_csv(OUT / "wave18_gse183047_psoriasis_compartment_counts.tsv", sep="\t", index=False)
    pd.DataFrame(module_gene_rows).to_csv(OUT / "wave18_gse183047_psoriasis_module_genes_present.tsv", sep="\t", index=False)
    sample_scores.to_csv(OUT / "wave18_gse183047_psoriasis_sample_module_scores.tsv", sep="\t", index=False)
    prepost.to_csv(OUT / "wave18_gse183047_psoriasis_prepost_tests.tsv", sep="\t", index=False)
    pd.DataFrame(run_log).to_csv(OUT / "wave18_gse183047_psoriasis_run_log.tsv", sep="\t", index=False)
    return sample_scores, prepost, counts


def compare_pso_prepost(sample_scores: pd.DataFrame) -> pd.DataFrame:
    rows = []
    pso = sample_scores[sample_scores["group"].eq("psoriasis") & sample_scores["lesion"].eq("LS")].copy()
    for (compartment, module), sub in pso.groupby(["marker_compartment", "module"], observed=True):
        base = sub[sub["timepoint"].eq("preTx")].sort_values("gsm").drop_duplicates("patient").set_index("patient")
        post = sub[sub["timepoint"].str.startswith("postTx", na=False)].copy()
        post = post.sort_values("time_order").drop_duplicates("patient").set_index("patient")
        common = sorted(set(base.index) & set(post.index))
        for metric in ["mean_score", "high_fraction"]:
            if len(common) >= 2:
                diff = post.loc[common, metric].to_numpy(float) - base.loc[common, metric].to_numpy(float)
                t_stat, p_value = stats.ttest_1samp(diff, 0.0, nan_policy="omit")
            else:
                diff, t_stat, p_value = np.array([]), np.nan, np.nan
            rows.append(
                {
                    "dataset": "GSE183047",
                    "test": "earliest_post_secukinumab_minus_pretreatment",
                    "marker_compartment": compartment,
                    "module": module,
                    "metric": metric,
                    "n_pairs": int(len(diff)),
                    "mean_delta": float(np.nanmean(diff)) if len(diff) else np.nan,
                    "median_delta": float(np.nanmedian(diff)) if len(diff) else np.nan,
                    "one_sample_t": float(t_stat) if pd.notna(t_stat) else np.nan,
                    "p": float(p_value) if pd.notna(p_value) else np.nan,
                }
            )
    out = pd.DataFrame(rows)
    if not out.empty:
        out["fdr"] = multipletests(out["p"].fillna(1.0), method="fdr_bh")[1]
    return out


def summarize_existing_gse253006() -> pd.DataFrame:
    base = ROOT / "results_v3" / "gse253006_tofacitinib_marker"
    rows = []
    baseline_path = base / "gse253006_marker_baseline_response_tests.tsv"
    prepost_path = base / "gse253006_marker_prepost_tests.tsv"
    if baseline_path.exists():
        baseline = pd.read_csv(baseline_path, sep="\t")
        keep = baseline[baseline["module"].isin(MODULES)].copy()
        for _, row in keep.sort_values(["fdr", "p", "hedges_g"], ascending=[True, True, False]).head(20).iterrows():
            rows.append(
                {
                    "dataset": "GSE253006",
                    "analysis_type": "baseline_response",
                    "compartment": row["marker_compartment"],
                    "module": row["module"],
                    "metric": row["metric"],
                    "n": f"{int(row['n_responder'])}R/{int(row['n_nonresponder'])}NR",
                    "effect": row["delta_responder_minus_nonresponder"],
                    "p": row["p"],
                    "fdr": row["fdr"],
                    "note": "UC tofacitinib marker-derived compartments; copied from existing V3 output",
                }
            )
    if prepost_path.exists():
        prepost = pd.read_csv(prepost_path, sep="\t")
        keep = prepost[prepost["module"].isin(MODULES)].copy()
        for _, row in keep.sort_values(["fdr", "p", "mean_delta"], ascending=[True, True, True]).head(20).iterrows():
            rows.append(
                {
                    "dataset": "GSE253006",
                    "analysis_type": "prepost_pharmacodynamic",
                    "compartment": row["marker_compartment"],
                    "module": row["module"],
                    "metric": row["metric"],
                    "n": f"{int(row['n_pairs'])} pairs {row['group']}",
                    "effect": row["mean_delta"],
                    "p": row["p"],
                    "fdr": row["fdr"],
                    "note": "earliest post-tofacitinib minus baseline",
                }
            )
    out = pd.DataFrame(rows)
    out.to_csv(OUT / "wave18_existing_gse253006_uc_summary.tsv", sep="\t", index=False)
    return out


def build_dataset_scout() -> pd.DataFrame:
    rows = [
        {
            "accession": "GSE253006",
            "disease": "ulcerative colitis",
            "treatment": "tofacitinib",
            "modality": "10x scRNA per-sample matrices; marker-derived compartments",
            "response_or_time": "baseline responder/non-responder and post-treatment timepoints",
            "wave18_status": "analyzed_existing_v3",
            "decision": "baseline predictor not corrected-significant; pharmacodynamic evidence weak/mixed",
        },
        {
            "accession": "GSE138746",
            "disease": "rheumatoid arthritis",
            "treatment": "adalimumab or etanercept",
            "modality": "bulk RNA-seq in sorted PBMC, CD14 monocyte, CD4 T cell compartments",
            "response_or_time": "baseline only; EULAR response class encoded as g/m/n",
            "wave18_status": "analyzed_wave18",
            "decision": "best corrected baseline-predictor dataset in this scout",
        },
        {
            "accession": "GSE183047",
            "disease": "psoriasis",
            "treatment": "secukinumab anti-IL-17A",
            "modality": "immune-enriched scRNA-seq MTX; marker-derived compartments",
            "response_or_time": "pre/post lesional skin; no responder labels in GEO",
            "wave18_status": "analyzed_wave18",
            "decision": "pharmacodynamic-only psoriasis evidence",
        },
        {
            "accession": "GSE261334",
            "disease": "ulcerative colitis",
            "treatment": "vedolizumab",
            "modality": "PBMC scRNA-seq 10x H5 plus VDJ",
            "response_or_time": "GEO series says 5 responders and 5 non-responders at week 0 and week 6, but donor-level response labels are not in SOFT",
            "wave18_status": "scouted_not_analyzed",
            "decision": "park until donor-to-response crosswalk is obtained; otherwise pharmacodynamic-only",
        },
        {
            "accession": "GSE296117",
            "disease": "rheumatoid arthritis",
            "treatment": "TNF-alpha/JAK inhibitor; synovial fluid pre/post",
            "modality": "single-cell RDS, 106,506 cells; raw human data controlled at GSA HRA011646",
            "response_or_time": "paired pre/post treatment, response labels unclear from GEO",
            "wave18_status": "scouted_not_analyzed",
            "decision": "high-value follow-up, but 2.3 GB RDS and controlled raw files make it too heavy for this scout",
        },
        {
            "accession": "GSE250453",
            "disease": "multiple sclerosis",
            "treatment": "fingolimod",
            "modality": "PBMC bulk RNA-seq",
            "response_or_time": "5 responders and 5 non-responders, baseline and 12 months",
            "wave18_status": "scouted_not_analyzed",
            "decision": "MS response dataset exists but is all-PBMC bulk; park for low-weight sensitivity only",
        },
        {
            "accession": "GSE235357",
            "disease": "multiple sclerosis",
            "treatment": "dimethyl fumarate",
            "modality": "blood/PBMC bulk RNA-seq",
            "response_or_time": "5 responders and 5 non-responders, baseline and 12 months",
            "wave18_status": "scouted_not_analyzed",
            "decision": "MS response dataset exists but is all-PBMC bulk; park for low-weight sensitivity only",
        },
    ]
    out = pd.DataFrame(rows)
    out.to_csv(OUT / "wave18_dataset_scout.tsv", sep="\t", index=False)
    return out


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    scout = build_dataset_scout()
    ra_scores, ra_tests, ra_presence = analyze_gse138746_ra()
    try:
        pso_scores, pso_prepost, pso_counts = analyze_gse183047_psoriasis()
        pso_status = {"status": "completed", "n_sample_module_rows": int(len(pso_scores)), "n_prepost_tests": int(len(pso_prepost))}
    except Exception as exc:  # noqa: BLE001
        pso_scores, pso_prepost, pso_counts = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
        pso_status = {"status": "failed", "error": f"{type(exc).__name__}: {exc}"}
    uc_summary = summarize_existing_gse253006()

    top_ra = (
        ra_tests.sort_values(["fdr", "p", "hedges_g"], ascending=[True, True, False])
        .head(30)
        .to_dict(orient="records")
        if not ra_tests.empty
        else []
    )
    top_pso_decreases = (
        pso_prepost[pso_prepost["mean_delta"] < 0]
        .sort_values(["fdr", "p", "mean_delta"], ascending=[True, True, True])
        .head(30)
        .to_dict(orient="records")
        if not pso_prepost.empty
        else []
    )
    summary = {
        "random_seed": SEED,
        "datasets_scouted": scout["accession"].tolist(),
        "gse138746_ra": {
            "n_sample_module_rows": int(len(ra_scores)),
            "n_tests": int(len(ra_tests)),
            "n_gene_presence_rows": int(len(ra_presence)),
            "top_results": top_ra,
        },
        "gse183047_psoriasis": pso_status | {"top_decreases": top_pso_decreases},
        "gse253006_uc_existing_summary_rows": int(len(uc_summary)),
        "interpretation_guardrail": (
            "RA GSE138746 is compartment-resolved sorted bulk and can test baseline prediction. "
            "UC GSE253006 and psoriasis GSE183047 use marker-derived compartments rather than curated cell labels. "
            "MS candidates found in this pass are all-PBMC bulk and are not promoted as primary evidence."
        ),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
