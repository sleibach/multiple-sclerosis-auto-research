#!/usr/bin/env python3
"""V38 cross-scale/control-systems reframing of the V22/V23 monitoring data.

This is not a new rule builder. It asks whether the existing bounded
treatment-response table is better described by baseline load, early control
action, treated set-point proximity, or simple negative-feedback features.
All tests are small-n aware and use exact label permutations where feasible.
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path
from functools import lru_cache

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "analysis/v32_confounder_audit/v32_subject_confounder_scores.tsv"
OUTDIR = ROOT / "analysis/v38_control_system"


MODULES = [
    "IFN_APC",
    "HLAII",
    "glycolysis",
    "oxphos",
    "immunometabolism_hif_nampt",
    "glucocorticoid_response",
    "general_inflammatory_tone",
    "ifn_suppression_inverse_isg",
    "stat1_axis",
    "proliferation",
    "monocyte_myeloid_composition",
    "t_cell_composition",
    "b_cell_composition",
]


def auc_raw(scores: np.ndarray, labels: np.ndarray) -> float:
    """Mann-Whitney AUC for higher score predicting label == 1."""
    pos = scores[labels == 1]
    neg = scores[labels == 0]
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    wins = 0.0
    for p in pos:
        wins += np.sum(p > neg)
        wins += 0.5 * np.sum(p == neg)
    return float(wins / (len(pos) * len(neg)))


def average_ranks(values: np.ndarray) -> np.ndarray:
    """1-based average ranks, handling ties without scipy."""
    order = np.argsort(values, kind="mergesort")
    sorted_values = values[order]
    ranks = np.empty(len(values), dtype=float)
    i = 0
    while i < len(values):
        j = i + 1
        while j < len(values) and sorted_values[j] == sorted_values[i]:
            j += 1
        avg_rank = (i + 1 + j) / 2.0
        ranks[order[i:j]] = avg_rank
        i = j
    return ranks


@lru_cache(maxsize=None)
def permutation_label_matrix(n: int, k: int) -> np.ndarray:
    """All label permutations preserving k positives."""
    rows = []
    for pos_idx in itertools.combinations(range(n), k):
        row = np.zeros(n, dtype=bool)
        row[list(pos_idx)] = True
        rows.append(row)
    return np.vstack(rows)


def auc_from_ranks(ranks: np.ndarray, label_matrix: np.ndarray, k: int) -> np.ndarray:
    """Vectorized Mann-Whitney AUC for many label permutations."""
    n = ranks.shape[0]
    denom = k * (n - k)
    rank_sums = label_matrix.astype(float) @ ranks
    return (rank_sums - (k * (k + 1) / 2.0)) / denom


def oriented_auc(scores: np.ndarray, labels: np.ndarray) -> tuple[float, float, str]:
    raw = auc_raw(scores, labels)
    if raw >= 0.5:
        return raw, raw, "higher_in_responders"
    return raw, 1.0 - raw, "lower_in_responders"


def exact_oriented_auc_p(scores: np.ndarray, labels: np.ndarray) -> float:
    """Exact permutation p for max(AUC, 1-AUC), preserving responder count."""
    obs = oriented_auc(scores, labels)[1]
    n = len(labels)
    k = int(labels.sum())
    label_matrix = permutation_label_matrix(n, k)
    aucs = auc_from_ranks(average_ranks(scores), label_matrix, k)
    stats = np.maximum(aucs, 1.0 - aucs)
    total = len(stats)
    ge = int(np.sum(stats >= obs - 1e-12))
    return (ge + 1.0) / (total + 1.0)


def bh_qvalues(pvalues: list[float]) -> list[float]:
    m = len(pvalues)
    order = np.argsort(pvalues)
    q = np.empty(m, dtype=float)
    running = 1.0
    for rank, idx in enumerate(order[::-1], start=1):
        # rank from largest p downward.
        true_rank = m - rank + 1
        running = min(running, pvalues[idx] * m / true_rank)
        q[idx] = running
    return q.tolist()


def responder_centroid_distances(
    matrix: np.ndarray, labels: np.ndarray, leave_one_out: bool = True
) -> np.ndarray:
    """Distance from each row to the responder centroid.

    For responders, leave-one-out avoids a sample being its own set-point.
    For non-responders, all responders define the set-point.
    """
    distances = np.zeros(len(labels), dtype=float)
    for i in range(len(labels)):
        mask = labels == 1
        if leave_one_out and labels[i] == 1:
            mask = mask.copy()
            mask[i] = False
        if not mask.any():
            distances[i] = np.nan
            continue
        center = np.nanmedian(matrix[mask, :], axis=0)
        distances[i] = float(np.linalg.norm(matrix[i, :] - center))
    return distances


def monte_carlo_setpoint_p(
    matrix: np.ndarray, labels: np.ndarray, n_permutations: int = 5000
) -> tuple[float, float]:
    """Permutation p for responder-centroid proximity, recomputing centroid."""
    obs_dist = responder_centroid_distances(matrix, labels)
    _, obs, _ = oriented_auc(obs_dist, labels)
    n = len(labels)
    k = int(labels.sum())
    rng = np.random.default_rng(3805)
    ge = 0
    for _ in range(n_permutations):
        pos_idx = rng.choice(n, size=k, replace=False)
        perm = np.zeros(n, dtype=int)
        perm[list(pos_idx)] = 1
        dist = responder_centroid_distances(matrix, perm)
        if np.isnan(dist).any():
            continue
        stat = oriented_auc(dist, perm)[1]
        if stat >= obs - 1e-12:
            ge += 1
    return obs, (ge + 1.0) / (n_permutations + 1.0)


def zscore_columns(values: np.ndarray) -> np.ndarray:
    mean = np.nanmean(values, axis=0)
    std = np.nanstd(values, axis=0)
    std[std == 0] = 1.0
    return (values - mean) / std


def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(INPUT, sep="\t")
    labels = (df["response"] == "Responder").astype(int).to_numpy()

    features: list[dict[str, object]] = []

    def add_feature(family: str, name: str, values: np.ndarray) -> None:
        raw, oriented, orientation = oriented_auc(values, labels)
        responders = values[labels == 1]
        nonresponders = values[labels == 0]
        features.append(
            {
                "feature_family": family,
                "feature": name,
                "auc_raw_higher_predicts_response": raw,
                "auc_oriented": oriented,
                "orientation": orientation,
                "exact_permutation_p": exact_oriented_auc_p(values, labels),
                "responder_median": float(np.nanmedian(responders)),
                "nonresponder_median": float(np.nanmedian(nonresponders)),
                "median_difference_responder_minus_nonresponder": float(
                    np.nanmedian(responders) - np.nanmedian(nonresponders)
                ),
            }
        )

    # Baseline load / initial state.
    for module in MODULES:
        col = f"baseline_{module}"
        if col in df:
            add_feature("baseline_load", col, df[col].to_numpy(float))
    add_feature("baseline_load", "baseline_apc_hla_level", df["baseline_apc_hla_level"].to_numpy(float))

    # Early control action / dynamic response.
    add_feature("early_delta", "locked_signed_score", df["locked_signed_score"].to_numpy(float))
    for module in MODULES:
        col = f"delta_{module}"
        if col in df:
            add_feature("early_delta", col, df[col].to_numpy(float))

    # Treated-state set-point as an unsupervised final-state readout.
    for module in MODULES:
        b = f"baseline_{module}"
        d = f"delta_{module}"
        if b in df and d in df:
            values = df[b].to_numpy(float) + df[d].to_numpy(float)
            add_feature("treated_state", f"treated_{module}", values)

    # Simple feedback features: positive values mean movement against the
    # baseline displacement. These test a control-action framing without
    # fitting a model.
    for module in MODULES:
        b = f"baseline_{module}"
        d = f"delta_{module}"
        if b in df and d in df:
            feedback = -df[b].to_numpy(float) * df[d].to_numpy(float)
            add_feature("negative_feedback", f"feedback_{module}", feedback)

    feature_df = pd.DataFrame(features)
    feature_df["bh_q_all_features"] = bh_qvalues(feature_df["exact_permutation_p"].tolist())
    feature_df = feature_df.sort_values(
        ["auc_oriented", "exact_permutation_p"], ascending=[False, True]
    )
    feature_df.to_csv(OUTDIR / "control_feature_tests.tsv", sep="\t", index=False)

    # Family-level best feature, with within-family max-AUC permutation where
    # the features are not response-derived.
    family_rows = []
    for family, sub in feature_df.groupby("feature_family", sort=False):
        best = sub.sort_values(["auc_oriented", "exact_permutation_p"], ascending=[False, True]).iloc[0]
        cols = sub["feature"].tolist()
        matrix = np.column_stack([df_col_values(df, col) for col in cols])
        obs = float(best["auc_oriented"])
        n = len(labels)
        k = int(labels.sum())
        label_matrix = permutation_label_matrix(n, k)
        rank_matrix = np.column_stack([average_ranks(matrix[:, j]) for j in range(matrix.shape[1])])
        aucs = auc_from_ranks(rank_matrix, label_matrix, k)
        stats = np.maximum(aucs, 1.0 - aucs).max(axis=1)
        total = len(stats)
        ge = int(np.sum(stats >= obs - 1e-12))
        family_rows.append(
            {
                "feature_family": family,
                "n_features": len(cols),
                "best_feature": best["feature"],
                "best_auc_oriented": obs,
                "best_feature_exact_p": best["exact_permutation_p"],
                "within_family_max_auc_permutation_p": (ge + 1.0) / (total + 1.0),
            }
        )
    family_df = pd.DataFrame(family_rows).sort_values("best_auc_oriented", ascending=False)
    family_df.to_csv(OUTDIR / "control_feature_family_tests.tsv", sep="\t", index=False)

    # Supervised responder-centroid set-point tests. These are exploratory and
    # their permutation recomputes the responder centroid each time.
    spaces = {
        "baseline_ifn_hlaii_stat1_metabolic": [
            "baseline_IFN_APC",
            "baseline_HLAII",
            "baseline_stat1_axis",
            "baseline_glycolysis",
            "baseline_oxphos",
        ],
        "delta_ifn_hlaii_stat1_metabolic": [
            "delta_IFN_APC",
            "delta_HLAII",
            "delta_stat1_axis",
            "delta_glycolysis",
            "delta_oxphos",
        ],
        "treated_ifn_hlaii_stat1_metabolic": [
            "treated_IFN_APC",
            "treated_HLAII",
            "treated_stat1_axis",
            "treated_glycolysis",
            "treated_oxphos",
        ],
        "treated_composition": [
            "treated_monocyte_myeloid_composition",
            "treated_t_cell_composition",
            "treated_b_cell_composition",
        ],
    }
    treated = {}
    for module in MODULES:
        b = f"baseline_{module}"
        d = f"delta_{module}"
        if b in df and d in df:
            treated[f"treated_{module}"] = df[b].to_numpy(float) + df[d].to_numpy(float)

    setpoint_rows = []
    for space_name, cols in spaces.items():
        vals = []
        missing = []
        for col in cols:
            if col in df:
                vals.append(df[col].to_numpy(float))
            elif col in treated:
                vals.append(treated[col])
            else:
                missing.append(col)
        if missing:
            continue
        matrix = zscore_columns(np.column_stack(vals))
        distances = responder_centroid_distances(matrix, labels)
        raw, oriented, orientation = oriented_auc(distances, labels)
        _, p = monte_carlo_setpoint_p(matrix, labels)
        setpoint_rows.append(
            {
                "setpoint_space": space_name,
                "columns": ",".join(cols),
                "auc_raw_higher_distance_predicts_response": raw,
                "auc_oriented": oriented,
                "orientation": orientation,
                "monte_carlo_permutation_p_recomputing_centroid": p,
                "n_monte_carlo_permutations": 5000,
                "responder_median_distance": float(np.nanmedian(distances[labels == 1])),
                "nonresponder_median_distance": float(np.nanmedian(distances[labels == 0])),
            }
        )
    setpoint_df = pd.DataFrame(setpoint_rows).sort_values("auc_oriented", ascending=False)
    setpoint_df.to_csv(OUTDIR / "setpoint_distance_tests.tsv", sep="\t", index=False)

    top_features = feature_df.head(10).to_dict(orient="records")
    summary = {
        "input": str(INPUT.relative_to(ROOT)),
        "n_subjects": int(len(df)),
        "n_responders": int(labels.sum()),
        "n_nonresponders": int(len(labels) - labels.sum()),
        "cohorts": df["cohort"].value_counts().to_dict(),
        "n_features_tested": int(len(feature_df)),
        "best_feature_by_oriented_auc": top_features[0],
        "family_best": family_df.to_dict(orient="records"),
        "setpoint_tests": setpoint_df.to_dict(orient="records"),
        "interpretation": (
            "Exploratory control-systems reframing. The strongest signal remains "
            "an early dynamic/control-action feature, not a pure baseline-load "
            "or treated-setpoint feature. Set-point distances are supervised "
            "exploratory probes tested with fixed-seed Monte Carlo label "
            "permutation and require fresh validation before any rule use."
        ),
    }
    with (OUTDIR / "control_system_summary.json").open("w") as handle:
        json.dump(summary, handle, indent=2)


def df_col_values(df: pd.DataFrame, feature: str) -> np.ndarray:
    if feature.startswith("treated_"):
        module = feature.removeprefix("treated_")
        return df[f"baseline_{module}"].to_numpy(float) + df[f"delta_{module}"].to_numpy(float)
    if feature.startswith("feedback_"):
        module = feature.removeprefix("feedback_")
        return -df[f"baseline_{module}"].to_numpy(float) * df[f"delta_{module}"].to_numpy(float)
    return df[feature].to_numpy(float)


if __name__ == "__main__":
    main()
