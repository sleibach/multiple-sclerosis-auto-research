# Wave78a sidecar: LILRB-family inhibitory myeloid receptors in autoimmune disease

Date: 2026-05-27

Scope: hostile prior-art and translational feasibility scout for LILRB2/ILT4, LILRB1/ILT2, and LILRB4/ILT3 in autoimmune disease. Sources checked where accessible: PubMed/Europe PMC, ClinicalTrials.gov, Google Patents, ChEMBL API, Open Targets API, and sponsor/peer-reviewed clinical program disclosures.

## Executive read

Do not promote as a clean new autoimmune intervention axis. The evidence base supports that LILRB-family receptors are real inhibitory immune checkpoints on myeloid/APC lineages, but the therapeutic direction is not stable across diseases:

- Autoimmune tolerance literature usually points toward agonism/induction of ILT3/ILT4-like tolerogenic programs, especially via tolerogenic dendritic cells, soluble ILT3/ILT3-Fc, HLA-G/LILRB1/2 signaling, IFN-beta/vitamin-D-associated tolerogenic phenotypes, or suppressor-cell induction.
- Oncology drug development has moved in the opposite direction: LILRB2, LILRB1/2, and LILRB4 antagonism/depletion to activate myeloid/T-cell immunity.
- SLE creates a special exception: LILRB4/ILT3 can be read as protective on DCs, but also as a pathogenic marker/functional participant on plasmablasts/plasma cells in some reports. That makes receptor-level directionality unsafe without cell-selective targeting.
- No autoimmune interventional clinical trial of a LILRB-targeted biologic was found in ClinicalTrials.gov. Existing interventional programs are oncology or AML/CMML, while autoimmune disease is commonly an exclusion criterion in immune-activating oncology studies.

Final call: **PARK_DIRECTIONALITY**.

Rationale: target family is druggable by biologics and heavily patented, but directionality is unresolved and disease/cell-context dependent. A generic "LILRB agonist for autoimmune disease" is blocked by older ILT3-Fc/targeted-immunotolerance prior art. A generic "LILRB antagonist/depleter for autoimmune disease" conflicts with tolerogenic biology and is crowded by oncology antagonist/depleter estates. A narrow lupus plasma-cell depletion/ligand-blocking hypothesis has prior art and would need a very specific translational delta.

## Target identifiers and resource checks

| Target | Alias | Open Targets ID | Current evidence shape |
|---|---:|---:|---|
| LILRB2 | ILT4, CD85d, LIR-2 | ENSG00000131042 | Open Targets associated-disease results are dominated by Alzheimer disease, COPD, neoplasm, and literature-only autoimmune signals such as SLE and psoriatic arthritis. Clinical drug programs are anti-tumor antagonists. |
| LILRB1 | ILT2, CD85j, LIR-1 | ENSG00000104972 | Open Targets top results include cancer, RA, SLE, and infection, mostly literature-driven. Drug development includes dual LILRB1/2 antagonists in oncology. |
| LILRB4 | ILT3, CD85k, LIR-5 | ENSG00000186818 | Open Targets top results are neurodegeneration/cancer/AML and literature signals. Biology spans tolerogenic DC/APC signaling, SLE plasma cells, IBD macrophage suppression, and AML targeting. |

ChEMBL API target search for `LILRB` returned no target records in this check, consistent with a biologics-first, extracellular receptor target class rather than mature small-molecule pharmacology.

## Closest prior art

### Broad autoimmune/tolerance prior art

