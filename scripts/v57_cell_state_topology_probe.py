#!/usr/bin/env python3
"""Patient-level 0D persistence probe in paired single-cell states."""

from __future__ import annotations

import argparse
import json
import math
import zlib
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy.spatial.distance import squareform, pdist

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
DEFAULT_OUT = ROOT / "analysis/v57_cell_state_topology"
SEEDS = (57121, 57122, 57123)
N_CELLS = 150
N_PERMUTATIONS = 200_000
METRICS = ("total_persistence", "max_lifetime", "persistence_entropy", "q90_median_ratio")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--permutations", type=int, default=N_PERMUTATIONS)
    return parser.parse_args()


def deterministic_sample(indices: np.ndarray, key: str, seed: int) -> np.ndarray:
    local_seed = (seed + zlib.crc32(key.encode("utf-8"))) % (2**32)
    rng = np.random.default_rng(local_seed)
    return np.sort(rng.choice(indices, size=N_CELLS, replace=False))


def persistence_metrics(points: np.ndarray) -> dict[str, float]:
    distance = squareform(pdist(points, metric="euclidean"))
    # Prim's algorithm is kept local because scipy's sparse MST treats exact
    # zero-distance ties as absent edges. Zero persistence is valid for tied
    # points and must remain in the fixed-size topology summary.
    selected = np.zeros(len(points), dtype=bool)
    selected[0] = True
    nearest = distance[0].copy()
    nearest[0] = np.inf
    lifetimes = np.empty(len(points) - 1, dtype=float)
    for index in range(len(points) - 1):
        candidate = int(np.argmin(np.where(selected, np.inf, nearest)))
        lifetimes[index] = nearest[candidate]
        selected[candidate] = True
        nearest = np.minimum(nearest, distance[candidate])
    if np.any(lifetimes < 0) or not np.all(np.isfinite(lifetimes)):
        raise ValueError("Invalid MST persistence lifetime")
    mass = lifetimes / np.sum(lifetimes)
    positive = mass > 0
    entropy = float(-np.sum(mass[positive] * np.log(mass[positive])) / np.log(len(lifetimes)))
    median = max(float(np.median(lifetimes)), 1e-12)
    return {
        "total_persistence": float(np.sum(lifetimes)),
        "max_lifetime": float(np.max(lifetimes)),
        "persistence_entropy": entropy,
        "q90_median_ratio": float(np.quantile(lifetimes, 0.90) / median),
    }


def build_pair_metrics(seed: int) -> pd.DataFrame:
    obs, scores, _ = load_cell_scores()
    matrix = np.column_stack([scores[module] for module in MODULES])
    center = np.nanmedian(matrix, axis=0)
    scale = np.nanquantile(matrix, 0.75, axis=0) - np.nanquantile(matrix, 0.25, axis=0)
    matrix = (matrix - center) / np.where(scale > 0, scale, 1.0)
    sample_ids = obs.sample_id.astype(str).to_numpy()
    states = obs.major.astype(str).to_numpy()
    depths = obs.log_total_counts.to_numpy(float)
    rows: list[dict[str, Any]] = []
    for pair in eligible_pairs().itertuples(index=False):
        pre_all = np.flatnonzero(
            (sample_ids == str(pair.pre_sample_id)) & (states == pair.cell_state)
        )
        post_all = np.flatnonzero(
            (sample_ids == str(pair.post_sample_id)) & (states == pair.cell_state)
        )
        if len(pre_all) < N_CELLS or len(post_all) < N_CELLS:
            continue
        pre = deterministic_sample(pre_all, f"{pair.pair_id}|pre", seed)
        post = deterministic_sample(post_all, f"{pair.pair_id}|post", seed)
        x = matrix[pre]
        y = matrix[post]
        if not np.all(np.isfinite(x)) or not np.all(np.isfinite(y)):
            continue
        pre_topology = persistence_metrics(x)
        post_topology = persistence_metrics(y)
        pre_depth_topology = persistence_metrics(depths[pre, None])
        post_depth_topology = persistence_metrics(depths[post, None])
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
                    "topology_delta": post_topology[metric] - pre_topology[metric],
                    "depth_topology_delta": post_depth_topology[metric]
                    - pre_depth_topology[metric],
                    "mean_shift_norm": mean_shift,
                    "abs_inflammation_score_change": float(
                        abs(pair.post_inflammation_score - pair.baseline_inflammation_score)
                    ),
                    "synthetic": False,
                }
            )
    return pd.DataFrame(rows)


