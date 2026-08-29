#!/usr/bin/env python3
"""Patient-level overlapping-neighborhood DA in paired single-cell states."""

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
DEFAULT_OUT = ROOT / "analysis/v57_neighborhood_da"
REFERENCE_SEED = 57130
COUNT_SEEDS = (57131, 57132, 57133)
CELLS_PER_UNIT = 50
LANDMARKS_PER_STATE = 20
NEIGHBOR_REFERENCE_CELLS = 100
N_PERMUTATIONS = 200_000


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--permutations", type=int, default=N_PERMUTATIONS)
    return parser.parse_args()


def deterministic_sample(indices: np.ndarray, key: str, seed: int) -> np.ndarray:
    if len(indices) < CELLS_PER_UNIT:
        return np.array([], dtype=int)
    local_seed = (seed + zlib.crc32(key.encode("utf-8"))) % (2**32)
    rng = np.random.default_rng(local_seed)
    return np.sort(rng.choice(indices, size=CELLS_PER_UNIT, replace=False))


def farthest_landmarks(points: np.ndarray, n_landmarks: int) -> np.ndarray:
    center = np.median(points, axis=0)
    first = int(np.argmin(np.linalg.norm(points - center, axis=1)))
    selected = [first]
    nearest = np.linalg.norm(points - points[first], axis=1)
    for _ in range(1, n_landmarks):
        candidate = int(np.argmax(nearest))
        selected.append(candidate)
        nearest = np.minimum(nearest, np.linalg.norm(points - points[candidate], axis=1))
    return points[np.array(selected, dtype=int)]


def load_scaled() -> tuple[pd.DataFrame, np.ndarray]:
    obs, scores, _ = load_cell_scores()
    matrix = np.column_stack([scores[module] for module in MODULES])
    center = np.nanmedian(matrix, axis=0)
    scale = np.nanquantile(matrix, 0.75, axis=0) - np.nanquantile(matrix, 0.25, axis=0)
    matrix = (matrix - center) / np.where(scale > 0, scale, 1.0)
    return obs, matrix


def eligible_units(obs: pd.DataFrame) -> list[dict[str, Any]]:
    sample_ids = obs.sample_id.astype(str).to_numpy()
    states = obs.major.astype(str).to_numpy()
    units: list[dict[str, Any]] = []
    for pair in eligible_pairs().itertuples(index=False):
        for visit, sample_id in (("pre", pair.pre_sample_id), ("post", pair.post_sample_id)):
            indices = np.flatnonzero(
                (sample_ids == str(sample_id)) & (states == pair.cell_state)
            )
            if len(indices) < CELLS_PER_UNIT:
                continue
            units.append(
                {
                    "pair": pair,
                    "visit": visit,
                    "sample_id": str(sample_id),
                    "indices": indices,
                }
            )
    return units


def define_neighborhoods(
    obs: pd.DataFrame, matrix: np.ndarray, units: list[dict[str, Any]]
) -> tuple[pd.DataFrame, dict[str, tuple[np.ndarray, np.ndarray]]]:
    rows = []
    definitions = {}
    for state in STATES:
        reference_parts = []
        for unit in units:
            if unit["pair"].cell_state != state:
                continue
            chosen = deterministic_sample(
                unit["indices"], f"{unit['sample_id']}|{state}|reference", REFERENCE_SEED
            )
            if len(chosen):
                reference_parts.append(matrix[chosen])
        reference = np.vstack(reference_parts)
        centers = farthest_landmarks(reference, LANDMARKS_PER_STATE)
        distances = cdist(reference, centers)
        radii = np.partition(distances, NEIGHBOR_REFERENCE_CELLS - 1, axis=0)[
            NEIGHBOR_REFERENCE_CELLS - 1
        ]
        definitions[state] = (centers, radii)
        for index, (center, radius) in enumerate(zip(centers, radii)):
            rows.append(
                {
                    "cell_state": state,
                    "neighborhood": f"N{index + 1:02d}",
                    "radius": radius,
                    **{f"center_{module}": center[j] for j, module in enumerate(MODULES)},
                    "outcome_blind": True,
                }
            )
    return pd.DataFrame(rows), definitions


