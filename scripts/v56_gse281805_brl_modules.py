#!/usr/bin/env python3
"""Run the frozen V56 donor-level GSE281805 BRL module test."""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy.stats import binomtest


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw/gse281805"
OUT = ROOT / "analysis/v56_gse281805_brl_modules"
SEED = 56281805
BOOTSTRAPS = 20_000
NULL_FAMILIES_PER_SEED = 10_000

EXPRESSION_XLSX = RAW / "41591_2025_3625_MOESM5_ESM.xlsx"
ANNOTATION_XLSX = RAW / "41591_2025_3625_MOESM10_ESM.xlsx"

MODULES = {
    "receptor_cd44_cxcr4": ["CD44", "CXCR4"],
    "hla_regulatory": ["CIITA", "RFX5"],
    "ifn_apc_unique": ["STAT1", "IRF1", "CXCL10", "GBP1"],
    "mif_ligand": ["MIF"],
    "lysosomal_unique": ["CTSS", "CTSB", "CTSD", "LAMP1", "LAMP2", "LAMP3"],
    "oxphos": [
        "NDUFA1", "NDUFA2", "NDUFA9", "NDUFB8", "SDHA", "SDHB", "UQCRC1",
        "UQCRC2", "COX4I1", "COX5A", "ATP5F1A", "ATP5F1B", "ATP5MC1",
    ],
    "lipid_repair": [
        "APOE", "LPL", "TREM2", "ABCA1", "ABCG1", "SPP1", "LGALS3", "GPNMB",
    ],
    "resolution_efferocytosis_proxy": [
        "MERTK", "AXL", "TYRO3", "GAS6", "PROS1", "TREM2", "APOE", "LPL",
        "ABCA1", "ABCG1", "NR1H3", "NR1H2", "PPARD", "PPARG", "MRC1", "CD163",
        "IL10", "TGFB1", "VSIG4", "C1QA", "C1QB", "C1QC", "F13A1", "LYVE1",
        "ANXA1", "FPR2", "CD36", "MARCO",
    ],
    "mocci_inflammatory_switch": ["C15ORF48", "NDUFA4"],
}
TEST_MODULES = list(MODULES)

