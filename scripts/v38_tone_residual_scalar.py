#!/usr/bin/env python3
"""Tone-stripped residual test for the bounded V22/V23 scalar.

Proposal source: V38 model-lens pass (Claude). Model output is not evidence.
This script grounds the proposal on the V32 subject-level confounder table.

Question: does the locked scalar's response signal live mostly in broad immune
tone, or in the residual after tone is removed?
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "analysis/v32_confounder_audit/v32_subject_confounder_scores.tsv"
OUTDIR = ROOT / "analysis/v38_tone_residual_scalar"

TONE_FEATURES = [
    "delta_general_inflammatory_tone",
    "delta_stat1_axis",
    "delta_glycolysis",
    "delta_immunometabolism_hif_nampt",
]


def auc_raw(scores: np.ndarray, labels: np.ndarray) -> float:
    pos = scores[labels == 1]
    neg = scores[labels == 0]
    wins = 0.0
    for p in pos:
        wins += np.sum(p > neg)
        wins += 0.5 * np.sum(p == neg)
    return float(wins / (len(pos) * len(neg)))


def oriented_auc(scores: np.ndarray, labels: np.ndarray) -> tuple[float, str]:
    raw = auc_raw(scores, labels)
    if raw >= 0.5:
        return raw, "higher_in_responders"
    return 1.0 - raw, "lower_in_responders"


def exact_p(scores: np.ndarray, labels: np.ndarray) -> float:
    obs, _ = oriented_auc(scores, labels)
    n = len(labels)
    k = int(labels.sum())
    ge = 0
    total = 0
    for pos_idx in itertools.combinations(range(n), k):
        perm = np.zeros(n, dtype=int)
        perm[list(pos_idx)] = 1
        stat, _ = oriented_auc(scores, perm)
        total += 1
        if stat >= obs - 1e-12:
            ge += 1
    return (ge + 1.0) / (total + 1.0)


def zscore(x: np.ndarray) -> np.ndarray:
    mean = np.nanmean(x, axis=0)
    std = np.nanstd(x, axis=0)
    std[std == 0] = 1.0
    return (x - mean) / std


def fit_predict_loocv(X: np.ndarray, y: np.ndarray) -> np.ndarray:
    preds = np.zeros(len(y), dtype=float)
    for i in range(len(y)):
        train = np.ones(len(y), dtype=bool)
        train[i] = False
        X_train = np.column_stack([np.ones(train.sum()), X[train]])
        coef, *_ = np.linalg.lstsq(X_train, y[train], rcond=None)
        X_i = np.r_[1.0, X[i]]
        preds[i] = float(X_i @ coef)
    return preds


def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(INPUT, sep="\t")
    labels = (df["response"] == "Responder").astype(int).to_numpy()
    scalar = df["locked_signed_score"].to_numpy(float)
    X = zscore(df[TONE_FEATURES].to_numpy(float))
    scalar_z = zscore(scalar.reshape(-1, 1)).ravel()

    tone_pred = fit_predict_loocv(X, scalar_z)
    residual = scalar_z - tone_pred

    rows = []
    for feature, values in [
        ("raw_locked_scalar", scalar_z),
        ("loocv_tone_prediction_of_scalar", tone_pred),
        ("tone_residual_scalar", residual),
        ("delta_stat1_axis", df["delta_stat1_axis"].to_numpy(float)),
        ("delta_general_inflammatory_tone", df["delta_general_inflammatory_tone"].to_numpy(float)),
        ("delta_glycolysis", df["delta_glycolysis"].to_numpy(float)),
    ]:
        auc, direction = oriented_auc(values, labels)
        rows.append(
            {
                "feature": feature,
                "auc_oriented": auc,
                "orientation": direction,
                "exact_permutation_p": exact_p(values, labels),
                "responder_median": float(np.median(values[labels == 1])),
                "nonresponder_median": float(np.median(values[labels == 0])),
            }
        )
    result = pd.DataFrame(rows).sort_values("auc_oriented", ascending=False)
    result.to_csv(OUTDIR / "tone_residual_scalar_auc.tsv", sep="\t", index=False)

    # Fitted-in-all-data coefficients are only descriptive; LOOCV predictions
    # above are used for the response comparison.
    X_all = np.column_stack([np.ones(len(scalar_z)), X])
    coef, *_ = np.linalg.lstsq(X_all, scalar_z, rcond=None)
    coef_rows = [{"term": "intercept", "coefficient": float(coef[0])}]
    coef_rows.extend(
        {"term": term, "coefficient": float(value)}
        for term, value in zip(TONE_FEATURES, coef[1:])
    )
    pd.DataFrame(coef_rows).to_csv(OUTDIR / "tone_model_coefficients_descriptive.tsv", sep="\t", index=False)

    summary = {
        "proposal_source": "analysis/v38_model_proposal_pass/claude_remaining_tests.json",
        "input": str(INPUT.relative_to(ROOT)),
        "n_subjects": int(len(df)),
        "n_responders": int(labels.sum()),
        "n_nonresponders": int(len(labels) - labels.sum()),
        "tone_features": TONE_FEATURES,
        "auc_results": result.to_dict(orient="records"),
        "interpretation": (
            "If the LOOCV tone prediction matches the raw scalar and the residual "
            "collapses, the scalar is mostly broad-tone-correlated. If residual "
            "performance persists, broad tone does not fully account for the scalar."
        ),
    }
    with (OUTDIR / "tone_residual_scalar_summary.json").open("w") as handle:
        json.dump(summary, handle, indent=2)


if __name__ == "__main__":
    main()
