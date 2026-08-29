#!/usr/bin/env python3
"""Stress the V57 rescue gate against a prespecified donor-context reversal.

The script generates seeded synthetic method-test observations only. It does
not model MS biology or provide evidence for a perturbation.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from scipy import stats


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import v57_multicriterion_perturbation_gate as parent  # noqa: E402


DEFAULT_OUTDIR = ROOT / "analysis/v57_context_safe_perturbation_gate"
SEEDS = (57101, 57102, 57103)
DONOR_COUNTS = (12, 16, 24)
EFFECT_SCALES = (0.80, 1.00)
N_SCREENS = 1000
CONTEXT_EFFICACY_MARGIN = -0.25
LABELS = np.array(
    ["uniform_broad_rescue"] * 4
    + ["subgroup_reversal"] * 4
    + ["tradeoff"] * 4
    + ["toxic_pseudorescue"] * 4
    + ["null"] * 8,
    dtype=object,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    return parser.parse_args()


def context_effects(donors: int, scale: float) -> tuple[np.ndarray, np.ndarray]:
    minority = int(round(donors / 3))
    context = np.zeros(donors, dtype=int)
    context[-minority:] = 1
    effects = np.zeros((parent.N_CANDIDATES, donors, parent.N_OUTCOMES))
    broad = scale * np.array([1.00, 0.90, 0.85, 0.80])
    effects[0:4, :, :4] = broad
    effects[0:4, :, 4] = -0.05
    effects[4:8, context == 0, :4] = broad
    effects[4:8, context == 1, :4] = -scale * np.array([0.70, 0.70, 0.60, 0.60])
    effects[4:8, :, 4] = -0.05
    effects[8:12, :, :4] = scale * np.array([1.00, 0.80, -0.50, -0.40])
    effects[8:12, :, 4] = -0.10
    effects[12:16, :, :4] = scale * np.array([1.00, 0.80, 0.70, 0.60])
    effects[12:16, :, 4] = -1.00
    return effects, context


def evaluate(selected: np.ndarray) -> dict[str, float]:
    uniform = LABELS == "uniform_broad_rescue"
    reversal = LABELS == "subgroup_reversal"
    n_selected = int(selected.sum())
    n_uniform = int(selected[:, uniform].sum())
    return {
        "prob_any_uniform_rescue": float(selected[:, uniform].any(axis=1).mean()),
        "prob_any_subgroup_reversal": float(selected[:, reversal].any(axis=1).mean()),
        "prob_any_other_false": float(selected[:, ~(uniform | reversal)].any(axis=1).mean()),
        "uniform_rescue_recall": float(n_uniform / (selected.shape[0] * uniform.sum())),
        "selection_precision": float(n_uniform / n_selected) if n_selected else 1.0,
        "mean_n_selected": float(selected.sum(axis=1).mean()),
    }


def run_cell(seed: int, donors: int, scale: float) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    rng = np.random.default_rng(seed * 10_000 + donors * 100 + int(scale * 100))
    effects, context = context_effects(donors, scale)
    corr = np.full((parent.N_OUTCOMES, parent.N_OUTCOMES), 0.10)
    corr[:4, :4] = 0.25
    np.fill_diagonal(corr, 1.0)
    chol = np.linalg.cholesky(corr)
    guide_factors = np.array([0.85, 1.00, 1.15])
    fixed = effects[None, :, :, None, :] * guide_factors[None, None, None, :, None]
    donor_global = parent.correlated_noise(rng, (N_SCREENS, 1, donors, 1), 0.15, chol)
    candidate_donor = parent.correlated_noise(
        rng, (N_SCREENS, parent.N_CANDIDATES, donors, 1), 0.30, chol
    )
    guide_noise = parent.correlated_noise(
        rng, (N_SCREENS, parent.N_CANDIDATES, 1, parent.N_GUIDES), 0.10, chol
    )
    measurement = parent.correlated_noise(
        rng, (N_SCREENS, parent.N_CANDIDATES, donors, parent.N_GUIDES), 0.45, chol
    )
    observed = fixed + donor_global + candidate_donor + guide_noise + measurement
    donor_means = observed.mean(axis=3)
    guide_means = observed.mean(axis=2)

    scalar_by_donor = donor_means[..., :4].mean(axis=-1)
    _, _, efficacy_p = parent.one_sided_p(donor_means[..., :4], axis=2)
    partial_conjunction_p = np.minimum(1.0, 2.0 * np.sort(efficacy_p, axis=-1)[..., 2])
    efficacy_pass = partial_conjunction_p <= parent.ALPHA / parent.N_CANDIDATES
    viability_mean, viability_se, _ = parent.one_sided_p(donor_means[..., 4], axis=2)
    pooled_tcrit = stats.t.ppf(
        1.0 - parent.ALPHA / parent.N_CANDIDATES, df=donors - 1
    )
    viability_pass = viability_mean - pooled_tcrit * viability_se > parent.VIABILITY_MARGIN
    total = scalar_by_donor.sum(axis=2, keepdims=True)
    donor_pass = ((total - scalar_by_donor) / (donors - 1)).min(axis=2) > 0.0
    guide_pass = (guide_means[..., :4].mean(axis=-1) > 0.0).sum(axis=2) >= 2
    pooled_selected = efficacy_pass & viability_pass & donor_pass & guide_pass

    context_pass = np.ones((N_SCREENS, parent.N_CANDIDATES), dtype=bool)
    for group in (0, 1):
        mask = context == group
        n_group = int(mask.sum())
        group_efficacy = scalar_by_donor[..., mask]
        group_mean = group_efficacy.mean(axis=2)
        group_se = group_efficacy.std(axis=2, ddof=1) / np.sqrt(n_group)
        tcrit = stats.t.ppf(
            1.0 - parent.ALPHA / (parent.N_CANDIDATES * 2), df=n_group - 1
        )
        efficacy_lower = group_mean - tcrit * group_se
        group_viability = donor_means[..., mask, 4]
        viability_lower = group_viability.mean(axis=2) - tcrit * (
            group_viability.std(axis=2, ddof=1) / np.sqrt(n_group)
        )
        context_pass &= efficacy_lower > CONTEXT_EFFICACY_MARGIN
        context_pass &= viability_lower > parent.VIABILITY_MARGIN
    context_selected = pooled_selected & context_pass

    perf_rows: list[dict[str, object]] = []
    class_rows: list[dict[str, object]] = []
    for method, selected in (
        ("pooled_replicated_gate", pooled_selected),
        ("context_safe_gate", context_selected),
    ):
        perf_rows.append({
            "seed": seed,
            "donors": donors,
            "minority_donors": int((context == 1).sum()),
            "effect_scale": f"{scale:.2f}",
            "method": method,
            **{key: f"{value:.6f}" for key, value in evaluate(selected).items()},
        })
        for class_name in np.unique(LABELS):
            class_mask = LABELS == class_name
            class_rows.append({
                "seed": seed,
                "donors": donors,
                "effect_scale": f"{scale:.2f}",
                "method": method,
                "truth_class": class_name,
                "candidate_selection_probability": f"{selected[:, class_mask].mean():.6f}",
            })
    return perf_rows, class_rows


def main() -> int:
    args = parse_args()
    outdir = args.outdir
    outdir.mkdir(parents=True, exist_ok=True)
    performance: list[dict[str, object]] = []
    class_rows: list[dict[str, object]] = []
    for seed in SEEDS:
        for donors in DONOR_COUNTS:
            for scale in EFFECT_SCALES:
                perf, classes = run_cell(seed, donors, scale)
                performance.extend(perf)
                class_rows.extend(classes)
    perf_fields = [
        "seed", "donors", "minority_donors", "effect_scale", "method",
        "prob_any_uniform_rescue", "prob_any_subgroup_reversal",
        "prob_any_other_false", "uniform_rescue_recall", "selection_precision",
        "mean_n_selected",
    ]
    parent.write_tsv(outdir / "performance.tsv", performance, perf_fields)
    parent.write_tsv(
        outdir / "class_selection.tsv", class_rows,
        ["seed", "donors", "effect_scale", "method", "truth_class", "candidate_selection_probability"],
    )
    lookup = {
        (int(row["seed"]), int(row["donors"]), float(row["effect_scale"]), str(row["method"])): row
        for row in performance
    }
    gates: list[dict[str, object]] = []
    for seed in SEEDS:
        for donors in (16, 24):
            for scale in EFFECT_SCALES:
                safe = lookup[(seed, donors, scale, "context_safe_gate")]
                pooled = lookup[(seed, donors, scale, "pooled_replicated_gate")]
                checks = {
                    "reversal_promotion_le_0.05": float(safe["prob_any_subgroup_reversal"]) <= 0.05,
                    "any_uniform_rescue_ge_0.80": float(safe["prob_any_uniform_rescue"]) >= 0.80,
                    "precision_ge_0.90": float(safe["selection_precision"]) >= 0.90,
                    "reversal_below_pooled": float(safe["prob_any_subgroup_reversal"])
                    < float(pooled["prob_any_subgroup_reversal"]),
                    "uniform_rescue_loss_le_0.10": float(safe["prob_any_uniform_rescue"])
                    >= float(pooled["prob_any_uniform_rescue"]) - 0.10,
                }
                for check, passed in checks.items():
                    gates.append({
                        "seed": seed, "donors": donors,
                        "effect_scale": f"{scale:.2f}", "check": check,
                        "status": "PASS" if passed else "FAIL",
                    })
    parent.write_tsv(
        outdir / "gate_checks.tsv", gates,
        ["seed", "donors", "effect_scale", "check", "status"],
    )
    donor_status = {
        donors: all(
            row["status"] == "PASS" for row in gates if int(row["donors"]) == donors
        )
        for donors in (16, 24)
    }
    passing = [donors for donors, passed in donor_status.items() if passed]
    eligible = [row for row in performance if int(row["donors"]) >= 16]
    pooled_eligible = [row for row in eligible if row["method"] == "pooled_replicated_gate"]
    safe_eligible = [row for row in eligible if row["method"] == "context_safe_gate"]
    summary = {
        "synthetic": True,
        "purpose": "context-reversal method stress test; no biological claim",
        "n_synthetic_screens": len(SEEDS) * len(DONOR_COUNTS) * len(EFFECT_SCALES) * N_SCREENS,
        "n_candidate_evaluations_per_method": len(SEEDS) * len(DONOR_COUNTS) * len(EFFECT_SCALES) * N_SCREENS * parent.N_CANDIDATES,
        "donor_status": {str(k): "PASS" if v else "FAIL" for k, v in donor_status.items()},
        "first_tested_passing_donor_count": min(passing) if passing else None,
        "n_gate_checks": len(gates),
        "n_gate_fail": sum(row["status"] == "FAIL" for row in gates),
        "overall_status": "PASS" if passing else "FAIL",
    }
    (outdir / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    status_text = "\n".join(
        f"- `{donors}` donors: **{'PASS' if passed else 'FAIL'}** across all frozen cells."
        for donors, passed in donor_status.items()
    )
    (outdir / "REPORT.md").write_text(f"""# V57 Context-Safe Perturbation Gate

