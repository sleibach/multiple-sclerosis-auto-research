#!/usr/bin/env python3
"""Wave30 upstream niche-driver audit.

V3 has repeatedly reproduced a cross-autoimmune IFN/HLA-II/CD74/GILT/APC
transition and an adjacent lipid-lysosomal myeloid module, but direct marker,
enzyme, checkpoint, genetics-first, and target-first therapeutic routes have
failed. This script asks a different question:

Can an upstream ligand/receptor/niche-driver axis explain the recurrent state
and provide a tractable intervention point without merely targeting module
markers?

The audit integrates only already generated local V3 evidence plus lightweight
public API hit counts cached in this wave. A positive call here would only
justify hostile novelty review; it is not itself a therapeutic finding.
"""

from __future__ import annotations

import json
import math
import time
from pathlib import Path
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results_v3" / "wave30_niche_driver_audit"
RAW = OUT / "raw_api"
SEED = 20260527
USER_AGENT = "ms-auto-research-wave30-niche-driver-audit/1.0"


PATHS = {
    "axis_rank": ROOT / "results_v3" / "disease_axis_convergence_rank.tsv",
    "axis_gene_rank": ROOT / "results_v3" / "disease_axis_candidate_gene_rank.tsv",
    "transition": ROOT / "results_v3" / "cross_disease_transition_summary.tsv",
    "gene_convergence": ROOT / "results_v3" / "cross_disease_gene_convergence.tsv",
    "surface": ROOT / "results_v3" / "wave15_surface_trafficking_dependency" / "candidate_ranked.tsv",
    "dependency": ROOT
    / "results_v3"
    / "wave15_orchestrator_dependency_scan"
    / "candidate_dependency_priority_summary.tsv",
    "accessible": ROOT / "results_v3" / "wave18_accessible_target_rescue" / "accessible_target_rescue_candidates.tsv",
    "foundation": ROOT / "results_v3" / "wave18_foundation_rescue" / "foundation_rescue_candidate_rank.tsv",
    "direct_perturb": ROOT / "results_v3" / "wave15_perturbation_drug_response" / "candidate_level_synthesis.tsv",
    "checkpoint": ROOT / "results_v3" / "wave19_tolerogenic_checkpoint" / "checkpoint_candidate_synthesis.tsv",
    "lysosomal": ROOT / "results_v3" / "wave19_lysosomal_controller" / "route_summary.tsv",
    "nonexpression": ROOT
    / "results_v3"
    / "wave23_orchestrator_nonexpression_axis_triage"
    / "wave23_route_triage.tsv",
    "genetics": ROOT / "results_v3" / "wave25_causal_genetics_module_proxy" / "causal_proxy_candidate_matrix.tsv",
    "target_first": ROOT / "results_v3" / "wave28_target_first_rescue" / "target_first_rescue_matrix.tsv",
}


DISEASE_CONDITION_QUERY = (
    '"multiple sclerosis" OR "rheumatoid arthritis" OR lupus OR Crohn OR '
    '"ulcerative colitis" OR psoriasis OR Sjogren OR "type 1 diabetes" OR '
    'celiac OR "autoimmune thyroid" OR autoimmune'
)


