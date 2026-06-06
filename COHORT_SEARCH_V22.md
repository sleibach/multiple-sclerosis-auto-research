# V22 Treatment-Response Cohort Search And Eligibility Notes

Purpose: document held-out cohort assembly for `LOCKED_RULE_V22.md`.

## Excluded Derivation / Prior-Validation Cohorts

These were not counted as V22 held-out validation because they contributed to
V6/V7 derivation, V7 validation, or V7 kill/survival decisions:

- `GSE282122`: anti-TNF IBD derivation for IFN/APC delta signal.
- `GSE138064`: MS IFN-beta baseline HLA-II derivation.
- `GSE24427`: MS IFN-beta longitudinal month-1 HLA-II derivation.
- `GSE16879`: V7 held-out infliximab IBD validation.
- `GSE73661_IFX`: V7 held-out infliximab IBD validation.
- `GSE73661_VDZ_W6_exploratory`: V7 exploratory vedolizumab branch.
- `GSE8350`, `GSE12051`, `GSE12251`, `GSE138746_CD14`: V7 negative or
  exclusion tests.

## Local Held-Out Cohorts Tested In V22

- `GSE235357`: MS dimethyl fumarate paired PBMC transcriptomics with
  responder/non-responder labels; local cache under
  `data/raw_v3/wave96_ms_treatment/`.
- `GSE250453`: MS fingolimod paired RNA-seq with responder/non-responder
  labels; local cache under `data/raw_v3/wave96_ms_treatment/`.
- `GSE85034_ADA`: psoriasis adalimumab lesional-skin baseline-to-week-1
  expression with week-16 PASI75 outcome; local cache under
  `data/raw_v3/wave89_psoriasis_response/`.
- `GSE253006_TOF`: ulcerative-colitis tofacitinib single-cell sample-level
  module summaries; local results under `results_v3/gse253006_tofacitinib/`.
  This is exploratory for V22 because the precomputed module is broader than
  the frozen V22 IFN/APC gene set and compartment is unresolved.

## Bounded External Index Check

NCBI GEO DataSets E-utilities were queried during V22 for obvious additional
MS DMT response transcriptomic cohorts:

- `multiple sclerosis natalizumab transcriptome response`: `Count=1` in GEO
  DataSets search; not acquired in this bounded session because eligibility
  metadata and paired early-treatment response structure were not established.
- `multiple sclerosis fingolimod transcriptome response`: `Count=0`.
- `ocrelizumab multiple sclerosis transcriptome response`: `Count=0`.
- `multiple sclerosis dimethyl fumarate transcriptome response`: query was
  rate-limited by NCBI after three unauthenticated requests.

No additional directly usable MS DMT held-out cohort was acquired in this
bounded V22 run.

## Remaining Acquisition Need

The most valuable next validation dataset is an MS DMT cohort with:

- baseline and early on-treatment whole-blood/PBMC or sorted-immune
  transcriptomics;
- natalizumab, ocrelizumab, fingolimod, dimethyl fumarate, or other current
  MS DMT exposure;
- prospective clinical response labels;
- enough samples for a meaningful CI, ideally `n >= 30`.

