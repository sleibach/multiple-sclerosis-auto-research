#!/usr/bin/env python3
"""Run the frozen V54 chronic-lesion state analysis in two held datasets."""

from __future__ import annotations

import gzip
import itertools
import json
import tarfile
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import statsmodels.api as sm


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw"
OUT = ROOT / "analysis/v54_progression_lesion_state"

MODULES = {
    "receptor_cd44_cxcr4": ["CD44", "CXCR4"],
    "hla_regulatory": ["CIITA", "RFX5"],
    "ifn_apc_unique": ["STAT1", "IRF1", "CXCL10", "GBP1"],
    "lysosomal_unique": ["CTSS", "CTSB", "CTSD", "LAMP1", "LAMP2", "LAMP3"],
    "complement_phagocytosis": [
        "C1QA", "C1QB", "C1QC", "C3", "ITGAM", "ITGB2", "TYROBP", "AIF1"
    ],
    "lipid_repair": [
        "APOE", "LPL", "TREM2", "ABCA1", "ABCG1", "SPP1", "LGALS3", "GPNMB"
    ],
}
ADJUSTMENT = {
    "b_apc_composition": ["CD79A", "MS4A1", "CD74", "HLA-DRA", "HLA-DPA1", "HLA-DPB1"]
}
ALL_MODULES = {**MODULES, **ADJUSTMENT}
TARGET_GENES = sorted({gene for genes in ALL_MODULES.values() for gene in genes})
TEST_MODULES = list(MODULES)
SEEDS = [54101, 54102, 54103]
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


def add_scores(frame: pd.DataFrame, modules: dict[str, list[str]]) -> tuple[pd.DataFrame, list[dict[str, Any]]]:
    output = frame.copy()
    coverage: list[dict[str, Any]] = []
    for module, genes in modules.items():
        present = [gene for gene in genes if gene in output.columns]
        absent = sorted(set(genes) - set(present))
        if not present:
            raise RuntimeError(f"No genes present for frozen module {module}")
        standardized = output[present].copy()
        sd = standardized.std(axis=0, ddof=0)
        valid = sd[sd > 0].index.tolist()
        if not valid:
            raise RuntimeError(f"Zero variance for all genes in {module}")
        standardized = (standardized[valid] - standardized[valid].mean()) / sd[valid]
        output[module] = standardized.mean(axis=1)
        module_sd = output[module].std(ddof=0)
        if not np.isfinite(module_sd) or module_sd == 0:
            raise RuntimeError(f"Invalid module variance for {module}")
        output[module] = (output[module] - output[module].mean()) / module_sd
        coverage.append(
            {
                "module": module,
                "n_requested": len(genes),
                "n_present": len(present),
                "n_variable": len(valid),
                "present_genes": ";".join(valid),
                "absent_genes": ";".join(absent),
            }
        )
    return output, coverage


def read_gse180759() -> tuple[pd.DataFrame, list[dict[str, Any]]]:
    annotation = pd.read_csv(RAW / "GSE180759_annotation.txt.gz", sep="\t")
    expected = annotation.nucleus_barcode.tolist()
    totals = np.zeros(len(annotation), dtype=np.float64)
    selected = {gene: np.zeros(len(annotation), dtype=np.float64) for gene in TARGET_GENES}
    found: set[str] = set()
    with gzip.open(RAW / "GSE180759_expression_matrix.csv.gz", "rt") as handle:
        observed = handle.readline().rstrip("\n").split(",")
        if observed != expected:
            raise RuntimeError("GSE180759 expression/annotation barcode mismatch")
        for line in handle:
            gene, values_text = line.rstrip("\n").split(",", 1)
            values = np.fromstring(values_text, sep=",", dtype=np.float64)
            if len(values) != len(annotation):
                raise RuntimeError(f"GSE180759 column mismatch for {gene}")
            totals += values
            if gene in selected:
                selected[gene] += values
                found.add(gene)
    annotation = annotation.copy()
    annotation["library_size"] = totals
    for gene in sorted(found):
        annotation[gene] = selected[gene]
    group_columns = ["NBB_case", "pathology", "cell_type"]
    aggregation: dict[str, str] = {"nucleus_barcode": "size", "library_size": "sum"}
    aggregation.update({gene: "sum" for gene in sorted(found)})
    pseudo = annotation.groupby(group_columns, observed=True).agg(aggregation).reset_index()
    pseudo = pseudo.rename(columns={"nucleus_barcode": "n_nuclei"})
    for gene in sorted(found):
        pseudo[gene] = np.log2(pseudo[gene] / pseudo.library_size * 1_000_000 + 1)
    eligible = pseudo[(pseudo.cell_type.eq("immune")) & (pseudo.n_nuclei >= 20)].copy()
    scored, coverage = add_scores(eligible, MODULES)
    keep = group_columns + ["n_nuclei", "library_size"] + sorted(found) + TEST_MODULES
    scored[keep].to_csv(OUT / "gse180759_immune_pseudobulk_scores.tsv", sep="\t", index=False)
    return scored, coverage


