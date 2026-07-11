#!/usr/bin/env python3
"""Write assumption-labeled sample-size targets for V53 microglia replication."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

from statsmodels.stats.power import TTestIndPower


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis/v53_ms_microglia_replication_spec"
EFFECTS = (0.5, 0.8, 1.0)
POWERS = (0.8, 0.9)
ALPHA = 0.05
INFLATION = 1.20


def main() -> int:
    calculator = TTestIndPower()
    rows = []
    for effect in EFFECTS:
        for power in POWERS:
            exact = float(
                calculator.solve_power(
                    effect_size=effect,
                    alpha=ALPHA,
                    power=power,
                    ratio=1.0,
                    alternative="two-sided",
                )
            )
            base = math.ceil(exact)
            inflated = math.ceil(base * INFLATION)
            rows.append(
                {
                    "assumed_standardized_effect": effect,
                    "target_power": power,
                    "two_sided_alpha": ALPHA,
                    "exact_n_per_group": exact,
                    "rounded_n_per_group": base,
                    "inflation_for_covariates_attrition": INFLATION,
                    "recommended_recruited_n_per_group": inflated,
                    "recommended_total_n": 2 * inflated,
                }
            )
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / "power_assumptions.tsv").open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(rows[0]),
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)
    summary = {
        "purpose": "Assumption-labeled planning power for independent CD44/CXCR4 state replication",
        "method": "statsmodels TTestIndPower, balanced independent groups, two-sided alpha 0.05",
        "inflation": "20% applied after ceiling for covariates, QC loss, and attrition; not a formal clustered-regression power model",
        "recommended_primary_design": "32 MS and 32 control donors for 80% power at assumed standardized effect 0.8",
        "biological_evidence": False,
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
