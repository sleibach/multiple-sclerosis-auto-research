# V6 Sidecar - Longitudinal Data Scout

Returned: 2026-05-28

Scope: identify accessible public or controlled-access pre-diagnostic and
longitudinal autoimmune datasets relevant to V6 Tier -1 promotion. Prioritized
tracks: TEDDY/T1D, pre-IBD, MS serum/PBMC, postpartum MS, and
treatment-resistance cohorts.

Files read:

- `knowledge/dimensions/D04_LONGITUDINAL_PRE_DISEASE.md`
- `meta/ROADMAP_V6.md`

Constraint interpretation: I did not edit shared indexes. This report is a
sidecar inventory and should be treated as a queue for orchestrator vetting.

## Executive Verdict

The highest-value V6 longitudinal dataset is still TEDDY. It is the only
identified resource with a real pre-autoimmune design, repeated blood sampling,
omics breadth, and explicit seroconversion/progression anchors. The main
limitation is access: the transcriptomic and microbiome matrices are
controlled-access through dbGaP/NIDDK rather than immediately downloadable.

For immediately analyzable public data, the best options are:

1. `GSE282122` / Zenodo anti-TNF IBD single-cell atlas for treatment-response
   and resistance mechanisms.
2. `GSE24427`, `GSE138064`, and related GEO MS IFN-beta response datasets for
   longitudinal/treatment-response tests.
3. `E-MTAB-12260`, `GSE17410`, `GSE235508`, and `GSE108497` for pregnancy and
   postpartum natural-experiment comparisons already partly used locally.
4. TEDDY Metabolomics Workbench `PR000950` / `ST001386` / `ST001636` for open
   pre-T1D plasma metabolome/lipidome trajectory tests, though raw data scale is
   large.

No open sample-level pre-diagnostic MS PBMC/serum omics matrix was verified.
The DoD serum repository MS EBV/NfL work is scientifically strong but not
public sample-level data. Treat it as literature anchoring, not a V6 runnable
dataset, unless controlled access is obtained.

## Search Log

Verified web searches performed:

- `TEDDY study longitudinal gene expression autoantibody seroconversion accession GEO dbGaP`
- `TEDDY peripheral blood gene expression 2025 autoantibody positive accession`
- `TEDDY metabolomics islet autoimmunity accession Metabolomics Workbench`
- `TEDDY microbiome phs001442 stool metagenomics accession`
- `preclinical inflammatory bowel disease serum proteomics cohort accession public data`
- `prediagnostic Crohn ulcerative colitis serum proteomics public data accession`
- `PREDICTS IBD proteomics pre-diagnostic serum public dataset`
- `pre-diagnostic inflammatory bowel disease metabolomics serum nested case control accession`
- `Bjornevik multiple sclerosis serum proteomics prediagnostic public data accession`
- `preclinical multiple sclerosis serum neurofilament public data military cohort accession`
- `multiple sclerosis pregnancy postpartum transcriptomics GEO relapse postpartum dataset`
- `anti-TNF refractory IBD single cell RNA-seq GEO treatment response accession`
- `multiple sclerosis treatment response gene expression GEO interferon beta responders accession`
- `GSE282122 inflammatory bowel disease anti-TNF single cell GEO`
- `GSE24427 multiple sclerosis interferon beta longitudinal GEO 25 patients`
- `GSE138064 multiple sclerosis interferon beta response GEO`
- `GSE228421 psoriasis risankizumab single cell GEO`

## Candidate Dataset Inventory

### 1. TEDDY / Type 1 Diabetes - controlled-access core omics

Accession/source:

- dbGaP `phs001442.v4.p3`, The Environmental Determinants of Diabetes in the
  Young (TEDDY) Study:
  <https://www.ncbi.nlm.nih.gov/projects/gap/cgi-bin/study.cgi?study_id=phs001442.v4.p3>
- Older dbGaP version `phs001442.v2.p2` explicitly describes available gene
  expression and microbiome data:
  <https://www.ncbi.nlm.nih.gov/projects/gap/cgi-bin/study.cgi?study_id=phs001442.v2.p2>
- NIDDK Central Repository TEDDY page was already recorded in
  `D04_LONGITUDINAL_PRE_DISEASE.md`:
  <https://repository.niddk.nih.gov/studies/teddy/DSIC/>

Modality:

- Longitudinal peripheral-blood gene expression on Illumina HumanHT-12 arrays.
- Genotypes, exome/WGS in newer releases.
- Longitudinal gut/nasal/plasma microbiome.
- Autoantibody timing, progression to T1D, diet/infection/environmental data.

