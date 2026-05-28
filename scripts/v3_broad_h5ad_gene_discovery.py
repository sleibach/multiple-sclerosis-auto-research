#!/usr/bin/env python3
"""Broad donor-level gene discovery across local autoimmune h5ad atlases.

Prior V3 pivots tested hand-picked targets and repeatedly found comparator
biology rather than a final target. This script broadens the search. It builds
donor-level pseudobulk expression for every mapped gene in each available local
h5ad compartment, tests case-vs-control at the donor level, and ranks genes by
cross-disease recurrence, MS white-matter microglia support, and local
OpenTargets-style evidence.

It is intentionally a discovery screen, not a final causal test.
"""

from __future__ import annotations

import json
import math
import re
from dataclasses import asdict
from pathlib import Path

import anndata as ad
import numpy as np
import pandas as pd
from scipy import sparse, stats
from statsmodels.stats.multitest import multipletests

from v3_analyze_osmr_complement_axes import CONFIGS, DirectConfig, ROOT

SEED = 20260526
OUT = ROOT / "results_v3" / "broad_h5ad_gene_discovery"
MS_SIGNATURE = ROOT / "results_v3" / "gse111972_full_ms_wm_signature.tsv"
OPENTARGETS = ROOT / "results_v3" / "opentargets_candidate_disease_hits.tsv"
CENTRAL_FIRST_PASS = ROOT / "results_v3" / "central_node_first_pass_rank.tsv"

MIN_DONOR_CELLS = 10
MIN_DONORS_PER_GROUP = 2
MIN_DETECTED_DONOR_FRACTION = 0.20
MIN_MEAN_LOG2_CPM = 0.25
MIN_ABS_DELTA_FOR_DIRECTION = 0.20

GENE_SYMBOL_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_.-]*$")
BAD_PREFIXES = ("ENSG", "LOC", "LINC", "AC0", "AL0", "MIR", "RNU", "SNOR", "RNA", "MT-")

LIPID_LYSOSOMAL_MYEOID_NEIGHBORHOOD = {
    "ACSL1",
    "ACSL3",
    "ACSL4",
    "ACSL5",
    "APOE",
    "APOC1",
    "LPL",
    "LIPA",
    "LAMP1",
    "LAMP2",
    "LAMP3",
    "CTSA",
    "CTSB",
    "CTSD",
    "CTSS",
    "CTSL",
    "IFI30",
    "TPP1",
    "GPNMB",
    "TREM2",
    "TYROBP",
    "MERTK",
    "AXL",
    "TYRO3",
    "MSR1",
    "MARCO",
    "CD36",
    "SCARB1",
    "SCARB2",
    "LRP1",
    "CALR",
    "CD44",
    "SPP1",
    "LGALS1",
    "LGALS3",
    "FABP5",
    "PLIN2",
    "PPARG",
    "NUPR1",
    "CHI3L1",
    "CST3",
    "VSIG4",
    "FOLR2",
    "MRC1",
    "STAB1",
    "LYVE1",
    "PLA2G7",
    "TBXAS1",
    "PTGS2",
    "ALOX5",
    "C1QA",
    "C1QB",
    "C1QC",
    "C3",
    "C3AR1",
    "C5AR1",
}


def clean_gene_symbol(symbol: object) -> str | None:
    value = str(symbol).strip()
    if not value or value.lower() == "nan":
        return None
    if not GENE_SYMBOL_RE.match(value):
        return None
    if any(value.upper().startswith(prefix) for prefix in BAD_PREFIXES):
        return None
    return value.upper()


def hedges_g(case: np.ndarray, control: np.ndarray) -> float:
    case = np.asarray(case, dtype=float)
    control = np.asarray(control, dtype=float)
    case = case[np.isfinite(case)]
    control = control[np.isfinite(control)]
    if len(case) < 2 or len(control) < 2:
        return np.nan
    pooled = ((len(case) - 1) * case.var(ddof=1) + (len(control) - 1) * control.var(ddof=1)) / (
        len(case) + len(control) - 2
    )
    if pooled <= 0:
        return np.nan
    correction = 1.0 - (3.0 / (4.0 * (len(case) + len(control)) - 9.0))
    return float(((case.mean() - control.mean()) / math.sqrt(pooled)) * correction)


