#!/usr/bin/env python3
"""Package-aware cross-cohort synthesis of the V53 microglia state effect."""

from __future__ import annotations

import json
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.stats import chi2, norm


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis/v53_microglia_cross_cohort_meta"
MACNAIR = ROOT / "analysis/v53_ms_microglia_independent_cohort_scout"
GSE = ROOT / "analysis/v53_ms_microglia_age_region_robustness/patient_equal_scores.tsv"


def design(frame: pd.DataFrame, study_fixed_effects: bool) -> tuple[np.ndarray, list[str]]:
    age = frame["age"].to_numpy(dtype=float)
    age_z = (age - age.mean()) / age.std(ddof=0)
    columns = [
        np.ones(len(frame)),
        frame["disease_binary"].to_numpy(dtype=float),
        age_z,
        age_z**2,
        frame["sex_male"].to_numpy(dtype=float),
    ]
    names = ["intercept", "disease_binary", "age_z", "age_z_squared", "sex_male"]
    if study_fixed_effects and frame["study"].nunique() > 1:
        for study in sorted(frame["study"].unique())[1:]:
            columns.append(frame["study"].eq(study).to_numpy(dtype=float))
            names.append(f"study_{study}")
    matrix = np.column_stack(columns)
    if np.linalg.matrix_rank(matrix) != matrix.shape[1]:
        raise ValueError(f"rank-deficient design: {names}")
    return matrix, names


def adjusted_effect(
    cohort: str,
    package: str,
    frame: pd.DataFrame,
    study_fixed_effects: bool,
) -> dict[str, object]:
    y = frame["score"].to_numpy(dtype=float)
    y = (y - y.mean()) / y.std(ddof=0)
    matrix, names = design(frame, study_fixed_effects)
    index = names.index("disease_binary")
    model = sm.OLS(y, matrix).fit(cov_type="HC3")
    ci = model.conf_int()[index]
    return {
        "cohort": cohort,
        "package_family": package,
        "n_donors": len(frame),
        "n_ms": int(frame.disease_binary.sum()),
        "n_control": int((1 - frame.disease_binary).sum()),
        "adjusted_standardized_beta": float(model.params[index]),
        "hc3_se": float(model.bse[index]),
        "hc3_ci_low": float(ci[0]),
        "hc3_ci_high": float(ci[1]),
        "hc3_p": float(model.pvalues[index]),
        "study_fixed_effects": study_fixed_effects and frame.study.nunique() > 1,
    }


def load_effects() -> pd.DataFrame:
    gse = pd.read_csv(GSE, sep="\t")
    gse["score"] = gse["receptor_cd44_cxcr4"]
    gse["study"] = "GSE111972"

    rows = [adjusted_effect("GSE111972", "GEO_GSE111972", gse, False)]
    for cohort in ["validation", "discovery"]:
        frame = pd.read_csv(MACNAIR / f"macnair_{cohort}/donor_scores.tsv", sep="\t")
        frame["age"] = frame["age_at_death"]
        frame["score"] = frame["receptor_cd44_cxcr4"]
        rows.append(
            adjusted_effect(
                f"Macnair_{cohort}",
                "zenodo_8338963",
                frame,
                study_fixed_effects=True,
            )
        )
    return pd.DataFrame(rows)


def pooled(effect: np.ndarray, variance: np.ndarray, random: bool) -> dict[str, float]:
    fixed_weights = 1.0 / variance
    fixed_mean = float(np.sum(fixed_weights * effect) / np.sum(fixed_weights))
    q = float(np.sum(fixed_weights * (effect - fixed_mean) ** 2))
    df = len(effect) - 1
    c = float(np.sum(fixed_weights) - np.sum(fixed_weights**2) / np.sum(fixed_weights))
    tau2 = max(0.0, (q - df) / c) if random and c > 0 else 0.0
    weights = 1.0 / (variance + tau2)
    mean = float(np.sum(weights * effect) / np.sum(weights))
    se = float(np.sqrt(1.0 / np.sum(weights)))
    return {
        "effect": mean,
        "se": se,
        "ci_low": mean - 1.96 * se,
        "ci_high": mean + 1.96 * se,
        "normal_two_sided_p": float(2 * norm.sf(abs(mean / se))),
        "q": q,
        "q_df": df,
        "q_p": float(chi2.sf(q, df)) if df > 0 else float("nan"),
        "i2_percent": max(0.0, (q - df) / q * 100.0) if q > 0 and df > 0 else 0.0,
        "tau2": tau2,
    }


def exact_sign_p(effects: np.ndarray) -> float:
    observed = abs(float(np.mean(effects)))
    null = []
    for signs in product([-1.0, 1.0], repeat=len(effects)):
        null.append(abs(float(np.mean(effects * np.asarray(signs)))))
    return float(np.mean(np.asarray(null) >= observed - 1e-12))


