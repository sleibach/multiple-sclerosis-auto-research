#!/usr/bin/env python3
"""Build dropout/missing-timepoint planning tables from the V45 power grid.

This is deterministic planning arithmetic over synthetic method-characterization
outputs. It does not create biological evidence.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_POWER_GRID = ROOT / "analysis/v45_power_decision_table/selected_scenarios_by_n.tsv"


def band_for_pass_rate(pass_rate: float | None) -> str:
    if pass_rate is None or pd.isna(pass_rate):
        return "below_simulated_grid"
    if pass_rate >= 0.80:
        return "decision_grade_pass_probability"
    if pass_rate >= 0.60:
        return "promising_but_not_decision_grade"
    if pass_rate >= 0.30:
        return "directional_or_often_inconclusive"
    return "mostly_inconclusive"


def nearest_grid_row(grid: pd.DataFrame, scenario: str, analyzable_n: int) -> pd.Series | None:
    sub = grid[(grid["scenario"] == scenario) & (grid["n_per_group"] <= analyzable_n)].copy()
    if sub.empty:
        return None
    return sub.sort_values("n_per_group").iloc[-1]


def build_enrollment_targets(dropout_fractions: list[float], target_analyzable: list[int]) -> pd.DataFrame:
    rows = []
    for target in target_analyzable:
        for frac in dropout_fractions:
            if frac >= 1.0:
                required = math.inf
            else:
                required = math.ceil(target / (1.0 - frac))
            rows.append(
                {
                    "target_analyzable_per_group": target,
                    "missing_or_dropout_fraction": frac,
                    "enrollment_required_per_group": required,
                    "total_enrollment_required": required * 2 if math.isfinite(required) else math.inf,
                    "interpretation": (
                        f"Enroll {required} per response group to retain about {target} analyzable paired subjects/group "
                        f"if missing/dropout is {frac:.0%}."
                    ),
                }
            )
    return pd.DataFrame(rows)


def build_attrition_impact(
    grid: pd.DataFrame,
    dropout_fractions: list[float],
    nominal_sizes: list[int],
) -> pd.DataFrame:
    rows = []
    scenarios = grid[["scenario", "description"]].drop_duplicates().sort_values("scenario")
    for nominal in nominal_sizes:
        for frac in dropout_fractions:
            analyzable = math.floor(nominal * (1.0 - frac))
            for _, scen in scenarios.iterrows():
                row = nearest_grid_row(grid, scen["scenario"], analyzable)
                if row is None:
                    rows.append(
                        {
                            "nominal_enrolled_per_group": nominal,
                            "missing_or_dropout_fraction": frac,
                            "expected_analyzable_per_group": analyzable,
                            "scenario": scen["scenario"],
                            "description": scen["description"],
                            "mapped_grid_n_per_group": pd.NA,
                            "pass_rate": pd.NA,
                            "conclusive_rate": pd.NA,
                            "decision_band": "below_simulated_grid",
                            "planning_note": "Expected analyzable n falls below the simulated planning grid.",
                        }
                    )
                    continue
                pass_rate = float(row["pass_rate"])
                band = band_for_pass_rate(pass_rate)
                rows.append(
                    {
                        "nominal_enrolled_per_group": nominal,
                        "missing_or_dropout_fraction": frac,
                        "expected_analyzable_per_group": analyzable,
                        "scenario": scen["scenario"],
                        "description": scen["description"],
                        "mapped_grid_n_per_group": int(row["n_per_group"]),
                        "pass_rate": pass_rate,
                        "conclusive_rate": float(row["conclusive_rate"]),
                        "decision_band": band,
                        "planning_note": (
                            f"Attrition maps nominal {nominal}/group to about {analyzable}/group; "
                            f"using nearest lower simulated grid n={int(row['n_per_group'])}."
                        ),
                    }
                )
    return pd.DataFrame(rows)


def summarize(attrition: pd.DataFrame) -> dict[str, object]:
    clean_large = attrition[
        (attrition["scenario"] == "large_clean")
        & (attrition["decision_band"] == "decision_grade_pass_probability")
    ].copy()
    first_decision = None
    if not clean_large.empty:
        clean_large = clean_large.sort_values(["missing_or_dropout_fraction", "nominal_enrolled_per_group"])
        first_decision = clean_large.iloc[0].to_dict()
    gafson_band = attrition[
        (attrition["nominal_enrolled_per_group"].isin([10, 15]))
        & (attrition["scenario"].isin(["moderate_clean", "large_clean"]))
    ]
    below_grid = int((attrition["decision_band"] == "below_simulated_grid").sum())
    return {
        "status": "synthetic_method_planning_only",
        "n_attrition_rows": int(len(attrition)),
        "below_grid_rows": below_grid,
        "first_large_clean_decision_grade_row": first_decision,
        "gafson_size_mean_pass_rate_moderate_or_large_clean": (
            float(gafson_band["pass_rate"].dropna().mean()) if not gafson_band.empty else None
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--power-grid", type=Path, default=DEFAULT_POWER_GRID)
    parser.add_argument("--outdir", type=Path, required=True)
    args = parser.parse_args()

    outdir = args.outdir
    outdir.mkdir(parents=True, exist_ok=True)
    grid = pd.read_csv(args.power_grid, sep="\t")
    dropout_fractions = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]
    target_analyzable = [15, 30, 60, 80]
    nominal_sizes = [15, 20, 30, 45, 60, 80, 100, 120]

    targets = build_enrollment_targets(dropout_fractions, target_analyzable)
    attrition = build_attrition_impact(grid, dropout_fractions, nominal_sizes)
    summary = summarize(attrition)

    targets.to_csv(outdir / "dropout_enrollment_targets.tsv", sep="\t", index=False)
    attrition.to_csv(outdir / "nominal_attrition_power_impact.tsv", sep="\t", index=False)
    (outdir / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True, default=str) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
