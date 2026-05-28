# Cross-Autoimmune Cell-State Replication Inputs: Zeno

Returned: 2026-05-26 19:44 UTC

## Axis To Quantify

Markers:

`CD74`, `CD44`, `CXCR4`, `HLA-DRA`, `HLA-DRB1`, `HLA-DPA1`, `HLA-DPB1`,
`STAT1`, `IRF1`, `IFI30`, `CTSS`, `LAMP3`, `CXCL10`.

Primary statistic should be donor-level, compartment-restricted pseudobulk or
cell-state fraction, not whole-tissue score.

## Recommended Datasets

### RA Synovium

- E-MTAB-8322, Single Cell Expression Atlas:
  `https://www.ebi.ac.uk/gxa/sc/experiments/E-MTAB-8322`
- Direct h5ad:
  `https://ftp.ebi.ac.uk/pub/databases/microarray/data/atlas/sc_experiments/E-MTAB-8322/E-MTAB-8322.project.h5ad`
- 70,246 cells; active RA, remission RA, controls/UA.
- Test macrophage clusters for `CD74/HLA-II/IFI30/CTSS/STAT1/IRF1` high state.

### IBD Gut

- CZI collection: Human IBD and healthy control 10x
  `https://cellxgene.cziscience.com/collections/7c7bd6c2-925b-4034-baab-620ef1b760e1`
- Direct h5ad:
  `https://datasets.cellxgene.cziscience.com/b1a62801-f509-45f8-b55f-533fbb7e7800.h5ad`
- Checked locally by subagent: 46,700 x 32,354; all target markers present.
- Myeloid counts: normal 677, Crohn 1,933, UC 1,161.
- Epithelial counts: normal 6,713, Crohn 4,701, UC 933.

### IBD Validation

- Crohn immune dysregulation collection:
  `https://cellxgene.cziscience.com/collections/5c868b6f-62c5-4532-9d7f-a346ad4b50a7`
- Colon immune:
  `https://datasets.cellxgene.cziscience.com/18abba9c-0c5c-48b8-b7e0-2d1738c75e2a.h5ad`
- Terminal ileum immune:
  `https://datasets.cellxgene.cziscience.com/6cfb8c33-9cfb-4e16-b868-18aff944e55a.h5ad`

### Psoriasis Skin

- CZI collection:
  `https://cellxgene.cziscience.com/collections/b1fd6a09-eb76-44ca-822d-68318548094c`
- Direct h5ad:
  `https://datasets.cellxgene.cziscience.com/5b293ff5-baa6-465e-b03b-043d9b892850.h5ad`
- Checked locally by subagent: 24,126 x 28,082.
- APC counts: dendritic cells normal 238 / psoriasis 237; monocyte psoriasis
  187; macrophage normal 238.
- Present: `CD74`, `CD44`, `CXCR4`, `STAT1`, `IRF1`, `IFI30`, `CTSS`, `LAMP3`,
  `CXCL10`.
- Caveat: canonical HLA-II marker incompleteness in this h5ad; use psoriasis
  for `CD74/IFN/IFI30/CTSS`, not as sole HLA-II replication.

### Sjogren Salivary Gland

- CZI collection:
  `https://cellxgene.cziscience.com/collections/21bbfaec-6958-46bc-b1cd-1535752f6304`
- scRNA h5ad:
  `https://datasets.cellxgene.cziscience.com/31380664-ba9c-49d1-9961-b2bf4f7131a2.h5ad`
- 94,227 cells; Sjogren and normal; 439 MB.
- Spatial samples are 25-75 MB each.

### T1D Islet Backup

- CZI collection:
  `https://cellxgene.cziscience.com/collections/51544e44-293b-4c2b-8c26-560678423380`
- h5ad:
  `https://datasets.cellxgene.cziscience.com/111d6e7d-d3d2-48fd-907a-4d3f8c77ee93.h5ad`
- 69,645 cells; 853 MB.

## Subagent Recommendation

Run RA E-MTAB-8322 macrophage analysis, IBD CZI, psoriasis CZI, and Sjogren
scRNA/spatial. Treat psoriasis HLA-II as incomplete unless validated in another
skin dataset.
