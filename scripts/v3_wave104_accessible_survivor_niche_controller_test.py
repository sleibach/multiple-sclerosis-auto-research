#!/usr/bin/env python3
"""Wave104 matched-donor niche-controller test for accessible survivors.

Wave102 showed that accessible survivor expression does not survive strict
same-compartment disease residualization. The Wave101 mechanism sidecar raised
one stricter mechanistic question: does tissue-resident candidate expression
predict matched-donor myeloid lipid-lysosomal module intensity?

This script pairs tissue-resident compartments (epithelial, stromal,
endothelial, keratinocyte) with myeloid/APC compartments from the same dataset,
disease contrast, and donor. It then tests whether candidate expression in the
tissue compartment predicts myeloid/APC lipid-lysosomal module scores after
adjusting both predictor and outcome for disease status and inflammatory/stress
modules.

Passing this test is only a forcing signal. It is not a therapeutic claim.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy import stats

from v3_analyze_osmr_complement_axes import ROOT
from v3_wave85_external_geo_antitnf_validation import markdown_table, rel, write_json


SEED = 20260527
OUT = ROOT / "phases/v3/results" / "wave104_accessible_survivor_niche_controller_test"

DONOR_SCORES = (
    ROOT
    / "phases/v3/results"
    / "wave102_accessible_survivor_residual_compartment_test"
    / "accessible_survivor_donor_scores.tsv"
)
MODULE_SCORES = ROOT / "phases/v3/results" / "direct_h5ad_cell_state" / "direct_h5ad_donor_module_scores.tsv"
W102 = (
    ROOT
    / "phases/v3/results"
    / "wave102_accessible_survivor_residual_compartment_test"
    / "accessible_survivor_residual_summary.tsv"
)

CANDIDATES = ["SEL1L3", "FXYD5", "APOC1", "CD82", "LAPTM5"]
FOCUS = {"SEL1L3", "FXYD5"}

TARGET_MODULES = [
    "lipid_loader_repair",
    "lysosomal_apc",
    "complement_phagocytosis",
    "c1q_phagocytic_myeloid",
]

COVARIATE_MODULES = [
    "ifn_apc",
    "inflammatory_nfkb",
    "hif_nampt_metabolic",
    "hla_ii_apc",
    "lysosomal_apc",
    "lipid_loader_repair",
]

MIN_PAIRS = 6

COVARIATE_PRIORITY = [
    "case_indicator",
    "target_inflammatory_nfkb",
    "target_hif_nampt_metabolic",
    "source_inflammatory_nfkb",
    "source_hif_nampt_metabolic",
    "target_ifn_apc",
    "source_ifn_apc",
    "target_hla_ii_apc",
    "source_hla_ii_apc",
    "source_lipid_loader_repair",
    "target_lipid_loader_repair",
    "source_lysosomal_apc",
    "target_lysosomal_apc",
]


def read_tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


def clean(value: Any) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except (TypeError, ValueError):
        pass
    return str(value)


def residualize(values: np.ndarray, covariates: pd.DataFrame) -> tuple[np.ndarray, int, float]:
    y = np.asarray(values, dtype=float)
    x = covariates.astype(float).to_numpy()
    mask = np.isfinite(y) & np.all(np.isfinite(x), axis=1)
    residuals = np.full(len(y), np.nan)
    if x.shape[1] == 0:
        return y.copy(), int(np.isfinite(y).sum()), 0.0
    if mask.sum() < max(5, x.shape[1] + 3):
        return residuals, int(mask.sum()), math.nan
    x_mask = x[mask]
    keep = np.nanstd(x_mask, axis=0) > 1e-8
    x_mask = x_mask[:, keep]
    if x_mask.shape[1] == 0:
        residuals[mask] = y[mask] - np.nanmean(y[mask])
        return residuals, int(mask.sum()), 0.0
    design = np.column_stack([np.ones(mask.sum()), x_mask])
    beta, *_ = np.linalg.lstsq(design, y[mask], rcond=None)
    fitted = design @ beta
    resid = y[mask] - fitted
    residuals[mask] = resid
    ss_res = float(np.sum(resid**2))
    ss_tot = float(np.sum((y[mask] - np.mean(y[mask])) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else math.nan
    return residuals, int(mask.sum()), r2


def linreg(x: np.ndarray, y: np.ndarray) -> dict[str, float]:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    mask = np.isfinite(x) & np.isfinite(y)
    if mask.sum() < MIN_PAIRS or np.nanstd(x[mask]) <= 1e-8 or np.nanstd(y[mask]) <= 1e-8:
        return {
            "n": int(mask.sum()),
            "slope": math.nan,
            "r": math.nan,
            "r2": math.nan,
            "p": math.nan,
            "spearman_rho": math.nan,
            "spearman_p": math.nan,
        }
    lr = stats.linregress(x[mask], y[mask])
    rho, sp = stats.spearmanr(x[mask], y[mask])
    return {
        "n": int(mask.sum()),
        "slope": float(lr.slope),
        "r": float(lr.rvalue),
        "r2": float(lr.rvalue**2),
        "p": float(lr.pvalue),
        "spearman_rho": float(rho),
        "spearman_p": float(sp),
    }


def adaptive_covariates(sub: pd.DataFrame, requested: list[str]) -> tuple[pd.DataFrame, list[str], str]:
    numeric = sub[requested].apply(pd.to_numeric, errors="coerce")
    n_complete_all = int(np.isfinite(numeric.to_numpy(float)).all(axis=1).sum()) if not numeric.empty else 0
    usable = []
    for col in requested:
        vals = pd.to_numeric(sub[col], errors="coerce").to_numpy(float)
        if np.isfinite(vals).sum() >= MIN_PAIRS and np.nanstd(vals[np.isfinite(vals)]) > 1e-8:
            usable.append(col)
    ordered = [col for col in COVARIATE_PRIORITY if col in usable] + [col for col in usable if col not in COVARIATE_PRIORITY]
    if not ordered:
        return pd.DataFrame(index=sub.index), [], "none"
    # Leave at least four degrees of freedom for residual-correlation testing.
    complete_for_ordered = np.isfinite(sub[ordered].apply(pd.to_numeric, errors="coerce").to_numpy(float)).all(axis=1)
    n_complete = int(complete_for_ordered.sum())
    max_covariates = max(1, n_complete - 4)
    selected = ordered[:max_covariates]
    mode = "full" if set(selected) == set(usable) else f"adaptive_top_{len(selected)}_of_{len(usable)}"
    if n_complete_all < MIN_PAIRS:
        mode += "_missingness_limited"
    return sub[selected].apply(pd.to_numeric, errors="coerce"), selected, mode


def module_wide(modules: pd.DataFrame) -> pd.DataFrame:
    base_cols = ["analysis", "dataset_path", "disease_name", "compartment", "donor_id", "disease", "group"]
    wide = modules.pivot_table(
        index=base_cols,
        columns="module",
        values="mean_score",
        aggfunc="mean",
    ).reset_index()
    wide.columns.name = None
    return wide


def build_pairs() -> pd.DataFrame:
    donor = read_tsv(DONOR_SCORES)
    modules = read_tsv(MODULE_SCORES)
    if donor.empty or modules.empty:
        return pd.DataFrame()
    donor = donor[donor["gene"].isin(CANDIDATES)].copy()
    role_map = donor[["analysis", "role"]].drop_duplicates()
    modules = modules.merge(role_map, on="analysis", how="left")
    mwide = module_wide(modules)
    mwide = mwide.merge(role_map, on="analysis", how="left")

    source = donor[donor["role"].ne("myeloid_apc")].copy()
    source = source.rename(
        columns={
            "analysis": "source_analysis",
            "compartment": "source_compartment",
            "role": "source_role",
            "mean_z_vs_controls": "source_gene_z",
            "mean_log_norm": "source_gene_log_norm",
            "detection_fraction": "source_gene_detection_fraction",
        }
    )
    source_modules = mwide.rename(
        columns={
            "analysis": "source_analysis",
            "compartment": "source_compartment",
            "role": "source_role",
        }
    )
    source = source.merge(
        source_modules[
            [
                "source_analysis",
                "donor_id",
                *[col for col in COVARIATE_MODULES if col in source_modules.columns],
            ]
        ].rename(columns={col: f"source_{col}" for col in COVARIATE_MODULES if col in source_modules.columns}),
        on=["source_analysis", "donor_id"],
        how="left",
    )

    target = mwide[mwide["role"].eq("myeloid_apc")].copy()
    target = target.rename(
        columns={
            "analysis": "target_analysis",
            "compartment": "target_compartment",
            "role": "target_role",
        }
    )
    target_module_cols = list(dict.fromkeys([col for col in TARGET_MODULES + COVARIATE_MODULES if col in target.columns]))
    target_cols = [
        "target_analysis",
        "dataset_path",
        "disease_name",
        "donor_id",
        "disease",
        "group",
        "target_compartment",
        "target_role",
        *target_module_cols,
    ]
    target = target[target_cols].copy()
    target = target.rename(columns={col: f"target_{col}" for col in target_module_cols})

    pairs = source.merge(
        target,
        on=["dataset_path", "disease_name", "donor_id", "disease", "group"],
        how="inner",
    )
    return pairs


def run_tests(pairs: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    if pairs.empty:
        return pd.DataFrame()
    rows = []
    for gene in CANDIDATES:
        gene_pairs = pairs[pairs["gene"].eq(gene)].copy()
        for (source_analysis, target_analysis), sub0 in gene_pairs.groupby(["source_analysis", "target_analysis"], observed=True):
            sub0 = sub0.copy()
            for module in TARGET_MODULES:
                target_col = f"target_{module}"
                if target_col not in sub0.columns:
                    continue
                sub = sub0[np.isfinite(pd.to_numeric(sub0[target_col], errors="coerce"))].copy()
                if len(sub) < MIN_PAIRS:
                    continue
                cov_cols = ["case_indicator"]
                sub["case_indicator"] = sub["group"].eq("case").astype(float)
                for cov in COVARIATE_MODULES:
                    for prefix in ["source", "target"]:
                        col = f"{prefix}_{cov}"
                        if col in sub.columns and col != target_col:
                            cov_cols.append(col)
                cov_cols = [col for col in dict.fromkeys(cov_cols) if col in sub.columns]
                covariates, selected_cov_cols, covariate_mode = adaptive_covariates(sub, cov_cols)
                x_raw = pd.to_numeric(sub["source_gene_z"], errors="coerce").to_numpy(float)
                y_raw = pd.to_numeric(sub[target_col], errors="coerce").to_numpy(float)
                x_resid, n_x, x_r2 = residualize(x_raw, covariates)
                y_resid, n_y, y_r2 = residualize(y_raw, covariates)
                raw = linreg(x_raw, y_raw)
                adj = linreg(x_resid, y_resid)
                case_sub = sub[sub["group"].eq("case")]
                case_raw = linreg(
                    pd.to_numeric(case_sub["source_gene_z"], errors="coerce").to_numpy(float),
                    pd.to_numeric(case_sub[target_col], errors="coerce").to_numpy(float),
                )
                first = sub.iloc[0]
                rows.append(
                    {
                        "gene": gene,
                        "focus_candidate": gene in FOCUS,
                        "source_analysis": source_analysis,
                        "target_analysis": target_analysis,
                        "dataset_path": first["dataset_path"],
                        "disease_name": first["disease_name"],
                        "source_compartment": first["source_compartment"],
                        "target_compartment": first["target_compartment"],
                        "target_module": module,
                        "n_pairs": raw["n"],
                        "n_case_pairs": case_raw["n"],
                        "raw_slope": raw["slope"],
                        "raw_r": raw["r"],
                        "raw_p": raw["p"],
                        "raw_spearman_rho": raw["spearman_rho"],
                        "raw_spearman_p": raw["spearman_p"],
                        "adjusted_n": adj["n"],
                        "adjusted_slope": adj["slope"],
                        "adjusted_r": adj["r"],
                        "adjusted_p": adj["p"],
                        "adjusted_spearman_rho": adj["spearman_rho"],
                        "adjusted_spearman_p": adj["spearman_p"],
                        "case_only_slope": case_raw["slope"],
                        "case_only_r": case_raw["r"],
                        "case_only_p": case_raw["p"],
                        "x_covariate_r2": x_r2,
                        "y_covariate_r2": y_r2,
                        "covariates": ";".join(selected_cov_cols),
                        "covariate_mode": covariate_mode,
                    }
                )
    out = pd.DataFrame(rows)
    if not out.empty:
        out["adjusted_positive_nominal"] = (
            (out["adjusted_slope"] > 0)
            & (out["adjusted_p"] < 0.05)
            & (out["adjusted_n"] >= MIN_PAIRS)
        )
        out["adjusted_negative_nominal"] = (
            (out["adjusted_slope"] < 0)
            & (out["adjusted_p"] < 0.05)
            & (out["adjusted_n"] >= MIN_PAIRS)
        )
        out["case_positive_nominal"] = (
            (out["case_only_slope"] > 0)
            & (out["case_only_p"] < 0.05)
            & (out["n_case_pairs"] >= MIN_PAIRS)
        )
        out = out.sort_values(["adjusted_positive_nominal", "adjusted_p", "raw_p"], ascending=[False, True, True])
    return out


def summarize(tests: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for gene in CANDIDATES:
        sub = tests[tests["gene"].eq(gene)].copy() if not tests.empty else pd.DataFrame()
        pos = sub[sub.get("adjusted_positive_nominal", pd.Series(False, index=sub.index))]
        neg = sub[sub.get("adjusted_negative_nominal", pd.Series(False, index=sub.index))]
        case_pos = sub[sub.get("case_positive_nominal", pd.Series(False, index=sub.index))]
        rows.append(
            {
                "gene": gene,
                "focus_candidate": gene in FOCUS,
                "tested_pair_count": int(len(sub)),
                "tested_disease_count": int(sub["disease_name"].nunique()) if not sub.empty else 0,
                "adjusted_positive_pair_count": int(len(pos)),
                "adjusted_positive_disease_count": int(pos["disease_name"].nunique()) if not pos.empty else 0,
                "adjusted_negative_pair_count": int(len(neg)),
                "adjusted_negative_disease_count": int(neg["disease_name"].nunique()) if not neg.empty else 0,
                "case_positive_pair_count": int(len(case_pos)),
                "case_positive_disease_count": int(case_pos["disease_name"].nunique()) if not case_pos.empty else 0,
                "best_adjusted_positive": (
                    pos.sort_values(["adjusted_p", "adjusted_slope"], ascending=[True, False])
                    .head(1)
                    .apply(
                        lambda r: (
                            f"{r['source_analysis']}->{r['target_analysis']}|{r['target_module']}:"
                            f"slope={r['adjusted_slope']:.3g},p={r['adjusted_p']:.3g},n={int(r['adjusted_n'])}"
                        ),
                        axis=1,
                    )
                    .iloc[0]
                    if not pos.empty
                    else ""
                ),
                "top_raw_or_adjusted_tests": (
                    sub.sort_values(["adjusted_p", "raw_p"], ascending=[True, True])
                    .head(5)
                    .apply(
                        lambda r: (
                            f"{r['source_analysis']}->{r['target_analysis']}|{r['target_module']}:"
                            f"adj_slope={r['adjusted_slope']:.3g},adj_p={r['adjusted_p']:.3g},"
                            f"raw_slope={r['raw_slope']:.3g},raw_p={r['raw_p']:.3g}"
                        ),
                        axis=1,
                    )
                    .pipe(lambda s: ";".join(s.tolist()))
                    if not sub.empty
                    else ""
                ),
            }
        )
    out = pd.DataFrame(rows)
    calls = []
    for _, row in out.iterrows():
        if row["tested_pair_count"] == 0:
            calls.append("NO_GO_NO_MATCHED_NICHE_TESTS")
        elif row["adjusted_positive_disease_count"] >= 2 and row["adjusted_negative_disease_count"] == 0:
            calls.append("REOPEN_NICHE_CONTROLLER_FOR_TARGET_SPECIFIC_FORCING")
        elif row["adjusted_positive_disease_count"] >= 1 and row["adjusted_negative_disease_count"] == 0:
            calls.append("PARK_SINGLE_CONTEXT_NICHE_SIGNAL")
        elif row["adjusted_negative_disease_count"] > 0:
            calls.append("NO_GO_DIRECTION_CONFLICTED_NICHE_SIGNAL")
        else:
            calls.append("NO_GO_NO_ADJUSTED_NICHE_CONTROLLER_SIGNAL")
    out["wave104_call"] = calls
    priority = {
        "REOPEN_NICHE_CONTROLLER_FOR_TARGET_SPECIFIC_FORCING": 0,
        "PARK_SINGLE_CONTEXT_NICHE_SIGNAL": 1,
        "NO_GO_DIRECTION_CONFLICTED_NICHE_SIGNAL": 2,
        "NO_GO_NO_ADJUSTED_NICHE_CONTROLLER_SIGNAL": 3,
        "NO_GO_NO_MATCHED_NICHE_TESTS": 4,
    }
    out["wave104_call_priority"] = out["wave104_call"].map(priority).fillna(99).astype(int)
    return out.sort_values(
        ["wave104_call_priority", "adjusted_positive_disease_count", "case_positive_disease_count"],
        ascending=[True, False, False],
    )


def write_report(summary_table: pd.DataFrame, tests: pd.DataFrame, payload: dict[str, Any]) -> None:
    cols = [
        "gene",
        "wave104_call",
        "tested_pair_count",
        "tested_disease_count",
        "adjusted_positive_disease_count",
        "adjusted_negative_disease_count",
        "case_positive_disease_count",
        "best_adjusted_positive",
        "top_raw_or_adjusted_tests",
    ]
    report = f"""# Wave104 Accessible-Survivor Niche-Controller Test