AXES: dict[str, dict[str, Any]] = {
    "IFNG_IFNGR_JAK_STAT1_CIITA": {
        "genes": ["IFNG", "IFNGR1", "IFNGR2", "JAK1", "JAK2", "STAT1", "IRF1", "CIITA", "CD74", "IFI30"],
        "core_intervention_genes": ["IFNGR1", "IFNGR2", "JAK1", "JAK2", "STAT1"],
        "state_axes": ["ifn_apc"],
        "role": "canonical inflammatory niche driver of HLA-II/CD74/GILT APC transition",
        "direction": "blockade suppresses state but is broad IFN/JAK immunosuppression",
        "modality": "JAK inhibitors, IFN-gamma/IFNGR pathway blockade, STAT/CIITA perturbation",
        "non_marker_upstream": True,
        "manual_druggability": 3.0,
        "manual_selectivity": 0.0,
        "manual_prior_risk": "blocking",
        "manual_blocker": "Real perturbation support is strong but non-selective; direct JAK/IFN blockade collapses host-defense programs and is saturated prior art.",
    },
    "TNF_TNFR_NFKB": {
        "genes": ["TNF", "TNFRSF1A", "TNFRSF1B", "NFKB1", "RELA", "CHUK"],
        "core_intervention_genes": ["TNF", "TNFRSF1A", "TNFRSF1B"],
        "state_axes": ["ifn_apc"],
        "role": "inflammatory costimulus feeding APC and tissue injury programs",
        "direction": "block TNF/TNFR signaling",
        "modality": "approved biologics and small-molecule pathway comparators",
        "non_marker_upstream": True,
        "manual_druggability": 3.0,
        "manual_selectivity": 0.0,
        "manual_prior_risk": "blocking",
        "manual_blocker": "Therapeutic class is already central across autoimmunity and can worsen demyelinating disease; not a new MS/cross-autoimmune intervention point.",
    },
    "OSM_OSMR_IL6ST_STAT3": {
        "genes": ["OSM", "OSMR", "IL6ST", "STAT3", "SOCS3"],
        "core_intervention_genes": ["OSM", "OSMR", "IL6ST"],
        "state_axes": ["ifn_apc", "hif_nampt_metabolic"],
        "role": "tissue-licensing cytokine axis in barrier/stromal injury compartments",
        "direction": "block OSM/OSMR if local tissue remodeling drives APC transition",
        "modality": "anti-OSM/OSMR biologic concept",
        "non_marker_upstream": True,
        "manual_druggability": 2.5,
        "manual_selectivity": 1.0,
        "manual_prior_risk": "medium_high",
        "manual_blocker": "Earlier V3 local quant found strongest support in UC/Crohn/T1D compartments but absent/ambiguous MS evidence.",
    },
    "MIF_CD74_CXCR4_CD44": {
        "genes": ["MIF", "DDT", "CD74", "CXCR4", "CD44"],
        "core_intervention_genes": ["MIF", "CD74", "CXCR4", "CD44"],
        "state_axes": ["ifn_apc"],
        "role": "MIF-responsive CD74/CD44/CXCR4 receptor state at inflamed tissue interfaces",
        "direction": "MIF/CD74-axis antagonism or stratified modulation",
        "modality": "MIF inhibitors, CD74/CXCR4/CD44 biologics or small molecules",
        "non_marker_upstream": True,
        "manual_druggability": 2.0,
        "manual_selectivity": 0.5,
        "manual_prior_risk": "blocking",
        "manual_blocker": "V3 residualization demoted this to biomarker-only; direct therapeutic direction is crowded and receptor state is a marker of IFN/APC activation.",
    },
    "SPP1_CD44_INTEGRIN_RETENTION": {
        "genes": ["SPP1", "CD44", "ITGAV", "ITGB1", "ITGB3", "ITGAM"],
        "core_intervention_genes": ["SPP1", "CD44", "ITGAV", "ITGB1", "ITGAM"],
        "state_axes": ["lipid_loader_repair", "complement_phagocytosis"],
        "role": "osteopontin/adhesion-retention route around lipid-loaded myeloid repair/injury states",
        "direction": "block pathogenic retention only if repair-preserving window exists",
        "modality": "neutralizing antibodies, integrin/CD44 modulation",
        "non_marker_upstream": True,
        "manual_druggability": 2.0,
        "manual_selectivity": 0.5,
        "manual_prior_risk": "high",
        "manual_blocker": "Direction is context dependent: the same axis can mark repair, fibrosis, retention, and leukocyte migration.",
    },
    "CXCL10_CXCR3_RECRUITMENT": {
        "genes": ["CXCL10", "CXCL9", "CXCL11", "CXCR3"],
        "core_intervention_genes": ["CXCL10", "CXCR3"],
        "state_axes": ["ifn_apc"],
        "role": "IFN-inducible chemokine recruitment loop coupling inflamed tissue and CXCR3+ lymphocytes",
        "direction": "block CXCL10/CXCR3 recruitment",
        "modality": "antibodies or chemokine receptor antagonists",
        "non_marker_upstream": True,
        "manual_druggability": 2.0,
        "manual_selectivity": 0.5,
        "manual_prior_risk": "high",
        "manual_blocker": "Likely downstream of IFN state rather than an upstream controller; recruitment blockade is crowded and not lesion-state selective.",
    },
    "CCL2_CCR2_MONOCYTE_RECRUITMENT": {
        "genes": ["CCL2", "CCR2", "CCL7", "CCL8"],
        "core_intervention_genes": ["CCL2", "CCR2"],
        "state_axes": ["complement_phagocytosis", "hif_nampt_metabolic"],
        "role": "monocyte recruitment into inflamed tissues",
        "direction": "block CCL2/CCR2 recruitment",
        "modality": "CCR2 antagonists or ligand antibodies",
        "non_marker_upstream": True,
        "manual_druggability": 2.0,
        "manual_selectivity": 0.5,
        "manual_prior_risk": "high",
        "manual_blocker": "Recruitment blockade is not the same as reversing resident lipid-lysosomal/APC state; prior inflammatory trials are extensive.",
    },
    "CD40_CD40LG_APC_LICENSING": {
        "genes": ["CD40", "CD40LG", "TRAF2", "TRAF3", "TRAF6", "NFKB1", "RELA"],
        "core_intervention_genes": ["CD40", "CD40LG"],
        "state_axes": ["ifn_apc"],
        "role": "T-cell/APC licensing signal that can sustain antigen presentation",
        "direction": "block CD40/CD40LG costimulation",
        "modality": "anti-CD40/CD40L biologics",
        "non_marker_upstream": True,
        "manual_druggability": 2.5,
        "manual_selectivity": 0.5,
        "manual_prior_risk": "blocking",
        "manual_blocker": "Known autoimmune costimulation axis with safety/prior-art saturation; not specific to lipid-lysosomal module.",
    },
    "TREM1_TYROBP_AMPLIFICATION": {
        "genes": ["TREM1", "TYROBP", "SYK", "NFKB1", "IL1B"],
        "core_intervention_genes": ["TREM1"],
        "state_axes": ["ifn_apc", "hif_nampt_metabolic"],
        "role": "amplifying myeloid receptor route in acute inflammatory tissues",
        "direction": "inhibit TREM1 amplification",
        "modality": "inhibitory peptide/antibody precedent",
        "non_marker_upstream": True,
        "manual_druggability": 2.0,
        "manual_selectivity": 1.0,
        "manual_prior_risk": "medium_high",
        "manual_blocker": "Earlier accessible-target audit found weak cross-disease breadth and no state-coupled support gate.",
    },
    "SLC15A4_TASL_IRF5_ENDOLYSOSOMAL_TLR": {
        "genes": ["SLC15A4", "IRF5", "TLR7", "TLR9", "MYD88", "UNC93B1"],
        "core_intervention_genes": ["SLC15A4", "IRF5"],
        "state_axes": ["ifn_apc"],
        "role": "endolysosomal nucleic-acid sensing/TASL-IRF5 inflammatory checkpoint",
        "direction": "inhibit endolysosomal TLR/TASL/IRF5 route if disease genotype or IFN module high",
        "modality": "small-molecule transporter/checkpoint inhibition is speculative; TLR inhibitors exist",
        "non_marker_upstream": True,
        "manual_druggability": 1.5,
        "manual_selectivity": 1.0,
        "manual_prior_risk": "high",
        "manual_blocker": "Strong lupus-adjacent biology but V3 lacks target-selective perturbation and non-crowded autoimmune delta.",
    },
    "LIPA_LAL_LYSOSOMAL_LIPID_CLEARANCE": {
        "genes": ["LIPA"],
        "core_intervention_genes": ["LIPA"],
        "state_axes": ["lysosomal_apc", "lipid_loader_repair"],
        "role": "lysosomal acid lipase route for lipid-loaded macrophage/epithelial stress",
        "direction": "enhance/replace LAL activity rather than inhibit",
        "modality": "enzyme replacement, targeted enzyme, mRNA/LNP, or gene delivery concept",
        "non_marker_upstream": False,
        "manual_druggability": 1.5,
        "manual_selectivity": 1.0,
        "manual_prior_risk": "medium_high",
        "manual_blocker": "Earlier V3 demoted LIPA because MS gene-level support was weak, myeloid direction was inconsistent, and delivery/MS-repair prior art blocks a claim.",
    },
    "NPC1_NPC2_CHOLESTEROL_EGRESS": {
        "genes": ["NPC1", "NPC2"],
        "core_intervention_genes": ["NPC1", "NPC2"],
        "state_axes": ["lysosomal_apc", "lipid_loader_repair"],
        "role": "lysosomal cholesterol-egress route adjacent to lipid-lysosomal stress",
        "direction": "enhance cholesterol egress or functional rescue",
        "modality": "cyclodextrin-like or chaperone/gene rescue concepts",
        "non_marker_upstream": False,
        "manual_druggability": 1.5,
        "manual_selectivity": 0.5,
        "manual_prior_risk": "medium",
        "manual_blocker": "Readout-like and delivery-heavy; earlier lysosomal-controller audit parked it without selective autoimmune perturbation.",
    },
    "ITGAM_CR3_COMPLEMENT_PHAGOCYTOSIS": {
        "genes": ["ITGAM", "ITGB2", "C3", "C1QA", "C1QB", "C1QC", "FCER1G"],
        "core_intervention_genes": ["ITGAM", "ITGB2", "C3"],
        "state_axes": ["complement_phagocytosis"],
        "role": "complement-opsonin uptake/phagocytosis axis in myeloid tissue injury and clearance",
        "direction": "restore regulated phagocytosis rather than bluntly block complement",
        "modality": "integrin/complement biologics, allosteric modulation, complement inhibitors",
        "non_marker_upstream": True,
        "manual_druggability": 2.0,
        "manual_selectivity": 0.5,
        "manual_prior_risk": "high",
        "manual_blocker": "Complement and CR3 biology is bidirectional: debris clearance can be protective while complement injury can be pathogenic.",
    },
    "CD274_PD1_TOLEROGENIC_CHECKPOINT": {
        "genes": ["CD274", "PDCD1", "PDCD1LG2"],
        "core_intervention_genes": ["CD274", "PDCD1"],
        "state_axes": ["ifn_apc"],
        "role": "PD-1/PD-L1 inhibitory checkpoint induced near IFN/APC states",
        "direction": "agonize PD-1 pathway or provide PD-L1-like tolerogenic signal",
        "modality": "PD-L1-Fc/PD-1 agonist biologic concept",
        "non_marker_upstream": True,
        "manual_druggability": 2.5,
        "manual_selectivity": 0.5,
        "manual_prior_risk": "blocking",
        "manual_blocker": "Checkpoint agonism is tractable but saturated and not module-specific in local V3.",
    },
    "CD24_SIGLEC10_DAMP_CHECKPOINT": {
        "genes": ["CD24", "SIGLEC10"],
        "core_intervention_genes": ["CD24", "SIGLEC10"],
        "state_axes": ["ifn_apc"],
        "role": "DAMP/glycan inhibitory checkpoint potentially dampening tissue inflammation",
        "direction": "agonize CD24-Siglec-10 checkpoint",
        "modality": "CD24Fc or engineered glyco-ligand concept",
        "non_marker_upstream": True,
        "manual_druggability": 2.0,
        "manual_selectivity": 1.0,
        "manual_prior_risk": "high",
        "manual_blocker": "Earlier checkpoint audit found local state-coupling below gate and crowded prior art.",
    },
    "LILRB_HLA_INHIBITORY_MYLOID_CHECKPOINT": {
        "genes": ["LILRB1", "LILRB2", "LILRB3", "LILRB4", "HLA-DRA", "HLA-DRB1"],
        "core_intervention_genes": ["LILRB1", "LILRB2", "LILRB4"],
        "state_axes": ["ifn_apc"],
        "role": "inhibitory HLA-sensing myeloid checkpoint superfamily",
        "direction": "agonize inhibitory LILRB signaling, not oncology-style antagonism",
        "modality": "agonist antibody/HLA-ligand biologics are concept-level",
        "non_marker_upstream": True,
        "manual_druggability": 1.5,
        "manual_selectivity": 1.0,
        "manual_prior_risk": "medium_high",
        "manual_blocker": "Disease-state coupling is weak in V3 checkpoint audit and therapeutic format direction is immature.",
    },
    "GPR65_ENDOLYSOSOMAL_PH_CAMP": {
        "genes": ["GPR65"],
        "core_intervention_genes": ["GPR65"],
        "state_axes": ["lysosomal_apc", "hif_nampt_metabolic"],
        "role": "acidic-tissue pH-sensing GPCR potentially buffering endolysosomal inflammation",
        "direction": "agonize or positively modulate if protective loss-of-function is supported",
        "modality": "small-molecule GPCR agonist/PAM concept",
        "non_marker_upstream": True,
        "manual_druggability": 2.5,
        "manual_selectivity": 1.5,
        "manual_prior_risk": "high",
        "manual_blocker": "Wave23 parked GPR65: genetics and druggability exist, but local module evidence and positive perturbation/model alignment are absent.",
    },
    "PTPN2_TCPTP_RESTORATION": {
        "genes": ["PTPN2", "JAK1", "JAK2", "STAT1"],
        "core_intervention_genes": ["PTPN2"],
        "state_axes": ["ifn_apc"],
        "role": "genetic cytokine-signaling brake benchmark for the IFN/APC transition",
        "direction": "restore TCPTP activity; inhibitors are wrong direction",
        "modality": "target-selective restoration/stabilization would be required",
        "non_marker_upstream": True,
        "manual_druggability": 0.5,
        "manual_selectivity": 0.5,
        "manual_prior_risk": "high",
        "manual_blocker": "Wave29 model found no selective suppression window under stated assumptions and no clinical-ready restoration modality exists.",
    },
}


