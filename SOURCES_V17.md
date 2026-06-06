# SOURCES_V17

Date: 2026-06-06

This file summarizes source endpoints used in the V17 GPR25/KIF21B mechanism
workup. Cached responses are under `analysis/v17_gpr25_mechanism/raw_api/`.

## Genetics / QTL

- OpenGWAS API v4, read through `scripts/check_opengwas_access.py` and prior
  V13-V16 scripts. Token loaded from gitignored `.env`; POST-only discipline.
- eQTLGen full cis-eQTL file:
  `https://download.gcc.rug.nl/downloads/eqtlgen/cis-eqtl/cis-eQTLs_full_20180905.txt.gz`.
  Access downgrade: `curl -k` required because the host presents an expired TLS
  certificate. Extracted rows are in
  `analysis/v17_gpr25_mechanism/eqtlgen_full_extract/chr1_candidate_gene_full_rows.tsv`.
- GTEx API:
  `https://gtexportal.org/api/v2/openapi.json` returned HTTP 200. Historical
  Google Cloud full archive paths tested in V17 returned HTTP 404.

## Protein / Target / Structure

- UniProt REST:
  - `GPR25` / UniProt `O00155`.
  - `KIF21B` / UniProt `O75037`.
- IUPHAR/GtoPdb target search:
  - GPR25 target ID `95`, type `GPCR`.
- AlphaFold DB API:
  - GPR25 `AF-O00155-F1`, version 6, global metric value `82.44`.
  - KIF21B `AF-O75037-F1`, version 6, global metric value `69.62`.
- ChEMBL API:
  - GPR25 target `CHEMBL4523858`; 2 activity records, 0 mechanism records.
  - KIF21B: no ChEMBL target and 0 mechanism records found.
- ClinicalTrials.gov API:
  - `GPR25`: 0 studies.
  - `KIF21B`: 0 studies.

## Literature / Prior Art

- Europe PMC:
  - `GPR25 AND CXCL17`: hit count `27`.
  - `GPR25 AND autoimmune`: hit count `51`.
  - `GPR25 AND (CITE-seq OR proteomics OR flow cytometry OR surface protein)`:
    hit count `175`.
  - `GPR25 AND (migration OR chemotaxis OR RhoA OR integrin)`: hit count `89`.
  - `KIF21B AND "multiple sclerosis"`: hit count `105`.
  - `KIF21B AND (ulcerative colitis OR Crohn OR inflammatory bowel disease)`:
    hit count `92`.
  - `KIF21B AND autoimmune`: hit count `125`.
- Notable GPR25 literature identified:
  - PMID `39293486`, DOI `10.1038/s41586-024-08043-2`.
  - PMID `41270189`, DOI `10.1126/sciimmunol.adu2089`.
  - PMID `42207165`, DOI `10.1111/bcpt.70255`.
- Notable KIF21B prior-art literature:
  - Human Molecular Genetics 2010, DOI `10.1093/hmg/ddp542`.
  - Journal of Medical Genetics 2010, DOI `10.1136/jmg.2009.075911`.

## Dataset Availability Searches

NCBI GEO Entrez searches returned no obvious public MS protein/CITE-seq dataset:

- `GPR25 CITE-seq multiple sclerosis`: count `0`.
- `GPR25 protein multiple sclerosis`: count `0`.
- `CXCL17 GPR25 multiple sclerosis`: count `0`.
- `KIF21B CITE-seq multiple sclerosis`: count `0`.
- `KIF21B T cell multiple sclerosis`: count `0`.

## Patent Search

- Google Patents exact `GPR25`: 1136 results; top inspected hits were broad
  target-list/platform or unrelated biomarker records, not a specific MS/UC
  GPR25 agonist program.
- Google Patents exact `KIF21B`: 492 results; top inspected hits were broad
  biomarker/platform or unrelated disease-context records, not a KIF21B
  autoimmune intervention program.
