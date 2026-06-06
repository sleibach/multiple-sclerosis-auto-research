# DATA_SCOUT_V24: Treatment-Response Validation Cohort Scout

Date: 2026-06-06

## Question

V23 concluded that no fresh held-out cohort remained for the bounded APC/HLA-II early-treatment monitoring rule. V24 tested whether that was a real data limitation or an artifact of analysis-time searching.

Target cohort specification:

- Human transcriptomics: bulk, sorted-cell, or single-cell.
- Treatment-response context, ideally MS disease-modifying therapy; bounded-domain cross-disease immune-remodeling or JAK-STAT therapy also acceptable.
- Baseline plus early on-treatment samples preferred; longitudinal later samples recorded as lower value.
- Clinical response, remission, relapse-free, or comparable outcome label.
- Not used in V6/V7 derivation or V22/V23 validation.

Excluded as already used: `GSE282122`, `GSE138064`, `GSE24427`, `GSE16879`, `GSE73661`, `GSE8350`, `GSE12051`, `GSE12251`, `GSE138746`, `GSE235357`, `GSE250453`, `GSE85034_ADA`, and `GSE253006`.

## Direct Answer

The public/low-barrier well is **not completely dry**, but there is **no clean, public, n>=30, fresh MS DMT transcriptomic validation cohort** ready for immediate V25 locked validation.

The best true validation target is **Gafson et al. 2018 DMF PBMC RNA-seq** (PMID `30283812`, DOI `10.1212/nxi.0000000000000470`): 24 RRMS patients sampled at baseline, 6 weeks, and 15 months, with NEDA-4 responder definition in the PubMed abstract. This is exactly the right therapy and timepoint class, but V24 did not find a clean public GEO/SRA/ENA accession. It is therefore **Tier 2 low-barrier author/data request**, not Tier 1 ready.

The best open but incomplete MS source is **GSE130478/GSE130491/GSE130494** (PMID `31300673`, DOI `10.1038/s41467-019-11139-3`): public longitudinal DMF data with response biology in the paper/series summary. The expression cohort is CD4 T-cell baseline/6-month array data, and response labels were not present in the GEO matrix. It is useful after label acquisition, but it is not a clean early-dynamic V22-rule validation cohort.

The only verified Tier 1 fresh testable transcriptomic subgroup found locally is the **unused GSE85034 methotrexate arm**: psoriasis lesional skin, 13 PASI75-labeled subjects, paired baseline/week16, 9 frozen-module genes present. It is a secondary stress test, not a clean independent MS validation, because the adalimumab arm from the same study was already used and the tissue/timepoint are not the bounded MS/JAK/DMF target.

## Ranked Inventory

| Rank | Source | Fit | Access | Verified usability | Verdict |
|---:|---|---|---|---|---|
| 1 | Gafson et al. 2018, PBMC RNA-seq DMF, PMID `30283812` | Excellent: MS, DMF, baseline/6w/15m, NEDA-4 response | Tier 2 low-barrier author request | PubMed abstract verifies design and labels; no public accession found by GEO/SRA/ENA search | **Best next validation cohort** if processed counts and sample labels can be obtained. |
| 2 | `GSE130478/GSE130491/GSE130494`, Karolinska DMF ROS cohort | Good but imperfect: MS DMF, paired, response biology | Tier 2 for labels; expression/methylation data open | GEO matrix confirms CD4 expression baseline/6m and CD14/CD4 methylation baseline/3m/6m; labels absent from metadata | Useful secondary MS DMF cohort after labels; 6m expression is outside early-window lock. |
| 3 | `GSE85034` methotrexate arm | Cross-disease secondary: psoriasis MTX | Tier 1 local/open | Local metadata: 13 PASI75-labeled MTX subjects; paired baseline/week16; 9 frozen genes represented | Fresh subgroup but same source as used ADA arm; secondary stress test only. |
| 4 | `GSE253495`, RA upadacitinib CD14 monocytes | JAK-class pharmacodynamic source | Tier 1 open | GEO confirms 3 paired baseline/3m RNA-seq patients; all improved | Not a validation cohort because no nonresponder class. |
| 5 | Diebold et al. 2022, DMF high-dimensional immune profiling, PMID `35881799` | Relevant monitoring biology | Tier 1 literature/supplement | Mass cytometry, not transcriptomics | Mechanistic context only; cannot compute locked gene modules. |
| 6 | Filgotinib UC immune-cell expression literature hit | Potential bounded-domain JAK/UC | Tier 2 uncertain | Repository accession not verified in V24 | Needs paper-specific data-availability tracing. |
| 7 | RA tofacitinib multi-omics literature hit | Potential bounded-domain JAK/RA | Tier 2 uncertain | Repository accession not verified in V24 | Needs paper-specific data-availability tracing. |
| 8 | MultipleMS / MS PATHS / Accelerated Cure Project / EGA / ImmPort | Potential MS DMT controlled-access sources | Tier 2/3 | No direct open paired transcriptomic validation dataset verified | Strategic access path, not immediate V25 data. |

