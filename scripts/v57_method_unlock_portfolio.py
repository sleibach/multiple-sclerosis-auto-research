#!/usr/bin/env python3
"""Rank prospective data packages by the blocked methods they unlock."""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis/v57_method_unlock_portfolio"

PACKAGES = [
    {
        "package_id": "D01_independent_ms_response_bulk",
        "name": "Independent paired MS treatment-response bulk cohort",
        "required_features": "baseline and early paired expression; frozen module genes; response outcome; batch; steroid; composition covariates",
        "methods": "M11;M12;M13;M29",
        "decisions": "external_monitoring_validation;cross_cohort_transport",
        "burden_min": 1,
        "burden_max": 2,
        "dependency": "none",
        "basis": "docs/validation/PREREGISTRATION_V42.md;docs/validation/POWER_MAP_V43.md;meta/METHOD_FRONTIER_V57.md",
    },
    {
        "package_id": "D02_ms_response_single_cell_trajectory",
        "name": "Paired response-labelled MS single-cell trajectory cohort",
        "required_features": "patient IDs; baseline plus at least two on-treatment times; response; cell counts; batch; module genes",
        "methods": "M14;M15;M16;M20;M23",
        "decisions": "within_cell_response;composition_response;trajectory_response",
        "burden_min": 3,
        "burden_max": 5,
        "dependency": "none",
        "basis": "meta/METHOD_FRONTIER_V57.md;analysis/v57_single_cell_transport/summary.json;analysis/v57_compositional_response/summary.json",
    },
    {
        "package_id": "D03_longitudinal_progression_molecular_ipd",
        "name": "Longitudinal molecular-to-confirmed-disability MS IPD",
        "required_features": "repeated molecular samples; raw disability components; confirmed CDP or PIRA; relapse; treatment; attendance; site; batch",
        "methods": "M21;M22;M23;M24",
        "decisions": "progression_association;mediation_identifiability;progression_trajectory",
        "burden_min": 4,
        "burden_max": 5,
        "dependency": "none",
        "basis": "docs/validation/PROGRESSION_ACQUISITION_VOI_V54.md;docs/reports/PROGRESSION_THERAPY_OPPORTUNITY_V56.md",
    },
    {
        "package_id": "D04_randomized_progression_trial_ipd",
        "name": "Randomized progression-trial participant-level clinical data",
        "required_features": "randomization; treatment; baseline modifiers; longitudinal disability; censoring; site; adherence and switching",
        "methods": "M09;M21;M25;M30",
        "decisions": "causal_treatment_effect;effect_transport;clinical_utility",
        "burden_min": 2,
        "burden_max": 4,
        "dependency": "none",
        "basis": "docs/reports/PROGRESSION_THERAPY_OPPORTUNITY_V56.md;docs/plans/V57_TRIAL_TRANSPORT_PLAN.md",
    },
    {
        "package_id": "D05_randomized_progression_molecular_substudy",
        "name": "Randomized progression trial with longitudinal molecular substudy",
        "required_features": "randomization; baseline and repeated molecular samples; disability outcome; treatment adherence; batch; composition",
        "methods": "M12;M20;M22;M23;M29",
        "decisions": "treatment_molecular_mechanism;mediation_identifiability;progression_trajectory",
        "burden_min": 4,
        "burden_max": 5,
        "dependency": "none",
        "basis": "docs/reports/PROGRESSION_THERAPY_OPPORTUNITY_V56.md;docs/validation/TOLEDYNAMIC_DESIGN_BRANCH_LOCK_V56.json",
    },
    {
        "package_id": "D06_primary_human_directional_perturbation",
        "name": "Direction-resolved multi-donor primary-human perturbation data",
        "required_features": "selective perturbation; target engagement; dose; donor; viability; host defense; remyelination or myelin-clearance function",
        "methods": "M04;M05;M17;M30",
        "decisions": "causal_axis_orientation;intervention_direction;functional_safety",
        "burden_min": 3,
        "burden_max": 5,
        "dependency": "progression-relevant state or target context",
        "basis": "docs/validation/PROGRESSION_ACQUISITION_VOI_V54.md;docs/reports/THERAPEUTIC_PATH_V52.md;docs/history/EXPLORATORY_FRONTIER_V53.md",
    },
    {
        "package_id": "D07_replicated_lesion_spatial",
        "name": "Replicated chronic-active-lesion spatial counts and coordinates",
        "required_features": "raw counts; coordinates; donor; slide; lesion region; matched NAWM; source and processing metadata",
        "methods": "M18;M19;M20",
        "decisions": "progression_compartment_localization;spatial_neighborhood",
        "burden_min": 2,
        "burden_max": 4,
        "dependency": "none",
        "basis": "docs/reports/PROGRESSION_THERAPY_OPPORTUNITY_V56.md;meta/METHOD_FRONTIER_V57.md",
    },
    {
        "package_id": "D08_genotype_linked_immune_perturbation",
        "name": "Genotype-linked immune state and perturbation cohort",
        "required_features": "genotype; immune expression or state; controlled perturbation; donor; allele harmonization; cellular context",
        "methods": "M05;M06;M22;M30",
        "decisions": "causal_gene_direction;context_specific_genetic_effect;mediation_identifiability",
        "burden_min": 3,
        "burden_max": 5,
        "dependency": "none",
        "basis": "docs/reports/THERAPEUTIC_PATH_V52.md;meta/METHOD_FRONTIER_V57.md",
    },
]

