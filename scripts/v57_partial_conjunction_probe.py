#!/usr/bin/env python3
"""Test whether the frozen V22 association recurs in at least r environments."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "analysis" / "v57_environment_stability" / "cohort_metrics.tsv"
OUT = ROOT / "analysis" / "v57_partial_conjunction"
ALPHA = 0.05


def bonferroni_partial_conjunction(ordered_p: np.ndarray, r: int) -> float:
    m = len(ordered_p)
    return float(min(1.0, (m - r + 1) * ordered_p[r - 1]))


def fisher_partial_conjunction(ordered_p: np.ndarray, r: int) -> float:
    retained = np.clip(ordered_p[r - 1 :], np.finfo(float).tiny, 1.0)
    statistic = float(-2.0 * np.log(retained).sum())
    return float(stats.chi2.sf(statistic, 2 * len(retained)))


def sequential_lower_bound(results: pd.DataFrame, column: str) -> int:
    lower = 0
    for row in results.sort_values("r_minimum_nonnull").itertuples(index=False):
        if getattr(row, column) <= ALPHA:
            lower = int(row.r_minimum_nonnull)
        else:
            break
    return lower


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    cohorts = pd.read_csv(INPUT, sep="\t").sort_values("cohort").reset_index(drop=True)
    required = {
        "cohort",
        "n",
        "auc",
        "exact_one_sided_auc_p",
        "direction_consistent_auc_gt_half",
    }
    missing = required - set(cohorts.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    if len(cohorts) != 4 or cohorts["cohort"].nunique() != 4:
        raise ValueError("Frozen contract requires four distinct environments")

    p_values = cohorts["exact_one_sided_auc_p"].to_numpy(float)
    ordered = np.sort(p_values)
    rows = []
    for r in range(1, len(ordered) + 1):
        bonf = bonferroni_partial_conjunction(ordered, r)
        fisher = fisher_partial_conjunction(ordered, r)
        rows.append(
            {
                "r_minimum_nonnull": r,
                "m_environments": len(ordered),
                "ordered_p_r": float(ordered[r - 1]),
                "bonferroni_pc_p": bonf,
                "bonferroni_reject_0_05": bonf <= ALPHA,
                "fisher_pc_p_independence_sensitivity": fisher,
                "fisher_reject_0_05": fisher <= ALPHA,
            }
        )
    results = pd.DataFrame(rows)
    primary = results[results["r_minimum_nonnull"] == 2].iloc[0]
    direction_count = int(cohorts["direction_consistent_auc_gt_half"].sum())
    primary_pass = bool(primary["bonferroni_pc_p"] <= ALPHA and direction_count >= 2)
    summary = {
        "purpose": "V57 cross-environment partial-conjunction method probe; no external validation claim",
        "n_environments": int(len(cohorts)),
        "n_subjects": int(cohorts["n"].sum()),
        "direction_positive_environments": direction_count,
        "primary_r": 2,
        "primary_bonferroni_pc_p": float(primary["bonferroni_pc_p"]),
        "primary_fisher_pc_p_independence_sensitivity": float(
            primary["fisher_pc_p_independence_sensitivity"]
        ),
        "primary_transport_replicability_pass": primary_pass,
        "dependence_valid_lower_bound_on_nonnull_environments_95pct": sequential_lower_bound(
            results, "bonferroni_pc_p"
        ),
        "independence_sensitivity_lower_bound_on_nonnull_environments_95pct": sequential_lower_bound(
            results, "fisher_pc_p_independence_sensitivity"
        ),
        "verdict": "AT_LEAST_TWO_ENVIRONMENTS_SUPPORTED" if primary_pass else "CROSS_ENVIRONMENT_REPLICABILITY_NOT_ESTABLISHED",
    }

    cohorts.to_csv(OUT / "environment_inputs.tsv", sep="\t", index=False)
    results.to_csv(OUT / "partial_conjunction_results.tsv", sep="\t", index=False)
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    report = f"""# V57 Partial-Conjunction Replicability Probe

## Result

All four exact one-sided environment p-values were retained. The primary
dependence-valid test for responder-higher association in at least two
environments gives partial-conjunction p =
{summary['primary_bonferroni_pc_p']:.3f}. The independence-based Fisher
sensitivity gives p =
{summary['primary_fisher_pc_p_independence_sensitivity']:.3f}. The predeclared
cross-environment replicability gate **{'passes' if primary_pass else 'fails'}**.

The conservative 95% lower bound on the number of non-null environments is
{summary['dependence_valid_lower_bound_on_nonnull_environments_95pct']}; under
the independence sensitivity it is
{summary['independence_sensitivity_lower_bound_on_nonnull_environments_95pct']}.
All {direction_count}/4 observed AUCs are above 0.50, but compatible direction
alone does not establish replicability.

## Interpretation

The prior weighted pooled association is not enough to claim that the signal
is present in two independent environments. The held evidence is compatible
with one strong environment plus weaker or null associations elsewhere. This
sharpens, rather than contradicts, the earlier `NOT_ENVIRONMENT_STABLE`
verdict: external validation remains necessary.

The cohorts differ in disease and therapy context, so even a positive result
would have been recurrence evidence rather than external MS validation. This
probe neither changes V22 nor supplies a biological or clinical claim.
"""
    (OUT / "REPORT.md").write_text(report)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
