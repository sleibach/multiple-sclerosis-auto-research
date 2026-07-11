#!/usr/bin/env python3
"""Test Macnair CD44/CXCR4 estimates against source-bank/study influence."""

from __future__ import annotations

import csv
import gzip
import io
import json
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.stats import chi2_contingency


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "analysis/v53_ms_microglia_independent_cohort_scout"
OUT = ROOT / "analysis/v53_macnair_source_influence"
DISCOVERY_METADATA_URL = (
    "https://zenodo.org/api/records/8338963/files/"
    "ms_lesions_snRNAseq_col_data_2023-09-12.txt.gz/content"
)
SEED = 53509
N_WILD = 100_000
N_STRATIFIED_PER_SEED = 100_000
STRATIFIED_SEEDS = [53591, 53592, 53593]


def discovery_sources() -> pd.DataFrame:
    by_donor: dict[str, set[str]] = {}
    with urllib.request.urlopen(DISCOVERY_METADATA_URL, timeout=120) as response:  # noqa: S310
        with gzip.GzipFile(fileobj=response) as compressed:
            with io.TextIOWrapper(compressed, encoding="utf-8", newline="") as text:
                for row in csv.DictReader(text):
                    if row.get("type_broad") != "Microglia":
                        continue
                    if row.get("exclude_pseudobulk") == "TRUE":
                        continue
                    if row.get("diagnosis") not in {"CTR", "PPMS", "RRMS", "SPMS"}:
                        continue
                    by_donor.setdefault(row["individual_id_anon"], set()).add(
                        row["sample_source"]
                    )
    if any(len(values) != 1 for values in by_donor.values()):
        raise ValueError("discovery donor maps to multiple sample sources")
    return pd.DataFrame(
        {
            "canonical_donor": sorted(by_donor),
            "source_family": [next(iter(by_donor[key])) for key in sorted(by_donor)],
        }
    )


def design(frame: pd.DataFrame, source_fixed: bool, include_disease: bool) -> np.ndarray:
    age = frame.age_at_death.to_numpy(dtype=float)
    age_z = (age - age.mean()) / age.std(ddof=0)
    columns = [np.ones(len(frame))]
    if include_disease:
        columns.append(frame.disease_binary.to_numpy(dtype=float))
    columns.extend([age_z, age_z**2, frame.sex.eq("M").to_numpy(dtype=float)])
    if source_fixed:
        for source in sorted(frame.source_family.unique())[1:]:
            columns.append(frame.source_family.eq(source).to_numpy(dtype=float))
    matrix = np.column_stack(columns)
    if np.linalg.matrix_rank(matrix) != matrix.shape[1]:
        raise ValueError("source-influence design is rank deficient")
    return matrix


def test(frame: pd.DataFrame, source_fixed: bool, seed_offset: int) -> dict[str, float]:
    y = frame.receptor_cd44_cxcr4.to_numpy(dtype=float)
    y = (y - y.mean()) / y.std(ddof=0)
    full = design(frame, source_fixed, True)
    reduced = design(frame, source_fixed, False)
    full_pinv = np.linalg.pinv(full)
    leverage = np.sum(full * full_pinv.T, axis=1)
    if np.linalg.cond(full) > 1e6 or float(leverage.max()) >= 0.99:
        raise ValueError(
            f"unstable design: condition={np.linalg.cond(full):.3g}; "
            f"max_leverage={leverage.max():.3g}"
        )
    model = sm.OLS(y, full).fit(cov_type="HC3")
    pinv = full_pinv
    observed = float((pinv @ y)[1])
    fitted = reduced @ (np.linalg.pinv(reduced) @ y)
    residual = y - fitted
    rng = np.random.default_rng(SEED + seed_offset)
    exceed = 0
    completed = 0
    while completed < N_WILD:
        batch = min(5_000, N_WILD - completed)
        signs = rng.choice([-1.0, 1.0], size=(batch, len(frame)))
        synthetic = fitted[None, :] + signs * residual[None, :]
        betas = np.einsum("bi,i->b", synthetic, pinv[1])
        if not np.all(np.isfinite(betas)):
            raise FloatingPointError("non-finite source-influence wild coefficients")
        exceed += int(np.sum(np.abs(betas) >= abs(observed)))
        completed += batch
    ci = model.conf_int()[1]
    diagnostics = np.asarray([model.bse[1], ci[0], ci[1], model.pvalues[1]])
    if not np.all(np.isfinite(diagnostics)):
        raise ValueError("non-finite HC3 source-influence diagnostics")
    return {
        "adjusted_standardized_beta": observed,
        "hc3_se": float(model.bse[1]),
        "hc3_ci_low": float(ci[0]),
        "hc3_ci_high": float(ci[1]),
        "hc3_p": float(model.pvalues[1]),
        "wild_two_sided_p": (exceed + 1) / (N_WILD + 1),
    }


