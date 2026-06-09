#!/usr/bin/env python3
"""V39 cross-domain anomaly/control-system reframing.

Question: in the bounded V22/V23 treatment-response table, do responders form
an immune-state "attractor" after treatment, or is the signal just another way
to score the locked scalar?

This is an exploratory cross-domain analysis. It does not create or tune a new
rule. It tests compactness/separation in pre-defined immune-tone spaces using
exact label permutations preserving the responder count.
"""

from __future__ import annotations

import itertools
import json
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "analysis" / "v32_confounder_audit" / "v32_subject_confounder_scores.tsv"
OUT = ROOT / "analysis" / "v39_immune_tone_anomaly"


CORE_MODULES = ["IFN_APC", "HLAII", "stat1_axis", "glycolysis", "oxphos"]
COMPOSITION_MODULES = [
    "monocyte_myeloid_composition",
    "t_cell_composition",
    "b_cell_composition",
]
BROAD_TONE_MODULES = [
    "general_inflammatory_tone",
    "stat1_axis",
    "glycolysis",
    "oxphos",
    "immunometabolism_hif_nampt",
]


@lru_cache(maxsize=None)
def label_matrix(n: int, k: int) -> np.ndarray:
    rows = []
    for pos in itertools.combinations(range(n), k):
        row = np.zeros(n, dtype=bool)
        row[list(pos)] = True
        rows.append(row)
    return np.vstack(rows)


def zscore(matrix: np.ndarray) -> np.ndarray:
    mean = np.nanmean(matrix, axis=0)
    std = np.nanstd(matrix, axis=0)
    std[std == 0] = 1.0
    return (matrix - mean) / std


def pairwise_distances(matrix: np.ndarray) -> np.ndarray:
    diff = matrix[:, None, :] - matrix[None, :, :]
    return np.sqrt(np.nansum(diff * diff, axis=2))


def median_pair_distance(dist: np.ndarray, mask_a: np.ndarray, mask_b: np.ndarray, same: bool) -> float:
    if same:
        idx = np.where(mask_a)[0]
        if len(idx) < 2:
            return float("nan")
        vals = [dist[i, j] for a, i in enumerate(idx) for j in idx[a + 1 :]]
    else:
        idx_a = np.where(mask_a)[0]
        idx_b = np.where(mask_b)[0]
        if len(idx_a) == 0 or len(idx_b) == 0:
            return float("nan")
        vals = [dist[i, j] for i in idx_a for j in idx_b]
    return float(np.nanmedian(vals))


def metrics_for_labels(dist: np.ndarray, labels: np.ndarray) -> dict[str, float]:
    responders = labels.astype(bool)
    nonresponders = ~responders
    within_r = median_pair_distance(dist, responders, responders, same=True)
    within_nr = median_pair_distance(dist, nonresponders, nonresponders, same=True)
    between = median_pair_distance(dist, responders, nonresponders, same=False)
    return {
        "responder_within_median_distance": within_r,
        "nonresponder_within_median_distance": within_nr,
        "between_group_median_distance": between,
        "responder_compactness_delta": within_r - within_nr,
        "separation_margin": between - 0.5 * (within_r + within_nr),
    }


def exact_permutation_tests(dist: np.ndarray, labels: np.ndarray) -> tuple[dict[str, float], dict[str, float]]:
    obs = metrics_for_labels(dist, labels)
    n = len(labels)
    k = int(labels.sum())
    compact_stats = []
    separation_stats = []
    for perm in label_matrix(n, k):
        m = metrics_for_labels(dist, perm)
        compact_stats.append(m["responder_compactness_delta"])
        separation_stats.append(m["separation_margin"])
    compact_stats = np.asarray(compact_stats, dtype=float)
    separation_stats = np.asarray(separation_stats, dtype=float)
    p_compact = (np.sum(compact_stats <= obs["responder_compactness_delta"] + 1e-12) + 1.0) / (
        len(compact_stats) + 1.0
    )
    p_separation = (np.sum(separation_stats >= obs["separation_margin"] - 1e-12) + 1.0) / (
        len(separation_stats) + 1.0
    )
    pvals = {
        "exact_p_responder_more_compact": float(p_compact),
        "exact_p_greater_group_separation": float(p_separation),
        "n_exact_label_permutations": int(len(compact_stats)),
    }
    return obs, pvals


