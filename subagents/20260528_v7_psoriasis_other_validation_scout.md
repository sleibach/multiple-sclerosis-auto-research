# V7 Psoriasis / Other Autoimmune Biologic Validation Cohort Scout

Date: 2026-05-28  
Role: sidecar cohort scout  
Scope: public psoriasis, lupus, Sjogren, RA, or other autoimmune biologic/JAK response transcriptomic cohorts not used in V6 derivation.  
V7 locked exclusions: `GSE282122`, `GSE138064`, `GSE24427`.

## Locked-Rule Mapping

Under `LOCKED_RULE_V7.md`, most cohorts below are **Class A - inflammatory input blockade**:

- anti-TNF: adalimumab, etanercept, infliximab;
- anti-IL-12/23 or anti-IL-23: ustekinumab, guselkumab, risankizumab;
- anti-IL-17/IL-17RA: secukinumab, brodalumab;
- JAK inhibition: tofacitinib, when used to reduce inflammatory cytokine signaling.

Primary V7 feature for Class A:

- if early on-treatment samples exist: `-1 * delta_IFN_APC`, first on-treatment minus pretreatment baseline;
- if only baseline exists: `baseline_IFN_APC`.

## Highest-Priority Validation Candidates

| Accession | Disease | Therapy | Locked class | Response labels | Baseline | Early/on-treatment | Data access | V7 priority |
|---|---|---|---|---|---|---|---|---|
| `GSE85034` | psoriasis | adalimumab anti-TNF; methotrexate comparator | Class A for adalimumab | Yes. GEO title/summary explicitly says early gene-expression predicts long-term treatment response; local V3 already derived patient response table. | Lesional and non-lesional baseline | Weeks 1, 2, 4, 16 | GEO series matrix; Illumina HT-12 V4; 179 samples | Very high, but note prior V3 use. Not V6 derivation. |
| `GSE117468` | psoriasis | brodalumab anti-IL17RA; ustekinumab anti-IL12/23; placebo | Class A | Likely usable. Phase 3 mechanistic substudy has treatment, patient IDs, BL/W4/W12, placebo; clinical trial source should allow PASI response derivation, and recent papers use it for brodalumab response modeling. | Lesional and non-lesional BL | W4 and W12 | GEO processed/sample tables and raw CEL; Affymetrix; 844 samples from 116 patients | Very high. Best large psoriasis biologic validation set. |
| `GSE201827` | psoriasis | secukinumab anti-IL17A; placebo then switch | Class A | Likely usable from ObePso-S clinical outcomes; GEO has randomized treatment arm and sample IDs. Need confirm PASI/IGA labels from source/supplement. | Lesional and non-lesional BL | W12 and W52, not very early | GEO series matrix/raw; Affymetrix GPL570; 434 samples | High. Good randomized anti-IL17 comparator; early delta limited to W12. |
| `GSE51440` | psoriasis | guselkumab anti-IL23p19 | Class A | Partial. Clinical improvement and sustained-remission subgroup reported; sample names include subject/time/tissue but response labels may require paper supplement. | Baseline LS/NL | Week 1 and week 12 | GEO series matrix/raw CEL; Affymetrix HT HG-U133+ PM; 59 samples | High if responder/sustained-remission labels can be joined. |
| `GSE228421` | psoriasis | risankizumab anti-IL23p19 | Class A | Weak for binary response. Five treated severe psoriasis patients; no responder/nonresponder labels apparent in GEO. Useful as APC/macrophage early pharmacodynamic support, not primary AUC validation unless response labels found. | Day 0 lesional and non-lesional | Day 3 and day 14 lesional | GEO has 20 scRNA samples; raw data to dbGaP per submitter; processed access must be checked | High for mechanism/context; lower for locked binary validation. |

## Psoriasis Cohort Details

### `GSE228421` - risankizumab, single-cell psoriasis

- Source: GEO accession page, title "Using single-cell transcriptomics to characterise early mechanisms of psoriasis resolution".
- Therapy class: risankizumab, IL-23 p19 blockade -> **Class A**.
- Design: full-thickness skin biopsies from five severe psoriasis patients; day 0 non-lesional and lesional skin, day 3 and day 14 lesional skin.
- Modality: 10x single-cell RNA-seq.
- Access: GEO lists 20 samples and states raw data will be submitted to dbGaP due to privacy. Need verify whether processed matrices are downloadable from GEO supplementary files or only sample records.
- Response labels: not obvious from GEO; likely all treated, no explicit responder/nonresponder split. Recent secondary paper frames macrophage polarization after risankizumab but does not by itself provide V7 binary response labels.
- V7 use:
  - Not ideal for primary AUC validation.
  - Good for Class A early delta pharmacodynamic test in APC/macrophage compartments: day 3/day 14 minus day 0 lesion.
  - Strongest use is causal/mechanistic support if locked IFN/APC downshift occurs in macrophage/APC pseudobulk.
