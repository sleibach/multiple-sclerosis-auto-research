#!/usr/bin/env python3
"""Component-resolved CD74/HLA-II residual test in local MS pseudobulk data."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import scipy.stats as st
import statsmodels.api as sm
from statsmodels.stats.multitest import multipletests


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "results/discovery_pseudobulk_scores.tsv"
OUT = ROOT / "analysis/tier_1_mechanism/mif_cd74_component_ms_pseudobulk"


COMPONENTS = {
    "cd74_alone": ["CD74"],
    "hla_ii_without_cd74": ["HLA-DRA", "HLA-DPA1", "HLA-DPB1"],
    "hla_ii_with_cd74": ["CD74", "HLA-DRA", "HLA-DPA1", "HLA-DPB1"],
    "lysosomal_partial": ["CTSB", "CD68"],
    "myeloid_lipid_partial": ["APOE", "C1QA", "C1QB", "C1QC", "TREM2", "LPL", "GPNMB"],
}

CONTRASTS = {
    "active_edge_vs_control_wm": ("chronic_active_MS_lesion_edge", "control_white_matter"),
    "inactive_edge_vs_control_wm": ("chronic_inactive_MS_lesion_edge", "control_white_matter"),
    "periplaque_vs_control_wm": ("MS_periplaque_white_matter", "control_white_matter"),
    "lesion_core_vs_control_wm": ("MS_lesion_core", "control_white_matter"),
    "active_edge_vs_inactive_edge": ("chronic_active_MS_lesion_edge", "chronic_inactive_MS_lesion_edge"),
}


def zscore_columns(df: pd.DataFrame, cols: list[str]) -> pd.Series:
    present = [c for c in cols if c in df.columns]
    if not present:
        return pd.Series(np.nan, index=df.index)
    z = df[present].astype(float)
    z = (z - z.mean(axis=0)) / z.std(axis=0, ddof=0).replace(0, np.nan)
    return z.mean(axis=1)


def hedges_g(a: pd.Series, b: pd.Series) -> float:
    a = a.dropna().astype(float)
    b = b.dropna().astype(float)
    if len(a) < 2 or len(b) < 2:
        return np.nan
    pooled = np.sqrt(((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) / (len(a) + len(b) - 2))
    if pooled == 0:
        return np.nan
    return float(((a.mean() - b.mean()) / pooled) * (1 - 3 / (4 * (len(a) + len(b)) - 9)))


def contrast(score: pd.Series, group: pd.Series, case: str, control: str) -> dict:
    a = score[group == case]
    b = score[group == control]
    if len(a) < 2 or len(b) < 2:
        return {"n_case": len(a), "n_control": len(b), "delta": np.nan, "hedges_g": np.nan, "p": np.nan}
    test = st.ttest_ind(a, b, equal_var=False, nan_policy="omit")
    return {
        "n_case": int(len(a)),
        "n_control": int(len(b)),
        "delta": float(a.mean() - b.mean()),
        "hedges_g": hedges_g(a, b),
        "p": float(test.pvalue),
    }


def residualize(y: pd.Series, covariates: pd.DataFrame) -> tuple[pd.Series, float]:
    frame = pd.concat([y.rename("y"), covariates], axis=1).dropna()
    residuals = pd.Series(np.nan, index=y.index)
    if len(frame) < covariates.shape[1] + 3:
        return residuals, np.nan
    x = sm.add_constant(frame[covariates.columns].astype(float))
    fit = sm.OLS(frame["y"].astype(float), x).fit()
    residuals.loc[frame.index] = fit.resid
    return residuals, float(fit.rsquared)


def md_tsv(df: pd.DataFrame) -> str:
    return "```tsv\n" + df.to_csv(sep="\t", index=False) + "```"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(INPUT, sep="\t")
    for name, genes in COMPONENTS.items():
        df[name] = zscore_columns(df, genes)

    rows = []
    for cell_type, sub in df.groupby("cell_type"):
        sub = sub.copy()
        if len(sub) < 4:
            continue
        covariates = pd.DataFrame(
            {
                "B_APC": sub["B_APC"],
                "n_nuclei_log": np.log2(sub["n_nuclei"].astype(float) + 1),
                "library_size_log": np.log2(sub["library_size"].astype(float) + 1),
            },
            index=sub.index,
        )
        for component in COMPONENTS:
            raw = sub[component]
            residual, r2 = residualize(raw, covariates)
            for contrast_name, (case, control) in CONTRASTS.items():
                raw_result = contrast(raw, sub["pathology"], case, control)
                res_result = contrast(residual, sub["pathology"], case, control)
                rows.append(
                    {
                        "cell_type": cell_type,
                        "component": component,
                        "contrast": contrast_name,
                        "case_pathology": case,
                        "control_pathology": control,
                        "covariate_r2": r2,
                        **{f"raw_{k}": v for k, v in raw_result.items()},
                        **{f"residual_{k}": v for k, v in res_result.items()},
                    }
                )

    tests = pd.DataFrame(rows)
    for col in ["raw_p", "residual_p"]:
        mask = tests[col].notna()
        tests[col.replace("_p", "_fdr")] = np.nan
        if mask.any():
            tests.loc[mask, col.replace("_p", "_fdr")] = multipletests(tests.loc[mask, col], method="fdr_bh")[1]
    tests.to_csv(OUT / "component_residual_tests.tsv", sep="\t", index=False)

    focus = tests[
        (tests["cell_type"].eq("immune"))
        & (tests["contrast"].isin(["active_edge_vs_control_wm", "periplaque_vs_control_wm", "active_edge_vs_inactive_edge"]))
    ].copy()
    focus.to_csv(OUT / "immune_focus_tests.tsv", sep="\t", index=False)

    retained = tests[
        (tests["component"].eq("cd74_alone"))
        & (tests["residual_delta"] > 0)
        & (tests["residual_p"] < 0.05)
    ].copy()
    summary = {
        "input": str(INPUT.relative_to(ROOT)),
        "scope": "Local pseudobulk score table; tests CD74/HLA-II components, not full MIF/CD74/CD44/CXCR4 receptor complex because MIF/CD44/CXCR4 are absent.",
        "n_rows": int(len(df)),
        "components": COMPONENTS,
        "cd74_residual_nominal_positive_count": int(len(retained)),
        "cd74_residual_nominal_positive_rows": retained.to_dict(orient="records"),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2))

    report = [
        "# MIF/CD74 Tier 1 Component Test: MS Pseudobulk",
        "",
        "## Scope Guardrail",
        "This is a component-resolved test on the local `results/discovery_pseudobulk_scores.tsv` table. It can test `CD74` and HLA-II separability from a broad `B_APC` score, nuclei count, and library size. It cannot test the full `MIF/CD74/CD44/CXCR4` receptor complex because `MIF`, `CD44`, and `CXCR4` are not present in this table.",
        "",
        "## Immune Focus Tests",
        md_tsv(focus.sort_values(["component", "contrast"])),
        "",
        "## Summary",
        f"Nominal positive residual `CD74` rows after `B_APC`/size adjustment: {len(retained)}.",
        "",
        "## Interpretation",
        "If CD74 loses residual support after broad APC adjustment, the MIF/CD74 candidate should be treated as generic APC/HLA-II biology unless another dataset contains the full receptor-complex variables and clinical linkage.",
        "",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
