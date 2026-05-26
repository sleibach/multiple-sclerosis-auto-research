#!/usr/bin/env python3
"""Power calculations for ACSL1 falsification experiments."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from statsmodels.stats.power import TTestIndPower, TTestPower


OUT = Path("results")


def main() -> int:
    rows = []
    paired = TTestPower()
    independent = TTestIndPower()

    rows.append(
        {
            "design": "ex_vivo_paired_high_vs_low_ACSL1_iPSC_microglia",
            "endpoint": "ACSL1 knockdown effect on myelin-debris lipid-droplet area and IL1B/TBXAS1 secretion composite",
            "assumed_standardized_effect": 0.8,
            "alpha_two_sided": 0.05,
            "power": 0.8,
            "calculated_n": paired.solve_power(effect_size=0.8, alpha=0.05, power=0.8, alternative="two-sided"),
            "rounded_n_with_attrition": 18,
            "unit": "paired donor-derived microglia lines",
        }
    )
    rows.append(
        {
            "design": "ex_vivo_three_arm_ACSL1_knockdown_rescue",
            "endpoint": "ACSL1 knockdown versus non-targeting control, with ACSL1 cDNA rescue",
            "assumed_standardized_effect": 0.9,
            "alpha_two_sided": 0.05,
            "power": 0.8,
            "calculated_n": independent.solve_power(effect_size=0.9, alpha=0.05, power=0.8, ratio=1.0, alternative="two-sided"),
            "rounded_n_with_attrition": 24,
            "unit": "biological replicates per arm across at least six donors",
        }
    )
    rows.append(
        {
            "design": "clinical_phase2_PRL_positive_ACSL1_high_target_engagement",
            "endpoint": "24-week change in new/enlarging PRL volume or QSM rim susceptibility after a CNS-engaged ACSL1 modulator exists",
            "assumed_standardized_effect": 0.5,
            "alpha_two_sided": 0.05,
            "power": 0.8,
            "calculated_n": independent.solve_power(effect_size=0.5, alpha=0.05, power=0.8, ratio=1.0, alternative="two-sided"),
            "rounded_n_with_attrition": 80,
            "unit": "patients per arm",
        }
    )
    frame = pd.DataFrame(rows)
    frame.to_csv(OUT / "acsl1_falsification_design.tsv", sep="\t", index=False)
    print(frame.to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
