#!/usr/bin/env python3
"""Run the frozen rapid-versus-slow SPMS module test for GSE247181."""

from __future__ import annotations

import itertools
import json
import math
from functools import lru_cache
from pathlib import Path
import re
from typing import Any

import numpy as np
import pandas as pd
from scipy.stats import binomtest, fisher_exact


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis/v56_gse247181_progression_modules"
SEED = 56247181
BOOTSTRAPS = 10_000
NULL_REPLICATES_PER_SEED = 2_000

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


@lru_cache(maxsize=None)
def assignment_matrix(n_total: int, n_a: int) -> np.ndarray:
    assignments = np.zeros((math.comb(n_total, n_a), n_total), dtype=np.float64)
    for row, selected in enumerate(itertools.combinations(range(n_total), n_a)):
        assignments[row, list(selected)] = 1.0
    assignments.flags.writeable = False
    return assignments


def exact_family_test(matrix: np.ndarray, n_a: int) -> tuple[np.ndarray, np.ndarray, np.ndarray, int]:
    n_total = len(matrix)
    n_b = n_total - n_a
    assignments = assignment_matrix(n_total, n_a)
    sums = np.einsum("ij,jk->ik", assignments, matrix, optimize=False)
    differences = sums / n_a - (matrix.sum(axis=0) - sums) / n_b
    observed = matrix[:n_a].mean(axis=0) - matrix[n_a:].mean(axis=0)
    absolute = np.abs(differences)
    tolerance = 1e-12
    nominal = np.mean(absolute + tolerance >= np.abs(observed), axis=0)
    maximum = absolute.max(axis=1)
    max_t = np.asarray([
        np.mean(maximum + tolerance >= abs(value)) for value in observed
    ])
    return observed, nominal, max_t, len(assignments)


def hedges_g(a: np.ndarray, b: np.ndarray) -> float:
    n_a, n_b = len(a), len(b)
    pooled = math.sqrt(float(
        ((n_a - 1) * a.var(ddof=1) + (n_b - 1) * b.var(ddof=1))
        / (n_a + n_b - 2)
    ))
    difference = float(a.mean() - b.mean())
    if pooled == 0:
        return 0.0 if difference == 0 else math.copysign(math.inf, difference)
    correction = 1 - 3 / (4 * (n_a + n_b) - 9)
    return correction * difference / pooled


def bootstrap_interval(a: np.ndarray, b: np.ndarray, seed: int) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    a_index = rng.integers(0, len(a), size=(BOOTSTRAPS, len(a)))
    b_index = rng.integers(0, len(b), size=(BOOTSTRAPS, len(b)))
    values = a[a_index].mean(axis=1) - b[b_index].mean(axis=1)
    low, high = np.quantile(values, [0.025, 0.975])
    return float(low), float(high)


def load_and_score() -> tuple[pd.DataFrame, pd.DataFrame, list[str]]:
    manifest = pd.read_csv(OUT / "retrieval_manifest.tsv", sep="\t")
    expression = pd.read_csv(OUT / "module_gene_expression_rma.tsv", sep="\t")
    expression = expression.set_index("symbol")
    if len(manifest) != 20 or manifest.progression_group.value_counts().to_dict() != {
        "slow": 10, "rapid": 10
    }:
        raise RuntimeError("frozen cohort is not 10 slow plus 10 rapid")
    if expression.index.duplicated().any():
        raise RuntimeError("duplicate gene symbols after deterministic collapse")
    if set(manifest.geo_accession) != set(expression.columns):
        raise RuntimeError("manifest and expression accessions differ")

    scores = manifest[["geo_accession", "progression_group", "sex", "file_name"]].copy()
    coverage_rows: list[dict[str, Any]] = []
    valid_modules: list[str] = []
    for module, genes in MODULES.items():
        present = [gene for gene in genes if gene in expression.index]
        variable = [
            gene for gene in present
            if float(expression.loc[gene].std(ddof=0)) > 0
        ]
        required = (len(genes) + 1) // 2
        mandatory = True
        if module == "mif_ligand":
            mandatory = variable == ["MIF"]
        elif module == "mocci_inflammatory_switch":
            mandatory = set(variable) == {"C15ORF48", "NDUFA4"}
        valid = len(variable) >= required and mandatory
        coverage_rows.append({
            "module": module,
            "n_requested": len(genes),
            "n_present": len(present),
            "n_variable": len(variable),
            "required_variable_genes": required,
            "mandatory_genes_ok": mandatory,
            "valid_for_test": valid,
            "variable_genes": ";".join(variable),
            "absent_or_constant_genes": ";".join(sorted(set(genes) - set(variable))),
        })
        if not valid:
            continue
        selected = expression.loc[variable, manifest.geo_accession].T
        z = (selected - selected.mean(axis=0)) / selected.std(axis=0, ddof=0)
        if module == "mocci_inflammatory_switch":
            values = z["C15ORF48"] - z["NDUFA4"]
        else:
            values = z.mean(axis=1)
        scores[module] = values.loc[scores.geo_accession].to_numpy()
        valid_modules.append(module)
    if not valid_modules:
        raise RuntimeError("no frozen module has valid coverage")
    return scores, pd.DataFrame(coverage_rows), valid_modules


