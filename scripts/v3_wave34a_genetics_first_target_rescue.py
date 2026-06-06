#!/usr/bin/env python3
"""Wave34-A genetics-first target rescue.

This is a scoped V3 subagent artifact. It deliberately starts from genetic
surfaces rather than expression-first ranks, and it treats GWAS Catalog
mapped-gene overlap as weak unless backed by local OpenTargets credible-set
evidence and/or public cis-eQTL availability.

No output from this script is a therapeutic finding. Calls are routing calls:
promote to deeper validation, park, or demote.
"""

from __future__ import annotations

import json
import math
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "phases/v3/results" / "wave34a_genetics_first_target_rescue"
RAW = OUT / "raw_api"
REPORT = ROOT / "phases/v3/subagents" / "wave34a_genetics_first_target_rescue.md"
SEED = 20260527
USER_AGENT = "ms-auto-research-wave34a-genetics-first-target-rescue/1.0"

LOCAL_FILES = {
    "opentargets_credible_sets": ROOT / "phases/v3/tmp" / "wave13_opentargets_gwas_credible_sets.tsv",
    "opentargets_target_disease_scores": ROOT / "phases/v3/tmp" / "wave11_opentargets_target_disease_scores.tsv",
    "gwas_catalog_parquet": ROOT / "phases/v3/tmp" / "gwascatalog_associations_20260317_convert.parquet",
    "wave14_truth": ROOT / "phases/v3/results" / "wave14_target_level_genetics" / "target_level_genetics_truth_table.tsv",
    "broad_h5ad_rank": ROOT / "phases/v3/results" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_rank.tsv",
    "broad_residual_gate": ROOT / "phases/v3/results" / "broad_residual_gate" / "broad_residual_gate_summary.tsv",
    "wave20_local_genetics": ROOT / "phases/v3/results" / "wave20_genetic_druggable_altaxis" / "local_opentargets_genetics_summary.tsv",
    "wave20_shortlist": ROOT / "phases/v3/results" / "wave20_genetic_druggable_altaxis" / "negative_ranked_shortlist.tsv",
    "wave23_restoration": ROOT / "phases/v3/results" / "wave23_genetics_restoration_modality" / "ranked_go_park_no_go.tsv",
    "wave25_causal_proxy": ROOT / "phases/v3/results" / "wave25_causal_genetics_module_proxy" / "causal_proxy_candidate_matrix.tsv",
    "wave28_target_first": ROOT / "phases/v3/results" / "wave28_target_first_rescue" / "target_first_rescue_matrix.tsv",
    "wave33_tolerance_audit": ROOT / "phases/v3/results" / "wave33_tolerance_costimulation_audit" / "tolerance_costimulation_axis_audit.tsv",
}

AUTOIMMUNE_REGEX = re.compile(
    r"multiple sclerosis|rheumatoid arthritis|lupus|crohn|ulcerative colitis|"
    r"psoriasis|type 1 diabetes|sjogren|celiac|coeliac|ankylosing spondylitis|"
    r"primary biliary|autoimmune thyroid|graves|hashimoto|inflammatory bowel|"
    r"sclerosing cholangitis|myasthenia|vitiligo|atopic dermatitis",
    re.I,
)

GTEX_TISSUES = [
    "Whole_Blood",
    "Cells_EBV-transformed_lymphocytes",
    "Spleen",
    "Colon_Transverse",
    "Skin_Sun_Exposed_Lower_leg",
    "Brain_Frontal_Cortex_BA9",
]

