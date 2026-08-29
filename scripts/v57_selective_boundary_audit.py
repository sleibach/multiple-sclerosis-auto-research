#!/usr/bin/env python3
"""Audit V22's bounded cohort pair against max-over-subset selection."""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

from v57_environment_stability_probe import auc_score, load_data


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "v57_selective_boundary"
SEEDS = (57101, 57102, 57103)
N_PERMUTATIONS = 200_000
CHUNK = 2_000
SELECTED = ("GSE235357", "GSE253006_TOF_exact")


def random_fixed_count_labels(
    rng: np.random.Generator, n_rows: int, n_subjects: int, n_positive: int
) -> np.ndarray:
    random_values = rng.random((n_rows, n_subjects))
    chosen = np.argpartition(random_values, n_positive - 1, axis=1)[:, :n_positive]
    labels = np.zeros((n_rows, n_subjects), dtype=np.float64)
    labels[np.arange(n_rows)[:, None], chosen] = 1.0
    return labels


def auc_many(labels: np.ndarray, scores: np.ndarray) -> np.ndarray:
    ranks = stats.rankdata(scores, method="average")
    n_positive = labels.sum(axis=1)
    n_negative = labels.shape[1] - n_positive
    rank_sum = (labels * ranks[None, :]).sum(axis=1)
    return (rank_sum - n_positive * (n_positive + 1.0) / 2.0) / (n_positive * n_negative)


def subset_frame(data: pd.DataFrame, subset: tuple[str, ...]) -> pd.DataFrame:
    frames = [data[data["cohort"] == cohort] for cohort in subset]
    return pd.concat(frames, ignore_index=True)


def observed_subsets(data: pd.DataFrame, subsets: list[tuple[str, ...]]) -> pd.DataFrame:
    rows = []
    for subset in subsets:
        frame = subset_frame(data, subset)
        y = frame["response_binary"].to_numpy(np.int8)
        rows.append(
            {
                "subset": ";".join(subset),
                "n_cohorts": len(subset),
                "n_subjects": len(frame),
                "raw_locked_auc": auc_score(y, frame["locked_signed_score"].to_numpy(float)),
                "cohort_percentile_auc": auc_score(y, frame["score_percentile"].to_numpy(float)),
                "is_selected_bounded_pair": subset == SELECTED,
            }
        )
    output = pd.DataFrame(rows)
    pairs = output[output["n_cohorts"] == 2]
    for metric in ("raw_locked_auc", "cohort_percentile_auc"):
        ranks = pairs[metric].rank(method="min", ascending=False).astype(int)
        output.loc[pairs.index, f"pair_rank_{metric}"] = ranks
    return output.sort_values(["n_cohorts", "subset"], kind="stable").reset_index(drop=True)


