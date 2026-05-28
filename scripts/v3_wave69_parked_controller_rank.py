#!/usr/bin/env python3
"""Wave69 controller/intervention ranking from Wave68 parked genes.

Wave68 found no direct promotable gene target in GSE282122, but it did leave
13 genetically anchored, treatment-response-associated nodes. This script asks
a narrower and stronger question: do those parked nodes converge on a druggable
upstream or downstream controller that is less blocked than the nodes
themselves?

The output is a gate, not a claim. It combines:
- Wave68 parked gene evidence.
- OmniPath immediate interaction neighborhoods.
- Enrichr pathway/TF enrichment of the parked gene set.
- ChEMBL target/activity/mechanism summaries for top controller nodes.
- EuropePMC and ClinicalTrials.gov crowding checks for top controller nodes.

No node is promoted unless network convergence, druggability, and prior-art
guardrails all agree.
"""

from __future__ import annotations

import json
import math
import re
import time
from collections import defaultdict
from pathlib import Path
from typing import Any
from urllib.parse import quote_plus, urlencode

import numpy as np
import pandas as pd
import requests


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results_v3" / "wave69_parked_controller_rank"
RAW = OUT / "raw_api"
SEED = 20260527

WAVE68 = ROOT / "results_v3" / "wave68_gse282122_unrestricted_gene_screen" / "integrated_gene_target_rank.tsv"
WAVE62 = ROOT / "results_v3" / "wave62_opentargets_target_resolution" / "target_resolution_summary.tsv"
WAVE37 = ROOT / "results_v3" / "wave37_gse212008_crispr_efferocytosis_screen" / "gene_level_screen_scores.tsv"
WAVE57 = ROOT / "results_v3" / "wave57_intervention_first_geneformer_screen" / "wave57_intervention_first_candidate_calls.tsv"
WAVE61 = ROOT / "results_v3" / "wave61_perturbation_first_guardrail" / "intervention_evidence_tiers.tsv"

ENRICHR_LIBRARIES = [
    "Reactome_2022",
    "GO_Biological_Process_2023",
    "TRRUST_Transcription_Factors_2019",
    "ChEA_2022",
    "KEGG_2021_Human",
    "WikiPathway_2023_Human",
]

MANUAL_BLOCKERS = {
    "CD28": "costimulation_axis_approved_prior_art_systemic_T_cell_activation_risk",
    "CTLA4": "costimulation_axis_approved_prior_art",
    "CD80": "costimulation_axis_prior_art_and_broad_T_cell_APC_biology",
    "CD86": "costimulation_axis_prior_art_and_broad_T_cell_APC_biology",
    "CD274": "PD_L1_checkpoint_prior_art_and_autoimmune_safety_direction_risk",
    "PDCD1": "PD_1_checkpoint_prior_art_and_autoimmune_safety_direction_risk",
    "TNFSF15": "TL1A_axis_prior_art_IBD_trials",
    "TNFRSF25": "TL1A_DR3_axis_prior_art_and_lymphocyte_pleiotropy",
    "IL7R": "prior_art_CD127_autoimmune_axis",
    "STAT4": "STAT4_TF_not_selectively_druggable",
    "SP140": "v3_sp140_prior_art_direction_conflict_ms_local_null",
    "FCGR2A": "Fc_receptor_directionality_and_safety",
    "FCGR2B": "Fc_receptor_directionality_and_safety",
    "SYK": "SYK_prior_art_broad_immunosuppression",
    "JAK1": "generic_JAK_STAT_axis_prior_art_host_defense",
    "JAK2": "generic_JAK_STAT_axis_prior_art_host_defense",
    "JAK3": "generic_JAK_STAT_axis_prior_art_host_defense",
    "TYK2": "generic_JAK_STAT_axis_prior_art_host_defense",
    "STAT1": "generic_IFN_transcription_axis",
    "RELA": "generic_NFKB_host_defense",
    "NFKB1": "generic_NFKB_host_defense",
    "TNF": "MS_directionally_unsafe_TNF_axis",
    "TNFRSF1A": "MS_directionally_unsafe_TNF_axis",
    "PRKACA": "broad_PKA_pleiotropy_no_myeloid_selectivity",
    "PRKACB": "broad_PKA_pleiotropy_no_myeloid_selectivity",
    "FYN": "broad_SRC_family_kinase_prior_art_selectivity_safety",
    "SRC": "broad_SRC_family_kinase_prior_art_selectivity_safety",
    "YES1": "broad_SRC_family_kinase_prior_art_selectivity_safety",
    "LYN": "broad_SRC_family_kinase_prior_art_selectivity_safety",
    "MAPK14": "p38_MAPK_autoimmune_prior_art_and_broad_stress_axis",
    "GSK3A": "GSK3_family_pleiotropic_neuroimmune_metabolic",
    "GSK3B": "GSK3_family_pleiotropic_neuroimmune_metabolic",
    "INSR": "systemic_insulin_receptor_metabolic_safety",
    "HRAS": "oncogenic_RAS_not_chronic_autoimmune_target",
    "RAF1": "MAPK_oncology_pleiotropy",
    "NCF1": "NADPH_oxidase_host_defense_CGD_directionality_risk",
    "NCF2": "NADPH_oxidase_host_defense_CGD_directionality_risk",
    "CYBB": "NADPH_oxidase_host_defense_CGD_directionality_risk",
}