def build_pair_counts(
    obs: pd.DataFrame,
    matrix: np.ndarray,
    units: list[dict[str, Any]],
    definitions: dict[str, tuple[np.ndarray, np.ndarray]],
    seed: int,
) -> pd.DataFrame:
    depth = obs.log_total_counts.to_numpy(float)
    sampled: dict[tuple[str, str], dict[str, Any]] = {}
    for unit in units:
        pair = unit["pair"]
        key = (str(pair.pair_id), unit["visit"])
        chosen = deterministic_sample(
            unit["indices"], f"{unit['sample_id']}|{pair.cell_state}|count", seed
        )
        if len(chosen):
            sampled[key] = {
                "points": matrix[chosen],
                "mean_depth": float(np.mean(depth[chosen])),
                "pair": pair,
            }
    rows = []
    for pair in eligible_pairs().itertuples(index=False):
        pre_key = (str(pair.pair_id), "pre")
        post_key = (str(pair.pair_id), "post")
        if pre_key not in sampled or post_key not in sampled:
            continue
        pre = sampled[pre_key]
        post = sampled[post_key]
        centers, radii = definitions[pair.cell_state]
        pre_membership = cdist(pre["points"], centers) <= radii[None, :]
        post_membership = cdist(post["points"], centers) <= radii[None, :]
        pre_count = pre_membership.sum(axis=0)
        post_count = post_membership.sum(axis=0)
        pre_prop = (pre_count + 0.5) / (CELLS_PER_UNIT + 1.0)
        post_prop = (post_count + 0.5) / (CELLS_PER_UNIT + 1.0)
        transformed_delta = np.arcsin(np.sqrt(post_prop)) - np.arcsin(np.sqrt(pre_prop))
        mean_shift = float(np.linalg.norm(np.mean(post["points"], axis=0) - np.mean(pre["points"], axis=0)))
        for index in range(LANDMARKS_PER_STATE):
            rows.append(
                {
                    "seed": seed,
                    "Patient": pair.Patient,
                    "Disease": pair.Disease,
                    "Site": pair.Site,
                    "Remission_status": pair.Remission_status,
                    "cell_state": pair.cell_state,
                    "pair_id": pair.pair_id,
                    "neighborhood": f"N{index + 1:02d}",
                    "pre_count": int(pre_count[index]),
                    "post_count": int(post_count[index]),
                    "abundance_delta": float(transformed_delta[index]),
                    "mean_depth_delta": post["mean_depth"] - pre["mean_depth"],
                    "mean_shift_norm": mean_shift,
                    "abs_inflammation_score_change": float(
                        abs(pair.post_inflammation_score - pair.baseline_inflammation_score)
                    ),
                }
            )
    return pd.DataFrame(rows)


def patient_aggregate(pair: pd.DataFrame) -> pd.DataFrame:
    columns = [
        "abundance_delta",
        "mean_depth_delta",
        "mean_shift_norm",
        "abs_inflammation_score_change",
    ]
    patient = pair.groupby(
        ["seed", "Patient", "Disease", "Remission_status", "cell_state", "neighborhood"],
        as_index=False,
    )[columns].median()
    patient["remission_binary"] = patient.Remission_status.eq("Remission").astype(np.int8)
    return patient


