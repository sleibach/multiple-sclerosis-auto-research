#!/usr/bin/env python3
"""Run the frozen V54 second progression-lesion module family."""

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
OUT = ROOT / "analysis/v54_progression_lesion_module_panel"

MODULES = {
    "oxphos": [
        "NDUFA1", "NDUFA2", "NDUFA9", "NDUFB8", "SDHA", "SDHB", "UQCRC1",
        "UQCRC2", "COX4I1", "COX5A", "ATP5F1A", "ATP5F1B", "ATP5MC1",
    ],
    "resolution_efferocytosis_proxy": [
        "MERTK", "AXL", "TYRO3", "GAS6", "PROS1", "TREM2", "APOE", "LPL",
        "ABCA1", "ABCG1", "NR1H3", "NR1H2", "PPARD", "PPARG", "MRC1", "CD163",
        "IL10", "TGFB1", "VSIG4", "C1QA", "C1QB", "C1QC", "F13A1", "LYVE1",
        "ANXA1", "FPR2", "CD36", "MARCO",
    ],
    "nrf2_antioxidant_response": ["NFE2L2", "KEAP1", "HMOX1", "NQO1"],
    "stress_cytotoxicity": [
        "DDIT3", "HSPA1A", "HSPA1B", "ATF4", "XBP1", "BAX", "CASP3", "FOS",
        "JUN", "DNAJB1", "HSP90AA1",
    ],
    "mocci_inflammatory_switch": ["C15ORF48", "NDUFA4"],
}
TARGET_GENES = sorted({gene for genes in MODULES.values() for gene in genes})
TEST_MODULES = list(MODULES)
SEEDS = [54301, 54302, 54303]
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


def add_scores(
    frame: pd.DataFrame, dataset: str
) -> tuple[pd.DataFrame, list[dict[str, Any]]]:
    output = frame.copy()
    coverage: list[dict[str, Any]] = []
    for module, genes in MODULES.items():
        present = [gene for gene in genes if gene in output.columns]
        sd = output[present].std(axis=0, ddof=0) if present else pd.Series(dtype=float)
        variable = sd[sd > 0].index.tolist()
        required = (len(genes) + 1) // 2
        if len(variable) < required:
            raise RuntimeError(
                f"{dataset} {module} has {len(variable)}/{len(genes)} variable genes; requires {required}"
            )
        z = (output[variable] - output[variable].mean()) / sd[variable]
        if module == "mocci_inflammatory_switch":
            if set(variable) != {"C15ORF48", "NDUFA4"}:
                raise RuntimeError(f"{dataset} MOCCI switch requires both frozen genes")
            score = z.C15ORF48 - z.NDUFA4
        else:
            score = z.mean(axis=1)
        score_sd = score.std(ddof=0)
        if not np.isfinite(score_sd) or score_sd == 0:
            raise RuntimeError(f"{dataset} {module} has invalid score variance")
        output[module] = (score - score.mean()) / score_sd
        coverage.append(
            {
                "dataset": dataset,
                "module": module,
                "n_requested": len(genes),
                "n_present": len(present),
                "n_variable": len(variable),
                "coverage_fraction": len(variable) / len(genes),
                "variable_genes": ";".join(variable),
                "absent_or_constant_genes": ";".join(sorted(set(genes) - set(variable))),
            }
        )
    return output, coverage


def read_gse180759() -> tuple[pd.DataFrame, list[dict[str, Any]]]:
    annotation = pd.read_csv(RAW / "GSE180759_annotation.txt.gz", sep="\t")
    old = pd.read_csv(
        ROOT / "analysis/v54_progression_lesion_state/gse180759_immune_pseudobulk_scores.tsv",
        sep="\t",
    )
    selected: dict[str, np.ndarray] = {}
    matrix = RAW / "GSE180759_expression_matrix.csv.gz"
    with gzip.open(matrix, "rt") as handle:
        header = handle.readline().rstrip("\n").split(",")
        if header != annotation.nucleus_barcode.tolist():
            raise RuntimeError("GSE180759 expression/annotation barcode mismatch")
        for line in handle:
            gene, values_text = line.rstrip("\n").split(",", 1)
            canonical_gene = gene.upper()
            if canonical_gene not in TARGET_GENES:
                continue
            values = np.fromstring(values_text, sep=",", dtype=np.float64)
            if len(values) != len(annotation):
                raise RuntimeError(f"GSE180759 column mismatch for {gene}")
            if canonical_gene in selected:
                raise RuntimeError(f"Duplicate case-normalized GSE180759 gene {canonical_gene}")
            selected[canonical_gene] = values
    annotation = annotation.copy()
    for gene, values in selected.items():
        annotation[gene] = values
    aggregation: dict[str, str] = {gene: "sum" for gene in selected}
    sums = (
        annotation.groupby(["NBB_case", "pathology", "cell_type"], observed=True)
        .agg(aggregation)
        .reset_index()
    )
    base_columns = ["NBB_case", "pathology", "cell_type", "n_nuclei", "library_size"]
    eligible = old[base_columns].merge(
        sums, on=["NBB_case", "pathology", "cell_type"], validate="one_to_one"
    )
    for gene in selected:
        eligible[gene] = np.log2(eligible[gene] / eligible.library_size * 1_000_000 + 1)
    scored, coverage = add_scores(eligible, "GSE180759")
    scored.to_csv(OUT / "gse180759_panel_scores.tsv", sep="\t", index=False)
    return scored, coverage


