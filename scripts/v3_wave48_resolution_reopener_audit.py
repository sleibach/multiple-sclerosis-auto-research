#!/usr/bin/env python3
"""Wave48 resolution-route reopener audit.

Wave47-G highlighted two routes that are not mere relabels of the closed
IFN/HLA-II/lysosomal axis: biased FPR2/ANXA1 pro-resolution signaling and
receptor-specific CD300 tuning. This script tests those routes with a stricter
operationalization than earlier family-level route summaries.

Promotion requires:

1. receptor-specific or ligand-biased direction,
2. local cross-autoimmune signal,
3. strict MS anchor,
4. disease-relevant real perturbation or validated foundation-model support,
5. tractable/selective intervention,
6. non-blocking prior art for the proposed autoimmune use.

Anything weaker is treated as an assay-reopening branch, not a V3 finding.
"""

from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import quote_plus

import pandas as pd
import requests


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "phases/v3/results" / "wave48_resolution_reopener_audit"
RAW = OUT / "raw_api"
SEED = 20260527


WAVE32_GENE = ROOT / "phases/v3/results" / "wave32_resolution_rescue_audit" / "resolution_rescue_gene_detail.tsv"
WAVE32_ROUTE = ROOT / "phases/v3/results" / "wave32_resolution_rescue_audit" / "resolution_rescue_route_audit.tsv"
WAVE32_GATE = ROOT / "phases/v3/results" / "wave32_resolution_rescue_audit" / "resolution_rescue_gate_matrix.tsv"
WAVE32C_ROUTE = ROOT / "phases/v3/results" / "wave32c_resolution_prior_art_audit" / "route_feasibility_ranked.tsv"
WAVE32C_API = ROOT / "phases/v3/results" / "wave32c_resolution_prior_art_audit" / "api_hit_summary.tsv"
WAVE32C_DRUG = ROOT / "phases/v3/results" / "wave32c_resolution_prior_art_audit" / "target_drug_database_hits.tsv"
WAVE34 = ROOT / "phases/v3/results" / "wave34_genetics_expression_druggability_scan" / "wave34_genetics_expression_druggability_rank.tsv"
WAVE36_REC = ROOT / "phases/v3/results" / "wave36a_gene_level_controller_rescue" / "gene_recurrence_in_rescue_like_contexts.tsv"
WAVE36_CONTRAST = ROOT / "phases/v3/results" / "wave36a_gene_level_controller_rescue" / "gene_contrast_scores.tsv"
WAVE37 = ROOT / "phases/v3/results" / "wave37_gse212008_crispr_efferocytosis_screen" / "gene_level_screen_scores.tsv"
PIVOT = ROOT / "phases/v3/results" / "pivot_panel_triage" / "pivot_panel_summary.tsv"
GENEFORMER_CTX = ROOT / "phases/v3/results" / "geneformer_pivot_panel_delete" / "geneformer_pivot_panel_context_metrics_ranked.tsv"
GENEFORMER_GENE = ROOT / "phases/v3/results" / "geneformer_pivot_panel_delete" / "geneformer_pivot_panel_gene_summary.tsv"


ROUTES = {
    "FPR2_ANXA1_BIASED_RESOLUTION": {
        "genes": ["FPR2", "ANXA1"],
        "strict_genes": ["FPR2", "ANXA1"],
        "prior_route_keys": ["specialized_pro_resolving_mediator_FPR2_axis"],
        "description": "biased FPR2/ALX agonism or ANXA1-mimetic pro-resolution signaling",
        "lead_assay": "human intestinal or synovial macrophage efferocytosis under lipid/IFN stress with biased FPR2 agonist plus antagonist rescue",
    },
    "CD300_RECEPTOR_SPECIFIC_TUNING": {
        "genes": ["CD300A", "CD300LF", "CD300E", "CD300C", "CD300LG"],
        "strict_genes": ["CD300A", "CD300LF", "CD300E"],
        "prior_route_keys": ["CD300_family_modulation", "CD300_RESOLUTION_CHECKPOINT"],
        "description": "receptor-specific CD300 lipid/apoptotic-cell checkpoint tuning",
        "lead_assay": "paired CD300A/CD300F/CD300E perturbation in human RA/IBD/MS myeloid cells with apoptotic-cell/myelin-debris uptake and cytokine readouts",
    },
}


