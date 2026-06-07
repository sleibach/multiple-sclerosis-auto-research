#!/usr/bin/env python3
"""Score the V35 host EBV-transformation module in GSE10325 sorted SLE cells."""

from __future__ import annotations

import csv
import gzip
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats


ROOT = Path(__file__).resolve().parents[1]
SERIES = ROOT / "data/raw_v2/GSE10325_series_matrix.txt.gz"
ANNOT = ROOT / "data/raw_v2/GPL96.annot.gz"
EBV_UP = ROOT / "analysis/v35_ebv_module_gse162516/host_ebv_transformation_up_top200.tsv"
EBV_DOWN = ROOT / "analysis/v35_ebv_module_gse162516/host_ebv_transformation_down_top200.tsv"
OUTDIR = ROOT / "analysis/v35_ebv_module_gse10325_sorted_sle"

IFN_APC_GENES = {
    "STAT1",
    "IRF1",
    "IRF7",
    "ISG15",
    "IFIT1",
    "IFIT2",
    "IFIT3",
    "MX1",
    "OAS1",
    "OAS2",
    "HLA-DRA",
    "HLA-DRB1",
    "HLA-DPA1",
    "HLA-DPB1",
    "HLA-DQA1",
    "HLA-DQB1",
    "CD74",
    "CIITA",
    "PSMB8",
    "PSMB9",
    "TAP1",
    "TAP2",
}


def read_module(path: Path, n: int = 100) -> set[str]:
    df = pd.read_csv(path, sep="\t")
    for candidate in ("gene", "gene_symbol", "tracking_id"):
        if candidate in df.columns:
            col = candidate
            break
    else:
        raise ValueError(f"No recognized gene column in {path}: {list(df.columns)}")
    return set(df[col].astype(str).str.upper().head(n))


def read_annotation(path: Path) -> pd.DataFrame:
    rows = []
    with gzip.open(path, "rt", errors="replace") as handle:
        in_table = False
        reader = None
        for line in handle:
            line = line.rstrip("\n")
            if line == "!platform_table_begin":
                in_table = True
                continue
            if line == "!platform_table_end":
                break
            if not in_table:
                continue
            if reader is None:
                header = line.split("\t")
                reader = csv.DictReader([], fieldnames=header, delimiter="\t")
                continue
            parts = line.split("\t")
            rec = dict(zip(reader.fieldnames or [], parts))
            probe = rec.get("ID", "")
            symbols = rec.get("Gene symbol", "")
            for sym in symbols.split("///"):
                sym = sym.strip().upper()
                if sym:
                    rows.append({"probe": probe, "gene": sym})
    return pd.DataFrame(rows).drop_duplicates()


