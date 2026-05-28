# Wave34-C checkpoint/prior-art sanity check

Timestamp: 2026-05-27 08:18 UTC

Scope: hostile checkpoint/adhesion/tolerance-axis audit for `BTLA/HVEM`, `CD6/ALCAM`, `CD226/TIGIT/PVR/NECTIN2`, `IL7R`, and `BACH2/IKZF`. This is not a finding claim.

## Bottom line

All five axes should be demoted for V3 target-discovery purposes. `CD6/ALCAM` and `IL7R` are translationally real, but that is exactly the problem: both are already in clinical or patent-protected autoimmune development and the local V3 signal does not define a new responder subgroup or disease-specific delta. `BTLA/HVEM` and `CD226/TIGIT/PVR/NECTIN2` have plausible tolerance biology but are crowded, directionally complex checkpoint networks with no sufficient local MS/cross-tissue state anchor. `BACH2/IKZF` is the strongest conceptual tolerance program, but the tractable intervention points either point in the wrong direction for a BACH2-restoration claim or are already occupied by IKZF1/IKZF3 degraders in lupus.

## Local V3 evidence used

- `results_v3/wave33_tolerance_costimulation_audit/tolerance_costimulation_axis_audit.tsv`
- `results_v3/wave33_tolerance_costimulation_audit/tolerance_costimulation_gate_matrix.tsv`
- `results_v3/wave33_tolerance_costimulation_audit/raw_api/`
- `results_v3/wave19_tolerogenic_checkpoint/checkpoint_candidate_synthesis.tsv`
- `results/mims2_like_all_gene_state_statistics.tsv`

Key local gate results:

| Axis | Wave33 call | Local/state issue | Trial count in Wave33 CT.gov query | Europe PMC autoimmune hit count | GWAS Catalog breadth in Wave33 | Local decision |
|---|---:|---|---:|---:|---:|---|
| `BTLA_HVEM_CHECKPOINT` | `NO_GO_TOLERANCE_PRIOR_ART_BLOCKED` | local breadth 3 but state coupling 0; no MS anchor | 1 | 4,154 | 11 trait labels, min p `8e-33` | Demote |
| `CD6_ALCAM_INTERFACE` | `NO_GO_TOLERANCE_PRIOR_ART_BLOCKED` | local breadth 1; MS white-matter delta nominal but no cross-disease cell-state support | 6 | 2,366 | 9 trait labels, min p `2e-29` | Demote as prior-arted clinical mechanism |
| `CD226_TIGIT_PVR_BALANCE` | `NO_GO_TOLERANCE_PRIOR_ART_BLOCKED` | local breadth 2, negative breadth 1, state coupling 0, no MS anchor | 19 | 10,594 | 15 trait labels, min p `7e-16` | Demote |
| `IL7R_TCELL_SURVIVAL` | `NO_GO_TOLERANCE_PRIOR_ART_BLOCKED` | local breadth 3 but negative breadth 2, state coupling 0, no MS anchor | 19 | 13,926 | 14 trait labels, min p `3e-99` | Demote as generic/crowded cytokine axis |
| `BACH2_IKZF_TREG_PROGRAM` | `NO_GO_TOLERANCE_AXIS` | local breadth 1, negative breadth 1, state coupling 0, no MS anchor | 68 | 54,777 | 43 trait labels, min p `9e-60` | Demote as nonselective/non-druggable program |

MS white-matter gene-state check from `results/mims2_like_all_gene_state_statistics.tsv` does not rescue any axis. Examples: `BTLA` mean delta `0.0012`, FDR `0.905`; `TIGIT` mean delta `-1.8e-05`, FDR `1`; `IL7R` mean delta `-0.00034`, FDR `1`; `BACH2` mean delta `0.0054`, FDR `1`; `CD6` mean delta `-0.00098`, FDR `1`. `ALCAM` is nominally positive but not FDR-significant (`mean_delta=0.1005`, `wilcoxon_p=0.083`, FDR `0.550`), and its protein signal in the older foamy screen is not sufficient to override clinical/prior-art saturation.

## Axis-by-axis hostile audit

### 1. `BTLA/HVEM` (`BTLA`, `TNFRSF14`, `TNFSF14/LIGHT`)

Verdict: demote.

Rationale:

- Novelty is blocked. Eli Lilly has granted/active BTLA agonist antibody patent family coverage for autoimmune use, explicitly including rheumatic, dermatology, neural disease, lupus nephritis, SLE, RA, psoriasis, atopic dermatitis, and MS. Source: Google Patents `US20200239578A1` / `US11396545B2`, https://patents.google.com/patent/US20200239578A1/en.
- Clinical saturation/failure risk exists. ANB032, a BTLA agonist, failed a 201-patient Phase 2b atopic dermatitis study according to AnaptysBio's December 11, 2024 Form 8-K. Source: https://ir.anaptysbio.com/static-files/37011815-d58f-4ad2-8e47-296c0ba20a10.
- The translational lane is occupied by current developers. HiFiBiO lists HFB200604 as a BTLA agonist mAb for autoimmune/inflammatory diseases with IND clearance in Q4 2024. Source: https://hifibio.com/pipeline/programs/hfb200604/.
- Modality direction is not clean. Agonizing BTLA can suppress activated T/B cells, but HVEM also binds LIGHT/CD160 and can participate in stimulatory or inhibitory networks. A molecule-to-clinic claim would need receptor/ligand-selective tuning rather than generic HVEM/BTLA expression.
- Local V3 support is insufficient. Wave19 parked `BTLA`; Wave33 failed MS-anchor, direction/modality, and prior-art gates. The signal is not state-coupled to the lipid-lysosomal module.

Possible narrow niche:

- A biomarker-defined `low-HVEM/high-BTLA-dysfunction` subgroup in SLE or Sjogren's might still be a development niche, but that is already close to published/industry rationale and was not established by V3 local data.

Unblocker required:

- Human disease tissue evidence showing a distinct BTLA/HVEM ligand-state defect not covered by ANB032/HFB200604/LY3361237-like programs, plus a selective agonist or ligand-biased biologic with target engagement and superiority over existing BTLA agonist concepts.

### 2. `CD6/ALCAM`

Verdict: demote despite real translational feasibility.

Rationale:

- The mechanism is clinically occupied. Itolizumab is an anti-CD6 antibody with Phase 3 psoriasis data and autoimmune development in lupus nephritis. Search/source anchors: phase-III psoriasis paper, PMID `24703722`, DOI `10.1016/j.jaad.2014.01.897`; EQUALISE lupus/SLE trial `NCT04128579`, https://clinicaltrials.gov/study/NCT04128579.
- Patent coverage is dense around itolizumab/CD6 phosphorylation and CD6-ALCAM signaling. Google Patents `WO2018073721A1` describes itolizumab, CD6-ALCAM signaling, psoriasis/RA efficacy, India psoriasis approval, and autoimmune/MS-related uses. Source: https://patents.google.com/patent/WO2018073721A1/en.
- Wave33 CT.gov query found 6 autoimmune-trial hits, including a not-yet-recruiting autologous `CD6-CAR Treg` study for stage 3 type 1 diabetes (`NCT07395050` in the local CT.gov API snapshot). That suggests additional clinical white space is being occupied, not opened.
- Modality direction is feasible but not novel: block pathogenic CD6-ALCAM interaction or tune CD6 signaling with antibodies/cell therapy. This is a known translational package, not a V3 discovery.
- Local V3 cross-disease support is weak. Wave33 local breadth is 1, state coupling is 0, and the axis fails local-cell-state and prior-art gates. The nominal MS anchor (`ms_anchor_delta=1.197`, `p=0.011`) is not enough because the broad cross-autoimmune cell-state support is missing.

Possible narrow niche:

- Stratification by tissue `ALCAM`-high endothelial/epithelial barrier entry plus `CD6`-high pathogenic T-cell infiltration could be viable scientifically, especially outside MS. But V3 did not establish that subgroup across diseases, and the niche would need differentiation from itolizumab/EQUALISE and CD6-CAR Treg programs.

Unblocker required:

- A cross-disease responder signature predicting anti-CD6 benefit that is absent from prior itolizumab work, plus independent tissue validation in at least three autoimmune indications.

### 3. `CD226/TIGIT/PVR/NECTIN2`

Verdict: demote.

Rationale:

