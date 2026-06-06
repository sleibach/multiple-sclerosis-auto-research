# Wave93 sidecar: GPR183/EBI2 oxysterol-niche biology in autoimmune disease

Date: 2026-05-27

Scope: evidence-only audit for GPR183/EBI2, CH25H, CYP7B1, HSD3B7, and 7alpha,25-dihydroxycholesterol (7alpha,25-OHC) as an autoimmune therapeutic route. Sources checked: PubMed/Europe PMC, bioRxiv search, ClinicalTrials.gov, Google Patents, ChEMBL, and existing V3 context. This does not claim a finding.

## Bottom Line

GPR183/EBI2 is a real oxysterol-sensing immune-positioning GPCR with direct autoimmune biology in EAE/MS, IBD/colitis, RA models, and lupus. It is not clean whitespace:

- **Clinical blocker:** IPG11406, an oral GPR183 antagonist, is already in human testing: completed Phase 1 healthy-volunteer study, recruiting Phase Ib/IIa lupus nephritis, and planned/not-yet-recruiting Phase 2 ulcerative colitis.
- **Patent blocker:** both old Sanford-Burnham EBI2-modulator patents and newer Immunophage GPR183-inhibitor filings claim autoimmune uses, including MS, RA, T1D, lupus, IBD/UC and broad autoimmune disease.
- **Directionality blocker:** most EAE/IBD/RA evidence supports antagonism or ligand-axis inhibition, but SLE has conflicting cell/time context: macrophage EBI2 signaling can suppress IFN/inflammatory cytokines, while early female B-cell GPR183 responses can promote lupus-like disease.
- **Translation blocker:** MS/EAE antagonist rationale is strong for immune-cell trafficking, but CNS biology also includes glial EBI2/remyelination data where persistent antagonism may impair repair.

Evidence status: **BLOCKED_BY_PRIOR_ART / TRANSLATIONALLY_DIRECTIONALITY_RISKED** for broad autoimmune positioning. Possible deltas are narrow and biomarker-defined, not generic GPR183 antagonism.

## Mechanism Anchor

GPR183/EBI2 is activated by oxysterols, especially 7alpha,25-OHC. Canonical ligand production is cholesterol -> 25-hydroxycholesterol via **CH25H**, then 7alpha,25-OHC via **CYP7B1**; degradation/inactivation is via **HSD3B7**. Foundational structural and biology papers:

- Hannedouche et al., Nature 2011, identified 7alpha,25-OHC as a potent/selective EBI2 agonist and showed Ch25h-dependent immune-cell positioning. PMID: 21796212, DOI: 10.1038/nature10280. Link: https://pmc.ncbi.nlm.nih.gov/articles/PMC4297623/
- Chen et al., Structure 2022, solved EBI2/GPR183 structures with endogenous agonist 7alpha,25-OHC and inverse agonist GSK682753A. PMID: 35537452, DOI: 10.1016/j.str.2022.04.006. Link: https://pubmed.ncbi.nlm.nih.gov/35537452/
- ChEMBL target search confirms GPR183 as a single-protein GPCR target, CHEMBL3259470. No ChEMBL molecule record for IPG11406 was found in this pass.

## Clinical Landscape

| Agent | Modality/direction | Trial | Status as checked | Indication | Notes |
|---|---|---:|---|---|---|
| IPG11406 | oral GPR183 antagonist | NCT06255834 | completed; results posted 2026-04-17 | healthy volunteers / listed condition IBD | Phase 1 SAD/MAD; 66 actual enrollment. Registry explicitly describes IPG11406 as a GPR183 antagonist. |
| IPG11406 | oral GPR183 antagonist | NCT06717815 | recruiting; start 2025-02-25 | lupus nephritis | Phase Ib/IIa, 36 estimated; includes biomarkers, SLEDAI-2K, cytokines, lymphocyte subsets, proteinuria/renal endpoints. |
| IPG11406 | oral GPR183 antagonist | NCT07535489 | not yet recruiting; posted 2026-04-17; estimated start 2026-07-07 | moderately to severely active UC | Phase 2, 144 estimated, 10/20/40 mg BID vs placebo, Week 12 modified Mayo clinical remission primary endpoint. |

ClinicalTrials links: https://clinicaltrials.gov/study/NCT06255834, https://clinicaltrials.gov/study/NCT06717815, https://clinicaltrials.gov/study/NCT07535489

Blocker implication: broad “GPR183 antagonist for autoimmune/IBD/lupus” is already clinically occupied.

## Closest Prior Art

### Broad EBI2/GPR183 autoimmune modulation