SOURCE_URLS = {
    "article": "https://doi.org/10.1038/s41591-025-03625-7",
    "geo_part_1": "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE264094",
    "geo_part_2": "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE281805",
    "supplements": "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12176629/supplementaryFiles",
    "analysis_code": "https://github.com/walter-ca/MS-lesions_code",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_processed_matrix() -> tuple[pd.DataFrame, pd.DataFrame]:
    raw = pd.read_excel(EXPRESSION_XLSX, sheet_name="Source_Data_Fig4_a", header=None)
    samples = raw.iloc[2, 6:].dropna().astype(str).tolist()
    genes = raw.iloc[3:, 5].dropna().astype(str).str.upper()
    values = raw.iloc[3 : 3 + len(genes), 6 : 6 + len(samples)].apply(
        pd.to_numeric, errors="raise"
    )
    values.index = genes.tolist()
    values.columns = samples
    if values.index.duplicated().any():
        duplicates = values.index[values.index.duplicated()].unique().tolist()
        raise RuntimeError(f"Duplicate source-matrix genes: {duplicates[:10]}")

    annotation = pd.read_excel(
        ANNOTATION_XLSX,
        sheet_name="SuppFig_6c_correlation",
        header=2,
        usecols="A:C",
    )
    annotation.columns = ["sample", "donor", "lesion_type"]
    annotation = annotation.dropna(subset=["sample", "donor", "lesion_type"]).copy()
    annotation = annotation.astype(str)
    if annotation["sample"].duplicated().any():
        raise RuntimeError("Duplicate samples in source annotation")
    if samples != annotation["sample"].tolist():
        raise RuntimeError("Source expression and annotation sample order differ")
    raw_sample_ids = {
        path.name.split("_", 1)[1].removesuffix(".dcc.gz")
        for path in RAW.glob("GSM*_DSP-*.dcc.gz")
    }
    missing_raw = sorted(set(samples) - raw_sample_ids)
    annotation.attrs["processed_samples_missing_raw_dcc"] = missing_raw
    annotation.attrs["processed_samples_with_raw_dcc"] = len(samples) - len(missing_raw)
    if set(annotation["lesion_type"]) != {"BRL_RIM", "mixed_RIM", "active_center"}:
        raise RuntimeError("Unexpected lesion labels in source annotation")
    if not annotation["donor"].str.fullmatch(r"MS\d+").all():
        raise RuntimeError("Non-MS donor entered the lesion source matrix")
    return values, annotation


def score_modules(
    expression: pd.DataFrame, annotation: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame, list[str]]:
    sample_scores = annotation.copy()
    coverage: list[dict[str, Any]] = []
    valid_modules: list[str] = []
    for module, requested in MODULES.items():
        present = [gene for gene in requested if gene in expression.index]
        variable = [
            gene
            for gene in present
            if float(expression.loc[gene].std(ddof=0)) > 0
        ]
        required = (len(requested) + 1) // 2
        mandatory_ok = True
        if module == "mif_ligand":
            mandatory_ok = variable == ["MIF"]
        if module == "mocci_inflammatory_switch":
            mandatory_ok = set(variable) == {"C15ORF48", "NDUFA4"}
        valid = len(variable) >= required and mandatory_ok
        coverage.append(
            {
                "module": module,
                "n_requested": len(requested),
                "n_present": len(present),
                "n_variable": len(variable),
                "coverage_fraction": len(variable) / len(requested),
                "required_variable_genes": required,
                "mandatory_genes_ok": mandatory_ok,
                "valid_for_test": valid,
                "absent_or_constant_genes": ";".join(sorted(set(requested) - set(variable))),
                "variable_genes": ";".join(variable),
            }
        )
        if not valid:
            continue
        selected = expression.loc[variable].T
        z = (selected - selected.mean(axis=0)) / selected.std(axis=0, ddof=0)
        if module == "mocci_inflammatory_switch":
            score = z["C15ORF48"] - z["NDUFA4"]
        else:
            score = z.mean(axis=1)
        sample_scores[module] = score.loc[sample_scores["sample"]].to_numpy()
        valid_modules.append(module)
    if not valid_modules:
        raise RuntimeError("No frozen module passed source-matrix coverage")
    return sample_scores, pd.DataFrame(coverage), valid_modules


def welch_t(a: np.ndarray, b: np.ndarray) -> float:
    if len(a) < 2 or len(b) < 2:
        return math.nan
    denominator = math.sqrt(float(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b)))
    difference = float(a.mean() - b.mean())
    if denominator == 0:
        if difference == 0:
            return 0.0
        return math.copysign(math.inf, difference)
    return difference / denominator


def hedges_g(a: np.ndarray, b: np.ndarray) -> float:
    n_a, n_b = len(a), len(b)
    pooled_numerator = (n_a - 1) * a.var(ddof=1) + (n_b - 1) * b.var(ddof=1)
    pooled = math.sqrt(float(pooled_numerator / (n_a + n_b - 2)))
    if pooled == 0:
        return math.copysign(math.inf, float(a.mean() - b.mean()))
    correction = 1 - 3 / (4 * (n_a + n_b) - 9)
    return correction * float(a.mean() - b.mean()) / pooled


@lru_cache(maxsize=None)
def assignment_matrix(n_total: int, n_a: int) -> np.ndarray:
    assignments = np.zeros((math.comb(n_total, n_a), n_total), dtype=np.float64)
    for row, selected in enumerate(itertools.combinations(range(n_total), n_a)):
        assignments[row, list(selected)] = 1.0
    assignments.flags.writeable = False
    return assignments


def exact_family_test(
    matrix: np.ndarray, n_a: int
) -> tuple[np.ndarray, np.ndarray, np.ndarray, int]:
    n_total, n_modules = matrix.shape
    assignments = assignment_matrix(n_total, n_a)
    n_b = n_total - n_a
    # einsum avoids platform-BLAS warnings observed for these small exact matrices.
    sums = np.einsum("ij,jk->ik", assignments, matrix, optimize=False)
    sums_sq = np.einsum("ij,jk->ik", assignments, matrix * matrix, optimize=False)
    totals = matrix.sum(axis=0)
    totals_sq = (matrix * matrix).sum(axis=0)
    means_a = sums / n_a
    means_b = (totals - sums) / n_b
    var_a = (sums_sq - sums * sums / n_a) / (n_a - 1)
    b_sums = totals - sums
    var_b = (totals_sq - sums_sq - b_sums * b_sums / n_b) / (n_b - 1)
    denominators = np.sqrt(np.maximum(var_a / n_a + var_b / n_b, 0))
    with np.errstate(divide="ignore", invalid="ignore"):
        null_t = np.divide(
            means_a - means_b,
            denominators,
            out=np.zeros_like(means_a),
            where=denominators > 0,
        )
    observed = np.asarray(
        [welch_t(matrix[:n_a, index], matrix[n_a:, index]) for index in range(n_modules)]
    )
    absolute = np.abs(null_t)
    tolerance = 1e-12
    nominal = np.mean(absolute + tolerance >= np.abs(observed), axis=0)
    maximum = absolute.max(axis=1)
    max_t = np.asarray(
        [np.mean(maximum + tolerance >= abs(value)) for value in observed]
    )
    return observed, nominal, max_t, len(assignments)


