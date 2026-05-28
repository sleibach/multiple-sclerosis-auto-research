#!/usr/bin/env python3
"""Wave152: external human interface-cell perturbation module test.

This wave uses verified public processed GEO matrices discovered after Wave151.
It deliberately avoids superseries/subseries that were not yet resolved into a
usable processed matrix.
"""

from __future__ import annotations

import gzip
import json
import math
import tarfile
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats


SEED = 20260527
np.random.seed(SEED)

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw_v3" / "interface_perturbation_geo"
OUT = ROOT / "results_v3" / "wave152_external_interface_perturbation_module_test"
OUT.mkdir(parents=True, exist_ok=True)

MODULES: dict[str, list[str]] = {
    "epithelial_chemokine_entry": [
        "CXCL1",
        "CXCL2",
        "CXCL3",
        "CXCL5",
        "CXCL8",
        "CCL20",
        "ICAM1",
        "SELE",
        "SAA1",
        "SAA2",
    ],
    "stromal_retention_fibrosis": [
        "PDPN",
        "VCAM1",
        "ICAM1",
        "SERPINE1",
        "COL1A1",
        "COL1A2",
        "COL3A1",
        "ITGA5",
        "ITGB1",
        "CXCL12",
        "MMP3",
        "MMP9",
    ],
    "endothelial_entry": [
        "VCAM1",
        "ICAM1",
        "SELE",
        "ANGPT2",
        "CXCL10",
        "CXCL11",
        "CCL2",
        "ACKR1",
        "VWF",
        "PECAM1",
    ],
    "tls_lymphoid_niche": [
        "CXCL13",
        "CCL19",
        "CCL21",
        "LTBR",
        "TNFSF14",
        "TNFRSF14",
        "PDPN",
        "CXCL12",
        "ICAM1",
        "VCAM1",
    ],
    "scfa_receptor_effector": ["HCAR2", "HCAR3", "FFAR2", "FFAR3", "SLC5A8", "HDAC1", "HDAC2"],
    "vdr_retinoid_effector": ["VDR", "RXRA", "RXRB", "CYP24A1", "CAMP", "CD14", "ALDH1A1"],
}


@dataclass(frozen=True)
class Contrast:
    dataset: str
    system: str
    contrast: str
    treatment_cols: tuple[str, ...]
    control_cols: tuple[str, ...]
    accession: str


def load_hgnc_mapping() -> dict[str, str]:
    hgnc = pd.read_csv(RAW / "hgnc_complete_set.txt", sep="\t", dtype=str)
    mapping: dict[str, str] = {}
    for _, row in hgnc.iterrows():
        symbol = str(row.get("symbol", "")).strip()
        ensembl = str(row.get("ensembl_gene_id", "")).strip()
        if symbol and ensembl and ensembl != "nan":
            mapping[ensembl.split(".")[0]] = symbol
    return mapping


def read_table(path: Path) -> pd.DataFrame:
    if path.suffix == ".gz":
        return pd.read_csv(path, sep="\t", compression="gzip")
    return pd.read_csv(path, sep="\t")


def collapse_to_symbols(df: pd.DataFrame, gene_col: str, symbol_map: dict[str, str] | None = None) -> pd.DataFrame:
    data = df.copy()
    if symbol_map is None:
        data["symbol"] = data[gene_col].astype(str)
    else:
        data["symbol"] = data[gene_col].astype(str).str.split(".").str[0].map(symbol_map)
    data = data.dropna(subset=["symbol"])
    data["symbol"] = data["symbol"].astype(str).str.upper()
    numeric_cols = [c for c in data.columns if c not in {gene_col, "symbol"} and pd.api.types.is_numeric_dtype(data[c])]
    if not numeric_cols:
        for c in data.columns:
            if c not in {gene_col, "symbol"}:
                data[c] = pd.to_numeric(data[c], errors="coerce")
        numeric_cols = [c for c in data.columns if c not in {gene_col, "symbol"} and pd.api.types.is_numeric_dtype(data[c])]
    collapsed = data.groupby("symbol", as_index=True)[numeric_cols].sum(min_count=1)
    return collapsed