def stratified_label_test(frame: pd.DataFrame) -> dict[str, object]:
    y = frame.receptor_cd44_cxcr4.to_numpy(dtype=float)
    y = (y - y.mean()) / y.std(ddof=0)
    covariates = design(frame, source_fixed=True, include_disease=False)
    covariate_pinv = np.linalg.solve(
        np.einsum("ni,nj->ij", covariates, covariates), covariates.T
    )
    projection = np.einsum("ij,jk->ik", covariates, covariate_pinv)
    residualizer = np.eye(len(frame)) - projection
    y_residual = np.einsum("ij,j->i", residualizer, y)
    observed_disease = frame.disease_binary.to_numpy(dtype=float)
    observed_residual = np.einsum("ij,j->i", residualizer, observed_disease)
    observed_beta = float(
        np.dot(observed_residual, y_residual) / np.dot(observed_residual, observed_residual)
    )
    source_indices = [
        np.flatnonzero(frame.source_family.eq(source).to_numpy())
        for source in sorted(frame.source_family.unique())
    ]
    source_cases = [int(frame.iloc[indices].disease_binary.sum()) for indices in source_indices]
    seed_rows = []
    total_exceed = 0
    for seed in STRATIFIED_SEEDS:
        rng = np.random.default_rng(seed)
        exceed = 0
        completed = 0
        while completed < N_STRATIFIED_PER_SEED:
            batch = min(5_000, N_STRATIFIED_PER_SEED - completed)
            assignments = np.zeros((batch, len(frame)), dtype=float)
            for indices, n_cases in zip(source_indices, source_cases, strict=True):
                if n_cases == 0:
                    continue
                if n_cases == len(indices):
                    assignments[:, indices] = 1.0
                    continue
                random_values = rng.random((batch, len(indices)))
                selected = np.argpartition(random_values, n_cases - 1, axis=1)[:, :n_cases]
                rows = np.arange(batch)[:, None]
                assignments[rows, indices[selected]] = 1.0
            disease_residual = np.einsum("bi,ji->bj", assignments, residualizer)
            numerator = np.einsum("bi,i->b", disease_residual, y_residual)
            denominator = np.einsum("bi,bi->b", disease_residual, disease_residual)
            betas = numerator / denominator
            if not np.all(np.isfinite(betas)):
                raise FloatingPointError("non-finite source-stratified label coefficients")
            exceed += int(np.sum(np.abs(betas) >= abs(observed_beta)))
            completed += batch
        total_exceed += exceed
        seed_rows.append(
            {
                "seed": seed,
                "n_permutations": N_STRATIFIED_PER_SEED,
                "exceedances": exceed,
                "two_sided_p": (exceed + 1) / (N_STRATIFIED_PER_SEED + 1),
            }
        )
    return {
        "observed_source_adjusted_standardized_beta": observed_beta,
        "n_permutations_total": N_STRATIFIED_PER_SEED * len(STRATIFIED_SEEDS),
        "pooled_two_sided_p": (total_exceed + 1)
        / (N_STRATIFIED_PER_SEED * len(STRATIFIED_SEEDS) + 1),
        "seed_p_min": min(row["two_sided_p"] for row in seed_rows),
        "seed_p_max": max(row["two_sided_p"] for row in seed_rows),
        "seed_results": seed_rows,
    }


