#!/usr/bin/env python3
"""Wave86 gene-level decomposition of external anti-TNF nonresponse state.

Wave85 showed that the residual lysosomal/APC endpoint did not externally
replicate, while generic inflammatory/IFN modules were consistently higher in
anti-TNF nonresponders. This script decomposes that signal into module genes.

The primary ranking uses only non-overlapping contexts:

- GSE12251 UC ACT1 baseline.
- GSE14580 UC Leuven baseline. The matching GSE16879 UC rows are kept as an
  overlap-control output but not counted independently.
- GSE16879 Crohn colitis baseline.
- GSE16879 Crohn ileitis baseline.
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
from v3_wave85_external_geo_antitnf_validation import (
    GPL570_ANNOT,
    MODULES,
    OUT as W85_OUT,
    RAW,
    SERIES_FILES,
    CohortSpec,
    bh,
    cohort_specs,
    design_matrix,
    expression_to_gene_level,
    hedges_g,
    markdown_table,
    mask_for_spec,
    patient_level_scores,
    read_gpl570_gene_map,
    read_series_matrix,
    rel,
    residualize,
    sample_metadata,
    write_json,
    zscore_rows,
)


SEED = 20260527
OUT = ROOT / "results_v3" / "wave86_external_geo_antitnf_gene_driver"

PRIMARY_CONTEXTS = {
    "GSE12251_UC_ACT1_baseline",
    "GSE14580_UC_Leuven_baseline",
    "GSE16879_Crohn_colitis_Leuven_baseline",
    "GSE16879_Crohn_ileitis_Leuven_baseline",
}

OVERLAP_CONTROL_CONTEXTS = {
    "GSE16879_UC_Leuven_baseline",
    "GSE16879_Crohn_all_Leuven_baseline",
    "GSE16879_all_IBD_Leuven_baseline",
}


def module_membership() -> pd.DataFrame:
    rows = []
    for module, genes in MODULES.items():
        for gene in genes:
            rows.append({"gene": gene, "module": module})
    return pd.DataFrame(rows).drop_duplicates()


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


def gene_patient_scores(gene_z: pd.DataFrame, info: pd.DataFrame, spec: CohortSpec) -> pd.DataFrame:
    scores = gene_z.T.copy()
    scores.index.name = "sample"
    return patient_level_scores(scores, info, spec)


def test_gene(df: pd.DataFrame, gene: str, spec: CohortSpec) -> dict[str, Any]:
    if gene not in df.columns:
        return {}
    base = df[["patient_id", "response", "disease", "tissue", gene]].copy()
    base[gene] = pd.to_numeric(base[gene], errors="coerce")
    base = base[np.isfinite(base[gene]) & base["response"].isin([0, 1])].copy()
    if len(base) < 6 or base["response"].nunique() < 2:
        return {}
    score = base[gene].to_numpy(float)
    if spec.adjustment_covariates:
        score = residualize(score, base, list(spec.adjustment_covariates))
    y = base["response"].astype(int).to_numpy()
    responders = score[y == 1]
    nonresponders = score[y == 0]
    if len(responders) >= 3 and len(nonresponders) >= 3:
        t_stat, p_value = stats.ttest_ind(responders, nonresponders, equal_var=False, nan_policy="omit")
    else:
        t_stat, p_value = np.nan, np.nan
    effect = float(np.nanmean(responders) - np.nanmean(nonresponders))
    auc_response = auc_score(y, score)
    return {
        "cohort": spec.cohort,
        "series": spec.series,
        "overlap_group": spec.overlap_group,
        "primary_independent_context": bool(spec.cohort in PRIMARY_CONTEXTS),
        "overlap_control_context": bool(spec.cohort in OVERLAP_CONTROL_CONTEXTS),
        "disease_scope": spec.disease_scope,
        "tissue_scope": spec.tissue_scope,
        "gene": gene,
        "n_patients": int(len(base)),
        "n_responders": int(y.sum()),
        "n_nonresponders": int((1 - y).sum()),
        "adjustment_covariates": ";".join(spec.adjustment_covariates),
        "effect_responder_minus_non": effect,
        "hedges_g_responder_minus_non": hedges_g(responders, nonresponders),
        "auc_high_score_response": auc_response,
        "auc_high_score_nonresponse": float(1.0 - auc_response) if np.isfinite(auc_response) else np.nan,
        "t": float(t_stat) if np.isfinite(t_stat) else np.nan,
        "p": float(p_value) if np.isfinite(p_value) else 1.0,
        "nonresponse_high_direction": bool(effect < 0),
    }


def summarize_gene_meta(tests: pd.DataFrame, membership: pd.DataFrame) -> pd.DataFrame:
    module_map = membership.groupby("gene")["module"].apply(lambda s: ";".join(sorted(set(s)))).to_dict()
    rows = []
    primary = tests[tests["primary_independent_context"]].copy()
    for gene, group in primary.groupby("gene"):
        g = group.copy()
        g = g[np.isfinite(g["hedges_g_responder_minus_non"])].copy()
        if g.empty:
            continue
        weights = g["n_patients"].astype(float).clip(lower=1.0)
        weighted_g = float(np.average(g["hedges_g_responder_minus_non"], weights=weights))
        nonresponse_contexts = int((g["effect_responder_minus_non"] < 0).sum())
        nominal_contexts = int(((g["effect_responder_minus_non"] < 0) & (g["p"] < 0.05)).sum())
        fdr_contexts = int(((g["effect_responder_minus_non"] < 0) & (g["fdr_within_cohort"] < 0.10)).sum())
        rows.append(
            {
                "gene": gene,
                "modules": module_map.get(gene, ""),
                "n_primary_contexts": int(len(g)),
                "n_primary_overlap_groups": int(g["overlap_group"].nunique()),
                "nonresponse_high_contexts": nonresponse_contexts,
                "responder_high_contexts": int((g["effect_responder_minus_non"] > 0).sum()),
                "nominal_nonresponse_contexts_p_lt_0_05": nominal_contexts,
                "fdr10_nonresponse_contexts": fdr_contexts,
                "weighted_mean_hedges_g_responder_minus_non": weighted_g,
                "median_auc_high_score_nonresponse": float(g["auc_high_score_nonresponse"].median()),
                "min_p": float(g["p"].min()),
                "best_context": str(g.sort_values("p").iloc[0]["cohort"]),
                "best_context_p": float(g["p"].min()),
                "best_context_effect": float(g.sort_values("p").iloc[0]["effect_responder_minus_non"]),
            }
        )
    out = pd.DataFrame(rows)
    if out.empty:
        return out
    out["meta_rank_score"] = (
        out["nonresponse_high_contexts"] * 3.0
        + out["nominal_nonresponse_contexts_p_lt_0_05"] * 2.0
        + out["fdr10_nonresponse_contexts"] * 1.5
        + (-out["weighted_mean_hedges_g_responder_minus_non"]).clip(lower=0.0)
        + (out["median_auc_high_score_nonresponse"] - 0.5).clip(lower=0.0)
        - out["responder_high_contexts"] * 2.0
    )
    out["call"] = np.where(
        (out["nonresponse_high_contexts"] >= 4)
        & (out["nominal_nonresponse_contexts_p_lt_0_05"] >= 2)
        & (out["weighted_mean_hedges_g_responder_minus_non"] < -0.5),
        "GENE_LEVEL_ANTITNF_NONRESPONSE_ANCHOR",
        np.where(
            (out["nonresponse_high_contexts"] >= 3)
            & (out["nominal_nonresponse_contexts_p_lt_0_05"] >= 1)
            & (out["weighted_mean_hedges_g_responder_minus_non"] < -0.25),
            "PARK_DIRECTIONAL_NONRESPONSE_GENE",
            "NO_GENE_LEVEL_CONVERGENCE",
        ),
    )
    return out.sort_values(
        [
            "call",
            "meta_rank_score",
            "nonresponse_high_contexts",
            "nominal_nonresponse_contexts_p_lt_0_05",
            "weighted_mean_hedges_g_responder_minus_non",
        ],
        ascending=[True, False, False, False, True],
    )


def analyze_gene_drivers() -> dict[str, Any]:
    OUT.mkdir(parents=True, exist_ok=True)
    wanted_genes = sorted({gene for genes in MODULES.values() for gene in genes})
    probe_to_genes, _ = read_gpl570_gene_map(GPL570_ANNOT, set(wanted_genes))
    membership = module_membership()

    all_patient_scores: list[pd.DataFrame] = []
    all_tests: list[dict[str, Any]] = []
    coverage_rows = []

    for series, path in SERIES_FILES.items():
        metadata, expr_probe = read_series_matrix(path)
        info = sample_metadata(series, metadata)
        gene_expr = expression_to_gene_level(expr_probe, probe_to_genes)

        for spec in cohort_specs(series, info):
            mask = mask_for_spec(info, spec)
            selected = info.loc[mask].copy()
            samples = [sample for sample in selected["sample"] if sample in gene_expr.columns]
            if len(samples) < 6:
                continue
            gene_z = zscore_rows(gene_expr[samples])
            present = [gene for gene in wanted_genes if gene in gene_z.index]
            missing = [gene for gene in wanted_genes if gene not in gene_z.index]
            coverage_rows.append(
                {
                    "cohort": spec.cohort,
                    "series": series,
                    "n_defined_genes": len(wanted_genes),
                    "n_present_genes": len(present),
                    "genes_present": ";".join(present),
                    "genes_missing": ";".join(missing),
                }
            )
            patients = gene_patient_scores(gene_z.loc[present], selected, spec)
            all_patient_scores.append(patients)
            for gene in present:
                row = test_gene(patients, gene, spec)
                if row:
                    all_tests.append(row)

    patient_scores = pd.concat(all_patient_scores, ignore_index=True) if all_patient_scores else pd.DataFrame()
    tests = pd.DataFrame(all_tests)
    if not tests.empty:
        tests["fdr_all_tests"] = bh(tests["p"])
        tests["fdr_within_cohort"] = tests.groupby("cohort")["p"].transform(lambda s: bh(s))
        tests = tests.merge(membership.groupby("gene")["module"].apply(lambda s: ";".join(sorted(set(s)))).rename("modules"), on="gene", how="left")
    meta = summarize_gene_meta(tests, membership) if not tests.empty else pd.DataFrame()

    patient_scores.to_csv(OUT / "external_geo_gene_patient_scores.tsv", sep="\t", index=False)
    tests.to_csv(OUT / "external_geo_gene_response_tests.tsv", sep="\t", index=False)
    pd.DataFrame(coverage_rows).to_csv(OUT / "external_geo_gene_coverage.tsv", sep="\t", index=False)
    membership.to_csv(OUT / "module_gene_membership.tsv", sep="\t", index=False)
    meta.to_csv(OUT / "external_geo_gene_meta_rank.tsv", sep="\t", index=False)

    call_counts = meta["call"].value_counts().to_dict() if not meta.empty else {}
    top = meta.head(20).copy()
    top_gene = str(top.iloc[0]["gene"]) if not top.empty else ""
    summary = {
        "seed": SEED,
        "call_counts": {str(k): int(v) for k, v in call_counts.items()},
        "top_gene": top_gene,
        "n_genes_tested": int(meta.shape[0]) if not meta.empty else 0,
        "primary_contexts": sorted(PRIMARY_CONTEXTS),
        "overlap_control_contexts": sorted(OVERLAP_CONTROL_CONTEXTS),
        "wave85_inputs_reused": {
            "raw_dir": rel(RAW),
            "gpl570_annotation": rel(GPL570_ANNOT),
            "wave85_output": rel(W85_OUT),
        },
    }
    write_json(OUT / "summary.json", summary)

    top_tests = tests[tests["gene"].isin(top["gene"].head(10).tolist()) & tests["primary_independent_context"]].copy() if not tests.empty and not top.empty else pd.DataFrame()
    report = [
        "# Wave86 External GEO Anti-TNF Gene Driver Decomposition",
        "",
        "Question: which gene-level component of the Wave85 generic inflammatory/IFN-high nonresponse signal is most stable across independent anti-TNF mucosal contexts?",
        "",
        "Primary independent contexts counted in the rank: ACT1 UC (`GSE12251`), Leuven UC (`GSE14580`), Leuven Crohn colitis (`GSE16879`), and Leuven Crohn ileitis (`GSE16879`). The duplicate UC representation inside `GSE16879` and the combined GSE16879 summaries are retained only as overlap/sensitivity outputs.",
        "",
        "## Gene Meta Rank",
        "",
        markdown_table(top, max_rows=30),
        "",
        "## Primary Context Tests For Top Genes",
        "",
        markdown_table(
            top_tests[
                [
                    "cohort",
                    "gene",
                    "modules",
                    "n_patients",
                    "effect_responder_minus_non",
                    "hedges_g_responder_minus_non",
                    "auc_high_score_nonresponse",
                    "p",
                    "fdr_within_cohort",
                ]
            ].sort_values(["gene", "cohort"]) if not top_tests.empty else top_tests,
            max_rows=80,
        ),
        "",
        "## Interpretation Guardrail",
        "",
        "This is a gene-level decomposition of bulk mucosal response data. It can nominate resistance-associated genes for prior-art and cell-state follow-up, but it does not prove that inhibiting or activating any gene would improve anti-TNF response.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    return summary


def main() -> None:
    analyze_gene_drivers()


if __name__ == "__main__":
    main()