MANUAL_SEED_CONTROLLERS = {
    # Known immediate receptor/effector partners that may not be densely
    # represented in OmniPath but are required to interpret the parked set.
    "RGS14": ["PRKACA", "HRAS", "RAF1", "RAP1A"],
    "CD274": ["PDCD1", "JAK1", "JAK2", "STAT1", "RELA"],
    "CD80": ["CD28", "CTLA4", "CD86"],
    "TNFSF15": ["TNFRSF25", "NFKB1", "RELA"],
    "FCGR2B": ["SYK", "INPP5D", "LILRB1"],
    "FCGR2A": ["SYK", "FCER1G"],
    "NCF1": ["CYBB", "NCF2", "NCF4", "RAC2"],
    "IL7R": ["JAK1", "JAK3", "STAT5A", "STAT5B"],
    "STAT4": ["JAK2", "TYK2", "IL12RB1", "IL12RB2"],
    "TNFRSF9": ["TRAF1", "TRAF2", "NFKB1", "RELA"],
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def f(value: Any, default: float = 0.0) -> float:
    try:
        if value is None or pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def s(value: Any) -> str:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return ""
    return str(value)


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True) + "\n", encoding="utf-8")


def cache_name(prefix: str, key: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9_.-]+", "_", f"{prefix}_{key}")[:180].strip("_")
    return safe + ".json"


def get_json(url: str, cache_path: Path, method: str = "GET", payload: dict[str, Any] | None = None) -> tuple[int | None, Any, str]:
    if cache_path.exists():
        try:
            return 200, json.loads(cache_path.read_text(encoding="utf-8")), "cache"
        except json.JSONDecodeError:
            pass
    try:
        if method == "POST":
            response = requests.post(url, data=payload or {}, timeout=35, headers={"User-Agent": "ms-auto-research-wave69/1.0"})
        else:
            response = requests.get(url, timeout=35, headers={"User-Agent": "ms-auto-research-wave69/1.0"})
        data = response.json() if response.text.strip() else {}
        cache_path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        time.sleep(0.15)
        return response.status_code, data, "live"
    except Exception as exc:  # noqa: BLE001
        data = {"error": type(exc).__name__, "message": str(exc), "url": url}
        cache_path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return None, data, "error"


def enrichr_add_list(library: str, gene_text: str) -> tuple[int | None, dict[str, Any], str]:
    cache_path = RAW / cache_name("enrichr_addList", library)
    if cache_path.exists():
        try:
            cached = json.loads(cache_path.read_text(encoding="utf-8"))
            if cached.get("userListId"):
                return 200, cached, "cache"
        except json.JSONDecodeError:
            pass
    try:
        response = requests.post(
            "https://maayanlab.cloud/Enrichr/addList",
            files={"list": (None, gene_text), "description": (None, f"wave69_{library}")},
            timeout=35,
            headers={"User-Agent": "ms-auto-research-wave69/1.0"},
        )
        data = response.json() if response.text.strip() else {}
        cache_path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        time.sleep(0.15)
        return response.status_code, data, "live"
    except Exception as exc:  # noqa: BLE001
        data = {"error": type(exc).__name__, "message": str(exc)}
        cache_path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return None, data, "error"


def load_tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


