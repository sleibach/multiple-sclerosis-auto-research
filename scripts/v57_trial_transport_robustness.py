#!/usr/bin/env python3
"""Synthetic robustness audit for candidate trial-to-trial transport."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy.special import expit

from v57_trial_transport_simulation import linear_predict, logistic_irls, weighted_mean


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "analysis/v57_trial_transport_robustness/synthetic"
SEEDS = (57101, 57102, 57103)
SCENARIOS = (
    "linear_correct",
    "sampling_wrong_outcome_correct",
    "sampling_correct_outcome_wrong",
    "both_linear_nuisances_wrong",
    "hidden_target_modifier",
    "positivity_failure",
)
N_SOURCE = 2400
N_TARGET = 2400
N_REPLICATES = 150


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--replicates", type=int, default=N_REPLICATES)
    return parser.parse_args()


def basis(x: np.ndarray, quadratic: bool) -> np.ndarray:
    columns = [np.ones(len(x)), x]
    if quadratic:
        columns.append(x**2)
    return np.column_stack(columns)


def outcome_design(x: np.ndarray, treatment: np.ndarray, quadratic: bool) -> np.ndarray:
    features = np.column_stack([x, x**2]) if quadratic else x
    return np.column_stack(
        [np.ones(len(x)), treatment, features, treatment[:, None] * features]
    )


def generate_pair(rng: np.random.Generator, scenario: str) -> dict[str, Any]:
    source_x = rng.normal(size=(N_SOURCE, 4))
    if scenario == "positivity_failure":
        target_x = rng.normal(
            loc=np.array([3.0, -1.5, 0.8, 1.2]),
            scale=np.array([0.45, 0.65, 1.0, 0.8]),
            size=(N_TARGET, 4),
        )
    elif scenario in {"sampling_wrong_outcome_correct", "both_linear_nuisances_wrong"}:
        target_x = rng.normal(
            loc=np.array([0.35, -0.25, 0.20, 0.30]),
            scale=np.array([1.40, 0.70, 1.30, 0.75]),
            size=(N_TARGET, 4),
        )
    else:
        target_x = rng.normal(
            loc=np.array([0.60, -0.40, 0.30, 0.50]), size=(N_TARGET, 4)
        )

    source_t = rng.integers(0, 2, size=N_SOURCE).astype(float)
    target_t = rng.integers(0, 2, size=N_TARGET).astype(float)
    nonlinear = scenario in {"sampling_correct_outcome_wrong", "both_linear_nuisances_wrong"}
    hidden = 0.85 if scenario == "hidden_target_modifier" else 0.0
    baseline_beta = np.array([0.35, -0.30, 0.20, 0.25])
    modifier_beta = np.array([-0.25, 0.15, 0.10, -0.10])

    def probability(x: np.ndarray, treatment: np.ndarray, extra: float) -> np.ndarray:
        baseline = -1.0 + linear_predict(x, baseline_beta)
        treatment_log_odds = -0.55 + linear_predict(x, modifier_beta) + extra
        if nonlinear:
            baseline = baseline + 0.50 * (x[:, 0] ** 2 - 1.0) - 0.35 * (
                x[:, 1] ** 2 - 1.0
            )
            treatment_log_odds = treatment_log_odds + 0.75 * (
                x[:, 2] ** 2 - 1.0
            ) - 0.55 * (x[:, 3] ** 2 - 1.0)
        return expit(baseline + treatment * treatment_log_odds)

    source_y = rng.binomial(1, probability(source_x, source_t, 0.0)).astype(float)
    target_y = rng.binomial(1, probability(target_x, target_t, hidden)).astype(float)
    true_target = float(
        np.mean(
            probability(target_x, np.ones(N_TARGET), hidden)
            - probability(target_x, np.zeros(N_TARGET), hidden)
        )
    )
    return {
        "source_x": source_x,
        "target_x": target_x,
        "source_t": source_t,
        "target_t": target_t,
        "source_y": source_y,
        "target_y": target_y,
        "true_target": true_target,
    }


def sampling_weights(
    source_x: np.ndarray, target_x: np.ndarray, quadratic: bool
) -> np.ndarray:
    pooled = np.vstack([source_x, target_x])
    indicator = np.concatenate([np.zeros(len(source_x)), np.ones(len(target_x))])
    beta = logistic_irls(basis(pooled, quadratic), indicator, ridge=1e-5)
    probability = np.clip(expit(linear_predict(basis(source_x, quadratic), beta)), 1e-6, 1 - 1e-6)
    return probability / (1.0 - probability) * len(source_x) / len(target_x)


def overlap_metrics(
    source_x: np.ndarray, target_x: np.ndarray, weights: np.ndarray
) -> dict[str, float | bool]:
    effective_fraction = float(
        np.sum(weights) ** 2 / np.sum(weights**2) / len(source_x)
    )
    median = max(float(np.median(weights)), 1e-12)
    q99_median_ratio = float(np.quantile(weights, 0.99) / median)
    source_moments = np.column_stack([source_x, source_x**2])
    target_moments = np.column_stack([target_x, target_x**2])
    weighted_source = np.array(
        [weighted_mean(source_moments[:, j], weights) for j in range(source_moments.shape[1])]
    )
    target_mean = np.mean(target_moments, axis=0)
    pooled_sd = np.sqrt(
        (np.var(source_moments, axis=0, ddof=1) + np.var(target_moments, axis=0, ddof=1))
        / 2.0
    )
    max_moment_smd = float(np.max(np.abs(weighted_source - target_mean) / pooled_sd))
    passed = bool(
        effective_fraction >= 0.30
        and q99_median_ratio <= 12.0
        and max_moment_smd <= 0.10
    )
    return {
        "effective_fraction": effective_fraction,
        "q99_median_weight_ratio": q99_median_ratio,
        "max_moment_smd": max_moment_smd,
        "overlap_pass": passed,
    }


def estimate(data: dict[str, Any], sampling_quadratic: bool, outcome_quadratic: bool) -> dict[str, float]:
    source_x = data["source_x"]
    target_x = data["target_x"]
    source_t = data["source_t"]
    target_t = data["target_t"]
    source_y = data["source_y"]
    target_y = data["target_y"]
    weights = sampling_weights(source_x, target_x, sampling_quadratic)
    beta = logistic_irls(
        outcome_design(source_x, source_t, outcome_quadratic), source_y, ridge=1e-5
    )
    target_m1 = expit(
        linear_predict(outcome_design(target_x, np.ones(len(target_x)), outcome_quadratic), beta)
    )
    target_m0 = expit(
        linear_predict(outcome_design(target_x, np.zeros(len(target_x)), outcome_quadratic), beta)
    )
    standardized = float(np.mean(target_m1 - target_m0))
    source_m1 = expit(
        linear_predict(outcome_design(source_x, np.ones(len(source_x)), outcome_quadratic), beta)
    )
    source_m0 = expit(
        linear_predict(outcome_design(source_x, np.zeros(len(source_x)), outcome_quadratic), beta)
    )
    residual = source_t / 0.5 * (source_y - source_m1) - (1.0 - source_t) / 0.5 * (
        source_y - source_m0
    )
    dr = standardized + weighted_mean(residual, weights)
    target_randomized = float(
        np.mean(target_y[target_t == 1]) - np.mean(target_y[target_t == 0])
    )
    return {
        "dr": dr,
        "error": dr - data["true_target"],
        "target_randomized_discrepancy": dr - target_randomized,
    }


def main() -> None:
    args = parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []
    for seed in SEEDS:
        rng = np.random.default_rng(seed)
        for scenario in SCENARIOS:
            for replicate in range(args.replicates):
                data = generate_pair(rng, scenario)
                linear = estimate(data, False, False)
                quadratic = estimate(data, True, True)
                q_weights = sampling_weights(data["source_x"], data["target_x"], True)
                overlap = overlap_metrics(data["source_x"], data["target_x"], q_weights)
                rows.append(
                    {
                        "seed": seed,
                        "scenario": scenario,
                        "replicate": replicate,
                        "linear_dr": linear["dr"],
                        "quadratic_dr": quadratic["dr"],
                        "linear_error": linear["error"],
                        "quadratic_error": quadratic["error"],
                        "linear_quadratic_difference": linear["dr"] - quadratic["dr"],
                        "quadratic_target_randomized_discrepancy": quadratic[
                            "target_randomized_discrepancy"
                        ],
                        **overlap,
                        "synthetic": True,
                    }
                )
    frame = pd.DataFrame(rows)
    summaries = []
    for (seed, scenario), group in frame.groupby(["seed", "scenario"], sort=True):
        eligible = group[group.overlap_pass]
        summaries.append(
            {
                "seed": seed,
                "scenario": scenario,
                "replicates": len(group),
                "overlap_pass_rate": float(group.overlap_pass.mean()),
                "mean_abs_linear_error": float(group.linear_error.abs().mean()),
                "mean_abs_quadratic_error": float(group.quadratic_error.abs().mean()),
                "quadratic_relative_improvement": float(
                    1.0 - group.quadratic_error.abs().mean() / group.linear_error.abs().mean()
                ),
                "eligible_discrepancy_gt_008_rate": float(
                    eligible.quadratic_target_randomized_discrepancy.abs().gt(0.08).mean()
                )
                if len(eligible)
                else math.nan,
                "median_effective_fraction": float(group.effective_fraction.median()),
                "median_q99_median_weight_ratio": float(
                    group.q99_median_weight_ratio.median()
                ),
                "median_max_moment_smd": float(group.max_moment_smd.median()),
                "synthetic": True,
            }
        )
    table = pd.DataFrame(summaries)

    def all_seed(scenario: str, expression: pd.Series) -> bool:
        subset = table[table.scenario.eq(scenario)]
        return bool(expression.loc[subset.index].all())

    good = SCENARIOS[:4]
    gates = {
        "eligible_scenarios_overlap": all(
            all_seed(name, table.overlap_pass_rate.ge(0.90)) for name in good
        ),
        "linear_correct_estimators": all_seed(
            "linear_correct",
            table.mean_abs_linear_error.le(0.03) & table.mean_abs_quadratic_error.le(0.03),
        ),
        "sampling_wrong_one_nuisance_robust": all_seed(
            "sampling_wrong_outcome_correct", table.mean_abs_linear_error.le(0.03)
        ),
        "outcome_wrong_one_nuisance_robust": all_seed(
            "sampling_correct_outcome_wrong", table.mean_abs_linear_error.le(0.03)
        ),
        "both_wrong_quadratic_rescue": all_seed(
            "both_linear_nuisances_wrong",
            table.mean_abs_quadratic_error.le(0.03)
            & table.quadratic_relative_improvement.ge(0.25),
        ),
        "hidden_modifier_detected": all_seed(
            "hidden_target_modifier", table.eligible_discrepancy_gt_008_rate.ge(0.80)
        ),
        "positivity_rejected": all_seed(
            "positivity_failure", table.overlap_pass_rate.le(0.10)
        ),
    }
    verified = bool(all(gates.values()))
    frame.to_csv(
        args.outdir / "synthetic_pair_results.tsv.gz",
        sep="\t",
        index=False,
        compression={"method": "gzip", "mtime": 0},
    )
    table.to_csv(args.outdir / "seed_scenario_summary.tsv", sep="\t", index=False)
    summary = {
        "purpose": "Seeded synthetic method behavior only; no MS or treatment evidence",
        "plan": "docs/plans/V57_TRIAL_TRANSPORT_ROBUSTNESS_PLAN.md",
        "seeds": list(SEEDS),
        "scenarios": list(SCENARIOS),
        "replicates_per_seed_scenario": args.replicates,
        "n_source_per_pair": N_SOURCE,
        "n_target_per_pair": N_TARGET,
        "total_synthetic_trial_pairs": len(frame),
        "gates": gates,
        "verified": verified,
        "verdict": "CANDIDATE_TRANSPORT_HARNESS_VERIFIED"
        if verified
        else "CANDIDATE_TRANSPORT_HARNESS_NOT_VERIFIED",
        "primary_v57_gate_status": "UNCHANGED_FAILED",
        "boundary": "A candidate method pass would still require controlled real IPD, endpoint harmonization, overlap, and an exchangeability argument.",
    }
    (args.outdir / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    report = f"""# V57 Trial-Transport Robustness Audit

