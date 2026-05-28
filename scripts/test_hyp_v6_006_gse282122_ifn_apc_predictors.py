#!/usr/bin/env python3
"""Tier 0 attempt for HYP_V6_006 in GSE282122 treatment-response data."""

from __future__ import annotations

import json
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import scipy.stats as st
import statsmodels.formula.api as smf
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import LeaveOneOut
from sklearn.preprocessing import StandardScaler


ROOT = Path(__file__).resolve().parents[1]
IN = ROOT / "analysis" / "tier_1_mechanism" / "mif_cd74_gse282122_component_response" / "paired_component_deltas.tsv"
OUT = ROOT / "analysis" / "tier_0_triage" / "hyp_v6_006_gse282122_ifn_apc_predictors"

FEATURES = [
    "ifn_apc",
    "hla_ii_without_cd74",
    "receptor_only_cd74_cd44_cxcr4",
    "cd74_alone",
    "full_mif_cd74_state",
]


def loocv_auc(df: pd.DataFrame, cols: list[str]) -> float:
    x = df[cols].astype(float).values
    y = df["remission_binary"].astype(int).values
    if len(np.unique(y)) < 2 or len(y) < 8:
        return np.nan
    preds = np.zeros(len(y))
    loo = LeaveOneOut()
    for train_idx, test_idx in loo.split(x):
        if len(np.unique(y[train_idx])) < 2:
            preds[test_idx] = y[train_idx].mean()
            continue
        scaler = StandardScaler()
        x_train = scaler.fit_transform(x[train_idx])
        x_test = scaler.transform(x[test_idx])
        model = LogisticRegression(C=1.0, solver="liblinear", random_state=20260528)
        model.fit(x_train, y[train_idx])
        preds[test_idx] = model.predict_proba(x_test)[:, 1]
    return float(roc_auc_score(y, preds))


def main() -> None:
    warnings.filterwarnings("ignore")
    OUT.mkdir(parents=True, exist_ok=True)
    wide = pd.read_csv(IN, sep="\t")
    rows = []
    nested_rows = []
    for state_level in ["major", "fine"]:
        for cell_state in sorted(wide.loc[wide["state_level"] == state_level, "cell_state"].dropna().unique()):
            sub = wide[(wide["state_level"] == state_level) & (wide["cell_state"] == cell_state)].copy()
            if sub["remission_binary"].nunique() < 2 or len(sub) < 12:
                continue
            for timing in ["pre", "delta"]:
                feature_cols = [f"{timing}__{f}" for f in FEATURES]
                sub2 = sub.dropna(subset=feature_cols + ["remission_binary", "baseline_inflammation_score", "Disease"]).copy()
                if sub2["remission_binary"].nunique() < 2 or len(sub2) < 12:
                    continue
                for feature, col in zip(FEATURES, feature_cols):
                    rem = sub2[sub2["remission_binary"] == 1][col]
                    non = sub2[sub2["remission_binary"] == 0][col]
                    t = st.ttest_ind(rem, non, equal_var=False, nan_policy="omit")
                    try:
                        fit = smf.logit(
                            f"remission_binary ~ Q('{col}') + baseline_inflammation_score + C(Disease)",
                            data=sub2,
                        ).fit(disp=False, maxiter=200)
                        coef = fit.params.get(f"Q('{col}')", np.nan)
                        p = fit.pvalues.get(f"Q('{col}')", np.nan)
                    except Exception:
                        coef = np.nan
                        p = np.nan
                    auc = loocv_auc(sub2, [col])
                    rows.append(
                        {
                            "state_level": state_level,
                            "cell_state": cell_state,
                            "timing": timing,
                            "feature": feature,
                            "n": len(sub2),
                            "n_remission": int(sub2["remission_binary"].sum()),
                            "delta_remission_minus_non": float(rem.mean() - non.mean()),
                            "welch_p": float(t.pvalue),
                            "adjusted_logit_coef": coef,
                            "adjusted_logit_p": p,
                            "loocv_auc_univariate": auc,
                        }
                    )
                nested_specs = {
                    "ifn_only": [f"{timing}__ifn_apc"],
                    "hla_only": [f"{timing}__hla_ii_without_cd74"],
                    "receptor_only": [f"{timing}__receptor_only_cd74_cd44_cxcr4"],
                    "ifn_plus_hla": [f"{timing}__ifn_apc", f"{timing}__hla_ii_without_cd74"],
                    "all_components": feature_cols,
                }
                for name, cols in nested_specs.items():
                    nested_rows.append(
                        {
                            "state_level": state_level,
                            "cell_state": cell_state,
                            "timing": timing,
                            "model": name,
                            "n": len(sub2),
                            "loocv_auc": loocv_auc(sub2, cols),
                            "features": ";".join(cols),
                        }
                    )

    results = pd.DataFrame(rows)
    nested = pd.DataFrame(nested_rows)
    results.to_csv(OUT / "univariate_predictors.tsv", sep="\t", index=False)
    nested.to_csv(OUT / "nested_model_auc.tsv", sep="\t", index=False)

    focus = results[
        (results["state_level"] == "major")
        & (results["cell_state"].isin(["Mono_macro", "DC"]))
        & (results["feature"].isin(["ifn_apc", "hla_ii_without_cd74", "receptor_only_cd74_cd44_cxcr4"]))
    ].copy()
    focus_nested = nested[
        (nested["state_level"] == "major")
        & (nested["cell_state"].isin(["Mono_macro", "DC"]))
    ].copy()
    summary = {
        "dataset": "GSE282122",
        "hypothesis": "HYP_V6_006",
        "focus_univariate": focus.to_dict(orient="records"),
        "focus_nested_auc": focus_nested.to_dict(orient="records"),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")

    lines = [
        "# HYP_V6_006 Tier 0 Attempt: GSE282122 IFN/APC Predictors",
        "",
        "## Scope",
        "",
        "Tests whether remission in anti-TNF-treated IBD myeloid/DC states is",
        "better described by IFN/APC remodeling than by CD74/HLA-II receptor",
        "components. This is a treatment-response hypothesis-generating test, not",
        "an MS therapeutic claim.",
        "",
        "## Major Myeloid/DC Univariate Results",
        "",
        "```tsv",
        focus.sort_values(["cell_state", "timing", "feature"]).to_csv(sep="\t", index=False).strip(),
        "```",
        "",
        "## Major Myeloid/DC LOOCV AUC Models",
        "",
        "```tsv",
        focus_nested.sort_values(["cell_state", "timing", "model"]).to_csv(sep="\t", index=False).strip(),
        "```",
        "",
        "## Interpretation",
        "",
        "Tier -1/Tier 0 promotion should favor the component whose baseline or",
        "delta behavior is directionally consistent, adjusted-model compatible,",
        "and not merely rescued by overfit multi-feature AUC in small n.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
