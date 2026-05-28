#!/usr/bin/env python3
"""Geneformer deletion screen for broad residual-gate leaders.

The broad residual gate can identify genes whose expression signal survives
generic module residualization, but it still does not show that perturbing the
gene normalizes disease-cell state. This lightweight Geneformer route tests the
top residual-gate genes with the same token-deletion protocol used in earlier
V3 screens.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "tmp_v3" / "foundation_wave6" / "geneformer_tiny_delete_screen.py"
INPUT = ROOT / "results_v3" / "broad_residual_gate" / "broad_residual_gate_summary.tsv"
OUT = ROOT / "results_v3" / "geneformer_broad_residual_delete"

MAX_GENES = 52
ALWAYS_INCLUDE = [
    "ATOX1",
    "SQLE",
    "TPM4",
    "LDLRAD3",
    "C1QTNF1",
    "HIF1A",
    "CBX3",
    "CFB",
    "TIMP1",
    "ACSL3",
    "C15ORF48",
    "CHI3L1",
    "DAP",
    "FMNL2",
    "SDC4",
    "CTSL",
    "SNX10",
]


def load_wave6_module():
    spec = importlib.util.spec_from_file_location("geneformer_wave6", SOURCE)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {SOURCE}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def select_candidate_genes() -> list[str]:
    summary = pd.read_csv(INPUT, sep="\t")
    genes: list[str] = []

    def add(gene: object) -> None:
        value = str(gene).strip().upper()
        if value and value != "NAN" and value not in genes:
            genes.append(value)

    for gene in ALWAYS_INCLUDE:
        add(gene)
    for _, row in summary.head(40).iterrows():
        add(row["gene"])
    ms_or_lipid = summary.loc[
        (summary["broad_ms_positive_nominal"].fillna(False).astype(bool))
        | (summary["in_lipid_lysosomal_myeloid_neighborhood"].fillna(False).astype(bool))
    ]
    for _, row in ms_or_lipid.head(24).iterrows():
        add(row["gene"])
    return genes[:MAX_GENES]


def zscore_against_random(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    denom = out["random_sd_shift_to_control_cosine"].replace(0, np.nan)
    out["cosine_shift_z_vs_random"] = (
        out["mean_shift_to_control_cosine"] - out["random_mean_shift_to_control_cosine"]
    ) / denom
    out["projection_minus_random"] = out["mean_projection_to_control"] - out["random_mean_projection_to_control"]
    out["candidate_support_flag"] = (
        (out["n_disease_cells_with_token"] >= 3)
        & (out["mean_shift_to_control_cosine"] > out["random_mean_shift_to_control_cosine"])
        & (out["mean_projection_to_control"] > out["random_mean_projection_to_control"])
    )
    out["candidate_strong_support_flag"] = (
        out["candidate_support_flag"]
        & (out["cosine_shift_z_vs_random"] > 0.5)
        & (out["projection_minus_random"] > 0)
    )
    return out


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    candidates = select_candidate_genes()
    gf = load_wave6_module()
    gf.OUT = OUT
    gf.SEED = 20260526
    gf.CANDIDATE_GENES = candidates
    gf.MAX_DISEASE = 30
    gf.MAX_CONTROL = 30
    gf.RANDOM_REPS = 4
    all_genes = tuple(candidates)
    gf.CONTEXTS = [
        gf.Context("IBD_epithelial", "data/raw_v3/cell_state/ibd_human_10x.h5ad", "colon epithelial cell", all_genes),
        gf.Context("IBD_stromal", "data/raw_v3/cell_state/ibd_human_10x.h5ad", "stromal cell of lamina propria of colon", all_genes),
        gf.Context("IBD_myeloid", "data/raw_v3/cell_state/ibd_human_10x.h5ad", "myeloid cell", all_genes),
        gf.Context("psoriasis_keratinocyte", "data/raw_v3/cell_state/psoriasis_skin.h5ad", "keratinocyte_family", all_genes),
        gf.Context("psoriasis_macrophage", "data/raw_v3/cell_state/psoriasis_skin.h5ad", "macrophage", all_genes),
        gf.Context("psoriasis_dendritic", "data/raw_v3/cell_state/psoriasis_skin.h5ad", "dendritic cell, human", all_genes),
        gf.Context("sjogren_acinar", "data/raw_v3/cell_state/sjogren_salivary.h5ad", "acinar cell of salivary gland", all_genes),
        gf.Context("sjogren_duct", "data/raw_v3/cell_state/sjogren_salivary.h5ad", "duct epithelial cell", all_genes),
        gf.Context("sjogren_APC", "data/raw_v3/cell_state/sjogren_salivary.h5ad", "salivary_APC", all_genes),
        gf.Context("t1d_acinar", "data/raw_v3/cell_state/t1d_hpap_islet.h5ad", "pancreatic acinar cell", all_genes),
        gf.Context("t1d_ductal", "data/raw_v3/cell_state/t1d_hpap_islet.h5ad", "pancreatic ductal cell", all_genes),
        gf.Context("t1d_stellate", "data/raw_v3/cell_state/t1d_hpap_islet.h5ad", "pancreatic stellate cell", all_genes),
        gf.Context("t1d_endothelial", "data/raw_v3/cell_state/t1d_hpap_islet.h5ad", "endothelial cell", all_genes),
    ]
    gf.main()

    metrics = pd.read_csv(OUT / "geneformer_tiny_delete_metrics.tsv", sep="\t")
    metrics = zscore_against_random(metrics)
    metrics.to_csv(OUT / "geneformer_broad_residual_delete_metrics.tsv", sep="\t", index=False)
    aggregate = (
        metrics.loc[metrics["n_disease_cells_with_token"] > 0]
        .groupby("gene", observed=True)
        .agg(
            contexts_with_token=("context", "nunique"),
            disease_cells_with_token=("n_disease_cells_with_token", "sum"),
            mean_cosine_shift=("mean_shift_to_control_cosine", "mean"),
            mean_projection_shift=("mean_projection_to_control", "mean"),
            mean_cosine_z_vs_random=("cosine_shift_z_vs_random", "mean"),
            support_contexts=("candidate_support_flag", "sum"),
            strong_support_contexts=("candidate_strong_support_flag", "sum"),
            positive_projection_contexts=("projection_minus_random", lambda s: int((s > 0).sum())),
            negative_projection_contexts=("projection_minus_random", lambda s: int((s < 0).sum())),
        )
        .reset_index()
        .sort_values(
            ["strong_support_contexts", "support_contexts", "positive_projection_contexts", "mean_cosine_z_vs_random"],
            ascending=[False, False, False, False],
        )
    )
    aggregate.to_csv(OUT / "geneformer_broad_residual_gene_summary.tsv", sep="\t", index=False)
    metrics.sort_values(
        ["candidate_support_flag", "cosine_shift_z_vs_random", "projection_minus_random"],
        ascending=[False, False, False],
    ).to_csv(OUT / "geneformer_broad_residual_context_metrics_ranked.tsv", sep="\t", index=False)

    summary = json.loads((OUT / "summary.json").read_text())
    summary["candidate_genes"] = candidates
    summary["posthoc_gene_summary"] = aggregate.to_dict(orient="records")
    summary["posthoc_support_rule"] = (
        "support requires >=3 disease cells with token and both cosine/projection deletion shifts "
        "exceeding random-token deletion means; strong support additionally requires cosine z > 0.5."
    )
    summary["interpretation_guardrail"] = (
        "This is a bounded model triage pass after residualized expression. "
        "It cannot establish causality, genetics, druggability, or novelty."
    )
    (OUT / "geneformer_broad_residual_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    print(aggregate.to_string(index=False))


if __name__ == "__main__":
    main()
