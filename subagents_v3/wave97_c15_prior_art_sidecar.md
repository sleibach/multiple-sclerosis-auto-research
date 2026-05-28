# Wave97 Sidecar: Prior-Art and Translational Audit for C15ORF48-State Proximal Candidates

Timestamp: 2026-05-27 20:44 CEST

Scope: prior-art/translational audit only. I read `results_v3/wave96_c15orf48_controller_search/REPORT.md` and `c15orf48_controller_candidate_rank.tsv`. I did not edit orchestrator files.

## Local Wave96 Context

Wave96 reopened zero C15ORF48 controllers and parked 13 proximal candidates. The relevant local signal is a C15ORF48-positive inflammatory/mitochondrial state, strongest in Crohn/UC colon myeloid and weaker in type 1 diabetes tissue-resident compartments.

Important local caution: a parked Wave96 call is not causality. Most candidates failed MS anchoring, genetics, perturbation, or donor-level validation gates.

## Search Methods

Databases searched: PubMed/web-indexed PubMed, Europe PMC/PMC mirrors, bioRxiv/medRxiv, ClinicalTrials.gov, Google Patents, and EPO/Espacenet-style patent publication pages where surfaced by search.

Search queries used:

- PubMed/Europe PMC: `CCL20 CCR6 multiple sclerosis autoimmune therapy EAE`; `IL23 IL23A multiple sclerosis ustekinumab trial`; `CD200 CD200R multiple sclerosis EAE therapy`; `PLEK2 autoimmune disease`; `LITAF autoimmune rheumatoid arthritis psoriasis inflammatory bowel disease`; `FKBP1A FKBP12 autoimmune tacrolimus rapamycin multiple sclerosis`; `CASP4 autoimmune multiple sclerosis inflammatory caspase inhibitor`; `JAK3 autoimmune disease multiple sclerosis clinical trial`; `IL15 autoimmune multiple sclerosis clinical trial antibody IL15`; `SLPI experimental autoimmune encephalomyelitis multiple sclerosis`; `PIK3R2 autoimmune disease`; `MTHFD2 autoimmune EAE inflammatory bowel disease`; `PDPN podoplanin autoimmune multiple sclerosis EAE`.
- ClinicalTrials.gov: `CCL20 CCR6 autoimmune`; `IL-23 multiple sclerosis ustekinumab`; `CD200R autoimmune multiple sclerosis`; `PLEK2 autoimmune`; `JAK3 autoimmune`; `IL-15 AMG 714 celiac rheumatoid arthritis`; `MTHFD2 inhibitor autoimmune`; `podoplanin PDPN autoimmune`.
- Patents: `CCL20 CCR6 autoimmune disease treatment antibody`; `IL23 autoimmune multiple sclerosis ustekinumab`; `CD200R agonist multiple sclerosis autoimmune treatment`; `JAK3 inhibitor autoimmune disease`; `IL15 autoimmune anti-IL-15 AMG714`; `CASP4 inhibitor autoimmune inflammatory disease`; `MTHFD2 inhibitor autoimmune disease EAE`; `podoplanin PDPN autoimmune disease`.
- C15ORF48 framing: `"C15ORF48" "CCL20"`; `"C15ORF48" "IL23A"`; `"C15ORF48" "CD200"`; `"C15ORF48" "PLEK2"`; `"C15ORF48" "LITAF"`; `"C15ORF48" "FKBP1A"`; `"C15ORF48" "CASP4"`; `"C15ORF48" "JAK3"`; `site:biorxiv.org C15ORF48 autoimmune myeloid`; `site:medrxiv.org C15ORF48 autoimmune myeloid`.

Access note: PubMed/PMC article pages often returned anti-bot interstitials when opened directly, but search-result metadata, PMIDs, ClinicalTrials.gov pages, publisher pages, and patent pages were accessible enough to verify titles and core claims. I did not infer authors or DOIs unless surfaced by an accessible page.

## Summary Calls