def analyze(scores: pd.DataFrame, modules: list[str]) -> tuple[pd.DataFrame, pd.DataFrame]:
    ordered = pd.concat([
        scores.loc[scores.progression_group.eq("rapid")].sort_values("geo_accession"),
        scores.loc[scores.progression_group.eq("slow")].sort_values("geo_accession"),
    ], ignore_index=True)
    matrix = ordered[modules].to_numpy(dtype=float)
    observed, nominal, max_t, assignments = exact_family_test(matrix, 10)
    rows: list[dict[str, Any]] = []
    loo_rows: list[dict[str, Any]] = []
    for index, module in enumerate(modules):
        rapid = ordered.loc[ordered.progression_group.eq("rapid"), module].to_numpy(float)
        slow = ordered.loc[ordered.progression_group.eq("slow"), module].to_numpy(float)
        difference = float(observed[index])
        low, high = bootstrap_interval(rapid, slow, SEED + index)
        loo_values = []
        for accession in ordered.geo_accession:
            left = ordered.loc[
                ordered.progression_group.eq("rapid") & ordered.geo_accession.ne(accession), module
            ].to_numpy(float)
            right = ordered.loc[
                ordered.progression_group.eq("slow") & ordered.geo_accession.ne(accession), module
            ].to_numpy(float)
            estimate = float(left.mean() - right.mean())
            loo_values.append(estimate)
            loo_rows.append({
                "module": module,
                "omitted_accession": accession,
                "estimate_rapid_minus_slow": estimate,
                "same_sign_as_full": bool(
                    estimate != 0 and difference != 0
                    and math.copysign(1, estimate) == math.copysign(1, difference)
                ),
            })
        sign_stable = all(
            value != 0 and difference != 0
            and math.copysign(1, value) == math.copysign(1, difference)
            for value in loo_values
        )
        ci_excludes_zero = low > 0 or high < 0
        if max_t[index] <= 0.05 and ci_excludes_zero and sign_stable:
            verdict = "association_gate_pass"
        elif nominal[index] > 0.05 and low <= 0 <= high:
            verdict = "not_supported"
        else:
            verdict = "inconclusive"
        rows.append({
            "module": module,
            "n_rapid": len(rapid),
            "n_slow": len(slow),
            "mean_rapid": float(rapid.mean()),
            "sd_rapid": float(rapid.std(ddof=1)),
            "mean_slow": float(slow.mean()),
            "sd_slow": float(slow.std(ddof=1)),
            "difference_rapid_minus_slow": difference,
            "hedges_g": hedges_g(rapid, slow),
            "bootstrap_ci_low": low,
            "bootstrap_ci_high": high,
            "exact_permutation_p": float(nominal[index]),
            "max_t_fwer_p": float(max_t[index]),
            "n_exact_assignments": assignments,
            "leave_one_out_sign_stable": sign_stable,
            "verdict": verdict,
        })
    return pd.DataFrame(rows), pd.DataFrame(loo_rows)