- **WO2015048570A2, "EBI2 modulators"**; Sanford-Burnham, priority 2013-09-26. Explicitly claims EBI2 modulator compounds for autoimmune disease, including **type 1 diabetes, multiple sclerosis, rheumatoid arthritis, and lupus**. Link: https://patents.google.com/patent/WO2015048570A2/en
- **US10196369B2, "Spirocyclic EBI2 modulators"**; Sanford-Burnham, active grant from the same family. Claims treatment of autoimmune disease in humans, including **T1D, MS, RA, and lupus**. Link: https://patents.google.com/patent/US10196369B2/en

### Newer GPR183 antagonist/IPG11406-like space

- **WO2023066190A1, "Compounds and their uses as GPR183 inhibitors"**; Nanjing Immunophage, priority 2021-10-18. Abstract/field states GPR183 inhibitors for treatment or prevention of cancers, **autoimmune diseases**, pain, and osteoporosis. Link: https://patents.google.com/patent/WO2023066190A1/en
- **WO2024208303A1, "Compounds and their uses as GPR183 inhibitors"**; Nanjing Immunophage continuation/follow-on family, priority 2021-10-18/related family. Relevant because it tracks the same clinical sponsor and inhibitor route. Link: https://patents.google.com/patent/WO2024208303A1/en
- **WO2024067810A1, "Anti-GPR183 antibodies and uses thereof"**; Immunophage-associated inventors, priority 2022-09-29. Antibody-space prior art against GPR183. Google Patents currently lists legal status as ceased, but it still counts as disclosure. Link: https://patents.google.com/patent/WO2024067810A1/en
- **US11919895B2, "GPR183 antagonists for the treatment of pain"**; Saint Louis University, active, expires listed 2041-09-18; not autoimmune-primary but includes autoimmune neuropathy language and reinforces antagonist chemistry crowding. Link: https://patents.google.com/patent/US11919895B2/en

## Disease Evidence

### MS / EAE

Direct preclinical evidence is already published.

- Chalmin et al., J Autoimmun 2015, "Oxysterols regulate encephalitogenic CD4+ T cell trafficking during central nervous system autoimmunity." PMID: 25456971, DOI: 10.1016/j.jaut.2014.10.001. In EAE, Ch25h deletion attenuated disease by limiting pathogenic CD4 T-cell trafficking to CNS; 7alpha,25-OHC promoted migration of activated CD44+CD4+ T cells via EBI2. Link: https://pubmed.ncbi.nlm.nih.gov/25456971/
- Wanke et al., Cell Reports 2017, "EBI2 is highly expressed in multiple sclerosis lesions and promotes early CNS migration of encephalitogenic CD4 T cells." PMID: 28147280, DOI: 10.1016/j.celrep.2017.01.020. During EAE, CH25H in microglia and CYP7B1 in CNS-infiltrating immune cells elevated CNS ligand; EBI2 enhanced early migration in transfer EAE but was dispensable in active EAE. Link: https://pubmed.ncbi.nlm.nih.gov/28147280/
- Klejbor et al., Eur J Neurosci 2021, "EBI2 is expressed in glial cells in multiple sclerosis lesions, and its knock-out modulates remyelination in the cuprizone model." PMID: 34145920, DOI: 10.1111/ejn.15359. EBI2 is strong in astrocytes/microglia in MS plaques; EBI2 KO showed less efficient myelin recovery in cuprizone recovery, raising repair-directionality risk. Link: https://pubmed.ncbi.nlm.nih.gov/34145920/
- Caratis et al., PLoS One 2025, "Differential expression and modulation of EBI2 and 7alpha,25-OHC synthesizing/degrading enzymes in mouse and human brain vascular cells." PMID: 39999050, DOI: 10.1371/journal.pone.0318822. Shows brain vascular cell expression of EBI2/CH25H/CYP7B1/HSD3B7 and inflammatory modulation; bioRxiv precursor found as DOI 10.1101/2023.04.16.537063. Link: https://pubmed.ncbi.nlm.nih.gov/39999050/

MS delta left: not "GPR183 antagonism for EAE/MS" generally. Possible deltas would need CNS-penetrant antagonist data, lesion-stage selection, or transient trafficking blockade that avoids remyelination impairment.

### IBD / Crohn / Ulcerative Colitis

This is clinically occupied by IPG11406.

