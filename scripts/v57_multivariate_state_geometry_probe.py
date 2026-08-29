#!/usr/bin/env python3
"""Patient-level multivariate energy-distance probe in paired single cells."""

from __future__ import annotations

import argparse
import json
import math
import zlib
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
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
DEFAULT_OUT = ROOT / "analysis/v57_multivariate_state_geometry"
MAX_CELLS = 200
SEED = 57031
N_PERMUTATIONS = 200_000


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--seed", type=int, default=SEED)
    parser.add_argument("--permutations", type=int, default=N_PERMUTATIONS)
    return parser.parse_args()


def energy_distance(x: np.ndarray, y: np.ndarray) -> float:
    between = cdist(x, y, metric="euclidean").mean()
    within_x = cdist(x, x, metric="euclidean").mean()
    within_y = cdist(y, y, metric="euclidean").mean()
    value = 2.0 * between - within_x - within_y
    return float(max(value, 0.0))


def deterministic_subsample(indices: np.ndarray, key: str, seed: int) -> np.ndarray:
    if len(indices) <= MAX_CELLS:
        return indices
    local_seed = (seed + zlib.crc32(key.encode("utf-8"))) % (2**32)
    rng = np.random.default_rng(local_seed)
    return np.sort(rng.choice(indices, size=MAX_CELLS, replace=False))


def pair_metrics(seed: int) -> tuple[pd.DataFrame, dict[str, list[str]]]:
    obs, scores, genes = load_cell_scores()
    score_matrix = np.column_stack([scores[module] for module in MODULES])
    median = np.nanmedian(score_matrix, axis=0)
    q25 = np.nanquantile(score_matrix, 0.25, axis=0)
    q75 = np.nanquantile(score_matrix, 0.75, axis=0)
    scale = q75 - q25
    scale = np.where(scale > 0, scale, 1.0)
    score_matrix = (score_matrix - median) / scale

    sample = obs.sample_id.astype(str).to_numpy()
    state = obs.major.astype(str).to_numpy()
    depth = obs.log_total_counts.to_numpy(float)
    rows: list[dict[str, Any]] = []
    for pair in eligible_pairs().itertuples(index=False):
        pre = np.flatnonzero((sample == str(pair.pre_sample_id)) & (state == pair.cell_state))
        post = np.flatnonzero((sample == str(pair.post_sample_id)) & (state == pair.cell_state))
        pre = deterministic_subsample(pre, f"{pair.pair_id}|pre", seed)
        post = deterministic_subsample(post, f"{pair.pair_id}|post", seed)
        if len(pre) < 50 or len(post) < 50:
            continue
        x = score_matrix[pre]
        y = score_matrix[post]
        valid_x = np.all(np.isfinite(x), axis=1)
        valid_y = np.all(np.isfinite(y), axis=1)
        x = x[valid_x]
        y = y[valid_y]
        if len(x) < 50 or len(y) < 50:
            continue
        x_centered = x - np.median(x, axis=0)
        y_centered = y - np.median(y, axis=0)
        pre_depth = depth[pre][valid_x]
        post_depth = depth[post][valid_y]
        technical = energy_distance(
            (pre_depth - np.median(pre_depth))[:, None],
            (post_depth - np.median(post_depth))[:, None],
        )
        rows.append(
            {
                "Patient": pair.Patient,
                "Disease": pair.Disease,
                "Site": pair.Site,
                "Remission_status": pair.Remission_status,
                "cell_state": pair.cell_state,
                "pair_id": pair.pair_id,
                "n_pre_cells": len(x),
                "n_post_cells": len(y),
                "energy_total": energy_distance(x, y),
                "energy_centered": energy_distance(x_centered, y_centered),
                "mean_shift_norm": float(np.linalg.norm(np.mean(y, axis=0) - np.mean(x, axis=0))),
                "technical_depth_energy_centered": technical,
                "abs_inflammation_score_change": float(
                    abs(pair.post_inflammation_score - pair.baseline_inflammation_score)
                ),
            }
        )
    return pd.DataFrame(rows), genes


