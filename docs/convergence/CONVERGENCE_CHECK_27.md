# Convergence Check 27

Timestamp: 2026-05-27 15:32 CEST.

## Current Question

Does an orthogonal biochemical modality sharpen the shared cross-autoimmune
lipid-lysosomal/APC module into a specific therapeutic-relevant axis?

## New Evidence

Wave66 metabolomics/lipidomics class audit:

- Downloaded usable individual-level Metabolomics Workbench feature data for 8
  studies: RA, Crohn/UC, UC severity, SLE lipid severity, ankylosing
  spondylitis, T1D, MS cellular lipid model, and psoriasis steroid biopsy.
- Produced 218 class-level contrast rows and 7,835 feature-provenance rows.
- No metabolite/lipid class passed the candidate biochemical-axis gate.
- Most relevant lipid hints:
  - `ceramide`: 6 diseases/model systems tested, 5 same direction, supportive
    in `MS_model`, `RA`, and `SLE`, median Hedges g 0.712.
  - `glycosphingolipid`: 5 tested, 4 same direction, supportive in `MS_model`,
    `RA`, and `UC`, median Hedges g 0.640.
  - `lysophosphatidylcholine`: 6 tested, 4 same direction, supportive in
    `MS_model` and `RA`.
- Non-lipid `amino_acid` depletion had broader support (`AS`, `Crohn`, `RA`,
  `UC`) but does not specifically resolve the lipid-lysosomal/APC mechanism.

Wave66 sidecars:

- Wave66-A confirmed Workbench access mechanics and marked TEDDY conditional
  until `cc` clinical codes are resolved.
- Wave66-B identified a feasible cell-resolved perturbation route for
  `GSE282122` through Zenodo `myeloid_final.h5ad` and `paired_sample_list.csv`.

## Agreement

- The broad lipid-lysosomal hypothesis remains plausible, especially around
  sphingolipid/ceramide handling, but current biochemical data do not nominate a
  single intervention point.
- Serum/plasma metabolomics does not establish tissue myeloid causality.
- The best next evidence channel is no longer bulk expression or serum class
  scoring; it is cell-resolved paired anti-TNF perturbation in annotated
  disease myeloid states.

## Disagreement

- The biochemical branch points weakly at sphingolipids, while prior gene-level
  branches have repeatedly failed to identify a druggable controller inside
  lysosomal/APC states.
- This could mean the relevant controller is not transcriptional, is
  context-specific, or is hidden by non-cell-autonomous tissue effects.

## Decision

Do not promote a metabolite class or target from Wave66.

Proceed to Wave67:

- Download Zenodo `myeloid_final.h5ad` and `paired_sample_list.csv`.
- Run patient/site-level pseudobulk module deltas in `Mono_macro` and `DC`.
- Require specificity beyond TNF/NF-kB and IFN/APC controls before reopening
  any intervention point.
