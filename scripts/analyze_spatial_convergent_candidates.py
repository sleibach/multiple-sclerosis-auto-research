#!/usr/bin/env python3
"""Spatially test convergent MIMS2/proteome candidates measured in GSE284005."""

from __future__ import annotations

import json

import pandas as pd

import analyze_spatial_targets as spatial


TARGETS = ["ACSL1", "NAMPT", "CTSD", "GPNMB", "LAMP1"]


def main() -> int:
    spatial.TARGETS = TARGETS
    cells = spatial.load_cells()
    pseudobulks, counts = spatial.build_pseudobulks(cells)
    contrasts, statistics = spatial.paired_donor_contrasts(pseudobulks)
    statistics["candidate_spatial_support"] = (
        (statistics["mean_delta_log10k"] > 0)
        & (statistics["positive_direction_fraction"] >= (2 / 3))
        & (statistics["paired_dz"] >= 0.5)
        & (statistics["wilcoxon_p"] < 0.05)
    )
    out = spatial.OUT
    pseudobulks.to_csv(out / "spatial_convergent_candidate_pseudobulks.tsv", sep="\t", index=False)
    contrasts.to_csv(out / "spatial_convergent_candidate_contrasts.tsv", sep="\t", index=False)
    statistics.to_csv(out / "spatial_convergent_candidate_statistics.tsv", sep="\t", index=False)

    summary = {
        "random_seed": spatial.SEED,
        "data_accession": "GSE284005",
        "targets": TARGETS,
        "cells_loaded": int(len(cells)),
        "dmwm_myeloid_cells": int(counts["n_dmwm_myeloid"].sum()),
        "analytical_unit": "donor-level mean of eligible specimen pseudobulk contrasts",
        "min_cells_per_pseudobulk": spatial.MIN_CELLS,
        "t_neighborhood": f"union of {spatial.NEIGHBOR_K} nearest non-self neighbors of author-labelled T cells",
        "candidate_spatial_support_genes": sorted(
            statistics.loc[statistics["candidate_spatial_support"], "gene"].unique().tolist()
        ),
    }
    (out / "spatial_convergent_candidate_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))

    print(pd.DataFrame(statistics).to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