def qc_group_checks(scores: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, Any]]:
    qc = pd.read_csv(OUT / "sample_qc.tsv", sep="\t")
    frame = scores[["geo_accession", "progression_group", "sex", "file_name"]].merge(
        qc, on=["geo_accession", "progression_group"], validate="one_to_one"
    )
    run_number = frame.file_name.str.extract(r"_R(\d+)_", expand=False)
    frame["deposited_file_r_number"] = pd.to_numeric(run_number, errors="coerce")
    metrics = [
        "raw_median_intensity", "raw_intensity_iqr", "normalized_median",
        "normalized_iqr", "pca1", "pca2", "deposited_file_r_number",
    ]
    ordered = pd.concat([
        frame.loc[frame.progression_group.eq("rapid")].sort_values("geo_accession"),
        frame.loc[frame.progression_group.eq("slow")].sort_values("geo_accession"),
    ], ignore_index=True)
    matrix = ordered[metrics].to_numpy(float)
    standardized = (matrix - matrix.mean(axis=0)) / matrix.std(axis=0, ddof=0)
    observed, nominal, max_t, assignments = exact_family_test(standardized, 10)
    result = pd.DataFrame({
        "diagnostic": metrics,
        "standardized_difference_rapid_minus_slow": observed,
        "exact_permutation_p": nominal,
        "max_t_fwer_p": max_t,
        "n_exact_assignments": assignments,
    })
    sex_table = pd.crosstab(frame.progression_group, frame.sex).reindex(
        index=["rapid", "slow"], columns=["F", "M"], fill_value=0
    )
    sex_p = float(fisher_exact(sex_table.to_numpy()).pvalue)
    summary = {
        "sex_counts": {
            group: {sex: int(sex_table.loc[group, sex]) for sex in sex_table.columns}
            for group in sex_table.index
        },
        "fisher_exact_sex_p": sex_p,
        "deposited_file_identifier_warning": (
            "The R-number embedded in deposited CEL names differs by group. GEO does not "
            "identify it as assay order or batch, so it is a design warning rather than a "
            "confirmed technical confounder."
        ),
    }
    return result, summary