def log_cpm(counts: pd.DataFrame) -> pd.DataFrame:
    mat = counts.astype(float)
    lib = mat.sum(axis=0).replace(0, np.nan)
    return np.log2(mat.div(lib, axis=1) * 1_000_000 + 1.0)


def log2_matrix(values: pd.DataFrame) -> pd.DataFrame:
    return np.log2(values.astype(float) + 1.0)


def module_stats(expr: pd.DataFrame, contrast: Contrast) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for module, genes in MODULES.items():
        present = [g for g in genes if g in expr.index]
        if len(present) < max(2, math.ceil(len(genes) * 0.25)):
            rows.append(
                {
                    "dataset": contrast.dataset,
                    "accession": contrast.accession,
                    "system": contrast.system,
                    "contrast": contrast.contrast,
                    "module": module,
                    "n_genes": len(genes),
                    "n_present": len(present),
                    "mean_delta": np.nan,
                    "p_value": np.nan,
                    "direction": "INSUFFICIENT_GENES",
                    "present_genes": ";".join(present),
                }
            )
            continue
        treatment = expr.loc[present, list(contrast.treatment_cols)].mean(axis=1)
        control = expr.loc[present, list(contrast.control_cols)].mean(axis=1)
        delta = treatment - control
        p_value = float(stats.ttest_1samp(delta.values, 0.0, nan_policy="omit").pvalue)
        mean_delta = float(np.nanmean(delta.values))
        if p_value < 0.05 and mean_delta > 0:
            direction = "UP"
        elif p_value < 0.05 and mean_delta < 0:
            direction = "DOWN"
        else:
            direction = "NS"
        rows.append(
            {
                "dataset": contrast.dataset,
                "accession": contrast.accession,
                "system": contrast.system,
                "contrast": contrast.contrast,
                "module": module,
                "n_genes": len(genes),
                "n_present": len(present),
                "mean_delta": mean_delta,
                "p_value": p_value,
                "direction": direction,
                "present_genes": ";".join(present),
            }
        )
    return rows


def cosine(a: pd.Series, b: pd.Series) -> float:
    common = sorted(set(a.dropna().index) & set(b.dropna().index))
    if not common:
        return float("nan")
    av = a.loc[common].astype(float).values
    bv = b.loc[common].astype(float).values
    denom = float(np.linalg.norm(av) * np.linalg.norm(bv))
    if denom == 0:
        return float("nan")
    return float(np.dot(av, bv) / denom)


def dataset_gse190634(symbol_map: dict[str, str]) -> tuple[pd.DataFrame, list[Contrast]]:
    df = read_table(RAW / "GSE190634_read_counts.txt.gz")
    counts = collapse_to_symbols(df, "geneID", symbol_map)
    expr = log_cpm(counts)
    controls = tuple(c for c in expr.columns if c.startswith("Control"))
    contrasts = [
        Contrast("GSE190634", "primary human colonoids", "TNF_vs_control", tuple(c for c in expr.columns if c.startswith("TNFa_")), controls, "GSE190634"),
        Contrast("GSE190634", "primary human colonoids", "IFNG_vs_control", tuple(c for c in expr.columns if c.startswith("IFNg_")), controls, "GSE190634"),
        Contrast("GSE190634", "primary human colonoids", "IL17A_vs_control", tuple(c for c in expr.columns if c.startswith("IL17_")), controls, "GSE190634"),
        Contrast("GSE190634", "primary human colonoids", "IL17A_IL22_vs_control", tuple(c for c in expr.columns if c.startswith("IL2217_")), controls, "GSE190634"),
    ]
    return expr, contrasts