Access status:

- Controlled access through dbGaP/NIDDK authorization, not open direct download.
- Public metadata and study description are accessible.

Verified details:

- TEDDY is a prospective longitudinal cohort of genetically at-risk children.
- Participants are followed every 3 months for islet autoantibodies until age 4
  years and at least every 6 months until age 15; autoantibody-positive
  participants continue 3-month follow-up.
- dbGaP page states TEDDY data currently include gene expression, SNPs, exome,
  microbiome, RNA-seq, and WGS.
- Older dbGaP version states blood RNA was collected starting at 3 months, then
  every 3 months up to 48 months and biannually afterward; total RNA was
  profiled on Illumina HumanHT-12 Expression BeadChips.
- 2025 Frontiers Immunology paper used PBMC gene-expression profiles from 62
  autoantibody-positive TEDDY children, 56 of whom progressed to diabetes, and
  accessed data through `phs001442`.

V6 hypotheses testable:

- H01 pDC/ISG source switch: test whether ISG/MHC-II/APC modules rise before or
  after islet-autoantibody seroconversion.
- H04 APC-state controller: identify whether upstream APC/HLA-II modules
  precede autoimmunity rather than merely follow tissue inflammation.
- Lipid-lysosomal myeloid module: test temporal precedence before T1D
  seroconversion and progression.
- Cross-autoimmune comparator: if a module appears pre-seroconversion in TEDDY
  but only cross-sectionally in MS/IBD, this gives a causal-priority anchor.

Priority:

- Highest scientific priority, access-gated.

Tier -1 promotion value:

- Very high. A positive result would satisfy the temporal-precedence dimension
  for a pan-autoimmune mechanism, but only after actual controlled-access data
  are obtained.

### 2. TEDDY Metabolomics / Lipidomics - open public trajectory data

Accession/source:

- Metabolomics Workbench project `PR000950`, DOI `10.21228/M8WM4P`:
  <https://workbench.sdsc.edu/data/DRCCMetadata.php?Mode=Project&ProjectID=PR000950>
- Study `ST001386`: TEDDY Metabolomics Study.
- Study `ST001636`: TEDDY Lipidomics Study.

Modality:

- Plasma primary metabolites and lipidomics from TEDDY case-control subjects.
- Mass spectrometry.

Access status:

- Public via Metabolomics Workbench.
- Practical compute/storage note: `ST001386` lists 11,560 samples and uploaded
  data of about 104.4 GB; `ST001636` lists 11,560 samples and raw uploaded data
  of about 4.7 TB. Download should be targeted to processed tabular matrices,
  not raw data, for V6.

Verified details:

- Project summary: quantification of primary metabolites in human plasma from
  TEDDY case-control subjects; goal is metabolic signatures in prediabetic
  autoimmunity and diabetes.
- Published TEDDY metabolome work reports longitudinal metabolome-wide signals
  before first islet autoantibody.

V6 hypotheses testable:

- H04 APC-state controller, indirectly: metabolic context preceding islet
  autoimmunity may distinguish lipid/lysosomal/metabolic driver states from
  secondary inflammation.
- Pregnancy hematologic/endothelial axis analog: test whether platelet/erythroid
  or lipid mediators precede autoimmune conversion in T1D.
- Candidate rescue: lipid-handling demotions from V3/V4 can be reconsidered if
  metabolites/lipids shift before seroconversion.

Priority:

- High and immediately actionable if processed tables are used.

Tier -1 promotion value:

- High for metabolic hypotheses; medium for gene-specific hypotheses because it
  lacks transcript-level readout.

### 3. TEDDY microbiome - controlled-access longitudinal microbiome

Accession/source:

- dbGaP `phs001442.v4.p3` and older `phs001442.v2.p2`.
- A search result also surfaced TEDDY microbiome primary accession
  `phs001443.v1.p1` in a microbiome paper PDF, but this should be reverified
  before use because the main TEDDY umbrella page is `phs001442`.

Modality:

- Longitudinal stool microbiome from monthly early-life collection, plus nasal
  and plasma microbiome sampling at defined intervals.

Access status:

- Controlled access through dbGaP for sample-level data.

Verified details:

- dbGaP TEDDY page says microbiome data are available, with stool collected
  monthly from 3 to 48 months and then every 3 months; nasal swabs and plasma
  collected every 3 months starting at 9 months or 3 months depending on sample
  type, with autoantibody-positive participants continuing higher-frequency
  collection.

