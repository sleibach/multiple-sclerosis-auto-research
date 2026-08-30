#!/usr/bin/env python3
"""Synthetic verification of a 2D-to-3D model-complexity escalation gate."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
SEEDS = [20260831, 20260832, 20260833]
N_SCREENS = 500
N_CANDIDATES = 12
N_PERMUTATIONS = 199
GAIN_MIN = 0.10
CORRELATION_MIN = 0.50
P_MAX = 0.05
BATCH_IMBALANCE_MAX = 0.25
SAFETY_MARGIN = 0.20


@dataclass(frozen=True)
class Scenario:
    name: str
    n_train: int
    n_test: int
    gamma_scale: float
    harm: bool = False
    confounded_batch: bool = False
    underpowered: bool = False


SCENARIOS = [
    Scenario("redundant_3d", 12, 8, 0.0),
    Scenario("complementary_3d", 12, 8, 1.15),
    Scenario("hidden_3d_harm", 12, 8, 0.0, harm=True),
    Scenario("response_correlated_3d_batch", 12, 8, 0.0, confounded_batch=True),
    Scenario("small_calibration_panel", 6, 4, 1.15, underpowered=True),
]


def linear_predict(x: np.ndarray, coef: np.ndarray) -> np.ndarray:
    return x[:, 0] * coef[0] + x[:, 1] * coef[1] + x[:, 2] * coef[2]


def ols_predict(train_x: np.ndarray, train_y: np.ndarray, test_x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    # Explicit three-column normal equations avoid platform-specific batched
    # matmul warnings observed from the local Accelerate-backed lstsq path.
    xtx = np.einsum("ni,nj->ij", train_x, train_x)
    xty = np.einsum("ni,n->i", train_x, train_y)
    coef = np.linalg.solve(xtx, xty)
    prediction = linear_predict(test_x, coef)
    if not np.isfinite(coef).all() or not np.isfinite(prediction).all():
        raise FloatingPointError("non-finite base-model coefficient or prediction")
    return prediction, coef


def candidate_means(values: np.ndarray) -> np.ndarray:
    return values.mean(axis=0)


def safe_corr(x: np.ndarray, y: np.ndarray) -> float:
    if np.std(x) < 1e-12 or np.std(y) < 1e-12:
        return 0.0
    return float(np.corrcoef(x, y)[0, 1])


def batch_imbalance(batch: np.ndarray) -> float:
    proportions = batch.mean(axis=0)
    return float(np.max(np.abs(proportions - 0.5)))


def safety_reversal(x2_train: np.ndarray, x2_test: np.ndarray, y3_train: np.ndarray, y3_test: np.ndarray) -> bool:
    x_train = candidate_means(x2_train)
    x_test = candidate_means(x2_test)
    y_train = candidate_means(y3_train)
    y_test = candidate_means(y3_test)
    se_x_train = x2_train.std(axis=0, ddof=1) / np.sqrt(x2_train.shape[0])
    se_x_test = x2_test.std(axis=0, ddof=1) / np.sqrt(x2_test.shape[0])
    se_y_train = y3_train.std(axis=0, ddof=1) / np.sqrt(y3_train.shape[0])
    se_y_test = y3_test.std(axis=0, ddof=1) / np.sqrt(y3_test.shape[0])
    z = 2.64  # Bonferroni-normal approximation for 12 predeclared candidates.
    favorable_2d = (x_train - z * se_x_train > SAFETY_MARGIN) & (x_test - z * se_x_test > SAFETY_MARGIN)
    harmful_3d = (y_train + z * se_y_train < -SAFETY_MARGIN) & (y_test + z * se_y_test < -SAFETY_MARGIN)
    return bool(np.any(favorable_2d & harmful_3d))


def one_screen(rng: np.random.Generator, scenario: Scenario) -> dict[str, object]:
    n_total = scenario.n_train + scenario.n_test
    candidate_effect = rng.normal(0.0, 0.55, N_CANDIDATES)
    gamma = np.zeros(N_CANDIDATES)
    if scenario.gamma_scale:
        gamma[:4] = scenario.gamma_scale * np.array([1.0, -0.9, 0.75, -0.7])
    if scenario.harm:
        candidate_effect[0] = 1.10
        gamma[0] = -2.25

    donor = rng.normal(0.0, 0.45, (n_total, 1))
    x2 = candidate_effect[None, :] + 0.35 * donor + rng.normal(0.0, 0.62, (n_total, N_CANDIDATES))
    if scenario.confounded_batch:
        probabilities = np.full(N_CANDIDATES, 0.5)
        probabilities[:3] = 0.92
        probabilities[3:6] = 0.08
        batch = rng.binomial(1, probabilities[None, :], size=(n_total, N_CANDIDATES))
    else:
        # Exact balance is required separately in the frozen train/test panels.
        batch = np.empty((n_total, N_CANDIDATES), dtype=int)
        for candidate in range(N_CANDIDATES):
            train_assignment = np.tile([0, 1], int(np.ceil(scenario.n_train / 2)))[: scenario.n_train]
            test_assignment = np.tile([0, 1], int(np.ceil(scenario.n_test / 2)))[: scenario.n_test]
            rng.shuffle(train_assignment)
            rng.shuffle(test_assignment)
            batch[:, candidate] = np.concatenate([train_assignment, test_assignment])
    y3 = (
        0.75 * x2
        + gamma[None, :]
        + 0.25 * donor
        + 0.95 * batch
        + rng.normal(0.0, 0.70, (n_total, N_CANDIDATES))
    )

    split = scenario.n_train
    x2_train, x2_test = x2[:split], x2[split:]
    y3_train, y3_test = y3[:split], y3[split:]
    batch_train, batch_test = batch[:split], batch[split:]

    train_design = np.column_stack([np.ones(x2_train.size), x2_train.ravel(), batch_train.ravel()])
    test_design = np.column_stack([np.ones(x2_test.size), x2_test.ravel(), batch_test.ravel()])
    pred_test, coef = ols_predict(train_design, y3_train.ravel(), test_design)
    base_test_residual = (y3_test.ravel() - pred_test).reshape(scenario.n_test, N_CANDIDATES)
    pred_train = linear_predict(train_design, coef)
    if not np.isfinite(pred_train).all():
        raise FloatingPointError("non-finite training prediction")
    base_train_residual = (y3_train.ravel() - pred_train).reshape(scenario.n_train, N_CANDIDATES)
    gamma_train = candidate_means(base_train_residual)
    gamma_test = candidate_means(base_test_residual)

    base_sse = float(np.sum(base_test_residual**2))
    full_sse = float(np.sum((base_test_residual - gamma_train[None, :]) ** 2))
    gain = 1.0 - full_sse / base_sse if base_sse > 0 else 0.0
    correlation = safe_corr(gamma_train, gamma_test)

    perm_gains = []
    for _ in range(N_PERMUTATIONS):
        permuted = rng.permutation(gamma_train)
        perm_sse = float(np.sum((base_test_residual - permuted[None, :]) ** 2))
        perm_gains.append(1.0 - perm_sse / base_sse if base_sse > 0 else 0.0)
    permutation_p = (1 + int(np.sum(np.asarray(perm_gains) >= gain))) / (N_PERMUTATIONS + 1)

    imbalance = max(batch_imbalance(batch_train), batch_imbalance(batch_test))
    batch_ok = imbalance <= BATCH_IMBALANCE_MAX
    incremental = bool(batch_ok and gain >= GAIN_MIN and correlation >= CORRELATION_MIN and permutation_p <= P_MAX)
    safety = bool(batch_ok and safety_reversal(x2_train, x2_test, y3_train, y3_test))

    if scenario.underpowered:
        decision = "ABSTAIN_UNDERPOWERED"
    elif not batch_ok:
        decision = "ABSTAIN_BATCH_CONFOUNDED"
    elif safety:
        decision = "SCALE_3D_SAFETY"
    elif incremental:
        decision = "SCALE_3D_INCREMENTAL"
    else:
        decision = "STOP_AT_2D_REDUNDANT"
    return {
        "gain": gain,
        "correlation": correlation,
        "permutation_p": permutation_p,
        "batch_imbalance": imbalance,
        "incremental": incremental,
        "safety": safety,
        "decision": decision,
    }


def run(outdir: Path) -> int:
    outdir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, object]] = []
    for scenario in SCENARIOS:
        for seed in SEEDS:
            rng = np.random.default_rng(seed)
            screens = [one_screen(rng, scenario) for _ in range(N_SCREENS)]
            frame = pd.DataFrame(screens)
            scale = frame["decision"].astype(str).str.startswith("SCALE_3D")
            rows.append(
                {
                    "scenario": scenario.name,
                    "seed": seed,
                    "n_screens": N_SCREENS,
                    "n_train_donor_pairs": scenario.n_train,
                    "n_test_donor_pairs": scenario.n_test,
                    "scale_probability": float(scale.mean()),
                    "incremental_scale_probability": float((frame["decision"] == "SCALE_3D_INCREMENTAL").mean()),
                    "safety_scale_probability": float((frame["decision"] == "SCALE_3D_SAFETY").mean()),
                    "batch_abstention_probability": float((frame["decision"] == "ABSTAIN_BATCH_CONFOUNDED").mean()),
                    "underpowered_abstention_probability": float((frame["decision"] == "ABSTAIN_UNDERPOWERED").mean()),
                    "median_heldout_rmse_gain": float(frame["gain"].median()),
                    "median_residual_correlation": float(frame["correlation"].median()),
                    "median_permutation_p": float(frame["permutation_p"].median()),
                }
            )
    result = pd.DataFrame(rows)
    result.to_csv(outdir / "multifidelity_escalation_results.tsv", sep="\t", index=False)

    grouped = result.groupby("scenario", sort=False).mean(numeric_only=True)
    checks = [
        ("redundant_false_scale", grouped.loc["redundant_3d", "scale_probability"] <= 0.05),
        ("complementary_incremental_power", grouped.loc["complementary_3d", "incremental_scale_probability"] >= 0.80),
        ("hidden_harm_safety_power", grouped.loc["hidden_3d_harm", "safety_scale_probability"] >= 0.80),
        ("batch_false_scale", grouped.loc["response_correlated_3d_batch", "scale_probability"] <= 0.05),
        ("batch_abstention", grouped.loc["response_correlated_3d_batch", "batch_abstention_probability"] >= 0.80),
        ("small_panel_scale", grouped.loc["small_calibration_panel", "scale_probability"] <= 0.20),
        ("small_panel_abstention", grouped.loc["small_calibration_panel", "underpowered_abstention_probability"] >= 0.80),
    ]
    check_rows = [{"check": name, "status": "PASS" if passed else "FAIL"} for name, passed in checks]
    pd.DataFrame(check_rows).to_csv(outdir / "multifidelity_escalation_checks.tsv", sep="\t", index=False)
    summary = {
        "synthetic": True,
        "purpose": "2D-to-3D model-complexity escalation method verification; no biological claim",
        "n_screens": len(SCENARIOS) * len(SEEDS) * N_SCREENS,
        "n_candidate_evaluations": len(SCENARIOS) * len(SEEDS) * N_SCREENS * N_CANDIDATES,
        "n_permuted_assignments": len(SCENARIOS) * len(SEEDS) * N_SCREENS * N_PERMUTATIONS,
        "n_checks": len(checks),
        "n_fail": sum(not passed for _, passed in checks),
        "overall_status": "PASS" if all(passed for _, passed in checks) else "FAIL",
        "scenario_means": grouped.to_dict(orient="index"),
    }
    (outdir / "multifidelity_escalation_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["overall_status"] == "PASS" else 2


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=ROOT / "analysis/v57_multifidelity_escalation")
    args = parser.parse_args()
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    return run(outdir)


if __name__ == "__main__":
    raise SystemExit(main())
