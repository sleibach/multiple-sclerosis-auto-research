# Decision 0019: Pregnancy / Hormonal Natural-Experiment Dimension Scout

Date: 2026-05-28

## Decision

Open the pregnancy-remission axis as the next V4 dimensional expansion target.

## Rationale

V4 requires at least one longitudinal or natural-experiment dimension for any
Tier 2+ candidate. V3 was dominated by cross-sectional transcriptomics. The
pregnancy/hormonal axis directly addresses this gap and is biologically relevant
to MS, RA, SLE, and other autoimmune diseases.

## Verified Starting Accessions

- `GSE235508`: RA, SLE, and healthy pregnancy; longitudinal blood bulk plus
  scRNA/cell-type-adjusted transcriptomics; public GEO.
- `GSE17410`: MS pregnancy PBMC expression array, before pregnancy vs ninth
  month; public GEO.
- `GSE17449`: MS pregnancy-related superseries; likely overlaps with
  `GSE17410`, independence must be checked.
- `GSE153459`: healthy pregnancy CD4 T-cell methylation across trimesters;
  reference only, not disease outcome.
- `GSE122894`: pregnant vs non-pregnant EAE TCR-beta repertoire; cross-species
  mechanistic support.

## Immediate Tier 0 Plan

Download or parse GEO metadata for `GSE235508` and `GSE17410`, then test whether
V4 candidate modules move toward remission-compatible direction during pregnancy
in RA/MS and whether SLE shows a contrasting pattern.

## Trace

- Sidecar: Zeno (`019e6e35-771a-7900-80b4-9f007184588e`)