- **US9078858B2, "ILT3 polypeptides and uses thereof"**; Columbia, priority 2004-09-03, granted 2015-07-14, Google legal status expired fee-related, adjusted expiry listed 2025-11-07. This is the closest blocker for LILRB4/ILT3 agonism/soluble receptor immunosuppression. The specification explicitly proposes soluble ILT3/ILT3-Fc for transplant rejection, autoimmune diabetes, GVHD, inflammatory disorders, and flare-up autoimmune attacks including RA, Crohn disease, MS, and juvenile dermatomyositis. Link: https://patents.google.com/patent/US9078858B2/en
- **US20180265584A1, "Targeted Immunotolerance"**; proposes multimerized HLA-G or agonistic anti-KIR2DL4, anti-LILRB1, or anti-LILRB2 antibody molecules to deliver inhibitory signals and create site-specific immune privilege. This is a direct conceptual blocker for LILRB1/2 agonism as targeted immunotolerance. Link: https://patents.google.com/patent/US20180265584A1/en
- **US8901281B2, "ILT3 binding molecules and uses therefor"**; covers ILT3-binding molecules and modulation of ILT3 activity, including downmodulating unwanted immune activation and ex vivo cell-treatment/reintroduction concepts. Link: https://patents.google.com/patent/US8901281B2/en

### LILRB2/ILT4 antagonist and antibody estate

- **US11401328B2 / WO2020014132A2/A3, "Antibodies binding to ILT4"**; Five Prime/BMS, priority 2018-07-09, active, adjusted expiry listed 2040-05-12. Claims ILT4/LILRB2 antibodies with selectivity over ILT2/ILT3/ILT5 and other LILR family members. This blocks much of clean anti-LILRB2 biologic space. Links: https://patents.google.com/patent/US11401328B2/en and https://patents.google.com/patent/WO2020014132A3/en
- **WO2020061059A1, "Anti-LILRB2 antibodies and methods of use thereof"**; antagonist antibodies altering macrophage maturation and enhancing inflammatory activation. Link: https://patents.google.com/patent/WO2020061059A1/en
- **US20230068663A1, "Novel LILRB2 antibodies and uses thereof"**; includes both agonising LILRB family receptors for autoimmune/inflammatory diseases and blocking ligand binding for antagonism. Link: https://patents.google.com/patent/US20230068663A1/en
- **WO2024261729A1, "LILRB2 binding proteins and uses thereof"**; recent LILRB2 binding proteins for diseases associated with increased LILRB2 activity, especially cancer. Link: https://patents.google.com/patent/WO2024261729A1/en

### LILRB1/2 dual antagonist estate

- **WO2022187968A1, "LILRB1 and LILRB2-binding molecules and uses therefor"**; covers antibodies binding LILRB1 and/or LILRB2 and use in inflammatory diseases, autoimmune diseases, and cancer. This is a direct blocker for dual LILRB1/2 biologics. Link: https://patents.google.com/patent/WO2022187968A1/en

### LILRB4/ILT3 antagonist/depletion estate

- **US12435133B2, "Antibodies specific for ILT3 and uses thereof"**; Merck/MSD, priority 2017-11-17, granted 2025-10-07, active, adjusted expiry listed 2040-09-24. Strong antibody estate for ILT3/LILRB4. Link: https://patents.google.com/patent/US12435133B2/en
- **US12180277B2, "LILRB4-binding antibody and methods of use thereof"**; University of Texas system/Allison-associated inventorship, priority 2019-03-01, active, expiry listed 2042-04-28. Link: https://patents.google.com/patent/US12180277B2/en
- **WO2024155891A2/A3, "LILRB4/ILT3 antagonist compositions and methods of use thereof"**; Washington University/Colonna, priority 2023-01-20, directed to anti-human LILRB4 antibodies and LILRB4-Fc fusions for microglial-associated neurological disease/amyloid biology. This is not autoimmune-specific but blocks CNS LILRB4 antagonist concepts. Link: https://patents.google.com/patent/WO2024155891A2/en
- **WO2023192850A1, "ILT3 and CD3 binding agents and methods of use thereof"**; ILT3 x CD3 T-cell engager format, oncology/depletion direction. Link: https://patents.google.com/patent/WO2023192850A1/en

## Clinical and drug-development landscape

No LILRB-directed autoimmune therapeutic trial was found. Clinical programs are immune-activating oncology or AML/CMML:

