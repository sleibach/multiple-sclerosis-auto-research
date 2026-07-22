#!/usr/bin/env python3
"""Audit treatment-policy and censor-at-switch progression estimands."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy.stats import binom, norm


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "analysis/v54_progression_treatment_switch_estimand"
SEEDS = (54101, 54103, 54107)
N_VALUES = (180, 320)
POST_SWITCH_HRS = (0.5, 1.0, 1.5)
MOLECULAR_HRS = (1.0, 1.7)
SWITCH_MECHANISMS = (
    "none",
    "independent",
    "score_dependent",
    "progression_risk_dependent",
    "joint_score_progression_risk",
)
ESTIMANDS = ("treatment_policy", "censor_at_switch")
REPLICATES = 400
EVENT_PROBABILITY = 0.30
SWITCH_PROBABILITY = 0.25
RELIABILITY = 0.70
SCORE_MISSING = 0.10
ALPHA = 0.05


def wilson(successes: int, total: int) -> tuple[float, float]:
    z = norm.ppf(0.975)
    probability = successes / total
    denominator = 1 + z * z / total
    center = (probability + z * z / (2 * total)) / denominator
    half = z * np.sqrt(
        probability * (1 - probability) / total + z * z / (4 * total * total)
    ) / denominator
    return float(center - half), float(center + half)


def calibrate_scale(multiplier: np.ndarray, target: float) -> np.ndarray:
    low = np.zeros(multiplier.shape[0])
    high = np.full(multiplier.shape[0], 20.0)
    for _ in range(50):
        middle = (low + high) / 2
        observed = np.mean(1 - np.exp(-middle[:, None] * multiplier), axis=1)
        below = observed < target
        low[below] = middle[below]
        high[~below] = middle[~below]
    return (low + high) / 2


def cox_score_test(score: np.ndarray, time: np.ndarray, event: np.ndarray) -> tuple[float, float, float]:
    order = np.argsort(time, kind="mergesort")
    ordered_score = score[order]
    ordered_event = event[order]
    event_index = np.flatnonzero(ordered_event)
    if not len(event_index):
        return np.nan, np.nan, np.nan
    risk_n = np.arange(len(order), 0, -1, dtype=float)
    risk_sum = np.cumsum(ordered_score[::-1])[::-1]
    risk_sum_sq = np.cumsum(ordered_score[::-1] ** 2)[::-1]
    risk_mean = risk_sum[event_index] / risk_n[event_index]
    risk_variance = risk_sum_sq[event_index] / risk_n[event_index] - risk_mean**2
    statistic = float(np.sum(ordered_score[event_index] - risk_mean))
    information = float(np.sum(np.maximum(risk_variance, 0.0)))
    if information <= 1e-12 or not np.isfinite(information):
        return np.nan, np.nan, np.nan
    z_value = statistic / np.sqrt(information)
    return (
        float(z_value),
        float(2 * norm.sf(abs(z_value))),
        float(statistic / information),
    )


def switch_linear_predictor(
    mechanism: str, latent_score: np.ndarray, frailty: np.ndarray
) -> np.ndarray:
    if mechanism == "independent":
        return np.zeros_like(latent_score)
    if mechanism == "score_dependent":
        return latent_score
    if mechanism == "progression_risk_dependent":
        return frailty
    if mechanism == "joint_score_progression_risk":
        return np.clip(0.8 * latent_score + 0.8 * frailty + latent_score * frailty, -5, 5)
    raise ValueError(mechanism)


def simulate_cell(
    *,
    rng: np.random.Generator,
    n: int,
    molecular_hr: float,
    post_switch_hr: float,
    mechanism: str,
) -> list[dict[str, Any]]:
    latent_score = rng.normal(size=(REPLICATES, n))
    frailty = rng.normal(size=(REPLICATES, n))
    event_multiplier = np.exp(np.log(molecular_hr) * latent_score + 0.7 * frailty)
    event_baseline = calibrate_scale(event_multiplier, EVENT_PROBABILITY)
    pre_event_draw = -np.log(np.clip(rng.random((REPLICATES, n)), 1e-12, 1.0))
    pre_event_time = pre_event_draw / (event_baseline[:, None] * event_multiplier)

    if mechanism == "none":
        switch_time = np.full_like(pre_event_time, np.inf)
    else:
        switch_multiplier = np.exp(switch_linear_predictor(mechanism, latent_score, frailty))
        switch_baseline = calibrate_scale(switch_multiplier, SWITCH_PROBABILITY)
        switch_time = -np.log(np.clip(rng.random((REPLICATES, n)), 1e-12, 1.0)) / (
            switch_baseline[:, None] * switch_multiplier
        )

    switched_first = switch_time < pre_event_time
    post_wait = -np.log(np.clip(rng.random((REPLICATES, n)), 1e-12, 1.0)) / (
        event_baseline[:, None] * event_multiplier * post_switch_hr
    )
    policy_event_time = np.where(switched_first, switch_time + post_wait, pre_event_time)
    policy_time = np.minimum(policy_event_time, 1.0)
    policy_event = policy_event_time <= 1.0
    censor_time = np.minimum(np.minimum(pre_event_time, switch_time), 1.0)
    censor_event = (pre_event_time <= switch_time) & (pre_event_time <= 1.0)
    switched_observed = (switch_time < pre_event_time) & (switch_time <= 1.0)

    observed_score = (
        np.sqrt(RELIABILITY) * latent_score
        + np.sqrt(1 - RELIABILITY) * rng.normal(size=latent_score.shape)
    )
    included = rng.random(size=latent_score.shape) >= SCORE_MISSING
    route_data = {
        "treatment_policy": (policy_time, policy_event),
        "censor_at_switch": (censor_time, censor_event),
    }
    outputs: list[dict[str, Any]] = []
    for estimand, (time, event) in route_data.items():
        valid = positive = negative = 0
        z_values: list[float] = []
        one_steps: list[float] = []
        event_counts: list[int] = []
        switch_counts: list[int] = []
        for replicate in range(REPLICATES):
            keep = included[replicate]
            score = observed_score[replicate, keep]
            events = event[replicate, keep]
            event_counts.append(int(events.sum()))
            switch_counts.append(int(switched_observed[replicate, keep].sum()))
            if keep.sum() < 20 or events.sum() < 10 or (~events).sum() < 10:
                continue
            sd = float(np.std(score, ddof=1))
            if not np.isfinite(sd) or sd <= 0:
                continue
            score = (score - score.mean()) / sd
            z_value, p_value, one_step = cox_score_test(score, time[replicate, keep], events)
            if not np.isfinite(p_value):
                continue
            valid += 1
            z_values.append(z_value)
            one_steps.append(one_step)
            if p_value <= ALPHA and z_value > 0:
                positive += 1
            if p_value <= ALPHA and z_value < 0:
                negative += 1
        significant = positive + negative
        low, high = wilson(significant, REPLICATES)
        outputs.append(
            {
                "n_requested": n,
                "molecular_progression_hr": molecular_hr,
                "post_switch_progression_hr": post_switch_hr,
                "switch_mechanism": mechanism,
                "estimand": estimand,
                "n_simulated_cohorts": REPLICATES,
                "n_valid_fits": valid,
                "valid_fit_rate": valid / REPLICATES,
                "significant_count": significant,
                "significant_probability": significant / REPLICATES,
                "significant_probability_ci_low": low,
                "significant_probability_ci_high": high,
                "positive_call_probability": positive / REPLICATES,
                "negative_call_probability": negative / REPLICATES,
                "median_score_z": float(np.median(z_values)) if z_values else np.nan,
                "median_one_step_log_hr": float(np.median(one_steps)) if one_steps else np.nan,
                "median_events": float(np.median(event_counts)),
                "median_switches": float(np.median(switch_counts)),
            }
        )
    return outputs


def aggregate(seed_frame: pd.DataFrame) -> pd.DataFrame:
    keys = [
        "n_requested",
        "molecular_progression_hr",
        "post_switch_progression_hr",
        "switch_mechanism",
        "estimand",
    ]
    rows: list[dict[str, Any]] = []
    for values, group in seed_frame.groupby(keys, sort=True):
        row = dict(zip(keys, values))
        total = int(group.n_simulated_cohorts.sum())
        significant = int(group.significant_count.sum())
        positive = int(round((group.positive_call_probability * group.n_simulated_cohorts).sum()))
        negative = int(round((group.negative_call_probability * group.n_simulated_cohorts).sum()))
        low, high = wilson(significant, total)
        row.update(
            {
                "n_simulated_cohorts": total,
                "n_valid_fits": int(group.n_valid_fits.sum()),
                "valid_fit_rate": float(group.n_valid_fits.sum() / total),
                "significant_count": significant,
                "significant_probability": significant / total,
                "significant_probability_ci_low": low,
                "significant_probability_ci_high": high,
                "minimum_seed_probability": float(group.significant_probability.min()),
                "maximum_seed_probability": float(group.significant_probability.max()),
                "positive_call_probability": positive / total,
                "negative_call_probability": negative / total,
                "median_score_z_across_seeds": float(group.median_score_z.median()),
                "median_one_step_log_hr_across_seeds": float(group.median_one_step_log_hr.median()),
                "median_events_across_seeds": float(group.median_events.median()),
                "median_switches_across_seeds": float(group.median_switches.median()),
            }
        )
        rows.append(row)
    return pd.DataFrame(rows)


def calibration(grid: pd.DataFrame) -> pd.DataFrame:
    null = grid.loc[grid.molecular_progression_hr.eq(1.0)]
    rows: list[dict[str, Any]] = []
    for (mechanism, estimand), group in null.groupby(["switch_mechanism", "estimand"], sort=True):
        maximum = group.loc[group.significant_probability.idxmax()]
        count = int(maximum.significant_count)
        total = int(maximum.n_simulated_cohorts)
        single_tail = float(binom.sf(count - 1, total, ALPHA))
        family_tail = float(1 - (1 - single_tail) ** len(group))
        strict = bool((group.significant_probability_ci_low > ALPHA).any())
        invalid = bool(strict and family_tail < ALPHA)
        rows.append(
            {
                "switch_mechanism": mechanism,
                "estimand": estimand,
                "n_null_cells": len(group),
                "median_null_probability": float(group.significant_probability.median()),
                "maximum_null_probability": float(maximum.significant_probability),
                "maximum_count": count,
                "maximum_total": total,
                "maximum_family_tail_probability": family_tail,
                "strict_cell_flag": strict,
                "strict_cell_flag_but_family_compatible": bool(strict and not invalid),
                "invalid_for_direct_prognostic_interpretation": invalid,
                "dominant_false_direction": (
                    "positive"
                    if maximum.positive_call_probability > maximum.negative_call_probability
                    else "negative"
                ),
            }
        )
    return pd.DataFrame(rows)


def write_report(output_dir: Path, calibration_frame: pd.DataFrame, grid: pd.DataFrame, summary: dict[str, Any]) -> None:
    invalid_lines = "\n".join(f"- `{item}`" for item in summary["invalid_null_families"])
    if not invalid_lines:
        invalid_lines = "- None."
    flagged_lines = "\n".join(
        f"- `{item}`" for item in summary["strict_cell_flag_but_family_compatible"]
    )
    if not flagged_lines:
        flagged_lines = "- None."
    calibrated = calibration_frame.loc[
        ~calibration_frame.invalid_for_direct_prognostic_interpretation
        & ~calibration_frame.strict_cell_flag
    ]
    calibrated_lines = "\n".join(
        f"- `{row.switch_mechanism}|{row.estimand}`: median null "
        f"`{row.median_null_probability:.3f}`, maximum `{row.maximum_null_probability:.3f}`."
        for row in calibrated.itertuples(index=False)
    )
    report = f"""# V54 Treatment-Switch Estimand Audit

