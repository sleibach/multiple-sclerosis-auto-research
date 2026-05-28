#!/usr/bin/env python3
"""Wave87 cross-system anti-TNF resistance gene check.

Wave86 identified a gene-level inflammatory/IFN-high anti-TNF nonresponse
state in IBD mucosal biopsies. This script asks whether the same genes also
predict anti-TNF nonresponse in a different autoimmune tissue system:
baseline RA synovium from GSE198520.

The point is falsification, not rescue. If the genes do not behave similarly in
RA synovium, they should be treated as IBD anti-TNF stratification biology, not
as a cross-autoimmune mechanism.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy import stats

from v3_analyze_direct_h5ad_cell_states import ROOT
from v3_wave85_external_geo_antitnf_validation import bh, design_matrix, hedges_g, markdown_table, rel, residualize, write_json, zscore_rows


SEED = 20260527
OUT = ROOT / "results_v3" / "wave87_cross_system_antitnf_resistance_gene_check"

W86_META = ROOT / "results_v3" / "wave86_external_geo_antitnf_gene_driver" / "external_geo_gene_meta_rank.tsv"
RA_COUNTS = ROOT / "results_v3" / "wave65_gse198520_ra_synovium_antitnf_audit" / "gse198520_counts_used.tsv"
RA_META = ROOT / "results_v3" / "wave65_gse198520_ra_synovium_antitnf_audit" / "gse198520_sample_metadata.tsv"
IBD_RAW = ROOT / "results_v3" / "wave68_gse282122_unrestricted_gene_screen" / "raw_remission_response_gene_tests.tsv"
IBD_ADJ = ROOT / "results_v3" / "wave68_gse282122_unrestricted_gene_screen" / "adjusted_top_gene_ols.tsv"


def log_cpm(counts: pd.DataFrame) -> pd.DataFrame:
    lib = counts.sum(axis=0).replace(0, np.nan)
    return np.log2(counts.div(lib, axis=1) * 1_000_000.0 + 1.0)


def auc_score(y: np.ndarray, score: np.ndarray) -> float:
    y = np.asarray(y, dtype=int)
    score = np.asarray(score, dtype=float)
    pos = score[y == 1]
    neg = score[y == 0]
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    wins = 0.0
    for value in pos:
        wins += float((value > neg).sum())
        wins += 0.5 * float((value == neg).sum())
    return wins / float(len(pos) * len(neg))


def test_ra_baseline_gene(expr: pd.DataFrame, meta: pd.DataFrame, gene: str) -> dict[str, Any]:
    if gene not in expr.index:
        return {}
    pre = meta[meta["timepoint"].astype(str).str.lower().eq("pre")].copy()
    pre = pre[pre["count_column"].isin(expr.columns)].copy()
    pre["response"] = pre["responder_moderate_or_good"].astype(str).str.lower().isin(["true", "1", "yes"]).astype(int)
    pre = pre[pre["response"].isin([0, 1])].copy()
    if len(pre) < 8 or pre["response"].nunique() < 2:
        return {}
    values = expr.loc[gene, pre["count_column"].tolist()].astype(float).to_numpy()
    df = pre.reset_index(drop=True).copy()
    df["_score"] = values
    df = df[np.isfinite(df["_score"])].copy()
    if len(df) < 8 or df["response"].nunique() < 2:
        return {}
    covars = ["pathotype", "biologic", "inflammatory_score", "das28_score"]
    adjusted = residualize(df["_score"].to_numpy(float), df, covars)
    y = df["response"].astype(int).to_numpy()
    responders = adjusted[y == 1]
    nonresponders = adjusted[y == 0]
    if len(responders) >= 3 and len(nonresponders) >= 3:
        t_stat, p_value = stats.ttest_ind(responders, nonresponders, equal_var=False, nan_policy="omit")
    else:
        t_stat, p_value = np.nan, np.nan
    effect = float(np.nanmean(responders) - np.nanmean(nonresponders))
    auc_response = auc_score(y, adjusted)
    return {
        "system": "RA_synovium_GSE198520_baseline",
        "gene": gene,
        "n_patients": int(len(df)),
        "n_responders": int(y.sum()),
        "n_nonresponders": int((1 - y).sum()),
        "covariates": ";".join(covars),
        "effect_responder_minus_non": effect,
        "hedges_g_responder_minus_non": hedges_g(responders, nonresponders),
        "auc_high_score_response": auc_response,
        "auc_high_score_nonresponse": float(1.0 - auc_response) if np.isfinite(auc_response) else np.nan,
        "p": float(p_value) if np.isfinite(p_value) else 1.0,
        "nonresponse_high_direction": bool(effect < 0),
    }


def summarize_ibd_gse282122(genes: list[str]) -> pd.DataFrame:
    if not IBD_RAW.exists():
        return pd.DataFrame()
    raw = pd.read_csv(IBD_RAW, sep="\t", low_memory=False)
    raw["gene"] = raw["gene"].astype(str).str.upper()
    keep = raw[raw["gene"].isin(genes)].copy()
    if keep.empty:
        return pd.DataFrame()
    keep["raw_fdr"] = pd.to_numeric(keep.get("raw_fdr"), errors="coerce")
    keep["raw_p"] = pd.to_numeric(keep.get("raw_p"), errors="coerce")
    keep["raw_delta_remission_minus_non"] = pd.to_numeric(keep.get("raw_delta_remission_minus_non"), errors="coerce")
    summary = (
        keep.groupby("gene")
        .agg(
            gse282122_cell_states_tested=("cell_state", "nunique"),
            gse282122_min_raw_p=("raw_p", "min"),
            gse282122_min_raw_fdr=("raw_fdr", "min"),
            gse282122_best_raw_delta_remission_minus_non=("raw_delta_remission_minus_non", lambda s: s.iloc[np.nanargmin(np.abs(s.to_numpy(float)))] if s.notna().any() else np.nan),
        )
        .reset_index()
    )
    best_rows = []
    for gene, group in keep.groupby("gene"):
        best = group.sort_values("raw_p").iloc[0]
        best_rows.append(
            {
                "gene": gene,
                "gse282122_best_cell_state": best.get("cell_state", ""),
                "gse282122_best_raw_p": best.get("raw_p", np.nan),
                "gse282122_best_raw_fdr": best.get("raw_fdr", np.nan),
                "gse282122_best_raw_delta_remission_minus_non": best.get("raw_delta_remission_minus_non", np.nan),
            }
        )
    best_df = pd.DataFrame(best_rows)
    summary = summary.drop(columns=["gse282122_best_raw_delta_remission_minus_non"], errors="ignore").merge(best_df, on="gene", how="left")
    return summary


def analyze_cross_system() -> dict[str, Any]:
    OUT.mkdir(parents=True, exist_ok=True)
    w86 = pd.read_csv(W86_META, sep="\t")
    anchors = w86[w86["call"].isin(["GENE_LEVEL_ANTITNF_NONRESPONSE_ANCHOR", "PARK_DIRECTIONAL_NONRESPONSE_GENE"])].copy()
    genes = sorted(anchors["gene"].astype(str).str.upper().unique())

    counts = pd.read_csv(RA_COUNTS, sep="\t", low_memory=False).set_index("GeneSymbol")
    counts.index = counts.index.astype(str).str.upper()
    meta = pd.read_csv(RA_META, sep="\t", low_memory=False)
    expr = zscore_rows(log_cpm(counts))

    ra_rows = []
    for gene in genes:
        row = test_ra_baseline_gene(expr, meta, gene)
        if row:
            ra_rows.append(row)
    ra = pd.DataFrame(ra_rows)
    if not ra.empty:
        ra["fdr_ra"] = bh(ra["p"])
        ra = ra.sort_values(["nonresponse_high_direction", "p"], ascending=[False, True])

    ibd282 = summarize_ibd_gse282122(genes)

    integrated = anchors.merge(ra, on="gene", how="left", suffixes=("_wave86", "_ra"))
    integrated = integrated.merge(ibd282, on="gene", how="left")
    ra_nonresponse = integrated["nonresponse_high_direction"].map(lambda value: bool(value) if pd.notna(value) else False)
    ra_p = integrated["p"].fillna(1.0).astype(float)
    integrated["ra_replication_call"] = np.where(
        ra_nonresponse & (ra_p < 0.10),
        "RA_BASELINE_DIRECTIONAL_REPLICATION",
        np.where(
            ra_nonresponse,
            "RA_BASELINE_SAME_DIRECTION_WEAK",
            "NO_RA_BASELINE_REPLICATION",
        ),
    )
    integrated["cross_system_call"] = np.where(
        integrated["ra_replication_call"].eq("RA_BASELINE_DIRECTIONAL_REPLICATION"),
        "PARK_CROSS_SYSTEM_ANTITNF_RESISTANCE_GENE",
        "IBD_RESTRICTED_OR_UNRESOLVED_ANTITNF_RESISTANCE_GENE",
    )
    integrated = integrated.sort_values(
        [
            "cross_system_call",
            "p",
            "meta_rank_score",
        ],
        ascending=[True, True, False],
    )

    ra.to_csv(OUT / "ra_synovium_baseline_gene_response_tests.tsv", sep="\t", index=False)
    ibd282.to_csv(OUT / "gse282122_top_gene_response_delta_summary.tsv", sep="\t", index=False)
    integrated.to_csv(OUT / "cross_system_antitnf_gene_integration.tsv", sep="\t", index=False)

    call_counts = integrated["cross_system_call"].value_counts().to_dict()
    summary = {
        "seed": SEED,
        "n_wave86_anchor_or_park_genes": int(len(genes)),
        "n_ra_tested_genes": int(len(ra)),
        "call_counts": {str(k): int(v) for k, v in call_counts.items()},
        "inputs": {
            "wave86_gene_meta": rel(W86_META),
            "ra_counts": rel(RA_COUNTS),
            "ra_metadata": rel(RA_META),
            "gse282122_raw_gene_tests": rel(IBD_RAW),
        },
    }
    write_json(OUT / "summary.json", summary)

    report = [
        "# Wave87 Cross-System Anti-TNF Resistance Gene Check",
        "",
        "Question: do Wave86 IBD anti-TNF nonresponse genes replicate as baseline anti-TNF nonresponse genes in RA synovium?",
        "",
        "## Integrated Gene Calls",
        "",
        markdown_table(
            integrated[
                [
                    "gene",
                    "modules",
                    "call",
                    "weighted_mean_hedges_g_responder_minus_non",
                    "median_auc_high_score_nonresponse",
                    "effect_responder_minus_non",
                    "hedges_g_responder_minus_non",
                    "auc_high_score_nonresponse",
                    "p",
                    "fdr_ra",
                    "ra_replication_call",
                    "cross_system_call",
                    "gse282122_best_cell_state",
                    "gse282122_best_raw_p",
                ]
            ],
            max_rows=40,
        ),
        "",
        "## Guardrail",
        "",
        "RA synovium is a different tissue and clinical response endpoint from IBD mucosa. A failure to replicate here does not refute IBD anti-TNF stratification, but it prevents a cross-autoimmune therapeutic mechanism claim.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    return summary


def main() -> None:
    analyze_cross_system()


if __name__ == "__main__":
    main()