def synthetic_checks(n_modules: int) -> dict[str, Any]:
    rng = np.random.default_rng(SEED - 1)
    fixture = rng.normal(size=(8, n_modules))
    observed, nominal, max_t, _ = exact_family_test(fixture, 4)
    naive = []
    for selected in itertools.combinations(range(8), 4):
        selected_set = set(selected)
        left = fixture[list(selected)]
        right = fixture[[index for index in range(8) if index not in selected_set]]
        naive.append(left.mean(axis=0) - right.mean(axis=0))
    naive_array = np.asarray(naive)
    naive_observed = fixture[:4].mean(axis=0) - fixture[4:].mean(axis=0)
    naive_nominal = np.mean(np.abs(naive_array) + 1e-12 >= np.abs(naive_observed), axis=0)
    naive_max = np.asarray([
        np.mean(np.abs(naive_array).max(axis=1) + 1e-12 >= abs(value))
        for value in naive_observed
    ])
    engine_match = bool(
        np.allclose(observed, naive_observed)
        and np.allclose(nominal, naive_nominal)
        and np.allclose(max_t, naive_max)
    )
    single_null_pass = bool(np.any(max_t <= 0.05))

    seeds = [SEED, SEED + 1, SEED + 2]
    assignments = assignment_matrix(12, 6)
    per_seed = []
    total_passes = 0
    for seed in seeds:
        local = np.random.default_rng(seed)
        passes = 0
        batch_size = 100
        for start in range(0, NULL_REPLICATES_PER_SEED, batch_size):
            count = min(batch_size, NULL_REPLICATES_PER_SEED - start)
            null = local.normal(size=(count, 12, n_modules))
            sums = np.einsum("ij,bjk->bik", assignments, null, optimize=False)
            differences = sums / 6 - (null.sum(axis=1)[:, None, :] - sums) / 6
            observed_null = null[:, :6].mean(axis=1) - null[:, 6:].mean(axis=1)
            maximum = np.abs(differences).max(axis=2)
            p_values = np.mean(
                maximum[:, :, None] + 1e-12 >= np.abs(observed_null)[:, None, :],
                axis=1,
            )
            passes += int(np.any(p_values <= 0.05, axis=1).sum())
        total_passes += passes

        planted = local.normal(scale=0.2, size=(12, n_modules))
        planted[:6, 0] += 4.0
        _, _, planted_p, _ = exact_family_test(planted, 6)
        per_seed.append({
            "seed": seed,
            "null_replicates": NULL_REPLICATES_PER_SEED,
            "null_family_passes": passes,
            "null_family_pass_rate": passes / NULL_REPLICATES_PER_SEED,
            "planted_module_max_t_fwer_p": float(planted_p[0]),
        })
    total = len(seeds) * NULL_REPLICATES_PER_SEED
    excess_p = float(binomtest(total_passes, total, p=0.05, alternative="greater").pvalue)
    checks = {
        "synthetic_only_not_biological_evidence": True,
        "vectorized_engine_matches_independent_naive_enumeration": engine_match,
        "single_fixed_null_fixture_any_module_passed": single_null_pass,
        "null_replicates": total,
        "null_family_passes": total_passes,
        "null_family_pass_rate": total_passes / total,
        "one_sided_binomial_p_for_excess_over_0_05": excess_p,
        "per_seed": per_seed,
        "null_check_pass": bool(engine_match and not single_null_pass and excess_p >= 0.01),
        "planted_check_pass": bool(all(row["planted_module_max_t_fwer_p"] <= 0.05 for row in per_seed)),
    }
    if not checks["null_check_pass"] or not checks["planted_check_pass"]:
        raise RuntimeError(f"synthetic method checks failed: {checks}")
    return checks


