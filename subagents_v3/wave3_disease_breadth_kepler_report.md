# Wave 3 Disease-Breadth Expansion Report - Kepler

Returned: 2026-05-26 21:13 UTC

Read the requested V3 files/reports and did not edit anything. This is routing
intelligence only, not evidence or a finding.

## Best Next Downloads

1. **RA synovium/macrophage, `E-MTAB-8322`**

Source: [EBI Single Cell Expression Atlas](https://www.ebi.ac.uk/gxa/sc/experiments/E-MTAB-8322)

Direct h5ad:
<https://ftp.ebi.ac.uk/pub/databases/microarray/data/atlas/sc_experiments/E-MTAB-8322/E-MTAB-8322.project.h5ad>

Size: `1,599,080,973` bytes, about 1.5 GB.

Metadata: strong for this run. `cell_metadata.tsv` has `disease`,
`response_to_treatment`, `individual`, `cell_type`; includes normal,
undifferentiated peripheral arthritis, RA treatment-naive, resistant, and
remission macrophages.

Feasibility: best immediate new tissue. Direct h5ad, public, donor/response
labels available. If bandwidth matters, EBI also exposes compressed
MTX/counts plus metadata, roughly 340-390 MB for core count files.

2. **T1D islet, HPAP / `GSE148073`, CZI collection `51544e44-293b-4c2b-8c26-560678423380`**

Source: [CELLxGENE collection](https://cellxgene.cziscience.com/collections/51544e44-293b-4c2b-8c26-560678423380) /
[GSE148073](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE148073)

Direct h5ad:
<https://datasets.cellxgene.cziscience.com/111d6e7d-d3d2-48fd-907a-4d3f8c77ee93.h5ad>

Size: `853,163,206` bytes.

Metadata: high CZI-standard metadata; 69,645 cells, 25,629 features, 24 donor
IDs, normal and T1D labels, islet/endocrine/exocrine/stromal/endothelial cell
types.

Feasibility: very good direct h5ad fit for the existing local h5ad workflow.
Caveat: likely best for endocrine/ductal antigen-presentation state, not myeloid
recurrence.

## Other Tractable Candidates

- **Autoimmune thyroid spatial, `GSE248205` / `PRJNA1042806`**
  - Source: [GEO GSE248205](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE248205)
  - Download:
    <https://ftp.ncbi.nlm.nih.gov/geo/series/GSE248nnn/GSE248205/suppl/GSE248205_Processed_data.tar.gz>
  - Size: 159.2 MB.
  - Metadata: 8 Visium samples: controls, Hashimoto thyroiditis, Graves
    disease. Strong relevance to epithelial `CD74/MIF` spatial biology, but
    spot-level not single-cell. Good backup if T1D immune sparsity is a problem.

- **Celiac duodenum scRNA-seq, `GSE277276` / `PRJNA1161628`**
  - Source: [GEO GSE277276](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE277276)
  - Downloads: `GSE277276_RAW.tar` 1.6 GB and `GSE277276_all_meta.csv.gz`
    14.5 MB from the GEO supplemental directory.
  - Metadata: strong; 203,555 cells across 21 active celiac and 11 control
    duodenal samples.
  - Feasibility: public and tractable, but MTX/TSV import required and gut
    partially overlaps the already analyzed IBD tissue lane.

- **PBC liver/PBMC scRNA-seq, `HRA008003` / `PRJCA027647`**
  - Source: [GSA-Human HRA008003](https://ngdc.cncb.ac.cn/gsa-human/browse/HRA008003),
    paper: [Nature Communications 2024](https://www.nature.com/articles/s41467-024-53104-9)
  - Download: <https://download.cncb.ac.cn/gsa-human/HRA008003>
  - Metadata: biologically strong; paper reports 51,943 liver cells and 47,644
    PBMCs from PBC/control comparisons.
  - Feasibility: open access, but not fastest. No direct h5ad/file sizes
    surfaced in quick checks; NGDC recommends FTP/Aspera.

- **Lupus nephritis kidney, `SCP3488` AMP2 Lupus Kidney**
  - Source: [Single Cell Portal SCP3488](https://singlecell.broadinstitute.org/single_cell/study/SCP3488/amp2-lupus-kidney-single-cell)
  - Size: portal reports 58,555 cells and 36,601 genes; direct file size not
    obtained.
  - Feasibility: scientifically attractive kidney tissue, but download friction
    is higher than RA/T1D. Do not make it one of the next two unless portal
    download is already scripted or credentials/session handling are available.

Recommended order: download `E-MTAB-8322.project.h5ad` first, then the HPAP T1D
h5ad. Keep thyroid spatial as the small backup route if the run needs a third
new tissue quickly.
