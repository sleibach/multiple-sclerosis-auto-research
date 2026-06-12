# Karolinska DMF ROS Preregistration Template V45

Status: template to be finalized only if labels arrive. This is not an active
validation plan yet and does not authorize scoring outcomes.

Shared no-degrees-of-freedom checklist:

`docs/validation/SECONDARY_ROUTE_NO_DOF_CHECKLIST_V45.md`

## Scope

Target cohort:

- `GSE130494` SuperSeries;
- `GSE130478` expression subseries;
- `GSE130491` methylation subseries;
- PMID `31300673`, DOI `10.1038/s41467-019-11139-3`.

Current blocker:

- public expression/methylation data exist;
- patient-level beneficial-response labels and GSM-to-patient/timepoint mapping
  are not public;
- therefore no response analysis is allowed until author-supplied labels and
  mapping are received, checksummed, and manifest-listed.

## Intended Role If Labels Arrive

Karolinska is a secondary MS DMF stress-test, not a primary Gafson replacement.

Reasons:

- `GSE130478` expression is CD4+ T-cell array data, not PBMC RNA-seq;
- expression timepoints are baseline and 6 months, not the V22 ideal early
  4-8 week window;
- the publication's beneficial-response definition is redox/monocyte-linked and
  must be frozen exactly as supplied before scoring.

Allowed role if mapping is adequate:

1. secondary direction/effect-size consistency check for DMF;
2. later-treatment pharmacodynamic stress test;
3. platform/cell-type portability check for the APC/HLA/IFN monitoring signal.

Forbidden role:

- do not count as a clean V22 early PBMC validation unless a future addendum
  documents an eligible early transcriptomic timepoint and PBMC-equivalent
  expression, which is not expected from public records.

## Files Required Before Finalization

Minimum:

- expression matrix or raw/processed expression files for `GSE130478`;
- GSM-to-subject/timepoint/cell-type map;
- beneficial-response/nonresponder label per subject;
- clinical definition and cutoff for beneficial response;
- technical covariates: array batch, processing date, RNA quality/QC where
  available.

Strongly preferred:

- monocyte count and ROS measures by subject/timepoint;
- steroid exposure near sampling;
- age, sex, disease duration, prior DMT, baseline disease activity;
- sample-level mapping to `GSE130491` if methylation/monocyte context is used.

## Blind Finalization Procedure

Once data arrive:

1. Place files under `data/raw_v3/karolinska_dmf_ros_2019/`.
2. Write `README_source.txt` and preserve original filenames.
3. Compute `SHA256SUMS` before opening content.
4. Update data manifest.
5. Fill the placeholders in this template using file metadata and author
   documentation only.
6. Commit the finalized Karolinska addendum before computing module scores or
   outcome associations.

## Frozen Candidate Analyses

The finalized addendum must choose exactly one of these roles before scoring:

### Role A: Secondary Response Stress Test

Use only if:

- each expression sample maps to subject and timepoint;
- each subject maps to a binary beneficial-response label;
- module coverage is adequate on the expression platform;
- baseline and 6-month samples pair within subject.

Fixed feature:

```text
late_dmf_signed_score = delta_HLAII - delta_IFN_APC
delta_module = month6_module_score - baseline_module_score
```

Fixed orientation:

- beneficial responders are predicted to have higher `late_dmf_signed_score`.

Interpretation:

- secondary late-timepoint consistency only;
- not a clean V22 early-monitoring validation.

### Role B: Pharmacodynamic / Platform Context Only

Use if response labels are missing, incomplete, non-binary, or not mapped to
paired expression subjects.

Allowed:

- module coverage;
- baseline-to-6-month module deltas;
- pharmacodynamic context with `scripts/v45_pharmacodynamic_only_harness.py`.

Forbidden:

- responder/nonresponder AUC;
- validation pass/fail language.

### Role C: Blocked

Use if sample mapping, timepoints, or module coverage are insufficient.

Output:

- blocker table only;
- no module-response scoring.

## Fixed Module Definitions

Use the V22 frozen modules unchanged:

- IFN/APC: `STAT1`, `IRF1`, `CXCL10`, `GBP1`, `ISG15`, `CD74`, `HLA-DRA`
- HLA-II: `HLA-DRA`, `HLA-DRB1`, `HLA-DPA1`, `HLA-DPB1`, `HLA-DQA1`,
  `HLA-DQB1`
- receptor-only control: `CD74`, `CD44`, `CXCR4`

Coverage:

- IFN/APC and HLA-II must each have at least `50%` mapped genes/features;
- receptor-only is reported if scoreable.

## Pre-Specified Metrics For Role A

Primary:

- AUC of `late_dmf_signed_score` for beneficial response;
- Hedges g, responder minus nonresponder;
- bootstrap AUC CI with seed `20260606`.

Secondary:

- `delta_IFN_APC`, `delta_HLAII`, and receptor-only delta separately;
- batch/QC diagnostics;
- steroid and prior-DMT sensitivity if metadata are supplied.

Interpretation thresholds:

- AUC `>= 0.70` and Hedges g `>= 0.50` = directional secondary support if
  technically clean;
- AUC `< 0.60` or Hedges g `< 0.20` in an adequate mapped set = secondary fail;
- any result with technical/batch ambiguity is non-specific.

Because this is a later CD4+ T-cell platform, a positive result cannot by itself
upgrade the primary V22 lead, and a negative result cannot by itself kill it.

## Placeholders To Fill Only After Receipt

```text
Received file manifest:
SHA256SUMS path:
Author-provided response definition:
Number of expression subjects with paired baseline/month6 samples:
Number of responders:
Number of nonresponders:
Expression platform annotation status:
Module coverage:
Technical covariates available:
Final assigned role (A/B/C):
```
