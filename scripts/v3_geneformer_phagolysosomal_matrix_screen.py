#!/usr/bin/env python3
"""Geneformer deletion screen for post-LGALS3 phagolysosomal/matrix candidates.

The LGALS3 residualized analysis demoted galectin-3 as a cross-autoimmune
central node and left a small set of residual survivors: CD44, TYROBP, and
cathepsins, with FABP5/MSR1/SCARB2/GPNMB as conflicted lipid-lysosomal
comparators. This script applies the same lightweight Geneformer V2-104M
named-gene deletion route used for the LTA4H veto to this successor family.

Positive deletion support means the disease-cell embedding moved toward the
matched control centroid after deleting a candidate token. This is a model
hypothesis screen only, not causal perturbation evidence.
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
OUT = ROOT / "results_v3" / "geneformer_phagolysosomal_matrix_delete"

CANDIDATE_GENES = [
    "LGALS3",
    "LGALS1",
    "LGALS9",
    "LGALS3BP",
    "CD44",
    "TYROBP",
    "CTSB",
    "CTSL",
    "CTSD",
    "FABP5",
    "MSR1",
    "SCARB2",
    "GPNMB",
    "SPP1",
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
    return out


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    gf = load_wave6_module()
    gf.OUT = OUT
    gf.SEED = 20260526
    gf.CANDIDATE_GENES = CANDIDATE_GENES
    gf.MAX_DISEASE = 24
    gf.MAX_CONTROL = 24
    gf.RANDOM_REPS = 3
    gf.CONTEXTS = [
        gf.Context(
            "IBD_myeloid",
            "data/raw_v3/cell_state/ibd_human_10x.h5ad",
            "myeloid cell",
            ("LGALS3", "TYROBP", "CTSB", "CTSD", "FABP5", "MSR1", "GPNMB", "SPP1"),
        ),
        gf.Context(
            "IBD_epithelial",
            "data/raw_v3/cell_state/ibd_human_10x.h5ad",
            "colon epithelial cell",
            ("CD44", "CTSB", "CTSL", "LGALS3", "FABP5", "SCARB2", "SPP1"),
        ),
        gf.Context(
            "IBD_stromal",
            "data/raw_v3/cell_state/ibd_human_10x.h5ad",
            "stromal cell of lamina propria of colon",
            ("LGALS3", "LGALS1", "LGALS3BP", "CD44", "CTSD", "SPP1"),
        ),
        gf.Context(
            "psoriasis_keratinocyte",
            "data/raw_v3/cell_state/psoriasis_skin.h5ad",
            "keratinocyte_family",
            ("LGALS3", "CTSB", "CTSL", "FABP5", "CD44", "SPP1", "SCARB2"),
        ),
        gf.Context(
            "psoriasis_stromal",
            "data/raw_v3/cell_state/psoriasis_skin.h5ad",
            "skin fibroblast",
            ("LGALS9", "CTSB", "LGALS3", "CD44", "SPP1"),
        ),
        gf.Context(
            "sjogren_APC",
            "data/raw_v3/cell_state/sjogren_salivary.h5ad",
            "salivary_APC",
            ("TYROBP", "MERTK", "LGALS3", "MSR1", "CTSB", "CTSD", "SPP1"),
        ),
        gf.Context(
            "sjogren_epithelial",
            "data/raw_v3/cell_state/sjogren_salivary.h5ad",
            "duct epithelial cell",
            ("TYROBP", "LGALS3", "CD44", "CTSB", "CTSL", "SCARB2"),
        ),
        gf.Context(
            "t1d_acinar",
            "data/raw_v3/cell_state/t1d_hpap_islet.h5ad",
            "pancreatic acinar cell",
            ("LGALS3", "LGALS1", "GPNMB", "CTSD", "CTSB", "FABP5", "SCARB2"),
        ),
        gf.Context(
            "t1d_ductal",
            "data/raw_v3/cell_state/t1d_hpap_islet.h5ad",
            "pancreatic ductal cell",
            ("LGALS3", "LGALS1", "CD44", "CTSB", "CTSL", "SCARB2", "SPP1"),
        ),
        gf.Context(
            "t1d_stellate",
            "data/raw_v3/cell_state/t1d_hpap_islet.h5ad",
            "pancreatic stellate cell",
            ("LGALS3", "LGALS1", "LGALS9", "CD44", "CTSB", "CTSL", "SPP1"),
        ),
    ]
    gf.main()

    metrics = pd.read_csv(OUT / "geneformer_tiny_delete_metrics.tsv", sep="\t")
    metrics = zscore_against_random(metrics)
    metrics.to_csv(OUT / "geneformer_phagolysosomal_matrix_delete_metrics.tsv", sep="\t", index=False)

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
            positive_projection_contexts=("projection_minus_random", lambda s: int((s > 0).sum())),
        )
        .reset_index()
        .sort_values(["support_contexts", "positive_projection_contexts", "mean_cosine_z_vs_random"], ascending=[False, False, False])
    )
    aggregate.to_csv(OUT / "geneformer_phagolysosomal_matrix_gene_summary.tsv", sep="\t", index=False)
    summary = json.loads((OUT / "summary.json").read_text())
    summary["posthoc_gene_summary"] = aggregate.to_dict(orient="records")
    summary["posthoc_support_rule"] = (
        "candidate_support_flag requires >=3 disease cells with token and both cosine and projection "
        "shift exceeding context random deletion means."
    )
    summary["interpretation_guardrail"] = (
        "This is a small embedding-deletion screen over candidate-enriched cells. "
        "It can veto weak expression-only candidates, but it cannot by itself establish target causality or safety."
    )
    (OUT / "geneformer_phagolysosomal_matrix_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    print(aggregate.to_string(index=False))


if __name__ == "__main__":
    main()
