#!/usr/bin/env python3
"""Patient-level multivariate transport-map probe in paired single cells."""

from __future__ import annotations

import argparse
import json
import math
import zlib
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy.optimize import linear_sum_assignment
from scipy.spatial.distance import cdist

from v57_single_cell_transport_probe import (
    MODULES,
    STATES,
    disease_directions,
    eligible_pairs,
    load_cell_scores,
    stratified_permutation_matrix,
    studentized_difference,
    vectorized_studentized_difference,
)


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "analysis/v57_multivariate_transport_map"
SEEDS = (57141, 57142, 57143)
N_CELLS = 50
N_PERMUTATIONS = 200_000
METRICS = ("transport_cost", "directional_coherence", "anisotropy", "norm_mad")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--permutations", type=int, default=N_PERMUTATIONS)
    return parser.parse_args()


def deterministic_sample(indices: np.ndarray, key: str, seed: int) -> np.ndarray:
    if len(indices) < N_CELLS:
        return np.array([], dtype=int)
    local_seed = (seed + zlib.crc32(key.encode("utf-8"))) % (2**32)
    rng = np.random.default_rng(local_seed)
    return np.sort(rng.choice(indices, size=N_CELLS, replace=False))


def displacement_metrics(pre: np.ndarray, post: np.ndarray) -> dict[str, float]:
    pre_index, post_index = linear_sum_assignment(cdist(pre, post, metric="euclidean"))
    displacement = post[post_index] - pre[pre_index]
    norms = np.linalg.norm(displacement, axis=1)
    mean_cost = float(np.mean(norms))
    coherence = float(np.linalg.norm(np.mean(displacement, axis=0)) / max(mean_cost, 1e-12))
    covariance = np.atleast_2d(np.cov(displacement, rowvar=False, ddof=1))
    eigenvalues = np.linalg.eigvalsh(covariance)
    anisotropy = float(np.max(eigenvalues) / max(float(np.sum(eigenvalues)), 1e-12))
    median = float(np.median(norms))
    return {
        "transport_cost": mean_cost,
        "directional_coherence": coherence,
        "anisotropy": anisotropy,
        "norm_mad": float(np.median(np.abs(norms - median))),
    }


def build_pairs(seed: int) -> pd.DataFrame:
    obs, scores, _ = load_cell_scores()
    matrix = np.column_stack([scores[module] for module in MODULES])
    center = np.nanmedian(matrix, axis=0)
    scale = np.nanquantile(matrix, 0.75, axis=0) - np.nanquantile(matrix, 0.25, axis=0)
    matrix = (matrix - center) / np.where(scale > 0, scale, 1.0)
    sample = obs.sample_id.astype(str).to_numpy()
    state = obs.major.astype(str).to_numpy()
    depth = obs.log_total_counts.to_numpy(float)
    rows: list[dict[str, Any]] = []
    for pair in eligible_pairs().itertuples(index=False):
        pre_all = np.flatnonzero(
            (sample == str(pair.pre_sample_id)) & (state == pair.cell_state)
        )
        post_all = np.flatnonzero(
            (sample == str(pair.post_sample_id)) & (state == pair.cell_state)
        )
        pre = deterministic_sample(pre_all, f"{pair.pair_id}|pre", seed)
        post = deterministic_sample(post_all, f"{pair.pair_id}|post", seed)
        if len(pre) != N_CELLS or len(post) != N_CELLS:
            continue
        x = matrix[pre]
        y = matrix[post]
        if not np.all(np.isfinite(x)) or not np.all(np.isfinite(y)):
            continue
        metrics = displacement_metrics(x, y)
        depth_metrics = displacement_metrics(depth[pre, None], depth[post, None])
        mean_shift = float(np.linalg.norm(np.mean(y, axis=0) - np.mean(x, axis=0)))
        for metric in METRICS:
            rows.append(
                {
                    "seed": seed,
                    "Patient": pair.Patient,
                    "Disease": pair.Disease,
                    "Site": pair.Site,
                    "Remission_status": pair.Remission_status,
                    "cell_state": pair.cell_state,
                    "pair_id": pair.pair_id,
                    "metric": metric,
                    "value": metrics[metric],
                    "depth_transport_cost": depth_metrics["transport_cost"],
                    "mean_shift_norm": mean_shift,
                    "abs_inflammation_score_change": float(
                        abs(pair.post_inflammation_score - pair.baseline_inflammation_score)
                    ),
                }
            )
    return pd.DataFrame(rows)


