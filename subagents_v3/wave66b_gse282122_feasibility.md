# Wave66-B Scout Report: GSE282122 Feasibility for V3 Myeloid/APC Module Testing

Scout scope: feasibility only. I do not claim a therapeutic finding.

Inspection date: 2026-05-27.

## Bottom Line

Recommendation: **GO, but only via the public Zenodo v3 companion myeloid object, not GEO-only tar files.**

Promotion criterion is met: a patient/site-level myeloid/APC pseudobulk perturbation analysis can be run without full atlas reintegration. The decisive file is `myeloid_final.h5ad` from Zenodo record `14007626`, which contains raw count-like sparse `X`, per-cell myeloid/DC annotations, `sample_id`, `Patient`, `Disease`, `Site`, `Treatment`, `Inflammation_score`, `Batch`, and `Remission_status`. A 3.1 kB paired-sample manifest identifies 55 site-matched pre/post biopsy pairs.

GEO-only is **not** sufficient for the cell-state analysis because the two GSE282122 GEO supplementary archives expose per-sample 10x `.h5` matrices, not the integrated/annotated cell-state object. Strictly using those archives would require reannotation/reintegration and should be demoted for this session.

## Sources Inspected

Primary GEO record:

- GEO accession page: `https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE282122`
- Series matrix: `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE282nnn/GSE282122/matrix/GSE282122_series_matrix.txt.gz`
- GEO filtered archive: `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE282nnn/GSE282122/suppl/GSE282122_filtered_processed_data.tar.gz`
- GEO raw archive: `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE282nnn/GSE282122/suppl/GSE282122_raw_processed_data.tar.gz`

Companion processed atlas record:

- Zenodo record: `https://zenodo.org/records/14007626`
- Zenodo API: `https://zenodo.org/api/records/14007626`
- Myeloid object: `https://zenodo.org/api/records/14007626/files/myeloid_final.h5ad/content`
- Paired manifest: `https://zenodo.org/api/records/14007626/files/paired_sample_list.csv/content`

Paper/context:

- Nature Immunology article: `https://www.nature.com/articles/s41590-024-01994-8`
- PMID: `39438660`
- BioProject: `PRJNA1179412`

## Exact Public File Inventory

### GEO GSE282122

The GEO page lists 216 samples and two supplementary tar archives.

Observed HTTP headers:

- `GSE282122_filtered_processed_data.tar.gz`
  - URL: `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE282nnn/GSE282122/suppl/GSE282122_filtered_processed_data.tar.gz`
  - Content-Length: `3027066520` bytes
  - GEO display size: 2.8 GB
  - Type: `application/x-gzip`
- `GSE282122_raw_processed_data.tar.gz`
  - URL: `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE282nnn/GSE282122/suppl/GSE282122_raw_processed_data.tar.gz`
  - Content-Length: `9046536153` bytes
  - GEO display size: 8.4 GB
  - Type: `application/x-gzip`
- `GSE282122_series_matrix.txt.gz`
  - URL: `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE282nnn/GSE282122/matrix/GSE282122_series_matrix.txt.gz`
  - Content-Length: `11652` bytes

Archive contents are only partly knowable without full sequential gzip streaming. Partial tar streams established this pattern:

```text
filtered_processed_data/
filtered_processed_data/CID003376-1/
filtered_processed_data/CID003376-1/filtered_feature_bc_matrix.h5
filtered_processed_data/CID005771-1/
filtered_processed_data/CID005771-1/filtered_feature_bc_matrix.h5
...

raw_processed_data/
raw_processed_data/CID003376-1/
raw_processed_data/CID003376-1/raw_feature_bc_matrix.h5
raw_processed_data/CID005771-1/
raw_processed_data/CID005771-1/raw_feature_bc_matrix.h5
...
```

Interpretation: GEO archives are per-sample 10x feature-barcode HDF5 matrices. They are useful for reprocessing but are not the minimal route for V3 because they do not expose the paper's cell-state annotations.

### Zenodo v3 Companion Files

The Zenodo record description says the October 30, 2024 v3 release supersedes earlier releases because prior metadata were incorrect. This matters: use v3 only.

Relevant files from `https://zenodo.org/api/records/14007626`:

| File | Size bytes | MD5 | Download |
|---|---:|---|---|
| `myeloid_final.h5ad` | 416,722,961 | `bdfe50345a11abdb1a72b2439bf9950e` | `https://zenodo.org/api/records/14007626/files/myeloid_final.h5ad/content` |
| `paired_sample_list.csv` | 3,102 | `3300a53889bb4b70c48ec66dbb66beea` | `https://zenodo.org/api/records/14007626/files/paired_sample_list.csv/content` |
| `TAURUS_raw_counts_annotated_final.h5ad` | 12,708,413,650 | `c1bd13b92cacb164a401c6c4a4e7912c` | `https://zenodo.org/api/records/14007626/files/TAURUS_raw_counts_annotated_final.h5ad/content` |
| `UMAP_combined_objects.txt.gz` | 15,580,288 | `6b45dba506fc2279da1861e21b561a0f` | `https://zenodo.org/api/records/14007626/files/UMAP_combined_objects.txt.gz/content` |
| `PC_combined_objects.txt.gz` | 1,188,318,207 | `d1f475b90097f5e63b0a9884accfd0fc` | `https://zenodo.org/api/records/14007626/files/PC_combined_objects.txt.gz/content` |

Other compartment `.h5ad` files exist (`bcells_final.h5ad`, `cd4tcells_final.h5ad`, `cd8tcells_final.h5ad`, `epicolonic_final.h5ad`, `fibperi_final.h5ad`, `ilealepi_final.h5ad`, `ilc_final.h5ad`, `plasmacells_final.h5ad`, `vasc_final.h5ad`), but they are not needed for this scout task.

## Metadata Available

### GEO Series Matrix

GEO sample metadata fields include:

- `tissue: gut`
- `librarytype: 3 prime V3` / `3 prime v3.1`
- `cellsloaded`
- `disease: UC` / `CD` / `Healthy`
- `disease duration`
- `patient`
- `site: Rectum`, `Descending_Colon`, `Ascending_Colon`, `Terminal_Ileum`, `Sigmoid`
- `inflammation: Inflamed`, `Non_Inflamed`, `Healthy`
- `treatment: Pre`, `Post`, `None`
- `age`
- `Sex`
- `ethnicity`
- `match: Yes` / `No`
- `batch: Batch_1` to `Batch_4`
- `inflammation score`

The GEO matrix is enough to reconstruct sample-level covariates and match against the Zenodo `sample_id`.

### `myeloid_final.h5ad`

Inspected with `anndata 0.12.16`, backed mode.

Object shape:

- Cells: `30,858`
- Genes/features: `33,075`
- `X`: CSR sparse matrix
- `X` nonzero entries: `45,481,461`
- `X.data` dtype: `float32`
- First `X.data` values are integer-like raw counts, and `uns/log1p` is empty. Treat `X` as raw count-like data for pseudobulk summation unless downstream inspection contradicts this.

Key `obs` columns:

```text
sample_id
Patient
Disease
Site
Treatment
Disease_duration
Inflammation
Age
Gender
Ethnicity
Inflammation_score
Ileum_vs_Colon
LibraryType
CellsLoaded
Match
Batch
cellbarcode
final_analysis
minor
major
sub_bucket
bucket
Remission_status
```

Cell-state hierarchy:

- `bucket`: `Myeloid`
- `major`: `Mono_macro`, `DC`, `Cycling_MNP`, `Mast`
- `minor`: `Macro`, `Mono`, `DC`, `Cycling_MNP`, `Mast`
- `final_analysis`: 11 fine states

Fine state counts:

| `final_analysis` | Cells |
|---|---:|
| `CD1Chi DC` | 6,466 |
| `S100A8 A9hi mono` | 6,050 |
| `C1Qhi IL1Bhi macro` | 4,255 |
| `C1Qhi IL1Blo macro` | 4,220 |
| `Mast` | 3,968 |
| `XCR1pos DC` | 1,237 |
| `Cycling MNP` | 1,214 |
| `S100A8 A9hi TNFhi IL6pos mono` | 1,182 |
| `LAMP3pos DC` | 796 |
| `pDC` | 768 |
| `LAMP3pos IL1Bpos DC` | 702 |

Major state counts:

| `major` | Cells |
|---|---:|
| `Mono_macro` | 15,707 |
| `DC` | 9,969 |
| `Mast` | 3,968 |
| `Cycling_MNP` | 1,214 |

Available subject/timepoint/remission fields:

- `Patient`: 41 unique patients
- `Disease`: `UC`, `CD`, `Healthy`
- `Treatment`: `Pre`, `Post`, missing/none for healthy
- `Remission_status`: `Remission`, `Non_Remission`, `None `, `Not_avail`
- `Site`: five gut regions
- `Inflammation_score`: continuous sample-level score
- `Match`: yes/no site matching indicator
- `Batch`: four batches

## Module Gene Coverage

All V3 module genes checked are present in `myeloid_final.h5ad`:

| Module | Present / Total | Present genes |
|---|---:|---|
| `lipid_loader_repair` | 14 / 14 | `APOE`, `APOC1`, `TREM2`, `GPNMB`, `LPL`, `SPP1`, `LGALS3`, `FABP5`, `CD9`, `AXL`, `MERTK`, `LIPA`, `LAMP1`, `CTSD` |
| `lysosomal_apc` | 14 / 14 | `LAMP1`, `LAMP2`, `CTSB`, `CTSD`, `CTSS`, `LIPA`, `IFI30`, `HLA-DRA`, `HLA-DRB1`, `HLA-DPA1`, `HLA-DPB1`, `CD74`, `PSAP`, `NPC2` |
| `complement_phagocytosis` | 12 / 12 | `C1QA`, `C1QB`, `C1QC`, `C3`, `TYROBP`, `FCGR3A`, `FCGR2A`, `ITGAM`, `ITGB2`, `AIF1`, `VSIG4`, `MRC1` |
| `tnf_autocrine_nfkb` | 11 / 11 | `TNF`, `TNFAIP3`, `NFKBIA`, `REL`, `RELA`, `IL1B`, `IL6`, `CXCL8`, `CCL3`, `CCL4`, `NFKB1` |

## Paired-Sample Feasibility

`paired_sample_list.csv` has 110 samples:

| Category | Samples |
|---|---:|
| `UC_Non_Remission` | 42 |
| `CD_Remission` | 38 |
| `UC_Remission` | 16 |
| `CD_Non_Remission` | 14 |

All 110 manifest samples are present in `myeloid_final.h5ad`.

Derived by grouping `Patient + Disease + Site + Category` and requiring both `Pre` and `Post`:

| Disease/category | Site-matched pre/post pairs | Patients | Pre myeloid cells | Post myeloid cells |
|---|---:|---:|---:|---:|
| `CD_Non_Remission` | 7 | 5 | 2,245 | 3,528 |
| `CD_Remission` | 19 | 10 | 4,563 | 2,254 |
| `UC_Non_Remission` | 21 | 13 | 2,875 | 4,054 |
| `UC_Remission` | 8 | 4 | 1,370 | 607 |
| **Total** | **55** | **32 unique patient-category/site groups** | **11,053** | **10,443** |

Per-pair myeloid cell counts:

- Pre median: `182` cells; range `14` to `680`
- Post median: `147` cells; range `27` to `1,574`

Broad state paired support, requiring both pre and post to have at least the threshold number of cells:

| Threshold per side | `Mono_macro` pairs | `DC` pairs | `Cycling_MNP` pairs | `Mast` pairs |
|---:|---:|---:|---:|---:|
| 10 cells | 52 | 53 | 5 | 16 |
| 20 cells | 43 | 43 | 0 | 7 |
| 50 cells | 27 | 16 | 0 | 1 |
| 100 cells | 9 | 4 | 0 | 0 |

Fine-state support is uneven. With at least 20 cells pre and post in the same fine state, the strongest strata are:

- `CD1Chi DC`: 13 CD remission pairs, 8 UC non-remission pairs, 6 CD non-remission pairs
- `S100A8 A9hi mono`: 11 UC non-remission pairs, 4 CD non-remission pairs, 3 CD remission pairs
- `C1Qhi IL1Blo macro`: 9 UC non-remission pairs, 6 CD remission pairs, 4 CD non-remission pairs
- `C1Qhi IL1Bhi macro`: 7 UC non-remission pairs, 4 CD remission pairs, 4 CD non-remission pairs

Implication: use `major` level (`Mono_macro`, `DC`) as the primary endpoint; use fine states as secondary/descriptive endpoints. Rare states such as `LAMP3pos DC`, `pDC`, `XCR1pos DC`, and `Cycling MNP` should not be primary perturbation endpoints.

## Minimal Feasible Analysis Plan

Goal: test whether anti-TNF-associated longitudinal shifts in V3 lipid-lysosomal/APC modules occur in myeloid/APC states and whether those shifts differ by remission outcome, without atlas reintegration.

1. Download only:
   - `myeloid_final.h5ad`
   - `paired_sample_list.csv`
   - optionally `GSE282122_series_matrix.txt.gz` for external metadata verification

2. Load `myeloid_final.h5ad` in backed or sparse mode. Do not load the 12.7 GB pooled atlas. Do not use GEO per-sample matrices unless reprocessing becomes necessary.

3. Join `paired_sample_list.csv` to `adata.obs` by `sample_id`.