| Candidate | Wave96 local status | Closest prior-art status | C15ORF48-state framing | Call |
| --- | --- | --- | --- | --- |
| CCL20/CCR6 | CCL20 parked; CCR6 itself weak/no-go | Directly crowded in EAE/MS biology, PsA clinical plan, anti-CCL20 patents including MS | Specific C15ORF48-state framing not found | NO-GO, novelty blocked |
| IL23A/IL-23 | Parked | Directly crowded; approved drugs, RRMS ustekinumab Phase II negative, patents/trials | Specific C15ORF48-state framing not found | NO-GO, saturated |
| CD200/CD200R | Parked but genetics/perturbation incomplete | Direct EAE/MS CD200R1 agonist prior and broad patents | C15-high lesion/myeloid framing not found | NO-GO for novelty; PARK only as directionality comparator |
| PLEK2 | Parked marker, strong MS expression, no genetics | Little direct autoimmune therapeutic prior | C15ORF48 co-state framing not found | PARK, novelty open but undruggable/marker-like |
| LITAF | Parked, strong C15 co-state/donor support, weak MS | IBD macrophage TNF and inflammatory arthritis genetic deletion prior | C15ORF48 co-state framing not found | PARK/NO-GO, generic TNF upstream and no modality |
| FKBP1A | Parked, many ChEMBL activities, weak MS | Tacrolimus/sirolimus/FKBP12 axis is foundational immunosuppression | No C15 framing found | NO-GO, generic/saturated |
| CASP4 | Parked; C15 co-state but weak MS/genetics | EAE/MS caspase-11/CASP4 biology and emerging inhibitor patents | No C15 framing found | PARK/NO-GO, inflammasome/generic and selectivity risk |
| JAK3 | Parked but MS direction negative in Wave96 | Autoimmune JAK3 inhibitor trials/patents are saturated | No C15 framing found | NO-GO, saturated and wrong local MS direction |
| IL15 | Parked but weak MS anchor | MS/EAE biology plus anti-IL-15 trials in RA/celiac | No C15 framing found | NO-GO, saturated |
| SLPI | Parked but MS direction negative | Direct EAE intervention prior | No C15 framing found | NO-GO, direct prior and opposite local MS direction |
| PIK3R2 | Parked marker; weak MS/genetics | PI3K autoimmune field saturated, but PIK3R2-specific autoimmune prior sparse | No C15 framing found | PARK weak, no selectivity/modality |
| MTHFD2 | Parked; weak MS/genetics | Direct EAE/autoimmune MTHFD2 inhibitor prior and RA paper | No C15 framing found | NO-GO for broad autoimmunity; PARK only for C15-stratified biomarker |
| PDPN | Parked marker; weak MS/genetics | MS/EAE/RA podoplanin biology and PDPN/CLEC-2 immunology prior | No C15 framing found | NO-GO/PARK, safety/directionality unresolved |

## Candidate Audits

### CCL20/CCR6

Local signal: CCL20 was one of the strongest parked proximal candidates: C15-positive in 5 contexts across 3 diseases; C15-state Pearson r = 0.711, p = 0.0020; MS delta = 1.147, p = 0.061. CCR6 itself was not a Wave96 parked candidate: C15-positive contexts = 0 and no donor co-state.

Verified closest prior art:

- PubMed: `C-C chemokine receptor 6-regulated entry of TH-17 cells into the CNS through the choroid plexus is required for the initiation of EAE` (PMID 19305396) links CCR6/CCL20 to CNS entry in EAE.
- PubMed: `CCL20/CCR6 chemokine signaling is not essential for pathogenesis in an experimental autoimmune encephalomyelitis mouse model of multiple sclerosis` (PMID 36527746) reports a negative/compensability result.
- ClinicalTrials.gov: `NCT02671188`, GSK3050002 anti-CCL20 in psoriatic arthritis, explicitly describes CCL20/CCR6 recruitment biology; withdrawn before treatment.
- Google Patents: `US8491901B2 Neutralizing anti-CCL20 antibodies` lists autoimmune diseases including RA, psoriasis, Crohn disease, IBD, and multiple sclerosis. `WO2017064564A2` covers psoriatic arthritis regimens with anti-CCL20 antibody/GSK3050002.

Delta: The C15ORF48-high myeloid/epithelial state framing was not found in those sources. However, therapeutic use of CCL20/CCR6 blockade in autoimmune disease and MS is already explicit. Local data also warns that CCR6 receptor expression did not share the C15 state.