def read_table(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path, sep="\t")


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None or (isinstance(value, float) and math.isnan(value)):
            return default
        if pd.isna(value):
            return default
        return float(value)
    except Exception:
        return default


def max_for_genes(df: pd.DataFrame, gene_col: str, genes: list[str], col: str) -> float:
    if df.empty or gene_col not in df.columns or col not in df.columns:
        return 0.0
    sub = df[df[gene_col].astype(str).isin(genes)]
    if sub.empty:
        return 0.0
    vals = pd.to_numeric(sub[col], errors="coerce")
    if vals.notna().any():
        return float(vals.max())
    return 0.0


def joined_for_genes(df: pd.DataFrame, gene_col: str, genes: list[str], col: str) -> str:
    if df.empty or gene_col not in df.columns or col not in df.columns:
        return ""
    values: set[str] = set()
    for entry in df[df[gene_col].astype(str).isin(genes)][col].dropna().astype(str):
        for token in entry.replace(",", ";").split(";"):
            token = token.strip()
            if token:
                values.add(token)
    return ";".join(sorted(values))


def count_diseases(joined: str) -> int:
    if not joined:
        return 0
    return len({x.strip() for x in joined.split(";") if x.strip()})


def api_json(url: str, cache_path: Path, delay: float = 0.15) -> dict[str, Any]:
    if cache_path.exists():
        try:
            return json.loads(cache_path.read_text())
        except json.JSONDecodeError:
            pass
    req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    try:
        with urlopen(req, timeout=20) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except Exception as exc:
        payload = {"_error": repr(exc), "_url": url}
    cache_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    time.sleep(delay)
    return payload


