#!/usr/bin/env python3
"""Wave62 Open Targets credible-set target-resolution audit.

Earlier genetics waves correctly refused to treat mapped-gene or aggregate
Open Targets association scores as coloc/MR. This wave probes the newer
Open Targets Platform `credibleSet`, `l2GPredictions`, and `colocalisation`
API fields. The output is target-resolution triage, not a therapeutic finding.
"""

from __future__ import annotations

import json
import math
import re
import time
from pathlib import Path
from typing import Any

import pandas as pd
import requests


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results_v3" / "wave62_opentargets_target_resolution"
RAW = OUT / "raw_api"
SEED = 20260527
OT_API = "https://api.platform.opentargets.org/api/v4/graphql"

DISEASES = {
    "MS": "MONDO_0005301",
    "RA": "EFO_0000685",
    "Crohn": "EFO_0000384",
    "UC": "EFO_0000729",
    "Psoriasis": "EFO_0000676",
    "SLE": "MONDO_0007915",
    "T1D": "MONDO_0005147",
    "Sjogren": "EFO_0000699",
    "AS": "EFO_0003898",
    "AITD": "EFO_0006812",
    "Celiac": "EFO_0001060",
    "PBC": "EFO_1001486",
}

INPUTS = {
    "broad_h5ad": ROOT / "results_v3" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_rank.tsv",
    "broad_residual": ROOT / "results_v3" / "broad_residual_gate" / "broad_residual_gate_summary.tsv",
    "wave34": ROOT / "results_v3" / "wave34_genetics_expression_druggability_scan" / "wave34_genetics_expression_druggability_rank.tsv",
    "wave34a": ROOT / "results_v3" / "wave34a_genetics_first_target_rescue" / "genetics_first_candidate_rank.tsv",
    "wave55": ROOT / "results_v3" / "wave55_external_genetics_druggability_sweep" / "external_genetics_rank.tsv",
    "wave61": ROOT / "results_v3" / "wave61_perturbation_first_guardrail" / "intervention_evidence_tiers.tsv",
}

MAX_STUDIES_PER_DISEASE = 60
MAX_CREDIBLE_SETS_PER_STUDY = 250
L2G_PAGE_SIZE = 10
COLOC_PAGE_SIZE = 25

QTL_STUDY_TYPES = ["eqtl", "pqtl", "sceqtl", "scpqtl", "sqtl", "tuqtl", "sctuqtl", "scsqtl"]

RELEVANT_BIOSAMPLE_RE = re.compile(
    r"monocyte|macrophage|microglia|blood|spleen|lymph|t[ -]?helper|t cell|b cell|"
    r"dendritic|colon|ileum|intestin|skin|brain|cortex|fibroblast|thyroid|pancrea|"
    r"salivary|liver|neutrophil",
    re.I,
)

MYELOID_BIOSAMPLE_RE = re.compile(r"monocyte|macrophage|microglia|dendritic|neutrophil", re.I)

MANUAL_BLOCKERS = {
    "HLA-DRA": "HLA_MHC_antigen_presentation_host_defense",
    "HLA-DRB1": "HLA_MHC_antigen_presentation_host_defense",
    "HLA-DQA1": "HLA_MHC_antigen_presentation_host_defense",
    "HLA-DQB1": "HLA_MHC_antigen_presentation_host_defense",
    "HLA-DPA1": "HLA_MHC_antigen_presentation_host_defense",
    "HLA-DPB1": "HLA_MHC_antigen_presentation_host_defense",
    "CD74": "direct_antigen_presentation_host_defense",
    "CIITA": "direct_antigen_presentation_host_defense",
    "RFX5": "direct_antigen_presentation_host_defense",
    "IFI30": "direct_antigen_processing_host_defense_and_druggability",
    "CTSS": "direct_antigen_processing_prior_art_host_defense",
    "TYK2": "prior_art_autoimmune_kinase_class",
    "IL12B": "prior_art_IL12_IL23_biologic_class",
    "IL12A": "prior_art_IL12_IL23_biologic_class",
    "IL7R": "prior_art_CD127_autoimmune_axis",
    "CD40": "prior_art_costimulation_axis",
    "TNFSF14": "HVEM_LIGHT_axis_directionality_prior_art",
    "PTGER4": "EP4_directionality_prior_art_conflicted",
    "TNFRSF14": "HVEM_LIGHT_axis_directionality_prior_art",
    "TNFAIP3": "A20_restoration_not_currently_druggable",
    "PTPN2": "TCPTP_restoration_not_currently_druggable",
    "IL23R": "prior_art_IL23_axis",
    "IRF5": "prior_art_or_crowded_TF_axis",
    "FCGR2A": "Fc_receptor_directionality_and_safety",
    "PTPN22": "directionality_unresolved_PTPN22_autoimmune_axis",
    "STAT4": "STAT4_TF_not_selectively_druggable",
    "IL2RA": "CD25_IL2_axis_prior_art_directionality",
    "TNFRSF1A": "TNF_axis_prior_art_and_MS_paradox_risk",
    "IL6R": "prior_art_IL6R_axis",
    "PDCD1": "checkpoint_axis_safety_prior_art",
}


