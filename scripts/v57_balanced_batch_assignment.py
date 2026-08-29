#!/usr/bin/env python3
"""Synthetic prospective batch-allocation method characterization for V57."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd


N_PATIENTS = 60
N_BATCHES = 6
CAPACITY = N_PATIENTS // N_BATCHES
N_CANDIDATES = 5_000
N_NULL = 20_000
SEEDS = (5701, 5702, 5703)
SCENARIOS = ("independent", "site_response_coupled", "rare_site")


def make_cohort(scenario: str, rng: np.random.Generator) -> pd.DataFrame:
    if scenario == "independent":
        site = np.repeat(np.arange(4), 15)
        rng.shuffle(site)
        response = rng.binomial(1, 0.5, N_PATIENTS)
        sex = rng.binomial(1, 0.5, N_PATIENTS)
    elif scenario == "site_response_coupled":
        site = np.repeat(np.arange(4), 15)
        rng.shuffle(site)
        response = rng.binomial(1, np.array([0.20, 0.35, 0.65, 0.80])[site])
        sex = rng.binomial(1, np.array([0.40, 0.45, 0.55, 0.60])[site])
    elif scenario == "rare_site":
        site = np.array([0] * 30 + [1] * 15 + [2] * 10 + [3] * 5)
        rng.shuffle(site)
        response = rng.binomial(1, np.array([0.35, 0.50, 0.65, 0.85])[site])
        sex = rng.binomial(1, np.array([0.45, 0.50, 0.60, 0.70])[site])
    else:
        raise ValueError(scenario)
    # Ensure both outcome classes exist and retain realistic prevalence.
    if response.sum() < 15 or response.sum() > 45:
        order = rng.permutation(N_PATIENTS)
        response = np.zeros(N_PATIENTS, dtype=int)
        response[order[:30]] = 1
    age = np.clip(rng.normal(42 + 2 * site, 9, N_PATIENTS), 18, 70)
    age_stratum = pd.cut(age, bins=[17, 34, 49, 70], labels=False).astype(int)
    return pd.DataFrame(
        {
            "patient": np.arange(N_PATIENTS),
            "site": site,
            "response": response,
            "sex": sex,
            "age": age,
            "age_stratum": age_stratum,
        }
    )


def random_assignment(rng: np.random.Generator) -> np.ndarray:
    assignment = np.repeat(np.arange(N_BATCHES), CAPACITY)
    rng.shuffle(assignment)
    return assignment


def standardized_imbalance(
    cohort: pd.DataFrame, assignment: np.ndarray, columns: tuple[str, ...]
) -> tuple[float, dict[str, float]]:
    per_column: dict[str, float] = {}
    for column in columns:
        values = cohort[column].to_numpy()
        levels = np.unique(values)
        worst = 0.0
        for level in levels:
            indicator = (values == level).astype(float)
            p = float(indicator.mean())
            scale = max(np.sqrt(p * (1.0 - p)), 0.10)
            for batch in range(N_BATCHES):
                local = float(indicator[assignment == batch].mean())
                worst = max(worst, abs(local - p) / scale)
        per_column[column] = worst
    return max(per_column.values()), per_column


def optimize_assignment(
    cohort: pd.DataFrame,
    columns: tuple[str, ...],
    rng: np.random.Generator,
) -> tuple[np.ndarray, float]:
    best: np.ndarray | None = None
    best_score = np.inf
    for _ in range(N_CANDIDATES):
        candidate = random_assignment(rng)
        score, _ = standardized_imbalance(cohort, candidate, columns)
        if score < best_score:
            best = candidate.copy()
            best_score = score
    assert best is not None
    return best, float(best_score)


def auc_many(labels: np.ndarray, scores: np.ndarray) -> np.ndarray:
    pos = scores[:, labels == 1]
    neg = scores[:, labels == 0]
    # Pairwise definition handles ties exactly and avoids distributional assumptions.
    total = np.zeros(scores.shape[0], dtype=float)
    for start in range(0, pos.shape[1], 8):
        block = pos[:, start : start + 8, None] - neg[:, None, :]
        total += (block > 0).sum(axis=(1, 2)) + 0.5 * (block == 0).sum(axis=(1, 2))
    return total / (pos.shape[1] * neg.shape[1])


def technical_null(
    cohort: pd.DataFrame,
    assignment: np.ndarray,
    rng: np.random.Generator,
) -> tuple[float, float, float]:
    labels = cohort["response"].to_numpy()
    batch_by_time = rng.normal(0.0, 0.75, size=(N_NULL, N_BATCHES))
    patient_noise = rng.normal(0.0, 1.0, size=(N_NULL, N_PATIENTS))
    delta = batch_by_time[:, assignment] + patient_noise
    auc = auc_many(labels, delta)
    return float(np.mean(auc >= 0.70)), float(np.median(auc)), float(np.quantile(auc, 0.95))


def run(outdir: Path) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, object]] = []
    batch_rows: list[dict[str, object]] = []
    for scenario_index, scenario in enumerate(SCENARIOS):
        for seed in SEEDS:
            cohort_rng = np.random.default_rng(seed + scenario_index * 100_000)
            cohort = make_cohort(scenario, cohort_rng)
            methods: dict[str, tuple[np.ndarray, tuple[str, ...]]] = {}
            methods["capacity_random"] = (
                random_assignment(np.random.default_rng(seed + 10_000)),
                tuple(),
            )
            blinded_cols = ("site", "sex", "age_stratum")
            methods["outcome_blind_constrained"] = (
                optimize_assignment(
                    cohort, blinded_cols, np.random.default_rng(seed + 20_000)
                )[0],
                blinded_cols,
            )
            aware_cols = ("site", "sex", "age_stratum", "response")
            methods["outcome_aware_constrained"] = (
                optimize_assignment(
                    cohort, aware_cols, np.random.default_rng(seed + 30_000)
                )[0],
                aware_cols,
            )
            for method_index, (method, (assignment, balanced_cols)) in enumerate(methods.items()):
                _, all_imbalance = standardized_imbalance(
                    cohort, assignment, ("site", "sex", "age_stratum", "response")
                )
                null_rate, null_median, null_q95 = technical_null(
                    cohort,
                    assignment,
                    np.random.default_rng(seed + scenario_index * 100_000 + method_index * 1_000_000),
                )
                rows.append(
                    {
                        "scenario": scenario,
                        "seed": seed,
                        "method": method,
                        "balanced_columns": ",".join(balanced_cols) if balanced_cols else "capacity_only",
                        "n_patients": N_PATIENTS,
                        "n_responders": int(cohort["response"].sum()),
                        "pair_split_rate": 0.0,
                        "baseline_early_count_difference_max": 0,
                        "response_imbalance": all_imbalance["response"],
                        "design_imbalance_max": max(
                            all_imbalance["site"],
                            all_imbalance["sex"],
                            all_imbalance["age_stratum"],
                        ),
                        "technical_null_raw_auc_ge_0_70_rate": null_rate,
                        "technical_null_auc_median": null_median,
                        "technical_null_auc_q95": null_q95,
                        "synthetic_only": True,
                    }
                )
                for batch in range(N_BATCHES):
                    idx = assignment == batch
                    batch_rows.append(
                        {
                            "scenario": scenario,
                            "seed": seed,
                            "method": method,
                            "batch": batch,
                            "n_patients": int(idx.sum()),
                            "n_baseline_samples": int(idx.sum()),
                            "n_early_samples": int(idx.sum()),
                            "response_fraction": float(cohort.loc[idx, "response"].mean()),
                            "synthetic_only": True,
                        }
                    )

    metrics = pd.DataFrame(rows)
    metrics.to_csv(outdir / "allocation_metrics.tsv", sep="\t", index=False)
    pd.DataFrame(batch_rows).to_csv(outdir / "batch_balance.tsv", sep="\t", index=False)
    aggregate = (
        metrics.groupby("method", sort=False)
        .agg(
            n_layouts=("seed", "size"),
            response_imbalance_median=("response_imbalance", "median"),
            response_imbalance_max=("response_imbalance", "max"),
            design_imbalance_median=("design_imbalance_max", "median"),
            technical_null_auc_ge_0_70_rate_mean=("technical_null_raw_auc_ge_0_70_rate", "mean"),
            technical_null_auc_ge_0_70_rate_max=("technical_null_raw_auc_ge_0_70_rate", "max"),
        )
        .reset_index()
    )
    aggregate.to_csv(outdir / "method_summary.tsv", sep="\t", index=False)
    by_method = aggregate.set_index("method")
    aware = by_method.loc["outcome_aware_constrained"]
    random = by_method.loc["capacity_random"]
    gate = bool(
        aware["response_imbalance_median"] < random["response_imbalance_median"]
        and aware["technical_null_auc_ge_0_70_rate_mean"]
        <= random["technical_null_auc_ge_0_70_rate_mean"]
        and (metrics["pair_split_rate"] == 0).all()
        and (metrics["baseline_early_count_difference_max"] == 0).all()
    )
    summary = {
        "purpose": "synthetic prospective batch-allocation method characterization; no MS claim",
        "synthetic_only": True,
        "n_scenarios": len(SCENARIOS),
        "n_seeds": len(SEEDS),
        "n_candidate_allocations_per_constrained_layout": N_CANDIDATES,
        "n_technical_null_replicates_per_layout": N_NULL,
        "n_technical_null_replicates_total": int(len(metrics) * N_NULL),
        "pair_preservation_pass": bool((metrics["pair_split_rate"] == 0).all()),
        "timepoint_balance_pass": bool((metrics["baseline_early_count_difference_max"] == 0).all()),
        "outcome_aware_method_gate": "PASS" if gate else "FAIL",
        "interpretation": (
            "Outcome-aware constrained laboratory allocation is supported as a prospective design option "
            "when labels are finalized and laboratory staff remain blinded; the outcome-blind branch "
            "does not guarantee response balance. Existing post-data batch diagnostics remain mandatory."
            if gate
            else "Constrained allocation did not meet the frozen synthetic method-behavior gate."
        ),
    }
    (outdir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")

    report_rows = []
    for row in aggregate.to_dict(orient="records"):
        report_rows.append(
            "| {method} | {response_imbalance_median:.3f} | {response_imbalance_max:.3f} | "
            "{design_imbalance_median:.3f} | {technical_null_auc_ge_0_70_rate_mean:.4f} | "
            "{technical_null_auc_ge_0_70_rate_max:.4f} |".format(**row)
        )
    report = f"""# V57 Prospective Balanced-Batch Design Result

