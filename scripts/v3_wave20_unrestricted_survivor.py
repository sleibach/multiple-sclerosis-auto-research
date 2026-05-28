#!/usr/bin/env python3
"""Wave20 stress test for unrestricted survivor candidates.

This script consolidates local V3 evidence and lightweight public API checks
for the unrestricted survivor set. It deliberately treats expression recurrence
as triage only; the output gate calls require residual specificity, perturbation
or model support, an explicit intervention direction, tractability, safety, and
prior-art delta.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import quote_plus

import pandas as pd
import requests


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results_v3" / "wave20_unrestricted_survivor"
DATE = "2026-05-27"

FOCUS_GENES = [
    "SNX10",
    "DAP",
    "FMNL2",
    "TNFAIP8L1",
    "PPIL3",
    "NCK1",
    "PLEK2",
    "SEL1L3",
    "AQR",
    "C15ORF48",
]


@dataclass(frozen=True)
class GateAnnotation:
    biology_class: str
    perturbation_note: str
    direction: str
    modality: str
    safety_repair_risk: str
    prior_art_delta: str
    wave20_call: str
    least_bad_rank: int | None
    rationale: str


ANNOTATIONS: dict[str, GateAnnotation] = {
    "SNX10": GateAnnotation(
        biology_class="intracellular endosomal/phagolysosomal trafficking marker",
        perturbation_note="Geneformer has the strongest focused signal in this set, and public mouse macrophage/colitis perturbation exists, but not against the V3 IFN/APC module.",
        direction="No safe direction. Inhibition/knockdown is the plausible anti-colitis direction; restoration/activation is plausible for host defense and phagosome maturation.",
        modality="Poor. Intracellular PX-domain trafficking protein; no mature selective SNX10 drug modality found.",
        safety_repair_risk="High host-defense and repair risk: SNX10 supports macrophage phagosome maturation and bacterial killing; osteoclast biology adds bone/remodeling liabilities.",
        prior_art_delta="Weak. IBD macrophage/colitis and phagosome biology are already public; broad autoimmunity delta is not established.",
        wave20_call="LEAST_BAD_COMPARATOR_ONLY",
        least_bad_rank=1,
        rationale="Best comparator because it has Crohn/UC myeloid recurrence plus weak model and public macrophage perturbation, but it fails strict residual specificity, modality, safety, and novelty.",
    ),
    "C15ORF48": GateAnnotation(
        biology_class="intracellular mitochondrial/inflammatory macrophage marker (MOCCI/miR-147b)",
        perturbation_note="No Geneformer token support in the current route; public MOCCI perturbation biology is inflammation/mitochondrial feedback, not a V3 module intervention.",
        direction="Ambiguous. Literature suggests MOCCI can be anti-inflammatory feedback, so high expression is not automatically a pathogenic inhibition target.",
        modality="Poor. Mitochondrial microprotein plus miRNA biology; no practical target-engagement modality for autoimmune tissue state.",
        safety_repair_risk="High uncertainty: manipulating mitochondrial inflammatory feedback can impair host defense or stress adaptation.",
        prior_art_delta="Weak. MOCCI/C15ORF48 inflammatory macrophage biology is already published; local signal is still marker-like.",
        wave20_call="STATE_MARKER_ONLY",
        least_bad_rank=2,
        rationale="Strong expression marker, including myeloid IBD, but model-blocked and non-druggable.",
    ),
    "NCK1": GateAnnotation(
        biology_class="intracellular adaptor for TCR/actin signaling",
        perturbation_note="Public TCR-Nck inhibitor literature exists, but local V3 support is residual-negative and not T-cell-specific.",
        direction="Inhibit TCR-Nck interaction if pursuing autoimmunity, but that is a broad T-cell immunosuppression route rather than V3 tissue-state control.",
        modality="Medium but wrong context. PPI/small-molecule precedent exists for TCR-Nck; not a selective tissue APC/repair-state modality.",
        safety_repair_risk="High: broad TCR, immune synapse, actin, and Treg/function effects.",
        prior_art_delta="Poor. Autoimmune TCR-Nck inhibitor prior art already captures the plausible intervention.",
        wave20_call="MODALITY_COMPARATOR_ONLY",
        least_bad_rank=3,
        rationale="Useful as a druggability comparator, not as a V3 survivor target.",
    ),
    "FMNL2": GateAnnotation(
        biology_class="intracellular formin/actin migration and barrier-remodeling marker",
        perturbation_note="Weak Geneformer support only; Crohn rare-variant/function paper is human genetics-adjacent but not causal broad autoimmunity.",
        direction="Inhibition of actin/formin migration is the only obvious direction, but local disease signal could mark repair/remodeling.",
        modality="Poor. No selective autoimmune-ready FMNL2 modality found.",
        safety_repair_risk="High: cytoskeletal migration, epithelial repair, macrophage/mesenchymal motility.",
        prior_art_delta="Insufficient. A Crohn rare-variant report exists but does not supply a broad therapeutic delta.",
        wave20_call="NO_GO_INTRACELLULAR_REMODELING_MARKER",
        least_bad_rank=4,
        rationale="Broad expression recurrence is offset by weak residual/model evidence and non-druggable repair biology.",
    ),
    "DAP": GateAnnotation(
        biology_class="intracellular IFN/cell-death/autophagy stress marker",
        perturbation_note="Geneformer support is present but weak and lacks real V3 perturbation concordance.",
        direction="Ambiguous. DAP1 inhibition or restoration would affect apoptosis/autophagy rather than a defined APC-state controller.",
        modality="Poor. No mature target-selective autoimmune modality found.",
        safety_repair_risk="High: apoptosis, autophagy, stress-response and cell survival liabilities.",
        prior_art_delta="Poor. IFN-gamma cell-death/autophagy biology is old and nonspecific.",
        wave20_call="NO_GO_STRESS_MARKER",
        least_bad_rank=5,
        rationale="Model signal is not enough; biology is generic IFN/death/autophagy.",
    ),
    "PPIL3": GateAnnotation(
        biology_class="nuclear cyclophilin/spliceosome-associated protein",
        perturbation_note="Only one weak Geneformer support context; no real perturbation support found.",
        direction="No explicit therapeutic direction.",
        modality="Poor. Nuclear PPIase/spliceosome biology lacks selective autoimmune modality.",
        safety_repair_risk="High: spliceosome/proteostasis intervention would be broadly toxic.",
        prior_art_delta="None useful; sparse gene-specific autoimmunity art.",
        wave20_call="NO_GO_NONDRUGGABLE_INTRACELLULAR",
        least_bad_rank=6,
        rationale="Expression-only survivor with no direction or tractability.",
    ),
    "PLEK2": GateAnnotation(
        biology_class="intracellular PI3K-phosphoinositide/actin cytoskeleton marker",
        perturbation_note="No Geneformer support and no real V3 perturbation support.",
        direction="No safe explicit direction; inhibition would likely affect actin remodeling and hematopoietic/tissue functions.",
        modality="Poor. No selective PLEK2 autoimmune modality found.",
        safety_repair_risk="High: cytoskeleton, spreading, migration, and tissue repair liabilities.",
        prior_art_delta="None useful; biology is generic cytoskeletal remodeling.",
        wave20_call="NO_GO_CYTOSKELETAL_MARKER",
        least_bad_rank=7,
        rationale="Strong MS nominal expression does not overcome zero residual/model/druggability support.",
    ),
    "TNFAIP8L1": GateAnnotation(
        biology_class="intracellular TIPE-family inflammation/cell-death/lipid-transfer-adjacent marker",
        perturbation_note="No Geneformer support and no direct V3 perturbation support.",
        direction="Ambiguous across TIPE-family immune regulation, cell death, autophagy, and lipid second-messenger biology.",
        modality="Poor. No gene-selective autoimmune modality found.",
        safety_repair_risk="High uncertainty: immune homeostasis and cell-death pathway risk.",
        prior_art_delta="Thin. Family-level inflammation literature exists but TNFAIP8L1-specific autoimmunity evidence is weak.",
        wave20_call="NO_GO_THIN_INTRACELLULAR_MARKER",
        least_bad_rank=8,
        rationale="Four-disease expression recurrence collapses under residual/model gates.",
    ),
    "SEL1L3": GateAnnotation(
        biology_class="undercharacterized intracellular/ER-adjacent SEL1L-family marker",
        perturbation_note="No Geneformer support and no real V3 perturbation support.",
        direction="No explicit therapeutic direction.",
        modality="Poor. No mature target modality found.",
        safety_repair_risk="Unknown-to-high: undercharacterized ER/protein-quality biology and tissue expression.",
        prior_art_delta="None useful for autoimmunity.",
        wave20_call="NO_GO_UNDERCHARACTERIZED_MARKER",
        least_bad_rank=9,
        rationale="Thin biology plus no residual, perturbation, direction, or modality.",
    ),
    "AQR": GateAnnotation(
        biology_class="nuclear spliceosome RNA helicase marker",
        perturbation_note="No Geneformer support and no real V3 perturbation support.",
        direction="No autoimmune-relevant direction.",
        modality="Poor. Spliceosome helicase intervention is not selective for inflamed tissue states.",
        safety_repair_risk="Very high: core RNA processing liability.",
        prior_art_delta="None; any spliceosome-autoimmunity link would be generic and unsafe.",
        wave20_call="NO_GO_CORE_SPLICEOSOME_MARKER",
        least_bad_rank=10,
        rationale="Expression recurrence only; core nuclear machinery is a kill under Wave19 gates.",
    ),
    "CHI3L1": GateAnnotation(
        biology_class="secreted YKL-40 inflammatory/repair biomarker",
        perturbation_note="No supportive Geneformer deletion; public autoimmune biomarker/target literature is crowded.",
        direction="Neutralization is conceivable but not V3-specific and may disturb repair/remodeling.",
        modality="Medium. Secreted protein is accessible, but disease-state selectivity is poor.",
        safety_repair_risk="Medium-to-high: tissue repair, fibrosis/remodeling, and inflammatory biomarker entanglement.",
        prior_art_delta="Poor; YKL-40 autoimmune/inflammatory biomarker literature is saturated.",
        wave20_call="ADJACENT_DEMOTE_PRIOR_ART",
        least_bad_rank=12,
        rationale="Accessible but crowded and marker-like.",
    ),
    "LTA4H": GateAnnotation(
        biology_class="intracellular leukotriene enzyme/lipid inflammation comparator",
        perturbation_note="Public LTA4H inhibitor/IBD inflammation literature exists; local model route was already vetoed.",
        direction="Inhibit leukotriene A4 hydrolase to reduce LTB4, but this is generic inflammatory-lipid prior art.",
        modality="High. Enzyme is druggable, but not novel or V3-specific.",
        safety_repair_risk="Medium: leukotriene and neutrophil/infection biology.",
        prior_art_delta="Poor; IBD/inflammatory inhibitor literature is already close.",
        wave20_call="ADJACENT_DEMOTE_PRIOR_ART",
        least_bad_rank=13,
        rationale="Druggable but prior-arted and generic.",
    ),
    "APOC1": GateAnnotation(
        biology_class="secreted/intracellular apolipoprotein lipid-myeloid marker",
        perturbation_note="Prior Geneformer deletion veto; local residual gate negative.",
        direction="No safe direction; lipid handling can be repair or pathology depending on compartment.",
        modality="Poor-to-medium. Secreted apolipoprotein biology is accessible in principle but nonspecific.",
        safety_repair_risk="High: lipid transport, myeloid repair, CNS/gut context dependence.",
        prior_art_delta="Poor; already demoted in V3 by model and prior-art gates.",
        wave20_call="ADJACENT_DEMOTE_MODEL",
        least_bad_rank=16,
        rationale="Failed the previous survivor route.",
    ),
    "CBX3": GateAnnotation(
        biology_class="intracellular chromatin/proliferation stress marker",
        perturbation_note="No real V3 perturbation support; one strict residual survivor is not enough and fits generic chromatin/stress.",
        direction="No selective autoimmune direction.",
        modality="Poor. Chromatin targeting would be broad and toxic.",
        safety_repair_risk="Very high: proliferation, chromatin, genome regulation.",
        prior_art_delta="Insufficient; broad chromatin biology is not a V3 target delta.",
        wave20_call="ADJACENT_HOLD_GENERIC",
        least_bad_rank=11,
        rationale="The only strict residual positive in this set, but it is a chromatin/proliferation marker with no tractable safe direction.",
    ),
    "CXCL9": GateAnnotation(
        biology_class="secreted IFN-gamma/CXCR3 chemokine",
        perturbation_note="No Geneformer support; biology is canonical IFN trafficking.",
        direction="Block CXCL9/CXCR3 axis, but that is broad lymphocyte trafficking and not lipid-lysosomal/APC-state selective.",
        modality="Medium. Secreted chemokine is accessible, but pathway redundancy and generic IFN confounding are high.",
        safety_repair_risk="High: host defense and lymphocyte recruitment.",
        prior_art_delta="Poor; IFN/CXCR3 chemokine autoimmunity prior art is crowded.",
        wave20_call="ADJACENT_HOLD_GENERIC_IFN",
        least_bad_rank=14,
        rationale="Expression recurrence is IFN/APC-density confounded.",
    ),
    "PPP3CA": GateAnnotation(
        biology_class="intracellular calcineurin catalytic subunit",
        perturbation_note="No supportive Geneformer signal; calcineurin inhibitors are already clinical immunosuppressants.",
        direction="Inhibit calcineurin, already captured by cyclosporine/tacrolimus class.",
        modality="High but unsafe/prior-arted.",
        safety_repair_risk="Very high: systemic immunosuppression, renal, neurologic, infection and broad T-cell liabilities.",
        prior_art_delta="None for V3; calcineurin immunosuppression is established.",
        wave20_call="ADJACENT_DEMOTE_PRIOR_ART",
        least_bad_rank=15,
        rationale="Druggable but not a novel or selective V3 target.",
    ),
}

SOURCE_LINKS = [
    {
        "gene": "SNX10",
        "source_key": "SNX10_colitis_pmid_26856241",
        "evidence_type": "mouse disease perturbation/prior art",
        "url": "https://pubmed.ncbi.nlm.nih.gov/26856241/",
        "note": "SNX10 as macrophage-polarization regulator in experimental mouse colitis.",
    },
    {
        "gene": "SNX10",
        "source_key": "SNX10_phagosome_pmc_5589552",
        "evidence_type": "host-defense safety",
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC5589552/",
        "note": "SNX10 promotes macrophage phagosome maturation and Listeria control.",
    },
    {
        "gene": "SNX10",
        "source_key": "SNX10_osteoclast_pmid_22174188",
        "evidence_type": "repair/bone safety",
        "url": "https://pubmed.ncbi.nlm.nih.gov/22174188/",
        "note": "SNX10 required for osteoclast formation and resorption.",
    },
    {
        "gene": "C15ORF48",
        "source_key": "C15ORF48_sciadv_pmid_34878835",
        "evidence_type": "macrophage inflammation prior art",
        "url": "https://pubmed.ncbi.nlm.nih.gov/34878835/",
        "note": "Inflammation-induced C15orf48/MOCCI cytochrome-c-oxidase remodeling.",
    },
    {
        "gene": "C15ORF48",
        "source_key": "MOCCI_natcomm_pmc_8035321",
        "evidence_type": "mechanism prior art",
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC8035321/",
        "note": "Coding and non-coding roles of MOCCI/C15ORF48 in host inflammation and immunity.",
    },
    {
        "gene": "DAP",
        "source_key": "DAP_ifng_pmid_7828849",
        "evidence_type": "IFN/death prior art",
        "url": "https://pubmed.ncbi.nlm.nih.gov/7828849/",
        "note": "Original IFN-gamma-induced DAP/DAPK cell-death mediator paper.",
    },
    {
        "gene": "DAP",
        "source_key": "DAP1_autophagy_pmc_4249318",
        "evidence_type": "autophagy safety",
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC4249318/",
        "note": "DAP1 as autophagy/apoptosis regulator.",
    },
    {
        "gene": "FMNL2",
        "source_key": "FMNL2_crohn_plosone_2021",
        "evidence_type": "human Crohn adjacent prior art",
        "url": "https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0252428",
        "note": "Functional characterization of FMNL2 L136P from a pediatric Crohn disease case.",
    },
    {
        "gene": "FMNL2",
        "source_key": "FMNL2_actin_pmc_3765947",
        "evidence_type": "cytoskeleton safety",
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC3765947/",
        "note": "FMNL2 drives actin protrusion and migration downstream of Cdc42.",
    },
    {
        "gene": "TNFAIP8L1",
        "source_key": "TIPE_family_pmid_30274259",
        "evidence_type": "family-level immune prior art",
        "url": "https://pubmed.ncbi.nlm.nih.gov/30274259/",
        "note": "TIPE/TNFAIP8 family review covering immunity, inflammation, cell death, autophagy and lipid messengers.",
    },
    {
        "gene": "PPIL3",
        "source_key": "nuclear_cyclophilins_pmid_30518120",
        "evidence_type": "spliceosome/nuclear cyclophilin biology",
        "url": "https://pubmed.ncbi.nlm.nih.gov/30518120/",
        "note": "Human nuclear cyclophilin review includes PPIL3.",
    },
    {
        "gene": "NCK1",
        "source_key": "TCR_NCK_inhibitor_pmid_28003549",
        "evidence_type": "small-molecule prior art",
        "url": "https://pubmed.ncbi.nlm.nih.gov/28003549/",
        "note": "First-in-class TCR-Nck inhibitor framed for autoimmune diseases.",
    },
    {
        "gene": "NCK1",
        "source_key": "AX024_reassessment_pmid_32317279",
        "evidence_type": "modality caveat",
        "url": "https://pubmed.ncbi.nlm.nih.gov/32317279/",
        "note": "AX-024 biology reassessment: T-cell proliferation effects may be independent of CD3epsilon/Nck1 interaction.",
    },
    {
        "gene": "PLEK2",
        "source_key": "PLEK2_review_frontiers_2021",
        "evidence_type": "cytoskeleton safety",
        "url": "https://www.frontiersin.org/articles/10.3389/fcell.2021.768238/full",
        "note": "Pleckstrin-2 roles in actin/cell spreading and hematopoietic contexts.",
    },
    {
        "gene": "SEL1L3",
        "source_key": "SEL1L3_hpa",
        "evidence_type": "expression/resource",
        "url": "https://www.proteinatlas.org/ENSG00000091490-SEL1L3/tissue",
        "note": "Human Protein Atlas tissue-expression resource for undercharacterized SEL1L3.",
    },
    {
        "gene": "AQR",
        "source_key": "AQR_spliceosome_pmid_25599396",
        "evidence_type": "core splicing safety",
        "url": "https://pubmed.ncbi.nlm.nih.gov/25599396/",
        "note": "Aquarius RNA helicase recruitment to spliceosomes.",
    },
    {
        "gene": "CHI3L1",
        "source_key": "YKL40_autoimmune_review_pmc_9254466",
        "evidence_type": "crowded prior art",
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC9254466/",
        "note": "Comprehensive review of YKL-40/CHI3L1 in autoimmune diseases.",
    },
    {
        "gene": "LTA4H",
        "source_key": "LTA4H_colitis_inhibitor_pmc_2267273",
        "evidence_type": "direct disease intervention prior art",
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC2267273/",
        "note": "Selective LTA4H inhibitor attenuated inflammatory rat colitis.",
    },
    {
        "gene": "SDC4",
        "source_key": "SDC4_EAE_pmid_24516197",
        "evidence_type": "adjacent survivor prior art",
        "url": "https://pubmed.ncbi.nlm.nih.gov/24516197/",
        "note": "DC-HIL/syndecan-4 pathway regulates autoimmune responses through MDSCs.",
    },
]

QUERY_PLAN = {
    "SNX10": [
        "SNX10 macrophage colitis",
        "SNX10 autoimmune",
        "SNX10 phagosome macrophage infection",
    ],
    "C15ORF48": [
        "C15ORF48 MOCCI inflammation macrophage",
        "C15ORF48 autoimmune",
        "MOCCI host inflammation immunity",
    ],
    "DAP": [
        "DAP1 interferon gamma cell death",
        "DAP1 autophagy apoptosis",
        "DAP1 autoimmune",
    ],
    "FMNL2": [
        "FMNL2 Crohn disease L136P",
        "FMNL2 actin migration inflammation",
        "FMNL2 autoimmune",
    ],
    "TNFAIP8L1": [
        "TNFAIP8L1 TIPE1 inflammation immune",
        "TNFAIP8L1 autoimmune",
    ],
    "PPIL3": [
        "PPIL3 cyclophilin spliceosome",
        "PPIL3 autoimmune",
    ],
    "NCK1": [
        "NCK1 TCR inhibitor autoimmune",
        "AX-024 Nck1 CD3 autoimmune",
        "NCK1 regulatory T cells",
    ],
    "PLEK2": [
        "PLEK2 actin cytoskeleton cell spreading",
        "PLEK2 autoimmune inflammation",
    ],
    "SEL1L3": [
        "SEL1L3 immune inflammation",
        "SEL1L3 Human Protein Atlas",
    ],
    "AQR": [
        "AQR Aquarius spliceosome",
        "AQR autoimmune",
    ],
    "CHI3L1": [
        "CHI3L1 YKL-40 autoimmune disease",
        "CHI3L1 biomarker inflammatory diseases",
    ],
    "LTA4H": [
        "LTA4H inhibitor colitis",
        "leukotriene A4 hydrolase autoimmune",
    ],
    "APOC1": [
        "APOC1 autoimmune inflammation",
        "APOC1 macrophage lipid inflammation",
    ],
    "CBX3": [
        "CBX3 autoimmune inflammation",
        "CBX3 chromatin inflammation",
    ],
    "CXCL9": [
        "CXCL9 autoimmune disease interferon gamma",
        "CXCL9 CXCR3 autoimmune",
    ],
    "PPP3CA": [
        "PPP3CA calcineurin autoimmune",
        "calcineurin inhibitors autoimmune tacrolimus cyclosporine",
    ],
}

CHEMBL_TARGET_WHITELIST = {
    "CHI3L1": "CHEMBL5724768",
    "LTA4H": "CHEMBL4618",
    "CBX3": "CHEMBL3826866",
    "PPP3CA": "CHEMBL4445",
    "NCK1": "CHEMBL4846",
}


def read_tsv(rel_path: str) -> pd.DataFrame:
    path = ROOT / rel_path
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path, sep="\t", low_memory=False)


def first_row(df: pd.DataFrame, gene: str) -> dict[str, Any]:
    if df.empty or "gene" not in df.columns:
        return {}
    sub = df[df["gene"].astype(str).eq(gene)]
    if sub.empty:
        return {}
    return sub.iloc[0].to_dict()


def num(value: Any, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except Exception:
        return default


def text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float) and pd.isna(value):
        return ""
    return str(value)


def short(value: Any, n: int = 300) -> str:
    s = text(value).replace("\n", " ").replace("\t", " ")
    return s[:n]


def api_get_json(url: str, timeout: int = 25) -> tuple[str, dict[str, Any] | None]:
    try:
        response = requests.get(url, timeout=timeout, headers={"User-Agent": "ms-auto-research-wave20/1.0"})
        response.raise_for_status()
        return "ok", response.json()
    except Exception as exc:
        return f"error:{type(exc).__name__}:{exc}", None


def europepmc_search_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for gene, queries in QUERY_PLAN.items():
        for query in queries:
            api_url = (
                "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
                f"?query={quote_plus(query)}&resultType=lite&pageSize=3&format=json"
            )
            status, payload = api_get_json(api_url)
            hit_count = ""
            top_title = ""
            top_year = ""
            top_url = ""
            if payload:
                hit_count = payload.get("hitCount", "")
                results = payload.get("resultList", {}).get("result", [])
                if results:
                    top = results[0]
                    top_title = top.get("title", "")
                    top_year = top.get("pubYear", "")
                    pmid = top.get("pmid", "")
                    doi = top.get("doi", "")
                    pmcid = top.get("pmcid", "")
                    if pmid:
                        top_url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
                    elif pmcid:
                        top_url = f"https://pmc.ncbi.nlm.nih.gov/articles/{pmcid}/"
                    elif doi:
                        top_url = f"https://doi.org/{doi}"
            rows.append(
                {
                    "gene": gene,
                    "source": "EuropePMC",
                    "query": query,
                    "hit_count": hit_count,
                    "top_title": short(top_title, 500),
                    "top_year": top_year,
                    "top_url": top_url,
                    "api_url": api_url,
                    "status": status,
                }
            )
            time.sleep(0.05)
    return rows


def uniprot_rows(genes: list[str]) -> list[dict[str, Any]]:
    rows = []
    fields = "accession,reviewed,protein_name,cc_function,cc_subcellular_location,ft_transmem,ft_signal"
    for gene in genes:
        api_url = (
            "https://rest.uniprot.org/uniprotkb/search"
            f"?query=gene_exact:{quote_plus(gene)}%20AND%20organism_id:9606%20AND%20reviewed:true"
            f"&fields={fields}&format=json&size=1"
        )
        status, payload = api_get_json(api_url)
        results = payload.get("results", []) if payload else []
        if not results:
            fallback_url = (
                "https://rest.uniprot.org/uniprotkb/search"
                f"?query=gene_exact:{quote_plus(gene)}%20AND%20organism_id:9606"
                f"&fields={fields}&format=json&size=1"
            )
            status, payload = api_get_json(fallback_url)
            api_url = fallback_url
            results = payload.get("results", []) if payload else []
        row = {
            "gene": gene,
            "source": "UniProt",
            "api_url": api_url,
            "status": status,
            "accession": "",
            "entry_type": "",
            "protein_name": "",
            "function_excerpt": "",
            "subcellular_location_excerpt": "",
            "transmembrane_feature_count": "",
            "signal_peptide_feature_count": "",
            "uniprot_url": "",
        }
        if results:
            entry = results[0]
            accession = entry.get("primaryAccession", "")
            row["accession"] = accession
            row["entry_type"] = entry.get("entryType", "")
            row["uniprot_url"] = f"https://www.uniprot.org/uniprotkb/{accession}/entry" if accession else ""
            pdesc = entry.get("proteinDescription", {})
            rec = pdesc.get("recommendedName", {})
            full = rec.get("fullName", {}).get("value", "")
            if not full:
                subs = pdesc.get("submissionNames", [])
                if subs:
                    full = subs[0].get("fullName", {}).get("value", "")
            row["protein_name"] = full
            comments = entry.get("comments", [])
            function_texts = []
            location_texts = []
            for comment in comments:
                if comment.get("commentType") == "FUNCTION":
                    for item in comment.get("texts", []):
                        function_texts.append(item.get("value", ""))
                if comment.get("commentType") == "SUBCELLULAR LOCATION":
                    for loc in comment.get("subcellularLocations", []):
                        location = loc.get("location", {}).get("value", "")
                        if location:
                            location_texts.append(location)
            row["function_excerpt"] = short(" ".join(function_texts), 700)
            row["subcellular_location_excerpt"] = short("; ".join(location_texts), 400)
            features = entry.get("features", [])
            row["transmembrane_feature_count"] = sum(1 for f in features if f.get("type") == "Transmembrane")
            row["signal_peptide_feature_count"] = sum(1 for f in features if f.get("type") == "Signal")
        rows.append(row)
        time.sleep(0.05)
    return rows


def chembl_rows(genes: list[str]) -> list[dict[str, Any]]:
    rows = []
    for gene in genes:
        api_url = f"https://www.ebi.ac.uk/chembl/api/data/target/search.json?q={quote_plus(gene)}"
        status, payload = api_get_json(api_url)
        targets = payload.get("targets", []) if payload else []
        whitelist_id = CHEMBL_TARGET_WHITELIST.get(gene)
        chosen = {}
        if whitelist_id:
            chosen = next((t for t in targets if t.get("target_chembl_id") == whitelist_id), {})
        if not chosen:
            human_targets = [t for t in targets if t.get("organism") == "Homo sapiens"]
            target_gene_in_name = [
                t for t in human_targets if gene.upper() in str(t.get("pref_name", "")).upper()
            ]
            chosen = target_gene_in_name[0] if target_gene_in_name else {}
        target_id = chosen.get("target_chembl_id", "")
        activity_count = ""
        activity_url = ""
        if target_id:
            activity_url = (
                "https://www.ebi.ac.uk/chembl/api/data/activity.json"
                f"?target_chembl_id={quote_plus(target_id)}&limit=1"
            )
            a_status, a_payload = api_get_json(activity_url)
            if a_payload:
                activity_count = a_payload.get("page_meta", {}).get("total_count", "")
            if status == "ok":
                status = f"ok;activity_{a_status}"
        rows.append(
            {
                "gene": gene,
                "source": "ChEMBL target search",
                "query": gene,
                "api_url": api_url,
                "status": status,
                "target_count": payload.get("page_meta", {}).get("total_count", "") if payload else "",
                "chosen_target_chembl_id": target_id,
                "chosen_pref_name": chosen.get("pref_name", ""),
                "chosen_target_type": chosen.get("target_type", ""),
                "chosen_organism": chosen.get("organism", ""),
                "activity_count_for_chosen_target": activity_count,
                "chembl_target_url": f"https://www.ebi.ac.uk/chembl/target_report_card/{target_id}/" if target_id else "",
                "chembl_activity_api_url": activity_url,
            }
        )
        time.sleep(0.05)
    return rows


def build_local_evidence(genes: list[str]) -> pd.DataFrame:
    survivor = read_tsv("results_v3/unrestricted_survivor_scan/unrestricted_survivor_candidates.tsv")
    broad = read_tsv("results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_rank.tsv")
    residual = read_tsv("results_v3/broad_residual_gate/broad_residual_gate_summary.tsv")
    focused_residual = read_tsv("results_v3/snx10_c15orf48_residual_gate/snx10_c15orf48_residual_gate.tsv")
    geneformer = read_tsv("results_v3/geneformer_unrestricted_survivor_delete/geneformer_unrestricted_survivor_gene_summary.tsv")

    rows = []
    for gene in genes:
        s = first_row(survivor, gene)
        b = first_row(broad, gene)
        r = first_row(residual, gene)
        fr = first_row(focused_residual, gene)
        gf = first_row(geneformer, gene)
        row = {
            "gene": gene,
            "scope": "focus" if gene in FOCUS_GENES else "adjacent_from_candidate_tsv",
            "routing_decision": text(s.get("routing_decision")),
            "manual_status": text(s.get("manual_status")),
            "manual_reason": text(s.get("manual_reason")),
            "positive_disease_count": num(s.get("positive_disease_count", b.get("positive_disease_count"))),
            "negative_disease_count": num(s.get("negative_disease_count", b.get("negative_disease_count"))),
            "positive_compartment_count": num(s.get("positive_compartment_count", b.get("positive_compartment_count"))),
            "positive_fdr10_compartment_count": num(b.get("positive_fdr10_compartment_count")),
            "positive_diseases": text(s.get("positive_diseases", b.get("positive_diseases"))),
            "top_positive_compartments": text(s.get("top_positive_compartments", b.get("top_positive_compartments"))),
            "ms_wm_delta_log2": num(s.get("ms_wm_delta_log2", b.get("ms_wm_delta_log2"))),
            "ms_wm_p": num(s.get("ms_wm_p", b.get("ms_wm_p")), float("nan")),
            "ms_wm_fdr": num(s.get("ms_wm_fdr", b.get("ms_wm_fdr")), float("nan")),
            "opentargets_evidence_present": text(s.get("opentargets_evidence_present", b.get("opentargets_disease_count"))),
            "geneformer_contexts_with_token": num(s.get("contexts_with_token", gf.get("contexts_with_token"))),
            "geneformer_disease_cells_with_token": num(s.get("disease_cells_with_token", gf.get("disease_cells_with_token"))),
            "geneformer_support_contexts": num(s.get("support_contexts", gf.get("support_contexts"))),
            "geneformer_strong_support_contexts": num(s.get("strong_support_contexts", gf.get("strong_support_contexts"))),
            "geneformer_mean_cosine_z_vs_random": num(s.get("mean_cosine_z_vs_random", gf.get("mean_cosine_z_vs_random")), float("nan")),
            "geneformer_mean_projection_shift": num(s.get("mean_projection_shift", gf.get("mean_projection_shift")), float("nan")),
            "residual_raw_positive_disease_count": num(r.get("raw_positive_disease_count")),
            "residual_retained_positive_disease_count": num(r.get("retained_positive_disease_count")),
            "residual_non_ibd_retained_positive_disease_count": num(r.get("non_ibd_retained_positive_disease_count")),
            "strict_core_covariate_surviving_disease_count": num(r.get("strict_core_covariate_surviving_disease_count")),
            "strict_core_covariate_surviving_analyses": text(r.get("strict_core_covariate_surviving_analyses")),
            "residual_gate_priority_score": num(r.get("residual_gate_priority_score")),
            "focused_strict_core_covariate_surviving_analysis_count": num(fr.get("strict_core_covariate_surviving_analysis_count")),
            "focused_retained_positive_disease_count": num(fr.get("retained_positive_disease_count")),
        }
        rows.append(row)
    return pd.DataFrame(rows)


def residual_gate_call(row: pd.Series) -> str:
    strict = num(row.get("strict_core_covariate_surviving_disease_count"))
    retained = num(row.get("residual_retained_positive_disease_count"))
    broad_pos = num(row.get("positive_disease_count"))
    if strict >= 2:
        return "PASS_RESIDUAL_SPECIFICITY"
    if strict == 1:
        return "FAIL_SINGLE_STRICT_RESIDUAL_ONLY"
    if retained >= 2:
        return "FAIL_RETAINED_ONLY_NO_STRICT_CORE_SURVIVAL"
    if broad_pos >= 3:
        return "FAIL_EXPRESSION_RECURRENCE_ONLY"
    return "FAIL_LOCAL_RECURRENCE"


def geneformer_gate_call(row: pd.Series, annotation: GateAnnotation) -> str:
    support = num(row.get("geneformer_support_contexts"))
    strong = num(row.get("geneformer_strong_support_contexts"))
    if "public mouse" in annotation.perturbation_note.lower() and support >= 3:
        return "WEAK_MODEL_PLUS_PUBLIC_MOUSE_PRIOR_ART_NOT_V3_CAUSALITY"
    if "public tcr-nck" in annotation.perturbation_note.lower():
        return "PUBLIC_PERTURBATION_WRONG_CONTEXT_PRIOR_ART"
    if support >= 3 and strong >= 1:
        return "MODEL_ONLY_WEAK_NO_REAL_V3_PERTURBATION"
    if support >= 1:
        return "MODEL_WEAK_NO_REAL_V3_PERTURBATION"
    return "FAIL_NO_MODEL_OR_REAL_PERTURBATION"


def build_gate_matrix(local: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, row in local.iterrows():
        gene = row["gene"]
        ann = ANNOTATIONS[gene]
        rows.append(
            {
                **row.to_dict(),
                "biology_class": ann.biology_class,
                "gate1_recurrence_residual": residual_gate_call(row),
                "gate2_perturbation_or_model": geneformer_gate_call(row, ann),
                "gate3_explicit_intervention_direction": ann.direction,
                "gate4_modality_druggability": ann.modality,
                "gate5_safety_repair_risk": ann.safety_repair_risk,
                "gate6_prior_art_delta": ann.prior_art_delta,
                "wave20_call": ann.wave20_call,
                "least_bad_comparator_rank": ann.least_bad_rank,
                "wave20_rationale": ann.rationale,
            }
        )
    out = pd.DataFrame(rows)
    return out.sort_values(
        ["least_bad_comparator_rank", "positive_disease_count", "gene"],
        ascending=[True, False, True],
        na_position="last",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    survivor = read_tsv("results_v3/unrestricted_survivor_scan/unrestricted_survivor_candidates.tsv")
    genes = survivor["gene"].astype(str).tolist()
    missing = sorted(set(ANNOTATIONS) - set(genes) - {"SDC4"})
    if missing:
        raise ValueError(f"Annotated genes absent from candidate TSV: {missing}")

    local = build_local_evidence(genes)
    gate = build_gate_matrix(local)
    sources = pd.DataFrame(SOURCE_LINKS)

    local.to_csv(OUT / "wave20_local_evidence.tsv", sep="\t", index=False)
    gate.to_csv(OUT / "wave20_gate_matrix.tsv", sep="\t", index=False)
    sources.to_csv(OUT / "wave20_source_links.tsv", sep="\t", index=False)

    public_queries = pd.DataFrame(europepmc_search_rows())
    public_queries.to_csv(OUT / "wave20_public_search_queries.tsv", sep="\t", index=False)

    uniprot = pd.DataFrame(uniprot_rows(genes))
    uniprot.to_csv(OUT / "wave20_uniprot_druggability.tsv", sep="\t", index=False)

    chembl = pd.DataFrame(chembl_rows(genes))
    chembl.to_csv(OUT / "wave20_chembl_target_search.tsv", sep="\t", index=False)

    no_go_count = int((~gate["wave20_call"].astype(str).str.contains("COMPARATOR", na=False)).sum())
    summary = {
        "date": DATE,
        "n_candidates_from_unrestricted_survivor_tsv": int(len(genes)),
        "focus_genes": FOCUS_GENES,
        "candidate_genes": genes,
        "promoted_targets": [],
        "least_bad_comparator": "SNX10",
        "least_bad_reason": ANNOTATIONS["SNX10"].rationale,
        "calls": gate["wave20_call"].value_counts().to_dict(),
        "strict_core_residual_survivors": gate.loc[
            pd.to_numeric(gate["strict_core_covariate_surviving_disease_count"], errors="coerce").fillna(0) > 0,
            ["gene", "strict_core_covariate_surviving_disease_count", "strict_core_covariate_surviving_analyses"],
        ].to_dict(orient="records"),
        "no_go_or_marker_count": no_go_count,
        "guardrail": (
            "No candidate is promoted. Expression recurrence is treated as observational triage only; "
            "focused candidates are intracellular markers/stress-remodeling genes or prior-arted broad immune nodes."
        ),
        "outputs": [
            "wave20_local_evidence.tsv",
            "wave20_gate_matrix.tsv",
            "wave20_public_search_queries.tsv",
            "wave20_source_links.tsv",
            "wave20_uniprot_druggability.tsv",
            "wave20_chembl_target_search.tsv",
            "summary.json",
        ],
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