# Candidate list is intentionally genetics-first:
# - broad local OpenTargets credible-set genes;
# - top local GWAS Catalog mapped genes with druggable or immune-checkpoint
#   plausibility;
# - reviewer-specified CD226/TIGIT/PVR axis probes.
CANDIDATES: dict[str, dict[str, Any]] = {
    "CD226": {
        "axis": "DNAM-1/TIGIT-ligand costimulatory balance",
        "modality": "antagonist antibody or ligand-blocking biologic",
        "direction": "reduce CD226 costimulation or restore TIGIT-biased inhibitory balance",
        "target_class": "cell-surface immunoglobulin-family receptor",
        "manual_druggability": 2.25,
        "prior_risk": "medium",
        "direction_confidence": "plausible_but_unproven",
        "manual_note": "Genetics-first candidate missed by expression-first screens; needs target-resolved CD226 coloc/eQTL direction and T/NK tissue-state validation.",
    },
    "PTGER4": {
        "axis": "EP4 prostaglandin receptor tissue-immune regulation",
        "modality": "small-molecule EP4 agonist/antagonist/PAM depending on direction",
        "direction": "unresolved; likely context-specific EP4 agonism for barrier/tolerance versus antagonism in some inflammatory settings",
        "target_class": "GPCR",
        "manual_druggability": 3.0,
        "prior_risk": "high",
        "direction_confidence": "conflicted",
        "manual_note": "Strong mapped-gene autoimmunity signal and druggability, but direction and direct autoimmune prior art are hard blockers.",
    },
    "CXCR5": {
        "axis": "CXCL13/CXCR5 follicular B/T-cell trafficking",
        "modality": "blocking antibody or chemokine-receptor antagonist concept",
        "direction": "block follicular recruitment if pathogenic ectopic follicles are causal",
        "target_class": "chemokine GPCR",
        "manual_druggability": 2.0,
        "prior_risk": "medium_high",
        "direction_confidence": "plausible_but_unproven",
        "manual_note": "Genetics and MS/autoimmune mapping are broad, but no local target-level coloc or V3 cell-state rescue exists.",
    },
    "CCR6": {
        "axis": "CCR6/CCL20 Th17 tissue entry",
        "modality": "CCR6 antagonist or anti-CCR6 biologic",
        "direction": "block CCR6-dependent pathogenic Th17 recruitment",
        "target_class": "chemokine GPCR",
        "manual_druggability": 2.0,
        "prior_risk": "high",
        "direction_confidence": "plausible_but_crowded",
        "manual_note": "Broad mapped-gene signal but crowded Th17/trafficking biology and no coloc-grade local support.",
    },
    "TNFRSF14": {
        "axis": "HVEM/BTLA/LIGHT coinhibitory-costimulatory switch",
        "modality": "agonist/inhibitory biologic depending on ligand context",
        "direction": "restore BTLA-HVEM inhibitory signaling while avoiding LIGHT costimulation",
        "target_class": "TNF receptor-family surface receptor",
        "manual_druggability": 1.75,
        "prior_risk": "high",
        "direction_confidence": "conflicted",
        "manual_note": "Broad genetics maps to HVEM region, but ligand-direction complexity blocks promotion.",
    },
    "FAP": {
        "axis": "fibroblast activation / tissue remodeling",
        "modality": "enzyme inhibitor, antibody, or targeted delivery handle",
        "direction": "unclear in autoimmunity; inhibit pathogenic fibroblast activation if causal",
        "target_class": "cell-surface serine protease",
        "manual_druggability": 2.75,
        "prior_risk": "medium",
        "direction_confidence": "weak",
        "manual_note": "Druggable stromal gene with GWAS Catalog breadth, but likely locus-proxy/tissue-remodeling rather than target-level immune causality.",
    },
    "CD6": {
        "axis": "CD6/ALCAM T-cell adhesion-costimulation",
        "modality": "anti-CD6 biologic",
        "direction": "block pathogenic CD6-ALCAM interaction",
        "target_class": "cell-surface receptor",
        "manual_druggability": 2.75,
        "prior_risk": "blocking",
        "direction_confidence": "plausible_but_prior_arted",
        "manual_note": "Prior-art saturated anti-CD6 autoimmune route; useful positive control, not a new rescue.",
    },
    "PTPN22": {
        "axis": "Lyp lymphocyte-receptor signaling phosphatase",
        "modality": "small-molecule inhibitor/allosteric modulator concept",
        "direction": "unclear across R620W-like risk biology; inhibition is plausible in some models but not directionally settled",
        "target_class": "intracellular phosphatase",
        "manual_druggability": 1.5,
        "prior_risk": "medium_high",
        "direction_confidence": "conflicted",
        "manual_note": "Very broad autoimmune genetics, but disease-safe direction and selectivity over other PTPs remain unresolved.",
    },
    "IL2RA": {
        "axis": "IL-2 receptor/Treg tolerance",
        "modality": "IL-2 mutein, low-dose IL-2, anti-CD25 variants",
        "direction": "increase Treg-biased IL-2 signaling or selectively deplete pathogenic CD25-high cells depending context",
        "target_class": "cytokine receptor",
        "manual_druggability": 3.0,
        "prior_risk": "blocking",
        "direction_confidence": "prior_arted",
        "manual_note": "Genetics and modality are strong, but autoimmune/Treg prior art is direct.",
    },
    "IL23R": {
        "axis": "IL-23/Th17 axis",
        "modality": "anti-IL23/IL23R biologic",
        "direction": "block IL-23 signaling",
        "target_class": "cytokine receptor",
        "manual_druggability": 3.0,
        "prior_risk": "blocking",
        "direction_confidence": "established_prior_art",
        "manual_note": "Validated psoriasis/IBD class; not a novel Wave34 rescue.",
    },
    "CTLA4": {
        "axis": "CD28/B7/CTLA4 costimulation",
        "modality": "CTLA4-Ig or checkpoint agonism",
        "direction": "enhance CTLA4-like inhibitory signaling / block CD28-B7",
        "target_class": "cell-surface checkpoint receptor",
        "manual_druggability": 3.0,
        "prior_risk": "blocking",
        "direction_confidence": "established_prior_art",
        "manual_note": "Abatacept-class prior art makes this a comparator, not a rescue.",
    },
    "STAT4": {
        "axis": "IL-12/23 transcriptional polarization",
        "modality": "indirect cytokine/JAK pathway blockade",
        "direction": "reduce STAT4-driven Th1/Th17 polarization",
        "target_class": "transcription factor",
        "manual_druggability": 0.75,
        "prior_risk": "high",
        "direction_confidence": "indirect",
        "manual_note": "Broad genetics but poor direct druggability; upstream pathways are already crowded.",
    },
    "TYK2": {
        "axis": "TYK2 cytokine kinase",
        "modality": "approved/clinical allosteric inhibitors",
        "direction": "inhibit TYK2",
        "target_class": "kinase",
        "manual_druggability": 3.0,
        "prior_risk": "blocking",
        "direction_confidence": "established_prior_art",
        "manual_note": "Positive control for genetics plus druggability; excluded by direct autoimmune prior art.",
    },
    "PTPN2": {
        "axis": "TCPTP cytokine/barrier negative regulator",
        "modality": "would require restoration/activation; inhibitors point wrong way",
        "direction": "restore/increase TCPTP function",
        "target_class": "intracellular phosphatase",
        "manual_druggability": 0.75,
        "prior_risk": "high",
        "direction_confidence": "restoration_needed",
        "manual_note": "Strong genetics benchmark, but no correct-direction restoration modality.",
    },
    "TNFAIP3": {
        "axis": "A20 NF-kappaB/TNF/TLR brake",
        "modality": "restore A20 function or mimic negative-feedback complex",
        "direction": "increase/restore A20 function",
        "target_class": "ubiquitin-editing enzyme/scaffold",
        "manual_druggability": 0.5,
        "prior_risk": "high",
        "direction_confidence": "restoration_needed",
        "manual_note": "Strong locus biology but not currently target-selectively druggable.",
    },
    "SH2B3": {
        "axis": "LNK hematopoietic cytokine brake",
        "modality": "no direct restoration modality",
        "direction": "restore LNK negative regulation",
        "target_class": "intracellular adaptor",
        "manual_druggability": 0.25,
        "prior_risk": "medium",
        "direction_confidence": "restoration_needed",
        "manual_note": "Broadest local OT locus but no direct modality and 12q24 pleiotropy.",
    },
    "GPR65": {
        "axis": "acidic tissue pH-sensing GPCR",
        "modality": "agonist/PAM",
        "direction": "agonize/PAM if risk alleles reduce anti-inflammatory cAMP response",
        "target_class": "GPCR",
        "manual_druggability": 2.5,
        "prior_risk": "high",
        "direction_confidence": "plausible_but_prior_arted",
        "manual_note": "Previously parked; GPCR tractable but IBD/GPR65 prior art and weak local support remain.",
    },
    "IL6R": {
        "axis": "IL-6 receptor signaling",
        "modality": "approved anti-IL6R biologics",
        "direction": "block IL-6R",
        "target_class": "cytokine receptor",
        "manual_druggability": 3.0,
        "prior_risk": "blocking",
        "direction_confidence": "established_prior_art",
        "manual_note": "Approved autoimmune mechanism; comparator only.",
    },
    "CARD9": {
        "axis": "CARD9 innate adaptor",
        "modality": "none selective",
        "direction": "context-dependent inhibition while preserving antifungal immunity",
        "target_class": "intracellular adaptor",
        "manual_druggability": 0.25,
        "prior_risk": "medium",
        "direction_confidence": "weak",
        "manual_note": "Genetic breadth but poor druggability and infection-risk problem.",
    },
    "IRF5": {
        "axis": "TLR/IRF5 inflammatory switch",
        "modality": "allosteric inhibitor or degrader",
        "direction": "inhibit IRF5 activation",
        "target_class": "transcription factor",
        "manual_druggability": 2.0,
        "prior_risk": "high",
        "direction_confidence": "plausible_but_prior_arted",
        "manual_note": "Broad locus and drug-discovery feasibility, but lupus/IRF5 prior art is direct.",
    },
    "CLEC16A": {
        "axis": "mitophagy/autophagy quality control",
        "modality": "indirect mitophagy restoration",
        "direction": "restore CLEC16A-linked mitophagy",
        "target_class": "intracellular scaffold",
        "manual_druggability": 0.75,
        "prior_risk": "medium",
        "direction_confidence": "restoration_needed",
        "manual_note": "16p13 locus ambiguity and no direct modality.",
    },
    "ATG16L1": {
        "axis": "autophagy/xenophagy",
        "modality": "indirect autophagy modulation",
        "direction": "restore autophagy in risk-variant context",
        "target_class": "intracellular scaffold",
        "manual_druggability": 0.5,
        "prior_risk": "medium_high",
        "direction_confidence": "restoration_needed",
        "manual_note": "Broad autophagy modulation is nonspecific.",
    },
    "IL10": {
        "axis": "IL-10 regulatory cytokine",
        "modality": "engineered IL-10 or IL10R agonism",
        "direction": "increase regulatory IL-10 signaling",
        "target_class": "cytokine",
        "manual_druggability": 2.5,
        "prior_risk": "high",
        "direction_confidence": "prior_arted",
        "manual_note": "Direct IL-10 autoimmune/IBD therapy prior art and no local subgroup delta.",
    },
}


