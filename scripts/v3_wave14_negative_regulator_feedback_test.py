#!/usr/bin/env python3
"""Test whether negative-regulator candidates behave like brakes or feedback markers.

`PTPN2`, `TNFAIP3`, and `SH2B3` have broad genetics and received the strongest
focused Geneformer support, but they are hard direct targets. Before looking
for downstream druggable handles, this script asks a simpler question in the
local donor-level data:

Do these genes anticorrelate with IFN/HLA/CD74 modules, as a candidate brake
might, or do they positively track the disease state, as compensatory feedback
markers often do?

The test is descriptive and donor-level. It is not causal inference.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results_v3" / "wave14_negative_regulator_feedback"
GENE_SCORES = ROOT / "results_v3" / "wave13_candidate_gene_local_validation" / "wave13_candidate_gene_donor_scores.tsv"
MODULE_SCORES = ROOT / "results_v3" / "direct_h5ad_cell_state" / "direct_h5ad_donor_module_scores.tsv"

GENES = ["PTPN2", "TNFAIP3", "SH2B3", "CLEC16A", "SLC15A4", "CD74", "CTSS", "CIITA", "RFX5"]
MODULES = ["ifn_apc", "hla_ii_apc", "mif_cd74_receptor_state", "mixscale_validated_ifng_readout", "lysosomal_apc"]


def corr(x: pd.Series, y: pd.Series) -> dict[str, object]:
    ok = pd.DataFrame({"x": x, "y": y}).replace([np.inf, -np.inf], np.nan).dropna()
    if len(ok) < 5 or ok["x"].nunique() < 3 or ok["y"].nunique() < 3:
        return {"n": int(len(ok)), "spearman_r": np.nan, "spearman_p": np.nan}
    res = stats.spearmanr(ok["x"], ok["y"])
    return {"n": int(len(ok)), "spearman_r": float(res.statistic), "spearman_p": float(res.pvalue)}


def classify(rho: float, p_value: float) -> str:
    if not np.isfinite(rho):
        return "insufficient"
    if rho <= -0.5 and np.isfinite(p_value) and p_value <= 0.10:
        return "brake_like_negative"
    if rho >= 0.5 and np.isfinite(p_value) and p_value <= 0.10:
        return "feedback_like_positive"
    if rho < -0.25:
        return "weak_negative"
    if rho > 0.25:
        return "weak_positive"
    return "flat"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    genes = pd.read_csv(GENE_SCORES, sep="\t")
    modules = pd.read_csv(MODULE_SCORES, sep="\t")
    genes = genes[genes["gene"].isin(GENES)].copy()
    modules = modules[modules["module"].isin(MODULES)].copy()

    rows: list[dict[str, object]] = []
    for analysis, gsub in genes.groupby("analysis", observed=True):
        msub = modules[modules["analysis"] == analysis]
        for gene, gg in gsub.groupby("gene", observed=True):
            gene_frame = gg[["donor_id", "group", "mean_log_norm", "detection_fraction"]].drop_duplicates()
            for module, mm in msub.groupby("module", observed=True):
                module_frame = mm[["donor_id", "mean_score", "high_fraction"]].drop_duplicates()
                merged = gene_frame.merge(module_frame, on="donor_id", how="inner")
                if merged.empty:
                    continue
                for group_name, sub in [("all_donors", merged), ("case_only", merged[merged["group"] == "case"])]:
                    for gene_metric in ["mean_log_norm", "detection_fraction"]:
                        for module_metric in ["mean_score", "high_fraction"]:
                            c = corr(sub[gene_metric], sub[module_metric])
                            rho = c["spearman_r"]
                            p_value = c["spearman_p"]
                            rows.append(
                                {
                                    "analysis": analysis,
                                    "disease_name": str(gsub["disease_name"].iloc[0]),
                                    "compartment": str(gsub["compartment"].iloc[0]),
                                    "gene": gene,
                                    "module": module,
                                    "group": group_name,
                                    "gene_metric": gene_metric,
                                    "module_metric": module_metric,
                                    **c,
                                    "relationship": classify(float(rho) if pd.notna(rho) else np.nan, float(p_value) if pd.notna(p_value) else np.nan),
                                }
                            )
    df = pd.DataFrame(rows)
    if not df.empty:
        df.to_csv(OUT / "negative_regulator_feedback_correlations.tsv", sep="\t", index=False)

    summary_rows = []
    for gene, sub in df[df["group"] == "all_donors"].groupby("gene", observed=True):
        informative = sub[sub["relationship"].isin(["brake_like_negative", "feedback_like_positive", "weak_negative", "weak_positive"])]
        summary_rows.append(
            {
                "gene": gene,
                "n_tests": int(len(sub)),
                "n_brake_like_negative": int((sub["relationship"] == "brake_like_negative").sum()),
                "n_feedback_like_positive": int((sub["relationship"] == "feedback_like_positive").sum()),
                "n_weak_negative": int((sub["relationship"] == "weak_negative").sum()),
                "n_weak_positive": int((sub["relationship"] == "weak_positive").sum()),
                "median_spearman_r": float(np.nanmedian(sub["spearman_r"])) if sub["spearman_r"].notna().any() else np.nan,
                "informative_relationships": int(len(informative)),
            }
        )
    summary = pd.DataFrame(summary_rows).sort_values(
        ["n_feedback_like_positive", "n_brake_like_negative", "n_weak_positive"],
        ascending=[False, True, False],
    )
    summary.to_csv(OUT / "negative_regulator_feedback_summary.tsv", sep="\t", index=False)

    out = {
        "genes": GENES,
        "modules": MODULES,
        "n_correlations": int(len(df)),
        "interpretation": (
            "Brake-like support would require repeated negative correlations with IFN/HLA/CD74 modules. "
            "Repeated positive correlations indicate feedback/state-marker behavior."
        ),
        "summary": summary.to_dict(orient="records"),
    }
    (OUT / "summary.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
