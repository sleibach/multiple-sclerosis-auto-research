#!/usr/bin/env python3
"""Compare the V54 Cox score implementation with statsmodels on synthetic data."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import norm
from statsmodels.duration.hazard_regression import PHReg

from v54_progression_event_time_power_design import cox_score_test


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis/v54_progression_event_time_power_design/reference_check"


def fixture(
    seed: int,
    beta: float,
    stratified: bool,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    n = 600
    score = rng.normal(size=n)
    source = rng.random(n) < (1 / (1 + np.exp(-0.8 * score)))
    treatment = rng.random(n) < (1 / (1 + np.exp(0.8 * score - 0.5 * source)))
    strata = 2 * source.astype(int) + treatment.astype(int)
    if not stratified:
        strata = np.zeros(n, dtype=int)
    multiplier = np.exp(
        beta * score
        + np.log(1.6) * source.astype(float)
        + np.log(0.7) * treatment.astype(float)
    )
    event_time = -np.log(rng.random(n)) / (0.25 * multiplier)
    dropout = rng.random(n) < 0.25
    censor_time = np.where(dropout, rng.uniform(0.05, 1.0, n), 1.0)
    event = event_time <= censor_time
    time = np.minimum(event_time, censor_time)
    return score, time, event, strata


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    cases = [
        ("null_unadjusted", 54901, 0.0, False),
        ("positive_unadjusted", 54902, np.log(1.8), False),
        ("null_stratified", 54903, 0.0, True),
        ("positive_stratified", 54904, np.log(1.8), True),
    ]
    rows = []
    for name, seed, beta, stratified in cases:
        score, time, event, strata = fixture(seed, beta, stratified)
        custom_z, custom_p, custom_one_step = cox_score_test(
            score, time, event, strata
        )
        model = PHReg(
            time,
            score[:, None],
            status=event,
            strata=strata,
            ties="breslow",
        )
        zero = np.zeros(1)
        reference_score = float(model.score(zero)[0])
        reference_information = float(-model.hessian(zero)[0, 0])
        reference_z = reference_score / np.sqrt(reference_information)
        reference_p = float(2 * norm.sf(abs(reference_z)))
        reference_one_step = reference_score / reference_information
        max_abs_difference = max(
            abs(custom_z - reference_z),
            abs(custom_p - reference_p),
            abs(custom_one_step - reference_one_step),
        )
        rows.append(
            {
                "fixture": name,
                "synthetic": True,
                "seed": seed,
                "n": len(score),
                "events": int(event.sum()),
                "stratified": stratified,
                "custom_z": custom_z,
                "reference_z": reference_z,
                "custom_p": custom_p,
                "reference_p": reference_p,
                "custom_one_step_log_hr": custom_one_step,
                "reference_one_step_log_hr": reference_one_step,
                "max_abs_difference": max_abs_difference,
                "reference_check_pass": max_abs_difference < 1e-10,
            }
        )
    frame = pd.DataFrame(rows)
    frame.to_csv(OUT / "reference_checks.tsv", sep="\t", index=False)
    passed = bool(frame["reference_check_pass"].all())
    summary = {
        "purpose": "Independent implementation check of V54 Cox score test",
        "synthetic": True,
        "reference": "statsmodels.duration.hazard_regression.PHReg score and Hessian at beta=0",
        "n_fixtures": len(frame),
        "n_pass": int(frame["reference_check_pass"].sum()),
        "maximum_absolute_difference": float(frame["max_abs_difference"].max()),
        "overall_status": "PASS" if passed else "FAIL",
        "boundary": "Synthetic numerical method check only; no biological evidence.",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    if not passed:
        raise RuntimeError("V54 event-time score reference check failed")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
