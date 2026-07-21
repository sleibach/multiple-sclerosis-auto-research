#!/usr/bin/env python3
"""Check the V54 tie-aware Cox score against statsmodels PHReg."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.special import expit
from scipy.stats import norm
from statsmodels.duration.hazard_regression import PHReg

from v54_progression_visit_schedule_robustness import breslow_score_test


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis/v54_progression_visit_schedule_robustness/reference_check"


def fixture(
    seed: int, beta: float, stratified: bool
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    n = 480
    score = rng.normal(size=n)
    source = rng.random(n) < expit(0.8 * score)
    treatment = rng.random(n) < expit(0.5 * source - 0.8 * score)
    strata = 2 * source.astype(int) + treatment.astype(int)
    if not stratified:
        strata = np.zeros(n, dtype=int)
    latent_multiplier = np.exp(
        beta * score
        + np.log(1.6) * source.astype(float)
        + np.log(0.7) * treatment.astype(float)
    )
    latent_time = -np.log(rng.random(n)) / (0.35 * latent_multiplier)
    visit_time = np.ceil(latent_time / 0.25) * 0.25
    censor_time = rng.choice([0.5, 0.75, 1.0, 1.25, 1.5, 2.0], size=n)
    event = visit_time <= censor_time
    observed_time = np.minimum(visit_time, censor_time)
    return score, observed_time, event, strata


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    cases = [
        ("null_unstratified_ties", 54941, 0.0, False),
        ("positive_unstratified_ties", 54942, np.log(1.7), False),
        ("null_stratified_ties", 54943, 0.0, True),
        ("positive_stratified_ties", 54944, np.log(1.7), True),
    ]
    rows = []
    for name, seed, beta, stratified in cases:
        score, time, event, strata = fixture(seed, beta, stratified)
        custom_z, custom_p, custom_one_step = breslow_score_test(
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
        maximum_difference = max(
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
                "maximum_absolute_difference": maximum_difference,
                "reference_check_pass": maximum_difference < 1e-10,
            }
        )
    frame = pd.DataFrame(rows)
    frame.to_csv(OUT / "reference_checks.tsv", sep="\t", index=False)
    passed = bool(frame.reference_check_pass.all())
    summary = {
        "purpose": "Independent numerical check of V54 tied-time Breslow Cox score",
        "synthetic": True,
        "reference": "statsmodels.duration.hazard_regression.PHReg(ties='breslow') score and Hessian at beta=0",
        "n_fixtures": len(frame),
        "n_pass": int(frame.reference_check_pass.sum()),
        "maximum_absolute_difference": float(frame.maximum_absolute_difference.max()),
        "overall_status": "PASS" if passed else "FAIL",
        "boundary": "Synthetic numerical method check only; no biological evidence.",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    if not passed:
        raise RuntimeError("V54 tied-time Breslow reference check failed")


if __name__ == "__main__":
    main()