def parse_series_matrix(path: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    meta: dict[str, list[str]] = {}
    matrix_lines: list[str] = []
    in_matrix = False
    with gzip.open(path, "rt", errors="replace") as handle:
        for raw in handle:
            line = raw.rstrip("\n")
            if line == "!series_matrix_table_begin":
                in_matrix = True
                continue
            if line == "!series_matrix_table_end":
                break
            if in_matrix:
                matrix_lines.append(line)
                continue
            if line.startswith("!Sample_title") or line.startswith("!Sample_geo_accession") or line.startswith("!Sample_characteristics_ch1"):
                parts = next(csv.reader([line], delimiter="\t"))
                meta[parts[0]] = [p.strip('"') for p in parts[1:]]

    accessions = meta["!Sample_geo_accession"]
    titles = meta["!Sample_title"]
    chars = meta["!Sample_characteristics_ch1"]
    samples = pd.DataFrame({"sample": accessions, "title": titles, "characteristics": chars})
    samples["condition"] = np.where(samples["characteristics"].str.contains("SLE", case=False), "SLE", "HC")
    samples["subset"] = samples["title"].str.extract(r"(CD4 T cells|CD19 B cells|myeloid cells)", expand=False)
    samples["subset"] = samples["subset"].map(
        {
            "CD4 T cells": "CD4_T",
            "CD19 B cells": "CD19_B",
            "myeloid cells": "myeloid",
        }
    )

    from io import StringIO

    expr = pd.read_csv(StringIO("\n".join(matrix_lines)), sep="\t")
    expr = expr.rename(columns={expr.columns[0]: "probe"})
    expr["probe"] = expr["probe"].astype(str).str.strip('"')
    for col in expr.columns[1:]:
        expr[col] = pd.to_numeric(expr[col], errors="coerce")
    return samples, expr


def score_module(expr: pd.DataFrame, annot: pd.DataFrame, genes: set[str], label: str) -> pd.Series:
    probes = set(annot.loc[annot["gene"].isin(genes), "probe"])
    use = expr[expr["probe"].isin(probes)].copy()
    if use.empty:
        return pd.Series(dtype=float, name=label), 0
    values = use.drop(columns=["probe"])
    return values.mean(axis=0).rename(label), len(use)


def welch(a: pd.Series, b: pd.Series) -> tuple[float, float, float, float, int, int]:
    a = pd.to_numeric(a, errors="coerce").dropna()
    b = pd.to_numeric(b, errors="coerce").dropna()
    if len(a) < 2 or len(b) < 2:
        return math.nan, math.nan, math.nan, math.nan, len(a), len(b)
    stat = stats.ttest_ind(a, b, equal_var=False)
    delta = float(a.mean() - b.mean())
    denom = math.sqrt(((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) / (len(a) + len(b) - 2))
    g = float(delta / denom) if denom else math.nan
    return delta, float(a.mean()), float(b.mean()), float(stat.pvalue), len(a), len(b)


def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    up = read_module(EBV_UP)
    down = read_module(EBV_DOWN)
    annot = read_annotation(ANNOT)
    samples, expr = parse_series_matrix(SERIES)

    scores = []
    counts = {}
    for genes, label in [(up, "ebv_up"), (down, "ebv_down"), (IFN_APC_GENES, "ifn_apc")]:
        score, n_probes = score_module(expr, annot, genes, label)
        scores.append(score)
        counts[label] = n_probes
    score_df = pd.concat(scores, axis=1).reset_index(names="sample")
    score_df = samples.merge(score_df, on="sample", how="left")
    score_df["ebv_up_minus_down"] = score_df["ebv_up"] - score_df["ebv_down"]

    rows = []
    for subset, sub in score_df.groupby("subset"):
        for score in ["ebv_up", "ebv_down", "ebv_up_minus_down", "ifn_apc"]:
            sle = sub.loc[sub["condition"] == "SLE", score]
            hc = sub.loc[sub["condition"] == "HC", score]
            delta, mean_sle, mean_hc, p, n_sle, n_hc = welch(sle, hc)
            rows.append(
                {
                    "subset": subset,
                    "score": score,
                    "n_sle": n_sle,
                    "n_hc": n_hc,
                    "mean_sle": mean_sle,
                    "mean_hc": mean_hc,
                    "delta_sle_minus_hc": delta,
                    "welch_p": p,
                }
            )

    # Residualize EBV-up against IFN/APC within each sorted subset, then test
    # the residual disease contrast. This is a narrow separability check, not a
    # causal EBV claim.
    for subset, sub in score_df.groupby("subset"):
        sub = sub.dropna(subset=["ebv_up", "ifn_apc"]).copy()
        x = sub["ifn_apc"].to_numpy()
        y = sub["ebv_up"].to_numpy()
        slope, intercept, *_ = stats.linregress(x, y)
        sub["ebv_up_resid_ifn"] = y - (intercept + slope * x)
        sle = sub.loc[sub["condition"] == "SLE", "ebv_up_resid_ifn"]
        hc = sub.loc[sub["condition"] == "HC", "ebv_up_resid_ifn"]
        delta, mean_sle, mean_hc, p, n_sle, n_hc = welch(sle, hc)
        rho, rho_p = stats.spearmanr(sub["ebv_up"], sub["ifn_apc"])
        rows.append(
            {
                "subset": subset,
                "score": "ebv_up_resid_ifn",
                "n_sle": n_sle,
                "n_hc": n_hc,
                "mean_sle": mean_sle,
                "mean_hc": mean_hc,
                "delta_sle_minus_hc": delta,
                "welch_p": p,
                "ebv_up_ifn_spearman": float(rho),
                "ebv_up_ifn_p": float(rho_p),
            }
        )

    test_df = pd.DataFrame(rows)
    score_df.to_csv(OUTDIR / "sample_sorted_scores.tsv", sep="\t", index=False)
    test_df.to_csv(OUTDIR / "sorted_sle_tests.tsv", sep="\t", index=False)

    resid = test_df[test_df["score"] == "ebv_up_resid_ifn"].sort_values("welch_p")
    summary = {
        "hypothesis": "SLE host EBV-module-like signal compartment localization",
        "grounded_result": "sorted_subset_test_no_ebv_metadata",
        "n_samples": int(len(samples)),
        "subsets": sorted(samples["subset"].dropna().unique()),
        "probe_counts": counts,
        "best_ifn_residualized_subset": resid.iloc[0].to_dict() if not resid.empty else None,
        "interpretation": (
            "GSE10325 tests whether the host EBV-transformation-like module is localized "
            "to sorted SLE immune subsets and separable from IFN/APC. It has no EBV "
            "serostatus or viral-load metadata, so it cannot establish EBV imprint causality."
        ),
    }
    (OUTDIR / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
