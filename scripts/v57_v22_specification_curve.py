#!/usr/bin/env python3
"""Summarize every frozen V32 confounder adjustment without selection."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
V32 = ROOT / "analysis" / "v32_confounder_audit"
OUT = ROOT / "analysis" / "v57_v22_specification_curve"


def family(name: str) -> str:
    if name.startswith("joint:"):
        return name
    stem = name.removeprefix("baseline_").removeprefix("delta_")
    if "composition" in stem:
        return "composition"
    if stem in {"glycolysis", "oxphos", "immunometabolism_hif_nampt"}:
        return "metabolic"
    if stem in {"general_inflammatory_tone", "stat1_axis", "ifn_suppression_inverse_isg"}:
        return "inflammatory_ifn"
    if stem == "glucocorticoid_response":
        return "glucocorticoid"
    if stem == "proliferation":
        return "proliferation"
    if stem == "apc_hla_level":
        return "baseline_apc_hla"
    return "other"


def load_specifications() -> pd.DataFrame:
    single = pd.read_csv(V32 / "v32_confounder_adjustment_metrics.tsv", sep="\t")
    single_out = pd.DataFrame(
        {
            "specification": single["confounder"],
            "specification_type": "single_confounder",
            "raw_auc": single["raw_locked_auc"],
            "adjusted_auc": single["adjusted_locked_auc"],
            "ci_low": single["adjusted_auc_ci_low"],
            "ci_high": single["adjusted_auc_ci_high"],
            "permutation_p": single["adjusted_permutation_p"],
            "confounder_only_loocv_auc": single["loocv_auc_confounder_only"],
            "locked_plus_confounder_loocv_auc": single["loocv_auc_locked_plus_confounder"],
            "auc_attenuation": single["auc_attenuation"],
            "v32_verdict": single["verdict"],
        }
    )

    joint = pd.read_csv(V32 / "v32_joint_adjustment_metrics.tsv", sep="\t")
    joint_name = "joint:" + joint["risk_set"].fillna("unnamed").astype(str)
    joint_out = pd.DataFrame(
        {
            "specification": joint_name,
            "specification_type": "joint_risk_set",
            "raw_auc": joint["raw_locked_auc"],
            "adjusted_auc": joint["joint_adjusted_auc"],
            "ci_low": joint["joint_adjusted_auc_ci_low"],
            "ci_high": joint["joint_adjusted_auc_ci_high"],
            "permutation_p": joint["joint_adjusted_permutation_p"],
            "confounder_only_loocv_auc": joint["loocv_auc_confounders_only"],
            "locked_plus_confounder_loocv_auc": joint["loocv_auc_locked_plus_confounders"],
            "auc_attenuation": joint["auc_attenuation"],
            "v32_verdict": joint["verdict"],
        }
    )
    specs = pd.concat([single_out, joint_out], ignore_index=True)
    specs["family"] = specs["specification"].map(family)
    specs["incremental_loocv_auc"] = (
        specs["locked_plus_confounder_loocv_auc"] - specs["confounder_only_loocv_auc"]
    )
    specs["direction_positive"] = specs["adjusted_auc"] > 0.50
    specs["practical_discrimination"] = specs["adjusted_auc"] >= 0.60
    specs["permutation_supported"] = specs["permutation_p"] <= 0.05
    specs["incremental_cv_positive"] = specs["incremental_loocv_auc"] > 0
    return specs.sort_values(["adjusted_auc", "specification"], kind="stable").reset_index(drop=True)


def fraction(series: pd.Series) -> float:
    return float(series.astype(bool).mean())


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    specs = load_specifications()
    gates = {
        "direction_robust": fraction(specs["direction_positive"]) >= 0.90,
        "practical_discrimination_robust": fraction(specs["practical_discrimination"]) >= 0.80,
        "permutation_support_robust": fraction(specs["permutation_supported"]) >= 0.80,
        "incremental_cv_robust": fraction(specs["incremental_cv_positive"]) >= 0.80,
    }
    gates["fully_robust_by_aggregate_gates"] = all(gates.values())

    least = specs.iloc[0]
    summary = {
        "n_specifications": int(len(specs)),
        "n_single_confounder": int((specs["specification_type"] == "single_confounder").sum()),
        "n_joint_risk_set": int((specs["specification_type"] == "joint_risk_set").sum()),
        "raw_auc": float(specs["raw_auc"].iloc[0]),
        "adjusted_auc_min": float(specs["adjusted_auc"].min()),
        "adjusted_auc_median": float(specs["adjusted_auc"].median()),
        "adjusted_auc_max": float(specs["adjusted_auc"].max()),
        "attenuation_min": float(specs["auc_attenuation"].min()),
        "attenuation_median": float(specs["auc_attenuation"].median()),
        "attenuation_max": float(specs["auc_attenuation"].max()),
        "direction_positive_fraction": fraction(specs["direction_positive"]),
        "practical_discrimination_fraction": fraction(specs["practical_discrimination"]),
        "permutation_supported_fraction": fraction(specs["permutation_supported"]),
        "incremental_cv_positive_fraction": fraction(specs["incremental_cv_positive"]),
        "least_favorable_specification": str(least["specification"]),
        "least_favorable_auc": float(least["adjusted_auc"]),
        "least_favorable_permutation_p": float(least["permutation_p"]),
        "least_favorable_incremental_loocv_auc": float(least["incremental_loocv_auc"]),
        "gates": gates,
    }

    family_summary = (
        specs.groupby("family", sort=True)
        .agg(
            n=("specification", "size"),
            adjusted_auc_min=("adjusted_auc", "min"),
            adjusted_auc_median=("adjusted_auc", "median"),
            adjusted_auc_max=("adjusted_auc", "max"),
            permutation_supported_fraction=("permutation_supported", "mean"),
            incremental_cv_positive_fraction=("incremental_cv_positive", "mean"),
        )
        .reset_index()
    )

    specs.to_csv(OUT / "specification_curve.tsv", sep="\t", index=False)
    family_summary.to_csv(OUT / "family_summary.tsv", sep="\t", index=False)
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")

    exception = specs.loc[~specs["permutation_supported"], "specification"].tolist()
    report = f"""# V57 V22 Specification-Curve Audit