def analyze(name: str, frame: pd.DataFrame) -> tuple[list[dict[str, object]], list[dict[str, object]], dict[str, object]]:
    table = pd.crosstab(frame.source_family, frame.disease_binary)
    chi2, association_p, _, _ = chi2_contingency(table)
    cramers_v = float(np.sqrt(chi2 / (len(frame) * min(table.shape[0] - 1, table.shape[1] - 1))))
    full = test(frame, source_fixed=True, seed_offset=0 if name == "discovery" else 100)
    stratified = stratified_label_test(frame)
    source_rows = []
    for source, group in frame.groupby("source_family"):
        source_rows.append(
            {
                "cohort": name,
                "source_family": source,
                "n_ms": int(group.disease_binary.sum()),
                "n_control": int((1 - group.disease_binary).sum()),
                "raw_ms_minus_control": (
                    float(
                        group.loc[group.disease_binary.eq(1), "receptor_cd44_cxcr4"].mean()
                        - group.loc[group.disease_binary.eq(0), "receptor_cd44_cxcr4"].mean()
                    )
                    if group.disease_binary.nunique() == 2
                    else float("nan")
                ),
            }
        )
    leave_out = []
    for index, source in enumerate(sorted(frame.source_family.unique()), start=1):
        retained = frame[~frame.source_family.eq(source)].copy()
        if retained.disease_binary.nunique() != 2 or min(retained.groupby("disease_binary").size()) < 5:
            continue
        base = {
            "cohort": name,
            "omitted_source_family": source,
            "n_donors": len(retained),
            "n_ms": int(retained.disease_binary.sum()),
            "n_control": int((1 - retained.disease_binary).sum()),
        }
        try:
            result = test(
                retained,
                source_fixed=retained.source_family.nunique() > 1,
                seed_offset=(0 if name == "discovery" else 100) + index,
            )
            leave_out.append({**base, "estimable": True, "non_estimable_reason": "", **result})
        except ValueError as error:
            leave_out.append(
                {
                    **base,
                    "estimable": False,
                    "non_estimable_reason": str(error),
                    "adjusted_standardized_beta": float("nan"),
                    "hc3_se": float("nan"),
                    "hc3_ci_low": float("nan"),
                    "hc3_ci_high": float("nan"),
                    "hc3_p": float("nan"),
                    "wild_two_sided_p": float("nan"),
                }
            )
    estimable_leave_out = [row for row in leave_out if row["estimable"]]
    summary = {
        "cohort": name,
        "n_donors": len(frame),
        "n_source_families": int(frame.source_family.nunique()),
        "disease_source_cramers_v": cramers_v,
        "disease_source_chi_square_p": float(association_p),
        "source_fixed_primary": full,
        "source_stratified_label_null": stratified,
        "n_leave_one_source_out_estimable": len(estimable_leave_out),
        "n_leave_one_source_out_non_estimable": len(leave_out) - len(estimable_leave_out),
        "minimum_leave_one_source_out_beta": min(row["adjusted_standardized_beta"] for row in estimable_leave_out),
        "maximum_leave_one_source_out_wild_p": max(row["wild_two_sided_p"] for row in estimable_leave_out),
        "all_source_specific_estimable_raw_directions_positive": all(
            row["raw_ms_minus_control"] > 0
            for row in source_rows
            if np.isfinite(row["raw_ms_minus_control"])
        ),
    }
    return source_rows, leave_out, summary


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    discovery = pd.read_csv(BASE / "macnair_discovery/donor_scores.tsv", sep="\t")
    discovery = discovery.merge(discovery_sources(), on="canonical_donor", validate="one_to_one")
    validation = pd.read_csv(BASE / "macnair_validation/donor_scores.tsv", sep="\t")
    validation["source_family"] = validation["study"]

    source_rows = []
    leave_rows = []
    summaries = {}
    for name, frame in [("discovery", discovery), ("validation", validation)]:
        by_source, leave_out, summary = analyze(name, frame)
        source_rows.extend(by_source)
        leave_rows.extend(leave_out)
        summaries[name] = summary
    supported = all(
        summary["source_fixed_primary"]["adjusted_standardized_beta"] > 0
        and summary["source_fixed_primary"]["wild_two_sided_p"] <= 0.05
        and summary["minimum_leave_one_source_out_beta"] > 0
        and summary["source_stratified_label_null"]["pooled_two_sided_p"] <= 0.05
        for summary in summaries.values()
    )
    summary = {
        "purpose": "Source-bank/study influence sensitivity for the frozen Macnair score",
        "n_wild_replicates_per_test": N_WILD,
        "n_source_stratified_label_permutations_per_seed": N_STRATIFIED_PER_SEED,
        "source_stratified_label_seeds": STRATIFIED_SEEDS,
        "seed": SEED,
        "cohorts": summaries,
        "source_influence_gate_pass": supported,
        "verdict": (
            "MACNAIR_STATE_ASSOCIATION_SURVIVES_SOURCE_FAMILY_INFLUENCE_GATE"
            if supported
            else "MACNAIR_STATE_ASSOCIATION_SOURCE_FAMILY_SENSITIVE"
        ),
        "boundary": "Robustness of a state association only; no causal, stage, monitoring, direction, or target claim.",
    }
    pd.DataFrame(source_rows).to_csv(OUT / "source_specific_directions.tsv", sep="\t", index=False)
    pd.DataFrame(leave_rows).to_csv(OUT / "leave_one_source_out.tsv", sep="\t", index=False)
    discovery[["canonical_donor", "source_family"]].to_csv(
        OUT / "discovery_donor_source_map.tsv", sep="\t", index=False
    )
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    report = [
        "# V53 Macnair Source-Family Influence",
        "",
        f"Verdict: **{summary['verdict']}**.",
        "",
    ]
    for name in ["discovery", "validation"]:
        item = summaries[name]
        primary = item["source_fixed_primary"]
        report.extend(
            [
                f"## {name.title()}",
                "",
                f"`{item['n_donors']}` donors span `{item['n_source_families']}` source",
                f"families. Disease/source Cramer's V is `{item['disease_source_cramers_v']:.3f}`",
                f"(chi-square p `{item['disease_source_chi_square_p']:.4g}`). With source fixed",
                f"effects, adjusted standardized beta is `{primary['adjusted_standardized_beta']:.3f}`",
                f"(HC3 CI `{primary['hc3_ci_low']:.3f}` to `{primary['hc3_ci_high']:.3f}`;",
                f"wild p `{primary['wild_two_sided_p']:.4g}`). The minimum leave-one-source-out",
                f"beta is `{item['minimum_leave_one_source_out_beta']:.3f}` and maximum wild p is",
                f"`{item['maximum_leave_one_source_out_wild_p']:.4g}`.",
                f"The three-seed source-stratified label null gives pooled p",
                f"`{item['source_stratified_label_null']['pooled_two_sided_p']:.4g}`",
                f"(seed range `{item['source_stratified_label_null']['seed_p_min']:.4g}` to",
                f"`{item['source_stratified_label_null']['seed_p_max']:.4g}`).",
                f"`{item['n_leave_one_source_out_non_estimable']}` leave-one-source design(s)",
                "were non-estimable under the fixed leverage/conditioning guard.",
                "",
            ]
        )
    report.extend(
        [
            "This sensitivity addresses deposited brain-bank/study structure. It cannot prove",
            "person-level independence across anonymized publications and does not upgrade the",
            "quality-qualified state association to a mechanism or target.",
        ]
    )
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
