#!/usr/bin/env python3
"""Rescore independent cross-disease atlases with disjoint APC modules."""

from __future__ import annotations

import contextlib
import csv
import io
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy import stats

import v3_analyze_direct_h5ad_cell_states as module_source
import v3_analyze_gse111972_microglia as micro_source
import v3_analyze_gse248205_thyroid_spatial as thyroid_source
import v3_analyze_gse315138_celiac_marker_compartments as celiac_source


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis/v53_additional_atlas_disjoint_rescoring"
MODULES = ("hla_ii_apc", "ifn_apc", "lysosomal_apc", "mif_cd74_receptor_state")
RIGHT = "mif_cd74_receptor_state"
DIRECT_MATRIX = (
    ROOT
    / "analysis/v53_cell_state_deoverlap_sensitivity/globally_unique_gene_cell_state_matrix.tsv"
)
DIRECT_RUN_LOG = ROOT / "analysis/v53_cell_state_deoverlap_sensitivity/run_log.tsv"


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


def globally_unique_modules(original: dict[str, list[str]]) -> dict[str, list[str]]:
    counts: dict[str, int] = {}
    for module in MODULES:
        for gene in set(original[module]):
            counts[gene] = counts.get(gene, 0) + 1
    return {
        module: [gene for gene in original[module] if counts[gene] == 1]
        for module in MODULES
    }


def run_micro(modules: dict[str, list[str]], label: str) -> pd.DataFrame:
    micro_source.MODULES = modules
    micro_source.TARGET_GENES = sorted({gene for genes in modules.values() for gene in genes})
    micro_source.OUT = OUT / "source_runs" / f"gse111972_{label}"
    micro_source.OUT.mkdir(parents=True, exist_ok=True)
    with contextlib.redirect_stdout(io.StringIO()):
        micro_source.main()
    return pd.read_csv(micro_source.OUT / "gse111972_module_contrasts.tsv", sep="\t")


def run_thyroid(modules: dict[str, list[str]], label: str) -> pd.DataFrame:
    thyroid_source.MODULES = modules
    thyroid_source.TARGET_GENES = sorted({gene for genes in modules.values() for gene in genes})
    thyroid_source.OUT = OUT / "source_runs" / f"gse248205_{label}"
    thyroid_source.OUT.mkdir(parents=True, exist_ok=True)
    with contextlib.redirect_stdout(io.StringIO()):
        thyroid_source.main()
    return pd.read_csv(
        thyroid_source.OUT / "gse248205_module_gene_contrasts.tsv", sep="\t"
    )


def run_celiac(modules: dict[str, list[str]], label: str) -> pd.DataFrame:
    celiac_source.MODULES = modules
    celiac_source.TARGET_GENES = sorted({gene for genes in modules.values() for gene in genes})
    celiac_source.ALL_GENES = sorted(
        set(celiac_source.TARGET_GENES) | set(celiac_source.MARKER_GENES)
    )
    celiac_source.OUT = OUT / "source_runs" / f"gse315138_{label}"
    celiac_source.OUT.mkdir(parents=True, exist_ok=True)
    with contextlib.redirect_stdout(io.StringIO()):
        celiac_source.main()
    return pd.read_csv(
        celiac_source.OUT / "gse315138_donor_module_comparisons.tsv", sep="\t"
    )


def max_matched_error(
    reference: pd.DataFrame,
    rebuilt: pd.DataFrame,
    keys: list[str],
    values: list[str],
) -> tuple[float, int]:
    merged = reference[keys + values].merge(
        rebuilt[keys + values], on=keys, suffixes=("_reference", "_rebuilt")
    )
    if len(merged) != len(reference):
        raise RuntimeError(
            f"Exact rebuild coverage failure for {keys}: {len(merged)} != {len(reference)}"
        )
    errors = []
    for value in values:
        errors.extend(
            abs(
                merged[f"{value}_reference"].to_numpy(dtype=float)
                - merged[f"{value}_rebuilt"].to_numpy(dtype=float)
            )
        )
    return float(np.nanmax(errors)), len(merged)


def extract_extra_effects(
    micro: pd.DataFrame,
    thyroid: pd.DataFrame,
    celiac: pd.DataFrame,
    definition: str,
) -> pd.DataFrame:
    rows = []
    for _, row in micro[
        micro["contrast"].eq("MS_WM_vs_CON_WM") & micro["feature"].isin(MODULES)
    ].iterrows():
        rows.append(
            {
                "definition": definition,
                "physical_dataset": "GSE111972",
                "context": "MS white-matter microglia",
                "module": row["feature"],
                "effect": float(row["delta_log2"]),
                "p": float(row["p"]),
                "n_genes_present": int(row["n_genes_present"]),
                "genes_present": row["genes_present"],
            }
        )
    for _, row in thyroid[
        thyroid["feature_type"].eq("module") & thyroid["feature"].isin(MODULES)
    ].iterrows():
        rows.append(
            {
                "definition": definition,
                "physical_dataset": "GSE248205",
                "context": str(row["contrast"]),
                "module": row["feature"],
                "effect": float(row["delta_case_minus_control"]),
                "p": float(row["p"]),
                "n_genes_present": "sample_specific",
                "genes_present": "see source-run sample score table",
            }
        )
    for _, row in celiac[
        celiac["metric"].eq("mean_score") & celiac["module"].isin(MODULES)
    ].iterrows():
        rows.append(
            {
                "definition": definition,
                "physical_dataset": "GSE315138",
                "context": f"celiac {row['compartment']}",
                "module": row["module"],
                "effect": float(row["delta_case_minus_control"]),
                "p": float(row["p"]),
                "n_genes_present": "compartment_specific",
                "genes_present": "see source-run module coverage table",
            }
        )
    return pd.DataFrame(rows)