Call: **NO-GO, novelty blocked.** Only possible use is as a positive-control chemokine axis for a C15-state map.

### IL23A / IL-23 Axis

Local signal: IL23A parked; C15-positive in 4 contexts across 4 diseases; C15-state Pearson r = 0.538, p = 0.0258; MS delta = 0.657, p = 0.092; Wave68 remission-adjusted FDR = 0.0297 but genetics failed.

Verified closest prior art:

- Lancet Neurology/ScienceDirect: `Repeated subcutaneous injections of IL12/23 p40 neutralising antibody, ustekinumab, in patients with relapsing-remitting multiple sclerosis: a phase II, double-blind, placebo-controlled, randomised, dose-ranging study`; search metadata reports 249 RRMS patients and no significant reduction in the primary endpoint versus placebo.
- ClinicalTrials.gov: `NCT00207727`, CNTO1275/ustekinumab in multiple sclerosis, with posted results.
- PubMed: `A phase I trial of an interleukin-12/23 monoclonal antibody in relapsing multiple sclerosis` (PMID 16968570).
- Google Patents: `US20150147337A1 Crystalline anti-human IL-23 antibodies`; `WO2023288028A2 Peptide inhibitors of interleukin-23 receptor`, explicitly discusses IL-23 in autoimmune inflammation and lists MS/RA/psoriasis/IBD.
- Established clinical landscape: IL-12/23 or IL-23 drugs are approved across psoriasis, psoriatic arthritis, Crohn disease, and ulcerative colitis.

Delta: I found no C15ORF48-state-specific IL23A therapeutic framing. That delta is too narrow to rescue novelty because IL-23 is one of the most saturated autoimmune axes, and MS already has negative clinical trial history.

Call: **NO-GO, saturated and prior-art blocked.**

### CD200 / CD200R

Local signal: CD200 parked; C15-positive in 4 contexts across 3 diseases; MS delta = 1.838, p = 0.091; donor co-state positive in 2 contexts across 2 diseases; genetics failed.

Verified closest prior art:

- PubMed/PMC: `CD200R1 agonist attenuates mechanisms of chronic disease in a murine model of multiple sclerosis` (PMID 20147531). Search metadata reports CD200Fc treatment during chronic EAE reduced disease severity, demyelination, axonal damage, macrophage/microglial accumulation, cytokines, and oligodendrocyte apoptosis.
- Review prior art: `CD200-CD200R signaling and diseases: a potential therapeutic target?` discusses CD200-CD200R as a therapeutic target.
- Google Patents/EPO-style result: AU patent document surfaced with claims around treating immune conditions via CD200R agonist/antagonist and disease examples including RA, diabetes, MS, and autoimmune thyroiditis.

Delta: A C15ORF48-positive lesion/myeloid-state-specific CD200/CD200R agonism frame was not found. But the core MS/EAE CD200R1 agonist therapeutic concept is directly published.

Call: **NO-GO for novelty.** PARK only as a comparator/checkpoint in C15-high state directionality experiments, because CD200 ligand upregulation may be compensatory rather than causal.

### PLEK2

Local signal: PLEK2 parked; strong MS expression anchor (MS delta = 3.046, p = 0.0074), C15-positive in 4 contexts across 3 diseases, C15-state Pearson r = 0.589, p = 0.0129. It failed genetics, perturbation, and modality gates.

Verified closest prior art:

- PubMed/PMC review: `Emerging Roles of Pleckstrin-2 Beyond Cell Spreading` indicates PLEK2 biology is mostly cytoskeletal/cancer/hematologic rather than autoimmune.
- Patent search surfaced PLEK2 therapeutic use mainly in myeloproliferative/JAK2-STAT5 contexts, not autoimmune.
- I did not find credible PLEK2 therapeutic prior art for MS/autoimmune disease.

Delta: The C15ORF48-positive autoimmune myeloid state association appears unpublished from the searches run. This is the cleanest novelty gap among the named candidates.

Call: **PARK, not GO.** Novelty is not the blocker; biology/actionability is. Without a selective modality or perturbation data, PLEK2 is a state marker, not a translational intervention point.