def unique_gene_matrix(donor_counts: np.ndarray, donor_detect: np.ndarray, symbols: list[str]) -> tuple[pd.DataFrame, pd.DataFrame]:
    counts_by_symbol: dict[str, np.ndarray] = {}
    detect_by_symbol: dict[str, np.ndarray] = {}
    for idx, raw_symbol in enumerate(symbols):
        symbol = clean_gene_symbol(raw_symbol)
        if symbol is None:
            continue
        if symbol not in counts_by_symbol:
            counts_by_symbol[symbol] = donor_counts[:, idx].astype(float, copy=True)
            detect_by_symbol[symbol] = donor_detect[:, idx].astype(float, copy=True)
        else:
            counts_by_symbol[symbol] += donor_counts[:, idx]
            detect_by_symbol[symbol] += donor_detect[:, idx]
    counts = pd.DataFrame(counts_by_symbol)
    detect = pd.DataFrame(detect_by_symbol)
    return counts, detect


def aggregate_config(config: DirectConfig, a, x) -> tuple[pd.DataFrame, pd.DataFrame]:
    obs = a.obs.copy()
    mask = obs["disease"].isin([config.disease_label, config.control_label]) & obs["cell_type"].isin(config.cell_types)
    obs_sub = obs.loc[mask].copy()
    cell_idx = np.flatnonzero(mask.to_numpy())
    if obs_sub.empty:
        raise ValueError(f"no cells for {config.name}")
    donor_counts = obs_sub.groupby(["donor_id", "disease"], observed=True).size().rename("n_cells").reset_index()
    donor_counts = donor_counts.loc[donor_counts["n_cells"] >= MIN_DONOR_CELLS].copy()
    if donor_counts.empty:
        raise ValueError(f"no donors with >= {MIN_DONOR_CELLS} cells for {config.name}")
    donor_keys = list(zip(donor_counts["donor_id"].astype(str), donor_counts["disease"].astype(str), strict=False))
    key_to_row = {key: i for i, key in enumerate(donor_keys)}
    rows = []
    cols = []
    data = []
    for local_cell, (donor, disease) in enumerate(
        zip(obs_sub["donor_id"].astype(str), obs_sub["disease"].astype(str), strict=False)
    ):
        key = (donor, disease)
        if key in key_to_row:
            rows.append(key_to_row[key])
            cols.append(local_cell)
            data.append(1.0)
    group = sparse.csr_matrix((data, (rows, cols)), shape=(len(donor_keys), len(obs_sub)))
    x_sub = x[cell_idx]
    summed = group @ x_sub
    detected = group @ (x_sub > 0)
    if sparse.issparse(summed):
        summed_arr = summed.toarray()
    else:
        summed_arr = np.asarray(summed)
    if sparse.issparse(detected):
        detect_arr = detected.toarray()
    else:
        detect_arr = np.asarray(detected)

    if config.gene_symbol_column in a.var.columns:
        raw_symbols = a.var[config.gene_symbol_column].astype(str).tolist()
    elif "feature_name" in a.var.columns:
        raw_symbols = a.var["feature_name"].astype(str).tolist()
    else:
        raw_symbols = list(map(str, a.var_names))
    counts, detect = unique_gene_matrix(summed_arr, detect_arr, raw_symbols)
    n_cells = donor_counts["n_cells"].to_numpy(float)
    lib_size = counts.sum(axis=1).replace(0, np.nan)
    log2_cpm = np.log2(counts.div(lib_size, axis=0).mul(1e6) + 1.0)
    detect_fraction = detect.div(n_cells, axis=0)

    meta = donor_counts.copy()
    meta["analysis"] = config.name
    meta["dataset_path"] = str(config.path.relative_to(ROOT))
    meta["disease_name"] = config.disease_label
    meta["compartment"] = config.compartment
    meta["role"] = config.role
    meta["group"] = np.where(meta["disease"].eq(config.disease_label), "case", "control")

    return meta.reset_index(drop=True), log2_cpm.reset_index(drop=True), detect_fraction.reset_index(drop=True)