def patient_aggregate(pairs: pd.DataFrame) -> pd.DataFrame:
    columns = [
        "energy_total",
        "energy_centered",
        "mean_shift_norm",
        "technical_depth_energy_centered",
        "abs_inflammation_score_change",
    ]
    patient = (
        pairs.groupby(
            ["Patient", "Disease", "Remission_status", "cell_state"], as_index=False
        )[columns]
        .median()
    )
    patient["remission_binary"] = patient.Remission_status.eq("Remission").astype(np.int8)
    return patient


def residualize(frame: pd.DataFrame) -> np.ndarray:
    y = frame.energy_centered.to_numpy(float)
    x = np.column_stack(
        [
            np.ones(len(frame)),
            frame.Disease.eq("UC").to_numpy(float),
            frame.technical_depth_energy_centered.to_numpy(float),
            frame.mean_shift_norm.to_numpy(float),
            frame.abs_inflammation_score_change.to_numpy(float),
        ]
    )
    valid = np.isfinite(y) & np.all(np.isfinite(x), axis=1)
    output = np.full(len(frame), np.nan)
    if valid.sum() > x.shape[1]:
        beta = np.linalg.lstsq(x[valid], y[valid], rcond=None)[0]
        output[valid] = y[valid] - x[valid] @ beta
    return output


def max_t_test(
    patient: pd.DataFrame,
    residual: bool,
    rng: np.random.Generator,
    n_permutations: int,
) -> tuple[pd.DataFrame, dict[str, float]]:
    labels = (
        patient[["Patient", "Disease", "remission_binary"]]
        .drop_duplicates()
        .sort_values(["Disease", "Patient"])
        .reset_index(drop=True)
    )
    if labels.Patient.duplicated().any():
        raise ValueError("Patient labels are inconsistent")
    patient_index = {str(value): index for index, value in enumerate(labels.Patient)}
    permuted = stratified_permutation_matrix(labels, rng, n_permutations)
    prepared = []
    for state in STATES:
        frame = patient[patient.cell_state.eq(state)].copy()
        frame["test_value"] = residualize(frame) if residual else frame.energy_centered
        frame = frame[np.isfinite(frame.test_value)].copy()
        statistic = studentized_difference(
            frame.test_value.to_numpy(float), frame.remission_binary.to_numpy(np.int8)
        )
        directions = disease_directions(frame.rename(columns={"test_value": "value"}), "value")
        prepared.append((state, frame, statistic, directions))

    null = np.empty((n_permutations, len(prepared)), dtype=np.float32)
    for index, (_, frame, _, _) in enumerate(prepared):
        patient_indices = np.array(
            [patient_index[str(value)] for value in frame.Patient], dtype=int
        )
        null[:, index] = vectorized_studentized_difference(
            frame.test_value.to_numpy(float), permuted[:, patient_indices]
        )
    null_abs = np.abs(null)
    null_max = np.nanmax(null_abs, axis=1)
    rows = []
    for index, (state, frame, statistic, directions) in enumerate(prepared):
        pooled_sign = int(np.sign(statistic))
        disease_matches = []
        for disease in ("CD", "UC"):
            direction = directions.get(disease, {}).get("mean_difference", math.nan)
            disease_matches.append(
                bool(np.isfinite(direction) and int(np.sign(direction)) == pooled_sign)
            )
        rows.append(
            {
                "cell_state": state,
                "analysis": "residualized" if residual else "raw",
                "n_patients": len(frame),
                "n_remission": int(frame.remission_binary.sum()),
                "n_nonremission": int((1 - frame.remission_binary).sum()),
                "studentized_effect": statistic,
                "raw_permutation_p": (
                    1 + int(np.sum(null_abs[:, index] >= abs(statistic)))
                )
                / (n_permutations + 1),
                "max_t_fwer_p": (1 + int(np.sum(null_max >= abs(statistic))))
                / (n_permutations + 1),
                "direction_consistent_cd_uc": bool(all(disease_matches)),
                "cd_mean_difference": directions.get("CD", {}).get("mean_difference", math.nan),
                "uc_mean_difference": directions.get("UC", {}).get("mean_difference", math.nan),
            }
        )
    result = pd.DataFrame(rows).sort_values("max_t_fwer_p")
    calibration = {
        "null_max_q90": float(np.nanquantile(null_max, 0.90)),
        "null_max_q95": float(np.nanquantile(null_max, 0.95)),
        "null_max_q99": float(np.nanquantile(null_max, 0.99)),
    }
    return result, calibration


