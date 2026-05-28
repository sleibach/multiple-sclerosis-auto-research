# Wave 13 Disease-Atlas Expansion Scout

Timestamp: 2026-05-27 02:23 Europe/Berlin

Scope: identify tractable public single-cell or spatial datasets that can add
independent disease breadth for the lipid-lysosomal / inflammatory myeloid /
APC module. This report makes no therapeutic claim.

## Workspace Context Read

Read locally:

- `ORCHESTRATION_LOG_V3.md` tail: current candidates (`APOC1`, `SNX10`,
  `C15ORF48`, broad residual candidates) were demoted; next route is independent
  disease breadth, especially RA/SLE or other missing autoimmune tissue.
- `DATA_V3.md`: already used direct h5ad datasets for IBD, psoriasis,
  Sjogren, T1D, and RA blood; thyroid spatial `GSE248205` already analyzed.
- `BLOCKERS_V3.md`: Census expression extraction stalled; RA
  `E-MTAB-8322.project.h5ad` transfer from EBI timed out; large SLE h5ad and
  State feature mapping remain blocked.
- `scripts/v3_analyze_direct_h5ad_cell_states.py`: current direct-h5ad
  analyzer expects a single h5ad with `obs` fields `disease`, `donor_id`,
  `cell_type`, `tissue`, and a gene symbol column such as `feature_name`.

Implication: the best expansion candidates are not more candidate genes, but
new disease/control atlases that can be converted to the current h5ad schema
or analyzed with a small import wrapper.

## Highest-Priority Tractable Additions

### 1. Celiac disease duodenal biopsies, `GSE315138`

- Accession: `GSE315138`
- GEO page: `https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE315138`
- Direct archive:
  `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE315nnn/GSE315138/suppl/GSE315138_RAW.tar`
- Header-verified size: `383,221,760` bytes, 365.5 MiB.
- GEO page summary: active celiac disease duodenal biopsies vs healthy control
  biopsies; 4 active CeD and 2 healthy controls; droplet 10x Chromium.
- Labels expected:
  - cases: sample titles beginning `celiac*` / active CeD.
  - controls: `Healthy1`, `Healthy2`.
- Tissue/cell types expected:
  - duodenal mucosa, all major mucosal cells.
  - high-value compartments for this module: macrophage/DC/APC, epithelial,
    stromal/endothelial.
- Expected analysis config after conversion to h5ad:

```python
DirectConfig(
    name="celiac_duodenum_apc",
    path=RAW / "celiac_gse315138.h5ad",
    disease_label="celiac disease",
    control_label="normal",
    compartment="duodenal APC/myeloid",
    cell_types=("macrophage", "dendritic cell", "monocyte"),
    gene_symbol_column="feature_name",
)
DirectConfig(
    name="celiac_duodenum_epithelial",
    path=RAW / "celiac_gse315138.h5ad",
    disease_label="celiac disease",
    control_label="normal",
    compartment="duodenal epithelial",
    cell_types=("enterocyte", "intestinal epithelial cell", "goblet cell"),
    gene_symbol_column="feature_name",
)
```

- Why it helps: adds a new autoimmune gut disease that is not IBD and directly
  samples target tissue. Strong fit for IFN/HLA-II/APC and epithelial stress
  recurrence checks.
- Blockers:
  - GEO supplement is Matrix Market / TSV, not h5ad; requires conversion and
    metadata harmonization before the existing direct-h5ad script can run.
  - Sample count is small, so use donor-level effect sizes only, not a decisive
    population estimate.

### 2. Myasthenia gravis PBMC, `GSE227835`

- Accession: `GSE227835`
- GEO page: `https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE227835`
- Direct archive:
  `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE227nnn/GSE227835/suppl/GSE227835_RAW.tar`
- Header-verified size: `887,582,720` bytes, 846.5 MiB.
- GEO labels:
  - `AChR-positive MG_1` through `AChR-positive MG_10`.
  - `Healthy control_1` through `Healthy control_10`.
  - `Seronegative MG pre-treatment_1..10` and matched
    `Seronegative MG post-treatment_1..10`.
- Tissue/cell types expected:
  - PBMC.
  - published reanalysis describes CD14 monocytes, CD16 monocytes, cDC, pDC,
    B cells, T/NK subsets, neutrophils, megakaryocytes.
- Expected analysis configs after conversion:

```python
DirectConfig(
    name="mg_pbmc_myeloid",
    path=RAW / "mg_gse227835.h5ad",
    disease_label="myasthenia gravis",
    control_label="normal",
    compartment="PBMC myeloid/APC",
    cell_types=("CD14 monocyte", "CD16 monocyte", "conventional dendritic cell", "plasmacytoid dendritic cell"),
    gene_symbol_column="feature_name",
)
DirectConfig(
    name="mg_pbmc_b_cell",
    path=RAW / "mg_gse227835.h5ad",
    disease_label="myasthenia gravis",
    control_label="normal",
    compartment="PBMC B/plasmablast",
    cell_types=("B cell", "memory B cell", "plasmablast"),
    gene_symbol_column="feature_name",
)
```

- Why it helps: adds a neuromuscular autoantibody disease with healthy controls
  and enough donors for donor-level testing. It is not tissue-resident myeloid
  biology, but it is useful breadth for systemic APC/IFN/HLA-II recurrence.
- Blockers:
  - GEO archive is TXT/matrix-like processed data, not h5ad.
  - PBMC signal may reflect circulating immune state rather than lesion tissue.
  - Treatment labels must be handled carefully: baseline AChR-positive and
    seronegative pre-treatment should not be pooled silently with post-treatment
    samples.

### 3. IgG4-related fibrotic lesions, `GSE231920`

- Accession: `GSE231920`
- GEO page: `https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE231920`
- Direct archive:
  `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE231nnn/GSE231920/suppl/GSE231920_RAW.tar`
- Header-verified size: `429,987,840` bytes, 410.1 MiB.
- GEO design: 3 IgG4-related disease tissues and 3 control tissues.
- Tissue/cell types expected:
  - retroperitoneal fibrotic lesions; immune and stromal compartments.
  - high-value compartments: macrophage/DC/APC, fibroblast/stromal, plasma/B
    cells.
- Expected configs after conversion:

```python
DirectConfig(
    name="igg4_rd_lesion_apc",
    path=RAW / "igg4rd_gse231920.h5ad",
    disease_label="IgG4-related disease",
    control_label="normal",
    compartment="retroperitoneal fibrotic lesion APC/myeloid",
    cell_types=("macrophage", "dendritic cell", "monocyte"),
    gene_symbol_column="feature_name",
)
DirectConfig(
    name="igg4_rd_lesion_stromal",
    path=RAW / "igg4rd_gse231920.h5ad",
    disease_label="IgG4-related disease",
    control_label="normal",
    compartment="retroperitoneal fibrotic lesion stromal",
    cell_types=("fibroblast", "stromal cell", "endothelial cell"),
    gene_symbol_column="feature_name",
)
```

- Why it helps: not autoimmune pancreatitis per se, but IgG4-RD is the systemic
  disease family containing type 1 autoimmune pancreatitis. This is a tractable
  tissue-level route into fibroinflammatory IgG4 biology.
- Blockers:
  - Only 3 case and 3 control tissues; useful for recurrence, not effect-size
    certainty.
  - Lesion site is retroperitoneal fibrosis, so pancreas-specific interpretation
    is not allowed.

### 4. Ankylosing spondylitis PBMC TNFi response, `GSE277791`

- Accession: `GSE277791`
- GEO page: `https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE277791`
- Direct archive:
  `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE277nnn/GSE277791/suppl/GSE277791_RAW.tar`
- Header-verified size: `174,387,200` bytes, 166.3 MiB.
- GEO labels:
  - `PBMC, NR, TNFi, Pre, KAS26_KAS27_KAS28`
  - `PBMC, NR, TNFi, Post, KAS26_KAS27_KAS28`
  - `PBMC, NR, TNFi, Pre, KAS29_KAS30_KAS31`
  - `PBMC, NR, TNFi, Post, KAS29_KAS30_KAS31`
- Tissue/cell types expected:
  - PBMC; original sample page lists 10x Genomics filtered feature-barcode H5.
- Expected analysis route:
  - Not a disease/control analysis because no healthy control appears in GEO.
  - Use only as within-AS pre/post TNFi response or non-responder baseline
    descriptive evidence.
  - If converted, configure as a paired-treatment module-score analysis rather
    than direct `DirectConfig`.
- Why it helps: adds spondyloarthritis breadth and a perturbation-like clinical
  axis, but only for treatment-response context.
- Blockers:
  - No healthy controls in the visible series design.
  - Only four pooled sample files; donor-level metadata may be pooled into
    `KAS26_KAS27_KAS28` style groups, limiting donor-aware inference.
  - Should not be counted as disease/control replication of the module.

## Useful But Large Or Currently Blocked

### SLE PBMC, CZI/CELLxGENE `218acb0f-9f2f-4f76-b90b-15a4b7c7f629`

