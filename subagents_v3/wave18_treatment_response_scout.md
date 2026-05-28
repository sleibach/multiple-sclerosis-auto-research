# Wave18-A Treatment-Response Scout

Date: 2026-05-27

## Scope

Goal: test whether V3 lysosomal/APC/HLA-II/IFN module readouts predict baseline treatment response or change pharmacodynamically after autoimmune treatment, avoiding all-cell bulk-like scores where compartment-resolved analysis is feasible.

V3 modules used from `scripts/v3_analyze_direct_h5ad_cell_states.py`: `ifn_apc`, `hla_ii_apc`, `lysosomal_apc`, `mif_cd74_receptor_state`, `mixscale_validated_ifng_readout`, `lipid_loader_repair`, `complement_phagocytosis`, `hif_nampt_metabolic`, `inflammatory_nfkb`.

Script run:

```bash
./.venv_v3_py312/bin/python scripts/v3_wave18_treatment_response_scout.py
```

Main output directory:

```text
results_v3/wave18_treatment_response/
```

## Datasets

| Accession | Disease | Treatment | Status | Why |
|---|---:|---:|---|---|
| `GSE253006` | UC | tofacitinib | Reused existing V3 marker-compartment analysis | Per-sample 10x matrices, response labels, pre/post timepoints; no curated cell labels, but marker compartments feasible. GEO: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE253006 |
| `GSE138746` | RA | adalimumab / etanercept | Analyzed | Baseline RNA-seq in sorted PBMC, CD14 monocyte, CD4 T compartments; sample names encode EULAR response class `g/m/n`. GEO: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE138746 |
| `GSE183047` | psoriasis | secukinumab anti-IL-17A | Analyzed | Immune-enriched scRNA-seq before/after treatment; no response labels, so pharmacodynamic-only. GEO: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE183047 |
| `GSE261334` | UC | vedolizumab | Parked | GEO states 5 responders and 5 non-responders at week 0/week 6, but donor-level response labels are not in SOFT. Do not infer response labels from sample order. GEO: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE261334 |
| `GSE296117` | RA | TNF-alpha/JAK inhibitor | Parked | Synovial-fluid scRNA pre/post, 106,506 cells, but only 2.3 GB RDS exposed in GEO and raw human data are controlled at GSA `HRA011646`; too heavy for this scout. GEO: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE296117 |
| `GSE250453` | MS | fingolimod | Parked | Responder/non-responder baseline/12m exists, but all-PBMC bulk; low-weight sensitivity only. GEO: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE250453 |
| `GSE235357` | MS | dimethyl fumarate | Parked | Responder/non-responder baseline/12m exists, but blood/PBMC bulk; low-weight sensitivity only. GEO: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE235357 |

No tractable lupus nephritis or Sjogren treatment-response dataset with cell-resolved or sorted-compartment transcriptomes was promoted in this pass. Existing SLE/Sjogren public single-cell resources are primarily disease atlases rather than treatment-response designs.

## Inputs Downloaded

`GSE138746`:

- `data/raw_v3/wave18_gse138746/GSE138746_Counts_Normalization_PBMC.csv.gz`
- `data/raw_v3/wave18_gse138746/GSE138746_Counts_Normalization_cd14.csv.gz`
- `data/raw_v3/wave18_gse138746/GSE138746_Counts_Normalization_cd4.csv.gz`
- `data/raw_v3/wave18_gse138746/GSE138746_rawReadsData.csv.gz`
- `data/raw_v3/wave18_gse138746/GSE138746_series_matrix.txt.gz`

`GSE183047`:

- `data/raw_v3/wave18_gse183047/GSE183047_RAW.tar`, 286,566,400 bytes, 84 MTX/TSV files extracted.
- `data/raw_v3/wave18_gse183047/GSE183047_family.soft.gz`

## Outputs