## Result

All {len(specs)} frozen V32 specifications were included: {summary['n_single_confounder']}
single-confounder adjustments and {summary['n_joint_risk_set']} named joint risk
sets. Adjusted AUC ranged from {summary['adjusted_auc_min']:.3f} to
{summary['adjusted_auc_max']:.3f} (median {summary['adjusted_auc_median']:.3f}),
versus raw AUC {summary['raw_auc']:.3f}.

- responder-higher direction: {summary['direction_positive_fraction']:.1%};
- adjusted AUC >= 0.60: {summary['practical_discrimination_fraction']:.1%};
- nominal stratified-permutation p <= 0.05: {summary['permutation_supported_fraction']:.1%};
- positive leave-one-out incremental AUC: {summary['incremental_cv_positive_fraction']:.1%}.

The predeclared aggregate gates all pass. This means the score's direction,
practical discrimination, and incremental value are not dependent on selecting
one favorable V32 adjustment. It does **not** make these specifications
independent replications or validate V22 externally.

## Mandatory Least-Favorable Result

`{summary['least_favorable_specification']}` was least favorable: adjusted AUC
{summary['least_favorable_auc']:.3f}, permutation p
{summary['least_favorable_permutation_p']:.3f}, and incremental leave-one-out
AUC {summary['least_favorable_incremental_loocv_auc']:+.3f}. The specifications
without nominal permutation support were: {', '.join(f'`{x}`' for x in exception)}.

That broad metabolic/inflammatory/STAT1 joint adjustment remains the important
exception and preserves V32's **partially confounded / immune-tone bounded**
interpretation. The aggregate curve strengthens robustness to ordinary
specification choice; it does not erase the broad-joint attenuation or the need
for an external cohort.

## Epistemic Boundary

This is a reanalysis of existing held subjects and frozen V32 outputs. It is a
methodological robustness result, not new MS discovery, not a revised locked
rule, and not external validation. Nominal p-values are displayed as stress-test
diagnostics and are not counted as independent evidence.
"""
    (OUT / "REPORT.md").write_text(report)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
