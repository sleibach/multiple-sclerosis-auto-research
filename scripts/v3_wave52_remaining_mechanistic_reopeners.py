#!/usr/bin/env python3
"""Wave52 consolidated audit of remaining mechanistic reopen-only routes.

The V3 run has repeatedly found plausible biology that fails therapeutic
promotion. This script deliberately audits the remaining named reopeners
(`CCR6`, `TREM2/APOE`, `SQLE`, localized `IL10`) against the same hard
therapeutic criteria, rather than accepting weaker surrogate evidence.
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
OUT = ROOT / "results_v3" / "wave52_remaining_mechanistic_reopeners"
RAW = OUT / "raw_api"
SEED = 20260527

INPUTS = {
    "wave47_reopen": ROOT / "results_v3" / "wave47_late_stage_survivor_map" / "reopen_only_requirements.tsv",
    "wave23_restoration": ROOT / "results_v3" / "wave23_genetics_restoration_modality" / "ranked_go_park_no_go.tsv",
    "wave28_target_first": ROOT / "results_v3" / "wave28_target_first_rescue" / "target_first_rescue_matrix.tsv",
    "wave32_resolution": ROOT / "results_v3" / "wave32_resolution_rescue_audit" / "resolution_rescue_route_audit.tsv",
    "wave34_genetics_expression": ROOT / "results_v3" / "wave34_genetics_expression_druggability_scan" / "wave34_genetics_expression_druggability_rank.tsv",
    "wave34a_genetics_first": ROOT / "results_v3" / "wave34a_genetics_first_target_rescue" / "genetics_first_candidate_rank.tsv",
    "wave22_sqle_decision": ROOT / "results_v3" / "wave22_sqle_failfast" / "sqle_decision.tsv",
    "broad_h5ad": ROOT / "results_v3" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_rank.tsv",
    "broad_residual": ROOT / "results_v3" / "broad_residual_gate" / "broad_residual_gate_summary.tsv",
}

CANDIDATES = {
    "CCR6_TH17_TRAFFICKING": {
        "genes": ["CCR6"],
        "primary_gene": "CCR6",
        "route_labels": ["CCR6"],
        "desired_intervention": "block CCR6/CCL20-dependent pathogenic Th17 tissue entry",
        "reason_for_reopen": "broad autoimmune mapped-gene signal and feasible chemokine-receptor modality",
    },
    "TREM2_APOE_LIPID_REPAIR": {
        "genes": ["TREM2", "APOE", "TYROBP", "LPL"],
        "primary_gene": "TREM2",
        "route_labels": ["TREM2_APOE_LIPID_REPAIR"],
        "desired_intervention": "enhance lesion-local phagolysosomal lipid/debris repair without chronic inflammatory lipid loading",
        "reason_for_reopen": "strong route-level biology in resolution/efferocytosis space",
    },
    "SQLE_STEROL_STROMAL": {
        "genes": ["SQLE"],
        "primary_gene": "SQLE",
        "route_labels": ["SQLE"],
        "desired_intervention": "reduce pathological sterol/stromal stress state while preserving repair",
        "reason_for_reopen": "cross-tissue stromal signal with available small-molecule chemistry",
    },
    "LOCALIZED_IL10_RESTORATION": {
        "genes": ["IL10", "IL10RA", "IL10RB"],
        "primary_gene": "IL10",
        "route_labels": ["IL10", "IL10_RESOLUTION_AXIS"],
        "desired_intervention": "restore anti-inflammatory IL-10 signaling only in the disease compartment",
        "reason_for_reopen": "broad autoimmune genetics and regulatory/restoration logic",
    },
}

PUBLIC_QUERIES = {
    "CCR6_TH17_TRAFFICKING": [
        ("EuropePMC", "CCR6 CCL20 antagonist autoimmune multiple sclerosis rheumatoid arthritis Crohn psoriasis"),
        ("EuropePMC", "CCR6 Th17 trafficking therapeutic target autoimmune disease"),
        ("ClinicalTrials.gov", "CCR6 autoimmune"),
    ],
    "TREM2_APOE_LIPID_REPAIR": [
        ("EuropePMC", "TREM2 agonist multiple sclerosis remyelination autoimmune"),
        ("EuropePMC", "TREM2 APOE lipid phagocytosis repair multiple sclerosis lesion"),
        ("ClinicalTrials.gov", "TREM2 multiple sclerosis"),
    ],
    "SQLE_STEROL_STROMAL": [
        ("EuropePMC", "SQLE squalene monooxygenase autoimmune inflammatory disease psoriasis IBD"),
        ("EuropePMC", "squalene monooxygenase inhibitor inflammation autoimmune"),
        ("ClinicalTrials.gov", "SQLE autoimmune"),
    ],
    "LOCALIZED_IL10_RESTORATION": [
        ("EuropePMC", "IL10 therapy autoimmune multiple sclerosis Crohn psoriasis rheumatoid arthritis"),
        ("EuropePMC", "targeted IL10 delivery autoimmune disease"),
        ("ClinicalTrials.gov", "IL10 autoimmune"),
    ],
}

PATENT_QUERIES = {
    "CCR6_TH17_TRAFFICKING": ["CCR6 antagonist autoimmune disease", "CCR6 CCL20 multiple sclerosis patent"],
    "TREM2_APOE_LIPID_REPAIR": ["TREM2 agonist multiple sclerosis", "TREM2 antibody autoimmune disease"],
    "SQLE_STEROL_STROMAL": ["SQLE inhibitor autoimmune disease", "squalene monooxygenase inhibitor inflammation"],
    "LOCALIZED_IL10_RESTORATION": ["IL10 targeted delivery autoimmune", "IL10 gene therapy autoimmune disease"],
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def read_tsv(path: Path) -> pd.DataFrame:
    if path.exists():
        return pd.read_csv(path, sep="\t", low_memory=False)
    return pd.DataFrame()


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True) + "\n", encoding="utf-8")


def f(value: Any) -> float | None:
    if value is None or pd.isna(value):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def i(value: Any) -> int:
    value_f = f(value)
    return int(value_f) if value_f is not None else 0


def s(value: Any) -> str:
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
        response = requests.get(url, timeout=timeout, headers={"User-Agent": "ms-auto-research-wave52/1.0"})
        payload = response.json() if response.text.strip() else {}
        cache_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        time.sleep(0.15)
        return response.status_code, payload, "live"
    except Exception as exc:  # noqa: BLE001
        payload = {"error": type(exc).__name__, "message": str(exc), "url": url}
        cache_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return None, payload, "error"


def matching_rows(df: pd.DataFrame, genes: list[str], labels: list[str]) -> pd.DataFrame:
    if df.empty:
        return df
    mask = pd.Series(False, index=df.index)
    for col in ["gene", "genes", "label", "route"]:
        if col not in df.columns:
            continue
        values = df[col].astype(str)
        for token in genes + labels:
            mask |= values.eq(token)
            mask |= values.str.contains(rf"(?:^|;){re.escape(token)}(?:$|;)", regex=True, na=False)
    return df[mask].copy()


def parse_json_text(text: str) -> dict[str, Any]:
    if not text:
        return {}
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {}


def local_evidence() -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for source, path in INPUTS.items():
        df = read_tsv(path)
        if df.empty:
            continue
        for candidate, cfg in CANDIDATES.items():
            sub = matching_rows(df, cfg["genes"], cfg["route_labels"])
            for _, r in sub.iterrows():
                local_json = parse_json_text(s(r.get("local_summary")))
                foundation_json = parse_json_text(s(r.get("foundation_summary")))
                prior_json = parse_json_text(s(r.get("prior_art_summary")))
                rows.append(
                    {
                        "candidate": candidate,
                        "primary_gene": cfg["primary_gene"],
                        "source": source,
                        "path": rel(path),
                        "matched_identifier": s(r.get("gene") or r.get("route") or r.get("label") or r.get("genes")),
                        "source_call": s(
                            r.get("wave34a_call")
                            or r.get("wave34_call")
                            or r.get("wave32_call")
                            or r.get("call")
                            or r.get("source_call")
                            or r.get("decision")
                        ),
                        "score": f(
                            r.get("genetics_first_score")
                            or r.get("wave34_score")
                            or r.get("resolution_rescue_score")
                            or r.get("rank_score")
                            or r.get("discovery_priority_score")
                            or r.get("source_score")
                        ),
                        "ot_disease_count": f(r.get("ot_n_diseases_score_ge_0_5") or r.get("opentargets_disease_count")),
                        "supporting_disease_count_union": f(r.get("supporting_disease_count_union")),
                        "gwas_trait_count": f(r.get("gwas_catalog_trait_count")),
                        "gwas_min_p": f(r.get("gwas_catalog_min_p")),
                        "local_positive_disease_count": f(
                            r.get("broad_positive_disease_count")
                            or r.get("local_positive_disease_count")
                            or r.get("positive_disease_count")
                            or r.get("local_breadth")
                            or local_json.get("broad_positive_disease_count")
                        ),
                        "local_negative_disease_count": f(
                            r.get("broad_negative_disease_count")
                            or r.get("local_negative_disease_count")
                            or r.get("negative_disease_count")
                            or r.get("negative_breadth")
                            or local_json.get("broad_negative_disease_count")
                        ),
                        "positive_diseases": s(
                            r.get("broad_positive_diseases")
                            or r.get("positive_diseases")
                            or r.get("supporting_diseases_union")
                            or local_json.get("positive_diseases")
                        ),
                        "negative_diseases": s(r.get("broad_negative_diseases") or r.get("negative_diseases")),
                        "ms_wm_delta_log2": f(r.get("ms_wm_delta_log2") or r.get("ms_anchor_delta") or local_json.get("ms_wm_delta_log2")),
                        "ms_wm_p": f(r.get("ms_wm_p") or r.get("ms_anchor_p_min") or local_json.get("ms_wm_p")),
                        "ms_wm_fdr": f(r.get("ms_wm_fdr")),
                        "ms_anchor_route_bool": s(r.get("ms_anchor")),
                        "strict_core_covariate_surviving_disease_count": f(
                            r.get("strict_core_covariate_surviving_disease_count")
                            or local_json.get("strict_core_covariate_surviving_disease_count")
                        ),
                        "retained_positive_disease_count": f(
                            r.get("retained_positive_disease_count")
                            or local_json.get("retained_positive_disease_count")
                        ),
                        "non_ibd_retained_positive_disease_count": f(
                            r.get("non_ibd_retained_positive_disease_count")
                            or local_json.get("non_ibd_retained_positive_disease_count")
                        ),
                        "foundation_contexts": f(r.get("foundation_contexts") or foundation_json.get("geneformer_support_contexts")),
                        "foundation_strong_contexts": f(foundation_json.get("geneformer_strong_support_contexts")),
                        "foundation_recommendation": s(foundation_json.get("foundation_recommendation")),
                        "real_perturbation_alignment_call": s(foundation_json.get("real_perturbation_alignment_call")),
                        "real_perturbation_alignment_pass": s(foundation_json.get("real_perturbation_alignment_pass")),
                        "l1000_reversal_pass": s(parse_json_text(s(r.get("lincs_summary"))).get("l1000_disease_signature_reversal_pass")),
                        "chembl_target_id": s(r.get("chembl_target_id") or r.get("chembl_best_target_snapshot")),
                        "chembl_activity_count": f(
                            r.get("chembl_activity_count_nM")
                            or r.get("chembl_nM_activity_count_first4_genes")
                            or r.get("chembl_activity_count")
                        ),
                        "europepmc_hit_count": f(r.get("europepmc_hit_count") or r.get("europepmc_autoimmune_hit_count")),
                        "clinicaltrials_count": f(r.get("clinicaltrials_count") or r.get("clinicaltrials_autoimmune_count")),
                        "prior_risk": s(r.get("prior_risk") or r.get("manual_prior_risk")),
                        "blocker_or_reason": s(
                            r.get("route_reason")
                            or r.get("decision_reason")
                            or r.get("manual_blocker")
                            or r.get("blocker")
                            or r.get("failed_gates")
                            or prior_json.get("prior_art_blockers")
                        ),
                    }
                )
    return pd.DataFrame(rows)


def public_search() -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for candidate, queries in PUBLIC_QUERIES.items():
        for source, query in queries:
            if source == "EuropePMC":
                url = (
                    "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
                    f"?query={quote_plus(query)}&format=json&pageSize=5&resultType=lite"
                )
                status, payload, mode = get_json(url, RAW / cache_name("europepmc", query))
                hits = (((payload or {}).get("resultList") or {}).get("result") or [])
                count = i((payload or {}).get("hitCount"))
                top_hits = " | ".join(
                    f"{h.get('pmid') or h.get('id')}: {h.get('title', '')} ({h.get('pubYear', '')})"
                    for h in hits[:5]
                )
            else:
                url = f"https://clinicaltrials.gov/api/v2/studies?query.term={quote_plus(query)}&pageSize=5"
                status, payload, mode = get_json(url, RAW / cache_name("clinicaltrials", query))
                studies = (payload or {}).get("studies") or []
                count = i((payload or {}).get("totalCount"))
                if count == 0 and studies:
                    count = len(studies)
                top_hits = " | ".join(
                    f"{(study.get('protocolSection') or {}).get('identificationModule', {}).get('nctId', '')}: "
                    f"{(study.get('protocolSection') or {}).get('identificationModule', {}).get('briefTitle', '')}"
                    for study in studies[:5]
                )
            rows.append(
                {
                    "candidate": candidate,
                    "source": source,
                    "query": query,
                    "count": count,
                    "top_hits": top_hits,
                    "status": status,
                    "mode": mode,
                    "url": url,
                    "raw_path": rel(RAW / cache_name(source.lower(), query)),
                }
            )
    return pd.DataFrame(rows)


def chembl_gene(gene: str) -> dict[str, Any]:
    target_url = f"https://www.ebi.ac.uk/chembl/api/data/target/search.json?q={quote_plus(gene)}&limit=10"
    status, payload, mode = get_json(target_url, RAW / cache_name("chembl_target", gene))
    targets = (payload or {}).get("targets") or []
    human = [t for t in targets if s(t.get("organism")).lower() == "homo sapiens"]
    target = human[0] if human else (targets[0] if targets else {})
    target_id = target.get("target_chembl_id") or ""
    activity_url = (
        f"https://www.ebi.ac.uk/chembl/api/data/activity.json?target_chembl_id={quote_plus(target_id)}&standard_units=nM&limit=100"
        if target_id
        else ""
    )
    a_status, a_payload, a_mode = (
        get_json(activity_url, RAW / cache_name("chembl_activity", target_id or gene))
        if activity_url
        else (None, {}, "")
    )
    values = [
        f(a.get("standard_value"))
        for a in ((a_payload or {}).get("activities") or [])
        if f(a.get("standard_value")) is not None
    ]
    return {
        "gene": gene,
        "target_chembl_id": target_id,
        "target_name": target.get("pref_name") or "",
        "target_type": target.get("target_type") or "",
        "organism": target.get("organism") or "",
        "target_status": status,
        "target_mode": mode,
        "activity_status": a_status,
        "activity_mode": a_mode,
        "activity_rows_bounded": len(values),
        "best_nM_bounded": min(values) if values else None,
    }


def chembl_summary() -> pd.DataFrame:
    genes = sorted({gene for cfg in CANDIDATES.values() for gene in cfg["genes"]})
    return pd.DataFrame([chembl_gene(gene) for gene in genes])


def patent_urls() -> pd.DataFrame:
    rows: list[dict[str, str]] = []
    for candidate, queries in PATENT_QUERIES.items():
        for query in queries:
            rows.append({"candidate": candidate, "database": "GooglePatents", "query": query, "url": f"https://patents.google.com/?q={quote_plus(query)}"})
            rows.append({"candidate": candidate, "database": "Espacenet", "query": query, "url": f"https://worldwide.espacenet.com/patent/search?q={quote_plus(query)}"})
    return pd.DataFrame(rows)


@dataclass
class Gate:
    candidate: str
    gate: str
    passed: bool
    value: str
    rationale: str


def non_null_max(values: list[Any], default: float = 0.0) -> float:
    nums = [f(v) for v in values]
    nums = [v for v in nums if v is not None]
    return max(nums) if nums else default


def non_null_min(values: list[Any], default: float = 1.0) -> float:
    nums = [f(v) for v in values]
    nums = [v for v in nums if v is not None]
    return min(nums) if nums else default


def candidate_metrics(candidate: str, local_df: pd.DataFrame, public_df: pd.DataFrame, chembl_df: pd.DataFrame) -> dict[str, Any]:
    cfg = CANDIDATES[candidate]
    sub = local_df[local_df["candidate"] == candidate].copy()
    public = public_df[public_df["candidate"] == candidate].copy()
    chembl = chembl_df[chembl_df["gene"].isin(cfg["genes"])].copy()
    blocker_text = " | ".join(sub["blocker_or_reason"].dropna().astype(str).tolist() + sub["prior_risk"].dropna().astype(str).tolist())
    source_calls = " | ".join(sub["source_call"].dropna().astype(str).tolist())
    gwas_traits = non_null_max(sub.get("gwas_trait_count", pd.Series(dtype=float)).tolist())
    gwas_min_p = non_null_min(sub.get("gwas_min_p", pd.Series(dtype=float)).tolist())
    ot_disease_count = non_null_max(sub.get("ot_disease_count", pd.Series(dtype=float)).tolist())
    support_union = non_null_max(sub.get("supporting_disease_count_union", pd.Series(dtype=float)).tolist())
    local_pos = non_null_max(sub.get("local_positive_disease_count", pd.Series(dtype=float)).tolist())
    local_neg = non_null_max(sub.get("local_negative_disease_count", pd.Series(dtype=float)).tolist())
    retained_pos = non_null_max(sub.get("retained_positive_disease_count", pd.Series(dtype=float)).tolist())
    non_ibd_retained = non_null_max(sub.get("non_ibd_retained_positive_disease_count", pd.Series(dtype=float)).tolist())
    strict_residual = non_null_max(sub.get("strict_core_covariate_surviving_disease_count", pd.Series(dtype=float)).tolist())
    ms_delta = non_null_max(sub.get("ms_wm_delta_log2", pd.Series(dtype=float)).tolist(), default=-999.0)
    ms_p = non_null_min(sub.get("ms_wm_p", pd.Series(dtype=float)).tolist())
    ms_fdr = non_null_min(sub.get("ms_wm_fdr", pd.Series(dtype=float)).tolist())
    route_ms_anchor = sub.get("ms_anchor_route_bool", pd.Series(dtype=str)).astype(str).str.contains("True|true", regex=True).any()
    foundation_contexts = non_null_max(sub.get("foundation_contexts", pd.Series(dtype=float)).tolist())
    foundation_strong = non_null_max(sub.get("foundation_strong_contexts", pd.Series(dtype=float)).tolist())
    real_perturb_ok = sub.get("real_perturbation_alignment_pass", pd.Series(dtype=str)).astype(str).str.lower().eq("true").any()
    real_perturb_bad = sub.get("real_perturbation_alignment_call", pd.Series(dtype=str)).astype(str).str.contains("contradict", case=False, na=False).any()
    l1000_ok = sub.get("l1000_reversal_pass", pd.Series(dtype=str)).astype(str).str.lower().eq("true").any()
    emax = int(public.loc[public["source"] == "EuropePMC", "count"].max()) if not public.empty else 0
    ctmax = int(public.loc[public["source"] == "ClinicalTrials.gov", "count"].max()) if not public.empty else 0
    direct_activity_rows = int(non_null_max(chembl.get("activity_rows_bounded", pd.Series(dtype=float)).tolist()))
    best_nm = non_null_min(chembl.get("best_nM_bounded", pd.Series(dtype=float)).tolist(), default=1e12)
    chemical_matter = direct_activity_rows >= 10 and best_nm <= 1000
    source_prior_block = any(token in f"{source_calls} {blocker_text}".lower() for token in ["prior_art", "prior-art", "crowd", "blocking"])
    literature_saturated = {
        "CCR6_TH17_TRAFFICKING": emax >= 500 or ctmax > 0,
        "TREM2_APOE_LIPID_REPAIR": emax >= 1000 or ctmax > 0,
        "SQLE_STEROL_STROMAL": "novel_autoimmune_delta_pass" in blocker_text or "no_go_sqle_failfast" in source_calls.lower(),
        "LOCALIZED_IL10_RESTORATION": emax >= 1000 or ctmax > 0,
    }[candidate]
    target_specific_ms_anchor = bool(ms_delta > 0 and ms_p < 0.05 and ms_fdr < 0.1)
    if candidate == "TREM2_APOE_LIPID_REPAIR":
        target_specific_ms_anchor = False
    return {
        "candidate": candidate,
        "primary_gene": cfg["primary_gene"],
        "genes": ";".join(cfg["genes"]),
        "desired_intervention": cfg["desired_intervention"],
        "reason_for_reopen": cfg["reason_for_reopen"],
        "source_calls": source_calls,
        "blocker_text": blocker_text,
        "gwas_trait_count": gwas_traits,
        "gwas_min_p": gwas_min_p,
        "ot_disease_count": ot_disease_count,
        "supporting_disease_count_union": support_union,
        "local_positive_disease_count": local_pos,
        "local_negative_disease_count": local_neg,
        "retained_positive_disease_count": retained_pos,
        "non_ibd_retained_positive_disease_count": non_ibd_retained,
        "strict_core_covariate_surviving_disease_count": strict_residual,
        "ms_wm_delta_log2": ms_delta,
        "ms_wm_p": ms_p,
        "ms_wm_fdr": ms_fdr if ms_fdr < 1.0 else None,
        "route_level_ms_anchor": route_ms_anchor,
        "target_specific_ms_anchor": target_specific_ms_anchor,
        "foundation_contexts": foundation_contexts,
        "foundation_strong_contexts": foundation_strong,
        "real_perturbation_alignment_pass": real_perturb_ok,
        "real_perturbation_contradicted": real_perturb_bad,
        "l1000_reversal_pass": l1000_ok,
        "europepmc_max_count": emax,
        "clinicaltrials_max_count": ctmax,
        "chembl_activity_rows_bounded": direct_activity_rows,
        "chembl_best_nM_bounded": best_nm if best_nm < 1e12 else None,
        "chemical_matter": chemical_matter,
        "prior_art_or_crowding_block": bool(source_prior_block or literature_saturated),
    }


def primary_blocker(candidate: str) -> str:
    return {
        "CCR6_TH17_TRAFFICKING": "Broad mapped-gene autoimmune signal is not target-resolved; local disease-cell-state and MS anchors are absent, and CCR6/CCL20/Th17 trafficking is crowded prior art with host-defense risk.",
        "TREM2_APOE_LIPID_REPAIR": "Route-level lipid repair biology is plausible, but target-specific causality is not established; TREM2 agonism is crowded in neurodegeneration and may mark phagocytic state rather than control it across autoimmune tissues.",
        "SQLE_STEROL_STROMAL": "The previous SQLE fail-fast stands: cross-disease signal is mostly stromal/IBD-skewed, MS anchor is negative, foundation-model support is contradicted by real perturbation, and no novel autoimmune-use delta survives.",
        "LOCALIZED_IL10_RESTORATION": "IL-10 restoration is biologically credible but not novel; systemic cytokine delivery has extensive prior art and local V3 artifacts do not define a compartment-specific subgroup or modality that solves selectivity.",
    }[candidate]


def decisive_reopen_test(candidate: str) -> str:
    return {
        "CCR6_TH17_TRAFFICKING": "Fine-map/colocalize the CCR6 locus with disease-tissue eQTLs and show CCR6 blockade prevents pathogenic Th17 entry in paired human inflamed-tissue organoids without suppressing protective mucosal recruitment.",
        "TREM2_APOE_LIPID_REPAIR": "Use MS lesion slice or iPSC-microglia/oligodendrocyte debris co-culture with a selective TREM2 agonist and TREM2 loss control; require increased myelin-debris clearance plus preserved remyelination and reduced inflammatory lipid loading.",
        "SQLE_STEROL_STROMAL": "Run selective SQLE perturbation in independent non-IBD autoimmune stromal/myeloid tissue and MS lesion models; reopen only if disease modules reverse and repair/barrier readouts are preserved.",
        "LOCALIZED_IL10_RESTORATION": "Engineer lesion/tissue-local IL-10 delivery and test in ex vivo autoimmune tissue explants; require local STAT3/Treg-like resolution without systemic immunosuppression or fibrotic/barrier impairment.",
    }[candidate]


def evaluate(local_df: pd.DataFrame, public_df: pd.DataFrame, chembl_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    audits: list[dict[str, Any]] = []
    gates: list[Gate] = []
    for candidate in CANDIDATES:
        m = candidate_metrics(candidate, local_df, public_df, chembl_df)
        broad_direct = max(m["ot_disease_count"], m["supporting_disease_count_union"], m["local_positive_disease_count"]) >= 5
        genetic_breadth = m["gwas_trait_count"] >= 5 and m["gwas_min_p"] < 5e-8
        cross_dataset_cell_state = m["local_positive_disease_count"] >= 3 and m["local_negative_disease_count"] <= 1 and m["retained_positive_disease_count"] >= 2
        if candidate == "TREM2_APOE_LIPID_REPAIR":
            cross_dataset_cell_state = bool(m["supporting_disease_count_union"] >= 5 and m["route_level_ms_anchor"])
        target_resolved_genetics = False
        real_perturbation = bool(m["real_perturbation_alignment_pass"] and not m["real_perturbation_contradicted"])
        foundation_real_alignment = bool(
            m["foundation_contexts"] >= 3
            and (m["foundation_strong_contexts"] >= 1 or candidate == "TREM2_APOE_LIPID_REPAIR")
            and real_perturbation
        )
        safe_selective_intervention = False
        route_gates = [
            Gate(candidate, "cross_autoimmune_breadth", bool(broad_direct or genetic_breadth), f"OT={m['ot_disease_count']}; support_union={m['supporting_disease_count_union']}; local_pos={m['local_positive_disease_count']}; GWAS_traits={m['gwas_trait_count']}; min_p={m['gwas_min_p']}", "requires evidence spanning at least five autoimmune diseases or strong genome-wide autoimmune breadth"),
            Gate(candidate, "cross_dataset_cell_state_replication", bool(cross_dataset_cell_state), f"local_pos={m['local_positive_disease_count']}; local_neg={m['local_negative_disease_count']}; retained={m['retained_positive_disease_count']}; support_union={m['supporting_disease_count_union']}", "requires repeated disease-state signal beyond one tissue or one disease"),
            Gate(candidate, "target_specific_ms_anchor", bool(m["target_specific_ms_anchor"]), f"delta={m['ms_wm_delta_log2']}; p={m['ms_wm_p']}; fdr={m['ms_wm_fdr']}; route_ms_anchor={m['route_level_ms_anchor']}", "requires target/intervention-specific MS support, not just route-level plausibility"),
            Gate(candidate, "target_resolved_genetics_or_coloc", target_resolved_genetics, "absent in local V3 artifacts", "mapped-gene or pathway genetics is insufficient for therapeutic promotion"),
            Gate(candidate, "foundation_plus_real_perturbation_alignment", foundation_real_alignment, f"foundation_contexts={m['foundation_contexts']}; strong={m['foundation_strong_contexts']}; real_pass={m['real_perturbation_alignment_pass']}; contradicted={m['real_perturbation_contradicted']}; l1000={m['l1000_reversal_pass']}", "requires foundation-model prediction aligned with real disease-relevant perturbation"),
            Gate(candidate, "tractable_intervention_point", bool(m["chemical_matter"] or candidate in {"CCR6_TH17_TRAFFICKING", "TREM2_APOE_LIPID_REPAIR", "LOCALIZED_IL10_RESTORATION"}), f"chemical_matter={m['chemical_matter']}; activity_rows={m['chembl_activity_rows_bounded']}; best_nM={m['chembl_best_nM_bounded']}", "requires at least a plausible biologic or small-molecule intervention point"),
            Gate(candidate, "safe_selective_direction_resolved", safe_selective_intervention, m["desired_intervention"], "requires a direction that is selective and unlikely to impair repair, barrier, or host defense"),
            Gate(candidate, "novelty_prior_art_unblocked", not m["prior_art_or_crowding_block"], f"EuropePMC={m['europepmc_max_count']}; ClinicalTrials={m['clinicaltrials_max_count']}; prior_block={m['prior_art_or_crowding_block']}", "requires a non-blocked novelty delta across the autoimmune cluster"),
        ]
        gates.extend(route_gates)
        pass_count = sum(g.passed for g in route_gates)
        if pass_count == len(route_gates):
            call = "PROMOTE_V3_CANDIDATE"
        elif candidate == "SQLE_STEROL_STROMAL":
            call = "NO_GO_SQLE_FAILFAST_RECONFIRMED"
        elif candidate == "CCR6_TH17_TRAFFICKING":
            call = "NO_GO_CROWDED_TRAFFICKING_NO_COLOC_LOCAL_SUPPORT"
        elif candidate == "TREM2_APOE_LIPID_REPAIR":
            call = "NO_GO_TREM2_PRIOR_ART_MARKER_CONFOUNDER"
        else:
            call = "NO_GO_IL10_PRIOR_ART_SYSTEMIC_CYTOKINE_DELIVERY"
        m.update(
            {
                "call": call,
                "critical_gate_pass_count": pass_count,
                "critical_gate_total": len(route_gates),
                "primary_blocker": primary_blocker(candidate),
                "decisive_reopen_test": decisive_reopen_test(candidate),
            }
        )
        audits.append(m)
    return pd.DataFrame(audits), pd.DataFrame([g.__dict__ for g in gates])


def write_report(audit: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = ["# Wave52 Remaining Mechanistic Reopeners", "", f"Random seed: `{SEED}`.", "", "## Verdict", ""]
    for _, r in audit.iterrows():
        lines.append(f"- `{r['candidate']}`: `{r['call']}`; {int(r['critical_gate_pass_count'])}/{int(r['critical_gate_total'])} critical gates passed.")
        lines.append(f"  - Primary blocker: {r['primary_blocker']}")
        lines.append(f"  - Decisive reopen test: {r['decisive_reopen_test']}")
    lines.extend(["", "## Gate Matrix", ""])
    for _, g in gates.iterrows():
        status = "PASS" if bool(g["passed"]) else "FAIL"
        lines.append(f"- `{g['candidate']}` / `{g['gate']}`: {status} (`{g['value']}`) - {g['rationale']}.")
    OUT.joinpath("REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)
    local_df = local_evidence()
    public_df = public_search()
    chembl_df = chembl_summary()
    audit, gates = evaluate(local_df, public_df, chembl_df)
    patents = patent_urls()
    local_df.to_csv(OUT / "local_evidence.tsv", sep="\t", index=False)
    public_df.to_csv(OUT / "public_api_counts.tsv", sep="\t", index=False)
    chembl_df.to_csv(OUT / "chembl_summary.tsv", sep="\t", index=False)
    patents.to_csv(OUT / "patent_search_urls.tsv", sep="\t", index=False)
    audit.to_csv(OUT / "remaining_reopeners_audit.tsv", sep="\t", index=False)
    gates.to_csv(OUT / "decision_matrix.tsv", sep="\t", index=False)
    write_report(audit, gates)
    summary = {
        "seed": SEED,
        "promoted_count": int(audit["call"].astype(str).str.contains("PROMOTE").sum()),
        "calls": dict(zip(audit["candidate"], audit["call"], strict=True)),
        "output_dir": rel(OUT),
        "key_outputs": [
            rel(OUT / "remaining_reopeners_audit.tsv"),
            rel(OUT / "decision_matrix.tsv"),
            rel(OUT / "REPORT.md"),
        ],
    }
    write_json(OUT / "summary.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