def load_anchors() -> pd.DataFrame:
    df = load_tsv(WAVE68)
    if df.empty:
        raise FileNotFoundError(WAVE68)
    anchors = df[df["wave68_call"].eq("PARK_GENETIC_PERTURBATION_INTERSECTION")].copy()
    for col in [
        "raw_p",
        "raw_fdr",
        "paired_p",
        "paired_fdr",
        "remission_adjusted_p",
        "remission_adjusted_fdr",
        "wave62_score",
        "strong_l2g_disease_count",
        "strong_qtl_coloc_disease_count",
        "myeloid_qtl_coloc_disease_count",
    ]:
        if col in anchors.columns:
            anchors[col] = pd.to_numeric(anchors[col], errors="coerce")
    p_candidates = anchors[["raw_p", "paired_p", "remission_adjusted_p"]].replace(0, np.nan)
    anchors["best_nominal_p"] = p_candidates.min(axis=1).fillna(1.0)
    anchors["response_weight"] = -np.log10(anchors["best_nominal_p"].clip(lower=1e-300))
    anchors["genetic_breadth_weight"] = (
        anchors["strong_l2g_disease_count"].fillna(0)
        + anchors["strong_qtl_coloc_disease_count"].fillna(0)
        + anchors["myeloid_qtl_coloc_disease_count"].fillna(0)
    ) / 3.0
    anchors["anchor_weight"] = (
        anchors["response_weight"].clip(upper=8)
        + anchors["wave62_score"].fillna(0).clip(upper=8) / 2.0
        + anchors["genetic_breadth_weight"].clip(upper=5) / 2.0
    )
    return anchors


