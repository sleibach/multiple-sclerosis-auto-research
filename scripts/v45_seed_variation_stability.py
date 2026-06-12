#!/usr/bin/env python3
"""Seed-variation stability checks for V45 synthetic method behavior.

Synthetic method-characterization only. No real cohort is read and no biological
claim is made.
"""

from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

multi = importlib.import_module("v45_multiconfounder_batch_guard_simulation")
post = importlib.import_module("v45_postpartum_harness_pathology_simulation")
tb = importlib.import_module("v45_tb_compartment_pathology_simulation")

OUT = ROOT / "analysis" / "v45_seed_variation_stability"
OUT.mkdir(parents=True, exist_ok=True)

SEED_BASES = [46045, 46145, 46245, 46345, 46445]
REPLICATES_PER_CELL = 30


def run_multiconfounder(seed_base: int) -> pd.DataFrame:
    rows = []
    idx = 0
    for truth in multi.TRUTHS:
        for scenario in multi.SCENARIOS:
            for severity in multi.SEVERITIES:
                for replicate in range(REPLICATES_PER_CELL):
                    spec = multi.SimSpec(
                        truth=truth,
                        scenario=scenario,
                        severity=severity,
                        replicate=replicate,
                        seed=seed_base + idx,
                    )
                    frame = multi.simulate(spec)
                    rec = {
                        "harness": "primary_multiconfounder_batch_guard",
                        "truth": truth,
                        "pathology": scenario,
                        "severity": severity,
                        "replicate": replicate,
                        "seed": seed_base + idx,
                    }
                    rec.update(multi.evaluate(frame))
                    rec["raw_pass"] = rec["primary_pass"]
                    rec["guarded_clean_pass"] = rec["individual_guarded_acceptable_pass"]
                    rows.append(rec)
                    idx += 1
    return pd.DataFrame(rows)


def run_postpartum(seed_base: int) -> pd.DataFrame:
    rows = []
    idx = 0
    for truth in post.TRUTHS:
        for pathology in post.PATHOLOGIES:
            for severity in post.SEVERITIES:
                for replicate in range(REPLICATES_PER_CELL):
                    spec = post.SimSpec(
                        truth=truth,
                        pathology=pathology,
                        severity=severity,
                        replicate=replicate,
                        seed=seed_base + idx,
                    )
                    frame = post.simulate(spec)
                    rec = {
                        "harness": "postpartum_apc_arm",
                        "truth": truth,
                        "pathology": pathology,
                        "severity": severity,
                        "replicate": replicate,
                        "seed": seed_base + idx,
                    }
                    rec.update(post.evaluate(frame, seed_base + idx))
                    rec["raw_pass"] = rec["primary_pass"]
                    rows.append(rec)
                    idx += 1
    return pd.DataFrame(rows)


def run_tb(seed_base: int) -> pd.DataFrame:
    rows = []
    idx = 0
    for truth in tb.TRUTHS:
        for pathology in tb.PATHOLOGIES:
            for severity in tb.SEVERITIES:
                for replicate in range(REPLICATES_PER_CELL):
                    spec = tb.SimSpec(
                        truth=truth,
                        pathology=pathology,
                        severity=severity,
                        replicate=replicate,
                        seed=seed_base + idx,
                    )
                    frame = tb.simulate(spec)
                    rec = {
                        "harness": "tb_compartment",
                        "truth": truth,
                        "pathology": pathology,
                        "severity": severity,
                        "replicate": replicate,
                        "seed": seed_base + idx,
                    }
                    rec.update(tb.evaluate(frame, seed_base + idx))
                    rec["raw_pass"] = rec["raw_pass"]
                    rows.append(rec)
                    idx += 1
    return pd.DataFrame(rows)


def summarize(metrics: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    cell = (
        metrics.groupby(["seed_family", "harness", "truth", "pathology", "severity"], as_index=False)
        .agg(
            cohorts=("raw_pass", "size"),
            raw_pass_rate=("raw_pass", "mean"),
            guarded_clean_pass_rate=("guarded_clean_pass", "mean"),
        )
    )
    rows = []
    for (seed_family, harness), group in cell.groupby(["seed_family", "harness"]):
        null = group[group["truth"].eq("synthetic_null")]
        planted = group[group["truth"].eq("planted")]
        rows.append(
            {
                "seed_family": seed_family,
                "harness": harness,
                "worst_null_raw_pass_rate": float(null["raw_pass_rate"].max()),
                "worst_null_guarded_clean_pass_rate": float(null["guarded_clean_pass_rate"].max()),
                "mean_null_guarded_clean_pass_rate": float(null["guarded_clean_pass_rate"].mean()),
                "best_planted_guarded_clean_pass_rate": float(planted["guarded_clean_pass_rate"].max()),
                "mean_planted_guarded_clean_pass_rate": float(planted["guarded_clean_pass_rate"].mean()),
            }
        )
    return cell, pd.DataFrame(rows)


def main() -> int:
    all_metrics = []
    for idx, seed_base in enumerate(SEED_BASES, start=1):
        for frame in [run_multiconfounder(seed_base), run_postpartum(seed_base + 10_000), run_tb(seed_base + 20_000)]:
            frame.insert(0, "seed_family", f"seed_family_{idx}")
            frame.insert(1, "seed_base", seed_base)
            all_metrics.append(frame)
    metrics = pd.concat(all_metrics, ignore_index=True, sort=False)
    metrics.to_csv(OUT / "seed_variation_metrics.tsv", sep="\t", index=False)
    cell, per_seed = summarize(metrics)
    cell.to_csv(OUT / "seed_variation_cell_summary.tsv", sep="\t", index=False)
    per_seed.to_csv(OUT / "seed_variation_per_seed_summary.tsv", sep="\t", index=False)
    stability = (
        per_seed.groupby("harness", as_index=False)
        .agg(
            seed_families=("seed_family", "nunique"),
            worst_null_guarded_min=("worst_null_guarded_clean_pass_rate", "min"),
            worst_null_guarded_median=("worst_null_guarded_clean_pass_rate", "median"),
            worst_null_guarded_max=("worst_null_guarded_clean_pass_rate", "max"),
            worst_null_raw_max=("worst_null_raw_pass_rate", "max"),
            best_planted_guarded_max=("best_planted_guarded_clean_pass_rate", "max"),
            mean_planted_guarded_median=("mean_planted_guarded_clean_pass_rate", "median"),
        )
    )
    stability["stable_null_guard_below_0_05_all_seeds"] = stability["worst_null_guarded_max"] <= 0.05
    stability.to_csv(OUT / "seed_variation_stability_summary.tsv", sep="\t", index=False)
    summary = {
        "synthetic": True,
        "seed_bases": SEED_BASES,
        "replicates_per_cell": REPLICATES_PER_CELL,
        "cohorts": int(len(metrics)),
        "harnesses": sorted(metrics["harness"].unique().tolist()),
        "all_harnesses_null_guard_below_0_05": bool(stability["stable_null_guard_below_0_05_all_seeds"].all()),
        "worst_guarded_null_by_harness": {
            row["harness"]: float(row["worst_null_guarded_max"]) for _, row in stability.iterrows()
        },
        "worst_raw_null_by_harness": {
            row["harness"]: float(row["worst_null_raw_max"]) for _, row in stability.iterrows()
        },
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
