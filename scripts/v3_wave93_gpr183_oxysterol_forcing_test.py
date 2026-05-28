#!/usr/bin/env python3
"""Wave93 GPR183/EBI2 oxysterol-niche forcing test.

After FABP5 failed on direct MS/EAE prior art, the V3 session pivoted from
module-internal lipid genes to upstream state-transition controllers. Wave74
parked GPR183/EBI2 because response signals existed but the local receptor,
ligand-production enzymes, and MS anchor did not cohere. This script forces the
question with target-level response tests and fresh druggability/prior-art
queries.

This is intentionally a hard-gate audit. A druggable GPCR cannot be promoted if
the MS anchor and local ligand/receptor coherence remain absent.
"""

from __future__ import annotations

import csv
import gzip
import io
import json
import math
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy import stats

from v3_analyze_direct_h5ad_cell_states import ROOT
from v3_wave85_external_geo_antitnf_validation import (
    GPL570_ANNOT,
    RAW as W85_RAW,
    SERIES_FILES,
    bh,
    cohort_specs,
    expression_to_gene_level as gpl570_expression_to_gene_level,
    hedges_g,
    markdown_table,
    mask_for_spec,
    patient_level_scores,
    read_gpl570_gene_map,
    read_series_matrix as read_gpl570_series_matrix,
    rel,
    residualize,
    sample_metadata as gpl570_sample_metadata,
    write_json,
    zscore_rows,
)
from v3_wave89_psoriasis_gse85034_response_validation import (
    GPL10558_ANNOT,
    SERIES as GSE85034_SERIES,
    build_patient_response_table,
    expression_to_gene_level as gpl10558_expression_to_gene_level,
    read_gpl10558_gene_map,
    read_series_matrix as read_gse85034_series_matrix,
    sample_metadata as gse85034_sample_metadata,
    test_feature as test_psoriasis_feature,
)


SEED = 20260527
OUT = ROOT / "results_v3" / "wave93_gpr183_oxysterol_forcing_test"

TARGET_GENES = ["GPR183", "CH25H", "CYP7B1", "HSD3B7", "CYP27A1"]
RESPONSE_GENES = ["CCR7", "CCL19", "CCL21", "CXCL13", "CXCR5", "LTA", "LTB", "CD83", "LAMP3", "ITGAX", "CCL17", "CCL22"]
ALL_GENES = sorted(set(TARGET_GENES + RESPONSE_GENES))

W74 = ROOT / "results_v3" / "wave74_gpr183_oxysterol_niche"
W83 = ROOT / "results_v3" / "wave83_intervention_class_meta_rank" / "intervention_class_meta_rank.tsv"
MS_SIG = ROOT / "results_v3" / "gse111972_full_ms_wm_signature.tsv"
BROAD = ROOT / "results_v3" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_contrasts.tsv"
W55 = ROOT / "results_v3" / "wave55_external_genetics_druggability_sweep" / "external_genetics_rank.tsv"
W62 = ROOT / "results_v3" / "wave62_opentargets_target_resolution" / "target_resolution_summary.tsv"
RA_COUNTS = ROOT / "results_v3" / "wave65_gse198520_ra_synovium_antitnf_audit" / "gse198520_counts_used.tsv"
RA_META = ROOT / "results_v3" / "wave65_gse198520_ra_synovium_antitnf_audit" / "gse198520_sample_metadata.tsv"

PRIMARY_IBD_CONTEXTS = {
    "GSE12251_UC_ACT1_baseline",
    "GSE14580_UC_Leuven_baseline",
    "GSE16879_Crohn_colitis_Leuven_baseline",
    "GSE16879_Crohn_ileitis_Leuven_baseline",
}

PUBMED_QUERIES = [
    'GPR183 multiple sclerosis',
    'EBI2 experimental autoimmune encephalomyelitis',
    'GPR183 experimental autoimmune encephalomyelitis',
    'GPR183 inflammatory bowel disease',
    'GPR183 colitis',
    'GPR183 rheumatoid arthritis',
    'GPR183 psoriasis',
    'GPR183 autoimmune',
    'CH25H CYP7B1 GPR183 autoimmune',
    '"7alpha,25-dihydroxycholesterol" autoimmune',
]

CLINICALTRIALS_QUERIES = [
    "GPR183",
    "EBI2 receptor",
    "GPR183 antagonist autoimmune",
    "oxysterol receptor autoimmune",
]

PATENT_QUERIES = [
    "GPR183 autoimmune antagonist",
    "EBI2 autoimmune antagonist",
    "GPR183 multiple sclerosis",
    "7alpha 25 dihydroxycholesterol autoimmune",
]


def read_tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


def f(value: Any) -> float:
    try:
        out = float(value)
    except (TypeError, ValueError):
        return math.nan
    return out


def s(value: Any) -> str:
    if value is None or pd.isna(value):
        return ""
    return str(value)


def finite(value: Any) -> bool:
    return math.isfinite(f(value))


def auc_score(y: np.ndarray, score: np.ndarray) -> float:
    y = np.asarray(y, dtype=int)
    score = np.asarray(score, dtype=float)
    pos = score[y == 1]
    neg = score[y == 0]
    if len(pos) == 0 or len(neg) == 0:
        return math.nan
    wins = 0.0
    for value in pos:
        wins += float((value > neg).sum())
        wins += 0.5 * float((value == neg).sum())
    return wins / float(len(pos) * len(neg))


