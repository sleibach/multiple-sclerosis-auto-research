# Current Status

Last updated: 2026-06-02 13:14 CEST

## Mission State

V10 is active. V8 produced the MS-centered multi-axis autoimmune mechanism map;
V9 upgraded the microbiome axis with primary data and showed that MS/IBD
proximity is not currently supported by broad shared taxonomic dysbiosis. V10
is now mining **axis disagreements**: where a comparator disease is near MS on
one supported axis and far/contradictory/intermediate on another.

Methodology integrity steps:

- V8 lock: `ROADMAP_V8.md`, `MAP_METHODOLOGY_V8.md`, commit `9c2e548`.
- V9 lock: `ROADMAP_V9.md`, `MAP_METHODOLOGY_V9.md`, commit `df7c7de`.
- V10 roadmap: `ROADMAP_V10.md`.

`OPENGWAS_JWT` is missing, so V10 genetics execution is access-blocked outside
existing UC/Crohn supported evidence.

## Current Deliverables

V10:

- `DISAGREEMENT_MATRIX_V10.md`
- `DISAGREEMENT_RESOLUTION_V10.md`
- `SJOGREN_SPLIT_AUDIT_V10.md`
- `RA_PREGNANCY_TREATMENT_DECOUPLING_V10.md`
- `TRANSFER_VALIDITY_MAP_V10.md`
- `AXIS_DISAGREEMENT_FINDINGS_V10.md`
- `CONVERGENCE_CHECK_V10_01.md`
- `CONVERGENCE_CHECK_V10_02.md`
- `analysis/v10_sjogren_gse23117/REPORT.md`
- `analysis/v10_disagreement/disagreement_pairs.tsv`
- `analysis/v10_disagreement/artifact_audit.tsv`

V9:

- `MICROBIOME_AXIS_V9.md`
- `DATA_SEARCH_V9.md`

V8:

- `MS_MECHANISM_MAP_V8.md`
- `analysis/v8_map/placement_matrix.tsv`
- `analysis/v8_map/evidence_registry.tsv`

## Current Interpretation

V10 supported-only matrix:

- `120` V8 placements.
- `21` supported/robust placements eligible.
- `10` supported-axis disagreement pairs.

Hostile critique corrected an overclaim:

- UC treatment-response versus tissue-repair looked clean initially, but
  Hypatia identified high axis non-independence because both axes reuse dynamic
  IFN/APC response evidence.
- `scripts/v10_build_disagreement_matrix.py` now applies an independence
  penalty to treatment-response/tissue-repair pairs.
- UC treatment-response versus tissue-repair is downgraded to an internal
  treatment-dynamics refinement, not a clean independent disagreement.

Cleanest current biological candidate:

- **Sjogren IFN/APC versus lipid-lysosomal split.**
- Sjogren salivary epithelial/APC antigen-presentation modules are positive or
  trending, while lipid-loader and lysosomal repair modules are null/negative
  in matched salivary epithelial/APC contexts.
- GSE23117 bulk salivary gland independently supports IFN/APC-positive and
  lysosomal/APC-null directionality:
  - `ifn_apc`: Hedges g `2.164`, p `0.000271`, FDR `0.00162`.
  - `lysosomal_apc`: Hedges g `0.165`, p `0.652`, FDR `0.652`.
- GSE23117 does not fully replicate a lipid-loader-negative claim because bulk
  `lipid_loader_repair` is positive-null: Hedges g `0.562`, p `0.144`, FDR
  `0.253`.
- MS implication: IFN/APC similarity alone is not sufficient evidence that a
  comparator disease models chronic-active MS lesion-rim lysosomal/APC or
  foamy myeloid biology. The lipid-loader part needs matched APC replication.

Important downgraded hypothesis:

- UC baseline mucosal IFN/APC height fails as a response predictor while early
  mucosal IFN/APC downshift repeatedly tracks response. This is a dynamic
  biomarker hypothesis, not a resolved MS mechanism.

Second V10 biological candidate:

- **RA pregnancy/postpartum versus blood APC/treatment decoupling.**
- RA blood APC state and RA anti-TNF blood response rules are negative or fail,
  but seropositive RA pregnancy data show late-pregnancy trough and postpartum
  rebound in MIF/CD74, HLA-II, IFN/APC, and lysosomal/APC modules.
- MS implication: RA is useful as a pregnancy/postpartum timing comparator, but
  not as a positive comparator for blood APC treatment-response biomarkers.

V9 microbiome result still stands:

- MS has primary-data stool microbiome shifts in one processed cohort.
- IBDMDB/HMP2 participant-aware tests did not support shared broad taxonomic
  IBD dysbiosis.
- MS/IBD proximity remains stronger on mucosal IFN/APC and response/repair
  axes than on microbiome.

## Highest-Value Next Actions

1. Attempt independent Sjogren salivary dataset replication or matched
   cell-type residualization for the IFN/APC versus lipid-lysosomal split.
2. Search for composition-adjusted RA/MS pregnancy datasets with monocyte/APC
   resolution and clinical activity timecourses.
3. Rebuild UC tissue-repair axis with independent repair endpoints before using
   it as an independent disagreement axis.
4. If genetics access becomes available, run harmonized LDSC/HDL with MHC
   exclusion.

## Compute / Access Notes

- Working directory: `/Users/soeren.leibach/Projects/ms-auto-research`.
- `.venv/bin/python` works for V7-V10 pandas/numpy/scipy/statsmodels scripts.
- `.venv_v3_py312/bin/python` works for the local TF-IDF knowledge index.
- R `4.6.0`, `phyloseq`, and `vegan` are installed.