### LITAF

Local signal: LITAF parked; C15-positive in 5 contexts across 3 diseases; C15-state Pearson r = 0.717, p = 0.00119; strong donor co-state validation (5 donor-case positive contexts, 3 diseases, median Spearman = 0.90). It failed MS anchor and genetics.

Verified closest prior art:

- PubMed: `LITAF mediation of increased TNF-alpha secretion from inflamed colonic lamina propria macrophages` (PMID 21984950), directly places LITAF in inflamed IBD macrophage TNF production.
- PubMed: `Whole-body deletion of LPS-induced TNF-alpha factor (LITAF) markedly improves experimental endotoxic shock and inflammatory arthritis` (PMID 22160695).
- UniProt: LITAF localizes to lysosomal/endosomal membranes, matching the lipid-lysosomal module but not proving targetability.

Delta: I found no direct C15ORF48-state LITAF therapeutic framing. The closest prior art is still mechanistically close: LITAF as a macrophage TNF regulator in IBD and inflammatory arthritis.

Call: **PARK/NO-GO.** It is mechanistically coherent but too close to generic TNF biology, intracellular/transcriptional/endosomal, and currently lacks a selective drugging modality. It is a useful C15-state controller hypothesis for perturbation, not a near-term drug target.

### FKBP1A

Local signal: FKBP1A parked; C15-positive in 6 contexts across 3 diseases; C15-state Pearson r = 0.456, p = 0.066; MS delta negative/non-supportive (-0.335, p = 0.239); ChEMBL activity count high.

Verified closest prior art:

- PMC review: `FK506-Binding Proteins and Their Diverse Functions` states FKBP12/FKBP1A is the target of FK506/tacrolimus and rapamycin/sirolimus complexes.
- Nature Reviews Immunology: mTOR inhibition by rapamycin-FKBP12 is a canonical immunoregulation mechanism.
- EAE/NFAT literature uses calcineurin inhibition/tacrolimus-class biology in autoimmune neuroinflammation models.

Delta: A C15ORF48-state-specific FKBP1A role was not found. The core biology is not novel; it is one of the oldest immunosuppression axes.

Call: **NO-GO, generic/saturated.** No therapeutic novelty and no C15-selective rationale.

### CASP4

Local signal: CASP4 parked; C15-positive in 6 contexts across 3 diseases; C15-state Pearson r = 0.392, p = 0.120; Wave68 remission-adjusted FDR = 0.028; MS/genetics weak.

Verified closest prior art:

- PubMed: `Caspase-11 mediates oligodendrocyte cell death and pathogenesis of autoimmune-mediated demyelination` (PMID 11136825), relevant because mouse caspase-11 is the noncanonical inflammatory caspase axis related to human CASP4/5.
- UniProt: CASP4 acts as an inflammatory caspase for noncanonical inflammasome/LPS-induced pyroptosis.
- WIPO/Patentscope: `WO2026055444 CASPASE-4 INHIBITORS AND USES THEREOF` surfaced as active inhibitor patent prior art.
- Broader NLRP3/caspase inflammasome inhibitor field is saturated in inflammatory disease.

Delta: C15ORF48-state-specific CASP4 targeting in autoimmune myeloid cells was not found. But the inflammatory caspase/demyelination and inhibitor-prior landscape is close enough that general autoimmune/MS novelty is weak.

Call: **PARK/NO-GO.** Could be tested as a C15-high pyroptosis-state biomarker, but not a clean therapeutic nomination without CASP4-vs-CASP1/CASP5 selectivity and disease-specific genetics.

### JAK3

Local signal: JAK3 parked but locally adverse for MS target logic: MS delta = -1.274, p = 0.015, while C15-positive in 5 contexts across 4 diseases. Very high ChEMBL activity count.

Verified closest prior art:

- PubMed: `Recent patents in the discovery of small molecule inhibitors of JAK3` (PMID 20402545) states JAK3 inhibitors have utility in multiple autoimmune disorders.
- ClinicalTrials.gov: `NCT01590459`, VX-509 selective JAK3 inhibitor in RA, describes broad autoimmune rationale.
- ClinicalTrials.gov documents for ritlecitinib/PF-06651600 list selective covalent JAK3/TEC-family inhibitor programs across autoimmune indications including alopecia areata, vitiligo, UC, Crohn disease, and RA.
- ClinicalTrials.gov: `NCT02535689`, tofacitinib in systemic lupus erythematosus.