def log_cpm(counts: pd.DataFrame) -> pd.DataFrame:
    mat = counts.drop(columns=["GeneSymbol"]).astype(float)
    lib = mat.sum(axis=0).replace(0, np.nan)
    out = np.log2(mat.div(lib, axis=1) * 1_000_000.0 + 1.0)
    out.insert(0, "GeneSymbol", counts["GeneSymbol"].astype(str).str.upper())
    return out


def http_json(url: str, timeout: int = 25) -> dict[str, Any]:
    req = urllib.request.Request(url, headers={"User-Agent": "ms-auto-research-wave93/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as handle:  # noqa: S310 - fixed public APIs
        return json.loads(handle.read().decode("utf-8"))


def safe_http_json(url: str, timeout: int = 25, retries: int = 2) -> tuple[dict[str, Any] | None, str]:
    last_error = ""
    for attempt in range(retries + 1):
        try:
            return http_json(url, timeout=timeout), ""
        except Exception as exc:  # network/API failures are recorded, not hidden
            last_error = f"{type(exc).__name__}: {exc}"
            time.sleep(0.5 * (attempt + 1))
    return None, last_error


def ms_gene_rows() -> pd.DataFrame:
    df = read_tsv(MS_SIG)
    if df.empty:
        return pd.DataFrame()
    df["gene"] = df["gene"].astype(str).str.upper()
    out = df[df["gene"].isin(TARGET_GENES)].copy()
    out["ms_anchor_call"] = np.where(
        (pd.to_numeric(out["delta_log2"], errors="coerce") > 0.0) & (pd.to_numeric(out["p"], errors="coerce") < 0.10),
        "MS_WM_UP_NOMINAL_OR_TREND",
        np.where(pd.to_numeric(out["delta_log2"], errors="coerce") < 0.0, "MS_WM_NOT_UP_NEGATIVE_DIRECTION", "NO_MS_WM_UP_SIGNAL"),
    )
    return out.sort_values("gene")


def broad_target_rows() -> tuple[pd.DataFrame, pd.DataFrame]:
    df = read_tsv(BROAD)
    if df.empty:
        return pd.DataFrame(), pd.DataFrame()
    df["gene"] = df["gene"].astype(str).str.upper()
    rows = df[df["gene"].isin(TARGET_GENES)].copy()
    rows["target_positive_trend"] = (pd.to_numeric(rows["delta_log2_cpm"], errors="coerce") > 0.30) & (
        pd.to_numeric(rows["p"], errors="coerce") < 0.10
    )
    rows["target_negative_trend"] = (pd.to_numeric(rows["delta_log2_cpm"], errors="coerce") < -0.30) & (
        pd.to_numeric(rows["p"], errors="coerce") < 0.10
    )
    summary_rows: list[dict[str, Any]] = []
    for gene, sub in rows.groupby("gene", dropna=False):
        pos = sub[sub["target_positive_trend"]]
        neg = sub[sub["target_negative_trend"]]
        summary_rows.append(
            {
                "gene": gene,
                "tested_contexts": int(len(sub)),
                "positive_contexts_p_lt_0_10": int(len(pos)),
                "negative_contexts_p_lt_0_10": int(len(neg)),
                "positive_disease_count": int(pos["disease_name"].nunique()) if not pos.empty else 0,
                "negative_disease_count": int(neg["disease_name"].nunique()) if not neg.empty else 0,
                "positive_diseases": ";".join(sorted(map(str, pos["disease_name"].dropna().unique()))) if not pos.empty else "",
                "negative_diseases": ";".join(sorted(map(str, neg["disease_name"].dropna().unique()))) if not neg.empty else "",
                "best_positive_context": (
                    pos.sort_values(["delta_log2_cpm", "p"], ascending=[False, True])
                    .head(1)
                    .apply(lambda r: f"{r['analysis']}|{r['disease_name']}|{r['compartment']}|delta={r['delta_log2_cpm']:.3g}|p={r['p']:.3g}", axis=1)
                    .iloc[0]
                    if not pos.empty
                    else ""
                ),
                "best_negative_context": (
                    neg.sort_values(["delta_log2_cpm", "p"], ascending=[True, True])
                    .head(1)
                    .apply(lambda r: f"{r['analysis']}|{r['disease_name']}|{r['compartment']}|delta={r['delta_log2_cpm']:.3g}|p={r['p']:.3g}", axis=1)
                    .iloc[0]
                    if not neg.empty
                    else ""
                ),
            }
        )
    return rows.sort_values(["gene", "p"]), pd.DataFrame(summary_rows).sort_values("gene")


def wave74_context() -> dict[str, pd.DataFrame]:
    names = {
        "integrated_decision": "integrated_decision.tsv",
        "coherence": "broad_h5ad_context_coherence.tsv",
        "ms_modules": "ms_gse111972_module_tests.tsv",
        "broad_summary": "broad_h5ad_module_summary.tsv",
        "gse282122": "gse282122_module_response_tests.tsv",
        "ra_modules": "ra_gse198520_module_tests.tsv",
        "external_target": "external_target_evidence.tsv",
    }
    return {key: read_tsv(W74 / file_name) for key, file_name in names.items()}


def test_ibd_gene(df: pd.DataFrame, gene: str, spec: Any) -> dict[str, Any]:
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
    t_stat, p_value = (
        stats.ttest_ind(responders, nonresponders, equal_var=False, nan_policy="omit")
        if len(responders) >= 3 and len(nonresponders) >= 3
        else (math.nan, math.nan)
    )
    effect = float(np.nanmean(responders) - np.nanmean(nonresponders))
    auc_response = auc_score(y, score)
    return {
        "cohort": spec.cohort,
        "series": spec.series,
        "primary_independent_context": bool(spec.cohort in PRIMARY_IBD_CONTEXTS),
        "disease_scope": spec.disease_scope,
        "tissue_scope": spec.tissue_scope,
        "gene": gene,
        "n_patients": int(len(base)),
        "n_responders": int(y.sum()),
        "n_nonresponders": int((1 - y).sum()),
        "effect_responder_minus_non": effect,
        "hedges_g_responder_minus_non": hedges_g(responders, nonresponders),
        "auc_high_expression_nonresponse": float(1.0 - auc_response) if np.isfinite(auc_response) else math.nan,
        "p": float(p_value) if np.isfinite(p_value) else 1.0,
        "nonresponse_high_direction": bool(effect < 0),
    }


def ibd_external_antitnf_tests() -> tuple[pd.DataFrame, pd.DataFrame]:
    probe_to_genes, coverage = read_gpl570_gene_map(GPL570_ANNOT, set(ALL_GENES))
    tests: list[dict[str, Any]] = []
    for series, path in SERIES_FILES.items():
        metadata, expr_probe = read_gpl570_series_matrix(path)
        info = gpl570_sample_metadata(series, metadata)
        gene_expr = gpl570_expression_to_gene_level(expr_probe, probe_to_genes)
        for spec in cohort_specs(series, info):
            selected = info.loc[mask_for_spec(info, spec)].copy()
            samples = [sample for sample in selected["sample"] if sample in gene_expr.columns]
            if len(samples) < 6:
                continue
            gene_z = zscore_rows(gene_expr[samples])
            present = [gene for gene in ALL_GENES if gene in gene_z.index]
            if not present:
                continue
            score_df = gene_z.loc[present].T.copy()
            score_df.index.name = "sample"
            patients = patient_level_scores(score_df, selected, spec)
            for gene in present:
                row = test_ibd_gene(patients, gene, spec)
                if row:
                    tests.append(row)
    out = pd.DataFrame(tests)
    if not out.empty:
        out["fdr_all"] = bh(out["p"].astype(float).to_numpy())
        out["fdr_within_cohort"] = out.groupby("cohort")["p"].transform(lambda vals: bh(vals.astype(float).to_numpy()))
        out["support_call"] = np.where(
            out["nonresponse_high_direction"] & (pd.to_numeric(out["p"], errors="coerce") < 0.10),
            "NONRESPONSE_HIGH_TREND",
            np.where(out["nonresponse_high_direction"], "NONRESPONSE_HIGH_WEAK", "RESPONDER_HIGH_OR_NULL"),
        )
        out = out.sort_values(["gene", "primary_independent_context", "p"], ascending=[True, False, True])
    return out, coverage


def summarize_response_meta(tests: pd.DataFrame, system: str) -> pd.DataFrame:
    if tests.empty:
        return pd.DataFrame()
    rows: list[dict[str, Any]] = []
    work = tests.copy()
    if "primary_independent_context" in work.columns:
        work = work[work["primary_independent_context"]].copy()
    for gene, sub in work.groupby("gene", dropna=False):
        clean = sub[np.isfinite(pd.to_numeric(sub["hedges_g_responder_minus_non"], errors="coerce"))].copy()
        if clean.empty:
            continue
        weights = pd.to_numeric(clean.get("n_patients", pd.Series(1, index=clean.index)), errors="coerce").fillna(1).clip(lower=1)
        rows.append(
            {
                "system": system,
                "gene": gene,
                "n_contexts": int(len(clean)),
                "nonresponse_high_contexts": int((pd.to_numeric(clean["effect_responder_minus_non"], errors="coerce") < 0).sum()),
                "responder_high_contexts": int((pd.to_numeric(clean["effect_responder_minus_non"], errors="coerce") > 0).sum()),
                "nominal_nonresponse_contexts_p_lt_0_10": int(
                    (
                        (pd.to_numeric(clean["effect_responder_minus_non"], errors="coerce") < 0)
                        & (pd.to_numeric(clean["p"], errors="coerce") < 0.10)
                    ).sum()
                ),
                "weighted_mean_hedges_g_responder_minus_non": float(
                    np.average(pd.to_numeric(clean["hedges_g_responder_minus_non"], errors="coerce"), weights=weights)
                ),
                "median_auc_high_expression_nonresponse": float(pd.to_numeric(clean["auc_high_expression_nonresponse"], errors="coerce").median())
                if "auc_high_expression_nonresponse" in clean.columns
                else math.nan,
                "min_p": float(pd.to_numeric(clean["p"], errors="coerce").min()),
            }
        )
    return pd.DataFrame(rows).sort_values(["system", "gene"])


def ra_baseline_response_tests() -> pd.DataFrame:
    counts = read_tsv(RA_COUNTS)
    meta = read_tsv(RA_META)
    if counts.empty or meta.empty:
        return pd.DataFrame()
    counts["GeneSymbol"] = counts["GeneSymbol"].astype(str).str.upper()
    expr = log_cpm(counts)
    sample_cols = [col for col in expr.columns if col != "GeneSymbol"]
    mat = expr.set_index("GeneSymbol")[sample_cols]
    gene_z = zscore_rows(mat)
    pre = meta[meta["timepoint"].astype(str).str.lower().eq("pre")].copy()
    pre = pre[pre["count_column"].isin(gene_z.columns)].copy()
    pre["response"] = pre["responder_moderate_or_good"].astype(str).str.lower().isin(["true", "1", "yes"]).astype(int)
    rows: list[dict[str, Any]] = []
    for gene in ALL_GENES:
        if gene not in gene_z.index:
            continue
        base = pre.copy()
        base["_score"] = pd.to_numeric(gene_z.loc[gene, base["count_column"].tolist()].to_numpy(), errors="coerce")
        base = base[np.isfinite(base["_score"]) & base["response"].isin([0, 1])].copy()
        if len(base) < 8 or base["response"].nunique() < 2:
            continue
        adjusted = residualize(base["_score"].to_numpy(float), base, ["pathotype", "biologic", "inflammatory_score", "das28_score"])
        y = base["response"].astype(int).to_numpy()
        responders = adjusted[y == 1]
        nonresponders = adjusted[y == 0]
        t_stat, p_value = stats.ttest_ind(responders, nonresponders, equal_var=False, nan_policy="omit")
        effect = float(np.nanmean(responders) - np.nanmean(nonresponders))
        auc_response = auc_score(y, adjusted)
        rows.append(
            {
                "system": "RA_GSE198520_baseline_synovium",
                "dataset": "GSE198520",
                "disease": "rheumatoid arthritis",
                "tissue": "synovium",
                "gene": gene,
                "n_patients": int(len(base)),
                "n_responders": int(y.sum()),
                "n_nonresponders": int((1 - y).sum()),
                "effect_responder_minus_non": effect,
                "hedges_g_responder_minus_non": hedges_g(responders, nonresponders),
                "auc_high_expression_nonresponse": float(1.0 - auc_response) if np.isfinite(auc_response) else math.nan,
                "p": float(p_value) if np.isfinite(p_value) else 1.0,
                "nonresponse_high_direction": bool(effect < 0),
            }
        )
    out = pd.DataFrame(rows)
    if not out.empty:
        out["fdr"] = bh(out["p"].astype(float).to_numpy())
        out["support_call"] = np.where(
            out["nonresponse_high_direction"] & (pd.to_numeric(out["p"], errors="coerce") < 0.10),
            "NONRESPONSE_HIGH_TREND",
            np.where(out["nonresponse_high_direction"], "NONRESPONSE_HIGH_WEAK", "RESPONDER_HIGH_OR_NULL"),
        )
        out = out.sort_values(["gene", "p"])
    return out


def psoriasis_baseline_response_tests() -> pd.DataFrame:
    if not GSE85034_SERIES.exists() or not GPL10558_ANNOT.exists():
        return pd.DataFrame()
    metadata, expr_probe = read_gse85034_series_matrix(GSE85034_SERIES)
    info = gse85034_sample_metadata(metadata)
    patients = build_patient_response_table(info)
    probe_to_genes, _coverage = read_gpl10558_gene_map(GPL10558_ANNOT, set(ALL_GENES))
    gene_expr = gpl10558_expression_to_gene_level(expr_probe, probe_to_genes)
    if gene_expr.empty:
        return pd.DataFrame()
    gene_z = zscore_rows(gene_expr)
    patient_gene = gene_z.T.copy()
    patient_gene.index.name = "sample"
    rows: list[dict[str, Any]] = []
    for treatment in ["ADA", "MTX", "ALL"]:
        for gene in sorted(set(ALL_GENES) & set(patient_gene.columns)):
            row = test_psoriasis_feature(patient_gene, patients, gene, treatment, "gene")
            if row:
                row["system"] = "psoriasis_GSE85034_baseline_skin"
                rows.append(row)
    out = pd.DataFrame(rows)
    if not out.empty:
        out = out.rename(columns={"feature": "gene", "auc_high_score_nonresponse": "auc_high_expression_nonresponse"})
        out["support_call"] = np.where(
            out["nonresponse_high_direction"] & (pd.to_numeric(out["p"], errors="coerce") < 0.10),
            "NONRESPONSE_HIGH_TREND",
            np.where(out["nonresponse_high_direction"], "NONRESPONSE_HIGH_WEAK", "RESPONDER_HIGH_OR_NULL"),
        )
        out["fdr_within_treatment"] = np.nan
        for treatment, idx in out.groupby("treatment").groups.items():
            out.loc[idx, "fdr_within_treatment"] = bh(out.loc[idx, "p"].astype(float).to_numpy())
        out = out.sort_values(["treatment", "gene", "p"])
    return out


def target_resolution_rows() -> pd.DataFrame:
    rows: list[pd.DataFrame] = []
    for label, path in [("wave55_external_genetics", W55), ("wave62_target_resolution", W62)]:
        df = read_tsv(path)
        if df.empty or "gene" not in df.columns:
            continue
        df["gene"] = df["gene"].astype(str).str.upper()
        keep = df[df["gene"].isin(TARGET_GENES)].copy()
        keep.insert(0, "source", label)
        rows.append(keep)
    return pd.concat(rows, ignore_index=True, sort=False) if rows else pd.DataFrame()


def chembl_target_query() -> tuple[pd.DataFrame, pd.DataFrame]:
    target_rows: list[dict[str, Any]] = []
    activity_rows: list[dict[str, Any]] = []
    for gene in TARGET_GENES:
        url = "https://www.ebi.ac.uk/chembl/api/data/target/search.json?" + urllib.parse.urlencode({"q": gene, "limit": 10})
        payload, error = safe_http_json(url)
        targets = (payload or {}).get("targets", []) if payload else []
        if not targets:
            target_rows.append({"gene": gene, "query_url": url, "chembl_query_error": error, "chembl_hit_count": 0})
            continue
        for target in targets[:5]:
            tid = target.get("target_chembl_id", "")
            pref = target.get("pref_name", "")
            target_type = target.get("target_type", "")
            organism = target.get("organism", "")
            is_human_exact = bool(organism == "Homo sapiens" and (gene.upper() in json.dumps(target).upper()))
            activity_url = (
                "https://www.ebi.ac.uk/chembl/api/data/activity.json?"
                + urllib.parse.urlencode({"target_chembl_id": tid, "standard_type__in": "IC50,Ki,Kd,EC50", "limit": 1})
            )
            act_payload, act_error = safe_http_json(activity_url)
            total = ((act_payload or {}).get("page_meta") or {}).get("total_count", 0) if act_payload else 0
            target_rows.append(
                {
                    "gene": gene,
                    "query_url": url,
                    "target_chembl_id": tid,
                    "pref_name": pref,
                    "target_type": target_type,
                    "organism": organism,
                    "is_human_exact_like_hit": is_human_exact,
                    "activity_query_url": activity_url,
                    "activity_count_reported": total,
                    "chembl_query_error": error,
                    "activity_query_error": act_error,
                    "chembl_hit_count": len(targets),
                }
            )
            if act_payload:
                for act in act_payload.get("activities", [])[:1]:
                    activity_rows.append({"gene": gene, "target_chembl_id": tid, **act})
    return pd.DataFrame(target_rows), pd.DataFrame(activity_rows)


def pubmed_search() -> tuple[pd.DataFrame, pd.DataFrame]:
    query_rows: list[dict[str, Any]] = []
    record_rows: list[dict[str, Any]] = []
    for query in PUBMED_QUERIES:
        params = urllib.parse.urlencode({"db": "pubmed", "term": query, "retmode": "json", "retmax": 20, "sort": "relevance"})
        url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?{params}"
        payload, error = safe_http_json(url)
        ids = ((payload or {}).get("esearchresult") or {}).get("idlist", []) if payload else []
        query_rows.append({"query": query, "url": url, "n_ids_returned": len(ids), "ids": ";".join(ids), "error": error})
        if not ids:
            continue
        summary_url = (
            "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?"
            + urllib.parse.urlencode({"db": "pubmed", "id": ",".join(ids), "retmode": "json"})
        )
        summary, sum_error = safe_http_json(summary_url)
        result = (summary or {}).get("result", {}) if summary else {}
        for pmid in ids:
            rec = result.get(pmid, {})
            title = s(rec.get("title"))
            journal = s(rec.get("fulljournalname")) or s(rec.get("source"))
            pubdate = s(rec.get("pubdate"))
            doi = ""
            for article_id in rec.get("articleids", []) if isinstance(rec.get("articleids"), list) else []:
                if article_id.get("idtype") == "doi":
                    doi = article_id.get("value", "")
                    break
            text = f"{title} {journal}".lower()
            direct_ms_eae = bool(("multiple sclerosis" in text or "encephalomyelitis" in text) and ("gpr183" in query.lower() or "ebi2" in query.lower()))
            autoimmune_route = bool(any(term in text for term in ["autoimmune", "colitis", "psoriasis", "rheumatoid", "lupus", "sjögren", "sjogren"]))
            record_rows.append(
                {
                    "query": query,
                    "pmid": pmid,
                    "title": title,
                    "journal": journal,
                    "pubdate": pubdate,
                    "doi": doi,
                    "esummary_error": sum_error,
                    "direct_ms_or_eae_gpr183_like_prior_art": direct_ms_eae,
                    "autoimmune_prior_art_like": autoimmune_route,
                }
            )
    records = pd.DataFrame(record_rows)
    if not records.empty:
        records = records.drop_duplicates("pmid").sort_values(["direct_ms_or_eae_gpr183_like_prior_art", "autoimmune_prior_art_like", "pubdate"], ascending=[False, False, False])
    return pd.DataFrame(query_rows), records


def clinicaltrials_search() -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for query in CLINICALTRIALS_QUERIES:
        url = (
            "https://clinicaltrials.gov/api/v2/studies?"
            + urllib.parse.urlencode({"query.term": query, "pageSize": 10, "format": "json"})
        )
        payload, error = safe_http_json(url)
        studies = (payload or {}).get("studies", []) if payload else []
        if not studies:
            rows.append({"query": query, "url": url, "n_records_returned": 0, "error": error})
            continue
        for study in studies:
            protocol = study.get("protocolSection", {})
            ident = protocol.get("identificationModule", {})
            status = protocol.get("statusModule", {})
            conditions = protocol.get("conditionsModule", {})
            design = protocol.get("designModule", {})
            rows.append(
                {
                    "query": query,
                    "url": url,
                    "nct_id": ident.get("nctId", ""),
                    "brief_title": ident.get("briefTitle", ""),
                    "overall_status": status.get("overallStatus", ""),
                    "conditions": ";".join(conditions.get("conditions", []) or []),
                    "phases": ";".join(design.get("phases", []) or []),
                    "n_records_returned": len(studies),
                    "error": error,
                }
            )
    return pd.DataFrame(rows)


def patent_search_urls() -> pd.DataFrame:
    rows = []
    for query in PATENT_QUERIES:
        encoded = urllib.parse.quote_plus(query)
        rows.append(
            {
                "query": query,
                "google_patents_url": f"https://patents.google.com/?q={encoded}",
                "espacenet_url": f"https://worldwide.espacenet.com/patent/search?q={encoded}",
            }
        )
    return pd.DataFrame(rows)


def integrate_decision(
    ms: pd.DataFrame,
    broad_summary: pd.DataFrame,
    w74: dict[str, pd.DataFrame],
    ibd_meta: pd.DataFrame,
    ra: pd.DataFrame,
    pso: pd.DataFrame,
    target_resolution: pd.DataFrame,
    chembl_targets: pd.DataFrame,
    pubmed_records: pd.DataFrame,
) -> pd.DataFrame:
    gpr_ms = ms[ms["gene"].eq("GPR183")] if not ms.empty else pd.DataFrame()
    ms_gpr183_positive = bool(
        not gpr_ms.empty and f(gpr_ms.iloc[0].get("delta_log2")) > 0 and f(gpr_ms.iloc[0].get("p")) < 0.10
    )
    ligand_ms = w74.get("ms_modules", pd.DataFrame())
    ligand_row = ligand_ms[ligand_ms["module"].eq("ligand_production_core")] if not ligand_ms.empty else pd.DataFrame()
    ligand_ms_positive = bool(
        not ligand_row.empty and f(ligand_row.iloc[0].get("mean_effect")) >= 0.30 and f(ligand_row.iloc[0].get("combined_p")) <= 0.10
    )
    coherence = w74.get("coherence", pd.DataFrame())
    coherent_context_count = int(coherence["coherent_program_pass"].astype(bool).sum()) if not coherence.empty else 0
    coherent_disease_count = int(coherence.loc[coherence["coherent_program_pass"].astype(bool), "disease_name"].nunique()) if coherent_context_count else 0

    target_res = target_resolution[target_resolution["gene"].eq("GPR183")] if not target_resolution.empty else pd.DataFrame()
    max_genetic_diseases = 0
    for col in ["n_diseases_genetic_ge_0_25", "strong_l2g_disease_count", "wave62_strong_l2g_disease_count"]:
        if col in target_res.columns:
            max_genetic_diseases = max(max_genetic_diseases, int(pd.to_numeric(target_res[col], errors="coerce").fillna(0).max()))

    def gene_response_support(meta: pd.DataFrame, system: str) -> dict[str, Any]:
        sub = meta[(meta["system"].eq(system)) & (meta["gene"].eq("GPR183"))] if not meta.empty and "system" in meta.columns else pd.DataFrame()
        if sub.empty:
            return {"support": False, "direction": "", "p": math.nan, "g": math.nan}
        r = sub.iloc[0]
        support = bool(int(r.get("nonresponse_high_contexts", 0)) > int(r.get("responder_high_contexts", 0)) and f(r.get("min_p")) < 0.20)
        return {
            "support": support,
            "direction": "nonresponse_high" if f(r.get("weighted_mean_hedges_g_responder_minus_non")) < 0 else "responder_high_or_null",
            "p": f(r.get("min_p")),
            "g": f(r.get("weighted_mean_hedges_g_responder_minus_non")),
        }

    ibd_g = gene_response_support(ibd_meta, "IBD_external_antitnf")
    ra_g = gene_response_support(summarize_response_meta(ra.assign(system="RA_baseline") if not ra.empty else ra, "RA_baseline"), "RA_baseline")
    pso_ada = pso[(pso["gene"].eq("GPR183")) & (pso["treatment"].eq("ADA"))] if not pso.empty else pd.DataFrame()
    pso_support = bool(
        not pso_ada.empty
        and bool(pso_ada.iloc[0].get("nonresponse_high_direction"))
        and f(pso_ada.iloc[0].get("p")) < 0.20
    )
    response_support_systems = int(ibd_g["support"]) + int(ra_g["support"]) + int(pso_support)

    chembl_human_activity = False
    if not chembl_targets.empty and {"gene", "is_human_exact_like_hit", "activity_count_reported"}.issubset(chembl_targets.columns):
        cg = chembl_targets[(chembl_targets["gene"].eq("GPR183")) & (chembl_targets["is_human_exact_like_hit"].astype(bool))]
        chembl_human_activity = bool((pd.to_numeric(cg["activity_count_reported"], errors="coerce").fillna(0) > 0).any())
    direct_prior = False
    prior_hits = ""
    if not pubmed_records.empty:
        blockers = pubmed_records[pubmed_records["direct_ms_or_eae_gpr183_like_prior_art"].astype(bool)]
        direct_prior = bool(not blockers.empty)
        prior_hits = ";".join(blockers["pmid"].astype(str).head(5).tolist())

    gate_rows = [
        {"gate": "MS_GPR183_receptor_anchor_positive", "pass": ms_gpr183_positive, "value": s(gpr_ms.iloc[0].get("delta_log2")) if not gpr_ms.empty else ""},
        {"gate": "MS_ligand_module_positive", "pass": ligand_ms_positive, "value": s(ligand_row.iloc[0].get("mean_effect")) if not ligand_row.empty else ""},
        {"gate": "cross_disease_coherent_ligand_receptor_response_contexts_ge3", "pass": coherent_disease_count >= 3, "value": coherent_disease_count},
        {"gate": "target_resolved_genetics_ge4_autoimmune_diseases", "pass": max_genetic_diseases >= 4, "value": max_genetic_diseases},
        {"gate": "gene_level_response_support_ge2_systems", "pass": response_support_systems >= 2, "value": response_support_systems},
        {"gate": "chembl_human_target_activity_present", "pass": chembl_human_activity, "value": chembl_human_activity},
        {"gate": "no_direct_ms_or_eae_prior_art", "pass": not direct_prior, "value": prior_hits},
    ]
    gates = pd.DataFrame(gate_rows)
    gate_count = int(gates["pass"].sum())
    hard_failures = ";".join(gates.loc[~gates["pass"], "gate"].tolist())
    if not ms_gpr183_positive and not ligand_ms_positive:
        call = "NO_GO_GPR183_NO_MS_RECEPTOR_OR_LIGAND_ANCHOR"
    elif coherent_disease_count < 3:
        call = "NO_GO_GPR183_NO_COHERENT_CROSS_DISEASE_NICHE"
    elif direct_prior:
        call = "NO_GO_GPR183_DIRECT_MS_EAE_PRIOR_ART"
    elif gate_count >= 6:
        call = "REOPEN_GPR183_FOR_DEEP_VALIDATION"
    else:
        call = "PARK_GPR183_INSUFFICIENT_FOR_V3_PROMOTION"

    decision = pd.DataFrame(
        [
            {
                "candidate": "GPR183_EBI2_oxysterol_niche",
                "wave93_call": call,
                "gate_count": gate_count,
                "total_gates": int(len(gates)),
                "hard_failures": hard_failures,
                "ms_gpr183_positive": ms_gpr183_positive,
                "ms_ligand_module_positive": ligand_ms_positive,
                "coherent_context_count": coherent_context_count,
                "coherent_disease_count": coherent_disease_count,
                "gpr183_genetic_disease_count_max": max_genetic_diseases,
                "response_support_systems": response_support_systems,
                "ibd_gpr183_direction": ibd_g["direction"],
                "ibd_gpr183_min_p": ibd_g["p"],
                "ibd_gpr183_weighted_g": ibd_g["g"],
                "ra_gpr183_direction": ra_g["direction"],
                "ra_gpr183_min_p": ra_g["p"],
                "ra_gpr183_weighted_g": ra_g["g"],
                "psoriasis_ada_gpr183_support": pso_support,
                "chembl_human_activity": chembl_human_activity,
                "direct_ms_or_eae_prior_art": direct_prior,
                "direct_prior_pmids": prior_hits,
            }
        ]
    )
    gates.to_csv(OUT / "gate_audit.tsv", sep="\t", index=False)
    return decision


def analyze() -> dict[str, Any]:
    OUT.mkdir(parents=True, exist_ok=True)

    ms = ms_gene_rows()
    broad_rows, broad_summary = broad_target_rows()
    w74 = wave74_context()
    ibd_tests, ibd_coverage = ibd_external_antitnf_tests()
    ibd_meta = summarize_response_meta(ibd_tests, "IBD_external_antitnf")
    ra_tests = ra_baseline_response_tests()
    ra_meta = summarize_response_meta(ra_tests.assign(system="RA_baseline") if not ra_tests.empty else ra_tests, "RA_baseline")
    pso_tests = psoriasis_baseline_response_tests()
    pso_meta = summarize_response_meta(
        pso_tests[pso_tests["treatment"].eq("ADA")].assign(system="psoriasis_ADA") if not pso_tests.empty else pso_tests,
        "psoriasis_ADA",
    )
    target_resolution = target_resolution_rows()
    chembl_targets, chembl_activities = chembl_target_query()
    pubmed_queries, pubmed_records = pubmed_search()
    trials = clinicaltrials_search()
    patents = patent_search_urls()

    decision = integrate_decision(ms, broad_summary, w74, ibd_meta, ra_tests, pso_tests, target_resolution, chembl_targets, pubmed_records)

    ms.to_csv(OUT / "ms_gse111972_target_gene_rows.tsv", sep="\t", index=False)
    broad_rows.to_csv(OUT / "broad_h5ad_target_gene_rows.tsv", sep="\t", index=False)
    broad_summary.to_csv(OUT / "broad_h5ad_target_gene_summary.tsv", sep="\t", index=False)
    ibd_tests.to_csv(OUT / "ibd_external_antitnf_gene_response_tests.tsv", sep="\t", index=False)
    ibd_meta.to_csv(OUT / "ibd_external_antitnf_gene_response_meta.tsv", sep="\t", index=False)
    ibd_coverage.to_csv(OUT / "ibd_external_antitnf_platform_coverage.tsv", sep="\t", index=False)
    ra_tests.to_csv(OUT / "ra_gse198520_baseline_gene_response_tests.tsv", sep="\t", index=False)
    ra_meta.to_csv(OUT / "ra_gse198520_baseline_gene_response_meta.tsv", sep="\t", index=False)
    pso_tests.to_csv(OUT / "psoriasis_gse85034_baseline_gene_response_tests.tsv", sep="\t", index=False)
    pso_meta.to_csv(OUT / "psoriasis_gse85034_ada_gene_response_meta.tsv", sep="\t", index=False)
    target_resolution.to_csv(OUT / "target_resolution_rows.tsv", sep="\t", index=False)
    chembl_targets.to_csv(OUT / "chembl_target_query.tsv", sep="\t", index=False)
    chembl_activities.to_csv(OUT / "chembl_example_activities.tsv", sep="\t", index=False)
    pubmed_queries.to_csv(OUT / "pubmed_query_log.tsv", sep="\t", index=False)
    pubmed_records.to_csv(OUT / "pubmed_records.tsv", sep="\t", index=False)
    trials.to_csv(OUT / "clinicaltrials_records.tsv", sep="\t", index=False)
    patents.to_csv(OUT / "patent_search_urls.tsv", sep="\t", index=False)
    decision.to_csv(OUT / "integrated_decision.tsv", sep="\t", index=False)

    summary = {
        "seed": SEED,
        "analysis_call": str(decision.iloc[0]["wave93_call"]),
        "candidate": "GPR183_EBI2_oxysterol_niche",
        "target_genes": TARGET_GENES,
        "response_genes": RESPONSE_GENES,
        "inputs": {
            "wave74": rel(W74),
            "wave83": rel(W83),
            "ms_signature": rel(MS_SIG),
            "broad_h5ad": rel(BROAD),
            "wave55": rel(W55),
            "wave62": rel(W62),
            "ibd_external_geo_raw": rel(W85_RAW),
            "ra_counts": rel(RA_COUNTS),
            "ra_meta": rel(RA_META),
            "psoriasis_series": rel(GSE85034_SERIES),
            "psoriasis_platform": rel(GPL10558_ANNOT),
        },
        "n_ibd_gene_tests": int(len(ibd_tests)),
        "n_ra_gene_tests": int(len(ra_tests)),
        "n_psoriasis_gene_tests": int(len(pso_tests)),
        "n_pubmed_records": int(len(pubmed_records)),
        "n_clinicaltrials_records": int(len(trials)),
    }
    write_json(OUT / "summary.json", summary)

    gpr_pubmed = pubmed_records.head(12) if not pubmed_records.empty else pd.DataFrame()
    report = [
        "# Wave93 GPR183/EBI2 Oxysterol-Niche Forcing Test",
        "",
        "Question: can a druggable upstream oxysterol-guided niche controller rescue the lipid-lysosomal myeloid module after direct lipid-state genes failed?",
        "",
        f"Analysis call: `{summary['analysis_call']}`.",
        "",
        "## Integrated Decision",
        "",
        markdown_table(decision, max_rows=5),
        "",
        "## Gate Audit",
        "",
        markdown_table(read_tsv(OUT / "gate_audit.tsv"), max_rows=20),
        "",
        "## MS Target-Gene Rows",
        "",
        markdown_table(ms, max_rows=20),
        "",
        "## Broad h5ad Target-Gene Summary",
        "",
        markdown_table(broad_summary, max_rows=20),
        "",
        "## IBD External Anti-TNF Gene-Level Meta",
        "",
        markdown_table(ibd_meta, max_rows=30),
        "",
        "## RA Baseline Anti-TNF Gene-Level Meta",
        "",
        markdown_table(ra_meta, max_rows=30),
        "",
        "## Psoriasis Adalimumab Gene-Level Meta",
        "",
        markdown_table(pso_meta, max_rows=30),
        "",
        "## Target Resolution Rows",
        "",
        markdown_table(
            target_resolution[
                [
                    col
                    for col in [
                        "source",
                        "gene",
                        "approved_name",
                        "wave55_score",
                        "wave62_score",
                        "wave62_call",
                        "n_diseases_genetic_ge_0_25",
                        "diseases_genetic_ge_0_25",
                        "strong_l2g_disease_count",
                        "strong_l2g_diseases",
                        "ms_wm_delta_log2",
                        "ms_wm_p",
                        "druggable_activity_count",
                    ]
                    if col in target_resolution.columns
                ]
            ],
            max_rows=20,
        ),
        "",
        "## ChEMBL Target Query",
        "",
        markdown_table(chembl_targets, max_rows=30),
        "",
        "## PubMed Closest Prior Art",
        "",
        markdown_table(gpr_pubmed[["pmid", "title", "journal", "pubdate", "doi", "direct_ms_or_eae_gpr183_like_prior_art", "autoimmune_prior_art_like"]] if not gpr_pubmed.empty else gpr_pubmed, max_rows=12),
        "",
        "## Guardrails",
        "",
        "- Promotion requires receptor/ligand coherence, not only response genes.",
        "- `EBI3` nomenclature is irrelevant here; EBI2 is `GPR183`.",
        "- A response association is not treated as an intervention target unless MS anchoring and target-resolved genetics/druggability also survive.",
        "- ChEMBL/PubMed/ClinicalTrials API failures, if any, are recorded in the corresponding TSVs rather than silently ignored.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    return summary


if __name__ == "__main__":
    np.random.seed(SEED)
    result = analyze()
    print(json.dumps(result, indent=2, sort_keys=True))