def dataset_gse217552() -> tuple[pd.DataFrame, list[Contrast], pd.Series, dict[str, pd.Series]]:
    df = read_table(RAW / "GSE217552_gene_count.txt.gz")
    numeric_cols = [c for c in df.columns if c.startswith("HEK")]
    counts = df[["gene_name", *numeric_cols]].copy()
    expr = log_cpm(collapse_to_symbols(counts, "gene_name"))
    control = tuple(c for c in expr.columns if c.startswith("HEKCTRL"))
    activated = tuple(c for c in expr.columns if c.startswith("HEKTNFIL17"))
    contrasts = [
        Contrast("GSE217552", "primary adult human epidermal keratinocytes", "TNF_IL17A_vs_control", activated, control, "GSE217552"),
        Contrast("GSE217552", "primary adult human epidermal keratinocytes", "fisetin_vs_activated", tuple(c for c in expr.columns if c.startswith("HEKT17_FIS")), activated, "GSE217552"),
        Contrast("GSE217552", "primary adult human epidermal keratinocytes", "rapamycin_vs_activated", tuple(c for c in expr.columns if c.startswith("HEKT17_RAP")), activated, "GSE217552"),
        Contrast("GSE217552", "primary adult human epidermal keratinocytes", "fisetin_rapamycin_vs_activated", tuple(c for c in expr.columns if c.startswith("HEKT17_FIRA")), activated, "GSE217552"),
        Contrast("GSE217552", "primary adult human epidermal keratinocytes", "methotrexate_vs_activated", tuple(c for c in expr.columns if c.startswith("HEKT17_MET")), activated, "GSE217552"),
    ]
    induction = expr[list(activated)].mean(axis=1) - expr[list(control)].mean(axis=1)
    treatment_deltas = {
        con.contrast: expr[list(con.treatment_cols)].mean(axis=1) - expr[list(con.control_cols)].mean(axis=1)
        for con in contrasts
        if con.contrast.endswith("_vs_activated")
    }
    return expr, contrasts, induction, treatment_deltas


def dataset_gse200309(symbol_map: dict[str, str]) -> tuple[pd.DataFrame, list[Contrast]]:
    df = read_table(RAW / "GSE200309_TxImport.GeneLevel.counts.GEO.txt.gz")
    df = df.rename(columns={df.columns[0]: "gene_id"})
    counts = collapse_to_symbols(df, "gene_id", symbol_map)
    expr = log2_matrix(counts)
    controls = ("19", "20", "21")
    contrasts = [
        Contrast("GSE200309", "human iPSC-derived intestinal epithelial layers", "butyrate_1mM_vs_control", ("1", "2", "3"), controls, "GSE200309"),
        Contrast("GSE200309", "human iPSC-derived intestinal epithelial layers", "butyrate_10mM_vs_control", ("4", "5", "6"), controls, "GSE200309"),
        Contrast("GSE200309", "human iPSC-derived intestinal epithelial layers", "acetate_1mM_vs_control", ("7", "8", "9"), controls, "GSE200309"),
        Contrast("GSE200309", "human iPSC-derived intestinal epithelial layers", "acetate_10mM_vs_control", ("10", "11", "12"), controls, "GSE200309"),
        Contrast("GSE200309", "human iPSC-derived intestinal epithelial layers", "propionate_1mM_vs_control", ("13", "14", "15"), controls, "GSE200309"),
        Contrast("GSE200309", "human iPSC-derived intestinal epithelial layers", "propionate_10mM_vs_control", ("16", "17", "18"), controls, "GSE200309"),
    ]
    return expr, contrasts


def dataset_gse237845() -> tuple[pd.DataFrame, list[Contrast]]:
    df = read_table(RAW / "GSE237845_normalized_counts.tsv.gz")
    df = df.rename(columns={df.columns[0]: "gene"})
    expr = log2_matrix(collapse_to_symbols(df, "gene"))
    contrasts = [
        Contrast("GSE237845", "human colonic fibroblast line CCD-18Co", "TWEAK_TNFSF12_vs_vehicle", ("coTWEAK24h_n1", "coTWEAK24h_n2", "coTWEAK24h_n3"), ("coVeh_n1", "coVeh_n2", "coVeh_n3"), "GSE237845")
    ]
    return expr, contrasts