V6 hypotheses testable:

- Infectious/microbiome trigger axis for T1D seroconversion.
- Whether lipid-lysosomal/APC signatures correlate temporally with microbial
  community shifts before autoimmunity.

Priority:

- Medium-high, access-gated.

Tier -1 promotion value:

- High if paired with TEDDY expression or metabolomics; weaker alone because
  cross-disease mapping from microbiome to MS mechanisms is indirect.

### 4. Pre-IBD PREDICTS / Tri-service subjects

Accession/source:

- PREDICTS cohort profile:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC6446072/>

Modality:

- Pre-disease serum compartment; designed for biomarkers in military
  Tri-service subjects before IBD diagnosis.

Access status:

- No open sample-level accession verified. Treat as publication/cohort anchor,
  not an immediately runnable dataset.

Verified details:

- Cohort profile describes PRoteomic Evaluation and Discovery in an IBD Cohort
  of Tri-service Subjects, intended to assess serum biomarkers before disease
  and identify pre-disease signals predicting IBD risk.

V6 hypotheses testable:

- Ideal for lipid-lysosomal/APC temporal precedence in Crohn/UC if access is
  possible.
- Could test whether serum innate/complement/APC proteins precede IBD diagnosis.

Priority:

- High scientific priority, low immediate feasibility.

Tier -1 promotion value:

- High if data access can be arranged; currently not a runnable V6 input.

### 5. Pre-IBD CCC-GEM nested case-control metabolomics/proteomics

Accession/source:

- 2025 preclinical Crohn metabolomics paper:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC12416195/>

Modality:

- Baseline serum metabolomics in healthy first-degree relatives of Crohn
  disease patients who later developed Crohn disease versus matched controls.
- Paper also describes proteomics, gut barrier function, fecal calprotectin,
  CRP, antimicrobial antibodies, and gut microbiota in the nested design.

Access status:

- No open matrix accession verified during this scout. Data may require author
  request or controlled cohort access.

Verified details:

- CCC-GEM followed 5,122 healthy first-degree relatives; nested case-control
  design includes pre-CD subjects who developed Crohn disease and matched
  disease-free controls.

V6 hypotheses testable:

- H04 APC-state/metabolic controller: test whether serum metabolic/protein
  changes precede Crohn onset.
- Candidate rescue for lipid metabolism, complement, and barrier-related Tier
  -1 hypotheses.

Priority:

- High, but access uncertain.

Tier -1 promotion value:

- High if data are available; currently report-level only.

### 6. Pre-IBD antibody epitope repertoire

Accession/source:

- 2025 paper record: "Crohn's disease and ulcerative colitis exhibit
  prediagnostic antibody signatures with shared and divergent changes towards
  disease onset":
  <https://weizmann.elsevierpure.com/en/publications/crohns-disease-and-ulcerative-colitis-exhibit-prediagnostic-antib/>

Modality:

- Prediagnosis and postdiagnosis serum antibody epitope repertoires using
  phage-display immunoprecipitation sequencing against 344,000 microbial, food,
  and immune antigens.

Access status:

- No open accession verified in this sidecar.

Verified details:

- Search result states paired prediagnosis/postdiagnosis serum samples with
  median 3.9-year span.

V6 hypotheses testable:

- Infectious/microbial antigen trigger axis.
- Whether antigenic shifts precede Crohn/UC and map to the cross-autoimmune
  APC/HLA-II module.

Priority:

- Medium-high, access uncertain.

Tier -1 promotion value:

- High for antigen-trigger hypotheses; lower for transcriptomic module tests.

### 7. MS prediagnostic DoD serum repository / EBV / NfL

Accession/source:

- JAMA Neurology presymptomatic MS serum NfL paper:
  <https://jamanetwork.com/journals/jamaneurology/fullarticle/2749888>
- Science EBV/MS longitudinal analysis summary:
  <https://colab.ws/articles/10.1126%2Fscience.abj8222>

Modality:

- Serial serum samples from US Department of Defense Serum Repository.
- EBV serology, NfL, and related serum biomarker measurements in pre-MS cases
  and controls.

Access status:

- Not public sample-level data. The DoDSR source population is controlled and
  requires institutional access/collaboration.

Verified details:

- DoDSR contains >60 million serum samples from active-duty personnel; personnel
  generally provide serum at entry and about every 2 years.