- Collection:
  `https://cellxgene.cziscience.com/collections/436154da-bcf1-4130-9c8b-120ff9a888f2`
- Discover API endpoint:
  `https://api.cellxgene.cziscience.com/curation/v1/datasets/218acb0f-9f2f-4f76-b90b-15a4b7c7f629/versions`
- Direct h5ad:
  `https://datasets.cellxgene.cziscience.com/4118e166-34f5-4c1f-9eed-c64b90a3dace.h5ad`
- API-reported size: `12,218,251,667` bytes, about 11.4 GiB.
- API-reported cells: 1,263,676.
- Labels: `normal`, `systemic lupus erythematosus`.
- Cell types include classical monocyte, non-classical monocyte,
  conventional dendritic cell, plasmacytoid dendritic cell, B cell,
  plasmablast, T/NK.
- Expected config if downsampled/obtained:

```python
DirectConfig(
    name="sle_blood_myeloid",
    path=RAW / "sle_pbmc_cellxgene.h5ad",
    disease_label="systemic lupus erythematosus",
    control_label="normal",
    compartment="blood myeloid/APC",
    cell_types=("classical monocyte", "non-classical monocyte", "conventional dendritic cell", "plasmacytoid dendritic cell"),
    gene_symbol_column="feature_name",
)
```

- Blocker: direct h5ad is well above the requested ~2 GB ceiling. A targeted
  Census extraction would be ideal, but this workspace previously stalled on
  Census expression materialization. Keep as a high-value route only if a small
  derived subset can be exported.

### Cutaneous lupus, `GSE179633`

- Accession: `GSE179633`
- GEO page: `https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE179633`
- Direct archive:
  `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE179nnn/GSE179633/suppl/GSE179633_RAW.tar`
- GEO page size: 2.3 GB.
- Design: 23 skin biopsies; 5 healthy controls, 8 DLE, 10 SLE; epidermis and
  dermis separated; processed data only, raw reads withheld for privacy.
- Useful compartments: dermal macrophage/DC, keratinocyte, fibroblast.
- Blockers:
  - Slightly above the preferred ~2 GB ceiling.
  - GEO notes raw data are not provided; processed supplement is Matrix Market /
    TSV/TAR.
  - Strong skin IFN biology likely, but this would duplicate IFN/APC signal more
    than directly test lipid-lysosomal myeloid specificity.

### RA synovium, `E-MTAB-8322`

- Accession: `E-MTAB-8322`
- ArrayExpress/BioStudies page:
  `https://www.ebi.ac.uk/biostudies/arrayexpress/studies/E-MTAB-8322`
- Previously selected direct h5ad route:
  `https://ftp.ebi.ac.uk/pub/databases/microarray/data/atlas/sc_experiments/E-MTAB-8322/E-MTAB-8322.project.h5ad`
- Disease/control labels from prior scout: RA synovial pathotypes and controls
  / non-RA comparators, with macrophage/myeloid relevance.
- Blocker: repeated HTTPS and directory-list transfers to `ftp.ebi.ac.uk`
  timed out in this workspace. Keep as high-value retry, but do not spend the
  next critical path on it unless EBI transfer stabilizes.

### RA synovial fibroblast / multiome / spatial, ImmPort `SDY2213`

- Study page: `https://immport.org/shared/study/SDY2213`
- Publication: `https://doi.org/10.1038/s41590-023-01527-9`
- Study description: RA synovial tissue scRNA/ATAC, multiplex imaging, and
  spatial transcriptomics; h5ad file for CELLxGENE viewer reported by the paper.
- Tissue/cell types: synovial fibroblasts, immune infiltrates, spatial
  microenvironments; very relevant to stromal/APC cross-talk.
- Blockers:
  - Exact h5ad URL was not exposed in the quick scout.
  - ImmPort access may require account/API workflow.
  - Strong for RA tissue biology, but not a drop-in direct URL yet.

### Primary biliary cholangitis, GSA-Human `HRA008003`

- Source publication:
  `https://www.nature.com/articles/s41467-024-53104-9`
- Accession from paper: GSA-Human `HRA008003`; mouse `CRA017680`.
- Data source URL family:
  `https://ngdc.cncb.ac.cn/gsa-human`
- Design from source: human PBC liver/PBMC single-cell data; reported
  liver-resident Th1-like T-cell expansion and control comparisons.
- Blockers:
  - GSA-Human access/download route and file sizes were not resolved in this
    scout.
  - Likely not a simple h5ad/10x direct download.
  - T-cell-centered biology; may be less direct for lipid-lysosomal myeloid/APC.