def patient_aggregate(pair_frame: pd.DataFrame) -> pd.DataFrame:
    columns = [
        "topology_delta",
        "depth_topology_delta",
        "mean_shift_norm",
        "abs_inflammation_score_change",
    ]
    patient = pair_frame.groupby(
        ["seed", "Patient", "Disease", "Remission_status", "cell_state", "metric"],
        as_index=False,
    )[columns].median()
    patient["remission_binary"] = patient.Remission_status.eq("Remission").astype(np.int8)
    return patient


def residualize(frame: pd.DataFrame) -> np.ndarray:
    y = frame.topology_delta.to_numpy(float)
    x = np.column_stack(
        [
            np.ones(len(frame)),
            frame.Disease.eq("UC").to_numpy(float),
            frame.depth_topology_delta.to_numpy(float),
            frame.mean_shift_norm.to_numpy(float),
            frame.abs_inflammation_score_change.to_numpy(float),
        ]
    )
    output = np.full(len(frame), np.nan)
    valid = np.isfinite(y) & np.all(np.isfinite(x), axis=1)
    if valid.sum() > x.shape[1]:
        beta = np.linalg.lstsq(x[valid], y[valid], rcond=None)[0]
        output[valid] = y[valid] - np.einsum("ij,j->i", x[valid], beta, optimize=False)
    return output