PRIOR_CONTEXT_BLOCKER_RE = re.compile(
    r"DEMOTE_|PRIOR_ART|NOT_DRUGGABLE|NO_TARGET_LEVEL|BLOCKED|MISMATCH|UNRESOLVED",
    re.I,
)


CALL_ORDER = {
    "REOPEN_TARGET_RESOLVED_NEEDS_INTERVENTION_AUDIT": 0,
    "PARK_TARGET_RESOLVED_BUT_BLOCKED_OR_NARROW": 1,
    "PARK_MS_TARGET_RESOLVED_NO_CROSS_DISEASE_MODULE": 2,
    "PARK_GENETIC_CELL_STATE_NOT_CURRENTLY_DRUGGABLE": 3,
    "NO_GO_WAVE62_TARGET_RESOLUTION": 4,
}


STUDIES_QUERY = """
query studies($diseaseIds: [String!], $page: Pagination) {
  studies(diseaseIds: $diseaseIds, page: $page) {
    count
    rows {
      id
      traitFromSource
      studyType
      hasSumstats
      nCases
      nControls
      nSamples
      pubmedId
      publicationFirstAuthor
      publicationDate
      diseases { id name }
      credibleSets(page: {index: 0, size: 0}) { count }
    }
  }
}
"""

CREDIBLE_SETS_QUERY = """
query credibleSets($studyIds: [String!], $page: Pagination) {
  credibleSets(studyIds: $studyIds, page: $page) {
    count
    rows {
      studyLocusId
      studyId
      studyType
      chromosome
      position
      pValueMantissa
      pValueExponent
      beta
      standardError
      confidence
      finemappingMethod
      purityMeanR2
      purityMinR2
      variant { id rsIds }
      l2GPredictions(page: {index: 0, size: 10}) {
        count
        rows {
          score
          target { id approvedSymbol approvedName }
        }
      }
      colocalisation(
        studyTypes: [eqtl, pqtl, sceqtl, scpqtl, sqtl, tuqtl, sctuqtl, scsqtl],
        page: {index: 0, size: 25}
      ) {
        count
        rows {
          h4
          clpp
          betaRatioSignAverage
          rightStudyType
          colocalisationMethod
          otherStudyLocus {
            studyId
            studyType
            qtlGeneId
            study {
              traitFromSource
              studyType
              target { id approvedSymbol approvedName }
              biosample { biosampleId biosampleName }
            }
          }
        }
      }
    }
  }
}
"""


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def read_tsv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path, sep="\t", low_memory=False)


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True) + "\n", encoding="utf-8")


def cache_key(prefix: str, text: str) -> Path:
    safe = re.sub(r"[^A-Za-z0-9_.-]+", "_", f"{prefix}_{text}")[:180].strip("_")
    return RAW / f"{safe}.json"


