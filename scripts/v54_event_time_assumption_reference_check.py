#!/usr/bin/env python3
"""Independent numerical checks for the V54 event-time assumption audit."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.special import expit
from scipy.stats import norm
from statsmodels.duration.hazard_regression import PHReg

from v54_progression_event_time_assumption_robustness import (
    calibrate_logistic_intercept,
    calibrate_scale,
    cox_score_test,
    piecewise_event_time_from_exponential,
)


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "analysis/v54_progression_event_time_assumption_robustness/reference_check"


def scalar_piecewise(
    draw: float,
    baseline: float,
    early_multiplier: float,
    late_multiplier: float,
    cut: float,
) -> float:
    early_hazard = baseline * early_multiplier
    early_cumulative = early_hazard * cut
    if draw <= early_cumulative:
        return draw / early_hazard
    return cut + (draw - early_cumulative) / (baseline * late_multiplier)


def main() -> None:
    DEFAULT_OUT.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, object]] = []

    draws = np.array([[0.10, 0.80, 2.00], [0.35, 1.20, 3.50]])
    baseline = np.array([0.5, 0.8])
    early = np.array([[1.0, 2.0, 0.5], [1.5, 0.7, 2.0]])
    late = np.array([[2.0, 0.5, 1.5], [0.6, 1.8, 0.8]])
    cut = 0.5
    vector = piecewise_event_time_from_exponential(draws, baseline, early, late, cut)
    scalar = np.array(
        [
            [scalar_piecewise(draws[i, j], baseline[i], early[i, j], late[i, j], cut) for j in range(draws.shape[1])]
            for i in range(draws.shape[0])
        ]
    )
    piecewise_error = float(np.max(np.abs(vector - scalar)))
    rows.append(
        {
            "check": "piecewise_inverse_against_scalar_reference",
            "maximum_absolute_difference": piecewise_error,
            "tolerance": 1e-12,
            "pass": piecewise_error < 1e-12,
        }
    )

    multiplier = np.array([[0.5, 1.0, 2.0, 4.0], [0.8, 1.2, 1.8, 2.6]])
    target_event = 0.30
    scale = calibrate_scale(multiplier, target_event)
    achieved_event = np.mean(1 - np.exp(-scale[:, None] * multiplier), axis=1)
    event_error = float(np.max(np.abs(achieved_event - target_event)))
    rows.append(
        {
            "check": "baseline_event_probability_calibration",
            "maximum_absolute_difference": event_error,
            "tolerance": 1e-12,
            "pass": event_error < 1e-12,
        }
    )

    linear = np.array([[-3.0, -1.0, 0.0, 2.0, 4.0], [-2.0, -0.5, 0.2, 1.0, 3.0]])
    target_dropout = 0.25
    intercept = calibrate_logistic_intercept(linear, target_dropout)
    achieved_dropout = expit(intercept[:, None] + linear).mean(axis=1)
    dropout_error = float(np.max(np.abs(achieved_dropout - target_dropout)))
    rows.append(
        {
            "check": "dropout_probability_calibration",
            "maximum_absolute_difference": dropout_error,
            "tolerance": 1e-12,
            "pass": dropout_error < 1e-12,
        }
    )

    rng = np.random.default_rng(54999)
    n = 700
    score = rng.normal(size=n)
    strata = rng.integers(0, 4, size=n)
    event_time = -np.log(rng.random(n)) / (0.22 * np.exp(0.4 * score))
    censor_time = np.where(rng.random(n) < 0.2, rng.uniform(0.05, 1.0, n), 1.0)
    event = event_time <= censor_time
    time = np.minimum(event_time, censor_time)
    custom_z, custom_p, custom_one_step = cox_score_test(score, time, event, strata)
    model = PHReg(time, score[:, None], status=event, strata=strata, ties="breslow")
    zero = np.zeros(1)
    reference_score = float(model.score(zero)[0])
    reference_information = float(-model.hessian(zero)[0, 0])
    reference_z = reference_score / np.sqrt(reference_information)
    reference_p = float(2 * norm.sf(abs(reference_z)))
    reference_one_step = reference_score / reference_information
    cox_error = float(
        max(
            abs(custom_z - reference_z),
            abs(custom_p - reference_p),
            abs(custom_one_step - reference_one_step),
        )
    )
    rows.append(
        {
            "check": "cox_score_against_statsmodels_phreg",
            "maximum_absolute_difference": cox_error,
            "tolerance": 1e-10,
            "pass": cox_error < 1e-10,
        }
    )

    frame = pd.DataFrame(rows)
    frame.to_csv(DEFAULT_OUT / "reference_checks.tsv", sep="\t", index=False)
    passed = bool(frame["pass"].all())
    summary = {
        "purpose": "Independent numerical checks for the V54 event-time assumption audit",
        "synthetic": True,
        "references": ["scalar piecewise inversion", "direct probability equations", "statsmodels.PHReg"],
        "n_checks": len(frame),
        "n_pass": int(frame["pass"].sum()),
        "maximum_absolute_difference": float(frame.maximum_absolute_difference.max()),
        "overall_status": "PASS" if passed else "FAIL",
        "boundary": "Synthetic numerical method checks only; no biological evidence.",
    }
    (DEFAULT_OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    if not passed:
        raise RuntimeError("V54 event-time assumption reference check failed")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
