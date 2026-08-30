#!/usr/bin/env python3
"""Characterize independent context confirmation after a broad screen.

All generated data are seeded synthetic method-test observations, never
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


DEFAULT_OUTDIR = ROOT / "analysis/v57_two_stage_context_confirmation"
SEEDS = (57201, 57202, 57203)
EFFECT_SCALES = (0.80, 1.00)
CONFIRM_PER_CONTEXT = (4, 6, 8)
N_SCREENS = 1000
DISCOVERY_DONORS = 12
MAX_NOMINATED = 4
EFFICACY_MARGIN = -0.25
LABELS = np.array(
    ["uniform_broad_rescue"] * 4
    + ["context_harm"] * 4
    + ["tradeoff"] * 4
    + ["toxic_pseudorescue"] * 4
    + ["null"] * 8,
    dtype=object,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    return parser.parse_args()


def make_effects(context: np.ndarray, scale: float) -> np.ndarray:
    donors = len(context)
    effects = np.zeros((parent.N_CANDIDATES, donors, parent.N_OUTCOMES))
    broad = scale * np.array([1.00, 0.90, 0.85, 0.80])
    effects[0:4, :, :4] = broad
    effects[0:4, :, 4] = -0.05
    effects[4:8, :, :4] = broad
    effects[4:8, context == 1, 3] = -0.80 * scale
    effects[4:8, :, 4] = -0.05
    effects[8:12, :, :4] = scale * np.array([1.00, 0.80, -0.50, -0.40])
    effects[8:12, :, 4] = -0.10
    effects[12:16, :, :4] = scale * np.array([1.00, 0.80, 0.70, 0.60])
    effects[12:16, :, 4] = -1.00
    return effects


def generate(
    rng: np.random.Generator, context: np.ndarray, scale: float, chol: np.ndarray
) -> np.ndarray:
    donors = len(context)
    effects = make_effects(context, scale)
    guide_factors = np.array([0.85, 1.00, 1.15])
    fixed = effects[None, :, :, None, :] * guide_factors[None, None, None, :, None]
    return (
        fixed
        + parent.correlated_noise(rng, (N_SCREENS, 1, donors, 1), 0.15, chol)
        + parent.correlated_noise(
            rng, (N_SCREENS, parent.N_CANDIDATES, donors, 1), 0.30, chol
        )
        + parent.correlated_noise(
            rng, (N_SCREENS, parent.N_CANDIDATES, 1, parent.N_GUIDES), 0.10, chol
        )
        + parent.correlated_noise(
            rng,
            (N_SCREENS, parent.N_CANDIDATES, donors, parent.N_GUIDES),
            0.45,
            chol,
        )
    )


def discovery_gate(observed: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    donors = observed.shape[2]
    donor_means = observed.mean(axis=3)
    guide_means = observed.mean(axis=2)
    scalar = donor_means[..., :4].mean(axis=-1)
    _, _, endpoint_p = parent.one_sided_p(donor_means[..., :4], axis=2)
    pc_p = np.minimum(1.0, 2.0 * np.sort(endpoint_p, axis=-1)[..., 2])
    efficacy_pass = pc_p <= parent.ALPHA / parent.N_CANDIDATES
    viability_mean, viability_se, _ = parent.one_sided_p(donor_means[..., 4], axis=2)
    tcrit = stats.t.ppf(1.0 - parent.ALPHA / parent.N_CANDIDATES, df=donors - 1)
    viability_pass = viability_mean - tcrit * viability_se > parent.VIABILITY_MARGIN
    total = scalar.sum(axis=2, keepdims=True)
    donor_pass = ((total - scalar) / (donors - 1)).min(axis=2) > 0.0
    guide_pass = (guide_means[..., :4].mean(axis=-1) > 0.0).sum(axis=2) >= 2
    passes = efficacy_pass & viability_pass & donor_pass & guide_pass
    rank_score = donor_means[..., :4].mean(axis=2).min(axis=-1)
    rank_score = np.where(passes, rank_score, -np.inf)
    order = np.argsort(-rank_score, axis=1)[:, :MAX_NOMINATED]
    rows = np.arange(N_SCREENS)[:, None]
    nominated = np.zeros_like(passes)
    nominated[rows, order] = passes[rows, order]
    return nominated, donor_means


def confirm_gate(
    observed: np.ndarray, context: np.ndarray, nominated: np.ndarray
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    donor_means = observed.mean(axis=3)
    alpha_cell = parent.ALPHA / (MAX_NOMINATED * 2 * parent.N_OUTCOMES)
    efficacy_pass = np.ones_like(nominated)
    viability_pass = np.ones_like(nominated)
    for group in (0, 1):
        mask = context == group
        n_group = int(mask.sum())
        values = donor_means[..., mask, :]
        mean = values.mean(axis=2)
        se = values.std(axis=2, ddof=1) / np.sqrt(n_group)
        tcrit = stats.t.ppf(1.0 - alpha_cell, df=n_group - 1)
        lower = mean - tcrit * se
        efficacy_pass &= (lower[..., :4] > EFFICACY_MARGIN).all(axis=-1)
        viability_pass &= lower[..., 4] > parent.VIABILITY_MARGIN
    confirmed = nominated & efficacy_pass & viability_pass
    return confirmed, efficacy_pass, viability_pass


def metrics(selected: np.ndarray) -> dict[str, float]:
    uniform = LABELS == "uniform_broad_rescue"
    harm = LABELS == "context_harm"
    n_selected = int(selected.sum())
    n_uniform = int(selected[:, uniform].sum())
    return {
        "prob_any_uniform_rescue": float(selected[:, uniform].any(axis=1).mean()),
        "prob_any_context_harm": float(selected[:, harm].any(axis=1).mean()),
        "prob_any_other_false": float(selected[:, ~(uniform | harm)].any(axis=1).mean()),
        "uniform_rescue_recall": float(n_uniform / (N_SCREENS * uniform.sum())),
        "selection_precision": float(n_uniform / n_selected) if n_selected else 1.0,
        "mean_n_selected": float(selected.sum(axis=1).mean()),
    }


def run_cell(
    seed: int, scale: float, confirm_n: int
) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    corr = np.full((parent.N_OUTCOMES, parent.N_OUTCOMES), 0.10)
    corr[:4, :4] = 0.25
    np.fill_diagonal(corr, 1.0)
    chol = np.linalg.cholesky(corr)
    discovery_context = np.array([0] * 8 + [1] * 4)
    discovery_rng = np.random.default_rng(seed * 10_000 + int(scale * 100))
    discovery = generate(discovery_rng, discovery_context, scale, chol)
    nominated, _ = discovery_gate(discovery)
    confirm_context = np.array([0] * confirm_n + [1] * confirm_n)
    confirm_rng = np.random.default_rng(
        seed * 10_000 + confirm_n * 100 + int(scale * 100) + 7_000_000
    )
    confirmation = generate(confirm_rng, confirm_context, scale, chol)
    confirmed, efficacy_pass, viability_pass = confirm_gate(
        confirmation, confirm_context, nominated
    )

    perf: list[dict[str, object]] = []
    classes: list[dict[str, object]] = []
    for method, selected in (
        ("discovery_nomination", nominated),
        ("independent_confirmation", confirmed),
    ):
        perf.append({
            "seed": seed,
            "effect_scale": f"{scale:.2f}",
            "confirm_donors_per_context": confirm_n,
            "confirm_total_donors": 2 * confirm_n,
            "method": method,
            **{key: f"{value:.6f}" for key, value in metrics(selected).items()},
        })
        for class_name in np.unique(LABELS):
            mask = LABELS == class_name
            classes.append({
                "seed": seed,
                "effect_scale": f"{scale:.2f}",
                "confirm_donors_per_context": confirm_n,
                "method": method,
                "truth_class": class_name,
                "candidate_selection_probability": f"{selected[:, mask].mean():.6f}",
            })
    diagnostics: list[dict[str, object]] = []
    for class_name in ("uniform_broad_rescue", "context_harm"):
        mask = LABELS == class_name
        nominated_class = nominated[:, mask]
        denominator = int(nominated_class.sum())
        diagnostics.append({
            "seed": seed,
            "effect_scale": f"{scale:.2f}",
            "confirm_donors_per_context": confirm_n,
            "truth_class": class_name,
            "n_nominated_candidate_instances": denominator,
            "efficacy_component_pass_rate": f"{((nominated_class & efficacy_pass[:, mask]).sum() / denominator if denominator else 0.0):.6f}",
            "viability_component_pass_rate": f"{((nominated_class & viability_pass[:, mask]).sum() / denominator if denominator else 0.0):.6f}",
            "joint_confirmation_rate": f"{((nominated_class & confirmed[:, mask]).sum() / denominator if denominator else 0.0):.6f}",
        })
    return perf, classes, diagnostics


def main() -> int:
    args = parse_args()
    outdir = args.outdir
    outdir.mkdir(parents=True, exist_ok=True)
    performance: list[dict[str, object]] = []
    classes: list[dict[str, object]] = []
    diagnostics: list[dict[str, object]] = []
    for seed in SEEDS:
        for scale in EFFECT_SCALES:
            for confirm_n in CONFIRM_PER_CONTEXT:
                perf, cls, diag = run_cell(seed, scale, confirm_n)
                performance.extend(perf)
                classes.extend(cls)
                diagnostics.extend(diag)
    perf_fields = [
        "seed", "effect_scale", "confirm_donors_per_context",
        "confirm_total_donors", "method", "prob_any_uniform_rescue",
        "prob_any_context_harm", "prob_any_other_false", "uniform_rescue_recall",
        "selection_precision", "mean_n_selected",
    ]
    parent.write_tsv(outdir / "performance.tsv", performance, perf_fields)
    parent.write_tsv(
        outdir / "class_selection.tsv", classes,
        ["seed", "effect_scale", "confirm_donors_per_context", "method", "truth_class", "candidate_selection_probability"],
    )
    parent.write_tsv(
        outdir / "component_diagnostics.tsv", diagnostics,
        ["seed", "effect_scale", "confirm_donors_per_context", "truth_class",
         "n_nominated_candidate_instances", "efficacy_component_pass_rate",
         "viability_component_pass_rate", "joint_confirmation_rate"],
    )
    lookup = {
        (int(row["seed"]), float(row["effect_scale"]), int(row["confirm_donors_per_context"]), str(row["method"])): row
        for row in performance
    }
    gates: list[dict[str, object]] = []
    for seed in SEEDS:
        for scale in EFFECT_SCALES:
            for confirm_n in (6, 8):
                disc = lookup[(seed, scale, confirm_n, "discovery_nomination")]
                conf = lookup[(seed, scale, confirm_n, "independent_confirmation")]
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
                        "confirm_donors_per_context": confirm_n, "check": check,
                        "status": "PASS" if passed else "FAIL",
                    })
    parent.write_tsv(
        outdir / "gate_checks.tsv", gates,
        ["seed", "effect_scale", "confirm_donors_per_context", "check", "status"],
    )
    n_status = {
        n: all(
            row["status"] == "PASS"
            for row in gates
            if int(row["confirm_donors_per_context"]) == n
        )
        for n in (6, 8)
    }
    passing = [n for n, passed in n_status.items() if passed]
    uniform_diagnostics = [
        row for row in diagnostics if row["truth_class"] == "uniform_broad_rescue"
    ]
    summary = {
        "synthetic": True,
        "purpose": "two-stage independent context-confirmation method test; no biological claim",
        "n_synthetic_screens": len(SEEDS) * len(EFFECT_SCALES) * len(CONFIRM_PER_CONTEXT) * N_SCREENS,
        "n_candidate_evaluations_per_stage": len(SEEDS) * len(EFFECT_SCALES) * len(CONFIRM_PER_CONTEXT) * N_SCREENS * parent.N_CANDIDATES,
        "confirmation_status": {str(k): "PASS" if v else "FAIL" for k, v in n_status.items()},
        "first_passing_donors_per_context": min(passing) if passing else None,
        "first_passing_total_confirmation_donors": 2 * min(passing) if passing else None,
        "n_gate_checks": len(gates),
        "n_gate_fail": sum(row["status"] == "FAIL" for row in gates),
        "overall_status": "PASS" if passing else "FAIL",
    }
    (outdir / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    status_text = "\n".join(
        f"- `{n}` fresh donors per context (`{2*n}` total): **{'PASS' if passed else 'FAIL'}**."
        for n, passed in n_status.items()
    )
    (outdir / "REPORT.md").write_text(f"""# V57 Two-Stage Context Confirmation

