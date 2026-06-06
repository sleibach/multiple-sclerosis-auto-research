# GPR25

Status: alive Tier 1 lead  
Last updated: 2026-06-06  
Primary evidence file: `../../GENETICS_GPR25_WORKUP_V17.md`

## Current Verdict

`GPR25` remains alive as a genetics-to-lymphocyte-trafficking lead at the
MS-UC chr1 shared locus, but it is not intervention-grade.

## Evidence

- V16 allele-aligned GTEx/eQTLGen evidence: expression-increasing alleles are
  protective for both MS and UC.
- V17 full eQTLGen candidate-gene extraction: `GPR25` is strongest in the
  disease-shared credible-set block.
- V17 bounded disease-vs-eQTL SuSiE-coloc:
  - MS/eQTL max PP.H4 `0.969296`;
  - UC/eQTL max PP.H4 `0.981623`.
- UniProt/IUPHAR support a CXCL17-GPR25 receptor axis with lymphocyte homing
  biology.

## Limits

- `KIF21B` also retains bounded eQTL-coloc support at the same locus.
- `GPR25` is absent from local MS CNS single-nucleus feature sets
  `GSE301908_sn_all.rds` and `GSE180759_expression_matrix.csv.gz`.
- Direct h5ad scans across local gut, RA blood, Sjogren salivary, psoriasis
  skin, and IBD myeloid atlases found `GPR25` absent or nearly absent
  (`0%` to `0.0159%` detected), so scRNA expression support is weak.
- Cell-type breakdown did not rescue this: highest observed GPR25 detection was
  Sjogren salivary pro-T cells at `0.9009%` in a small group (`n=111`).
- ChEMBL has only screening activity records and no mechanism records.
- No ClinicalTrials.gov GPR25 studies were found.

## Next Required Test

Resolve `GPR25` versus `KIF21B` in immune-cell or CSF protein/CITE-seq data
where GPR25 surface protein can be measured, then test whether the protective
genotype raises GPR25 expression and alters CXCL17-directed migration/RhoA/
integrin readouts.
