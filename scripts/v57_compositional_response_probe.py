#!/usr/bin/env python3
"""Patient-level CLR analysis of paired GSE282122 myeloid composition."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

import anndata as ad
import numpy as np
import pandas as pd

from v57_single_cell_transport_probe import (
    disease_directions,
    stratified_permutation_matrix,
    studentized_difference,
    vectorized_studentized_difference,
)


ROOT = Path(__file__).resolve().parents[1]
H5AD = ROOT / "data/raw_v3/wave67_gse282122_myeloid/myeloid_final.h5ad"
PAIRS = ROOT / "phases/v3/results/wave67_gse282122_myeloid_pseudobulk/paired_module_deltas.tsv"
DEFAULT_OUT = ROOT / "analysis/v57_compositional_response"
MIN_CELLS = 100
PSEUDOCOUNT = 0.5
SEED = 57021
N_PERMUTATIONS = 200_000


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--seed", type=int, default=SEED)
    parser.add_argument("--permutations", type=int, default=N_PERMUTATIONS)
    return parser.parse_args()


def load_counts() -> tuple[pd.DataFrame, list[str]]:
    adata = ad.read_h5ad(H5AD, backed="r")
    obs = adata.obs[
        ["sample_id", "Patient", "Disease", "Site", "Remission_status", "final_analysis"]
    ].reset_index(drop=True)
    adata.file.close()
    obs = obs.dropna(subset=["sample_id", "final_analysis"]).copy()
    obs["sample_id"] = obs.sample_id.astype(str)
    obs["final_analysis"] = obs.final_analysis.astype(str)
    categories = sorted(obs.final_analysis.unique().tolist())
    counts = (
        obs.groupby(["sample_id", "final_analysis"], observed=True)
        .size()
        .unstack(fill_value=0)
        .reindex(columns=categories, fill_value=0)
    )
    counts.columns.name = None
    counts["total_myeloid_cells"] = counts.sum(axis=1)
    counts = counts.reset_index()
    return counts, categories


def load_pair_contract() -> pd.DataFrame:
    pairs = pd.read_csv(PAIRS, sep="\t")
    pairs = pairs[
        pairs.state_level.eq("major")
        & pairs.module.eq("ifn_apc")
        & pairs.pre_batch.eq(pairs.post_batch)
    ].copy()
    columns = [
        "Patient",
        "Disease",
        "Site",
        "Remission_status",
        "pre_sample_id",
        "post_sample_id",
        "pre_batch",
        "post_batch",
        "baseline_inflammation_score",
        "post_inflammation_score",
    ]
    identity = ["Patient", "Disease", "Site", "pre_sample_id", "post_sample_id"]
    pairs = pairs[columns].copy()
    categorical = ["Remission_status", "pre_batch", "post_batch"]
    if (pairs.groupby(identity)[categorical].nunique().max(axis=1) > 1).any():
        raise ValueError("Categorical pair metadata are inconsistent across major-state rows")
    score_range = pairs.groupby(identity)[
        ["baseline_inflammation_score", "post_inflammation_score"]
    ].agg(lambda values: values.max() - values.min())
    if score_range.to_numpy().max() > 1e-10:
        raise ValueError("Inflammation scores are inconsistent across major-state rows")
    pairs = (
        pairs.groupby(identity, as_index=False)
        .agg(
            Remission_status=("Remission_status", "first"),
            pre_batch=("pre_batch", "first"),
            post_batch=("post_batch", "first"),
            baseline_inflammation_score=("baseline_inflammation_score", "mean"),
            post_inflammation_score=("post_inflammation_score", "mean"),
        )
        .reset_index(drop=True)
    )
    pairs["pair_id"] = (
        pairs.Patient.astype(str)
        + "|"
        + pairs.Disease.astype(str)
        + "|"
        + pairs.Site.astype(str)
    )
    return pairs


def clr(values: np.ndarray) -> np.ndarray:
    logged = np.log(values.astype(np.float64) + PSEUDOCOUNT)
    return logged - np.mean(logged)


def build_pair_changes(
    counts: pd.DataFrame, categories: list[str], pairs: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:
    by_sample = counts.set_index("sample_id")
    pair_meta: list[dict[str, Any]] = []
    changes: list[dict[str, Any]] = []
    for pair in pairs.itertuples(index=False):
        if pair.pre_sample_id not in by_sample.index or pair.post_sample_id not in by_sample.index:
            continue
        pre_row = by_sample.loc[pair.pre_sample_id]
        post_row = by_sample.loc[pair.post_sample_id]
        pre_total = int(pre_row.total_myeloid_cells)
        post_total = int(post_row.total_myeloid_cells)
        if pre_total < MIN_CELLS or post_total < MIN_CELLS:
            continue
        pre_clr = clr(pre_row[categories].to_numpy(float))
        post_clr = clr(post_row[categories].to_numpy(float))
        inflammation_change = abs(
            float(pair.post_inflammation_score) - float(pair.baseline_inflammation_score)
        )
        pair_meta.append(
            {
                "pair_id": pair.pair_id,
                "Patient": pair.Patient,
                "Disease": pair.Disease,
                "Site": pair.Site,
                "Remission_status": pair.Remission_status,
                "pre_sample_id": pair.pre_sample_id,
                "post_sample_id": pair.post_sample_id,
                "pre_batch": pair.pre_batch,
                "post_batch": pair.post_batch,
                "pre_total_myeloid_cells": pre_total,
                "post_total_myeloid_cells": post_total,
                "log_post_pre_cell_count_ratio": math.log(post_total / pre_total),
                "abs_inflammation_score_change": inflammation_change,
            }
        )
        for index, category in enumerate(categories):
            changes.append(
                {
                    "pair_id": pair.pair_id,
                    "Patient": pair.Patient,
                    "Disease": pair.Disease,
                    "Site": pair.Site,
                    "Remission_status": pair.Remission_status,
                    "category": category,
                    "pre_count": int(pre_row[category]),
                    "post_count": int(post_row[category]),
                    "pre_clr": float(pre_clr[index]),
                    "post_clr": float(post_clr[index]),
                    "delta_clr_post_minus_pre": float(post_clr[index] - pre_clr[index]),
                    "log_post_pre_cell_count_ratio": math.log(post_total / pre_total),
                    "abs_inflammation_score_change": inflammation_change,
                }
            )
    return pd.DataFrame(pair_meta), pd.DataFrame(changes)


def patient_aggregate(pair_changes: pd.DataFrame) -> pd.DataFrame:
    values = [
        "pre_clr",
        "post_clr",
        "delta_clr_post_minus_pre",
        "log_post_pre_cell_count_ratio",
        "abs_inflammation_score_change",
    ]
    patient = (
        pair_changes.groupby(
            ["Patient", "Disease", "Remission_status", "category"], as_index=False
        )[values]
        .median()
    )
    patient["remission_binary"] = patient.Remission_status.eq("Remission").astype(np.int8)
    return patient


def residualize(frame: pd.DataFrame) -> np.ndarray:
    y = frame.delta_clr_post_minus_pre.to_numpy(float)
    x = np.column_stack(
        [
            np.ones(len(frame)),
            frame.Disease.eq("UC").to_numpy(float),
            frame.log_post_pre_cell_count_ratio.to_numpy(float),
            frame.abs_inflammation_score_change.to_numpy(float),
            frame.pre_clr.to_numpy(float),
        ]
    )
    valid = np.isfinite(y) & np.all(np.isfinite(x), axis=1)
    residuals = np.full(len(frame), np.nan)
    if valid.sum() > x.shape[1]:
        beta = np.linalg.lstsq(x[valid], y[valid], rcond=None)[0]
        residuals[valid] = y[valid] - x[valid] @ beta
    return residuals


def max_t_tests(
    patient: pd.DataFrame,
    categories: list[str],
    residual: bool,
    rng: np.random.Generator,
    n_permutations: int,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    labels = (
        patient[["Patient", "Disease", "remission_binary"]]
        .drop_duplicates()
        .sort_values(["Disease", "Patient"])
        .reset_index(drop=True)
    )
    if labels.Patient.duplicated().any():
        raise ValueError("Patient labels or diseases are inconsistent")
    patient_index = {str(value): index for index, value in enumerate(labels.Patient)}
    permuted = stratified_permutation_matrix(labels, rng, n_permutations)

    prepared: list[tuple[str, pd.DataFrame, float, dict[str, Any]]] = []
    for category in categories:
        frame = patient[patient.category.eq(category)].copy()
        frame["test_value"] = residualize(frame) if residual else frame.delta_clr_post_minus_pre
        frame = frame[np.isfinite(frame.test_value)].copy()
        if frame.remission_binary.value_counts().min() < 3:
            continue
        statistic = studentized_difference(
            frame.test_value.to_numpy(float), frame.remission_binary.to_numpy(np.int8)
        )
        directions = disease_directions(frame.rename(columns={"test_value": "value"}), "value")
        prepared.append((category, frame, statistic, directions))

    null = np.empty((n_permutations, len(prepared)), dtype=np.float32)
    for category_index, (_, frame, _, _) in enumerate(prepared):
        indices = np.array([patient_index[str(value)] for value in frame.Patient], dtype=int)
        null[:, category_index] = vectorized_studentized_difference(
            frame.test_value.to_numpy(float), permuted[:, indices]
        )
    null_abs = np.abs(null)
    null_max = np.nanmax(null_abs, axis=1)

    rows: list[dict[str, Any]] = []
    for category_index, (category, frame, statistic, directions) in enumerate(prepared):
        raw_p = (1 + int(np.sum(null_abs[:, category_index] >= abs(statistic)))) / (
            n_permutations + 1
        )
        max_t_p = (1 + int(np.sum(null_max >= abs(statistic)))) / (n_permutations + 1)
        pooled_sign = int(np.sign(statistic))
        estimable = []
        matching = []
        for disease in ("CD", "UC"):
            item = directions.get(disease, {})
            direction = item.get("mean_difference", math.nan)
            is_estimable = bool(np.isfinite(direction))
            estimable.append(is_estimable)
            matching.append(is_estimable and int(np.sign(direction)) == pooled_sign)
        rows.append(
            {
                "category": category,
                "analysis": "residualized" if residual else "raw",
                "n_patients": len(frame),
                "n_remission": int(frame.remission_binary.sum()),
                "n_nonremission": int((1 - frame.remission_binary).sum()),
                "studentized_effect": statistic,
                "raw_permutation_p": raw_p,
                "max_t_fwer_p": max_t_p,
                "direction_consistent_cd_uc": bool(all(estimable) and all(matching)),
                "cd_mean_difference": directions.get("CD", {}).get("mean_difference", math.nan),
                "uc_mean_difference": directions.get("UC", {}).get("mean_difference", math.nan),
            }
        )
    result = pd.DataFrame(rows).sort_values(["max_t_fwer_p", "raw_permutation_p"])
    calibration = {
        "null_max_q90": float(np.nanquantile(null_max, 0.90)),
        "null_max_q95": float(np.nanquantile(null_max, 0.95)),
        "null_max_q99": float(np.nanquantile(null_max, 0.99)),
    }
    return result, calibration


def write_report(
    outdir: Path,
    pair_meta: pd.DataFrame,
    patient: pd.DataFrame,
    raw: pd.DataFrame,
    adjusted: pd.DataFrame,
    summary: dict[str, Any],
) -> None:
    top_raw = raw.iloc[0]
    top_adjusted = adjusted.iloc[0]
    report = f"""# V57 Paired Myeloid Composition Probe