## Bottom Line

Branch call: `{payload["branch_call"]}`.

This test pairs tissue-resident candidate expression with matched-donor
myeloid/APC lipid-lysosomal module scores. It answers the mechanism sidecar's
request directly: whether `SEL1L3` or `FXYD5` behaves like a tissue-niche
controller of myeloid lipid-lysosomal state rather than a marker.

## Candidate Summary

{markdown_table(summary_table[cols], max_rows=20)}

## Strongest Adjusted Tests

{markdown_table(tests.sort_values(["adjusted_p", "raw_p"], ascending=[True, True]).head(20), max_rows=20)}

## Interpretation

An adjusted positive in one context is not enough to reopen a V3 therapeutic
branch. Reopening requires same-direction adjusted positive niche-controller
signal in at least two diseases with no adjusted negative disease.

## Reproducibility

- Script: `{rel(ROOT / "scripts" / "v3_wave104_accessible_survivor_niche_controller_test.py")}`
- Matched pairs: `{rel(OUT / "matched_niche_pairs.tsv")}`
- Tests: `{rel(OUT / "niche_controller_tests.tsv")}`
- Summary: `{rel(OUT / "niche_controller_summary.tsv")}`
- Seed: `{SEED}`
"""
    (OUT / "REPORT.md").write_text(report, encoding="utf-8")


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    pairs = build_pairs()
    pairs.to_csv(OUT / "matched_niche_pairs.tsv", sep="\t", index=False)
    tests = run_tests(pairs)
    summary_table = summarize(tests)

    w102 = read_tsv(W102)
    if not w102.empty:
        keep = [
            col
            for col in [
                "gene",
                "wave102_call",
                "raw_positive_disease_count",
                "retained_positive_disease_count",
                "strict_core_covariate_surviving_disease_count",
                "core_all_multivariable_surviving_disease_count",
            ]
            if col in w102.columns
        ]
        summary_table = summary_table.merge(w102[keep], on="gene", how="left")

    tests.to_csv(OUT / "niche_controller_tests.tsv", sep="\t", index=False)
    summary_table.to_csv(OUT / "niche_controller_summary.tsv", sep="\t", index=False)

    reopened = summary_table[
        summary_table["wave104_call"].eq("REOPEN_NICHE_CONTROLLER_FOR_TARGET_SPECIFIC_FORCING")
    ]
    payload = {
        "random_seed": SEED,
        "branch_call": "REOPEN_ACCESSIBLE_SURVIVOR_NICHE_CONTROLLER"
        if not reopened.empty
        else "NO_REOPEN_ACCESSIBLE_SURVIVOR_NICHE_CONTROLLER",
        "n_pairs": int(len(pairs)),
        "n_tests": int(len(tests)),
        "call_counts": summary_table["wave104_call"].value_counts().to_dict(),
        "top_candidate": clean(summary_table.iloc[0]["gene"]) if not summary_table.empty else "",
        "top_candidate_call": clean(summary_table.iloc[0]["wave104_call"]) if not summary_table.empty else "",
        "inputs": {
            "donor_scores": rel(DONOR_SCORES),
            "module_scores": rel(MODULE_SCORES),
            "wave102": rel(W102),
        },
        "guardrail": (
            "Matched-donor niche correlation is not causal and can still reflect "
            "shared tissue severity, medication, cell composition, or batch. "
            "It is used only as a forcing test for target-specific follow-up."
        ),
    }
    write_json(OUT / "summary.json", payload)
    write_report(summary_table, tests, payload)


if __name__ == "__main__":
    main()