def europepmc_count(term: str, cache_key: str) -> tuple[int | None, str]:
    query = f'({term}) AND ({DISEASE_CONDITION_QUERY})'
    params = urlencode({"query": query, "format": "json", "pageSize": 1})
    url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?{params}"
    data = api_json(url, RAW / f"europepmc_{cache_key}.json")
    if "_error" in data:
        return None, url
    return int(data.get("hitCount", 0)), url


def clinicaltrials_count(term: str, cache_key: str) -> tuple[int | None, str]:
    params = urlencode(
        {
            "query.term": term,
            "query.cond": DISEASE_CONDITION_QUERY,
            "pageSize": 1,
            "countTotal": "true",
            "format": "json",
        }
    )
    url = f"https://clinicaltrials.gov/api/v2/studies?{params}"
    data = api_json(url, RAW / f"clinicaltrials_{cache_key}.json")
    if "_error" in data:
        return None, url
    return int(data.get("totalCount", 0) or 0), url


def chembl_target_snapshot(gene: str, cache_key: str) -> dict[str, Any]:
    params = urlencode({"format": "json", "q": gene, "limit": 3})
    url = f"https://www.ebi.ac.uk/chembl/api/data/target/search.json?{params}"
    data = api_json(url, RAW / f"chembl_target_{cache_key}_{gene}.json")
    targets = data.get("targets", []) if isinstance(data, dict) else []
    best = targets[0] if targets else {}
    chembl_id = best.get("target_chembl_id", "")
    pref = best.get("pref_name", "")
    target_type = best.get("target_type", "")
    activity_count = None
    if chembl_id:
        params2 = urlencode(
            {
                "format": "json",
                "target_chembl_id": chembl_id,
                "standard_type__in": "IC50,EC50,Ki,Kd,AC50",
                "standard_units": "nM",
                "limit": 1,
            }
        )
        url2 = f"https://www.ebi.ac.uk/chembl/api/data/activity.json?{params2}"
        act = api_json(url2, RAW / f"chembl_activity_{cache_key}_{gene}_{chembl_id}.json")
        page_meta = act.get("page_meta", {}) if isinstance(act, dict) else {}
        activity_count = page_meta.get("total_count")
    return {
        "gene": gene,
        "chembl_target_chembl_id": chembl_id,
        "chembl_pref_name": pref,
        "chembl_target_type": target_type,
        "chembl_activity_records": activity_count,
    }


