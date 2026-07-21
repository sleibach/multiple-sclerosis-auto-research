#!/usr/bin/env python3
"""Run the frozen V54 Macnair source-by-stage interaction audit."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import statsmodels.api as sm


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "analysis/v54_progressive_stage_modules/donor_standardized_residual_scores.tsv"
OUT = ROOT / "analysis/v54_progressive_stage_source_interaction"
MODULES = [
    "receptor_cd44_cxcr4",
    "hla_regulatory",
    "mif_ligand",
    "ifn_apc_unique",
    "lysosomal_unique",
]
SOURCES = ["Amsterdam BB", "UK MS TB"]
SEEDS = [54701, 54702, 54703]
N_PER_SEED = 100_000
BATCH = 2_000


def bh(values: np.ndarray) -> np.ndarray:
    order = np.argsort(values)
    adjusted = np.empty(len(values), dtype=float)
    running = 1.0
    for reverse_rank in range(len(values) - 1, -1, -1):
        index = order[reverse_rank]
        running = min(running, values[index] * len(values) / (reverse_rank + 1))
        adjusted[index] = running
    return adjusted


def hc3_fit(y: np.ndarray, x: np.ndarray, coefficient: int) -> dict[str, float]:
    model = sm.OLS(y, x).fit(cov_type="HC3")
    ci = model.conf_int()[coefficient]
    return {
        "beta": float(model.params[coefficient]),
        "ci_low": float(ci[0]),
        "ci_high": float(ci[1]),
        "p": float(model.pvalues[coefficient]),
        "t": float(model.tvalues[coefficient]),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    frame = pd.read_csv(INPUT, sep="\t")
    required = {"canonical_donor", "diagnosis", "source_family", *MODULES}
    missing = sorted(required - set(frame.columns))
    if missing:
        raise RuntimeError(f"Missing columns: {missing}")
    if set(frame.source_family) != set(SOURCES):
        raise RuntimeError("Unexpected source family")
    if set(frame.diagnosis) != {"PPMS", "SPMS"}:
        raise RuntimeError("Unexpected stage labels")
    if frame.canonical_donor.duplicated().any():
        raise RuntimeError("Expected one row per donor")

    stage = frame.diagnosis.eq("SPMS").astype(float).to_numpy()
    uk = frame.source_family.eq("UK MS TB").astype(float).to_numpy()
    interaction = stage * uk
    reduced_x = np.column_stack([np.ones(len(frame)), stage, uk])
    full_x = np.column_stack([reduced_x, interaction])
    if np.linalg.matrix_rank(full_x) != full_x.shape[1]:
        raise RuntimeError("Rank-deficient interaction design")
    y = frame[MODULES].to_numpy(dtype=float)

    # QR plus einsum avoids a platform BLAS warning observed for direct
    # normal-equation matmul on otherwise finite, well-conditioned designs.
    full_q, full_r = np.linalg.qr(full_x, mode="reduced")
    reduced_q, reduced_r = np.linalg.qr(reduced_x, mode="reduced")
    full_pinv = np.linalg.solve(full_r, full_q.T.copy())
    full_hat = np.einsum("ik,kn->in", full_x, full_pinv)
    full_leverage = np.diag(full_hat)
    interaction_weights = full_pinv[3]
    reduced_pinv = np.linalg.solve(reduced_r, reduced_q.T.copy())
    reduced_fit = np.einsum("ik,km->im", reduced_x, reduced_pinv @ y)
    reduced_residual = y - reduced_fit

    observed_rows: list[dict[str, Any]] = []
    observed_t = np.zeros(len(MODULES), dtype=float)
    for index, module in enumerate(MODULES):
        fit = hc3_fit(y[:, index], full_x, 3)
        observed_t[index] = fit["t"]
        observed_rows.append(
            {
                "module": module,
                "interaction_beta_uk_minus_amsterdam": fit["beta"],
                "hc3_ci_low": fit["ci_low"],
                "hc3_ci_high": fit["ci_high"],
                "hc3_p": fit["p"],
            }
        )

    aggregate_exceed = np.zeros(len(MODULES), dtype=np.int64)
    aggregate_max_exceed = np.zeros(len(MODULES), dtype=np.int64)
    seed_rows: list[dict[str, Any]] = []
    hc3_weight = (interaction_weights / (1.0 - full_leverage)) ** 2
    for seed in SEEDS:
        rng = np.random.default_rng(seed)
        seed_exceed = np.zeros(len(MODULES), dtype=np.int64)
        seed_max_exceed = np.zeros(len(MODULES), dtype=np.int64)
        completed = 0
        while completed < N_PER_SEED:
            batch = min(BATCH, N_PER_SEED - completed)
            signs = rng.choice(np.array([-1.0, 1.0]), size=(batch, len(frame), 1))
            y_star = reduced_fit[None, :, :] + signs * reduced_residual[None, :, :]
            coefficients = np.einsum("kn,bnm->bkm", full_pinv, y_star)
            fitted = np.einsum("nk,bkm->bnm", full_x, coefficients)
            residual = y_star - fitted
            variances = np.einsum("n,bnm->bm", hc3_weight, residual**2)
            if np.any(variances <= 0) or not np.isfinite(variances).all():
                raise RuntimeError("Invalid wild-bootstrap HC3 variance")
            t_star = coefficients[:, 3, :] / np.sqrt(variances)
            absolute = np.abs(t_star)
            seed_exceed += np.sum(absolute >= np.abs(observed_t)[None, :], axis=0)
            null_max = np.max(absolute, axis=1)
            seed_max_exceed += np.sum(
                null_max[:, None] >= np.abs(observed_t)[None, :], axis=0
            )
            completed += batch
        aggregate_exceed += seed_exceed
        aggregate_max_exceed += seed_max_exceed
        for index, module in enumerate(MODULES):
            seed_rows.append(
                {
                    "seed": seed,
                    "module": module,
                    "n_replicates": N_PER_SEED,
                    "interaction_wild_p": (1 + int(seed_exceed[index]))
                    / (N_PER_SEED + 1),
                    "max_t_fwer_p": (1 + int(seed_max_exceed[index]))
                    / (N_PER_SEED + 1),
                }
            )

    total = len(SEEDS) * N_PER_SEED
    wild_p = (1 + aggregate_exceed) / (total + 1)
    max_p = (1 + aggregate_max_exceed) / (total + 1)
    q_values = bh(wild_p)

    source_rows: list[dict[str, Any]] = []
    for source in SOURCES:
        source_frame = frame[frame.source_family.eq(source)].copy()
        source_stage = source_frame.diagnosis.eq("SPMS").astype(float).to_numpy()
        source_x = sm.add_constant(source_stage)
        for module in MODULES:
            values = source_frame[module].to_numpy(dtype=float)
            full = hc3_fit(values, source_x, 1)
            lodo = []
            donors = source_frame.canonical_donor.tolist()
            for left_out in range(len(source_frame)):
                keep = np.arange(len(source_frame)) != left_out
                if np.unique(source_stage[keep]).size != 2:
                    continue
                fit = np.linalg.lstsq(source_x[keep], values[keep], rcond=None)[0]
                lodo.append(float(fit[1]))
            observed_sign = np.sign(full["beta"])
            source_rows.append(
                {
                    "module": module,
                    "source_family": source,
                    "n_donors": len(donors),
                    "n_ppms": int(np.sum(source_stage == 0)),
                    "n_spms": int(np.sum(source_stage == 1)),
                    "stage_beta": full["beta"],
                    "hc3_ci_low": full["ci_low"],
                    "hc3_ci_high": full["ci_high"],
                    "hc3_p": full["p"],
                    "lodo_min_beta": min(lodo),
                    "lodo_max_beta": max(lodo),
                    "lodo_same_sign_fraction": float(
                        np.mean(np.sign(np.asarray(lodo)) == observed_sign)
                    ),
                    "n_lodo": len(lodo),
                }
            )

    source_table = pd.DataFrame(source_rows)
    source_lookup = source_table.set_index(["module", "source_family"])
    test_rows: list[dict[str, Any]] = []
    for index, row in enumerate(observed_rows):
        amsterdam = source_lookup.loc[(row["module"], "Amsterdam BB")]
        uk_row = source_lookup.loc[(row["module"], "UK MS TB")]
        ci_excludes_zero = row["hc3_ci_low"] > 0 or row["hc3_ci_high"] < 0
        passes = bool(
            ci_excludes_zero
            and wild_p[index] <= 0.05
            and q_values[index] <= 0.10
            and max_p[index] <= 0.10
        )
        same_direction = bool(np.sign(amsterdam.stage_beta) == np.sign(uk_row.stage_beta))
        test_rows.append(
            {
                **row,
                "interaction_wild_p": float(wild_p[index]),
                "bh_q": float(q_values[index]),
                "max_t_fwer_p": float(max_p[index]),
                "amsterdam_stage_beta": float(amsterdam.stage_beta),
                "uk_stage_beta": float(uk_row.stage_beta),
                "source_direction_concordant": same_direction,
                "passes_frozen_interaction_gate": passes,
                "outcome": (
                    "supported_context_heterogeneity"
                    if passes
                    else "interaction_not_supported"
                    if row["hc3_p"] > 0.20 and wild_p[index] > 0.20
                    else "interaction_inconclusive"
                ),
            }
        )

    tests = pd.DataFrame(test_rows)
    tests.to_csv(OUT / "interaction_tests.tsv", sep="\t", index=False)
    source_table.to_csv(OUT / "source_effects_lodo.tsv", sep="\t", index=False)
    pd.DataFrame(seed_rows).to_csv(OUT / "seed_stability.tsv", sep="\t", index=False)
    supported = tests.loc[tests.passes_frozen_interaction_gate, "module"].tolist()
    summary = {
        "purpose": "Frozen source-by-stage audit; cross-sectional context only",
        "n_donors": len(frame),
        "n_modules": len(MODULES),
        "seeds": SEEDS,
        "null_replicates": total,
        "supported_context_interactions": supported,
        "n_supported_context_interactions": len(supported),
        "overall_verdict": (
            "supported_source_tissue_context_heterogeneity"
            if supported
            else "no_supported_source_tissue_interaction"
        ),
        "boundary": (
            "Source and tissue are inseparable; this audit cannot establish temporal "
            "progression, transition, causality, or intervention direction."
        ),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")

    lines = [
        "# V54 Progressive-Stage Source-Interaction Audit",
        "",
        f"Verdict: **{summary['overall_verdict']}**.",
        "",
        f"The frozen five-module audit used {len(frame)} donor-level observations and "
        f"{total:,} reduced-model wild-bootstrap replicates. No interaction is called "
        "progression because source and tissue are inseparable.",
        "",
        "| module | Amsterdam beta | UK beta | UK-minus-Amsterdam interaction | 95% CI | wild p | max-T p | outcome |",
        "|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in test_rows:
        lines.append(
            f"| {row['module']} | {row['amsterdam_stage_beta']:.3f} | "
            f"{row['uk_stage_beta']:.3f} | "
            f"{row['interaction_beta_uk_minus_amsterdam']:.3f} | "
            f"{row['hc3_ci_low']:.3f} to {row['hc3_ci_high']:.3f} | "
            f"{row['interaction_wild_p']:.4f} | {row['max_t_fwer_p']:.4f} | "
            f"{row['outcome']} |"
        )
    lines.extend(
        [
            "",
            "Per-source HC3 intervals and leave-one-donor influence ranges are in "
            "`source_effects_lodo.tsv`. Same-sign effects are descriptive; they do not "
            "become portable merely because the formal interaction is not supported.",
            "",
            "This is a cross-sectional source/tissue sensitivity, not evidence about "
            "disability accumulation or a therapeutic control point.",
        ]
    )
    (OUT / "REPORT.md").write_text("\n".join(lines) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
