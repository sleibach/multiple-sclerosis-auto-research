#!/usr/bin/env python3
"""Build compact stakeholder-facing validation power tables from V43 outputs."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
POWER = ROOT / "analysis/v43_method_validation/power_map_summary.tsv"
OUT = ROOT / "analysis/v45_power_decision_table"


SCENARIOS = [
    ("moderate_clean", 0.75, 0.0, "none", "moderate effect, clean labels, no confounder"),
    ("large_clean", 1.00, 0.0, "none", "large effect, clean labels, no confounder"),
    ("moderate_noisy_immune", 0.75, 0.10, "immune_tone", "moderate effect, 10% label noise, immune-tone structure"),
    ("large_noisy_immune", 1.00, 0.10, "immune_tone", "large effect, 10% label noise, immune-tone structure"),
]


def band(pass_rate: float) -> str:
    if pass_rate >= 0.80:
        return "decision_grade_in_grid"
    if pass_rate >= 0.50:
        return "borderline_directional"
    return "mostly_directional_or_inconclusive"


def scenario_by_n(power: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for scenario, effect, noise, confounder, description in SCENARIOS:
        sub = power[
            (power["effect_size"].eq(effect))
            & (power["label_noise"].eq(noise))
            & (power["confounder_structure"].eq(confounder))
        ]
        grouped = (
            sub.groupby("n_per_group", as_index=False)
            .agg(
                pass_rate=("pass_rate", "mean"),
                conclusive_rate=("conclusive_rate", "mean"),
                mean_auc=("mean_auc", "mean"),
                mean_hedges_g=("mean_hedges_g", "mean"),
                parameter_cells=("cohorts", "count"),
                synthetic_cohorts=("cohorts", "sum"),
            )
            .sort_values("n_per_group")
        )
        for _, row in grouped.iterrows():
            rows.append(
                {
                    "scenario": scenario,
                    "description": description,
                    "effect_size": effect,
                    "label_noise": noise,
                    "confounder_structure": confounder,
                    "n_per_group": int(row["n_per_group"]),
                    "pass_rate": float(row["pass_rate"]),
                    "conclusive_rate": float(row["conclusive_rate"]),
                    "mean_auc": float(row["mean_auc"]),
                    "mean_hedges_g": float(row["mean_hedges_g"]),
                    "parameter_cells": int(row["parameter_cells"]),
                    "synthetic_cohorts": int(row["synthetic_cohorts"]),
                    "decision_band": band(float(row["pass_rate"])),
                }
            )
    return pd.DataFrame(rows)


def decision_rows(power: pd.DataFrame, by_n: pd.DataFrame) -> pd.DataFrame:
    null_fp = float(power.loc[power["effect_size"].eq(0), "false_positive_rate"].mean())
    gafson_small = power[power["n_per_group"].isin([10, 15])]
    rows = [
        {
            "decision_question": "What is the synthetic null false-positive rate?",
            "machine_result": f"{null_fp:.3f}",
            "interpretation": "False positives are controlled on average, but V43/V44/V45 show response-correlated batch can still fake raw positives without the guard.",
            "stakeholder_action": "Never interpret a raw pass without batch/confounder diagnostics.",
        },
        {
            "decision_question": "Can a Gafson-sized cohort settle the rule?",
            "machine_result": f"n=10-15/group mean conclusive rate {gafson_small['conclusive_rate'].mean():.3f}; mean pass rate {gafson_small['pass_rate'].mean():.3f}",
            "interpretation": "Useful effect-size/CI information, but often not decisive.",
            "stakeholder_action": "Run Gafson if obtained, but pursue Karolinska labels and larger cohort options in parallel.",
        },
    ]
    for scenario, _, _, _, description in SCENARIOS:
        sub = by_n[by_n["scenario"].eq(scenario)]
        hit = sub[sub["pass_rate"].ge(0.80)].sort_values("n_per_group")
        if hit.empty:
            machine = "80% pass probability not reached up to n=80/group"
            action = "Do not expect this scenario to settle the rule without cleaner labels, lower confounding, or a larger cohort."
        else:
            first = hit.iloc[0]
            machine = f"first reaches >=80% pass at n={int(first['n_per_group'])}/group (pass_rate {first['pass_rate']:.3f})"
            action = "This is the minimum decision-grade planning cell; prefer larger if metadata or labels are imperfect."
        rows.append(
            {
                "decision_question": f"What sample size works for {description}?",
                "machine_result": machine,
                "interpretation": "Synthetic method-characterization only; exact rates are planning bands.",
                "stakeholder_action": action,
            }
        )
    rows.append(
        {
            "decision_question": "What cohort should the medical team seek?",
            "machine_result": "Minimum 30+30 only for large clean effects; preferred 60-80/group; moderate noisy immune-tone effects may require >80/group or better labels/confounder control.",
            "interpretation": "The real design target is not just sample size; it is paired early samples plus labels, batch balance, steroid metadata, and cell-composition covariates.",
            "stakeholder_action": "Ask for Gafson, Karolinska labels, and any prospective/collaborator cohort capable of 60-80/group with the V45 CRF fields.",
        }
    )
    return pd.DataFrame(rows)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    power = pd.read_csv(POWER, sep="\t")
    by_n = scenario_by_n(power)
    decisions = decision_rows(power, by_n)
    by_n.to_csv(OUT / "selected_scenarios_by_n.tsv", sep="\t", index=False)
    decisions.to_csv(OUT / "stakeholder_power_decision_table.tsv", sep="\t", index=False)
    summary = {
        "synthetic": True,
        "source": str(POWER.relative_to(ROOT)),
        "n_selected_scenario_rows": int(len(by_n)),
        "n_decision_rows": int(len(decisions)),
        "headline": "Gafson-sized cohorts are often informative but inconclusive; 30+30 is decision-grade only for large clean effects; moderate/noisy immune-tone cases did not reach 80% pass up to 80/group.",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
