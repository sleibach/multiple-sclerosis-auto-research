# Wave42-B Hostile Critique: FADS1/FADS2 Lipid-Desaturation Axis

Date: 2026-05-27

Scope: independently assess whether `FADS1/FADS2` desaturation biology can serve as a cross-autoimmune lipid-module intervention point for the V3 autoimmune/MS research branch. This is critique, not a therapeutic finding.

## 1. Verdict

**DEMOTE**

The FADS locus is real lipid biology and `FADS1` is chemically tractable, but it is not promotable as a cross-autoimmune lipid-module intervention point. The blockers are target-level causal ambiguity, directionally conflicting immune-disease genetics, weak local MS/lesion cell-state evidence, no lesion-relevant perturbation support, and nontrivial prior art around FADS1 inhibitor compounds and biomarker-selected FADS1 inhibition.

## 2. Strongest Evidence For The FADS Axis

Local V3 genetics-first signal:

- `results_v3/wave34_genetics_expression_druggability_scan/summary.json` lists `FADS1` among top candidates with `wave34_call=PARK_GENETIC_DRUGGABLE_NEEDS_CELL_STATE`, `gwas_catalog_trait_count=9`, ChEMBL activity count `61`, and `chembl_best_nM=0.52`.
- `results_v3/wave34_genetics_expression_druggability_scan/wave34_genetics_expression_druggability_rank.tsv` shows broad GWAS Catalog mapped-gene recurrence for `FADS1`: atopic dermatitis, Crohn's disease, IBD, RA/hypothyroidism pleiotropy, T1D, UC, vitiligo, and psychiatric/IBD MTAG traits. `FADS2` has similar recurrence with `gwas_catalog_trait_count=10`.
- Local cross-disease expression is not absent: `FADS1` is positive in psoriasis and UC; `FADS2` is positive in Crohn disease and UC in the wave34 row. This is weak because it is not MS-driven and not retained after residual module gates.

Biological plausibility:

- Human metabolomics strongly supports the FADS locus as a major controller of long-chain PUFA-containing lipids. A Scientific Reports metabolomic/genetic analysis found FADS-locus variation associated with 52 LC-PUFA-containing lipids and signaling molecules, and identified FADS1/FADS2 as rate-limiting delta-5/delta-6 desaturases in the pathway. Source: https://www.nature.com/articles/s41598-020-71948-1
- The pathway sits directly upstream of arachidonic-acid, EPA/DHA, eicosanoid, endocannabinoid, phospholipid, and lyso-phospholipid biology. That is at least conceptually adjacent to the V3 lipid/lysosomal inflammatory module.
- In Crohn's disease mesenteric adipose tissue, reduced `FADS2` expression/activity was linked to impaired n-3/n-6 desaturation flux; restoring `FADS2` reduced pro-inflammatory macrophage infiltration and inflammatory cytokine/adipokine expression in the authors' systems. This is the strongest disease-mechanistic prior art, but it supports **FADS2 restoration**, not FADS1 inhibition. Source: https://academic.oup.com/ecco-jcc/article/14/11/1581/5828999
- A 2025 psoriasis study reports `PPARA`-orchestrated `FADS2` fatty-acid metabolism in keratinocyte skin inflammation, reinforcing that FADS biology is tissue-specific and already visible in inflammatory skin disease. Source: https://doi.org/10.1002/advs.202417049

Druggability:

- ChEMBL identifies human `FADS1` as `CHEMBL5840`, "Acyl-CoA (8-3)-desaturase", with delta-5 desaturase synonyms and lipid/eicosanoid GO annotations. ChEMBL activity records include cell-based delta-5 desaturase inhibition assays in HepG2 cells. Source/API: `https://www.ebi.ac.uk/chembl/api/data/target/CHEMBL5840.json`
- AMG 786 has a completed Phase 1 study in healthy participants/obesity (`NCT05406115`), showing industry-grade clinical interest in a systemic lipid-metabolism modulator. The ClinicalTrials.gov record does not state the target as FADS1, so target identity should not be asserted from the registry alone. Source: https://clinicaltrials.gov/study/NCT05406115

## 3. Strongest Reasons It Fails

1. **The cross-autoimmune direction is not coherent.** A 2026 Scientific Reports immune-disease MR target-prioritization paper explicitly reports opposite direction of effect across IMDs for `FADS1`, alongside `IL3`, `CSF2`, and `PPARG`, and states this indicates lack of feasibility for drug repurposing and possible adverse side effects. It reports `FADS1` shared between IBD and asthma in eosinophil-count-instrumented, coloc-supported results, but direction discordance blocks a shared intervention direction. Source: https://www.nature.com/articles/s41598-026-41818-3

2. **The strongest disease-mechanistic paper points to `FADS2` restoration, not FADS inhibition.** The Crohn's mesenteric adipocyte study frames decreased `FADS2` as pathogenic and rescue by `FADS2` overexpression/AAV as anti-inflammatory. That contradicts a naive "block desaturation" strategy and does not provide a small-molecule restoration modality.

