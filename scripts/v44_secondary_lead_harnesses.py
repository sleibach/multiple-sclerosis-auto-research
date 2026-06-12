#!/usr/bin/env python3
"""Synthetic harness checks for V44 secondary live-lead pre-registrations.

This script validates mechanics only for two future-data validation plans:

1. postpartum HLA-II/CD64 APC-arm imbalance;
2. T/B-readable treatment-response monitoring state.

All generated data are synthetic and are not biological evidence.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd


SEED = 44044
OUT = Path("analysis/v44_secondary_lead_harnesses")


def auc_score(y: np.ndarray, score: np.ndarray) -> float:
    y = np.asarray(y, dtype=int)
    score = np.asarray(score, dtype=float)
    ok = np.isfinite(score)
    y = y[ok]
    score = score[ok]
    pos = score[y == 1]
    neg = score[y == 0]
    if len(pos) == 0 or len(neg) == 0:
        return math.nan
    ranks = pd.Series(score).rank(method="average").to_numpy()
    n1 = int(y.sum())
    n0 = int(len(y) - n1)
    return float((ranks[y == 1].sum() - n1 * (n1 + 1) / 2.0) / (n1 * n0))


def hedges_g(y: np.ndarray, score: np.ndarray) -> float:
    y = np.asarray(y, dtype=int)
    score = np.asarray(score, dtype=float)
    ok = np.isfinite(score)
    y = y[ok]
    score = score[ok]
    a = score[y == 1]
    b = score[y == 0]
    if len(a) < 2 or len(b) < 2:
        return math.nan
    pooled = math.sqrt(
        ((len(a) - 1) * np.var(a, ddof=1) + (len(b) - 1) * np.var(b, ddof=1))
        / (len(a) + len(b) - 2)
    )
    if pooled == 0:
        return 0.0
    correction = 1 - 3 / (4 * (len(a) + len(b)) - 9)
    return float(((np.mean(a) - np.mean(b)) / pooled) * correction)


def ci_auc(y: np.ndarray, score: np.ndarray, rng: np.random.Generator, n_boot: int = 500) -> tuple[float, float]:
    idx = np.arange(len(y))
    aucs = []
    for _ in range(n_boot):
        take = rng.choice(idx, len(idx), replace=True)
        if len(np.unique(y[take])) < 2:
            continue
        aucs.append(auc_score(y[take], score[take]))
    if not aucs:
        return math.nan, math.nan
    return float(np.percentile(aucs, 2.5)), float(np.percentile(aucs, 97.5))


def residualize(values: np.ndarray, covariates: pd.DataFrame) -> np.ndarray:
    x = covariates.replace([np.inf, -np.inf], np.nan).fillna(0.0)
    design = np.column_stack([np.ones(len(x)), x.to_numpy(float)])
    beta = np.linalg.lstsq(design, values, rcond=None)[0]
    return values - design @ beta


def postpartum_synthetic(mode: str, outdir: Path) -> dict[str, object]:
    rng = np.random.default_rng(SEED + (1 if mode == "planted" else 0))
    n = 60
    y = np.array([1] * 30 + [0] * 30)
    rng.shuffle(y)
    baseline_arm = rng.normal(0.0, 0.8, n)
    healthy_rebound = rng.normal(0.6, 0.35, n)
    if mode == "planted":
        rebound = healthy_rebound - 1.2 * y + rng.normal(0.0, 0.25, n)
    else:
        rebound = healthy_rebound + rng.normal(0.0, 0.25, n)
    steroid = rng.normal(0.0, 1.0, n) + 0.25 * y
    dmt_restart = (rng.random(n) < (0.35 + 0.10 * (1 - y))).astype(int)
    hla_late = baseline_arm + rng.normal(0.0, 0.3, n)
    cd64_late = rng.normal(0.3, 0.4, n)
    arm_late = hla_late - cd64_late
    arm_6w = arm_late + rebound
    risk_score = -(arm_6w - arm_late)
    residual = residualize(risk_score, pd.DataFrame({"steroid": steroid, "dmt_restart": dmt_restart}))
    if auc_score(y, residual) < 0.5:
        residual = -residual
    ci_low, ci_high = ci_auc(y, risk_score, rng)
    result = {
        "mode": mode,
        "synthetic": True,
        "n": n,
        "n_relapse": int(y.sum()),
        "primary_auc": auc_score(y, risk_score),
        "primary_hedges_g": hedges_g(y, risk_score),
        "auc_ci_low": ci_low,
        "auc_ci_high": ci_high,
        "residual_auc_steroid_dmt": auc_score(y, residual),
        "pass": bool(auc_score(y, risk_score) >= 0.70 and hedges_g(y, risk_score) >= 0.50 and auc_score(y, residual) >= 0.65),
    }
    frame = pd.DataFrame(
        {
            "synthetic": True,
            "subject": [f"P{i:03d}" for i in range(n)],
            "postpartum_relapse_3m": y,
            "late_pregnancy_hla_minus_cd64": arm_late,
            "postpartum_6w_hla_minus_cd64": arm_6w,
            "apc_arm_rebound": arm_6w - arm_late,
            "risk_score_lack_of_rebound": risk_score,
            "steroid_exposure": steroid,
            "dmt_restart": dmt_restart,
        }
    )
    outdir.mkdir(parents=True, exist_ok=True)
    frame.to_csv(outdir / f"postpartum_{mode}_synthetic.tsv", sep="\t", index=False)
    return result


def tb_synthetic(mode: str, outdir: Path) -> dict[str, object]:
    rng = np.random.default_rng(SEED + (11 if mode == "planted" else 10))
    n = 60
    y = np.array([1] * 30 + [0] * 30)
    rng.shuffle(y)
    composition_shift = rng.normal(0.0, 1.0, n)
    if mode == "planted":
        b_locked = 1.1 * y + 0.25 * composition_shift + rng.normal(0.0, 0.8, n)
        t_locked = 0.75 * y + 0.45 * composition_shift + rng.normal(0.0, 0.9, n)
    else:
        b_locked = 0.25 * composition_shift + rng.normal(0.0, 1.0, n)
        t_locked = 0.45 * composition_shift + rng.normal(0.0, 1.0, n)
    b_resid = residualize(b_locked, pd.DataFrame({"composition_shift": composition_shift}))
    t_resid = residualize(t_locked, pd.DataFrame({"composition_shift": composition_shift}))
    if auc_score(y, b_resid) < 0.5:
        b_resid = -b_resid
    if auc_score(y, t_resid) < 0.5:
        t_resid = -t_resid
    b_auc = auc_score(y, b_locked)
    t_auc = auc_score(y, t_locked)
    b_ci_low, b_ci_high = ci_auc(y, b_locked, rng)
    result = {
        "mode": mode,
        "synthetic": True,
        "n": n,
        "n_responders": int(y.sum()),
        "b_plasma_auc": b_auc,
        "b_plasma_hedges_g": hedges_g(y, b_locked),
        "b_plasma_auc_ci_low": b_ci_low,
        "b_plasma_auc_ci_high": b_ci_high,
        "t_cell_auc": t_auc,
        "t_cell_hedges_g": hedges_g(y, t_locked),
        "b_plasma_residual_auc": auc_score(y, b_resid),
        "t_cell_residual_auc": auc_score(y, t_resid),
        "pass": bool(
            b_auc >= 0.70
            and hedges_g(y, b_locked) >= 0.50
            and t_auc >= 0.60
            and auc_score(y, b_resid) >= 0.65
        ),
    }
    frame = pd.DataFrame(
        {
            "synthetic": True,
            "subject": [f"T{i:03d}" for i in range(n)],
            "responder": y,
            "b_plasma_locked_delta": b_locked,
            "t_cell_locked_delta": t_locked,
            "composition_shift": composition_shift,
        }
    )
    outdir.mkdir(parents=True, exist_ok=True)
    frame.to_csv(outdir / f"tb_{mode}_synthetic.tsv", sep="\t", index=False)
    return result


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    results = {
        "postpartum_null": postpartum_synthetic("null", OUT / "synthetic"),
        "postpartum_planted": postpartum_synthetic("planted", OUT / "synthetic"),
        "tb_null": tb_synthetic("null", OUT / "synthetic"),
        "tb_planted": tb_synthetic("planted", OUT / "synthetic"),
    }
    checks = {
        "postpartum_null_expected_fail": not results["postpartum_null"]["pass"],
        "postpartum_planted_expected_pass": results["postpartum_planted"]["pass"],
        "tb_null_expected_fail": not results["tb_null"]["pass"],
        "tb_planted_expected_pass": results["tb_planted"]["pass"],
    }
    summary = {"synthetic": True, "seed": SEED, "checks": checks, "results": results}
    (OUT / "secondary_harness_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True))
    rows = []
    for name, result in results.items():
        rows.append({"scenario": name, **result})
    pd.DataFrame(rows).to_csv(OUT / "secondary_harness_metrics.tsv", sep="\t", index=False)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
