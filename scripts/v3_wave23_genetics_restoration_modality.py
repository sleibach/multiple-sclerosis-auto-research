#!/usr/bin/env python3
"""Wave23 genetics-first restoration modality scout.

This worker reuses local V3 genetics, h5ad, perturbation, ChEMBL/UniProt, and
Wave20 public API cache outputs. The question is deliberately narrower than
Wave20: if the protective allele story points toward restoring a negative
regulator or endolysosomal/autophagy function, is there a current modality that
can restore that target selectively in the relevant disease compartment?
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results_v3" / "wave23_genetics_restoration_modality"

OT_CREDIBLE = ROOT / "tmp_v3" / "wave13_opentargets_gwas_credible_sets.tsv"
WAVE20 = ROOT / "results_v3" / "wave20_genetic_druggable_altaxis"
WAVE14_TRUTH = ROOT / "results_v3" / "wave14_target_level_genetics" / "target_level_genetics_truth_table.tsv"
BROAD_H5AD = ROOT / "results_v3" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_rank.tsv"
PERT_SYNTH = ROOT / "results_v3" / "wave15_perturbation_drug_response" / "candidate_level_synthesis.tsv"
LOCAL_CHEMBL = ROOT / "results_v3" / "druggability" / "chembl_target_activity_summary.tsv"
LOCAL_UNIPROT = ROOT / "results_v3" / "druggability" / "uniprot_target_summary.tsv"


CANDIDATES: dict[str, dict[str, Any]] = {
    "GPR65": {
        "scope": "prompt",
        "axis": "acidic tissue pH-sensing GPCR / cAMP brake",
        "restoration_direction": "agonize or positively modulate GPR65 if risk alleles reduce the anti-inflammatory pH/cAMP response",
        "allele_direction": "IBD-focused variant biology supports reduced GPR65 function as risk; local audit still lacks disease-by-cell coloc.",
        "target_tissue": "inflamed gut and acidic tissue myeloid/T-cell compartments; possible epithelial-adjacent immune niches",
        "current_feasible_modality": "selective small-molecule agonist/PAM is a feasible GPCR modality; ChEMBL and patents indicate chemistry exists.",
        "speculative_restoration": "biomarker-gated agonism in non-IBD autoimmune tissue or compartment-targeted exposure remains speculative.",
        "modality_precedent": "GPCR small molecules; GPR65 autoimmune/IBD modulator patent precedent.",
        "safety": "risk of broad immune suppression or tissue-pH biology effects; direction depends on preserving host defense and not amplifying maladaptive cAMP states.",
        "restoration_modality_score": 2.0,
        "target_selective_restoration": "partial",
        "hard_blocker": "current modality class is plausible, but local support is weak/contradictory and IBD/GPR65 prior art is already direct.",
        "needed_to_reopen": "fine-mapped non-IBD coloc plus selective agonist/PAM rescue in human disease myeloid or epithelial-immune systems.",
    },
    "IL10": {
        "scope": "prompt",
        "axis": "IL-10 regulatory cytokine tolerance",
        "restoration_direction": "increase IL-10 pathway signaling in the right inflammatory compartment",
        "allele_direction": "IL10 loss of function is immunoregulatory failure; common-locus direction is not target-resolved locally.",
        "target_tissue": "intestinal lamina propria, macrophage/DC/Treg circuits, and other inflamed tissue immune niches",
        "current_feasible_modality": "recombinant or engineered IL-10/IL10R agonism is feasible as a biologic modality.",
        "speculative_restoration": "compartment-targeted IL-10, matrix/fibronectin-targeted IL-10, or gene/cell-local IL-10 delivery is still not a validated cross-autoimmune route here.",
        "modality_precedent": "systemic recombinant IL-10 and localized/engineered IL-10 concepts have autoimmune/IBD precedent.",
        "safety": "systemic cytokine exposure can be nonselective; efficacy and dose-limiting immune effects are historical concerns.",
        "restoration_modality_score": 2.0,
        "target_selective_restoration": "partial",
        "hard_blocker": "restoration modality exists, but direct prior art and lack of local biomarker delta block a new V3 claim.",
        "needed_to_reopen": "localized IL-10 delivery with responder biomarker and human disease-cell rescue outside saturated IBD prior art.",
    },
    "PTPN2": {
        "scope": "prompt",
        "axis": "TCPTP cytokine/TCR and epithelial-barrier brake",
        "restoration_direction": "restore or increase TCPTP function; inhibition is directionally wrong for autoimmune genetics.",
        "allele_direction": "local Wave14 calls direction likely restoration; published biology links PTPN2 loss of function with inflammatory/autoimmune risk.",
        "target_tissue": "T cells, myeloid cells, intestinal epithelium/barrier tissue, thyroid/immune interfaces",
        "current_feasible_modality": "no target-selective TCPTP activator/restorer in local ChEMBL/Wave20 evidence; inhibitor chemistry is abundant but wrong direction.",
        "speculative_restoration": "mRNA, gene correction, allele repair, targeted protein stabilization, or pathway-bypass restoration.",
        "modality_precedent": "PTPN2/PTPN1 inhibitors and degraders for oncology, not autoimmune restoration.",
        "safety": "restoration would need cell-selective tuning; global PTPN2 manipulation touches cytokine signaling, TCR signaling, and barrier homeostasis.",
        "restoration_modality_score": 0.25,
        "target_selective_restoration": "no",
        "hard_blocker": "correct direction is restoration, but no current target-selective modality can restore TCPTP in the relevant compartments.",
        "needed_to_reopen": "true TCPTP activator/restorer or allele-correcting delivery plus human disease-cell rescue and coloc.",
    },
    "TNFAIP3": {
        "scope": "prompt",
        "axis": "A20 ubiquitin-editing NF-kappaB/TNF/TLR brake",
        "restoration_direction": "restore A20 function or mimic its negative-feedback complex.",
        "allele_direction": "human haploinsufficiency and locus biology point to insufficient A20/NF-kappaB braking; local GTEx panel lacked a usable cis-eQTL.",
        "target_tissue": "broad immune cells, epithelial/stromal inflammatory interfaces, keratinocytes and gut tissue depending on disease",
        "current_feasible_modality": "no direct A20 function-restoring small molecule or targeted biologic in local evidence.",
        "speculative_restoration": "gene replacement, mRNA, protein stabilization, E3/DUB complex modulation, or downstream NF-kappaB pathway mimicry.",
        "modality_precedent": "downstream anti-TNF/NF-kappaB pathway drugs exist, but they are not target-selective A20 restoration.",
        "safety": "A20 is broad and tumor-suppressor-adjacent in some contexts; systemic restoration or bypass could be hard to titrate.",
        "restoration_modality_score": 0.25,
        "target_selective_restoration": "no",
        "hard_blocker": "strong restoration biology but no current target-selective A20 restoration modality.",
        "needed_to_reopen": "selective A20 stabilizer/restorer with immune-cell target engagement and target-level genetic direction.",
    },
    "CLEC16A": {
        "scope": "prompt",
        "axis": "CLEC16A mitophagy/autophagy quality control",
        "restoration_direction": "restore CLEC16A-linked mitophagy/autophagy if risk alleles cause hypofunction.",
        "allele_direction": "direction is plausible hypofunction/restoration but not resolved locally; 16p13 locus is ambiguous with CIITA/DEXI/SOCS1.",
        "target_tissue": "immune cells, pancreatic beta-cell stress circuits, CNS/glial contexts, and tissue-specific endolysosomal quality control",
        "current_feasible_modality": "no selective direct CLEC16A drug; only broad indirect mitophagy/autophagy modulators.",
        "speculative_restoration": "cell-selective mitophagy tuning, targeted gene/mRNA replacement, or precise downstream pathway restoration.",
        "modality_precedent": "repurposed autophagy/mitophagy modulation concepts, not direct CLEC16A target engagement.",
        "safety": "broad autophagy modulation can affect survival, antigen handling, infection, and tissue stress responses.",
        "restoration_modality_score": 0.5,
        "target_selective_restoration": "no",
        "hard_blocker": "correct direction may be restoration, but current tools are indirect and not target-selective; locus causality is unresolved.",
        "needed_to_reopen": "fine mapping separating CLEC16A from neighboring genes plus selective CLEC16A/mitophagy rescue in disease-relevant cells.",
    },
    "ATG16L1": {
        "scope": "prompt",
        "axis": "autophagy/xenophagy epithelial-immune stress handling",
        "restoration_direction": "restore autophagy/xenophagy in hypomorphic risk-variant carriers.",
        "allele_direction": "ATG16L1 T300A/Crohn biology supports reduced autophagy function, but local cross-disease direction is not target-resolved.",
        "target_tissue": "intestinal epithelium/Paneth cells, macrophages, bacterial handling compartments, and gut immune niches",
        "current_feasible_modality": "no selective ATG16L1 restoration drug; pathway autophagy modulators are broad.",
        "speculative_restoration": "allele-specific correction, targeted protein stabilization, or compartment-selective autophagy enhancement.",
        "modality_precedent": "autophagy enhancers/repurposed pathway modulators, not ATG16L1-selective restoration.",
        "safety": "global autophagy enhancement or suppression has infection, cancer, epithelial stress, and immune-processing liabilities.",
        "restoration_modality_score": 0.5,
        "target_selective_restoration": "no",
        "hard_blocker": "restoration direction is plausible, but no current modality restores ATG16L1 selectively in gut/immune compartments.",
        "needed_to_reopen": "ATG16L1-selective target engagement or allele-correcting strategy plus gut/immune rescue data.",
    },
    "SH2B3": {
        "scope": "prompt",
        "axis": "LNK hematopoietic cytokine/JAK adaptor brake",
        "restoration_direction": "restore LNK/SH2B3 negative-regulatory adaptor function.",
        "allele_direction": "local genetics are broad, but 12q24 pleiotropy prevents a clean allele-to-target direction; restoration is the likely negative-regulator hypothesis.",
        "target_tissue": "hematopoietic stem/progenitor, T-cell, myeloid, platelet, and vascular-adjacent blood compartments",
        "current_feasible_modality": "no direct adaptor-function restoration modality.",
        "speculative_restoration": "gene editing/replacement, protein interaction stabilization, or downstream cytokine-pathway tuning.",
        "modality_precedent": "downstream JAK/cytokine inhibitors exist, but those do not restore LNK itself.",
        "safety": "hematopoietic, platelet, vascular, and cytokine pleiotropy make systemic restoration risky and hard to disease-target.",
        "restoration_modality_score": 0.25,
        "target_selective_restoration": "no",
        "hard_blocker": "broad genetics but no current target-selective restoration modality and substantial pleiotropy.",
        "needed_to_reopen": "target-resolved coloc/MR independent of 12q24 pleiotropy plus an LNK-restoring delivery concept.",
    },
    "CARD9": {
        "scope": "prompt",
        "axis": "CARD9 innate fungal/NF-kappaB adaptor",
        "restoration_direction": "not cleanly restoration; allele/context may require pathway normalization while preserving antifungal immunity.",
        "allele_direction": "local locus support is IBD/AS/psoriasis/UC-focused; CARD9 loss-of-function biology creates infectious risk, so restoration vs inhibition is not simple.",
        "target_tissue": "myeloid cells, gut innate immune/fungal sensing niches",
        "current_feasible_modality": "no direct CARD9-restoring or target-selective adaptor modality.",
        "speculative_restoration": "microbiome/fungal axis modulation or protein-interaction tuning.",
        "modality_precedent": "no local ChEMBL direct target evidence; infection genetics dominate safety thinking.",
        "safety": "antifungal immunity and innate NF-kappaB liabilities are central.",
        "restoration_modality_score": 0.0,
        "target_selective_restoration": "no",
        "hard_blocker": "direction is not a clean restoration hypothesis and no direct modality exists.",
        "needed_to_reopen": "allele-specific disease mechanism and selective myeloid pathway-normalization data.",
    },
    "IRF5": {
        "scope": "prompt",
        "axis": "TLR7/8/9-IRF5 inflammatory transcriptional switch",
        "restoration_direction": "not restoration; genetic and pharmacology precedent point to reducing IRF5 activation in IRF5/TLR-high disease.",
        "allele_direction": "broad locus evidence; plausible risk direction is increased IRF5 pathway activation, but local target-level coloc/MR is not completed.",
        "target_tissue": "monocytes, macrophages, dendritic cells, B cells, lupus/Sjogren-like IFN niches",
        "current_feasible_modality": "current inhibitor/degrader programs exist; they are inhibitors, not restoration modalities.",
        "speculative_restoration": "not applicable for this prompt except as pathway comparator.",
        "modality_precedent": "small-molecule allosteric inhibitors and degraders reported publicly in lupus-relevant systems.",
        "safety": "host defense and broad type-I-IFN/TLR biology risks; heavy lupus prior art.",
        "restoration_modality_score": 0.0,
        "target_selective_restoration": "not_applicable",
        "hard_blocker": "not a restoration target; inhibitor route is feasible but saturated and close to generic TLR/IFN biology.",
        "needed_to_reopen": "non-lupus biomarker population and freedom-to-operate beyond active IRF5 inhibitor/degrader programs.",
    },
    "IL6R": {
        "scope": "prompt",
        "axis": "IL-6 receptor inflammatory cytokine signaling",
        "restoration_direction": "not restoration; protective biology and approved drugs point to IL-6R blockade.",
        "allele_direction": "therapeutic genetic direction is blockade/reduced IL-6 signaling, not restoring a brake.",
        "target_tissue": "broad immune, liver/acute-phase, stromal and synovial inflammatory compartments",
        "current_feasible_modality": "approved anti-IL6R biologics are feasible but are inhibitors/blockers.",
        "speculative_restoration": "not applicable.",
        "modality_precedent": "tocilizumab/sarilumab class and biosimilars; autoimmune use is direct prior art.",
        "safety": "infection risk, lab monitoring, GI perforation and broad cytokine-blockade liabilities by class.",
        "restoration_modality_score": 0.0,
        "target_selective_restoration": "not_applicable",
        "hard_blocker": "feasible current modality is blockade, not restoration, and the autoimmune target class is fully prior-arted.",
        "needed_to_reopen": "not a restoration-first candidate unless a distinct genetically defined agonism story emerges.",
    },
    "TYK2": {
        "scope": "prompt",
        "axis": "TYK2 IL-12/23/type-I-IFN cytokine kinase",
        "restoration_direction": "not restoration; protective genetics and approved/clinical precedent support inhibition.",
        "allele_direction": "protective loss-of-function/inhibition logic is established externally; local Wave20 treated it as generic JAK/IFN comparator.",
        "target_tissue": "hematopoietic cytokine signaling across T cells, myeloid cells, dendritic cells, and skin/gut immune niches",
        "current_feasible_modality": "approved/clinical allosteric and ATP-competitive inhibitors.",
        "speculative_restoration": "not applicable.",
        "modality_precedent": "deucravacitinib and other TYK2 inhibitor programs.",
        "safety": "infection, malignancy/lab-monitoring concerns by cytokine-kinase class; broad JAK/IFN route.",
        "restoration_modality_score": 0.0,
        "target_selective_restoration": "not_applicable",
        "hard_blocker": "not a restoration target and explicitly excluded as generic JAK/IFN without a new modality/population delta.",
        "needed_to_reopen": "no restoration reopen; only a new biomarker-defined TYK2 inhibitor delta could be separately reviewed.",
    },
    "OSMR": {
        "scope": "local_addition_wave20",
        "axis": "OSM/OSMR tissue inflammatory remodeling comparator",
        "restoration_direction": "not restoration; if anything the current modality concept is OSM/OSMR blockade.",
        "allele_direction": "local OT support reaches four diseases but is locus-level and not directionally resolved for restoration.",
        "target_tissue": "stromal, epithelial, fibroblast-like and tissue-remodeling inflammatory compartments",
        "current_feasible_modality": "anti-OSM/anti-OSMR biologic concept is feasible but inhibitory.",
        "speculative_restoration": "not applicable.",
        "modality_precedent": "OSM/OSMR inflammatory tissue remodeling literature and biologic concepts.",
        "safety": "tissue repair/remodeling biology and disease-specific direction risks.",
        "restoration_modality_score": 0.0,
        "target_selective_restoration": "not_applicable",
        "hard_blocker": "locally justified comparator, but not a restoration target and previously demoted as IBD/tissue-remodeling prior art.",
        "needed_to_reopen": "separate blockade-focused biomarker delta; not this restoration scout.",
    },
    "SLC15A4": {
        "scope": "local_addition_endolysosomal",
        "axis": "endolysosomal TLR/SLC15A4-TASL pathway",
        "restoration_direction": "not restoration; therapeutic concept is inhibition of the TLR7/8/9-IRF5 branch.",
        "allele_direction": "local genetics are SLE-heavy and limited; direction does not support broad restoration.",
        "target_tissue": "pDC, B-cell and myeloid endolysosomal TLR compartments",
        "current_feasible_modality": "SLC15A4 inhibitor chemistry exists publicly, but that is not restoration.",
        "speculative_restoration": "not applicable.",
        "modality_precedent": "chemoproteomic SLC15A4 inhibitor prior art and lupus/TLR pathway saturation.",
        "safety": "endolysosomal innate immune suppression and host-defense risk.",
        "restoration_modality_score": 0.0,
        "target_selective_restoration": "not_applicable",
        "hard_blocker": "local endolysosomal comparator, but correct pharmacology is inhibition and genetics breadth is limited.",
        "needed_to_reopen": "not a restoration candidate; only inhibitor novelty could be reviewed separately.",
    },
    "TASL": {
        "scope": "local_addition_endolysosomal",
        "axis": "SLC15A4 adaptor / CXorf21-TASL endolysosomal TLR pathway",
        "restoration_direction": "not restoration; pathway concept is dampening TASL-dependent TLR/IRF signaling.",
        "allele_direction": "local locus evidence is RA/SLE only and X-linked/sparse; no restoration direction.",
        "target_tissue": "pDC, B-cell and myeloid endolysosomal TLR compartments",
        "current_feasible_modality": "no direct TASL restoration modality; pathway inhibition would be the relevant comparator.",
        "speculative_restoration": "not applicable.",
        "modality_precedent": "SLC15A4/TASL lupus/TLR biology prior art.",
        "safety": "host-defense and innate immune suppression liabilities if inhibited; no restoration rationale.",
        "restoration_modality_score": 0.0,
        "target_selective_restoration": "not_applicable",
        "hard_blocker": "locally justified endolysosomal comparator, but not a restoration target and genetics breadth is limited.",
        "needed_to_reopen": "not a restoration candidate.",
    },
}


PUBLIC_SOURCE_NOTES = [
    {
        "gene": "GPR65",
        "source": "GPR65 experimental colitis and target rationale",
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC8629932/",
        "use": "Shows GPR65 is already framed as an IBD intervention target; supports feasibility and prior-art crowding.",
    },
    {
        "gene": "GPR65",
        "source": "WO2023067322A1 GPR65 modulators",
        "url": "https://patents.google.com/patent/WO2023067322A1/en",
        "use": "Patent precedent for GPR65 modulators with autoimmune disease language.",
    },
    {
        "gene": "PTPN2",
        "source": "PTPN2 loss-of-function and autoimmunity review",
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC9456094/",
        "use": "Supports restoration direction for autoimmune genetics.",
    },
    {
        "gene": "PTPN2",
        "source": "PTPN2/PTPN1 inhibitor oncology precedent",
        "url": "https://www.nature.com/articles/s41586-023-06575-7",
        "use": "Demonstrates strong inhibitor precedent, which is wrong-direction for autoimmune restoration.",
    },
    {
        "gene": "TNFAIP3",
        "source": "A20 haploinsufficiency GeneReviews",
        "url": "https://www.ncbi.nlm.nih.gov/sites/books/NBK610430/",
        "use": "Supports insufficient A20 function as an inflammatory disease mechanism.",
    },
    {
        "gene": "CLEC16A",
        "source": "CLEC16A autoimmunity/mitophagy review",
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC10179542/",
        "use": "Supports mitophagy restoration concept but mostly via indirect repurposing logic.",
    },
    {
        "gene": "IRF5",
        "source": "HotSpot Therapeutics IRF5 inhibitor program",
        "url": "https://www.hotspotthera.com/press_release/hotspot-therapeutics-presents-preclinical-data-from-small-molecule-irf5-inhibitor-program-at-15th-european-lupus-meeting/",
        "use": "Current inhibitor modality precedent; not restoration.",
    },
    {
        "gene": "IRF5",
        "source": "Kymera KT-579 IRF5 degrader public material",
        "url": "https://investors.kymeratx.com/node/11946/pdf",
        "use": "Current degrader modality precedent and prior-art crowding.",
    },
    {
        "gene": "IL10",
        "source": "Recombinant human IL-10 Crohn trial",
        "url": "https://pubmed.ncbi.nlm.nih.gov/11113068/",
        "use": "Direct IL-10 restoration therapy precedent in IBD.",
    },
    {
        "gene": "IL6R",
        "source": "ACTEMRA prescribing information",
        "url": "https://www.accessdata.fda.gov/drugsatfda_docs/label/2024/125276s144%2C125472s056lbl.pdf",
        "use": "Approved IL-6 receptor antagonist precedent; blockade, not restoration.",
    },
    {
        "gene": "TYK2",
        "source": "FDA SOTYKTU drug trial snapshot",
        "url": "https://www.fda.gov/drugs/drug-approvals-and-databases/drug-trials-snapshots-sotyktu",
        "use": "Approved TYK2 inhibitor precedent; inhibition, not restoration.",
    },
]


def read_tsv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path, sep="\t", low_memory=False)


def safe_num(value: Any, default: float = 0.0) -> float:
    try:
        if value is None or pd.isna(value):
            return default
        return float(value)
    except Exception:
        return default


def safe_int(value: Any) -> int:
    return int(round(safe_num(value, 0.0)))


def clean_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float) and math.isnan(value):
        return ""
    if pd.isna(value):
        return ""
    return str(value)


def first_record(df: pd.DataFrame, gene: str, col: str = "gene") -> dict[str, Any]:
    if df.empty or col not in df.columns:
        return {}
    sub = df[df[col].astype(str).eq(gene)]
    if sub.empty:
        return {}
    return sub.iloc[0].to_dict()


def ot_summary_from_credible() -> pd.DataFrame:
    if not OT_CREDIBLE.exists():
        return pd.DataFrame(columns=["gene"])
    df = read_tsv(OT_CREDIBLE)
    rows = []
    for gene in sorted(CANDIDATES):
        sub = df[df["query_gene"].astype(str).eq(gene)] if "query_gene" in df.columns else pd.DataFrame()
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
        ge05 = sub[sub["max_score"].fillna(0) >= 0.5]
        ge08 = sub[sub["max_score"].fillna(0) >= 0.8]
        rows.append(
            {
                "gene": gene,
                "ot_n_diseases_score_ge_0_5": ge05["disease"].nunique(),
                "ot_diseases_score_ge_0_5": ";".join(sorted(ge05["disease"].dropna().astype(str).unique())),
                "ot_n_diseases_score_ge_0_8": ge08["disease"].nunique(),
                "ot_diseases_score_ge_0_8": ";".join(sorted(ge08["disease"].dropna().astype(str).unique())),
                "ot_max_score": safe_num(sub["max_score"].max()),
                "ot_evidence_count_sum": safe_int(sub["evidence_count"].sum()),
            }
        )
    return pd.DataFrame(rows)


def build_evidence_matrix() -> pd.DataFrame:
    wave20_ot = read_tsv(WAVE20 / "local_opentargets_genetics_summary.tsv")
    if wave20_ot.empty:
        wave20_ot = ot_summary_from_credible()
    else:
        supplemental_ot = ot_summary_from_credible()
        wave20_genes = set(wave20_ot["gene"].astype(str))
        wave20_ot = pd.concat(
            [wave20_ot, supplemental_ot[~supplemental_ot["gene"].astype(str).isin(wave20_genes)]],
            ignore_index=True,
        )

    wave20_local = read_tsv(WAVE20 / "local_biology_and_druggability_metrics.tsv")
    wave20_rank = read_tsv(WAVE20 / "negative_ranked_shortlist.tsv")
    wave20_public = read_tsv(WAVE20 / "public_api_prior_art_druggability_audit.tsv")
    truth = read_tsv(WAVE14_TRUTH)
    broad = read_tsv(BROAD_H5AD)
    pert = read_tsv(PERT_SYNTH)
    chembl = read_tsv(LOCAL_CHEMBL)
    uniprot = read_tsv(LOCAL_UNIPROT)

    rows = []
    for gene, meta in CANDIDATES.items():
        ot = first_record(wave20_ot, gene)
        local = first_record(wave20_local, gene)
        rank = first_record(wave20_rank, gene)
        pub = first_record(wave20_public, gene)
        truth_row = first_record(truth, gene)
        broad_row = first_record(broad, gene)
        pert_row = first_record(pert, gene, col="candidate")
        chembl_sub = chembl[chembl["gene"].astype(str).eq(gene)] if not chembl.empty and "gene" in chembl.columns else pd.DataFrame()
        uniprot_row = first_record(uniprot, gene)

        if not local and broad_row:
            local = {
                "broad_positive_disease_count": broad_row.get("positive_disease_count", 0),
                "broad_negative_disease_count": broad_row.get("negative_disease_count", 0),
                "broad_positive_diseases": broad_row.get("positive_diseases", ""),
                "broad_negative_diseases": broad_row.get("negative_diseases", ""),
                "ms_wm_delta_log2": broad_row.get("ms_wm_delta_log2", ""),
                "ms_wm_p": broad_row.get("ms_wm_p", ""),
                "discovery_priority_score": broad_row.get("discovery_priority_score", 0),
            }

        local_chembl_count = 0
        local_chembl_best = ""
        if not chembl_sub.empty:
            local_chembl_count = safe_int(chembl_sub["activity_values_nM_count"].fillna(0).max())
            local_chembl_best = safe_num(chembl_sub["best_standard_value_nM"].min(), float("nan"))

        perturbation_note = "no direct local perturbation row"
        if pert_row:
            perturbation_note = (
                f"{clean_text(pert_row.get('sources'))}: "
                f"{clean_text(pert_row.get('direct_evidence_calls'))}; "
                f"selectivity={safe_num(pert_row.get('best_direct_selectivity_score'), float('nan')):.3g}"
            )
        elif rank:
            perturbation_note = f"Wave20 manual perturbation score {safe_num(rank.get('perturbation_score_manual')):.1f}"

        target_level_call = clean_text(truth_row.get("target_level_genetics_dod_call")) or clean_text(rank.get("target_level_signal"))
        coloc_blocker = clean_text(truth_row.get("coloc_mr_blocker")) or clean_text(rank.get("manual_target_level_note"))

        rows.append(
            {
                "gene": gene,
                "scope": meta["scope"],
                "axis": meta["axis"],
                "ot_n_diseases_score_ge_0_5": safe_int(ot.get("ot_n_diseases_score_ge_0_5")),
                "ot_diseases_score_ge_0_5": clean_text(ot.get("ot_diseases_score_ge_0_5")),
                "ot_n_diseases_score_ge_0_8": safe_int(ot.get("ot_n_diseases_score_ge_0_8")),
                "ot_diseases_score_ge_0_8": clean_text(ot.get("ot_diseases_score_ge_0_8")),
                "ot_max_score": safe_num(ot.get("ot_max_score")),
                "target_level_genetics_call": target_level_call,
                "coloc_mr_blocker": coloc_blocker,
                "allele_direction": meta["allele_direction"],
                "target_tissue": meta["target_tissue"],
                "broad_positive_disease_count": safe_int(local.get("broad_positive_disease_count")),
                "broad_positive_diseases": clean_text(local.get("broad_positive_diseases")),
                "broad_negative_disease_count": safe_int(local.get("broad_negative_disease_count")),
                "broad_negative_diseases": clean_text(local.get("broad_negative_diseases")),
                "ms_wm_delta_log2": safe_num(local.get("ms_wm_delta_log2"), float("nan")),
                "perturbation_evidence": perturbation_note,
                "wave20_prior_gate": clean_text(rank.get("promotion_gate")),
                "wave20_gate_failures": clean_text(rank.get("gate_failures")),
                "europepmc_hit_count": safe_int(pub.get("europepmc_hit_count")),
                "clinicaltrials_hit_count": safe_int(pub.get("clinicaltrials_hit_count")),
                "public_chembl_activity_records": safe_int(pub.get("chembl_activity_records")),
                "local_chembl_activity_values_nM_count": local_chembl_count,
                "local_chembl_best_standard_value_nM": local_chembl_best,
                "uniprot_accession": clean_text(uniprot_row.get("accession")),
                "current_feasible_modality": meta["current_feasible_modality"],
                "speculative_restoration": meta["speculative_restoration"],
                "modality_precedent": meta["modality_precedent"],
                "target_selective_restoration": meta["target_selective_restoration"],
                "restoration_direction": meta["restoration_direction"],
                "restoration_modality_score": meta["restoration_modality_score"],
                "safety": meta["safety"],
                "hard_blocker": meta["hard_blocker"],
                "needed_to_reopen": meta["needed_to_reopen"],
            }
        )
    return pd.DataFrame(rows)


def call_candidates(evidence: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for record in evidence.to_dict(orient="records"):
        gene = record["gene"]
        genetics_score = min(3.0, safe_num(record["ot_n_diseases_score_ge_0_5"]) / 3.0)
        local_score = min(1.5, safe_num(record["broad_positive_disease_count"]) * 0.4) - min(
            1.0, safe_num(record["broad_negative_disease_count"]) * 0.4
        )
        modality_score = safe_num(record["restoration_modality_score"])
        prior_penalty = 0.0
        if safe_num(record["clinicaltrials_hit_count"]) > 0:
            prior_penalty += 0.75
        if safe_num(record["europepmc_hit_count"]) >= 500:
            prior_penalty += 0.5
        if safe_num(record["europepmc_hit_count"]) >= 2000:
            prior_penalty += 0.5

        target_selective = record["target_selective_restoration"]
        restoration_applicable = target_selective not in {"not_applicable"}
        if target_selective == "no":
            call = "NO_GO"
        elif target_selective == "not_applicable":
            call = "NO_GO"
        elif target_selective == "partial":
            call = "PARK"
        else:
            call = "PARK"

        score = genetics_score + local_score + modality_score - prior_penalty
        if call == "NO_GO":
            score -= 2.0
        if gene in {"GPR65", "IL10"}:
            score += 0.25
        if gene in {"IL6R", "TYK2", "IRF5"}:
            score -= 1.0

        if call == "PARK":
            decision_reason = record["hard_blocker"]
        elif not restoration_applicable:
            decision_reason = "Not a restoration-first target in this scout: " + record["hard_blocker"]
        else:
            decision_reason = record["hard_blocker"]

        rows.append(
            {
                "gene": gene,
                "rank_score": round(score, 3),
                "call": call,
                "axis": record["axis"],
                "scope": record["scope"],
                "genetic_anchor": f"{record['ot_n_diseases_score_ge_0_5']} OT diseases >=0.5: {record['ot_diseases_score_ge_0_5']}",
                "target_level_status": record["target_level_genetics_call"] or "locus-level/local-only",
                "restoration_direction": record["restoration_direction"],
                "current_feasible_modality": record["current_feasible_modality"],
                "speculative_restoration": record["speculative_restoration"],
                "target_tissue": record["target_tissue"],
                "perturbation_evidence": record["perturbation_evidence"],
                "prior_art_signal": f"EuropePMC={record['europepmc_hit_count']}; ClinicalTrials={record['clinicaltrials_hit_count']}; ChEMBL_API={record['public_chembl_activity_records']}",
                "safety": record["safety"],
                "decision_reason": decision_reason,
                "needed_to_reopen": record["needed_to_reopen"],
            }
        )
    ranked = pd.DataFrame(rows)
    call_order = {"PARK": 0, "NO_GO": 1}
    ranked["call_order"] = ranked["call"].map(call_order).fillna(9)
    ranked = ranked.sort_values(["call_order", "rank_score", "gene"], ascending=[True, False, True]).drop(columns=["call_order"])
    ranked.insert(0, "rank", range(1, len(ranked) + 1))
    return ranked


def build_summary(evidence: pd.DataFrame, ranked: pd.DataFrame) -> dict[str, Any]:
    return {
        "date": "2026-05-27",
        "scope": "genetics-first restoration modality scout; not a final therapeutic finding",
        "candidate_count": int(len(ranked)),
        "calls": ranked["call"].value_counts().to_dict(),
        "parked": ranked.loc[ranked["call"].eq("PARK"), "gene"].tolist(),
        "no_go": ranked.loc[ranked["call"].eq("NO_GO"), "gene"].tolist(),
        "go": ranked.loc[ranked["call"].eq("GO"), "gene"].tolist() if "GO" in set(ranked["call"]) else [],
        "local_inputs": [
            str(OT_CREDIBLE.relative_to(ROOT)),
            str(WAVE20.relative_to(ROOT)),
            str(WAVE14_TRUTH.relative_to(ROOT)),
            str(BROAD_H5AD.relative_to(ROOT)),
            str(PERT_SYNTH.relative_to(ROOT)),
            str(LOCAL_CHEMBL.relative_to(ROOT)),
            str(LOCAL_UNIPROT.relative_to(ROOT)),
        ],
        "interpretation": (
            "No candidate is promoted. GPR65 and IL10 are PARK because a current modality class can in principle "
            "increase pathway activity, but both remain blocked by prior art/local evidence gaps. All other candidates "
            "are NO_GO for restoration because the correct direction is not restoration or no current target-selective "
            "restoration modality can reach the relevant immune/tissue compartments."
        ),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    evidence = build_evidence_matrix()
    ranked = call_candidates(evidence)
    sources = pd.DataFrame(PUBLIC_SOURCE_NOTES)
    summary = build_summary(evidence, ranked)

    evidence.to_csv(OUT / "local_restoration_evidence_matrix.tsv", sep="\t", index=False)
    ranked.to_csv(OUT / "ranked_go_park_no_go.tsv", sep="\t", index=False)
    sources.to_csv(OUT / "public_source_interpretation.tsv", sep="\t", index=False)
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")

    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
