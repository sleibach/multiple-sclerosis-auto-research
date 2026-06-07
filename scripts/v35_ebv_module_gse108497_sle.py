#!/usr/bin/env python3
"""Score host EBV module in local GSE108497 SLE/healthy pregnancy blood."""

from __future__ import annotations

import gzip
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats


ROOT = Path(__file__).resolve().parents[1]
EXPR = ROOT / "data/raw/GSE108497/GSE108497_normalized_data.txt.gz"
PROBES = ROOT / "results/pregnancy_dimension/gse108497_sle/platform_probe_symbols.tsv"
META = ROOT / "results/pregnancy_dimension/gse108497_sle/sample_metadata_parsed.tsv"
MODULE_SCORES = ROOT / "results/pregnancy_dimension/gse108497_sle/module_scores.tsv"
EBV_UP = ROOT / "analysis/v35_ebv_module_gse162516/host_ebv_transformation_up_top200.tsv"
EBV_DOWN = ROOT / "analysis/v35_ebv_module_gse162516/host_ebv_transformation_down_top200.tsv"
OUTDIR = ROOT / "analysis/v35_ebv_module_gse108497_sle"
OUTDIR.mkdir(parents=True, exist_ok=True)


up_genes = set(pd.read_csv(EBV_UP, sep="\t")["tracking_id"].head(100))
down_genes = set(pd.read_csv(EBV_DOWN, sep="\t")["tracking_id"].head(100))
probe_map = pd.read_csv(PROBES, sep="\t")
up_probes = sorted(probe_map[probe_map["gene"].isin(up_genes)]["ID_REF"].unique())
down_probes = sorted(probe_map[probe_map["gene"].isin(down_genes)]["ID_REF"].unique())

# Normalized file has alternating value and Detection Pval columns. Keep values
# whose header matches sample array IDs from metadata.
meta = pd.read_csv(META, sep="\t")
array_ids = set(meta["array_id"])
expr = pd.read_csv(EXPR, sep="\t", compression="gzip")
value_cols = ["ID_REF"] + [c for c in expr.columns if c in array_ids]
expr = expr[value_cols].set_index("ID_REF")

def module_score(probes: list[str]) -> pd.Series:
    present = [p for p in probes if p in expr.index]
    return expr.loc[present].astype(float).mean(axis=0)

scores = pd.DataFrame(
    {
        "array_id": list(array_ids),
    }
)
scores = scores.set_index("array_id")
scores["ebv_up_score"] = module_score(up_probes)
scores["ebv_down_score"] = module_score(down_probes)
scores["ebv_up_minus_down"] = scores["ebv_up_score"] - scores["ebv_down_score"]
scores = scores.reset_index().merge(meta, on="array_id", how="left")

ifn = pd.read_csv(MODULE_SCORES, sep="\t")
ifn = ifn[ifn["module"] == "ifn_apc"][["array_id", "score"]].rename(columns={"score": "ifn_apc_score"})
scores = scores.merge(ifn, on="array_id", how="left")
scores.to_csv(OUTDIR / "sample_ebv_ifn_scores.tsv", sep="\t", index=False)

tests = []
for score in ["ebv_up_score", "ebv_down_score", "ebv_up_minus_down"]:
    for tp_label, sub in scores.groupby("tp_label"):
        sle = sub[sub["sle"] == 1][score].dropna().astype(float)
        hc = sub[sub["sle"] == 0][score].dropna().astype(float)
        if len(sle) >= 3 and len(hc) >= 3:
            tests.append(
                {
                    "score": score,
                    "contrast": f"SLE_vs_HC_at_{tp_label}",
                    "n_sle": int(len(sle)),
                    "n_hc": int(len(hc)),
                    "mean_sle": float(sle.mean()),
                    "mean_hc": float(hc.mean()),
                    "delta_sle_minus_hc": float(sle.mean() - hc.mean()),
                    "welch_p": float(stats.ttest_ind(sle, hc, equal_var=False).pvalue),
                }
            )

# Simple IFN residualization for EBV-up score.
valid = scores[["ebv_up_score", "ifn_apc_score", "sle"]].dropna()
X = np.column_stack([np.ones(len(valid)), valid["ifn_apc_score"].to_numpy()])
y = valid["ebv_up_score"].to_numpy()
beta = np.linalg.lstsq(X, y, rcond=None)[0]
valid = valid.copy()
valid["ebv_up_resid_ifn"] = y - X @ beta
resid_sle = valid[valid["sle"] == 1]["ebv_up_resid_ifn"]
resid_hc = valid[valid["sle"] == 0]["ebv_up_resid_ifn"]
resid_test = {
    "score": "ebv_up_resid_ifn",
    "contrast": "SLE_vs_HC_all_timepoints_after_linear_IFN_residualization",
    "n_sle": int(len(resid_sle)),
    "n_hc": int(len(resid_hc)),
    "mean_sle": float(resid_sle.mean()),
    "mean_hc": float(resid_hc.mean()),
    "delta_sle_minus_hc": float(resid_sle.mean() - resid_hc.mean()),
    "welch_p": float(stats.ttest_ind(resid_sle, resid_hc, equal_var=False).pvalue),
}
tests.append(resid_test)

pd.DataFrame(tests).to_csv(OUTDIR / "sle_ebv_module_tests.tsv", sep="\t", index=False)

corr = {
    "ebv_up_vs_ifn_spearman": float(stats.spearmanr(scores["ebv_up_score"], scores["ifn_apc_score"], nan_policy="omit").statistic),
    "ebv_up_vs_ifn_p": float(stats.spearmanr(scores["ebv_up_score"], scores["ifn_apc_score"], nan_policy="omit").pvalue),
}
summary = {
    "hypothesis": "SLE host EBV-module-like state",
    "grounded_result": "scored_no_ebv_metadata_not_imprint",
    "n_samples": int(len(scores)),
    "n_up_probes": len(up_probes),
    "n_down_probes": len(down_probes),
    "correlations": corr,
    "residual_test": resid_test,
    "interpretation": (
        "The host EBV module can be scored in local SLE/healthy pregnancy blood. "
        "Because GSE108497 lacks EBV serostatus/viral-load metadata, this tests "
        "only an EBV-module-like host transcriptional state. Any SLE difference "
        "must be interpreted after IFN/APC residualization and cannot establish "
        "EBV imprint causality."
    ),
}
with (OUTDIR / "summary.json").open("w") as fh:
    json.dump(summary, fh, indent=2, sort_keys=True)
print(json.dumps(summary, indent=2, sort_keys=True))