- Source anchors:
  - GEO: public Dec 15 2023; 5 individuals; day 0/day 3/day 14; 20 samples; raw dbGaP note: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE228421
  - Paper: scRNA/in vitro validation reports risankizumab induces anti-inflammatory macrophage polarization in psoriasis: https://pmc.ncbi.nlm.nih.gov/articles/PMC12613610/

### `GSE117468` - brodalumab / ustekinumab phase 3 psoriasis substudy

- Source: GEO accession page.
- Therapy classes:
  - brodalumab anti-IL17RA -> **Class A**;
  - ustekinumab anti-IL12/23 -> **Class A**;
  - placebo arm can serve as contextual control but not primary biologic validation.
- Design: subset of 116 patients from AMAGINE-1/2/3 phase 3 trials; 140 mg brodalumab, 210 mg brodalumab, ustekinumab, and placebo; lesional and non-lesional biopsies at baseline, week 4, and week 12; 844 samples.
- Access: GEO sample tables and raw CEL/series matrix should be public.
- Response labels:
  - GEO sample titles encode patient ID, tissue, visit, and treatment.
  - Clinical response labels are not visible in the accession summary, but the source phase 3 substudy and downstream response-model papers indicate PASI response features are available or derivable from supplementary clinical data.
- V7 use:
  - Primary: early delta IFN/APC from W4 LS minus BL LS for brodalumab and ustekinumab arms.
  - Secondary: W12 delta; placebo as negative/context arm.
  - Strong because it is large and includes two Class A biologic mechanisms.
- Source anchors:
  - GEO summary: 116 patients, 844 samples, BL/W4/W12, brodalumab/placebo and ustekinumab sample titles: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE117468
  - Response modeling paper using GSE117468 for brodalumab response: https://pmc.ncbi.nlm.nih.gov/articles/PMC12378525/

### `GSE201827` - secukinumab ObePso-S psoriasis

- Source: GEO accession page.
- Therapy class: secukinumab anti-IL17A -> **Class A**.
- Design: randomized 2:1 secukinumab 300 mg versus placebo, stratified by body weight; placebo switched to secukinumab at week 12; lesional and non-lesional skin biopsies at baseline, week 12, and week 52; 434 samples.
- Access: GEO series matrix/raw data; Affymetrix GPL570.
- Response labels:
  - GEO summary confirms trial design and treatment assignment.
  - Need source paper/supplement for PASI/IGA response labels or derive response from available clinical metadata if present in series matrix.
- V7 use:
  - Class A early delta is limited: first on-treatment transcriptome is W12, not week 1/2/4.
  - Still useful because randomized placebo arm and large sample count provide strong contextual validation.
- Source anchor: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE201827

### `GSE171012` - secukinumab longitudinal psoriasis, bulk and sorted T cells

- Source: GEO accession page and publication.
- Therapy class: secukinumab anti-IL17A -> **Class A**.
- Design: 15 moderate-to-severe plaque psoriasis patients treated with secukinumab; lesional skin at pretreatment and weeks 2, 4, 12; healthy skin controls; bulk tissue plus sorted CD8 T cells, CD4 Teff, and CD4 Treg; 271 RNA-seq samples.
- Access: GEO processed count TSV (`GSE171012_CountData_SecukinumabPsoRnaSeq_20210324.tsv.gz`) plus raw SRA.
- Response labels:
  - GEO/paper state secukinumab was clinically effective but do not obviously expose binary responder/nonresponder labels.
  - Use as pharmacodynamic/mechanistic cohort unless individual PASI response labels can be recovered.
- V7 use:
  - Excellent early delta timepoints W2 and W4.
  - Less ideal for primary AUC because apparent lack of explicit nonresponder labels and focus on treatment mechanism.
- Source anchor: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE171012

### `GSE51440` - guselkumab psoriasis

