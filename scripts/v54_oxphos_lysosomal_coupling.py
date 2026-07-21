#!/usr/bin/env python3
"""Run the frozen post-result OXPHOS/lysosomal morphology sensitivity."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import statsmodels.api as sm


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "analysis/v54_progression_lesion_module_panel/gse279972_panel_scores.tsv"
OUT = ROOT / "analysis/v54_oxphos_lysosomal_coupling"
ENDPOINTS = {
    "oxphos": {"outcome": "oxphos", "mutual_covariate": "lysosomal_unique"},
    "lysosomal_unique": {"outcome": "lysosomal_unique", "mutual_covariate": "oxphos"},
}
SEEDS = [54401, 54402, 54403]
N_PER_SEED = 100_000
BATCH = 2_500


def design(frame: pd.DataFrame, mutual: str | None) -> tuple[np.ndarray, np.ndarray, list[str]]:
    lesion = pd.get_dummies(
        frame.Lesion_type_6.astype(str), prefix="lesion", drop_first=True, dtype=float
    )
    reduced = pd.DataFrame(
        {
            "intercept": np.ones(len(frame)),
            "b_apc_composition": frame.b_apc_composition.to_numpy(dtype=float),
            "resident_microglia_identity": frame.resident_microglia_identity.to_numpy(dtype=float),
            "mims_deoverlapped": frame.mims_deoverlapped.to_numpy(dtype=float),
        }
    )
    if mutual is not None:
        reduced[mutual] = frame[mutual].to_numpy(dtype=float)
    reduced = pd.concat([reduced, lesion.reset_index(drop=True)], axis=1)
    full = reduced.copy()
    full.insert(1, "foamy", frame.foamy.to_numpy(dtype=float))
    x = full.to_numpy(dtype=float)
    x0 = reduced.to_numpy(dtype=float)
    if np.linalg.matrix_rank(x) != x.shape[1] or np.linalg.matrix_rank(x0) != x0.shape[1]:
        raise RuntimeError(f"Rank-deficient coupling design with mutual={mutual}")
    return x, x0, full.columns.tolist()


def fit_model(frame: pd.DataFrame, outcome: str, mutual: str | None) -> dict[str, Any]:
    x, x0, columns = design(frame, mutual)
    y = frame[outcome].to_numpy(dtype=float)
    pinv = np.linalg.solve(x.T @ x, x.T)
    pinv0 = np.linalg.solve(x0.T @ x0, x0.T)
    observed = float(pinv[1] @ y)
    model = sm.OLS(y, x).fit(
        cov_type="cluster",
        cov_kwds={"groups": frame.donor.astype(str), "use_correction": True},
    )
    ci = model.conf_int()[1]
    if not np.isclose(observed, model.params[1], atol=1e-10):
        raise RuntimeError(f"Coefficient mismatch for {outcome}, mutual={mutual}")
    fitted0 = x0 @ (pinv0 @ y)
    return {
        "x": x,
        "y": y,
        "beta_weight": pinv[1],
        "fitted0": fitted0,
        "residual0": y - fitted0,
        "observed": observed,
        "cluster_ci_low": float(ci[0]),
        "cluster_ci_high": float(ci[1]),
        "cluster_p": float(model.pvalues[1]),
        "design_columns": columns,
        "design_condition": float(np.linalg.cond(x)),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    frame = pd.read_csv(INPUT, sep="\t")
    required = {
        "foamy", "donor", "Lesion_type_6", "b_apc_composition",
        "resident_microglia_identity", "mims_deoverlapped", "oxphos",
        "lysosomal_unique",
    }
    missing = sorted(required - set(frame.columns))
    if missing:
        raise RuntimeError(f"Missing coupling fields: {missing}")
    if len(frame) != 54 or frame.donor.nunique() != 21:
        raise RuntimeError("Coupling cohort does not reproduce 54 samples / 21 donors")

    source_oxphos = pd.read_csv(
        ROOT / "analysis/v54_progression_lesion_module_panel/gse279972_morphology_tests.tsv",
        sep="\t",
    ).set_index("module").loc["oxphos", "foamy_adjusted_beta"]
    source_lysosomal = pd.read_csv(
        ROOT / "analysis/v54_lysosomal_morphology_specificity/specificity_models.tsv",
        sep="\t",
    ).set_index("model").loc["resident_and_mims_adjusted", "foamy_adjusted_beta"]
    expected = {"oxphos": float(source_oxphos), "lysosomal_unique": float(source_lysosomal)}

    models: dict[str, dict[str, Any]] = {}
    rows: list[dict[str, Any]] = []
    for name, spec in ENDPOINTS.items():
        base = fit_model(frame, str(spec["outcome"]), None)
        if not np.isclose(base["observed"], expected[name], atol=1e-10):
            raise RuntimeError(f"{name} base coefficient does not reproduce its committed source")
        mutual = fit_model(frame, str(spec["outcome"]), str(spec["mutual_covariate"]))
        models[name] = mutual
        rows.append(
            {
                "endpoint": name,
                "outcome": spec["outcome"],
                "mutual_covariate": spec["mutual_covariate"],
                "base_foamy_beta": base["observed"],
                "mutual_adjusted_foamy_beta": mutual["observed"],
                "beta_retention_fraction": mutual["observed"] / base["observed"],
                "cluster_ci_low": mutual["cluster_ci_low"],
                "cluster_ci_high": mutual["cluster_ci_high"],
                "cluster_p": mutual["cluster_p"],
                "design_condition": mutual["design_condition"],
            }
        )

    donor_codes, donors = pd.factorize(frame.donor.astype(str), sort=True)
    names = list(ENDPOINTS)
    aggregate_exceed = np.zeros(len(names), dtype=np.int64)
    aggregate_max = np.zeros(len(names), dtype=np.int64)
    seed_rows: list[dict[str, Any]] = []
    for seed in SEEDS:
        rng = np.random.default_rng(seed)
        seed_exceed = np.zeros(len(names), dtype=np.int64)
        seed_max = np.zeros(len(names), dtype=np.int64)
        completed = 0
        while completed < N_PER_SEED:
            batch = min(BATCH, N_PER_SEED - completed)
            donor_signs = rng.choice([-1.0, 1.0], size=(batch, len(donors)))
            signs = donor_signs[:, donor_codes]
            null = np.empty((batch, len(names)), dtype=float)
            for index, name in enumerate(names):
                model = models[name]
                synthetic = (
                    model["fitted0"][None, :] + signs * model["residual0"][None, :]
                )
                null[:, index] = np.einsum("i,bi->b", model["beta_weight"], synthetic)
            if not np.isfinite(null).all():
                raise RuntimeError("Non-finite OXPHOS/lysosomal coupling null")
            absolute = np.abs(null)
            observed = np.asarray([models[name]["observed"] for name in names])
            seed_exceed += np.sum(absolute >= np.abs(observed)[None, :], axis=0)
            max_abs = absolute.max(axis=1)
            seed_max += np.sum(max_abs[:, None] >= np.abs(observed)[None, :], axis=0)
            completed += batch
        aggregate_exceed += seed_exceed
        aggregate_max += seed_max
        for index, name in enumerate(names):
            seed_rows.append(
                {
                    "seed": seed,
                    "endpoint": name,
                    "n_wild_replicates": N_PER_SEED,
                    "donor_wild_p": (1 + int(seed_exceed[index])) / (N_PER_SEED + 1),
                    "max_endpoint_fwer_p": (1 + int(seed_max[index])) / (N_PER_SEED + 1),
                }
            )
    total = len(SEEDS) * N_PER_SEED
    p = (1 + aggregate_exceed) / (total + 1)
    max_p = (1 + aggregate_max) / (total + 1)

    leave_rows: list[dict[str, Any]] = []
    for name, spec in ENDPOINTS.items():
        for donor in donors:
            keep = frame.donor.astype(str).ne(str(donor)).to_numpy()
            leave_frame = frame.loc[keep].reset_index(drop=True)
            try:
                x, _, _ = design(leave_frame, str(spec["mutual_covariate"]))
                y = leave_frame[str(spec["outcome"])].to_numpy(dtype=float)
                beta = float(np.linalg.solve(x.T @ x, x.T)[1] @ y)
                status = "estimated"
            except (RuntimeError, np.linalg.LinAlgError):
                beta = np.nan
                status = "rank_deficient"
            leave_rows.append(
                {
                    "endpoint": name,
                    "left_out_donor": donor,
                    "status": status,
                    "mutual_adjusted_foamy_beta": beta,
                }
            )
    leave = pd.DataFrame(leave_rows)
    leave.to_csv(OUT / "leave_one_donor.tsv", sep="\t", index=False)
    for index, item in enumerate(rows):
        estimated = leave[
            leave.endpoint.eq(item["endpoint"]) & leave.status.eq("estimated")
        ].mutual_adjusted_foamy_beta
        item["donor_wild_p"] = float(p[index])
        item["max_endpoint_fwer_p"] = float(max_p[index])
        item["leave_one_donor_min_beta"] = float(estimated.min())
        item["leave_one_donor_max_beta"] = float(estimated.max())
        item["leave_one_donor_direction_retained"] = bool(
            np.all(np.sign(estimated) == np.sign(item["mutual_adjusted_foamy_beta"]))
        )
        item["survives_mutual_adjustment"] = bool(
            (item["cluster_ci_low"] > 0 or item["cluster_ci_high"] < 0)
            and item["donor_wild_p"] <= 0.05
            and item["max_endpoint_fwer_p"] <= 0.10
            and item["leave_one_donor_direction_retained"]
        )
    tests = pd.DataFrame(rows)
    tests.to_csv(OUT / "mutual_adjustment_tests.tsv", sep="\t", index=False)
    pd.DataFrame(seed_rows).to_csv(OUT / "seed_stability.tsv", sep="\t", index=False)

    survived = tests.loc[tests.survives_mutual_adjustment, "endpoint"].tolist()
    if len(survived) == 2:
        verdict = "BOTH_MORPHOLOGY_ASSOCIATIONS_SEPARABLE_UNDER_TESTED_MODEL"
    elif len(survived) == 1:
        verdict = f"ONLY_{survived[0].upper()}_SURVIVES_MUTUAL_ADJUSTMENT"
    else:
        verdict = "BOTH_ASSOCIATIONS_ATTENUATE_UNDER_MUTUAL_ADJUSTMENT"
    summary = {
        "purpose": "Post-result OXPHOS/lysosomal foamy-morphology coupling sensitivity",
        "n_samples": len(frame),
        "n_donors": len(donors),
        "n_wild_replicates": total,
        "endpoints_surviving": survived,
        "verdict": verdict,
        "boundary": "Model separability is not independent biology, progression, causality, flux, or treatment evidence.",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    report = [
        "# V54 OXPHOS-Lysosomal Foamy-State Coupling",
        "",
        "> Later evidential-grade update: neither endpoint passes Holm correction across",
        "> the complete 12-test V54 post-result morphology sequence (both `p=0.0960`).",
        "> See `analysis/v54_post_result_morphology_multiplicity/REPORT.md`. The local",
        "> coefficients below remain reproducible, but the two-endpoint claim is",
        "> exploratory rather than globally gate-passing.",
        "",
        f"Verdict: **{verdict}**.",
        "",
        "This post-result sensitivity mutually adjusted the two disjoint transcript",
        "scores within the 54-sample, 21-donor GSE279972 morphology model.",
        "",
        "| endpoint | base beta | mutual-adjusted beta | retention | cluster CI | wild p | max-endpoint p | survives |",
        "|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for item in rows:
        report.append(
            "| {endpoint} | {base_foamy_beta:.3f} | {mutual_adjusted_foamy_beta:.3f} | "
            "{beta_retention_fraction:.3f} | [{cluster_ci_low:.3f}, {cluster_ci_high:.3f}] | "
            "{donor_wild_p:.4g} | {max_endpoint_fwer_p:.4g} | "
            "{survives_mutual_adjustment} |".format(**item)
        )
    report.extend(
        [
            "",
            "Persistence means only that neither fixed transcript score statistically",
            "subsumes the other under these measured covariates. Both remain properties of",
            "one foamy-morphology cohort and lack orthogonal chronic-active-edge support.",
            "No progression, causal, metabolic-flux, target, or treatment inference follows.",
        ]
    )
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
