#!/usr/bin/env python3
"""Stress the observed V22 score against measurement and label error."""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "analysis" / "v32_confounder_audit" / "v32_subject_confounder_scores.tsv"
OUT = ROOT / "analysis" / "v57_v22_integrity_envelope"
RELIABILITIES = (1.00, 0.95, 0.90, 0.80, 0.70, 0.60, 0.50)
SEEDS = (57001, 57002, 57003)
N_REPLICATES = 50_000


def auc_vector(scores: np.ndarray, labels: np.ndarray) -> np.ndarray:
    """Mann-Whitney AUC for one row or a matrix of replicate rows."""
    matrix = np.atleast_2d(np.asarray(scores, dtype=float))
    pos = matrix[:, labels == 1]
    neg = matrix[:, labels == 0]
    comparisons = pos[:, :, None] - neg[:, None, :]
    auc = ((comparisons > 0).sum(axis=(1, 2)) + 0.5 * (comparisons == 0).sum(axis=(1, 2))) / (
        pos.shape[1] * neg.shape[1]
    )
    return auc


def score_noise_scale(scores: np.ndarray, cohorts: np.ndarray, reliability: float, mode: str) -> np.ndarray:
    if reliability == 1.0:
        return np.zeros_like(scores)
    multiplier = np.sqrt((1.0 - reliability) / reliability)
    if mode == "global":
        return np.full_like(scores, np.std(scores, ddof=1) * multiplier)
    if mode == "cohort_scaled":
        out = np.zeros_like(scores)
        for cohort in np.unique(cohorts):
            mask = cohorts == cohort
            out[mask] = np.std(scores[mask], ddof=1) * multiplier
        return out
    raise ValueError(f"Unknown mode: {mode}")


def measurement_envelope(scores: np.ndarray, labels: np.ndarray, cohorts: np.ndarray) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for mode in ("global", "cohort_scaled"):
        for reliability in RELIABILITIES:
            scale = score_noise_scale(scores, cohorts, reliability, mode)
            for seed in SEEDS:
                if reliability == 1.0:
                    aucs = np.repeat(auc_vector(scores, labels)[0], N_REPLICATES)
                else:
                    rng = np.random.default_rng(seed + (0 if mode == "global" else 100_000))
                    perturbed = scores[None, :] + rng.normal(size=(N_REPLICATES, len(scores))) * scale[None, :]
                    aucs = auc_vector(perturbed, labels)
                rows.append(
                    {
                        "mode": mode,
                        "reliability": reliability,
                        "seed": seed,
                        "n_replicates": N_REPLICATES,
                        "auc_median": float(np.median(aucs)),
                        "auc_q05": float(np.quantile(aucs, 0.05)),
                        "auc_q95": float(np.quantile(aucs, 0.95)),
                        "prob_auc_gt_0_50": float(np.mean(aucs > 0.50)),
                        "prob_auc_ge_0_60": float(np.mean(aucs >= 0.60)),
                        "prob_auc_ge_0_70": float(np.mean(aucs >= 0.70)),
                    }
                )
    result = pd.DataFrame(rows)
    result["practical_cell_pass"] = (result["auc_median"] >= 0.70) & (result["prob_auc_ge_0_60"] >= 0.80)
    return result


def label_exchange_envelope(frame: pd.DataFrame, scores: np.ndarray, labels: np.ndarray) -> pd.DataFrame:
    positive = tuple(np.flatnonzero(labels == 1).tolist())
    negative = tuple(np.flatnonzero(labels == 0).tolist())
    cohorts = frame["cohort"].astype(str).to_numpy()
    rows: list[dict[str, object]] = []
    config_id = 0
    for k in (1, 2, 3):
        for pos_swap in itertools.combinations(positive, k):
            for neg_swap in itertools.combinations(negative, k):
                swapped = labels.copy()
                swapped[list(pos_swap)] = 0
                swapped[list(neg_swap)] = 1
                auc = float(auc_vector(scores, swapped)[0])
                within = all(
                    sum(cohorts[i] == cohort for i in pos_swap)
                    == sum(cohorts[i] == cohort for i in neg_swap)
                    for cohort in np.unique(cohorts)
                )
                rows.append(
                    {
                        "configuration_id": config_id,
                        "k_label_pairs_exchanged": k,
                        "within_cohort_balance_preserved": within,
                        "auc": auc,
                    }
                )
                config_id += 1
    return pd.DataFrame(rows)