- The biology is real but already heavily reviewed and patented. Frontiers 2022 reviews TIGIT reinforcement strategies for autoimmunity, including TIGIT-Ig, agonist anti-TIGIT antibody, TIGIT overexpression, and recombinant CD155. Source: https://www.frontiersin.org/journals/immunology/articles/10.3389/fimmu.2022.911919/full.
- Patent coverage exists for immune/inflammatory disease using TIGIT agonism and CD226/PVR-axis modulation. Example: `EP4226943A1`, "Therapeutic agent for immune/inflammatory disease", explicitly discusses agonistic anti-TIGIT and CD226 competition with CD155/CD112. Source: https://data.epo.org/publication-server/rest/v1.0/publication-dates/20230816/patents/EP4226943NWA1/document.pdf.
- Additional patent prior art covers Treg isolation/uses and mentions antagonists or agonists against CD226 or TIGIT for autoimmune disorders. Source: Justia `US11022615`, https://patents.justia.com/patent/11022615.
- Direction is conflicted by oncology. Oncology programs mostly antagonize TIGIT or agonize CD226 to restore antitumor/NK/CD8 function; autoimmunity would likely need the opposite direction: CD226 blockade, TIGIT agonism, or ligand engineering. That creates safety and mechanism uncertainty for viral/tumor surveillance.
- Local V3 support fails the strict gate. Wave33 shows GWAS breadth but local breadth only 2, negative breadth 1, state coupling 0, no MS anchor, and prior-art failure. Wave19 individually called `TIGIT` no-go, `PVR` park-low, and `NECTIN2` no-go.

Possible narrow niche:

- A genetically stratified CD226-risk autoimmune subgroup could be worth a separate genetics-first program, but only if target-resolved colocalization and directionality are shown. V3 currently only has broad GWAS Catalog co-listing, not target-resolved causal evidence.

Unblocker required:

- Fine-mapped CD226 or TIGIT/PVR/NECTIN2 causal variant evidence across at least four autoimmune diseases, plus disease-tissue T/NK/Treg state evidence and a pharmacology package proving immunosuppression without unacceptable antiviral/antitumor liability.

### 4. `IL7R/IL7`

Verdict: demote as clinically saturated/generic, not as biologically irrelevant.

Rationale:

- The genetic MS association and splice/sIL7R mechanism are well known and patent-covered. Google Patents `WO2019183570A1` describes antisense/splicing modulation of soluble IL7R to treat autoimmune diseases including MS, cites `rs6897932`, and frames elevated sIL7R as an autoimmune etiology. Source: https://patents.google.com/patent/WO2019183570A1/en.
- Anti-IL7R clinical development is active. OSE-127/lusvertikimab is a non-cytotoxic IL-7Rα antagonist under clinical development for autoimmune disease, with Phase 2 UC (`NCT04882007`) and Sjogren's (`NCT04605978`) programs. Sources: https://clinicaltrials.gov/study/NCT04882007 and https://clinicaltrials.servier.com/trial/NCT04605978/efficacy-and-safety-of-s95011-in-primary-sjogrens-syndrome-patients.
- Recent UC sources report positive Phase 2 induction data for lusvertikimab, which strengthens the target as a real therapeutic class but weakens novelty for V3. Example sponsor report: https://www.globenewswire.com/news-release/2025/02/24/3030859/0/en/OSE-Immunotherapeutics-Reports-Full-Phase-2-Induction-Results-for-Anti-IL-7R-mAb-Lusvertikimab-in-Ulcerative-Colitis-at-the-20th-Congress-of-ECCO.html.
- Safety/modality issue: IL-7R is broad T-cell survival/homeostasis biology. Blockade may be effective in inflammatory tissues but is not a lipid-lysosomal myeloid module-specific intervention and has infection/immune-reconstitution concerns that require careful trial design.
- Local V3 evidence is generic. Wave33 passes local breadth, but with negative breadth 2, state coupling 0, no MS anchor, and failed safety/prior-art gates. Wave18 foundation rescue ranked `IL7R` as `do_not_promote`, with `token_not_detected` in many disease-cell contexts and no aligned selective perturbation support.

Possible narrow niche:

- UC with high mucosal IL7/IL7R biology is already the obvious lead indication and is already occupied. For MS, an sIL7R-splicing biomarker subgroup could be scientifically coherent but patent/prior-arted and not established in V3 tissue data.

Unblocker required:

- A non-overlapping intervention point downstream of pathogenic IL7R that preserves protective T-cell homeostasis, plus V3-relevant tissue evidence and clear differentiation from OSE-127/lusvertikimab and sIL7R antisense patent claims.

### 5. `BACH2/IKZF` tolerance program (`BACH2`, `IKZF1`, `IKZF3`, `FOXP3`)

Verdict: demote as a direct target package.

Rationale:

- BACH2 is a strong causal/regulatory concept but not a current druggable intervention point. Nature 2013 showed BACH2 stabilizes Treg-mediated immune homeostasis and linked polymorphisms to asthma, MS, Crohn's, coeliac disease, and type 1 diabetes. Source: https://www.nature.com/articles/nature12199.
- The tractable IKZF branch is already clinically developed in lupus. Iberdomide/CC-220 is a cereblon modulator that degrades IKZF1/Ikaros and IKZF3/Aiolos. Phase 2 SLE trial sources include `NCT03161483`, NEJM 2022, and PMIDs in the CT.gov record. Source: https://clinicaltrials.gov/study/NCT03161483.
- Direction is not equivalent to BACH2 restoration. A BACH2-restoration/Treg-stability claim would need increase or preserve tolerance-program function; IKZF1/3 degraders are immunomodulatory but act through broad B-cell, pDC, T-cell, IL-2/Treg and IFN effects. This is not a clean direct restoration of the V3 proposed program.
- Safety is nontrivial. IKZF degraders are systemic hematopoietic transcription-factor perturbations. Reported lupus-study adverse-event themes include neutropenia, infection signals, rash/GI effects in published summaries. This is not a selective tissue-targeted tolerance controller.
- Local V3 evidence is weak or negative. Wave33 local breadth 1, negative breadth 1, state coupling 0, no MS anchor; MS white-matter `IKZF1` is negative (`mean_delta=-0.252`, nominal p `0.0059` but FDR not significant), while `BACH2` is null.

Possible narrow niche:

- Engineered antigen-specific Treg or cell-therapy programs that enforce BACH2-like stability could be scientifically interesting, but that is a modality/program claim rather than a druggable target from the current V3 datasets. It would also overlap with broad Treg-cell-therapy patent space.

Unblocker required:

- A selective BACH2-stabilizing modality or ex vivo Treg-engineering strategy with autoimmune antigen specificity, plus tissue evidence that the failed lipid-lysosomal/APC branch is downstream of a BACH2-low T-cell state. Current V3 data do not show this.

## Public search/query log

Databases/surfaces checked: local Wave33 Europe PMC and CT.gov API snapshots; web lookup of PubMed/Europe PMC-indexed literature; ClinicalTrials.gov; Google Patents; Espacenet/EPO patent PDF; company trial disclosures where official clinical records were sparse.

Representative public queries:

- `BTLA agonist antibody autoimmune disease patent BTLA HVEM autoimmune trial`
- `BTLA agonist ANB032 phase 2 atopic dermatitis clinical trial autoimmune`
- `ClinicalTrials.gov BTLA autoimmune trial BTLA agonist`
- `CD6 ALCAM itolizumab autoimmune disease clinical trial lupus nephritis psoriasis multiple sclerosis patent`
- `itolizumab anti-CD6 approved psoriasis lupus nephritis trial EQUALISE safety`
- `CD226 TIGIT PVR NECTIN2 autoimmune disease CD226 blockade patent agonist TIGIT autoimmune`
- `TIGIT agonist antibody autoimmune disease patent CD226 antagonist autoimmune`
- `IL7R IL-7 receptor alpha antibody autoimmune disease trial OSE-127 ulcerative colitis Sjogren multiple sclerosis`
- `lusvertikimab OSE-127 anti-IL-7R ulcerative colitis Sjogren clinical trial safety`
- `BACH2 autoimmune disease regulatory T cells therapeutic target IKZF1 IKZF3 iberdomide lupus trial`
- `iberdomide IKZF1 IKZF3 systemic lupus erythematosus phase 2 trial safety`
- `BACH2 Treg autoimmune patent cell therapy BACH2 regulatory T cells`

## Sanity conclusion for orchestrator

Do not promote any of these five as V3 therapeutic findings. The main run should treat them as comparator failures:

- `CD6/ALCAM`: clinically feasible but prior-arted; use as "known translational axis" positive control.
- `IL7R`: genetically and clinically real but crowded/generic; use as "known cytokine genetics" positive control.
- `BTLA/HVEM`: checkpoint-tolerance concept with active developers and Phase 2 failure signal; no V3-specific niche.
- `CD226/TIGIT/PVR/NECTIN2`: genetics-first idea remains possible but requires target-resolved coloc and safety-resolved direction before reopening.
- `BACH2/IKZF`: keep as biological tolerance scaffold; do not treat as a druggable central node without a new selective modality.