```text
results_v3/wave18_treatment_response/summary.json
results_v3/wave18_treatment_response/wave18_dataset_scout.tsv
results_v3/wave18_treatment_response/wave18_existing_gse253006_uc_summary.tsv
results_v3/wave18_treatment_response/wave18_gse138746_ra_baseline_response_tests.tsv
results_v3/wave18_treatment_response/wave18_gse138746_ra_gene_map.tsv
results_v3/wave18_treatment_response/wave18_gse138746_ra_gene_presence.tsv
results_v3/wave18_treatment_response/wave18_gse138746_ra_sample_module_scores.tsv
results_v3/wave18_treatment_response/wave18_gse183047_psoriasis_compartment_counts.tsv
results_v3/wave18_treatment_response/wave18_gse183047_psoriasis_module_genes_present.tsv
results_v3/wave18_treatment_response/wave18_gse183047_psoriasis_prepost_tests.tsv
results_v3/wave18_treatment_response/wave18_gse183047_psoriasis_run_log.tsv
results_v3/wave18_treatment_response/wave18_gse183047_psoriasis_sample_module_scores.tsv
```

## Methods

`GSE138746` RA:

- Used normalized baseline RNA-seq matrices for PBMC, CD14 monocytes, and CD4 T cells.
- Mapped V3 gene symbols to Ensembl IDs via Ensembl REST and recorded mapping in `wave18_gse138746_ra_gene_map.tsv`.
- Applied `log1p`, z-scored genes within each compartment, and averaged present genes per V3 module.
- Tested `moderate/good` vs `none` and `good` vs `none`.
- Reported Welch p, Hedges g, AUC, BH FDR, and for pooled anti-TNF tests an OLS response coefficient adjusted for drug.

`GSE183047` psoriasis:

- Read each MTX sample and extracted only V3 genes plus marker genes.
- Assigned cells to marker-derived `myeloid_apc_like`, `t_cell_like`, `b_plasma_like`, `keratinocyte_like`, and `stromal_endothelial_like` compartments.
- Z-scored genes against pretreatment lesional-skin cells within each marker compartment.
- Tested earliest post-secukinumab lesional sample vs pretreatment by paired patient-level module scores.

`GSE253006` UC:

- Reused existing V3 marker-compartment outputs from `results_v3/gse253006_tofacitinib_marker/`.

## Numbers

### RA Baseline Predictor: `GSE138746`

Rows produced:

- Sample-module scores: 2,115.
- Response tests: 162.
- Gene presence rows: 165.

No baseline predictor survived BH correction. Minimum FDR was `0.6056`; minimum nominal p was `0.00763`.

Top nominal signals:

| Test | Compartment | Drug scope | Module | n | Delta R-NR | Hedges g | AUC high | p | FDR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| EULAR moderate/good vs none | CD4 T | adalimumab | `ifn_apc` | 19R/18NR | +0.586 | +0.913 | 0.751 | 0.00763 | 0.606 |
| Good vs none | CD4 T | adalimumab | `mixscale_validated_ifng_readout` | 11R/18NR | +0.473 | +1.013 | 0.783 | 0.00942 | 0.606 |
| Good vs none | CD14 monocyte | all anti-TNF, drug-adjusted | `complement_phagocytosis` | 20R/41NR | -0.321 | -0.552 | 0.311 | 0.0162 | 0.606 |
| EULAR moderate/good vs none | CD14 monocyte | all anti-TNF, drug-adjusted | `complement_phagocytosis` | 37R/41NR | -0.284 | -0.527 | 0.327 | 0.0187 | 0.606 |
| EULAR moderate/good vs none | CD14 monocyte | etanercept | `lysosomal_apc` | 17R/23NR | -0.495 | -0.796 | 0.304 | 0.0273 | 0.668 |
| EULAR moderate/good vs none | CD14 monocyte | all anti-TNF, drug-adjusted | `lysosomal_apc` | 37R/41NR | -0.277 | -0.468 | 0.367 | 0.0429 | 0.772 |

Interpretation: RA has the best baseline-response sample size and true compartment resolution, but the result is not a corrected predictor. Direction is also inconsistent with the intended biomarker branch: responder CD14 monocytes trend lower for complement/lysosomal modules, while adalimumab CD4 T cells trend higher for IFN/APC readouts.

### UC Baseline Predictor And Pharmacodynamics: `GSE253006`

Existing marker-compartment analysis:

- Total cells: 97,004.
- Samples: 23.
- Baseline samples: 11.
- Baseline response groups: 5 responders, 6 non-responders.

Baseline response:

- Minimum baseline p: `0.0353`.
- Minimum baseline FDR: `0.976`.
- Best nominal baseline row was stromal/endothelial `lipid_loader_repair` high fraction lower in responders, 4R/6NR, delta `-0.0780`, Hedges g `-1.292`, AUC `0.125`, FDR `0.976`.

Pharmacodynamic:

- Best row: responder `t_cell_like` `mixscale_validated_ifng_readout` high fraction decreased after tofacitinib, 5 pairs, mean delta `-0.114`, p `0.000395`, FDR `0.0869`.
- V3-relevant nominal decreases also included responder stromal/endothelial `lysosomal_apc` high fraction, 4 pairs, mean delta `-0.128`, p `0.0129`, FDR `0.502`; responder myeloid/APC `lysosomal_apc` mean score, 5 pairs, mean delta `-0.110`, p `0.0333`, FDR `0.502`.

Interpretation: no corrected baseline-response predictor. Pharmacodynamic signal is plausible but small-n and mostly T-cell/JAK-IFN rather than a clean myeloid APC biomarker.

### Psoriasis Pharmacodynamics: `GSE183047`

Cell assignment totals:

| Marker compartment | Cells |
|---|---:|
| `keratinocyte_like` | 36,786 |
| `t_cell_like` | 6,854 |
| `myeloid_apc_like` | 5,770 |
| `ambiguous` | 3,524 |
| `b_plasma_like` | 622 |
| `stromal_endothelial_like` | 272 |

Rows produced:

- Sample-module scores: 902.
- Pre/post tests: 88.
- Paired lesional pretreatment/posttreatment patients: 4 for analyzable compartments.

No pharmacodynamic row survived BH correction. Minimum FDR was `0.743`; minimum nominal p was `0.0157`.

Top nominal rows:

| Compartment | Module | Metric | n pairs | Mean post-pre delta | p | FDR |
|---|---:|---:|---:|---:|---:|---:|
| `keratinocyte_like` | `il17_keratinocyte_inflammation` | mean score | 4 | -0.524 | 0.0157 | 0.743 |
| `myeloid_apc_like` | `lysosomal_apc` | mean score | 4 | -0.208 | 0.0198 | 0.743 |
| `keratinocyte_like` | `il17_keratinocyte_inflammation` | high fraction | 4 | -0.212 | 0.0253 | 0.743 |
| `myeloid_apc_like` | `complement_phagocytosis` | mean score | 4 | -0.230 | 0.0653 | 0.975 |
| `myeloid_apc_like` | `lysosomal_apc` | high fraction | 4 | -0.113 | 0.0898 | 0.975 |

Interpretation: the assay recovers the expected IL-17 keratinocyte pharmacodynamic direction and gives a nominal myeloid/APC lysosomal decrease, but only 4 paired patients are analyzable and no corrected module result survives.

## Recommendation

**No-go for a baseline treatment-response biomarker branch from the current V3 module readouts.**

Reason: the two analyzable baseline-response datasets fail correction:

- `GSE138746` RA: best nominal p `0.00763`, minimum FDR `0.606`.
- `GSE253006` UC tofacitinib: best baseline p `0.0353`, minimum baseline FDR `0.976`.

The best pharmacodynamic-only evidence is:

- UC tofacitinib responder T-cell `mixscale_validated_ifng_readout` high-fraction decrease, FDR `0.0869`.
- Psoriasis secukinumab nominal myeloid/APC `lysosomal_apc` mean-score decrease, p `0.0198`, FDR `0.743`.

This is not enough to claim a cross-disease treatment-response predictor. It is enough to **park** a narrower pharmacodynamic readout hypothesis: broad anti-inflammatory/JAK/IL-17 blockade can reduce parts of the IFN/APC/lysosomal module in some compartments after treatment. That branch should be treated as mechanism-supporting pharmacodynamics, not patient-stratification.

Stop criterion for this biomarker branch: do not invest further in V3 module baseline predictor work unless one of these becomes available:

1. `GSE261334` donor-to-response crosswalk for vedolizumab responders/non-responders.
2. A tractable extraction from `GSE296117` RA synovial-fluid RDS with response or treatment-outcome labels.
3. A larger public cell-resolved IBD/psoriasis/RA treatment-response cohort with explicit baseline response labels and curated or defensible marker compartments.

Until then, prioritize target/mechanism work over treatment-response biomarker development.