def bootstrap_interval(a: np.ndarray, b: np.ndarray, seed: int) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    a_indices = rng.integers(0, len(a), size=(BOOTSTRAPS, len(a)))
    b_indices = rng.integers(0, len(b), size=(BOOTSTRAPS, len(b)))
    differences = a[a_indices].mean(axis=1) - b[b_indices].mean(axis=1)
    low, high = np.quantile(differences, [0.025, 0.975])
    return float(low), float(high)


def analyze_contrast(
    donor_scores: pd.DataFrame,
    group_a: str,
    group_b: str,
    label: str,
    modules: list[str],
    pass_verdict: str = "brl_specific_gate_pass",
) -> tuple[pd.DataFrame, pd.DataFrame]:
    left = donor_scores.loc[donor_scores.lesion_type.eq(group_a)].sort_values("donor")
    right = donor_scores.loc[donor_scores.lesion_type.eq(group_b)].sort_values("donor")
    shared = sorted(set(left.donor) & set(right.donor))
    if shared:
        left = left.loc[~left.donor.isin(shared)].copy()
        right = right.loc[~right.donor.isin(shared)].copy()
    if len(left) < 2 or len(right) < 2:
        raise RuntimeError(f"Too few independent donors for {label}")
    combined = pd.concat([left, right], ignore_index=True)
    matrix = combined[modules].to_numpy(dtype=float)
    observed_t, nominal_p, max_t_p, assignments = exact_family_test(matrix, len(left))

    rows: list[dict[str, Any]] = []
    loo_rows: list[dict[str, Any]] = []
    for index, module in enumerate(modules):
        a = left[module].to_numpy(dtype=float)
        b = right[module].to_numpy(dtype=float)
        difference = float(a.mean() - b.mean())
        low, high = bootstrap_interval(a, b, SEED + index)
        loo_values: list[float] = []
        for donor in combined.donor:
            loo_a = left.loc[left.donor.ne(donor), module].to_numpy(dtype=float)
            loo_b = right.loc[right.donor.ne(donor), module].to_numpy(dtype=float)
            estimate = float(loo_a.mean() - loo_b.mean())
            loo_values.append(estimate)
            loo_rows.append(
                {
                    "contrast": label,
                    "module": module,
                    "omitted_donor": donor,
                    "estimate": estimate,
                    "same_sign_as_full": bool(
                        estimate == 0 if difference == 0 else math.copysign(1, estimate) == math.copysign(1, difference)
                    ),
                }
            )
        sign_stable = all(
            value != 0 and math.copysign(1, value) == math.copysign(1, difference)
            for value in loo_values
        )
        ci_excludes_zero = low > 0 or high < 0
        gate_pass = bool(max_t_p[index] <= 0.05 and ci_excludes_zero and sign_stable)
        if gate_pass:
            verdict = pass_verdict
        elif nominal_p[index] > 0.05 and low <= 0 <= high:
            verdict = "not_supported"
        else:
            verdict = "inconclusive"
        rows.append(
            {
                "contrast": label,
                "group_a": group_a,
                "group_b": group_b,
                "module": module,
                "n_a": len(a),
                "n_b": len(b),
                "donors_a": ";".join(left.donor),
                "donors_b": ";".join(right.donor),
                "shared_donors_removed": ";".join(shared),
                "mean_a": float(a.mean()),
                "sd_a": float(a.std(ddof=1)),
                "mean_b": float(b.mean()),
                "sd_b": float(b.std(ddof=1)),
                "difference_a_minus_b": difference,
                "hedges_g": hedges_g(a, b),
                "welch_t": float(observed_t[index]),
                "bootstrap_ci_low": low,
                "bootstrap_ci_high": high,
                "exact_permutation_p": float(nominal_p[index]),
                "max_t_fwer_p": float(max_t_p[index]),
                "n_exact_assignments": assignments,
                "leave_one_out_sign_stable": sign_stable,
                "verdict": verdict,
            }
        )
    return pd.DataFrame(rows), pd.DataFrame(loo_rows)