- **MK-4830**, anti-ILT4/LILRB2 IgG4 antagonist, first-in-human phase 1 in advanced solid tumors, **NCT03564691**. Peer-reviewed report describes it as a first-in-class anti-ILT4 myeloid checkpoint antibody studied alone and with pembrolizumab. Link: https://clinicaltrials.gov/study/NCT03564691 and https://pmc.ncbi.nlm.nih.gov/articles/PMC9401547/
- **JTX-8064**, anti-LILRB2/ILT4 inhibitor mAb, phase 1/2 in advanced refractory solid tumors, **NCT04669899**, completed, enrollment 190. ClinicalTrials states it blocks LILRB2 interaction with MHC-I ligands. Link: https://clinicaltrials.gov/study/NCT04669899
- **IO-108**, anti-LILRB2 antagonist antibody, phase 1 solid tumors, **NCT05054348**. Publication reports dose-escalation proof of concept for myeloid-suppressive pathway inhibition. Link: https://clinicaltrials.gov/study/NCT05054348 and https://pmc.ncbi.nlm.nih.gov/articles/PMC11580248/
- **NGM707 / PF-07826390**, anti-ILT2/anti-ILT4 dual antagonist, phase 1/2 solid tumors, **NCT04913337**. Trial excludes active/history of clinically significant autoimmune disease requiring chronic systemic immunosuppression and prior LILRB1/2 pathway agents. Link: https://clinicaltrials.gov/study/NCT04913337
- **SAR444881**, anti-ILT2/LILRB1 antibody oncology trial, **NCT05546268** per sponsor materials; autoimmune disease is an exclusion in the trial poster. Link: https://clinicaltrials.gov/study/NCT05546268
- **CHS-1000**, LILRB2/ILT4 solid-tumor program, **NCT06389526**, not yet recruiting in the registry snapshot, phase 1 with toripalimab combination. Link: https://clinicaltrials.gov/study/NCT06389526
- **IO-202**, anti-LILRB4 antibody, solid tumors **NCT05309187** and AML/CMML **NCT04372433** in public trial records; plus **LILRB4 STAR-T cells**, AML/CMML **NCT05548088**. These are depletion/antagonism oncology directions. Links: https://clinicaltrials.gov/study/NCT05309187 and https://clinicaltrials.gov/study/NCT05548088

Translational implication: antagonist safety packages from cancer do not de-risk autoimmune use. They are designed to break suppressive myeloid checkpoints, and many protocols exclude autoimmune disease. Conversely, tolerogenic autoimmune use would need agonist/multimerized-ligand/soluble-receptor pharmacology, which is less clinically mature and closer to older patent estates.

## Disease-by-disease directionality notes

### Multiple sclerosis

Evidence supports tolerogenic direction more than antagonism. TolDC reviews list ILT3/ILT4 among inhibitory molecules characteristic of tolerogenic dendritic cells, and LILRB4 reviews summarize MS as a setting where IFN-beta/vitamin D can increase LILRB4 on APCs and suppress inflammatory cytokine production. However, I did not find a LILRB-targeted MS interventional trial. Closest prior-art blocker is soluble ILT3/ILT3-Fc for autoimmune flare-ups including MS in US9078858B2.

Disposition: **not blocked by an MS-specific clinical LILRB drug**, but **blocked/crowded for generic ILT3 agonism** and directionally hostile to antagonism.

### Rheumatoid arthritis

Human RA synovium study: Huynh et al., Rheumatology 2007, PMID: 17202177, found abundant LILRB2/LILRB3/LILRA2 expression in RA synovial tissue pre-treatment; expression decreased in DMARD responders but remained high in nonresponders. This reads more as inflammatory-infiltrate biomarker biology than clean target validation. Link: https://doi.org/10.1093/rheumatology/kel405 and https://europepmc.org/article/MED/17202177

Patents explicitly mention RA flare-up treatment with soluble ILT3, so tolerogenic/agonist autoimmune claims are prior-art exposed. Antagonism would risk amplifying macrophage/T-cell activation.

Disposition: **PARK_DIRECTIONALITY**; no RA-specific LILRB drug trial, but no clean delta.

### IBD / Crohn disease / ulcerative colitis

