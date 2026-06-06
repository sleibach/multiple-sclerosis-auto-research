#!/usr/bin/env python3
"""Geneformer embedding-deletion screen for broad-discovery candidates.

This wraps the Wave-6 scratch Geneformer route without duplicating the long
model utility code. It is a lightweight named-gene model-hypothesis screen:
delete a candidate gene token from real disease-cell sequences and measure
whether the embedding moves toward matched normal/control cells.

The output is not causal evidence and must not override real perturbation data.
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
OUT = ROOT / "phases/v3/results" / "geneformer_candidate_delete"

CANDIDATE_GENES = [
    "LTA4H",
    "CHI3L1",
    "C15ORF48",
    "SNX10",
    "CBX3",
    "FMNL2",
    "TNFAIP8L1",
    "HIF1A",
    "TGM2",
    "STAT1",
    "IFITM2",
    "IFITM3",
    "CFB",
    "MMP7",
    "SERPINA1",
    "LIPA",
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
            ("LTA4H", "C15ORF48", "SNX10", "HIF1A", "TGM2", "STAT1", "IFITM2", "IFITM3", "SERPINA1"),
        ),
        gf.Context(
            "IBD_stromal",
            "data/raw_v3/cell_state/ibd_human_10x.h5ad",
            "stromal cell of lamina propria of colon",
            ("CHI3L1", "CBX3", "FMNL2", "TNFAIP8L1", "HIF1A", "TGM2", "CFB", "MMP7"),
        ),
        gf.Context(
            "IBD_epithelial",
            "data/raw_v3/cell_state/ibd_human_10x.h5ad",
            "colon epithelial cell",
            ("CBX3", "FMNL2", "TGM2", "HIF1A", "MMP7", "IFITM2", "IFITM3"),
        ),
        gf.Context(
            "psoriasis_keratinocyte",
            "data/raw_v3/cell_state/psoriasis_skin.h5ad",
            "keratinocyte_family",
            ("CBX3", "IFITM2", "IFITM3", "CFB", "MMP7", "CHI3L1", "TGM2"),
        ),
        gf.Context(
            "t1d_acinar",
            "data/raw_v3/cell_state/t1d_hpap_islet.h5ad",
            "pancreatic acinar cell",
            ("LTA4H", "CBX3", "IFITM2", "IFITM3", "HIF1A", "SERPINA1", "LIPA", "CHI3L1"),
        ),
        gf.Context(
            "t1d_stellate",
            "data/raw_v3/cell_state/t1d_hpap_islet.h5ad",
            "pancreatic stellate cell",
            ("CHI3L1", "SNX10", "C15ORF48", "CBX3", "SERPINA1", "MMP7"),
        ),
        gf.Context(
            "t1d_endothelial",
            "data/raw_v3/cell_state/t1d_hpap_islet.h5ad",
            "endothelial cell",
            ("CHI3L1", "C15ORF48", "SNX10", "MMP7", "SERPINA1", "FMNL2"),
        ),
        gf.Context(
            "sjogren_APC",
            "data/raw_v3/cell_state/sjogren_salivary.h5ad",
            "salivary_APC",
            ("IFITM2", "IFITM3", "STAT1", "C15ORF48", "SNX10"),
        ),
    ]
    gf.main()

    metrics = pd.read_csv(OUT / "geneformer_tiny_delete_metrics.tsv", sep="\t")
    metrics = zscore_against_random(metrics)
    metrics.to_csv(OUT / "geneformer_candidate_delete_metrics.tsv", sep="\t", index=False)

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
        )
        .reset_index()
        .sort_values(["support_contexts", "mean_cosine_z_vs_random"], ascending=[False, False])
    )
    aggregate.to_csv(OUT / "geneformer_candidate_delete_gene_summary.tsv", sep="\t", index=False)
    summary = json.loads((OUT / "summary.json").read_text())
    summary["posthoc_gene_summary"] = aggregate.to_dict(orient="records")
    summary["posthoc_support_rule"] = (
        "candidate_support_flag requires >=3 disease cells with token and both cosine and projection "
        "shift exceeding context random deletion means."
    )
    (OUT / "geneformer_candidate_delete_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    print(aggregate.to_string(index=False))


if __name__ == "__main__":
    main()
