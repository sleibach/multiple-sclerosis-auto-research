#!/usr/bin/env python3
"""Map viability-assay precision for independent context confirmation.

All generated observations are seeded synthetic method-test data and are not
biological evidence.
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
import v57_two_stage_context_confirmation as stage  # noqa: E402


DEFAULT_OUTDIR = ROOT / "analysis/v57_safety_assay_precision"
SEEDS = (57301, 57302, 57303)
EFFECT_SCALES = (0.80, 1.00)
DONORS_PER_CONTEXT = (8, 12)
TECHNICAL_WELLS = (1, 2, 4)
N_SCREENS = 1000


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    return parser.parse_args()


def orthogonal_viability(
    rng: np.random.Generator,
    context: np.ndarray,
    scale: float,
    technical_wells: int,
) -> np.ndarray:
    effects = stage.make_effects(context, scale)[..., 4]
    donors = len(context)
    guides = np.array([0.85, 1.00, 1.15])
    fixed = effects[None, :, :, None, None] * guides[None, None, None, :, None]
    return (
        fixed
        + rng.normal(0.0, 0.10, size=(N_SCREENS, 1, donors, 1, 1))
        + rng.normal(
            0.0,
            0.20,
            size=(N_SCREENS, parent.N_CANDIDATES, donors, 1, 1),
        )
        + rng.normal(
            0.0,
            0.05,
            size=(N_SCREENS, parent.N_CANDIDATES, 1, parent.N_GUIDES, 1),
        )
        + rng.normal(
            0.0,
            0.40,
            size=(
                N_SCREENS,
                parent.N_CANDIDATES,
                donors,
                parent.N_GUIDES,
                technical_wells,
            ),
        )
    ).mean(axis=(3, 4))


def run_cell(
    seed: int, scale: float, donors_per_context: int, technical_wells: int
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    corr = np.full((parent.N_OUTCOMES, parent.N_OUTCOMES), 0.10)
    corr[:4, :4] = 0.25
    np.fill_diagonal(corr, 1.0)
    chol = np.linalg.cholesky(corr)
    discovery_context = np.array([0] * 8 + [1] * 4)
    discovery_rng = np.random.default_rng(seed * 10_000 + int(scale * 100))
    discovery = stage.generate(discovery_rng, discovery_context, scale, chol)
    nominated, _ = stage.discovery_gate(discovery)

    context = np.array([0] * donors_per_context + [1] * donors_per_context)
    efficacy_rng = np.random.default_rng(
        seed * 10_000 + donors_per_context * 100 + int(scale * 100) + 8_000_000
    )
    efficacy_observed = stage.generate(efficacy_rng, context, scale, chol)
    efficacy_donor = efficacy_observed.mean(axis=3)[..., :4]
    viability_rng = np.random.default_rng(
        seed * 10_000
        + donors_per_context * 100
        + technical_wells * 10
        + int(scale * 100)
        + 9_000_000
    )
    viability_donor = orthogonal_viability(
        viability_rng, context, scale, technical_wells
    )
    alpha_cell = parent.ALPHA / (
        stage.MAX_NOMINATED * 2 * parent.N_OUTCOMES
    )
    efficacy_pass = np.ones_like(nominated)
    viability_pass = np.ones_like(nominated)
    for group in (0, 1):
        mask = context == group
        n_group = int(mask.sum())
        tcrit = stats.t.ppf(1.0 - alpha_cell, df=n_group - 1)
        eff = efficacy_donor[..., mask, :]
        eff_lower = eff.mean(axis=2) - tcrit * (
            eff.std(axis=2, ddof=1) / np.sqrt(n_group)
        )
        efficacy_pass &= (eff_lower > stage.EFFICACY_MARGIN).all(axis=-1)
        via = viability_donor[..., mask]
        via_lower = via.mean(axis=2) - tcrit * (
            via.std(axis=2, ddof=1) / np.sqrt(n_group)
        )
        viability_pass &= via_lower > parent.VIABILITY_MARGIN
    confirmed = nominated & efficacy_pass & viability_pass

    performance: list[dict[str, object]] = []
    diagnostics: list[dict[str, object]] = []
    for method, selected in (
        ("discovery_nomination", nominated),
        ("orthogonal_safety_confirmation", confirmed),
    ):
        performance.append({
            "seed": seed,
            "effect_scale": f"{scale:.2f}",
            "donors_per_context": donors_per_context,
            "technical_wells": technical_wells,
            "donor_guide_wells_per_candidate": 2 * donors_per_context * parent.N_GUIDES * technical_wells,
            "method": method,
            **{key: f"{value:.6f}" for key, value in stage.metrics(selected).items()},
        })
    for class_name in ("uniform_broad_rescue", "context_harm"):
        mask = stage.LABELS == class_name
        selected = nominated[:, mask]
        denominator = int(selected.sum())
        diagnostics.append({
            "seed": seed,
            "effect_scale": f"{scale:.2f}",
            "donors_per_context": donors_per_context,
            "technical_wells": technical_wells,
            "truth_class": class_name,
            "n_nominated_candidate_instances": denominator,
            "efficacy_component_pass_rate": f"{((selected & efficacy_pass[:, mask]).sum() / denominator if denominator else 0.0):.6f}",
            "viability_component_pass_rate": f"{((selected & viability_pass[:, mask]).sum() / denominator if denominator else 0.0):.6f}",
            "joint_confirmation_rate": f"{((selected & confirmed[:, mask]).sum() / denominator if denominator else 0.0):.6f}",
        })
    return performance, diagnostics


def main() -> int:
    args = parse_args()
    outdir = args.outdir
    outdir.mkdir(parents=True, exist_ok=True)
    performance: list[dict[str, object]] = []
    diagnostics: list[dict[str, object]] = []
    for seed in SEEDS:
        for scale in EFFECT_SCALES:
            for donors in DONORS_PER_CONTEXT:
                for wells in TECHNICAL_WELLS:
                    perf, diag = run_cell(seed, scale, donors, wells)
                    performance.extend(perf)
                    diagnostics.extend(diag)
    perf_fields = [
        "seed", "effect_scale", "donors_per_context", "technical_wells",
        "donor_guide_wells_per_candidate", "method", "prob_any_uniform_rescue",
        "prob_any_context_harm", "prob_any_other_false", "uniform_rescue_recall",
        "selection_precision", "mean_n_selected",
    ]
    parent.write_tsv(outdir / "performance.tsv", performance, perf_fields)
    parent.write_tsv(
        outdir / "component_diagnostics.tsv", diagnostics,
        ["seed", "effect_scale", "donors_per_context", "technical_wells",
         "truth_class", "n_nominated_candidate_instances",
         "efficacy_component_pass_rate", "viability_component_pass_rate",
         "joint_confirmation_rate"],
    )
    lookup = {
        (int(row["seed"]), float(row["effect_scale"]), int(row["donors_per_context"]), int(row["technical_wells"]), str(row["method"])): row
        for row in performance
    }
    gates: list[dict[str, object]] = []
    for seed in SEEDS:
        for scale in EFFECT_SCALES:
            for donors in DONORS_PER_CONTEXT:
                for wells in TECHNICAL_WELLS:
                    disc = lookup[(seed, scale, donors, wells, "discovery_nomination")]
                    conf = lookup[(seed, scale, donors, wells, "orthogonal_safety_confirmation")]
                    checks = {
                        "context_harm_le_0.05": float(conf["prob_any_context_harm"]) <= 0.05,
                        "any_uniform_rescue_ge_0.80": float(conf["prob_any_uniform_rescue"]) >= 0.80,
                        "precision_ge_0.90": float(conf["selection_precision"]) >= 0.90,
                        "context_harm_below_discovery": float(conf["prob_any_context_harm"])
                        < float(disc["prob_any_context_harm"]),
                        "uniform_rescue_loss_le_0.10": float(conf["prob_any_uniform_rescue"])
                        >= float(disc["prob_any_uniform_rescue"]) - 0.10,
                    }
                    for check, passed in checks.items():
                        gates.append({
                            "seed": seed, "effect_scale": f"{scale:.2f}",
                            "donors_per_context": donors,
                            "technical_wells": wells, "check": check,
                            "status": "PASS" if passed else "FAIL",
                        })
    parent.write_tsv(
        outdir / "gate_checks.tsv", gates,
        ["seed", "effect_scale", "donors_per_context", "technical_wells", "check", "status"],
    )
    design_status: dict[tuple[int, int], bool] = {}
    for donors in DONORS_PER_CONTEXT:
        for wells in TECHNICAL_WELLS:
            design_status[(donors, wells)] = all(
                row["status"] == "PASS"
                for row in gates
                if int(row["donors_per_context"]) == donors
                and int(row["technical_wells"]) == wells
            )
    passing = [
        (2 * donors * parent.N_GUIDES * wells, donors, wells)
        for (donors, wells), passed in design_status.items()
        if passed
    ]
    best = min(passing) if passing else None
    summary = {
        "synthetic": True,
        "purpose": "orthogonal safety-assay precision method test; no biological claim",
        "n_synthetic_screens": len(SEEDS) * len(EFFECT_SCALES) * len(DONORS_PER_CONTEXT) * len(TECHNICAL_WELLS) * N_SCREENS,
        "n_candidate_evaluations_per_stage": len(SEEDS) * len(EFFECT_SCALES) * len(DONORS_PER_CONTEXT) * len(TECHNICAL_WELLS) * N_SCREENS * parent.N_CANDIDATES,
        "design_status": {f"{d}_donors_per_context_{w}_wells": "PASS" if p else "FAIL" for (d, w), p in design_status.items()},
        "least_resource_passing_design": ({"donor_guide_wells_per_candidate": best[0], "donors_per_context": best[1], "technical_wells": best[2]} if best else None),
        "n_gate_checks": len(gates),
        "n_gate_fail": sum(row["status"] == "FAIL" for row in gates),
        "overall_status": "PASS" if best else "FAIL",
    }
    (outdir / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    status_lines = "\n".join(
        f"- `{donors}` donors/context, `{wells}` wells/guide: **{'PASS' if passed else 'FAIL'}**."
        for (donors, wells), passed in design_status.items()
    )
    best_text = json.dumps(summary["least_resource_passing_design"], sort_keys=True)
    (outdir / "REPORT.md").write_text(f"""# V57 Orthogonal Safety-Assay Precision

Status: **{summary['overall_status']}** as seeded synthetic method behavior;
no biological or MS claim.

## Scale

- Synthetic screens: `{summary['n_synthetic_screens']:,}`.
- Candidate evaluations: `{summary['n_candidate_evaluations_per_stage']:,}` per stage.
- Viability donor heterogeneity remains; only per-well assay noise is reduced
  by technical replication.

## Frozen Results

{status_lines}

Least-resource passing design: `{best_text}`.
Failed checks: `{summary['n_gate_fail']}` of `{summary['n_gate_checks']}`.

## Meaning

This result identifies an assay-design requirement under explicitly synthetic
variance assumptions. It does not estimate real assay variance, show that a
rescue exists, or establish any MS mechanism. A blinded empirical variance
pilot is required before using the resource count prospectively.
""")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