- Source: GEO accession page.
- Therapy class: guselkumab anti-IL23p19 -> **Class A**.
- Design: phase 1 randomized, double-blind, placebo-controlled first-in-human study; moderate-to-severe psoriasis skin biopsies; baseline, week 1, week 12; 59 samples.
- Access: GEO sample tables, series matrix, raw CEL; processed data included in sample table.
- Response labels:
  - GEO confirms clinical/molecular response but does not expose responder labels in summary.
  - Publication reports clinical improvements and sustained-remission subgroup; response labels may require supplement/manual join.
- V7 use:
  - Strong for early delta IFN/APC at week 1.
  - Good IL-23 class validation if response labels can be recovered; otherwise pharmacodynamic/context cohort.
- Source anchors:
  - GEO: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE51440
  - OmicsDI summary mentions 11 sustained-remission subjects off therapy: https://www.omicsdi.org/dataset/geo/GSE51440

### `GSE85034` - adalimumab / methotrexate psoriasis

- Source: GEO accession page and local V3 use.
- Therapy class:
  - adalimumab anti-TNF -> **Class A**;
  - methotrexate is not a biologic but can be exploratory inflammatory-input comparator.
- Design: moderate-to-severe psoriasis; skin tissue at baseline non-lesional and lesional, weeks 1, 2, 4, and 16; 179 samples.
- Access: GEO series matrix; Illumina HumanHT-12 V4.0.
- Response labels:
  - GEO title/summary explicitly frames early expression prediction of long-term treatment response.
  - Local V3 artifacts already include `patient_response_table.tsv`; do not treat as V6 derivation, but note prior local use in V3.
- V7 use:
  - Very strong Class A anti-TNF validation candidate if V7 accepts prior V3-but-not-V6 cohorts.
  - Primary feature: week 1 minus baseline lesional IFN/APC, signed negative.
- Source anchor: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE85034

### `GSE41663` / `GSE41664` - etanercept psoriasis

- Source: GEO accession pages.
- Therapy class: etanercept anti-TNF -> **Class A**.
- Design:
  - `GSE41663`: subset of samples from etanercept trial `GSE11903`, 14 patients, baseline lesional/non-lesional plus post-dose samples; weeks 1, 2, 4, and for some subjects week 12; 81 samples.
  - `GSE41664`: superseries containing `GSE41663` plus psoriatic lesional/non-lesional sets; 157 samples total.
- Access: GEO processed sample tables and raw CEL; Affymetrix GPL570.
- Response labels:
  - Not visible in GEO summary.
  - May require original `GSE11903`/publication supplementary clinical response labels.
- V7 use:
  - Useful anti-TNF early-delta validation if response labels can be joined.
  - Otherwise pharmacodynamic/supporting cohort.
- Source anchors:
  - `GSE41663`: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE41663
  - `GSE41664`: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE41664

### `GSE69967` - tofacitinib psoriasis

- Source: GEO accession page.
- Therapy class: tofacitinib JAK inhibition -> **Class A**.
- Design: randomized phase 2; 12 plaque psoriasis patients randomized 3:1 to tofacitinib 10 mg BID or placebo for 12 weeks; non-lesional baseline and lesional baseline, days 1 and 3, weeks 1, 2, 4, 12.
- Access: GEO series matrix/raw; Affymetrix GPL570.
- Response labels:
  - GEO summary reports clinical and histologic response associations but does not present clear binary labels in accession summary.
  - Small sample size and 3:1 randomization limit AUC validation.
- V7 use:
  - Excellent early pharmacodynamic Class A/JAK comparator.
  - Lower priority for primary response validation unless responder/nonresponder labels are recoverable.
- Source anchor: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE69967

## Other Autoimmune Cohorts

### `GSE172188` - RA abatacept synovium

- Disease: rheumatoid arthritis.
- Therapy: abatacept CTLA4-Ig costimulation blockade.
- Locked class: likely **Class C** by V7 because it is non-APC-primary/costimulation and not inflammatory-input blockade in the same sense; can be exploratory unless a pre-registered APC hypothesis is documented.
- Design: synovial biopsies from the same joint before W0 and W16 after abatacept 125 mg weekly.
- Response labels: publication reports EULAR/remission categories and 7/14 remission at W16; GEO summary likely has paired samples, labels may require paper supplement.
- Access: public GEO.
- V7 use: exploratory falsification/context, not primary validation unless orchestrator explicitly pre-registers APC-relevant hypothesis under Class C exception.
- Source anchors:
  - GEO: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE172188
  - Publication: https://pmc.ncbi.nlm.nih.gov/articles/PMC8435834/

### RA anti-TNF response meta-cohorts