def summarize_label_exchanges(exchanges: pd.DataFrame) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    for mode, subset in (
        ("unrestricted_balance_preserving", exchanges),
        ("within_cohort_balance_preserving", exchanges[exchanges["within_cohort_balance_preserved"]]),
    ):
        summary = (
            subset.groupby("k_label_pairs_exchanged")
            .agg(
                n_configurations=("configuration_id", "size"),
                auc_min=("auc", "min"),
                auc_median=("auc", "median"),
                auc_max=("auc", "max"),
                fraction_auc_lt_0_60=("auc", lambda x: float(np.mean(x < 0.60))),
                fraction_auc_le_0_50=("auc", lambda x: float(np.mean(x <= 0.50))),
            )
            .reset_index()
        )
        summary.insert(0, "mode", mode)
        frames.append(summary)
    return pd.concat(frames, ignore_index=True)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    frame = pd.read_csv(INPUT, sep="\t")
    labels = frame["response"].eq("Responder").astype(int).to_numpy()
    scores = frame["locked_signed_score"].to_numpy(float)
    cohorts = frame["cohort"].astype(str).to_numpy()
    observed_auc = float(auc_vector(scores, labels)[0])

    measurement = measurement_envelope(scores, labels, cohorts)
    exchanges = label_exchange_envelope(frame, scores, labels)
    exchange_summary = summarize_label_exchanges(exchanges)

    high_reliability = measurement[measurement["reliability"] >= 0.80]
    reliability_grid = (
        measurement.groupby("reliability", sort=False)["practical_cell_pass"].all().sort_index(ascending=False)
    )
    passing_reliabilities = reliability_grid[reliability_grid].index.tolist()
    unrestricted_one = exchange_summary[
        (exchange_summary["mode"] == "unrestricted_balance_preserving")
        & (exchange_summary["k_label_pairs_exchanged"] == 1)
    ].iloc[0]
    worst = exchanges.sort_values(["auc", "configuration_id"], kind="stable").iloc[0]
    worst_one = exchanges[exchanges["k_label_pairs_exchanged"] == 1].sort_values(
        ["auc", "configuration_id"], kind="stable"
    ).iloc[0]
    summary = {
        "purpose": "V57 V22 measurement and label integrity sensitivity; not biological evidence",
        "n_held_subjects": int(len(frame)),
        "n_responders": int(labels.sum()),
        "n_nonresponders": int((labels == 0).sum()),
        "observed_auc": observed_auc,
        "measurement_replicates_evaluated": int(len(measurement) * N_REPLICATES),
        "measurement_modes": sorted(measurement["mode"].unique().tolist()),
        "measurement_seeds": list(SEEDS),
        "high_reliability_all_cells_pass": bool(high_reliability["practical_cell_pass"].all()),
        "lowest_reliability_all_cells_pass": float(min(passing_reliabilities)) if passing_reliabilities else None,
        "minimum_prob_auc_ge_0_60_at_reliability_ge_0_80": float(high_reliability["prob_auc_ge_0_60"].min()),
        "minimum_median_auc_at_reliability_ge_0_80": float(high_reliability["auc_median"].min()),
        "label_exchange_configurations": int(len(exchanges)),
        "single_pair_min_auc": float(unrestricted_one["auc_min"]),
        "single_pair_fraction_auc_lt_0_60": float(unrestricted_one["fraction_auc_lt_0_60"]),
        "single_pair_adversarially_robust": bool(unrestricted_one["auc_min"] >= 0.60),
        "worst_single_pair": {
            "auc": float(worst_one["auc"]),
        },
        "worst_any_exchange": {
            "k": int(worst["k_label_pairs_exchanged"]),
            "auc": float(worst["auc"]),
        },
    }

    measurement.to_csv(OUT / "measurement_error_envelope.tsv", sep="\t", index=False)
    exchange_summary.to_csv(OUT / "label_exchange_summary.tsv", sep="\t", index=False)
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")

    report = f"""# V57 V22 Measurement and Label Integrity Envelope

## Measurement-error result

The audit evaluated {summary['measurement_replicates_evaluated']:,} seeded
score perturbations across two variance modes, seven assumed reliabilities,
and three seeds. At reliability at least 0.80, the least favorable cell had
median AUC {summary['minimum_median_auc_at_reliability_ge_0_80']:.3f} and
probability {summary['minimum_prob_auc_ge_0_60_at_reliability_ge_0_80']:.1%}
of retaining AUC >= 0.60. The predeclared high-reliability criterion
{'passes' if summary['high_reliability_all_cells_pass'] else 'fails'}; the
lowest grid reliability for which every seed and mode passes is
{summary['lowest_reliability_all_cells_pass']}.

This is conditional sensitivity around observed scores. It does not estimate
the reliability of Gafson, Karolinska, or any assay and cannot substitute for
empirical technical replicates.

## Label-integrity result

The audit exhaustively evaluated {summary['label_exchange_configurations']:,}
balance-preserving label-exchange configurations. A single adversarial pair
can reduce AUC from {observed_auc:.3f} to {summary['single_pair_min_auc']:.3f};
{summary['single_pair_fraction_auc_lt_0_60']:.1%} of all one-pair exchanges
fall below 0.60. The predeclared adversarial single-pair criterion therefore
{'passes' if summary['single_pair_adversarially_robust'] else 'fails'}.

The worst single exchange yields AUC
{summary['worst_single_pair']['auc']:.3f}. Participant-level exchange
configurations are intentionally not persisted in this public repository;
the committed aggregates are sufficient to reproduce the method conclusion
from the already-governed held input.

## Decision implication

The frozen score is reasonably tolerant of added independent measurement
noise under the stated reliability model, but the 19-subject result is
materially dependent on clinical-label integrity. External validation should
require blinded endpoint adjudication and an auditable label provenance trail,
not merely adequate expression measurement. This does not change V22 or add
biological evidence.
"""
    (OUT / "REPORT.md").write_text(report)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