def matrix_for_space(df: pd.DataFrame, timing: str, modules: list[str]) -> np.ndarray:
    cols = []
    for module in modules:
        if timing == "baseline":
            cols.append(df[f"baseline_{module}"].to_numpy(float))
        elif timing == "delta":
            cols.append(df[f"delta_{module}"].to_numpy(float))
        elif timing == "treated":
            cols.append(
                df[f"baseline_{module}"].to_numpy(float) + df[f"delta_{module}"].to_numpy(float)
            )
        else:
            raise ValueError(timing)
    return np.column_stack(cols)


def bh_qvalues(values: list[float]) -> list[float]:
    m = len(values)
    order = np.argsort(values)
    q = np.empty(m, dtype=float)
    running = 1.0
    for rank, idx in enumerate(order[::-1], start=1):
        true_rank = m - rank + 1
        running = min(running, values[idx] * m / true_rank)
        q[idx] = running
    return q.tolist()


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(INPUT, sep="\t")
    labels = (df["response"] == "Responder").astype(int).to_numpy()

    spaces = [
        ("baseline_core", "baseline", CORE_MODULES),
        ("delta_core", "delta", CORE_MODULES),
        ("treated_core", "treated", CORE_MODULES),
        ("baseline_composition", "baseline", COMPOSITION_MODULES),
        ("delta_composition", "delta", COMPOSITION_MODULES),
        ("treated_composition", "treated", COMPOSITION_MODULES),
        ("delta_broad_tone", "delta", BROAD_TONE_MODULES),
        ("treated_broad_tone", "treated", BROAD_TONE_MODULES),
    ]

    rows = []
    for name, timing, modules in spaces:
        matrix = zscore(matrix_for_space(df, timing, modules))
        dist = pairwise_distances(matrix)
        obs, pvals = exact_permutation_tests(dist, labels)
        rows.append(
            {
                "space": name,
                "timing": timing,
                "modules": ";".join(modules),
                **obs,
                **pvals,
            }
        )

    result = pd.DataFrame(rows)
    result["compactness_bonferroni_p"] = np.minimum(
        1.0, result["exact_p_responder_more_compact"] * len(result)
    )
    result["separation_bonferroni_p"] = np.minimum(
        1.0, result["exact_p_greater_group_separation"] * len(result)
    )
    result["compactness_bh_q"] = bh_qvalues(result["exact_p_responder_more_compact"].tolist())
    result["separation_bh_q"] = bh_qvalues(result["exact_p_greater_group_separation"].tolist())
    result = result.sort_values(
        ["exact_p_responder_more_compact", "exact_p_greater_group_separation"],
        ascending=[True, True],
    )
    result.to_csv(OUT / "immune_tone_anomaly_spaces.tsv", sep="\t", index=False)

    best_compact = result.iloc[0].to_dict()
    best_separation = result.sort_values("exact_p_greater_group_separation").iloc[0].to_dict()
    summary = {
        "input": str(INPUT.relative_to(ROOT)),
        "n_subjects": int(len(df)),
        "n_responders": int(labels.sum()),
        "n_nonresponders": int((1 - labels).sum()),
        "spaces_tested": int(len(result)),
        "best_compactness_space": best_compact,
        "best_separation_space": best_separation,
        "interpretation": (
            "Exploratory anomaly/control-system framing. Responders are tested for "
            "compactness and group separation in pre-defined immune-tone spaces with "
            "exact label permutations and eight-space multiple-testing correction. "
            "This is not a new rule and must not replace the locked V22 scalar."
        ),
    }
    (OUT / "immune_tone_anomaly_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
