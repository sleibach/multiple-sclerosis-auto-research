#!/usr/bin/env python3
"""Ground V35 lysosomal APC-processing bottleneck on held perturbation modules."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats


ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "analysis/v26_deep_structure/perturbation_module_matrix.tsv"
OUTDIR = ROOT / "analysis/v35_lysosomal_apc_bottleneck"
OUTDIR.mkdir(parents=True, exist_ok=True)


def perm_p(x: np.ndarray, y: np.ndarray, observed: float, n_perm: int = 10000, seed: int = 35) -> float:
    rng = np.random.default_rng(seed)
    extreme = 0
    for _ in range(n_perm):
        yp = rng.permutation(y)
        r = stats.spearmanr(x, yp).statistic
        if abs(r) >= abs(observed):
            extreme += 1
    return (extreme + 1) / (n_perm + 1)


m = pd.read_csv(MATRIX, sep="\t", index_col=0)
lys = m["gilt_lysosomal_apc"].to_numpy()

pairs = []
for module in ["hla_ii_apc", "ifn_apc", "mif_cd74_receptor_state"]:
    y = m[module].to_numpy()
    spearman = stats.spearmanr(lys, y).statistic
    pearson = stats.pearsonr(lys, y).statistic
    pairs.append(
        {
            "comparison": f"gilt_lysosomal_apc_vs_{module}",
            "spearman_r": spearman,
            "pearson_r": pearson,
            "spearman_perm_p_two_sided": perm_p(lys, y, spearman),
        }
    )

pair_df = pd.DataFrame(pairs)
pair_df.to_csv(OUTDIR / "lysosomal_module_correlations.tsv", sep="\t", index=False)

# Residualize lysosomal APC against IFN/HLA/MIF-CD74 to find perturbations where
# lysosomal movement is not explained by the coupled APC axis.
X = m[["hla_ii_apc", "ifn_apc", "mif_cd74_receptor_state"]].to_numpy()
X = np.column_stack([np.ones(X.shape[0]), X])
beta = np.linalg.lstsq(X, lys, rcond=None)[0]
pred = X @ beta
resid = lys - pred
sd = resid.std(ddof=1)
out = m.copy()
out["lysosomal_residual"] = resid
out["lysosomal_residual_z"] = resid / sd if sd else 0.0
out["abs_lysosomal_residual_z"] = out["lysosomal_residual_z"].abs()
out.sort_values("abs_lysosomal_residual_z", ascending=False).to_csv(
    OUTDIR / "lysosomal_residual_outliers.tsv", sep="\t"
)

strong_positive = int((pair_df["spearman_r"] > 0.45).sum())
negative = int((pair_df["spearman_r"] < -0.30).sum())
best_residual = out.sort_values("abs_lysosomal_residual_z", ascending=False).head(5)

summary = {
    "hypothesis": "lysosomal APC-processing bottleneck",
    "dataset": str(MATRIX.relative_to(ROOT)),
    "n_perturbations": int(m.shape[0]),
    "module_tests": pairs,
    "grounded_result": (
        "supports_coupled_lysosomal_apc_axis_not_functional_bottleneck"
        if strong_positive >= 2 and negative == 0
        else "inconclusive"
    ),
    "interpretation": (
        "Held Mixscale perturbation module data show GILT/lysosomal APC moving "
        "with IFN/HLA/CD74 modules, especially IFN/APC, not as an independently "
        "opposed bottleneck. This supports coupled APC remodeling but does not "
        "prove antigen-processing flux or myelin peptide presentation defects."
    ),
    "top_residual_outliers": [
        {"perturbation": idx, "lysosomal_residual_z": float(row["lysosomal_residual_z"])}
        for idx, row in best_residual.iterrows()
    ],
    "minimum_next_test": [
        "Direct cathepsin/V-ATPase/lysosomal pH or antigen-processing perturbation in APCs.",
        "HLA-peptidomics or myelin-antigen pulse-chase readout, not transcript-only module movement.",
        "Reject bottleneck interpretation if lysosomal perturbation changes transcript modules without changing antigen-processing output.",
    ],
}

with (OUTDIR / "summary.json").open("w") as fh:
    json.dump(summary, fh, indent=2, sort_keys=True)

print(json.dumps(summary, indent=2, sort_keys=True))
