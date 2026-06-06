#!/usr/bin/env python3
"""Wave28 target-first rescue audit.

The prior V3 analyses repeatedly found a cross-autoimmune lipid-lysosomal/APC
state but failed to nominate an intervention point. This audit reverses the
search order: start from druggable, mechanistically plausible autoimmune/CNS
targets and ask whether any one of them can be connected back to the replicated
module without using expression-only evidence as a surrogate for causality.

Promotion gates are deliberately harsh:

1. target-level genetic anchor or strong cross-disease genetics proxy,
2. module/cell-state support in the local V3 datasets,
3. real perturbation or foundation-model-plus-real-perturbation alignment,
4. druggable modality in the biologically correct direction,
5. no blocking prior art for the proposed autoimmune use.

The output is an audit, not a finding. A PARK call means "next data needed"; a
GO would only justify hostile novelty review.
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
OUT = ROOT / "phases/v3/results" / "wave28_target_first_rescue"
RAW = OUT / "raw_api"
SEED = 20260527
USER_AGENT = "ms-auto-research-wave28-target-first-rescue/1.0"

PATHS = {
    "wave20_altaxis": ROOT
    / "phases/v3/results"
    / "wave20_genetic_druggable_altaxis"
    / "negative_ranked_shortlist.tsv",
    "wave21_residual": ROOT
    / "phases/v3/results"
    / "wave21_residual_druggability_scan"
    / "wave21_residual_druggability_rank.tsv",
    "wave18_accessible": ROOT
    / "phases/v3/results"
    / "wave18_accessible_target_rescue"
    / "accessible_target_rescue_candidates.tsv",
    "wave25_genetics": ROOT
    / "phases/v3/results"
    / "wave25_causal_genetics_module_proxy"
    / "causal_proxy_candidate_matrix.tsv",
    "wave18_foundation": ROOT
    / "phases/v3/results"
    / "wave18_foundation_rescue"
    / "foundation_rescue_candidate_rank.tsv",
    "direct_perturbation": ROOT
    / "phases/v3/results"
    / "wave15_perturbation_drug_response"
    / "ranked_direct_perturbations.tsv",
    "l1000_recurrent": ROOT
    / "phases/v3/results"
    / "wave24_l1000_recurrent_reversal"
    / "recurrent_l1000_compound_triage.tsv",
    "central_rank": ROOT / "phases/v3/results" / "central_and_intervention_candidate_rank.tsv",
    "local_chembl": ROOT / "phases/v3/results" / "druggability" / "chembl_target_activity_summary.tsv",
}

DISEASE_QUERY = (
    '"multiple sclerosis" OR "rheumatoid arthritis" OR lupus OR Crohn OR '
    '"ulcerative colitis" OR psoriasis OR Sjogren OR "type 1 diabetes" OR '
    'celiac OR "autoimmune thyroid" OR "primary biliary cholangitis" OR autoimmune'
)

TARGETS: dict[str, dict[str, Any]] = {
    "LRRK2": {
        "axis": "lysosomal/autophagy kinase controlling myeloid vesicle handling",
        "direction": "inhibit kinase only if disease-risk gain-of-function drives the state",
        "modality": "brain-penetrant kinase inhibitor precedent",
        "manual_druggability_score": 3.0,
        "manual_prior_risk": "medium_high",
        "manual_blocker": "Crohn/Parkinson biology is plausible but local V3 lacks cross-disease module perturbation or target-resolved autoimmune genetics.",
        "query_aliases": ["LRRK2", "dardarin"],
    },
    "RIPK1": {
        "axis": "necroptosis/inflammatory cell-death kinase",
        "direction": "inhibit RIPK1 kinase activity",
        "modality": "CNS-penetrant and peripheral small-molecule inhibitors",
        "manual_druggability_score": 3.0,
        "manual_prior_risk": "high",
        "manual_blocker": "Cell-death route is plausible but not specifically tied to the replicated lipid-lysosomal/APC state in local data.",
        "query_aliases": ["RIPK1", "RIP1 kinase"],
    },
    "NLRP3": {
        "axis": "inflammasome-driven IL-1 beta / pyroptotic myeloid activation",
        "direction": "inhibit inflammasome activation",
        "modality": "small-molecule inflammasome inhibitors",
        "manual_druggability_score": 3.0,
        "manual_prior_risk": "high",
        "manual_blocker": "Broad inflammatory prior art is heavy and local module-specific perturbation support is absent.",
        "query_aliases": ["NLRP3", "inflammasome"],
    },
    "IRAK4": {
        "axis": "TLR/MyD88 innate signaling kinase upstream of lysosomal TLR programs",
        "direction": "inhibit IRAK4",
        "modality": "small-molecule kinase inhibitors/degraders",
        "manual_druggability_score": 3.0,
        "manual_prior_risk": "high",
        "manual_blocker": "Generic TLR blockade, infection risk, and prior autoimmune programs block a novel cross-module claim.",
        "query_aliases": ["IRAK4"],
    },
    "BTK": {
        "axis": "B-cell and myeloid BCR/FcR signaling kinase",
        "direction": "inhibit BTK",
        "modality": "clinical CNS-penetrant and peripheral BTK inhibitors",
        "manual_druggability_score": 3.0,
        "manual_prior_risk": "blocking",
        "manual_blocker": "Direct MS and autoimmune clinical prior art is blocking for a new V3 therapeutic claim.",
        "query_aliases": ["BTK", "Bruton tyrosine kinase"],
    },
    "CSF1R": {
        "axis": "macrophage/microglial survival and differentiation receptor",
        "direction": "partial inhibition or reprogramming, not wholesale depletion",
        "modality": "small-molecule inhibitors and antibodies",
        "manual_druggability_score": 2.5,
        "manual_prior_risk": "high",
        "manual_blocker": "Microglial depletion/repopulation biology is not selective for the APC lipid-lysosomal state and carries safety/liability concerns.",
        "query_aliases": ["CSF1R", "colony stimulating factor 1 receptor"],
    },
    "SYK": {
        "axis": "Fc receptor / ITAM myeloid signaling kinase",
        "direction": "inhibit SYK",
        "modality": "small-molecule kinase inhibitors",
        "manual_druggability_score": 3.0,
        "manual_prior_risk": "high",
        "manual_blocker": "Broad immune kinase with extensive autoimmune prior art and no local module-specific selectivity.",
        "query_aliases": ["SYK", "spleen tyrosine kinase"],
    },
    "PDE4B": {
        "axis": "cAMP brake on inflammatory APC activation",
        "direction": "inhibit PDE4B-selectively if cAMP restoration suppresses APC state",
        "modality": "small-molecule PDE4-family inhibitors",
        "manual_druggability_score": 2.5,
        "manual_prior_risk": "high",
        "manual_blocker": "Prior local PDE4/LINCS audit did not support a strong reversal signal; PDE4 is clinically/prior-art saturated in psoriasis/IBD.",
        "query_aliases": ["PDE4B", "phosphodiesterase 4B"],
    },
    "PDE4D": {
        "axis": "cAMP brake on inflammatory APC activation",
        "direction": "inhibit PDE4D only if isoform selectivity avoids class toxicity",
        "modality": "small-molecule PDE4-family inhibitors",
        "manual_druggability_score": 2.5,
        "manual_prior_risk": "high",
        "manual_blocker": "PDE4D selectivity does not solve weak local module reversal and class prior-art saturation.",
        "query_aliases": ["PDE4D", "phosphodiesterase 4D"],
    },
    "PIK3CG": {
        "axis": "PI3K-gamma myeloid inflammatory trafficking/metabolism",
        "direction": "inhibit PI3K-gamma",
        "modality": "small-molecule lipid kinase inhibitors",
        "manual_druggability_score": 3.0,
        "manual_prior_risk": "medium_high",
        "manual_blocker": "Plausible myeloid target but local genetics and module-specific perturbation support are absent.",
        "query_aliases": ["PIK3CG", "PI3K gamma"],
    },
    "FAAH": {
        "axis": "endocannabinoid lipid signaling",
        "direction": "inhibit FAAH to increase endocannabinoid tone",
        "modality": "small-molecule enzyme inhibitors",
        "manual_druggability_score": 2.5,
        "manual_prior_risk": "medium_high",
        "manual_blocker": "CNS/lipid plausibility is not enough; no local module-state or genetics anchor emerged.",
        "query_aliases": ["FAAH", "fatty acid amide hydrolase"],
    },
    "TSPO": {
        "axis": "mitochondrial cholesterol/steroidogenesis and neuroinflammation imaging marker",
        "direction": "unclear; ligand direction is not established for autoimmune module control",
        "modality": "small-molecule ligands",
        "manual_druggability_score": 2.0,
        "manual_prior_risk": "medium_high",
        "manual_blocker": "Likely biomarker/imaging handle rather than causal controller in current data.",
        "query_aliases": ["TSPO", "translocator protein"],
    },
    "PTGER4": {
        "axis": "PGE2 EP4 receptor signaling",
        "direction": "context-dependent agonism or antagonism",
        "modality": "small-molecule GPCR modulators",
        "manual_druggability_score": 3.0,
        "manual_prior_risk": "high",
        "manual_blocker": "Eicosanoid/prostanoid route was already rejected as generic and directionally unstable.",
        "query_aliases": ["PTGER4", "EP4 receptor"],
    },
    "ALOX5": {
        "axis": "leukotriene/eicosanoid inflammatory lipid synthesis",
        "direction": "inhibit 5-lipoxygenase",
        "modality": "small-molecule enzyme inhibitors",
        "manual_druggability_score": 2.5,
        "manual_prior_risk": "high",
        "manual_blocker": "Generic eicosanoid route with prior anti-inflammatory clinical history and weak module specificity.",
        "query_aliases": ["ALOX5", "5-lipoxygenase"],
    },
    "GPR65": {
        "axis": "acidic tissue pH-sensing GPCR/cAMP response",
        "direction": "agonize/PAM if risk alleles reduce protective signaling",
        "modality": "GPCR agonist or positive allosteric modulator",
        "manual_druggability_score": 2.5,
        "manual_prior_risk": "high",
        "manual_blocker": "Best genetics/druggability near-miss but local module support and disease-direction resolution remain weak; IBD prior art is direct.",
        "query_aliases": ["GPR65", "TDAG8"],
    },
    "PTPN2": {
        "axis": "TCPTP negative regulation of JAK/STAT/barrier signaling",
        "direction": "restore/increase TCPTP function",
        "modality": "requires activator/restoration modality; inhibitors are wrong direction",
        "manual_druggability_score": 0.75,
        "manual_prior_risk": "high",
        "manual_blocker": "Strong broad genetics proxy, but no correct-direction drug modality or target-resolved coloc/MR in this run.",
        "query_aliases": ["PTPN2", "TCPTP"],
    },
    "TNFAIP3": {
        "axis": "A20 ubiquitin-editing NF-kappaB/TNF/TLR brake",
        "direction": "restore A20 function",
        "modality": "restoration/mimetic modality required",
        "manual_druggability_score": 0.5,
        "manual_prior_risk": "high",
        "manual_blocker": "Broad genetics proxy but no practical selective restoration modality.",
        "query_aliases": ["TNFAIP3", "A20"],
    },
    "SH2B3": {
        "axis": "LNK cytokine/JAK signaling adaptor",
        "direction": "restore LNK negative regulation",
        "modality": "no direct modality",
        "manual_druggability_score": 0.25,
        "manual_prior_risk": "medium",
        "manual_blocker": "Broad pleiotropic 12q24 genetics but poor druggability and weak local module biology.",
        "query_aliases": ["SH2B3", "LNK"],
    },
    "IRF5": {
        "axis": "TLR/IRF inflammatory transcription-factor switch",
        "direction": "inhibit IRF5 activation",
        "modality": "small-molecule inhibitor/degrader in principle",
        "manual_druggability_score": 2.0,
        "manual_prior_risk": "high",
        "manual_blocker": "Broad locus but weak local module-state support and direct lupus/TLR/IFN prior art.",
        "query_aliases": ["IRF5"],
    },
    "TYK2": {
        "axis": "IL-12/23/type-I-IFN cytokine kinase",
        "direction": "inhibit TYK2",
        "modality": "approved/clinical TYK2 inhibitors",
        "manual_druggability_score": 3.0,
        "manual_prior_risk": "blocking",
        "manual_blocker": "Direct autoimmune drug class prior art; no new lipid-lysosomal/APC-selective delta.",
        "query_aliases": ["TYK2"],
    },
    "IL6R": {
        "axis": "IL-6 receptor inflammatory signaling",
        "direction": "block IL-6R",
        "modality": "approved anti-IL6R biologics",
        "manual_druggability_score": 3.0,
        "manual_prior_risk": "blocking",
        "manual_blocker": "Approved autoimmune biologic class; not novel and not module-selective.",
        "query_aliases": ["IL6R", "tocilizumab"],
    },
    "CTSS": {
        "axis": "lysosomal antigen-processing cathepsin",
        "direction": "inhibit cathepsin S",
        "modality": "small-molecule cysteine protease inhibitors",
        "manual_druggability_score": 3.0,
        "manual_prior_risk": "blocking",
        "manual_blocker": "Direct cathepsin S autoimmune clinical/prior-art history and local selectivity concerns already demoted this route.",
        "query_aliases": ["CTSS", "cathepsin S"],
    },
    "IFI30": {
        "axis": "GILT lysosomal antigen-processing redox enzyme",
        "direction": "inhibit or modulate only if pathogenic antigen processing is causal",
        "modality": "enzyme in principle, but chemical matter uncertain",
        "manual_druggability_score": 1.0,
        "manual_prior_risk": "medium",
        "manual_blocker": "Excellent state marker/effector but no target-level genetics, chemical matter, or perturbation package.",
        "query_aliases": ["IFI30", "GILT"],
    },
    "GSK3B": {
        "axis": "kinase controller of CIITA/MHC-II response in macrophage perturbation data",
        "direction": "inhibit GSK3B only if selectivity and safety are solved",
        "modality": "small-molecule kinase inhibitors",
        "manual_druggability_score": 2.0,
        "manual_prior_risk": "high",
        "manual_blocker": "Real perturbation signal exists, but no cross-autoimmune genetics and broad pleiotropic kinase safety block promotion.",
        "query_aliases": ["GSK3B", "GSK-3 beta"],
    },
    "SQLE": {
        "axis": "sterol-biosynthesis enzyme in residual stromal module",
        "direction": "inhibit SQLE if stromal sterol activation is causal",
        "modality": "small-molecule enzyme inhibitors",
        "manual_druggability_score": 3.0,
        "manual_prior_risk": "medium_high",
        "manual_blocker": "Strict residual survivor but IBD-stromal only after deeper audit; no genetics or perturbation support.",
        "query_aliases": ["SQLE", "squalene monooxygenase"],
    },
    "OSMR": {
        "axis": "OSM/OSMR tissue inflammatory remodeling",
        "direction": "block OSMR signaling",
        "modality": "antibody/biologic",
        "manual_druggability_score": 2.0,
        "manual_prior_risk": "medium_high",
        "manual_blocker": "Tissue-remodeling axis remains plausible but local module link and novelty are insufficient.",
        "query_aliases": ["OSMR", "oncostatin M receptor"],
    },
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def read_table(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path, sep="\t", low_memory=False)


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True) + "\n", encoding="utf-8")


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None or pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def split_count(value: Any) -> int:
    if value is None or pd.isna(value):
        return 0
    return len([item for item in str(value).split(";") if item.strip()])


def first_gene(df: pd.DataFrame, gene: str, col: str = "gene") -> dict[str, Any]:
    if df.empty or col not in df.columns:
        return {}
    sub = df[df[col].astype(str).str.upper() == gene.upper()]
    if sub.empty:
        return {}
    return sub.iloc[0].to_dict()


def gene_rows(df: pd.DataFrame, gene: str, col: str = "gene") -> pd.DataFrame:
    if df.empty or col not in df.columns:
        return pd.DataFrame()
    return df[df[col].astype(str).str.upper() == gene.upper()].copy()


def api_get_json(url: str, params: dict[str, Any], cache_name: str, timeout: int = 25) -> dict[str, Any]:
    RAW.mkdir(parents=True, exist_ok=True)
    cache = RAW / cache_name
    if cache.exists():
        return json.loads(cache.read_text(encoding="utf-8"))
    full = f"{url}?{urlencode(params)}"
    headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    last_error: str | None = None
    for attempt in range(3):
        try:
            with urlopen(Request(full, headers=headers), timeout=timeout) as response:
                payload = json.loads(response.read().decode("utf-8"))
            cache.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            return payload
        except Exception as exc:  # noqa: BLE001 - audit records concrete API failures.
            last_error = f"{type(exc).__name__}: {exc}"
            time.sleep(0.75 * (attempt + 1))
    payload = {"api_error": last_error, "url": full}
    cache.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return payload


def europepmc_count(gene: str, aliases: list[str]) -> dict[str, Any]:
    terms = " OR ".join(f'"{alias}"' for alias in aliases)
    query = f"({terms}) AND ({DISEASE_QUERY})"
    payload = api_get_json(
        "https://www.ebi.ac.uk/europepmc/webservices/rest/search",
        {"query": query, "format": "json", "pageSize": 3, "resultType": "lite"},
        f"europepmc_{gene}.json",
    )
    examples = []
    for item in payload.get("resultList", {}).get("result", [])[:3]:
        examples.append(
            {
                "id": item.get("id", ""),
                "source": item.get("source", ""),
                "title": item.get("title", ""),
                "year": item.get("pubYear", ""),
            }
        )
    return {
        "europepmc_query": query,
        "europepmc_hit_count": int(payload.get("hitCount", 0) or 0) if "api_error" not in payload else np.nan,
        "europepmc_error": payload.get("api_error", ""),
        "europepmc_examples": examples,
    }


def clinicaltrials_count(gene: str, aliases: list[str]) -> dict[str, Any]:
    term = " OR ".join(f'"{alias}"' if " " in alias else alias for alias in aliases)
    condition = 'autoimmune OR "multiple sclerosis" OR "rheumatoid arthritis" OR lupus OR Crohn OR psoriasis'
    payload = api_get_json(
        "https://clinicaltrials.gov/api/v2/studies",
        {
            "query.term": term,
            "query.cond": condition,
            "pageSize": 1,
            "format": "json",
            "countTotal": "true",
        },
        f"clinicaltrials_counted_{gene}.json",
    )
    return {
        "clinicaltrials_query": f"term=({term}); condition=({condition})",
        "clinicaltrials_returned_count": len(payload.get("studies", [])) if "api_error" not in payload else np.nan,
        "clinicaltrials_total_count": int(payload.get("totalCount", 0) or 0) if "api_error" not in payload else np.nan,
        "clinicaltrials_error": payload.get("api_error", ""),
    }


def chembl_snapshot(gene: str, aliases: list[str], local_chembl: pd.DataFrame) -> dict[str, Any]:
    rows = gene_rows(local_chembl, gene)
    if not rows.empty:
        rows = rows.copy()
        rows["activity_records_returned"] = pd.to_numeric(rows["activity_records_returned"], errors="coerce")
        rows["best_standard_value_nM"] = pd.to_numeric(rows["best_standard_value_nM"], errors="coerce")
        best = rows.sort_values(
            by=["activity_records_returned", "best_standard_value_nM"],
            ascending=[False, True],
            na_position="last",
        ).iloc[0]
        return {
            "chembl_source": "local_v3_druggability_table",
            "chembl_target_chembl_id": best.get("target_chembl_id", ""),
            "chembl_pref_name": best.get("pref_name", ""),
            "chembl_target_type": best.get("target_type", ""),
            "chembl_activity_records": as_float(best.get("activity_records_returned"), 0.0),
            "chembl_best_nM": as_float(best.get("best_standard_value_nM"), np.nan),
            "chembl_error": "",
        }

    query = aliases[0]
    search = api_get_json(
        "https://www.ebi.ac.uk/chembl/api/data/target/search.json",
        {"q": query, "limit": 10},
        f"chembl_target_search_{gene}.json",
    )
    if "api_error" in search:
        return {
            "chembl_source": "chembl_api_failed",
            "chembl_target_chembl_id": "",
            "chembl_pref_name": "",
            "chembl_target_type": "",
            "chembl_activity_records": np.nan,
            "chembl_best_nM": np.nan,
            "chembl_error": search.get("api_error", ""),
        }
    targets = search.get("targets", [])
    chosen = None
    for target in targets:
        if target.get("organism") == "Homo sapiens" and target.get("target_type") in {
            "SINGLE PROTEIN",
            "PROTEIN COMPLEX",
            "PROTEIN FAMILY",
        }:
            chosen = target
            break
    if chosen is None and targets:
        chosen = targets[0]
    if chosen is None:
        return {
            "chembl_source": "chembl_api_search_no_target",
            "chembl_target_chembl_id": "",
            "chembl_pref_name": "",
            "chembl_target_type": "",
            "chembl_activity_records": 0.0,
            "chembl_best_nM": np.nan,
            "chembl_error": "",
        }
    target_id = chosen.get("target_chembl_id", "")
    acts = api_get_json(
        "https://www.ebi.ac.uk/chembl/api/data/activity.json",
        {"target_chembl_id": target_id, "standard_type__in": "IC50,Ki,Kd,EC50", "limit": 1},
        f"chembl_activity_{gene}_{target_id}.json",
    )
    page_meta = acts.get("page_meta", {}) if isinstance(acts, dict) else {}
    return {
        "chembl_source": "chembl_api",
        "chembl_target_chembl_id": target_id,
        "chembl_pref_name": chosen.get("pref_name", ""),
        "chembl_target_type": chosen.get("target_type", ""),
        "chembl_activity_records": int(page_meta.get("total_count", 0) or 0) if "api_error" not in acts else np.nan,
        "chembl_best_nM": np.nan,
        "chembl_error": acts.get("api_error", ""),
    }


def direct_perturbation_summary(direct: pd.DataFrame, gene: str) -> dict[str, Any]:
    if direct.empty or "perturbation" not in direct.columns:
        return {
            "direct_perturbation_rows": 0,
            "best_direct_selectivity_score": 0.0,
            "best_direct_target_module_effect": np.nan,
            "best_direct_evidence_call": "",
            "direct_selective_support": False,
        }
    rows = direct[direct["perturbation"].astype(str).str.upper() == gene.upper()].copy()
    if rows.empty:
        return {
            "direct_perturbation_rows": 0,
            "best_direct_selectivity_score": 0.0,
            "best_direct_target_module_effect": np.nan,
            "best_direct_evidence_call": "",
            "direct_selective_support": False,
        }
    rows["selectivity_score_num"] = pd.to_numeric(rows.get("selectivity_score"), errors="coerce").fillna(0.0)
    best = rows.sort_values("selectivity_score_num", ascending=False).iloc[0]
    call = str(best.get("evidence_call", ""))
    return {
        "direct_perturbation_rows": int(len(rows)),
        "best_direct_dataset": best.get("dataset", ""),
        "best_direct_condition": best.get("condition", ""),
        "best_direct_selectivity_score": float(best.get("selectivity_score_num", 0.0)),
        "best_direct_target_module_effect": as_float(best.get("target_module_effect"), np.nan),
        "best_direct_evidence_call": call,
        "direct_selective_support": call == "selective_target_suppression",
    }


def l1000_target_summary(l1000: pd.DataFrame, gene: str) -> dict[str, Any]:
    if l1000.empty or "target" not in l1000.columns:
        return {"l1000_target_rows": 0, "l1000_best_qval": np.nan, "l1000_gate_counts": "", "l1000_non_no_go": False}
    rows = l1000[l1000["target"].astype(str).str.upper().str.split("|").apply(lambda xs: gene.upper() in xs)]
    if rows.empty:
        return {"l1000_target_rows": 0, "l1000_best_qval": np.nan, "l1000_gate_counts": "", "l1000_non_no_go": False}
    gates = rows.get("promotion_gate", pd.Series(dtype=str)).astype(str).value_counts().to_dict()
    return {
        "l1000_target_rows": int(len(rows)),
        "l1000_best_qval": float(pd.to_numeric(rows.get("min_opposite_qval"), errors="coerce").min()),
        "l1000_best_abs_score": float(pd.to_numeric(rows.get("max_opposite_abs_score"), errors="coerce").max()),
        "l1000_gate_counts": ";".join(f"{k}:{v}" for k, v in sorted(gates.items())),
        "l1000_non_no_go": any(k not in {"NO_GO", "NO_GO_PRIOR"} for k in gates),
    }


def prior_risk_penalty(risk: str, europepmc_hits: float, clinical_trials: float) -> float:
    base = {
        "low": 0.0,
        "medium": 1.0,
        "medium_high": 1.75,
        "high": 2.5,
        "blocking": 4.0,
    }.get(risk, 1.0)
    if not math.isnan(europepmc_hits):
        if europepmc_hits >= 1000:
            base += 1.0
        elif europepmc_hits >= 250:
            base += 0.5
    if not math.isnan(clinical_trials) and clinical_trials > 0:
        base += 0.75
    return min(base, 5.0)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)

    wave20 = read_table(PATHS["wave20_altaxis"])
    wave21 = read_table(PATHS["wave21_residual"])
    wave18_accessible = read_table(PATHS["wave18_accessible"])
    wave25 = read_table(PATHS["wave25_genetics"])
    foundation = read_table(PATHS["wave18_foundation"])
    direct = read_table(PATHS["direct_perturbation"])
    l1000 = read_table(PATHS["l1000_recurrent"])
    local_chembl = read_table(PATHS["local_chembl"])

    records: list[dict[str, Any]] = []
    api_logs: list[dict[str, Any]] = []
    for gene, meta in TARGETS.items():
        aliases = meta.get("query_aliases", [gene])
        g25 = first_gene(wave25, gene)
        w20 = first_gene(wave20, gene)
        w21 = first_gene(wave21, gene)
        w18a = first_gene(wave18_accessible, gene)
        fnd = first_gene(foundation, gene)
        direct_sum = direct_perturbation_summary(direct, gene)
        l1000_sum = l1000_target_summary(l1000, gene)
        chembl = chembl_snapshot(gene, aliases, local_chembl)
        epmc = europepmc_count(gene, aliases)
        ct = clinicaltrials_count(gene, aliases)
        api_logs.append(
            {
                "gene": gene,
                "europepmc_query": epmc["europepmc_query"],
                "europepmc_hit_count": epmc["europepmc_hit_count"],
                "clinicaltrials_query": ct["clinicaltrials_query"],
                "clinicaltrials_total_count": ct["clinicaltrials_total_count"],
                "chembl_source": chembl["chembl_source"],
                "chembl_target_chembl_id": chembl["chembl_target_chembl_id"],
                "chembl_error": chembl["chembl_error"],
                "europepmc_error": epmc["europepmc_error"],
                "clinicaltrials_error": ct["clinicaltrials_error"],
            }
        )

        genetics_diseases = int(as_float(g25.get("ot_n_diseases_score_ge_0_5", w20.get("ot_n_diseases_score_ge_0_5", 0)), 0))
        genetics_ready_score = as_float(g25.get("genetics_ready_score", w20.get("genetics_score", 0)), 0)
        proxy_call = str(g25.get("proxy_call", w20.get("target_level_signal", "")))
        coloc_feasible = bool(g25.get("proper_coloc_or_mr_feasible_this_run", False))
        if isinstance(g25.get("proper_coloc_or_mr_feasible_this_run"), str):
            coloc_feasible = g25.get("proper_coloc_or_mr_feasible_this_run") == "True"

        broad_positive = int(
            max(
                as_float(g25.get("broad_positive_disease_count"), 0),
                as_float(w21.get("broad_positive_disease_count"), 0),
                as_float(w18a.get("broad_positive_disease_count"), 0),
                as_float(w20.get("broad_positive_disease_count"), 0),
            )
        )
        strict_residual = int(as_float(w21.get("strict_core_covariate_surviving_disease_count"), 0))
        non_ibd_residual = int(as_float(w21.get("non_ibd_retained_positive_disease_count"), 0))
        ms_anchor = bool(w21.get("ms_anchor", False)) or bool(as_float(g25.get("ms_positive_nominal"), 0))
        module_score = max(
            as_float(g25.get("module_state_score"), 0),
            broad_positive + 0.5 * strict_residual + 0.5 * non_ibd_residual + (1.0 if ms_anchor else 0.0),
        )

        foundation_call = str(fnd.get("real_perturbation_alignment_call", g25.get("foundation_real_perturbation_alignment_call", "")))
        foundation_recommendation = str(
            fnd.get("foundation_rescue_recommendation", g25.get("foundation_rescue_recommendation", ""))
        )
        foundation_support = (
            foundation_call
            and "contradicted" not in foundation_call
            and "do_not_promote" not in foundation_recommendation
            and "no_rescue" not in foundation_call
        )
        perturbation_score = max(
            as_float(g25.get("perturbation_score"), 0),
            as_float(fnd.get("best_direct_selectivity_score"), 0),
            direct_sum["best_direct_selectivity_score"],
            1.0 if l1000_sum["l1000_non_no_go"] else 0.0,
        )
        perturbation_support = (
            bool(direct_sum["direct_selective_support"])
            or foundation_support
            or (l1000_sum["l1000_non_no_go"] and l1000_sum["l1000_target_rows"] >= 2)
        )

        activity_records = as_float(chembl["chembl_activity_records"], 0.0)
        chembl_druggable = activity_records >= 20 or as_float(chembl["chembl_best_nM"], 1e9) <= 1000
        manual_druggability = as_float(meta.get("manual_druggability_score"), 0)
        druggability_score = max(manual_druggability, 3.0 if activity_records >= 100 else 2.0 if chembl_druggable else 0.0)
        correct_direction_modality = manual_druggability >= 2.0 and "wrong direction" not in str(meta.get("manual_blocker", "")).lower()

        epmc_hits = as_float(epmc["europepmc_hit_count"], np.nan)
        ct_hits = as_float(ct["clinicaltrials_total_count"], np.nan)
        prior_penalty = prior_risk_penalty(str(meta.get("manual_prior_risk", "medium")), epmc_hits, ct_hits)

        genetic_gate = coloc_feasible or (
            genetics_diseases >= 4 and proxy_call not in {"", "NO_GO_CAUSAL_PROXY", "MODULE_MARKER_NOT_GENETICALLY_ANCHORED"}
        )
        module_gate = broad_positive >= 3 or strict_residual >= 2 or module_score >= 5.0
        perturbation_gate = perturbation_support and perturbation_score >= 1.0
        druggable_gate = druggability_score >= 2.0 and correct_direction_modality
        novelty_gate = prior_penalty < 3.0 and str(meta.get("manual_prior_risk")) != "blocking"

        hard_failures = []
        if not genetic_gate:
            hard_failures.append("no_target_level_genetic_anchor")
        if not module_gate:
            hard_failures.append("weak_or_absent_local_module_state_support")
        if not perturbation_gate:
            hard_failures.append("no_real_selective_perturbation_or_validated_foundation_support")
        if not druggable_gate:
            hard_failures.append("no_correct_direction_druggable_modality")
        if not novelty_gate:
            hard_failures.append("prior_art_or_clinical_saturation")

        if not hard_failures:
            gate_call = "GO_TO_HOSTILE_NOVELTY_REVIEW"
        elif len(hard_failures) <= 2 and module_gate and druggable_gate:
            gate_call = "PARK_REQUIRES_TARGET_CAUSALITY_OR_PERTURBATION"
        else:
            gate_call = "NO_GO_TARGET_FIRST"

        total_score = (
            min(genetics_diseases, 5)
            + module_score
            + perturbation_score
            + druggability_score
            - prior_penalty
            - 2.0 * len(hard_failures)
        )
        records.append(
            {
                "gene": gene,
                "axis": meta["axis"],
                "direction": meta["direction"],
                "modality": meta["modality"],
                "gate_call": gate_call,
                "hard_failures": ";".join(hard_failures),
                "target_first_score": total_score,
                "genetic_gate": genetic_gate,
                "module_gate": module_gate,
                "perturbation_gate": perturbation_gate,
                "druggable_gate": druggable_gate,
                "novelty_gate": novelty_gate,
                "genetics_diseases_ge_0_5": genetics_diseases,
                "genetics_ready_score": genetics_ready_score,
                "genetics_proxy_call": proxy_call,
                "proper_coloc_or_mr_feasible_this_run": coloc_feasible,
                "broad_positive_disease_count": broad_positive,
                "strict_residual_disease_count": strict_residual,
                "non_ibd_residual_positive_disease_count": non_ibd_residual,
                "ms_anchor": ms_anchor,
                "module_score": module_score,
                "foundation_alignment_call": foundation_call,
                "foundation_recommendation": foundation_recommendation,
                "foundation_support_gate_component": foundation_support,
                "perturbation_score": perturbation_score,
                **direct_sum,
                **l1000_sum,
                "manual_druggability_score": manual_druggability,
                "druggability_score": druggability_score,
                "chembl_druggable_by_activity": chembl_druggable,
                **chembl,
                "manual_prior_risk": meta.get("manual_prior_risk", ""),
                "prior_penalty": prior_penalty,
                "europepmc_hit_count": epmc["europepmc_hit_count"],
                "clinicaltrials_total_count": ct["clinicaltrials_total_count"],
                "manual_blocker": meta["manual_blocker"],
                "europepmc_examples_json": json.dumps(epmc["europepmc_examples"], ensure_ascii=True),
            }
        )

    matrix = pd.DataFrame(records).sort_values(
        ["gate_call", "target_first_score", "module_score"],
        ascending=[True, False, False],
    )
    gate_summary = (
        matrix.groupby("gate_call", dropna=False)
        .agg(
            n=("gene", "count"),
            top_score=("target_first_score", "max"),
            genes=("gene", lambda s: ";".join(map(str, s))),
        )
        .reset_index()
        .sort_values(["gate_call"])
    )
    api_log = pd.DataFrame(api_logs)

    matrix.to_csv(OUT / "target_first_rescue_matrix.tsv", sep="\t", index=False)
    gate_summary.to_csv(OUT / "target_first_gate_summary.tsv", sep="\t", index=False)
    api_log.to_csv(OUT / "target_first_api_log.tsv", sep="\t", index=False)

    summary = {
        "date": "2026-05-27",
        "random_seed": SEED,
        "candidate_count": int(len(matrix)),
        "gate_call_counts": matrix["gate_call"].value_counts().to_dict(),
        "promoted_count": int((matrix["gate_call"] == "GO_TO_HOSTILE_NOVELTY_REVIEW").sum()),
        "park_count": int((matrix["gate_call"] == "PARK_REQUIRES_TARGET_CAUSALITY_OR_PERTURBATION").sum()),
        "top_candidates": matrix.head(8).replace({np.nan: None}).to_dict(orient="records"),
        "interpretation": (
            "Wave28 is negative for promotion: target-first druggable candidates do not simultaneously clear "
            "genetic, module-state, perturbation, correct-modality, and novelty gates."
        ),
        "inputs": [rel(path) for path in PATHS.values()],
    }
    write_json(OUT / "summary.json", summary)


if __name__ == "__main__":
    main()