- Emgard et al., Immunity 2018, "Oxysterol Sensing through the Receptor GPR183 Promotes the Lymphoid-Tissue-Inducing Function of Innate Lymphoid Cells and Colonic Inflammation." PMID: 29343433, DOI: 10.1016/j.immuni.2017.11.020. GPR183 drove ILC3 positioning, cryptopatch/ILF formation and inflammation-induced colitis via oxysterol-dependent recruitment. Link: https://pubmed.ncbi.nlm.nih.gov/29343433/
- Ruiz et al., Br J Pharmacol 2021, "A single nucleotide polymorphism in the gene for GPR183 increases its surface expression on blood lymphocytes of patients with inflammatory bowel disease." PMID: 33511653, DOI: 10.1111/bph.15395. Human IBD genetics/surface-expression support. Link: https://pubmed.ncbi.nlm.nih.gov/33511653/
- Verstockt et al., BMJ Open Gastroenterol 2023, IBD circulating immune-cell transcriptomes prioritized GPR183 among drug targets for ileal Crohn disease. PMID: 36746519, DOI: 10.1136/bmjgast-2022-001003. Link: https://pubmed.ncbi.nlm.nih.gov/36746519/
- Ameraoui et al., Cell Mol Life Sci 2025, "Oxysterol-mediated modulation of intestinal inflammation: insights into sex differences and GPR183 signaling." PMID: 41396480, DOI: 10.1007/s00018-025-05981-6. DSS/ex vivo work showed sex-specific oxysterol effects and NIBR189/GPR183 antagonist effects on activation/trafficking. Link: https://pubmed.ncbi.nlm.nih.gov/41396480/

IBD delta left: none for generic UC/IBD antagonist. Potential deltas are Crohn-location stratification, sex-stratified oxysterol biomarker selection, or alternative tissue-local delivery/combinations not covered by IPG11406 claims.

### Rheumatoid Arthritis

- Xi et al., J Med Chem 2023, "Discovery of a First-in-Class GPR183 Antagonist for the Potential Treatment of Rheumatoid Arthritis." PMID: 38047891, DOI: 10.1021/acs.jmedchem.3c01364. Compound 32/IPG11406 had potent/selective GPR183 antagonism and efficacy in mouse collagen-induced arthritis at reported low doses. Link: https://pubmed.ncbi.nlm.nih.gov/38047891/

RA delta left: generic small-molecule antagonist for RA is directly published and patent-crowded. Remaining delta would need a distinct chemotype/FTO, human synovial oxysterol-gradient biomarker, or osteoclast-specific positioning biology not already taught.

### Lupus / Lupus Nephritis

This is active clinically and directionally conflicted.

- Zhang et al., Adv Sci 2023, "The Oxysterol Receptor EBI2 Links Innate and Adaptive Immunity to Limit IFN Response and Systemic Lupus Erythematosus." PMID: 37469011, DOI: 10.1002/advs.202207108. SLE patients had increased plasma 7alpha,25-OHC; 7alpha,25-OHC/EBI2 signaling in macrophages suppressed STAT activation, IFN-beta, chemokines and cytokines; reduced monocyte/macrophage EBI2 associated with enhanced inflammation in models. Link: https://pubmed.ncbi.nlm.nih.gov/37469011/
- Matei et al., iScience 2026, "Sexual dimorphism of early GPR183-dependent B cell responses in systemic lupus erythematosus." PMID: 41816282, DOI: 10.1016/j.isci.2026.114980. Early female lupus-like disease showed increased GPR183+ splenic B cells and migration toward 7alpha,25-OHC; disrupting early, not late, GPR183-dependent responses reduced B-cell activation/disease in female mice. Link: https://pubmed.ncbi.nlm.nih.gov/41816282/
- IPG11406 lupus nephritis trial NCT06717815 is already recruiting.

Lupus delta left: not broad antagonist. A viable evidence delta would need phase/time/cell-state specificity: e.g., early B-cell trafficking antagonism while preserving macrophage EBI2 anti-IFN signaling, or biomarker-selected Th1/Th2-high LN as in the trial entry criteria.

### Psoriasis

Evidence is weak compared with IBD/MS/RA/SLE. GPR183 appears in autoimmune GPCR reviews and older patents list autoimmune diseases broadly; prior IBD SNP paper keywords include psoriasis because UBAC2/GPR183 region is shared in immune genetics, but I did not verify a psoriasis-specific GPR183 interventional paper or trial in this pass.

Delta left: psoriasis-specific claim currently lacks enough direct evidence and is still blocked by broad autoimmune EBI2-modulator patent language.

### Type 1 Diabetes

Old EBI2-modulator patents explicitly claim T1D. Literature located in this pass is mostly broader autoimmune/B-cell GPCR review and metabolic/Gpr183 mouse biology, not a direct T1D therapeutic study. The mechanism could intersect B-cell positioning and immune activation, but T1D as a therapeutic indication is prior-art named.

Delta left: no generic T1D claim; would require beta-cell/islet-local oxysterol mapping or human T1D immune-subset biomarker data.

### Sjogren

No direct GPR183/EBI2 therapeutic paper or trial in Sjogren was verified in this pass. Broad autoimmune GPCR reviews include B-cell GPCR mechanisms, but this is insufficient for Sjogren-specific promotion.

Delta left: primary Sjogren salivary-gland ectopic lymphoid structure/oxysterol-gradient evidence would be needed; otherwise no-go on evidence.

## Directionality Risks