See `analysis/v24_data_scout/v24_candidate_inventory.tsv` for the machine-readable inventory.

## Source-Type Coverage

### 1. GEO

Searched MS DMTs and bounded-domain therapies. Verified hits:

- `GSE130478`: expression array, 14 MS patients baseline/6m after DMF, CD4 T cells. Response/nonresponse is stated in the series summary/paper but not in sample metadata.
- `GSE130491`: methylation profiling, 19 MS patients baseline/3m/6m after DMF, CD14/CD4 cells. Not transcriptomic.
- `GSE253495`: RA upadacitinib CD14 monocyte RNA-seq, 3 paired patients, all improved. Not a responder/nonresponder validation cohort.

False or rejected hits:

- `GSE261258`: MS B-cell TIM-1/TIGIT biology, not treatment response.
- `GSE143443`: RA fibroblast-like synoviocyte joint-location study, not treatment response.
- `GSE240466/GSE240335`: lichen planus IFN landscape, not SLE anifrolumab response.
- `GSE312339/GSE231871`: false positives from Gafson/DMF queries.

### 2. ArrayExpress / BioStudies

BioStudies searches found relevant publications but no additional ready transcriptomic validation cohort beyond the GEO records above. `S-EPMC9351505` is a DMF monitoring paper but uses high-dimensional immune profiling rather than transcriptomic module genes. `S-EPMC3094352` is IFN-beta response and belongs to the already-used V6/V7 lineage.

### 3. ENA / SRA

SRA exact-author/title searches did not produce a clean accession for the Gafson DMF RNA-seq cohort. Broad SRA queries returned nonspecific results or false positives. ENA quoted query attempts returned HTTP 400 and no accession was verified. The absence of a clean accession is part of the Tier 2 classification for Gafson et al.

### 4. EGA

The EGA search endpoint attempted in this run returned HTTP 404. No EGA dataset was verified from the sandbox. This remains a controlled-access scout gap, not evidence that no EGA source exists.

### 5. Zenodo, Figshare, Dryad, OSF

Zenodo returned broad topical hits but no verified paired/labeled treatment-response transcriptomic cohort. Narrower Zenodo queries timed out. Figshare API queries returned HTTP 404. OSF returned topical but nonspecific projects, not treatment-response transcriptomics. Dryad was not linked by any verified candidate record in this run.

### 6. Published-Paper Mining

Three exact paper records matter:

- Gafson et al. 2018, PMID `30283812`: best target; PBMC RNA-seq, DMF, baseline/6w/15m, NEDA-4 response. Needs author/data request because no public accession was found.
- Carlstrom/Ewing et al. 2019, PMID `31300673`: public GEO expression/methylation data; response labels not in GEO metadata.
- Diebold et al. 2022, PMID `35881799`: high-dimensional immune profiling, monitoring-relevant but not transcriptomic validation.

### 7. Consortia and Cohort Portals

