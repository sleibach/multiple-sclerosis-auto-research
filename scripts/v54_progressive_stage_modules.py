#!/usr/bin/env python3
"""Run the frozen V54 source/tissue-balanced PPMS-versus-SPMS module test."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import statsmodels.api as sm


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "analysis/v53_ms_microglia_independent_cohort_scout/macnair_discovery/sample_scores.tsv"
SOURCE_MAP = ROOT / "analysis/v53_macnair_source_influence/discovery_donor_source_map.tsv"
OUT = ROOT / "analysis/v54_progressive_stage_modules"

MODULES = [
    "receptor_cd44_cxcr4",
    "hla_regulatory",
    "mif_ligand",
    "ifn_apc_unique",
    "lysosomal_unique",
]
SOURCE_TISSUE = {"Amsterdam BB": "WM", "UK MS TB": "GM"}
STAGES = ["PPMS", "SPMS"]
SEEDS = [54001, 54002, 54003]
N_PER_SEED = 100_000
BATCH = 2_500


def bh(values: list[float]) -> list[float]:
    p = np.asarray(values, dtype=float)
    order = np.argsort(p)
    adjusted = np.empty(len(p), dtype=float)
    running = 1.0
    for reverse_rank in range(len(p) - 1, -1, -1):
        index = order[reverse_rank]
        running = min(running, p[index] * len(p) / (reverse_rank + 1))
        adjusted[index] = running
    return adjusted.tolist()


def nuisance_residuals(frame: pd.DataFrame, module: str) -> tuple[pd.DataFrame, dict[str, Any]]:
    source = str(frame.source_family.iloc[0])
    age = frame.age_at_death.to_numpy(dtype=float)
    age_z = (age - age.mean()) / age.std(ddof=0)
    log_cells = np.log1p(frame.n_microglia.to_numpy(dtype=float))
    log_cells_z = (log_cells - log_cells.mean()) / log_cells.std(ddof=0)
    lesion = pd.get_dummies(frame.lesion_type, prefix="lesion", drop_first=True, dtype=float)
    design = pd.DataFrame(
        {
            "intercept": np.ones(len(frame)),
            "age_z": age_z,
            "age_z2": age_z**2,
            "sex_male": frame.sex.eq("M").astype(float).to_numpy(),
            "log_n_microglia_z": log_cells_z,
        },
        index=frame.index,
    )
    design = pd.concat([design, lesion.set_axis(frame.index)], axis=1)
    x = design.to_numpy(dtype=float)
    if np.linalg.matrix_rank(x) != x.shape[1]:
        raise RuntimeError(f"Rank-deficient nuisance design for {source} {module}")
    donor_n = frame.groupby("canonical_donor").size()
    weights = frame.canonical_donor.map(lambda donor: 1.0 / donor_n.loc[donor]).to_numpy()
    sqrt_w = np.sqrt(weights)
    y = frame[module].to_numpy(dtype=float)
    coefficients = np.linalg.lstsq(x * sqrt_w[:, None], y * sqrt_w, rcond=None)[0]
    residual = y - x @ coefficients
    donor = frame[["canonical_donor", "diagnosis", "source_family"]].copy()
    donor["residual"] = residual
    donor = donor.groupby("canonical_donor", as_index=False).agg(
        diagnosis=("diagnosis", "first"),
        source_family=("source_family", "first"),
        residual=("residual", "mean"),
        n_samples=("residual", "size"),
    )
    if donor.residual.std(ddof=0) == 0:
        raise RuntimeError(f"Zero donor residual variance for {source} {module}")
    donor["standardized_residual"] = (
        donor.residual - donor.residual.mean()
    ) / donor.residual.std(ddof=0)
    diagnostic = {
        "source_family": source,
        "matter": SOURCE_TISSUE[source],
        "module": module,
        "n_samples": len(frame),
        "n_donors": donor.canonical_donor.nunique(),
        "n_ppms": int(donor.diagnosis.eq("PPMS").sum()),
        "n_spms": int(donor.diagnosis.eq("SPMS").sum()),
        "lesion_contexts": ";".join(sorted(frame.lesion_type.unique())),
        "n_design_columns": x.shape[1],
        "design_rank": int(np.linalg.matrix_rank(x)),
        "design_condition": float(np.linalg.cond(x * sqrt_w[:, None])),
        "max_donor_samples": int(donor.n_samples.max()),
    }
    return donor, diagnostic


def source_effect(frame: pd.DataFrame, module: str) -> dict[str, Any]:
    y = frame[module].to_numpy(dtype=float)
    stage = frame.diagnosis.eq("SPMS").astype(float).to_numpy()
    model = sm.OLS(y, sm.add_constant(stage)).fit(cov_type="HC3")
    ci = model.conf_int()[1]
    return {
        "module": module,
        "source_family": str(frame.source_family.iloc[0]),
        "n_ppms": int(np.sum(stage == 0)),
        "n_spms": int(np.sum(stage == 1)),
        "spms_minus_ppms_standardized_beta": float(model.params[1]),
        "hc3_ci_low": float(ci[0]),
        "hc3_ci_high": float(ci[1]),
        "hc3_p": float(model.pvalues[1]),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sample = pd.read_csv(INPUT, sep="\t")
    source_map = pd.read_csv(SOURCE_MAP, sep="\t")
    sample = sample[sample.study.eq(sample.selected_source)].copy()
    sample = sample.merge(source_map, on="canonical_donor", validate="many_to_one")
    sample = sample[
        sample.diagnosis.isin(STAGES) & sample.source_family.isin(SOURCE_TISSUE)
    ].copy()
    sample = sample[
        sample.apply(lambda row: row.matter == SOURCE_TISSUE[row.source_family], axis=1)
    ].copy()
    missing = [module for module in MODULES if module not in sample.columns]
    if missing:
        raise RuntimeError(f"Missing frozen modules: {missing}")

    source_donor_frames: list[pd.DataFrame] = []
    diagnostics: list[dict[str, Any]] = []
    for source in SOURCE_TISSUE:
        source_frame = sample[sample.source_family.eq(source)].copy()
        source_donor: pd.DataFrame | None = None
        for module in MODULES:
            donor, diagnostic = nuisance_residuals(source_frame, module)
            donor = donor.rename(columns={"standardized_residual": module})
            donor = donor[["canonical_donor", "diagnosis", "source_family", module]]
            if source_donor is None:
                source_donor = donor
            else:
                source_donor = source_donor.merge(
                    donor,
                    on=["canonical_donor", "diagnosis", "source_family"],
                    validate="one_to_one",
                )
            diagnostics.append(diagnostic)
        if source_donor is None:
            raise RuntimeError(f"No eligible donors for {source}")
        source_donor_frames.append(source_donor)

    donor = pd.concat(source_donor_frames, ignore_index=True)
    donor = donor.sort_values(["source_family", "canonical_donor"]).reset_index(drop=True)
    if donor[MODULES].isna().any().any():
        raise RuntimeError("Missing donor residual score")
    donor.to_csv(OUT / "donor_standardized_residual_scores.tsv", sep="\t", index=False)
    pd.DataFrame(diagnostics).to_csv(OUT / "nuisance_designs.tsv", sep="\t", index=False)

    source_rows = []
    for source in SOURCE_TISSUE:
        source_frame = donor[donor.source_family.eq(source)]
        for module in MODULES:
            source_rows.append(source_effect(source_frame, module))
    source_table = pd.DataFrame(source_rows)

    y = donor[MODULES].to_numpy(dtype=float)
    stage = donor.diagnosis.eq("SPMS").astype(float).to_numpy()
    source_names = list(SOURCE_TISSUE)
    source_masks = [donor.source_family.eq(source).to_numpy() for source in source_names]
    source_proportions = [float(stage[mask].mean()) for mask in source_masks]
    residualized_stage = stage.copy()
    for mask, proportion in zip(source_masks, source_proportions, strict=True):
        residualized_stage[mask] -= proportion
    denominator = float(np.dot(residualized_stage, residualized_stage))
    if not np.isfinite(denominator) or denominator <= 0:
        raise RuntimeError(f"Invalid pooled permutation denominator: {denominator}")
    observed = residualized_stage @ y / denominator

    full_design = np.column_stack(
        [
            np.ones(len(donor)),
            stage,
            donor.source_family.eq(source_names[1]).astype(float).to_numpy(),
        ]
    )
    hc3_rows: list[dict[str, Any]] = []
    for index, module in enumerate(MODULES):
        model = sm.OLS(y[:, index], full_design).fit(cov_type="HC3")
        ci = model.conf_int()[1]
        if not np.isclose(model.params[1], observed[index], atol=1e-10):
            raise RuntimeError(f"Residualized and OLS stage effects disagree for {module}")
        hc3_rows.append(
            {
                "module": module,
                "spms_minus_ppms_standardized_beta": float(model.params[1]),
                "hc3_ci_low": float(ci[0]),
                "hc3_ci_high": float(ci[1]),
                "hc3_p": float(model.pvalues[1]),
            }
        )

    aggregate_exceed = np.zeros(len(MODULES), dtype=np.int64)
    aggregate_max_exceed = np.zeros(len(MODULES), dtype=np.int64)
    source_exceed = np.zeros((len(source_names), len(MODULES)), dtype=np.int64)
    source_observed = np.zeros((len(source_names), len(MODULES)), dtype=float)
    source_denominators = np.zeros(len(source_names), dtype=float)
    for source_index, (mask, proportion) in enumerate(
        zip(source_masks, source_proportions, strict=True)
    ):
        z = stage[mask] - proportion
        source_denominators[source_index] = float(np.dot(z, z))
        if not np.isfinite(source_denominators[source_index]) or source_denominators[source_index] <= 0:
            raise RuntimeError(
                f"Invalid source permutation denominator for {source_names[source_index]}"
            )
        source_observed[source_index] = z @ y[mask] / source_denominators[source_index]

    seed_rows: list[dict[str, Any]] = []
    for seed in SEEDS:
        rng = np.random.default_rng(seed)
        seed_exceed = np.zeros(len(MODULES), dtype=np.int64)
        seed_max_exceed = np.zeros(len(MODULES), dtype=np.int64)
        completed = 0
        while completed < N_PER_SEED:
            batch = min(BATCH, N_PER_SEED - completed)
            permuted_stage = np.zeros((batch, len(donor)), dtype=float)
            for mask in source_masks:
                indices = np.flatnonzero(mask)
                n_spms = int(stage[mask].sum())
                random_order = np.argsort(rng.random((batch, len(indices))), axis=1)
                chosen = random_order[:, :n_spms]
                row_indices = np.arange(batch)[:, None]
                permuted_stage[row_indices, indices[chosen]] = 1.0
            permuted_residual = permuted_stage.copy()
            for mask, proportion in zip(source_masks, source_proportions, strict=True):
                permuted_residual[:, mask] -= proportion
            if not np.isfinite(permuted_residual).all():
                raise RuntimeError("Non-finite permuted stage matrix")
            for mask in source_masks:
                expected = int(stage[mask].sum())
                if not np.all(permuted_stage[:, mask].sum(axis=1) == expected):
                    raise RuntimeError("Permutation did not preserve source-specific stage counts")
            null_beta = np.einsum("bi,ij->bj", permuted_residual, y) / denominator
            if not np.isfinite(null_beta).all():
                raise RuntimeError("Non-finite pooled null coefficient")
            absolute = np.abs(null_beta)
            seed_exceed += np.sum(absolute >= np.abs(observed)[None, :], axis=0)
            null_max = np.max(absolute, axis=1)
            seed_max_exceed += np.sum(
                null_max[:, None] >= np.abs(observed)[None, :], axis=0
            )
            for source_index, mask in enumerate(source_masks):
                z = permuted_residual[:, mask]
                null_source = (
                    np.einsum("bi,ij->bj", z, y[mask])
                    / source_denominators[source_index]
                )
                if not np.isfinite(null_source).all():
                    raise RuntimeError(
                        f"Non-finite source null coefficient for {source_names[source_index]}"
                    )
                source_exceed[source_index] += np.sum(
                    np.abs(null_source) >= np.abs(source_observed[source_index])[None, :],
                    axis=0,
                )
            completed += batch
        aggregate_exceed += seed_exceed
        aggregate_max_exceed += seed_max_exceed
        for index, module in enumerate(MODULES):
            seed_rows.append(
                {
                    "seed": seed,
                    "module": module,
                    "n_permutations": N_PER_SEED,
                    "two_sided_p": (1 + int(seed_exceed[index])) / (N_PER_SEED + 1),
                    "max_t_fwer_p": (1 + int(seed_max_exceed[index])) / (N_PER_SEED + 1),
                }
            )

    total_null = len(SEEDS) * N_PER_SEED
    aggregate_p = ((1 + aggregate_exceed) / (total_null + 1)).tolist()
    aggregate_max_p = ((1 + aggregate_max_exceed) / (total_null + 1)).tolist()
    q_values = bh(aggregate_p)
    source_lookup = source_table.set_index(["source_family", "module"])
    test_rows = []
    for index, row in enumerate(hc3_rows):
        source_betas = [
            float(source_lookup.loc[(source, row["module"]), "spms_minus_ppms_standardized_beta"])
            for source in source_names
        ]
        direction_concordant = bool(np.sign(source_betas[0]) == np.sign(source_betas[1]))
        ci_excludes_zero = bool(row["hc3_ci_low"] > 0 or row["hc3_ci_high"] < 0)
        passes = bool(
            direction_concordant
            and ci_excludes_zero
            and aggregate_p[index] <= 0.05
            and q_values[index] <= 0.10
            and aggregate_max_p[index] <= 0.10
        )
        outcome = (
            "supported_provisional"
            if passes
            else "inconclusive"
            if direction_concordant
            else "not_supported"
        )
        test_rows.append(
            {
                **row,
                "permutation_p": aggregate_p[index],
                "bh_q": q_values[index],
                "max_t_fwer_p": aggregate_max_p[index],
                "amsterdam_beta": source_betas[0],
                "uk_beta": source_betas[1],
                "source_direction_concordant": direction_concordant,
                "passes_frozen_portable_stage_gate": passes,
                "outcome": outcome,
            }
        )
    tests = pd.DataFrame(test_rows)
    tests.to_csv(OUT / "module_tests.tsv", sep="\t", index=False)
    pd.DataFrame(seed_rows).to_csv(OUT / "seed_stability.tsv", sep="\t", index=False)

    for source_index, source in enumerate(source_names):
        for module_index, module in enumerate(MODULES):
            mask = (source_table.source_family.eq(source)) & source_table.module.eq(module)
            source_table.loc[mask, "permutation_p"] = (
                1 + int(source_exceed[source_index, module_index])
            ) / (total_null + 1)
    source_table.to_csv(OUT / "source_effects.tsv", sep="\t", index=False)

    supported = tests.loc[tests.passes_frozen_portable_stage_gate, "module"].tolist()
    summary = {
        "purpose": "Frozen cross-sectional PPMS-vs-SPMS module test; not progression-rate or treatment evidence",
        "n_donors": len(donor),
        "donors_by_source_stage": {
            f"{source}|{stage_name}": int(
                ((donor.source_family.eq(source)) & (donor.diagnosis.eq(stage_name))).sum()
            )
            for source in source_names
            for stage_name in STAGES
        },
        "modules_tested": MODULES,
        "n_null_replicates": total_null,
        "seeds": SEEDS,
        "supported_modules": supported,
        "n_supported_modules": len(supported),
        "verdict": (
            "PORTABLE_CROSS_SECTIONAL_STAGE_ASSOCIATION_SUPPORTED"
            if supported
            else "NO_PORTABLE_CROSS_SECTIONAL_STAGE_ASSOCIATION"
        ),
        "boundary": (
            "Cross-sectional stage association only. A positive result would not identify transition, disability accumulation, causality, or treatment benefit."
        ),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")

    report = [
        "# V54 Source/Tissue-Balanced Progressive-Stage Modules",
        "",
        f"Verdict: **{summary['verdict']}**.",
        "",
        "The frozen test compared SPMS with PPMS after restricting Amsterdam to",
        "white matter and UK to grey matter, nuisance-adjusting deposited lesion",
        "context, age, sex, and microglial yield, and treating donors as the",
        "inferential units. Three seeds supplied 300,000 within-source label nulls.",
        "",
        "| module | pooled beta | HC3 CI | permutation p | BH q | max-T p | Amsterdam beta | UK beta | outcome |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in test_rows:
        report.append(
            "| {module} | {spms_minus_ppms_standardized_beta:.3f} | "
            "[{hc3_ci_low:.3f}, {hc3_ci_high:.3f}] | {permutation_p:.4g} | "
            "{bh_q:.4g} | {max_t_fwer_p:.4g} | {amsterdam_beta:.3f} | "
            "{uk_beta:.3f} | {outcome} |".format(**row)
        )
    report.extend(
        [
            "",
            "No result changes a therapeutic verdict. This package has no repeated",
            "disability outcome and no RRMS transition series; the analysis cannot say",
            "whether any state drives or can halt progression.",
        ]
    )
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
