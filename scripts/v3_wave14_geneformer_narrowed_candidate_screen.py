#!/usr/bin/env python3
"""Focused Geneformer deletion screen for narrowed V3 candidates.

This fills a concrete gap: the existing Geneformer screens did not include the
hour-6 narrowed candidates (`SLC15A4/TASL/IRF5`, `GSK3B`, `CIITA/RFX5`, and
genetic anchors). It reuses the same bounded V2-104M token-deletion machinery
from wave 6.

Interpretation guardrail: a positive shift means the candidate-token deletion
moved selected disease-cell embeddings toward the matched control centroid more
than random-token deletion in that local context. It is a foundation-model
hypothesis screen, not causal perturbation evidence or expression log2FC.
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
OUT = ROOT / "results_v3" / "wave14_geneformer_narrowed_candidate_delete"

CANDIDATE_GENES = [
    "SLC15A4",
    "TASL",
    "IRF5",
    "TLR7",
    "TLR8",
    "TLR9",
    "UNC93B1",
    "PTPN2",
    "TNFAIP3",
    "CLEC16A",
    "SH2B3",
    "GPR65",
    "GSK3B",
    "CIITA",
    "RFX5",
    "CD74",
    "CTSS",
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
    gf.MAX_DISEASE = 24
    gf.MAX_CONTROL = 24
    gf.RANDOM_REPS = 3
    gf.CONTEXTS = [
        gf.Context(
            "IBD_myeloid",
            "data/raw_v3/cell_state/ibd_human_10x.h5ad",
            "myeloid cell",
            tuple(CANDIDATE_GENES),
        ),
        gf.Context(
            "IBD_epithelial",
            "data/raw_v3/cell_state/ibd_human_10x.h5ad",
            "colon epithelial cell",
            tuple(CANDIDATE_GENES),
        ),
        gf.Context(
            "psoriasis_macrophage",
            "data/raw_v3/cell_state/psoriasis_skin.h5ad",
            "macrophage",
            tuple(CANDIDATE_GENES),
        ),
        gf.Context(
            "psoriasis_dendritic",
            "data/raw_v3/cell_state/psoriasis_skin.h5ad",
            "dendritic cell, human",
            tuple(CANDIDATE_GENES),
        ),
        gf.Context(
            "sjogren_APC",
            "data/raw_v3/cell_state/sjogren_salivary.h5ad",
            "salivary_APC",
            tuple(CANDIDATE_GENES),
        ),
        gf.Context(
            "t1d_ductal",
            "data/raw_v3/cell_state/t1d_hpap_islet.h5ad",
            "pancreatic ductal cell",
            tuple(CANDIDATE_GENES),
        ),
        gf.Context(
            "t1d_acinar",
            "data/raw_v3/cell_state/t1d_hpap_islet.h5ad",
            "pancreatic acinar cell",
            tuple(CANDIDATE_GENES),
        ),
        gf.Context(
            "ra_classical_monocyte",
            "data/raw_v3/cell_state/ra_binvignat_blood.h5ad",
            "classical monocyte",
            tuple(CANDIDATE_GENES),
        ),
        gf.Context(
            "ra_nonclassical_monocyte",
            "data/raw_v3/cell_state/ra_binvignat_blood.h5ad",
            "non-classical monocyte",
            tuple(CANDIDATE_GENES),
        ),
        gf.Context(
            "ra_myeloid_dendritic",
            "data/raw_v3/cell_state/ra_binvignat_blood.h5ad",
            "myeloid dendritic cell",
            tuple(CANDIDATE_GENES),
        ),
    ]
    gf.main()

    metrics = pd.read_csv(OUT / "geneformer_tiny_delete_metrics.tsv", sep="\t")
    metrics = zscore_against_random(metrics)
    metrics.to_csv(OUT / "wave14_geneformer_narrowed_candidate_delete_metrics.tsv", sep="\t", index=False)

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
    aggregate.to_csv(OUT / "wave14_geneformer_narrowed_candidate_gene_summary.tsv", sep="\t", index=False)

    context_gene = metrics.sort_values(
        ["candidate_support_flag", "cosine_shift_z_vs_random", "projection_minus_random"],
        ascending=[False, False, False],
    )
    context_gene.to_csv(OUT / "wave14_geneformer_narrowed_candidate_context_metrics_ranked.tsv", sep="\t", index=False)

    summary = json.loads((OUT / "summary.json").read_text())
    summary["candidate_genes"] = CANDIDATE_GENES
    summary["posthoc_gene_summary"] = aggregate.to_dict(orient="records")
    summary["posthoc_support_rule"] = (
        "support requires >=3 disease cells with token and both cosine/projection deletion shifts "
        "exceeding random-token deletion means; strong support additionally requires cosine z > 0.5."
    )
    summary["interpretation_guardrail"] = (
        "This screen tests whether deleting narrowed candidate tokens makes selected disease cells look "
        "more control-like in Geneformer embedding space. It is a model-triage channel only."
    )
    (OUT / "wave14_geneformer_narrowed_candidate_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    print(aggregate.to_string(index=False))


if __name__ == "__main__":
    main()