Status: **{summary['overall_status']}** as seeded synthetic method behavior;
no biological or MS claim.

## Scale

- Synthetic screens: `{summary['n_synthetic_screens']:,}`.
- Candidate evaluations: `{summary['n_candidate_evaluations_per_method']:,}` per method.
- One-third prespecified minority context; pooled favorable effects can reverse
  across all efficacy outcomes in that context.

## Frozen Result

{status_text}

First tested passing context-safe design: `{summary['first_tested_passing_donor_count']}` donors.
Failed checks: `{summary['n_gate_fail']}` of `{summary['n_gate_checks']}`.

Across the frozen 16/24-donor operating cells, the pooled gate's minimum
uniform-rescue detection was `{min(float(row['prob_any_uniform_rescue']) for row in pooled_eligible):.3f}` and maximum subgroup-reversal promotion was
`{max(float(row['prob_any_subgroup_reversal']) for row in pooled_eligible):.3f}`. The context-safe gate's corresponding values were
`{min(float(row['prob_any_uniform_rescue']) for row in safe_eligible):.3f}` and
`{max(float(row['prob_any_subgroup_reversal']) for row in safe_eligible):.3f}`.

## Meaning

The pooled gate can be inspected against `performance.tsv`; the context-safe
gate is acceptable only where it controls subgroup-reversal promotion and
retains uniform-rescue sensitivity under every seed and effect. Here it does
not: simultaneous within-context non-harm bounds add little specificity to the
already conservative pooled gate and destroy useful sensitivity. The method is
rejected rather than retuned. This is a design stress test under a known,
prespecified context. It neither discovers a human subgroup nor establishes a
biological rescue. Unknown contexts still require broader donor sampling and
independent replication.
""")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