def exact_paired_tests(scored: pd.DataFrame) -> pd.DataFrame:
    active = "chronic_active_MS_lesion_edge"
    inactive = "chronic_inactive_MS_lesion_edge"
    differences: dict[str, np.ndarray] = {}
    donors: list[str] | None = None
    for module in TEST_MODULES:
        paired = scored.loc[scored.pathology.eq(active), ["NBB_case", module]].merge(
            scored.loc[scored.pathology.eq(inactive), ["NBB_case", module]],
            on="NBB_case",
            suffixes=("_active", "_inactive"),
            validate="one_to_one",
        )
        if donors is None:
            donors = paired.NBB_case.astype(str).tolist()
        elif donors != paired.NBB_case.astype(str).tolist():
            raise RuntimeError("GSE180759 paired donors differ across panel modules")
        differences[module] = (
            paired[f"{module}_active"] - paired[f"{module}_inactive"]
        ).to_numpy(dtype=float)
    n_pairs = len(donors or [])
    if n_pairs != 3:
        raise RuntimeError(f"Expected three GSE180759 paired donors, observed {n_pairs}")
    signs = np.asarray(list(itertools.product([-1.0, 1.0], repeat=n_pairs)))
    null = np.column_stack(
        [np.mean(signs * differences[module][None, :], axis=1) for module in TEST_MODULES]
    )
    observed = np.asarray([differences[module].mean() for module in TEST_MODULES])
    absolute = np.abs(null)
    max_abs = absolute.max(axis=1)
    p = [float(np.mean(absolute[:, index] >= abs(value))) for index, value in enumerate(observed)]
    max_p = [float(np.mean(max_abs >= abs(value))) for value in observed]
    q = bh(p)
    rows = []
    for index, module in enumerate(TEST_MODULES):
        diff = differences[module]
        rows.append(
            {
                "module": module,
                "n_paired_donors": n_pairs,
                "donors": ";".join(donors or []),
                "mean_active_minus_inactive": float(diff.mean()),
                "median_active_minus_inactive": float(np.median(diff)),
                "n_positive": int(np.sum(diff > 0)),
                "n_negative": int(np.sum(diff < 0)),
                "exact_sign_flip_p": p[index],
                "bh_q": q[index],
                "max_module_fwer_p": max_p[index],
            }
        )
    return pd.DataFrame(rows)


def stream_gse279972(gsms: set[str]) -> pd.DataFrame:
    records: list[dict[str, float | str]] = []
    with tarfile.open(RAW / "GSE279972_RAW.tar") as archive:
        for member in archive.getmembers():
            if not member.isfile() or not member.name.endswith(".count.txt.gz"):
                continue
            gsm = member.name.split("_", 1)[0]
            if gsm not in gsms:
                continue
            source = archive.extractfile(member)
            if source is None:
                continue
            counts = {gene: 0.0 for gene in TARGET_GENES}
            with gzip.GzipFile(fileobj=source) as nested:
                for raw in nested:
                    fields = raw.decode().rstrip("\n").split("\t")
                    canonical_gene = fields[1].upper() if len(fields) == 3 else ""
                    if canonical_gene in counts:
                        counts[canonical_gene] += float(fields[2])
            records.append({"gsm": gsm, **counts})
    frame = pd.DataFrame(records)
    if set(frame.gsm.astype(str)) != gsms:
        raise RuntimeError("GSE279972 panel extraction did not cover every eligible GSM")
    return frame


def read_gse279972() -> tuple[pd.DataFrame, list[dict[str, Any]]]:
    base = pd.read_csv(
        ROOT / "analysis/v54_lysosomal_morphology_specificity/specificity_scores.tsv",
        sep="\t",
    )
    base = base.drop(columns=[gene for gene in TARGET_GENES if gene in base.columns])
    expression = stream_gse279972(set(base.gsm.astype(str)))
    frame = base.merge(expression, on="gsm", validate="one_to_one")
    for gene in TARGET_GENES:
        frame[gene] = np.log2(frame[gene] / frame.library_size * 1_000_000 + 1)
    scored, coverage = add_scores(frame, "GSE279972")
    scored.to_csv(OUT / "gse279972_panel_scores.tsv", sep="\t", index=False)
    return scored, coverage


