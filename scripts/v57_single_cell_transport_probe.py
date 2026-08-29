#!/usr/bin/env python3
"""Donor-level Wasserstein probe of paired GSE282122 myeloid cell states."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

import anndata as ad
import numpy as np
import pandas as pd
from scipy import sparse, stats

from v3_wave67_gse282122_myeloid_pseudobulk import EXPANDED_MODULES


ROOT = Path(__file__).resolve().parents[1]
H5AD = ROOT / "data/raw_v3/wave67_gse282122_myeloid/myeloid_final.h5ad"
PAIRS = ROOT / "phases/v3/results/wave67_gse282122_myeloid_pseudobulk/paired_module_deltas.tsv"
DEFAULT_OUT = ROOT / "analysis/v57_single_cell_transport"
MODULES = (
    "ifn_apc",
    "hla_ii_apc",
    "mif_cd74_receptor_state",
    "lysosomal_apc",
    "inflammatory_nfkb",
)
STATES = ("DC", "Mono_macro")
MIN_CELLS = 50
SEED = 57011
N_PERMUTATIONS = 200_000


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--seed", type=int, default=SEED)
    parser.add_argument("--permutations", type=int, default=N_PERMUTATIONS)
    return parser.parse_args()


def gene_symbols(adata: ad.AnnData) -> pd.Series:
    if "gene_symbol" in adata.var:
        return adata.var["gene_symbol"].astype(str)
    return pd.Series(adata.var_names.astype(str), index=adata.var_names)


def load_cell_scores() -> tuple[pd.DataFrame, dict[str, np.ndarray], dict[str, list[str]]]:
    adata = ad.read_h5ad(H5AD, backed="r")
    symbols = gene_symbols(adata)
    first_index: dict[str, int] = {}
    for index, symbol in enumerate(symbols):
        first_index.setdefault(symbol.upper(), index)
    present_by_module: dict[str, list[str]] = {}
    wanted: list[str] = []
    for module in MODULES:
        present = [gene for gene in EXPANDED_MODULES[module] if gene.upper() in first_index]
        if len(present) < math.ceil(len(EXPANDED_MODULES[module]) / 2):
            raise ValueError(f"Module coverage below 50%: {module} {len(present)}")
        present_by_module[module] = present
        wanted.extend(present)
    unique_genes = sorted(set(wanted))
    indices = [first_index[gene.upper()] for gene in unique_genes]
    selected = adata.X[:, indices]
    if sparse.issparse(selected):
        selected = selected.toarray()
    else:
        selected = np.asarray(selected)
    obs = adata.obs.reset_index(names="cell_id").copy()
    adata.file.close()
    total = pd.to_numeric(obs["total_counts"], errors="coerce").to_numpy(float)
    total = np.where(total > 0, total, np.nan)
    normalized = np.log1p(selected.astype(np.float64) / total[:, None] * 10_000.0)
    gene_column = {gene: index for index, gene in enumerate(unique_genes)}
    module_scores = {
        module: np.nanmean(normalized[:, [gene_column[gene] for gene in genes]], axis=1)
        for module, genes in present_by_module.items()
    }
    obs["log_total_counts"] = np.log1p(total)
    return obs, module_scores, present_by_module


def eligible_pairs() -> pd.DataFrame:
    pairs = pd.read_csv(PAIRS, sep="\t")
    pairs = pairs[
        pairs.state_level.eq("major")
        & pairs.cell_state.isin(STATES)
        & pairs.module.eq("ifn_apc")
        & pairs.passes_cell_threshold.astype(bool)
        & pairs.pre_batch.eq(pairs.post_batch)
        & pairs.pre_n_cells.ge(MIN_CELLS)
        & pairs.post_n_cells.ge(MIN_CELLS)
    ].copy()
    if pairs.pair_id.duplicated().any():
        raise ValueError("Pair contract has duplicate major-state pair IDs")
    return pairs


def transport_rows(
    obs: pd.DataFrame,
    scores: dict[str, np.ndarray],
    pairs: pd.DataFrame,
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    sample = obs["sample_id"].astype(str).to_numpy()
    state = obs["major"].astype(str).to_numpy()
    depth = obs["log_total_counts"].to_numpy(float)
    for pair in pairs.itertuples(index=False):
        pre_index = np.flatnonzero((sample == str(pair.pre_sample_id)) & (state == pair.cell_state))
        post_index = np.flatnonzero((sample == str(pair.post_sample_id)) & (state == pair.cell_state))
        if len(pre_index) < MIN_CELLS or len(post_index) < MIN_CELLS:
            continue
        pre_depth = depth[pre_index]
        post_depth = depth[post_index]
        technical_centered = stats.wasserstein_distance(
            pre_depth - np.nanmedian(pre_depth), post_depth - np.nanmedian(post_depth)
        )
        for module in MODULES:
            pre = scores[module][pre_index]
            post = scores[module][post_index]
            pre = pre[np.isfinite(pre)]
            post = post[np.isfinite(post)]
            rows.append(
                {
                    "Patient": pair.Patient,
                    "Disease": pair.Disease,
                    "Site": pair.Site,
                    "Remission_status": pair.Remission_status,
                    "cell_state": pair.cell_state,
                    "module": module,
                    "pre_sample_id": pair.pre_sample_id,
                    "post_sample_id": pair.post_sample_id,
                    "n_pre_cells": len(pre),
                    "n_post_cells": len(post),
                    "wasserstein_total": stats.wasserstein_distance(pre, post),
                    "wasserstein_centered": stats.wasserstein_distance(
                        pre - np.median(pre), post - np.median(post)
                    ),
                    "mean_shift_post_minus_pre": float(np.mean(post) - np.mean(pre)),
                    "abs_mean_shift": float(abs(np.mean(post) - np.mean(pre))),
                    "technical_depth_wasserstein_centered": float(technical_centered),
                    "abs_inflammation_score_change": float(
                        abs(pair.post_inflammation_score - pair.baseline_inflammation_score)
                    ),
                    "pair_id": pair.pair_id,
                }
            )
    return pd.DataFrame(rows)


def patient_aggregate(pair_rows: pd.DataFrame) -> pd.DataFrame:
    value_columns = [
        "wasserstein_total",
        "wasserstein_centered",
        "abs_mean_shift",
        "technical_depth_wasserstein_centered",
        "abs_inflammation_score_change",
    ]
    patient = (
        pair_rows.groupby(
            ["Patient", "Disease", "Remission_status", "cell_state", "module"],
            as_index=False,
        )[value_columns]
        .median()
    )
    patient["remission_binary"] = patient.Remission_status.eq("Remission").astype(np.int8)
    patient["feature"] = patient.cell_state + "__" + patient.module
    return patient


def studentized_difference(values: np.ndarray, labels: np.ndarray) -> float:
    positive = values[labels == 1]
    negative = values[labels == 0]
    if len(positive) < 3 or len(negative) < 3:
        return math.nan
    variance = np.var(positive, ddof=1) / len(positive) + np.var(negative, ddof=1) / len(negative)
    if variance <= 0 or not np.isfinite(variance):
        return 0.0
    return float((np.mean(positive) - np.mean(negative)) / math.sqrt(variance))


def residualize(frame: pd.DataFrame) -> np.ndarray:
    y = frame.wasserstein_centered.to_numpy(float)
    disease = frame.Disease.eq("UC").to_numpy(float)
    x = np.column_stack(
        [
            np.ones(len(frame)),
            disease,
            frame.technical_depth_wasserstein_centered.to_numpy(float),
            frame.abs_mean_shift.to_numpy(float),
            frame.abs_inflammation_score_change.to_numpy(float),
        ]
    )
    valid = np.all(np.isfinite(x), axis=1) & np.isfinite(y)
    residuals = np.full(len(frame), np.nan)
    if valid.sum() > x.shape[1]:
        beta = np.linalg.lstsq(x[valid], y[valid], rcond=None)[0]
        residuals[valid] = y[valid] - x[valid] @ beta
    return residuals


def disease_directions(frame: pd.DataFrame, value_column: str) -> dict[str, Any]:
    directions: dict[str, Any] = {}
    for disease, sub in frame.groupby("Disease"):
        positive = sub.loc[sub.remission_binary.eq(1), value_column].dropna().to_numpy(float)
        negative = sub.loc[sub.remission_binary.eq(0), value_column].dropna().to_numpy(float)
        directions[disease] = {
            "n_remission": len(positive),
            "n_nonremission": len(negative),
            "mean_difference": float(np.mean(positive) - np.mean(negative))
            if len(positive) and len(negative)
            else math.nan,
        }
    return directions


def make_feature_frames(patient: pd.DataFrame, residual: bool) -> list[dict[str, Any]]:
    frames: list[dict[str, Any]] = []
    for feature in [f"{state}__{module}" for state in STATES for module in MODULES]:
        frame = patient[patient.feature.eq(feature)].copy()
        if residual:
            frame["test_value"] = residualize(frame)
        else:
            frame["test_value"] = frame.wasserstein_centered
        frame = frame[np.isfinite(frame.test_value)].copy()
        if frame.remission_binary.value_counts().min() < 3:
            continue
        frames.append({"feature": feature, "frame": frame})
    return frames


def stratified_permutation_matrix(
    patient_labels: pd.DataFrame,
    rng: np.random.Generator,
    n_permutations: int,
) -> np.ndarray:
    """Draw label assignments uniformly within disease strata."""
    matrix = np.zeros((n_permutations, len(patient_labels)), dtype=np.int8)
    for _, frame in patient_labels.groupby("Disease", sort=True):
        indices = frame.index.to_numpy(dtype=int)
        n_positive = int(frame.remission_binary.sum())
        if n_positive == 0 or n_positive == len(frame):
            matrix[:, indices] = frame.remission_binary.to_numpy(np.int8)
            continue
        random_order = rng.random((n_permutations, len(indices)), dtype=np.float32)
        selected = np.argpartition(random_order, n_positive - 1, axis=1)[:, :n_positive]
        matrix[np.arange(n_permutations)[:, None], indices[selected]] = 1
    return matrix


def vectorized_studentized_difference(values: np.ndarray, labels: np.ndarray) -> np.ndarray:
    """Compute Welch-style statistics for many label rows at once."""
    values = values.astype(np.float64, copy=False)
    labels_float = labels.astype(np.float64, copy=False)
    n1 = labels_float.sum(axis=1)
    n0 = len(values) - n1
    # NumPy's BLAS matmul path emitted spurious overflow warnings for these
    # small finite arrays on the project macOS runtime. An explicit contraction
    # is deterministic here and avoids that platform-specific numerical path.
    sum1 = np.einsum("ij,j->i", labels_float, values, optimize=False)
    sumsq1 = np.einsum("ij,j->i", labels_float, values * values, optimize=False)
    total = float(values.sum())
    total_sq = float(np.sum(values * values))
    sum0 = total - sum1
    sumsq0 = total_sq - sumsq1
    with np.errstate(divide="ignore", invalid="ignore"):
        mean1 = sum1 / n1
        mean0 = sum0 / n0
        var1 = (sumsq1 - sum1 * sum1 / n1) / (n1 - 1)
        var0 = (sumsq0 - sum0 * sum0 / n0) / (n0 - 1)
        denominator = np.sqrt(np.maximum(var1, 0) / n1 + np.maximum(var0, 0) / n0)
        statistic = (mean1 - mean0) / denominator
    invalid = (n1 < 3) | (n0 < 3) | ~np.isfinite(statistic) | (denominator <= 0)
    statistic[invalid] = np.nan
    return statistic


def max_t_tests(
    patient: pd.DataFrame,
    residual: bool,
    rng: np.random.Generator,
    n_permutations: int,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    feature_frames = make_feature_frames(patient, residual=residual)
    patient_labels = (
        patient[["Patient", "Disease", "remission_binary"]]
        .drop_duplicates()
        .sort_values(["Disease", "Patient"])
        .reset_index(drop=True)
    )
    if patient_labels.Patient.duplicated().any():
        raise ValueError("Patient response/disease labels are inconsistent")
    patient_index = {str(patient): index for index, patient in enumerate(patient_labels.Patient)}
    observed = []
    for item in feature_frames:
        frame = item["frame"]
        statistic = studentized_difference(
            frame.test_value.to_numpy(float), frame.remission_binary.to_numpy(np.int8)
        )
        directions = disease_directions(frame.rename(columns={"test_value": "value"}), "value")
        observed.append((item["feature"], statistic, directions, frame))

    permuted_labels = stratified_permutation_matrix(patient_labels, rng, n_permutations)
    null = np.empty((n_permutations, len(observed)), dtype=np.float32)
    for feature_index, (_, _, _, frame) in enumerate(observed):
        indices = np.array([patient_index[str(patient)] for patient in frame.Patient], dtype=int)
        null[:, feature_index] = vectorized_studentized_difference(
            frame.test_value.to_numpy(float), permuted_labels[:, indices]
        )
    null_abs = np.abs(null)
    null_max = np.nanmax(null_abs, axis=1)
    rows: list[dict[str, Any]] = []
    for feature_index, (feature, statistic, directions, frame) in enumerate(observed):
        raw_p = (1 + int(np.sum(null_abs[:, feature_index] >= abs(statistic)))) / (
            n_permutations + 1
        )
        fwer_p = (1 + int(np.sum(null_max >= abs(statistic)))) / (n_permutations + 1)
        pooled_direction = int(np.sign(statistic))
        direction_values = [
            item["mean_difference"]
            for item in directions.values()
            if np.isfinite(item["mean_difference"])
        ]
        direction_consistent = bool(
            len(direction_values) == 2
            and all(int(np.sign(value)) == pooled_direction for value in direction_values)
        )
        rows.append(
            {
                "feature": feature,
                "n_patients": len(frame),
                "n_remission": int(frame.remission_binary.sum()),
                "n_nonremission": int((1 - frame.remission_binary).sum()),
                "studentized_remission_minus_nonremission": statistic,
                "raw_permutation_p": raw_p,
                "max_t_fwer_p": fwer_p,
                "cd_mean_difference": directions.get("CD", {}).get("mean_difference", math.nan),
                "uc_mean_difference": directions.get("UC", {}).get("mean_difference", math.nan),
                "direction_consistent_cd_uc": direction_consistent,
            }
        )
    summary = {
        "n_features": len(rows),
        "null_max_abs_t_q90": float(np.quantile(null_max, 0.90)),
        "null_max_abs_t_q95": float(np.quantile(null_max, 0.95)),
        "null_max_abs_t_q99": float(np.quantile(null_max, 0.99)),
    }
    return pd.DataFrame(rows).sort_values("max_t_fwer_p"), summary


def report(
    outdir: Path,
    raw_tests: pd.DataFrame,
    residual_tests: pd.DataFrame,
    summary: dict[str, Any],
) -> None:
    top = raw_tests.iloc[0] if len(raw_tests) else None
    lines = [
        "# V57 Paired Single-Cell Distribution Transport",
        "",
        "This donor-level IBD analysis tests method behavior and cross-disease context.",
        "It is not evidence for an MS biomarker, mechanism, target, or treatment.",
        "",
        f"- Eligible site-state pairs: `{summary['n_eligible_pair_state_rows']}`.",
        f"- Patient-state-module rows: `{summary['n_patient_state_module_rows']}`.",
        f"- Primary family size: `{summary['raw_null']['n_features']}`.",
    ]
    if top is not None:
        lines.extend(
            [
                f"- Best raw centered-transport feature: `{top.feature}` "
                f"(max-T p=`{top.max_t_fwer_p:.6f}`).",
                f"- Frozen verdict: **{summary['verdict']}**.",
            ]
        )
    lines.extend(
        [
            "",
            "A feature could advance only if raw and nuisance-residualized max-T tests",
            "both passed and CD/UC directions agreed. Total cell-level sample size does",
            "not replace the patient as the inferential unit.",
        ]
    )
    (outdir / "REPORT.md").write_text("\n".join(lines) + "\n")


def main() -> int:
    args = parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(args.seed)
    pairs = eligible_pairs()
    obs, scores, present = load_cell_scores()
    pair_rows = transport_rows(obs, scores, pairs)
    pair_rows.to_csv(args.outdir / "pair_transport_metrics.tsv", sep="\t", index=False)
    patient = patient_aggregate(pair_rows)
    patient.to_csv(args.outdir / "patient_transport_metrics.tsv", sep="\t", index=False)
    raw_tests, raw_null = max_t_tests(patient, False, rng, args.permutations)
    residual_tests, residual_null = max_t_tests(patient, True, rng, args.permutations)
    raw_tests.to_csv(args.outdir / "centered_transport_tests.tsv", sep="\t", index=False)
    residual_tests.to_csv(args.outdir / "residualized_centered_transport_tests.tsv", sep="\t", index=False)
    merged = raw_tests[["feature", "max_t_fwer_p", "direction_consistent_cd_uc"]].merge(
        residual_tests[["feature", "max_t_fwer_p"]],
        on="feature",
        suffixes=("_raw", "_residualized"),
    )
    passes = merged[
        merged.max_t_fwer_p_raw.le(0.10)
        & merged.max_t_fwer_p_residualized.le(0.10)
        & merged.direction_consistent_cd_uc
    ]
    summary = {
        "purpose": "V57 distribution-method probe; no MS biological claim",
        "plan": "docs/plans/V57_SINGLE_CELL_TRANSPORT_PLAN.md",
        "seed": args.seed,
        "n_permutations": args.permutations,
        "min_cells_per_side": MIN_CELLS,
        "modules": list(MODULES),
        "states": list(STATES),
        "module_genes_present": present,
        "n_eligible_pair_state_rows": int(len(pairs)),
        "n_pair_state_module_rows": int(len(pair_rows)),
        "n_patients": int(patient.Patient.nunique()),
        "n_patient_state_module_rows": int(len(patient)),
        "raw_null": raw_null,
        "residualized_null": residual_null,
        "passing_features": passes.feature.tolist(),
        "verdict": "DISTRIBUTIONAL_FEATURE_FOR_REPLICATION"
        if len(passes)
        else "NO_RESPONSE_SPECIFIC_DISTRIBUTIONAL_FEATURE",
    }
    (args.outdir / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    report(args.outdir, raw_tests, residual_tests, summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