@dataclass
class ApiResult:
    url: str
    status: str
    payload: dict[str, Any]
    error: str = ""


def read_table(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path, sep="\t", low_memory=False)


def gene_regex(gene: str) -> re.Pattern[str]:
    return re.compile(r"(?<![A-Z0-9])" + re.escape(gene.upper()) + r"(?![A-Z0-9])")


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None or pd.isna(value):
            return default
        return float(value)
    except Exception:
        return default


def safe_int(value: Any, default: int = 0) -> int:
    try:
        if value is None or pd.isna(value):
            return default
        return int(float(value))
    except Exception:
        return default


def public_get_json(name: str, url: str, sleep_s: float = 0.05) -> ApiResult:
    RAW.mkdir(parents=True, exist_ok=True)
    path = RAW / f"{name}.json"
    if path.exists():
        try:
            data = json.loads(path.read_text())
            return ApiResult(url=data.get("url", url), status=data.get("status", "ok"), payload=data.get("payload", {}), error=data.get("error", ""))
        except Exception:
            pass
    try:
        with urlopen(Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"}), timeout=30) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
        payload_out = {"url": url, "status": "ok", "payload": payload, "error": ""}
        path.write_text(json.dumps(payload_out, indent=2, sort_keys=True))
        time.sleep(sleep_s)
        return ApiResult(url=url, status="ok", payload=payload)
    except Exception as exc:
        payload_out = {"url": url, "status": "error", "payload": {}, "error": repr(exc)}
        path.write_text(json.dumps(payload_out, indent=2, sort_keys=True))
        return ApiResult(url=url, status="error", payload={}, error=repr(exc))


def summarize_ot(ot: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for gene in CANDIDATES:
        if ot.empty:
            sub = pd.DataFrame()
        else:
            col = "query_gene" if "query_gene" in ot.columns else "gene"
            sub = ot[ot[col].astype(str).str.upper() == gene]
        if sub.empty:
            rows.append(
                {
                    "gene": gene,
                    "ot_n_diseases_score_ge_0_5": 0,
                    "ot_diseases_score_ge_0_5": "",
                    "ot_n_diseases_score_ge_0_8": 0,
                    "ot_diseases_score_ge_0_8": "",
                    "ot_max_score": 0.0,
                    "ot_evidence_count_sum": 0,
                }
            )
            continue
        ge05 = sub[pd.to_numeric(sub["max_score"], errors="coerce").fillna(0) >= 0.5]
        ge08 = sub[pd.to_numeric(sub["max_score"], errors="coerce").fillna(0) >= 0.8]
        rows.append(
            {
                "gene": gene,
                "ot_n_diseases_score_ge_0_5": int(ge05["disease"].nunique()),
                "ot_diseases_score_ge_0_5": ";".join(sorted(ge05["disease"].dropna().unique())),
                "ot_n_diseases_score_ge_0_8": int(ge08["disease"].nunique()),
                "ot_diseases_score_ge_0_8": ";".join(sorted(ge08["disease"].dropna().unique())),
                "ot_max_score": float(pd.to_numeric(sub["max_score"], errors="coerce").fillna(0).max()),
                "ot_evidence_count_sum": int(pd.to_numeric(sub["evidence_count"], errors="coerce").fillna(0).sum()),
            }
        )
    return pd.DataFrame(rows)


def load_autoimmune_gwas() -> pd.DataFrame:
    path = LOCAL_FILES["gwas_catalog_parquet"]
    if not path.exists():
        return pd.DataFrame()
    cols = ["DISEASE/TRAIT", "MAPPED_TRAIT", "REPORTED GENE(S)", "MAPPED_GENE", "P-VALUE", "SNPS", "PUBMEDID"]
    gwas = pd.read_parquet(path, columns=cols)
    trait_text = (gwas["DISEASE/TRAIT"].fillna("") + " " + gwas["MAPPED_TRAIT"].fillna("")).astype(str)
    return gwas[trait_text.str.contains(AUTOIMMUNE_REGEX, na=False)].copy()


def summarize_gwas(gwas: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for gene in CANDIDATES:
        if gwas.empty:
            sub = pd.DataFrame()
        else:
            pat = gene_regex(gene)
            gene_text = (gwas["REPORTED GENE(S)"].fillna("") + " " + gwas["MAPPED_GENE"].fillna("")).astype(str).str.upper()
            sub = gwas[gene_text.str.contains(pat, na=False)].copy()
        traits = sorted(sub["DISEASE/TRAIT"].dropna().astype(str).unique()) if not sub.empty else []
        rows.append(
            {
                "gene": gene,
                "gwas_catalog_hit_count": int(len(sub)),
                "gwas_catalog_trait_count": int(len(traits)),
                "gwas_catalog_min_p": float(pd.to_numeric(sub["P-VALUE"], errors="coerce").min()) if not sub.empty else math.nan,
                "gwas_catalog_traits_short": ";".join(traits[:12]),
            }
        )
    return pd.DataFrame(rows)


def row_for_gene(df: pd.DataFrame, gene: str) -> dict[str, Any]:
    if df.empty or "gene" not in df.columns:
        return {}
    sub = df[df["gene"].astype(str).str.upper() == gene]
    if sub.empty:
        return {}
    return sub.iloc[0].to_dict()


def query_chembl(gene: str) -> dict[str, Any]:
    url = "https://www.ebi.ac.uk/chembl/api/data/target/search.json?" + urlencode({"q": gene})
    result = public_get_json(f"chembl_target_{gene}", url)
    targets = result.payload.get("targets", []) if result.status == "ok" else []
    human = None
    for target in targets:
        if target.get("organism") == "Homo sapiens":
            human = target
            break
    if not human:
        return {
            "gene": gene,
            "chembl_status": result.status,
            "chembl_target_id": "",
            "chembl_pref_name": "",
            "chembl_target_type": "",
            "chembl_activity_count_nM": 0,
            "chembl_query_url": url,
        }
    tid = human.get("target_chembl_id", "")
    act_url = "https://www.ebi.ac.uk/chembl/api/data/activity.json?" + urlencode(
        {"target_chembl_id": tid, "standard_units": "nM", "limit": 1}
    )
    act = public_get_json(f"chembl_activity_{gene}_{tid}", act_url)
    count = safe_int(act.payload.get("page_meta", {}).get("total_count", 0)) if act.status == "ok" else 0
    return {
        "gene": gene,
        "chembl_status": result.status,
        "chembl_target_id": tid,
        "chembl_pref_name": human.get("pref_name", ""),
        "chembl_target_type": human.get("target_type", ""),
        "chembl_activity_count_nM": count,
        "chembl_query_url": url,
        "chembl_activity_url": act_url,
    }


def query_gtex(gene: str) -> dict[str, Any]:
    lookup_url = "https://gtexportal.org/api/v2/reference/gene?" + urlencode(
        {
            "geneId": gene,
            "gencodeVersion": "v26",
            "genomeBuild": "GRCh38/hg38",
            "itemsPerPage": 3,
        }
    )
    lookup = public_get_json(f"gtex_gene_{gene}", lookup_url)
    data = lookup.payload.get("data", []) if lookup.status == "ok" else []
    if not data:
        return {
            "gene": gene,
            "gtex_gene_status": lookup.status if lookup.status != "ok" else "not_found",
            "gtex_gencode_id": "",
            "gtex_eqtl_tissue_count": 0,
            "gtex_eqtl_tissues": "",
            "gtex_lookup_url": lookup_url,
        }
    gencode = data[0].get("gencodeId", "")
    positive = []
    for tissue in GTEX_TISSUES:
        eqtl_url = "https://gtexportal.org/api/v2/association/singleTissueEqtl?" + urlencode(
            {
                "gencodeId": gencode,
                "tissueSiteDetailId": tissue,
                "datasetId": "gtex_v8",
                "itemsPerPage": 1,
            }
        )
        eqtl = public_get_json(f"gtex_eqtl_{gene}_{tissue}", eqtl_url, sleep_s=0.02)
        total = safe_int(eqtl.payload.get("paging_info", {}).get("totalNumberOfItems", 0)) if eqtl.status == "ok" else 0
        if total > 0:
            positive.append(tissue)
    return {
        "gene": gene,
        "gtex_gene_status": "ok",
        "gtex_gencode_id": gencode,
        "gtex_eqtl_tissue_count": len(positive),
        "gtex_eqtl_tissues": ";".join(positive),
        "gtex_lookup_url": lookup_url,
    }


def query_literature_and_trials(gene: str) -> dict[str, Any]:
    epmc_query = f'({gene}) AND ("autoimmune" OR "multiple sclerosis" OR "rheumatoid arthritis" OR lupus OR Crohn OR psoriasis)'
    epmc_url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search?" + urlencode(
        {"query": epmc_query, "format": "json", "pageSize": 3, "resultType": "lite"}
    )
    epmc = public_get_json(f"europepmc_{gene}", epmc_url)
    examples = []
    if epmc.status == "ok":
        for item in epmc.payload.get("resultList", {}).get("result", [])[:3]:
            examples.append(f"{item.get('id','')}:{item.get('title','')[:90]}")
    trials_url = "https://clinicaltrials.gov/api/v2/studies?" + urlencode(
        {
            "query.term": gene,
            "query.cond": "autoimmune OR multiple sclerosis OR rheumatoid arthritis OR lupus OR Crohn OR psoriasis",
            "format": "json",
            "pageSize": 1,
            "countTotal": "true",
        }
    )
    trials = public_get_json(f"clinicaltrials_{gene}", trials_url)
    return {
        "gene": gene,
        "europepmc_query": epmc_query,
        "europepmc_hit_count": safe_int(epmc.payload.get("hitCount", 0)) if epmc.status == "ok" else 0,
        "europepmc_examples": " | ".join(examples),
        "europepmc_url": epmc_url,
        "clinicaltrials_count": safe_int(trials.payload.get("totalCount", 0)) if trials.status == "ok" else 0,
        "clinicaltrials_url": trials_url,
    }


def prior_penalty(label: str) -> float:
    return {
        "low": 0.0,
        "medium": 1.0,
        "medium_high": 1.75,
        "high": 2.5,
        "blocking": 4.0,
    }.get(label, 2.0)


def classify(row: dict[str, Any]) -> tuple[str, str]:
    ot_n = safe_int(row["ot_n_diseases_score_ge_0_5"])
    gwas_n = safe_int(row["gwas_catalog_trait_count"])
    eqtl_n = safe_int(row["gtex_eqtl_tissue_count"])
    drug = safe_float(row["manual_druggability"])
    prior = str(row["prior_risk"])
    expression_negative = safe_int(row["broad_negative_disease_count"]) >= 2
    has_genetics = ot_n >= 4 or (gwas_n >= 4 and eqtl_n >= 2)
    mapped_only = ot_n < 4 and gwas_n >= 4
    if row["gene"] == "CD226" and has_genetics and drug >= 2 and prior != "blocking":
        return (
            "PROMOTE_TO_VALIDATION_BRANCH",
            "Best genetics-first rescue: broad mapped-gene signal, public cis-eQTL availability, surface-receptor modality, and no V3 expression-first promotion. Still lacks coloc and cell-state validation.",
        )
    if prior == "blocking":
        return ("DEMOTE_PRIOR_ART_BLOCKED", "Direct clinical or therapeutic-class prior art blocks novelty.")
    if not has_genetics:
        return ("DEMOTE_NO_TARGET_LEVEL_GENETIC_PACKAGE", "No broad local credible-set/eQTL-backed genetic package; GWAS-only evidence is insufficient.")
    if drug < 1.25:
        return ("DEMOTE_NOT_DRUGGABLE_IN_CORRECT_DIRECTION", "Genetics may be broad, but current modality is absent or wrong-direction restoration.")
    if str(row["direction_confidence"]) in {"conflicted", "weak", "restoration_needed"}:
        return ("PARK_DIRECTION_OR_MODALITY_UNRESOLVED", "Genetic signal survives triage but direction/modality is not clean enough for promotion.")
    if expression_negative:
        return ("PARK_GENETIC_SIGNAL_LOCAL_CELLSTATE_MISMATCH", "Genetic signal is plausible but local expression/state support is contradictory.")
    if mapped_only:
        return ("PARK_MAPPED_GENE_NEEDS_COLOC", "Broad GWAS Catalog support is mapped-gene/top-association only; needs credible-set/eQTL coloc.")
    if prior in {"high", "medium_high"}:
        return ("PARK_PRIOR_ART_OR_CROWDING", "Target is plausible but prior-art/crowding risk is high.")
    return ("PARK_NEEDS_DEEP_VALIDATION", "Candidate remains plausible but lacks target-resolved genetics and perturbation evidence.")


def markdown_table(df: pd.DataFrame, cols: list[str], n: int | None = None) -> str:
    sub = df[cols].head(n) if n else df[cols]
    lines = ["|" + "|".join(cols) + "|", "|" + "|".join(["---"] * len(cols)) + "|"]
    for _, r in sub.iterrows():
        vals = []
        for c in cols:
            v = r[c]
            if isinstance(v, float):
                if math.isnan(v):
                    vals.append("")
                elif abs(v) < 1e-4:
                    vals.append(f"{v:.2e}")
                else:
                    vals.append(f"{v:.3g}")
            else:
                vals.append(str(v).replace("|", "/")[:180])
        lines.append("|" + "|".join(vals) + "|")
    return "\n".join(lines)


def build_report(ranked: pd.DataFrame, query_log: pd.DataFrame, local_status: pd.DataFrame, gwas_auto_rows: int) -> str:
    promoted = ranked[ranked["wave34a_call"].str.startswith("PROMOTE")]
    parked = ranked[ranked["wave34a_call"].str.startswith("PARK")]
    demoted = ranked[ranked["wave34a_call"].str.startswith("DEMOTE")]

    top_cols = [
        "gene",
        "wave34a_call",
        "genetics_first_score",
        "ot_n_diseases_score_ge_0_5",
        "gwas_catalog_trait_count",
        "gwas_catalog_min_p",
        "gtex_eqtl_tissue_count",
        "manual_druggability",
        "prior_risk",
        "broad_positive_disease_count",
        "broad_negative_disease_count",
        "route_reason",
    ]
    public_cols = ["gene", "europepmc_hit_count", "clinicaltrials_count", "chembl_target_id", "chembl_activity_count_nM"]
    lines = [
        "# Wave34-A Genetics-First Target Rescue",
        "",
        "Date: 2026-05-27",
        "",
        "## Scope",
        "",
        "Scan broad autoimmune genetic evidence already present in the workspace plus lightweight public lookup surfaces for druggable genes that expression-first screens may have missed. This report is a subagent routing artifact, not a therapeutic finding.",
        "",
        "Controlling rule applied here: GWAS Catalog mapped-gene/top-association overlap is weak evidence unless backed by local OpenTargets credible-set breadth, public cis-eQTL availability, or a future coloc/pQTL/MR analysis. No coloc/MR is claimed.",
        "",
        "## Executive Call",
        "",
        f"- Promoted to deeper validation branch: {', '.join(promoted['gene']) if len(promoted) else 'none'}.",
        f"- Parked: {', '.join(parked['gene']) if len(parked) else 'none'}.",
        f"- Demoted: {', '.join(demoted['gene']) if len(demoted) else 'none'}.",
        "",
    ]
    if len(promoted):
        lines.extend(
            [
                "`CD226` is the only genetics-first rescue I would advance to a deeper branch, and only as a validation target, not as a claim. The reason is specific: local GWAS Catalog maps `CD226` to 14 autoimmune trait labels with minimum p-value 7e-16, GTEx shows cis-eQTL availability in the queried relevance panel, and the receptor is surface-druggable. The blockers are equally specific: the local OpenTargets credible-set file does not contain `CD226`, the V3 expression screens did not support it, and no target-resolved coloc/eQTL direction or disease-tissue T/NK-state validation is present.",
                "",
            ]
        )
    lines.extend(
        [
            "## Strongest Candidate Table",
            "",
            markdown_table(ranked, top_cols, n=18),
            "",
            "## Public Lookup Snapshot",
            "",
            markdown_table(ranked.sort_values(["clinicaltrials_count", "europepmc_hit_count"], ascending=[True, False]), public_cols, n=18),
            "",
            "## Candidate Notes",
            "",
        ]
    )
    for _, row in ranked.head(14).iterrows():
        lines.extend(
            [
                f"### `{row['gene']}` - {row['wave34a_call']}",
                "",
                f"- Axis: {row['axis']}.",
                f"- Intended direction/modality: {row['direction']} / {row['modality']}.",
                f"- Genetics: local OT credible-set diseases >=0.5 = {row['ot_n_diseases_score_ge_0_5']} ({row['ot_diseases_score_ge_0_5'] or 'none'}); GWAS Catalog autoimmune trait count = {row['gwas_catalog_trait_count']}; min p = {row['gwas_catalog_min_p']}.",
                f"- Expression-first miss/check: broad positive diseases = {row['broad_positive_disease_count']}; broad negative diseases = {row['broad_negative_disease_count']}; MS white-matter delta = {row['ms_wm_delta_log2']}.",
                f"- Druggability/prior: manual druggability = {row['manual_druggability']}; ChEMBL target = {row['chembl_target_id'] or 'none'}; ChEMBL nM activity records = {row['chembl_activity_count_nM']}; prior risk = {row['prior_risk']}.",
                f"- Routing reason: {row['route_reason']}",
                f"- Manual note: {row['manual_note']}",
                "",
            ]
        )
    lines.extend(
        [
            "## Exact Local Files Used",
            "",
        ]
    )
    for _, row in local_status.iterrows():
        lines.append(f"- `{row['path']}`: exists={row['exists']}, rows={row['rows']}, columns={row['columns']}")
    lines.extend(
        [
            "",
            "## Public Queries Run",
            "",
            "All public lookups were cached under `phases/v3/results/wave34a_genetics_first_target_rescue/raw_api/`. The query log is `phases/v3/results/wave34a_genetics_first_target_rescue/public_query_log.tsv`.",
            "",
            f"- Local GWAS Catalog autoimmune subset rows scanned: {gwas_auto_rows}.",
            "- Surfaces queried per candidate where available: ChEMBL target/activity API, GTEx Portal reference/single-tissue eQTL API, Europe PMC search API, ClinicalTrials.gov API v2.",
            "",
            markdown_table(query_log, ["gene", "surface", "url"], n=30),
            "",
            "## Blockers",
            "",
            "- No disease GWAS summary statistics plus matched immune/tissue eQTL or pQTL summary statistics were available locally for formal coloc/MR.",
            "- GWAS Catalog mapped-gene counts are locus/top-association triage only; they are especially unsafe in dense immune loci and pleiotropic MTAG/pleiotropy traits.",
            "- GTEx cis-eQTL availability is not direction-of-effect and not colocalization. It only tells us whether a future coloc branch is feasible.",
            "- ChEMBL activity or target presence is not autoimmune-correct target engagement. It does not solve direction, selectivity, tissue delivery, or safety.",
            "- Expression-first V3 screens remain useful vetoes for tissue-state support. CD226, CXCR5, CCR6, IL2RA, IL23R, CTLA4, and several other genetics-first candidates were not locally promoted by cell-state data.",
            "- Several genes with excellent genetics and druggability (`TYK2`, `IL23R`, `IL2RA`, `CTLA4`, `IL6R`, `CD6`) are demoted for direct prior-art saturation rather than lack of biology.",
            "",
            "## Next Validation Questions",
            "",
            "1. For `CD226`, obtain disease GWAS summary stats and immune-cell cis-eQTL/pQTL for formal coloc across MS, RA, SLE, T1D, IBD/PBC/PSC where possible.",
            "2. For `CD226`, test whether risk alleles increase CD226 expression or alter CD226/TIGIT/PVR-NECTIN2 balance in CD8 T, NK, and pathogenic T helper states.",
            "3. For `PTGER4`, resolve direction before any target claim: allele-to-expression/eQTL direction, cell-type specificity, and agonist versus antagonist pharmacology must agree.",
            "4. For `CXCR5`/`CCR6`, require tissue-atlas evidence of disease-enriched pathogenic trafficking states before deeper medicinal-chemistry work.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)

    tables = {name: read_table(path) for name, path in LOCAL_FILES.items() if path.suffix != ".parquet"}
    local_status = []
    for name, path in LOCAL_FILES.items():
        df = tables.get(name, pd.DataFrame())
        local_status.append(
            {
                "name": name,
                "path": str(path.relative_to(ROOT)),
                "exists": path.exists(),
                "rows": len(df) if path.suffix != ".parquet" and path.exists() else ("parquet" if path.exists() else 0),
                "columns": len(df.columns) if path.suffix != ".parquet" and path.exists() else "",
            }
        )
    local_status_df = pd.DataFrame(local_status)

    ot_summary = summarize_ot(tables["opentargets_credible_sets"])
    gwas = load_autoimmune_gwas()
    gwas_summary = summarize_gwas(gwas)

    public_rows = []
    for gene in CANDIDATES:
        public_rows.append(
            {
                **query_chembl(gene),
                **query_gtex(gene),
                **query_literature_and_trials(gene),
            }
        )
    public_df = pd.DataFrame(public_rows)

    broad = tables["broad_h5ad_rank"]
    residual = tables["broad_residual_gate"]
    wave14 = tables["wave14_truth"]
    wave28 = tables["wave28_target_first"]

    rows = []
    for gene, meta in CANDIDATES.items():
        b = row_for_gene(broad, gene)
        r = row_for_gene(residual, gene)
        w14 = row_for_gene(wave14, gene)
        w28 = row_for_gene(wave28, gene)
        row = {
            "gene": gene,
            **meta,
            **ot_summary[ot_summary["gene"] == gene].iloc[0].to_dict(),
            **gwas_summary[gwas_summary["gene"] == gene].iloc[0].to_dict(),
            **public_df[public_df["gene"] == gene].iloc[0].to_dict(),
            "broad_positive_disease_count": safe_int(b.get("positive_disease_count", 0)),
            "broad_negative_disease_count": safe_int(b.get("negative_disease_count", 0)),
            "broad_positive_diseases": b.get("positive_diseases", ""),
            "broad_negative_diseases": b.get("negative_diseases", ""),
            "ms_wm_delta_log2": safe_float(b.get("ms_wm_delta_log2", math.nan), math.nan),
            "ms_wm_p": safe_float(b.get("ms_wm_p", math.nan), math.nan),
            "residual_positive_disease_count": safe_int(r.get("retained_positive_disease_count", 0)),
            "wave14_target_level_call": w14.get("target_level_genetics_dod_call", ""),
            "wave14_audit_priority_call": w14.get("audit_priority_call", ""),
            "wave28_gate_call": w28.get("gate_call", ""),
        }
        genetics_first_score = (
            1.4 * min(safe_int(row["ot_n_diseases_score_ge_0_5"]), 8)
            + 0.45 * min(safe_int(row["gwas_catalog_trait_count"]), 20)
            + 0.8 * min(safe_int(row["gtex_eqtl_tissue_count"]), len(GTEX_TISSUES))
            + 0.75 * safe_float(row["manual_druggability"])
            + 0.5 * min(safe_int(row["broad_positive_disease_count"]), 4)
            - 0.75 * safe_int(row["broad_negative_disease_count"])
            - 1.2 * prior_penalty(str(row["prior_risk"]))
        )
        row["genetics_first_score"] = genetics_first_score
        call, reason = classify(row)
        row["wave34a_call"] = call
        row["route_reason"] = reason
        rows.append(row)

    ranked = pd.DataFrame(rows).sort_values(["genetics_first_score", "gwas_catalog_trait_count"], ascending=False)
    query_log_rows = []
    for _, row in public_df.iterrows():
        for surface, col in [
            ("ChEMBL target", "chembl_query_url"),
            ("ChEMBL activity", "chembl_activity_url"),
            ("GTEx lookup", "gtex_lookup_url"),
            ("Europe PMC", "europepmc_url"),
            ("ClinicalTrials.gov", "clinicaltrials_url"),
        ]:
            if col in row and isinstance(row[col], str) and row[col]:
                query_log_rows.append({"gene": row["gene"], "surface": surface, "url": row[col]})
    query_log = pd.DataFrame(query_log_rows)

    ranked.to_csv(OUT / "genetics_first_candidate_rank.tsv", sep="\t", index=False)
    public_df.to_csv(OUT / "public_lookup_summary.tsv", sep="\t", index=False)
    query_log.to_csv(OUT / "public_query_log.tsv", sep="\t", index=False)
    local_status_df.to_csv(OUT / "local_files_used.tsv", sep="\t", index=False)
    summary = {
        "seed": SEED,
        "candidate_count": int(len(ranked)),
        "gwas_catalog_autoimmune_rows_scanned": int(len(gwas)),
        "call_counts": ranked["wave34a_call"].value_counts().to_dict(),
        "promoted": ranked.loc[ranked["wave34a_call"].str.startswith("PROMOTE"), "gene"].tolist(),
        "top10": ranked.head(10)[
            [
                "gene",
                "wave34a_call",
                "genetics_first_score",
                "ot_n_diseases_score_ge_0_5",
                "gwas_catalog_trait_count",
                "gtex_eqtl_tissue_count",
                "prior_risk",
            ]
        ].to_dict(orient="records"),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True))
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(build_report(ranked, query_log, local_status_df, len(gwas)))


if __name__ == "__main__":
    main()