def graphql(query: str, variables: dict[str, Any], cache_path: Path) -> dict[str, Any]:
    if cache_path.exists():
        try:
            return json.loads(cache_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    response = requests.post(
        OT_API,
        json={"query": query, "variables": variables},
        headers={"User-Agent": "ms-auto-research-wave62/1.0", "content-type": "application/json"},
        timeout=60,
    )
    try:
        payload = response.json()
    except ValueError:
        payload = {"errors": [{"message": response.text[:1000]}], "status_code": response.status_code}
    cache_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    time.sleep(0.08)
    return payload


def f(value: Any, default: float = 0.0) -> float:
    try:
        if value is None or pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def p_value(row: dict[str, Any]) -> float:
    mantissa = f(row.get("pValueMantissa"), 1.0)
    exponent = f(row.get("pValueExponent"), 0.0)
    return mantissa * (10 ** exponent)


def disease_names(study: dict[str, Any]) -> str:
    return ";".join(sorted({str(d.get("name", "")) for d in study.get("diseases", []) if d.get("name")}))


def fetch_studies() -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for disease, disease_id in DISEASES.items():
        payload = graphql(
            STUDIES_QUERY,
            {"diseaseIds": [disease_id], "page": {"index": 0, "size": MAX_STUDIES_PER_DISEASE}},
            cache_key("studies", disease),
        )
        if payload.get("errors"):
            rows.append({"disease": disease, "disease_id": disease_id, "api_error": json.dumps(payload.get("errors"))})
            continue
        studies = ((payload.get("data") or {}).get("studies") or {})
        for study in studies.get("rows") or []:
            rows.append(
                {
                    "disease": disease,
                    "disease_id": disease_id,
                    "study_id": study.get("id", ""),
                    "trait_from_source": study.get("traitFromSource", ""),
                    "study_type": study.get("studyType", ""),
                    "has_sumstats": bool(study.get("hasSumstats")),
                    "n_cases": study.get("nCases"),
                    "n_controls": study.get("nControls"),
                    "n_samples": study.get("nSamples"),
                    "pubmed_id": study.get("pubmedId", ""),
                    "publication_first_author": study.get("publicationFirstAuthor", ""),
                    "publication_date": study.get("publicationDate", ""),
                    "mapped_diseases": disease_names(study),
                    "credible_set_count": (((study.get("credibleSets") or {}).get("count")) or 0),
                    "disease_study_count_from_api": studies.get("count", 0),
                    "study_cap": MAX_STUDIES_PER_DISEASE,
                }
            )
    return pd.DataFrame(rows)


def fetch_credible_sets(studies: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    credible_rows: list[dict[str, Any]] = []
    l2g_rows: list[dict[str, Any]] = []
    coloc_rows: list[dict[str, Any]] = []
    caps: list[dict[str, Any]] = []

    if studies.empty:
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    eligible = studies[
        (studies["study_type"].astype(str) == "gwas")
        & studies["has_sumstats"].astype(bool)
        & (pd.to_numeric(studies["credible_set_count"], errors="coerce").fillna(0) > 0)
    ].copy()

    for _, study in eligible.iterrows():
        study_id = str(study["study_id"])
        total = int(study["credible_set_count"])
        if total > MAX_CREDIBLE_SETS_PER_STUDY:
            caps.append(
                {
                    "study_id": study_id,
                    "disease": study["disease"],
                    "credible_set_count": total,
                    "cap": MAX_CREDIBLE_SETS_PER_STUDY,
                    "cap_reason": "credible_sets_truncated_for_runtime",
                }
            )
        size = min(MAX_CREDIBLE_SETS_PER_STUDY, max(total, 1))
        payload = graphql(
            CREDIBLE_SETS_QUERY,
            {"studyIds": [study_id], "page": {"index": 0, "size": size}},
            cache_key("credible_sets", study_id),
        )
        if payload.get("errors"):
            caps.append(
                {
                    "study_id": study_id,
                    "disease": study["disease"],
                    "credible_set_count": total,
                    "cap": size,
                    "cap_reason": "api_error",
                    "api_error": json.dumps(payload.get("errors"))[:1000],
                }
            )
            continue
        cs = ((payload.get("data") or {}).get("credibleSets") or {})
        for credible in cs.get("rows") or []:
            base = {
                "disease": study["disease"],
                "disease_id": study["disease_id"],
                "study_id": study_id,
                "trait_from_source": study["trait_from_source"],
                "study_locus_id": credible.get("studyLocusId", ""),
                "chromosome": credible.get("chromosome", ""),
                "position": credible.get("position"),
                "variant_id": ((credible.get("variant") or {}).get("id")) or "",
                "rs_ids": ";".join((credible.get("variant") or {}).get("rsIds") or []),
                "p_value": p_value(credible),
                "beta": credible.get("beta"),
                "standard_error": credible.get("standardError"),
                "confidence": credible.get("confidence", ""),
                "finemapping_method": credible.get("finemappingMethod", ""),
                "purity_mean_r2": credible.get("purityMeanR2"),
                "purity_min_r2": credible.get("purityMinR2"),
                "n_cases": study["n_cases"],
                "n_controls": study["n_controls"],
                "n_samples": study["n_samples"],
            }
            l2g = credible.get("l2GPredictions") or {}
            coloc = credible.get("colocalisation") or {}
            credible_rows.append(
                {
                    **base,
                    "l2g_count": l2g.get("count", 0),
                    "colocalisation_count": coloc.get("count", 0),
                    "l2g_cap": L2G_PAGE_SIZE,
                    "coloc_cap": COLOC_PAGE_SIZE,
                }
            )
            for rank, pred in enumerate(l2g.get("rows") or [], start=1):
                target = pred.get("target") or {}
                l2g_rows.append(
                    {
                        **base,
                        "l2g_rank": rank,
                        "l2g_score": pred.get("score"),
                        "target_id": target.get("id", ""),
                        "gene": target.get("approvedSymbol", ""),
                        "approved_name": target.get("approvedName", ""),
                    }
                )
            for rank, row in enumerate(coloc.get("rows") or [], start=1):
                other = row.get("otherStudyLocus") or {}
                other_study = other.get("study") or {}
                target = other_study.get("target") or {}
                biosample = other_study.get("biosample") or {}
                biosample_name = biosample.get("biosampleName", "")
                gene = target.get("approvedSymbol") or ""
                disease_beta = f(credible.get("beta"), math.nan)
                beta_sign = f(row.get("betaRatioSignAverage"), math.nan)
                coloc_rows.append(
                    {
                        **base,
                        "coloc_rank": rank,
                        "qtl_study_id": other.get("studyId", ""),
                        "qtl_study_type": other.get("studyType", ""),
                        "qtl_gene_id": other.get("qtlGeneId", ""),
                        "qtl_trait_from_source": other_study.get("traitFromSource", ""),
                        "qtl_target_id": target.get("id", ""),
                        "gene": gene,
                        "approved_name": target.get("approvedName", ""),
                        "biosample_id": biosample.get("biosampleId", ""),
                        "biosample_name": biosample_name,
                        "h4": row.get("h4"),
                        "clpp": row.get("clpp"),
                        "beta_ratio_sign_average": row.get("betaRatioSignAverage"),
                        "right_study_type": row.get("rightStudyType", ""),
                        "colocalisation_method": row.get("colocalisationMethod", ""),
                        "risk_qtl_direction_proxy": disease_beta * beta_sign
                        if not math.isnan(disease_beta) and not math.isnan(beta_sign)
                        else math.nan,
                        "biosample_relevant": bool(RELEVANT_BIOSAMPLE_RE.search(str(biosample_name))),
                        "biosample_myeloid": bool(MYELOID_BIOSAMPLE_RE.search(str(biosample_name))),
                    }
                )
    return pd.DataFrame(credible_rows), pd.DataFrame(l2g_rows), pd.DataFrame(coloc_rows), pd.DataFrame(caps)


def first_row(df: pd.DataFrame, gene: str, col: str = "gene") -> dict[str, Any]:
    if df.empty or col not in df.columns:
        return {}
    sub = df[df[col].astype(str).str.upper() == gene.upper()]
    if sub.empty:
        return {}
    return sub.iloc[0].to_dict()


def join_local_context(gene: str, broad: pd.DataFrame, residual: pd.DataFrame, wave34: pd.DataFrame, wave34a: pd.DataFrame, wave55: pd.DataFrame, wave61: pd.DataFrame) -> dict[str, Any]:
    broad_row = first_row(broad, gene)
    residual_row = first_row(residual, gene)
    wave34_row = first_row(wave34, gene)
    wave34a_row = first_row(wave34a, gene)
    wave55_row = first_row(wave55, gene)
    wave61_gene = wave61[wave61.get("gene", pd.Series(dtype=str)).astype(str).str.upper() == gene.upper()] if not wave61.empty and "gene" in wave61.columns else pd.DataFrame()
    best_wave61 = wave61_gene.iloc[0].to_dict() if not wave61_gene.empty else {}
    return {
        "local_positive_disease_count": f(broad_row.get("positive_disease_count")),
        "local_negative_disease_count": f(broad_row.get("negative_disease_count")),
        "local_positive_diseases": broad_row.get("positive_diseases", ""),
        "ms_wm_delta_log2": f(broad_row.get("ms_wm_delta_log2")),
        "ms_wm_p": f(broad_row.get("ms_wm_p"), 1.0),
        "ms_wm_fdr": f(broad_row.get("ms_wm_fdr"), 1.0),
        "in_lipid_lysosomal_myeloid_neighborhood": bool(broad_row.get("in_lipid_lysosomal_myeloid_neighborhood", False)),
        "residual_retained_disease_count": f(residual_row.get("retained_positive_disease_count")),
        "strict_core_covariate_surviving_disease_count": f(residual_row.get("strict_core_covariate_surviving_disease_count")),
        "wave34_call": wave34_row.get("wave34_call", ""),
        "gwas_catalog_trait_count": f(wave34_row.get("gwas_catalog_trait_count")),
        "chembl_target_id": wave34_row.get("chembl_target_id", ""),
        "druggable_activity_count": f(wave34_row.get("druggable_activity_count")),
        "wave34a_call": wave34a_row.get("wave34a_call", ""),
        "wave34a_direction": wave34a_row.get("direction", ""),
        "wave34a_route_reason": wave34a_row.get("route_reason", ""),
        "wave55_score": f(wave55_row.get("wave55_score")),
        "wave55_genetic_diseases_ge_0_25": wave55_row.get("diseases_genetic_ge_0_25", ""),
        "wave61_best_call": best_wave61.get("wave61_call", ""),
        "wave61_best_manual_blocker": best_wave61.get("manual_blocker", ""),
        "wave61_best_target_suppression": f(best_wave61.get("target_suppression")),
        "wave61_best_selectivity": f(best_wave61.get("selectivity_score")),
    }


def unique_join(df: pd.DataFrame, col: str, limit: int = 500) -> str:
    if df.empty or col not in df.columns:
        return ""
    return ";".join(sorted(set(df[col].dropna().astype(str))))[:limit]


def summarize_targets(l2g: pd.DataFrame, coloc: pd.DataFrame, local_context: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    if l2g.empty:
        return pd.DataFrame()

    l2g = l2g.copy()
    l2g["l2g_score"] = pd.to_numeric(l2g["l2g_score"], errors="coerce")
    coloc = coloc.copy()
    if not coloc.empty:
        coloc["h4"] = pd.to_numeric(coloc["h4"], errors="coerce")
        coloc["clpp"] = pd.to_numeric(coloc["clpp"], errors="coerce")

    for gene, sub in l2g.groupby("gene", dropna=True):
        gene = str(gene)
        if not gene or gene == "nan":
            continue
        strong = sub[sub["l2g_score"] >= 0.5]
        supporting = sub[sub["l2g_score"] >= 0.3]
        same_coloc = coloc[coloc["gene"].astype(str).str.upper() == gene.upper()] if not coloc.empty else pd.DataFrame()
        strong_coloc = same_coloc[same_coloc["h4"] >= 0.8] if not same_coloc.empty else pd.DataFrame()
        relevant_coloc = strong_coloc[strong_coloc["biosample_relevant"].astype(bool)] if not strong_coloc.empty and "biosample_relevant" in strong_coloc else pd.DataFrame()
        myeloid_coloc = strong_coloc[strong_coloc["biosample_myeloid"].astype(bool)] if not strong_coloc.empty and "biosample_myeloid" in strong_coloc else pd.DataFrame()
        ms_l2g = sub[sub["disease"] == "MS"]
        ms_strong = ms_l2g[ms_l2g["l2g_score"] >= 0.5]
        ms_coloc = strong_coloc[strong_coloc["disease"] == "MS"] if not strong_coloc.empty else pd.DataFrame()
        ms_relevant_coloc = relevant_coloc[relevant_coloc["disease"] == "MS"] if not relevant_coloc.empty else pd.DataFrame()
        blocker = MANUAL_BLOCKERS.get(gene, "")
        ctx = join_local_context(gene, **local_context)
        prior_context_blocker = ""
        prior_text = " ".join(
            str(ctx.get(k, ""))
            for k in [
                "wave34_call",
                "wave34a_call",
                "wave34a_direction",
                "wave34a_route_reason",
                "wave61_best_call",
                "wave61_best_manual_blocker",
            ]
        )
        if PRIOR_CONTEXT_BLOCKER_RE.search(prior_text):
            prior_context_blocker = "prior_branch_blocker_or_directionality_unresolved"
        cross_disease_strong = sorted(set(str(x) for x in strong["disease"].dropna()))
        cross_disease_supporting = sorted(set(str(x) for x in supporting["disease"].dropna()))
        coloc_diseases = sorted(set(str(x) for x in strong_coloc["disease"].dropna())) if not strong_coloc.empty else []
        relevant_coloc_diseases = sorted(set(str(x) for x in relevant_coloc["disease"].dropna())) if not relevant_coloc.empty else []

        target_resolved = bool(
            not ms_strong.empty
            and not ms_relevant_coloc.empty
            and len(cross_disease_strong) >= 2
            and len(relevant_coloc_diseases) >= 1
        )
        broad_cross_autoimmune = bool(len(cross_disease_strong) >= 4 or len(cross_disease_supporting) >= 5)
        module_link = bool(
            ctx["in_lipid_lysosomal_myeloid_neighborhood"]
            or ctx["local_positive_disease_count"] >= 3
            or ctx["residual_retained_disease_count"] >= 2
        )
        raw_druggable = bool(ctx["druggable_activity_count"] >= 10 or str(ctx["chembl_target_id"]).strip())
        druggable = bool(raw_druggable and not blocker and not prior_context_blocker)

        score = (
            3.0 * target_resolved
            + 1.5 * broad_cross_autoimmune
            + 1.0 * module_link
            + 0.5 * raw_druggable
            + min(float(sub["l2g_score"].max()), 1.0)
            + min(float(strong_coloc["h4"].max()) if not strong_coloc.empty else 0.0, 1.0)
            - 1.5 * bool(blocker)
            - 1.0 * bool(prior_context_blocker)
        )
        if target_resolved and broad_cross_autoimmune and module_link and druggable:
            call = "REOPEN_TARGET_RESOLVED_NEEDS_INTERVENTION_AUDIT"
        elif target_resolved and (module_link or broad_cross_autoimmune):
            call = "PARK_TARGET_RESOLVED_BUT_BLOCKED_OR_NARROW"
        elif not ms_strong.empty and not ms_relevant_coloc.empty:
            call = "PARK_MS_TARGET_RESOLVED_NO_CROSS_DISEASE_MODULE"
        else:
            call = "NO_GO_WAVE62_TARGET_RESOLUTION"

        rows.append(
            {
                "gene": gene,
                "approved_name": sub["approved_name"].dropna().astype(str).iloc[0] if "approved_name" in sub and sub["approved_name"].notna().any() else "",
                "wave62_score": score,
                "wave62_call": call,
                "manual_blocker": blocker,
                "prior_context_blocker": prior_context_blocker,
                "max_l2g_score": float(sub["l2g_score"].max()),
                "best_l2g_disease": sub.sort_values("l2g_score", ascending=False).iloc[0]["disease"],
                "strong_l2g_disease_count": len(cross_disease_strong),
                "strong_l2g_diseases": ";".join(cross_disease_strong),
                "supporting_l2g_disease_count": len(cross_disease_supporting),
                "supporting_l2g_diseases": ";".join(cross_disease_supporting),
                "ms_max_l2g_score": float(ms_l2g["l2g_score"].max()) if not ms_l2g.empty else 0.0,
                "ms_l2g_study_loci": ";".join(ms_strong["study_locus_id"].dropna().astype(str).unique()[:10]),
                "strong_qtl_coloc_disease_count": len(coloc_diseases),
                "strong_qtl_coloc_diseases": ";".join(coloc_diseases),
                "relevant_qtl_coloc_disease_count": len(relevant_coloc_diseases),
                "relevant_qtl_coloc_diseases": ";".join(relevant_coloc_diseases),
                "myeloid_qtl_coloc_disease_count": len(set(myeloid_coloc["disease"].dropna())) if not myeloid_coloc.empty else 0,
                "max_qtl_h4": float(strong_coloc["h4"].max()) if not strong_coloc.empty else 0.0,
                "ms_max_qtl_h4": float(ms_coloc["h4"].max()) if not ms_coloc.empty else 0.0,
                "ms_max_relevant_qtl_h4": float(ms_relevant_coloc["h4"].max()) if not ms_relevant_coloc.empty else 0.0,
                "ms_relevant_qtl_biosamples": unique_join(ms_relevant_coloc, "biosample_name"),
                "direction_proxy_values": ";".join(
                    sorted(
                        set(
                            f"{r.disease}:{r.biosample_name}:{r.risk_qtl_direction_proxy:.3g}"
                            for r in relevant_coloc.itertuples()
                            if not pd.isna(getattr(r, "risk_qtl_direction_proxy", math.nan))
                        )
                    )
                )[:1000]
                if not relevant_coloc.empty
                else "",
                **ctx,
            }
        )
    out = pd.DataFrame(rows)
    if out.empty:
        return out
    out["_call_order"] = out["wave62_call"].map(CALL_ORDER).fillna(9)
    out = out.sort_values(["_call_order", "wave62_score"], ascending=[True, False]).drop(columns=["_call_order"])
    return out


def gate_matrix(summary: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    if summary.empty:
        return pd.DataFrame()
    for _, row in summary.iterrows():
        gates = {
            "ms_l2g_ge_0_5": f(row.get("ms_max_l2g_score")) >= 0.5,
            "ms_relevant_qtl_h4_ge_0_8": f(row.get("ms_max_relevant_qtl_h4")) >= 0.8,
            "cross_disease_l2g_ge_4_or_supporting_ge_5": f(row.get("strong_l2g_disease_count")) >= 4
            or f(row.get("supporting_l2g_disease_count")) >= 5,
            "qtl_coloc_multiple_diseases": f(row.get("relevant_qtl_coloc_disease_count")) >= 2,
            "module_link": bool(row.get("in_lipid_lysosomal_myeloid_neighborhood"))
            or f(row.get("local_positive_disease_count")) >= 3
            or f(row.get("residual_retained_disease_count")) >= 2,
            "druggable_or_modality": f(row.get("druggable_activity_count")) >= 10 or bool(str(row.get("chembl_target_id", "")).strip()),
            "no_manual_blocker": not bool(str(row.get("manual_blocker", "")).strip()),
            "no_prior_context_blocker": not bool(str(row.get("prior_context_blocker", "")).strip()),
        }
        for gate, passed in gates.items():
            rows.append(
                {
                    "gene": row["gene"],
                    "gate": gate,
                    "passed": passed,
                    "wave62_call": row["wave62_call"],
                }
            )
    return pd.DataFrame(rows)


def md_table(df: pd.DataFrame) -> str:
    if df.empty:
        return ""
    formatted = df.copy()
    for col in formatted.columns:
        formatted[col] = formatted[col].map(
            lambda value: ""
            if value is None or (isinstance(value, float) and math.isnan(value))
            else str(value).replace("|", "\\|").replace("\n", " ")
        )
    header = "| " + " | ".join(formatted.columns) + " |"
    separator = "| " + " | ".join(["---"] * len(formatted.columns)) + " |"
    body = ["| " + " | ".join(row) + " |" for row in formatted.astype(str).values.tolist()]
    return "\n".join([header, separator, *body])


def write_report(summary: pd.DataFrame, payload: dict[str, Any]) -> None:
    top_cols = [
        "gene",
        "wave62_call",
        "wave62_score",
        "manual_blocker",
        "prior_context_blocker",
        "max_l2g_score",
        "best_l2g_disease",
        "strong_l2g_disease_count",
        "strong_l2g_diseases",
        "ms_max_l2g_score",
        "ms_max_relevant_qtl_h4",
        "ms_relevant_qtl_biosamples",
        "local_positive_disease_count",
        "residual_retained_disease_count",
        "wave61_best_call",
    ]
    lines = [
        "# Wave62 Open Targets Target-Resolution Audit",
        "",
        f"Random seed: `{SEED}`.",
        "",
        "## Verdict",
        "",
        f"- Reopen calls: `{payload['reopen_count']}`.",
        f"- Park calls: `{payload['park_count']}`.",
        f"- No output is a therapeutic claim; target resolution still requires intervention, safety, and prior-art validation.",
        "",
        "## Top Target-Resolution Rows",
        "",
        md_table(summary[top_cols].head(20)) if not summary.empty else "No target rows.",
        "",
        "## Summary JSON",
        "",
        "```json",
        json.dumps(payload, indent=2, sort_keys=True, allow_nan=True),
        "```",
        "",
        "## Guardrail",
        "",
        "Open Targets L2G plus QTL colocalisation can prioritize a target but does not prove therapeutic causality. HLA/antigen-processing rows require especially strict intervention and host-defense review.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)

    studies = fetch_studies()
    studies.to_csv(OUT / "opentargets_studies.tsv", sep="\t", index=False)
    credible, l2g, coloc, caps = fetch_credible_sets(studies)
    credible.to_csv(OUT / "opentargets_credible_sets.tsv", sep="\t", index=False)
    l2g.to_csv(OUT / "opentargets_l2g_rows.tsv", sep="\t", index=False)
    coloc.to_csv(OUT / "opentargets_qtl_coloc_rows.tsv", sep="\t", index=False)
    caps.to_csv(OUT / "api_caps_and_errors.tsv", sep="\t", index=False)

    local_context = {
        "broad": read_tsv(INPUTS["broad_h5ad"]),
        "residual": read_tsv(INPUTS["broad_residual"]),
        "wave34": read_tsv(INPUTS["wave34"]),
        "wave34a": read_tsv(INPUTS["wave34a"]),
        "wave55": read_tsv(INPUTS["wave55"]),
        "wave61": read_tsv(INPUTS["wave61"]),
    }
    target_summary = summarize_targets(l2g, coloc, local_context)
    gates = gate_matrix(target_summary)
    target_summary.to_csv(OUT / "target_resolution_summary.tsv", sep="\t", index=False)
    gates.to_csv(OUT / "target_resolution_gate_matrix.tsv", sep="\t", index=False)

    payload = {
        "seed": SEED,
        "inputs": {k: rel(v) for k, v in INPUTS.items() if v.exists()},
        "diseases": DISEASES,
        "caps": {
            "max_studies_per_disease": MAX_STUDIES_PER_DISEASE,
            "max_credible_sets_per_study": MAX_CREDIBLE_SETS_PER_STUDY,
            "l2g_page_size": L2G_PAGE_SIZE,
            "coloc_page_size": COLOC_PAGE_SIZE,
        },
        "n_study_rows": int(len(studies)),
        "n_eligible_gwas_studies": int(
            (
                (studies.get("study_type", pd.Series(dtype=str)).astype(str) == "gwas")
                & studies.get("has_sumstats", pd.Series(dtype=bool)).astype(bool)
                & (pd.to_numeric(studies.get("credible_set_count", pd.Series(dtype=float)), errors="coerce").fillna(0) > 0)
            ).sum()
        )
        if not studies.empty
        else 0,
        "n_credible_sets": int(len(credible)),
        "n_l2g_rows": int(len(l2g)),
        "n_qtl_coloc_rows": int(len(coloc)),
        "n_targets": int(len(target_summary)),
        "reopen_count": int(target_summary["wave62_call"].astype(str).str.startswith("REOPEN").sum()) if not target_summary.empty else 0,
        "park_count": int(target_summary["wave62_call"].astype(str).str.startswith("PARK").sum()) if not target_summary.empty else 0,
        "top_targets": target_summary.head(15)["gene"].tolist() if not target_summary.empty else [],
        "interpretation": "Target-resolution triage only. L2G/QTL colocalisation is not therapeutic causality.",
    }
    write_json(OUT / "summary.json", payload)
    write_report(target_summary, payload)
    print(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True))


if __name__ == "__main__":
    main()