def contrast_config(config: DirectConfig, meta: pd.DataFrame, log2_cpm: pd.DataFrame, detect_fraction: pd.DataFrame) -> pd.DataFrame:
    groups = meta["group"].to_numpy()
    case_mask = groups == "case"
    control_mask = groups == "control"
    rows: list[dict[str, object]] = []
    if case_mask.sum() < MIN_DONORS_PER_GROUP or control_mask.sum() < MIN_DONORS_PER_GROUP:
        return pd.DataFrame()
    for gene in log2_cpm.columns:
        values = log2_cpm[gene].to_numpy(float)
        detect = detect_fraction[gene].to_numpy(float)
        detected_donor_fraction = float(np.mean(detect > 0))
        mean_log2_cpm = float(np.nanmean(values))
        if detected_donor_fraction < MIN_DETECTED_DONOR_FRACTION and mean_log2_cpm < MIN_MEAN_LOG2_CPM:
            continue
        case = values[case_mask]
        control = values[control_mask]
        if len(case) >= 2 and len(control) >= 2:
            t_stat, p_value = stats.ttest_ind(case, control, equal_var=False, nan_policy="omit")
        else:
            t_stat, p_value = np.nan, np.nan
        rows.append(
            {
                "analysis": config.name,
                "dataset_path": str(config.path.relative_to(ROOT)),
                "disease_name": config.disease_label,
                "compartment": config.compartment,
                "role": config.role,
                "gene": gene,
                "n_case_donors": int(case_mask.sum()),
                "n_control_donors": int(control_mask.sum()),
                "mean_case_log2_cpm": float(np.nanmean(case)),
                "mean_control_log2_cpm": float(np.nanmean(control)),
                "delta_log2_cpm": float(np.nanmean(case) - np.nanmean(control)),
                "hedges_g": hedges_g(case, control),
                "welch_t": float(t_stat) if pd.notna(t_stat) else np.nan,
                "p": float(p_value) if pd.notna(p_value) else np.nan,
                "mean_case_detection_fraction": float(np.nanmean(detect[case_mask])),
                "mean_control_detection_fraction": float(np.nanmean(detect[control_mask])),
                "detected_donor_fraction": detected_donor_fraction,
                "mean_log2_cpm": mean_log2_cpm,
                "in_lipid_lysosomal_myeloid_neighborhood": gene in LIPID_LYSOSOMAL_MYEOID_NEIGHBORHOOD,
            }
        )
    out = pd.DataFrame(rows)
    if not out.empty:
        out["fdr"] = multipletests(out["p"].fillna(1.0), method="fdr_bh")[1]
        out["positive_nominal"] = (out["delta_log2_cpm"] >= MIN_ABS_DELTA_FOR_DIRECTION) & (out["p"] < 0.05)
        out["negative_nominal"] = (out["delta_log2_cpm"] <= -MIN_ABS_DELTA_FOR_DIRECTION) & (out["p"] < 0.05)
        out["positive_fdr10"] = (out["delta_log2_cpm"] >= MIN_ABS_DELTA_FOR_DIRECTION) & (out["fdr"] <= 0.10)
        out["negative_fdr10"] = (out["delta_log2_cpm"] <= -MIN_ABS_DELTA_FOR_DIRECTION) & (out["fdr"] <= 0.10)
    return out


