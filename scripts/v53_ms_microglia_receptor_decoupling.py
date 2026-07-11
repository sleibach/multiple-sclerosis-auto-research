#!/usr/bin/env python3
"""Test CD44/CXCR4 decoupling from HLA-II and MIF ligand in MS microglia."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import statsmodels.api as sm

import v3_analyze_gse111972_microglia as source


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis/v53_ms_microglia_receptor_decoupling"
SEED = 53504
N_WILD_BOOTSTRAP = 100_000
MODULES = {
    "receptor_cd44_cxcr4": ["CD44", "CXCR4"],
    "hla_regulatory_ciita_rfx5": ["CIITA", "RFX5"],
    "mif_ddt_ligand": ["MIF", "DDT"],
    "ifn_unique": ["STAT1", "IRF1", "CXCL10", "GBP1"],
    "lysosomal_unique": ["CTSS", "CTSB", "CTSD", "LAMP1", "LAMP2", "LAMP3"],
}
CONTRASTS = {
    "receptor_minus_hla": ("receptor_cd44_cxcr4", "hla_regulatory_ciita_rfx5"),
    "receptor_minus_mif_ligand": ("receptor_cd44_cxcr4", "mif_ddt_ligand"),
}


def write_tsv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(rows[0]),
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def bh_adjust(p_values: list[float]) -> list[float]:
    order = np.argsort(p_values)
    adjusted = np.ones(len(p_values), dtype=float)
    running = 1.0
    for offset, index in enumerate(order[::-1], start=1):
        rank = len(p_values) - offset + 1
        running = min(running, p_values[int(index)] * len(p_values) / rank)
        adjusted[int(index)] = running
    return adjusted.tolist()


def wild_cluster_test(
    outcome: np.ndarray,
    full_design: np.ndarray,
    reduced_design: np.ndarray,
    cluster_index: np.ndarray,
    rng: np.random.Generator,
) -> tuple[float, float]:
    full_pinv = np.linalg.pinv(full_design)
    reduced_beta = np.linalg.pinv(reduced_design) @ outcome
    fitted_reduced = reduced_design @ reduced_beta
    residual = outcome - fitted_reduced
    observed_beta = float((full_pinv @ outcome)[1])
    exceed = 0
    completed = 0
    batch_size = 5_000
    n_clusters = int(cluster_index.max()) + 1
    while completed < N_WILD_BOOTSTRAP:
        n_batch = min(batch_size, N_WILD_BOOTSTRAP - completed)
        cluster_signs = rng.choice([-1.0, 1.0], size=(n_batch, n_clusters))
        sample_signs = cluster_signs[:, cluster_index]
        synthetic = fitted_reduced[None, :] + sample_signs * residual[None, :]
        synthetic_betas = synthetic @ full_pinv.T
        exceed += int(np.sum(np.abs(synthetic_betas[:, 1]) >= abs(observed_beta)))
        completed += n_batch
    return observed_beta, (1 + exceed) / (N_WILD_BOOTSTRAP + 1)


def main() -> int:
    meta = source.load_sample_metadata()
    expression = source.load_expression()
    meta = meta.loc[meta["sample"].isin(expression.columns)].reset_index(drop=True)
    samples = meta["sample"].tolist()

    genes = sorted({gene for module in MODULES.values() for gene in module})
    missing = sorted(set(genes) - set(expression.index))
    if missing:
        raise RuntimeError(f"Required genes missing from GSE111972 expression: {missing}")
    z = expression.loc[genes, samples]
    z = z.sub(z.mean(axis=1), axis=0).div(z.std(axis=1).replace(0, np.nan), axis=0)
    scores = pd.DataFrame(index=meta.index)
    for module, module_genes in MODULES.items():
        scores[module] = z.loc[module_genes, samples].mean(axis=0).to_numpy(dtype=float)
    for contrast, (left, right) in CONTRASTS.items():
        scores[contrast] = scores[left] - scores[right]

    patient_codes, patient_labels = pd.factorize(meta["patient"], sort=True)
    age = meta["age"].to_numpy(dtype=float)
    age = (age - np.mean(age)) / np.std(age)
    disease = meta["disease_ms"].to_numpy(dtype=float)
    region = meta["region_white_matter"].to_numpy(dtype=float)
    sex = meta["sex_male"].to_numpy(dtype=float)
    full_design = np.column_stack([np.ones(len(meta)), disease, region, age, sex])
    reduced_design = np.column_stack([np.ones(len(meta)), region, age, sex])
    rng = np.random.default_rng(SEED)

    rows = []
    p_values = []
    for outcome_name in [*MODULES, *CONTRASTS]:
        outcome = scores[outcome_name].to_numpy(dtype=float)
        model = sm.OLS(outcome, full_design).fit(
            cov_type="cluster", cov_kwds={"groups": patient_codes}
        )
        beta, wild_p = wild_cluster_test(
            outcome, full_design, reduced_design, patient_codes, rng
        )
        wm = meta["region"].eq("white_matter").to_numpy()
        gm = meta["region"].eq("grey_matter").to_numpy()
        rows.append(
            {
                "outcome": outcome_name,
                "outcome_type": "module" if outcome_name in MODULES else "module_difference",
                "n_samples": len(meta),
                "n_patients": len(patient_labels),
                "disease_beta_adjusted": beta,
                "cluster_robust_se": float(model.bse[1]),
                "cluster_robust_p": float(model.pvalues[1]),
                "wild_cluster_two_sided_p": wild_p,
                "white_matter_case_minus_control": float(
                    np.mean(outcome[wm & (disease == 1)]) - np.mean(outcome[wm & (disease == 0)])
                ),
                "grey_matter_case_minus_control": float(
                    np.mean(outcome[gm & (disease == 1)]) - np.mean(outcome[gm & (disease == 0)])
                ),
            }
        )
        p_values.append(wild_p)
    for row, q_value in zip(rows, bh_adjust(p_values), strict=True):
        row["wild_cluster_q_bh_seven_tests"] = q_value

    by_name = {row["outcome"]: row for row in rows}
    receptor = by_name["receptor_cd44_cxcr4"]
    receptor_hla = by_name["receptor_minus_hla"]
    receptor_ligand = by_name["receptor_minus_mif_ligand"]
    gate_components = {
        "receptor_positive_and_q_le_0_10": (
            receptor["disease_beta_adjusted"] > 0
            and receptor["wild_cluster_q_bh_seven_tests"] <= 0.10
        ),
        "receptor_minus_hla_positive_and_q_le_0_10": (
            receptor_hla["disease_beta_adjusted"] > 0
            and receptor_hla["wild_cluster_q_bh_seven_tests"] <= 0.10
        ),
        "receptor_minus_ligand_positive_and_q_le_0_10": (
            receptor_ligand["disease_beta_adjusted"] > 0
            and receptor_ligand["wild_cluster_q_bh_seven_tests"] <= 0.10
        ),
        "receptor_same_direction_both_regions": (
            receptor["white_matter_case_minus_control"] > 0
            and receptor["grey_matter_case_minus_control"] > 0
        ),
    }
    supported = all(gate_components.values())
    summary = {
        "purpose": "V53 patient-clustered test of MS microglial CD44/CXCR4 decoupling from HLA regulation and MIF ligand",
        "dataset": "GSE111972 sorted bulk microglia",
        "n_samples": len(meta),
        "n_patients": len(patient_labels),
        "n_wild_cluster_bootstrap_replicates_per_test": N_WILD_BOOTSTRAP,
        "seed": SEED,
        "gate_components": gate_components,
        "receptor_adjusted_beta": receptor["disease_beta_adjusted"],
        "receptor_wild_cluster_q": receptor["wild_cluster_q_bh_seven_tests"],
        "receptor_minus_hla_adjusted_beta": receptor_hla["disease_beta_adjusted"],
        "receptor_minus_hla_wild_cluster_q": receptor_hla[
            "wild_cluster_q_bh_seven_tests"
        ],
        "receptor_minus_ligand_adjusted_beta": receptor_ligand["disease_beta_adjusted"],
        "receptor_minus_ligand_wild_cluster_q": receptor_ligand[
            "wild_cluster_q_bh_seven_tests"
        ],
        "decoupling_gate_pass": supported,
        "verdict": (
            "MS_MICROGLIA_CD44_CXCR4_DECOUPLING_SUPPORTED_IN_GSE111972"
            if supported
            else "MS_MICROGLIA_CD44_CXCR4_DECOUPLING_NOT_ESTABLISHED"
        ),
        "boundary": "Single-cohort sorted-bulk state contrast; not causal, treatment-direction, target, or replication evidence.",
    }

    OUT.mkdir(parents=True, exist_ok=True)
    write_tsv(OUT / "clustered_module_tests.tsv", rows)
    pd.concat([meta[["sample", "patient", "disease", "region", "age", "sex_male"]], scores], axis=1).to_csv(
        OUT / "sample_module_scores.tsv", sep="\t", index=False
    )
    write_tsv(
        OUT / "module_definitions.tsv",
        [
            {"module": module, "genes": ";".join(genes_in_module)}
            for module, genes_in_module in MODULES.items()
        ],
    )
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    report = [
        "# V53 MS Microglia Receptor-State Decoupling",
        "",
        f"Verdict: **{summary['verdict']}**.",
        "",
        f"GSE111972 contains `{len(meta)}` sorted-microglia samples from `{len(patient_labels)}`",
        "patients. The primary model adjusts for region, standardized age, and sex, uses",
        "patient-clustered standard errors, and applies 100,000 patient-cluster wild-null",
        "replicates per outcome with BH correction across five modules/controls and two",
        "pre-specified module-difference tests.",
        "",
        f"CD44/CXCR4 adjusted disease beta is `{receptor['disease_beta_adjusted']:.3f}`",
        f"(wild-cluster q `{receptor['wild_cluster_q_bh_seven_tests']:.4f}`). Its difference",
        f"from CIITA/RFX5 is `{receptor_hla['disease_beta_adjusted']:.3f}`",
        f"(q `{receptor_hla['wild_cluster_q_bh_seven_tests']:.4f}`), and its difference",
        f"from MIF/DDT ligand is `{receptor_ligand['disease_beta_adjusted']:.3f}`",
        f"(q `{receptor_ligand['wild_cluster_q_bh_seven_tests']:.4f}`).",
        "",
        "The receptor-state association passes its component gate, but the full decoupling",
        "gate does not. This single-cohort sorted-bulk result does not establish cell-intrinsic",
        "causality, beneficial intervention",
        "direction, target selectivity, or replication in an independent MS cohort.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