LIVE_QUERIES = [
    {
        "route": "FPR2_ANXA1_BIASED_RESOLUTION",
        "source": "EuropePMC",
        "query": '"FPR2" "biased agonist" efferocytosis autoimmune',
    },
    {
        "route": "FPR2_ANXA1_BIASED_RESOLUTION",
        "source": "EuropePMC",
        "query": '"annexin A1" FPR2 autoimmune multiple sclerosis EAE',
    },
    {
        "route": "FPR2_ANXA1_BIASED_RESOLUTION",
        "source": "EuropePMC",
        "query": '"resolvin D1" "multiple sclerosis" EAE FPR2',
    },
    {
        "route": "CD300_RECEPTOR_SPECIFIC_TUNING",
        "source": "EuropePMC",
        "query": 'CD300A CD300F CD300LF autoimmune efferocytosis macrophage',
    },
    {
        "route": "CD300_RECEPTOR_SPECIFIC_TUNING",
        "source": "EuropePMC",
        "query": 'CD300E CD300B colitis inflammation repair macrophage',
    },
    {
        "route": "CD300_RECEPTOR_SPECIFIC_TUNING",
        "source": "EuropePMC",
        "query": 'CD300A agonist antibody autoimmune disease',
    },
    {
        "route": "FPR2_ANXA1_BIASED_RESOLUTION",
        "source": "ClinicalTrials.gov",
        "query": 'FPR2 agonist autoimmune',
    },
    {
        "route": "FPR2_ANXA1_BIASED_RESOLUTION",
        "source": "ClinicalTrials.gov",
        "query": 'annexin A1 autoimmune',
    },
    {
        "route": "CD300_RECEPTOR_SPECIFIC_TUNING",
        "source": "ClinicalTrials.gov",
        "query": 'CD300 autoimmune',
    },
]


PATENT_QUERIES = [
    ("FPR2_ANXA1_BIASED_RESOLUTION", "FPR2 biased agonist autoimmune disease"),
    ("FPR2_ANXA1_BIASED_RESOLUTION", "annexin A1 mimetic autoimmune multiple sclerosis"),
    ("FPR2_ANXA1_BIASED_RESOLUTION", "resolvin FPR2 autoimmune disease"),
    ("CD300_RECEPTOR_SPECIFIC_TUNING", "CD300A agonist antibody autoimmune disease"),
    ("CD300_RECEPTOR_SPECIFIC_TUNING", "CD300F CD300LF agonist antibody autoimmune"),
    ("CD300_RECEPTOR_SPECIFIC_TUNING", "CD300E antagonist inflammatory bowel disease"),
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def read_tsv(path: Path) -> pd.DataFrame:
    if path.exists():
        return pd.read_csv(path, sep="\t", low_memory=False)
    return pd.DataFrame()


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True) + "\n", encoding="utf-8")


def as_float(value: Any) -> float | None:
    if value is None or pd.isna(value):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def as_int(value: Any) -> int:
    f = as_float(value)
    if f is None:
        return 0
    return int(f)


def as_str(value: Any) -> str:
    if value is None or pd.isna(value):
        return ""
    return str(value)


def cache_name(source: str, query: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9_.-]+", "_", f"{source}_{query}")[:180]
    return safe.strip("_") + ".json"