def prior_risk_penalty(label: str) -> float:
    return {
        "low": 0.0,
        "medium": 1.0,
        "medium_high": 2.0,
        "high": 3.0,
        "blocking": 4.0,
    }.get(label, 2.0)


def axis_public_query(axis: str, meta: dict[str, Any]) -> dict[str, Any]:
    core = meta["core_intervention_genes"]
    term = " OR ".join(core[:4])
    pmc_count, pmc_url = europepmc_count(term, axis)
    ct_count, ct_url = clinicaltrials_count(term, axis)
    chembl_rows = [chembl_target_snapshot(gene, axis) for gene in core[:3]]
    max_activity = max([safe_float(row.get("chembl_activity_records")) for row in chembl_rows] or [0.0])
    first_chembl = next((row for row in chembl_rows if row.get("chembl_target_chembl_id")), {})
    return {
        "axis": axis,
        "public_query_term": term,
        "europepmc_hit_count": pmc_count,
        "europepmc_url": pmc_url,
        "clinicaltrials_hit_count": ct_count,
        "clinicaltrials_url": ct_url,
        "max_chembl_activity_records": max_activity,
        "example_chembl_target": first_chembl.get("chembl_target_chembl_id", ""),
        "example_chembl_pref_name": first_chembl.get("chembl_pref_name", ""),
    }


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)

    tables = {name: read_table(path) for name, path in PATHS.items()}
    transition = tables["transition"]
    if transition.empty:
        transition_summary = {}
    else:
        transition_summary = transition.iloc[0].to_dict()

    axis_rank = tables["axis_rank"]
    axis_support_by_name: dict[str, dict[str, Any]] = {}
    if not axis_rank.empty:
        for _, row in axis_rank.iterrows():
            axis_support_by_name[str(row.get("axis", ""))] = row.to_dict()

    public_records = [axis_public_query(axis, meta) for axis, meta in AXES.items()]
    public_df = pd.DataFrame(public_records)
    public_df.to_csv(OUT / "niche_driver_public_query_snapshot.tsv", sep="\t", index=False)

    rows: list[dict[str, Any]] = []
    gate_rows: list[dict[str, Any]] = []

    for axis, meta in AXES.items():
        genes = meta["genes"]
        public = public_df[public_df["axis"] == axis].iloc[0].to_dict()

        axis_weighted = 0.0
        axis_strong_diseases = 0.0
        axis_supportive_diseases = 0.0
        for state_axis in meta["state_axes"]:
            support = axis_support_by_name.get(state_axis, {})
            axis_weighted = max(axis_weighted, safe_float(support.get("weighted_score")))
            axis_strong_diseases = max(axis_strong_diseases, safe_float(support.get("strong_disease_count")))
            axis_supportive_diseases = max(axis_supportive_diseases, safe_float(support.get("supportive_disease_count")))

        transition_trend_or_better = safe_float(transition_summary.get("n_trend_or_better_diseases", 0.0))
        transition_supportive = safe_float(transition_summary.get("n_supportive_or_strong_diseases", 0.0))
        transition_strong = safe_float(transition_summary.get("n_strong_diseases", 0.0))
        if "ifn_apc" not in meta["state_axes"]:
            transition_trend_or_better = 0.0
            transition_supportive = 0.0
            transition_strong = 0.0

        axis_gene_mentions = max_for_genes(tables["axis_gene_rank"], "gene", genes, "axis_mentioned_disease_count")
        axis_gene_priority = max_for_genes(tables["axis_gene_rank"], "gene", genes, "priority_score")
        axis_gene_diseases = joined_for_genes(tables["axis_gene_rank"], "gene", genes, "axis_mentioned_diseases")

        surface_delta_trend = max_for_genes(tables["surface"], "gene", genes, "n_delta_trend_or_better_diseases")
        surface_resid = max_for_genes(tables["surface"], "gene", genes, "n_state_resid_non_ifn_r_ge_0_35_diseases")
        surface_neg = max_for_genes(tables["surface"], "gene", genes, "n_delta_negative_trend_diseases")
        surface_call_genes = joined_for_genes(tables["surface"], "gene", genes, "go_no_go")

        accessible_local = max_for_genes(tables["accessible"], "gene", genes, "local_recurrence_disease_count_union")
        accessible_state = max_for_genes(tables["accessible"], "gene", genes, "local_state_coupled_disease_count_union")
        accessible_broad_pos = max_for_genes(tables["accessible"], "gene", genes, "broad_positive_disease_count")
        accessible_neg = max_for_genes(tables["accessible"], "gene", genes, "broad_negative_disease_count")
        accessible_calls = joined_for_genes(tables["accessible"], "gene", genes, "wave18_call")

        checkpoint_local = max_for_genes(tables["checkpoint"], "gene", genes, "local_recurrence_disease_count_union")
        checkpoint_state = max_for_genes(tables["checkpoint"], "gene", genes, "local_state_coupled_count_union")
        checkpoint_calls = joined_for_genes(tables["checkpoint"], "gene", genes, "wave19_call")

        genetics_diseases = max_for_genes(tables["genetics"], "gene", genes, "ot_n_diseases_score_ge_0_5")
        genetics_ready = max_for_genes(tables["genetics"], "gene", genes, "genetics_ready_score")
        genetics_call = joined_for_genes(tables["genetics"], "gene", genes, "proxy_call")

        foundation_contexts = max_for_genes(tables["foundation"], "gene", genes, "total_support_contexts")
        foundation_strong = max_for_genes(tables["foundation"], "gene", genes, "total_strong_support_contexts")
        foundation_calls = joined_for_genes(tables["foundation"], "gene", genes, "real_perturbation_alignment_call")

        direct_selectivity = max_for_genes(tables["direct_perturb"], "candidate", genes, "best_direct_selectivity_score")
        direct_suppression = max_for_genes(tables["direct_perturb"], "candidate", genes, "best_direct_target_suppression")
        direct_calls = joined_for_genes(tables["direct_perturb"], "candidate", genes, "direct_evidence_calls")

        target_first_support = max_for_genes(tables["target_first"], "gene", genes, "cross_disease_module_score")
        target_first_genetics = max_for_genes(tables["target_first"], "gene", genes, "genetics_score")
        target_first_gate = joined_for_genes(tables["target_first"], "gene", genes, "gate_call")

        lysosomal_route_call = ""
        lysosomal_local = 0.0
        if not tables["lysosomal"].empty:
            for _, lrow in tables["lysosomal"].iterrows():
                route_genes = {g.strip() for g in str(lrow.get("genes", "")).split(";") if g.strip()}
                if route_genes.intersection(genes):
                    lysosomal_local = max(lysosomal_local, safe_float(lrow.get("max_local_recurrence")))
                    if lrow.get("route_call"):
                        lysosomal_route_call += f"{lrow.get('route')}:{lrow.get('route_call')};"

        nonexpression_route_call = ""
        nonexpression_score = 0.0
        if not tables["nonexpression"].empty:
            for _, nrow in tables["nonexpression"].iterrows():
                route_genes = {g.strip() for g in str(nrow.get("genes", "")).split(";") if g.strip()}
                if route_genes.intersection(genes):
                    nonexpression_score = max(nonexpression_score, safe_float(nrow.get("priority_score")))
                    nonexpression_route_call += f"{nrow.get('route')}:{nrow.get('route_call')};"

        global_module_breadth = max(axis_supportive_diseases, transition_supportive)
        candidate_specific_breadth = max(
            axis_gene_mentions,
            surface_delta_trend,
            accessible_local,
            accessible_broad_pos,
            checkpoint_local,
            lysosomal_local,
        )
        if axis == "IFNG_IFNGR_JAK_STAT1_CIITA":
            candidate_specific_breadth = max(candidate_specific_breadth, transition_supportive)

        best_local_breadth = max(
            axis_supportive_diseases,
            transition_supportive,
            axis_gene_mentions,
            surface_delta_trend,
            accessible_local,
            accessible_broad_pos,
            checkpoint_local,
            lysosomal_local,
        )
        best_residual_or_state = max(surface_resid, accessible_state, checkpoint_state)
        best_genetics = max(genetics_diseases, target_first_genetics)
        best_perturbation = max(foundation_contexts, foundation_strong * 2.0, direct_selectivity, direct_suppression)
        max_public_prior = max(safe_float(public["europepmc_hit_count"]), safe_float(public["clinicaltrials_hit_count"]))

        # Do not let a broad IFN/APC module rescue every candidate annotated to
        # that module. Candidate-specific evidence must recur independently.
        cross_disease_support_gate = candidate_specific_breadth >= 5
        residual_state_gate = best_residual_or_state >= 3 or (
            axis == "IFNG_IFNGR_JAK_STAT1_CIITA" and transition_supportive >= 6
        )
        upstream_gate = bool(meta["non_marker_upstream"])
        causality_gate = best_genetics >= 4 or "selective_target_suppression" in direct_calls or "model_and" in foundation_calls
        perturbation_gate = best_perturbation >= 2
        druggable_gate = safe_float(meta["manual_druggability"]) >= 2
        selectivity_gate = safe_float(meta["manual_selectivity"]) >= 1.5 or (
            "selective_target_suppression" in direct_calls and direct_selectivity >= 0.75
        )
        prior_gate = prior_risk_penalty(meta["manual_prior_risk"]) < 3 and (
            safe_float(public["clinicaltrials_hit_count"]) <= 2 or pd.isna(public["clinicaltrials_hit_count"])
        )
        contradiction_gate = surface_neg + accessible_neg <= 1

        gate_map = {
            "cross_disease_support_gate": cross_disease_support_gate,
            "residual_or_state_gate": residual_state_gate,
            "upstream_non_marker_gate": upstream_gate,
            "target_causality_gate": causality_gate,
            "perturbation_or_model_gate": perturbation_gate,
            "druggable_correct_direction_gate": druggable_gate,
            "selectivity_window_gate": selectivity_gate,
            "prior_art_not_blocking_gate": prior_gate,
            "low_directional_contradiction_gate": contradiction_gate,
        }
        failures = [name for name, passed in gate_map.items() if not passed]

        centrality_score = (
            0.8 * candidate_specific_breadth
            + 0.25 * global_module_breadth
            + 0.6 * best_residual_or_state
            + 0.5 * best_genetics
            + 0.3 * best_perturbation
            + 0.2 * axis_gene_priority
            - 1.0 * (surface_neg + accessible_neg)
        )
        intervention_score = (
            0.7 * best_genetics
            + 0.8 * best_perturbation
            + 1.5 * safe_float(meta["manual_druggability"])
            + 1.5 * safe_float(meta["manual_selectivity"])
            - 2.0 * prior_risk_penalty(meta["manual_prior_risk"])
            - 1.0 * (surface_neg + accessible_neg)
        )

        if all(gate_map.values()):
            call = "GO_TO_HOSTILE_NOVELTY_REVIEW"
        elif cross_disease_support_gate and residual_state_gate and not selectivity_gate:
            call = "CENTRAL_STATE_DRIVER_NOT_SELECTIVE_THERAPEUTIC"
        elif cross_disease_support_gate and upstream_gate and druggable_gate and not prior_gate:
            call = "PARK_PRIOR_ART_OR_GENERIC_AXIS_BLOCKER"
        elif cross_disease_support_gate and upstream_gate and not causality_gate:
            call = "PARK_REQUIRES_TARGET_CAUSALITY_OR_REAL_PERTURBATION"
        else:
            call = "NO_GO_NICHE_DRIVER"

        row = {
            "axis": axis,
            "genes": ";".join(genes),
            "core_intervention_genes": ";".join(meta["core_intervention_genes"]),
            "role": meta["role"],
            "direction": meta["direction"],
            "modality": meta["modality"],
            "manual_blocker": meta["manual_blocker"],
            "manual_prior_risk": meta["manual_prior_risk"],
            "manual_druggability": meta["manual_druggability"],
            "manual_selectivity": meta["manual_selectivity"],
            "candidate_specific_breadth_diseases": candidate_specific_breadth,
            "global_module_breadth_diseases": global_module_breadth,
            "best_local_breadth_diseases": best_local_breadth,
            "best_residual_or_state_diseases": best_residual_or_state,
            "best_genetics_disease_count": best_genetics,
            "best_perturbation_or_model_score": best_perturbation,
            "axis_weighted_score": axis_weighted,
            "axis_strong_diseases": axis_strong_diseases,
            "axis_supportive_diseases": axis_supportive_diseases,
            "transition_strong_diseases": transition_strong,
            "transition_supportive_diseases": transition_supportive,
            "transition_trend_or_better_diseases": transition_trend_or_better,
            "axis_gene_mentions": axis_gene_mentions,
            "axis_gene_priority": axis_gene_priority,
            "axis_gene_diseases": axis_gene_diseases,
            "surface_delta_trend_diseases": surface_delta_trend,
            "surface_residual_state_diseases": surface_resid,
            "surface_negative_diseases": surface_neg,
            "surface_calls": surface_call_genes,
            "accessible_local_diseases": accessible_local,
            "accessible_state_diseases": accessible_state,
            "accessible_broad_positive_diseases": accessible_broad_pos,
            "accessible_negative_diseases": accessible_neg,
            "accessible_calls": accessible_calls,
            "checkpoint_local_diseases": checkpoint_local,
            "checkpoint_state_diseases": checkpoint_state,
            "checkpoint_calls": checkpoint_calls,
            "lysosomal_route_calls": lysosomal_route_call,
            "nonexpression_route_calls": nonexpression_route_call,
            "nonexpression_route_score": nonexpression_score,
            "genetics_ready_score": genetics_ready,
            "genetics_calls": genetics_call,
            "foundation_contexts": foundation_contexts,
            "foundation_strong_contexts": foundation_strong,
            "foundation_calls": foundation_calls,
            "direct_selectivity_score": direct_selectivity,
            "direct_target_suppression": direct_suppression,
            "direct_calls": direct_calls,
            "target_first_module_score": target_first_support,
            "target_first_genetics_score": target_first_genetics,
            "target_first_gate": target_first_gate,
            "europepmc_hit_count": public["europepmc_hit_count"],
            "clinicaltrials_hit_count": public["clinicaltrials_hit_count"],
            "max_chembl_activity_records": public["max_chembl_activity_records"],
            "example_chembl_target": public["example_chembl_target"],
            "example_chembl_pref_name": public["example_chembl_pref_name"],
            "centrality_score": centrality_score,
            "intervention_score": intervention_score,
            "n_gate_failures": len(failures),
            "gate_failures": ";".join(failures),
            "wave30_call": call,
        }
        rows.append(row)

        for gate, passed in gate_map.items():
            gate_rows.append(
                {
                    "axis": axis,
                    "gate": gate,
                    "passed": bool(passed),
                    "value_context": json.dumps(
                        {
                            "best_local_breadth": best_local_breadth,
                            "best_residual_or_state": best_residual_or_state,
                            "best_genetics": best_genetics,
                            "best_perturbation": best_perturbation,
                            "manual_druggability": meta["manual_druggability"],
                            "manual_selectivity": meta["manual_selectivity"],
                            "manual_prior_risk": meta["manual_prior_risk"],
                            "surface_plus_accessible_negatives": surface_neg + accessible_neg,
                        },
                        sort_keys=True,
                    ),
                }
            )

    ranked = pd.DataFrame(rows).sort_values(
        ["wave30_call", "centrality_score", "intervention_score"], ascending=[True, False, False]
    )
    gate_df = pd.DataFrame(gate_rows)
    ranked.to_csv(OUT / "niche_driver_axis_audit.tsv", sep="\t", index=False)
    gate_df.to_csv(OUT / "niche_driver_gate_matrix.tsv", sep="\t", index=False)

    summary = {
        "seed": SEED,
        "n_axes": int(len(ranked)),
        "call_counts": ranked["wave30_call"].value_counts().to_dict(),
        "top_centrality_axes": ranked.sort_values("centrality_score", ascending=False)
        .head(5)[["axis", "centrality_score", "intervention_score", "wave30_call", "gate_failures"]]
        .to_dict(orient="records"),
        "top_intervention_axes": ranked.sort_values("intervention_score", ascending=False)
        .head(5)[["axis", "centrality_score", "intervention_score", "wave30_call", "gate_failures"]]
        .to_dict(orient="records"),
        "interpretation": (
            "No axis is promoted unless all gates pass. A CENTRAL_STATE_DRIVER_NOT_SELECTIVE_THERAPEUTIC call means the "
            "axis probably explains the recurrent state but fails as a tractable, selective intervention point."
        ),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