def main() -> None:
    symbol_map = load_hgnc_mapping()
    all_rows: list[dict[str, object]] = []
    dataset_metadata: list[dict[str, object]] = []

    for loader in [dataset_gse190634, dataset_gse200309]:
        expr, contrasts = loader(symbol_map)
        dataset_metadata.append({"dataset": contrasts[0].dataset, "n_genes": int(expr.shape[0]), "n_samples": int(expr.shape[1])})
        for contrast in contrasts:
            all_rows.extend(module_stats(expr, contrast))

    expr217, contrasts217, induction217, treatment_deltas217 = dataset_gse217552()
    dataset_metadata.append({"dataset": "GSE217552", "n_genes": int(expr217.shape[0]), "n_samples": int(expr217.shape[1])})
    for contrast in contrasts217:
        all_rows.extend(module_stats(expr217, contrast))

    expr237, contrasts237 = dataset_gse237845()
    dataset_metadata.append({"dataset": "GSE237845", "n_genes": int(expr237.shape[0]), "n_samples": int(expr237.shape[1])})
    for contrast in contrasts237:
        all_rows.extend(module_stats(expr237, contrast))

    result = pd.DataFrame(all_rows)
    result["q_value_bh"] = np.nan
    valid = result["p_value"].notna()
    if valid.any():
        p = result.loc[valid, "p_value"].astype(float)
        order = np.argsort(p.values)
        ranks = np.empty_like(order)
        ranks[order] = np.arange(1, len(p) + 1)
        q = np.minimum(1.0, p.values * len(p) / ranks)
        result.loc[valid, "q_value_bh"] = q

    rescue_rows = []
    for name, delta in treatment_deltas217.items():
        rescue_rows.append(
            {
                "dataset": "GSE217552",
                "treatment_contrast": name,
                "global_cosine_vs_inflammatory_induction": cosine(delta, induction217),
                "interpretation": "negative_cosine_suggests_reversal",
            }
        )
    rescue = pd.DataFrame(rescue_rows)

    # Positive route definition for this wave: module is induced by autoimmune-
    # relevant cytokines in at least two human interface systems and at least one
    # treatment/ligand moves it down in the same or adjacent human interface
    # system at nominal p<0.05.
    induced = result[(result["direction"] == "UP") & result["contrast"].str.contains("vs_control|vs_vehicle", regex=True)]
    down = result[(result["direction"] == "DOWN") & result["contrast"].str.contains("vs_activated|vs_control", regex=True)]
    module_summary = []
    for module in MODULES:
        induced_systems = sorted(set(induced.loc[induced["module"] == module, "dataset"]))
        down_systems = sorted(set(down.loc[down["module"] == module, "dataset"]))
        module_summary.append(
            {
                "module": module,
                "induced_dataset_count": len(induced_systems),
                "induced_datasets": ";".join(induced_systems),
                "down_dataset_count": len(down_systems),
                "down_datasets": ";".join(down_systems),
                "passes_wave152_route_gate": len(induced_systems) >= 2 and len(down_systems) >= 1,
            }
        )
    summary_df = pd.DataFrame(module_summary)
    passing = summary_df[summary_df["passes_wave152_route_gate"]]
    branch = "INTERFACE_MODULE_ROUTE_REOPENED" if len(passing) else "NO_EXTERNAL_INTERFACE_MODULE_ROUTE_REOPENED"

    result.to_csv(OUT / "module_contrast_results.tsv", sep="\t", index=False)
    rescue.to_csv(OUT / "gse217552_global_rescue_cosines.tsv", sep="\t", index=False)
    summary_df.to_csv(OUT / "module_route_summary.tsv", sep="\t", index=False)
    (OUT / "dataset_metadata.json").write_text(json.dumps(dataset_metadata, indent=2) + "\n")
    summary = {
        "branch_call": branch,
        "random_seed": SEED,
        "datasets_analyzed": [m["dataset"] for m in dataset_metadata],
        "n_module_contrasts": int(len(result)),
        "n_route_gate_passing_modules": int(len(passing)),
        "route_gate_passing_modules": passing["module"].tolist(),
        "note": "GSE129488 was not analyzed in this wave because the superseries matrix URL did not resolve to a usable processed matrix; subseries resolution is deferred.",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    (OUT / "REPORT.md").write_text(
        "# Wave152 External Interface Perturbation Module Test\n\n"
        f"Branch call: `{branch}`.\n\n"
        "Datasets analyzed: `GSE190634`, `GSE217552`, `GSE200309`, `GSE237845`.\n\n"
        "This wave directly tests public human interface-cell perturbation matrices discovered after Wave151. "
        "The route gate requires module induction in at least two human interface datasets and a nominal down-shift "
        "under a treatment/ligand contrast in at least one dataset. It is a module-level perturbation screen, not a "
        "target claim.\n"
    )


if __name__ == "__main__":
    main()
