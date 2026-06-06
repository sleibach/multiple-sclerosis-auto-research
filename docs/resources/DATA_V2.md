# Data Inventory V2

**Created:** 2026-05-26T17:47:25Z

## Already Local MS Data

| Source | Local status | V2 role |
|---|---|---|
| `GSE279972` + Zenodo `10.5281/zenodo.19352263` | Raw/processed files downloaded; manifest with hashes. | Lesion proteomics/lipidomics/ABPP and metadata; re-check ACSL1 and pathway specificity. |
| `GSE301908` | `data/raw/GSE301908_sn_all.rds` present. | Independent microglial MIMS2-like validation; test ACSL1 neighbors and in-silico state perturbation. |
| `GSE284005` | Raw MERFISH archives present. | Spatial compartment check for ACSL1 and pathway genes. |
| `GSE180759` | Expression/annotation local. | Older chronic-active lesion snRNA cross-check if target genes are expressed in immune/myeloid blocks. |

## Candidate Cross-Autoimmune Data

The broaden track will prioritize datasets that can be accessed without controlled-access barriers:

| Disease | Candidate public data type | Intended signal |
|---|---|---|
| Rheumatoid arthritis | Synovial scRNA-seq or bulk synovium GEO datasets; OpenTargets genetics. | ACSL1-high inflammatory macrophage/fibroblast-adjacent state. |
| IBD / Crohn's / ulcerative colitis | Inflamed colon scRNA/bulk expression; OpenTargets genetics. | Lamina-propria inflammatory macrophages with lipid-droplet/metabolic activation. |
| Psoriasis | Lesional skin scRNA/bulk expression. | Myeloid/keratinocyte inflammatory lipid module and therapeutic reversibility. |
| SLE / lupus nephritis | PBMC/kidney scRNA or bulk datasets. | Monocyte/macrophage lipid-inflammatory module; type-I-IFN confounding. |
| Type 1 diabetes | Pancreas/islet scRNA or bulk; genetics. | Infiltrating myeloid lipid stress if accessible, otherwise negative evidence. |
| Sjogren's syndrome | Salivary gland scRNA/bulk. | Tissue macrophage lipid/inflammatory program. |

## Data Acceptance Rules

- A dataset contributes quantitative evidence only if accession/source, sample counts, and code trace are recorded.
- Literature-only evidence can support plausibility or novelty but cannot substitute for the cross-autoimmune evidence requirement.
- If a dataset is inaccessible, too large, or missing processed expression, log it in `BLOCKERS_V2.md` or `LAB_NOTEBOOK_V2.md` and pivot.
