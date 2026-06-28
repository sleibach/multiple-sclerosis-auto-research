# V50 GSE255952 Future Import Checklist

Status: future import checklist only. This file does not import expression data,
run analysis, or make any biological claim.

Inputs:

- metadata scout:
  `knowledge_external/synthesis/V50_GSE255952_METADATA_SCOUT.md`
- metadata summary:
  `analysis/v50_gse255952_metadata_scout/GSE255952_metadata_summary_v50.json`

## Allowed Future Purpose

GSE255952 may be used only for steroid/glucocorticoid panel stress testing and
cell-compartment response characterization. It is not a DMF validation cohort
and must not be routed as a V22 scalar validation dataset.

## Pre-Import Stop/Go Checklist

| check | required result before import |
|---|---|
| Explicit task scope | Future task states "steroid-panel stress test" or equivalent method-characterization purpose. |
| No Gafson/V22 validation route | Task explicitly states the dataset is not being used to validate the locked V22 DMF scalar. |
| Source files identified | Processed matrix and sample metadata locators recorded from GEO. |
| Expression values permitted | Source and reuse terms reviewed for project-local analysis. |
| Sample pairing verified | T0/T1 pairs recoverable for each relapse treatment and compartment. |
| Compartment labels verified | CD19+ B-cell and CD4+ T-helper-cell labels recoverable per sample. |
| Response labels verified | Improved versus non-improved relapse-treatment labels recoverable without manual inference. |
| Patient/relapse-course grouping verified | The three patients with two methylprednisolone courses are handled without independence inflation. |
| Gene identifiers mapped | Clariom D array identifiers mapped to the V32 steroid/glucocorticoid panel genes. |
| Batch/platform fields recorded | Any array batch or processing fields captured before model fitting. |
| Null plan written | Pre/post label permutation or pair-label shuffling plan written before scoring. |

## Import Boundaries

Allowed:

- import processed gene-level matrix after the checklist passes;
- score only pre-specified steroid/glucocorticoid and possibly broad immune-tone
  panels;
- stratify by CD19+ B-cell and CD4+ T-helper-cell compartments;
- report method behavior of confounder panels.

Not allowed:

- use GSE255952 as evidence for DMF response;
- use GSE255952 as external validation of the locked V22 scalar;
- tune V22 modules, thresholds, or validation interpretation;
- treat methylprednisolone relapse-response biology as DMF treatment-response
  biology;
- ignore repeated relapse-treatment structure in the three patients with two
  courses.

## Minimum Future Output

A valid future import should produce:

1. sample manifest with patient, relapse course, compartment, T0/T1, and
   response labels;
2. gene-ID mapping manifest;
3. pre/post steroid-panel effect size by compartment;
4. null/permutation result;
5. explicit statement that the result is method-characterization for confounder
   scoring, not biological evidence for the V22 rule.

## Decision

GSE255952 is ready for a future scoped import only after the checklist above is
explicitly satisfied. Until then, V50 stores metadata only.