SCENARIOS = {
    "equal": {},
    "validation_first": {"external_monitoring_validation": 5, "cross_cohort_transport": 4},
    "progression_first": {"progression_association": 5, "progression_trajectory": 5, "progression_compartment_localization": 4},
    "causal_treatment_first": {"causal_treatment_effect": 5, "effect_transport": 5, "clinical_utility": 4, "mediation_identifiability": 4},
    "mechanism_first": {"causal_axis_orientation": 5, "intervention_direction": 5, "functional_safety": 5, "treatment_molecular_mechanism": 4},
    "feasibility_first": {"external_monitoring_validation": 4, "cross_cohort_transport": 4, "spatial_neighborhood": 2},
}


def split_set(value: str) -> set[str]:
    return {item for item in value.split(";") if item}


def score_decisions(decisions: set[str], overrides: dict[str, int]) -> int:
    return sum(overrides.get(decision, 1) for decision in decisions)


def dominates(a: pd.Series, b: pd.Series) -> bool:
    better_or_equal = (
        a.n_methods >= b.n_methods
        and a.n_decisions >= b.n_decisions
        and a.min_scenario_score >= b.min_scenario_score
        and a.burden_max <= b.burden_max
    )
    strictly_better = (
        a.n_methods > b.n_methods
        or a.n_decisions > b.n_decisions
        or a.min_scenario_score > b.min_scenario_score
        or a.burden_max < b.burden_max
    )
    return bool(better_or_equal and strictly_better)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    package_frame = pd.DataFrame(PACKAGES)
    for basis in package_frame.basis:
        for relpath in basis.split(";"):
            if not (ROOT / relpath).exists():
                raise FileNotFoundError(relpath)

    ranking_rows: list[dict[str, object]] = []
    for scenario, overrides in SCENARIOS.items():
        for package in PACKAGES:
            decisions = split_set(package["decisions"])
            score = score_decisions(decisions, overrides)
            # Burden-normalized score is a transparent planning ratio. Use the
            # conservative high burden for ranking and retain raw score too.
            ranking_rows.append(
                {
                    "scenario": scenario,
                    "package_id": package["package_id"],
                    "decision_score": score,
                    "n_methods": len(split_set(package["methods"])),
                    "burden_max": package["burden_max"],
                    "score_per_max_burden": score / package["burden_max"],
                }
            )
    rankings = pd.DataFrame(ranking_rows)
    rankings["rank"] = rankings.groupby("scenario")["score_per_max_burden"].rank(
        method="min", ascending=False
    ).astype(int)
    rank_summary = (
        rankings.groupby("package_id")
        .agg(
            scenarios_ranked_first=("rank", lambda x: int((x == 1).sum())),
            median_rank=("rank", "median"),
            worst_rank=("rank", "max"),
        )
        .reset_index()
    )

    portfolios: list[dict[str, object]] = []
    for size in (1, 2, 3):
        for combo in itertools.combinations(PACKAGES, size):
            methods = set().union(*(split_set(item["methods"]) for item in combo))
            decisions = set().union(*(split_set(item["decisions"]) for item in combo))
            scenario_scores = [score_decisions(decisions, value) for value in SCENARIOS.values()]
            portfolios.append(
                {
                    "portfolio_size": size,
                    "package_ids": ";".join(item["package_id"] for item in combo),
                    "n_methods": len(methods),
                    "n_decisions": len(decisions),
                    "methods": ";".join(sorted(methods)),
                    "decisions": ";".join(sorted(decisions)),
                    "burden_min": sum(int(item["burden_min"]) for item in combo),
                    "burden_max": sum(int(item["burden_max"]) for item in combo),
                    "min_scenario_score": min(scenario_scores),
                    "max_scenario_score": max(scenario_scores),
                }
            )
    portfolio_frame = pd.DataFrame(portfolios)
    portfolio_frame["pareto"] = False
    for size, group in portfolio_frame.groupby("portfolio_size"):
        for index, row in group.iterrows():
            portfolio_frame.loc[index, "pareto"] = not any(
                dominates(other, row) for other_index, other in group.iterrows() if other_index != index
            )

    one_package = portfolio_frame[portfolio_frame.portfolio_size == 1]
    one_package_pareto = set(one_package.loc[one_package.pareto, "package_ids"])
    robust = rank_summary[
        (rank_summary.scenarios_ranked_first >= 4)
        & rank_summary.package_id.isin(one_package_pareto)
    ]

    package_frame.to_csv(OUT / "data_packages.tsv", sep="\t", index=False)
    rankings.sort_values(["scenario", "rank", "package_id"]).to_csv(
        OUT / "scenario_rankings.tsv", sep="\t", index=False
    )
    rank_summary.sort_values(["median_rank", "worst_rank", "package_id"]).to_csv(
        OUT / "rank_stability.tsv", sep="\t", index=False
    )
    portfolio_frame.sort_values(
        ["portfolio_size", "pareto", "n_methods", "n_decisions", "burden_max"],
        ascending=[True, False, False, False, True],
    ).to_csv(OUT / "portfolio_frontier.tsv", sep="\t", index=False)

    summary = {
        "n_packages": len(PACKAGES),
        "n_methods_in_union": len(set().union(*(split_set(item["methods"]) for item in PACKAGES))),
        "n_decisions_in_union": len(set().union(*(split_set(item["decisions"]) for item in PACKAGES))),
        "n_scenarios": len(SCENARIOS),
        "n_portfolios_evaluated": len(portfolio_frame),
        "one_package_pareto": sorted(one_package_pareto),
        "robust_first_ask": robust.package_id.tolist(),
        "verdict": "ROBUST_FIRST_ASK" if len(robust) == 1 else "NO_SINGLE_ROBUST_WINNER_USE_PARETO_FRONTIER",
        "boundary": "Operational method-unlock analysis only; weights are decision priorities and burden is ordinal. No biological-success probability or MS effect is estimated.",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    report = """# V57 Cross-Method Data-Unlock Portfolio

## Result

Status: **NO_SINGLE_ROBUST_WINNER_USE_PARETO_FRONTIER**.

Eight prospective package types were mapped to 21 currently blocked or
unverified method classes and 19 decision types. All 92 one-, two-, and
three-package portfolios were evaluated under six predeclared priority views.
No single package ranked first in at least four views while remaining
Pareto-optimal.

## Decision-Specific First Asks

| Objective | First package | Reason |
|---|---|---|
| Validate the one live monitoring lead | `D01_independent_ms_response_bulk` | Lowest ordinal burden; unlocks external validation, environment stability, selective prediction, and sequential accumulation |
| Test progression biology prospectively | `D03_longitudinal_progression_molecular_ipd` | Only package that directly links an earlier molecular state to confirmed disability accumulation |
| Estimate and transport a progression treatment effect | `D04_randomized_progression_trial_ipd` | Randomization supports the strongest causal-treatment estimand; transport still requires overlap |
| Resolve intervention direction and function | `D06_primary_human_directional_perturbation` | Directly tests selective direction, target engagement, function, viability, and host-defense liabilities |

The one-package Pareto frontier also contains `D02` (paired MS single-cell
trajectory) and `D05` (randomized molecular progression substudy). Spatial
data and genotype-linked perturbation remain useful specialist packages but
are not robust first asks under these planning views.

## Portfolio Consequence

No universal acquisition order is defensible because the objectives are not
interchangeable. If two packages can be pursued in parallel, the Pareto set
contains four distinct strategies:

- `D01 + D04`: low-burden live-lead validation plus causal progression-trial
  inference;
- `D01 + D02`: monitoring validation plus within-cell, composition, and
  trajectory resolution;
- `D02 + D04`: cell-state resolution plus causal clinical inference; and
- `D04 + D05`: clinical treatment effect plus a molecular substudy.

The appropriate choice therefore follows the decision: validate now, explain
progression, estimate treatment effect, or establish intervention direction.
This analysis does not assign probabilities that any package will reveal a
useful mechanism.

## Boundary

This is operational decision support. Ordinal burdens are not costs, scenario
weights are not biological-effect priors, and package receipt does not bypass
the V42/V54 quality and identifiability gates.
"""
    (OUT / "REPORT.md").write_text(report)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
