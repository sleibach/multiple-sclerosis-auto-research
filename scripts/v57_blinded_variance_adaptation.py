#!/usr/bin/env python3
"""Test blinded nuisance-variance adaptation for staged confirmation.

Every generated observation is seeded synthetic method-test data. Nothing in
this script is biological evidence.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy import stats


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import v57_multicriterion_perturbation_gate as parent  # noqa: E402
import v57_two_stage_context_confirmation as stage  # noqa: E402


DEFAULT_OUTDIR = ROOT / "analysis/v57_blinded_variance_adaptation"
SEEDS = (57401, 57402, 57403)
EFFECT_SCALES = (0.80, 1.00)
NOISE_MULTIPLIERS = (0.75, 1.00, 1.25, 1.50)
DONOR_GRID = (12, 16, 20, 24, 32)
N_SCREENS = 500
PILOT_DF = 48
TECHNICAL_WELLS = 2


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    return parser.parse_args()


def choose_grid(required: np.ndarray) -> np.ndarray:
    chosen = np.zeros(required.shape, dtype=int)
    for donors in DONOR_GRID:
        chosen[(chosen == 0) & (required <= donors)] = donors
    return chosen


def confirmation_potential_outcomes(
    rng: np.random.Generator, donors_per_context: int, scale: float, multiplier: float
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    context = np.array([0] * donors_per_context + [1] * donors_per_context)
    donors = len(context)
    effects = stage.make_effects(context, scale)
    efficacy_fixed = effects[None, :, :, :4]
    efficacy = (
        efficacy_fixed
        + rng.normal(0.0, 0.15 * multiplier, size=(N_SCREENS, 1, donors, 4))
        + rng.normal(
            0.0,
            0.30 * multiplier,
            size=(N_SCREENS, parent.N_CANDIDATES, donors, 4),
        )
        + rng.normal(
            0.0,
            0.10 * multiplier / np.sqrt(parent.N_GUIDES),
            size=(N_SCREENS, parent.N_CANDIDATES, 1, 4),
        )
        + rng.normal(
            0.0,
            0.45 * multiplier / np.sqrt(parent.N_GUIDES),
            size=(N_SCREENS, parent.N_CANDIDATES, donors, 4),
        )
    )
    viability_fixed = effects[None, :, :, 4]
    viability = (
        viability_fixed
        + rng.normal(0.0, 0.10 * multiplier, size=(N_SCREENS, 1, donors))
        + rng.normal(
            0.0,
            0.20 * multiplier,
            size=(N_SCREENS, parent.N_CANDIDATES, donors),
        )
        + rng.normal(
            0.0,
            0.05 * multiplier / np.sqrt(parent.N_GUIDES),
            size=(N_SCREENS, parent.N_CANDIDATES, 1),
        )
        + rng.normal(
            0.0,
            0.40
            * multiplier
            / np.sqrt(parent.N_GUIDES * TECHNICAL_WELLS),
            size=(N_SCREENS, parent.N_CANDIDATES, donors),
        )
    )
    return efficacy, viability, context


def confirm(
    efficacy: np.ndarray,
    viability: np.ndarray,
    context: np.ndarray,
    nominated: np.ndarray,
) -> np.ndarray:
    alpha_cell = parent.ALPHA / (
        stage.MAX_NOMINATED * 2 * parent.N_OUTCOMES
    )
    passed = nominated.copy()
    for group in (0, 1):
        mask = context == group
        n_group = int(mask.sum())
        tcrit = stats.t.ppf(1.0 - alpha_cell, df=n_group - 1)
        eff = efficacy[..., mask, :]
        eff_lower = eff.mean(axis=2) - tcrit * (
            eff.std(axis=2, ddof=1) / np.sqrt(n_group)
        )
        via = viability[..., mask]
        via_lower = via.mean(axis=2) - tcrit * (
            via.std(axis=2, ddof=1) / np.sqrt(n_group)
        )
        passed &= (eff_lower > stage.EFFICACY_MARGIN).all(axis=-1)
        passed &= via_lower > parent.VIABILITY_MARGIN
    return passed


def run_cell(
    seed: int, scale: float, multiplier: float
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    stage.N_SCREENS = N_SCREENS
    corr = np.full((parent.N_OUTCOMES, parent.N_OUTCOMES), 0.10)
    corr[:4, :4] = 0.25
    np.fill_diagonal(corr, 1.0)
    chol = np.linalg.cholesky(corr)
    discovery_context = np.array([0] * 8 + [1] * 4)
    discovery_rng = np.random.default_rng(seed * 10_000 + int(scale * 100))
    discovery = stage.generate(discovery_rng, discovery_context, scale, chol)
    nominated, _ = stage.discovery_gate(discovery)

    pilot_rng = np.random.default_rng(
        seed * 10_000 + int(scale * 100) + int(multiplier * 100) + 10_000_000
    )
    s_hat = multiplier * np.sqrt(pilot_rng.chisquare(PILOT_DF, size=N_SCREENS) / PILOT_DF)
    upper_multiplier = s_hat * np.sqrt(
        PILOT_DF / stats.chi2.ppf(0.10, df=PILOT_DF)
    )
    adaptive_required = np.ceil(12.0 * upper_multiplier**2).astype(int)
    adaptive_n = choose_grid(adaptive_required)
    oracle_required = np.full(
        N_SCREENS, math.ceil(12.0 * multiplier**2), dtype=int
    )
    oracle_n = choose_grid(oracle_required)
    fixed_n = np.full(N_SCREENS, 12, dtype=int)

    confirmed_by_n: dict[int, np.ndarray] = {}
    for donors in DONOR_GRID:
        rng = np.random.default_rng(
            seed * 10_000
            + donors * 100
            + int(scale * 100)
            + int(multiplier * 1000)
            + 11_000_000
        )
        efficacy, viability, context = confirmation_potential_outcomes(
            rng, donors, scale, multiplier
        )
        confirmed_by_n[donors] = confirm(efficacy, viability, context, nominated)

    rows = np.arange(N_SCREENS)
    performance: list[dict[str, object]] = []
    distributions: list[dict[str, object]] = []
    for method, donor_choice in (
        ("fixed_12", fixed_n),
        ("blinded_adaptive", adaptive_n),
        ("oracle", oracle_n),
    ):
        selected = np.zeros_like(nominated)
        for donors in DONOR_GRID:
            mask = donor_choice == donors
            selected[mask] = confirmed_by_n[donors][mask]
        measured = stage.metrics(selected)
        performance.append({
            "seed": seed,
            "effect_scale": f"{scale:.2f}",
            "true_noise_multiplier": f"{multiplier:.2f}",
            "method": method,
            "abstention_probability": f"{(donor_choice == 0).mean():.6f}",
            "mean_donors_per_context": f"{donor_choice.mean():.6f}",
            **{key: f"{value:.6f}" for key, value in measured.items()},
        })
        for donors in (0,) + DONOR_GRID:
            distributions.append({
                "seed": seed,
                "effect_scale": f"{scale:.2f}",
                "true_noise_multiplier": f"{multiplier:.2f}",
                "method": method,
                "donors_per_context": donors,
                "probability": f"{(donor_choice == donors).mean():.6f}",
            })
    adaptive = adaptive_n
    oracle = oracle_n
    for row in performance:
        if row["method"] == "blinded_adaptive":
            row["undersize_vs_oracle_probability"] = f"{((adaptive > 0) & (adaptive < oracle)).mean():.6f}"
            row["oversize_vs_oracle_probability"] = f"{(adaptive > oracle).mean():.6f}"
        else:
            row["undersize_vs_oracle_probability"] = ""
            row["oversize_vs_oracle_probability"] = ""
    return performance, distributions


def main() -> int:
    args = parse_args()
    outdir = args.outdir
    outdir.mkdir(parents=True, exist_ok=True)
    performance: list[dict[str, object]] = []
    distributions: list[dict[str, object]] = []
    for seed in SEEDS:
        for scale in EFFECT_SCALES:
            for multiplier in NOISE_MULTIPLIERS:
                perf, dist = run_cell(seed, scale, multiplier)
                performance.extend(perf)
                distributions.extend(dist)
    perf_fields = [
        "seed", "effect_scale", "true_noise_multiplier", "method",
        "abstention_probability", "mean_donors_per_context",
        "prob_any_uniform_rescue", "prob_any_context_harm", "prob_any_other_false",
        "uniform_rescue_recall", "selection_precision", "mean_n_selected",
        "undersize_vs_oracle_probability", "oversize_vs_oracle_probability",
    ]
    parent.write_tsv(outdir / "performance.tsv", performance, perf_fields)
    parent.write_tsv(
        outdir / "sample_size_distribution.tsv", distributions,
        ["seed", "effect_scale", "true_noise_multiplier", "method",
         "donors_per_context", "probability"],
    )
    lookup = {
        (int(row["seed"]), float(row["effect_scale"]), float(row["true_noise_multiplier"]), str(row["method"])): row
        for row in performance
    }
    gates: list[dict[str, object]] = []
    for seed in SEEDS:
        for scale in EFFECT_SCALES:
            for multiplier in NOISE_MULTIPLIERS:
                adaptive = lookup[(seed, scale, multiplier, "blinded_adaptive")]
                oracle = lookup[(seed, scale, multiplier, "oracle")]
                checks = {
                    "context_harm_le_0.05": float(adaptive["prob_any_context_harm"]) <= 0.05,
                    "any_uniform_rescue_ge_0.80": float(adaptive["prob_any_uniform_rescue"]) >= 0.80,
                    "precision_ge_0.90": float(adaptive["selection_precision"]) >= 0.90,
                    "uniform_rescue_loss_vs_oracle_le_0.10": float(adaptive["prob_any_uniform_rescue"])
                    >= float(oracle["prob_any_uniform_rescue"]) - 0.10,
                    "abstention_le_0.10": float(adaptive["abstention_probability"]) <= 0.10,
                }
                for check, passed in checks.items():
                    gates.append({
                        "seed": seed, "effect_scale": f"{scale:.2f}",
                        "true_noise_multiplier": f"{multiplier:.2f}",
                        "check": check, "status": "PASS" if passed else "FAIL",
                    })
    parent.write_tsv(
        outdir / "gate_checks.tsv", gates,
        ["seed", "effect_scale", "true_noise_multiplier", "check", "status"],
    )
    multiplier_status = {
        multiplier: all(
            row["status"] == "PASS"
            for row in gates
            if float(row["true_noise_multiplier"]) == multiplier
        )
        for multiplier in NOISE_MULTIPLIERS
    }
    summary = {
        "synthetic": True,
        "purpose": "blinded nuisance-variance adaptation method test; no biological claim",
        "n_synthetic_screens": len(SEEDS) * len(EFFECT_SCALES) * len(NOISE_MULTIPLIERS) * N_SCREENS,
        "n_candidate_evaluations_per_method": len(SEEDS) * len(EFFECT_SCALES) * len(NOISE_MULTIPLIERS) * N_SCREENS * parent.N_CANDIDATES,
        "multiplier_status": {f"{k:.2f}": "PASS" if v else "FAIL" for k, v in multiplier_status.items()},
        "n_gate_checks": len(gates),
        "n_gate_fail": sum(row["status"] == "FAIL" for row in gates),
        "overall_status": "PASS" if all(multiplier_status.values()) else "FAIL",
    }
    (outdir / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    status_lines = "\n".join(
        f"- true noise multiplier `{m:.2f}`: **{'PASS' if p else 'FAIL'}**."
        for m, p in multiplier_status.items()
    )
    adaptive_rows = [row for row in performance if row["method"] == "blinded_adaptive"]
    (outdir / "REPORT.md").write_text(f"""# V57 Blinded Variance Adaptation

Status: **{summary['overall_status']}** as seeded synthetic method behavior;
no biological or MS claim.

## Scale

- Synthetic screens: `{summary['n_synthetic_screens']:,}`.
- Candidate evaluations: `{summary['n_candidate_evaluations_per_method']:,}` per method.
- Resizing uses a blinded variance estimate only; candidate means and outcomes
  are unavailable to the rule.

## Frozen Result

{status_lines}

Adaptive donor counts ranged from mean
`{min(float(row['mean_donors_per_context']) for row in adaptive_rows):.1f}` to
`{max(float(row['mean_donors_per_context']) for row in adaptive_rows):.1f}` per context; abstention ranged
`{min(float(row['abstention_probability']) for row in adaptive_rows):.3f}`-`{max(float(row['abstention_probability']) for row in adaptive_rows):.3f}`.
Failed checks: `{summary['n_gate_fail']}` of `{summary['n_gate_checks']}`.

## Meaning

A passing regime would license blinded nuisance-based resizing under these
synthetic assumptions. A failed regime identifies where the donor grid or
pilot precision is inadequate; it cannot be fixed by looking at candidate
effects. Real pilot variance and assay diagnostics remain prerequisites.
""")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