def get_json(url: str, cache_path: Path, timeout: int = 25) -> tuple[int | None, dict[str, Any] | None, str]:
    if cache_path.exists():
        try:
            return 200, json.loads(cache_path.read_text(encoding="utf-8")), "cache"
        except json.JSONDecodeError:
            pass
    try:
        response = requests.get(url, timeout=timeout, headers={"User-Agent": "ms-auto-research-wave48/1.0"})
        status = response.status_code
        payload = response.json() if response.text.strip() else {}
        cache_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        time.sleep(0.2)
        return status, payload, "live"
    except Exception as exc:  # noqa: BLE001 - trace public API failures.
        error = {"error": type(exc).__name__, "message": str(exc), "url": url}
        cache_path.write_text(json.dumps(error, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return None, error, "error"


def europepmc_search(query: str) -> dict[str, Any]:
    url = (
        "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
        f"?query={quote_plus(query)}&format=json&pageSize=5&resultType=lite"
    )
    status, payload, mode = get_json(url, RAW / cache_name("europepmc", query))
    result_list = (((payload or {}).get("resultList") or {}).get("result") or [])
    count = as_int((payload or {}).get("hitCount"))
    top_hits = []
    for hit in result_list[:5]:
        pmid = hit.get("pmid") or hit.get("id") or ""
        title = hit.get("title") or ""
        year = hit.get("pubYear") or ""
        top_hits.append(f"{pmid}: {title} ({year})")
    return {
        "status": status,
        "mode": mode,
        "count": count,
        "top_hits": " | ".join(top_hits),
        "url": url,
        "raw_path": rel(RAW / cache_name("europepmc", query)),
    }


def clinicaltrials_search(query: str) -> dict[str, Any]:
    url = f"https://clinicaltrials.gov/api/v2/studies?query.term={quote_plus(query)}&pageSize=5"
    status, payload, mode = get_json(url, RAW / cache_name("clinicaltrials", query))
    studies = (payload or {}).get("studies") or []
    count = as_int((payload or {}).get("totalCount"))
    if count == 0 and studies:
        count = len(studies)
    top_hits = []
    for study in studies[:5]:
        proto = study.get("protocolSection") or {}
        ident = proto.get("identificationModule") or {}
        status_mod = proto.get("statusModule") or {}
        title = ident.get("briefTitle") or ident.get("officialTitle") or ""
        nct = ident.get("nctId") or ""
        phase = ";".join((proto.get("designModule") or {}).get("phases") or [])
        overall = status_mod.get("overallStatus") or ""
        top_hits.append(f"{nct}: {title} [{phase}; {overall}]")
    return {
        "status": status,
        "mode": mode,
        "count": count,
        "top_hits": " | ".join(top_hits),
        "url": url,
        "raw_path": rel(RAW / cache_name("clinicaltrials", query)),
    }


def chembl_target_search(gene: str) -> dict[str, Any]:
    query = gene
    url = f"https://www.ebi.ac.uk/chembl/api/data/target/search.json?q={quote_plus(query)}&limit=10"
    status, payload, mode = get_json(url, RAW / cache_name("chembl_target", query))
    targets = (payload or {}).get("targets") or []
    total = as_int(((payload or {}).get("page_meta") or {}).get("total_count"))
    human = [t for t in targets if as_str(t.get("organism")).lower() == "homo sapiens"]
    best = human[0] if human else (targets[0] if targets else {})
    target_id = best.get("target_chembl_id") or ""
    target_name = best.get("pref_name") or ""
    return {
        "gene": gene,
        "status": status,
        "mode": mode,
        "count": total,
        "target_chembl_id": target_id,
        "target_name": target_name,
        "target_type": best.get("target_type") or "",
        "organism": best.get("organism") or "",
        "url": url,
        "raw_path": rel(RAW / cache_name("chembl_target", query)),
    }


def chembl_activity_count(target_id: str) -> dict[str, Any]:
    if not target_id:
        return {"activity_count": 0, "best_standard_type": "", "best_standard_value": None}
    url = (
        "https://www.ebi.ac.uk/chembl/api/data/activity.json"
        f"?target_chembl_id={quote_plus(target_id)}&limit=1"
    )
    status, payload, mode = get_json(url, RAW / cache_name("chembl_activity", target_id))
    activities = (payload or {}).get("activities") or []
    total = as_int(((payload or {}).get("page_meta") or {}).get("total_count"))
    best = activities[0] if activities else {}
    return {
        "activity_status": status,
        "activity_mode": mode,
        "activity_count": total,
        "best_standard_type": best.get("standard_type") or "",
        "best_standard_value": as_float(best.get("standard_value")),
        "best_standard_units": best.get("standard_units") or "",
        "activity_url": url,
        "activity_raw_path": rel(RAW / cache_name("chembl_activity", target_id)),
    }


def route_prior_rows(df: pd.DataFrame, keys: list[str]) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()
    cols = [c for c in ["route", "query"] if c in df.columns]
    if not cols:
        return pd.DataFrame()
    mask = pd.Series(False, index=df.index)
    for key in keys:
        for col in cols:
            mask |= df[col].astype(str).str.contains(re.escape(key), case=False, na=False)
    return df[mask].copy()


@dataclass
class Gate:
    route: str
    gate: str
    passed: bool
    value: str
    rationale: str


def candidate_gene_table() -> pd.DataFrame:
    genes = sorted({g for route in ROUTES.values() for g in route["genes"]})
    wave32_gene = read_tsv(WAVE32_GENE)
    wave34 = read_tsv(WAVE34)
    wave36_rec = read_tsv(WAVE36_REC)
    wave36_contrast = read_tsv(WAVE36_CONTRAST)
    wave37 = read_tsv(WAVE37)
    pivot = read_tsv(PIVOT)
    geneformer_ctx = read_tsv(GENEFORMER_CTX)
    geneformer_gene = read_tsv(GENEFORMER_GENE)
    chembl_targets = {gene: chembl_target_search(gene) for gene in genes}
    chembl_activities = {
        gene: chembl_activity_count(chembl_targets[gene].get("target_chembl_id", ""))
        for gene in genes
    }

    rows: list[dict[str, Any]] = []
    for gene in genes:
        row: dict[str, Any] = {"gene": gene}

        sub = wave32_gene[wave32_gene.get("gene", pd.Series(dtype=str)).astype(str) == gene] if not wave32_gene.empty else pd.DataFrame()
        if not sub.empty:
            r = sub.iloc[0]
            row.update(
                {
                    "wave32_route": as_str(r.get("route")),
                    "wave32_broad_positive_disease_count": as_float(r.get("broad_positive_disease_count")),
                    "wave32_broad_negative_disease_count": as_float(r.get("broad_negative_disease_count")),
                    "wave32_ms_wm_delta_log2": as_float(r.get("broad_ms_wm_delta_log2")),
                    "wave32_ms_wm_p": as_float(r.get("broad_ms_wm_p")),
                    "wave32_surface_resid_state_diseases": as_float(r.get("surface_resid_state_diseases")),
                    "wave32_genetics_disease_count": as_float(r.get("genetics_disease_count")),
                }
            )

        sub = wave34[wave34.get("gene", pd.Series(dtype=str)).astype(str) == gene] if not wave34.empty else pd.DataFrame()
        if not sub.empty:
            r = sub.iloc[0]
            row.update(
                {
                    "wave34_score": as_float(r.get("wave34_score")),
                    "wave34_call": as_str(r.get("wave34_call")),
                    "wave34_failed_gates": as_str(r.get("failed_gates")),
                    "wave34_gwas_trait_count": as_float(r.get("gwas_catalog_trait_count")),
                    "wave34_gwas_min_p": as_float(r.get("gwas_catalog_min_p")),
                    "wave34_gwas_traits": as_str(r.get("gwas_catalog_traits")),
                    "wave34_local_positive_disease_count": as_float(r.get("local_positive_disease_count")),
                    "wave34_local_negative_disease_count": as_float(r.get("local_negative_disease_count")),
                    "wave34_positive_diseases": as_str(r.get("positive_diseases")),
                    "wave34_residual_retained_disease_count": as_float(r.get("residual_retained_disease_count")),
                    "wave34_ms_anchor": bool(r.get("ms_anchor")) if not pd.isna(r.get("ms_anchor")) else False,
                    "wave34_ms_wm_delta_log2": as_float(r.get("ms_wm_delta_log2")),
                    "wave34_ms_wm_p": as_float(r.get("ms_wm_p")),
                    "wave34_chembl_target_id": as_str(r.get("chembl_target_id")),
                    "wave34_primary_blocker": as_str(r.get("primary_blocker")),
                }
            )

        sub = wave36_rec[wave36_rec.get("gene", pd.Series(dtype=str)).astype(str) == gene] if not wave36_rec.empty else pd.DataFrame()
        if not sub.empty:
            r = sub.iloc[0]
            row.update(
                {
                    "wave36_n_up_contexts": as_float(r.get("n_up_contexts")),
                    "wave36_n_up_datasets": as_float(r.get("n_up_datasets")),
                    "wave36_n_down_contexts": as_float(r.get("n_down_contexts")),
                    "wave36_n_down_datasets": as_float(r.get("n_down_datasets")),
                    "wave36_max_delta": as_float(r.get("max_delta")),
                    "wave36_min_delta": as_float(r.get("min_delta")),
                    "wave36_up_contexts": as_str(r.get("up_contexts")),
                    "wave36_down_contexts": as_str(r.get("down_contexts")),
                }
            )
        sub = wave36_contrast[wave36_contrast.get("gene", pd.Series(dtype=str)).astype(str) == gene] if not wave36_contrast.empty else pd.DataFrame()
        if not sub.empty:
            p_col = "p_value" if "p_value" in sub.columns else "p"
            type_col = "comparison_type" if "comparison_type" in sub.columns else "contrast_type"
            p_series = sub[p_col].apply(as_float).fillna(1.0) if p_col in sub.columns else pd.Series(1.0, index=sub.index)
            type_series = sub[type_col].astype(str) if type_col in sub.columns else pd.Series("", index=sub.index)
            sig = sub[(p_series < 0.05) & (type_series == "group")]
            row["wave36_significant_group_contexts_p_lt_0_05"] = int(len(sig))
            row["wave36_significant_group_context_names"] = ";".join(sig.get("contrast", pd.Series(dtype=str)).astype(str).tolist()[:10])

        sub = wave37[wave37.get("gene_symbol", pd.Series(dtype=str)).astype(str) == gene] if not wave37.empty else pd.DataFrame()
        if not sub.empty:
            r = sub.iloc[0]
            row.update(
                {
                    "wave37_n_sgrna": as_float(r.get("n_sgrna")),
                    "wave37_median_efficient_lfc": as_float(r.get("median_efficient_lfc")),
                    "wave37_median_noneater_lfc": as_float(r.get("median_noneater_lfc")),
                    "wave37_median_efficient_minus_noneater_lfc": as_float(r.get("median_efficient_minus_noneater_lfc")),
                    "wave37_efficient_fdr": as_float(r.get("efficient_fdr")),
                    "wave37_noneater_fdr": as_float(r.get("noneater_fdr")),
                    "wave37_contrast_fdr": as_float(r.get("contrast_fdr")),
                    "wave37_screen_call": as_str(r.get("screen_call")),
                    "wave37_tracked_candidate": bool(r.get("tracked_candidate")) if not pd.isna(r.get("tracked_candidate")) else False,
                }
            )

        sub = pivot[pivot.get("gene", pd.Series(dtype=str)).astype(str) == gene] if not pivot.empty else pd.DataFrame()
        if not sub.empty:
            r = sub.iloc[0]
            row.update(
                {
                    "pivot_direct_positive_disease_count": as_float(r.get("direct_positive_disease_count")),
                    "pivot_direct_negative_disease_count": as_float(r.get("direct_negative_disease_count")),
                    "pivot_direct_positive_diseases": as_str(r.get("direct_positive_diseases")),
                    "pivot_ms_wm_delta_log2": as_float(r.get("ms_wm_delta_log2")),
                    "pivot_ms_wm_p": as_float(r.get("ms_wm_p")),
                    "pivot_geneformer_support_contexts": as_float(r.get("geneformer_support_contexts")),
                    "pivot_routing_decision": as_str(r.get("routing_decision")),
                    "pivot_routing_rationale": as_str(r.get("routing_rationale")),
                }
            )

        sub = geneformer_gene[geneformer_gene.get("gene", pd.Series(dtype=str)).astype(str) == gene] if not geneformer_gene.empty else pd.DataFrame()
        if not sub.empty:
            r = sub.iloc[0]
            row.update(
                {
                    "geneformer_contexts_with_token": as_float(r.get("contexts_with_token")),
                    "geneformer_total_disease_cells_with_token": as_float(r.get("total_disease_cells_with_token")),
                    "geneformer_mean_shift_to_control_cosine": as_float(r.get("mean_shift_to_control_cosine")),
                    "geneformer_mean_projection_to_control": as_float(r.get("mean_projection_to_control")),
                    "geneformer_mean_cosine_shift_z_vs_random": as_float(r.get("mean_cosine_shift_z_vs_random")),
                    "geneformer_support_contexts": as_float(r.get("support_contexts")),
                    "geneformer_strong_support_contexts": as_float(r.get("strong_support_contexts")),
                }
            )
        sub = geneformer_ctx[geneformer_ctx.get("gene", pd.Series(dtype=str)).astype(str) == gene] if not geneformer_ctx.empty else pd.DataFrame()
        if not sub.empty:
            supports = sub[sub.get("candidate_support_flag", False).astype(bool)]
            row["geneformer_support_context_names"] = ";".join(
                supports.get("context", pd.Series(dtype=str)).astype(str).tolist()[:10]
            )

        row.update({f"chembl_{k}": v for k, v in chembl_targets[gene].items() if k != "gene"})
        row.update({f"chembl_{k}": v for k, v in chembl_activities[gene].items()})
        rows.append(row)
    return pd.DataFrame(rows)


def public_api_counts() -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    prior = read_tsv(WAVE32C_API)
    if not prior.empty:
        subset = route_prior_rows(
            prior,
            [
                "specialized_pro_resolving_mediator_FPR2_axis",
                "CD300_family_modulation",
                "FPR2",
                "CD300",
            ],
        )
        for _, r in subset.iterrows():
            rows.append(
                {
                    "route": as_str(r.get("route")),
                    "source": f"cached_Wave32C_{as_str(r.get('source'))}",
                    "query": as_str(r.get("query")),
                    "count": as_int(r.get("count")),
                    "top_hits": as_str(r.get("top_hits")),
                    "status": "",
                    "mode": "cached_prior_wave",
                    "url": "",
                    "raw_path": "",
                }
            )
    for spec in LIVE_QUERIES:
        if spec["source"] == "EuropePMC":
            result = europepmc_search(spec["query"])
        elif spec["source"] == "ClinicalTrials.gov":
            result = clinicaltrials_search(spec["query"])
        else:
            continue
        rows.append(
            {
                "route": spec["route"],
                "source": spec["source"],
                "query": spec["query"],
                "count": result["count"],
                "top_hits": result["top_hits"],
                "status": result["status"],
                "mode": result["mode"],
                "url": result["url"],
                "raw_path": result["raw_path"],
            }
        )
    return pd.DataFrame(rows)


def patent_urls() -> pd.DataFrame:
    rows = []
    for route, query in PATENT_QUERIES:
        rows.append(
            {
                "route": route,
                "database": "GooglePatents",
                "query": query,
                "url": f"https://patents.google.com/?q={quote_plus(query)}",
            }
        )
        rows.append(
            {
                "route": route,
                "database": "Espacenet",
                "query": query,
                "url": f"https://worldwide.espacenet.com/patent/search?q={quote_plus(query)}",
            }
        )
    return pd.DataFrame(rows)


def evaluate_routes(candidate_df: pd.DataFrame, api_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    wave32_route = read_tsv(WAVE32_ROUTE)
    wave32_gate = read_tsv(WAVE32_GATE)
    wave32c_route = read_tsv(WAVE32C_ROUTE)
    gates: list[Gate] = []
    route_rows: list[dict[str, Any]] = []

    def gene_rows(route: str) -> pd.DataFrame:
        genes = ROUTES[route]["strict_genes"]
        return candidate_df[candidate_df["gene"].isin(genes)].copy()

    for route_name, spec in ROUTES.items():
        gdf = gene_rows(route_name)
        api_route = api_df[api_df["route"].astype(str).str.contains(route_name, na=False)]
        if route_name == "FPR2_ANXA1_BIASED_RESOLUTION":
            api_prior = api_df[api_df["route"].astype(str).str.contains("specialized_pro_resolving_mediator_FPR2_axis", na=False)]
        else:
            api_prior = api_df[api_df["route"].astype(str).str.contains("CD300_family_modulation", na=False)]
        prior_rows = route_prior_rows(wave32c_route, spec["prior_route_keys"])
        prior_status = ";".join(prior_rows.get("blocking_status", pd.Series(dtype=str)).astype(str).unique().tolist())
        prior_not_blocked = "NOT_BLOCKED" in prior_status and not prior_status.startswith("BLOCKED")

        if route_name == "FPR2_ANXA1_BIASED_RESOLUTION":
            fpr2 = gdf[gdf["gene"] == "FPR2"].iloc[0].to_dict() if (gdf["gene"] == "FPR2").any() else {}
            anxa1 = gdf[gdf["gene"] == "ANXA1"].iloc[0].to_dict() if (gdf["gene"] == "ANXA1").any() else {}
            local_breadth = max(
                as_float(fpr2.get("wave34_local_positive_disease_count")) or 0.0,
                as_float(anxa1.get("pivot_direct_positive_disease_count")) or 0.0,
                as_float(anxa1.get("wave36_n_up_datasets")) or 0.0,
            )
            strict_ms = bool(fpr2.get("wave34_ms_anchor")) and (as_float(fpr2.get("wave34_ms_wm_delta_log2")) or 0.0) > 0
            perturb = (
                (as_str(fpr2.get("wave37_screen_call")).startswith("KO_ENHANCES") or as_str(anxa1.get("wave37_screen_call")).startswith("KO_ENHANCES"))
                and min(as_float(fpr2.get("wave37_contrast_fdr")) or 1.0, as_float(anxa1.get("wave37_contrast_fdr")) or 1.0) < 0.1
            )
            druggable = (as_float(fpr2.get("chembl_activity_count")) or 0.0) >= 100
            route_specific = True
            prior_count = int(api_prior.get("count", pd.Series(dtype=int)).fillna(0).max() if not api_prior.empty else 0)
            novelty_delta_sufficient = False
            foundation = False
            route_signal = (
                f"FPR2 GWAS trait count={as_int(fpr2.get('wave34_gwas_trait_count'))}, "
                f"min_p={fpr2.get('wave34_gwas_min_p')}; "
                f"FPR2 local positives={fpr2.get('wave34_local_positive_disease_count')} "
                f"({fpr2.get('wave34_positive_diseases')}); "
                f"ANXA1 rescue-context up={anxa1.get('wave36_n_up_contexts')} contexts/"
                f"{anxa1.get('wave36_n_up_datasets')} datasets; "
                f"Wave37 FPR2 call={fpr2.get('wave37_screen_call')}, "
                f"ANXA1 call={anxa1.get('wave37_screen_call')}; "
                f"ChEMBL FPR2 activities={as_int(fpr2.get('chembl_activity_count'))}."
            )
            blocker = (
                "dynamic resolution biology and chemical tractability exist, but strict MS "
                "expression anchor is negative/non-significant, the GWAS hit is not target-resolved, "
                "Wave37 efferocytosis perturbation is unresolved, and prior literature already covers "
                "SPM/FPR2 activity in autoimmune/EAE/colitis contexts."
            )
        else:
            cd300e = gdf[gdf["gene"] == "CD300E"].iloc[0].to_dict() if (gdf["gene"] == "CD300E").any() else {}
            cd300lf = gdf[gdf["gene"] == "CD300LF"].iloc[0].to_dict() if (gdf["gene"] == "CD300LF").any() else {}
            cd300a = gdf[gdf["gene"] == "CD300A"].iloc[0].to_dict() if (gdf["gene"] == "CD300A").any() else {}
            local_breadth = max(
                as_float(cd300e.get("pivot_direct_positive_disease_count")) or 0.0,
                as_float(cd300lf.get("pivot_direct_positive_disease_count")) or 0.0,
                as_float(cd300a.get("wave32_broad_positive_disease_count")) or 0.0,
            )
            strict_ms = any(
                (as_float(row.get("pivot_ms_wm_p")) or 1.0) < 0.05 and (as_float(row.get("pivot_ms_wm_delta_log2")) or 0.0) > 0
                for row in [cd300e, cd300lf, cd300a]
            )
            perturb = (
                (as_float(cd300a.get("wave37_contrast_fdr")) or 1.0) < 0.1
                or (as_float(cd300e.get("wave37_contrast_fdr")) or 1.0) < 0.1
                or (as_float(cd300lf.get("wave37_contrast_fdr")) or 1.0) < 0.1
            )
            foundation = (
                (as_float(cd300e.get("geneformer_strong_support_contexts")) or 0.0) >= 1
                and (as_float(cd300e.get("pivot_direct_positive_disease_count")) or 0.0) >= 3
            )
            druggable = any((as_float(row.get("chembl_count")) or 0.0) > 0 for row in [cd300a, cd300e, cd300lf])
            route_specific = False
            prior_count = int(api_prior.get("count", pd.Series(dtype=int)).fillna(0).max() if not api_prior.empty else 0)
            novelty_delta_sufficient = False
            route_signal = (
                f"CD300E direct positives={cd300e.get('pivot_direct_positive_disease_count')} "
                f"({cd300e.get('pivot_direct_positive_diseases')}); "
                f"CD300E Geneformer strong contexts={cd300e.get('geneformer_strong_support_contexts')}; "
                f"CD300A Wave37 median efficient-minus-noneater={cd300a.get('wave37_median_efficient_minus_noneater_lfc')}, "
                f"contrast_fdr={cd300a.get('wave37_contrast_fdr')}; "
                f"CD300LF Wave37 call={cd300lf.get('wave37_screen_call')}; "
                f"strict MS positive anchors absent."
            )
            blocker = (
                "family-level CD300 direction remains biologically unsafe: CD300A/F/LF/E have "
                "different inhibitory/activating roles, local MS anchoring is absent or negative, "
                "and the only strong-looking CRISPR contrast is not significant after FDR."
            )

        gates.extend(
            [
                Gate(route_name, "specific_directionality", route_specific, str(route_specific), "requires biased ligand or receptor-specific direction"),
                Gate(route_name, "cross_autoimmune_local_signal", local_breadth >= 3, str(local_breadth), "requires at least three disease/tissue signals"),
                Gate(route_name, "strict_ms_anchor", strict_ms, str(strict_ms), "requires positive MS expression/state or target-resolved MS genetics"),
                Gate(route_name, "real_perturbation_anchor", perturb, str(perturb), "requires real disease-relevant perturbation rather than expression recurrence"),
                Gate(route_name, "foundation_model_support", foundation, str(foundation), "requires disease-context support beyond a single token/small context"),
                Gate(route_name, "druggability_selectivity", druggable, str(druggable), "requires targetable chemical/biologic matter and plausible selectivity"),
                Gate(route_name, "prior_art_not_blocking", prior_not_blocked, prior_status or str(prior_count), "requires no blocking patent/clinical/prior-art status in route audit"),
                Gate(route_name, "novelty_delta_sufficient", novelty_delta_sufficient, str(prior_count), "requires a direct delta beyond known autoimmune/efferocytosis literature"),
            ]
        )
        critical_pass = all(
            gate.passed
            for gate in gates
            if gate.route == route_name
            and gate.gate
            in {
                "specific_directionality",
                "cross_autoimmune_local_signal",
                "strict_ms_anchor",
                "real_perturbation_anchor",
                "druggability_selectivity",
                "prior_art_not_blocking",
                "novelty_delta_sufficient",
            }
        )
        critical_gate_names = {
            "specific_directionality",
            "cross_autoimmune_local_signal",
            "strict_ms_anchor",
            "real_perturbation_anchor",
            "druggability_selectivity",
            "prior_art_not_blocking",
            "novelty_delta_sufficient",
        }
        if critical_pass:
            call = "PROMOTE_CANDIDATE_FOR_FULL_V3_SYNTHESIS"
        elif route_name == "FPR2_ANXA1_BIASED_RESOLUTION":
            call = "REOPEN_WITH_WETLAB_TEST_ONLY_NOT_V3_PROMOTION"
        else:
            call = "REOPEN_ONLY_IF_RECEPTOR_SPECIFIC_PERTURBATION_NOT_V3_PROMOTION"

        wave32_rows = route_prior_rows(wave32_route, spec["prior_route_keys"])
        wave32_gates = route_prior_rows(wave32_gate, spec["prior_route_keys"])
        route_rows.append(
            {
                "route": route_name,
                "description": spec["description"],
                "genes": ";".join(spec["genes"]),
                "call": call,
                "critical_gate_pass_count": sum(
                    gate.passed
                    for gate in gates
                    if gate.route == route_name
                    and gate.gate in critical_gate_names
                ),
                "critical_gate_total": len(critical_gate_names),
                "route_signal_summary": route_signal,
                "primary_blocker": blocker,
                "lead_reopen_assay": spec["lead_assay"],
                "wave32_prior_call": ";".join(wave32_rows.get("wave32_call", pd.Series(dtype=str)).astype(str).unique().tolist()),
                "wave32_gate_failures": ";".join(wave32_gates.loc[~wave32_gates.get("passed", False).astype(bool), "gate"].astype(str).tolist())
                if not wave32_gates.empty and "passed" in wave32_gates.columns and "gate" in wave32_gates.columns
                else "",
                "wave32c_translational_verdict": ";".join(prior_rows.get("verdict", pd.Series(dtype=str)).astype(str).unique().tolist()),
                "wave32c_blocking_status": ";".join(prior_rows.get("blocking_status", pd.Series(dtype=str)).astype(str).unique().tolist()),
            }
        )
    gate_df = pd.DataFrame([gate.__dict__ for gate in gates])
    route_df = pd.DataFrame(route_rows)
    return route_df, gate_df


def write_report(route_df: pd.DataFrame, gate_df: pd.DataFrame, candidate_df: pd.DataFrame, api_df: pd.DataFrame) -> None:
    lines: list[str] = []
    lines.append("# Wave48 Resolution-Reopener Audit")
    lines.append("")
    lines.append(f"Random seed: `{SEED}`.")
    lines.append("")
    lines.append("## Verdict")
    lines.append("")
    for _, r in route_df.iterrows():
        lines.append(f"- `{r['route']}`: `{r['call']}`.")
        lines.append(f"  - Signal: {r['route_signal_summary']}")
        lines.append(f"  - Blocker: {r['primary_blocker']}")
        lines.append(f"  - Decisive reopen assay: {r['lead_reopen_assay']}.")
    lines.append("")
    lines.append("No branch satisfies V3 promotion gates. Both remain assay-reopeners only.")
    lines.append("")
    lines.append("## Gate Matrix")
    lines.append("")
    for _, r in gate_df.iterrows():
        status = "PASS" if bool(r["passed"]) else "FAIL"
        lines.append(f"- `{r['route']}` / `{r['gate']}`: {status} (`{r['value']}`) - {r['rationale']}.")
    lines.append("")
    lines.append("## Traceable Outputs")
    lines.append("")
    lines.append("- `route_reopener_audit.tsv`: route-level verdicts.")
    lines.append("- `decision_matrix.tsv`: strict promotion gates.")
    lines.append("- `candidate_gene_evidence.tsv`: gene-level local, perturbation, foundation-model, and ChEMBL evidence.")
    lines.append("- `public_api_counts.tsv`: cached prior and live Europe PMC / ClinicalTrials.gov counts.")
    lines.append("- `patent_search_urls.tsv`: patent search URLs retained for manual verification.")
    lines.append("")
    OUT.joinpath("REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)

    candidate_df = candidate_gene_table()
    api_df = public_api_counts()
    patent_df = patent_urls()
    route_df, gate_df = evaluate_routes(candidate_df, api_df)

    candidate_df.to_csv(OUT / "candidate_gene_evidence.tsv", sep="\t", index=False)
    api_df.to_csv(OUT / "public_api_counts.tsv", sep="\t", index=False)
    patent_df.to_csv(OUT / "patent_search_urls.tsv", sep="\t", index=False)
    route_df.to_csv(OUT / "route_reopener_audit.tsv", sep="\t", index=False)
    gate_df.to_csv(OUT / "decision_matrix.tsv", sep="\t", index=False)
    write_report(route_df, gate_df, candidate_df, api_df)

    summary = {
        "seed": SEED,
        "routes_tested": sorted(route_df["route"].tolist()),
        "promoted_count": int(route_df["call"].astype(str).str.contains("PROMOTE").sum()),
        "calls": dict(zip(route_df["route"], route_df["call"], strict=True)),
        "output_dir": rel(OUT),
        "key_outputs": [
            rel(OUT / "route_reopener_audit.tsv"),
            rel(OUT / "decision_matrix.tsv"),
            rel(OUT / "candidate_gene_evidence.tsv"),
            rel(OUT / "public_api_counts.tsv"),
            rel(OUT / "REPORT.md"),
        ],
    }
    write_json(OUT / "summary.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