Searches for MultipleMS, MS PATHS, Accelerated Cure Project, and ImmPort did not reveal a directly downloadable paired transcriptomic DMT response cohort. These remain Tier 2/3 collaboration or portal-access routes.

### 8. Preprint Supplements

bioRxiv/medRxiv-oriented Europe PMC searches returned broad or unrelated results. No fresh paired/labeled validation cohort was verified from preprint supplements.

### 9. Partially Used Datasets

`GSE85034` contains an unused methotrexate arm. It is verified local/open and has response labels, but it is psoriasis lesional skin and late week-16 endpoint. It can be a secondary V25 stress test if a successor validation plan explicitly permits partially used datasets and same-study caveats.

## Tier 1 Sources Ready Now

No Tier 1 source meets the ideal fresh MS DMT validation spec.

Tier 1 source usable only as secondary stress test:

- `GSE85034_MTX`: local data at `data/raw_v3/wave89_psoriasis_response/GSE85034_series_matrix.txt.gz`; 13 PASI75-labeled MTX subjects; paired baseline/week16 lesional skin; module coverage 9 frozen genes.

Tier 1 source usable only for pharmacodynamics:

- `GSE253495`: open GEO RA upadacitinib CD14 monocyte RNA-seq; 3 paired patients, all improved; no response-discrimination labels.

## Tier 2 Low-Barrier Human Actions

1. Request Gafson et al. 2018 DMF PBMC RNA-seq processed counts and sample-level metadata.
   - Ask for: normalized and/or raw gene counts for all 24 RRMS patients at baseline, 6 weeks, and 15 months; sample-to-patient map; NEDA-4 responder status; any batch/covariate table.
   - Why: this is the single best validation cohort for the V22/V23 bounded monitoring rule.
   - Suggested subject: `Data request for DMF PBMC RNA-seq response cohort (PMID 30283812)`.

2. Request response labels for `GSE130478/GSE130491/GSE130494`.
   - GEO contact: `ewoud.ewing@ki.se`.
   - Ask for: patient-level beneficial-response/nonresponder labels, mapping to Patient_1..Patient_14/19, and any clinical covariates.
   - Why: open expression/methylation data are already public; labels would make this a useful secondary MS DMF cohort.

3. Trace the filgotinib UC and RA tofacitinib multi-omics papers manually.
   - V24 did not verify repository accessions from top-level searches.
   - Ask only after identifying the exact paper and data availability statement.

## Tier 3 / Controlled or Collaboration Paths

- MultipleMS, MS PATHS, Accelerated Cure Project, EGA/controlled MS cohorts.
- Required files: paired baseline/early-treatment expression matrices, response labels, therapy/timepoint metadata.
- Governance: individual-level clinical transcriptomics may carry usage restrictions; obtain institutional approval and follow portal terms before placing files in the sandbox.

## What the Human Should Do Next

1. **Highest leverage:** obtain the Gafson et al. DMF PBMC RNA-seq data and metadata. This is the only identified cohort that directly matches MS, DMF, early on-treatment timing, transcriptomics, and response labels.
2. **Second:** request `GSE130478/GSE130491/GSE130494` response labels from the GEO contact. This converts public data into a secondary MS validation cohort.
3. **Optional immediate V25 stress test:** run the locked V22/V23 rule on `GSE85034_MTX` as a caveated secondary cross-disease stress test, not as primary validation.
4. **Portal path:** pursue consortium/controlled MS cohorts only after the two low-barrier requests above, because those require more process and were not directly available in V24.

## Bottom Line

The earlier "no fresh held-out cohort remained" statement was too strong. V24 found no clean public ready-to-run MS validation cohort, but it did find a strong low-barrier target (Gafson et al. 2018) and one open but label-incomplete MS DMF cohort (`GSE130478/GSE130491`). The correct conclusion is:

**Public ready-to-run data are effectively dry for primary validation, but low-barrier data are not dry. The next validation unlock is human acquisition of Gafson et al. processed RNA-seq plus NEDA-4 labels.**