def test_seed(
    patient: pd.DataFrame, seed: int, residual: bool, n_permutations: int
) -> pd.DataFrame:
    frame_seed = patient[patient.seed.eq(seed)].copy()
    labels = (
        frame_seed[["Patient", "Disease", "remission_binary"]]
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
            feature = frame_seed[
                frame_seed.cell_state.eq(state) & frame_seed.metric.eq(metric)
            ].copy()
            feature["value"] = residualize(feature) if residual else feature.topology_delta
            feature = feature[np.isfinite(feature.value)].copy()
            statistic = studentized_difference(
                feature.value.to_numpy(float), feature.remission_binary.to_numpy(np.int8)
            )
            directions = disease_directions(feature, "value")
            prepared.append((state, metric, feature, statistic, directions))
    null = np.empty((n_permutations, len(prepared)), dtype=np.float32)
    for column, (_, _, feature, _, _) in enumerate(prepared):
        indices = np.array(
            [patient_index[str(value)] for value in feature.Patient], dtype=int
        )
        null[:, column] = vectorized_studentized_difference(
            feature.value.to_numpy(float), permutations[:, indices]
        )
    null_abs = np.abs(null)
    null_max = np.nanmax(null_abs, axis=1)
    rows = []
    for column, (state, metric, feature, statistic, directions) in enumerate(prepared):
        sign = int(np.sign(statistic))
        consistent = all(
            np.isfinite(directions.get(disease, {}).get("mean_difference", math.nan))
            and int(np.sign(directions[disease]["mean_difference"])) == sign
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
                "cd_mean_difference": directions.get("CD", {}).get("mean_difference", math.nan),
                "uc_mean_difference": directions.get("UC", {}).get("mean_difference", math.nan),
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    args = parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)
    pair = pd.concat([build_pair_metrics(seed) for seed in SEEDS], ignore_index=True)
    patient = patient_aggregate(pair)
    eligibility_rows = []
    for (seed, state, metric), group in patient.groupby(
        ["seed", "cell_state", "metric"], sort=True
    ):
        disease_label_complete = all(
            set(
                group.loc[group.Disease.eq(disease), "remission_binary"].astype(int)
            )
            == {0, 1}
            for disease in ("CD", "UC")
        )
        eligibility_rows.append(
            {
                "seed": seed,
                "cell_state": state,
                "metric": metric,
                "n_patients": len(group),
                "n_remission": int(group.remission_binary.sum()),
                "n_nonremission": int((1 - group.remission_binary).sum()),
                "both_labels_in_each_disease": disease_label_complete,
                "estimable": bool(
                    group.remission_binary.nunique() == 2 and disease_label_complete
                ),
            }
        )
    eligibility = pd.DataFrame(eligibility_rows)
    eligibility.to_csv(args.outdir / "feature_eligibility.tsv", sep="\t", index=False)
    pair.to_csv(args.outdir / "pair_topology_metrics.tsv", sep="\t", index=False)
    patient.to_csv(args.outdir / "patient_topology_metrics.tsv", sep="\t", index=False)
    if eligibility.empty or not eligibility.estimable.any():
        empty_test = pd.DataFrame(
            columns=[
                "seed",
                "analysis",
                "cell_state",
                "metric",
                "n_patients",
                "studentized_effect",
                "raw_permutation_p",
                "max_t_fwer_p",
                "direction_consistent_cd_uc",
            ]
        )
        empty_test.to_csv(args.outdir / "topology_tests.tsv", sep="\t", index=False)
        pd.DataFrame(
            columns=["seed", "cell_state", "metric", "passes_seed"]
        ).to_csv(args.outdir / "seed_pass_matrix.tsv", sep="\t", index=False)
        summary = {
            "seeds": list(SEEDS),
            "cells_per_sample_compartment": N_CELLS,
            "n_pair_metric_rows": len(pair),
            "n_unique_patients": int(patient.Patient.nunique()),
            "n_remission_patients": int(
                patient.loc[patient.remission_binary.eq(1), "Patient"].nunique()
            ),
            "n_nonremission_patients": int(
                patient.loc[patient.remission_binary.eq(0), "Patient"].nunique()
            ),
            "n_test_features_estimable": 0,
            "stable_passing_features": [],
            "verdict": "TOPOLOGY_NOT_ESTIMABLE_AT_FROZEN_CELL_COUNT",
            "boundary": "Held anti-TNF IBD method context only; no outcome test was run and this is not an MS finding",
        }
        (args.outdir / "summary.json").write_text(
            json.dumps(summary, indent=2, sort_keys=True) + "\n"
        )
        report = f"""# V57 Paired Cell-State Topology Probe

## Fail-Closed Result

The frozen requirement of 150 cells in both samples of a paired compartment
left {patient.Patient.nunique()} unique patients, including
{summary['n_remission_patients']} remitting and
{summary['n_nonremission_patients']} non-remitting patients. Only one
compartment remained. A response association and CD/UC direction check are
therefore not identifiable, so no label permutation was run.

Verdict: **{summary['verdict']}**.

The cell threshold is not lowered after observing this imbalance. A future
topology test requires a paired, response-labelled cohort with enough cells in
both outcome groups and both diseases, preferably an MS cohort. This is a data
feasibility result, not a biological null.
"""
        (args.outdir / "REPORT.md").write_text(report)
        print(json.dumps(summary, indent=2, sort_keys=True))
        return
    tests = []
    for seed in SEEDS:
        tests.append(test_seed(patient, seed, False, args.permutations))
        tests.append(test_seed(patient, seed, True, args.permutations))
    test_frame = pd.concat(tests, ignore_index=True)
    wide = test_frame.pivot(
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
    stable = (
        wide.groupby(["cell_state", "metric"], as_index=False)
        .passes_seed.all()
        .query("passes_seed")
    )
    stable_features = [f"{row.cell_state}__{row.metric}" for row in stable.itertuples()]
    summary = {
        "seeds": list(SEEDS),
        "n_permutations_per_analysis_seed": args.permutations,
        "cells_per_sample_compartment": N_CELLS,
        "n_pair_metric_rows": len(pair),
        "n_unique_patients": int(patient.Patient.nunique()),
        "n_test_features": len(STATES) * len(METRICS),
        "stable_passing_features": stable_features,
        "verdict": "STABLE_RESPONSE_SPECIFIC_TOPOLOGY_SUPPORTED"
        if stable_features
        else "NO_STABLE_RESPONSE_SPECIFIC_TOPOLOGY",
        "boundary": "Held anti-TNF IBD method context only; not an MS finding or target result",
    }
    test_frame.to_csv(args.outdir / "topology_tests.tsv", sep="\t", index=False)
    wide.to_csv(args.outdir / "seed_pass_matrix.tsv", sep="\t", index=False)
    (args.outdir / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n"
    )
    top = test_frame.sort_values("max_t_fwer_p").iloc[0]
    report = f"""# V57 Paired Cell-State Topology Probe

## Boundary

This is a held anti-TNF IBD method-feasibility result, not an MS biological
finding.

## Result

- Patients: {patient.Patient.nunique()}
- Fixed cells per sample-compartment: {N_CELLS}
- Features in each max-T family: {len(STATES) * len(METRICS)}
- Label permutations per seed and analysis: {args.permutations:,}
- Best single seed/analysis feature: `{top.cell_state}__{top.metric}`
  (max-T p={top.max_t_fwer_p:.4f})
- Features passing every raw/residualized/disease/stability gate:
  {', '.join(stable_features) if stable_features else 'none'}

Verdict: **{summary['verdict']}**.

The bounded topology probe adds no response-specific state feature. Paired,
response-labelled MS single-cell trajectories would be required for an
MS-specific topological test.
"""
    (args.outdir / "REPORT.md").write_text(report)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