def morphology_tests(scored: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    lesion = pd.get_dummies(
        scored.Lesion_type_6.astype(str), prefix="lesion", drop_first=True, dtype=float
    )
    reduced = pd.DataFrame(
        {
            "intercept": np.ones(len(scored)),
            "b_apc_composition": scored.b_apc_composition.to_numpy(dtype=float),
            "resident_microglia_identity": scored.resident_microglia_identity.to_numpy(dtype=float),
            "mims_deoverlapped": scored.mims_deoverlapped.to_numpy(dtype=float),
        }
    )
    reduced = pd.concat([reduced, lesion.reset_index(drop=True)], axis=1)
    full = reduced.copy()
    full.insert(1, "foamy", scored.foamy.to_numpy(dtype=float))
    x = full.to_numpy(dtype=float)
    x0 = reduced.to_numpy(dtype=float)
    if np.linalg.matrix_rank(x) != x.shape[1] or np.linalg.matrix_rank(x0) != x0.shape[1]:
        raise RuntimeError("Rank-deficient GSE279972 panel design")
    y = scored[TEST_MODULES].to_numpy(dtype=float)
    pinv = np.linalg.solve(x.T @ x, x.T)
    pinv0 = np.linalg.solve(x0.T @ x0, x0.T)
    observed = pinv[1] @ y
    fitted0 = x0 @ (pinv0 @ y)
    residual0 = y - fitted0
    donor_codes, donors = pd.factorize(scored.donor.astype(str), sort=True)

    rows: list[dict[str, Any]] = []
    for index, module in enumerate(TEST_MODULES):
        model = sm.OLS(y[:, index], x).fit(
            cov_type="cluster",
            cov_kwds={"groups": scored.donor.astype(str), "use_correction": True},
        )
        ci = model.conf_int()[1]
        if not np.isclose(model.params[1], observed[index], atol=1e-10):
            raise RuntimeError(f"GSE279972 coefficient mismatch for {module}")
        rows.append(
            {
                "module": module,
                "foamy_adjusted_beta": float(observed[index]),
                "cluster_ci_low": float(ci[0]),
                "cluster_ci_high": float(ci[1]),
                "cluster_p": float(model.pvalues[1]),
                "design_condition": float(np.linalg.cond(x)),
            }
        )

    aggregate_exceed = np.zeros(len(TEST_MODULES), dtype=np.int64)
    aggregate_max = np.zeros(len(TEST_MODULES), dtype=np.int64)
    seed_rows: list[dict[str, Any]] = []
    for seed in SEEDS:
        rng = np.random.default_rng(seed)
        seed_exceed = np.zeros(len(TEST_MODULES), dtype=np.int64)
        seed_max = np.zeros(len(TEST_MODULES), dtype=np.int64)
        completed = 0
        while completed < N_PER_SEED:
            batch = min(BATCH, N_PER_SEED - completed)
            donor_signs = rng.choice([-1.0, 1.0], size=(batch, len(donors)))
            signs = donor_signs[:, donor_codes]
            synthetic = fitted0[None, :, :] + signs[:, :, None] * residual0[None, :, :]
            null_beta = np.einsum("i,bim->bm", pinv[1], synthetic)
            if not np.isfinite(null_beta).all():
                raise RuntimeError("Non-finite GSE279972 panel null")
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
                    "donor_wild_p": (1 + int(seed_exceed[index])) / (N_PER_SEED + 1),
                    "max_module_fwer_p": (1 + int(seed_max[index])) / (N_PER_SEED + 1),
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
            for module in TEST_MODULES:
                leave_rows.append(
                    {"left_out_donor": donor, "module": module, "status": "rank_deficient"}
                )
            continue
        beta = np.linalg.solve(x_leave.T @ x_leave, x_leave.T)[1] @ y[keep]
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
    for index, item in enumerate(rows):
        estimates = leave[
            leave.module.eq(item["module"]) & leave.status.eq("estimated")
        ].foamy_adjusted_beta
        item["donor_wild_p"] = p[index]
        item["bh_q"] = q[index]
        item["max_module_fwer_p"] = max_p[index]
        item["leave_one_donor_min_beta"] = float(estimates.min())
        item["leave_one_donor_max_beta"] = float(estimates.max())
        item["leave_one_donor_direction_retained"] = bool(
            np.all(np.sign(estimates) == np.sign(item["foamy_adjusted_beta"]))
        )
    return pd.DataFrame(rows), pd.DataFrame(seed_rows), leave


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    gse180, coverage180 = read_gse180759()
    paired = exact_paired_tests(gse180)
    paired.to_csv(OUT / "gse180759_active_inactive_tests.tsv", sep="\t", index=False)

    gse279, coverage279 = read_gse279972()
    morphology, seeds, leave = morphology_tests(gse279)
    morphology.to_csv(OUT / "gse279972_morphology_tests.tsv", sep="\t", index=False)
    seeds.to_csv(OUT / "gse279972_seed_stability.tsv", sep="\t", index=False)
    leave.to_csv(OUT / "gse279972_leave_one_donor.tsv", sep="\t", index=False)
    pd.DataFrame(coverage180 + coverage279).to_csv(
        OUT / "module_gene_coverage.tsv", sep="\t", index=False
    )

    joined = paired.merge(morphology, on="module", validate="one_to_one")
    outcomes: list[dict[str, Any]] = []
    for _, item in joined.iterrows():
        paired_direction = (
            1
            if item.n_positive == item.n_paired_donors
            else -1
            if item.n_negative == item.n_paired_donors
            else 0
        )
        morphology_direction = int(np.sign(item.foamy_adjusted_beta))
        same_direction = paired_direction != 0 and paired_direction == morphology_direction
        morphology_pass = bool(
            (item.cluster_ci_low > 0 or item.cluster_ci_high < 0)
            and item.donor_wild_p <= 0.05
            and item.bh_q_y <= 0.10
            and item.max_module_fwer_p_y <= 0.10
            and item.leave_one_donor_direction_retained
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
                "module": item.module,
                "gse180759_mean_active_minus_inactive": item.mean_active_minus_inactive,
                "gse180759_n_positive": int(item.n_positive),
                "gse180759_n_negative": int(item.n_negative),
                "gse180759_exact_p": item.exact_sign_flip_p,
                "gse279972_foamy_adjusted_beta": item.foamy_adjusted_beta,
                "gse279972_cluster_ci_low": item.cluster_ci_low,
                "gse279972_cluster_ci_high": item.cluster_ci_high,
                "gse279972_donor_wild_p": item.donor_wild_p,
                "gse279972_bh_q": item.bh_q_y,
                "gse279972_max_module_p": item.max_module_fwer_p_y,
                "cross_context_same_direction": same_direction,
                "outcome": outcome,
            }
        )
    outcomes_frame = pd.DataFrame(outcomes)
    outcomes_frame.to_csv(OUT / "cross_context_outcomes.tsv", sep="\t", index=False)
    supported = outcomes_frame.loc[
        outcomes_frame.outcome.eq("orthogonally_consistent_needs_data"), "module"
    ].tolist()
    summary = {
        "purpose": "Frozen second progression-lesion module family; pathology context only",
        "n_modules": len(TEST_MODULES),
        "n_gse180759_paired_donors": int(paired.n_paired_donors.iloc[0]),
        "n_gse279972_samples": len(gse279),
        "n_gse279972_donors": int(gse279.donor.nunique()),
        "n_gse279972_wild_replicates": len(SEEDS) * N_PER_SEED,
        "orthogonally_consistent_modules": supported,
        "verdict": (
            "ORTHOGONAL_PATHOLOGY_CONTEXT_REQUIRES_REPLICATION"
            if supported
            else "NO_ORTHOGONALLY_SUPPORTED_SECOND_PANEL_MODULE"
        ),
        "untested_dimensions": {
            "iron_handling": "no frozen project-local module",
            "cellular_senescence": "no frozen project-local module",
            "direct_remyelination": "no held functional remyelination endpoint",
        },
        "boundary": "No disability, causal, target, or therapeutic-direction inference is permitted.",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    report = [
        "# V54 Progression Lesion Module Panel",
        "",
        f"Verdict: **{summary['verdict']}**.",
        "",
        "Five project-pre-existing modules were tested in three paired chronic-active/",
        "chronic-inactive donors and in 54 foamy/nonfoamy samples from 21 donors.",
        "The morphology model adjusted lesion class, B/APC composition, resident",
        "microglia identity, and de-overlapped MIMS state and used 300,000 donor-wild",
        "nulls plus leave-one-donor checks.",
        "",
        "| module | active-inactive mean | pairs +/- | foamy adjusted beta | wild p | max-module p | outcome |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for item in outcomes:
        report.append(
            "| {module} | {gse180759_mean_active_minus_inactive:.3f} | "
            "{gse180759_n_positive}/{gse180759_n_negative} | "
            "{gse279972_foamy_adjusted_beta:.3f} | {gse279972_donor_wild_p:.4g} | "
            "{gse279972_max_module_p:.4g} | {outcome} |".format(**item)
        )
    report.extend(
        [
            "",
            "Iron handling and cellular senescence remain untested because the project",
            "does not have a frozen local module for either. The resolution/efferocytosis",
            "score is a transcript proxy, not measured myelin uptake or remyelination.",
            "No result here can establish disability progression, causality, or an",
            "intervention direction.",
        ]
    )
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