def fetch_enrichr(genes: list[str]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    gene_text = "\n".join(genes)
    for library in ENRICHR_LIBRARIES:
        cache = RAW / cache_name("enrichr", library)
        if cache.exists():
            data = json.loads(cache.read_text(encoding="utf-8"))
            status, mode = 200, "cache"
        else:
            status_add, data_add, mode_add = enrichr_add_list(library, gene_text)
            user_id = (data_add or {}).get("userListId")
            if not user_id:
                rows.append({"library": library, "status": status_add, "mode": mode_add, "term": "ERROR_NO_USER_LIST"})
                continue
            url = f"https://maayanlab.cloud/Enrichr/enrich?{urlencode({'userListId': user_id, 'backgroundType': library})}"
            status, data, mode = get_json(url, cache)
        for item in (data or {}).get(library, [])[:100]:
            rank, term, pval, zscore, combined, overlap, adj_p, old_p, old_adj = item[:9]
            rows.append(
                {
                    "library": library,
                    "status": status,
                    "mode": mode,
                    "rank": rank,
                    "term": term,
                    "p_value": pval,
                    "z_score": zscore,
                    "combined_score": combined,
                    "overlap_genes": ";".join(overlap),
                    "adjusted_p": adj_p,
                    "old_p": old_p,
                    "old_adjusted_p": old_adj,
                }
            )
    out = pd.DataFrame(rows)
    if not out.empty and "adjusted_p" in out.columns:
        out["adjusted_p"] = pd.to_numeric(out["adjusted_p"], errors="coerce")
    return out


def fetch_omnipath(genes: list[str]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    base = "https://omnipathdb.org/interactions"
    for gene in genes:
        for role, param in [("incoming_to_anchor", "targets"), ("outgoing_from_anchor", "sources")]:
            url = base + "?" + urlencode(
                {
                    "genesymbols": "yes",
                    "format": "json",
                    "fields": "sources,references,curation_effort",
                    param: gene,
                }
            )
            status, data, mode = get_json(url, RAW / cache_name("omnipath", f"{role}_{gene}"))
            if isinstance(data, list):
                for item in data:
                    if not isinstance(item, dict):
                        continue
                    src = s(item.get("source_genesymbol") or item.get("source")).upper()
                    tgt = s(item.get("target_genesymbol") or item.get("target")).upper()
                    rows.append(
                        {
                            "anchor_gene": gene,
                            "query_role": role,
                            "source_gene": src,
                            "target_gene": tgt,
                            "candidate_node": src if role == "incoming_to_anchor" else tgt,
                            "is_directed": item.get("is_directed"),
                            "is_stimulation": item.get("is_stimulation"),
                            "is_inhibition": item.get("is_inhibition"),
                            "consensus_direction": item.get("consensus_direction"),
                            "consensus_stimulation": item.get("consensus_stimulation"),
                            "consensus_inhibition": item.get("consensus_inhibition"),
                            "source_databases": ";".join(item.get("sources") or []),
                            "reference_count": len(item.get("references") or []),
                            "curation_effort": item.get("curation_effort"),
                            "status": status,
                            "mode": mode,
                        }
                    )
    for anchor, controllers in MANUAL_SEED_CONTROLLERS.items():
        if anchor not in genes:
            continue
        for node in controllers:
            rows.append(
                {
                    "anchor_gene": anchor,
                    "query_role": "manual_seed_controller",
                    "source_gene": node,
                    "target_gene": anchor,
                    "candidate_node": node,
                    "is_directed": True,
                    "is_stimulation": None,
                    "is_inhibition": None,
                    "consensus_direction": None,
                    "consensus_stimulation": None,
                    "consensus_inhibition": None,
                    "source_databases": "manual_seed_from_immediate_known_biology",
                    "reference_count": np.nan,
                    "curation_effort": np.nan,
                    "status": 200,
                    "mode": "manual",
                }
            )
    out = pd.DataFrame(rows)
    if not out.empty:
        out = out[out["candidate_node"].astype(str).str.len() > 0].drop_duplicates()
    return out


def chembl_summary(gene: str) -> dict[str, Any]:
    target_url = f"https://www.ebi.ac.uk/chembl/api/data/target/search.json?q={quote_plus(gene)}&limit=20"
    status, data, mode = get_json(target_url, RAW / cache_name("chembl_target", gene))
    targets = data.get("targets") or [] if isinstance(data, dict) else []
    human = [target for target in targets if s(target.get("organism")).lower() == "homo sapiens"]
    target = human[0] if human else (targets[0] if targets else {})
    chembl_id = target.get("target_chembl_id") or ""
    activity_url = (
        f"https://www.ebi.ac.uk/chembl/api/data/activity.json?target_chembl_id={quote_plus(chembl_id)}&standard_units=nM&limit=100"
        if chembl_id
        else ""
    )
    a_status, a_data, a_mode = get_json(activity_url, RAW / cache_name("chembl_activity", chembl_id or gene)) if activity_url else (None, {}, "")
    values = [
        f(activity.get("standard_value"), math.nan)
        for activity in (a_data.get("activities") or [])
        if not math.isnan(f(activity.get("standard_value"), math.nan))
    ]
    mechanism_url = f"https://www.ebi.ac.uk/chembl/api/data/mechanism.json?target_chembl_id={quote_plus(chembl_id)}&limit=50" if chembl_id else ""
    m_status, m_data, m_mode = get_json(mechanism_url, RAW / cache_name("chembl_mechanism", chembl_id or gene)) if mechanism_url else (None, {}, "")
    mechanisms = m_data.get("mechanisms") or [] if isinstance(m_data, dict) else []
    return {
        "candidate_node": gene,
        "chembl_target_id": chembl_id,
        "chembl_pref_name": target.get("pref_name") or "",
        "chembl_target_type": target.get("target_type") or "",
        "chembl_organism": target.get("organism") or "",
        "chembl_activity_rows": int((a_data.get("page_meta") or {}).get("total_count", len(values)) or 0) if isinstance(a_data, dict) else 0,
        "chembl_scanned_activity_rows": len(values),
        "chembl_best_nM": min(values) if values else np.nan,
        "chembl_mechanism_rows": len(mechanisms),
        "chembl_mechanism_molecules": ";".join(
            f"{m.get('molecule_chembl_id')}:{m.get('action_type')}" for m in mechanisms[:20] if m.get("molecule_chembl_id")
        ),
        "chembl_target_status": status,
        "chembl_activity_status": a_status,
        "chembl_mechanism_status": m_status,
        "chembl_target_mode": mode,
        "chembl_activity_mode": a_mode,
        "chembl_mechanism_mode": m_mode,
    }


def europepmc_count(query: str) -> dict[str, Any]:
    url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={quote_plus(query)}&format=json&pageSize=3"
    status, data, mode = get_json(url, RAW / cache_name("europepmc", query))
    results = (data.get("resultList") or {}).get("result") or [] if isinstance(data, dict) else []
    return {
        "query": query,
        "source": "EuropePMC",
        "status": status,
        "mode": mode,
        "hit_count": int(data.get("hitCount", 0) or 0) if isinstance(data, dict) else 0,
        "top_titles": " || ".join(s(row.get("title"))[:180] for row in results[:3]),
        "url": url,
    }


def clinicaltrials_count(query: str) -> dict[str, Any]:
    url = f"https://clinicaltrials.gov/api/v2/studies?query.term={quote_plus(query)}&pageSize=5&format=json"
    status, data, mode = get_json(url, RAW / cache_name("clinicaltrials", query))
    studies = data.get("studies") or [] if isinstance(data, dict) else []
    return {
        "query": query,
        "source": "ClinicalTrials.gov",
        "status": status,
        "mode": mode,
        "hit_count": int(data.get("totalCount", len(studies)) or 0) if isinstance(data, dict) else 0,
        "top_titles": " || ".join(
            s(((study.get("protocolSection") or {}).get("identificationModule") or {}).get("briefTitle"))[:160]
            for study in studies[:3]
        ),
        "url": url,
    }


def infer_tf_hits(enrichr: pd.DataFrame) -> dict[str, dict[str, Any]]:
    tf_hits: dict[str, dict[str, Any]] = {}
    if enrichr.empty:
        return tf_hits
    tf_lib = enrichr[enrichr["library"].isin(["TRRUST_Transcription_Factors_2019", "ChEA_2022"])].copy()
    for _, row in tf_lib.iterrows():
        term = s(row.get("term"))
        token = re.split(r"[\\s_:/()\\-]+", term)[0].upper()
        if not token:
            continue
        current = tf_hits.get(token)
        adj = f(row.get("adjusted_p"), 1.0)
        if current is None or adj < current["best_enrichr_tf_adjusted_p"]:
            tf_hits[token] = {
                "best_enrichr_tf_library": row.get("library"),
                "best_enrichr_tf_term": term,
                "best_enrichr_tf_adjusted_p": adj,
                "best_enrichr_tf_overlap": row.get("overlap_genes"),
            }
    return tf_hits


def add_local_guardrails(nodes: pd.DataFrame) -> pd.DataFrame:
    wave62 = load_tsv(WAVE62)
    wave37 = load_tsv(WAVE37)
    wave57 = load_tsv(WAVE57)
    wave61 = load_tsv(WAVE61)
    out = nodes.copy()
    for df, col in [(wave62, "gene"), (wave57, "gene")]:
        if not df.empty and col in df.columns:
            df[col] = df[col].astype(str).str.upper()
    if not wave37.empty and "gene_symbol" in wave37.columns:
        wave37["gene_symbol"] = wave37["gene_symbol"].astype(str).str.upper()
    if not wave61.empty and "gene" in wave61.columns:
        wave61["gene"] = wave61["gene"].astype(str).str.upper()

    rows: list[dict[str, Any]] = []
    for row in out.itertuples(index=False):
        gene = row.candidate_node
        w62 = wave62[wave62["gene"].eq(gene)].head(1).to_dict("records") if not wave62.empty and "gene" in wave62.columns else []
        w37 = wave37[wave37["gene_symbol"].eq(gene)].head(1).to_dict("records") if not wave37.empty and "gene_symbol" in wave37.columns else []
        w57 = wave57[wave57["gene"].eq(gene)].head(1).to_dict("records") if not wave57.empty and "gene" in wave57.columns else []
        w61 = wave61[wave61["gene"].eq(gene)].head(1).to_dict("records") if not wave61.empty and "gene" in wave61.columns else []
        w62r = w62[0] if w62 else {}
        w37r = w37[0] if w37 else {}
        w57r = w57[0] if w57 else {}
        w61r = w61[0] if w61 else {}
        rows.append(
            {
                "candidate_node": gene,
                "wave62_score": f(w62r.get("wave62_score")),
                "wave62_call": w62r.get("wave62_call", ""),
                "wave62_manual_blocker": w62r.get("manual_blocker", ""),
                "wave62_prior_context_blocker": w62r.get("prior_context_blocker", ""),
                "wave62_strong_l2g_disease_count": f(w62r.get("strong_l2g_disease_count")),
                "wave62_strong_qtl_coloc_disease_count": f(w62r.get("strong_qtl_coloc_disease_count")),
                "wave62_ms_max_relevant_qtl_h4": f(w62r.get("ms_max_relevant_qtl_h4")),
                "efferocytosis_screen_call": w37r.get("screen_call", ""),
                "efferocytosis_median_lfc": f(w37r.get("median_efficient_minus_noneater_lfc"), np.nan),
                "efferocytosis_fdr": f(w37r.get("contrast_fdr"), np.nan),
                "wave57_call": w57r.get("wave57_call", ""),
                "wave57_model_priority_score": f(w57r.get("wave57_model_priority_score")),
                "wave61_call": w61r.get("wave61_call", ""),
                "wave61_manual_blocker": w61r.get("manual_blocker", ""),
            }
        )
    return out.merge(pd.DataFrame(rows), on="candidate_node", how="left")


def build_node_rank(anchors: pd.DataFrame, interactions: pd.DataFrame, enrichr: pd.DataFrame) -> pd.DataFrame:
    connections: list[dict[str, Any]] = []
    anchor_weights = anchors.set_index("gene")["anchor_weight"].to_dict()
    for row in anchors.itertuples(index=False):
        connections.append(
            {
                "candidate_node": row.gene,
                "anchor_gene": row.gene,
                "connection_role": "self_anchor",
                "connection_weight": row.anchor_weight,
                "source_databases": "wave68_self_anchor",
            }
        )
    for row in interactions.itertuples(index=False):
        node = s(row.candidate_node).upper()
        anchor = s(row.anchor_gene).upper()
        if node == anchor or not node:
            continue
        connections.append(
            {
                "candidate_node": node,
                "anchor_gene": anchor,
                "connection_role": row.query_role,
                "connection_weight": anchor_weights.get(anchor, 0.0),
                "source_databases": row.source_databases,
            }
        )
    conn = pd.DataFrame(connections)
    if conn.empty:
        return pd.DataFrame()

    tf_hits = infer_tf_hits(enrichr)
    rows: list[dict[str, Any]] = []
    for node, sub in conn.groupby("candidate_node", dropna=False):
        anchors_connected = sorted(sub["anchor_gene"].dropna().astype(str).str.upper().unique())
        roles = sorted(sub["connection_role"].dropna().astype(str).unique())
        source_dbs = sorted(set(";".join(sub["source_databases"].dropna().astype(str)).split(";")) - {""})
        tf = tf_hits.get(node, {})
        rows.append(
            {
                "candidate_node": node,
                "connected_anchor_count": len(anchors_connected),
                "connected_anchors": ";".join(anchors_connected),
                "connection_roles": ";".join(roles),
                "connection_weight_sum": float(sub["connection_weight"].sum()),
                "connection_weight_max": float(sub["connection_weight"].max()),
                "source_database_count": len(source_dbs),
                "top_source_databases": ";".join(source_dbs[:12]),
                "best_enrichr_tf_library": tf.get("best_enrichr_tf_library", ""),
                "best_enrichr_tf_term": tf.get("best_enrichr_tf_term", ""),
                "best_enrichr_tf_adjusted_p": tf.get("best_enrichr_tf_adjusted_p", np.nan),
                "best_enrichr_tf_overlap": tf.get("best_enrichr_tf_overlap", ""),
            }
        )
    nodes = pd.DataFrame(rows)
    return nodes.sort_values(["connected_anchor_count", "connection_weight_sum"], ascending=[False, False])


def score_nodes(nodes: pd.DataFrame, chembl: pd.DataFrame, public: pd.DataFrame) -> pd.DataFrame:
    out = nodes.merge(chembl, on="candidate_node", how="left")
    if not public.empty:
        pivot = public.pivot_table(index="candidate_node", columns="source", values="hit_count", aggfunc="max").reset_index()
        pivot = pivot.rename(columns={"EuropePMC": "europepmc_prior_hits", "ClinicalTrials.gov": "clinicaltrials_hits"})
        out = out.merge(pivot, on="candidate_node", how="left")
    else:
        out["europepmc_prior_hits"] = np.nan
        out["clinicaltrials_hits"] = np.nan
    out = add_local_guardrails(out)
    for col in [
        "chembl_activity_rows",
        "chembl_mechanism_rows",
        "connected_anchor_count",
        "connection_weight_sum",
        "source_database_count",
        "europepmc_prior_hits",
        "clinicaltrials_hits",
    ]:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce").fillna(0.0)
    out["has_chembl_activity"] = out["chembl_activity_rows"] >= 10
    out["has_chembl_mechanism"] = out["chembl_mechanism_rows"] > 0
    out["has_tf_enrichment_hint"] = pd.to_numeric(out["best_enrichr_tf_adjusted_p"], errors="coerce").fillna(1.0) <= 0.10
    out["manual_blocker"] = out["candidate_node"].map(MANUAL_BLOCKERS).fillna("")
    for col in ["wave62_manual_blocker", "wave62_prior_context_blocker", "wave61_manual_blocker"]:
        out[col] = out[col].fillna("").astype(str)
        out.loc[out[col].str.lower().eq("nan"), col] = ""
    out["any_blocker"] = (
        out["manual_blocker"].astype(str).ne("")
        | out["wave62_manual_blocker"].astype(str).ne("")
        | out["wave62_prior_context_blocker"].astype(str).ne("")
        | out["wave61_manual_blocker"].astype(str).ne("")
    )
    out["controller_score"] = (
        out["connection_weight_sum"].clip(upper=25)
        + out["connected_anchor_count"].clip(upper=6) * 1.5
        + out["source_database_count"].clip(upper=8) * 0.25
        + out["has_chembl_activity"].astype(float) * 2.0
        + out["has_chembl_mechanism"].astype(float) * 1.5
        + out["has_tf_enrichment_hint"].astype(float) * 1.0
        - out["any_blocker"].astype(float) * 5.0
        - np.log10(out["clinicaltrials_hits"].fillna(0) + 1.0) * 0.5
        - np.log10(out["europepmc_prior_hits"].fillna(0) + 1.0) * 0.25
    )
    calls = []
    for row in out.itertuples(index=False):
        if row.any_blocker:
            calls.append("NO_GO_BLOCKED_PRIOR_OR_BROAD_BIOLOGY")
        elif row.connected_anchor_count >= 2 and (row.has_chembl_activity or row.has_chembl_mechanism):
            calls.append("PARK_DRUGGABLE_CONTROLLER_SCOUT_NEEDS_DIRECT_VALIDATION")
        elif row.connected_anchor_count >= 2:
            calls.append("PARK_NETWORK_CONTROLLER_NO_DRUGGABLE_HANDLE")
        else:
            calls.append("DESCRIPTIVE_SINGLE_ANCHOR_NEIGHBOR")
    out["wave69_call"] = calls
    priority = {
        "PARK_DRUGGABLE_CONTROLLER_SCOUT_NEEDS_DIRECT_VALIDATION": 0,
        "PARK_NETWORK_CONTROLLER_NO_DRUGGABLE_HANDLE": 1,
        "NO_GO_BLOCKED_PRIOR_OR_BROAD_BIOLOGY": 2,
        "DESCRIPTIVE_SINGLE_ANCHOR_NEIGHBOR": 3,
    }
    out["wave69_call_priority"] = out["wave69_call"].map(priority).fillna(9)
    return out.sort_values(["wave69_call_priority", "controller_score"], ascending=[True, False])


def markdown_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "_No rows._"
    cols = list(df.columns)
    lines = ["| " + " | ".join(cols) + " |", "| " + " | ".join(["---"] * len(cols)) + " |"]
    for _, row in df.iterrows():
        vals = []
        for col in cols:
            value = "" if pd.isna(row[col]) else str(row[col])
            vals.append(value.replace("\n", " ").replace("|", "\\|")[:500])
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines)


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)

    anchors = load_anchors()
    genes = sorted(anchors["gene"].dropna().astype(str).str.upper().unique())
    enrichr = fetch_enrichr(genes)
    interactions = fetch_omnipath(genes)
    nodes = build_node_rank(anchors, interactions, enrichr)

    # Limit expensive public target/prior checks to nodes with either network
    # convergence or direct anchor status. Single-edge neighbors stay visible in
    # the network table but do not consume API calls.
    top_nodes = nodes[
        (nodes["connected_anchor_count"] >= 2)
        | nodes["connection_roles"].astype(str).str.contains("self_anchor", na=False)
    ].head(80)["candidate_node"].dropna().astype(str).tolist()
    chembl = pd.DataFrame([chembl_summary(gene) for gene in top_nodes])
    public_rows: list[dict[str, Any]] = []
    public_nodes = top_nodes[:35]
    for gene in public_nodes:
        epmc = europepmc_count(f'"{gene}" autoimmune therapeutic target OR multiple sclerosis OR Crohn OR psoriasis OR rheumatoid')
        public_rows.append({"candidate_node": gene, **epmc})
        ct = clinicaltrials_count(f"{gene} autoimmune OR multiple sclerosis OR Crohn OR psoriasis OR rheumatoid")
        public_rows.append({"candidate_node": gene, **ct})
    public = pd.DataFrame(public_rows)

    ranked = score_nodes(nodes, chembl, public)

    anchors.to_csv(OUT / "wave68_parked_anchor_genes.tsv", sep="\t", index=False)
    enrichr.to_csv(OUT / "parked_gene_enrichr.tsv", sep="\t", index=False)
    interactions.to_csv(OUT / "parked_gene_omnipath_interactions.tsv", sep="\t", index=False)
    nodes.to_csv(OUT / "controller_node_network_summary.tsv", sep="\t", index=False)
    chembl.to_csv(OUT / "controller_chembl_summary.tsv", sep="\t", index=False)
    public.to_csv(OUT / "controller_public_crowding.tsv", sep="\t", index=False)
    ranked.to_csv(OUT / "controller_intervention_rank.tsv", sep="\t", index=False)

    promoted = ranked[ranked["wave69_call"].str.startswith("PARK_DRUGGABLE", na=False)]
    summary = {
        "date": "2026-05-27",
        "random_seed": SEED,
        "anchor_genes": genes,
        "n_anchor_genes": len(genes),
        "n_omnipath_or_manual_interactions": int(len(interactions)),
        "n_controller_nodes": int(len(nodes)),
        "n_chembl_checked_nodes": int(len(chembl)),
        "n_public_crowding_checked_nodes": int(len(public_nodes)),
        "call_counts": ranked["wave69_call"].value_counts().to_dict(),
        "top_calls": ranked.head(20)[
            [
                "candidate_node",
                "wave69_call",
                "controller_score",
                "connected_anchor_count",
                "connected_anchors",
                "chembl_activity_rows",
                "chembl_mechanism_rows",
                "manual_blocker",
            ]
        ].to_dict("records"),
        "interpretation": (
            "Wave69 is a controller-ranking gate. PARK rows are not therapeutic claims; "
            "they require direct perturbation validation and novelty/patent clearance."
        ),
    }
    write_json(OUT / "summary.json", summary)

    top_cols = [
        "candidate_node",
        "wave69_call",
        "controller_score",
        "connected_anchor_count",
        "connected_anchors",
        "connection_roles",
        "chembl_target_id",
        "chembl_activity_rows",
        "chembl_mechanism_rows",
        "europepmc_prior_hits",
        "clinicaltrials_hits",
        "manual_blocker",
        "wave62_call",
        "wave57_call",
        "wave61_call",
    ]
    enrich_cols = ["library", "rank", "term", "adjusted_p", "overlap_genes"]
    if not enrichr.empty and {"adjusted_p", "p_value"}.issubset(enrichr.columns):
        top_enrichr = enrichr.sort_values(["adjusted_p", "p_value"])[[c for c in enrich_cols if c in enrichr.columns]].head(30)
    elif not enrichr.empty:
        top_enrichr = enrichr[[c for c in enrich_cols if c in enrichr.columns]].head(30)
    else:
        top_enrichr = pd.DataFrame()
    report = [
        "# Wave69 Parked-Gene Controller Rank",
        "",
        "## Verdict",
        "",
        f"Anchor genes: `{';'.join(genes)}`.",
        f"Calls: `{summary['call_counts']}`.",
        "",
        "This gate does not promote a therapeutic claim. It asks whether the Wave68 parked genes converge on a less-blocked intervention point.",
        "",
        "## Top Controller Nodes",
        "",
        markdown_table(ranked[[c for c in top_cols if c in ranked.columns]].head(40)),
        "",
        "## Top Enrichr Terms",
        "",
        markdown_table(top_enrichr),
        "",
        "## Parked Druggable Controller Scouts",
        "",
        markdown_table(promoted[[c for c in top_cols if c in promoted.columns]].head(30)),
        "",
        "## Guardrails",
        "",
        "- Immediate network convergence is not causality.",
        "- ChEMBL activity or mechanism rows mean chemical matter exists, not that tissue-selective autoimmune target engagement is feasible.",
        "- Manual blockers encode already-known V3 and clinical-class failures so prior-art-heavy checkpoint/JAK/TNF/TL1A axes do not masquerade as discoveries.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True, allow_nan=True))


if __name__ == "__main__":
    main()