Delta: No C15ORF48-state-specific JAK3 therapeutic frame found. But JAK3 is a saturated immunology target and the local MS direction is negative.

Call: **NO-GO, saturated and locally directionally wrong.**

### IL15

Local signal: IL15 parked; C15-positive in 5 contexts across 4 diseases; MS delta = 1.196, p = 0.123; donor support limited; genetics failed.

Verified closest prior art:

- PubMed/PMC: `IL-15 mRNA expression is up-regulated in blood and cerebrospinal fluid mononuclear cells in multiple sclerosis`.
- PubMed/PMC: `Interleukin-15 enhances proinflammatory T-cell responses in patients with MS and EAE`.
- ClinicalTrials.gov: `NCT00433875`, AMG 714 anti-IL-15 mAb Phase 2 in rheumatoid arthritis, enrollment 180.
- ClinicalTrials.gov: `NCT02637141`, AMG 714 in adult celiac disease, results posted; `NCT02633020`, AMG 714 in type II refractory celiac disease.
- Amgen/Provention materials and Guide to Pharmacology identify AMG714/ordesekimab/PRV-015 as an anti-IL-15 antibody developed for celiac disease; prior RA/psoriasis development was discontinued after disappointing studies.

Delta: No C15ORF48-state-specific IL15 framing found. The autoimmune therapeutic concept is heavily prior-arted.

Call: **NO-GO, saturated.**

### SLPI

Local signal: SLPI parked but local MS direction is negative: MS delta = -2.815, p = 0.017. C15-positive in 5 contexts across 3 diseases; C15-state Pearson r = 0.573, p = 0.016.

Verified closest prior art:

- BMC Neuroscience/Springer: `Inhibition of SLPI ameliorates disease activity in experimental autoimmune encephalomyelitis` (2012). The accessible page reports that SLPI vaccination/neutralization reduced EAE severity and delayed onset, and recombinant SLPI worsened disease.
- Journal of Neuroinflammation/PMC: `Novel role for SLPI in MOG-induced EAE revealed by spinal cord expression analysis` (2008).

Delta: C15ORF48-specific state framing was not found. The direct EAE therapeutic prior is too close, and local MS expression direction is opposite to a simple replacement/agonism strategy.

Call: **NO-GO.** Potentially useful as a sanity-check marker for an EAE-like inflammatory state, not a novel therapeutic route.

### PIK3R2

Local signal: PIK3R2 parked; C15-positive in 4 contexts across 3 diseases; MS delta = -0.040, p = 0.847; no genetics; ChEMBL activity count high due PI3K-family chemistry.

Verified closest prior art:

- PMC review: `The Therapeutic Potential for PI3K Inhibitors in Autoimmune Rheumatic Diseases` discusses PI3K inhibition, especially p110gamma/p110delta, in RA and SLE.
- PubMed/Gene searches did not surface a convincing PIK3R2-specific autoimmune therapy prior.
- Patent searches surfaced broad PI3K inhibitor chemistry rather than PIK3R2-selective autoimmune claims.

Delta: The C15ORF48-state/PIK3R2 association appears unpublished, but PIK3R2 is a regulatory subunit without a clean isoform-selective intervention concept. Pan-PI3K immunomodulation is crowded and toxicity-prone.

Call: **PARK weak.** No current go: insufficient MS anchor, no PIK3R2-specific druggability path, and generic PI3K prior art.

### MTHFD2

Local signal: MTHFD2 parked; C15-positive in 4 contexts across 3 diseases; C15-state Pearson r = 0.333, p = 0.192; MS delta = 0.046, p = 0.815; Wave18 had foundation support but explicitly `do_not_promote_from_foundation_model`.

Verified closest prior art:

- PMC/Springer: `MTHFD2 is a Metabolic Checkpoint Controlling Effector and Regulatory T Cell Fate and Function` reports MTHFD2 upregulation in CNS-infiltrating CD4 T cells in EAE and MTHFD2 inhibitor use in T-cell differentiation contexts.
- PMC/Springer: `MTHFD2 promotes osteoclastogenesis and bone loss in rheumatoid arthritis by enhancing CKMT1-mediated oxidative phosphorylation` reports elevated MTHFD2 in RA CD14+ monocytes and CIA mice and inhibitor/knockdown effects on osteoclastogenesis/bone loss.
- Reviews: `MTHFD2: a promising metabolic checkpoint for diseases` and `MTHFD2 in healthy and cancer cells` discuss inflammatory/autoimmune MTHFD2 inhibitor evidence including EAE and delayed-type hypersensitivity.
- Google Patents: `WO2017023894A1 MTHFD2 inhibitors and uses thereof`.

Delta: A C15ORF48-positive myeloid-state-stratified MTHFD2 hypothesis was not found. But broad autoimmune/EAE MTHFD2 inhibition is directly prior-arted, and local MS evidence is weak.

Call: **NO-GO for broad autoimmune/MS therapeutic novelty. PARK only as a C15-high stratification/metabolic-state biomarker if later data show cell-type specificity.**

### PDPN

Local signal: PDPN parked; C15-positive in 4 contexts across 2 diseases; MS delta = 0.165, p = 0.497; no genetics; some residual tissue signal but weak donor co-state.

Verified closest prior art:

- PubMed: `Inflammation induces neuro-lymphatic protein expression in multiple sclerosis brain neurovasculature` (PMID 24124909) links podoplanin-positive Th17/TLO biology to MS/EAE.
- PubMed/PMC: `The Role of Podoplanin in the Immune System and Inflammation` reviews PDPN in MS, RA, EAE, HEV, FLS, and immune regulation.
- PubMed: `Distribution of Podoplanin in Synovial Tissues in Rheumatoid Arthritis Patients Using Biologic or Conventional Disease-Modifying Anti-Rheumatic Drugs` (PMID 27030253).
- PubMed/PMC: `C-type lectin-like receptor 2: roles and drug target` and `CLEC-2 Prevents Accumulation and Retention of Inflammatory Macrophages During Murine Peritonitis` establish PDPN/CLEC-2 as an immuno-thromboinflammatory axis.
- Google Patents/PubChem: anti-podoplanin antibody patents exist, though mostly oncology/PDPN-directed rather than C15 autoimmune state specific.

Delta: C15ORF48-state-specific PDPN targeting was not found. But PDPN in MS/EAE/RA inflammation is already published, and platelet/CLEC-2/lymphatic biology creates safety and directionality risk.

Call: **NO-GO/PARK.** Not a clean therapeutic target without tissue-restricted modulation and proof that blocking vs agonizing PDPN/CLEC-2 helps the C15 state.

## Cross-Candidate Conclusion

The specific phrase-level framing "C15ORF48-positive autoimmune myeloid state proximal controller" appears unpublished from the searches run. That does not create a promotable therapeutic target among this set. The candidates split into two groups:

1. **Prior-art blocked/saturated:** CCL20/CCR6, IL23A/IL-23, CD200/CD200R, FKBP1A, JAK3, IL15, SLPI, MTHFD2, and probably PDPN for general autoimmune use.
2. **Novelty-open but not druggable enough:** PLEK2, LITAF, PIK3R2, with CASP4 partly in between because CASP4 inhibitor patents and EAE caspase biology are already close.

No candidate earns a Wave97 GO call for a novel MS/autoimmune therapeutic use. The most defensible next-step experiments, if the orchestrator wants to continue the C15 branch, are perturbation-first rather than prior-art-first:

- **LITAF:** CRISPRi or degron perturbation in primary human inflammatory macrophages/organoids to test whether C15ORF48, CCL20, IL23A, CASP4, and TNF module output falls without global macrophage collapse.
- **PLEK2:** CRISPRi perturbation in C15-high myeloid cells to test whether it is merely a cytoskeletal marker or a state-maintenance dependency.
- **MTHFD2:** not novel as a general target, but possible as a comparator for whether C15-high myeloid cells share the published EAE/T-cell metabolic checkpoint or represent a different one-carbon/metabolic state.