def report(
    coverage: pd.DataFrame,
    results: pd.DataFrame,
    qc: pd.DataFrame,
    qc_summary: dict[str, Any],
    checks: dict[str, Any],
) -> str:
    passed = results.loc[results.verdict.eq("association_gate_pass")]
    if passed.empty:
        headline = "**No pre-existing V54 progression route cleared the frozen rapid-versus-slow SPMS association gate.**"
    else:
        headline = (
            "**First association gate cleared by: "
            + ", ".join(f"`{name}`" for name in passed.module)
            + ".**"
        )
    lines = [
        "# V56 Rapid-Versus-Slow SPMS PBMC Module Test",
        "",
        "## Verdict",
        "",
        headline,
        "",
        "This is a frozen, cross-sectional reanalysis of 10 deposited rapid/aggressive and 10 slow untreated SPMS participants. It is not prospective prediction, causality, treatment response, evidence that an intervention slows disability, or a therapeutic target.",
        "",
        "## Cohort And Processing",
        "",
        "- Exactly 20 pre-eligible CEL files were processed together: 10 `SPMS-a` (rapid/aggressive) and 10 `SPMS-s` (slow), all deposited as untreated.",
        "- Core-transcript RMA was run with `oligo` 1.76.0 and `pd.clariom.d.human` 3.14.1; identifiers used `clariomdhumantranscriptcluster.db` 8.8.0.",
        f"- Frozen-module coverage: {int(coverage.valid_for_test.sum())}/9 valid. No module was outcome-adapted.",
        "- Every primary test enumerated all 184,756 possible 10/10 label assignments; max-T controlled the complete valid-module family.",
        f"- Synthetic calibration: {checks['null_family_passes']}/{checks['null_replicates']} null families passed (rate {checks['null_family_pass_rate']:.4f}; one-sided p for excess over 0.05={checks['one_sided_binomial_p_for_excess_over_0_05']:.4f}); independent naive and vectorized exact engines matched={checks['vectorized_engine_matches_independent_naive_enumeration']}; planted signals passed in all three seeds. Synthetic results characterize code only.",
        "",
        "## Frozen Primary Results",
        "",
        "| module | rapid-slow difference | Hedges g | exact p | max-T FWER p | bootstrap 95% CI | LOO sign | verdict |",
        "|---|---:|---:|---:|---:|---:|---|---|",
    ]
    for row in results.sort_values(["max_t_fwer_p", "exact_permutation_p"]).itertuples(index=False):
        lines.append(
            f"| `{row.module}` | {row.difference_rapid_minus_slow:.3f} | {row.hedges_g:.3f} | "
            f"{row.exact_permutation_p:.4f} | {row.max_t_fwer_p:.4f} | "
            f"[{row.bootstrap_ci_low:.3f}, {row.bootstrap_ci_high:.3f}] | "
            f"{'stable' if row.leave_one_out_sign_stable else 'unstable'} | `{row.verdict}` |"
        )
    lines.extend([
        "",
        "## Technical And Demographic Audit",
        "",
        f"- Sex counts were rapid {qc_summary['sex_counts']['rapid']} and slow {qc_summary['sex_counts']['slow']} (Fisher exact p={qc_summary['fisher_exact_sex_p']:.4f}). Age was not deposited, so the frozen secondary age/sex model could not run.",
        f"- {qc_summary['deposited_file_identifier_warning']}",
        "- RMA distribution and global-PCA diagnostics were tested as a separate max-T family and did not remove samples. Results:",
        "",
        "| diagnostic | standardized rapid-slow difference | exact p | max-T FWER p |",
        "|---|---:|---:|---:|",
    ])
    for row in qc.sort_values("max_t_fwer_p").itertuples(index=False):
        lines.append(
            f"| `{row.diagnostic}` | {row.standardized_difference_rapid_minus_slow:.3f} | "
            f"{row.exact_permutation_p:.4f} | {row.max_t_fwer_p:.4f} |"
        )
    lines.extend([
        "",
        "## Therapeutic Boundary",
        "",
        "A module that clears this association gate would still need pathogenic direction, causal-node specificity, selective functional perturbation, collateral guardrails, CNS exposure, modality fit, and independent longitudinal replication. A failed or inconclusive module is not rescued by its effect-size rank. No result here is intervention-grade.",
        "",
        "## Reproducibility",
        "",
        "- Frozen plan: `docs/plans/V56_GSE247181_RAPID_SLOW_PROGRESSION_TEST.md`",
        "- Selector/downloader: `scripts/v56_prepare_gse247181.py`",
        "- RMA processor: `scripts/v56_process_gse247181.R`",
        "- Exact analysis: `scripts/v56_analyze_gse247181.py`",
        "- Public source: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE247181",
        "- Every input URL, expected byte count, and local SHA-256 is in `retrieval_manifest.tsv`; raw CEL files remain ignored.",
        "",
    ])
    return "\n".join(lines)


def main() -> None:
    scores, coverage, modules = load_and_score()
    checks = synthetic_checks(len(modules))
    results, loo = analyze(scores, modules)
    qc, qc_summary = qc_group_checks(scores)
    coverage.to_csv(OUT / "module_coverage_analysis.tsv", sep="\t", index=False)
    scores.to_csv(OUT / "participant_module_scores.tsv", sep="\t", index=False)
    results.to_csv(OUT / "primary_rapid_vs_slow.tsv", sep="\t", index=False)
    loo.to_csv(OUT / "leave_one_participant_out.tsv", sep="\t", index=False)
    qc.to_csv(OUT / "qc_group_checks.tsv", sep="\t", index=False)
    (OUT / "qc_summary.json").write_text(json.dumps(qc_summary, indent=2, sort_keys=True) + "\n")
    (OUT / "synthetic_method_checks.json").write_text(json.dumps(checks, indent=2, sort_keys=True) + "\n")
    (OUT / "REPORT.md").write_text(report(coverage, results, qc, qc_summary, checks))
    print(results[["module", "difference_rapid_minus_slow", "max_t_fwer_p", "verdict"]].to_string(index=False))
    print(json.dumps(checks, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
