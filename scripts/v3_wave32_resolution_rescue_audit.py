#!/usr/bin/env python3
"""Wave32 downstream-resolution rescue audit.

After Wave31, the direct "suppress HLA-II/CD74/GILT" route is blocked: MED16_KO
is a strong perturbation comparator but not a druggable intervention. This wave
asks a different therapeutic question:

Can the recurrent lipid-lysosomal inflammatory state be pushed toward
efferocytosis, lipid clearance, and tissue repair without collapsing generic
IFN/HLA-II host-defense signaling?

This is an audit, not a claim generator. It integrates existing V3 outputs and
lightweight API snapshots. A positive call would only authorize hostile novelty
review and a deeper validation branch.
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "phases/v3/results" / "wave32_resolution_rescue_audit"
RAW = OUT / "raw_api"
SEED = 20260527
USER_AGENT = "ms-auto-research-wave32-resolution-rescue/1.0"


PATHS = {
    "cross_gene": ROOT / "phases/v3/results" / "cross_disease_gene_summary.tsv",
    "broad_gene": ROOT / "phases/v3/results" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_rank.tsv",
    "residual": ROOT / "phases/v3/results" / "broad_residual_gate" / "broad_residual_gate_summary.tsv",
    "surface": ROOT / "phases/v3/results" / "wave15_surface_trafficking_dependency" / "candidate_ranked.tsv",
    "accessible": ROOT / "phases/v3/results" / "wave18_accessible_target_rescue" / "accessible_target_rescue_candidates.tsv",
    "foundation": ROOT / "phases/v3/results" / "wave18_foundation_rescue" / "foundation_rescue_candidate_rank.tsv",
    "checkpoint": ROOT / "phases/v3/results" / "wave19_tolerogenic_checkpoint" / "checkpoint_candidate_synthesis.tsv",
    "lysosomal_routes": ROOT / "phases/v3/results" / "wave19_lysosomal_controller" / "route_summary.tsv",
    "controller_triage": ROOT / "phases/v3/results" / "wave19_orchestrator_controller_triage" / "wave19_controller_triage.tsv",
    "genetics": ROOT / "phases/v3/results" / "wave25_causal_genetics_module_proxy" / "causal_proxy_candidate_matrix.tsv",
    "target_first": ROOT / "phases/v3/results" / "wave28_target_first_rescue" / "target_first_rescue_matrix.tsv",
    "direct": ROOT / "phases/v3/results" / "wave15_perturbation_drug_response" / "candidate_level_synthesis.tsv",
    "l1000": ROOT / "phases/v3/results" / "wave15_perturbation_drug_response" / "l1000fwd_selectivity_compound_rank.tsv",
}


AUTOIMMUNE_QUERY = (
    '"multiple sclerosis" OR "rheumatoid arthritis" OR lupus OR Crohn OR '
    '"ulcerative colitis" OR psoriasis OR Sjogren OR "type 1 diabetes" OR '
    '"primary biliary cholangitis" OR autoimmune'
)


ROUTES: dict[str, dict[str, Any]] = {
    "TAM_EFFEROCYTOSIS_AGONISM": {
        "genes": ["MERTK", "AXL", "TYRO3", "GAS6", "PROS1"],
        "route_class": "efferocytosis receptor/ligand",
        "desired_direction": "agonize or restore TAM-mediated efferocytosis; inhibitors are wrong direction for repair",
        "modality": "agonist biologic/ligand engineering; small-molecule TAM kinase inhibitors are directionally wrong",
        "manual_druggability": 1.5,
        "manual_direction_score": 1.0,
        "manual_safety_score": 1.0,
        "manual_prior_risk": "high",
        "manual_blocker": "TAM biology is repair-relevant, but available mature chemical matter is mostly inhibitory oncology pharmacology; agonism/delivery and autoimmune direction are immature.",
    },
    "MERTK_CENTERED_EFFEROCYTOSIS": {
        "genes": ["MERTK", "GAS6", "PROS1"],
        "route_class": "efferocytosis receptor",
        "desired_direction": "agonize or restore MERTK-mediated myelin/apoptotic-cell clearance",
        "modality": "MERTK agonist/ligand biologic concept or cell-targeted gene/protein delivery",
        "manual_druggability": 1.25,
        "manual_direction_score": 1.0,
        "manual_safety_score": 1.5,
        "manual_prior_risk": "high",
        "manual_blocker": "MERTK is a strong repair/efferocytosis comparator, but local V3 gene-level recurrence is weak and direct agonist modality is not mature.",
    },
    "TREM2_APOE_LIPID_REPAIR": {
        "genes": ["TREM2", "APOE", "TYROBP", "LPL"],
        "route_class": "microglial lipid/debris repair",
        "desired_direction": "agonize TREM2-like phagolysosomal repair while avoiding chronic inflammatory lipid loading",
        "modality": "TREM2 agonist antibody precedent; APOE/LPL are not direct autoimmune targets",
        "manual_druggability": 1.75,
        "manual_direction_score": 1.0,
        "manual_safety_score": 1.0,
        "manual_prior_risk": "high",
        "manual_blocker": "TREM2 agonism is crowded in neurodegeneration and local cross-autoimmune support is marker/confounder dominated rather than target-causal.",
    },
    "LXR_ABCA1_CHOLESTEROL_EFFLUX": {
        "genes": ["NR1H3", "NR1H2", "ABCA1", "ABCG1", "APOE"],
        "route_class": "cholesterol efflux nuclear receptor",
        "desired_direction": "activate LXR/ABCA1/ABCG1 efflux only if lipogenesis and systemic metabolic liabilities are separable",
        "modality": "LXR/RXR agonists or indirect sterol-efflux modulation",
        "manual_druggability": 2.0,
        "manual_direction_score": 1.0,
        "manual_safety_score": 0.5,
        "manual_prior_risk": "blocking",
        "manual_blocker": "LXR/ABCA1 is biologically coherent but broad lipid-metabolic prior art and lipogenesis/safety liabilities block a novel V3 target claim.",
    },
    "PPAR_RXR_RESOLUTION": {
        "genes": ["PPARG", "PPARA", "PPARD", "RXRA", "RXRB", "RXRG"],
        "route_class": "nuclear lipid-sensor resolution",
        "desired_direction": "agonize pro-resolution macrophage lipid programs",
        "modality": "PPAR/RXR agonists",
        "manual_druggability": 2.5,
        "manual_direction_score": 1.0,
        "manual_safety_score": 0.5,
        "manual_prior_risk": "blocking",
        "manual_blocker": "PPAR/RXR biology is broad, metabolic, and heavily prior-arted; V3 perturbation data do not show module-selective benefit.",
    },
    "LIPA_LAL_ENHANCEMENT": {
        "genes": ["LIPA"],
        "route_class": "lysosomal lipid clearance enzyme",
        "desired_direction": "enhance or replace lysosomal acid lipase; inhibition is wrong direction",
        "modality": "enzyme replacement, targeted enzyme, mRNA/LNP, or gene delivery concept",
        "manual_druggability": 1.75,
        "manual_direction_score": 1.0,
        "manual_safety_score": 1.5,
        "manual_prior_risk": "high",
        "manual_blocker": "Earlier V3 work parked LIPA: support is epithelial/ductal/keratinocyte-skewed, myeloid direction is inconsistent, and CNS repair prior art crowds the MS claim.",
        "route_summary_key": "LIPA_LAL_enhancement",
    },
    "NPC1_NPC2_CHOLESTEROL_EGRESS": {
        "genes": ["NPC1", "NPC2"],
        "route_class": "lysosomal cholesterol egress",
        "desired_direction": "enhance cholesterol egress/lysosomal export",
        "modality": "chaperone/cyclodextrin-like or gene/protein rescue concepts",
        "manual_druggability": 1.5,
        "manual_direction_score": 1.0,
        "manual_safety_score": 1.0,
        "manual_prior_risk": "medium",
        "manual_blocker": "V3 found NPC1/NPC2 to be readout-like; clinical-style enhancement is not autoimmune-validated and CNS/peripheral delivery is unresolved.",
        "route_summary_key": "NPC1_NPC2_cholesterol_egress",
    },
    "GPNMB_REPAIR_STATE_HANDLE": {
        "genes": ["GPNMB"],
        "route_class": "surface repair-state marker/possible delivery handle",
        "desired_direction": "use as state marker or delivery handle, not chronic depletion",
        "modality": "antibody/ADC precedent exists but autoimmune repair direction would require non-depleting delivery",
        "manual_druggability": 1.5,
        "manual_direction_score": 0.5,
        "manual_safety_score": 1.0,
        "manual_prior_risk": "high",
        "manual_blocker": "Strong MS foamy-state marker but local autoimmune direction is mixed and oncology-style targeting is therapeutically misaligned.",
    },
    "CD200_CD200R_MYeloid_RESOLUTION": {
        "genes": ["CD200", "CD200R1"],
        "route_class": "inhibitory myeloid checkpoint",
        "desired_direction": "provide CD200-like inhibitory/resolution signal",
        "modality": "CD200-Fc or agonist biologic concept",
        "manual_druggability": 1.5,
        "manual_direction_score": 1.0,
        "manual_safety_score": 1.0,
        "manual_prior_risk": "high",
        "manual_blocker": "Checkpoint biology is plausible but not lipid-resolution specific; prior Wave19 found state coupling below gate and crowded prior art.",
    },
    "CD300_RESOLUTION_CHECKPOINT": {
        "genes": ["CD300A", "CD300C", "CD300E", "CD300LF"],
        "route_class": "lipid/apoptotic-cell checkpoint receptor family",
        "desired_direction": "agonize inhibitory CD300 family signals or tune apoptotic-cell recognition; direction is receptor-specific",
        "modality": "antibody/ligand concepts, no mature autoimmune-grade route identified",
        "manual_druggability": 1.0,
        "manual_direction_score": 0.5,
        "manual_safety_score": 1.0,
        "manual_prior_risk": "medium",
        "manual_blocker": "Family-level direction is ambiguous and local V3 checkpoint analyses did not show state-coupled support.",
    },
    "SIRPA_CD47_EATME_BALANCE": {
        "genes": ["SIRPA", "CD47", "CALR", "LRP1"],
        "route_class": "efferocytosis eat-me/don't-eat-me balance",
        "desired_direction": "increase pathogenic debris clearance without erythrocyte/host-cell toxicity; oncology CD47 blockade is not directly transferable",
        "modality": "CD47/SIRPA antibodies, engineered fragments, or cargo-specific efferocytosis concepts",
        "manual_druggability": 2.0,
        "manual_direction_score": 0.5,
        "manual_safety_score": 0.25,
        "manual_prior_risk": "blocking",
        "manual_blocker": "CD47/SIRPA is druggable but systemic phagocytosis toxicity and oncology prior art make autoimmune transfer unsafe without cargo/cell specificity.",
    },
    "IL10_RESOLUTION_AXIS": {
        "genes": ["IL10", "IL10RA", "IL10RB"],
        "route_class": "anti-inflammatory cytokine resolution",
        "desired_direction": "augment IL-10 signaling in a targeted way",
        "modality": "cytokine, mutein, tissue-targeted biologic, or gene delivery",
        "manual_druggability": 1.75,
        "manual_direction_score": 1.0,
        "manual_safety_score": 1.0,
        "manual_prior_risk": "blocking",
        "manual_blocker": "IL-10 augmentation is known and clinically difficult; earlier V3 parked it only as comparator because broad cytokine delivery lacks novelty/selectivity.",
    },
    "NFE2L2_NRF2_RESOLUTION": {
        "genes": ["NFE2L2", "KEAP1", "HMOX1", "NQO1"],
        "route_class": "oxidative-stress/pro-resolution transcriptional program",
        "desired_direction": "activate NRF2-like resolution/antioxidant program",
        "modality": "fumarates/KEAP1-NRF2 activators",
        "manual_druggability": 2.5,
        "manual_direction_score": 1.0,
        "manual_safety_score": 1.0,
        "manual_prior_risk": "blocking",
        "manual_blocker": "NRF2 activation is already clinically established in MS via fumarate-class biology and is not a novel cross-autoimmune V3 finding.",
    },
    "MAF_KLF4_RESOLUTION_MACROPHAGE_SWITCH": {
        "genes": ["MAF", "MAFB", "KLF4"],
        "route_class": "resolution macrophage transcriptional switch",
        "desired_direction": "increase reparative macrophage identity without disabling host defense",
        "modality": "no direct selective modality; indirect cytokine/metabolic routes are broad",
        "manual_druggability": 0.5,
        "manual_direction_score": 1.0,
        "manual_safety_score": 1.0,
        "manual_prior_risk": "medium",
        "manual_blocker": "Mechanistically attractive state switch, but transcription factors lack a realistic selective intervention point in this session.",
    },
}


def read_table(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path, sep="\t")


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None or pd.isna(value):
            return default
        return float(value)
    except Exception:
        return default


def prior_penalty(label: str) -> float:
    return {"low": 0.0, "medium": 1.0, "high": 3.0, "blocking": 4.0}.get(label, 2.0)


def split_diseases(value: Any) -> set[str]:
    if value is None or pd.isna(value):
        return set()
    return {x.strip() for x in str(value).replace("|", ";").split(";") if x.strip()}


def subset_by_genes(df: pd.DataFrame, genes: list[str]) -> pd.DataFrame:
    if df.empty or "gene" not in df.columns:
        return pd.DataFrame()
    return df[df["gene"].astype(str).str.upper().isin({g.upper() for g in genes})].copy()


def max_numeric(df: pd.DataFrame, col: str) -> float:
    if df.empty or col not in df.columns:
        return 0.0
    return float(pd.to_numeric(df[col], errors="coerce").fillna(0).max())


def min_numeric(df: pd.DataFrame, col: str, default: float = 1.0) -> float:
    if df.empty or col not in df.columns:
        return default
    ser = pd.to_numeric(df[col], errors="coerce").dropna()
    return float(ser.min()) if len(ser) else default


def union_diseases(df: pd.DataFrame, cols: list[str]) -> set[str]:
    out: set[str] = set()
    if df.empty:
        return out
    for col in cols:
        if col in df.columns:
            for value in df[col].dropna():
                out |= split_diseases(value)
    return out


def cache_json(name: str, url: str, sleep_s: float = 0.2) -> dict[str, Any]:
    RAW.mkdir(parents=True, exist_ok=True)
    path = RAW / f"{name}.json"
    if path.exists():
        try:
            return json.loads(path.read_text())
        except Exception:
            pass
    try:
        req = Request(url, headers={"User-Agent": USER_AGENT})
        with urlopen(req, timeout=25) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
        path.write_text(json.dumps({"url": url, "payload": payload}, indent=2, sort_keys=True))
        time.sleep(sleep_s)
        return {"url": url, "payload": payload}
    except Exception as exc:
        path.write_text(json.dumps({"url": url, "error": repr(exc)}, indent=2, sort_keys=True))
        return {"url": url, "error": repr(exc)}


def europepmc_count(route: str, genes: list[str]) -> tuple[int, list[str]]:
    query = f'({" OR ".join(genes)}) AND ({AUTOIMMUNE_QUERY})'
    url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search?" + urlencode(
        {"query": query, "format": "json", "pageSize": 3, "resultType": "core"}
    )
    data = cache_json(f"europepmc_{route}", url)
    payload = data.get("payload", {})
    count = int(payload.get("hitCount", 0) or 0)
    titles = []
    for row in payload.get("resultList", {}).get("result", [])[:3]:
        title = row.get("title")
        year = row.get("pubYear") or row.get("firstPublicationDate")
        if title:
            titles.append(f"{year}: {title}")
    return count, titles


def clinicaltrials_count(route: str, genes: list[str]) -> int:
    term = " OR ".join(genes[:4])
    url = "https://clinicaltrials.gov/api/v2/studies?" + urlencode(
        {
            "query.term": term,
            "query.cond": "autoimmune OR multiple sclerosis OR rheumatoid arthritis OR lupus OR Crohn OR psoriasis",
            "format": "json",
            "pageSize": 1,
            "countTotal": "true",
        }
    )
    data = cache_json(f"clinicaltrials_{route}", url)
    payload = data.get("payload", {})
    return int(payload.get("totalCount", 0) or 0)


def chembl_target_activity_count(route: str, genes: list[str]) -> tuple[int, str]:
    total = 0
    best_target = ""
    for gene in genes[:4]:
        url = "https://www.ebi.ac.uk/chembl/api/data/target/search.json?" + urlencode({"q": gene})
        data = cache_json(f"chembl_target_{route}_{gene}", url, sleep_s=0.1)
        targets = data.get("payload", {}).get("targets", [])
        target_id = ""
        for target in targets:
            if target.get("organism") == "Homo sapiens":
                target_id = target.get("target_chembl_id") or ""
                best_target = best_target or f"{gene}:{target_id}:{target.get('pref_name', '')}"
                break
        if not target_id:
            continue
        act_url = f"https://www.ebi.ac.uk/chembl/api/data/activity.json?limit=1&target_chembl_id={target_id}&standard_units=nM"
        act = cache_json(f"chembl_activity_{route}_{gene}_{target_id}", act_url, sleep_s=0.1)
        total += int(act.get("payload", {}).get("page_meta", {}).get("total_count", 0) or 0)
    return total, best_target


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)

    tables = {name: read_table(path) for name, path in PATHS.items()}
    rows: list[dict[str, Any]] = []
    gene_rows: list[dict[str, Any]] = []
    gate_rows: list[dict[str, Any]] = []

    for route, meta in ROUTES.items():
        genes = meta["genes"]
        cross = subset_by_genes(tables["cross_gene"], genes)
        broad = subset_by_genes(tables["broad_gene"], genes)
        residual = subset_by_genes(tables["residual"], genes)
        surface = subset_by_genes(tables["surface"], genes)
        accessible = subset_by_genes(tables["accessible"], genes)
        foundation = subset_by_genes(tables["foundation"], genes)
        checkpoint = subset_by_genes(tables["checkpoint"], genes)
        controller = subset_by_genes(tables["controller_triage"], genes)
        genetics = subset_by_genes(tables["genetics"], genes)
        target_first = subset_by_genes(tables["target_first"], genes)
        direct = tables["direct"]
        if not direct.empty and "candidate" in direct.columns:
            direct_sub = direct[
                direct["candidate"].astype(str).str.upper().str.replace("_KO", "", regex=False).isin(
                    {g.upper() for g in genes}
                )
            ].copy()
        else:
            direct_sub = pd.DataFrame()

        route_summary_key = meta.get("route_summary_key", "")
        lysosomal_route = pd.DataFrame()
        lys = tables["lysosomal_routes"]
        if route_summary_key and not lys.empty and "route" in lys.columns:
            lysosomal_route = lys[lys["route"].astype(str) == route_summary_key].copy()

        local_breadth = max(
            max_numeric(cross, "n_trend_or_better_diseases"),
            max_numeric(broad, "positive_disease_count"),
            max_numeric(residual, "retained_positive_disease_count"),
            max_numeric(surface, "n_delta_trend_or_better_diseases"),
            max_numeric(accessible, "local_recurrence_disease_count_union"),
            max_numeric(checkpoint, "local_recurrence_disease_count_union"),
            max_numeric(controller, "broad_positive_disease_count"),
            max_numeric(lysosomal_route, "max_local_recurrence"),
        )
        negative_breadth = max(
            max_numeric(cross, "n_negative_trend_diseases"),
            max_numeric(broad, "negative_disease_count"),
            max_numeric(surface, "n_delta_negative_trend_diseases"),
            max_numeric(controller, "broad_negative_disease_count"),
            max_numeric(lysosomal_route, "max_local_negative"),
        )
        state_coupling = max(
            max_numeric(surface, "n_state_resid_non_ifn_r_ge_0_35_diseases"),
            max_numeric(surface, "n_state_resid_with_ifn_r_ge_0_25_diseases"),
            max_numeric(accessible, "local_state_coupled_disease_count_union"),
            max_numeric(checkpoint, "local_state_coupled_count_union"),
            max_numeric(controller, "orchestrator_residual_state_support_diseases"),
            max_numeric(lysosomal_route, "max_local_state_support"),
        )
        confounder_dominant = max(
            max_numeric(surface, "n_confounder_dominant_diseases"),
            max_numeric(controller, "surface_confounder_dominant_diseases"),
        )
        ms_anchor_delta = max(
            max_numeric(broad, "ms_wm_delta_log2"),
            max_numeric(accessible, "broad_ms_wm_delta_log2"),
            max_numeric(controller, "ms_wm_delta_log2"),
        )
        ms_anchor_p = min(
            min_numeric(broad, "ms_wm_p", default=1.0),
            min_numeric(accessible, "broad_ms_wm_p", default=1.0),
            min_numeric(controller, "ms_wm_p", default=1.0),
        )
        ms_anchor = ms_anchor_delta > 0 and ms_anchor_p < 0.1
        genetics_disease_count = max(
            max_numeric(genetics, "ot_n_diseases_score_ge_0_5"),
            max_numeric(target_first, "genetics_diseases_ge_0_5"),
            max_numeric(accessible, "local_opentargets_disease_rows"),
            max_numeric(controller, "opentargets_diseases_score_ge_0_5"),
        )
        genetics_ready = max(
            max_numeric(genetics, "genetics_ready_score"),
            max_numeric(target_first, "genetics_ready_score"),
        )
        foundation_contexts = max(
            max_numeric(foundation, "total_support_contexts"),
            max_numeric(controller, "geneformer_support_contexts"),
            max_numeric(controller, "geneformer_strong_support_contexts"),
        )
        best_direct_selectivity = max_numeric(direct_sub, "best_direct_selectivity_score")
        best_direct_margin = max_numeric(direct_sub, "best_direct_target_vs_ifn_margin")
        direct_selective = best_direct_selectivity >= 0.75 and best_direct_margin >= 0.75

        epmc_count, epmc_titles = europepmc_count(route, genes)
        ct_count = clinicaltrials_count(route, genes)
        chembl_count, chembl_best = chembl_target_activity_count(route, genes)

        supporting_diseases = union_diseases(
            cross,
            ["supporting_diseases"],
        ) | union_diseases(
            broad,
            ["positive_diseases"],
        ) | union_diseases(
            residual,
            ["top_retained_tests"],
        ) | union_diseases(
            surface,
            ["delta_supporting_diseases", "resid_non_ifn_supporting_diseases"],
        ) | union_diseases(
            accessible,
            ["local_recurrence_disease_union", "local_state_coupled_disease_union"],
        ) | union_diseases(
            checkpoint,
            ["local_recurrence_disease_union", "local_state_coupled_union"],
        )

        druggability = safe_float(meta["manual_druggability"])
        direction_score = safe_float(meta["manual_direction_score"])
        safety_score = safe_float(meta["manual_safety_score"])
        prior = prior_penalty(meta["manual_prior_risk"])

        gates = {
            "local_breadth_at_least_5_or_strong_state_specific_4": local_breadth >= 5
            or (local_breadth >= 4 and state_coupling >= 4),
            "ms_anchor_present": ms_anchor,
            "state_coupling_not_density_only": state_coupling >= 3 and confounder_dominant <= 3,
            "genetic_or_real_perturbation_anchor": genetics_disease_count >= 4 or direct_selective,
            "correct_direction_modality": druggability >= 1.5 and direction_score >= 1.0,
            "repair_safety_not_obviously_wrong": safety_score >= 1.0,
            "not_prior_art_blocked": prior < 3,
            "has_independent_validation_channel": direct_selective or foundation_contexts >= 3 or genetics_disease_count >= 4,
        }
        failures = [gate for gate, passed in gates.items() if not passed]

        score = (
            1.25 * min(local_breadth, 7)
            + 1.25 * min(state_coupling, 7)
            + 1.0 * (2.0 if ms_anchor else 0.0)
            + 0.7 * min(genetics_disease_count, 8)
            + 1.5 * (1.0 if direct_selective else 0.0)
            + 0.25 * min(foundation_contexts, 6)
            + 0.75 * druggability
            + 0.5 * direction_score
            + 0.5 * safety_score
            - 0.8 * min(negative_breadth, 5)
            - 0.5 * min(confounder_dominant, 6)
            - 1.5 * prior
            - (1.0 if epmc_count > 5000 else 0.0)
            - (1.0 if ct_count > 3 else 0.0)
        )

        if all(gates.values()):
            call = "GO_TO_HOSTILE_NOVELTY_REVIEW"
        elif (
            gates["local_breadth_at_least_5_or_strong_state_specific_4"]
            and gates["ms_anchor_present"]
            and gates["correct_direction_modality"]
            and not gates["genetic_or_real_perturbation_anchor"]
        ):
            call = "PARK_RESOLUTION_BIOLOGY_NO_CAUSAL_ANCHOR"
        elif gates["local_breadth_at_least_5_or_strong_state_specific_4"] and not gates["not_prior_art_blocked"]:
            call = "NO_GO_RESOLUTION_PRIOR_ART_BLOCKED"
        elif local_breadth >= 3 or state_coupling >= 3:
            call = "NO_GO_RESOLUTION_MARKER_OR_UNVALIDATED_ROUTE"
        else:
            call = "NO_GO_RESOLUTION_ROUTE"

        row = {
            "route": route,
            "genes": ";".join(genes),
            "route_class": meta["route_class"],
            "desired_direction": meta["desired_direction"],
            "modality": meta["modality"],
            "local_breadth": local_breadth,
            "negative_breadth": negative_breadth,
            "state_coupling": state_coupling,
            "confounder_dominant": confounder_dominant,
            "ms_anchor_delta": ms_anchor_delta,
            "ms_anchor_p_min": ms_anchor_p,
            "ms_anchor": bool(ms_anchor),
            "genetics_disease_count": genetics_disease_count,
            "genetics_ready_score": genetics_ready,
            "foundation_contexts": foundation_contexts,
            "best_direct_selectivity": best_direct_selectivity,
            "best_direct_margin": best_direct_margin,
            "direct_selective": bool(direct_selective),
            "manual_druggability": druggability,
            "manual_direction_score": direction_score,
            "manual_safety_score": safety_score,
            "manual_prior_risk": meta["manual_prior_risk"],
            "europepmc_autoimmune_hit_count": epmc_count,
            "clinicaltrials_autoimmune_count": ct_count,
            "chembl_nM_activity_count_first4_genes": chembl_count,
            "chembl_best_target_snapshot": chembl_best,
            "supporting_diseases_union": ";".join(sorted(supporting_diseases)),
            "supporting_disease_count_union": len(supporting_diseases),
            "resolution_rescue_score": score,
            "n_gate_failures": len(failures),
            "gate_failures": ";".join(failures),
            "wave32_call": call,
            "manual_blocker": meta["manual_blocker"],
            "europepmc_top_titles": " || ".join(epmc_titles),
        }
        rows.append(row)

        for gene in genes:
            gsub = subset_by_genes(broad, [gene])
            gene_rows.append(
                {
                    "route": route,
                    "gene": gene,
                    "broad_positive_disease_count": max_numeric(gsub, "positive_disease_count"),
                    "broad_negative_disease_count": max_numeric(gsub, "negative_disease_count"),
                    "broad_ms_wm_delta_log2": max_numeric(gsub, "ms_wm_delta_log2"),
                    "broad_ms_wm_p": min_numeric(gsub, "ms_wm_p", default=np.nan),
                    "cross_trend_or_better_diseases": max_numeric(subset_by_genes(cross, [gene]), "n_trend_or_better_diseases"),
                    "surface_resid_state_diseases": max_numeric(
                        subset_by_genes(surface, [gene]), "n_state_resid_non_ifn_r_ge_0_35_diseases"
                    ),
                    "genetics_disease_count": max_numeric(subset_by_genes(genetics, [gene]), "ot_n_diseases_score_ge_0_5"),
                    "target_first_call": ";".join(
                        sorted(
                            set(
                                subset_by_genes(target_first, [gene])
                                .get("gate_call", pd.Series(dtype=str))
                                .dropna()
                                .astype(str)
                            )
                        )
                    ),
                }
            )

        for gate, passed in gates.items():
            gate_rows.append({"route": route, "gate": gate, "passed": bool(passed), "score": score, "call": call})

    ranked = pd.DataFrame(rows).sort_values("resolution_rescue_score", ascending=False)
    ranked.to_csv(OUT / "resolution_rescue_route_audit.tsv", sep="\t", index=False)
    pd.DataFrame(gene_rows).to_csv(OUT / "resolution_rescue_gene_detail.tsv", sep="\t", index=False)
    pd.DataFrame(gate_rows).to_csv(OUT / "resolution_rescue_gate_matrix.tsv", sep="\t", index=False)

    summary = {
        "seed": SEED,
        "n_routes": int(len(ranked)),
        "call_counts": ranked["wave32_call"].value_counts().to_dict(),
        "top_routes": ranked.head(8)[
            [
                "route",
                "resolution_rescue_score",
                "wave32_call",
                "local_breadth",
                "state_coupling",
                "ms_anchor",
                "genetics_disease_count",
                "direct_selective",
                "manual_prior_risk",
                "manual_blocker",
            ]
        ].to_dict(orient="records"),
        "interpretation": (
            "Resolution/efferocytosis biology is mechanistically relevant, but no audited route combines "
            "cross-disease state recurrence, MS anchoring, target-level causal/perturbation evidence, "
            "correct-direction druggability, and non-blocking prior art."
        ),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
