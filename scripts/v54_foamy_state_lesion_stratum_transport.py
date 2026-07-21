#!/usr/bin/env python3
"""Test whether the fixed foamy-state endpoints transport across lesion strata."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import statsmodels.api as sm


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "analysis/v54_progression_lesion_module_panel/gse279972_panel_scores.tsv"
OUT = ROOT / "analysis/v54_foamy_state_lesion_stratum_transport"
ENDPOINTS = {
    "oxphos": {"mutual": "lysosomal_unique", "expected_sign": -1},
    "lysosomal_unique": {"mutual": "oxphos", "expected_sign": 1},
}
SEEDS = [54501, 54502, 54503]
N_PER_SEED = 100_000
BATCH = 2_500


def design(frame: pd.DataFrame, mutual: str) -> tuple[np.ndarray, np.ndarray]:
    reduced = np.column_stack(
        [
            np.ones(len(frame)),
            frame["b_apc_composition"].to_numpy(float),
            frame["resident_microglia_identity"].to_numpy(float),
            frame["mims_deoverlapped"].to_numpy(float),
            frame[mutual].to_numpy(float),
        ]
    )
    full = np.insert(reduced, 1, frame["foamy"].to_numpy(float), axis=1)
    return full, reduced


def fit(frame: pd.DataFrame, endpoint: str, mutual: str) -> dict[str, Any]:
    x, x0 = design(frame, mutual)
    if np.linalg.matrix_rank(x) != x.shape[1] or np.linalg.matrix_rank(x0) != x0.shape[1]:
        raise RuntimeError(f"Rank-deficient stratum model: {endpoint}")
    y = frame[endpoint].to_numpy(float)
    pinv = np.linalg.solve(x.T @ x, x.T)
    pinv0 = np.linalg.solve(x0.T @ x0, x0.T)
    model = sm.OLS(y, x).fit(
        cov_type="cluster",
        cov_kwds={"groups": frame["donor"].astype(str), "use_correction": True},
    )
    ci = model.conf_int()[1]
    observed = float(pinv[1] @ y)
    assert np.isclose(observed, model.params[1], atol=1e-10)
    fitted0 = x0 @ (pinv0 @ y)
    return {
        "observed": observed,
        "cluster_ci_low": float(ci[0]),
        "cluster_ci_high": float(ci[1]),
        "cluster_p": float(model.pvalues[1]),
        "condition": float(np.linalg.cond(x)),
        "beta_weight": pinv[1],
        "fitted0": fitted0,
        "residual0": y - fitted0,
        "donors": frame["donor"].astype(str).to_numpy(),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    frame = pd.read_csv(INPUT, sep="\t")
    required = {
        "gsm", "donor", "Lesion_type_6", "foamy", "b_apc_composition",
        "resident_microglia_identity", "mims_deoverlapped", "oxphos",
        "lysosomal_unique",
    }
    missing = sorted(required - set(frame.columns))
    if missing:
        raise RuntimeError(f"Missing fields: {missing}")
    assert len(frame) == 54 and frame["donor"].nunique() == 21

    eligibility_rows = []
    eligible: list[str] = []
    for stratum, subset in frame.groupby(frame["Lesion_type_6"].astype(str), sort=True):
        morphology_donors = subset.groupby("foamy")["donor"].nunique().to_dict()
        conditions = []
        full_rank = True
        for endpoint, spec in ENDPOINTS.items():
            x, x0 = design(subset, spec["mutual"])
            full_rank = full_rank and (
                np.linalg.matrix_rank(x) == x.shape[1]
                and np.linalg.matrix_rank(x0) == x0.shape[1]
            )
            conditions.append(float(np.linalg.cond(x)))
        passes = all(
            [
                subset["donor"].nunique() >= 12,
                morphology_donors.get(0, 0) >= 5,
                morphology_donors.get(1, 0) >= 5,
                full_rank,
                max(conditions) <= 30,
            ]
        )
        if passes:
            eligible.append(stratum)
        eligibility_rows.append(
            {
                "lesion_stratum": stratum,
                "n_samples": len(subset),
                "n_donors": subset["donor"].nunique(),
                "n_nonfoamy_donors": morphology_donors.get(0, 0),
                "n_foamy_donors": morphology_donors.get(1, 0),
                "full_rank_both_endpoints": full_rank,
                "max_design_condition": max(conditions),
                "eligible": passes,
                "reason": "passes frozen metadata/design gate" if passes else "fails frozen donor/morphology/design gate",
            }
        )
    eligibility = pd.DataFrame(eligibility_rows)
    eligibility.to_csv(OUT / "stratum_eligibility.tsv", sep="\t", index=False)
    assert eligible == ["2", "3"], eligible

    tests: list[dict[str, Any]] = []
    models: list[dict[str, Any]] = []
    for stratum in eligible:
        subset = frame.loc[frame["Lesion_type_6"].astype(str).eq(stratum)].reset_index(drop=True)
        for endpoint, spec in ENDPOINTS.items():
            result = fit(subset, endpoint, spec["mutual"])
            models.append({"stratum": stratum, "endpoint": endpoint, **result})
            tests.append(
                {
                    "lesion_stratum": stratum,
                    "endpoint": endpoint,
                    "mutual_covariate": spec["mutual"],
                    "expected_sign": spec["expected_sign"],
                    "n_samples": len(subset),
                    "n_donors": subset["donor"].nunique(),
                    "foamy_beta": result["observed"],
                    "cluster_ci_low": result["cluster_ci_low"],
                    "cluster_ci_high": result["cluster_ci_high"],
                    "cluster_p": result["cluster_p"],
                    "design_condition": result["condition"],
                }
            )

    global_donors = sorted(frame["donor"].astype(str).unique())
    donor_index = {donor: index for index, donor in enumerate(global_donors)}
    model_donor_codes = [
        np.asarray([donor_index[donor] for donor in model["donors"]], dtype=int)
        for model in models
    ]
    observed = np.asarray([model["observed"] for model in models])
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
            donor_signs = rng.choice([-1.0, 1.0], size=(batch, len(global_donors)))
            null = np.empty((batch, len(models)), dtype=float)
            for index, model in enumerate(models):
                signs = donor_signs[:, model_donor_codes[index]]
                synthetic = model["fitted0"][None, :] + signs * model["residual0"][None, :]
                null[:, index] = np.einsum("i,bi->b", model["beta_weight"], synthetic)
            absolute = np.abs(null)
            seed_exceed += np.sum(absolute >= np.abs(observed)[None, :], axis=0)
            maximum = absolute.max(axis=1)
            seed_max += np.sum(maximum[:, None] >= np.abs(observed)[None, :], axis=0)
            completed += batch
        aggregate_exceed += seed_exceed
        aggregate_max += seed_max
        for index, model in enumerate(models):
            seed_rows.append(
                {
                    "seed": seed,
                    "lesion_stratum": model["stratum"],
                    "endpoint": model["endpoint"],
                    "n_replicates": N_PER_SEED,
                    "donor_wild_p": (1 + seed_exceed[index]) / (N_PER_SEED + 1),
                    "max_family_p": (1 + seed_max[index]) / (N_PER_SEED + 1),
                }
            )
    total = len(SEEDS) * N_PER_SEED
    wild_p = (1 + aggregate_exceed) / (total + 1)
    max_p = (1 + aggregate_max) / (total + 1)

    leave_rows = []
    for model, row in zip(models, tests):
        stratum = model["stratum"]
        endpoint = model["endpoint"]
        mutual = ENDPOINTS[endpoint]["mutual"]
        subset = frame.loc[frame["Lesion_type_6"].astype(str).eq(stratum)].reset_index(drop=True)
        for donor in sorted(subset["donor"].astype(str).unique()):
            leave = subset.loc[subset["donor"].astype(str).ne(donor)].reset_index(drop=True)
            try:
                estimate = fit(leave, endpoint, mutual)["observed"]
                status = "estimated"
            except (RuntimeError, np.linalg.LinAlgError, ValueError):
                estimate = np.nan
                status = "not_estimable"
            leave_rows.append(
                {
                    "lesion_stratum": stratum,
                    "endpoint": endpoint,
                    "left_out_donor": donor,
                    "status": status,
                    "foamy_beta": estimate,
                }
            )
    leave = pd.DataFrame(leave_rows)
    leave.to_csv(OUT / "leave_one_donor.tsv", sep="\t", index=False)

    for index, row in enumerate(tests):
        estimates = leave.loc[
            leave["lesion_stratum"].eq(row["lesion_stratum"])
            & leave["endpoint"].eq(row["endpoint"])
            & leave["status"].eq("estimated"),
            "foamy_beta",
        ]
        expected = int(row["expected_sign"])
        row["donor_wild_p"] = float(wild_p[index])
        row["max_family_p"] = float(max_p[index])
        row["n_lodo_estimable"] = len(estimates)
        row["lodo_min_beta"] = float(estimates.min())
        row["lodo_max_beta"] = float(estimates.max())
        row["lodo_expected_direction_retained"] = bool(
            np.all(np.sign(estimates) == expected)
        )
        row["stratum_gate_pass"] = bool(
            np.sign(row["foamy_beta"]) == expected
            and (row["cluster_ci_low"] > 0 or row["cluster_ci_high"] < 0)
            and row["donor_wild_p"] <= 0.05
            and row["max_family_p"] <= 0.10
            and row["lodo_expected_direction_retained"]
        )
    tests_frame = pd.DataFrame(tests)
    tests_frame.to_csv(OUT / "stratum_tests.tsv", sep="\t", index=False)
    pd.DataFrame(seed_rows).to_csv(OUT / "seed_stability.tsv", sep="\t", index=False)

    endpoint_rows = []
    for endpoint in ENDPOINTS:
        selected = tests_frame.loc[tests_frame["endpoint"].eq(endpoint)]
        passes = bool(len(selected) == len(eligible) and selected["stratum_gate_pass"].all())
        endpoint_rows.append(
            {
                "endpoint": endpoint,
                "n_eligible_strata": len(selected),
                "n_expected_direction": int(
                    (np.sign(selected["foamy_beta"]) == ENDPOINTS[endpoint]["expected_sign"]).sum()
                ),
                "n_stratum_gate_pass": int(selected["stratum_gate_pass"].sum()),
                "transport_supported": passes,
            }
        )
    endpoint_frame = pd.DataFrame(endpoint_rows)
    endpoint_frame.to_csv(OUT / "endpoint_transport_verdicts.tsv", sep="\t", index=False)

    passed = endpoint_frame.loc[endpoint_frame["transport_supported"], "endpoint"].tolist()
    if len(passed) == len(ENDPOINTS):
        verdict = "BOTH_MORPHOLOGY_ASSOCIATIONS_TRANSPORT_ACROSS_ELIGIBLE_LESION_STRATA"
    elif passed:
        verdict = "PARTIAL_LESION_STRATUM_TRANSPORT"
    else:
        verdict = "NO_LESION_STRATUM_TRANSPORT_SUPPORTED"
    summary = {
        "purpose": "Post-result foamy-state lesion-stratum transport sensitivity",
        "eligible_strata": eligible,
        "ineligible_strata": eligibility.loc[~eligibility["eligible"], "lesion_stratum"].tolist(),
        "n_endpoints": len(ENDPOINTS),
        "n_tests": len(tests_frame),
        "n_donor_wild_replicates": total,
        "transport_supported_endpoints": passed,
        "verdict": verdict,
        "boundary": (
            "Within-cohort morphology transport only; no progression, flux, causal, "
            "target, or treatment-direction inference."
        ),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")

    report = [
        "# V54 Foamy-State Lesion-Stratum Transport",
        "",
        f"Verdict: **{verdict}**.",
        "",
        "Classes 2 and 3 passed the frozen pre-score eligibility rule; NAWM was",
        "ineligible because only four foamy donors were available.",
        "",
        "| stratum | endpoint | beta | clustered 95% CI | wild p | max-family p | LODO stable | gate |",
        "|---|---|---:|---:|---:|---:|---|---|",
    ]
    for row in tests:
        report.append(
            "| {lesion_stratum} | {endpoint} | {foamy_beta:.3f} | "
            "[{cluster_ci_low:.3f}, {cluster_ci_high:.3f}] | {donor_wild_p:.4g} | "
            "{max_family_p:.4g} | {lodo_expected_direction_retained} | "
            "{stratum_gate_pass} |".format(**row)
        )
    report.extend(
        [
            "",
            "This sensitivity asks whether the pooled morphology associations survive",
            "lesion-class restriction. It does not identify longitudinal progression,",
            "metabolic or lysosomal flux, causality, or an intervention direction.",
        ]
    )
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