def patient_aggregate(pair: pd.DataFrame) -> pd.DataFrame:
    columns = [
        "value",
        "depth_transport_cost",
        "mean_shift_norm",
        "abs_inflammation_score_change",
    ]
    patient = pair.groupby(
        ["seed", "Patient", "Disease", "Remission_status", "cell_state", "metric"],
        as_index=False,
    )[columns].median()
    patient["remission_binary"] = patient.Remission_status.eq("Remission").astype(np.int8)
    return patient


def residualize(frame: pd.DataFrame) -> np.ndarray:
    y = frame.value.to_numpy(float)
    x = np.column_stack(
        [
            np.ones(len(frame)),
            frame.Disease.eq("UC").to_numpy(float),
            frame.depth_transport_cost.to_numpy(float),
            frame.mean_shift_norm.to_numpy(float),
            frame.abs_inflammation_score_change.to_numpy(float),
        ]
    )
    valid = np.isfinite(y) & np.all(np.isfinite(x), axis=1)
    output = np.full(len(frame), np.nan)
    if valid.sum() > x.shape[1]:
        beta = np.linalg.lstsq(x[valid], y[valid], rcond=None)[0]
        output[valid] = y[valid] - np.einsum("ij,j->i", x[valid], beta, optimize=False)
    return output


def estimable(frame: pd.DataFrame) -> bool:
    return frame.remission_binary.nunique() == 2 and all(
        set(frame.loc[frame.Disease.eq(disease), "remission_binary"].astype(int)) == {0, 1}
        for disease in ("CD", "UC")
    )


