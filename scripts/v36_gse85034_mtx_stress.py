#!/usr/bin/env python3
"""Caveated V36 stress test of the V22 dynamic APC/HLA-II rule in GSE85034 MTX.

This is not a primary validation cohort for the MS/JAK-STAT bounded monitoring
lead. It is a reachable, unused psoriasis methotrexate arm with paired lesional
skin baseline/week-1 expression and week-16 PASI75 labels, so it is useful as a
cross-disease stress test only.
"""

from __future__ import annotations

import itertools
import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import v3_wave89_psoriasis_gse85034_response_validation as psor  # noqa: E402

OUT = ROOT / "analysis" / "v36_gse85034_mtx_stress"

IFN_APC = ["STAT1", "IRF1", "CXCL10", "GBP1", "ISG15", "CD74", "HLA-DRA"]
HLAII = ["HLA-DRA", "HLA-DRB1", "HLA-DPA1", "HLA-DPB1", "HLA-DQA1", "HLA-DQB1"]
RECEPTOR = ["CD74", "CD44", "CXCR4"]


def module_scores(expr: pd.DataFrame, genes: list[str]) -> tuple[pd.Series, list[str]]:
    present = [gene for gene in genes if gene in expr.index]
    if not present:
        return pd.Series(dtype=float), []
    z = expr.sub(expr.mean(axis=1), axis=0).div(expr.std(axis=1).replace(0, np.nan), axis=0)
    return z.loc[present].mean(axis=0, skipna=True), present


def auc_score(scores: np.ndarray, y: np.ndarray) -> float:
    if len(set(y.tolist())) < 2:
        return math.nan
    ranks = pd.Series(scores).rank(method="average").to_numpy()
    n1 = int(y.sum())
    n0 = int(len(y) - n1)
    rank_sum = float(ranks[y == 1].sum())
    return float((rank_sum - n1 * (n1 + 1) / 2.0) / (n1 * n0))


def exact_auc_p(scores: np.ndarray, y: np.ndarray) -> float:
    """One-sided exact label-permutation p for AUC >= observed."""
    n = len(y)
    n_pos = int(y.sum())
    observed = auc_score(scores, y)
    if not np.isfinite(observed) or n_pos == 0 or n_pos == n:
        return math.nan
    total = 0
    extreme = 0
    for pos_idx in itertools.combinations(range(n), n_pos):
        yy = np.zeros(n, dtype=int)
        yy[list(pos_idx)] = 1
        total += 1
        if auc_score(scores, yy) >= observed - 1e-12:
            extreme += 1
    return float(extreme / total)


def hedges_g(responder: np.ndarray, nonresponder: np.ndarray) -> float:
    if len(responder) < 2 or len(nonresponder) < 2:
        return math.nan
    pooled = math.sqrt(
        ((len(responder) - 1) * np.var(responder, ddof=1) + (len(nonresponder) - 1) * np.var(nonresponder, ddof=1))
        / (len(responder) + len(nonresponder) - 2)
    )
    if pooled == 0:
        return 0.0
    correction = 1.0 - 3.0 / (4.0 * (len(responder) + len(nonresponder)) - 9.0)
    return float(((np.mean(responder) - np.mean(nonresponder)) / pooled) * correction)


def summarize_feature(df: pd.DataFrame, feature: str) -> dict[str, object]:
    y = df["pasi75_wk16"].astype(int).to_numpy()
    scores = df[feature].to_numpy(float)
    responders = scores[y == 1]
    nonresponders = scores[y == 0]
    return {
        "feature": feature,
        "n": int(len(df)),
        "n_responders": int(y.sum()),
        "n_nonresponders": int(len(y) - y.sum()),
        "auc_high_score_response": auc_score(scores, y),
        "exact_auc_p": exact_auc_p(scores, y),
        "mean_responder": float(np.mean(responders)),
        "mean_nonresponder": float(np.mean(nonresponders)),
        "hedges_g_responder_minus_non": hedges_g(responders, nonresponders),
        "welch_p": float(stats.ttest_ind(responders, nonresponders, equal_var=False).pvalue)
        if len(responders) >= 2 and len(nonresponders) >= 2
        else math.nan,
    }


