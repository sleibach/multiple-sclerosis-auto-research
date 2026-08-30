#!/usr/bin/env python3
"""Ground model-proposed donor-stability and negative-control safeguards."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
SEEDS = [20260901, 20260902, 20260903]
N_CANDIDATES = 12
N_LODO_SCREENS = 800
N_CONTROL_SCREENS = 5000
GAIN_MIN = 0.10
CORR_MIN = 0.50


def fit_effects(x2_train: np.ndarray, y3_train: np.ndarray, batch_train: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    design = np.column_stack([np.ones(x2_train.size), x2_train.ravel(), batch_train.ravel()])
    xtx = np.einsum("ni,nj->ij", design, design)
    xty = np.einsum("ni,n->i", design, y3_train.ravel())
    coef = np.linalg.solve(xtx, xty)
    pred = coef[0] + coef[1] * x2_train.ravel() + coef[2] * batch_train.ravel()
    residual = (y3_train.ravel() - pred).reshape(x2_train.shape)
    return coef, residual.mean(axis=0)


def heldout_metrics(
    coef: np.ndarray,
    gamma: np.ndarray,
    x2_test: np.ndarray,
    y3_test: np.ndarray,
    batch_test: np.ndarray,
) -> tuple[float, float]:
    pred = coef[0] + coef[1] * x2_test.ravel() + coef[2] * batch_test.ravel()
    residual = (y3_test.ravel() - pred).reshape(x2_test.shape)
    base_sse = float(np.sum(residual**2))
    full_sse = float(np.sum((residual - gamma[None, :]) ** 2))
    gain = 1.0 - full_sse / base_sse
    test_gamma = residual.mean(axis=0)
    correlation = 0.0 if min(np.std(gamma), np.std(test_gamma)) < 1e-12 else float(np.corrcoef(gamma, test_gamma)[0, 1])
    return gain, correlation


def balanced_batch(rng: np.random.Generator, n: int) -> np.ndarray:
    batch = np.empty((n, N_CANDIDATES), dtype=int)
    for candidate in range(N_CANDIDATES):
        assignment = np.tile([0, 1], int(np.ceil(n / 2)))[:n]
        rng.shuffle(assignment)
        batch[:, candidate] = assignment
    return batch


def simulate_panel(
    rng: np.random.Generator,
    n_train: int,
    n_test: int,
    leverage: bool,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    candidate = rng.normal(0.0, 0.55, N_CANDIDATES)
    gamma = np.zeros(N_CANDIDATES) if leverage else 1.15 * np.array([1.0, -0.9, 0.75, -0.7] + [0.0] * 8)
    donor_train = rng.normal(0.0, 0.45, (n_train, 1))
    donor_test = rng.normal(0.0, 0.45, (n_test, 1))
    x_train = candidate[None, :] + 0.35 * donor_train + rng.normal(0.0, 0.62, (n_train, N_CANDIDATES))
    x_test = candidate[None, :] + 0.35 * donor_test + rng.normal(0.0, 0.62, (n_test, N_CANDIDATES))
    b_train = balanced_batch(rng, n_train)
    b_test = balanced_batch(rng, n_test)
    y_train = 0.75 * x_train + gamma[None, :] + 0.25 * donor_train + 0.95 * b_train + rng.normal(0.0, 0.70, x_train.shape)
    y_test = 0.75 * x_test + gamma[None, :] + 0.25 * donor_test + 0.95 * b_test + rng.normal(0.0, 0.70, x_test.shape)
    if leverage:
        pattern = 3.2 * np.array([1.0, -1.0, 0.8, -0.8, 0.6, -0.6] + [0.0] * 6)
        y_train[0] += pattern
        y_test[0] += pattern
    return x_train, y_train, b_train, x_test, y_test, b_test


def lodo_pass(data: tuple[np.ndarray, ...]) -> tuple[bool, bool, float, float]:
    x_train, y_train, b_train, x_test, y_test, b_test = data
    coef, gamma = fit_effects(x_train, y_train, b_train)
    gain, corr = heldout_metrics(coef, gamma, x_test, y_test, b_test)
    parent = gain >= GAIN_MIN and corr >= CORR_MIN
    gains = [gain]
    corrs = [corr]
    for donor in range(x_train.shape[0]):
        keep = np.arange(x_train.shape[0]) != donor
        coef_i, gamma_i = fit_effects(x_train[keep], y_train[keep], b_train[keep])
        gain_i, corr_i = heldout_metrics(coef_i, gamma_i, x_test, y_test, b_test)
        gains.append(gain_i)
        corrs.append(corr_i)
    for donor in range(x_test.shape[0]):
        keep = np.arange(x_test.shape[0]) != donor
        gain_i, corr_i = heldout_metrics(coef, gamma, x_test[keep], y_test[keep], b_test[keep])
        gains.append(gain_i)
        corrs.append(corr_i)
    robust = parent and min(gains) >= GAIN_MIN and min(corrs) >= CORR_MIN
    return parent, robust, float(min(gains)), float(min(corrs))


def control_stop(rng: np.random.Generator, scenario: str, n_train: int = 12, n_test: int = 8) -> bool:
    train = rng.normal(0.0, 0.75, (n_train, 4))
    test = rng.normal(0.0, 0.75, (n_test, 4))
    if scenario == "common_hidden_drift":
        train += 0.75
        test += 0.75
    elif scenario == "control_specific_artifact":
        train[:, 0] += 1.15
        test[:, 0] += 1.15
    for panel in (train, test):
        means = panel.mean(axis=0)
        ses = panel.std(axis=0, ddof=1) / np.sqrt(panel.shape[0])
        if np.any(np.abs(means / ses) >= 2.50):
            return True
    return False


def run(outdir: Path) -> int:
    outdir.mkdir(parents=True, exist_ok=True)
    lodo_rows = []
    for n_train, n_test in [(12, 8), (16, 12)]:
        for scenario, leverage in [("complementary", False), ("paired_high_leverage", True)]:
            for seed in SEEDS:
                rng = np.random.default_rng(seed)
                values = [lodo_pass(simulate_panel(rng, n_train, n_test, leverage)) for _ in range(N_LODO_SCREENS)]
                frame = pd.DataFrame(values, columns=["parent", "robust", "min_gain", "min_corr"])
                lodo_rows.append(
                    {
                        "n_train": n_train,
                        "n_test": n_test,
                        "scenario": scenario,
                        "seed": seed,
                        "n_screens": N_LODO_SCREENS,
                        "parent_pass_probability": float(frame["parent"].mean()),
                        "lodo_pass_probability": float(frame["robust"].mean()),
                        "median_min_gain": float(frame["min_gain"].median()),
                        "median_min_correlation": float(frame["min_corr"].median()),
                    }
                )
    lodo = pd.DataFrame(lodo_rows)
    lodo.to_csv(outdir / "leave_one_donor_results.tsv", sep="\t", index=False)

    control_rows = []
    for scenario in ["clean", "common_hidden_drift", "control_specific_artifact"]:
        for seed in SEEDS:
            rng = np.random.default_rng(seed)
            probability = np.mean([control_stop(rng, scenario) for _ in range(N_CONTROL_SCREENS)])
            control_rows.append({"scenario": scenario, "seed": seed, "n_screens": N_CONTROL_SCREENS, "stop_probability": float(probability)})
    controls = pd.DataFrame(control_rows)
    controls.to_csv(outdir / "negative_control_results.tsv", sep="\t", index=False)

    lodo16 = lodo[(lodo.n_train == 16) & (lodo.n_test == 12)]
    checks = [
        ("lodo_complementary_power_16_12", bool(lodo16[lodo16.scenario == "complementary"].lodo_pass_probability.ge(0.80).all())),
        ("lodo_leverage_false_pass_16_12", bool(lodo16[lodo16.scenario == "paired_high_leverage"].lodo_pass_probability.le(0.05).all())),
        ("negative_control_clean_fwer", bool(controls[controls.scenario == "clean"].stop_probability.le(0.05).all())),
        ("negative_control_common_drift_power", bool(controls[controls.scenario == "common_hidden_drift"].stop_probability.ge(0.80).all())),
        ("negative_control_specific_artifact_power", bool(controls[controls.scenario == "control_specific_artifact"].stop_probability.ge(0.80).all())),
    ]
    pd.DataFrame([{"check": name, "status": "PASS" if passed else "FAIL"} for name, passed in checks]).to_csv(
        outdir / "adversarial_extension_checks.tsv", sep="\t", index=False
    )
    summary = {
        "synthetic": True,
        "purpose": "model-proposed multifidelity safeguard grounding; no biological claim",
        "model_proposals_are_evidence": False,
        "lodo_screens": 2 * 2 * len(SEEDS) * N_LODO_SCREENS,
        "negative_control_screens": 3 * len(SEEDS) * N_CONTROL_SCREENS,
        "n_checks": len(checks),
        "n_fail": sum(not passed for _, passed in checks),
        "overall_status": "PASS" if all(passed for _, passed in checks) else "FAIL",
    }
    (outdir / "adversarial_extension_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["overall_status"] == "PASS" else 2


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=ROOT / "analysis/v57_multifidelity_adversarial_extension")
    args = parser.parse_args()
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    return run(outdir)


if __name__ == "__main__":
    raise SystemExit(main())