def synthetic_checks() -> dict[str, Any]:
    fixture = np.random.default_rng(SEED - 1).normal(size=(7, 4))
    vector_t, vector_nominal, vector_max_t, _ = exact_family_test(fixture, 3)
    fixture_stats: list[np.ndarray] = []
    for selected in itertools.combinations(range(len(fixture)), 3):
        selected_set = set(selected)
        left = fixture[list(selected)]
        right = fixture[
            [index for index in range(len(fixture)) if index not in selected_set]
        ]
        fixture_stats.append(
            np.asarray([welch_t(left[:, index], right[:, index]) for index in range(4)])
        )
    naive_null = np.abs(np.vstack(fixture_stats))
    naive_observed = np.asarray(
        [welch_t(fixture[:3, index], fixture[3:, index]) for index in range(4)]
    )
    naive_nominal = np.mean(naive_null + 1e-12 >= np.abs(naive_observed), axis=0)
    naive_max_t = np.asarray(
        [
            np.mean(naive_null.max(axis=1) + 1e-12 >= abs(value))
            for value in naive_observed
        ]
    )
    naive_engine_match = bool(
        np.allclose(vector_t, naive_observed, atol=1e-12)
        and np.allclose(vector_nominal, naive_nominal, atol=1e-12)
        and np.allclose(vector_max_t, naive_max_t, atol=1e-12)
    )
    seeds = [SEED, SEED + 1, SEED + 2]
    per_seed: list[dict[str, Any]] = []
    null_min_p: list[float] = []
    planted_p: list[float] = []
    for seed in seeds:
        rng = np.random.default_rng(seed)
        passes = 0
        for _ in range(NULL_FAMILIES_PER_SEED):
            matrix = rng.normal(size=(15, len(TEST_MODULES)))
            _, _, max_p, _ = exact_family_test(matrix, 8)
            passes += int(np.any(max_p <= 0.05))
            null_min_p.append(float(max_p.min()))
        planted = rng.normal(size=(15, len(TEST_MODULES)))
        planted[:8, 0] += 4.0
        _, _, planted_max_p, _ = exact_family_test(planted, 8)
        planted_p.append(float(planted_max_p[0]))
        per_seed.append(
            {
                "seed": seed,
                "null_replicates": NULL_FAMILIES_PER_SEED,
                "null_family_passes": passes,
                "null_family_pass_rate": passes / NULL_FAMILIES_PER_SEED,
                "planted_max_t_fwer_p": float(planted_max_p[0]),
            }
        )
    null_passes = sum(item["null_family_passes"] for item in per_seed)
    null_replicates = sum(item["null_replicates"] for item in per_seed)
    excess_fwer_p = float(
        binomtest(null_passes, null_replicates, p=0.05, alternative="greater").pvalue
    )
    checks = {
        "synthetic_only_not_biological_evidence": True,
        "seeds": seeds,
        "per_seed": per_seed,
        "null_replicates": null_replicates,
        "null_family_passes": null_passes,
        "null_family_pass_rate": null_passes / null_replicates,
        "one_sided_binomial_p_for_excess_over_0_05": excess_fwer_p,
        "vectorized_engine_matches_naive_enumeration": naive_engine_match,
        "null_min_max_t_p": min(null_min_p),
        "planted_module": TEST_MODULES[0],
        "planted_shift_sd": 4.0,
        "planted_max_t_fwer_p_by_seed": planted_p,
        "null_check_pass": excess_fwer_p >= 0.01 and naive_engine_match,
        "planted_check_pass": bool(all(value <= 0.05 for value in planted_p)),
    }
    if not checks["null_check_pass"] or not checks["planted_check_pass"]:
        raise RuntimeError(f"Synthetic method checks failed: {checks}")
    return checks


