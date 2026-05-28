#!/usr/bin/env python3
"""Trajectory-level module analysis for GSE235508 pregnancy/postpartum data."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


ROOT = Path(__file__).resolve().parents[1]
IN = ROOT / "results" / "pregnancy_dimension" / "gse235508_modules" / "sample_module_scores.tsv"
OUT = ROOT / "results" / "pregnancy_dimension" / "gse235508_timecourse"
SEED = 20260528


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(IN, sep="\t")
    df = df.dropna(subset=["timepoint", "score", "samplegroup", "module"]).copy()
    df["timepoint"] = df["timepoint"].astype(int)
    df["pregnancy_id"] = df["pregnancy_id"].fillna("")

    means = (
        df.groupby(["samplegroup", "module", "timepoint"])
        .agg(n=("score", "size"), mean_score=("score", "mean"), sd_score=("score", "std"))
        .reset_index()
        .sort_values(["samplegroup", "module", "timepoint"])
    )
    means.to_csv(OUT / "module_timepoint_means.tsv", sep="\t", index=False)

    contrasts = []
    for group in sorted(df["samplegroup"].dropna().unique()):
        for module in sorted(df["module"].unique()):
            sub = df[(df["samplegroup"] == group) & (df["module"] == module)].copy()
            if sub["timepoint"].nunique() < 3:
                continue
            for contrast_name, test_tp, ref_tp in [
                ("late_pregnancy_t3_vs_pre_t0", 3, 0),
                ("postpartum_6wk_t4_vs_late_t3", 4, 3),
                ("postpartum_6mo_t5_vs_late_t3", 5, 3),
                ("postpartum_12mo_t6_vs_late_t3", 6, 3),
                ("late_t3_vs_early_t1", 3, 1),
            ]:
                test = sub[sub["timepoint"] == test_tp]["score"]
                ref = sub[sub["timepoint"] == ref_tp]["score"]
                if len(test) >= 2 and len(ref) >= 2:
                    contrasts.append(
                        {
                            "samplegroup": group,
                            "module": module,
                            "contrast": contrast_name,
                            "test_timepoint": test_tp,
                            "reference_timepoint": ref_tp,
                            "n_test": len(test),
                            "n_reference": len(ref),
                            "mean_test": test.mean(),
                            "mean_reference": ref.mean(),
                            "delta_test_minus_reference": test.mean() - ref.mean(),
                        }
                    )
    pd.DataFrame(contrasts).to_csv(OUT / "timepoint_contrasts.tsv", sep="\t", index=False)

    model_rows = []
    for group in sorted(df["samplegroup"].dropna().unique()):
        for module in sorted(df["module"].unique()):
            sub = df[(df["samplegroup"] == group) & (df["module"] == module)].copy()
            if len(sub) < 12 or sub["timepoint"].nunique() < 4:
                continue
            sub["timepoint_cat"] = sub["timepoint"].astype("category")
            try:
                fit = smf.ols("score ~ C(timepoint_cat)", data=sub).fit()
                for term, coef in fit.params.items():
                    if term == "Intercept":
                        continue
                    model_rows.append(
                        {
                            "samplegroup": group,
                            "module": module,
                            "term": term,
                            "coef_vs_reference_timepoint": coef,
                            "p": fit.pvalues[term],
                            "n": len(sub),
                            "r2": fit.rsquared,
                        }
                    )
            except Exception as exc:
                model_rows.append(
                    {
                        "samplegroup": group,
                        "module": module,
                        "term": "MODEL_ERROR",
                        "coef_vs_reference_timepoint": "",
                        "p": "",
                        "n": len(sub),
                        "r2": "",
                        "error": str(exc),
                    }
                )
    pd.DataFrame(model_rows).to_csv(OUT / "timepoint_ols_terms.tsv", sep="\t", index=False)

    summary = {
        "random_seed": SEED,
        "dataset": "GSE235508",
        "inputs": str(IN.relative_to(ROOT)),
        "outputs": [
            "module_timepoint_means.tsv",
            "timepoint_contrasts.tsv",
            "timepoint_ols_terms.tsv",
        ],
        "caution": "Timepoint labels inferred from GEO numeric coding; source-paper confirmation still required.",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")


if __name__ == "__main__":
    main()
