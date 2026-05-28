# D04 Longitudinal Pre-Disease Cohorts

Status: scoping in V5  
Last updated: 2026-05-28

## Why This Dimension Matters

Cross-sectional autoimmune tissue signals cannot distinguish cause from
consequence. Pre-diagnostic or pre-seroconversion cohorts can establish temporal
precedence and are therefore higher value than another tissue atlas.

## V5 First Scan

Searches initiated:
- `pre-diagnostic multiple sclerosis serum transcriptomics public dataset GEO PROXIMUS`
- `preclinical multiple sclerosis serum proteomics public dataset Bjornevik EBV military serum GEO`
- `TEDDY study public transcriptomics autoantibody seroconversion data GEO type 1 diabetes`
- `TEDDY study RNA sequencing GEO autoantibody seroconversion type 1 diabetes accession`
- `TEDDY study longitudinal gene expression autoantibody seroconversion dataset`
- `The Environmental Determinants of Diabetes in the Young transcriptomics dataset GEO`

## Current Access Assessment

### Multiple Sclerosis

Known direction:
- Pre-diagnostic serum repositories were central to the EBV/MS temporal-risk
  literature and related serum biomarker work.

Current blocker:
- No immediately verified public GEO/ArrayExpress-style pre-MS PBMC or serum
  transcriptomic dataset has been identified in V5 so far.
- The likely high-value data live in military/biobank repositories with
  controlled access or publication-level summary statistics, not open sample-
  level matrices.

V5 implication:
- Do not claim temporal precedence for MS candidate mechanisms unless a public
  or controlled-access dataset is actually obtained.
- For now, MS temporal claims must be framed as literature-supported or
  inaccessible, not analyzed.

### Type 1 Diabetes / TEDDY

Known direction:
- TEDDY followed genetically at-risk children longitudinally before islet
  autoantibody seroconversion and clinical T1D.

Current status:
- TEDDY is the strongest practical starting point for a pre-autoimmune
  longitudinal omics dimension because public and controlled-access data routes
  exist for transcriptomic, microbiome, autoantibody, and clinical trajectories.
- Verified source anchors:
  - NIDDK Central Repository has a TEDDY study page:
    <https://repository.niddk.nih.gov/studies/teddy/DSIC/>.
  - TEDDY metagenomic sequencing data are reported as dbGaP
    `phs001442.v3.p2` in a public study of islet autoantibody seroconversion
    and infant gut microbiomes.
  - A 2025 TEDDY peripheral-blood gene-expression paper reports longitudinal
    expression profiling in autoantibody-positive children and stratification
    of progression rate to T1D, with MHC-II and immune-response pathway
    enrichment after seroconversion.
  - A TEDDY plasma metabolome/vitamin/fatty-acid nested case-control study
    followed samples until islet-autoantibody seroconversion.

V5 implication:
- TEDDY can test whether lipid-lysosomal/IFN/APC-like programs precede
  autoimmune seroconversion in a non-MS disease.
- A positive TEDDY signal would not prove MS causality, but it would support a
  pan-autoimmune temporal axis.

## Candidate Relevance

Current highest-priority uses:
- Pregnancy axis: distinguish transient hematologic shifts from true
  pre-flare/peripheral priming.
- Lipid-lysosomal myeloid module: test whether module components precede
  autoimmune conversion or only appear after tissue inflammation.
- Recalibrated demotions: candidates with only cross-sectional support should
  not advance without D04 or another causal-direction dimension.

## Next Concrete Steps

1. Identify exact TEDDY accessions and accessible matrices suitable for
   seroconversion-aligned module scoring.
2. Search for pre-IBD nested cohort public omics.
3. Search for MS longitudinal established-disease cohorts with public
   biomarker matrices if true pre-MS omics remain inaccessible.
4. Record every accession in `data/manifest.tsv` only after actual download or
   verified access URL.