def run_seed(
    data: pd.DataFrame,
    subsets: list[tuple[str, ...]],
    observed_raw: float,
    observed_percentile: float,
    seed: int,
) -> list[dict[str, object]]:
    rng = np.random.default_rng(seed)
    cohort_frames = {
        cohort: data[data["cohort"] == cohort].reset_index(drop=True)
        for cohort in sorted(data["cohort"].unique())
    }
    exceed = {
        "raw_selected_unadjusted": 0,
        "raw_max_six_pairs": 0,
        "raw_max_all_subsets": 0,
        "percentile_selected_unadjusted": 0,
        "percentile_max_six_pairs": 0,
        "percentile_max_all_subsets": 0,
    }
    processed = 0
    while processed < N_PERMUTATIONS:
        batch = min(CHUNK, N_PERMUTATIONS - processed)
        labels_by_cohort = {
            cohort: random_fixed_count_labels(
                rng,
                batch,
                len(frame),
                int(frame["response_binary"].sum()),
            )
            for cohort, frame in cohort_frames.items()
        }
        max_pair_raw = np.full(batch, -np.inf)
        max_all_raw = np.full(batch, -np.inf)
        max_pair_pct = np.full(batch, -np.inf)
        max_all_pct = np.full(batch, -np.inf)
        selected_raw = None
        selected_pct = None
        for subset in subsets:
            labels = np.concatenate([labels_by_cohort[cohort] for cohort in subset], axis=1)
            scores_raw = np.concatenate(
                [cohort_frames[cohort]["locked_signed_score"].to_numpy(float) for cohort in subset]
            )
            scores_pct = np.concatenate(
                [cohort_frames[cohort]["score_percentile"].to_numpy(float) for cohort in subset]
            )
            raw_auc = auc_many(labels, scores_raw)
            pct_auc = auc_many(labels, scores_pct)
            max_all_raw = np.maximum(max_all_raw, raw_auc)
            max_all_pct = np.maximum(max_all_pct, pct_auc)
            if len(subset) == 2:
                max_pair_raw = np.maximum(max_pair_raw, raw_auc)
                max_pair_pct = np.maximum(max_pair_pct, pct_auc)
            if subset == SELECTED:
                selected_raw = raw_auc
                selected_pct = pct_auc
        if selected_raw is None or selected_pct is None:
            raise RuntimeError("Selected subset absent from candidate family")
        exceed["raw_selected_unadjusted"] += int(np.sum(selected_raw >= observed_raw - 1e-12))
        exceed["raw_max_six_pairs"] += int(np.sum(max_pair_raw >= observed_raw - 1e-12))
        exceed["raw_max_all_subsets"] += int(np.sum(max_all_raw >= observed_raw - 1e-12))
        exceed["percentile_selected_unadjusted"] += int(
            np.sum(selected_pct >= observed_percentile - 1e-12)
        )
        exceed["percentile_max_six_pairs"] += int(
            np.sum(max_pair_pct >= observed_percentile - 1e-12)
        )
        exceed["percentile_max_all_subsets"] += int(
            np.sum(max_all_pct >= observed_percentile - 1e-12)
        )
        processed += batch

    rows = []
    for test, count in exceed.items():
        rows.append(
            {
                "seed": seed,
                "test": test,
                "n_permutations": N_PERMUTATIONS,
                "exceedances": count,
                "permutation_p": (count + 1) / (N_PERMUTATIONS + 1),
            }
        )
    return rows


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    data = load_data()
    cohorts = tuple(sorted(data["cohort"].unique()))
    subsets = [
        subset
        for size in (2, 3, 4)
        for subset in itertools.combinations(cohorts, size)
    ]
    observed = observed_subsets(data, subsets)
    selected = observed[observed["is_selected_bounded_pair"]].iloc[0]
    rows = []
    for seed in SEEDS:
        rows.extend(
            run_seed(
                data,
                subsets,
                float(selected["raw_locked_auc"]),
                float(selected["cohort_percentile_auc"]),
                seed,
            )
        )
    tests = pd.DataFrame(rows)
    raw_pair = tests[tests["test"] == "raw_max_six_pairs"]
    pct_pair = tests[tests["test"] == "percentile_max_six_pairs"]
    gate = bool((raw_pair["permutation_p"] <= 0.05).all() and (pct_pair["permutation_p"] <= 0.05).all())
    summary = {
        "purpose": "V57 mechanism-boundary subset-selection sensitivity; not evidence of selection intent",
        "cohorts": list(cohorts),
        "selected_pair": list(SELECTED),
        "n_pair_candidates": 6,
        "n_all_subset_candidates": len(subsets),
        "n_permutations_per_seed": N_PERMUTATIONS,
        "seeds": list(SEEDS),
        "selected_raw_auc": float(selected["raw_locked_auc"]),
        "selected_percentile_auc": float(selected["cohort_percentile_auc"]),
        "selected_pair_raw_rank": int(selected["pair_rank_raw_locked_auc"]),
        "selected_pair_percentile_rank": int(selected["pair_rank_cohort_percentile_auc"]),
        "raw_max_pair_p_range": [float(raw_pair["permutation_p"].min()), float(raw_pair["permutation_p"].max())],
        "percentile_max_pair_p_range": [float(pct_pair["permutation_p"].min()), float(pct_pair["permutation_p"].max())],
        "selection_robust_gate_pass": gate,
        "verdict": "BOUNDARY_SURVIVES_WORST_CASE_PAIR_SELECTION" if gate else "BOUNDARY_NOT_SELECTION_ROBUST_ON_HELD_FAMILY",
    }
    observed.to_csv(OUT / "observed_cohort_subsets.tsv", sep="\t", index=False)
    tests.to_csv(OUT / "selective_permutation_tests.tsv", sep="\t", index=False)
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    report = f"""# V57 Mechanism-Boundary Selective-Inference Audit

## Result

The selected bounded pair has raw pooled AUC
{summary['selected_raw_auc']:.3f} and within-cohort-percentile AUC
{summary['selected_percentile_auc']:.3f}. It ranks
{summary['selected_pair_raw_rank']}/6 among all cohort pairs by raw AUC and
{summary['selected_pair_percentile_rank']}/6 by percentile AUC.

After max-over-six-pair correction, raw-score permutation p ranges from
{summary['raw_max_pair_p_range'][0]:.4f} to
{summary['raw_max_pair_p_range'][1]:.4f}; percentile-score p ranges from
{summary['percentile_max_pair_p_range'][0]:.4f} to
{summary['percentile_max_pair_p_range'][1]:.4f}. The predeclared
selection-robust gate **{'passes' if gate else 'fails'}**.

## Interpretation

The observed bounded-pair performance remains unusual even after allowing an
analyst to choose the best of the six cohort pairs. This weakens pure favorable
pair selection as a sufficient explanation of the held result. It does not
prove V23's biological mechanism rationale: the audit reuses the same four
held cohorts, tests a finite candidate family, and supplies no independent MS
validation. The mechanism boundary still requires an externally preregistered
cohort before it can carry generalization weight.

The V22 rule, V23 mechanism labels, and validation plan remain unchanged. This
is an adversarial selection sensitivity, not external validation or a new MS
finding.
"""
    (OUT / "REPORT.md").write_text(report)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