Older ILT3-Fc patent explicitly lists Crohn disease autoimmune flare-up treatment. Reviews describe LILRB4 on macrophages as limiting ERK/NF-kB/proinflammatory cytokine activation in IBD-like contexts. A UC dendritic-cell study (Al-Hassi et al., PMID: 24347371) supports altered gut DC properties in UC, but not a direct LILRB therapeutic. Link: https://pubmed.ncbi.nlm.nih.gov/24347371/

Disposition: **PARK_DIRECTIONALITY**; agonism is prior-art crowded, antagonism is biologically risky.

### Psoriasis / psoriatic arthritis / ankylosing spondylitis

Open Targets returns a literature-only LILRB2 association with psoriatic arthritis, but I did not identify disease-specific LILRB intervention trials or strong mechanistic prior art for psoriasis/AS. The HLA/LILR axis is plausible because LILRB1/2 bind MHC-I/HLA-G family ligands, but that is not sufficient for a therapeutic claim.

Disposition: **NO_GO for broad psoriasis/AS promotion on current evidence**; too indirect and likely covered by generic LILRB immunotolerance/antibody claims.

### SLE / lupus

This is the most conflicted disease:

- LILRB2/ILT4 in SLE DCs: Guerra-de Blas et al., J Immunol Res 2016, PMID: 27057555, found decreased ILT4-positive plasmacytoid and myeloid DCs in SLE patients and partial inhibitory effects of ILT4 ligation on SLE DC immunogenic capability. Link: https://europepmc.org/article/MED/27057555
- LILRB4/ILT3 in SLE genetics/DCs: Jensen et al., Ann Rheum Dis 2013, PMID: 22904259, reported ILT3 loss-of-function polymorphisms associated with decreased DC surface expression and increased type I IFN/TNF-alpha cytokine activity in SLE. Link: https://europepmc.org/article/MED/22904259
- LILRB4/ILT3 in SLE plasma cells: LILRB4 reviews cite high LILRB4 on plasmablasts/plasma cells from untreated SLE and a model in which fibronectin-LILRB4 interaction can support pathogenic IgG autoantibody output; blocking with anti-LILRB4 or recombinant LILRB4 is proposed to reduce pathogenic IgG and increase protective IgM. Review link: https://pmc.ncbi.nlm.nih.gov/articles/PMC10887124/

Interpretation: receptor-level agonism vs antagonism is unsafe. DC biology suggests preserving/agonizing inhibitory signaling; plasma-cell biology suggests blockade/depletion may be useful in a subset. A promotable angle would need cell-selective delivery, biomarker-defined SLE plasmablast/plasma-cell dependence, and freedom-to-operate around ILT3 antibody estates.

Disposition: **PARK_DIRECTIONALITY / likely prior-art crowded for LILRB4 blockade**.

### Sjogren disease

No LILRB1/2/4 therapeutic prior art specific to Sjogren was identified in this pass. Given overlap with IFN-high SLE-like biology, inhibitory receptor agonism could be hypothesized, but evidence is not sufficient.

Disposition: **NO_GO on current evidence**.

### Type 1 diabetes

US9078858B2 is directly blocking: it claims/prefigures ILT3 polypeptides for autoimmune diabetes, including NOD mouse treatment with ILT3-Fc or IgG. TolDC literature also includes type 1 diabetes clinical tolDC development, where ILT3/ILT4 are tolerogenic markers rather than standalone drug targets.

Disposition: **BLOCKED_BY_PRIOR_ART for soluble ILT3/ILT3-Fc agonist-style T1D claims**.

### Celiac disease

No strong LILRB-specific celiac therapeutic evidence was found. Generic tolerogenic APC concepts may be relevant, but not enough for promotion.

Disposition: **NO_GO on current evidence**.

### Autoimmune thyroid disease

Recent reviews of cellular immunomodulation/tolDCs in autoimmune thyroiditis mention tolerogenic-cell strategies, but I found no LILRB-targeted therapeutic program. This is generic tolerance biology, not a targetable delta.

Disposition: **NO_GO on current evidence**.

### Primary biliary cholangitis

No LILRB-targeted PBC-specific therapeutic evidence was identified. Liver-transplant tolerance studies measure ILT3/ILT4 as DC/tolerance markers, but that does not translate to PBC treatment.

