#!/usr/bin/env python3
"""Run the frozen V54 within-donor foamy-morphology estimand audit."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import statsmodels.api as sm


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "analysis/v54_progression_lesion_module_panel/gse279972_panel_scores.tsv"
INTERACTIONS = ROOT / "analysis/v54_foamy_lesion_heterogeneity/interaction_tests.tsv"
INTERACTION_LODO = ROOT / "analysis/v54_foamy_lesion_heterogeneity/leave_one_donor.tsv"
OUT = ROOT / "analysis/v54_foamy_donor_estimand_audit"
ENDPOINTS = {"oxphos": "lysosomal_unique", "lysosomal_unique": "oxphos"}
EXPECTED_SIGN = {"oxphos": -1, "lysosomal_unique": 1}
SEEDS = [54801, 54802, 54803]
N_PER_SEED = 100_000
BATCH = 1_500


def matrices(frame: pd.DataFrame, mutual: str) -> tuple[np.ndarray, np.ndarray, list[str]]:
    donor = pd.get_dummies(frame.donor, prefix="donor", drop_first=True, dtype=float)
    lesion = pd.get_dummies(
        frame.Lesion_type_6.astype(str), prefix="lesion", drop_first=True, dtype=float
    )
    reduced = pd.DataFrame(
        {
            "intercept": np.ones(len(frame)),
            "b_apc_composition": frame.b_apc_composition.to_numpy(float),
            "resident_microglia_identity": frame.resident_microglia_identity.to_numpy(float),
            "mims_deoverlapped": frame.mims_deoverlapped.to_numpy(float),
            mutual: frame[mutual].to_numpy(float),
        }
    )
    reduced = pd.concat(
        [reduced, lesion.reset_index(drop=True), donor.reset_index(drop=True)], axis=1
    )
    full = reduced.copy()
    full.insert(1, "foamy", frame.foamy.to_numpy(float))
    x = full.to_numpy(float)
    x0 = reduced.to_numpy(float)
    if np.linalg.matrix_rank(x) != x.shape[1] or np.linalg.matrix_rank(x0) != x0.shape[1]:
        raise RuntimeError(f"Rank-deficient donor-FE design with mutual={mutual}")
    return x, x0, full.columns.tolist()


def qr_pinv(x: np.ndarray) -> np.ndarray:
    q, r = np.linalg.qr(x, mode="reduced")
    return np.linalg.solve(r, q.T.copy())


def fit(frame: pd.DataFrame, endpoint: str, mutual: str) -> dict[str, Any]:
    x, x0, columns = matrices(frame, mutual)
    y = frame[endpoint].to_numpy(float)
    pinv = qr_pinv(x)
    pinv0 = qr_pinv(x0)
    model = sm.OLS(y, x).fit(cov_type="HC3")
    ci = model.conf_int()[1]
    observed = float(pinv[1] @ y)
    if not np.isclose(observed, model.params[1], atol=1e-9):
        raise RuntimeError(f"Coefficient mismatch for {endpoint}")
    fitted0 = np.einsum("ik,k->i", x0, pinv0 @ y)
    leverage = np.einsum("ik,ki->i", x, pinv)
    if np.any(leverage >= 1.0):
        raise RuntimeError(f"Invalid leverage for {endpoint}")
    return {
        "x": x,
        "pinv": pinv,
        "y": y,
        "observed": observed,
        "observed_t": float(model.tvalues[1]),
        "hc3_ci_low": float(ci[0]),
        "hc3_ci_high": float(ci[1]),
        "hc3_p": float(model.pvalues[1]),
        "fitted0": fitted0,
        "residual0": y - fitted0,
        "leverage": leverage,
        "columns": columns,
        "condition": float(np.linalg.cond(x)),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    frame = pd.read_csv(INPUT, sep="\t")
    required = {
        "donor",
        "Lesion_type_6",
        "morphology",
        "foamy",
        "b_apc_composition",
        "resident_microglia_identity",
        "mims_deoverlapped",
        *ENDPOINTS,
    }
    missing = sorted(required - set(frame.columns))
    if missing:
        raise RuntimeError(f"Missing fields: {missing}")
    if len(frame) != 54 or frame.donor.nunique() != 21:
        raise RuntimeError("Expected the committed 54-sample, 21-donor cohort")

    coverage = (
        frame.groupby(["donor", "Lesion_type_6", "morphology"])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )
    for label in ("foamy", "non_foamy"):
        if label not in coverage:
            coverage[label] = 0
    coverage["n_samples"] = coverage.foamy + coverage.non_foamy
    coverage["within_block_morphology_variation"] = (
        coverage.foamy.gt(0) & coverage.non_foamy.gt(0)
    )
    coverage.to_csv(OUT / "donor_lesion_morphology_coverage.tsv", sep="\t", index=False)

    donor_variation = frame.groupby("donor").foamy.nunique().eq(2)
    informative_donors = donor_variation[donor_variation].index.tolist()
    mixed_blocks = coverage[coverage.within_block_morphology_variation]
    mixed_keys = set(zip(mixed_blocks.donor, mixed_blocks.Lesion_type_6, strict=True))
    if len(informative_donors) != 6 or len(mixed_blocks) != 3:
        raise RuntimeError("Metadata coverage changed from the frozen plan")

    estimand_frame = frame[frame.donor.isin(informative_donors)].reset_index(drop=True)
    if len(estimand_frame) != 23:
        raise RuntimeError("Expected 23 samples from six morphology-varying donors")
    models = {
        endpoint: fit(estimand_frame, endpoint, mutual)
        for endpoint, mutual in ENDPOINTS.items()
    }
    donors = estimand_frame.donor.astype(str).to_numpy()
    unique_donors = sorted(estimand_frame.donor.astype(str).unique())
    aggregate_exceed = np.zeros(len(ENDPOINTS), dtype=np.int64)
    aggregate_max = np.zeros(len(ENDPOINTS), dtype=np.int64)
    seed_rows: list[dict[str, Any]] = []
    endpoint_names = list(ENDPOINTS)
    for seed in SEEDS:
        rng = np.random.default_rng(seed)
        seed_exceed = np.zeros(len(ENDPOINTS), dtype=np.int64)
        seed_max = np.zeros(len(ENDPOINTS), dtype=np.int64)
        completed = 0
        while completed < N_PER_SEED:
            batch = min(BATCH, N_PER_SEED - completed)
            donor_sign = rng.choice(
                np.array([-1.0, 1.0]), size=(batch, len(unique_donors))
            )
            sign_lookup = {donor: i for i, donor in enumerate(unique_donors)}
            signs = donor_sign[:, [sign_lookup[donor] for donor in donors]]
            t_null = np.zeros((batch, len(ENDPOINTS)), dtype=float)
            for endpoint_index, endpoint in enumerate(endpoint_names):
                result = models[endpoint]
                y_star = result["fitted0"][None, :] + signs * result["residual0"][None, :]
                coefficients = np.einsum("kn,bn->bk", result["pinv"], y_star)
                fitted = np.einsum("nk,bk->bn", result["x"], coefficients)
                residual = y_star - fitted
                weights = (
                    result["pinv"][1] / (1.0 - result["leverage"])
                ) ** 2
                variance = np.einsum("n,bn->b", weights, residual**2)
                if np.any(variance <= 0) or not np.isfinite(variance).all():
                    raise RuntimeError("Invalid donor-wild HC3 variance")
                t_null[:, endpoint_index] = coefficients[:, 1] / np.sqrt(variance)
            absolute = np.abs(t_null)
            observed = np.array(
                [abs(models[endpoint]["observed_t"]) for endpoint in endpoint_names]
            )
            seed_exceed += np.sum(absolute >= observed[None, :], axis=0)
            null_max = np.max(absolute, axis=1)
            seed_max += np.sum(null_max[:, None] >= observed[None, :], axis=0)
            completed += batch
        aggregate_exceed += seed_exceed
        aggregate_max += seed_max
        for index, endpoint in enumerate(endpoint_names):
            seed_rows.append(
                {
                    "seed": seed,
                    "endpoint": endpoint,
                    "n_replicates": N_PER_SEED,
                    "donor_wild_p": (1 + int(seed_exceed[index])) / (N_PER_SEED + 1),
                    "max_endpoint_p": (1 + int(seed_max[index])) / (N_PER_SEED + 1),
                }
            )

    total = len(SEEDS) * N_PER_SEED
    wild_p = (1 + aggregate_exceed) / (total + 1)
    max_p = (1 + aggregate_max) / (total + 1)
    lodo_rows: list[dict[str, Any]] = []
    test_rows: list[dict[str, Any]] = []
    for index, endpoint in enumerate(endpoint_names):
        result = models[endpoint]
        lodo_values = []
        for left_out in informative_donors:
            leave = estimand_frame[~estimand_frame.donor.eq(left_out)].reset_index(drop=True)
            leave_result = fit(leave, endpoint, ENDPOINTS[endpoint])
            beta = float(leave_result["observed"])
            lodo_values.append(beta)
            lodo_rows.append(
                {
                    "endpoint": endpoint,
                    "left_out_informative_donor": left_out,
                    "within_donor_foamy_beta": beta,
                }
            )
        expected = EXPECTED_SIGN[endpoint]
        retains = bool(np.sign(lodo_values).tolist().count(expected) == len(lodo_values))
        ci_excludes_zero = result["hc3_ci_low"] > 0 or result["hc3_ci_high"] < 0
        passes = bool(
            np.sign(result["observed"]) == expected
            and ci_excludes_zero
            and wild_p[index] <= 0.05
            and max_p[index] <= 0.10
            and retains
        )
        outcome = (
            "within_donor_supported_exploratory"
            if passes
            else "direction_retained_but_underpowered"
            if np.sign(result["observed"]) == expected
            else "substantially_between_donor_or_unresolved"
        )
        test_rows.append(
            {
                "endpoint": endpoint,
                "mutual_covariate": ENDPOINTS[endpoint],
                "n_samples": len(estimand_frame),
                "n_donors": estimand_frame.donor.nunique(),
                "n_informative_donors": len(informative_donors),
                "within_donor_foamy_beta": result["observed"],
                "hc3_ci_low": result["hc3_ci_low"],
                "hc3_ci_high": result["hc3_ci_high"],
                "hc3_p": result["hc3_p"],
                "donor_wild_p": float(wild_p[index]),
                "max_endpoint_p": float(max_p[index]),
                "design_condition": result["condition"],
                "informative_lodo_min_beta": min(lodo_values),
                "informative_lodo_max_beta": max(lodo_values),
                "informative_lodo_direction_retained": retains,
                "passes_frozen_within_donor_gate": passes,
                "outcome": outcome,
            }
        )

    block_rows: list[dict[str, Any]] = []
    for donor, lesion in sorted(mixed_keys):
        block = frame[
            frame.donor.eq(donor) & frame.Lesion_type_6.eq(lesion)
        ]
        for endpoint in endpoint_names:
            difference = (
                block.loc[block.foamy.eq(1), endpoint].mean()
                - block.loc[block.foamy.eq(0), endpoint].mean()
            )
            block_rows.append(
                {
                    "donor": donor,
                    "lesion_stratum": lesion,
                    "endpoint": endpoint,
                    "n_foamy": int(block.foamy.eq(1).sum()),
                    "n_nonfoamy": int(block.foamy.eq(0).sum()),
                    "foamy_minus_nonfoamy": float(difference),
                    "matches_pooled_direction": bool(
                        np.sign(difference) == EXPECTED_SIGN[endpoint]
                    ),
                }
            )

    interaction = pd.read_csv(INTERACTIONS, sep="\t").set_index("endpoint")
    interaction_lodo = pd.read_csv(INTERACTION_LODO, sep="\t")
    influence_rows: list[dict[str, Any]] = []
    for endpoint in endpoint_names:
        full = interaction.loc[endpoint]
        se = (float(full.cluster_ci_high) - float(full.cluster_ci_low)) / (2 * 1.96)
        subset = interaction_lodo[interaction_lodo.endpoint.eq(endpoint)]
        for row in subset.itertuples(index=False):
            change = (float(row.interaction_beta) - float(full.interaction_beta)) / se
            influence_rows.append(
                {
                    "endpoint": endpoint,
                    "left_out_donor": row.left_out_donor,
                    "full_interaction_beta": float(full.interaction_beta),
                    "lodo_interaction_beta": float(row.interaction_beta),
                    "standardized_deletion_change": change,
                    "interaction_sign_changed": bool(
                        np.sign(row.interaction_beta) != np.sign(full.interaction_beta)
                    ),
                    "absolute_change_exceeds_one_se": bool(abs(change) > 1),
                }
            )

    tests = pd.DataFrame(test_rows)
    tests.to_csv(OUT / "within_donor_tests.tsv", sep="\t", index=False)
    pd.DataFrame(lodo_rows).to_csv(OUT / "informative_donor_lodo.tsv", sep="\t", index=False)
    pd.DataFrame(block_rows).to_csv(OUT / "within_donor_lesion_block_differences.tsv", sep="\t", index=False)
    pd.DataFrame(influence_rows).to_csv(OUT / "interaction_donor_influence.tsv", sep="\t", index=False)
    pd.DataFrame(seed_rows).to_csv(OUT / "seed_stability.tsv", sep="\t", index=False)

    supported = tests.loc[tests.passes_frozen_within_donor_gate, "endpoint"].tolist()
    summary = {
        "purpose": "Within-donor estimand and influence audit of exploratory post-result morphology coefficients",
        "n_samples": len(frame),
        "n_donors": frame.donor.nunique(),
        "n_donors_with_both_morphologies": len(informative_donors),
        "n_donor_lesion_blocks": len(coverage),
        "n_blocks_with_both_morphologies": len(mixed_blocks),
        "n_wild_replicates": total,
        "supported_within_donor_endpoints": supported,
        "overall_verdict": (
            "within_donor_support_for_exploratory_endpoint"
            if supported
            else "within_donor_estimand_not_supported"
        ),
        "boundary": (
            "The audit cannot restore global family support or identify progression, "
            "causality, flux, or intervention direction."
        ),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")

    lines = [
        "# V54 Foamy Morphology Donor-Estimand Audit",
        "",
        f"Verdict: **{summary['overall_verdict']}**.",
        "",
        f"Only {len(informative_donors)}/21 donors contain both morphology labels and "
        f"only {len(mixed_blocks)}/43 donor-by-lesion blocks contain both labels. "
        "A donor-by-lesion Fisher test would be invalid for these repeated, "
        "multi-category observations; the frozen audit instead uses donor fixed effects.",
        "",
        "| endpoint | within-donor beta | HC3 CI | wild p | max-T p | informative LODO range | outcome |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in test_rows:
        lines.append(
            f"| {row['endpoint']} | {row['within_donor_foamy_beta']:.3f} | "
            f"{row['hc3_ci_low']:.3f} to {row['hc3_ci_high']:.3f} | "
            f"{row['donor_wild_p']:.4f} | {row['max_endpoint_p']:.4f} | "
            f"{row['informative_lodo_min_beta']:.3f} to "
            f"{row['informative_lodo_max_beta']:.3f} | {row['outcome']} |"
        )
    block_table = pd.DataFrame(block_rows)
    lines.extend(
        [
            "",
            "The three same-donor, same-lesion blocks are descriptive only; the minimum "
            "possible exact two-sided sign p-value is 0.25. Direction matches by endpoint: "
            + ", ".join(
                f"{endpoint} {int(block_table[block_table.endpoint.eq(endpoint)].matches_pooled_direction.sum())}/3"
                for endpoint in endpoint_names
            )
            + ".",
            "",
            "Donor-deletion changes for the earlier lesion interaction remain an influence "
            "diagnostic. A sign flip around an interaction already near zero does not "
            "establish donor-specific heterogeneity.",
            "",
            "This audit cannot restore the global family gate or support progression, "
            "disability, causal, flux, target, or therapeutic claims.",
        ]
    )
    (OUT / "REPORT.md").write_text("\n".join(lines) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