def exact_paired_tests(scored: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    active = "chronic_active_MS_lesion_edge"
    primary_comp = "chronic_inactive_MS_lesion_edge"
    differences: dict[str, np.ndarray] = {}
    primary_donors: list[str] | None = None
    for module in TEST_MODULES:
        left = scored[scored.pathology.eq(active)][["NBB_case", module]]
        right = scored[scored.pathology.eq(primary_comp)][["NBB_case", module]]
        paired = left.merge(right, on="NBB_case", suffixes=("_active", "_reference"))
        if primary_donors is None:
            primary_donors = paired.NBB_case.tolist()
        elif primary_donors != paired.NBB_case.tolist():
            raise RuntimeError("Primary paired donors differ across modules")
        differences[module] = (
            paired[f"{module}_active"] - paired[f"{module}_reference"]
        ).to_numpy(dtype=float)
    n_pairs = len(primary_donors or [])
    if n_pairs < 2:
        raise RuntimeError("Too few primary GSE180759 donor pairs")
    sign_patterns = np.asarray(list(itertools.product([-1.0, 1.0], repeat=n_pairs)))
    null = np.column_stack(
        [np.mean(sign_patterns * differences[module][None, :], axis=1) for module in TEST_MODULES]
    )
    observed = np.asarray([differences[module].mean() for module in TEST_MODULES])
    absolute = np.abs(null)
    max_null = absolute.max(axis=1)
    p_values = [float(np.mean(absolute[:, i] >= abs(observed[i]))) for i in range(len(TEST_MODULES))]
    max_p = [float(np.mean(max_null >= abs(value))) for value in observed]
    q_values = bh(p_values)
    primary_rows = []
    for index, module in enumerate(TEST_MODULES):
        diff = differences[module]
        primary_rows.append(
            {
                "module": module,
                "n_paired_donors": n_pairs,
                "donors": ";".join(primary_donors or []),
                "mean_active_minus_inactive": float(diff.mean()),
                "median_active_minus_inactive": float(np.median(diff)),
                "n_positive": int(np.sum(diff > 0)),
                "n_negative": int(np.sum(diff < 0)),
                "exact_sign_flip_p": p_values[index],
                "bh_q": q_values[index],
                "max_t_fwer_p": max_p[index],
            }
        )
    sensitivity_rows = []
    for comparator in ["MS_periplaque_white_matter", "MS_lesion_core"]:
        for module in TEST_MODULES:
            left = scored[scored.pathology.eq(active)][["NBB_case", module]]
            right = scored[scored.pathology.eq(comparator)][["NBB_case", module]]
            paired = left.merge(right, on="NBB_case", suffixes=("_active", "_reference"))
            diff = paired[f"{module}_active"] - paired[f"{module}_reference"]
            sensitivity_rows.append(
                {
                    "comparator": comparator,
                    "module": module,
                    "n_paired_donors": len(paired),
                    "donors": ";".join(paired.NBB_case.astype(str)),
                    "mean_active_minus_comparator": float(diff.mean()) if len(diff) else np.nan,
                    "n_positive": int((diff > 0).sum()),
                    "n_negative": int((diff < 0).sum()),
                    "inferential_status": "descriptive_n_lt_3" if len(paired) < 3 else "eligible_sensitivity",
                }
            )
    return pd.DataFrame(primary_rows), pd.DataFrame(sensitivity_rows)


def parse_soft_mapping() -> pd.DataFrame:
    records: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    with gzip.open(RAW / "GSE279972_family.soft.gz", "rt", errors="replace") as handle:
        for raw in handle:
            line = raw.rstrip("\n")
            if line.startswith("^SAMPLE = "):
                if current:
                    records.append(current)
                current = {"gsm": line.split(" = ", 1)[1]}
            elif current is not None and line.startswith("!Sample_characteristics_ch1 = "):
                item = line.split(" = ", 1)[1]
                if ": " in item:
                    key, value = item.split(": ", 1)
                    current[key.replace(" ", "_")] = value
        if current:
            records.append(current)
    frame = pd.DataFrame(records)
    if "sample_code" not in frame.columns:
        raise RuntimeError("GSE279972 SOFT lacks sample_code mapping")
    return frame[["gsm", "sample_code"]]


def read_gse279972() -> tuple[pd.DataFrame, list[dict[str, Any]]]:
    records: list[dict[str, float | str]] = []
    with tarfile.open(RAW / "GSE279972_RAW.tar") as archive:
        for member in archive.getmembers():
            if not member.isfile() or not member.name.endswith(".count.txt.gz"):
                continue
            source = archive.extractfile(member)
            if source is None:
                continue
            gsm = member.name.split("_", 1)[0]
            counts = {gene: 0.0 for gene in TARGET_GENES}
            total = 0.0
            with gzip.GzipFile(fileobj=source) as nested:
                for raw in nested:
                    fields = raw.decode().rstrip("\n").split("\t")
                    if len(fields) != 3:
                        continue
                    value = float(fields[2])
                    total += value
                    if fields[1] in counts:
                        counts[fields[1]] += value
            row: dict[str, float | str] = {"gsm": gsm, "library_size": total}
            for gene, value in counts.items():
                row[gene] = np.log2(value / total * 1_000_000 + 1)
            records.append(row)
    expression = pd.DataFrame(records).merge(parse_soft_mapping(), on="gsm", validate="one_to_one")
    metadata = pd.read_csv(ROOT / "data/derived/gse279972_sample_metadata.tsv", sep="\t")
    expression = expression.merge(metadata, on="sample_code", validate="one_to_one")
    is_ms = expression.is_ms.eq(True) | expression.is_ms.astype(str).str.lower().eq("true")
    eligible = expression[
        is_ms & expression.morphology.isin(["foamy", "non_foamy"])
    ].copy()
    scored, coverage = add_scores(eligible, ALL_MODULES)
    scored["foamy"] = scored.morphology.eq("foamy").astype(int)
    keep = [
        "gsm", "sample_code", "donor", "Lesion_type_6", "morphology", "foamy", "library_size"
    ] + TARGET_GENES + list(ALL_MODULES)
    scored[keep].to_csv(OUT / "gse279972_morphology_scores.tsv", sep="\t", index=False)
    return scored, coverage


def morphology_tests(scored: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    lesion = pd.get_dummies(scored.Lesion_type_6.astype(str), prefix="lesion", drop_first=True, dtype=float)
    reduced = pd.DataFrame({"intercept": 1.0, "b_apc_composition": scored.b_apc_composition})
    reduced = pd.concat([reduced.reset_index(drop=True), lesion.reset_index(drop=True)], axis=1)
    full = reduced.copy()
    full.insert(1, "foamy", scored.foamy.to_numpy(dtype=float))
    x = full.to_numpy(dtype=float)
    x0 = reduced.to_numpy(dtype=float)
    if np.linalg.matrix_rank(x) != x.shape[1] or np.linalg.matrix_rank(x0) != x0.shape[1]:
        raise RuntimeError("Rank-deficient GSE279972 morphology design")
    y = scored[TEST_MODULES].to_numpy(dtype=float)
    full_pinv = np.linalg.solve(x.T @ x, x.T)
    reduced_pinv = np.linalg.solve(x0.T @ x0, x0.T)
    observed = full_pinv[1] @ y
    fitted0 = x0 @ (reduced_pinv @ y)
    residual0 = y - fitted0
    donor_codes, donors = pd.factorize(scored.donor.astype(str), sort=True)
    n_donors = len(donors)

    cluster_rows: list[dict[str, Any]] = []
    for index, module in enumerate(TEST_MODULES):
        model = sm.OLS(y[:, index], x).fit(
            cov_type="cluster",
            cov_kwds={"groups": scored.donor.astype(str), "use_correction": True},
        )
        ci = model.conf_int()[1]
        cluster_rows.append(
            {
                "module": module,
                "foamy_adjusted_beta": float(model.params[1]),
                "cluster_ci_low": float(ci[0]),
                "cluster_ci_high": float(ci[1]),
                "cluster_p": float(model.pvalues[1]),
            }
        )
    aggregate_exceed = np.zeros(len(TEST_MODULES), dtype=np.int64)
    aggregate_max = np.zeros(len(TEST_MODULES), dtype=np.int64)
    seed_rows: list[dict[str, Any]] = []
    beta_weight = full_pinv[1]
    for seed in SEEDS:
        rng = np.random.default_rng(seed)
        seed_exceed = np.zeros(len(TEST_MODULES), dtype=np.int64)
        seed_max = np.zeros(len(TEST_MODULES), dtype=np.int64)
        completed = 0
        while completed < N_PER_SEED:
            batch = min(BATCH, N_PER_SEED - completed)
            signs_by_donor = rng.choice([-1.0, 1.0], size=(batch, n_donors))
            signs = signs_by_donor[:, donor_codes]
            synthetic = fitted0[None, :, :] + signs[:, :, None] * residual0[None, :, :]
            null_beta = np.einsum("i,bim->bm", beta_weight, synthetic)
            if not np.isfinite(null_beta).all():
                raise RuntimeError("Non-finite GSE279972 wild-null coefficient")
            absolute = np.abs(null_beta)
            seed_exceed += np.sum(absolute >= np.abs(observed)[None, :], axis=0)
            max_abs = absolute.max(axis=1)
            seed_max += np.sum(max_abs[:, None] >= np.abs(observed)[None, :], axis=0)
            completed += batch
        aggregate_exceed += seed_exceed
        aggregate_max += seed_max
        for index, module in enumerate(TEST_MODULES):
            seed_rows.append(
                {
                    "seed": seed,
                    "module": module,
                    "n_wild_replicates": N_PER_SEED,
                    "wild_p": (1 + int(seed_exceed[index])) / (N_PER_SEED + 1),
                    "max_t_fwer_p": (1 + int(seed_max[index])) / (N_PER_SEED + 1),
                }
            )
    total = len(SEEDS) * N_PER_SEED
    p = ((1 + aggregate_exceed) / (total + 1)).tolist()
    max_p = ((1 + aggregate_max) / (total + 1)).tolist()
    q = bh(p)

    leave_rows: list[dict[str, Any]] = []
    for donor in donors:
        keep = scored.donor.astype(str).ne(str(donor)).to_numpy()
        x_leave = x[keep]
        if np.linalg.matrix_rank(x_leave) != x_leave.shape[1]:
            leave_rows.append({"left_out_donor": donor, "module": "ALL", "status": "rank_deficient"})
            continue
        pinv = np.linalg.solve(x_leave.T @ x_leave, x_leave.T)
        beta = pinv[1] @ y[keep]
        for index, module in enumerate(TEST_MODULES):
            leave_rows.append(
                {
                    "left_out_donor": donor,
                    "module": module,
                    "status": "estimated",
                    "foamy_adjusted_beta": float(beta[index]),
                }
            )
    leave = pd.DataFrame(leave_rows)
    table_rows = []
    for index, row in enumerate(cluster_rows):
        estimates = leave[(leave.module.eq(row["module"])) & leave.status.eq("estimated")]
        table_rows.append(
            {
                **row,
                "donor_wild_p": p[index],
                "bh_q": q[index],
                "max_t_fwer_p": max_p[index],
                "leave_one_donor_min_beta": float(estimates.foamy_adjusted_beta.min()),
                "leave_one_donor_max_beta": float(estimates.foamy_adjusted_beta.max()),
                "leave_one_donor_direction_retained": bool(
                    np.all(np.sign(estimates.foamy_adjusted_beta) == np.sign(row["foamy_adjusted_beta"]))
                ),
                "n_samples": len(scored),
                "n_donors": n_donors,
            }
        )
    return pd.DataFrame(table_rows), pd.DataFrame(seed_rows), leave


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    gse180, coverage180 = read_gse180759()
    paired, sensitivity = exact_paired_tests(gse180)
    paired.to_csv(OUT / "gse180759_active_inactive_exact_tests.tsv", sep="\t", index=False)
    sensitivity.to_csv(OUT / "gse180759_paired_sensitivities.tsv", sep="\t", index=False)
    coverage180_table = pd.DataFrame(coverage180).assign(dataset="GSE180759")

    gse279, coverage279 = read_gse279972()
    morphology, seed_stability, leave = morphology_tests(gse279)
    morphology.to_csv(OUT / "gse279972_morphology_tests.tsv", sep="\t", index=False)
    seed_stability.to_csv(OUT / "gse279972_seed_stability.tsv", sep="\t", index=False)
    leave.to_csv(OUT / "gse279972_leave_one_donor.tsv", sep="\t", index=False)
    coverage = pd.concat(
        [coverage180_table, pd.DataFrame(coverage279).assign(dataset="GSE279972")],
        ignore_index=True,
    )
    coverage.to_csv(OUT / "module_gene_coverage.tsv", sep="\t", index=False)

    joined = paired.merge(morphology, on="module", validate="one_to_one")
    outcomes = []
    for _, row in joined.iterrows():
        all_active_positive = row.n_positive == row.n_paired_donors
        all_active_negative = row.n_negative == row.n_paired_donors
        paired_direction = 1 if all_active_positive else -1 if all_active_negative else 0
        morphology_direction = int(np.sign(row.foamy_adjusted_beta))
        same_direction = paired_direction != 0 and paired_direction == morphology_direction
        morphology_pass = bool(
            row.donor_wild_p <= 0.05
            and row.bh_q_y <= 0.10
            and row.max_t_fwer_p_y <= 0.10
            and row.leave_one_donor_direction_retained
        )
        outcome = (
            "orthogonally_consistent_needs_data"
            if same_direction and morphology_pass
            else "inconclusive"
            if same_direction
            else "not_supported"
        )
        outcomes.append(
            {
                "module": row.module,
                "gse180759_mean_active_minus_inactive": row.mean_active_minus_inactive,
                "gse180759_all_pairs_same_direction": paired_direction != 0,
                "gse180759_exact_p": row.exact_sign_flip_p,
                "gse180759_max_t_p": row.max_t_fwer_p_x,
                "gse279972_foamy_adjusted_beta": row.foamy_adjusted_beta,
                "gse279972_donor_wild_p": row.donor_wild_p,
                "gse279972_bh_q": row.bh_q_y,
                "gse279972_max_t_p": row.max_t_fwer_p_y,
                "cross_context_direction_concordant": same_direction,
                "outcome": outcome,
            }
        )
    outcome_table = pd.DataFrame(outcomes)
    outcome_table.to_csv(OUT / "cross_context_outcomes.tsv", sep="\t", index=False)
    promising = outcome_table[
        outcome_table.outcome.eq("orthogonally_consistent_needs_data")
    ].module.tolist()
    summary = {
        "purpose": "Frozen progression-lesion state test; pathology context only, not clinical progression evidence",
        "gse180759_n_primary_pairs": int(paired.n_paired_donors.iloc[0]),
        "gse180759_min_exact_p": float(paired.exact_sign_flip_p.min()),
        "gse279972_n_samples": len(gse279),
        "gse279972_n_donors": int(gse279.donor.nunique()),
        "n_donor_wild_replicates": len(SEEDS) * N_PER_SEED,
        "orthogonally_consistent_needs_data_modules": promising,
        "n_orthogonally_consistent_needs_data": len(promising),
        "verdict": (
            "BOUNDED_ORTHOGONAL_PATHOLOGY_CONTEXT"
            if promising
            else "NO_ORTHOGONALLY_SUPPORTED_PROGRESSION_LESION_MODULE"
        ),
        "boundary": (
            "Chronic-active edge and foamy morphology are non-identical cross-sectional pathology contexts; neither measures disability accumulation or treatment benefit."
        ),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")

    report = [
        "# V54 Progression-Lesion State Test",
        "",
        f"Verdict: **{summary['verdict']}**.",
        "",
        "GSE180759 used donor/pathology immune pseudobulks with at least 20 nuclei",
        "and exact paired sign flips. GSE279972 used 54 morphology-labelled MS",
        "samples from 21 donors, lesion-class and B-APC adjustment, clustered",
        "intervals, and 300,000 three-seed donor-wild nulls.",
        "",
        "| module | active-inactive mean | exact p | foamy adjusted beta | wild p | BH q | max-T p | outcome |",
        "|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in outcomes:
        report.append(
            "| {module} | {gse180759_mean_active_minus_inactive:.3f} | "
            "{gse180759_exact_p:.3g} | {gse279972_foamy_adjusted_beta:.3f} | "
            "{gse279972_donor_wild_p:.3g} | {gse279972_bh_q:.3g} | "
            "{gse279972_max_t_p:.3g} | {outcome} |".format(**row)
        )
    report.extend(
        [
            "",
            "Even an orthogonally consistent row remains needs-data because only three",
            "GSE180759 donor pairs are eligible (minimum exact two-sided p=0.25), and",
            "foamy morphology is not the same estimand as a chronic-active lesion edge.",
            "No result is a progression-rate, causal, intervention, or therapeutic claim.",
        ]
    )
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
