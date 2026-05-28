#!/usr/bin/env python3
"""Geneformer deletion screen for the post-triage pivot panel.

`v3_pivot_panel_triage.py` routes APOC1 to foundation-model testing because it
has a local MS white-matter anchor plus direct non-MS breadth, while most other
post-hour-4 pivots fail either breadth, MS anchoring, model support, or target
plausibility. This script tests APOC1 against those comparators using the same
bounded Geneformer V2-104M token-deletion route used earlier in V3.

Positive support means deleting a candidate token moves disease-cell embeddings
toward the matched control centroid more than matched random token deletions.
This is a lightweight in-silico perturbation screen only; it is not wet-lab
validation, full InSilicoPerturber output, or causal proof.
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
OUT = ROOT / "results_v3" / "geneformer_pivot_panel_delete"

CANDIDATE_GENES = [
    "APOC1",
    "APOE",
    "LPL",
    "PLIN2",
    "ACSL3",
    "LAMP3",
    "CTSL",
    "CTSB",
    "CD44",
    "CHI3L1",
    "CD300E",
    "CD300LF",
    "LGALS8",
    "UGCG",
    "GBA2",
    "GPNMB",
    "FABP5",
    "MSR1",
    "SCARB2",
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
    gf.CONTEXTS = [
        gf.Context(
            "IBD_epithelial",
            "data/raw_v3/cell_state/ibd_human_10x.h5ad",
            "colon epithelial cell",
            ("APOC1", "APOE", "LPL", "ACSL3", "LAMP3", "CTSL", "CTSB", "CD44", "FABP5", "SCARB2"),
        ),
        gf.Context(
            "IBD_stromal",
            "data/raw_v3/cell_state/ibd_human_10x.h5ad",
            "stromal cell of lamina propria of colon",
            ("APOC1", "APOE", "LPL", "ACSL3", "LAMP3", "CTSL", "CTSB", "CD44", "CHI3L1", "GPNMB"),
        ),
        gf.Context(
            "IBD_myeloid",
            "data/raw_v3/cell_state/ibd_human_10x.h5ad",
            "myeloid cell",
            ("APOC1", "APOE", "LPL", "LAMP3", "CTSL", "CTSB", "CD300E", "GPNMB", "FABP5", "MSR1"),
        ),
        gf.Context(
            "psoriasis_keratinocyte",
            "data/raw_v3/cell_state/psoriasis_skin.h5ad",
            "keratinocyte_family",
            ("APOC1", "APOE", "LPL", "CTSL", "CTSB", "CHI3L1", "CD44", "FABP5", "SCARB2"),
        ),
        gf.Context(
            "psoriasis_macrophage",
            "data/raw_v3/cell_state/psoriasis_skin.h5ad",
            "macrophage",
            ("APOC1", "APOE", "LPL", "CD300E", "CD300LF", "CTSL", "CTSB", "GPNMB", "MSR1"),
        ),
        gf.Context(
            "psoriasis_dendritic",
            "data/raw_v3/cell_state/psoriasis_skin.h5ad",
            "dendritic cell, human",
            ("APOC1", "APOE", "LPL", "CD300E", "CD300LF", "LAMP3", "CTSL", "CTSB", "GPNMB"),
        ),
        gf.Context(
            "sjogren_acinar",
            "data/raw_v3/cell_state/sjogren_salivary.h5ad",
            "acinar cell of salivary gland",
            ("APOC1", "APOE", "LPL", "ACSL3", "UGCG", "GBA2", "CTSL", "CTSB", "GPNMB"),
        ),
        gf.Context(
            "sjogren_duct",
            "data/raw_v3/cell_state/sjogren_salivary.h5ad",
            "duct epithelial cell",
            ("APOC1", "APOE", "LPL", "ACSL3", "UGCG", "GBA2", "CTSL", "CTSB", "CD44", "SCARB2"),
        ),
        gf.Context(
            "sjogren_APC",
            "data/raw_v3/cell_state/sjogren_salivary.h5ad",
            "salivary_APC",
            ("APOC1", "APOE", "LPL", "CD300E", "CD300LF", "CTSL", "CTSB", "GPNMB", "MSR1"),
        ),
        gf.Context(
            "t1d_acinar",
            "data/raw_v3/cell_state/t1d_hpap_islet.h5ad",
            "pancreatic acinar cell",
            ("APOC1", "APOE", "LPL", "ACSL3", "UGCG", "GBA2", "CTSL", "CTSB", "GPNMB", "FABP5"),
        ),
        gf.Context(
            "t1d_ductal",
            "data/raw_v3/cell_state/t1d_hpap_islet.h5ad",
            "pancreatic ductal cell",
            ("APOC1", "APOE", "LPL", "ACSL3", "UGCG", "GBA2", "CTSL", "CTSB", "CD44", "SCARB2"),
        ),
        gf.Context(
            "t1d_stellate",
            "data/raw_v3/cell_state/t1d_hpap_islet.h5ad",
            "pancreatic stellate cell",
            ("APOC1", "APOE", "LPL", "ACSL3", "UGCG", "GBA2", "CTSL", "CTSB", "CD44", "CHI3L1"),
        ),
        gf.Context(
            "t1d_endothelial",
            "data/raw_v3/cell_state/t1d_hpap_islet.h5ad",
            "endothelial cell",
            ("APOC1", "APOE", "LPL", "ACSL3", "UGCG", "GBA2", "LAMP3", "CHI3L1"),
        ),
    ]
    gf.main()

    metrics = pd.read_csv(OUT / "geneformer_tiny_delete_metrics.tsv", sep="\t")
    metrics = zscore_against_random(metrics)
    metrics.to_csv(OUT / "geneformer_pivot_panel_delete_metrics.tsv", sep="\t", index=False)

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
    aggregate.to_csv(OUT / "geneformer_pivot_panel_gene_summary.tsv", sep="\t", index=False)
    context_gene = metrics.sort_values(
        ["candidate_support_flag", "cosine_shift_z_vs_random", "projection_minus_random"],
        ascending=[False, False, False],
    )
    context_gene.to_csv(OUT / "geneformer_pivot_panel_context_metrics_ranked.tsv", sep="\t", index=False)
    summary = json.loads((OUT / "summary.json").read_text())
    summary["candidate_genes"] = CANDIDATE_GENES
    summary["posthoc_gene_summary"] = aggregate.to_dict(orient="records")
    summary["posthoc_support_rule"] = (
        "support requires >=3 disease cells with token and both cosine/projection deletion shifts "
        "exceeding random-token deletion means; strong support additionally requires cosine z > 0.5."
    )
    summary["interpretation_guardrail"] = (
        "APOC1 advances only if this model screen supports normalization and later genetics/prior-art gates do not veto. "
        "Small embedding shifts are not causal proof."
    )
    (OUT / "geneformer_pivot_panel_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    print(aggregate.to_string(index=False))


if __name__ == "__main__":
    main()
