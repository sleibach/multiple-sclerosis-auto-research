#!/usr/bin/env python3
"""Test gene coherence and broad-state specificity of MS CD44/CXCR4 signal."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

import v3_analyze_gse111972_microglia as source


ROOT = Path(__file__).resolve().parents[1]
SAMPLE_SCORES = ROOT / "analysis/v53_ms_microglia_receptor_decoupling/sample_module_scores.tsv"
OUT = ROOT / "analysis/v53_ms_microglia_component_specificity"
SEED = 53508
N_WILD_BOOTSTRAP = 100_000
CONTROLS = [
    "hla_regulatory_ciita_rfx5",
    "mif_ddt_ligand",
    "ifn_unique",
    "lysosomal_unique",
]


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


def standardized(values: np.ndarray) -> np.ndarray:
    sd = float(np.std(values))
    return (values - np.mean(values)) / sd if sd else np.zeros(len(values))


def design(frame: pd.DataFrame, include_controls: bool) -> np.ndarray:
    age_z = standardized(frame["age"].to_numpy(dtype=float))
    columns = [
        np.ones(len(frame)),
        frame["disease_binary"].to_numpy(dtype=float),
        age_z,
        age_z**2,
        frame["sex_male"].to_numpy(dtype=float),
    ]
    if include_controls:
        columns.extend(
            standardized(frame[control].to_numpy(dtype=float)) for control in CONTROLS
        )
    return np.column_stack(columns)


def wild_test(
    frame: pd.DataFrame,
    outcome_name: str,
    include_controls: bool,
    rng: np.random.Generator,
) -> tuple[float, float, float]:
    outcome = frame[outcome_name].to_numpy(dtype=float)
    full = design(frame, include_controls)
    reduced = np.delete(full, 1, axis=1)
    full_pinv = np.linalg.pinv(full)
    observed = float((full_pinv @ outcome)[1])
    fitted = reduced @ (np.linalg.pinv(reduced) @ outcome)
    residual = outcome - fitted
    exceed = 0
    completed = 0
    while completed < N_WILD_BOOTSTRAP:
        batch = min(5_000, N_WILD_BOOTSTRAP - completed)
        signs = rng.choice([-1.0, 1.0], size=(batch, len(frame)))
        synthetic = fitted[None, :] + signs * residual[None, :]
        betas = synthetic @ full_pinv.T
        exceed += int(np.sum(np.abs(betas[:, 1]) >= abs(observed)))
        completed += batch
    return observed, (1 + exceed) / (N_WILD_BOOTSTRAP + 1), float(np.linalg.cond(full))


def coefficient(frame: pd.DataFrame, include_controls: bool) -> float:
    full = design(frame, include_controls)
    return float((np.linalg.pinv(full) @ frame["receptor_cd44_cxcr4"].to_numpy(dtype=float))[1])


def main() -> int:
    sample = pd.read_csv(SAMPLE_SCORES, sep="\t")
    expression = source.load_expression()
    samples = sample["sample"].tolist()
    if not {"CD44", "CXCR4"}.issubset(expression.index):
        raise RuntimeError("CD44/CXCR4 missing from GSE111972 expression")
    genes = expression.loc[["CD44", "CXCR4"], samples]
    genes = genes.sub(genes.mean(axis=1), axis=0).div(genes.std(axis=1), axis=0)
    sample["CD44_gene_z"] = genes.loc["CD44", samples].to_numpy(dtype=float)
    sample["CXCR4_gene_z"] = genes.loc["CXCR4", samples].to_numpy(dtype=float)
    sample["disease_binary"] = sample["disease"].eq("MS").astype(int)

    aggregate_columns = [
        "disease_binary",
        "age",
        "sex_male",
        "receptor_cd44_cxcr4",
        "CD44_gene_z",
        "CXCR4_gene_z",
        *CONTROLS,
    ]
    aggregations = {column: "mean" for column in aggregate_columns}
    for column in ["disease_binary", "age", "sex_male"]:
        aggregations[column] = "first"
    patient = sample.groupby("patient", as_index=False).agg(aggregations)

    rng = np.random.default_rng(SEED)
    gene_rows = []
    gene_p = []
    for gene in ["CD44_gene_z", "CXCR4_gene_z"]:
        beta, p_value, condition = wild_test(patient, gene, False, rng)
        gene_rows.append(
            {
                "outcome": gene,
                "disease_beta": beta,
                "wild_two_sided_p": p_value,
                "design_condition_number": condition,
            }
        )
        gene_p.append(p_value)
    for row, q_value in zip(gene_rows, bh_adjust(gene_p), strict=True):
        row["q_bh_two_genes"] = q_value

    base_beta, base_p, base_condition = wild_test(
        patient, "receptor_cd44_cxcr4", False, rng
    )
    joint_beta, joint_p, joint_condition = wild_test(
        patient, "receptor_cd44_cxcr4", True, rng
    )
    loo_rows = []
    for omitted in patient["patient"]:
        retained = patient[~patient["patient"].eq(omitted)].copy()
        loo_rows.append(
            {
                "omitted_patient": omitted,
                "joint_adjusted_disease_beta": coefficient(retained, include_controls=True),
            }
        )
    min_loo = min(float(row["joint_adjusted_disease_beta"]) for row in loo_rows)
    attenuation_fraction = 1.0 - joint_beta / base_beta if base_beta else float("nan")
    gate_components = {
        "both_genes_positive_q_le_0_10": all(
            row["disease_beta"] > 0 and row["q_bh_two_genes"] <= 0.10
            for row in gene_rows
        ),
        "joint_adjusted_receptor_beta_positive_p_le_0_10": joint_beta > 0 and joint_p <= 0.10,
        "joint_design_condition_number_le_30": joint_condition <= 30,
        "all_joint_adjusted_lopo_betas_positive": min_loo > 0,
    }
    specific = all(gate_components.values())
    summary = {
        "purpose": "V53 gene-coherence and broad-state specificity sensitivity for GSE111972 CD44/CXCR4",
        "n_patients": len(patient),
        "n_wild_bootstrap_replicates_per_test": N_WILD_BOOTSTRAP,
        "seed": SEED,
        "base_receptor_beta": base_beta,
        "base_receptor_wild_p": base_p,
        "joint_adjusted_receptor_beta": joint_beta,
        "joint_adjusted_receptor_wild_p": joint_p,
        "joint_adjustment_attenuation_fraction": attenuation_fraction,
        "joint_design_condition_number": joint_condition,
        "minimum_lopo_joint_adjusted_beta": min_loo,
        "gate_components": gate_components,
        "component_specificity_gate_pass": specific,
        "verdict": (
            "CD44_CXCR4_ASSOCIATION_GENE_COHERENT_AND_BROAD_STATE_ADJUSTED"
            if specific
            else "CD44_CXCR4_ASSOCIATION_NOT_COMPONENT_SPECIFIC_AFTER_STRICT_GATE"
        ),
        "boundary": "Single-cohort expression specificity only; not causal, therapeutic-direction, or target evidence.",
    }

    OUT.mkdir(parents=True, exist_ok=True)
    write_tsv(OUT / "gene_tests.tsv", gene_rows)
    write_tsv(
        OUT / "module_specificity_tests.tsv",
        [
            {
                "model": "base_age_quadratic_sex",
                "disease_beta": base_beta,
                "wild_two_sided_p": base_p,
                "condition_number": base_condition,
            },
            {
                "model": "joint_plus_hla_mif_ifn_lysosomal_controls",
                "disease_beta": joint_beta,
                "wild_two_sided_p": joint_p,
                "condition_number": joint_condition,
            },
        ],
    )
    write_tsv(OUT / "leave_one_patient_out_joint.tsv", loo_rows)
    patient.to_csv(OUT / "patient_component_scores.tsv", sep="\t", index=False)
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    report = [
        "# V53 MS Microglia Component Specificity",
        "",
        f"Verdict: **{summary['verdict']}**.",
        "",
        "CD44 and CXCR4 were tested separately in patient-equal quadratic-age models with",
        "100,000 wild-null replicates and BH correction across the two genes. The receptor",
        "module was then jointly adjusted for CIITA/RFX5, MIF/DDT, unique IFN/APC, and unique",
        "lysosomal scores.",
        "",
        f"Base receptor beta is `{base_beta:.3f}` (p `{base_p:.4f}`); joint-adjusted beta is",
        f"`{joint_beta:.3f}` (p `{joint_p:.4f}`), attenuation `{attenuation_fraction:.1%}`,",
        f"condition number `{joint_condition:.2f}`, and minimum leave-one-patient-out joint",
        f"beta `{min_loo:.3f}`.",
        "",
        "Passing this gate would support component coherence and separation from measured broad",
        "state scores in one cohort only. It would not establish causality, intervention",
        "direction, target selectivity, or independent replication.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
