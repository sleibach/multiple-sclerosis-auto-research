# CONVERGENCE_CHECK_V11_01

Timestamp: 2026-06-04 00:22 CEST

## Session Objective

Initialize the V11 resume backbone and advance at least one previously
unresolved supported disagreement cell.

## Resume Backbone Created

- `analysis/v11_matrix/disagreement_matrix.tsv`
- `meta/MATRIX_STATUS.md`
- `meta/NEXT_ACTIONS.md`
- `scripts/v11_update_matrix_state.py`

The V11 matrix is frozen from the V10 supported-only disagreement enumeration.

## Matrix State

- Total qualifying supported disagreement cells: `10`.
- Non-unresolved cells: `6`.
- Completion: `60.0%`.
- Status counts:
  - `intervention_derived`: `1`.
  - `biological`: `3`.
  - `artifact`: `2`.
  - `unresolved`: `4`.

## Cells Resolved This Session

### 001 UC IFN/APC Near Versus Treatment-Response Contradictory

File:

- `UC_STATIC_DYNAMIC_APC_DECOUPLING_V11.md`

Resolution:

- Status: `intervention_derived`.
- Classification: biological/measurement-class decoupling with MS
  transfer-validity consequence.

Finding:

> UC is near MS on inflammatory IFN/APC state, but treatment-response transfer
> depends on dynamic IFN/APC downshift rather than baseline IFN/APC height.

Key evidence:

- UC colon myeloid cross-sectional IFN/APC is high:
  - `mixscale_validated_ifng_readout`: Hedges g `3.271`, p `0.000116`, FDR
    `0.0250`.
  - `ifn_apc`: Hedges g `2.359`, p `0.00130`, FDR `0.0525`.
- Baseline UC mucosal IFN/APC fails:
  - `GSE12251`: AUC `0.250`, Hedges g `-1.043`, p `0.0195`, n `22`.
- Early mucosal `-delta_IFN_APC` passes:
  - `GSE16879`: AUC `0.754`, Hedges g `0.985`, p `0.000365`, n `60`.
  - `GSE73661_IFX`: AUC `0.825`, Hedges g `1.390`, p `0.0127`, n `23`.

MS consequence:

- Do not transfer UC baseline IFN/APC height as an MS response stratifier.
- If transferring this axis, test early compartment-relevant IFN/APC delta as a
  pharmacodynamic readout.

### 005 RA Tissue-Repair Far Versus Pregnancy Near

File:

- `RA_TISSUE_REPAIR_PREGNANCY_SCOPE_AUDIT_V11.md`

Resolution:

- Status: `artifact`.
- Classification: axis-scope correction.

Finding:

> The RA axis-08 far placement is supported mainly by blood anti-TNF
> response-monitoring failures, while synovial tissue repair remains
> under-tested.

MS consequence:

- RA pregnancy/postpartum timing remains transferable as a natural-experiment
  comparator.
- RA blood APC response-monitoring remains non-transferable.
- RA synovial repair must be rebuilt as a separate axis before any MS transfer
  claim.

## Genetics Credential

`OPENGWAS_JWT` remained unavailable this session. Executable OpenGWAS/LDSC work
therefore remains blocked; genetics-involving cells should use existing
published/support-grade evidence unless credentials become available.

## Next Session First Action

Read `meta/NEXT_ACTIONS.md`, then start with:

- `006_ulcerative_colitis_axis_02_genetics_vs_axis_07_treatment_response`

Required first audit:

- Treat it as a genetics-involving cell.
- Do not run OpenGWAS unless `OPENGWAS_JWT` is present.
- If still blocked, resolve using the existing Yang 2021 MS-UC genetic
  correlation evidence plus the V7 UC treatment-response contradiction, with
  explicit limitation that coloc/local-rg is unavailable.
