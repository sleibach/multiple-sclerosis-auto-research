#!/usr/bin/env python3
"""Wave19 lysosomal/lipid-controller audit.

This script is intentionally table-first: it only reads existing V3 outputs and
emits a reproducible local evidence merge plus curated source/decision tables
for the lysosomal stress and lipid-handling controller panel.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "phases/v3/results" / "wave19_lysosomal_controller"


CANDIDATES = [
    # CLEAR/lysosomal stress controllers
    {"gene": "TFEB", "route": "TFEB_TFE3_CLEAR_activation", "class": "CLEAR transcription factor"},
    {"gene": "TFE3", "route": "TFEB_TFE3_CLEAR_activation", "class": "CLEAR transcription factor"},
    {"gene": "MCOLN1", "route": "MCOLN1_TRPML1_activation", "class": "lysosomal calcium channel"},
    {"gene": "PIKFYVE", "route": "PIKFYVE_inhibition", "class": "endolysosomal lipid kinase"},
    {"gene": "MTOR", "route": "mTOR_autophagy_modulation", "class": "mTOR/autophagy regulator"},
    {"gene": "TSC1", "route": "mTOR_autophagy_modulation", "class": "mTOR/autophagy regulator"},
    {"gene": "TSC2", "route": "mTOR_autophagy_modulation", "class": "mTOR/autophagy regulator"},
    {"gene": "RPTOR", "route": "mTOR_autophagy_modulation", "class": "mTOR/autophagy regulator"},
    {"gene": "RHEB", "route": "mTOR_autophagy_modulation", "class": "mTOR/autophagy regulator"},
    {"gene": "ULK1", "route": "mTOR_autophagy_modulation", "class": "mTOR/autophagy regulator"},
    {"gene": "BECN1", "route": "mTOR_autophagy_modulation", "class": "mTOR/autophagy regulator"},
    {"gene": "ATG5", "route": "mTOR_autophagy_modulation", "class": "mTOR/autophagy regulator"},
    {"gene": "ATG7", "route": "mTOR_autophagy_modulation", "class": "mTOR/autophagy regulator"},
    {"gene": "SQSTM1", "route": "mTOR_autophagy_modulation", "class": "mTOR/autophagy regulator"},
    # Lysosomal lipid handling
    {"gene": "LIPA", "route": "LIPA_LAL_enhancement", "class": "lysosomal neutral-lipid hydrolase"},
    {"gene": "NPC1", "route": "NPC1_NPC2_cholesterol_egress", "class": "lysosomal cholesterol transporter"},
    {"gene": "NPC2", "route": "NPC1_NPC2_cholesterol_egress", "class": "lysosomal cholesterol transporter"},
    {"gene": "GBA", "route": "GBA_GBA2_sphingolipid_modulation", "class": "lysosomal sphingolipid enzyme"},
    {"gene": "GBA2", "route": "GBA_GBA2_sphingolipid_modulation", "class": "non-lysosomal sphingolipid enzyme"},
    {"gene": "LRRK2", "route": "LRRK2_inhibition", "class": "lysosomal/vesicle kinase"},
    {"gene": "PPARG", "route": "PPAR_LXR_cholesterol_efflux_activation", "class": "lipid nuclear receptor"},
    {"gene": "NR1H3", "route": "PPAR_LXR_cholesterol_efflux_activation", "class": "lipid nuclear receptor"},
    {"gene": "NR1H2", "route": "PPAR_LXR_cholesterol_efflux_activation", "class": "lipid nuclear receptor"},
    {"gene": "ABCA1", "route": "PPAR_LXR_cholesterol_efflux_activation", "class": "cholesterol efflux transporter"},
    {"gene": "ABCG1", "route": "PPAR_LXR_cholesterol_efflux_activation", "class": "cholesterol efflux transporter"},
    # Local positive/negative lysosomal APC controls
    {"gene": "CTSH", "route": "cathepsin_IFI30_local_controls", "class": "lysosomal protease control"},
    {"gene": "CTSS", "route": "cathepsin_IFI30_local_controls", "class": "lysosomal protease control"},
    {"gene": "CTSB", "route": "cathepsin_IFI30_local_controls", "class": "lysosomal protease control"},
    {"gene": "CTSD", "route": "cathepsin_IFI30_local_controls", "class": "lysosomal protease control"},
    {"gene": "IFI30", "route": "cathepsin_IFI30_local_controls", "class": "lysosomal antigen-processing control"},
    {"gene": "LAMP1", "route": "lysosomal_membrane_controls", "class": "lysosomal membrane control"},
    {"gene": "LAMP2", "route": "lysosomal_membrane_controls", "class": "lysosomal membrane control"},
    # Extra trafficking comparators that had V3 local coverage.
    {"gene": "SNX10", "route": "endolysosomal_trafficking_comparators", "class": "endolysosomal trafficking comparator"},
    {"gene": "VPS35", "route": "endolysosomal_trafficking_comparators", "class": "endolysosomal trafficking comparator"},
    {"gene": "RAB5A", "route": "endolysosomal_trafficking_comparators", "class": "endolysosomal trafficking comparator"},
]


EXTERNAL_ROUTES = [
    {
        "route": "LIPA_LAL_enhancement",
        "genes": "LIPA",
        "therapeutic_direction": "Enhance/replace LAL activity; do not inhibit.",
        "plausible_modality": "IV enzyme replacement is real for LAL deficiency; autoimmune use would need tissue/cell-targeted enzyme, mRNA/LNP, AAV, or indirect lipid-mobilization rather than chronic LAL inhibition.",
        "independent_evidence_channel": "Human LAL deficiency and Lipa mouse work establish lipid-loaded macrophage/inflammatory phenotypes; local V3 LIPA residual signals persist in T1D ductal cells and psoriasis keratinocytes, but myeloid compartments are contradictory.",
        "chemical_or_modality_matter": "Approved sebelipase alfa/Kanuma; LAL inhibitors are assay tools and are directionally wrong for this hypothesis.",
        "delivery_feasibility": "Peripheral reticuloendothelial delivery is feasible; CNS microglia and epithelial/keratinocyte target engagement remain unproven.",
        "autoimmune_prior_art": "No direct autoimmune LAL augmentation trial found in checked query terms, but a 2026 white-matter repair/remyelination LAL paper crowds the MS repair claim.",
        "blocking_issue": "Local cross-disease state support is confounder-heavy and not myeloid-stable; CNS delivery and MS repair prior art block a GO call.",
        "route_call": "PARK",
        "source_ids": "S_LIPA_UNIPROT;S_LIPA_GENEREVIEWS;S_LIPA_MACROPHAGE;S_LIPA_EFFEROCYTOSIS;S_LIPA_CHEMBL;S_LIPA_FDA;S_LIPA_MS_REPAIR",
        "query_terms": '"LIPA" "multiple sclerosis"; "lysosomal acid lipase" autoimmune; "sebelipase alfa" autoimmune',
    },
    {
        "route": "MCOLN1_TRPML1_activation",
        "genes": "MCOLN1",
        "therapeutic_direction": "Activate TRPML1/CLEAR flux if used as a tool.",
        "plausible_modality": "Small-molecule TRPML agonism exists preclinically.",
        "independent_evidence_channel": "TRPML1-mediated lysosomal calcium activates calcineurin/TFEB and autophagy/lysosomal biogenesis.",
        "chemical_or_modality_matter": "ML-SA1 and related TRPML agonists are tool compounds; no clinical autoimmune-grade package found.",
        "delivery_feasibility": "Small molecules may be feasible in principle, but CNS and tissue APC target engagement are not established.",
        "autoimmune_prior_art": "Little direct autoimmune prior art found, which is whitespace by absence rather than validation.",
        "blocking_issue": "Local V3 broad h5ad signal is negative/absent for MCOLN1; no cross-disease state coupling table supports it.",
        "route_call": "NO_GO_TOOL_ONLY",
        "source_ids": "S_TFEB_TRPML1;S_MLSA1",
        "query_terms": '"TRPML1" TFEB calcineurin; "ML-SA1" TRPML1 agonist autoimmune',
    },
    {
        "route": "TFEB_TFE3_CLEAR_activation",
        "genes": "TFEB;TFE3",
        "therapeutic_direction": "Activate lysosomal biogenesis/CLEAR only if a selective tissue route exists.",
        "plausible_modality": "Mostly indirect and broad routes: mTOR inhibition, calcium/calcineurin, stress-response modulators, gene therapy concepts.",
        "independent_evidence_channel": "TFEB is a master CLEAR/lysosomal biogenesis and autophagy regulator.",
        "chemical_or_modality_matter": "No clean, target-selective clinical TFEB/TFE3 activator package for autoimmune APCs.",
        "delivery_feasibility": "Systemic activation risks broad autophagy/metabolism effects; CNS delivery would be an additional barrier.",
        "autoimmune_prior_art": "Autophagy/lysosome activation is broad and crowded; no specific cross-autoimmune HLA-II/APC controller evidence found.",
        "blocking_issue": "Local TFEB/TFE3 expression is not recurrently positive; both have negative broad h5ad disease calls.",
        "route_call": "NO_GO",
        "source_ids": "S_TFEB_CLEAR;S_TFEB_AUTOPHAGY;S_TFEB_MTOR",
        "query_terms": '"TFEB" "lysosomal biogenesis" autoimmune; "TFE3" lysosome autoimmune',
    },
    {
        "route": "PIKFYVE_inhibition",
        "genes": "PIKFYVE",
        "therapeutic_direction": "Inhibit PIKFYVE only for IL-12/23/TLR suppression; this is not a lysosomal-rescue direction.",
        "plausible_modality": "Small molecules exist; apilimod is the main clinical precedent.",
        "independent_evidence_channel": "Apilimod/PIKFYVE inhibition suppresses IL-12/23 production but directly perturbs endolysosomal phosphoinositide trafficking.",
        "chemical_or_modality_matter": "Apilimod reached inflammatory disease trials; PIKFYVE inhibition also causes lysosomal vacuolation/endolysosomal disruption.",
        "delivery_feasibility": "Systemic small molecule feasible; CNS feasibility is irrelevant unless toxicity/selectivity are solved.",
        "autoimmune_prior_art": "Crohn disease, psoriasis, and rheumatoid arthritis prior art/trials make the autoimmune anti-inflammatory claim crowded.",
        "blocking_issue": "Wrong direction for restoring lipid-lysosomal/APC homeostasis and too broad/toxic for chronic shared-autoimmune modulation.",
        "route_call": "NO_GO",
        "source_ids": "S_PIKFYVE_APILIMOD_IL12;S_PIKFYVE_CROHN_TRIAL;S_PIKFYVE_CHRONIC_TOX",
        "query_terms": '"apilimod" Crohn disease; "PIKfyve inhibitor" autoimmune; "apilimod" IL-12 IL-23',
    },
    {
        "route": "NPC1_NPC2_cholesterol_egress",
        "genes": "NPC1;NPC2",
        "therapeutic_direction": "Enhance lysosomal cholesterol egress/functional rescue, not inhibit.",
        "plausible_modality": "Cyclodextrin-like lipid mobilization, chaperone/proteostasis, or gene/enzyme-like disease-modifying approaches.",
        "independent_evidence_channel": "NPC1/NPC2 disease biology establishes lysosomal cholesterol trafficking and CNS relevance.",
        "chemical_or_modality_matter": "Hydroxypropyl-beta-cyclodextrin and NPC disease therapeutics create modality precedents, but not selective autoimmune APC intervention.",
        "delivery_feasibility": "CNS delivery has required invasive/high-burden approaches in NPC programs; peripheral APC delivery is plausible but unvalidated.",
        "autoimmune_prior_art": "No direct cross-autoimmune NPC1/NPC2 intervention prior art found in checked terms.",
        "blocking_issue": "NPC1/NPC2 local state coupling is confounder-dominant and lacks a selective activation drug package.",
        "route_call": "PARK_READOUT",
        "source_ids": "S_NPC_GENEREVIEWS;S_NPC_HPBCD_TRIAL",
        "query_terms": '"NPC1" autoimmune; "NPC2" antigen presentation autoimmune; "hydroxypropyl-beta-cyclodextrin" Niemann-Pick type C trial',
    },
    {
        "route": "GBA_GBA2_sphingolipid_modulation",
        "genes": "GBA;GBA2",
        "therapeutic_direction": "Enhance GBA or selectively rebalance glycosphingolipid handling; avoid nonspecific sphingolipid disruption.",
        "plausible_modality": "Gaucher ERT/substrate-reduction and ambroxol chaperone precedent, but not an autoimmune APC strategy.",
        "independent_evidence_channel": "GBA disease/Parkinson biology validates lysosomal glucocerebrosidase as a druggable enzyme axis.",
        "chemical_or_modality_matter": "Imiglucerase/velaglucerase/taliglucerase and ambroxol-like chaperone work exist; GBA2 inhibitor biology is less autoimmune-directed.",
        "delivery_feasibility": "ERT is peripheral and poor for CNS; oral chaperone CNS exposure is possible but autoimmune target engagement is absent.",
        "autoimmune_prior_art": "No compelling direct MS/RA/SLE/IBD shared-autoimmune intervention art found; also little local support.",
        "blocking_issue": "Local V3 recurrence is absent or negative for GBA/GBA2.",
        "route_call": "NO_GO",
        "source_ids": "S_GBA_AMBROXOL;S_GBA_GAUCHER_FDA",
        "query_terms": '"GBA" autoimmune; "glucocerebrosidase" multiple sclerosis; "GBA2" autoimmune',
    },
    {
        "route": "LRRK2_inhibition",
        "genes": "LRRK2",
        "therapeutic_direction": "Inhibit LRRK2 kinase if pursuing Crohn/myeloid-lysosome biology.",
        "plausible_modality": "Oral CNS-penetrant kinase inhibitors are in Parkinson programs.",
        "independent_evidence_channel": "LRRK2 functional variants link Crohn disease and Parkinson disease risk; LRRK2 is tied to lysosomal/vesicular immune biology.",
        "chemical_or_modality_matter": "Clinical kinase inhibitor matter exists, including BIIB122/DNL151-class programs.",
        "delivery_feasibility": "CNS delivery is plausible; chronic peripheral immune target engagement and safety remain concerns.",
        "autoimmune_prior_art": "Crohn/LRRK2 genetics and IBD biology are crowded; cross-autoimmune breadth is not established.",
        "blocking_issue": "Local support is IBD-skewed and lacks residual HLA-II/APC state coupling in Wave15 tables.",
        "route_call": "PARK_DISEASE_SPECIFIC",
        "source_ids": "S_LRRK2_CROHN_PD;S_LRRK2_CT",
        "query_terms": '"LRRK2" Crohn disease autoimmune; "LRRK2 inhibitor" ClinicalTrials.gov',
    },
    {
        "route": "PPAR_LXR_cholesterol_efflux_activation",
        "genes": "PPARG;NR1H3;NR1H2;ABCA1;ABCG1",
        "therapeutic_direction": "Activate PPAR/LXR cholesterol-efflux programs; ABCA1/ABCG1 are downstream readouts, not easy direct activators.",
        "plausible_modality": "PPAR-gamma agonists are approved metabolic drugs; LXR agonists are preclinical/limited by lipogenesis.",
        "independent_evidence_channel": "PPAR/LXR biology regulates macrophage cholesterol efflux and has EAE/IBD/psoriasis literature.",
        "chemical_or_modality_matter": "Plenty of chemical matter, but generic PPAR/LXR claims are saturated and metabolically constrained.",
        "delivery_feasibility": "Oral systemic delivery is feasible; CNS and tissue-selective immune delivery are not the blocker, selectivity is.",
        "autoimmune_prior_art": "PPAR-gamma and LXR autoimmune anti-inflammatory claims are crowded across MS/EAE, IBD, psoriasis, and RA.",
        "blocking_issue": "Local V3 signal is mixed/negative for PPARG/NR1H3/ABCG1 and promotion criteria explicitly demote saturated generic PPAR/LXR claims.",
        "route_call": "NO_GO",
        "source_ids": "S_LXR_EAE;S_LXR_LIPOGENESIS;S_PPARG_UC_TRIAL;S_PPARG_MS_TRIAL",
        "query_terms": '"LXR agonist" experimental autoimmune encephalomyelitis; "PPAR gamma" ulcerative colitis trial; "pioglitazone" multiple sclerosis trial',
    },
    {
        "route": "mTOR_autophagy_modulation",
        "genes": "MTOR;TSC1;TSC2;RPTOR;RHEB;ULK1;BECN1;ATG5;ATG7;SQSTM1",
        "therapeutic_direction": "mTOR inhibition/autophagy induction is the usual direction, but it is broad immunometabolic modulation.",
        "plausible_modality": "Rapalogs and many autophagy modulators exist.",
        "independent_evidence_channel": "mTORC1 controls TFEB and autophagy; sirolimus has human autoimmune/SLE prior art.",
        "chemical_or_modality_matter": "Strong chemical matter, weak selectivity for the target module.",
        "delivery_feasibility": "Systemic and CNS exposure can be achieved for some agents, but chronic tolerability and broad immunosuppression are the issue.",
        "autoimmune_prior_art": "mTOR/sirolimus autoimmune trials and autophagy literature are saturated.",
        "blocking_issue": "Promotion criteria demote broad toxic lysosome/autophagy routes; local V3 does not rescue specificity.",
        "route_call": "NO_GO",
        "source_ids": "S_MTOR_TFEB;S_SIROLIMUS_SLE;S_SIROLIMUS_LABEL",
        "query_terms": '"mTOR" TFEB lysosome; sirolimus systemic lupus erythematosus trial; autophagy autoimmune',
    },
]


SOURCES = [
    {
        "source_id": "S_TFEB_CLEAR",
        "source_type": "PubMed",
        "title": "A gene network regulating lysosomal biogenesis and function",
        "url": "https://pubmed.ncbi.nlm.nih.gov/19556463/",
        "query_terms": "TFEB CLEAR network lysosomal biogenesis",
        "used_for": "TFEB as CLEAR/lysosomal biogenesis master regulator.",
    },
    {
        "source_id": "S_TFEB_AUTOPHAGY",
        "source_type": "PubMed",
        "title": "TFEB links autophagy to lysosomal biogenesis",
        "url": "https://pubmed.ncbi.nlm.nih.gov/21617040/",
        "query_terms": "TFEB links autophagy lysosomal biogenesis",
        "used_for": "TFEB autophagy-lysosome activation biology.",
    },
    {
        "source_id": "S_TFEB_MTOR",
        "source_type": "PubMed",
        "title": "mTORC1 controls lysosomal function through TFEB regulation",
        "url": "https://pubmed.ncbi.nlm.nih.gov/22576015/",
        "query_terms": "mTORC1 TFEB lysosomal function",
        "used_for": "mTOR/TFEB direction and broadness.",
    },
    {
        "source_id": "S_TFEB_TRPML1",
        "source_type": "PubMed",
        "title": "Lysosomal calcium signalling regulates autophagy through calcineurin and TFEB",
        "url": "https://pubmed.ncbi.nlm.nih.gov/25720963/",
        "query_terms": "TRPML1 calcineurin TFEB lysosomal calcium",
        "used_for": "MCOLN1/TRPML1 activation mechanism.",
    },
    {
        "source_id": "S_MLSA1",
        "source_type": "PubMed",
        "title": "Differential mechanisms of action of the mucolipin synthetic agonist ML-SA1",
        "url": "https://pubmed.ncbi.nlm.nih.gov/25266962/",
        "query_terms": "ML-SA1 TRPML1 agonist",
        "used_for": "TRPML1 chemical-matter precedent.",
    },
    {
        "source_id": "S_PIKFYVE_APILIMOD_IL12",
        "source_type": "PubMed",
        "title": "Selective abrogation of Th1 response by STA-5326, a potent IL-12/IL-23 inhibitor",
        "url": "https://pubmed.ncbi.nlm.nih.gov/17053051/",
        "query_terms": "apilimod IL-12 IL-23 PIKfyve",
        "used_for": "PIKFYVE/apilimod anti-inflammatory perturbation channel.",
    },
    {
        "source_id": "S_PIKFYVE_CROHN_TRIAL",
        "source_type": "PubMed",
        "title": "Apilimod mesylate in patients with active Crohn disease",
        "url": "https://pubmed.ncbi.nlm.nih.gov/19918967/",
        "query_terms": "apilimod mesylate active Crohn disease trial",
        "used_for": "Autoimmune/IBD prior art and clinical precedent.",
    },
    {
        "source_id": "S_PIKFYVE_CHRONIC_TOX",
        "source_type": "PMC",
        "title": "PIKfyve deficiency/inhibition impairs lysosomal homeostasis in macrophages",
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC6791654/",
        "query_terms": "PIKfyve inhibition lysosomal homeostasis macrophage apilimod",
        "used_for": "Broad lysosomal-disruption liability.",
    },
    {
        "source_id": "S_LIPA_UNIPROT",
        "source_type": "UniProt",
        "title": "LIPA human lysosomal acid lipase/cholesteryl ester hydrolase",
        "url": "https://www.uniprot.org/uniprotkb/P38571/entry",
        "query_terms": "UniProt LIPA P38571",
        "used_for": "Target function and biology.",
    },
    {
        "source_id": "S_LIPA_GENEREVIEWS",
        "source_type": "NCBI Bookshelf",
        "title": "Lysosomal Acid Lipase Deficiency",
        "url": "https://www.ncbi.nlm.nih.gov/books/NBK305870/",
        "query_terms": "GeneReviews lysosomal acid lipase deficiency sebelipase alfa",
        "used_for": "Human disease, direction, and replacement therapy precedent.",
    },
    {
        "source_id": "S_LIPA_MACROPHAGE",
        "source_type": "PMC",
        "title": "Macrophage lysosomal acid lipase controls inflammatory phenotypes in LAL-deficient mice",
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC3178672/",
        "query_terms": "lysosomal acid lipase macrophage inflammation PMC3178672",
        "used_for": "Independent perturbation/mechanistic support.",
    },
    {
        "source_id": "S_LIPA_EFFEROCYTOSIS",
        "source_type": "PMC",
        "title": "Lysosomal acid lipase, macrophage efferocytosis, and LXR biology",
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC6034181/",
        "query_terms": "LIPA macrophage efferocytosis LXR cholesterol",
        "used_for": "LIPA to cholesterol-efflux/anti-inflammatory mechanism.",
    },
    {
        "source_id": "S_LIPA_CHEMBL",
        "source_type": "ChEMBL",
        "title": "CHEMBL4184 lysosomal acid lipase and CHEMBL3039537 sebelipase alfa",
        "url": "https://www.ebi.ac.uk/chembl/explore/target/CHEMBL4184",
        "query_terms": "ChEMBL LIPA sebelipase alfa",
        "used_for": "Druggability/modality precedent.",
    },
    {
        "source_id": "S_LIPA_FDA",
        "source_type": "FDA label",
        "title": "Kanuma (sebelipase alfa) prescribing information",
        "url": "https://www.accessdata.fda.gov/drugsatfda_docs/label/2024/125561s020lbl.pdf",
        "query_terms": "FDA Kanuma sebelipase alfa label",
        "used_for": "Approved enzyme replacement and delivery route.",
    },
    {
        "source_id": "S_LIPA_MS_REPAIR",
        "source_type": "Journal article",
        "title": "LAL/Lipa microglial white-matter repair/remyelination report",
        "url": "https://link.springer.com/article/10.1186/s12974-026-03782-7",
        "query_terms": "lysosomal acid lipase GPNMB microglia remyelination 2026",
        "used_for": "MS/CNS repair prior art and mechanistic plausibility.",
    },
    {
        "source_id": "S_NPC_GENEREVIEWS",
        "source_type": "NCBI Bookshelf",
        "title": "Niemann-Pick Disease Type C",
        "url": "https://www.ncbi.nlm.nih.gov/books/NBK1296/",
        "query_terms": "GeneReviews Niemann-Pick disease type C NPC1 NPC2",
        "used_for": "NPC1/NPC2 disease biology and CNS delivery context.",
    },
    {
        "source_id": "S_NPC_HPBCD_TRIAL",
        "source_type": "ClinicalTrials.gov",
        "title": "Hydroxypropyl-beta-cyclodextrin in Niemann-Pick type C disease",
        "url": "https://clinicaltrials.gov/search?term=hydroxypropyl-beta-cyclodextrin%20Niemann-Pick%20type%20C",
        "query_terms": "hydroxypropyl-beta-cyclodextrin Niemann-Pick type C trial",
        "used_for": "NPC modality and delivery precedent.",
    },
    {
        "source_id": "S_GBA_AMBROXOL",
        "source_type": "PubMed",
        "title": "Ambroxol as a glucocerebrosidase chaperone in Parkinson disease",
        "url": "https://pubmed.ncbi.nlm.nih.gov/31779818/",
        "query_terms": "ambroxol glucocerebrosidase Parkinson disease trial",
        "used_for": "GBA chemical and CNS chaperone precedent.",
    },
    {
        "source_id": "S_GBA_GAUCHER_FDA",
        "source_type": "FDA label",
        "title": "Cerezyme (imiglucerase) prescribing information",
        "url": "https://www.accessdata.fda.gov/drugsatfda_docs/label/2022/020367s081lbl.pdf",
        "query_terms": "FDA Cerezyme imiglucerase label",
        "used_for": "Peripheral GBA enzyme-replacement precedent.",
    },
    {
        "source_id": "S_LRRK2_CROHN_PD",
        "source_type": "Science Translational Medicine",
        "title": "Functional variants in LRRK2 confer shared effects on risk for Crohn disease and Parkinson disease",
        "url": "https://www.science.org/doi/10.1126/scitranslmed.aai7795",
        "query_terms": "LRRK2 Crohn disease Parkinson functional variants",
        "used_for": "LRRK2 genetics and disease-specific rationale.",
    },
    {
        "source_id": "S_LRRK2_CT",
        "source_type": "ClinicalTrials.gov",
        "title": "LRRK2 inhibitor clinical trials",
        "url": "https://clinicaltrials.gov/search?term=LRRK2%20inhibitor",
        "query_terms": "LRRK2 inhibitor ClinicalTrials.gov BIIB122 DNL151",
        "used_for": "LRRK2 modality/drug-development maturity.",
    },
    {
        "source_id": "S_LXR_EAE",
        "source_type": "PubMed",
        "title": "Liver X receptor agonists modulate experimental autoimmune encephalomyelitis",
        "url": "https://pubmed.ncbi.nlm.nih.gov/16955483/",
        "query_terms": "LXR agonist experimental autoimmune encephalomyelitis",
        "used_for": "LXR autoimmune prior art.",
    },
    {
        "source_id": "S_LXR_LIPOGENESIS",
        "source_type": "PubMed",
        "title": "Role of LXRs in control of lipogenesis",
        "url": "https://pubmed.ncbi.nlm.nih.gov/11090131/",
        "query_terms": "LXR agonist SREBP-1c lipogenesis hypertriglyceridemia",
        "used_for": "LXR toxicity/selectivity concern.",
    },
    {
        "source_id": "S_PPARG_UC_TRIAL",
        "source_type": "PubMed",
        "title": "Rosiglitazone for mildly to moderately active ulcerative colitis",
        "url": "https://pubmed.ncbi.nlm.nih.gov/18325386/",
        "query_terms": "rosiglitazone ulcerative colitis trial PPAR gamma",
        "used_for": "PPAR-gamma autoimmune/IBD prior art.",
    },
    {
        "source_id": "S_PPARG_MS_TRIAL",
        "source_type": "PubMed",
        "title": "Pioglitazone in multiple sclerosis clinical literature",
        "url": "https://pubmed.ncbi.nlm.nih.gov/?term=pioglitazone+multiple+sclerosis+trial",
        "query_terms": "pioglitazone multiple sclerosis trial",
        "used_for": "PPAR-gamma/MS prior-art query anchor.",
    },
    {
        "source_id": "S_MTOR_TFEB",
        "source_type": "PubMed",
        "title": "mTORC1 controls lysosomal function through TFEB regulation",
        "url": "https://pubmed.ncbi.nlm.nih.gov/22576015/",
        "query_terms": "mTORC1 TFEB lysosomal function",
        "used_for": "mTOR/autophagy connection to lysosomal stress.",
    },
    {
        "source_id": "S_SIROLIMUS_SLE",
        "source_type": "PubMed",
        "title": "Sirolimus in active systemic lupus erythematosus",
        "url": "https://pubmed.ncbi.nlm.nih.gov/29551338/",
        "query_terms": "sirolimus systemic lupus erythematosus trial",
        "used_for": "mTOR autoimmune prior art.",
    },
    {
        "source_id": "S_SIROLIMUS_LABEL",
        "source_type": "FDA label",
        "title": "Rapamune (sirolimus) prescribing information",
        "url": "https://www.accessdata.fda.gov/drugsatfda_docs/label/2024/021083s076lbl.pdf",
        "query_terms": "FDA Rapamune sirolimus label",
        "used_for": "mTOR inhibitor clinical modality and systemic immunosuppression context.",
    },
]


DECISIONS = [
    {
        "route": "LIPA_LAL_enhancement",
        "local_cross_disease_support": "Borderline: broad h5ad positive in 3 diseases plus Wave15 residual state support in 5 diseases, but confounder-dominant and myeloid-contradictory.",
        "explicit_therapeutic_direction": "Yes: enhance/replace LAL.",
        "plausible_modality_delivery": "Partial: approved enzyme replacement exists; autoimmune tissue/CNS delivery is unsolved.",
        "independent_perturbation_or_mechanism": "Yes.",
        "blocking_prior_art": "Partial: broad MS remyelination/white-matter repair angle is already published.",
        "toxicity_or_selectivity": "Moderate delivery/selectivity risk, not broad-lysosome toxicity if targeted.",
        "promotion_gate_result": "Fails local robustness and delivery/prior-art gates.",
        "decision": "PARK",
    },
    {
        "route": "MCOLN1_TRPML1_activation",
        "local_cross_disease_support": "Fails: MCOLN1 is not recurrently positive locally.",
        "explicit_therapeutic_direction": "Yes: activate.",
        "plausible_modality_delivery": "Preclinical tool molecules only.",
        "independent_perturbation_or_mechanism": "Yes.",
        "blocking_prior_art": "No blocking autoimmune prior art found.",
        "toxicity_or_selectivity": "Unknown; lysosomal calcium activation is broad.",
        "promotion_gate_result": "Fails local and clinical tractability gates.",
        "decision": "NO_GO_TOOL_ONLY",
    },
    {
        "route": "TFEB_TFE3_CLEAR_activation",
        "local_cross_disease_support": "Fails: TFEB/TFE3 are locally negative/absent.",
        "explicit_therapeutic_direction": "Yes but broad: activate CLEAR/autophagy.",
        "plausible_modality_delivery": "Weak: indirect broad mechanisms dominate.",
        "independent_perturbation_or_mechanism": "Yes.",
        "blocking_prior_art": "Generic autophagy/TFEB literature is broad.",
        "toxicity_or_selectivity": "High broad autophagy/metabolic risk.",
        "promotion_gate_result": "Fails local, selectivity, and modality gates.",
        "decision": "NO_GO",
    },
    {
        "route": "PIKFYVE_inhibition",
        "local_cross_disease_support": "Fails/weak: expression positive in 2 diseases without state coupling.",
        "explicit_therapeutic_direction": "Yes: inhibit, but wrong for lysosomal rescue.",
        "plausible_modality_delivery": "Yes: small molecules.",
        "independent_perturbation_or_mechanism": "Yes.",
        "blocking_prior_art": "Yes: Crohn/psoriasis/RA/apilimod prior art.",
        "toxicity_or_selectivity": "High endolysosomal-disruption liability.",
        "promotion_gate_result": "Fails direction, toxicity, and prior-art gates.",
        "decision": "NO_GO",
    },
    {
        "route": "NPC1_NPC2_cholesterol_egress",
        "local_cross_disease_support": "Partial: NPC1/NPC2 state coupling exists in Wave15 but is confounder-dominant; broad recurrence is limited.",
        "explicit_therapeutic_direction": "Yes: rescue cholesterol egress.",
        "plausible_modality_delivery": "Partial but not selective.",
        "independent_perturbation_or_mechanism": "Yes for NPC disease biology, not autoimmune.",
        "blocking_prior_art": "No direct autoimmune blocker found.",
        "toxicity_or_selectivity": "Moderate CNS/delivery and lipid-mobilization risks.",
        "promotion_gate_result": "Fails direct autoimmune perturbation and modality specificity.",
        "decision": "PARK_READOUT",
    },
    {
        "route": "GBA_GBA2_sphingolipid_modulation",
        "local_cross_disease_support": "Fails: no local recurrence support.",
        "explicit_therapeutic_direction": "Unclear outside GBA enhancement.",
        "plausible_modality_delivery": "Partial, disease-specific.",
        "independent_perturbation_or_mechanism": "Yes for Gaucher/Parkinson, not autoimmune module.",
        "blocking_prior_art": "No direct autoimmune blocker found.",
        "toxicity_or_selectivity": "Delivery and pathway-breadth concerns.",
        "promotion_gate_result": "Fails local support and direction gates.",
        "decision": "NO_GO",
    },
    {
        "route": "LRRK2_inhibition",
        "local_cross_disease_support": "IBD-skewed: Crohn/UC positive and MS trend, but no cross-autoimmune state support.",
        "explicit_therapeutic_direction": "Yes: inhibit kinase.",
        "plausible_modality_delivery": "Yes: clinical CNS-penetrant kinase inhibitors.",
        "independent_perturbation_or_mechanism": "Yes: genetics/lysosomal immune biology.",
        "blocking_prior_art": "Crowded in Crohn/Parkinson.",
        "toxicity_or_selectivity": "Kinase/safety and chronic immune target risks.",
        "promotion_gate_result": "Fails shared cross-disease state gate.",
        "decision": "PARK_DISEASE_SPECIFIC",
    },
    {
        "route": "PPAR_LXR_cholesterol_efflux_activation",
        "local_cross_disease_support": "Fails/mixed: PPARG/NR1H3/ABCG1 are mixed or negative; ABCA1 is MS-positive but broad-negative.",
        "explicit_therapeutic_direction": "Yes: activate.",
        "plausible_modality_delivery": "Yes for systemic drugs, but not selective.",
        "independent_perturbation_or_mechanism": "Yes, heavily prior-arted.",
        "blocking_prior_art": "Yes: generic PPAR/LXR autoimmune claims are saturated.",
        "toxicity_or_selectivity": "Metabolic/lipogenesis/edema-weight concerns.",
        "promotion_gate_result": "Fails novelty and local specificity gates.",
        "decision": "NO_GO",
    },
    {
        "route": "mTOR_autophagy_modulation",
        "local_cross_disease_support": "Fails specificity: individual autophagy genes are sparse/mixed locally.",
        "explicit_therapeutic_direction": "Yes but broad: mTOR inhibition/autophagy induction.",
        "plausible_modality_delivery": "Yes.",
        "independent_perturbation_or_mechanism": "Yes.",
        "blocking_prior_art": "Yes: sirolimus/autophagy autoimmune prior art.",
        "toxicity_or_selectivity": "High broad immunosuppression/metabolic toxicity.",
        "promotion_gate_result": "Fails broad-toxic-route guardrail.",
        "decision": "NO_GO",
    },
]


def read_table(relative: str) -> pd.DataFrame:
    path = ROOT / relative
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path, sep="\t", low_memory=False)


def coerce_numeric(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    for col in columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def collapse_geneformer() -> pd.DataFrame:
    files = [
        *ROOT.glob("phases/v3/results/geneformer_*/*gene_summary.tsv"),
        *ROOT.glob("phases/v3/results/wave14_geneformer_narrowed_candidate_delete/*gene_summary.tsv"),
        *ROOT.glob("phases/v3/results/wave15_geneformer_loader_dependency_delete/*gene_summary.tsv"),
    ]
    frames = []
    for path in files:
        df = pd.read_csv(path, sep="\t", low_memory=False)
        if "gene" not in df.columns:
            continue
        df = df.copy()
        df["foundation_source"] = str(path.relative_to(ROOT))
        for col in [
            "contexts_with_token",
            "disease_cells_with_token",
            "mean_projection_shift",
            "mean_cosine_z_vs_random",
            "support_contexts",
            "strong_support_contexts",
        ]:
            if col not in df.columns:
                df[col] = 0
        frames.append(df)
    if not frames:
        return pd.DataFrame(columns=["gene"])
    all_df = pd.concat(frames, ignore_index=True, sort=False)
    all_df = coerce_numeric(
        all_df,
        [
            "contexts_with_token",
            "disease_cells_with_token",
            "mean_projection_shift",
            "mean_cosine_z_vs_random",
            "support_contexts",
            "strong_support_contexts",
        ],
    )
    all_df["sort_support"] = all_df["support_contexts"].fillna(0)
    all_df["sort_strong"] = all_df["strong_support_contexts"].fillna(0)
    all_df["sort_contexts"] = all_df["contexts_with_token"].fillna(0)
    return (
        all_df.sort_values(["gene", "sort_strong", "sort_support", "sort_contexts"], ascending=[True, False, False, False])
        .drop_duplicates("gene", keep="first")
        .drop(columns=["sort_support", "sort_strong", "sort_contexts"])
    )


def local_evidence() -> pd.DataFrame:
    base = pd.DataFrame(CANDIDATES)

    broad_cols = [
        "gene",
        "tested_compartment_count",
        "positive_disease_count",
        "negative_disease_count",
        "positive_fdr10_compartment_count",
        "negative_fdr10_compartment_count",
        "positive_diseases",
        "negative_diseases",
        "ms_wm_delta_log2",
        "ms_wm_hedges_g",
        "ms_wm_p",
        "existing_positive_disease_count",
        "existing_negative_disease_count",
        "existing_positive_diseases",
        "existing_negative_diseases",
        "ms_positive_nominal",
        "ms_positive_trend",
        "discovery_priority_score",
    ]
    broad = read_table("phases/v3/results/broad_h5ad_gene_discovery/broad_h5ad_gene_rank.tsv")
    if not broad.empty:
        broad = broad[[c for c in broad_cols if c in broad.columns]]
        broad = broad.add_prefix("broad_").rename(columns={"broad_gene": "gene"})
        base = base.merge(broad, on="gene", how="left")

    cross_cols = [
        "gene",
        "n_diseases_tested",
        "n_strong_diseases",
        "n_supportive_or_strong_diseases",
        "n_trend_or_better_diseases",
        "n_negative_trend_diseases",
        "median_positive_hedges_g",
        "supporting_diseases",
    ]
    cross = read_table("phases/v3/results/cross_disease_gene_summary.tsv")
    if not cross.empty:
        cross = cross[[c for c in cross_cols if c in cross.columns]]
        cross = cross.add_prefix("cross_").rename(columns={"cross_gene": "gene"})
        base = base.merge(cross, on="gene", how="left")

    surface_cols = [
        "gene",
        "family",
        "druggability_score",
        "n_delta_trend_or_better_diseases",
        "n_delta_fdr10_positive_diseases",
        "n_delta_negative_trend_diseases",
        "delta_supporting_diseases",
        "delta_negative_diseases",
        "n_state_raw_r_ge_0_5_diseases",
        "n_state_resid_non_ifn_r_ge_0_35_diseases",
        "n_state_resid_with_ifn_r_ge_0_25_diseases",
        "n_confounder_dominant_diseases",
        "raw_state_supporting_diseases",
        "resid_non_ifn_supporting_diseases",
        "rank_score",
        "go_no_go",
        "demotion_or_support_reason",
    ]
    surface = read_table("phases/v3/results/wave15_surface_trafficking_dependency/candidate_ranked.tsv")
    if not surface.empty:
        surface = surface[[c for c in surface_cols if c in surface.columns]]
        surface = surface.add_prefix("surface_").rename(columns={"surface_gene": "gene"})
        base = base.merge(surface, on="gene", how="left")

    orch_cols = [
        "gene",
        "candidate_class",
        "n_expr_trend_or_better_diseases",
        "n_expr_fdr10_positive_diseases",
        "n_expr_negative_trend_diseases",
        "n_resid_state_support_diseases",
        "n_raw_state_support_diseases",
        "expression_supporting_diseases",
        "resid_state_supporting_diseases",
        "raw_state_supporting_diseases",
        "priority_score",
    ]
    orch = read_table("phases/v3/results/wave15_orchestrator_dependency_scan/candidate_dependency_priority_summary.tsv")
    if not orch.empty:
        orch = orch[[c for c in orch_cols if c in orch.columns]]
        orch = orch.add_prefix("orchestrator_").rename(columns={"orchestrator_gene": "gene"})
        base = base.merge(orch, on="gene", how="left")

    gf = collapse_geneformer()
    gf_cols = [
        "gene",
        "foundation_source",
        "contexts_with_token",
        "disease_cells_with_token",
        "mean_projection_shift",
        "mean_cosine_z_vs_random",
        "support_contexts",
        "strong_support_contexts",
        "positive_projection_contexts",
        "negative_projection_contexts",
    ]
    if not gf.empty:
        gf = gf[[c for c in gf_cols if c in gf.columns]]
        gf = gf.add_prefix("foundation_").rename(columns={"foundation_gene": "gene"})
        base = base.merge(gf, on="gene", how="left")

    numeric = [
        "broad_positive_disease_count",
        "broad_negative_disease_count",
        "broad_existing_positive_disease_count",
        "broad_existing_negative_disease_count",
        "cross_n_trend_or_better_diseases",
        "surface_n_delta_trend_or_better_diseases",
        "surface_n_state_resid_non_ifn_r_ge_0_35_diseases",
        "surface_n_confounder_dominant_diseases",
        "orchestrator_n_expr_trend_or_better_diseases",
        "orchestrator_n_resid_state_support_diseases",
        "foundation_support_contexts",
        "foundation_strong_support_contexts",
    ]
    base = coerce_numeric(base, numeric)
    base["local_recurrence_disease_count_max"] = base[
        [
            "broad_positive_disease_count",
            "broad_existing_positive_disease_count",
            "cross_n_trend_or_better_diseases",
            "surface_n_delta_trend_or_better_diseases",
            "orchestrator_n_expr_trend_or_better_diseases",
        ]
    ].max(axis=1, skipna=True)
    base["local_state_support_disease_count_max"] = base[
        [
            "surface_n_state_resid_non_ifn_r_ge_0_35_diseases",
            "orchestrator_n_resid_state_support_diseases",
        ]
    ].max(axis=1, skipna=True)
    base["local_negative_disease_count_max"] = base[
        [
            "broad_negative_disease_count",
            "broad_existing_negative_disease_count",
            "cross_n_negative_trend_diseases",
            "surface_n_delta_negative_trend_diseases",
            "orchestrator_n_expr_negative_trend_diseases",
        ]
    ].max(axis=1, skipna=True)
    base["foundation_any_support"] = base["foundation_support_contexts"].fillna(0) > 0
    base["local_gate_flag"] = "weak_or_absent"
    base.loc[
        (base["local_recurrence_disease_count_max"].fillna(0) >= 3)
        & (base["local_state_support_disease_count_max"].fillna(0) >= 4),
        "local_gate_flag",
    ] = "state_supported"
    base.loc[
        (base["local_recurrence_disease_count_max"].fillna(0) >= 3)
        & (base["local_state_support_disease_count_max"].fillna(0) < 4),
        "local_gate_flag",
    ] = "recurrence_without_state"
    base.loc[
        base["surface_n_confounder_dominant_diseases"].fillna(0) >= base["local_state_support_disease_count_max"].fillna(999),
        "local_gate_flag",
    ] = base["local_gate_flag"] + "_confounded"
    base.loc[
        base["local_negative_disease_count_max"].fillna(0) >= 2,
        "local_gate_flag",
    ] = base["local_gate_flag"] + "_mixed_negative"
    return base


def route_summary(local: pd.DataFrame) -> pd.DataFrame:
    route_calls = {row["route"]: row for row in EXTERNAL_ROUTES}
    grouped = (
        local.groupby("route", as_index=False)
        .agg(
            genes=("gene", lambda x: ";".join(x)),
            max_local_recurrence=("local_recurrence_disease_count_max", "max"),
            max_local_state_support=("local_state_support_disease_count_max", "max"),
            max_local_negative=("local_negative_disease_count_max", "max"),
            any_foundation_support=("foundation_any_support", "max"),
            n_state_supported_genes=("local_gate_flag", lambda x: sum(str(v).startswith("state_supported") for v in x)),
        )
    )
    external = pd.DataFrame(EXTERNAL_ROUTES)
    decisions = pd.DataFrame(DECISIONS)[["route", "promotion_gate_result", "decision"]]
    out = grouped.merge(external, on="route", how="outer", suffixes=("_local", ""))
    out["genes"] = out["genes"].fillna(out["genes_local"])
    if "genes_local" in out.columns:
        out = out.drop(columns=["genes_local"])
    out = out.merge(decisions, on="route", how="left")
    out["route_call"] = out["route_call"].fillna(out["decision"])
    out["route_call"] = out["route_call"].fillna("COMPARATOR_ONLY")
    out["promotion_gate_result"] = out["promotion_gate_result"].fillna(
        "Local comparator/control route; not evaluated as an upstream therapeutic intervention route."
    )
    return out


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    local = local_evidence()
    external = pd.DataFrame(EXTERNAL_ROUTES)
    sources = pd.DataFrame(SOURCES)
    decisions = pd.DataFrame(DECISIONS)
    routes = route_summary(local)

    local.to_csv(OUT / "candidate_local_evidence.tsv", sep="\t", index=False)
    external.to_csv(OUT / "external_evidence_matrix.tsv", sep="\t", index=False)
    sources.to_csv(OUT / "source_log.tsv", sep="\t", index=False)
    decisions.to_csv(OUT / "decision_matrix.tsv", sep="\t", index=False)
    routes.to_csv(OUT / "route_summary.tsv", sep="\t", index=False)

    summary = {
        "n_candidates": int(local.shape[0]),
        "n_routes": int(routes.shape[0]),
        "route_call_counts": routes["route_call"].fillna("UNCLASSIFIED").value_counts().to_dict(),
        "promoted_go_routes": [],
        "parked_routes": routes.loc[routes["route_call"].fillna("").str.contains("PARK"), "route"].tolist(),
        "no_go_routes": routes.loc[routes["route_call"].fillna("").str.contains("NO_GO"), "route"].tolist(),
        "inputs": [
            "phases/v3/results/broad_h5ad_gene_discovery/broad_h5ad_gene_rank.tsv",
            "phases/v3/results/cross_disease_gene_summary.tsv",
            "phases/v3/results/wave15_surface_trafficking_dependency/candidate_ranked.tsv",
            "phases/v3/results/wave15_orchestrator_dependency_scan/candidate_dependency_priority_summary.tsv",
            "phases/v3/results/geneformer_*/*gene_summary.tsv",
            "phases/v3/results/wave14_geneformer_narrowed_candidate_delete/*gene_summary.tsv",
            "phases/v3/results/wave15_geneformer_loader_dependency_delete/*gene_summary.tsv",
        ],
        "outputs": [
            "candidate_local_evidence.tsv",
            "external_evidence_matrix.tsv",
            "source_log.tsv",
            "decision_matrix.tsv",
            "route_summary.tsv",
            "summary.json",
        ],
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")


if __name__ == "__main__":
    main()