Status: **{summary['verdict']}**.

This is seeded synthetic method behavior only. It is not evidence about an MS
treatment, switching process, molecular predictor, or effect.

## Invalid Direct-Prognostic Families

{invalid_lines}

## Strict-Cell Flags Compatible With Family Maxima

{flagged_lines}

These families are not called invalid, but are conservatively excluded from
positive-performance interpretation. The initial implementation overcalled
them by omitting the already-frozen family-maximum adjudication; that mismatch
was corrected before this result was committed.

## Calibrated Families

{calibrated_lines}

The treatment-policy route follows observed post-switch outcomes and therefore
answers a policy-specific association question. When treatment assignment
depends on score and the treatment changes progression hazard, a non-null score
association can arise even when the direct molecular progression HR is one.
That is not the untreated prognostic estimand.

Censoring at switch removes post-switch treatment effects but is not a generic
repair: joint score/progression-risk switching can select the risk set and must
be audited as informative censoring. Both estimands must be frozen and reported;
neither may be selected because its direction or p-value is favorable.

## Boundary

These simulations identify method failure regimes under a fixed generator.
They do not select a clinical estimand, estimate causal treatment effects, or
show that any molecular state predicts or halts MS progression.
"""
    (output_dir / "REPORT.md").write_text(report)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, Any]] = []
    for seed in SEEDS:
        rng = np.random.default_rng(seed)
        for n in N_VALUES:
            for molecular_hr in MOLECULAR_HRS:
                for post_switch_hr in POST_SWITCH_HRS:
                    for mechanism in SWITCH_MECHANISMS:
                        for result in simulate_cell(
                            rng=rng,
                            n=n,
                            molecular_hr=molecular_hr,
                            post_switch_hr=post_switch_hr,
                            mechanism=mechanism,
                        ):
                            result["seed"] = seed
                            rows.append(result)
    seed_frame = pd.DataFrame(rows)
    grid = aggregate(seed_frame)
    calibration_frame = calibration(grid)
    seed_frame.to_csv(output_dir / "seed_results.tsv", sep="\t", index=False)
    grid.to_csv(output_dir / "estimand_grid.tsv", sep="\t", index=False)
    calibration_frame.to_csv(output_dir / "null_calibration.tsv", sep="\t", index=False)

    invalid = [
        f"{row.switch_mechanism}|{row.estimand}"
        for row in calibration_frame.itertuples(index=False)
        if row.invalid_for_direct_prognostic_interpretation
    ]
    flagged_compatible = [
        f"{row.switch_mechanism}|{row.estimand}"
        for row in calibration_frame.itertuples(index=False)
        if row.strict_cell_flag_but_family_compatible
    ]
    null = grid.loc[grid.molecular_progression_hr.eq(1.0)]
    worst = null.loc[null.significant_probability.idxmax()]
    nonnull = grid.loc[grid.molecular_progression_hr.eq(1.7)].copy()
    pivot = nonnull.pivot_table(
        index=["n_requested", "post_switch_progression_hr", "switch_mechanism"],
        columns="estimand",
        values="significant_probability",
    ).reset_index()
    pivot["absolute_estimand_difference"] = (
        pivot["treatment_policy"] - pivot["censor_at_switch"]
    ).abs()
    pivot.to_csv(output_dir / "nonnull_estimand_differences.tsv", sep="\t", index=False)
    summary = {
        "purpose": "V54 seeded synthetic treatment-switch estimand audit; no biological claim",
        "synthetic": True,
        "seeds": list(SEEDS),
        "replicates_per_cell_seed": REPLICATES,
        "n_unique_simulated_cohorts": int(len(seed_frame) * REPLICATES / len(ESTIMANDS)),
        "n_estimand_route_evaluations": int(len(seed_frame) * REPLICATES),
        "n_null_families": len(calibration_frame),
        "n_invalid_null_families": len(invalid),
        "invalid_null_families": invalid,
        "n_strict_cell_flag_but_family_compatible": len(flagged_compatible),
        "strict_cell_flag_but_family_compatible": flagged_compatible,
        "worst_null_cell": {
            "n": int(worst.n_requested),
            "post_switch_hr": float(worst.post_switch_progression_hr),
            "switch_mechanism": worst.switch_mechanism,
            "estimand": worst.estimand,
            "significant_probability": float(worst.significant_probability),
            "positive_call_probability": float(worst.positive_call_probability),
            "negative_call_probability": float(worst.negative_call_probability),
        },
        "n_nonnull_cells_with_estimand_difference_ge_0_10": int(
            (pivot.absolute_estimand_difference >= 0.10).sum()
        ),
        "maximum_nonnull_estimand_difference": float(pivot.absolute_estimand_difference.max()),
        "verdict": "ESTIMAND_MUST_BE_FROZEN_SWITCHING_CAN_CHANGE_OR_INVALIDATE_INTERPRETATION",
        "boundary": "Synthetic method behavior only; no empirical MS treatment, switching, molecular, progression, or causal effect.",
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    config = {
        "purpose": summary["purpose"],
        "synthetic": True,
        "seeds": list(SEEDS),
        "n_values": list(N_VALUES),
        "post_switch_hrs": list(POST_SWITCH_HRS),
        "molecular_hrs": list(MOLECULAR_HRS),
        "switch_mechanisms": list(SWITCH_MECHANISMS),
        "estimands": list(ESTIMANDS),
        "replicates": REPLICATES,
        "event_probability": EVENT_PROBABILITY,
        "switch_probability": SWITCH_PROBABILITY,
        "reliability": RELIABILITY,
        "score_missing": SCORE_MISSING,
        "alpha": ALPHA,
        "null_invalidity_rule": "strict aggregate-cell Wilson lower bound >0.05 and fixed-family maximum tail <0.05; strict family-compatible flags excluded",
    }
    (output_dir / "simulation_config.json").write_text(json.dumps(config, indent=2) + "\n")
    write_report(output_dir, calibration_frame, grid, summary)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