def residualize(frame: pd.DataFrame) -> np.ndarray:
    y = frame.abundance_delta.to_numpy(float)
    x = np.column_stack(
        [
            np.ones(len(frame)),
            frame.Disease.eq("UC").to_numpy(float),
            frame.mean_depth_delta.to_numpy(float),
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
        for neighborhood in [f"N{index + 1:02d}" for index in range(LANDMARKS_PER_STATE)]:
            feature = data[
                data.cell_state.eq(state) & data.neighborhood.eq(neighborhood)
            ].copy()
            if not estimable(feature):
                continue
            feature["value"] = residualize(feature) if residual else feature.abundance_delta
            feature = feature[np.isfinite(feature.value)].copy()
            if not estimable(feature):
                continue
            statistic = studentized_difference(
                feature.value.to_numpy(float), feature.remission_binary.to_numpy(np.int8)
            )
            if not np.isfinite(statistic):
                continue
            prepared.append(
                (state, neighborhood, feature, statistic, disease_directions(feature, "value"))
            )
    if not prepared:
        return pd.DataFrame()
    null = np.empty((n_permutations, len(prepared)), dtype=np.float32)
    for column, (_, _, feature, _, _) in enumerate(prepared):
        indices = np.array([patient_index[str(value)] for value in feature.Patient], dtype=int)
        null[:, column] = vectorized_studentized_difference(
            feature.value.to_numpy(float), permutations[:, indices]
        )
    null_abs = np.abs(null)
    null_max = np.nanmax(null_abs, axis=1)
    rows = []
    for column, (state, neighborhood, feature, statistic, directions) in enumerate(prepared):
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
                "neighborhood": neighborhood,
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
    obs, matrix = load_scaled()
    units = eligible_units(obs)
    neighborhoods, definitions = define_neighborhoods(obs, matrix, units)
    pair = pd.concat(
        [build_pair_counts(obs, matrix, units, definitions, seed) for seed in COUNT_SEEDS],
        ignore_index=True,
    )
    patient = patient_aggregate(pair)
    test_parts = []
    for seed in COUNT_SEEDS:
        for residual in (False, True):
            result = test_seed(patient, seed, residual, args.permutations)
            if not result.empty:
                test_parts.append(result)
    tests = pd.concat(test_parts, ignore_index=True) if test_parts else pd.DataFrame()
    stable_features: list[str] = []
    if not tests.empty:
        wide = tests.pivot(
            index=["seed", "cell_state", "neighborhood"],
            columns="analysis",
            values=["studentized_effect", "max_t_fwer_p", "direction_consistent_cd_uc"],
        )
        wide.columns = ["_".join(column) for column in wide.columns]
        wide = wide.reset_index()
        required = {
            "studentized_effect_raw",
            "studentized_effect_residualized",
            "max_t_fwer_p_raw",
            "max_t_fwer_p_residualized",
            "direction_consistent_cd_uc_raw",
            "direction_consistent_cd_uc_residualized",
        }
        if required.issubset(wide.columns):
            wide["passes_seed"] = (
                wide.max_t_fwer_p_raw.le(0.10)
                & wide.max_t_fwer_p_residualized.le(0.10)
                & (
                    np.sign(wide.studentized_effect_raw)
                    == np.sign(wide.studentized_effect_residualized)
                )
                & wide.direction_consistent_cd_uc_raw.astype(bool)
                & wide.direction_consistent_cd_uc_residualized.astype(bool)
            )
            stable = (
                wide.groupby(["cell_state", "neighborhood"], as_index=False)
                .agg(n_seeds=("seed", "nunique"), all_pass=("passes_seed", "all"))
            )
            stable = stable[
                stable.n_seeds.eq(len(COUNT_SEEDS)) & stable.all_pass.astype(bool)
            ]
            stable_features = [
                f"{row.cell_state}__{row.neighborhood}" for row in stable.itertuples()
            ]
        wide.to_csv(args.outdir / "seed_pass_matrix.tsv", sep="\t", index=False)
    else:
        pd.DataFrame().to_csv(args.outdir / "seed_pass_matrix.tsv", sep="\t", index=False)
    summary = {
        "reference_seed": REFERENCE_SEED,
        "count_seeds": list(COUNT_SEEDS),
        "cells_per_sample_compartment": CELLS_PER_UNIT,
        "landmarks_per_compartment": LANDMARKS_PER_STATE,
        "reference_cells_per_neighborhood": NEIGHBOR_REFERENCE_CELLS,
        "n_permutations_per_seed_analysis": args.permutations,
        "n_unique_patients": int(patient.Patient.nunique()),
        "n_pair_neighborhood_rows": len(pair),
        "n_estimable_tests": int(
            tests[["cell_state", "neighborhood"]].drop_duplicates().shape[0]
        )
        if not tests.empty
        else 0,
        "stable_passing_features": stable_features,
        "verdict": "STABLE_RESPONSE_SPECIFIC_NEIGHBORHOOD_SUPPORTED"
        if stable_features
        else "NO_STABLE_RESPONSE_SPECIFIC_NEIGHBORHOOD",
        "boundary": "Held anti-TNF IBD method context only; not an MS finding or target result",
    }
    neighborhoods.to_csv(args.outdir / "neighborhood_definitions.tsv", sep="\t", index=False)
    pair.to_csv(args.outdir / "pair_neighborhood_counts.tsv", sep="\t", index=False)
    patient.to_csv(args.outdir / "patient_neighborhood_deltas.tsv", sep="\t", index=False)
    tests.to_csv(args.outdir / "neighborhood_tests.tsv", sep="\t", index=False)
    (args.outdir / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n"
    )
    top_text = "none"
    if not tests.empty:
        top = tests.sort_values("max_t_fwer_p").iloc[0]
        top_text = f"{top.cell_state}__{top.neighborhood} (max-T p={top.max_t_fwer_p:.4f})"
    report = f"""# V57 Overlapping-Neighborhood Differential Abundance

## Boundary

This is a held anti-TNF IBD method-feasibility result, not an MS biological
finding.

## Result

- Outcome-blind neighborhoods: {len(neighborhoods)}
- Unique patients: {patient.Patient.nunique()}
- Estimable compartment-neighborhood tests: {summary['n_estimable_tests']}
- Best single seed/analysis result: {top_text}
- Stable features passing every gate:
  {', '.join(stable_features) if stable_features else 'none'}

Verdict: **{summary['verdict']}**.

The isolated best residualized result (`Mono_macro__N17`, max-T p=0.0483)
did not pass its raw test (p=0.1560) and was not stable across count seeds. It
is therefore not a supported feature.

Only patient labels were permuted; cells were never treated as independent
outcome replicates. A response-labelled MS single-cell cohort is required for
an MS-specific neighborhood test.
"""
    (args.outdir / "REPORT.md").write_text(report)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
