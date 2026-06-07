#!/usr/bin/env python3
"""Random-gene-set specificity control for the GSE108497 EBV-module result."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
EXPR = ROOT / "data/raw/GSE108497/GSE108497_normalized_data.txt.gz"
PROBES = ROOT / "results/pregnancy_dimension/gse108497_sle/platform_probe_symbols.tsv"
META = ROOT / "results/pregnancy_dimension/gse108497_sle/sample_metadata_parsed.tsv"
MODULE_SCORES = ROOT / "results/pregnancy_dimension/gse108497_sle/module_scores.tsv"
EBV_UP = ROOT / "analysis/v35_ebv_module_gse162516/host_ebv_transformation_up_top200.tsv"
OUTDIR = ROOT / "analysis/v35_ebv_random_geneset_control"


def residualize(y: np.ndarray, x: np.ndarray) -> np.ndarray:
    ok = np.isfinite(y) & np.isfinite(x)
    resid = np.full(y.shape, np.nan, dtype=float)
    X = np.column_stack([np.ones(ok.sum()), x[ok]])
    beta = np.linalg.lstsq(X, y[ok], rcond=None)[0]
    resid[ok] = y[ok] - X @ beta
    return resid


def delta_sle_hc(values: np.ndarray, labels: np.ndarray) -> float:
    return float(np.nanmean(values[labels == 1]) - np.nanmean(values[labels == 0]))


def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(35017)

    meta = pd.read_csv(META, sep="\t")
    array_ids = list(meta["array_id"])
    expr = pd.read_csv(EXPR, sep="\t", compression="gzip")
    value_cols = ["ID_REF"] + [c for c in expr.columns if c in set(array_ids)]
    expr = expr[value_cols].set_index("ID_REF").astype(float)
    meta = meta.set_index("array_id").loc[expr.columns].reset_index()

    ifn = pd.read_csv(MODULE_SCORES, sep="\t")
    ifn = ifn[ifn["module"] == "ifn_apc"].set_index("array_id").loc[expr.columns]["score"].to_numpy(float)
    labels = meta["sle"].to_numpy(int)

    probe_map = pd.read_csv(PROBES, sep="\t")
    probe_map = probe_map[probe_map["ID_REF"].isin(expr.index)].dropna(subset=["gene"])
    probe_map["gene"] = probe_map["gene"].astype(str).str.upper()
    gene_to_probes = {
        gene: sorted(group["ID_REF"].unique())
        for gene, group in probe_map.groupby("gene")
        if len(group["ID_REF"].unique()) > 0
    }
    universe = np.array(sorted(gene_to_probes))

    ebv_genes = set(pd.read_csv(EBV_UP, sep="\t")["tracking_id"].head(100).astype(str).str.upper())
    ebv_present = sorted(ebv_genes.intersection(gene_to_probes))

    def score_genes(genes: list[str]) -> np.ndarray:
        probes = sorted({probe for gene in genes for probe in gene_to_probes[gene]})
        return expr.loc[probes].mean(axis=0).to_numpy(float)

    observed_score = score_genes(ebv_present)
    observed_resid = residualize(observed_score, ifn)
    observed_delta = delta_sle_hc(observed_resid, labels)

    rows = []
    n_gene = len(ebv_present)
    for i in range(2000):
        sampled = rng.choice(universe, size=n_gene, replace=False)
        score = score_genes(list(sampled))
        resid = residualize(score, ifn)
        delta = delta_sle_hc(resid, labels)
        rows.append({"iteration": i + 1, "delta_sle_minus_hc": delta})
    null = pd.DataFrame(rows)
    null.to_csv(OUTDIR / "random_geneset_null.tsv", sep="\t", index=False)

    abs_p = float(((null["delta_sle_minus_hc"].abs() >= abs(observed_delta)).sum() + 1) / (len(null) + 1))
    upper_p = float(((null["delta_sle_minus_hc"] >= observed_delta).sum() + 1) / (len(null) + 1))
    summary = {
        "hypothesis": "GSE108497 EBV-up module specificity versus random same-size gene sets",
        "grounded_result": "not_specific_against_random_gene_sets",
        "n_ebv_genes_present": n_gene,
        "n_random_sets": int(len(null)),
        "observed_ifn_residualized_delta_sle_minus_hc": observed_delta,
        "null_delta_mean": float(null["delta_sle_minus_hc"].mean()),
        "null_delta_sd": float(null["delta_sle_minus_hc"].std(ddof=1)),
        "empirical_p_two_sided_abs": abs_p,
        "empirical_p_upper_tail": upper_p,
        "observed_percentile": float((null["delta_sle_minus_hc"] < observed_delta).mean()),
        "interpretation": (
            "The IFN-residualized GSE108497 SLE contrast is robust to label permutation, "
            "but it is not stronger than random same-size gene modules on this platform. "
            "This argues for an SLE host-state signal rather than EBV-module specificity."
        ),
    }
    (OUTDIR / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