- Presymptomatic MS study used active-duty personnel with stored serum samples.
- Science EBV/MS longitudinal analysis reported NfL increase only after EBV
  seroconversion.

V6 hypotheses testable:

- MS temporal anchor for EBV/NfL axis.
- Not suitable for direct V6 module scoring unless data access is obtained.

Priority:

- High biological relevance, low immediate feasibility.

Tier -1 promotion value:

- Literature-level only for now. Do not use as in-silico evidence unless a
  matrix or summary table is obtained.

### 8. MS pregnancy/postpartum T-cell cohort

Accession/source:

- Paper: "Effector T Helper Cells Are Selectively Controlled During Pregnancy
  and Related to a Postpartum Relapse in Multiple Sclerosis":
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC8005718/>

Modality:

- Paired third-trimester and postpartum blood in MS patients with/without
  postpartum relapse and healthy controls.
- Flow/cytometry-style Th cell phenotyping and serum-exposure in vitro assays.

Access status:

- Paper is open. No machine-readable public accession verified during this
  scout.

Verified details:

- Study analyzed paired third trimester and postpartum blood of 19 MS patients
  and 12 healthy controls.
- The paper directly links effector Th phenotype to postpartum relapse status.
- It reports higher pro-inflammatory cytokine potential in relapsing patients
  at third trimester and postpartum.

V6 hypotheses testable:

- H03 postpartum T-cell trafficking readiness.
- H01 pDC/ISG source switch, indirectly, as a clinical-relapse-linked
  postpartum comparator.
- Tests whether `E-MTAB-12260` postpartum trafficking signal maps to relapse
  biology rather than generic postpartum immune reconstitution.

Priority:

- High for interpretation; low for direct computation unless supplemental tables
  can be extracted.

Tier -1 promotion value:

- Medium. It can justify an MS postpartum hypothesis but cannot by itself
  provide reproducible module scoring without accessible sample-level data.

### 9. MS pregnancy transcriptomics already local

Accessions/source:

- `GSE17410`: MS PBMC pre-pregnancy versus month 9 pregnancy.
- `E-MTAB-12260`: MS sorted CD4/CD8 T-cell RNA-seq across pregnancy and
  postpartum.
- `GSE17449`: related MS pregnancy superseries; local records indicate overlap
  with `GSE17410`, not independent.

Modality:

- PBMC expression array and sorted T-cell RNA-seq.

Access status:

- Public and already locally used.

Verified local status:

- `GSE17410` month-9 IFN/APC signal survives leave-one-out but decomposes to
  ISG/composition rather than MIF/CD74/APC specificity.
- `E-MTAB-12260` does not reproduce broad late-pregnancy T-cell IFN/APC
  activation but shows postpartum T-cell trafficking increase.

V6 hypotheses testable:

- H01 MS late-pregnancy hematologic/endothelial axis.
- H02 pDC-depletion/ISG-source switch.
- H03 postpartum T-cell trafficking readiness.

Priority:

- High because local and already parsed.

Tier -1 promotion value:

- Medium-high. These are natural-experiment datasets, but they need independent
  clinical/postpartum relapse support before Tier 0+ claims.

### 10. Cross-disease pregnancy comparators already local

Accessions/source:

- `GSE235508`: RA/SLE/healthy longitudinal pregnancy/postpartum whole blood.
- `GSE108497`: SLE/healthy pregnancy/postpartum whole-blood Illumina array.

Modality:

- Whole-blood RNA expression across pregnancy and postpartum.

Access status:

- Public and locally parsed.

Verified local status:

- `GSE235508` seropositive RA shows late-pregnancy trough and postpartum
  rebound in MIF/CD74/HLA-II/IFN-APC modules.
- `GSE108497` provides SLE/healthy timepoints with explicit TP coding:
  `<16`, `16-23`, `24-31`, `32-40` weeks, and `8-20 weeks postpartum`; local
  V5 analysis found outcome-specific APC/HLA-II kinetics.

V6 hypotheses testable:

- Whether MS pregnancy effects are generic pregnancy immunology, disease-
  specific rebound, or compartment-specific.
- Whether postpartum flare biology maps to HLA-II/APC rebound across RA/SLE/MS.

Priority:

- High as natural-experiment comparators.

Tier -1 promotion value:

- Medium-high. Already supports cross-disease patterning but not MS causality.

### 11. IBD anti-TNF treatment-response atlas

Accession/source:

- GEO `GSE282122`:
  <https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE282122>