def build_report(
    coverage: pd.DataFrame,
    donor_scores: pd.DataFrame,
    primary: pd.DataFrame,
    secondary: pd.DataFrame,
    batch_overlap: pd.DataFrame,
    common_slides: list[str],
    missing_raw_dcc: list[str],
    checks: dict[str, Any],
) -> str:
    primary_sorted = primary.sort_values(["max_t_fwer_p", "exact_permutation_p"])
    passed = primary.loc[primary.verdict.eq("brl_specific_gate_pass")]
    top = primary_sorted.iloc[0]
    lines = [
        "# V56 Donor-Level Broad-Rim-Lesion Module Test",
        "",
        "## Verdict",
        "",
    ]
    if passed.empty:
        lines.append(
            "**No pre-existing V54 route cleared the frozen BRL-specific association gate.**"
        )
    else:
        names = ", ".join(passed.module.tolist())
        lines.append(f"**Frozen primary result: {names} cleared the first association gate.**")
        lines.append("")
        lines.append(
            "**Overall interpretation: inconclusive for route advancement. No module clears the post-result "
            "common-slide sensitivity, and matched NAWM is absent from the processed deposit.**"
        )
    lines.extend(
        [
            "",
            "This is a donor-aggregated reanalysis of a progression-associated postmortem lesion phenotype. "
            "It is not evidence that any intervention slows disability, and it does not establish a causal target.",
            "",
            "## Cohort And Audit",
            "",
            f"- Source matrix: 120 quality-controlled lesion AOIs, {donor_scores.donor.nunique()} unique MS donors.",
            f"- Donor-state units: {len(donor_scores)}. Primary BRL donors: {int((donor_scores.lesion_type == 'BRL_RIM').sum())}; mixed-rim donors: {int((donor_scores.lesion_type == 'mixed_RIM').sum())}.",
            f"- Frozen-module coverage: {int(coverage.valid_for_test.sum())}/9 valid. Under-covered modules remain untestable and were not redefined.",
            f"- Raw GEO identity audit: {120 - len(missing_raw_dcc)}/120 processed AOIs have a deposited DCC. The source workbook contains all 120, but raw reconstruction cannot exactly reproduce `{';'.join(missing_raw_dcc) if missing_raw_dcc else 'none missing'}`.",
            "- Every primary p-value enumerates all donor-label assignments; max-T controls all valid frozen modules.",
            "- NAWM expression was not present in the deposited processed matrix. The stronger matched-NAWM difference-of-differences is therefore blocked pending raw reconstruction and was not approximated.",
            f"- Synthetic method checks: vectorized exact engine versus independent naive enumeration = {checks['vectorized_engine_matches_naive_enumeration']}; {checks['null_family_passes']}/{checks['null_replicates']} null families passed at max-T <= 0.05 across three seeds (one-sided binomial p for excess over 0.05={checks['one_sided_binomial_p_for_excess_over_0_05']:.4f}); planted 4-SD max-T p-values were {', '.join(f'{value:.6g}' for value in checks['planted_max_t_fwer_p_by_seed'])}. Synthetic results characterize code behavior only, never MS biology.",
            "",
        ]
    )
    invalid = coverage.loc[~coverage.valid_for_test]
    if not invalid.empty:
        lines.extend(["", "## Untestable Frozen Modules", ""])
        for row in invalid.itertuples(index=False):
            lines.append(
                f"- `{row.module}`: {row.n_variable}/{row.n_requested} variable genes "
                f"(required {row.required_variable_genes}); absent/constant: `{row.absent_or_constant_genes}`."
            )
        lines.extend(["", "No missing module was rescued with a substitute gene set.", ""])
    lines.extend(
        [
            "## Primary Results: BRL Rim Versus Classical Mixed Rim",
            "",
            "| module | difference | Hedges g | exact p | max-T FWER p | bootstrap 95% CI | LOO sign | verdict |",
            "|---|---:|---:|---:|---:|---:|---|---|",
        ]
    )
    for row in primary_sorted.itertuples(index=False):
        lines.append(
            f"| `{row.module}` | {row.difference_a_minus_b:.3f} | {row.hedges_g:.3f} | "
            f"{row.exact_permutation_p:.4f} | {row.max_t_fwer_p:.4f} | "
            f"[{row.bootstrap_ci_low:.3f}, {row.bootstrap_ci_high:.3f}] | "
            f"{'stable' if row.leave_one_out_sign_stable else 'unstable'} | `{row.verdict}` |"
        )
    lines.extend(
        [
            "",
            "The numerically strongest primary module was "
            f"`{top.module}` (difference {top.difference_a_minus_b:.3f}, max-T FWER p={top.max_t_fwer_p:.4f}). "
            "Its status follows the frozen multi-part gate, not its rank.",
            "",
            "## Post-Result Acquisition-Batch Sensitivity",
            "",
            "This adversarial sensitivity was specified after the frozen result was visible and therefore cannot "
            "confirm or upgrade it. Early slides contained BRL but no mixed-rim AOIs. The source matrix had already "
            "been batch-corrected by the authors, but residual acquisition confounding remains plausible. The "
            f"sensitivity retains only the {len(common_slides)} slides containing both primary lesion types: "
            f"`{';'.join(common_slides)}`.",
            "",
            "| module | donors BRL/mixed | difference | exact p | max-T FWER p | LOO sign | sensitivity status |",
            "|---|---:|---:|---:|---:|---|---|",
        ]
    )
    for row in batch_overlap.sort_values(["max_t_fwer_p", "exact_permutation_p"]).itertuples(index=False):
        status = "clears sensitivity" if row.verdict == "sensitivity_gate_pass" else "does not clear sensitivity"
        lines.append(
            f"| `{row.module}` | {row.n_a}/{row.n_b} | {row.difference_a_minus_b:.3f} | "
            f"{row.exact_permutation_p:.4f} | {row.max_t_fwer_p:.4f} | "
            f"{'stable' if row.leave_one_out_sign_stable else 'unstable'} | {status} |"
        )
    sensitivity_passed = batch_overlap.loc[
        batch_overlap.verdict.eq("sensitivity_gate_pass"), "module"
    ].tolist()
    if sensitivity_passed:
        batch_statement = (
            "Modules clearing this post-result sensitivity: "
            + ", ".join(f"`{module}`" for module in sensitivity_passed)
            + ". This remains sensitivity evidence, not a confirmatory gate."
        )
    else:
        batch_statement = (
            "**No module clears the common-slide max-T sensitivity.** Directions remain positive for several "
            "modules, but the available data cannot separate those associations cleanly from acquisition structure."
        )
    lines.extend(
        [
            "",
            batch_statement,
            "",
            "## Secondary Results: BRL Rim Versus Active Center",
            "",
            "Shared donors are removed from both groups before this independent-donor sensitivity analysis.",
            "",
            "| module | difference | max-T FWER p | bootstrap 95% CI | verdict |",
            "|---|---:|---:|---:|---|",
        ]
    )
    for row in secondary.sort_values(["max_t_fwer_p", "exact_permutation_p"]).itertuples(index=False):
        lines.append(
            f"| `{row.module}` | {row.difference_a_minus_b:.3f} | {row.max_t_fwer_p:.4f} | "
            f"[{row.bootstrap_ci_low:.3f}, {row.bootstrap_ci_high:.3f}] | `{row.verdict}` |"
        )
    lines.extend(
        [
            "",
            "## Interpretation Boundary",
            "",
            "The modules were frozen before this dataset was found, but the source publication already reports "
            "broad inflammatory and antigen-presentation enrichment in BRLs. This is therefore a conservative "
            "targeted module reanalysis, not independent discovery. Donor aggregation removes AOI pseudoreplication, "
            "but the processed deposit lacks NAWM and cannot distinguish every BRL shift from generic lesion activation.",
            "",
            "A route may advance only after longitudinal progression association, intervention direction, causal-node "
            "specificity, selective perturbation, collateral-function guardrails, CNS exposure, modality fit, and "
            "independent replication all hold. None of those requirements is supplied by this analysis alone.",
            "",
            "## Provenance",
            "",
            f"- Primary article: {SOURCE_URLS['article']}",
            f"- GEO part 1: {SOURCE_URLS['geo_part_1']}",
            f"- GEO part 2: {SOURCE_URLS['geo_part_2']}",
            f"- Source code: {SOURCE_URLS['analysis_code']}",
            "- Input checksums and exact source locations are in `retrieval_manifest.json`.",
            "- Full module coverage, AOI scores, donor-state scores, exact tests, and leave-one-out results are committed beside this report.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    checks = synthetic_checks()
    expression, annotation = load_processed_matrix()
    missing_raw_dcc = annotation.attrs["processed_samples_missing_raw_dcc"]
    sample_scores, coverage, valid_modules = score_modules(expression, annotation)
    sample_scores["slide"] = sample_scores["sample"].str.extract(r"^(DSP-\d+-[A-Z])")
    if sample_scores["slide"].isna().any():
        raise RuntimeError("Could not parse GeoMx slide identifier")
    donor_scores = (
        sample_scores.groupby(["donor", "lesion_type"], as_index=False)[valid_modules]
        .mean()
        .sort_values(["lesion_type", "donor"])
        .reset_index(drop=True)
    )
    primary, primary_loo = analyze_contrast(
        donor_scores, "BRL_RIM", "mixed_RIM", "brl_vs_mixed", valid_modules
    )
    secondary, secondary_loo = analyze_contrast(
        donor_scores,
        "BRL_RIM",
        "active_center",
        "brl_vs_active",
        valid_modules,
        pass_verdict="secondary_contrast_gate_pass",
    )
    slide_states = sample_scores.groupby("slide")["lesion_type"].agg(set)
    common_slides = sorted(
        slide for slide, states in slide_states.items()
        if {"BRL_RIM", "mixed_RIM"}.issubset(states)
    )
    overlap_scores = sample_scores.loc[sample_scores["slide"].isin(common_slides)]
    overlap_donors = (
        overlap_scores.groupby(["donor", "lesion_type"], as_index=False)[valid_modules]
        .mean()
        .sort_values(["lesion_type", "donor"])
        .reset_index(drop=True)
    )
    batch_overlap, batch_overlap_loo = analyze_contrast(
        overlap_donors,
        "BRL_RIM",
        "mixed_RIM",
        "post_result_common_slide_brl_vs_mixed",
        valid_modules,
        pass_verdict="sensitivity_gate_pass",
    )

    coverage.to_csv(OUT / "module_coverage.tsv", sep="\t", index=False)
    sample_scores.to_csv(OUT / "aoi_module_scores.tsv", sep="\t", index=False)
    donor_scores.to_csv(OUT / "donor_state_module_scores.tsv", sep="\t", index=False)
    primary.to_csv(OUT / "primary_brl_vs_mixed.tsv", sep="\t", index=False)
    secondary.to_csv(OUT / "secondary_brl_vs_active.tsv", sep="\t", index=False)
    batch_overlap.to_csv(
        OUT / "post_result_common_slide_sensitivity.tsv", sep="\t", index=False
    )
    pd.concat([primary_loo, secondary_loo, batch_overlap_loo], ignore_index=True).to_csv(
        OUT / "leave_one_donor_out.tsv", sep="\t", index=False
    )
    (OUT / "synthetic_method_checks.json").write_text(
        json.dumps(checks, indent=2, sort_keys=True) + "\n"
    )
    manifest = {
        "accessed_utc_date": "2026-08-05",
        "external_inputs_are_public_data_not_project_claims": True,
        "sources": SOURCE_URLS,
        "files": {
            str(EXPRESSION_XLSX.relative_to(ROOT)): sha256(EXPRESSION_XLSX),
            str(ANNOTATION_XLSX.relative_to(ROOT)): sha256(ANNOTATION_XLSX),
            "data/raw/gse281805/GSE281805_RAW.tar": sha256(RAW / "GSE281805_RAW.tar"),
            "data/raw/gse281805/GSE264094_RAW.tar": sha256(RAW / "GSE264094_RAW.tar"),
            "data/raw/gse281805/PMC12176629_supplementary.zip": sha256(
                RAW / "PMC12176629_supplementary.zip"
            ),
        },
        "source_workbook_sheets": {
            "expression": "Source_Data_Fig4_a",
            "annotation": "SuppFig_6c_correlation",
        },
        "raw_geo_dcc_count": len(list(RAW.glob("GSM*_DSP-*.dcc.gz"))),
        "processed_source_samples_with_raw_dcc": 120 - len(missing_raw_dcc),
        "processed_source_samples_missing_raw_dcc": missing_raw_dcc,
        "analysis_plan": "docs/plans/V56_GSE281805_BRL_MODULE_TEST.md",
    }
    (OUT / "retrieval_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    )
    report = build_report(
        coverage,
        donor_scores,
        primary,
        secondary,
        batch_overlap,
        common_slides,
        missing_raw_dcc,
        checks,
    )
    (OUT / "REPORT.md").write_text(report)

    print(primary[["module", "difference_a_minus_b", "max_t_fwer_p", "verdict"]].to_string(index=False))
    print(json.dumps(checks, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