def main() -> None:
    args = parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)
    pair, genes = pair_metrics(args.seed)
    patient = patient_aggregate(pair)
    rng = np.random.default_rng(args.seed)
    raw, raw_null = max_t_test(patient, False, rng, args.permutations)
    adjusted, adjusted_null = max_t_test(patient, True, rng, args.permutations)
    merged = raw.merge(adjusted, on="cell_state", suffixes=("_raw", "_residualized"))
    passing = merged[
        merged.max_t_fwer_p_raw.le(0.10)
        & merged.max_t_fwer_p_residualized.le(0.10)
        & (
            np.sign(merged.studentized_effect_raw)
            == np.sign(merged.studentized_effect_residualized)
        )
        & merged.direction_consistent_cd_uc_raw
        & merged.direction_consistent_cd_uc_residualized
    ].cell_state.tolist()
    summary = {
        "seed": args.seed,
        "n_permutations": args.permutations,
        "max_cells_per_sample_state": MAX_CELLS,
        "n_pair_state_rows": len(pair),
        "n_patient_state_rows": len(patient),
        "n_patients": int(patient.Patient.nunique()),
        "modules": list(MODULES),
        "module_genes_present": genes,
        "raw_null": raw_null,
        "residualized_null": adjusted_null,
        "passing_states": passing,
        "verdict": "RESPONSE_SPECIFIC_JOINT_GEOMETRY_SUPPORTED"
        if passing
        else "NO_RESPONSE_SPECIFIC_JOINT_GEOMETRY",
        "boundary": "IBD method context only; not an MS biological finding",
    }
    pair.to_csv(
        args.outdir / "pair_state_energy_metrics.tsv", sep="\t", index=False, na_rep="NA"
    )
    patient.to_csv(
        args.outdir / "patient_state_energy_metrics.tsv", sep="\t", index=False, na_rep="NA"
    )
    raw.to_csv(args.outdir / "raw_state_tests.tsv", sep="\t", index=False, na_rep="NA")
    adjusted.to_csv(
        args.outdir / "residualized_state_tests.tsv", sep="\t", index=False, na_rep="NA"
    )
    (args.outdir / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    top_raw = raw.iloc[0]
    top_adjusted = adjusted.iloc[0]
    report = f"""# V57 Multivariate Cell-State Geometry Probe

## Boundary

This is a method-feasibility result from paired IBD single-cell data, not an
MS biological finding.

## Result

- Eligible pair-compartment rows: {len(pair)}
- Unique patients: {patient.Patient.nunique()}
- Patient-label permutations: {args.permutations:,}
- Top raw compartment: `{top_raw.cell_state}` (effect
  {top_raw.studentized_effect:.3f}, max-T p={top_raw.max_t_fwer_p:.4f})
- Top residualized compartment: `{top_adjusted.cell_state}` (effect
  {top_adjusted.studentized_effect:.3f}, max-T p={top_adjusted.max_t_fwer_p:.4f})
- Passing compartments: {', '.join(passing) if passing else 'none'}

Verdict: **{summary['verdict']}**.

The test does not establish a response-specific change in joint module-shape
geometry after technical, mean-shift, inflammation, family, and disease-
direction gates. This closes the bounded held-data probe; paired MS response
single-cell data would be required for an MS-specific test.
"""
    (args.outdir / "REPORT.md").write_text(report, encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