def package_sensitivity(effects: pd.DataFrame) -> pd.DataFrame:
    gse = effects[effects.package_family.eq("GEO_GSE111972")].iloc[0]
    mac = effects[effects.package_family.eq("zenodo_8338963")].copy()
    if len(mac) != 2:
        raise ValueError("expected exactly two Macnair partitions")
    mac_effect = float(mac.adjusted_standardized_beta.mean())
    v1, v2 = (mac.hc3_se.to_numpy(dtype=float) ** 2).tolist()
    rows = []
    for rho in np.linspace(0.0, 1.0, 5):
        mac_variance = (v1 + v2 + 2 * rho * np.sqrt(v1 * v2)) / 4.0
        result = pooled(
            np.asarray([float(gse.adjusted_standardized_beta), mac_effect]),
            np.asarray([float(gse.hc3_se) ** 2, mac_variance]),
            random=False,
        )
        rows.append(
            {
                "assumed_macnair_partition_correlation": rho,
                "macnair_equal_partition_effect": mac_effect,
                "macnair_package_se": np.sqrt(mac_variance),
                "pooled_two_package_effect": result["effect"],
                "pooled_two_package_se": result["se"],
                "pooled_two_package_ci_low": result["ci_low"],
                "pooled_two_package_ci_high": result["ci_high"],
                "pooled_two_package_normal_p": result["normal_two_sided_p"],
                "two_package_exact_sign_p": exact_sign_p(
                    np.asarray([float(gse.adjusted_standardized_beta), mac_effect])
                ),
            }
        )
    return pd.DataFrame(rows)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    effects = load_effects()
    betas = effects.adjusted_standardized_beta.to_numpy(dtype=float)
    variances = effects.hc3_se.to_numpy(dtype=float) ** 2
    fixed = pooled(betas, variances, random=False)
    random = pooled(betas, variances, random=True)

    leave_one_out = []
    for omitted in effects.cohort:
        retained = effects[~effects.cohort.eq(omitted)]
        result = pooled(
            retained.adjusted_standardized_beta.to_numpy(dtype=float),
            retained.hc3_se.to_numpy(dtype=float) ** 2,
            random=True,
        )
        leave_one_out.append({"omitted_cohort": omitted, **result})
    leave_one_out_frame = pd.DataFrame(leave_one_out)
    package = package_sensitivity(effects)

    summary = {
        "purpose": "Cross-cohort synthesis of a pre-existing frozen score; not new discovery",
        "n_analyzed_partitions": len(effects),
        "n_deposition_packages": int(effects.package_family.nunique()),
        "all_partition_effects_positive": bool((betas > 0).all()),
        "three_partition_fixed_effect": fixed,
        "three_partition_random_effect": random,
        "three_partition_exact_sign_p": exact_sign_p(betas),
        "minimum_leave_one_partition_out_random_effect": float(
            leave_one_out_frame.effect.min()
        ),
        "package_correlation_sensitivity_min_ci_low": float(
            package.pooled_two_package_ci_low.min()
        ),
        "package_correlation_sensitivity_max_p": float(
            package.pooled_two_package_normal_p.max()
        ),
        "two_package_exact_sign_p": float(package.two_package_exact_sign_p.iloc[0]),
        "verdict": "POSITIVE_CROSS_SOURCE_EFFECT_WITH_HETEROGENEITY_AND_LOW_SOURCE_FAMILY_COUNT",
        "boundary": (
            "All estimates are donor-level standardized and covariate-adjusted. The two "
            "Macnair partitions share one package and may be dependent; their correlation "
            "is swept from 0 to 1. Normal-theory pooled intervals remain positive, but the "
            "exact sign test has only two independent package signs and cannot establish "
            "meta-significance. Individual frozen wild-null tests remain the primary evidence."
        ),
    }

    effects.to_csv(OUT / "cohort_adjusted_standardized_effects.tsv", sep="\t", index=False)
    leave_one_out_frame.to_csv(OUT / "leave_one_partition_out.tsv", sep="\t", index=False)
    package.to_csv(OUT / "macnair_dependence_sensitivity.tsv", sep="\t", index=False)
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")

    report = [
        "# V53 Cross-Cohort CD44/CXCR4 State Synthesis",
        "",
        f"Verdict: **{summary['verdict']}**.",
        "",
        "## Commensurate Effects",
        "",
        "Each donor-level receptor score was standardized within cohort, then fit with the",
        "same disease, age, quadratic-age, and sex model; the validation composite also",
        "includes deposited study fixed effects. All three adjusted standardized effects are",
        "positive:",
        "",
        "| partition | adjusted standardized beta | HC3 95% CI |",
        "|---|---:|---:|",
    ]
    for row in effects.itertuples(index=False):
        report.append(
            f"| {row.cohort} | `{row.adjusted_standardized_beta:.3f}` | "
            f"`{row.hc3_ci_low:.3f}` to `{row.hc3_ci_high:.3f}` |"
        )
    report.extend(
        [
            "",
            "## Heterogeneity And Dependence",
            "",
            f"The conventional three-partition random-effects estimate is `{random['effect']:.3f}`",
            f"(95% CI `{random['ci_low']:.3f}` to `{random['ci_high']:.3f}`), with",
            f"I2 `{random['i2_percent']:.1f}%` and tau2 `{random['tau2']:.3f}`. This is a",
            "sensitivity only because the two Macnair partitions share one deposition package.",
            "",
            "The package-aware analysis gives the Macnair partitions equal weight, varies their",
            "unknown correlation from 0 to 1, and pools that package estimate with GSE111972.",
            f"Across the full correlation sweep, the lowest normal-theory CI bound is",
            f"`{summary['package_correlation_sensitivity_min_ci_low']:.3f}` and the largest p is",
            f"`{summary['package_correlation_sensitivity_max_p']:.4g}`. However, the exact",
            f"two-package sign test is `p={summary['two_package_exact_sign_p']:.3f}`: two source",
            "families are too few for an independent meta-significance claim.",
            "",
            "## Interpretation",
            "",
            "The direction is not driven by one analyzed partition, and normal-theory estimates",
            "remain positive under worst-case Macnair dependence. Effect magnitude is strongly",
            "heterogeneous, and the source-family count is small. The defensible result remains a",
            "replicated, quality-qualified state association. It is not a causal receptor",
            "mechanism, stage-specific marker, monitoring rule, therapeutic direction, or target.",
        ]
    )
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