Disposition: **NO_GO on current evidence**.

### Myasthenia gravis

No LILRB-targeted MG therapeutic evidence was identified. General myeloid/tolDC immune tolerance is too broad.

Disposition: **NO_GO on current evidence**.

## Druggability and selectivity assessment

- **Biologics feasibility: high.** Extracellular Ig-like receptors are antibody-accessible. Multiple clinical antibodies already exist for LILRB2, LILRB1/2, and LILRB4, plus T-cell engager/CAR/STAR-T formats for LILRB4-positive AML.
- **Small-molecule feasibility: low/unclear.** ChEMBL target search did not return LILRB target entries, and the ligand interfaces are large protein-protein interfaces with MHC-I/HLA-G, fibronectin, ApoE, ALCAM, and related ligands depending on receptor/cell context.
- **Selectivity risk: high.** LILRB1 and LILRB2 both bind broad MHC-I/HLA-G ligands; antibody families emphasize selectivity over related LILRA/LILRB members because cross-reactivity is a known issue. LILRB4 mouse-human biology is especially awkward: patent/review materials note mouse LILRB4 is not a direct ortholog of human LILRB4, weakening standard mouse autoimmune model translation.
- **Directionality risk: very high.** Agonizing inhibitory receptors may suppress pathogenic autoimmunity but can impair host defense, tumor surveillance, and vaccine responses. Antagonizing/depleting them may improve antitumor immunity but can plausibly worsen autoimmune inflammation. LILRB4 in SLE is cell-state bifurcated: protective-looking on DCs, pathogenic-looking on plasma cells.
- **Biomarker feasibility: moderate.** Flow cytometry can measure LILRB1/2/4 on monocytes, DCs, pDCs, macrophages, NK/T subsets, plasmablasts/plasma cells. But receptor occupancy and downstream ITIM/SHP signaling are harder to interpret when the desired effect changes by cell type.

## Trial and patent blockers by modality

| Modality | Evidence/blocker | Feasibility call |
|---|---|---|
| LILRB4/ILT3 soluble receptor or agonist for autoimmune disease | Directly prefigured by US9078858B2 and generic tolDC/ILT3 literature. | **BLOCKED_BY_PRIOR_ART** for broad autoimmune claims. |
| LILRB1/2 agonism via HLA-G or agonist antibody for site-specific immunotolerance | US20180265584A1 directly proposes HLA-G or agonistic anti-LILRB1/2 targeted immunotolerance. | **BLOCKED_BY_PRIOR_ART** unless a very specific delivery/indication delta exists. |
| LILRB2 antagonist for autoimmune disease | Crowded by BMS/Five Prime, Merck, Jounce, Immune-Onc, NGM/Pfizer-like oncology antibody estates; biology conflicts with tolerance. | **PARK_DIRECTIONALITY / likely no-go**. |
| LILRB4 antagonist or depletion for SLE plasma cells | Some disease rationale exists, but Merck/MSD, UT/Allison, Washington University/Colonna and AML programs crowd antibodies/depleters. DC biology cuts the opposite way. | **PARK_DIRECTIONALITY**, not promotable without cell-selective delta. |
| Dual LILRB1/2 antagonist | WO2022187968A1 and NGM707/PF-07826390 clinical program. Autoimmune exclusion in oncology trial highlights risk. | **NO_GO for autoimmune without strong mechanistic reversal.** |
| Small molecule | No ChEMBL target support found; PPI surfaces. | **NO_GO near term**. |

## Bottom line

The family is real and druggable, but the autoimmune translational case is not clean. The most defensible autoimmune direction is tolerogenic agonism/induction of ILT3/ILT4/LILRB1/2 signaling, yet that is exactly where old soluble ILT3 and targeted HLA-G/LILRB immunotolerance prior art sits. The opposite direction, antagonist/depletion, is clinically active in oncology but mechanistically risky for autoimmune disease and already crowded by antibody estates. SLE plasma-cell LILRB4 is the only plausible narrow exception, but it is also the highest directionality trap because DC and plasma-cell biology point in different directions.

Final call: **PARK_DIRECTIONALITY**.