def direct_dataset_effects() -> pd.DataFrame:
    matrix = pd.read_csv(DIRECT_MATRIX, sep="\t", index_col=0)
    log = pd.read_csv(DIRECT_RUN_LOG, sep="\t")
    mapping = dict(zip(log["analysis"], log["dataset_path"], strict=True))
    matrix["analysis"] = [label.split("|", 1)[0] for label in matrix.index]
    matrix["physical_dataset"] = matrix["analysis"].map(mapping)
    if matrix["physical_dataset"].isna().any():
        raise RuntimeError("Direct-h5ad physical-dataset mapping is incomplete")
    return matrix.groupby("physical_dataset", as_index=False)[list(MODULES)].mean()


def main() -> int:
    np.random.seed(53503)
    original = {module: list(module_source.MODULES[module]) for module in MODULES}
    unique = globally_unique_modules(original)

    micro_original = run_micro(original, "original")
    thyroid_original = run_thyroid(original, "original")
    celiac_original = run_celiac(original, "original")
    micro_unique = run_micro(unique, "unique")
    thyroid_unique = run_thyroid(unique, "unique")
    celiac_unique = run_celiac(unique, "unique")

    committed_micro = pd.read_csv(
        ROOT / "phases/v3/results/gse111972_module_contrasts.tsv", sep="\t"
    )
    micro_ref = committed_micro[committed_micro["feature"].eq(RIGHT)].copy()
    micro_test = micro_original[micro_original["feature"].eq(RIGHT)].copy()
    micro_error, micro_rows = max_matched_error(
        micro_ref,
        micro_test,
        ["feature", "contrast"],
        ["delta_log2", "hedges_g", "p"],
    )

    committed_thyroid = pd.read_csv(
        ROOT
        / "phases/v3/results/gse248205_thyroid_spatial/gse248205_module_gene_contrasts.tsv",
        sep="\t",
    )
    thyroid_ref = committed_thyroid[
        committed_thyroid["feature_type"].eq("module")
        & committed_thyroid["feature"].isin(MODULES)
    ].copy()
    thyroid_test = thyroid_original[
        thyroid_original["feature_type"].eq("module")
        & thyroid_original["feature"].isin(MODULES)
    ].copy()
    thyroid_error, thyroid_rows = max_matched_error(
        thyroid_ref,
        thyroid_test,
        ["feature", "contrast"],
        ["delta_case_minus_control", "hedges_g", "p"],
    )

    committed_celiac = pd.read_csv(
        ROOT
        / "phases/v3/results/gse315138_celiac_marker/gse315138_donor_module_comparisons.tsv",
        sep="\t",
    )
    celiac_ref = committed_celiac[
        committed_celiac["metric"].eq("mean_score")
        & committed_celiac["module"].isin(MODULES)
    ].copy()
    celiac_test = celiac_original[
        celiac_original["metric"].eq("mean_score")
        & celiac_original["module"].isin(MODULES)
    ].copy()
    celiac_error, celiac_rows = max_matched_error(
        celiac_ref,
        celiac_test,
        ["module", "metric", "compartment"],
        ["delta_case_minus_control", "hedges_g", "p"],
    )

    exact_rows = [
        {
            "source": "GSE111972",
            "scope": "MIF/CD74 module only; canonical IFN/HLA/GILT modules are new sensitivity scores",
            "n_rows_compared": micro_rows,
            "max_absolute_error": micro_error,
        },
        {
            "source": "GSE248205",
            "scope": "four canonical modules",
            "n_rows_compared": thyroid_rows,
            "max_absolute_error": thyroid_error,
        },
        {
            "source": "GSE315138",
            "scope": "four canonical mean-score modules",
            "n_rows_compared": celiac_rows,
            "max_absolute_error": celiac_error,
        },
    ]
    if max(row["max_absolute_error"] for row in exact_rows) > 1e-10:
        raise RuntimeError(f"Additional-atlas original rebuild mismatch: {exact_rows}")

    original_extra = extract_extra_effects(
        micro_original, thyroid_original, celiac_original, "canonical_original"
    )
    unique_extra = extract_extra_effects(
        micro_unique, thyroid_unique, celiac_unique, "globally_disjoint"
    )
    extra_effects = pd.concat([original_extra, unique_extra], ignore_index=True)

    direct = direct_dataset_effects()
    extra_dataset = (
        unique_extra.groupby(["physical_dataset", "module"], as_index=False)["effect"]
        .mean()
        .pivot(index="physical_dataset", columns="module", values="effect")
        .reset_index()
    )
    dataset_effects = pd.concat([direct, extra_dataset], ignore_index=True)
    dataset_effects = dataset_effects[["physical_dataset", *MODULES]]
    if dataset_effects[list(MODULES)].isna().any().any() or len(dataset_effects) != 8:
        raise RuntimeError("Expected complete four-module effects across eight physical datasets")

    recurrence_rows = []
    p_values = []
    for module in MODULES:
        effects = dataset_effects[module].to_numpy(dtype=float)
        n_positive = int(np.sum(effects > 0))
        p_value = float(stats.binomtest(n_positive, len(effects), 0.5, alternative="greater").pvalue)
        lodo_proportions = []
        for omitted in range(len(effects)):
            retained = np.delete(effects, omitted)
            lodo_proportions.append(float(np.mean(retained > 0)))
        recurrence_rows.append(
            {
                "module": module,
                "n_physical_datasets": len(effects),
                "n_positive_dataset_means": n_positive,
                "positive_fraction": n_positive / len(effects),
                "one_sided_exact_binomial_p": p_value,
                "minimum_lodo_positive_fraction": min(lodo_proportions),
            }
        )
        p_values.append(p_value)
    for row, q_value in zip(recurrence_rows, bh_adjust(p_values), strict=True):
        row["q_bh_four_modules"] = q_value
        row["passes_disjoint_recurrence_gate"] = (
            int(row["n_positive_dataset_means"]) >= 7
            and q_value <= 0.10
            and float(row["minimum_lodo_positive_fraction"]) >= 0.75
        )

    passing = [row["module"] for row in recurrence_rows if row["passes_disjoint_recurrence_gate"]]
    summary = {
        "purpose": "V53 source-level globally disjoint APC recurrence sensitivity across independent atlases",
        "n_physical_datasets": len(dataset_effects),
        "physical_datasets": dataset_effects["physical_dataset"].tolist(),
        "n_additional_source_contexts": len(unique_extra) // len(MODULES),
        "original_rebuild_max_errors": {
            row["source"]: row["max_absolute_error"] for row in exact_rows
        },
        "globally_unique_gene_counts": {module: len(unique[module]) for module in MODULES},
        "modules_passing_disjoint_recurrence_gate": passing,
        "verdict": (
            "BROAD_APC_RECURRENCE_SURVIVES_DISJOINT_PHYSICAL_DATASET_GATE"
            if passing
            else "BROAD_APC_RECURRENCE_NOT_ESTABLISHED_AFTER_DISJOINT_PHYSICAL_DATASET_GATE"
        ),
        "boundary": "Cross-disease direction recurrence only; not MS-specific, causal, predictive, or therapeutic evidence.",
    }

    OUT.mkdir(parents=True, exist_ok=True)
    extra_effects.to_csv(OUT / "additional_atlas_module_effects.tsv", sep="\t", index=False)
    dataset_effects.to_csv(OUT / "disjoint_physical_dataset_effects.tsv", sep="\t", index=False)
    write_tsv(OUT / "original_rebuild_checks.tsv", exact_rows)
    write_tsv(OUT / "module_recurrence_tests.tsv", recurrence_rows)
    write_tsv(
        OUT / "module_gene_partition.tsv",
        [
            {
                "module": module,
                "original_genes": ";".join(original[module]),
                "globally_disjoint_genes": ";".join(unique[module]),
            }
            for module in MODULES
        ],
    )
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    report = [
        "# V53 Additional-Atlas Disjoint Rescoring",
        "",
        f"Verdict: **{summary['verdict']}**.",
        "",
        "Canonical original scores were source-rebuilt before sensitivity analysis. Exact",
        "checks cover the unchanged GSE111972 receptor module and all four canonical modules",
        "in GSE248205 and GSE315138. Effects were then recomputed with genes globally unique",
        "to each of the four APC modules.",
        "",
        "For recurrence, compartments and disease contrasts were averaged within each physical",
        "dataset before a directional sign test. This yields eight physical datasets: five",
        "held direct-h5ad sources plus GSE111972, GSE248205, and GSE315138. The gate requires",
        "at least 7/8 positive dataset means, BH q<=0.10 across four modules, and leave-one-",
        "dataset-out positive fraction >=0.75.",
        "",
        f"Modules passing: `{';'.join(passing) if passing else 'none'}`.",
        "This result concerns broad cross-disease recurrence only. It is not MS-specific and",
        "does not identify causal direction, treatment benefit, or a therapeutic target.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
