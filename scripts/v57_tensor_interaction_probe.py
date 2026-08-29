#!/usr/bin/env python3
"""LOPO HOSVD-versus-additive response prediction on a held paired tensor."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Callable

import numpy as np
import pandas as pd

from v57_single_cell_transport_probe import stratified_permutation_matrix


ROOT = Path(__file__).resolve().parents[1]
PAIRS = ROOT / "phases/v3/results/wave67_gse282122_myeloid_pseudobulk/paired_module_deltas.tsv"
DEFAULT_OUT = ROOT / "analysis/v57_tensor_interaction"
STATES = ("DC", "Mono_macro")
SEED = 57071
N_PERMUTATIONS = 200_000
RIDGE = 1.0
BATCH_SIZE = 5_000


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--seed", type=int, default=SEED)
    parser.add_argument("--permutations", type=int, default=N_PERMUTATIONS)
    return parser.parse_args()


def load_tensor() -> tuple[np.ndarray, pd.DataFrame, list[str]]:
    data = pd.read_csv(PAIRS, sep="\t")
    data = data[
        data.state_level.eq("major")
        & data.cell_state.isin(STATES)
        & data.passes_cell_threshold.astype(bool)
        & data.pre_batch.eq(data.post_batch)
    ].copy()
    patient = (
        data.groupby(
            ["Patient", "Disease", "Remission_status", "cell_state", "module"],
            as_index=False,
        ).delta_post_minus_pre.median()
    )
    modules = sorted(patient.module.unique())
    wide = patient.pivot_table(
        index=["Patient", "Disease", "Remission_status"],
        columns=["cell_state", "module"],
        values="delta_post_minus_pre",
    )
    expected = pd.MultiIndex.from_product([STATES, modules], names=["cell_state", "module"])
    wide = wide.reindex(columns=expected).dropna().sort_index()
    metadata = wide.index.to_frame(index=False)
    metadata["response_binary"] = metadata.Remission_status.eq("Remission").astype(np.int8)
    tensor = wide.to_numpy(float).reshape(len(wide), len(STATES), len(modules))
    if not np.all(np.isfinite(tensor)):
        raise ValueError("Complete tensor contains nonfinite values")
    return tensor, metadata, modules


def additive_features(tensor: np.ndarray) -> np.ndarray:
    grand = np.mean(tensor, axis=(1, 2))[:, None]
    state = (np.mean(tensor[:, 0, :], axis=1) - np.mean(tensor[:, 1, :], axis=1))[:, None]
    module_mean = np.mean(tensor, axis=1)
    module_contrast = module_mean[:, :-1] - module_mean[:, -1, None]
    return np.column_stack([grand, state, module_contrast])


def tensor_features(train: np.ndarray, held: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    state_covariance = np.einsum("nsm,ntm->st", train, train, optimize=False)
    module_covariance = np.einsum("nsm,nsq->mq", train, train, optimize=False)
    _, state_vectors = np.linalg.eigh(state_covariance)
    _, module_vectors = np.linalg.eigh(module_covariance)
    state_basis = state_vectors[:, -2:]
    module_basis = module_vectors[:, -2:]
    train_core = np.einsum(
        "nsm,sa,mb->nab", train, state_basis, module_basis, optimize=False
    ).reshape(len(train), -1)
    held_core = np.einsum(
        "nsm,sa,mb->nab", held, state_basis, module_basis, optimize=False
    ).reshape(len(held), -1)
    return train_core, held_core


def ridge_prediction_coefficients(train: np.ndarray, held: np.ndarray) -> np.ndarray:
    mean = np.mean(train, axis=0)
    scale = np.std(train, axis=0, ddof=0)
    scale = np.where(scale > 1e-12, scale, 1.0)
    train_scaled = (train - mean) / scale
    held_scaled = (held - mean) / scale
    design = np.column_stack([np.ones(len(train)), train_scaled])
    held_design = np.concatenate([[1.0], held_scaled[0]])
    penalty = np.eye(design.shape[1]) * RIDGE
    penalty[0, 0] = 0.0
    inverse = np.linalg.inv(
        np.einsum("ni,nj->ij", design, design, optimize=False) + penalty
    )
    return np.einsum(
        "i,ij,nj->n", held_design, inverse, design, optimize=False
    )


def coefficient_matrix(
    tensor: np.ndarray,
    feature_builder: Callable[[np.ndarray, np.ndarray], tuple[np.ndarray, np.ndarray]],
) -> np.ndarray:
    n = len(tensor)
    coefficients = np.zeros((n, n), dtype=np.float64)
    for held_index in range(n):
        train_index = np.arange(n) != held_index
        train = tensor[train_index]
        held = tensor[held_index : held_index + 1]
        center = np.mean(train, axis=0)
        scale = np.std(train, axis=0, ddof=0)
        scale = np.where(scale > 1e-12, scale, 1.0)
        train_standardized = (train - center) / scale
        held_standardized = (held - center) / scale
        train_features, held_features = feature_builder(
            train_standardized, held_standardized
        )
        coefficients[held_index, train_index] = ridge_prediction_coefficients(
            train_features, held_features
        )
    return coefficients


def additive_builder(train: np.ndarray, held: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    return additive_features(train), additive_features(held)


def weighted_within_disease_auc(
    labels: np.ndarray, scores: np.ndarray, diseases: np.ndarray
) -> np.ndarray:
    result = np.zeros(len(labels), dtype=np.float64)
    total = len(diseases)
    for disease in sorted(np.unique(diseases)):
        index = np.flatnonzero(diseases == disease)
        y = labels[:, index]
        value = scores[:, index]
        positive = y[:, :, None]
        negative = 1.0 - y[:, None, :]
        greater = value[:, :, None] > value[:, None, :]
        equal = value[:, :, None] == value[:, None, :]
        numerator = np.sum(positive * negative * (greater + 0.5 * equal), axis=(1, 2))
        denominator = np.sum(y, axis=1) * np.sum(1.0 - y, axis=1)
        result += len(index) / total * numerator / denominator
    return result


def null_auc(
    coefficients: np.ndarray,
    permuted_labels: np.ndarray,
    diseases: np.ndarray,
) -> np.ndarray:
    output = np.empty(len(permuted_labels), dtype=np.float64)
    for start in range(0, len(permuted_labels), BATCH_SIZE):
        stop = min(start + BATCH_SIZE, len(permuted_labels))
        labels = permuted_labels[start:stop].astype(np.float64)
        scores = np.einsum("ij,bj->bi", coefficients, labels, optimize=False)
        output[start:stop] = weighted_within_disease_auc(labels, scores, diseases)
    return output


def disease_auc(labels: np.ndarray, scores: np.ndarray, diseases: np.ndarray) -> dict[str, float]:
    output = {}
    for disease in sorted(np.unique(diseases)):
        index = diseases == disease
        output[disease] = float(
            weighted_within_disease_auc(
                labels[None, index], scores[None, index], diseases[index]
            )[0]
        )
    return output


def main() -> None:
    args = parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)
    tensor, metadata, modules = load_tensor()
    additive = coefficient_matrix(tensor, additive_builder)
    hosvd = coefficient_matrix(tensor, tensor_features)
    observed_label = metadata.response_binary.to_numpy(np.int8)
    diseases = metadata.Disease.astype(str).to_numpy()
    observed_additive_score = np.einsum(
        "ij,j->i", additive, observed_label.astype(float), optimize=False
    )
    observed_tensor_score = np.einsum(
        "ij,j->i", hosvd, observed_label.astype(float), optimize=False
    )
    observed_additive_auc = float(
        weighted_within_disease_auc(
            observed_label[None, :], observed_additive_score[None, :], diseases
        )[0]
    )
    observed_tensor_auc = float(
        weighted_within_disease_auc(
            observed_label[None, :], observed_tensor_score[None, :], diseases
        )[0]
    )

    label_frame = metadata[["Patient", "Disease", "response_binary"]].rename(
        columns={"response_binary": "remission_binary"}
    )
    label_frame = label_frame.reset_index(drop=True)
    rng = np.random.default_rng(args.seed)
    permuted = stratified_permutation_matrix(label_frame, rng, args.permutations)
    null_additive = null_auc(additive, permuted, diseases)
    null_tensor = null_auc(hosvd, permuted, diseases)
    observed_gain = observed_tensor_auc - observed_additive_auc
    null_gain = null_tensor - null_additive
    null_max = np.maximum(null_additive, null_tensor)
    tensor_fwer_p = float(
        (1 + np.sum(null_max >= observed_tensor_auc)) / (args.permutations + 1)
    )
    gain_p = float(
        (1 + np.sum(null_gain >= observed_gain)) / (args.permutations + 1)
    )
    directions = disease_auc(observed_label, observed_tensor_score, diseases)
    passes = bool(
        observed_tensor_auc >= 0.65
        and tensor_fwer_p <= 0.05
        and observed_gain >= 0.05
        and gain_p <= 0.05
        and all(value > 0.5 for value in directions.values())
    )
    prediction = metadata.copy()
    prediction["additive_lopo_score"] = observed_additive_score
    prediction["tensor_hosvd_lopo_score"] = observed_tensor_score
    summary = {
        "purpose": "IBD method probe only; no MS biological claim",
        "plan": "docs/plans/V57_TENSOR_INTERACTION_PLAN.md",
        "seed": args.seed,
        "n_permutations": args.permutations,
        "n_patients": len(metadata),
        "states": list(STATES),
        "modules": modules,
        "additive_weighted_within_disease_auc": observed_additive_auc,
        "tensor_weighted_within_disease_auc": observed_tensor_auc,
        "tensor_minus_additive_auc": observed_gain,
        "tensor_max_model_fwer_p": tensor_fwer_p,
        "tensor_gain_permutation_p": gain_p,
        "tensor_disease_specific_auc": directions,
        "promotion_gate": passes,
        "verdict": "TENSOR_INTERACTION_WORTH_DEDICATED_RUN"
        if passes
        else "NO_REPRODUCIBLE_TENSOR_GAIN",
    }
    prediction.to_csv(args.outdir / "lopo_predictions.tsv", sep="\t", index=False)
    pd.DataFrame(additive).to_csv(
        args.outdir / "additive_prediction_coefficients.tsv", sep="\t", index=False
    )
    pd.DataFrame(hosvd).to_csv(
        args.outdir / "tensor_prediction_coefficients.tsv", sep="\t", index=False
    )
    pd.DataFrame(
        {
            "null_additive_auc": null_additive,
            "null_tensor_auc": null_tensor,
            "null_tensor_minus_additive_auc": null_gain,
        }
    ).to_csv(
        args.outdir / "null_auc.tsv.gz",
        sep="\t",
        index=False,
        compression={"method": "gzip", "mtime": 0},
    )
    (args.outdir / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    report = f"""# V57 Donor-State-Module Tensor Probe

## Boundary

This is a patient-level method probe in paired IBD data, not an MS finding.

## Result

- Complete patients: {len(metadata)}
- Tensor: {len(metadata)} x {len(STATES)} states x {len(modules)} modules
- Additive weighted within-disease LOPO AUC: {observed_additive_auc:.3f}
- Tensor HOSVD weighted within-disease LOPO AUC: {observed_tensor_auc:.3f}
- Tensor-minus-additive AUC: {observed_gain:.3f}
- Tensor max-model FWER p: {tensor_fwer_p:.4f}
- Tensor-gain permutation p: {gain_p:.4f}
- Disease-specific tensor AUC: {directions}

Verdict: **{summary['verdict']}**.

The complete donor, decomposition, and ridge fit is held out patient by
patient and rerun under disease-stratified labels. A failed gate means low-rank
multiway compression does not recover a reproducible response interaction in
this held tensor; it does not rule out such interactions in MS-specific data.
"""
    (args.outdir / "REPORT.md").write_text(report, encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
