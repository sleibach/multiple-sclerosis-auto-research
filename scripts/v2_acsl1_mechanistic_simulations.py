#!/usr/bin/env python3
"""Mechanistic simulations for ACSL1 perturbation.

These are explicit, assumption-driven simulations. They are used to test
whether a plausible therapeutic window exists, not to prove causality.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

SEED = 20260526
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "phases/v2/results"
RNG = np.random.default_rng(SEED)


def simulate_ode(params: dict[str, float], acsl_activity: float, tmax: float = 80.0, dt: float = 0.05) -> dict[str, float]:
    """Three-variable lipid/inflammation model.

    F: free fatty-acid/lipotoxic pool from myelin debris.
    D: stored lipid-droplet pool.
    I: inflammatory output.

    ACSL1 activity increases esterification/storage and debris handling, but
    stored lipid droplets contribute to inflammatory output. Suppression can
    reduce LD-driven inflammation while increasing free-lipid toxicity.
    """
    F = params["F0"]
    D = params["D0"]
    I = params["I0"]
    activity = acsl_activity
    for _ in range(int(tmax / dt)):
        esterification = params["k_ester"] * activity * F
        alt_clear = params["k_alt_clear"] * F
        lipolysis = params["k_lipolysis"] * D
        export = params["k_export"] * D
        debris = params["debris_input"]
        dF = debris - esterification - alt_clear + lipolysis
        dD = esterification - lipolysis - export
        inflammatory_drive = params["ifn_tone"] + params["k_ld_inflam"] * D + params["k_free_inflam"] * F
        dI = inflammatory_drive - params["k_resolution"] * I
        F = max(0.0, F + dt * dF)
        D = max(0.0, D + dt * dD)
        I = max(0.0, I + dt * dI)
    debris_clearance_capacity = params["k_alt_clear"] + params["k_ester"] * activity
    injury_index = I + params["w_ld"] * D + params["w_free"] * F
    return {
        "activity": activity,
        "F": F,
        "D": D,
        "I": I,
        "debris_clearance_capacity": debris_clearance_capacity,
        "injury_index": injury_index,
    }


def draw_params(n: int) -> list[dict[str, float]]:
    draws = []
    for _ in range(n):
        draws.append(
            {
                "F0": RNG.uniform(0.2, 1.0),
                "D0": RNG.uniform(0.5, 2.0),
                "I0": RNG.uniform(0.5, 2.0),
                "debris_input": RNG.uniform(0.7, 1.3),
                "k_ester": RNG.uniform(0.6, 1.6),
                "k_alt_clear": RNG.uniform(0.1, 0.6),
                "k_lipolysis": RNG.uniform(0.05, 0.35),
                "k_export": RNG.uniform(0.05, 0.35),
                "ifn_tone": RNG.uniform(0.1, 0.8),
                "k_ld_inflam": RNG.uniform(0.3, 1.8),
                "k_free_inflam": RNG.uniform(0.4, 2.0),
                "k_resolution": RNG.uniform(0.4, 1.1),
                "w_ld": RNG.uniform(0.1, 0.6),
                "w_free": RNG.uniform(0.4, 1.2),
            }
        )
    return draws


def run_ode_sensitivity(n: int = 1000) -> pd.DataFrame:
    activities = [1.0, 0.8, 0.6, 0.4, 0.2]
    rows = []
    for i, params in enumerate(draw_params(n)):
        baseline = simulate_ode(params, 1.0)
        for act in activities:
            res = simulate_ode(params, act)
            injury_reduction = (baseline["injury_index"] - res["injury_index"]) / baseline["injury_index"]
            free_increase = (res["F"] - baseline["F"]) / baseline["F"] if baseline["F"] > 0 else math.nan
            clearance_drop = (baseline["debris_clearance_capacity"] - res["debris_clearance_capacity"]) / baseline["debris_clearance_capacity"]
            safe = (free_increase <= 0.20) and (clearance_drop <= 0.20)
            rows.append(
                {
                    "draw": i,
                    "activity": act,
                    "inhibition_fraction": 1 - act,
                    "injury_reduction_fraction": injury_reduction,
                    "free_lipid_increase_fraction": free_increase,
                    "clearance_capacity_drop_fraction": clearance_drop,
                    "safe_window_rule": safe,
                    **{f"param_{k}": v for k, v in params.items()},
                }
            )
    return pd.DataFrame(rows)


def run_abm(seed: int, activity: float, steps: int = 80, size: int = 34) -> dict[str, float]:
    rng = np.random.default_rng(seed)
    debris = np.zeros((size, size), dtype=float)
    inflam = np.zeros((size, size), dtype=float)
    cx = cy = size // 2
    for i in range(size):
        for j in range(size):
            r = math.sqrt((i - cx) ** 2 + (j - cy) ** 2)
            if 5 <= r <= 8:
                debris[i, j] = rng.uniform(0.6, 1.0)
                inflam[i, j] = rng.uniform(0.3, 0.8)
    for _ in range(steps):
        neigh = (
            np.roll(inflam, 1, 0)
            + np.roll(inflam, -1, 0)
            + np.roll(inflam, 1, 1)
            + np.roll(inflam, -1, 1)
        ) / 4
        new_damage_prob = 1 / (1 + np.exp(-4 * (neigh - 0.55)))
        new_damage = rng.binomial(1, np.clip(new_damage_prob * 0.10, 0, 0.3))
        debris += new_damage * rng.uniform(0.2, 0.5, size=(size, size))
        clearance = (0.05 + 0.18 * activity) * debris
        stored_ld_signal = activity * debris
        free_lipid_signal = (1 - activity) * debris
        inflam = (
            0.86 * inflam
            + 0.06 * stored_ld_signal
            + 0.10 * free_lipid_signal
            + 0.02 * neigh
            + rng.normal(0, 0.005, size=(size, size))
        )
        inflam = np.clip(inflam, 0, None)
        debris = np.clip(debris - clearance, 0, None)
    active_area = ((debris > 0.25) | (inflam > 0.45)).sum()
    high_inflam_area = (inflam > 0.75).sum()
    total_debris = debris.sum()
    total_inflam = inflam.sum()
    return {
        "seed": seed,
        "activity": activity,
        "inhibition_fraction": 1 - activity,
        "active_area_cells": float(active_area),
        "high_inflam_area_cells": float(high_inflam_area),
        "total_debris": float(total_debris),
        "total_inflammation": float(total_inflam),
    }


def trial_power(effect: float, n_per_arm: int, responder_fraction: float, attrition: float, n_trials: int = 4000) -> dict[str, float]:
    significant = 0
    observed_effects = []
    for _ in range(n_trials):
        n_t = RNG.binomial(n_per_arm, 1 - attrition)
        n_c = RNG.binomial(n_per_arm, 1 - attrition)
        responder = RNG.binomial(1, responder_fraction, size=n_t)
        tx = RNG.normal(-effect * responder, 1.0, size=n_t)
        ctrl = RNG.normal(0.0, 1.0, size=n_c)
        p = stats.ttest_ind(tx, ctrl, equal_var=False).pvalue
        significant += p < 0.05
        pooled = math.sqrt(((n_t - 1) * tx.var(ddof=1) + (n_c - 1) * ctrl.var(ddof=1)) / (n_t + n_c - 2))
        observed_effects.append((ctrl.mean() - tx.mean()) / pooled if pooled > 0 else math.nan)
    return {
        "n_per_arm": n_per_arm,
        "true_responder_effect_sd": effect,
        "responder_fraction": responder_fraction,
        "attrition": attrition,
        "power_alpha_0_05": significant / n_trials,
        "median_observed_d": float(np.nanmedian(observed_effects)),
        "p10_observed_d": float(np.nanpercentile(observed_effects, 10)),
        "p90_observed_d": float(np.nanpercentile(observed_effects, 90)),
        "n_trials": n_trials,
    }


def main() -> None:
    OUT.mkdir(exist_ok=True)
    ode = run_ode_sensitivity()
    ode.to_csv(OUT / "acsl1_ode_sensitivity.tsv", sep="\t", index=False)

    candidate = ode[(ode["activity"] < 1.0)].copy()
    summary_by_activity = (
        candidate.groupby("activity")
        .agg(
            median_injury_reduction=("injury_reduction_fraction", "median"),
            p25_injury_reduction=("injury_reduction_fraction", lambda x: float(np.percentile(x, 25))),
            p75_injury_reduction=("injury_reduction_fraction", lambda x: float(np.percentile(x, 75))),
            safe_fraction=("safe_window_rule", "mean"),
            median_free_lipid_increase=("free_lipid_increase_fraction", "median"),
            median_clearance_drop=("clearance_capacity_drop_fraction", "median"),
        )
        .reset_index()
    )
    summary_by_activity.to_csv(OUT / "acsl1_ode_summary_by_activity.tsv", sep="\t", index=False)
    therapeutic = candidate[(candidate["injury_reduction_fraction"] >= 0.20) & candidate["safe_window_rule"]]
    ode_summary = {
        "random_seed": SEED,
        "draws": int(ode["draw"].nunique()),
        "activities_tested": sorted(ode["activity"].unique().tolist()),
        "therapeutic_window_rule": ">=20% injury reduction with <=20% free-lipid increase and <=20% debris-clearance capacity drop",
        "draw_fraction_with_any_safe_therapeutic_window": float(therapeutic["draw"].nunique() / ode["draw"].nunique()),
        "best_activity_by_median_injury_reduction": float(summary_by_activity.sort_values("median_injury_reduction", ascending=False)["activity"].iloc[0]),
        "interpretation": "If the safe-window fraction is low, ACSL1 inhibition requires careful cell-state/modality control and cannot be treated as generally safe.",
    }
    (OUT / "acsl1_ode_summary.json").write_text(json.dumps(ode_summary, indent=2) + "\n")

    abm_rows = []
    for activity in [1.0, 0.8, 0.6, 0.4, 0.2]:
        for seed in range(SEED, SEED + 120):
            abm_rows.append(run_abm(seed, activity))
    abm = pd.DataFrame(abm_rows)
    abm.to_csv(OUT / "acsl1_abm_runs.tsv", sep="\t", index=False)
    abm_summary = abm.groupby("activity").agg(
        active_area_median=("active_area_cells", "median"),
        active_area_p25=("active_area_cells", lambda x: float(np.percentile(x, 25))),
        active_area_p75=("active_area_cells", lambda x: float(np.percentile(x, 75))),
        high_inflam_area_median=("high_inflam_area_cells", "median"),
        total_debris_median=("total_debris", "median"),
        total_inflammation_median=("total_inflammation", "median"),
    )
    baseline_area = abm_summary.loc[1.0, "active_area_median"]
    baseline_inflam = abm_summary.loc[1.0, "total_inflammation_median"]
    abm_summary["active_area_reduction_vs_baseline"] = (baseline_area - abm_summary["active_area_median"]) / baseline_area
    abm_summary["inflammation_reduction_vs_baseline"] = (baseline_inflam - abm_summary["total_inflammation_median"]) / baseline_inflam
    abm_summary.reset_index().to_csv(OUT / "acsl1_abm_summary.tsv", sep="\t", index=False)

    trial_rows = []
    for effect in [0.35, 0.5, 0.65]:
        for responder_fraction in [0.35, 0.50, 0.65]:
            for n in [40, 80, 120, 160]:
                trial_rows.append(trial_power(effect, n, responder_fraction, attrition=0.15))
    trial = pd.DataFrame(trial_rows)
    trial.to_csv(OUT / "acsl1_trial_feasibility_simulation.tsv", sep="\t", index=False)

    print(json.dumps(ode_summary, indent=2))
    print(summary_by_activity.to_string(index=False))
    print(abm_summary.reset_index().to_string(index=False))
    print(trial[(trial["true_responder_effect_sd"] == 0.5) & (trial["responder_fraction"] == 0.5)].to_string(index=False))


if __name__ == "__main__":
    main()