- Zenodo record:
  <https://zenodo.org/records/14007626>
- Paper:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC11519010/>

Modality:

- Longitudinal single-cell RNA-seq of gut biopsies during anti-TNF treatment in
  Crohn disease and ulcerative colitis.
- About 1 million single-cell transcriptomes from 216 gut biopsies, 41
  subjects.
- Response/remission outcome annotations.

Access status:

- Public GEO/Zenodo; already locally used for MIF/CD74 component response.

Verified details:

- GEO title: "A longitudinal single-cell atlas of anti-tumour necrosis factor
  treatment in inflammatory bowel disease."
- Summary says pretreatment epithelial and myeloid differences were associated
  with remission outcomes.

V6 hypotheses testable:

- H06 anti-TNF HLA-II remodeling.
- H04 APC-state-controller rather than CD74.
- Treatment-resistance phenotype dimension for lipid-lysosomal myeloid module.

Priority:

- Highest immediate treatment-response dataset.

Tier -1 promotion value:

- High. It can test baseline predictors and dynamic remodeling under a real
  therapeutic perturbation.

### 12. MS interferon-beta longitudinal responder datasets

Accessions/source:

- GEO `GSE24427`, described in PMC reanalysis:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC6930778/>
- GEO `GSE138064`:
  <https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE138064>
- Related GEO datasets reported in IFN-beta MS reanalysis: `GSE19285`,
  `GSE33464`, `GSE26104`, `GSE5574`, `GSE53716`.
- GEO `GSE138064` PLOS/University of Chicago record:
  search result states accession `GSE138064`.

Modality:

- PBMC or whole-blood gene expression under interferon-beta treatment,
  sometimes longitudinal and/or responder-stratified.

Access status:

- Public GEO for at least `GSE24427` and `GSE138064`; other listed GEO datasets
  require direct accession verification before use.

Verified details:

- `GSE24427`: longitudinal gene expression from 25 German RRMS patients treated
  with recombinant IFN-beta-1b for two years. Reanalysis categorized responders
  and nonresponders by first relapse time.
- `GSE138064`: GEO summary says immune up-regulation in MS is coupled to
  subnormal response to IFN-beta and low serum IFN-beta; samples include
  partial responders 4 hours after IFN-beta injection.

V6 hypotheses testable:

- H01/H02 ISG-source switch: distinguish baseline ISG-high poor response from
  pharmacologic inducibility.
- H04 APC-state controller: test whether HLA-II/APC markers predict or follow
  IFN-beta response.
- Treatment-resistance dimension for MS, especially if response labels are
  robust.

Priority:

- High and immediately actionable.

Tier -1 promotion value:

- High for MS treatment-response hypotheses; lower for pre-disease causality.

### 13. Psoriasis risankizumab longitudinal single-cell atlas

Accession/source:

- GEO `GSE228421`:
  <https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE228421>
- EGA/dbGaP-style protected record surfaced as `phs003351`:
  <https://ega-archive.org/studies/phs003351>
- Paper:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC10828502/>

Modality:

- Longitudinal scRNA-seq of psoriasis skin biopsies during IL-23 blockade
  (risankizumab): baseline non-lesional/lesional, day 3, day 14.

Access status:

- GEO series is public and has processed information; raw data controlled due
  to privacy according to GEO submitter. EGA/dbGaP-style raw access may be
  controlled.

Verified details:

- GEO summary: 5 individuals with severe psoriasis receiving risankizumab;
  biopsies at day 0, day 3, and day 14; 10x Genomics.
- Follow-up paper/reanalysis reports macrophage polarization effects.

V6 hypotheses testable:

- Cross-disease treatment-response comparator for APC/myeloid remodeling.
- Tests whether lipid-lysosomal/APC-state modules reverse under IL-23 blockade
  in a non-MS autoimmune tissue.

Priority:

- Medium-high, especially for cross-disease validation.

Tier -1 promotion value:

- Medium. Strong perturbation dimension, but not pre-diagnostic and small n.

### 14. MS clinical longitudinal serum NfL / trial biomarker datasets

Sources:

- ADVANCE/ATTAIN serum NfL paper:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC8414824/>
- ASCLEPIOS serum NfL open paper:
  <https://digitalcommons.wustl.edu/oa_4/650/>
- BENEFIT baseline metabolomics and 5-year outcome summary:
  <https://www.broadinstitute.org/publications/broad1376626>

Modality:

- Serum NfL or metabolomics linked to MRI/EDSS/relapse outcomes in established
  MS or first clinical demyelinating event.

Access status:

- Publication-level summaries are public; sample-level matrices not verified as
  open during this scout.

Verified details:

- ADVANCE/ATTAIN paper analyzes sNfL changes at 3, 6, 9, and 12 months against
  4-year outcomes.
- BENEFIT summary: baseline untargeted metabolomics of 545 metabolites in 468
  first clinical episode patients with 5-year follow-up.

V6 hypotheses testable:

- H01 hematologic/endothelial or metabolic axis as prognostic rather than
  pre-diagnostic.
- Lipid/metabolic candidate rescue if baseline metabolite associations are
  accessible.

Priority:

- Medium, access-limited.

Tier -1 promotion value:

- Medium. Useful for disease-progression temporal ordering but not preclinical
  autoimmunity unless data access is obtained.

## Ranked Next Actions

1. **Immediate runnable path:** use `GSE24427` and `GSE138064` to test whether
   V6 ISG/APC/hematologic hypotheses predict or follow IFN-beta response in MS.
   These are public GEO datasets and directly map to MS treatment-response.
2. **Immediate runnable path:** continue `GSE282122` treatment-response mining
   for APC-state-controller versus CD74/HLA-II-only effects.
3. **Immediate runnable path:** mine TEDDY Metabolomics Workbench processed
   tables (`PR000950`, `ST001386`, `ST001636`) for pre-seroconversion metabolic
   trajectories, avoiding raw 4.7 TB lipidomics unless necessary.
4. **Access-gated high-value path:** request or plan dbGaP/NIDDK access for
   TEDDY `phs001442.v4.p3`, prioritizing gene-expression and paired
   seroconversion/progression phenotypes.
5. **Access-gated high-value path:** identify whether PREDICTS or CCC-GEM have
   controlled public data request routes; no open accession was verified here.
6. **Interpretation path:** use the MS postpartum Th-cell paper as a clinical
   comparator for `E-MTAB-12260` trafficking but do not treat it as a
   reproducible omics dataset unless supplemental tables are machine-extracted.

## Hypothesis-to-Dataset Map

| V6 hypothesis | Best dataset(s) | What would count as Tier -1 support |
|---|---|---|
| H01 MS late-pregnancy hematologic/endothelial axis | `GSE17410`, `E-MTAB-12260`, MS postpartum Th-cell paper, `GSE24427`/`GSE138064` | Same hematologic/ISG axis predicts postpartum relapse or IFN-beta response, not just one PBMC pregnancy contrast |
| H02 pDC-depletion/ISG-source switch | `GSE17410`, `GSE24427`, `GSE138064`, TEDDY expression if accessed | ISG-high state separates from pDC abundance and predicts response/progression in a second longitudinal setting |
| H03 postpartum T-cell trafficking readiness | `E-MTAB-12260`, postpartum Th-cell paper, `GSE235508` RA comparator | Postpartum trafficking genes recur and align with relapse or disease rebound |
| H04 APC-state controller rather than CD74 | `GSE282122`, TEDDY expression, `GSE24427`, `GSE228421` | Upstream APC/HLA-II controller predicts response or pre-seroconversion better than CD74 alone |
| H05 OPC CD74 lesion-stress state | No direct longitudinal dataset found | Needs MS lesion/CSF longitudinal or treatment-linked data; none verified here |
| H06 anti-TNF HLA-II remodeling | `GSE282122`; psoriasis `GSE228421` as comparator | Pretreatment or early-treatment HLA-II/APC remodeling predicts remission in IBD and shares direction with another treated autoimmune tissue |
| Lipid-lysosomal myeloid module temporal precedence | TEDDY `phs001442`, TEDDY `PR000950`/`ST001386`/`ST001636`, CCC-GEM if accessible | Module-related metabolites/transcripts shift before seroconversion/diagnosis rather than only after inflammation |

## Bottom Line

For V6 Tier -1 promotion, do not wait on inaccessible pre-MS serum. The practical
route is:

1. Run public MS treatment-response GEO (`GSE24427`, `GSE138064`) for ISG/APC
   directionality.
2. Run public IBD anti-TNF (`GSE282122`) for therapeutic perturbation.
3. Use TEDDY open metabolomics now and treat TEDDY expression/microbiome as a
   controlled-access target.
4. Keep PREDICTS, CCC-GEM, and DoDSR MS as high-value but non-runnable temporal
   anchors until access is solved.
