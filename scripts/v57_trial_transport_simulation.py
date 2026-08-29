#!/usr/bin/env python3
"""Seeded synthetic verification of trial-to-trial effect transport."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy.special import expit


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "analysis/v57_trial_transport/synthetic"
SEEDS = (57061, 57062, 57063)
SCENARIOS = ("covariate_shift_only", "hidden_target_modifier", "positivity_failure")
N_REPLICATES = 250
N_SOURCE = 800
N_TARGET = 800


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--replicates", type=int, default=N_REPLICATES)
    return parser.parse_args()


def logistic_irls(x: np.ndarray, y: np.ndarray, ridge: float = 1e-6) -> np.ndarray:
    beta = np.zeros(x.shape[1], dtype=np.float64)
    penalty = np.eye(x.shape[1]) * ridge
    penalty[0, 0] = 0.0
    for _ in range(60):
        eta = np.clip(np.einsum("ij,j->i", x, beta, optimize=False), -30.0, 30.0)
        probability = expit(eta)
        weight = np.maximum(probability * (1.0 - probability), 1e-6)
        hessian = np.einsum("ni,n,nj->ij", x, weight, x, optimize=False) + penalty
        gradient = np.einsum(
            "ni,n->i", x, y - probability, optimize=False
        ) - np.einsum("ij,j->i", penalty, beta, optimize=False)
        step = np.linalg.solve(hessian, gradient)
        beta_new = beta + step
        if np.max(np.abs(step)) < 1e-8:
            return beta_new
        beta = beta_new
    return beta


def outcome_design(covariates: np.ndarray, treatment: np.ndarray) -> np.ndarray:
    treatment = treatment[:, None]
    return np.column_stack(
        [np.ones(len(covariates)), treatment, covariates, treatment * covariates]
    )


def linear_predict(x: np.ndarray, beta: np.ndarray) -> np.ndarray:
    return np.einsum("ij,j->i", x, beta, optimize=False)


def generate_trial_pair(
    rng: np.random.Generator,
    scenario: str,
    n_source: int = N_SOURCE,
    n_target: int = N_TARGET,
) -> dict[str, np.ndarray | float]:
    source_x = rng.normal(size=(n_source, 4))
    if scenario == "positivity_failure":
        target_x = rng.normal(
            loc=np.array([3.0, -1.5, 0.8, 1.2]),
            scale=np.array([0.45, 0.65, 1.0, 0.8]),
            size=(n_target, 4),
        )
    else:
        target_x = rng.normal(
            loc=np.array([0.60, -0.40, 0.30, 0.50]), size=(n_target, 4)
        )
    source_t = rng.integers(0, 2, size=n_source).astype(float)
    target_t = rng.integers(0, 2, size=n_target).astype(float)
    baseline_beta = np.array([0.35, -0.30, 0.20, 0.25])
    modifier_beta = np.array([-0.25, 0.15, 0.10, -0.10])

    def probabilities(x: np.ndarray, treatment: np.ndarray, target_extra: float) -> np.ndarray:
        baseline = -1.0 + linear_predict(x, baseline_beta)
        treatment_log_odds = -0.55 + linear_predict(x, modifier_beta) + target_extra
        return expit(baseline + treatment * treatment_log_odds)

    source_probability = probabilities(source_x, source_t, 0.0)
    target_extra = 0.85 if scenario == "hidden_target_modifier" else 0.0
    target_probability = probabilities(target_x, target_t, target_extra)
    source_y = rng.binomial(1, source_probability).astype(float)
    target_y = rng.binomial(1, target_probability).astype(float)
    target_probability_1 = probabilities(target_x, np.ones(n_target), target_extra)
    target_probability_0 = probabilities(target_x, np.zeros(n_target), target_extra)
    true_target_risk_difference = float(np.mean(target_probability_1 - target_probability_0))
    source_mechanism_target_risk_difference = float(
        np.mean(
            probabilities(target_x, np.ones(n_target), 0.0)
            - probabilities(target_x, np.zeros(n_target), 0.0)
        )
    )
    return {
        "source_x": source_x,
        "target_x": target_x,
        "source_t": source_t,
        "target_t": target_t,
        "source_y": source_y,
        "target_y": target_y,
        "true_target_risk_difference": true_target_risk_difference,
        "source_mechanism_target_risk_difference": source_mechanism_target_risk_difference,
    }


def weighted_mean(values: np.ndarray, weights: np.ndarray) -> float:
    return float(np.sum(weights * values) / np.sum(weights))


def estimate_transport(data: dict[str, np.ndarray | float]) -> dict[str, float | bool]:
    source_x = np.asarray(data["source_x"])
    target_x = np.asarray(data["target_x"])
    source_t = np.asarray(data["source_t"])
    target_t = np.asarray(data["target_t"])
    source_y = np.asarray(data["source_y"])
    target_y = np.asarray(data["target_y"])

    n_source = len(source_x)
    n_target = len(target_x)
    pooled_x = np.vstack([source_x, target_x])
    target_indicator = np.concatenate([np.zeros(n_source), np.ones(n_target)])
    sampling_design = np.column_stack([np.ones(len(pooled_x)), pooled_x])
    sampling_beta = logistic_irls(sampling_design, target_indicator)
    source_target_probability = np.clip(
        expit(linear_predict(np.column_stack([np.ones(n_source), source_x]), sampling_beta)),
        1e-5,
        1.0 - 1e-5,
    )
    sampling_weight = source_target_probability / (1.0 - source_target_probability)
    sampling_weight *= n_source / n_target

    effective_n = float(np.sum(sampling_weight) ** 2 / np.sum(sampling_weight**2))
    source_weighted_mean = np.array(
        [weighted_mean(source_x[:, index], sampling_weight) for index in range(4)]
    )
    target_mean = np.mean(target_x, axis=0)
    pooled_sd = np.sqrt(
        (np.var(source_x, axis=0, ddof=1) + np.var(target_x, axis=0, ddof=1)) / 2.0
    )
    max_smd = float(np.max(np.abs(source_weighted_mean - target_mean) / pooled_sd))
    max_weight = float(np.max(sampling_weight))
    overlap_pass = bool(
        effective_n >= 0.30 * n_source and max_weight <= 20.0 and max_smd <= 0.10
    )

    treated = source_t == 1
    ipw = weighted_mean(source_y[treated], sampling_weight[treated]) - weighted_mean(
        source_y[~treated], sampling_weight[~treated]
    )
    outcome_beta = logistic_irls(outcome_design(source_x, source_t), source_y)
    target_m1 = expit(linear_predict(outcome_design(target_x, np.ones(n_target)), outcome_beta))
    target_m0 = expit(linear_predict(outcome_design(target_x, np.zeros(n_target)), outcome_beta))
    outcome_standardized = float(np.mean(target_m1 - target_m0))

    source_m1 = expit(linear_predict(outcome_design(source_x, np.ones(n_source)), outcome_beta))
    source_m0 = expit(linear_predict(outcome_design(source_x, np.zeros(n_source)), outcome_beta))
    residual = (
        source_t / 0.5 * (source_y - source_m1)
        - (1.0 - source_t) / 0.5 * (source_y - source_m0)
    )
    doubly_robust = outcome_standardized + weighted_mean(residual, sampling_weight)
    target_randomized = float(
        np.mean(target_y[target_t == 1]) - np.mean(target_y[target_t == 0])
    )
    return {
        "ipw_transport": ipw,
        "outcome_standardized_transport": outcome_standardized,
        "doubly_robust_transport": doubly_robust,
        "target_randomized_risk_difference": target_randomized,
        "true_target_risk_difference": float(data["true_target_risk_difference"]),
        "source_mechanism_target_risk_difference": float(
            data["source_mechanism_target_risk_difference"]
        ),
        "dr_error_to_true_target": doubly_robust - float(data["true_target_risk_difference"]),
        "transport_target_randomized_discrepancy": doubly_robust - target_randomized,
        "ipw_or_disagreement": ipw - outcome_standardized,
        "sampling_weight_effective_n": effective_n,
        "sampling_weight_effective_fraction": effective_n / n_source,
        "max_sampling_weight": max_weight,
        "max_weighted_smd": max_smd,
        "overlap_pass": overlap_pass,
        "synthetic": True,
    }


def summarize(rows: pd.DataFrame) -> pd.DataFrame:
    summaries = []
    for (seed, scenario), frame in rows.groupby(["seed", "scenario"], sort=True):
        eligible = frame[frame.overlap_pass]
        summaries.append(
            {
                "seed": seed,
                "scenario": scenario,
                "replicates": len(frame),
                "overlap_pass_rate": float(frame.overlap_pass.mean()),
                "overlap_reject_rate": float(1.0 - frame.overlap_pass.mean()),
                "mean_dr_error_to_true_target": float(frame.dr_error_to_true_target.mean()),
                "mean_abs_dr_error_to_true_target": float(
                    frame.dr_error_to_true_target.abs().mean()
                ),
                "p90_abs_dr_error_to_true_target": float(
                    frame.dr_error_to_true_target.abs().quantile(0.90)
                ),
                "eligible_discrepancy_gt_008_rate": float(
                    eligible.transport_target_randomized_discrepancy.abs().gt(0.08).mean()
                )
                if len(eligible)
                else math.nan,
                "median_effective_fraction": float(
                    frame.sampling_weight_effective_fraction.median()
                ),
                "median_max_weighted_smd": float(frame.max_weighted_smd.median()),
                "synthetic": True,
            }
        )
    return pd.DataFrame(summaries)


def main() -> None:
    args = parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []
    for seed in SEEDS:
        rng = np.random.default_rng(seed)
        for scenario in SCENARIOS:
            for replicate in range(args.replicates):
                estimates = estimate_transport(generate_trial_pair(rng, scenario))
                rows.append(
                    {
                        "seed": seed,
                        "scenario": scenario,
                        "replicate": replicate,
                        **estimates,
                    }
                )
    frame = pd.DataFrame(rows)
    summary_table = summarize(frame)

    covariate = summary_table[summary_table.scenario.eq("covariate_shift_only")]
    hidden = summary_table[summary_table.scenario.eq("hidden_target_modifier")]
    positivity = summary_table[summary_table.scenario.eq("positivity_failure")]
    gates = {
        "covariate_shift_all_seeds_pass": bool(
            covariate.overlap_pass_rate.ge(0.90).all()
            and covariate.mean_abs_dr_error_to_true_target.le(0.03).all()
        ),
        "hidden_modifier_all_seeds_pass": bool(
            hidden.eligible_discrepancy_gt_008_rate.ge(0.80).all()
        ),
        "positivity_failure_all_seeds_pass": bool(
            positivity.overlap_reject_rate.ge(0.90).all()
        ),
    }
    overall = bool(all(gates.values()))
    summary = {
        "purpose": "Synthetic method verification only; no MS or treatment evidence",
        "plan": "docs/plans/V57_TRIAL_TRANSPORT_PLAN.md",
        "seeds": list(SEEDS),
        "scenarios": list(SCENARIOS),
        "replicates_per_seed_scenario": args.replicates,
        "total_synthetic_trial_pairs": len(frame),
        "n_source_per_pair": N_SOURCE,
        "n_target_per_pair": N_TARGET,
        "gates": gates,
        "overall_method_verification": overall,
        "verdict": "TRIAL_TRANSPORT_HARNESS_VERIFIED"
        if overall
        else "TRIAL_TRANSPORT_HARNESS_NOT_VERIFIED",
        "boundary": "Controlled real IPD and real overlap/exchangeability audits are still required",
    }
    frame.to_csv(
        args.outdir / "synthetic_trial_pair_results.tsv.gz",
        sep="\t",
        index=False,
        compression={"method": "gzip", "mtime": 0},
    )
    summary_table.to_csv(args.outdir / "synthetic_scenario_summary.tsv", sep="\t", index=False)
    (args.outdir / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    report = f"""# V57 Trial-to-Trial Transport Method Verification

## Synthetic-Only Boundary

Every result here comes from seeded synthetic trials. This characterizes a
method and is not biological or treatment evidence about MS.

## Scale

- Synthetic trial pairs: {len(frame):,}
- Seeds: {', '.join(map(str, SEEDS))}
- Source/target participants per pair: {N_SOURCE}/{N_TARGET}

## Gates

| Gate | Passed across all seeds |
|---|---|
| Covariate shift recovered with adequate overlap | {gates['covariate_shift_all_seeds_pass']} |
| Hidden target modifier produces detectable incompatibility | {gates['hidden_modifier_all_seeds_pass']} |
| Positivity failure is rejected | {gates['positivity_failure_all_seeds_pass']} |

Verdict: **{summary['verdict']}**.

If verified, this method is worth applying only inside an approved controlled
environment holding harmonized source and target randomized trial IPD. It can
test whether measured population composition accounts for a trial difference;
it cannot prove exchangeability, repair endpoint mismatch, or infer an MS
effect from synthetic data.
"""
    (args.outdir / "REPORT.md").write_text(report, encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
