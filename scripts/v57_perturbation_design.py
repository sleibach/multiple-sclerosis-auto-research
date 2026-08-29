#!/usr/bin/env python3
"""Synthetic comparison of D-optimal and random combinatorial screen designs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import rankdata


N_TARGETS = 24
N_DESCRIPTORS = 6
N_PAIRS = 36
N_REPLICATES = 1_000
SEEDS = (5731, 5732, 5733)
REGIMES = ("descriptor_aligned", "mixed", "idiosyncratic")
RIDGE = 1.0


def pair_features(descriptors: np.ndarray) -> tuple[np.ndarray, list[tuple[int, int]]]:
    pairs = [(i, j) for i in range(len(descriptors)) for j in range(i + 1, len(descriptors))]
    rows = []
    for i, j in pairs:
        zi = descriptors[i]
        zj = descriptors[j]
        rows.append(
            [
                (zi[a] * zj[b] + zi[b] * zj[a]) / 2.0
                for a in range(N_DESCRIPTORS)
                for b in range(a, N_DESCRIPTORS)
            ]
        )
    matrix = np.asarray(rows)
    matrix = (matrix - matrix.mean(axis=0)) / matrix.std(axis=0)
    return matrix, pairs


def d_optimal_indices(features: np.ndarray, n_select: int) -> np.ndarray:
    information_inverse = np.eye(features.shape[1]) / RIDGE
    remaining = np.ones(len(features), dtype=bool)
    selected = []
    for _ in range(n_select):
        candidate_index = np.where(remaining)[0]
        candidate = features[candidate_index]
        leverage = np.einsum("ij,jk,ik->i", candidate, information_inverse, candidate)
        chosen = int(candidate_index[np.argmax(leverage)])
        x = features[chosen]
        ax = information_inverse @ x
        information_inverse -= np.outer(ax, ax) / (1.0 + x @ ax)
        remaining[chosen] = False
        selected.append(chosen)
    return np.asarray(selected, dtype=int)


def ridge_predict(features: np.ndarray, observed: np.ndarray, train: np.ndarray) -> np.ndarray:
    x = features[train]
    with np.errstate(all="ignore"):
        gram = np.einsum("ni,nj->ij", x, x) + RIDGE * np.eye(features.shape[1])
        rhs = np.einsum("ni,n->i", x, observed[train])
        beta = np.linalg.solve(gram, rhs)
        prediction = np.einsum("ij,j->i", features, beta)
    if not np.isfinite(prediction).all():
        raise FloatingPointError("non-finite ridge prediction")
    return prediction


def spearman(first: np.ndarray, second: np.ndarray) -> float:
    if np.std(first) == 0 or np.std(second) == 0:
        return 0.0
    return float(np.corrcoef(rankdata(first), rankdata(second))[0, 1])


def effect_vector(features: np.ndarray, regime: str, rng: np.random.Generator) -> np.ndarray:
    theta = rng.normal(size=features.shape[1])
    with np.errstate(all="ignore"):
        aligned = np.einsum("ij,j->i", features, theta) / np.sqrt(features.shape[1])
    if not np.isfinite(aligned).all():
        raise FloatingPointError("non-finite aligned synthetic effect")
    if regime == "descriptor_aligned":
        return aligned
    sparse = np.zeros(len(features))
    active = rng.choice(len(features), size=max(1, int(0.12 * len(features))), replace=False)
    sparse[active] = rng.normal(0, 2.0, len(active))
    if regime == "mixed":
        return 0.70 * aligned + sparse
    if regime == "idiosyncratic":
        return sparse
    raise ValueError(regime)


def evaluate(true: np.ndarray, predicted: np.ndarray, test: np.ndarray) -> tuple[float, float, float]:
    truth = true[test]
    estimate = predicted[test]
    rmse = float(np.sqrt(np.mean((truth - estimate) ** 2)))
    rho = spearman(truth, estimate)
    top_n = min(10, len(test))
    true_top = set(test[np.argsort(np.abs(truth))[-top_n:]])
    pred_top = set(test[np.argsort(np.abs(estimate))[-top_n:]])
    recall = len(true_top & pred_top) / top_n
    return rmse, rho, recall


def run(outdir: Path) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    synthetic_dir = outdir / "synthetic"
    synthetic_dir.mkdir(exist_ok=True)
    config = {
        "synthetic_only": True,
        "purpose": "method behavior only; no MS target or biological evidence",
        "n_targets": N_TARGETS,
        "descriptor_dimensions": N_DESCRIPTORS,
        "candidate_pairs": N_TARGETS * (N_TARGETS - 1) // 2,
        "selected_pairs": N_PAIRS,
        "replicates_per_regime_seed": N_REPLICATES,
        "seeds": list(SEEDS),
        "regimes": list(REGIMES),
    }
    (synthetic_dir / "simulation_config.json").write_text(json.dumps(config, indent=2) + "\n")

    aggregate_rows = []
    selection_rows = []
    for seed in SEEDS:
        design_rng = np.random.default_rng(seed)
        descriptors = design_rng.normal(size=(N_TARGETS, N_DESCRIPTORS))
        features, pairs = pair_features(descriptors)
        d_opt = d_optimal_indices(features, N_PAIRS)
        for index in d_opt:
            selection_rows.append(
                {
                    "seed": seed,
                    "design": "d_optimal",
                    "generic_pair": f"P{pairs[index][0] + 1:02d}-P{pairs[index][1] + 1:02d}",
                    "synthetic_only": True,
                }
            )
        raw_rows = []
        for regime_index, regime in enumerate(REGIMES):
            rng = np.random.default_rng(seed + (regime_index + 1) * 1_000_000)
            for replicate in range(N_REPLICATES):
                random_selection = rng.choice(len(features), size=N_PAIRS, replace=False)
                common_test = np.setdiff1d(
                    np.arange(len(features)),
                    np.union1d(d_opt, random_selection),
                    assume_unique=False,
                )
                true = effect_vector(features, regime, rng)
                observed = true + rng.normal(0, 0.50, len(true))
                for design, selected in (("d_optimal", d_opt), ("random", random_selection)):
                    predicted = ridge_predict(features, observed, selected)
                    rmse, rho, recall = evaluate(true, predicted, common_test)
                    raw_rows.append(
                        {
                            "regime": regime,
                            "replicate": replicate,
                            "design": design,
                            "rmse": rmse,
                            "spearman": rho,
                            "top10_recall": recall,
                        }
                    )
        raw = pd.DataFrame(raw_rows)
        for (regime, design), sub in raw.groupby(["regime", "design"], sort=False):
            aggregate_rows.append(
                {
                    "seed": seed,
                    "regime": regime,
                    "design": design,
                    "n_replicates": len(sub),
                    "rmse_median": float(sub["rmse"].median()),
                    "rmse_q95": float(sub["rmse"].quantile(0.95)),
                    "spearman_median": float(sub["spearman"].median()),
                    "top10_recall_median": float(sub["top10_recall"].median()),
                    "synthetic_only": True,
                }
            )

    aggregate = pd.DataFrame(aggregate_rows)
    aggregate.to_csv(outdir / "design_performance.tsv", sep="\t", index=False)
    pd.DataFrame(selection_rows).to_csv(
        synthetic_dir / "generic_d_optimal_pair_layouts.tsv", sep="\t", index=False
    )
    comparison_rows = []
    all_seed_pass = True
    for seed in SEEDS:
        for regime in REGIMES:
            sub = aggregate[(aggregate["seed"] == seed) & (aggregate["regime"] == regime)].set_index("design")
            comparison_rows.append(
                {
                    "seed": seed,
                    "regime": regime,
                    "rmse_ratio_dopt_to_random": float(sub.loc["d_optimal", "rmse_median"] / sub.loc["random", "rmse_median"]),
                    "spearman_gain": float(sub.loc["d_optimal", "spearman_median"] - sub.loc["random", "spearman_median"]),
                    "top10_recall_gain": float(sub.loc["d_optimal", "top10_recall_median"] - sub.loc["random", "top10_recall_median"]),
                }
            )
        seed_rows = {row["regime"]: row for row in comparison_rows if row["seed"] == seed}
        seed_pass = bool(
            seed_rows["descriptor_aligned"]["rmse_ratio_dopt_to_random"] <= 0.90
            and seed_rows["descriptor_aligned"]["spearman_gain"] >= 0.05
            and seed_rows["mixed"]["rmse_ratio_dopt_to_random"] <= 0.95
            and seed_rows["mixed"]["spearman_gain"] >= 0.02
        )
        all_seed_pass &= seed_pass
    comparison = pd.DataFrame(comparison_rows)
    comparison.to_csv(outdir / "design_comparison.tsv", sep="\t", index=False)
    summary = {
        "purpose": "seeded synthetic combinatorial-screen design comparison; no biological claim",
        "synthetic_only": True,
        "n_effect_noise_replicates": N_REPLICATES * len(REGIMES) * len(SEEDS),
        "n_method_evaluations": N_REPLICATES * len(REGIMES) * len(SEEDS) * 2,
        "conditional_d_optimal_gate": "PASS" if all_seed_pass else "FAIL",
        "interpretation": (
            "D-optimal pair selection is conditionally supported when descriptors capture substantial interaction structure."
            if all_seed_pass
            else "D-optimal pair selection did not meet the frozen cross-seed method gate."
        ),
        "falsification_boundary": "No advantage is licensed when interactions are idiosyncratic to the descriptor model.",
    }
    (outdir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    rows = []
    for row in comparison.to_dict(orient="records"):
        rows.append(
            f"| {row['seed']} | {row['regime']} | {row['rmse_ratio_dopt_to_random']:.3f} | "
            f"{row['spearman_gain']:.3f} | {row['top10_recall_gain']:.3f} |"
        )
    report = f"""# V57 Combinatorial Perturbation Design Result

## Result

- Conditional D-optimal method gate: **{summary['conditional_d_optimal_gate']}**.
- Scale: {summary['n_effect_noise_replicates']:,} seeded synthetic screens and
  {summary['n_method_evaluations']:,} design evaluations.
- No target identity or biological measurement was simulated as real evidence.

| seed | regime | D-opt/random RMSE | rank-correlation gain | top-10 recall gain |
|---:|---|---:|---:|---:|
{chr(10).join(rows)}

## Decision boundary

A pass licenses only a small pilot whose pre-assay descriptors are audited and
whose random-design comparator is retained. The idiosyncratic regime is the
failure case: if descriptors do not encode real interaction structure, geometry
cannot create it. Any future human-cell screen still needs independent donors,
CRISPRi and CRISPRa direction arms, non-targeting controls, batch-balanced
processing, held-out perturbations, and orthogonal functional readouts. This
simulation does not nominate a target or establish anything about MS.
"""
    (outdir / "REPORT.md").write_text(report)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", type=Path, default=Path("analysis/v57_perturbation_design"))
    args = parser.parse_args()
    run(args.outdir)


if __name__ == "__main__":
    main()
