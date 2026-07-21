#!/usr/bin/env python3
"""Check V54 multi-site Cox components against statsmodels PHReg."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import norm
from statsmodels.duration.hazard_regression import PHReg

from v54_progression_multisite_transportability import cox_score_components


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis/v54_progression_multisite_transportability/reference_check"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for seed, beta in [(54961, 0.0), (54962, np.log(1.7))]:
        rng = np.random.default_rng(seed)
        n = 600
        site = np.repeat(np.arange(3), n // 3)
        score = rng.normal(size=n) + np.array([-0.5, 0.0, 0.5])[site]
        within = score - np.array([-0.5, 0.0, 0.5])[site]
        multiplier = np.array([0.6, 1.0, 1.8])[site] * np.exp(beta * within)
        event_time = -np.log(rng.random(n)) / (0.25 * multiplier)
        event = event_time <= 1.0
        time = np.minimum(event_time, 1.0)
        for route, strata in [
            ("pooled", np.zeros(n, dtype=int)),
            ("site_stratified", site),
        ]:
            custom_u, custom_i = cox_score_components(score, time, event, strata)
            model = PHReg(time, score[:, None], status=event, strata=strata)
            zero = np.zeros(1)
            reference_u = float(model.score(zero)[0])
            reference_i = float(-model.hessian(zero)[0, 0])
            custom_z = custom_u / np.sqrt(custom_i)
            reference_z = reference_u / np.sqrt(reference_i)
            maximum_difference = max(
                abs(custom_u - reference_u),
                abs(custom_i - reference_i),
                abs(custom_z - reference_z),
                abs(2 * norm.sf(abs(custom_z)) - 2 * norm.sf(abs(reference_z))),
            )
            rows.append(
                {
                    "synthetic": True,
                    "seed": seed,
                    "beta": beta,
                    "route": route,
                    "events": int(event.sum()),
                    "custom_score": custom_u,
                    "reference_score": reference_u,
                    "custom_information": custom_i,
                    "reference_information": reference_i,
                    "maximum_absolute_difference": maximum_difference,
                    "reference_check_pass": maximum_difference < 1e-10,
                }
            )
    frame = pd.DataFrame(rows)
    frame.to_csv(OUT / "reference_checks.tsv", sep="\t", index=False)
    passed = bool(frame.reference_check_pass.all())
    summary = {
        "purpose": "Independent numerical check of V54 multi-site Cox score and information",
        "synthetic": True,
        "reference": "statsmodels.duration.hazard_regression.PHReg score and Hessian at beta=0",
        "n_fixtures": len(frame),
        "n_pass": int(frame.reference_check_pass.sum()),
        "maximum_absolute_difference": float(frame.maximum_absolute_difference.max()),
        "overall_status": "PASS" if passed else "FAIL",
        "boundary": "Synthetic numerical method check only; no biological evidence.",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    if not passed:
        raise RuntimeError("V54 multi-site Cox reference check failed")


if __name__ == "__main__":
    main()
