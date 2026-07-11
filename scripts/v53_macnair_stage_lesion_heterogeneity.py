#!/usr/bin/env python3
"""Test stage and lesion context for the replicated Macnair receptor state."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import statsmodels.api as sm


ROOT = Path(__file__).resolve().parents[1]
BASE_INPUT = ROOT / "analysis/v53_ms_microglia_independent_cohort_scout"
BASE_OUT = ROOT / "analysis/v53_macnair_stage_lesion_heterogeneity"
OUTCOME = "receptor_cd44_cxcr4"
N_NULL = 100_000
SEED = 53531


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cohort", choices=["discovery", "validation"], required=True)
    return parser.parse_args()


def bh(rows: list[dict[str, Any]], p_field: str = "wild_two_sided_p") -> None:
    if not rows:
        return
    values = np.array([float(row[p_field]) for row in rows])
    order = np.argsort(values)
    adjusted = np.empty(len(values), dtype=float)
    running = 1.0
    for rank in range(len(values) - 1, -1, -1):
        index = order[rank]
        running = min(running, values[index] * len(values) / (rank + 1))
        adjusted[index] = running
    for row, value in zip(rows, adjusted, strict=True):
        row["bh_q"] = float(value)


def donor_average(frame: pd.DataFrame, group_name: str, group_value: int) -> pd.DataFrame:
    if frame.empty:
        return frame
    donor = (
        frame.groupby("canonical_donor", as_index=False)
        .agg(
            diagnosis=("diagnosis", "first"),
            study=("study", "first"),
            sex=("sex", "first"),
            age_at_death=("age_at_death", "first"),
            n_microglia=("n_microglia", "sum"),
            receptor_cd44_cxcr4=(OUTCOME, "mean"),
            n_samples=("sample_id", "nunique"),
        )
    )
    donor[group_name] = group_value
    donor["sex_male"] = donor.sex.eq("M").astype(int)
    donor["log_n_microglia"] = np.log1p(donor.n_microglia)
    return donor


def design(frame: pd.DataFrame) -> np.ndarray:
    age = frame.age_at_death.to_numpy(dtype=float)
    age_z = (age - age.mean()) / age.std(ddof=0)
    log_cells = frame.log_n_microglia.to_numpy(dtype=float)
    log_cells_z = (log_cells - log_cells.mean()) / log_cells.std(ddof=0)
    matrix = np.column_stack(
        [
            np.ones(len(frame)),
            frame.test_group.to_numpy(dtype=float),
            age_z,
            age_z**2,
            frame.sex_male.to_numpy(dtype=float),
            log_cells_z,
        ]
    )
    studies = sorted(frame.study.unique())
    if len(studies) > 1:
        matrix = np.column_stack(
            [matrix]
            + [frame.study.eq(study).to_numpy(dtype=float) for study in studies[1:]]
        )
    if np.linalg.matrix_rank(matrix) != matrix.shape[1] or np.linalg.cond(matrix) > 1e6:
        raise ValueError("invalid binary-test design")
    return matrix


def binary_wild_test(frame: pd.DataFrame, seed_offset: int) -> dict[str, float]:
    full = design(frame)
    reduced = np.delete(full, 1, axis=1)
    y = frame[OUTCOME].to_numpy(dtype=float)
    full_pinv = np.linalg.solve(np.einsum("ni,nj->ij", full, full), full.T)
    reduced_pinv = np.linalg.solve(np.einsum("ni,nj->ij", reduced, reduced), reduced.T)
    observed = np.einsum("ij,j->i", full_pinv, y)
    reduced_coefficients = np.einsum("ij,j->i", reduced_pinv, y)
    fitted = np.einsum("ij,j->i", reduced, reduced_coefficients)
    residual = y - fitted
    weights = full_pinv[1]
    rng = np.random.default_rng(SEED + seed_offset)
    exceed = 0
    completed = 0
    while completed < N_NULL:
        batch = min(5_000, N_NULL - completed)
        signs = rng.choice([-1.0, 1.0], size=(batch, len(frame)))
        synthetic = fitted[None, :] + signs * residual[None, :]
        betas = np.add.reduce(synthetic * weights[None, :], axis=1)
        exceed += int(np.sum(np.abs(betas) >= abs(observed[1])))
        completed += batch
    model = sm.OLS(y, full).fit(cov_type="HC3")
    ci = model.conf_int()[1]
    positive = frame.loc[frame.test_group.eq(1), OUTCOME].to_numpy(dtype=float)
    reference = frame.loc[frame.test_group.eq(0), OUTCOME].to_numpy(dtype=float)
    pooled = np.sqrt(
        ((len(positive) - 1) * positive.var(ddof=1) + (len(reference) - 1) * reference.var(ddof=1))
        / (len(positive) + len(reference) - 2)
    )
    return {
        "disease_or_context_beta": float(observed[1]),
        "hc3_ci_low": float(ci[0]),
        "hc3_ci_high": float(ci[1]),
        "hc3_p": float(model.pvalues[1]),
        "wild_two_sided_p": (1 + exceed) / (N_NULL + 1),
        "standardized_difference": float((positive.mean() - reference.mean()) / pooled),
    }


def sign_flip_test(differences: np.ndarray, seed_offset: int) -> float:
    observed = abs(float(differences.mean()))
    rng = np.random.default_rng(SEED + seed_offset)
    exceed = 0
    completed = 0
    while completed < N_NULL:
        batch = min(10_000, N_NULL - completed)
        signs = rng.choice([-1.0, 1.0], size=(batch, len(differences)))
        null_means = np.abs(np.mean(signs * differences[None, :], axis=1))
        exceed += int(np.sum(null_means >= observed))
        completed += batch
    return (1 + exceed) / (N_NULL + 1)


def main() -> None:
    args = parse_args()
    input_path = BASE_INPUT / f"macnair_{args.cohort}/sample_scores.tsv"
    outdir = BASE_OUT / args.cohort
    sample = pd.read_csv(input_path, sep="\t")
    sample = sample[sample.study.eq(sample.selected_source)].copy()
    wm = sample[sample.matter.eq("WM")].copy()
    control_wm = donor_average(wm[wm.disease_binary.eq(0)], "test_group", 0)

    stage_rows: list[dict[str, Any]] = []
    for offset, stage in enumerate(["PPMS", "SPMS", "RRMS"]):
        cases = donor_average(wm[wm.diagnosis.eq(stage)], "test_group", 1)
        frame = pd.concat([control_wm, cases], ignore_index=True)
        if len(cases) < 2:
            continue
        result = binary_wild_test(frame, offset)
        stage_rows.append(
            {
                "stage": stage,
                "n_stage": len(cases),
                "n_control": len(control_wm),
                "underpowered_n_lt_8": len(cases) < 8,
                **result,
            }
        )
    bh(stage_rows)

    stage_contrast_rows: list[dict[str, Any]] = []
    for offset, (positive_stage, reference_stage) in enumerate(
        [("SPMS", "PPMS"), ("SPMS", "RRMS"), ("PPMS", "RRMS")], start=5
    ):
        positive = donor_average(wm[wm.diagnosis.eq(positive_stage)], "test_group", 1)
        reference = donor_average(wm[wm.diagnosis.eq(reference_stage)], "test_group", 0)
        if len(positive) < 2 or len(reference) < 2:
            continue
        result = binary_wild_test(pd.concat([reference, positive], ignore_index=True), offset)
        stage_contrast_rows.append(
            {
                "contrast": f"{positive_stage}_minus_{reference_stage}",
                "n_positive_stage": len(positive),
                "n_reference_stage": len(reference),
                "underpowered_min_group_lt_8": min(len(positive), len(reference)) < 8,
                **result,
            }
        )
    bh(stage_contrast_rows)

    context_rows: list[dict[str, Any]] = []
    contexts = [
        ("NAWM", "WM"),
        ("AL", "WM"),
        ("CAL", "WM"),
        ("CIL", "WM"),
        ("RL", "WM"),
        ("NAGM", "GM"),
        ("GML", "GM"),
    ]
    for offset, (context, reference_matter) in enumerate(contexts, start=10):
        cases = donor_average(sample[sample.lesion_type.eq(context)], "test_group", 1)
        controls = donor_average(
            sample[sample.disease_binary.eq(0) & sample.lesion_type.eq(reference_matter)],
            "test_group",
            0,
        )
        if len(cases) < 5 or len(controls) < 5:
            continue
        result = binary_wild_test(pd.concat([controls, cases], ignore_index=True), offset)
        context_rows.append(
            {
                "context": context,
                "reference": f"control_{reference_matter}",
                "n_ms": len(cases),
                "n_control": len(controls),
                **result,
            }
        )
    bh(context_rows)

    paired_rows: list[dict[str, Any]] = []
    nawm = sample[sample.lesion_type.eq("NAWM")].groupby("canonical_donor")[OUTCOME].mean()
    for offset, context in enumerate(["AL", "CAL", "CIL", "RL"], start=30):
        lesion = sample[sample.lesion_type.eq(context)].groupby("canonical_donor")[OUTCOME].mean()
        shared = nawm.index.intersection(lesion.index)
        if len(shared) < 5:
            continue
        differences = lesion.loc[shared].to_numpy() - nawm.loc[shared].to_numpy()
        paired_rows.append(
            {
                "context": context,
                "n_paired_donors": len(shared),
                "mean_lesion_minus_nawm": float(differences.mean()),
                "median_lesion_minus_nawm": float(np.median(differences)),
                "sign_flip_two_sided_p": sign_flip_test(differences, offset),
            }
        )
    bh(paired_rows, p_field="sign_flip_two_sided_p")

    by_context = {row["context"]: row for row in context_rows}
    nawm_supported = bool(
        "NAWM" in by_context
        and by_context["NAWM"]["disease_or_context_beta"] > 0
        and by_context["NAWM"]["bh_q"] <= 0.10
    )
    lesion_amplification = any(
        row["mean_lesion_minus_nawm"] > 0 and row["bh_q"] <= 0.10 for row in paired_rows
    )
    stage_supported = [
        row["stage"]
        for row in stage_rows
        if not row["underpowered_n_lt_8"]
        and row["disease_or_context_beta"] > 0
        and row["bh_q"] <= 0.10
    ]
    stage_difference_supported = any(
        row["contrast"] == "SPMS_minus_PPMS"
        and not row["underpowered_min_group_lt_8"]
        and row["disease_or_context_beta"] > 0
        and row["bh_q"] <= 0.10
        for row in stage_contrast_rows
    )
    summary = {
        "purpose": "Fixed-score disease-stage and lesion-context heterogeneity for the replicated V53 microglial state",
        "cohort": args.cohort,
        "n_null_replicates_per_test": N_NULL,
        "seed": SEED,
        "families": {
            "stage": stage_rows,
            "stage_contrasts": stage_contrast_rows,
            "ms_context_vs_matched_control": context_rows,
            "within_ms_lesion_vs_nawm": paired_rows,
        },
        "nawm_state_supported": nawm_supported,
        "lesion_amplification_supported": lesion_amplification,
        "adequately_sized_stages_supported": stage_supported,
        "spms_vs_ppms_difference_supported": stage_difference_supported,
        "verdict": (
            "STATE_PRESENT_IN_NORMAL_APPEARING_MS_TISSUE"
            if nawm_supported
            else "STATE_NOT_SEPARABLE_FROM_LESION_CONTEXT"
        ),
        "boundary": "Context localization only; no causal or therapeutic interpretation.",
    }

    outdir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(stage_rows).to_csv(outdir / "stage_tests.tsv", sep="\t", index=False)
    pd.DataFrame(stage_contrast_rows).to_csv(
        outdir / "stage_contrasts.tsv", sep="\t", index=False
    )
    pd.DataFrame(context_rows).to_csv(outdir / "context_tests.tsv", sep="\t", index=False)
    pd.DataFrame(paired_rows).to_csv(outdir / "paired_lesion_vs_nawm.tsv", sep="\t", index=False)
    (outdir / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    report = [
        f"# V53 Macnair {args.cohort.title()} Stage And Lesion Heterogeneity",
        "",
        f"Verdict: **{summary['verdict']}**.",
        "",
        f"Normal-appearing white matter support: `{nawm_supported}`. Lesion amplification over paired",
        f"NAWM: `{lesion_amplification}`. Adequately sized stage groups passing their corrected family:",
        f"`{', '.join(stage_supported) if stage_supported else 'none'}`.",
        f"Direct SPMS-versus-PPMS difference supported: `{stage_difference_supported}`.",
        "",
        "All binary tests adjust for age, quadratic age, sex, and log microglial yield and use",
        f"`{N_NULL}` wild-null replicates. Stage, context, and paired-lesion tests are BH-corrected",
        "within separate pre-specified families. RRMS has only two donors and is explicitly",
        "underpowered. These tests localize a state; they do not establish cause or treatment direction.",
    ]
    (outdir / "REPORT.md").write_text("\n".join(report) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
