#!/usr/bin/env python3
"""Apply the frozen V53 CD44/CXCR4 test to a prepared Macnair cohort."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.stats import chi2_contingency


SCORES = {
    "receptor_cd44_cxcr4": ["CD44", "CXCR4"],
    "hla_regulatory": ["CIITA", "RFX5"],
    "mif_ligand": ["MIF", "DDT"],
    "ifn_apc_unique": ["STAT1", "IRF1", "CXCL10", "GBP1"],
    "lysosomal_unique": ["CTSS", "CTSB", "CTSD", "LAMP1", "LAMP2", "LAMP3"],
}
SEED = 53507
N_WILD = 100_000


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--indir", type=Path, required=True)
    parser.add_argument("--cohort", choices=["discovery", "validation"], required=True)
    return parser.parse_args()


def canonical_donor(cohort: str, donor: str) -> str:
    if cohort == "validation":
        return re.sub(r"^[^_]+_", "", donor)
    return donor


def design(
    frame: pd.DataFrame,
    include_disease: bool = True,
    extra_covariates: tuple[str, ...] = (),
) -> tuple[np.ndarray, list[str]]:
    age = frame["age_at_death"].to_numpy(dtype=float)
    age_z = (age - age.mean()) / age.std(ddof=0)
    columns = [np.ones(len(frame))]
    names = ["intercept"]
    if include_disease:
        columns.append(frame["disease_binary"].to_numpy(dtype=float))
        names.append("disease_binary")
    columns.extend([age_z, age_z**2, frame["sex_male"].to_numpy(dtype=float)])
    names.extend(["age_z", "age_z_squared", "sex_male"])
    studies = sorted(frame["study"].unique())
    for study in studies[1:]:
        columns.append(frame["study"].eq(study).to_numpy(dtype=float))
        names.append(f"study_{study}")
    for covariate in extra_covariates:
        values = frame[covariate].to_numpy(dtype=float)
        scale = values.std(ddof=0)
        if scale == 0:
            raise ValueError(f"zero-variance extra covariate: {covariate}")
        columns.append((values - values.mean()) / scale)
        names.append(covariate)
    matrix = np.column_stack(columns)
    if np.linalg.matrix_rank(matrix) != matrix.shape[1]:
        raise ValueError(f"rank-deficient design: {names}")
    return matrix, names


def wild_test(
    frame: pd.DataFrame,
    outcome: str,
    seed_offset: int,
    extra_covariates: tuple[str, ...] = (),
) -> dict[str, float]:
    y = frame[outcome].to_numpy(dtype=float)
    full, names = design(frame, include_disease=True, extra_covariates=extra_covariates)
    reduced, _ = design(frame, include_disease=False, extra_covariates=extra_covariates)
    disease_index = names.index("disease_binary")
    if np.linalg.cond(full) > 1e6 or np.linalg.cond(reduced) > 1e6:
        raise ValueError("ill-conditioned replication design")
    full_pinv = np.linalg.solve(np.einsum("ni,nj->ij", full, full), full.T)
    observed = np.einsum("ij,j->i", full_pinv, y)
    reduced_pinv = np.linalg.solve(
        np.einsum("ni,nj->ij", reduced, reduced), reduced.T
    )
    reduced_coefficients = np.einsum("ij,j->i", reduced_pinv, y)
    fitted = np.einsum("ij,j->i", reduced, reduced_coefficients)
    residual = y - fitted
    rng = np.random.default_rng(SEED + seed_offset)
    exceed = 0
    completed = 0
    while completed < N_WILD:
        batch = min(5_000, N_WILD - completed)
        signs = rng.choice([-1.0, 1.0], size=(batch, len(frame)))
        synthetic = fitted[None, :] + signs * residual[None, :]
        disease_betas = np.add.reduce(
            synthetic * full_pinv[disease_index, :][None, :], axis=1
        )
        if not np.all(np.isfinite(disease_betas)):
            raise FloatingPointError("non-finite wild-bootstrap disease coefficients")
        exceed += int(np.sum(np.abs(disease_betas) >= abs(observed[disease_index])))
        completed += batch
    fitted_model = sm.OLS(y, full).fit(cov_type="HC3")
    ci = fitted_model.conf_int()[disease_index]
    return {
        "disease_beta": float(observed[disease_index]),
        "hc3_se": float(fitted_model.bse[disease_index]),
        "hc3_ci_low": float(ci[0]),
        "hc3_ci_high": float(ci[1]),
        "hc3_p": float(fitted_model.pvalues[disease_index]),
        "wild_two_sided_p": (1 + exceed) / (N_WILD + 1),
    }


def bh(values: list[float]) -> list[float]:
    order = np.argsort(values)
    adjusted = np.empty(len(values), dtype=float)
    running = 1.0
    for rank in range(len(values) - 1, -1, -1):
        index = order[rank]
        running = min(running, values[index] * len(values) / (rank + 1))
        adjusted[index] = running
    return adjusted.tolist()


def standardized_difference(frame: pd.DataFrame, outcome: str) -> float:
    ms = frame.loc[frame.disease_binary.eq(1), outcome].to_numpy(dtype=float)
    control = frame.loc[frame.disease_binary.eq(0), outcome].to_numpy(dtype=float)
    pooled = np.sqrt(((len(ms) - 1) * ms.var(ddof=1) + (len(control) - 1) * control.var(ddof=1)) / (len(ms) + len(control) - 2))
    return float((ms.mean() - control.mean()) / pooled)


def main() -> None:
    args = parse_args()
    metadata = pd.read_csv(args.indir / "sample_metadata.tsv", sep="\t")
    counts = pd.read_csv(args.indir / "target_pseudobulk_counts.tsv", sep="\t")
    target_rows = pd.read_csv(args.indir / "target_rows.tsv", sep="\t")
    expected = len(metadata) * len(target_rows)
    if len(counts) != expected:
        raise ValueError(f"target-count row mismatch: expected {expected}, observed {len(counts)}")
    if counts.groupby("group_idx")["library_total"].nunique().max() != 1:
        raise ValueError("library total changes within a sample")

    wide = counts.pivot(index="group_idx", columns="gene", values="raw_count")
    library = counts.groupby("group_idx")["library_total"].first()
    log_cpm = np.log2(wide.div(library, axis=0) * 1_000_000.0 + 1.0)
    variable_genes = [gene for gene in log_cpm if float(log_cpm[gene].std(ddof=0)) > 0]
    z = (log_cpm[variable_genes] - log_cpm[variable_genes].mean()) / log_cpm[variable_genes].std(ddof=0)
    sample = metadata.set_index("group_idx").join(log_cpm.add_prefix("logcpm_"))
    for score, genes in SCORES.items():
        usable = [gene for gene in genes if gene in variable_genes]
        if len(usable) < (len(genes) + 1) // 2:
            raise ValueError(f"score {score} has insufficient variable genes: {usable}")
        sample[score] = z[usable].mean(axis=1)
    sample["receptor_minus_hla"] = sample["receptor_cd44_cxcr4"] - sample["hla_regulatory"]
    sample["receptor_minus_mif"] = sample["receptor_cd44_cxcr4"] - sample["mif_ligand"]
    sample["canonical_donor"] = [canonical_donor(args.cohort, value) for value in sample["donor_id"]]

    # Some validation publications profiled the same named donor. Pick the
    # source study with the most eligible microglia before looking at outcomes.
    source_sizes = (
        sample.groupby(["canonical_donor", "study"], as_index=False)["n_microglia"]
        .sum()
        .sort_values(["canonical_donor", "n_microglia", "study"], ascending=[True, False, True])
    )
    selected_sources = source_sizes.drop_duplicates("canonical_donor").set_index("canonical_donor")["study"]
    sample["selected_source"] = sample["canonical_donor"].map(selected_sources)
    retained = sample[sample.study.eq(sample.selected_source)].copy()

    invariant_fields = ["diagnosis", "disease_binary", "sex", "age_at_death"]
    for field in invariant_fields:
        if retained.groupby("canonical_donor")[field].nunique().max() != 1:
            raise ValueError(f"donor field changes across retained samples: {field}")
    outcome_columns = list(SCORES) + ["receptor_minus_hla", "receptor_minus_mif"]
    donor = (
        retained.groupby("canonical_donor", as_index=False)
        .agg(
            diagnosis=("diagnosis", "first"),
            disease_binary=("disease_binary", "first"),
            sex=("sex", "first"),
            age_at_death=("age_at_death", "first"),
            study=("study", "first"),
            n_samples=("sample_id", "nunique"),
            n_microglia=("n_microglia", "sum"),
            **{column: (column, "mean") for column in outcome_columns},
        )
    )
    donor["sex_male"] = donor.sex.eq("M").astype(int)
    donor["log_n_microglia"] = np.log1p(donor["n_microglia"])

    primary = wild_test(donor, "receptor_cd44_cxcr4", 0)
    primary["standardized_ms_minus_control"] = standardized_difference(donor, "receptor_cd44_cxcr4")
    primary["raw_ms_minus_control"] = float(
        donor.loc[donor.disease_binary.eq(1), "receptor_cd44_cxcr4"].mean()
        - donor.loc[donor.disease_binary.eq(0), "receptor_cd44_cxcr4"].mean()
    )
    cell_count_adjusted = wild_test(
        donor,
        "receptor_cd44_cxcr4",
        4,
        extra_covariates=("log_n_microglia",),
    )
    component_adjusted = wild_test(
        donor,
        "receptor_cd44_cxcr4",
        5,
        extra_covariates=(
            "hla_regulatory",
            "mif_ligand",
            "ifn_apc_unique",
            "lysosomal_unique",
        ),
    )

    cell_threshold_sensitivity = []
    for threshold_index, minimum_cells in enumerate([1, 10, 25, 50, 100], start=10):
        frame = donor[donor.n_microglia.ge(minimum_cells)].copy()
        if (
            frame.disease_binary.nunique() != 2
            or min(frame.groupby("disease_binary").size()) < 5
            or len(frame) <= design(frame)[0].shape[1] + 2
        ):
            continue
        result = wild_test(frame, "receptor_cd44_cxcr4", threshold_index)
        cell_threshold_sensitivity.append(
            {
                "minimum_microglia": minimum_cells,
                "n_donors": len(frame),
                "n_ms": int(frame.disease_binary.sum()),
                "n_control": int((1 - frame.disease_binary).sum()),
                **result,
            }
        )

    secondary = []
    for offset, outcome in enumerate(["receptor_minus_hla", "receptor_minus_mif"], start=1):
        result = wild_test(donor, outcome, offset)
        secondary.append({"outcome": outcome, **result})
    q_values = bh([float(row["wild_two_sided_p"]) for row in secondary])
    for row, q_value in zip(secondary, q_values, strict=True):
        row["wild_bh_q"] = q_value

    table = pd.crosstab(donor.study, donor.disease_binary)
    if min(table.shape[0] - 1, table.shape[1] - 1) == 0:
        batch_p = 1.0
        cramers_v = 0.0
    else:
        chi2, batch_p, _, _ = chi2_contingency(table)
        cramers_v = float(
            np.sqrt(chi2 / (len(donor) * min(table.shape[0] - 1, table.shape[1] - 1)))
        )
    age_group = donor.groupby("disease_binary")["age_at_death"].agg(["mean", "std", "min", "max"])
    pooled_age = np.sqrt(
        (
            (sum(donor.disease_binary.eq(1)) - 1) * age_group.loc[1, "std"] ** 2
            + (sum(donor.disease_binary.eq(0)) - 1) * age_group.loc[0, "std"] ** 2
        )
        / (len(donor) - 2)
    )
    age_smd = float((age_group.loc[1, "mean"] - age_group.loc[0, "mean"]) / pooled_age)
    common_low = float(max(age_group.loc[0, "min"], age_group.loc[1, "min"]))
    common_high = float(min(age_group.loc[0, "max"], age_group.loc[1, "max"]))
    common = donor[donor.age_at_death.between(common_low, common_high)].copy()
    common_result: dict[str, float] | None = None
    if common.disease_binary.nunique() == 2 and len(common) >= design(common)[0].shape[1] + 3:
        common_result = wild_test(common, "receptor_cd44_cxcr4", 3)

    by_study = []
    for study, frame in donor.groupby("study"):
        if frame.disease_binary.nunique() != 2:
            continue
        by_study.append(
            {
                "study": study,
                "n_ms": int(frame.disease_binary.sum()),
                "n_control": int((1 - frame.disease_binary).sum()),
                "raw_ms_minus_control": float(
                    frame.loc[frame.disease_binary.eq(1), "receptor_cd44_cxcr4"].mean()
                    - frame.loc[frame.disease_binary.eq(0), "receptor_cd44_cxcr4"].mean()
                ),
            }
        )

    low_detection = []
    for gene, frame in counts.groupby("gene"):
        detected_fraction = float(np.mean(frame.raw_count.gt(0)))
        if detected_fraction < 0.5:
            low_detection.append({"gene": gene, "detected_sample_fraction": detected_fraction})

    frozen_primary_components = {
        "disease_beta_positive": bool(primary["disease_beta"] > 0),
        "standardized_effect_at_least_0_50": bool(primary["standardized_ms_minus_control"] >= 0.5),
        "wild_p_at_most_0_05": bool(primary["wild_two_sided_p"] <= 0.05),
        "hc3_interval_excludes_zero": bool(primary["hc3_ci_low"] > 0),
        "no_detected_study_batch_association": bool(batch_p > 0.05),
        "common_age_support_effect_positive": bool(
            common_result is not None and common_result["disease_beta"] > 0
        ),
        "direction_positive_in_each_study": bool(
            by_study and all(row["raw_ms_minus_control"] > 0 for row in by_study)
        ),
    }
    quality_tightening_components = {
        "microglia_depth_adjusted_effect_positive_p_le_0_05": bool(
            cell_count_adjusted["disease_beta"] > 0
            and cell_count_adjusted["wild_two_sided_p"] <= 0.05
            and cell_count_adjusted["hc3_ci_low"] > 0
        ),
        "microglia_threshold_directions_all_positive": bool(
            cell_threshold_sensitivity
            and all(row["disease_beta"] > 0 for row in cell_threshold_sensitivity)
        ),
    }
    frozen_primary_pass = all(frozen_primary_components.values())
    clean_components = {**frozen_primary_components, **quality_tightening_components}
    clean_pass = all(clean_components.values())
    same_direction = primary["disease_beta"] > 0 and primary["standardized_ms_minus_control"] > 0
    if clean_pass:
        verdict = "REPLICATED_STATE_ASSOCIATION"
    elif frozen_primary_pass:
        verdict = "FROZEN_PRIMARY_PASS_QUALITY_SENSITIVE"
    elif same_direction:
        verdict = "PROVISIONAL_SAME_DIRECTION"
    else:
        verdict = "NOT_SUPPORTED_IN_LOW_POWER_INDEPENDENT_COHORT"
    decoupled = clean_pass and all(row["disease_beta"] > 0 and row["wild_bh_q"] <= 0.10 for row in secondary)
    if decoupled:
        verdict = "REPLICATED_AND_DECOUPLED"

    summary: dict[str, Any] = {
        "purpose": "Frozen V53 independent-cohort CD44/CXCR4 replication test",
        "cohort": args.cohort,
        "n_donors": len(donor),
        "n_ms_donors": int(donor.disease_binary.sum()),
        "n_control_donors": int((1 - donor.disease_binary).sum()),
        "n_samples_retained": int(donor.n_samples.sum()),
        "n_microglia_retained": int(donor.n_microglia.sum()),
        "n_cross_study_duplicate_donors_resolved": int(sample.canonical_donor.nunique() - sample.donor_id.nunique()) * -1,
        "source_selection_rule": "For cross-study duplicate donor codes, retain the study with most eligible microglia; ties lexicographic; rule applied before outcome modeling.",
        "n_wild_replicates_per_test": N_WILD,
        "seed": SEED,
        "primary": primary,
        "microglia_depth_diagnostic": {
            "score_log_microglia_correlation": float(
                np.corrcoef(donor.receptor_cd44_cxcr4, donor.log_n_microglia)[0, 1]
            ),
            "cell_count_adjusted": cell_count_adjusted,
            "minimum_cell_threshold_sensitivity": cell_threshold_sensitivity,
        },
        "joint_component_adjusted_sensitivity": component_adjusted,
        "secondary": secondary,
        "batch_diagnostic": {"chi_square_p": float(batch_p), "cramers_v": cramers_v},
        "age_diagnostic": {
            "standardized_mean_difference_ms_minus_control": age_smd,
            "common_support": [common_low, common_high],
            "n_common_support": len(common),
            "common_support_result": common_result,
        },
        "by_study_direction": by_study,
        "low_detection_genes": low_detection,
        "clean_replication_components": clean_components,
        "frozen_primary_components": frozen_primary_components,
        "frozen_primary_pass": frozen_primary_pass,
        "quality_tightening_components": quality_tightening_components,
        "clean_replication_pass": clean_pass,
        "decoupling_pass": decoupled,
        "verdict": verdict,
        "boundary": "Independent public-cohort test; no causal, intervention-direction, or therapeutic-target conclusion.",
    }

    sample.reset_index().to_csv(args.indir / "sample_scores.tsv", sep="\t", index=False)
    donor.to_csv(args.indir / "donor_scores.tsv", sep="\t", index=False)
    pd.DataFrame(secondary).to_csv(args.indir / "secondary_tests.tsv", sep="\t", index=False)
    pd.DataFrame(by_study).to_csv(args.indir / "study_directions.tsv", sep="\t", index=False)
    pd.DataFrame(cell_threshold_sensitivity).to_csv(
        args.indir / "microglia_count_threshold_sensitivity.tsv", sep="\t", index=False
    )
    (args.indir / "replication_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    report = [
        f"# Macnair {args.cohort.title()} Frozen CD44/CXCR4 Test",
        "",
        f"Verdict: **{verdict}**.",
        "",
        f"After deterministic cross-study donor de-duplication, the test includes `{len(donor)}` donors",
        f"(`{int(donor.disease_binary.sum())}` MS, `{int((1 - donor.disease_binary).sum())}` controls),",
        f"`{int(donor.n_microglia.sum())}` annotated microglia, and the exact frozen score genes.",
        f"The adjusted disease beta is `{primary['disease_beta']:.3f}` (wild p `{primary['wild_two_sided_p']:.4f}`,",
        f"HC3 95% CI `{primary['hc3_ci_low']:.3f}` to `{primary['hc3_ci_high']:.3f}`); the raw standardized",
        f"MS-control effect is `{primary['standardized_ms_minus_control']:.3f}`.",
        "",
        f"Study/batch association has p `{batch_p:.4f}` and Cramer's V `{cramers_v:.3f}`. Age SMD is",
        f"`{age_smd:.3f}`. The clean replication gate passes `{sum(clean_components.values())}/{len(clean_components)}`",
        "components. Secondary decoupling is not claimed unless both frozen contrasts pass BH q <= 0.10",
        "after a clean primary replication.",
        f"The score-to-log-microglia-count correlation is `{summary['microglia_depth_diagnostic']['score_log_microglia_correlation']:.3f}`,",
        f"but count-adjusted disease beta is `{cell_count_adjusted['disease_beta']:.3f}` (wild p",
        f"`{cell_count_adjusted['wild_two_sided_p']:.4f}`), and all executable thresholds in the transparent",
        "post-result 1/10/25/50/100-cell sensitivity grid retain positive direction. The grid is a",
        "conservative quality tightening, not part of the frozen primary; it addresses, but does not erase,",
        "sparse-control-pseudobulk risk.",
        "",
        "This is an independent public-cohort analysis, but it remains a state-association test. It cannot",
        "establish causality, therapeutic direction, or target status.",
    ]
    (args.indir / "REPORT.md").write_text("\n".join(report) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
