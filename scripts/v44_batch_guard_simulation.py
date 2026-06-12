#!/usr/bin/env python3
"""Validate the additive V44 batch guard on V43 synthetic robustness data.

Synthetic data are method-characterization artifacts only. This script does not
read real Gafson data and does not alter the locked V22 rule.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
IN = ROOT / "analysis" / "v43_method_validation" / "synthetic" / "robustness_simulation_subjects.tsv.gz"
OUT = ROOT / "analysis" / "v44_batch_guard"
OUT.mkdir(parents=True, exist_ok=True)


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


def residualize(values: np.ndarray, covariates: pd.DataFrame) -> np.ndarray:
    x = covariates.copy()
    for col in x.columns:
        x[col] = pd.to_numeric(x[col], errors="coerce")
    x = x.replace([np.inf, -np.inf], np.nan).fillna(0.0)
    values = np.asarray(values, dtype=float)
    design = np.column_stack([np.ones(len(x)), x.to_numpy(float)])
    beta = np.linalg.lstsq(design, values, rcond=None)[0]
    return values - design @ beta


def pass_like(n: int, n_resp: int, n_non: int, auc: float, g: float, receptor_auc: float) -> bool:
    if not np.isfinite(auc) or not np.isfinite(g):
        return False
    receptor_bad = np.isfinite(receptor_auc) and receptor_auc - auc >= 0.10
    if n >= 30:
        return auc >= 0.70 and g >= 0.50 and not receptor_bad
    return auc >= 0.70 and g >= 0.50 and not receptor_bad


def evaluate_group(group: pd.DataFrame) -> dict[str, object]:
    y = group["response_observed"].to_numpy(int)
    score = group["locked_score"].to_numpy(float)
    receptor = group["delta_RECEPTOR"].to_numpy(float)
    batch = group["batch"].to_numpy(float)
    auc = auc_score(y, score)
    g = hedges_g(y, score)
    receptor_auc = auc_score(y, receptor)
    batch_auc = auc_score(y, batch)
    if np.isfinite(batch_auc) and batch_auc < 0.5:
        batch_auc = 1.0 - batch_auc
    batch_score_r = float(pd.Series(batch).corr(pd.Series(score), method="spearman"))
    batch_response_delta = abs(float(np.mean(batch[y == 1]) - np.mean(batch[y == 0])))
    resid = residualize(score, pd.DataFrame({"batch": batch}))
    residual_auc = auc_score(y, resid)
    if residual_auc < 0.5:
        resid = -resid
        residual_auc = auc_score(y, resid)
    residual_g = hedges_g(y, resid)
    attenuation = auc - residual_auc
    primary_pass = pass_like(len(group), int(y.sum()), int(len(y) - y.sum()), auc, g, receptor_auc)
    batch_risk = (
        batch_response_delta >= 0.25
        or (np.isfinite(batch_auc) and batch_auc >= 0.60)
        or (np.isfinite(batch_score_r) and abs(batch_score_r) >= 0.35)
        or (np.isfinite(attenuation) and attenuation >= 0.05)
    )
    guarded_acceptable_pass = bool(primary_pass and not batch_risk)
    return {
        "n": int(len(group)),
        "n_responders": int(y.sum()),
        "n_nonresponders": int(len(y) - y.sum()),
        "auc": auc,
        "hedges_g": g,
        "receptor_auc": receptor_auc,
        "batch_auc": batch_auc,
        "batch_score_spearman": batch_score_r,
        "batch_response_delta": batch_response_delta,
        "batch_residualized_auc": residual_auc,
        "batch_residualized_hedges_g": residual_g,
        "auc_attenuation_after_batch": attenuation,
        "primary_pass": primary_pass,
        "batch_risk_flag": batch_risk,
        "guarded_acceptable_pass": guarded_acceptable_pass,
    }


def main() -> int:
    df = pd.read_csv(IN, sep="\t", keep_default_na=False)
    group_cols = ["truth", "pathology", "pathology_severity", "replicate", "seed"]
    rows = []
    for keys, group in df.groupby(group_cols, sort=True):
        record = dict(zip(group_cols, keys))
        record.update(evaluate_group(group))
        rows.append(record)
    metrics = pd.DataFrame(rows)
    metrics.to_csv(OUT / "batch_guard_cohort_metrics.tsv", sep="\t", index=False)
    summary = (
        metrics.groupby(["truth", "pathology", "pathology_severity"], as_index=False)
        .agg(
            cohorts=("primary_pass", "size"),
            primary_pass_rate=("primary_pass", "mean"),
            batch_risk_flag_rate=("batch_risk_flag", "mean"),
            guarded_acceptable_pass_rate=("guarded_acceptable_pass", "mean"),
            mean_auc=("auc", "mean"),
            mean_batch_auc=("batch_auc", "mean"),
            mean_batch_response_delta=("batch_response_delta", "mean"),
            mean_auc_attenuation=("auc_attenuation_after_batch", "mean"),
        )
    )
    summary.to_csv(OUT / "batch_guard_summary.tsv", sep="\t", index=False)
    null = summary[summary["truth"].eq("null")].copy()
    planted = summary[summary["truth"].eq("planted")].copy()
    envelope_rows = []
    for pathology in sorted(summary["pathology"].unique()):
        ok = summary[
            summary["pathology"].eq(pathology)
            & (
                (
                    summary["truth"].eq("null")
                    & summary["guarded_acceptable_pass_rate"].le(0.05)
                )
                | (
                    summary["truth"].eq("planted")
                    & summary["guarded_acceptable_pass_rate"].ge(0.80)
                )
            )
        ]
        severities = []
        for severity in sorted(summary[summary["pathology"].eq(pathology)]["pathology_severity"].unique()):
            nrow = null[(null["pathology"].eq(pathology)) & (null["pathology_severity"].eq(severity))]
            prow = planted[(planted["pathology"].eq(pathology)) & (planted["pathology_severity"].eq(severity))]
            if nrow.empty or prow.empty:
                continue
            if (
                float(nrow["guarded_acceptable_pass_rate"].iloc[0]) <= 0.05
                and float(prow["guarded_acceptable_pass_rate"].iloc[0]) >= 0.80
            ):
                severities.append(float(severity))
        envelope_rows.append(
            {
                "pathology": pathology,
                "largest_severity_inside_guarded_envelope": max(severities) if severities else math.nan,
            }
        )
    envelope = pd.DataFrame(envelope_rows)
    envelope.to_csv(OUT / "batch_guard_envelope.tsv", sep="\t", index=False)
    batch_null = summary[
        summary["truth"].eq("null") & summary["pathology"].eq("batch_response_correlated")
    ]
    before = float(batch_null["primary_pass_rate"].max())
    after = float(batch_null["guarded_acceptable_pass_rate"].max())
    out = {
        "synthetic": True,
        "cohorts": int(len(metrics)),
        "batch_response_null_max_primary_pass_rate": before,
        "batch_response_null_max_guarded_acceptable_pass_rate": after,
        "batch_response_null_absolute_reduction": before - after,
        "output_dir": str(OUT),
    }
    (OUT / "summary.json").write_text(json.dumps(out, indent=2, sort_keys=True))
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
