#!/usr/bin/env python3
"""Outcome-blind energy/MMD shift diagnostics for held V22 cohorts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Callable

import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist

from v57_environment_stability_probe import load_data


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "analysis/v57_outcome_blind_shift"
FEATURES = ("delta_IFN_APC", "delta_HLAII", "delta_RECEPTOR")
SEED = 57041
N_PERMUTATIONS = 200_000
BATCH_SIZE = 5_000


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--seed", type=int, default=SEED)
    parser.add_argument("--permutations", type=int, default=N_PERMUTATIONS)
    return parser.parse_args()


def robust_scale(data: pd.DataFrame) -> tuple[np.ndarray, pd.DataFrame]:
    values = data.loc[:, FEATURES].to_numpy(float)
    if not np.all(np.isfinite(values)):
        raise ValueError("Shift features contain nonfinite values")
    median = np.median(values, axis=0)
    q25 = np.quantile(values, 0.25, axis=0)
    q75 = np.quantile(values, 0.75, axis=0)
    scale = q75 - q25
    scale = np.where(scale > 0, scale, 1.0)
    parameters = pd.DataFrame(
        {"feature": FEATURES, "median": median, "iqr": scale}
    )
    return (values - median) / scale, parameters


def energy_components(distance: np.ndarray, membership: np.ndarray) -> np.ndarray:
    group = membership.astype(np.float64, copy=False)
    other = 1.0 - group
    n_group = group.sum(axis=1)
    n_other = other.sum(axis=1)
    group_distance = np.einsum("bi,ij->bj", group, distance, optimize=False)
    within_group = np.sum(group_distance * group, axis=1) / (n_group * n_group)
    other_distance = np.einsum("bi,ij->bj", other, distance, optimize=False)
    within_other = np.sum(other_distance * other, axis=1) / (n_other * n_other)
    between = np.sum(group_distance * other, axis=1) / (n_group * n_other)
    return np.maximum(2.0 * between - within_group - within_other, 0.0)


def unbiased_mmd_components(kernel: np.ndarray, membership: np.ndarray) -> np.ndarray:
    group = membership.astype(np.float64, copy=False)
    other = 1.0 - group
    n_group = group.sum(axis=1)
    n_other = other.sum(axis=1)
    group_kernel = np.einsum("bi,ij->bj", group, kernel, optimize=False)
    other_kernel = np.einsum("bi,ij->bj", other, kernel, optimize=False)
    diagonal = np.diag(kernel)
    group_diagonal = np.einsum("bi,i->b", group, diagonal, optimize=False)
    other_diagonal = np.einsum("bi,i->b", other, diagonal, optimize=False)
    within_group = (np.sum(group_kernel * group, axis=1) - group_diagonal) / (
        n_group * (n_group - 1)
    )
    within_other = (np.sum(other_kernel * other, axis=1) - other_diagonal) / (
        n_other * (n_other - 1)
    )
    between = np.sum(group_kernel * other, axis=1) / (n_group * n_other)
    return within_group + within_other - 2.0 * between


def observed_statistics(
    matrix: np.ndarray,
    labels: np.ndarray,
    cohorts: list[str],
    statistic: Callable[[np.ndarray, np.ndarray], np.ndarray],
) -> np.ndarray:
    membership = np.column_stack([labels == cohort for cohort in cohorts]).T
    return np.array(
        [statistic(matrix, membership[index : index + 1])[0] for index in range(len(cohorts))]
    )


def permutation_family(
    matrix: np.ndarray,
    labels: np.ndarray,
    cohorts: list[str],
    observed: np.ndarray,
    statistic: Callable[[np.ndarray, np.ndarray], np.ndarray],
    rng: np.random.Generator,
    n_permutations: int,
) -> tuple[pd.DataFrame, dict[str, float]]:
    null = np.empty((n_permutations, len(cohorts)), dtype=np.float32)
    for start in range(0, n_permutations, BATCH_SIZE):
        stop = min(start + BATCH_SIZE, n_permutations)
        orders = np.argsort(
            rng.random((stop - start, len(labels)), dtype=np.float32), axis=1
        )
        permuted_labels = labels[orders]
        for index, cohort in enumerate(cohorts):
            membership = permuted_labels == cohort
            null[start:stop, index] = statistic(matrix, membership)
    null_max = np.max(null, axis=1)
    rows = []
    for index, cohort in enumerate(cohorts):
        rows.append(
            {
                "cohort": cohort,
                "n": int(np.sum(labels == cohort)),
                "statistic": float(observed[index]),
                "raw_permutation_p": float(
                    (1 + np.sum(null[:, index] >= observed[index])) / (n_permutations + 1)
                ),
                "max_stat_fwer_p": float(
                    (1 + np.sum(null_max >= observed[index])) / (n_permutations + 1)
                ),
            }
        )
    calibration = {
        "null_max_q90": float(np.quantile(null_max, 0.90)),
        "null_max_q95": float(np.quantile(null_max, 0.95)),
        "null_max_q99": float(np.quantile(null_max, 0.99)),
    }
    return pd.DataFrame(rows).sort_values("max_stat_fwer_p"), calibration


def main() -> None:
    args = parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)
    data = load_data().sort_values(["cohort", "patient"]).reset_index(drop=True)
    x, scale = robust_scale(data)
    labels = data.cohort.astype(str).to_numpy()
    cohorts = sorted(data.cohort.unique())
    distance = cdist(x, x, metric="euclidean")
    squared = cdist(x, x, metric="sqeuclidean")
    nonzero = squared[squared > 0]
    bandwidth_sq = float(np.median(nonzero)) if len(nonzero) else 1.0
    kernel = np.exp(-squared / (2.0 * bandwidth_sq))

    observed_energy = observed_statistics(distance, labels, cohorts, energy_components)
    observed_mmd = observed_statistics(kernel, labels, cohorts, unbiased_mmd_components)
    rng = np.random.default_rng(args.seed)
    energy, energy_null = permutation_family(
        distance,
        labels,
        cohorts,
        observed_energy,
        energy_components,
        rng,
        args.permutations,
    )
    mmd, mmd_null = permutation_family(
        kernel,
        labels,
        cohorts,
        observed_mmd,
        unbiased_mmd_components,
        rng,
        args.permutations,
    )
    energy = energy.rename(columns={"statistic": "energy_distance"})
    mmd = mmd.rename(
        columns={
            "statistic": "unbiased_mmd2",
            "raw_permutation_p": "mmd_raw_permutation_p",
            "max_stat_fwer_p": "mmd_max_stat_fwer_p",
        }
    )
    results = energy.merge(mmd, on=["cohort", "n"], validate="one_to_one")
    results["energy_ood_flag"] = results.max_stat_fwer_p.le(0.10)
    results["mmd_ood_flag"] = results.mmd_max_stat_fwer_p.le(0.10)
    results["concordant_ood_flag"] = results.energy_ood_flag & results.mmd_ood_flag

    summary = {
        "purpose": "Outcome-blind transport diagnostic; no biological finding or rule change",
        "plan": "docs/plans/V57_OUTCOME_BLIND_SHIFT_PLAN.md",
        "seed": args.seed,
        "n_permutations_per_family": args.permutations,
        "features": list(FEATURES),
        "n_subjects": len(data),
        "n_cohorts": len(cohorts),
        "rbf_bandwidth_squared": bandwidth_sq,
        "energy_null": energy_null,
        "mmd_null": mmd_null,
        "energy_ood_cohorts": results.loc[results.energy_ood_flag, "cohort"].tolist(),
        "mmd_ood_cohorts": results.loc[results.mmd_ood_flag, "cohort"].tolist(),
        "concordant_ood_cohorts": results.loc[results.concordant_ood_flag, "cohort"].tolist(),
    }
    scale.to_csv(args.outdir / "outcome_blind_scaling.tsv", sep="\t", index=False)
    results.to_csv(args.outdir / "cohort_shift_tests.tsv", sep="\t", index=False)
    (args.outdir / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    rows = [
        "# V57 Outcome-Blind Cohort-Shift Preflight",
        "",
        "This diagnostic uses no response labels. It does not alter the frozen",
        "score or validation thresholds and is not a biological finding.",
        "",
        "| Cohort | n | Energy | Energy FWER p | MMD2 | MMD FWER p | Concordant OOD |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for item in results.itertuples(index=False):
        rows.append(
            f"| `{item.cohort}` | {item.n} | {item.energy_distance:.3f} | "
            f"{item.max_stat_fwer_p:.4f} | {item.unbiased_mmd2:.3f} | "
            f"{item.mmd_max_stat_fwer_p:.4f} | {item.concordant_ood_flag} |"
        )
    rows.extend(
        [
            "",
            "A flag means source-distribution transport is unsafe to assume; it",
            "does not explain, invalidate, or rescue an outcome association. The",
            "same outcome-blind diagnostic can be run before labels are opened in",
            "a future eligible validation cohort.",
        ]
    )
    (args.outdir / "REPORT.md").write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