3. **Local MS lesion evidence is weak or directionally wrong.** Wave34 shows no MS anchor for either gene. `FADS1` has `ms_wm_delta_log2=-0.558`, nominal `p=0.0303`; `FADS2` has `ms_wm_delta_log2=-1.512`, `p=0.130`. In `results/mims2_like_all_gene_state_statistics.tsv`, both `FADS1` and `FADS2` are slightly lower in reconstructed MIMS2-like microglia versus HMG-like cells, not elevated in the promoted lesion lipid state. This argues against an expression-up intervention target in foamy MS microglia.

4. **FADS1 and FADS2 are locus-coupled and biology-coupled.** The GWAS signal is a chromosome 11 FADS cluster signal, not clean target-resolved evidence. Without fine-mapping/colocalization that separates `FADS1`, `FADS2`, `FADS3`, regulatory haplotypes, diet interaction, and lipid mediator traits, "FADS mapped gene recurrence" is not a target claim.

5. **Prior art is already close.** Amgen has active/published patent families for heterocyclic delta-5 desaturase inhibitors and biomarker-selected FADS1 inhibitor treatment of FADS1-mediated diseases using PUFA ratios, cell types, DEGs/signatures, and metabolites. That is close to a biomarker-selected FADS1 lipid-intervention thesis even if autoimmune/MS is not named. Sources: https://patents.google.com/patent/US12448396B2/en and https://patents.google.com/patent/WO2024112763A1/en

6. **Clinical/dietary prior art has already tested PUFA manipulation in MS.** The OFAMS randomized MS trial found increased serum omega-3 fatty acids but no beneficial effect on MS disease activity versus placebo. This does not falsify genotype-selected FADS pharmacology, but it blocks any broad "PUFA axis improves MS" story. Source: https://jamanetwork.com/journals/jamaneurology/fullarticle/1151851

7. **Safety is not a detail.** FADS1/FADS2 alter essential long-chain PUFA pools used in brain, immune, liver, skin, cardiovascular, reproductive, and developmental biology. Broad systemic inhibition risks shifting arachidonic-acid, DGLA, EPA/DHA, prostaglandin, thromboxane, leukotriene, endocannabinoid, membrane, and myelin lipid composition. The V3 branch has already rejected lipid targets when myelin-debris clearance and repair safety were unresolved; FADS is broader than ACSL1, not narrower.

8. **No direct lesion-relevant perturbation evidence.** Wave34 marks `perturbation_or_model_support=False` for both `FADS1` and `FADS2`. I found no evidence that FADS1 inhibition or FADS2 restoration reverses the MS chronic-active-lesion microglial lipid/lysosomal program, PRL biology, or cross-autoimmune myeloid module in a disease-relevant human system.

## 4. Closest Prior Art And Searches

Public searches run or checked on 2026-05-27:

PubMed:

- Query: `(FADS1 OR FADS2 OR "fatty acid desaturase") AND (autoimmune OR "multiple sclerosis" OR rheumatoid OR lupus OR Crohn OR colitis OR psoriasis OR "type 1 diabetes")`
  - Result count from NCBI ESearch: `54`.
- Query: `(FADS1 OR FADS2 OR "fatty acid desaturase") AND ("multiple sclerosis" OR EAE OR demyelination OR microglia)`
  - Result count from NCBI ESearch: `7`.
- Query: `(FADS1 OR FADS2 OR "fatty acid desaturase") AND (inhibitor OR inhibition OR agonist OR overexpression OR knockdown) AND (autoimmune OR Crohn OR psoriasis OR "multiple sclerosis")`
  - Result count from NCBI ESearch: `9`.

Europe PMC:

- Query: `(FADS1 OR FADS2 OR "fatty acid desaturase") AND (autoimmune OR "multiple sclerosis" OR rheumatoid OR lupus OR Crohn OR colitis OR psoriasis OR "type 1 diabetes")`
  - Result count: `1691`.
  - Top relevant/current hit: Sobczyk and Gaunt 2026, integrative MR target prioritization in immune-mediated diseases; flags `FADS1` direction discordance across IMDs. https://www.nature.com/articles/s41598-026-41818-3

ClinicalTrials.gov:

- Query: `FADS1 OR FADS2 OR "delta-5 desaturase" OR "fatty acid desaturase 1" OR "fatty acid desaturase 2"`
  - Returned `NCT04555044`, a completed pediatric essential fatty acid deficiency/parenteral nutrition trial with `FADS1 and FADS2` as keywords; not an autoimmune intervention trial.
- Query: `"AMG 786" OR "delta-5 desaturase inhibitor" OR "D5D inhibitor"`
  - Returned `NCT05406115`, completed Phase 1 AMG 786 study in healthy participants and obesity; not autoimmune/MS.

Patents:

- Query: `Google Patents FADS1 inhibitor autoimmune disease delta 5 desaturase`
  - Closest: Amgen `US12448396B2`, "Methods of using heterocyclic compounds as Delta-5 Desaturase inhibitors"; active, publication 2025-10-21, anti-inflammatory/metabolic classifications. https://patents.google.com/patent/US12448396B2/en