### PSC / autoimmune cholangitis comparator, `E-MTAB-10143`

- Accession: `E-MTAB-10143`
- BioStudies page:
  `https://www.ebi.ac.uk/biostudies/arrayexpress/studies/E-MTAB-10143`
- Disease context: PSC, healthy donors, liver/PBMC intrahepatic T cells.
- File route: ArrayExpress/BioStudies; direct h5ad not found in quick scout.
- Value: autoimmune cholangitis comparator for liver immune programs, but not
  PBC and mostly T-cell rather than myeloid/APC.
- Blockers:
  - Direct files and sizes not resolved.
  - Not a strong fit for current lipid-lysosomal myeloid module.

### Autoimmune pancreatitis / IgG4-RD, GSA routes

- Type 1 autoimmune pancreatitis source:
  - publication mentions pancreatic-cell AIP scRNA-seq accession `HRA007090`.
  - source article:
    `https://pmc.ncbi.nlm.nih.gov/articles/PMC13097352/`
- IgG4-RD PBMC source:
  - accession `HRA003750`.
  - source article:
    `https://pmc.ncbi.nlm.nih.gov/articles/PMC10544205/`
- Blockers:
  - GSA-Human access/download details and file sizes not resolved.
  - No direct h5ad/10x matrix URL identified.
  - These remain high-interest disease-specific routes but not immediate
    under-2-GB direct-download candidates.

### Hashimoto thyroiditis scRNA, GSA/CNGB routes

- Hashimoto tissue/PBMC scRNA paper:
  `https://pmc.ncbi.nlm.nih.gov/articles/PMC11811715/`
- Accessions from source: GSA-Human `HRA001684` and `HRA002138`.
- CNGB project surfaced in search:
  `https://db.cngb.org/data_resources/project/CNP0001494`
- Blockers:
  - No direct h5ad/10x matrix URL or file size resolved.
  - Current workspace already has `GSE248205` thyroid spatial recurrence, so
    this is useful only if a direct scRNA route is later resolved.

## Already In Workspace Or Already Counted

### RA blood CZI h5ad

- Dataset ID: `d18736c3-6292-4379-919a-d6d973204c87`
- Collection:
  `https://cellxgene.cziscience.com/collections/e1a9ca56-f2ee-435d-980a-4f49ab7a952b`
- Direct h5ad:
  `https://datasets.cellxgene.cziscience.com/dbed890d-a14a-4502-a413-b57a4650d3af.h5ad`
- API-reported size: `259,732,658` bytes, 247.7 MiB.
- Status: already downloaded locally as
  `data/raw_v3/cell_state/ra_binvignat_blood.h5ad`.
- Keep as current RA blood evidence; do not count as new expansion.

### Autoimmune thyroid spatial, `GSE248205`

- Accession: `GSE248205`
- GEO page: `https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE248205`
- Direct archive already used:
  `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE248nnn/GSE248205/suppl/GSE248205_Processed_data.tar.gz`
- Local size in `DATA_V3.md`: 159 MB.
- Labels: 2 controls, 3 Hashimoto thyroiditis, 3 Graves disease.
- Status: already analyzed as spatial tissue recurrence; not a new scout hit.

## Recommended Next Dispatch Order

1. `GSE315138` celiac duodenum: best immediate addition because it is target
   tissue, disease/control, under 400 MB, and mechanistically adjacent to IBD
   without being the same disease.
2. `GSE227835` myasthenia gravis PBMC: best systemic autoantibody breadth
   dataset under 1 GB with healthy controls and enough donors.
3. `GSE231920` IgG4-RD fibrotic tissue: best tractable proxy for
   autoimmune-pancreatitis / IgG4 fibroinflammatory biology.
4. `GSE277791` ankylosing spondylitis: use only as TNFi-response / baseline
   descriptive evidence, not disease/control replication.
5. SLE routes: either targeted Census export from the 11.4 GiB CZI h5ad or
   accept the 2.3 GB cutaneous lupus `GSE179633` archive if disk/network budget
   allows; neither is an immediate under-2-GB direct h5ad candidate.

## Report-Level Guardrails

- No listed dataset is evidence for a therapeutic target until processed with
  donor-aware, compartment-restricted tests and checked for batch/sample-label
  confounding.
- Matrix archives require explicit h5ad conversion, harmonized metadata, and
  cell-type annotation before being used with
  `scripts/v3_analyze_direct_h5ad_cell_states.py`.
- PBMC datasets add systemic breadth but do not substitute for diseased-tissue
  evidence when the mechanistic claim concerns local tissue myeloid/APC states.