def test_seed(
    patient: pd.DataFrame, seed: int, residual: bool, n_permutations: int
) -> pd.DataFrame:
    data = patient[patient.seed.eq(seed)].copy()
    labels = (
        data[["Patient", "Disease", "remission_binary"]]
        .drop_duplicates()
        .sort_values(["Disease", "Patient"])
        .reset_index(drop=True)
    )
    patient_index = {str(value): index for index, value in enumerate(labels.Patient)}
    rng = np.random.default_rng(seed + (10_000 if residual else 0))
    permutations = stratified_permutation_matrix(labels, rng, n_permutations)
    prepared = []
    for state in STATES:
        for metric in METRICS:
            feature = data[data.cell_state.eq(state) & data.metric.eq(metric)].copy()
            if not estimable(feature):
                continue
            feature["test_value"] = residualize(feature) if residual else feature.value
            feature = feature[np.isfinite(feature.test_value)].copy()
            if not estimable(feature):
                continue
            statistic = studentized_difference(
                feature.test_value.to_numpy(float), feature.remission_binary.to_numpy(np.int8)
            )
            if np.isfinite(statistic):
                prepared.append(
                    (
                        state,
                        metric,
                        feature,
                        statistic,
                        disease_directions(feature.rename(columns={"test_value": "test"}), "test"),
                    )
                )
    if not prepared:
        return pd.DataFrame()
    null = np.empty((n_permutations, len(prepared)), dtype=np.float32)
    for column, (_, _, feature, _, _) in enumerate(prepared):
        indices = np.array([patient_index[str(value)] for value in feature.Patient], dtype=int)
        null[:, column] = vectorized_studentized_difference(
            feature.test_value.to_numpy(float), permutations[:, indices]
        )
    null_abs = np.abs(null)
    null_max = np.nanmax(null_abs, axis=1)
    rows = []
    for column, (state, metric, feature, statistic, directions) in enumerate(prepared):
        sign = int(np.sign(statistic))
        consistent = all(
            int(np.sign(directions[disease]["mean_difference"])) == sign
            for disease in ("CD", "UC")
        )
        rows.append(
            {
                "seed": seed,
                "analysis": "residualized" if residual else "raw",
                "cell_state": state,
                "metric": metric,
                "n_patients": len(feature),
                "studentized_effect": statistic,
                "raw_permutation_p": (1 + int(np.sum(null_abs[:, column] >= abs(statistic))))
                / (n_permutations + 1),
                "max_t_fwer_p": (1 + int(np.sum(null_max >= abs(statistic))))
                / (n_permutations + 1),
                "direction_consistent_cd_uc": bool(consistent),
                "cd_mean_difference": directions["CD"]["mean_difference"],
                "uc_mean_difference": directions["UC"]["mean_difference"],
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    args = parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)
    pair = pd.concat([build_pairs(seed) for seed in SEEDS], ignore_index=True)
    patient = patient_aggregate(pair)
    pieces = []
    for seed in SEEDS:
        for residual in (False, True):
            result = test_seed(patient, seed, residual, args.permutations)
            if not result.empty:
                pieces.append(result)
    tests = pd.concat(pieces, ignore_index=True) if pieces else pd.DataFrame()
    stable_features: list[str] = []
    if not tests.empty:
        wide = tests.pivot(
            index=["seed", "cell_state", "metric"],
            columns="analysis",
            values=["studentized_effect", "max_t_fwer_p", "direction_consistent_cd_uc"],
        )
        wide.columns = ["_".join(column) for column in wide.columns]
        wide = wide.reset_index()
        wide["passes_seed"] = (
            wide.max_t_fwer_p_raw.le(0.10)
            & wide.max_t_fwer_p_residualized.le(0.10)
            & (np.sign(wide.studentized_effect_raw) == np.sign(wide.studentized_effect_residualized))
            & wide.direction_consistent_cd_uc_raw.astype(bool)
            & wide.direction_consistent_cd_uc_residualized.astype(bool)
        )
        stable = wide.groupby(["cell_state", "metric"], as_index=False).agg(
            n_seeds=("seed", "nunique"), all_pass=("passes_seed", "all")
        )
        stable = stable[stable.n_seeds.eq(len(SEEDS)) & stable.all_pass.astype(bool)]
        stable_features = [f"{row.cell_state}__{row.metric}" for row in stable.itertuples()]
        wide.to_csv(args.outdir / "seed_pass_matrix.tsv", sep="\t", index=False)
    else:
        pd.DataFrame().to_csv(args.outdir / "seed_pass_matrix.tsv", sep="\t", index=False)
    summary = {
        "seeds": list(SEEDS),
        "cells_per_sample_compartment": N_CELLS,
        "n_permutations_per_seed_analysis": args.permutations,
        "n_unique_patients": int(patient.Patient.nunique()),
        "n_pair_metric_rows": len(pair),
        "n_estimable_features": int(tests[["cell_state", "metric"]].drop_duplicates().shape[0])
        if not tests.empty
        else 0,
        "stable_passing_features": stable_features,
        "verdict": "STABLE_RESPONSE_SPECIFIC_TRANSPORT_MAP_SUPPORTED"
        if stable_features
        else "NO_STABLE_RESPONSE_SPECIFIC_TRANSPORT_MAP",
        "boundary": "Held anti-TNF IBD method context only; not an MS finding or target result",
    }
    pair.to_csv(args.outdir / "pair_transport_map_metrics.tsv", sep="\t", index=False)
    patient.to_csv(args.outdir / "patient_transport_map_metrics.tsv", sep="\t", index=False)
    tests.to_csv(args.outdir / "transport_map_tests.tsv", sep="\t", index=False)
    (args.outdir / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n"
    )
    top_text = "none"
    if not tests.empty:
        top = tests.sort_values("max_t_fwer_p").iloc[0]
        top_text = f"{top.cell_state}__{top.metric} (max-T p={top.max_t_fwer_p:.4f})"
    report = f"""# V57 Multivariate Cell-State Transport Map

## Boundary

This is a held anti-TNF IBD method-feasibility result, not an MS biological
finding.

## Result

- Unique patients: {patient.Patient.nunique()}
- Estimable compartment-summary features: {summary['n_estimable_features']}
- Best single seed/analysis result: {top_text}
- Stable features passing every gate:
  {', '.join(stable_features) if stable_features else 'none'}

Verdict: **{summary['verdict']}**.

The result tests matched displacement-field geometry beyond marginal and
global distances. Cells were never treated as outcome replicates. A paired,
response-labelled MS single-cell cohort is required for an MS-specific test.
"""
    (args.outdir / "REPORT.md").write_text(report)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
