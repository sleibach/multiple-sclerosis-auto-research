#!/usr/bin/env python3
"""Check the V54 batched P2 OLS interaction against statsmodels."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

from v54_progression_p2_interaction_power import batched_ols_test


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis/v54_progression_p2_interaction_power/reference_check"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(54919)
    cases = []
    for name, n, adjusted, coefficient_index in (
        ("paired_unadjusted", 80, False, 1),
        ("paired_adjusted", 80, True, 1),
        ("unpaired_unadjusted", 120, False, 3),
        ("unpaired_adjusted", 120, True, 3),
    ):
        outcome = np.tile([0.0, 1.0], n // 2)
        compartment = np.repeat([0.0, 1.0], n // 2)
        interaction = outcome * compartment
        composition = rng.normal(size=n) + 0.4 * interaction
        if name.startswith("paired"):
            columns = [np.ones(n), outcome]
            if adjusted:
                columns.append(composition)
            response = 0.6 * outcome + 0.5 * composition + rng.normal(size=n)
        else:
            columns = [np.ones(n), outcome, compartment, interaction]
            if adjusted:
                columns.extend([composition, composition * compartment])
            response = (
                0.2 * outcome
                + 0.7 * interaction
                + 0.5 * composition
                + rng.normal(size=n)
            )
        design = np.column_stack(columns)
        batched = batched_ols_test(
            response[None, :], design[None, :, :], coefficient_index
        )
        reference = sm.OLS(response, design).fit()
        values = {
            "estimate": float(batched["estimate"][0]),
            "se": float(batched["se"][0]),
            "statistic": float(batched["statistic"][0]),
            "p_value": float(batched["p_value"][0]),
        }
        reference_values = {
            "estimate": float(reference.params[coefficient_index]),
            "se": float(reference.bse[coefficient_index]),
            "statistic": float(reference.tvalues[coefficient_index]),
            "p_value": float(reference.pvalues[coefficient_index]),
        }
        max_difference = max(
            abs(values[key] - reference_values[key]) for key in values
        )
        cases.append(
            {
                "fixture": name,
                "synthetic": True,
                "n": n,
                "coefficient_index": coefficient_index,
                **{f"batched_{key}": value for key, value in values.items()},
                **{
                    f"statsmodels_{key}": value
                    for key, value in reference_values.items()
                },
                "maximum_absolute_difference": max_difference,
                "reference_check_pass": max_difference < 1e-10,
            }
        )
    frame = pd.DataFrame(cases)
    frame.to_csv(OUT / "reference_checks.tsv", sep="\t", index=False)
    passed = bool(frame["reference_check_pass"].all())
    summary = {
        "purpose": "Independent numerical check of V54 P2 batched OLS interaction",
        "synthetic": True,
        "reference": "statsmodels.api.OLS",
        "n_fixtures": len(frame),
        "n_pass": int(frame["reference_check_pass"].sum()),
        "maximum_absolute_difference": float(frame["maximum_absolute_difference"].max()),
        "overall_status": "PASS" if passed else "FAIL",
        "boundary": "Synthetic numerical method check only; no biological evidence.",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    if not passed:
        raise RuntimeError("V54 P2 OLS reference check failed")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