Status: **{summary['overall_status']}** as seeded synthetic method behavior;
no biological or MS claim.

## Design

- Discovery: 12 donors, pooled replicated gate, at most four nominees.
- Confirmation: fresh, balanced donor contexts; no discovery data reused.
- Synthetic screens: `{summary['n_synthetic_screens']:,}`.
- Candidate evaluations: `{summary['n_candidate_evaluations_per_stage']:,}` per stage.

## Frozen Result

{status_text}

First passing panel: `{summary['first_passing_donors_per_context']}` donors per
context (`{summary['first_passing_total_confirmation_donors']}` total).
Failed checks: `{summary['n_gate_fail']}` of `{summary['n_gate_checks']}`.

Among nominated uniform-rescue candidate instances, the efficacy component
passed in `{min(float(row['efficacy_component_pass_rate']) for row in uniform_diagnostics):.3f}`-`{max(float(row['efficacy_component_pass_rate']) for row in uniform_diagnostics):.3f}` of cases and the viability component in
`{min(float(row['viability_component_pass_rate']) for row in uniform_diagnostics):.3f}`-`{max(float(row['viability_component_pass_rate']) for row in uniform_diagnostics):.3f}`. These post-result diagnostics do not change the frozen gate; they localize the
precision requirement for a future assay-design test.

## Meaning

This test asks whether independent confirmation can reject a candidate that
looks broadly favorable in discovery but harms one functional endpoint in a
prespecified donor context. A pass licenses only the staged method under this
synthetic variance model. It does not discover a context, candidate, target, or
treatment, and empirical pilot variance remains necessary.
""")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
