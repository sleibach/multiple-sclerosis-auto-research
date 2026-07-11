#!/usr/bin/env python3
"""Stress-test the provisional GSE111972 CD44/CXCR4 state association."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import statsmodels.api as sm


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "analysis/v53_ms_microglia_receptor_decoupling/sample_module_scores.tsv"
OUT = ROOT / "analysis/v53_ms_microglia_age_region_robustness"
OUTCOME = "receptor_cd44_cxcr4"
SEED = 53506
N_WILD_BOOTSTRAP = 100_000


def write_tsv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(rows[0]),
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def design_matrix(frame: pd.DataFrame, quadratic_age: bool, interaction: bool) -> np.ndarray:
    age = frame["age"].to_numpy(dtype=float)
    age_z = (age - np.mean(age)) / np.std(age)
    disease = frame["disease_binary"].to_numpy(dtype=float)
    region = frame.get("region_white", pd.Series(0.0, index=frame.index)).to_numpy(dtype=float)
    columns = [
        np.ones(len(frame)),
        disease,
        region,
        age_z,
        frame["sex_male"].to_numpy(dtype=float),
    ]
    if quadratic_age:
        columns.append(age_z**2)
    if interaction:
        columns.append(disease * region)
    return np.column_stack(columns)


def reduced_design(frame: pd.DataFrame, quadratic_age: bool, interaction: bool) -> np.ndarray:
    full = design_matrix(frame, quadratic_age, interaction)
    # Remove disease and disease-by-region; the wild null is no disease effect.
    keep = [0, 2, 3, 4]
    if quadratic_age:
        keep.append(5)
    return full[:, keep]


def wild_test(
    frame: pd.DataFrame,
    quadratic_age: bool,
    interaction: bool,
    cluster_column: str,
    rng: np.random.Generator,
) -> tuple[float, float, float, float]:
    outcome = frame[OUTCOME].to_numpy(dtype=float)
    full = design_matrix(frame, quadratic_age, interaction)
    reduced = reduced_design(frame, quadratic_age, interaction)
    codes, _ = pd.factorize(frame[cluster_column], sort=True)
    full_pinv = np.linalg.pinv(full)
    observed = full_pinv @ outcome
    fitted = reduced @ (np.linalg.pinv(reduced) @ outcome)
    residual = outcome - fitted
    exceed = 0
    completed = 0
    n_clusters = int(codes.max()) + 1
    while completed < N_WILD_BOOTSTRAP:
        batch = min(5_000, N_WILD_BOOTSTRAP - completed)
        signs = rng.choice([-1.0, 1.0], size=(batch, n_clusters))[:, codes]
        synthetic = fitted[None, :] + signs * residual[None, :]
        betas = synthetic @ full_pinv.T
        exceed += int(np.sum(np.abs(betas[:, 1]) >= abs(observed[1])))
        completed += batch
    model = sm.OLS(outcome, full).fit(cov_type="HC3")
    interaction_beta = float(observed[-1]) if interaction else float("nan")
    interaction_p = float(model.pvalues[-1]) if interaction else float("nan")
    return (
        float(observed[1]),
        (1 + exceed) / (N_WILD_BOOTSTRAP + 1),
        interaction_beta,
        interaction_p,
    )


def disease_beta(frame: pd.DataFrame, quadratic_age: bool) -> float:
    design = design_matrix(frame, quadratic_age, interaction=False)
    return float((np.linalg.pinv(design) @ frame[OUTCOME].to_numpy(dtype=float))[1])


def main() -> int:
    sample = pd.read_csv(INPUT, sep="\t")
    sample["disease_binary"] = sample["disease"].eq("MS").astype(int)
    sample["region_white"] = sample["region"].eq("white_matter").astype(int)
    patient = (
        sample.groupby("patient", as_index=False)
        .agg(
            disease_binary=("disease_binary", "first"),
            age=("age", "first"),
            sex_male=("sex_male", "first"),
            receptor_cd44_cxcr4=(OUTCOME, "mean"),
            n_regions=("region", "nunique"),
        )
    )
    patient["region_white"] = 0.0
    patient["cluster"] = patient["patient"]
    common_low = max(
        patient.loc[patient["disease_binary"].eq(1), "age"].min(),
        patient.loc[patient["disease_binary"].eq(0), "age"].min(),
    )
    common_high = min(
        patient.loc[patient["disease_binary"].eq(1), "age"].max(),
        patient.loc[patient["disease_binary"].eq(0), "age"].max(),
    )
    common = patient[patient["age"].between(common_low, common_high)].copy()

    rng = np.random.default_rng(SEED)
    variants = []
    for name, frame, quadratic, interaction, cluster in [
        ("patient_equal_linear_age", patient, False, False, "cluster"),
        ("patient_equal_quadratic_age", patient, True, False, "cluster"),
        ("patient_equal_common_age_support", common, False, False, "cluster"),
        ("sample_level_region_interaction", sample, False, True, "patient"),
    ]:
        beta, p_value, interaction_beta, interaction_p = wild_test(
            frame, quadratic, interaction, cluster, rng
        )
        variants.append(
            {
                "variant": name,
                "n_rows": len(frame),
                "n_patients": frame[cluster].nunique(),
                "quadratic_age": quadratic,
                "region_interaction": interaction,
                "disease_beta": beta,
                "wild_cluster_two_sided_p": p_value,
                "disease_by_region_beta": interaction_beta,
                "disease_by_region_hc3_p": interaction_p,
            }
        )

    loo_rows = []
    for omitted in patient["patient"]:
        retained = patient[~patient["patient"].eq(omitted)].copy()
        loo_rows.append(
            {
                "omitted_patient": omitted,
                "quadratic_age_disease_beta": disease_beta(retained, quadratic_age=True),
            }
        )

    regional = []
    for region, sub in sample.groupby("region"):
        regional.append(
            {
                "region": region,
                "n_samples": len(sub),
                "n_ms": int(sub["disease_binary"].sum()),
                "n_control": int((1 - sub["disease_binary"]).sum()),
                "raw_ms_minus_control": float(
                    sub.loc[sub["disease_binary"].eq(1), OUTCOME].mean()
                    - sub.loc[sub["disease_binary"].eq(0), OUTCOME].mean()
                ),
            }
        )

    by_variant = {row["variant"]: row for row in variants}
    quadratic = by_variant["patient_equal_quadratic_age"]
    overlap = by_variant["patient_equal_common_age_support"]
    interaction = by_variant["sample_level_region_interaction"]
    min_loo_beta = min(float(row["quadratic_age_disease_beta"]) for row in loo_rows)
    gate_components = {
        "patient_equal_quadratic_beta_positive_p_le_0_10": (
            quadratic["disease_beta"] > 0
            and quadratic["wild_cluster_two_sided_p"] <= 0.10
        ),
        "common_age_support_beta_positive_p_le_0_10": (
            overlap["disease_beta"] > 0
            and overlap["wild_cluster_two_sided_p"] <= 0.10
        ),
        "all_leave_one_patient_out_betas_positive": min_loo_beta > 0,
        "raw_effect_positive_in_both_regions": all(
            float(row["raw_ms_minus_control"]) > 0 for row in regional
        ),
        "no_detected_disease_by_region_interaction_p_gt_0_10": (
            interaction["disease_by_region_hc3_p"] > 0.10
        ),
    }
    robust = all(gate_components.values())
    age_by_group = patient.groupby("disease_binary")["age"].agg(["mean", "std", "min", "max"])
    pooled_age_sd = float(
        np.sqrt(
            (
                (len(patient[patient.disease_binary.eq(1)]) - 1)
                * age_by_group.loc[1, "std"] ** 2
                + (len(patient[patient.disease_binary.eq(0)]) - 1)
                * age_by_group.loc[0, "std"] ** 2
            )
            / (len(patient) - 2)
        )
    )
    age_smd = float(
        (age_by_group.loc[1, "mean"] - age_by_group.loc[0, "mean"]) / pooled_age_sd
    )
    summary = {
        "purpose": "V53 age, repeated-region, and influence sensitivity for GSE111972 CD44/CXCR4",
        "n_samples": len(sample),
        "n_patients": len(patient),
        "age_standardized_mean_difference_ms_minus_control": age_smd,
        "common_age_support": [float(common_low), float(common_high)],
        "n_patients_in_common_age_support": len(common),
        "n_wild_cluster_bootstrap_replicates_per_variant": N_WILD_BOOTSTRAP,
        "seed": SEED,
        "minimum_leave_one_patient_out_quadratic_beta": min_loo_beta,
        "gate_components": gate_components,
        "robustness_gate_pass": robust,
        "verdict": (
            "MS_MICROGLIA_CD44_CXCR4_ASSOCIATION_SURVIVES_AGE_REGION_INFLUENCE_GATE"
            if robust
            else "MS_MICROGLIA_CD44_CXCR4_ASSOCIATION_FAILS_AGE_REGION_INFLUENCE_GATE"
        ),
        "boundary": "Single-cohort robustness only; no causal, replication, drug-direction, or target claim.",
    }

    OUT.mkdir(parents=True, exist_ok=True)
    write_tsv(OUT / "model_variants.tsv", variants)
    write_tsv(OUT / "leave_one_patient_out.tsv", loo_rows)
    write_tsv(OUT / "regional_effects.tsv", regional)
    patient.to_csv(OUT / "patient_equal_scores.tsv", sep="\t", index=False)
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    report = [
        "# V53 MS Microglia Age/Region Robustness",
        "",
        f"Verdict: **{summary['verdict']}**.",
        "",
        f"The patient-level age imbalance is SMD `{age_smd:.3f}` (MS minus control).",
        f"Patient-equal quadratic-age beta is `{quadratic['disease_beta']:.3f}`",
        f"(wild p `{quadratic['wild_cluster_two_sided_p']:.4f}`); restriction to the",
        f"common age range `{common_low:.0f}-{common_high:.0f}` gives beta",
        f"`{overlap['disease_beta']:.3f}` (p `{overlap['wild_cluster_two_sided_p']:.4f}`).",
        f"The minimum leave-one-patient-out quadratic beta is `{min_loo_beta:.3f}`.",
        "",
        f"Disease-by-region interaction HC3 p is `{interaction['disease_by_region_hc3_p']:.4f}`",
        "and raw effects are required to remain positive in both regions. Passing this gate",
        "supports robustness of the single-cohort state association only; it cannot establish",
        "causality, independent replication, therapeutic direction, or a target.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