def load_ms_signature() -> pd.DataFrame:
    if not MS_SIGNATURE.exists():
        return pd.DataFrame()
    ms = pd.read_csv(MS_SIGNATURE, sep="\t")
    ms["gene"] = ms["gene"].astype(str).str.upper()
    return ms.rename(
        columns={
            "delta_log2": "ms_wm_delta_log2",
            "hedges_g": "ms_wm_hedges_g",
            "p": "ms_wm_p",
            "fdr": "ms_wm_fdr",
        }
    )[["gene", "ms_wm_delta_log2", "ms_wm_hedges_g", "ms_wm_p", "ms_wm_fdr"]]


def load_opentargets_summary() -> pd.DataFrame:
    if not OPENTARGETS.exists():
        return pd.DataFrame()
    ot = pd.read_csv(OPENTARGETS, sep="\t")
    ot = ot.rename(columns={"target": "gene"})
    ot["gene"] = ot["gene"].astype(str).str.upper()
    score_cols = [c for c in ot.columns if c.startswith("datatype_")]
    rows = []
    for gene, sub in ot.groupby("gene", observed=True):
        rows.append(
            {
                "gene": gene,
                "opentargets_disease_count": int(sub["disease"].nunique()),
                "opentargets_diseases": ";".join(sorted(sub["disease"].astype(str).unique())),
                "opentargets_max_overall": float(sub["overall_score"].max()),
                "opentargets_max_genetic_association": float(sub["datatype_genetic_association"].max())
                if "datatype_genetic_association" in sub
                else np.nan,
                "opentargets_max_known_drug_or_clinical": float(sub["datatype_clinical"].max())
                if "datatype_clinical" in sub
                else np.nan,
                "opentargets_channels_present": ";".join(
                    sorted(c for c in score_cols if sub[c].notna().any())
                ),
            }
        )
    return pd.DataFrame(rows)


def load_existing_rank() -> pd.DataFrame:
    if not CENTRAL_FIRST_PASS.exists():
        return pd.DataFrame()
    df = pd.read_csv(CENTRAL_FIRST_PASS, sep="\t")
    if "gene" not in df:
        return pd.DataFrame()
    df["gene"] = df["gene"].astype(str).str.upper()
    keep = [
        c
        for c in [
            "gene",
            "priority_score",
            "weighted_evidence_score",
            "ms_anchor_score",
            "positive_disease_count",
            "negative_disease_count",
            "positive_diseases",
            "negative_diseases",
            "prior_flag",
        ]
        if c in df.columns
    ]
    return df[keep].rename(
        columns={
            "priority_score": "existing_priority_score",
            "weighted_evidence_score": "existing_weighted_evidence_score",
            "ms_anchor_score": "existing_ms_anchor_score",
            "positive_disease_count": "existing_positive_disease_count",
            "negative_disease_count": "existing_negative_disease_count",
            "positive_diseases": "existing_positive_diseases",
            "negative_diseases": "existing_negative_diseases",
            "prior_flag": "existing_prior_flag",
        }
    )


