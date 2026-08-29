#!/usr/bin/env python3
"""Prior-sensitive hierarchical meta-prediction for held V22 environments."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy.special import logsumexp

from v57_environment_stability_probe import cohort_metrics, load_data


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "analysis/v57_hierarchical_environment"
SEED = 57051
N_PERMUTATIONS = 20_000
MU_SDS = (0.5, 1.0, 2.0)
TAU_SCALES = (0.25, 0.5, 1.0, 2.0)
REFERENCE_MU_SD = 1.0
REFERENCE_TAU_SCALE = 0.5


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--seed", type=int, default=SEED)
    parser.add_argument("--permutations", type=int, default=N_PERMUTATIONS)
    return parser.parse_args()


def log_normal(value: np.ndarray, mean: np.ndarray, variance: np.ndarray) -> np.ndarray:
    return -0.5 * (
        np.log(2.0 * math.pi * variance) + (value - mean) ** 2 / variance
    )


def posterior_tau(
    effects: np.ndarray,
    variances: np.ndarray,
    mu_sd: float,
    tau_scale: float,
    tau: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    total_variance = variances[:, None] + tau[None, :] ** 2
    weight = 1.0 / total_variance
    posterior_variance = 1.0 / (1.0 / mu_sd**2 + np.sum(weight, axis=0))
    posterior_mean = posterior_variance * np.sum(weight * effects[:, None], axis=0)
    log_marginal = (
        -0.5 * np.sum(np.log(2.0 * math.pi * total_variance), axis=0)
        - 0.5 * np.sum(weight * effects[:, None] ** 2, axis=0)
        + 0.5 * posterior_mean**2 / posterior_variance
        + 0.5 * np.log(posterior_variance / mu_sd**2)
    )
    log_prior = -0.5 * (tau / tau_scale) ** 2
    integration_weight = np.ones(len(tau))
    integration_weight[[0, -1]] = 0.5
    log_weight = log_marginal + log_prior + np.log(integration_weight)
    log_weight -= logsumexp(log_weight)
    return log_weight, posterior_mean, posterior_variance


def predictive_log_density(
    held_effect: float,
    held_variance: float,
    log_weight: np.ndarray,
    mean: np.ndarray,
    variance: np.ndarray,
    tau: np.ndarray,
) -> float:
    predictive_variance = held_variance + tau**2 + variance
    return float(
        logsumexp(
            log_weight
            + log_normal(np.array(held_effect), mean, predictive_variance)
        )
    )


def fixed_log_density(
    train_effect: np.ndarray,
    train_variance: np.ndarray,
    held_effect: float,
    held_variance: float,
    mu_sd: float,
) -> float:
    weight = 1.0 / train_variance
    variance = 1.0 / (1.0 / mu_sd**2 + np.sum(weight))
    mean = variance * np.sum(weight * train_effect)
    return float(log_normal(np.array(held_effect), np.array(mean), np.array(held_variance + variance)))


def loo_scores(
    effects: np.ndarray,
    variances: np.ndarray,
    cohorts: list[str],
    mu_sd: float,
    tau_scale: float,
    tau: np.ndarray,
) -> tuple[pd.DataFrame, float]:
    rows: list[dict[str, Any]] = []
    for held in range(len(effects)):
        train = np.arange(len(effects)) != held
        log_weight, mean, variance = posterior_tau(
            effects[train], variances[train], mu_sd, tau_scale, tau
        )
        hierarchical = predictive_log_density(
            effects[held], variances[held], log_weight, mean, variance, tau
        )
        fixed = fixed_log_density(
            effects[train], variances[train], effects[held], variances[held], mu_sd
        )
        rows.append(
            {
                "held_out_cohort": cohorts[held],
                "observed_hedges_g": effects[held],
                "hierarchical_log_predictive_density": hierarchical,
                "fixed_tau0_log_predictive_density": fixed,
                "hierarchical_minus_fixed": hierarchical - fixed,
            }
        )
    frame = pd.DataFrame(rows)
    return frame, float(frame.hierarchical_minus_fixed.sum())


def full_posterior_summary(
    effects: np.ndarray,
    variances: np.ndarray,
    mu_sd: float,
    tau_scale: float,
    tau: np.ndarray,
) -> dict[str, float]:
    log_weight, mean, variance = posterior_tau(effects, variances, mu_sd, tau_scale, tau)
    weight = np.exp(log_weight)
    tau_cdf = np.cumsum(weight)
    tau_median = float(tau[np.searchsorted(tau_cdf, 0.5)])
    posterior_mu_mean = float(np.sum(weight * mean))
    probability_positive = float(
        np.sum(weight * 0.5 * (1.0 + np.vectorize(math.erf)(mean / np.sqrt(2.0 * variance))))
    )
    return {
        "posterior_mu_mean": posterior_mu_mean,
        "posterior_probability_mu_positive": probability_positive,
        "posterior_tau_median": tau_median,
    }


def permuted_effects(
    data: pd.DataFrame, rng: np.random.Generator, n_permutations: int
) -> tuple[np.ndarray, np.ndarray, list[str]]:
    cohorts = sorted(data.cohort.unique())
    effects = np.empty((n_permutations, len(cohorts)), dtype=np.float64)
    variances = np.empty_like(effects)
    for cohort_index, cohort in enumerate(cohorts):
        frame = data[data.cohort.eq(cohort)]
        score = frame.locked_signed_score.to_numpy(float)
        n = len(score)
        n1 = int(frame.response_binary.sum())
        n0 = n - n1
        random_order = rng.random((n_permutations, n), dtype=np.float32)
        selected = np.argpartition(random_order, n1 - 1, axis=1)[:, :n1]
        label = np.zeros((n_permutations, n), dtype=np.float64)
        label[np.arange(n_permutations)[:, None], selected] = 1.0
        sum1 = np.einsum("bi,i->b", label, score, optimize=False)
        sumsq1 = np.einsum("bi,i->b", label, score * score, optimize=False)
        sum0 = np.sum(score) - sum1
        sumsq0 = np.sum(score * score) - sumsq1
        mean1 = sum1 / n1
        mean0 = sum0 / n0
        var1 = (sumsq1 - sum1 * sum1 / n1) / (n1 - 1)
        var0 = (sumsq0 - sum0 * sum0 / n0) / (n0 - 1)
        pooled = ((n1 - 1) * var1 + (n0 - 1) * var0) / (n1 + n0 - 2)
        correction = 1.0 - 3.0 / (4.0 * (n1 + n0) - 9.0)
        g = correction * (mean1 - mean0) / np.sqrt(np.maximum(pooled, 1e-15))
        effects[:, cohort_index] = g
        variances[:, cohort_index] = (n1 + n0) / (n1 * n0) + g * g / (
            2.0 * (n1 + n0 - 2)
        )
    return effects, variances, cohorts


def batched_null_gains(
    effects: np.ndarray,
    variances: np.ndarray,
    mu_sd: float,
    tau_scale: float,
    tau: np.ndarray,
    batch_size: int = 1000,
) -> np.ndarray:
    output = np.empty(len(effects), dtype=np.float64)
    tau2 = tau**2
    log_prior = -0.5 * (tau / tau_scale) ** 2
    integration = np.ones(len(tau))
    integration[[0, -1]] = 0.5
    log_prior = log_prior + np.log(integration)
    for start in range(0, len(effects), batch_size):
        stop = min(start + batch_size, len(effects))
        y = effects[start:stop]
        v = variances[start:stop]
        gain = np.zeros(stop - start, dtype=np.float64)
        for held in range(y.shape[1]):
            train = np.arange(y.shape[1]) != held
            train_y = y[:, train]
            train_v = v[:, train]
            total_variance = train_v[:, :, None] + tau2[None, None, :]
            weight = 1.0 / total_variance
            post_variance = 1.0 / (1.0 / mu_sd**2 + np.sum(weight, axis=1))
            post_mean = post_variance * np.sum(weight * train_y[:, :, None], axis=1)
            log_marginal = (
                -0.5 * np.sum(np.log(2.0 * math.pi * total_variance), axis=1)
                - 0.5 * np.sum(weight * train_y[:, :, None] ** 2, axis=1)
                + 0.5 * post_mean**2 / post_variance
                + 0.5 * np.log(post_variance / mu_sd**2)
            )
            log_post = log_marginal + log_prior[None, :]
            log_post -= logsumexp(log_post, axis=1)[:, None]
            prediction_variance = v[:, held, None] + tau2[None, :] + post_variance
            hierarchy = logsumexp(
                log_post
                + log_normal(y[:, held, None], post_mean, prediction_variance),
                axis=1,
            )
            fixed_weight = 1.0 / train_v
            fixed_variance = 1.0 / (1.0 / mu_sd**2 + np.sum(fixed_weight, axis=1))
            fixed_mean = fixed_variance * np.sum(fixed_weight * train_y, axis=1)
            fixed = log_normal(
                y[:, held], fixed_mean, v[:, held] + fixed_variance
            )
            gain += hierarchy - fixed
        output[start:stop] = gain
    return output


def main() -> None:
    args = parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)
    data = load_data()
    metrics = cohort_metrics(data).sort_values("cohort").reset_index(drop=True)
    cohorts = metrics.cohort.tolist()
    effects = metrics.hedges_g.to_numpy(float)
    variances = metrics.hedges_g_variance.to_numpy(float)
    tau = np.linspace(0.0, 3.0, 2001)

    prior_rows = []
    reference_loo = None
    reference_gain = math.nan
    for mu_sd in MU_SDS:
        for tau_scale in TAU_SCALES:
            loo, gain = loo_scores(
                effects, variances, cohorts, mu_sd, tau_scale, tau
            )
            posterior = full_posterior_summary(
                effects, variances, mu_sd, tau_scale, tau
            )
            prior_rows.append(
                {
                    "mu_sd": mu_sd,
                    "tau_scale": tau_scale,
                    "loo_log_score_gain": gain,
                    "worst_cohort_log_score_gain": float(loo.hierarchical_minus_fixed.min()),
                    **posterior,
                }
            )
            if mu_sd == REFERENCE_MU_SD and tau_scale == REFERENCE_TAU_SCALE:
                reference_loo = loo
                reference_gain = gain
    prior = pd.DataFrame(prior_rows)
    if reference_loo is None:
        raise RuntimeError("Reference prior was not evaluated")

    rng = np.random.default_rng(args.seed)
    null_effects, null_variances, null_cohorts = permuted_effects(
        data, rng, args.permutations
    )
    if null_cohorts != cohorts:
        raise ValueError("Null cohort order mismatch")
    null_tau = np.linspace(0.0, 3.0, 301)
    null_gain = batched_null_gains(
        null_effects,
        null_variances,
        REFERENCE_MU_SD,
        REFERENCE_TAU_SCALE,
        null_tau,
    )
    null_p = float((1 + np.sum(null_gain >= reference_gain)) / (len(null_gain) + 1))
    passes = bool(
        prior.loo_log_score_gain.min() >= 2.0
        and null_p <= 0.05
        and reference_loo.hierarchical_minus_fixed.min() >= -1.0
    )
    summary = {
        "purpose": "Method-utility probe around frozen effects; no biological discovery claim",
        "plan": "docs/plans/V57_HIERARCHICAL_ENVIRONMENT_PLAN.md",
        "seed": args.seed,
        "n_environments": len(cohorts),
        "n_null_permutations": args.permutations,
        "reference_prior": {"mu_sd": REFERENCE_MU_SD, "tau_scale": REFERENCE_TAU_SCALE},
        "reference_loo_log_score_gain": reference_gain,
        "reference_gain_null_p": null_p,
        "null_gain_quantiles": {
            "q50": float(np.quantile(null_gain, 0.50)),
            "q90": float(np.quantile(null_gain, 0.90)),
            "q95": float(np.quantile(null_gain, 0.95)),
            "q99": float(np.quantile(null_gain, 0.99)),
        },
        "minimum_prior_sensitivity_gain": float(prior.loo_log_score_gain.min()),
        "maximum_prior_sensitivity_gain": float(prior.loo_log_score_gain.max()),
        "reference_worst_cohort_gain": float(reference_loo.hierarchical_minus_fixed.min()),
        "promotion_gate": passes,
        "verdict": "HIERARCHICAL_TRANSPORT_STUDY_JUSTIFIED"
        if passes
        else "HIERARCHICAL_MODEL_NOT_READY",
    }
    metrics.to_csv(args.outdir / "environment_effects.tsv", sep="\t", index=False)
    prior.to_csv(args.outdir / "prior_sensitivity.tsv", sep="\t", index=False)
    reference_loo.to_csv(args.outdir / "reference_loo_scores.tsv", sep="\t", index=False)
    pd.DataFrame({"null_loo_gain": null_gain}).to_csv(
        args.outdir / "null_loo_gain.tsv.gz", sep="\t", index=False, compression="gzip"
    )
    (args.outdir / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    report = f"""# V57 Hierarchical Environment Model

## Boundary

This compares transport methods around the frozen cohort effects. It is not a
new biomarker or biological finding.

## Result

- Environments: {len(cohorts)}
- Reference-prior LOO log-score gain over `tau=0`: {reference_gain:.3f}
- Within-cohort label-permutation p: {null_p:.4f}
- Gain range over 12 prior settings: {prior.loo_log_score_gain.min():.3f} to
  {prior.loo_log_score_gain.max():.3f}
- Worst reference-prior held-cohort gain: {reference_loo.hierarchical_minus_fixed.min():.3f}

Verdict: **{summary['verdict']}**.

With four environments, explicitly modeling heterogeneity does not earn a
dedicated biological interpretation unless it improves unseen-cohort
prediction robustly across priors and beyond the label null. Failure of that
gate means a richer hierarchy is not a substitute for additional independent
MS environments.
"""
    (args.outdir / "REPORT.md").write_text(report, encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
