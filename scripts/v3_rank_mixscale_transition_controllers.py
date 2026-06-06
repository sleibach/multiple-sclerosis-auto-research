#!/usr/bin/env python3
"""Rank Mixscale perturbations by suppression of the V3 transition readouts."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "phases/v3/results" / "mixscale"

MODULE_WEIGHTS = {
    "ifn_apc": 1.0,
    "hla_ii_apc": 1.2,
    "mif_cd74_receptor_state": 1.0,
    "gilt_lysosomal_apc": 0.6,
}


def main() -> None:
    path = OUT / "mixscale_module_summary.tsv"
    modules = pd.read_csv(path, sep="\t")
    modules = modules[modules["module"].isin(MODULE_WEIGHTS)].copy()
    modules["module_weight"] = modules["module"].map(MODULE_WEIGHTS)
    modules["negative_magnitude"] = modules["mean_module_log2fc_across_cell_types"].map(lambda x: max(0.0, -float(x)))
    modules["coverage_factor"] = np.minimum(1.0, modules["mean_genes_present"].fillna(0.0) / 5.0)
    modules["suppression_component"] = (
        modules["negative_magnitude"]
        * modules["cell_type_negative_fraction"].fillna(0.0)
        * modules["module_weight"]
        * modules["coverage_factor"]
    )

    rows: list[dict[str, object]] = []
    for (pathway, perturbation), sub in modules.groupby(["pathway", "perturbation"]):
        wide = {
            f"{row.module}_mean_log2fc": row.mean_module_log2fc_across_cell_types
            for row in sub.itertuples()
        }
        rows.append(
            {
                "pathway": pathway,
                "perturbation": perturbation,
                "transition_suppression_score": float(sub["suppression_component"].sum()),
                "n_modules_with_data": int(sub["mean_module_log2fc_across_cell_types"].notna().sum()),
                "n_modules_suppressed": int(
                    ((sub["mean_module_log2fc_across_cell_types"] < 0) & (sub["cell_type_negative_fraction"] >= 0.5)).sum()
                ),
                "mean_cell_type_negative_fraction": float(sub["cell_type_negative_fraction"].mean()),
                "total_sig_negative_gene_celltype": int(sub["total_sig_negative_gene_celltype"].sum()),
                "total_sig_positive_gene_celltype": int(sub["total_sig_positive_gene_celltype"].sum()),
                **wide,
            }
        )
    rank = pd.DataFrame(rows).sort_values(
        ["transition_suppression_score", "n_modules_suppressed", "total_sig_negative_gene_celltype"],
        ascending=False,
    )
    rank.to_csv(OUT / "mixscale_transition_controller_rank.tsv", sep="\t", index=False)
    summary = {
        "input": str(path.relative_to(ROOT)),
        "module_weights": MODULE_WEIGHTS,
        "scoring": (
            "For each cytokine-pathway perturbation, sum max(0,-mean module log2FC) times "
            "cell-type negative fraction, module weight, and a gene-coverage cap. This ranks "
            "wiring controllers, not drug targets."
        ),
        "top_controllers": rank.head(15).to_dict(orient="records"),
        "guardrail": (
            "Mixscale perturbations are in stimulated human cancer cell lines. A controller that "
            "moves the transition readout still requires disease-cell validation and prior-art review."
        ),
    }
    (OUT / "mixscale_transition_controller_rank_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