def markdown_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "_No rows._"
    clean = df.copy()
    for col in clean.columns:
        clean[col] = clean[col].map(lambda x: f"{x:.4g}" if isinstance(x, float) and np.isfinite(x) else x)
    header = "| " + " | ".join(clean.columns.astype(str)) + " |"
    sep = "| " + " | ".join(["---"] * len(clean.columns)) + " |"
    rows = ["| " + " | ".join(str(x) for x in row) + " |" for row in clean.to_numpy()]
    return "\n".join([header, sep, *rows])


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    wanted = set(IFN_APC + HLAII + RECEPTOR)
    metadata, expr_probe = psor.read_series_matrix(psor.SERIES)
    info = psor.sample_metadata(metadata)
    patients = psor.build_patient_response_table(info)
    probe_to_genes, coverage = psor.read_gpl10558_gene_map(psor.GPL10558_ANNOT, wanted)
    gene_expr = psor.expression_to_gene_level(expr_probe, probe_to_genes)

    ifn, ifn_present = module_scores(gene_expr, IFN_APC)
    hla, hla_present = module_scores(gene_expr, HLAII)
    rec, rec_present = module_scores(gene_expr, RECEPTOR)

    rows: list[dict[str, object]] = []
    for _, row in patients[patients["treatment"].eq("MTX")].iterrows():
        base = row["baseline_ls_sample"]
        if not base or not np.isfinite(row["pasi75_wk16"]):
            continue
        wk1 = info[(info["subject_id"].eq(row["subject_id"])) & (info["timepoint"].eq("WK1"))]["sample"]
        if wk1.empty:
            continue
        wk1_sample = str(wk1.iloc[0])
        if base not in ifn.index or wk1_sample not in ifn.index:
            continue
        delta_ifn = float(ifn[wk1_sample] - ifn[base])
        delta_hla = float(hla[wk1_sample] - hla[base]) if base in hla.index and wk1_sample in hla.index else math.nan
        delta_rec = float(rec[wk1_sample] - rec[base]) if base in rec.index and wk1_sample in rec.index else math.nan
        rows.append(
            {
                "subject_id": row["subject_id"],
                "baseline_sample": base,
                "week1_sample": wk1_sample,
                "baseline_pasi": row["baseline_pasi"],
                "week16_pasi": row["week16_pasi"],
                "pct_pasi_improvement_wk16": row["pct_pasi_improvement_wk16"],
                "pasi75_wk16": int(row["pasi75_wk16"]),
                "delta_IFN_APC": delta_ifn,
                "locked_signed_score": -delta_ifn,
                "delta_HLAII": delta_hla,
                "delta_RECEPTOR": delta_rec,
                "negative_delta_RECEPTOR": -delta_rec if np.isfinite(delta_rec) else math.nan,
            }
        )
    paired = pd.DataFrame(rows)
    paired.to_csv(OUT / "gse85034_mtx_paired_scores.tsv", sep="\t", index=False)
    coverage.to_csv(OUT / "module_gene_coverage.tsv", sep="\t", index=False)

    features = ["locked_signed_score", "delta_IFN_APC", "delta_HLAII", "negative_delta_RECEPTOR"]
    stats_rows = [summarize_feature(paired.dropna(subset=[feature]), feature) for feature in features if feature in paired]
    stats_df = pd.DataFrame(stats_rows)
    stats_df.to_csv(OUT / "gse85034_mtx_feature_tests.tsv", sep="\t", index=False)

    summary = {
        "cohort": "GSE85034_MTX",
        "disease": "psoriasis",
        "therapy": "methotrexate",
        "scope": "caveated_cross_disease_stress_test_only",
        "n_paired_labeled": int(len(paired)),
        "n_responders": int(paired["pasi75_wk16"].sum()) if not paired.empty else 0,
        "n_nonresponders": int(len(paired) - paired["pasi75_wk16"].sum()) if not paired.empty else 0,
        "timepoint": "baseline lesional skin to week 1",
        "outcome": "PASI75 at week 16 reconstructed from GEO PASI fields",
        "present_IFN_APC": ifn_present,
        "present_HLAII": hla_present,
        "present_RECEPTOR": rec_present,
        "primary_feature": "locked_signed_score = -delta_IFN_APC",
        "primary_result": stats_df[stats_df["feature"].eq("locked_signed_score")].to_dict("records")[0]
        if not stats_df.empty and stats_df["feature"].eq("locked_signed_score").any()
        else {},
        "interpretation": "secondary stress test; not a validation-pass/fail for the bounded MS/JAK-STAT monitoring rule",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    report = [
        "# V36 GSE85034 MTX Stress Test",
        "",
        "This is a caveated cross-disease stress test of the immutable V22 dynamic",
        "IFN/APC feature in the unused GSE85034 methotrexate arm. It is psoriasis",
        "lesional skin, not MS blood/CSF and not the bounded immune-remodeling",
        "validation setting; it therefore cannot upgrade or kill the V22/V23 lead.",
        "",
        "## Cohort",
        "",
        f"- Paired labeled subjects: `{summary['n_paired_labeled']}`.",
        f"- PASI75 responders/nonresponders: `{summary['n_responders']}` / `{summary['n_nonresponders']}`.",
        "- Feature: baseline lesional skin to week 1; outcome PASI75 at week 16.",
        f"- IFN/APC genes present: `{';'.join(ifn_present)}`.",
        f"- HLA-II genes present: `{';'.join(hla_present)}`.",
        f"- receptor genes present: `{';'.join(rec_present)}`.",
        "",
        "## Feature Tests",
        "",
        markdown_table(stats_df),
        "",
        "## Interpretation",
        "",
        "The result is recorded as a stress test only. A positive metric would show",
        "that early dynamic immune-remodeling information is not unique to the",
        "tofacitinib artifact, while a negative metric would be unsurprising because",
        "methotrexate psoriasis skin is outside the V23 bounded domain. Either way,",
        "the primary validation target remains the pre-specified V22/V23 monitoring",
        "rule in a fresh MS DMT cohort with steroid, QC, batch, timing, and cell",
        "composition metadata.",
    ]
    (OUT / "summary.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