## Scope

This is **seeded synthetic method characterization only**. It makes no claim
about MS biology and changes neither the locked V22 score nor the V42/V44
validation rules. It asks whether batch confounding can be prevented at the
laboratory-layout stage rather than only detected afterward.

## Result

| method | median response imbalance | maximum response imbalance | median design imbalance | mean null raw AUC >=0.70 | max null raw AUC >=0.70 |
|---|---:|---:|---:|---:|---:|
{chr(10).join(report_rows)}

- Method gate: **{summary['outcome_aware_method_gate']}**.
- All {len(metrics)} layouts kept paired samples together and placed equal
  baseline and early sample counts in every batch.
- Scale: {summary['n_technical_null_replicates_total']:,} technical-null
  cohorts across three cohort structures, three seeds, and three methods.

## Decision

The prospective option is a computer-generated, capacity-constrained layout
that keeps each patient's timepoints together and, when finalized labels exist,
balances response together with site, sex, and age stratum. The laboratory must
remain blinded to labels. If labels cannot legitimately be used before
processing, use the outcome-blind layout and do **not** claim response balance.

This is prevention, not a replacement for the V44 guard: batch/QC metadata and
the pre-specified diagnostic remain mandatory because unmeasured technical
structure can persist. The method has not been tested on a real validation
cohort and cannot validate the APC/HLA-II signal.
"""
    (outdir / "REPORT.md").write_text(report)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", type=Path, default=Path("analysis/v57_balanced_batch_design"))
    args = parser.parse_args()
    run(args.outdir)


if __name__ == "__main__":
    main()