def summarize_contrasts(contrasts: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for gene, sub in contrasts.groupby("gene", observed=True):
        pos = sub.loc[sub["positive_nominal"]]
        neg = sub.loc[sub["negative_nominal"]]
        pos_fdr = sub.loc[sub["positive_fdr10"]]
        neg_fdr = sub.loc[sub["negative_fdr10"]]
        rows.append(
            {
                "gene": gene,
                "tested_compartment_count": int(sub["analysis"].nunique()),
                "positive_compartment_count": int(pos["analysis"].nunique()),
                "negative_compartment_count": int(neg["analysis"].nunique()),
                "positive_fdr10_compartment_count": int(pos_fdr["analysis"].nunique()),
                "negative_fdr10_compartment_count": int(neg_fdr["analysis"].nunique()),
                "positive_disease_count": int(pos["disease_name"].nunique()),
                "negative_disease_count": int(neg["disease_name"].nunique()),
                "positive_diseases": ";".join(sorted(pos["disease_name"].astype(str).unique())),
                "negative_diseases": ";".join(sorted(neg["disease_name"].astype(str).unique())),
                "best_positive_p": float(pos["p"].min()) if not pos.empty else np.nan,
                "best_positive_fdr": float(pos["fdr"].min()) if not pos.empty else np.nan,
                "max_positive_delta_log2_cpm": float(pos["delta_log2_cpm"].max()) if not pos.empty else np.nan,
                "median_positive_hedges_g": float(pos["hedges_g"].median()) if not pos.empty else np.nan,
                "best_negative_p": float(neg["p"].min()) if not neg.empty else np.nan,
                "min_negative_delta_log2_cpm": float(neg["delta_log2_cpm"].min()) if not neg.empty else np.nan,
                "top_positive_compartments": ";".join(
                    (
                        pos.sort_values(["p", "delta_log2_cpm"], ascending=[True, False])
                        .head(8)
                        .apply(lambda r: f"{r['analysis']}:{r['delta_log2_cpm']:.3g},p={r['p']:.2g}", axis=1)
                        .tolist()
                    )
                ),
                "in_lipid_lysosomal_myeloid_neighborhood": gene in LIPID_LYSOSOMAL_MYEOID_NEIGHBORHOOD,
            }
        )
    return pd.DataFrame(rows)


def rank_genes(summary: pd.DataFrame) -> pd.DataFrame:
    ms = load_ms_signature()
    ot = load_opentargets_summary()
    existing = load_existing_rank()
    out = summary.copy()
    if not ms.empty:
        out = out.merge(ms, on="gene", how="left")
    if not ot.empty:
        out = out.merge(ot, on="gene", how="left")
    if not existing.empty:
        out = out.merge(existing, on="gene", how="left")
    for col in [
        "ms_wm_delta_log2",
        "ms_wm_hedges_g",
        "ms_wm_p",
        "opentargets_disease_count",
        "opentargets_max_overall",
        "opentargets_max_genetic_association",
        "existing_priority_score",
        "existing_ms_anchor_score",
    ]:
        if col not in out.columns:
            out[col] = np.nan
    out["ms_positive_nominal"] = (
        (out["ms_wm_delta_log2"].fillna(0) >= MIN_ABS_DELTA_FOR_DIRECTION)
        & (out["ms_wm_p"].fillna(1.0) < 0.05)
    )
    out["ms_positive_trend"] = (
        (out["ms_wm_delta_log2"].fillna(0) >= MIN_ABS_DELTA_FOR_DIRECTION)
        & (out["ms_wm_p"].fillna(1.0) < 0.15)
    )
    out["genetic_or_target_db_breadth"] = out["opentargets_disease_count"].fillna(0)
    out["discovery_priority_score"] = (
        3.0 * out["positive_disease_count"].fillna(0)
        + 1.0 * out["positive_compartment_count"].fillna(0)
        + 2.0 * out["positive_fdr10_compartment_count"].fillna(0)
        - 3.0 * out["negative_disease_count"].fillna(0)
        - 1.0 * out["negative_compartment_count"].fillna(0)
        + 5.0 * out["ms_positive_nominal"].astype(float)
        + 2.0 * out["ms_positive_trend"].astype(float)
        + 1.0 * out["in_lipid_lysosomal_myeloid_neighborhood"].astype(float)
        + 0.5 * out["genetic_or_target_db_breadth"].fillna(0).clip(upper=6)
        + 0.05 * out["existing_priority_score"].fillna(0)
    )
    out = out.sort_values(
        ["discovery_priority_score", "positive_disease_count", "ms_positive_nominal", "best_positive_p"],
        ascending=[False, False, False, True],
    )
    return out


def serializable_config(config: DirectConfig) -> dict[str, object]:
    payload = asdict(config)
    payload["path"] = str(config.path.relative_to(ROOT))
    return payload


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    cache: dict[Path, tuple] = {}
    contrast_tables: list[pd.DataFrame] = []
    run_log: list[dict[str, object]] = []
    for config in CONFIGS:
        try:
            print(f"[broad-discovery] starting {config.name}", flush=True)
            if config.path not in cache:
                a = ad.read_h5ad(config.path)
                x = a.X.tocsr() if sparse.issparse(a.X) else sparse.csr_matrix(a.X)
                cache[config.path] = (a, x)
            a, x = cache[config.path]
            meta, log2_cpm, detect_fraction = aggregate_config(config, a, x)
            contrasts = contrast_config(config, meta, log2_cpm, detect_fraction)
            contrast_tables.append(contrasts)
            run_log.append(
                {
                    "analysis": config.name,
                    "status": "completed",
                    "config": serializable_config(config),
                    "n_donors": int(len(meta)),
                    "n_genes_tested": int(len(contrasts)),
                }
            )
            print(
                f"[broad-discovery] completed {config.name}: "
                f"{len(meta)} donors, {len(contrasts)} genes",
                flush=True,
            )
        except Exception as exc:
            run_log.append(
                {
                    "analysis": config.name,
                    "status": "failed",
                    "config": serializable_config(config),
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )
            print(f"[broad-discovery] failed {config.name}: {type(exc).__name__}: {exc}", flush=True)

    contrasts_all = pd.concat(contrast_tables, ignore_index=True) if contrast_tables else pd.DataFrame()
    contrasts_all.to_csv(OUT / "broad_h5ad_gene_contrasts.tsv", sep="\t", index=False)
    summary = summarize_contrasts(contrasts_all) if not contrasts_all.empty else pd.DataFrame()
    ranked = rank_genes(summary) if not summary.empty else pd.DataFrame()
    summary.to_csv(OUT / "broad_h5ad_gene_summary.tsv", sep="\t", index=False)
    ranked.to_csv(OUT / "broad_h5ad_gene_rank.tsv", sep="\t", index=False)

    neighborhood = ranked.loc[ranked["in_lipid_lysosomal_myeloid_neighborhood"]].head(80) if not ranked.empty else pd.DataFrame()
    ms_positive = ranked.loc[ranked["ms_positive_nominal"]].head(80) if not ranked.empty else pd.DataFrame()
    broad = ranked.head(120) if not ranked.empty else pd.DataFrame()
    neighborhood.to_csv(OUT / "broad_h5ad_lipid_lysosomal_neighborhood_rank.tsv", sep="\t", index=False)
    ms_positive.to_csv(OUT / "broad_h5ad_ms_positive_rank.tsv", sep="\t", index=False)

    summary_json = {
        "random_seed": SEED,
        "run_log": run_log,
        "n_contrasts": int(len(contrasts_all)),
        "n_genes_ranked": int(len(ranked)),
        "ranking_formula": (
            "3*positive_disease_count + positive_compartment_count + "
            "2*positive_fdr10_compartment_count - 3*negative_disease_count - "
            "negative_compartment_count + 5*MS_positive_nominal + 2*MS_positive_trend + "
            "1*lipid_lysosomal_neighborhood + 0.5*OpenTargets disease breadth capped at 6 + "
            "0.05*existing_priority_score"
        ),
        "top_overall": broad.head(30).to_dict(orient="records"),
        "top_lipid_lysosomal_neighborhood": neighborhood.head(30).to_dict(orient="records"),
        "top_ms_positive": ms_positive.head(30).to_dict(orient="records"),
        "guardrail": (
            "This is donor-level pseudobulk discovery across available local h5ad datasets. "
            "It is biased toward the diseases and compartments already downloaded, uses Welch tests "
            "without donor covariates, and should only nominate candidates for stronger follow-up."
        ),
    }
    (OUT / "broad_h5ad_gene_discovery_summary.json").write_text(
        json.dumps(summary_json, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary_json, indent=2))


if __name__ == "__main__":
    main()
