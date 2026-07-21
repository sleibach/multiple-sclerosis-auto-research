#!/usr/bin/env python3
"""Directly test post-result foamy-by-lesion heterogeneity for two endpoints."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import statsmodels.api as sm


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "analysis/v54_progression_lesion_module_panel/gse279972_panel_scores.tsv"
OUT = ROOT / "analysis/v54_foamy_lesion_heterogeneity"
ENDPOINTS = {
    "oxphos": "lysosomal_unique",
    "lysosomal_unique": "oxphos",
}
SEEDS = [54601, 54602, 54603]
N_PER_SEED = 100_000
BATCH = 2_500


def matrices(frame: pd.DataFrame, mutual: str) -> tuple[np.ndarray, np.ndarray]:
    stratum3 = frame["Lesion_type_6"].astype(str).eq("3").astype(float).to_numpy()
    foamy = frame["foamy"].to_numpy(float)
    reduced = np.column_stack(
        [
            np.ones(len(frame)),
            foamy,
            stratum3,
            frame["b_apc_composition"].to_numpy(float),
            frame["resident_microglia_identity"].to_numpy(float),
            frame["mims_deoverlapped"].to_numpy(float),
            frame[mutual].to_numpy(float),
        ]
    )
    full = np.insert(reduced, 3, foamy * stratum3, axis=1)
    return full, reduced


def fit(frame: pd.DataFrame, endpoint: str, mutual: str) -> dict[str, Any]:
    x, x0 = matrices(frame, mutual)
    if np.linalg.matrix_rank(x) != x.shape[1] or np.linalg.matrix_rank(x0) != x0.shape[1]:
        raise RuntimeError(f"Rank-deficient heterogeneity model for {endpoint}")
    y = frame[endpoint].to_numpy(float)
    # QR avoids a platform BLAS warning observed for normal-equation matmul on
    # this otherwise finite, well-conditioned interaction design.
    q, r = np.linalg.qr(x, mode="reduced")
    q0, r0 = np.linalg.qr(x0, mode="reduced")
    pinv = np.linalg.solve(r, q.T.copy())
    pinv0 = np.linalg.solve(r0, q0.T.copy())
    model = sm.OLS(y, x).fit(
        cov_type="cluster",
        cov_kwds={"groups": frame["donor"].astype(str), "use_correction": True},
    )
    ci = model.conf_int()[3]
    observed = float(pinv[3] @ y)
    assert np.isclose(observed, model.params[3], atol=1e-10)
    fitted0 = x0 @ (pinv0 @ y)
    return {
        "interaction_beta": observed,
        "cluster_ci_low": float(ci[0]),
        "cluster_ci_high": float(ci[1]),
        "cluster_p": float(model.pvalues[3]),
        "design_condition": float(np.linalg.cond(x)),
        "beta_weight": pinv[3],
        "fitted0": fitted0,
        "residual0": y - fitted0,
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    full_frame = pd.read_csv(INPUT, sep="\t")
    frame = full_frame.loc[
        full_frame["Lesion_type_6"].astype(str).isin(["2", "3"])
    ].reset_index(drop=True)
    assert len(frame) == 35 and frame["donor"].nunique() == 21

    models = []
    rows = []
    for endpoint, mutual in ENDPOINTS.items():
        result = fit(frame, endpoint, mutual)
        models.append(result)
        rows.append(
            {
                "endpoint": endpoint,
                "mutual_covariate": mutual,
                "n_samples": len(frame),
                "n_donors": frame["donor"].nunique(),
                **{key: value for key, value in result.items() if key not in {"beta_weight", "fitted0", "residual0"}},
            }
        )

    donor_codes, donors = pd.factorize(frame["donor"].astype(str), sort=True)
    observed = np.asarray([model["interaction_beta"] for model in models])
    aggregate_exceed = np.zeros(len(models), dtype=np.int64)
    aggregate_max = np.zeros(len(models), dtype=np.int64)
    seed_rows = []
    for seed in SEEDS:
        rng = np.random.default_rng(seed)
        seed_exceed = np.zeros(len(models), dtype=np.int64)
        seed_max = np.zeros(len(models), dtype=np.int64)
        completed = 0
        while completed < N_PER_SEED:
            batch = min(BATCH, N_PER_SEED - completed)
            signs = rng.choice([-1.0, 1.0], size=(batch, len(donors)))[:, donor_codes]
            null = np.empty((batch, len(models)), dtype=float)
            for index, model in enumerate(models):
                synthetic = model["fitted0"][None, :] + signs * model["residual0"][None, :]
                null[:, index] = np.einsum("i,bi->b", model["beta_weight"], synthetic)
            absolute = np.abs(null)
            seed_exceed += np.sum(absolute >= np.abs(observed)[None, :], axis=0)
            maximum = absolute.max(axis=1)
            seed_max += np.sum(maximum[:, None] >= np.abs(observed)[None, :], axis=0)
            completed += batch
        aggregate_exceed += seed_exceed
        aggregate_max += seed_max
        for index, endpoint in enumerate(ENDPOINTS):
            seed_rows.append(
                {
                    "seed": seed,
                    "endpoint": endpoint,
                    "n_replicates": N_PER_SEED,
                    "donor_wild_p": (1 + seed_exceed[index]) / (N_PER_SEED + 1),
                    "max_family_p": (1 + seed_max[index]) / (N_PER_SEED + 1),
                }
            )
    total = len(SEEDS) * N_PER_SEED
    wild_p = (1 + aggregate_exceed) / (total + 1)
    max_p = (1 + aggregate_max) / (total + 1)

    leave_rows = []
    for endpoint, mutual in ENDPOINTS.items():
        for donor in donors:
            leave = frame.loc[frame["donor"].astype(str).ne(str(donor))].reset_index(drop=True)
            try:
                estimate = fit(leave, endpoint, mutual)["interaction_beta"]
                status = "estimated"
            except (RuntimeError, np.linalg.LinAlgError, ValueError):
                estimate = np.nan
                status = "not_estimable"
            leave_rows.append(
                {
                    "endpoint": endpoint,
                    "left_out_donor": donor,
                    "status": status,
                    "interaction_beta": estimate,
                }
            )
    leave = pd.DataFrame(leave_rows)
    leave.to_csv(OUT / "leave_one_donor.tsv", sep="\t", index=False)

    for index, row in enumerate(rows):
        estimates = leave.loc[
            leave["endpoint"].eq(row["endpoint"]) & leave["status"].eq("estimated"),
            "interaction_beta",
        ]
        observed_sign = np.sign(row["interaction_beta"])
        row["donor_wild_p"] = float(wild_p[index])
        row["max_family_p"] = float(max_p[index])
        row["n_lodo_estimable"] = len(estimates)
        row["lodo_min_beta"] = float(estimates.min())
        row["lodo_max_beta"] = float(estimates.max())
        row["lodo_direction_retained"] = bool(np.all(np.sign(estimates) == observed_sign))
        row["heterogeneity_gate_pass"] = bool(
            (row["cluster_ci_low"] > 0 or row["cluster_ci_high"] < 0)
            and row["donor_wild_p"] <= 0.05
            and row["max_family_p"] <= 0.10
            and row["lodo_direction_retained"]
        )
        row["outcome"] = (
            "post_result_heterogeneity_supported"
            if row["heterogeneity_gate_pass"]
            else "heterogeneity_not_supported"
        )
    tests = pd.DataFrame(rows)
    tests.to_csv(OUT / "interaction_tests.tsv", sep="\t", index=False)
    pd.DataFrame(seed_rows).to_csv(OUT / "seed_stability.tsv", sep="\t", index=False)

    supported = tests.loc[tests["heterogeneity_gate_pass"], "endpoint"].tolist()
    summary = {
        "purpose": "Post-result direct foamy-by-lesion heterogeneity test",
        "lesion_classes": ["2", "3"],
        "n_samples": len(frame),
        "n_donors": len(donors),
        "n_donor_wild_replicates": total,
        "heterogeneity_supported_endpoints": supported,
        "verdict": "POST_RESULT_HETEROGENEITY_SUPPORTED" if supported else "HETEROGENEITY_NOT_SUPPORTED",
        "boundary": (
            "Triggered by same-data stratum transport result; no independent confirmation, "
            "homogeneity, equivalence, progression, causal, or treatment inference."
        ),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")

    report = [
        "# V54 Foamy Morphology-By-Lesion Heterogeneity",
        "",
        f"Verdict: **{summary['verdict']}**.",
        "",
        "The interaction is class-3 minus class-2 foamy-effect heterogeneity.",
        "",
        "| endpoint | interaction beta | clustered 95% CI | wild p | max-family p | LODO stable | outcome |",
        "|---|---:|---:|---:|---:|---|---|",
    ]
    for row in rows:
        report.append(
            "| {endpoint} | {interaction_beta:.3f} | [{cluster_ci_low:.3f}, "
            "{cluster_ci_high:.3f}] | {donor_wild_p:.4g} | {max_family_p:.4g} | "
            "{lodo_direction_retained} | {outcome} |".format(**row)
        )
    report.extend(
        [
            "",
            "This direct test avoids treating different subgroup p-values as an",
            "interaction. Because it was triggered by those same subgroup results, even a",
            "pass would remain post-result until independent replication. A failure does",
            "not establish homogeneous effects or equivalence.",
        ]
    )
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