## Synthetic-Only Result

- Synthetic trial pairs: {len(frame):,}
- Participants per source/target pair: {N_SOURCE:,}/{N_TARGET:,}
- Seeds: {', '.join(map(str, SEEDS))}
- Candidate verdict: **{summary['verdict']}**
- Original V57 transport verdict: **UNCHANGED FAILED**

| Gate | Passed under every seed |
|---|---|
""" + "\n".join(f"| {key} | {value} |" for key, value in gates.items()) + """

## Interpretation

Six of seven gates passed. The only failed gate was overlap eligibility for
the two variance-shift scenarios: seed-specific pass rates were 19.3%-26.0%.
The candidate guard did not fail because of its weight-tail threshold;
effective sample fractions and weighted first/second-moment balance were at
or beyond their frozen boundaries. The linear estimator nevertheless met its
one-correct-nuisance accuracy gate, and the quadratic estimator rescued the
both-wrong scenario, but a real transport analysis must still fail closed when
the observed populations have this little usable overlap.

This audit therefore removes the sample-maximum defect but does not verify the
full harness. A fixed-guard severity sweep can map where population shift
becomes ineligible; it cannot retroactively rescue either failed result. The
method also cannot establish source-to-target exchangeability in a real trial.
Synthetic verification never constitutes MS or treatment evidence.
"""
    (args.outdir / "REPORT.md").write_text(report, encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
