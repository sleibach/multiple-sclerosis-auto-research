#!/usr/bin/env python3
"""Wave80 CD58/CD2-axis deepening.

Wave79 parked CD58 because it has unusually strong MS genetic support and
Crohn/UC myeloid recurrence, but failed the adjusted RA/IBD response-specificity
gate. This wave asks whether CD58 can be reframed as a CD2/CD58 immune-synapse
intervention rather than a lipid-lysosomal myeloid target.

The new local test attacks the strongest local response signal: in RA synovium,
does baseline CD58 still separate anti-TNF responders after adjusting for T-cell
and effector-memory T-cell abundance modules, or is the signal mostly immune
cell composition/costimulation context?
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from statsmodels.stats.multitest import multipletests

from v3_analyze_direct_h5ad_cell_states import MODULES, ROOT


SEED = 20260527
OUT = ROOT / "results_v3" / "wave80_cd58_cd2_axis_deepening"

RA_COUNTS = ROOT / "results_v3" / "wave65_gse198520_ra_synovium_antitnf_audit" / "gse198520_counts_used.tsv"
RA_META = ROOT / "results_v3" / "wave65_gse198520_ra_synovium_antitnf_audit" / "gse198520_sample_metadata.tsv"
W79_DECISION = ROOT / "results_v3" / "wave79_targetability_shortlist_audit" / "targetability_integrated_decision.tsv"
W79_CONV = ROOT / "results_v3" / "wave79_targetability_shortlist_audit" / "targetability_adjusted_response_convergence.tsv"
W62 = ROOT / "results_v3" / "wave62_opentargets_target_resolution" / "target_resolution_summary.tsv"
W62_QTL = ROOT / "results_v3" / "wave62_opentargets_target_resolution" / "opentargets_qtl_coloc_rows.tsv"

GENE = "CD58"
T_CELL_MODULE = [
    "CD2",
    "CD3D",
    "CD3E",
    "CD3G",
    "TRAC",
    "CD4",
    "CD8A",
    "CD8B",
    "IL7R",
    "CCR7",
    "SELL",
    "LTB",
    "CD27",
]
EFFECTOR_MEMORY_MODULE = [
    "CD2",
    "CD8A",
    "GZMB",
    "PRF1",
    "NKG7",
    "GNLY",
    "CCL5",
    "CXCR3",
    "KLRD1",
]
GENERIC_INFLAMMATION = MODULES["inflammatory_nfkb"]


PRIOR_ART = [
    {
        "source_type": "published_ms_genetics",
        "claim": "CD58 protective allele is associated with increased CD58 expression and enhanced FOXP3/Treg function in MS-context samples.",
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC2664005/",
        "identifier": "PNAS 2009 CD58 locus in MS",
        "local_interpretation": "supports CD58 as MS biology, but direction is increased CD58/restored CD2 engagement rather than simple CD58 blockade",
    },
    {
        "source_type": "meta_analysis",
        "claim": "2024 meta-analysis reports CD58 SNP associations with MS risk and protective effects in several genetic models.",
        "url": "https://doi.org/10.1016/j.msard.2023.105411",
        "identifier": "MSARD 2024 105411",
        "local_interpretation": "confirms non-novel MS genetic anchor",
    },
    {
        "source_type": "approved_drug_and_autoimmune_prior_art",
        "claim": "Alefacept is a CD58/LFA-3-Ig fusion protein targeting CD2; approved/tested in psoriasis and other immune indications.",
        "url": "https://www.nejm.org/doi/full/10.1056/NEJM200107263450403",
        "identifier": "NEJM 2001 psoriasis alefacept",
        "local_interpretation": "blocks novelty for generic CD2/CD58 autoimmune intervention",
    },
    {
        "source_type": "clinical_trial",
        "claim": "T1DAL tested alefacept in new-onset type 1 diabetes; 12-month primary 2h C-peptide endpoint missed, secondary 4h C-peptide/insulin/hypoglycemia endpoints favored alefacept.",
        "url": "https://clinicaltrials.gov/study/NCT00965458",
        "identifier": "NCT00965458",
        "local_interpretation": "strong cross-autoimmune prior art and a plausible lead-indication precedent, not a novel MS mechanism",
    },
    {
        "source_type": "clinical_followup",
        "claim": "T1DAL 24-month follow-up reported sustained C-peptide and clinical/immunologic effects after alefacept.",
        "url": "https://www.jci.org/articles/view/81722/sd/1",
        "identifier": "JCI T1DAL 24-month follow-up",
        "local_interpretation": "supports CD2 targeting as biologically active, but increases prior-art burden",
    },
    {
        "source_type": "trial_registry_search",
        "claim": "ClinicalTrials.gov searches surfaced psoriasis, T1D, transplant, graft-versus-host, aplastic anemia, and skin-disease alefacept studies, but no registered MS alefacept trial in the search results used here.",
        "url": "https://clinicaltrials.gov/search?term=alefacept%20multiple%20sclerosis",
        "identifier": "ClinicalTrials.gov query 2026-05-27",
        "local_interpretation": "MS-specific trial novelty may remain, but generic autoimmune CD2/CD58 intervention is not novel",
    },
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def read_tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True) + "\n", encoding="utf-8")


def markdown_table(df: pd.DataFrame, max_rows: int = 30) -> str:
    if df.empty:
        return "_No rows._"
    view = df.head(max_rows).copy()
    cols = list(view.columns)
    lines = ["| " + " | ".join(cols) + " |", "| " + " | ".join(["---"] * len(cols)) + " |"]
    for _, row in view.iterrows():
        vals = []
        for col in cols:
            value = row[col]
            if isinstance(value, float):
                vals.append("" if math.isnan(value) else f"{value:.4g}")
            else:
                vals.append(str(value).replace("|", "\\|"))
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines)


def bh(values: pd.Series | np.ndarray) -> np.ndarray:
    return multipletests(pd.Series(values).fillna(1.0).to_numpy(float), method="fdr_bh")[1]


def numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series.replace("NA", np.nan), errors="coerce")


def log_cpm(counts: pd.DataFrame) -> pd.DataFrame:
    lib = counts.sum(axis=0).replace(0, np.nan)
    return np.log2(counts.div(lib, axis=1) * 1_000_000.0 + 1.0)


def zscore_rows(expr: pd.DataFrame) -> pd.DataFrame:
    return expr.sub(expr.mean(axis=1), axis=0).div(expr.std(axis=1, ddof=1).replace(0, np.nan), axis=0)


def module_score(z: pd.DataFrame, genes: list[str]) -> pd.Series:
    present = [g for g in genes if g in z.index]
    if not present:
        return pd.Series(index=z.columns, dtype=float)
    return z.loc[present].mean(axis=0, skipna=True)


def build_ra_cd58_pairs() -> tuple[pd.DataFrame, pd.DataFrame]:
    counts = read_tsv(RA_COUNTS)
    meta = read_tsv(RA_META)
    if counts.empty or meta.empty:
        return pd.DataFrame(), pd.DataFrame()
    counts = counts.set_index("GeneSymbol")
    counts.index = counts.index.astype(str).str.upper()
    expr = log_cpm(counts.astype(float))
    z = zscore_rows(expr)
    sample = meta[
        [
            "count_column",
            "patient",
            "response_code",
            "response_class",
            "timepoint",
            "pathotype",
            "biologic",
            "inflammatory_score",
            "das28_score",
        ]
    ].copy()
    sample["inflammatory_score"] = numeric(sample["inflammatory_score"])
    sample["das28_score"] = numeric(sample["das28_score"])
    for name, genes in [
        ("generic_inflammatory_nfkb", GENERIC_INFLAMMATION),
        ("t_cell_score", T_CELL_MODULE),
        ("effector_memory_t_cell_score", EFFECTOR_MEMORY_MODULE),
    ]:
        score = module_score(z, genes)
        sample[name] = sample["count_column"].map(score.to_dict()).astype(float)
    if GENE in z.index:
        sample["cd58_score"] = sample["count_column"].map(z.loc[GENE].to_dict()).astype(float)
    else:
        sample["cd58_score"] = np.nan

    rows = []
    for patient, sub in sample.groupby("patient", observed=True):
        pre = sub[sub["timepoint"].eq("pre")]
        post = sub[sub["timepoint"].eq("post")]
        if len(pre) != 1 or len(post) != 1:
            continue
        p = pre.iloc[0]
        q = post.iloc[0]
        rows.append(
            {
                "patient": patient,
                "response_code": p["response_code"],
                "response_class": p["response_class"],
                "good_response": int(p["response_code"] == "r"),
                "moderate_good_response": int(p["response_code"] in {"r", "mr"}),
                "pathotype": p.get("pathotype", ""),
                "biologic": p.get("biologic", ""),
                "inflammatory_score": p.get("inflammatory_score", np.nan),
                "das28_score": p.get("das28_score", np.nan),
                "pre_cd58": float(p["cd58_score"]),
                "post_cd58": float(q["cd58_score"]),
                "delta_cd58": float(q["cd58_score"] - p["cd58_score"]),
                "pre_generic": float(p["generic_inflammatory_nfkb"]),
                "delta_generic": float(q["generic_inflammatory_nfkb"] - p["generic_inflammatory_nfkb"]),
                "pre_t_cell": float(p["t_cell_score"]),
                "delta_t_cell": float(q["t_cell_score"] - p["t_cell_score"]),
                "pre_effmem_t": float(p["effector_memory_t_cell_score"]),
                "delta_effmem_t": float(q["effector_memory_t_cell_score"] - p["effector_memory_t_cell_score"]),
            }
        )
    pairs = pd.DataFrame(rows)
    coverage = pd.DataFrame(
        [
            {"module": "t_cell_score", "n_present": len([g for g in T_CELL_MODULE if g in z.index]), "genes_present": ";".join([g for g in T_CELL_MODULE if g in z.index])},
            {
                "module": "effector_memory_t_cell_score",
                "n_present": len([g for g in EFFECTOR_MEMORY_MODULE if g in z.index]),
                "genes_present": ";".join([g for g in EFFECTOR_MEMORY_MODULE if g in z.index]),
            },
            {
                "module": "generic_inflammatory_nfkb",
                "n_present": len([g for g in GENERIC_INFLAMMATION if g in z.index]),
                "genes_present": ";".join([g for g in GENERIC_INFLAMMATION if g in z.index]),
            },
        ]
    )
    return pairs, coverage


def fit_models(pairs: pd.DataFrame) -> pd.DataFrame:
    rows = []
    if pairs.empty:
        return pd.DataFrame()
    specs = [
        ("baseline_pre", "pre_cd58", "generic_only", "good_response + pre_generic + C(pathotype) + C(biologic) + inflammatory_score + das28_score"),
        (
            "baseline_pre",
            "pre_cd58",
            "generic_plus_t_cell",
            "good_response + pre_generic + pre_t_cell + C(pathotype) + C(biologic) + inflammatory_score + das28_score",
        ),
        (
            "baseline_pre",
            "pre_cd58",
            "generic_plus_t_cell_plus_effmem",
            "good_response + pre_generic + pre_t_cell + pre_effmem_t + C(pathotype) + C(biologic) + inflammatory_score + das28_score",
        ),
        (
            "delta_post_minus_pre",
            "delta_cd58",
            "generic_only",
            "good_response + pre_cd58 + pre_generic + delta_generic + C(pathotype) + C(biologic) + inflammatory_score + das28_score",
        ),
        (
            "delta_post_minus_pre",
            "delta_cd58",
            "generic_plus_t_cell",
            "good_response + pre_cd58 + pre_generic + delta_generic + pre_t_cell + delta_t_cell + C(pathotype) + C(biologic) + inflammatory_score + das28_score",
        ),
        (
            "delta_post_minus_pre",
            "delta_cd58",
            "generic_plus_t_cell_plus_effmem",
            "good_response + pre_cd58 + pre_generic + delta_generic + pre_t_cell + delta_t_cell + pre_effmem_t + delta_effmem_t + C(pathotype) + C(biologic) + inflammatory_score + das28_score",
        ),
    ]
    for endpoint, y_col, model_name, rhs in specs:
        needed = [y_col, "good_response"]
        for col in [
            "pre_cd58",
            "pre_generic",
            "delta_generic",
            "pre_t_cell",
            "delta_t_cell",
            "pre_effmem_t",
            "delta_effmem_t",
            "inflammatory_score",
            "das28_score",
        ]:
            if col in rhs:
                needed.append(col)
        model_df = pairs.dropna(subset=needed).copy()
        if model_df.shape[0] < 12 or model_df["good_response"].nunique() < 2:
            rows.append(
                {
                    "endpoint": endpoint,
                    "model_name": model_name,
                    "n": int(model_df.shape[0]),
                    "response_coef": np.nan,
                    "response_p": np.nan,
                    "model_status": "insufficient_rows_or_response_levels",
                    "formula": "",
                }
            )
            continue
        formula = f"y ~ {rhs}"
        model_df = model_df.rename(columns={y_col: "y"})
        try:
            fit = smf.ols(formula, data=model_df).fit()
            rows.append(
                {
                    "endpoint": endpoint,
                    "model_name": model_name,
                    "n": int(model_df.shape[0]),
                    "response_coef": float(fit.params.get("good_response", np.nan)),
                    "response_p": float(fit.pvalues.get("good_response", np.nan)),
                    "t_cell_coef": float(fit.params.get("pre_t_cell", np.nan)),
                    "t_cell_p": float(fit.pvalues.get("pre_t_cell", np.nan)),
                    "effmem_t_coef": float(fit.params.get("pre_effmem_t", np.nan)),
                    "effmem_t_p": float(fit.pvalues.get("pre_effmem_t", np.nan)),
                    "model_status": "ok",
                    "formula": formula,
                }
            )
        except Exception as exc:  # noqa: BLE001
            rows.append(
                {
                    "endpoint": endpoint,
                    "model_name": model_name,
                    "n": int(model_df.shape[0]),
                    "response_coef": np.nan,
                    "response_p": np.nan,
                    "model_status": f"fit_failed:{type(exc).__name__}:{exc}",
                    "formula": formula,
                }
            )
    out = pd.DataFrame(rows)
    out["response_fdr"] = bh(out["response_p"])
    return out


def read_local_evidence() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    w79_dec = read_tsv(W79_DECISION)
    w79_conv = read_tsv(W79_CONV)
    w62 = read_tsv(W62)
    qtl = read_tsv(W62_QTL)
    if not w79_dec.empty:
        w79_dec = w79_dec[w79_dec["gene"].astype(str).str.upper().eq(GENE)].copy()
    if not w79_conv.empty:
        w79_conv = w79_conv[w79_conv["gene"].astype(str).str.upper().eq(GENE)].copy()
    if not w62.empty:
        w62 = w62[w62["gene"].astype(str).str.upper().eq(GENE)].copy()
    if not qtl.empty:
        qtl = qtl[qtl["gene"].astype(str).str.upper().eq(GENE)].copy()
    return w79_dec, w79_conv, w62, qtl


def decision(w79_dec: pd.DataFrame, w79_conv: pd.DataFrame, ra_models: pd.DataFrame, prior: pd.DataFrame) -> pd.DataFrame:
    local = w79_dec.iloc[0].to_dict() if not w79_dec.empty else {}
    best_baseline = (
        ra_models[(ra_models["endpoint"].eq("baseline_pre")) & (ra_models["model_status"].eq("ok"))]
        .sort_values("model_name")
        .copy()
    )
    full = best_baseline[best_baseline["model_name"].eq("generic_plus_t_cell_plus_effmem")]
    full_coef = float(full["response_coef"].iloc[0]) if not full.empty else np.nan
    full_p = float(full["response_p"].iloc[0]) if not full.empty else np.nan
    w79_ibd_p = float(local.get("ibd_response_p", np.nan))
    ms_anchor = bool(local.get("gate_ms_anchor", 0))
    generic_autoimmune_prior = bool(prior["source_type"].isin(["approved_drug_and_autoimmune_prior_art", "clinical_trial"]).any())
    direction_conflict = True
    if ms_anchor and full_p <= 0.05 and w79_ibd_p <= 0.10 and not generic_autoimmune_prior and not direction_conflict:
        call = "REOPEN_CD58_CD2_AXIS"
        reason = "CD58/CD2 axis passes reframed response, novelty, and direction gates"
    elif ms_anchor and full_p <= 0.10:
        call = "PARK_CD58_CD2_AXIS_PRIOR_ART_OR_IBD_LIMITED"
        reason = "MS genetics and RA CD58 signal survive T-cell adjustment, but IBD replication, direction, or prior art block promotion"
    else:
        call = "NO_GO_CD58_CD2_AXIS"
        reason = "CD58 signal does not survive reframed CD2-axis gates"
    return pd.DataFrame(
        [
            {
                "candidate": "CD58_CD2_axis",
                "wave80_call": call,
                "ms_anchor": int(ms_anchor),
                "ra_full_tcell_adjusted_coef": full_coef,
                "ra_full_tcell_adjusted_p": full_p,
                "wave79_ibd_response_p": w79_ibd_p,
                "wave79_ibd_target_generic_abs_ratio": local.get("ibd_target_generic_abs_ratio", np.nan),
                "wave79_ra_response_p": local.get("ra_response_p", np.nan),
                "wave79_ra_target_generic_abs_ratio": local.get("ra_target_generic_abs_ratio", np.nan),
                "generic_autoimmune_prior_art": int(generic_autoimmune_prior),
                "direction_conflict": int(direction_conflict),
                "decision_reason": reason,
            }
        ]
    )


def write_report(
    dec: pd.DataFrame,
    pairs: pd.DataFrame,
    coverage: pd.DataFrame,
    ra_models: pd.DataFrame,
    w79_dec: pd.DataFrame,
    w79_conv: pd.DataFrame,
    w62: pd.DataFrame,
    qtl: pd.DataFrame,
    prior: pd.DataFrame,
) -> None:
    lines = [
        "# Wave80 CD58/CD2-Axis Deepening",
        "",
        "## Question",
        "",
        "Can `CD58` be reframed from a weak myeloid-module target into a",
        "defensible cross-autoimmune CD2/CD58 immune-synapse intervention?",
        "",
        "## Verdict",
        "",
        str(dec.iloc[0]["wave80_call"]),
        "",
        "## Integrated Decision",
        "",
        markdown_table(dec),
        "",
        "## RA CD58 Models With T-Cell Adjustment",
        "",
        markdown_table(ra_models, max_rows=20),
        "",
        "## RA Module Coverage",
        "",
        markdown_table(coverage),
        "",
        "## Wave79 CD58 Evidence",
        "",
        markdown_table(w79_dec),
        "",
        "## Wave79 Adjusted RA/IBD Convergence Row",
        "",
        markdown_table(w79_conv),
        "",
        "## Wave62 CD58 Target Resolution",
        "",
        markdown_table(w62),
        "",
        "## Wave62 CD58 QTL/Coloc Rows",
        "",
        markdown_table(
            qtl[
                [
                    "disease",
                    "trait_from_source",
                    "variant_id",
                    "rs_ids",
                    "beta",
                    "qtl_study_type",
                    "biosample_name",
                    "h4",
                    "risk_qtl_direction_proxy",
                    "biosample_relevant",
                    "biosample_myeloid",
                ]
            ]
            if not qtl.empty
            else qtl,
            max_rows=20,
        ),
        "",
        "## Verified Prior-Art / Directionality Table",
        "",
        markdown_table(prior, max_rows=20),
        "",
        "## Interpretation",
        "",
        "The strongest local `CD58` signal is compatible with immune-synapse biology,",
        "but the intervention direction is conflicted. MS genetics and the classic",
        "CD58 locus paper point toward higher CD58 expression and Treg support,",
        "whereas the available drug precedent, alefacept, is a CD58-Ig/CD2-directed",
        "agent that blocks CD2/CD58 interaction and depletes CD2-high memory T",
        "cells. That is a plausible autoimmune mechanism, but it is already prior",
        "art in psoriasis and T1D and does not rescue the weak IBD replication in",
        "the local V3 analysis.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)

    pairs, coverage = build_ra_cd58_pairs()
    ra_models = fit_models(pairs)
    w79_dec, w79_conv, w62, qtl = read_local_evidence()
    prior = pd.DataFrame(PRIOR_ART)
    dec = decision(w79_dec, w79_conv, ra_models, prior)

    pairs.to_csv(OUT / "cd58_ra_patient_pairs_with_tcell_scores.tsv", sep="\t", index=False)
    coverage.to_csv(OUT / "cd58_ra_module_gene_coverage.tsv", sep="\t", index=False)
    ra_models.to_csv(OUT / "cd58_ra_tcell_adjusted_models.tsv", sep="\t", index=False)
    w79_dec.to_csv(OUT / "cd58_wave79_decision_row.tsv", sep="\t", index=False)
    w79_conv.to_csv(OUT / "cd58_wave79_response_convergence_row.tsv", sep="\t", index=False)
    w62.to_csv(OUT / "cd58_wave62_summary_row.tsv", sep="\t", index=False)
    qtl.to_csv(OUT / "cd58_wave62_qtl_rows.tsv", sep="\t", index=False)
    prior.to_csv(OUT / "cd58_prior_art_directionality_sources.tsv", sep="\t", index=False)
    dec.to_csv(OUT / "cd58_cd2_axis_decision.tsv", sep="\t", index=False)

    summary = {
        "random_seed": SEED,
        "inputs": {
            "ra_counts": rel(RA_COUNTS),
            "ra_meta": rel(RA_META),
            "wave79_decision": rel(W79_DECISION),
            "wave79_convergence": rel(W79_CONV),
            "wave62_summary": rel(W62),
            "wave62_qtl": rel(W62_QTL),
            "prior_art_sources": "embedded verified source table written to cd58_prior_art_directionality_sources.tsv",
        },
        "decision": dec.replace({np.nan: None}).to_dict(orient="records")[0],
        "top_ra_models": ra_models.head(20).replace({np.nan: None}).to_dict(orient="records"),
    }
    write_json(OUT / "summary.json", summary)
    write_report(dec, pairs, coverage, ra_models, w79_dec, w79_conv, w62, qtl, prior)


if __name__ == "__main__":
    main()