- Disease: rheumatoid arthritis.
- Therapy: infliximab/anti-TNF -> **Class A**.
- Candidate accessions from published systematic analysis: `GSE3592`, `GSE8350`, `GSE12051`, `GSE42296`, `GSE58795`, `GSE20690`, `GSE33377`, `GSE78068`.
- Response labels: published analysis states pretreatment blood samples with later response to infliximab were available.
- Baseline/early availability: mostly baseline-only; likely no early delta.
- Access: public GEO per paper, but each accession needs V7 ledger verification.
- V7 use: baseline-only Class A validation; high value for second disease if not used in V6.
- Source anchor: systematic analysis lists eight GEO accessions and response criteria: https://pmc.ncbi.nlm.nih.gov/articles/PMC5404751/

### Sjogren TRACTISS / multi-trial transcriptomic response

- Disease: primary Sjogren's disease.
- Therapies: rituximab, abatacept, hydroxychloroquine/leflunomide in recent pooled transcriptomic stratification.
- Locked class:
  - rituximab is **Class C** under V7 cell depletion;
  - abatacept likely **Class C**;
  - HCQ/LEF not a clean biologic/JAK Class A/B.
- Response labels: recent PubMed record reports responder differences across randomized trials; TRACTISS had substantial biospecimen collection.
- Access:
  - A TRACTISS RNA-seq web resource exists, but GEO-style download status is not established in this scout.
  - Treat as possible but not immediately V7-ready until data download terms are confirmed.
- V7 use: likely exploratory/context, not primary locked validation.
- Source anchors:
  - PubMed pooled transcriptomic stratification: https://pubmed.ncbi.nlm.nih.gov/41448992/
  - TRACTISS resource page: https://tractiss.hpc.qmul.ac.uk/
  - TRACTISS biospecimen/data-resource metrics: https://www.qmul.ac.uk/whri/emr/clinical-trials-emr/tractiss/

### SLE biologic / immunosuppressive response transcriptomics

- Disease: SLE.
- Therapies found in public literature: belimumab, rituximab, cyclophosphamide, mycophenolate, anifrolumab.
- Locked class:
  - belimumab and rituximab are B-cell axis/cell-depletion-like and probably **Class C** under current V7 rule unless an APC-relevant pretreatment hypothesis is pre-registered.
  - anifrolumab is exogenous IFN-receptor blockade, not Class B IFN-beta reprogramming; likely not cleanly classed without a V7 amendment.
- Response labels: publications report treatment response analyses.
- Access: no GEO accession verified in this scout for the belimumab/SLE RNA-seq response paper; PMC access was blocked by browser check during scouting.
- V7 use: lower priority until accession and clean locked-class mapping are established.
- Source anchors:
  - SLE treatment transcriptome paper summary: https://pmc.ncbi.nlm.nih.gov/articles/PMC11931925/
  - Belimumab blood transcriptome response PubMed: https://pubmed.ncbi.nlm.nih.gov/39919899/

## Recommended Acquisition Order

1. `GSE117468` first. It is large, public, psoriasis, Class A, two biologic mechanisms, baseline plus W4/W12, and likely recoverable PASI response labels.
2. `GSE85034` second if prior V3 use is acceptable. It is the cleanest anti-TNF psoriasis response cohort with early weeks 1/2/4 and explicit response framing.
3. `GSE201827` third. It adds randomized secukinumab but first on-treatment transcriptome is W12.
4. `GSE51440` fourth. Excellent IL-23 early-delta design, but response labels need supplement recovery.
5. `GSE228421` as mechanism-sidecar, not primary validation, unless processed scRNA and binary response labels are recovered.
6. `GSE41663/GSE41664` if etanercept response labels can be joined.
7. RA anti-TNF baseline cohorts as second-disease baseline-only validation once psoriasis pipeline is working.

## Immediate Risks

- Many psoriasis treatment cohorts show strong clinical response with few or no nonresponders; they may support pharmacodynamic delta but not ROC AUC validation.
- Skin biopsy signal may be dominated by keratinocyte normalization, not APC architecture. V7 analysis should pre-register whole-lesion versus APC/deconvolved sensitivity.
- `GSE228421` is attractive but small (`n=5`) and raw data access may be dbGaP-limited.
- `GSE85034` was used in V3, so the orchestrator should decide whether "not used in V6" is sufficient for V7 independent validation. It is not excluded by `LOCKED_RULE_V7.md`, but it is not a clean never-seen cohort.