- Query: `site:patents.google.com "FADS1" "FADS1 inhibitor" "PUFA ratio"`
  - Closest: Amgen `WO2024112763A1`, "Selection of patients for the treatment of fads1-mediated diseases or disorders using fads-1 inhibitors"; uses PUFA ratios including AA:DGLA, cell types, DEG/gene signatures, and metabolites as selection biomarkers. https://patents.google.com/patent/WO2024112763A1/en
- Query: `site:patents.google.com delta-5 desaturase inhibitor inflammatory disease`
  - Closest older art: `US20190070193A1`, "Compound for inhibition of delta-5-desaturase (D5D) and treatment of cancer and inflammation." https://patents.google.com/patent/US20190070193A1/en
- Query: `site:patents.google.com "FADS1" "multiple sclerosis"` and `site:patents.google.com "delta-5 desaturase" "multiple sclerosis"`
  - No direct MS-specific FADS1 inhibitor patent surfaced in accessible search results, but absence of direct MS wording does not rescue novelty because the broad FADS1 inhibitor/biomarker-selection claims are already close.

Closest literature/prior-art interpretation:

- **Mechanism prior art:** FADS locus controls PUFA/lipid mediator pools; this is established and not novel.
- **Autoimmune/disease prior art:** Crohn's and psoriasis already tie `FADS2` to tissue inflammation; immune-disease MR already identifies `FADS1` but warns about direction discordance.
- **Intervention prior art:** FADS1 inhibitor chemistry and biomarker-selected FADS1 inhibition are already active/patented. MS-specific FADS pharmacology was not found, but the broad concept is not clean white space.

## 5. Exact Evidence Required To Revive

Revival should require all of the following, not just one:

1. **Target-resolved genetics**
   - Fine-mapped, ancestry-aware colocalization separating `FADS1`, `FADS2`, `FADS3`, and neighboring regulatory haplotypes across at least four autoimmune diseases.
   - Direction of effect must be concordant for the same biochemical exposure, e.g. lower AA:DGLA or lower FADS1 activity is protective in the intended diseases, without opposite-direction hits in major autoimmune comparators.
   - MR should use lipid mediator instruments, eQTL/sQTL, pQTL where available, and disease outcomes; Steiger direction, horizontal pleiotropy, and diet/ancestry interaction must be explicitly tested.

2. **MS lesion relevance**
   - PRL/chronic-active-lesion tissue must show a FADS-linked lipid mediator state, not merely `FADS1/FADS2` expression. Required readout: lesion-rim myeloid or glial AA:DGLA/EPA/DHA/eicosanoid/SPM pattern associated with active rim expansion or disability.
   - FADS risk haplotypes must predict the lesion lipid state or PRL burden in human MS cohorts after controlling for ancestry, diet, BMI, statin/NSAID use, smoking, and DMT exposure.

3. **Cell-type and direction clarity**
   - Define whether the intended intervention is `FADS1` inhibition, `FADS2` restoration, substrate supplementation, or downstream lipid-mediator rescue.
   - Demonstrate the causal cell type: microglia/macrophage, adipocyte/stromal, keratinocyte/epithelial, T cell, B cell, or hepatocyte-driven systemic lipid effect. A cross-autoimmune claim cannot mix Crohn adipocytes, psoriasis keratinocytes, and MS microglia without showing a shared lipid-state mechanism.

4. **Perturbation in human disease-relevant systems**
   - In human iPSC microglia or primary macrophage/myelin-debris systems, FADS intervention must reduce the V3 lipid/lysosomal inflammatory module by at least `30%` while preserving phagocytosis, lysosomal acidification, myelin processing, oligodendrocyte support, and axonal survival.
   - In non-MS autoimmune tissue models, the same biochemical direction must reduce disease-relevant inflammatory readouts in at least three indications without requiring opposite pharmacology.

5. **Safety and pharmacology package**
   - Demonstrate partial, reversible modulation with measured lipidomic target engagement: AA:DGLA, EPA/DHA, prostaglandins, thromboxanes, leukotrienes, SPMs, endocannabinoids, and membrane phospholipid remodeling.
   - Show CNS exposure or justify a peripheral-only mechanism with human causal data.
   - Predefine stop criteria for impaired myelin repair, neurodevelopment/reproductive toxicity, liver lipid handling, bleeding/thrombosis, infection risk, and mood/neuropsychiatric signals.

6. **Freedom-to-operate differentiation**
   - Any revived claim must distinguish itself from Amgen FADS1 inhibitor and FADS1 biomarker-selection patent families, and from prior broad D5D inflammation patents.
   - A viable novelty lane would likely need a specific MS/PRL lipidomic responder signature, a non-FADS1-inhibitor modality such as `FADS2` restoration in a defined cell type, or a downstream lipid mediator correction not claimed by broad PUFA-ratio FADS1 inhibitor patents.

Stop-loss rule: do not reopen as a therapeutic target if target-resolved genetics remains discordant, if MS lesion lipidomics do not point to a FADS-controlled mediator state, or if perturbation requires opposite directions across autoimmune indications.
