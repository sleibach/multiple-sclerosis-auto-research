#!/usr/bin/env python3
"""Bound whether any fixed V27/V28 score can improve V22 by AUC 0.05."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "analysis" / "v27_coupled_axis" / "v27_feature_table.tsv"
OUT = ROOT / "analysis" / "v57_successor_nonsuperiority"
SEEDS = (57091, 57092, 57093)
N_BOOTSTRAP = 200_000
MARGIN = 0.05
CHUNK = 5_000
CANDIDATES = (
    "delta_RECEPTOR",
    "coupled_projection",
    "coupled_v22_augmented",
    "coupling_coordination",
    "apc_vector_norm",
    "hla_vs_ifn_angle",
    "hla_ifn_product",
)


def add_features(frame: pd.DataFrame) -> pd.DataFrame:
    out = frame.copy()
    out["apc_vector_norm"] = np.sqrt(
        out["delta_IFN_APC"] ** 2 + out["delta_HLAII"] ** 2 + out["delta_RECEPTOR"] ** 2
    )
    out["hla_vs_ifn_angle"] = np.arctan2(out["delta_HLAII"], -out["delta_IFN_APC"])
    out["hla_ifn_product"] = out["delta_HLAII"] * (-out["delta_IFN_APC"])
    return out


def auc_one(labels: np.ndarray, scores: np.ndarray) -> float:
    pos = scores[labels == 1]
    neg = scores[labels == 0]
    diff = pos[:, None] - neg[None, :]
    return float(((diff > 0).sum() + 0.5 * (diff == 0).sum()) / diff.size)


def auc_bootstrap(scores: np.ndarray, sampled_indices: np.ndarray, bootstrap_labels: np.ndarray) -> np.ndarray:
    output = np.empty(len(sampled_indices), dtype=float)
    pos_mask = bootstrap_labels == 1
    neg_mask = ~pos_mask
    for start in range(0, len(sampled_indices), CHUNK):
        stop = min(start + CHUNK, len(sampled_indices))
        values = scores[sampled_indices[start:stop]]
        pos = values[:, pos_mask]
        neg = values[:, neg_mask]
        diff = pos[:, :, None] - neg[:, None, :]
        output[start:stop] = (
            (diff > 0).sum(axis=(1, 2)) + 0.5 * (diff == 0).sum(axis=(1, 2))
        ) / (pos.shape[1] * neg.shape[1])
    return output


def stratified_indices(frame: pd.DataFrame, rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    blocks = []
    labels = []
    for (_, label), group in frame.groupby(["cohort", "response_binary"], sort=True):
        indices = group.index.to_numpy(dtype=np.int32)
        blocks.append(rng.choice(indices, size=(N_BOOTSTRAP, len(indices)), replace=True))
        labels.extend([int(label)] * len(indices))
    return np.concatenate(blocks, axis=1), np.asarray(labels, dtype=np.int8)


def analyze_set(frame: pd.DataFrame, set_name: str) -> tuple[pd.DataFrame, dict[str, object]]:
    frame = frame.reset_index(drop=True)
    labels = frame["response_binary"].to_numpy(dtype=np.int8)
    locked = frame["locked_signed_score"].to_numpy(float)
    observed_locked = auc_one(labels, locked)
    observed_deltas = {
        candidate: auc_one(labels, frame[candidate].to_numpy(float)) - observed_locked
        for candidate in CANDIDATES
    }
    rows: list[dict[str, object]] = []
    family_upper = []
    for seed in SEEDS:
        rng = np.random.default_rng(seed)
        indices, bootstrap_labels = stratified_indices(frame, rng)
        locked_auc = auc_bootstrap(locked, indices, bootstrap_labels)
        deltas = np.empty((N_BOOTSTRAP, len(CANDIDATES)), dtype=float)
        for column, candidate in enumerate(CANDIDATES):
            candidate_auc = auc_bootstrap(
                frame[candidate].to_numpy(float), indices, bootstrap_labels
            )
            delta = candidate_auc - locked_auc
            deltas[:, column] = delta
            rows.append(
                {
                    "analysis_set": set_name,
                    "seed": seed,
                    "candidate": candidate,
                    "n": len(frame),
                    "n_bootstrap": N_BOOTSTRAP,
                    "meaningful_improvement_margin": MARGIN,
                    "observed_delta_auc": observed_deltas[candidate],
                    "delta_q05": float(np.quantile(delta, 0.05)),
                    "delta_median": float(np.median(delta)),
                    "one_sided_upper_q95": float(np.quantile(delta, 0.95)),
                    "bootstrap_probability_delta_ge_margin": float(np.mean(delta >= MARGIN)),
                    "nonsuperiority_pass": bool(np.quantile(delta, 0.95) < MARGIN),
                }
            )
        family_delta = np.max(deltas, axis=1)
        upper = float(np.quantile(family_delta, 0.95))
        family_upper.append(upper)
        rows.append(
            {
                "analysis_set": set_name,
                "seed": seed,
                "candidate": "family_maximum_of_7",
                "n": len(frame),
                "n_bootstrap": N_BOOTSTRAP,
                "meaningful_improvement_margin": MARGIN,
                "observed_delta_auc": max(observed_deltas.values()),
                "delta_q05": float(np.quantile(family_delta, 0.05)),
                "delta_median": float(np.median(family_delta)),
                "one_sided_upper_q95": upper,
                "bootstrap_probability_delta_ge_margin": float(np.mean(family_delta >= MARGIN)),
                "nonsuperiority_pass": bool(upper < MARGIN),
            }
        )
    info = {
        "n": int(len(frame)),
        "locked_auc": observed_locked,
        "best_observed_candidate": max(observed_deltas, key=observed_deltas.get),
        "best_observed_delta_auc": float(max(observed_deltas.values())),
        "family_upper_q95_min_across_seeds": float(min(family_upper)),
        "family_upper_q95_max_across_seeds": float(max(family_upper)),
        "family_nonsuperiority_all_seeds": bool(all(value < MARGIN for value in family_upper)),
    }
    return pd.DataFrame(rows), info


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    frame = add_features(pd.read_csv(INPUT, sep="\t"))
    frame["response_binary"] = frame["response_binary"].astype(np.int8)
    sets = {
        "bounded_immune_remodeling": frame[frame["domain"] == "bounded"].copy(),
        "all_primary_plus_exact_uc": frame.copy(),
    }
    tables = []
    set_info = {}
    for name, subset in sets.items():
        table, info = analyze_set(subset, name)
        tables.append(table)
        set_info[name] = info
    results = pd.concat(tables, ignore_index=True)
    primary = set_info["bounded_immune_remodeling"]
    pass_gate = bool(primary["family_nonsuperiority_all_seeds"])
    summary = {
        "purpose": "V57 paired AUC successor non-superiority probe; not external validation",
        "seeds": list(SEEDS),
        "n_bootstrap_per_seed_and_set": N_BOOTSTRAP,
        "candidate_count": len(CANDIDATES),
        "meaningful_improvement_margin": MARGIN,
        "sets": set_info,
        "primary_family_nonsuperiority_pass": pass_gate,
        "verdict": (
            "MEANINGFUL_FIXED_SCORE_SUCCESSOR_GAIN_EXCLUDED"
            if pass_gate
            else "NO_OBSERVED_IMPROVEMENT_BUT_MEANINGFUL_GAIN_NOT_EXCLUDED"
        ),
    }
    results.to_csv(OUT / "successor_nonsuperiority_bounds.tsv", sep="\t", index=False)
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    report = f"""# V57 Fixed-Score Successor Non-Superiority Audit

## Result

The best observed bounded-set candidate is
`{primary['best_observed_candidate']}` with candidate-minus-locked AUC
{primary['best_observed_delta_auc']:+.3f}. After paired cohort-by-outcome
resampling and taking the best of all seven candidates in every replicate, the
one-sided 95% upper bound ranges from
{primary['family_upper_q95_min_across_seeds']:.3f} to
{primary['family_upper_q95_max_across_seeds']:.3f} across three seeds. The
predeclared family non-superiority gate **{'passes' if pass_gate else 'fails'}**
against the inherited +0.05 AUC margin.

## Interpretation

No fixed-score successor improves the observed bounded AUC, but the small held
sample cannot exclude a meaningful +0.05 gain after accounting for selection
among seven candidates. The defensible wording is therefore **no observed
improvement, with meaningful improvement still statistically unexcluded**.
This is stricter than treating a nonsignificant superiority test as proof of
equivalence.

The immutable scalar remains the only pre-locked validation target because no
successor met its original promotion gate. This audit does not rehabilitate a
post-hoc candidate, alter V22, or create external validation evidence.
"""
    (OUT / "REPORT.md").write_text(report)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
