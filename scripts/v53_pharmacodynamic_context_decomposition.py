#!/usr/bin/env python3
"""Decompose the V53 pharmacodynamic edge by context and response semantics."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy import stats


ROOT = Path(__file__).resolve().parents[1]
INPUT = (
    ROOT
    / "analysis/v53_pharmacodynamic_deoverlap_sensitivity/globally_unique_gene_pharmacodynamic_matrix.tsv"
)
OUT = ROOT / "analysis/v53_pharmacodynamic_context_decomposition"
LEFT = "hla_ii_apc"
RIGHT = "mif_cd74_receptor_state"
SEED = 53505
N_PERMUTATIONS = 50_000


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


def safe_spearman(left: np.ndarray, right: np.ndarray) -> float:
    if len(left) < 3 or np.std(left) == 0 or np.std(right) == 0:
        return float("nan")
    return float(stats.spearmanr(left, right).statistic)


def stratified_permutation_p(
    left: np.ndarray,
    right: np.ndarray,
    strata: np.ndarray,
    rng: np.random.Generator,
) -> tuple[float, float]:
    observed = safe_spearman(left, right)
    null = np.empty(N_PERMUTATIONS, dtype=float)
    for iteration in range(N_PERMUTATIONS):
        permuted = right.copy()
        for stratum in np.unique(strata):
            group = np.flatnonzero(strata == stratum)
            permuted[group] = right[group[rng.permutation(len(group))]]
        null[iteration] = abs(safe_spearman(left, permuted))
    return observed, (1 + int(np.sum(null >= abs(observed)))) / (N_PERMUTATIONS + 1)


def context_parts(label: str) -> tuple[str, str, dict[str, str]]:
    dataset, therapy, scope = label.split("|", 2)
    fields = {}
    for item in scope.split(";"):
        if "=" in item:
            key, value = item.split("=", 1)
            fields[key] = value
    return dataset, therapy, fields


def response_contrasts(matrix: pd.DataFrame) -> pd.DataFrame:
    rows = []
    parsed = {label: context_parts(label) for label in matrix.index}

    def add_pair(name: str, favorable_label: str, unfavorable_label: str) -> None:
        rows.append(
            {
                "contrast": name,
                "favorable_context": favorable_label,
                "unfavorable_context": unfavorable_label,
                LEFT: float(matrix.loc[favorable_label, LEFT] - matrix.loc[unfavorable_label, LEFT]),
                RIGHT: float(matrix.loc[favorable_label, RIGHT] - matrix.loc[unfavorable_label, RIGHT]),
            }
        )

    for therapy in ["etanercept", "ustekinumab"]:
        labels = [
            label
            for label, (dataset, _, fields) in parsed.items()
            if dataset == "GSE106992" and fields.get("therapy") == therapy
        ]
        by_response = {parsed[label][2]["response"]: label for label in labels}
        add_pair(f"GSE106992:{therapy}:R_minus_NR", by_response["R"], by_response["NR"])

    for dataset in ["GSE235357", "GSE250453"]:
        labels = [label for label, parts in parsed.items() if parts[0] == dataset]
        by_response = {parsed[label][2]["response"]: label for label in labels}
        add_pair(f"{dataset}:R_minus_NR", by_response["R"], by_response["NR"])

    uc_labels = [label for label, parts in parsed.items() if parts[0] == "GSE253006"]
    compartments = sorted({parsed[label][2]["marker_compartment"] for label in uc_labels})
    for compartment in compartments:
        labels = [
            label
            for label in uc_labels
            if parsed[label][2]["marker_compartment"] == compartment
        ]
        by_group = {parsed[label][2]["group"]: label for label in labels}
        add_pair(
            f"GSE253006:{compartment}:Responder_minus_No_responder",
            by_group["Responder"],
            by_group["No responder"],
        )

    rituximab = [label for label, parts in parsed.items() if parts[0] == "GSE24742"]
    by_response = {parsed[label][2]["response"]: label for label in rituximab}
    add_pair("GSE24742:good_minus_poor", by_response["good"], by_response["poor"])
    return pd.DataFrame(rows)


def main() -> int:
    matrix = pd.read_csv(INPUT, sep="\t", index_col=0)
    if matrix[[LEFT, RIGHT]].isna().any().any() or len(matrix) != 24:
        raise RuntimeError("Expected complete 24-context disjoint pharmacodynamic matrix")
    datasets = np.asarray([label.split("|", 1)[0] for label in matrix.index], dtype=str)
    rng = np.random.default_rng(SEED)

    partition_masks = {
        "all_contexts": np.ones(len(matrix), dtype=bool),
        "bulk_response_strata": np.isin(
            datasets, ["GSE106992", "GSE235357", "GSE24742", "GSE250453"]
        ),
        "marker_compartment_contexts": np.isin(datasets, ["GSE183047", "GSE253006"]),
        "gse253006_only": datasets == "GSE253006",
        "exclude_gse253006": datasets != "GSE253006",
    }
    partition_rows = []
    p_values = []
    for partition, mask in partition_masks.items():
        rho, p_value = stratified_permutation_p(
            matrix.loc[mask, LEFT].to_numpy(dtype=float),
            matrix.loc[mask, RIGHT].to_numpy(dtype=float),
            datasets[mask],
            rng,
        )
        partition_rows.append(
            {
                "partition": partition,
                "n_contexts": int(np.sum(mask)),
                "n_datasets": int(len(np.unique(datasets[mask]))),
                "spearman": rho,
                "dataset_stratified_permutation_p": p_value,
            }
        )
        p_values.append(p_value)
    for row, q_value in zip(partition_rows, bh_adjust(p_values), strict=True):
        row["q_bh_five_partitions"] = q_value

    contrasts = response_contrasts(matrix)
    contrast_rho = safe_spearman(
        contrasts[LEFT].to_numpy(dtype=float), contrasts[RIGHT].to_numpy(dtype=float)
    )
    contrast_null = np.empty(N_PERMUTATIONS, dtype=float)
    right = contrasts[RIGHT].to_numpy(dtype=float)
    left = contrasts[LEFT].to_numpy(dtype=float)
    for iteration in range(N_PERMUTATIONS):
        contrast_null[iteration] = abs(safe_spearman(left, rng.permutation(right)))
    contrast_p = (1 + int(np.sum(contrast_null >= abs(contrast_rho)))) / (
        N_PERMUTATIONS + 1
    )
    same_direction = int(np.sum(np.sign(left) == np.sign(right)))
    concordance_p = float(
        stats.binomtest(same_direction, len(contrasts), 0.5, alternative="greater").pvalue
    )
    contrast_q, concordance_q = bh_adjust([contrast_p, concordance_p])

    by_partition = {row["partition"]: row for row in partition_rows}
    bulk = by_partition["bulk_response_strata"]
    compartment = by_partition["marker_compartment_contexts"]
    gate_components = {
        "bulk_partition_rho_ge_0_30_and_q_le_0_10": (
            bulk["spearman"] >= 0.30 and bulk["q_bh_five_partitions"] <= 0.10
        ),
        "compartment_partition_rho_ge_0_30_and_q_le_0_10": (
            compartment["spearman"] >= 0.30
            and compartment["q_bh_five_partitions"] <= 0.10
        ),
        "response_contrast_rho_ge_0_30_and_q_le_0_10": (
            contrast_rho >= 0.30 and contrast_q <= 0.10
        ),
        "response_concordance_q_le_0_10": concordance_q <= 0.10,
    }
    response_structured = all(gate_components.values())
    summary = {
        "purpose": "V53 context-semantic decomposition of the disjoint pharmacodynamic HLA-II/receptor edge",
        "n_contexts": len(matrix),
        "n_response_contrasts": len(contrasts),
        "n_permutations_per_test": N_PERMUTATIONS,
        "seed": SEED,
        "response_contrast_spearman": contrast_rho,
        "response_contrast_permutation_p": contrast_p,
        "response_contrast_q_bh_two_tests": contrast_q,
        "same_direction_response_contrasts": same_direction,
        "response_concordance_exact_p": concordance_p,
        "response_concordance_q_bh_two_tests": concordance_q,
        "gate_components": gate_components,
        "response_structured_gate_pass": response_structured,
        "verdict": (
            "PHARMACODYNAMIC_EDGE_REPLICATES_ACROSS_CONTEXT_TYPES_AND_RESPONSE_CONTRASTS"
            if response_structured
            else "PHARMACODYNAMIC_EDGE_NOT_RESPONSE_STRUCTURED_ACROSS_CONTEXT_TYPES"
        ),
        "boundary": "Context decomposition of an existing edge; no causal, predictive, or therapeutic claim.",
    }

    OUT.mkdir(parents=True, exist_ok=True)
    write_tsv(OUT / "partition_tests.tsv", partition_rows)
    contrasts.to_csv(OUT / "response_contrasts.tsv", sep="\t", index=False)
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    report = [
        "# V53 Pharmacodynamic Context Decomposition",
        "",
        f"Verdict: **{summary['verdict']}**.",
        "",
        f"The 24 disjoint contexts were split into `{bulk['n_contexts']}` bulk response",
        f"strata and `{compartment['n_contexts']}` marker-compartment contexts. Their",
        f"Spearman values are `{bulk['spearman']:.3f}` and `{compartment['spearman']:.3f}`",
        f"with five-partition BH q-values `{bulk['q_bh_five_partitions']:.4f}` and",
        f"`{compartment['q_bh_five_partitions']:.4f}`.",
        "",
        f"Across `{len(contrasts)}` favorable-minus-unfavorable response contrasts,",
        f"HLA-II and receptor-state changes correlate at rho `{contrast_rho:.3f}`",
        f"(permutation q `{contrast_q:.4f}`); `{same_direction}/{len(contrasts)}` have",
        f"the same sign (exact-binomial q `{concordance_q:.4f}`).",
        "",
        "This analysis tests whether an existing pharmacodynamic relationship carries",
        "consistent response semantics. It does not estimate treatment benefit, causal",
        "direction, a clinical rule, or a therapeutic target.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