| Context | Direction supported by evidence | Risk |
|---|---|---|
| EAE/MS immune-cell trafficking | inhibit CH25H/7alpha,25-OHC/GPR183 axis to reduce pathogenic T-cell CNS entry | Active EAE dispensability in one model; glial/remyelination data suggest persistent blockade may impair repair. |
| IBD/UC colitis | antagonism reduces inflammatory positioning/recruitment; clinical UC trial already tests this | Mucosal lymphoid-tissue biology could be homeostatic as well as pathogenic; sex-specific oxysterol effects. |
| RA/CIA | antagonism/IPG11406-like compound | Already published; human RA not yet clinically de-risked. |
| SLE macrophages | agonism/preservation of EBI2 signaling may suppress IFN/inflammatory cytokines | Conflicts with IPG11406 antagonist clinical LN route and early female B-cell antagonist rationale. |
| SLE early B-cell responses | antagonism/disruption early in female disease models | Time/sex/cell specificity; late disease effect may differ. |

## Explicit Blockers

- **Clinical blocker:** IPG11406 occupies the exact oral GPR183 antagonist route in UC and lupus nephritis.
- **IP blocker:** WO2015048570A2/US10196369B2 already name T1D, MS, RA, and lupus for EBI2 modulators; WO2023066190A1/WO2024208303A1 cover newer GPR183 inhibitors for autoimmune disease; antibody route has WO2024067810A1 disclosure.
- **Mechanistic novelty blocker:** EAE/MS trafficking, IBD colitis positioning, RA CIA efficacy, and SLE oxysterol/EBI2 biology are all published.
- **Assay/biomarker blocker:** 7alpha,25-OHC is hard to infer from transcriptomics alone because CH25H/CYP7B1/HSD3B7 expression, local cell source, and degradation jointly determine gradient. Direct LC-MS/MS tissue or plasma oxysterol data are needed.
- **Safety/biology blocker:** GPR183 regulates normal B-cell, DC, ILC3, and stromal/lymphoid organization; chronic blockade may alter host defense, gut lymphoid structures, antibody responses, and tissue repair.

## Possible Deltas Worth Keeping As Evidence Hypotheses

These are not findings; they are the narrow spaces not immediately killed by the audit:

1. **MS lesion-stage delta:** transient or lesion-stage-specific GPR183 blockade aimed at early immune entry, explicitly avoiding chronic blockade during remyelination/recovery.
2. **Biomarker delta:** direct 7alpha,25-OHC/25-OHC/CYP7B1/HSD3B7 LC-MS/MS signature plus GPR183+ pathogenic-cell localization, not bulk CH25H/GPR183 expression alone.
3. **SLE cell-state delta:** distinguish early GPR183+ B-cell trafficking from macrophage EBI2 anti-IFN signaling; generic antagonism is directionally unsafe.
4. **Crohn-location delta:** ileal Crohn CD4 T-cell GPR183 program and oxysterol gradient may be distinct from UC, but UC is already clinically occupied.
5. **Sjogren ectopic lymphoid delta:** glandular ectopic lymphoid structures could be a plausible oxysterol-niche setting, but direct evidence was not found here.
6. **Non-orthosteric/biased modulation delta:** biased or partial modulation could be differentiated from IPG11406-like antagonism only if it preserves repair/homeostatic trafficking while blocking pathogenic recruitment.

## Evidence Status by Disease

| Disease | Evidence strength | Main blockers | Evidence-only status |
|---|---:|---|---|
| MS/EAE | High preclinical, moderate human lesion support | old EBI2 modulator patents; remyelination directionality | blocked/crowded; only lesion-stage delta remains |
| IBD/UC/CD | High preclinical + human SNP/expression + active UC trial | IPG11406 Phase 2 UC; Immunophage patents | blocked for broad IBD/UC antagonist |
| RA | Published antagonist chemistry and CIA efficacy | J Med Chem/IPG11406 route and patents | blocked for generic RA antagonist |
| Lupus/LN | Human oxysterol + model biology + active LN trial | IPG11406 LN; SLE directionality conflict | clinically occupied and directionality-risked |
| Psoriasis | Weak/directly unproven | broad autoimmune patent claims | insufficient evidence |
| T1D | Weak direct biology in this pass | named in old EBI2-modulator patents | prior-art named; evidence gap |
| Sjogren | Not verified direct | no disease-specific data found; broad patent crowding | evidence gap/no-go without gland data |

## Final Evidence Call

**BLOCKED_BY_PRIOR_ART / TRANSLATIONALLY_DIRECTIONALITY_RISKED** for broad autoimmune GPR183/EBI2 oxysterol-niche therapeutics.

The strongest evidence-backed route is GPR183 antagonism, but it is already in clinical development for UC and lupus nephritis and supported by prior RA/EAE/IBD publications. The only credible deltas are narrow, biomarker- and tissue-context-defined variants that explicitly avoid replaying IPG11406-style broad antagonism.