## Boundary

This is a method-feasibility result from paired IBD single-cell data. It is
not an MS biological finding and does not validate or modify the V22 rule.

## Design

- Eligible same-batch pre/post sample pairs: {len(pair_meta)}
- Unique patients: {patient.Patient.nunique()}
- Myeloid categories in the frozen CLR family: {patient.category.nunique()}
- Minimum cells per sample: {MIN_CELLS}
- Pseudocount: {PSEUDOCOUNT}
- Disease-stratified patient-label permutations: {summary['n_permutations']:,}
- Family control: maximum absolute studentized statistic

## Result

No category passed the predeclared joint raw, residualized, and cross-disease
gate. The top raw category was `{top_raw.category}` (studentized effect
{top_raw.studentized_effect:.3f}, max-T p={top_raw.max_t_fwer_p:.4f}). The top
residualized category was `{top_adjusted.category}` (studentized effect
{top_adjusted.studentized_effect:.3f}, max-T p={top_adjusted.max_t_fwer_p:.4f}).

Verdict: **{summary['verdict']}**.

## Interpretation

Within this held IBD cohort, a formal closed-composition analysis does not
support a reproducible response-associated redistribution of annotated
myeloid subtypes under the strict gate. This does not prove that composition
is irrelevant in MS; it shows that this particular cross-disease dataset
does not supply the missing evidence. A decisive test requires paired,
response-labelled MS single-cell data.
"""
    (outdir / "REPORT.md").write_text(report, encoding="utf-8")


def main() -> None:
    args = parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(args.seed)

    counts, categories = load_counts()
    pairs = load_pair_contract()
    pair_meta, pair_changes = build_pair_changes(counts, categories, pairs)
    patient = patient_aggregate(pair_changes)
    raw, raw_calibration = max_t_tests(
        patient, categories, residual=False, rng=rng, n_permutations=args.permutations
    )
    adjusted, adjusted_calibration = max_t_tests(
        patient, categories, residual=True, rng=rng, n_permutations=args.permutations
    )

    merged = raw.merge(
        adjusted,
        on="category",
        suffixes=("_raw", "_residualized"),
        validate="one_to_one",
    )
    same_sign = np.sign(merged.studentized_effect_raw) == np.sign(
        merged.studentized_effect_residualized
    )
    passing = merged[
        merged.max_t_fwer_p_raw.le(0.10)
        & merged.max_t_fwer_p_residualized.le(0.10)
        & same_sign
        & merged.direction_consistent_cd_uc_raw
        & merged.direction_consistent_cd_uc_residualized
    ].category.tolist()
    summary = {
        "input": str(H5AD.relative_to(ROOT)),
        "pair_contract": str(PAIRS.relative_to(ROOT)),
        "seed": args.seed,
        "n_permutations": args.permutations,
        "minimum_cells_per_sample": MIN_CELLS,
        "pseudocount": PSEUDOCOUNT,
        "n_eligible_pairs": len(pair_meta),
        "n_unique_patients": int(patient.Patient.nunique()),
        "n_categories": len(categories),
        "categories": categories,
        "raw_null_calibration": raw_calibration,
        "residualized_null_calibration": adjusted_calibration,
        "passing_categories": passing,
        "verdict": "RESPONSE_SPECIFIC_COMPOSITION_SUPPORTED"
        if passing
        else "NO_RESPONSE_SPECIFIC_COMPOSITION",
        "boundary": "IBD method context only; not an MS biological finding",
    }

    pair_meta.to_csv(args.outdir / "eligible_pairs.tsv", sep="\t", index=False)
    pair_changes.to_csv(args.outdir / "pair_category_clr_changes.tsv", sep="\t", index=False)
    patient.to_csv(args.outdir / "patient_category_clr_changes.tsv", sep="\t", index=False)
    raw.to_csv(args.outdir / "raw_composition_tests.tsv", sep="\t", index=False)
    adjusted.to_csv(args.outdir / "residualized_composition_tests.tsv", sep="\t", index=False)
    (args.outdir / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    write_report(args.outdir, pair_meta, patient, raw, adjusted, summary)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
