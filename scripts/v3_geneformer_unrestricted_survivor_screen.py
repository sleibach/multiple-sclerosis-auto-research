#!/usr/bin/env python3
"""Geneformer deletion screen for unrestricted post-APOC1 survivors.

After APOC1 failed the pivot-panel Geneformer screen, the full broad h5ad table
was reopened. This script tests the top MS-positive, cross-disease survivors
that are not already demoted by prior-art/model checks.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "phases/v3/tmp" / "foundation_wave6" / "geneformer_tiny_delete_screen.py"
OUT = ROOT / "phases/v3/results" / "geneformer_unrestricted_survivor_delete"

CANDIDATE_GENES = [
    "FMNL2",
    "TNFAIP8L1",
    "C15ORF48",
    "NCK1",
    "SNX10",
    "PPIL3",
    "SEL1L3",
    "PLEK2",
    "DAP",
    "AQR",
    "LIMS1",
    "ABHD2",
    "SDC4",
    "BIRC3",
    "STARD10",
    "MMADHC",
    "TRIQK",
    "DCLRE1B",
    "MYO1E",
    "IL2RG",
    "PPP3CA",
    "CXCL9",
]


def load_wave6_module():
    spec = importlib.util.spec_from_file_location("geneformer_wave6", SOURCE)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {SOURCE}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


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
    gf = load_wave6_module()
    gf.OUT = OUT
    gf.SEED = 20260526
    gf.CANDIDATE_GENES = CANDIDATE_GENES
    gf.MAX_DISEASE = 30
    gf.MAX_CONTROL = 30
    gf.RANDOM_REPS = 4
    all_genes = tuple(CANDIDATE_GENES)
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
    metrics.to_csv(OUT / "geneformer_unrestricted_survivor_delete_metrics.tsv", sep="\t", index=False)
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
    aggregate.to_csv(OUT / "geneformer_unrestricted_survivor_gene_summary.tsv", sep="\t", index=False)
    metrics.sort_values(
        ["candidate_support_flag", "cosine_shift_z_vs_random", "projection_minus_random"],
        ascending=[False, False, False],
    ).to_csv(OUT / "geneformer_unrestricted_survivor_context_metrics_ranked.tsv", sep="\t", index=False)
    summary = json.loads((OUT / "summary.json").read_text())
    summary["candidate_genes"] = CANDIDATE_GENES
    summary["posthoc_gene_summary"] = aggregate.to_dict(orient="records")
    summary["posthoc_support_rule"] = (
        "support requires >=3 disease cells with token and both cosine/projection deletion shifts "
        "exceeding random-token deletion means; strong support additionally requires cosine z > 0.5."
    )
    summary["interpretation_guardrail"] = (
        "This is a second-pass foundation-model screen after APOC1 failed. "
        "It can prioritize mechanisms but cannot establish target causality."
    )
    (OUT / "geneformer_unrestricted_survivor_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    print(aggregate.to_string(index=False))


if __name__ == "__main__":
    main()