4. Filter:
   - `Disease in {CD, UC}`
   - `Treatment in {Pre, Post}`
   - `Remission_status in {Remission, Non_Remission}`
   - samples present in `paired_sample_list.csv`
   - primary cell strata: `major in {Mono_macro, DC}`
   - secondary states: `C1Qhi IL1Blo macro`, `C1Qhi IL1Bhi macro`, `S100A8 A9hi mono`, `S100A8 A9hi TNFhi IL6pos mono`, `CD1Chi DC`
   - exclude `Mast` from APC primary analysis

5. Build pseudobulk raw counts by:
   - primary key: `Patient + Disease + Site + Treatment + Remission_status + major`
   - secondary key: same plus `final_analysis`
   - sum sparse raw counts per stratum
   - retain strata with at least 20 cells per side for broad-state module-score analysis; require at least 50 cells per side for gene-level differential expression if feasible

6. Derive site-matched pre/post deltas:
   - match by `Patient + Disease + Site + cell_state`
   - compute module scores on logCPM pseudobulk counts
   - delta = `Post - Pre`

7. Primary tests:
   - Paired within-outcome effect: one-sample test of `delta` against zero per module and major state.
   - Response interaction: `delta ~ Remission_status + Disease + Site + baseline_Inflammation_score + baseline_module_score + Batch`, clustered or mixed by patient where multiple sites per patient are retained.
   - Robust fallback: patient-level collapse across sites before modeling, to avoid pseudoreplication.

8. Specific V3 gate:
   - target modules: `lipid_loader_repair`, `lysosomal_apc`, `complement_phagocytosis`
   - generic-inflammatory controls: `tnf_autocrine_nfkb` and, if available from V3 scripts, `inflammatory_nfkb` / `ifn_apc`
   - require module-specific response effect not reducible to generic inflammation: absolute target effect at least 2x generic-inflammatory effect or significant after covarying generic score.

9. Positive signal definition:
   - same direction in `Mono_macro` and `DC`, or one broad state plus matching fine-state secondary support
   - observed in both CD and UC or clearly disease-specific with adequate cell counts
   - BH FDR <= 0.10 for primary module tests, with effect size stability across leave-one-patient-out sensitivity
   - no reversal after adjusting for baseline inflammation score and site

10. Negative/demotion definition:
   - effects disappear after baseline inflammation and generic TNF/NF-kB adjustment
   - signal exists only in rare underpowered fine states
   - site-level duplicates drive significance and patient-collapsed analysis fails
   - remission/non-remission contrast is explained by baseline inflammation score or cell counts

## Compute, Disk, and Memory Risks

Minimal route:

- Download: ~417 MB for `myeloid_final.h5ad` plus small metadata files.
- Disk: <1 GB for minimal inputs; <2 GB including outputs.
- Memory:
  - backed inspection works comfortably.
  - sparse raw count pseudobulk should fit in ~1-3 GB RAM.
  - avoid dense conversion of `X`. Dense float32 for `30,858 x 33,075` would be ~4.1 GB before pandas/anndata overhead; float64 would be ~8.2 GB.

Avoid:

- `TAURUS_raw_counts_annotated_final.h5ad` at 12.7 GB unless the myeloid object proves insufficient.
- GEO filtered archive at 3.0 GB and raw archive at 9.0 GB for this session. They require decompression/streaming and lack cell-state labels.
- PC file at 1.19 GB unless embedding-level analysis is required.
- Full atlas reintegration. It is unnecessary for the pseudobulk perturbation question and would add failure risk without improving the core test.

Statistical risks:

- Fine-state analysis is underpowered for rare states.
- Multiple biopsies/sites per patient can cause pseudoreplication; use patient collapse or mixed models.
- Remission status is an outcome label, not a randomized condition. Response-specific deltas are pharmacodynamic associations, not causal target evidence.
- Anti-TNF directly affects generic inflammatory programs; module effects must be adjusted against TNF/NF-kB/IFN controls.
- Baseline inflammation and biopsy site are strong confounders; both must be included.

## Go / No-Go Decision

**GO** for a V3 analysis that uses `myeloid_final.h5ad` and `paired_sample_list.csv` to run patient/site-level pseudobulk module tests in `Mono_macro` and `DC` states.

**NO-GO** for a GEO-only route, because GEO supplementary tar files expose per-sample 10x matrices and would require reannotation/reintegration.

**NO-GO as primary endpoint** for rare fine states (`LAMP3pos DC`, `pDC`, `XCR1pos DC`, `Cycling MNP`) because matched pre/post support is too sparse.

Recommended next local script: `v3_wave66_gse282122_myeloid_pseudobulk.py`, with minimal input downloads from Zenodo, sparse pseudobulk aggregation, module-score deltas, remission-interaction tests, and patient-collapsed sensitivity analysis.
