#!/usr/bin/env python3
"""Treatment-response interaction test for MIF/CD74 state in GSE282122."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats


ROOT = Path(__file__).resolve().parents[1]
IN = ROOT / "phases/v3/results" / "wave67_gse282122_myeloid_pseudobulk" / "paired_module_deltas.tsv"
OUT = ROOT / "analysis" / "tier_0_triage" / "mif_cd74_stratification" / "gse282122_remission_interaction"
SEED = 20260528


def hedges_g(a: pd.Series, b: pd.Series) -> float:
    a = a.dropna()
    b = b.dropna()
    pooled = (((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) / (len(a) + len(b) - 2)) ** 0.5
    if pooled == 0:
        return float("nan")
    d = (a.mean() - b.mean()) / pooled
    return d * (1 - (3 / (4 * (len(a) + len(b)) - 9)))


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(IN, sep="\t")
    df = df[df["passes_cell_threshold"] == True].copy()
    df["remission_binary"] = (df["Remission_status"] == "Remission").astype(int)

    wide = df.pivot_table(
        index=[
            "Patient",
            "Disease",
            "Site",
            "Remission_status",
            "state_level",
            "cell_state",
            "pair_id",
            "baseline_inflammation_score",
        ],
        columns="module",
        values=["pre_score", "delta_post_minus_pre"],
        aggfunc="first",
    )
    wide.columns = [f"{a}__{b}" for a, b in wide.columns]
    wide = wide.reset_index()
    wide["remission_binary"] = (wide["Remission_status"] == "Remission").astype(int)

    target = "mif_cd74_receptor_state"
    generic = "ifn_apc"
    rows = []
    baseline_rows = []
    for state_level in ["major", "fine"]:
        for cell_state in sorted(wide.loc[wide["state_level"] == state_level, "cell_state"].dropna().unique()):
            sub = wide[(wide["state_level"] == state_level) & (wide["cell_state"] == cell_state)].copy()
            need = [
                f"delta_post_minus_pre__{target}",
                f"pre_score__{target}",
                f"delta_post_minus_pre__{generic}",
                "baseline_inflammation_score",
                "remission_binary",
            ]
            if not all(col in sub.columns for col in need):
                continue
            sub = sub.dropna(subset=need)
            if sub["remission_binary"].nunique() < 2 or len(sub) < 8:
                continue
            rem = sub[sub["remission_binary"] == 1][f"delta_post_minus_pre__{target}"]
            non = sub[sub["remission_binary"] == 0][f"delta_post_minus_pre__{target}"]
            t = stats.ttest_ind(rem, non, equal_var=False, nan_policy="omit")
            formula = (
                f"Q('delta_post_minus_pre__{target}') ~ remission_binary + "
                f"Q('pre_score__{target}') + Q('delta_post_minus_pre__{generic}') + "
                "baseline_inflammation_score + C(Disease)"
            )
            try:
                fit = smf.ols(formula, data=sub).fit()
                adj_delta = fit.params.get("remission_binary", float("nan"))
                adj_p = fit.pvalues.get("remission_binary", float("nan"))
            except Exception:
                adj_delta = float("nan")
                adj_p = float("nan")
            rows.append(
                {
                    "state_level": state_level,
                    "cell_state": cell_state,
                    "n": len(sub),
                    "n_remission": int(sub["remission_binary"].sum()),
                    "n_non_remission": int((1 - sub["remission_binary"]).sum()),
                    "mean_delta_remission": rem.mean(),
                    "mean_delta_non_remission": non.mean(),
                    "raw_delta_remission_minus_non": rem.mean() - non.mean(),
                    "raw_hedges_g": hedges_g(rem, non),
                    "raw_p": t.pvalue,
                    "generic_adjusted_delta": adj_delta,
                    "generic_adjusted_p": adj_p,
                }
            )
            rem_base = sub[sub["remission_binary"] == 1][f"pre_score__{target}"]
            non_base = sub[sub["remission_binary"] == 0][f"pre_score__{target}"]
            base_t = stats.ttest_ind(rem_base, non_base, equal_var=False, nan_policy="omit")
            try:
                base_fit = smf.logit(
                    f"remission_binary ~ Q('pre_score__{target}') + baseline_inflammation_score + C(Disease)",
                    data=sub,
                ).fit(disp=False)
                base_coef = base_fit.params.get(f"Q('pre_score__{target}')", float("nan"))
                base_p = base_fit.pvalues.get(f"Q('pre_score__{target}')", float("nan"))
            except Exception:
                base_coef = float("nan")
                base_p = float("nan")
            baseline_rows.append(
                {
                    "state_level": state_level,
                    "cell_state": cell_state,
                    "n": len(sub),
                    "n_remission": int(sub["remission_binary"].sum()),
                    "n_non_remission": int((1 - sub["remission_binary"]).sum()),
                    "mean_baseline_remission": rem_base.mean(),
                    "mean_baseline_non_remission": non_base.mean(),
                    "raw_delta_baseline_remission_minus_non": rem_base.mean() - non_base.mean(),
                    "raw_hedges_g": hedges_g(rem_base, non_base),
                    "raw_p": base_t.pvalue,
                    "logit_coef_baseline_target": base_coef,
                    "logit_p_baseline_target": base_p,
                }
            )

    out = pd.DataFrame(rows).sort_values("generic_adjusted_p", na_position="last")
    out.to_csv(OUT / "mif_cd74_remission_interaction.tsv", sep="\t", index=False)
    base_out = pd.DataFrame(baseline_rows).sort_values("logit_p_baseline_target", na_position="last")
    base_out.to_csv(OUT / "mif_cd74_baseline_predictive.tsv", sep="\t", index=False)
    sig = out[(out["generic_adjusted_p"] <= 0.10) & (out["generic_adjusted_delta"] < 0)]
    base_sig = base_out[base_out["logit_p_baseline_target"] <= 0.10]
    summary = {
        "random_seed": SEED,
        "dataset": "GSE282122 paired anti-TNF IBD myeloid pseudobulk",
        "target_module": target,
        "adjustment": "baseline target score, ifn_apc delta, baseline inflammation, disease",
        "n_tests": int(len(out)),
        "n_nominal_adj_p_le_0_10_remission_decrease": int(len(sig)),
        "n_baseline_predictive_p_le_0_10": int(len(base_sig)),
        "top_rows": out.head(5).to_dict(orient="records"),
        "top_baseline_rows": base_out.head(5).to_dict(orient="records"),
        "interpretation": "Negative adjusted delta means remission is associated with a larger post-treatment decrease in MIF/CD74 state than non-remission.",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")


if __name__ == "__main__":
    main()
