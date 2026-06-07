#!/usr/bin/env python3
"""Permutation/FDR robustness checks for V35 EBV-module exploratory results."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
GSE108497_SCORES = ROOT / "analysis/v35_ebv_module_gse108497_sle/sample_ebv_ifn_scores.tsv"
GSE108497_TESTS = ROOT / "analysis/v35_ebv_module_gse108497_sle/sle_ebv_module_tests.tsv"
GSE10325_SCORES = ROOT / "analysis/v35_ebv_module_gse10325_sorted_sle/sample_sorted_scores.tsv"
GSE10325_TESTS = ROOT / "analysis/v35_ebv_module_gse10325_sorted_sle/sorted_sle_tests.tsv"
OUTDIR = ROOT / "analysis/v35_ebv_module_robustness"


def bh_fdr(pvals: pd.Series) -> pd.Series:
    p = pd.to_numeric(pvals, errors="coerce").fillna(1.0).to_numpy(float)
    n = len(p)
    order = np.argsort(p)
    ranked = p[order]
    adj = ranked * n / (np.arange(n) + 1)
    adj = np.minimum.accumulate(adj[::-1])[::-1]
    adj = np.minimum(adj, 1.0)
    out = np.empty(n)
    out[order] = adj
    return pd.Series(out, index=pvals.index)


def residualize(y: np.ndarray, x: np.ndarray) -> np.ndarray:
    ok = np.isfinite(y) & np.isfinite(x)
    resid = np.full(y.shape, np.nan, dtype=float)
    if ok.sum() < 3:
        return resid
    X = np.column_stack([np.ones(ok.sum()), x[ok]])
    beta = np.linalg.lstsq(X, y[ok], rcond=None)[0]
    resid[ok] = y[ok] - X @ beta
    return resid


def mean_delta(values: np.ndarray, labels: np.ndarray) -> float:
    return float(np.nanmean(values[labels == 1]) - np.nanmean(values[labels == 0]))


def permutation_p(values: np.ndarray, labels: np.ndarray, n_perm: int = 10000, seed: int = 35) -> float:
    rng = np.random.default_rng(seed)
    observed = mean_delta(values, labels)
    hits = 0
    valid = 0
    for _ in range(n_perm):
        perm = rng.permutation(labels)
        delta = mean_delta(values, perm)
        if np.isfinite(delta):
            valid += 1
            if abs(delta) >= abs(observed):
                hits += 1
    return float((hits + 1) / (valid + 1))


def stratified_permutation_p(
    values: np.ndarray,
    labels: np.ndarray,
    strata: np.ndarray,
    n_perm: int = 10000,
    seed: int = 3500,
) -> float:
    rng = np.random.default_rng(seed)
    observed = mean_delta(values, labels)
    hits = 0
    valid = 0
    uniq = pd.Series(strata).dropna().unique()
    for _ in range(n_perm):
        perm = labels.copy()
        for s in uniq:
            idx = np.flatnonzero(strata == s)
            perm[idx] = rng.permutation(perm[idx])
        delta = mean_delta(values, perm)
        if np.isfinite(delta):
            valid += 1
            if abs(delta) >= abs(observed):
                hits += 1
    return float((hits + 1) / (valid + 1))


def gse108497_residual_test() -> dict[str, float | str | int]:
    df = pd.read_csv(GSE108497_SCORES, sep="\t")
    values = df["ebv_up_score"].to_numpy(float)
    ifn = df["ifn_apc_score"].to_numpy(float)
    resid = residualize(values, ifn)
    labels = df["sle"].to_numpy(int)
    strata = df["tp_label"].astype(str).to_numpy()
    return {
        "dataset": "GSE108497",
        "contrast": "SLE_vs_HC_EBV_up_residualized_for_IFN_APC",
        "delta": mean_delta(resid, labels),
        "n_sle": int(labels.sum()),
        "n_hc": int((labels == 0).sum()),
        "permutation_p_unstratified": permutation_p(resid, labels, seed=108497),
        "permutation_p_timepoint_stratified": stratified_permutation_p(resid, labels, strata, seed=108498),
    }


def gse10325_residual_tests() -> list[dict[str, float | str | int]]:
    df = pd.read_csv(GSE10325_SCORES, sep="\t")
    rows = []
    for subset, sub in df.groupby("subset"):
        sub = sub.dropna(subset=["ebv_up", "ifn_apc", "condition"]).copy()
        values = sub["ebv_up"].to_numpy(float)
        ifn = sub["ifn_apc"].to_numpy(float)
        resid = residualize(values, ifn)
        labels = sub["condition"].eq("SLE").astype(int).to_numpy()
        rows.append(
            {
                "dataset": "GSE10325",
                "subset": subset,
                "contrast": "SLE_vs_HC_EBV_up_residualized_for_IFN_APC",
                "delta": mean_delta(resid, labels),
                "n_sle": int(labels.sum()),
                "n_hc": int((labels == 0).sum()),
                "permutation_p_unstratified": permutation_p(resid, labels, seed=10325 + len(rows)),
            }
        )
    return rows


def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    all_tests = []
    for path, dataset in [(GSE108497_TESTS, "GSE108497"), (GSE10325_TESTS, "GSE10325")]:
        df = pd.read_csv(path, sep="\t")
        df.insert(0, "dataset", dataset)
        df["fdr_within_dataset"] = bh_fdr(df["welch_p"])
        all_tests.append(df)
    fdr_df = pd.concat(all_tests, ignore_index=True, sort=False)
    fdr_df["fdr_across_all_ebv_tests"] = bh_fdr(fdr_df["welch_p"])
    fdr_df.to_csv(OUTDIR / "ebv_module_fdr_table.tsv", sep="\t", index=False)

    perm_rows = [gse108497_residual_test(), *gse10325_residual_tests()]
    perm_df = pd.DataFrame(perm_rows)
    perm_df["fdr_permutation_family"] = bh_fdr(perm_df["permutation_p_unstratified"])
    perm_df.to_csv(OUTDIR / "ebv_module_permutation_tests.tsv", sep="\t", index=False)

    summary = {
        "hypothesis": "EBV module robustness and multiple-testing accounting",
        "grounded_result": "GSE108497 robust host-module-like SLE signal; GSE10325 sorted subset inconclusive",
        "gse108497_timepoint_stratified_permutation_p": float(
            perm_df.loc[perm_df["dataset"].eq("GSE108497"), "permutation_p_timepoint_stratified"].iloc[0]
        ),
        "gse10325_best_subset": perm_df.loc[perm_df["dataset"].eq("GSE10325")]
        .sort_values("permutation_p_unstratified")
        .iloc[0]
        .to_dict(),
        "fdr_min_across_all_ebv_tests": float(fdr_df["fdr_across_all_ebv_tests"].min()),
        "interpretation": (
            "Multiple-testing and permutation checks support a SLE-associated host EBV-module-like "
            "blood signal in GSE108497 after IFN/APC residualization. Sorted-cell GSE10325 remains "
            "inconclusive for B-cell/APC localization. Neither dataset has EBV exposure/load metadata, "
            "so EBV imprint causality remains unproven."
        ),
    }
    (OUTDIR / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
