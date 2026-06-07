#!/usr/bin/env python3
"""Rank V35 lysosomal APC coupling against all V26 module-pair dependencies."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DEPS = ROOT / "analysis/v26_deep_structure/workstream_b_module_dependencies.tsv"
OUTDIR = ROOT / "analysis/v35_lysosomal_apc_specificity"


def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    deps = pd.read_csv(DEPS, sep="\t")
    pert = deps[deps["modality"] == "perturbation_mixscale"].copy()
    pert["abs_spearman_r"] = pert["spearman_r"].abs()
    pert = pert.sort_values("abs_spearman_r", ascending=False).reset_index(drop=True)
    pert["rank_abs_spearman_within_perturbation"] = pert.index + 1
    pert.to_csv(OUTDIR / "perturbation_module_pair_rankings.tsv", sep="\t", index=False)

    lys = pert[
        pert["module_a"].eq("gilt_lysosomal_apc") | pert["module_b"].eq("gilt_lysosomal_apc")
    ].copy()
    lys.to_csv(OUTDIR / "lysosomal_pair_rankings.tsv", sep="\t", index=False)
    top = lys.sort_values("abs_spearman_r", ascending=False).iloc[0].to_dict()

    replicated_supported = deps[
        (deps["module_a"].eq(top["module_a"]))
        & (deps["module_b"].eq(top["module_b"]))
        & (deps["claim_grade"].eq("supported"))
    ]
    summary = {
        "hypothesis": "lysosomal APC coupling specificity",
        "grounded_result": "strong_within_mixscale_not_cross_modality_supported",
        "top_lysosomal_pair": top,
        "n_perturbation_pairs": int(len(pert)),
        "n_lysosomal_pairs": int(len(lys)),
        "top_pair_supported_elsewhere": bool(len(replicated_supported) > 0),
        "interpretation": (
            "The GILT/lysosomal APC to IFN/APC pair is the strongest perturbation-module "
            "correlation among tested pairs, but V26 did not grade lysosomal pairs as "
            "supported because replication across independent modalities was insufficient. "
            "It remains a coupled transcript-state observation, not a proven antigen-processing bottleneck."
        ),
    }
    (OUTDIR / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
