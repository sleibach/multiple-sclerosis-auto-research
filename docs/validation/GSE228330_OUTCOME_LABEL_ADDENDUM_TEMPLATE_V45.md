# V45 GSE228330 Outcome-Label Addendum Template

Status: blank preregistration addendum template. No GSE228330 outcome labels have
been received or scored.

Shared no-degrees-of-freedom checklist:

`docs/validation/SECONDARY_ROUTE_NO_DOF_CHECKLIST_V45.md`

## Purpose

`GSE228330` is currently open ocrelizumab PBMC pharmacodynamic context only. If
authors later provide sample-mapped response/NEDA/relapse/EDSS labels and a
verified subject/timepoint map, this template defines the addendum that must be
filled and committed before any outcome-labeled analysis.

This template exists to prevent an outcome-labeled GSE228330 upgrade from being
improvised after labels arrive.

## Non-Negotiable Role Statement

GSE228330 is **not** a drop-in primary replacement for the Gafson DMF/NEDA V42
validation.

Reason:

- therapy is ocrelizumab / anti-CD20, not DMF;
- the V23/V32/V44 interpretation is mechanism-bounded and immune-tone/batch
  guarded;
- public data currently lack verified paired subject mapping and outcomes;
- array processing is not ready locally without additional Bioconductor platform
  support or author processed expression.

If labels arrive, the pre-specified role is:

> secondary anti-CD20 mechanism-domain stress test of pharmacodynamic trajectory
> and outcome association, not primary validation of the DMF V22/V42 rule.

A clean positive would support broader follow-up. A clean negative would bound
or weaken anti-CD20 transferability but would not by itself kill the DMF/Gafson
primary monitoring lead.

## Required Before Finalizing This Addendum

Fill and freeze all of these before scoring:

1. `docs/validation/input_schemas/V45_data_use_terms_capture_template.tsv`
2. `docs/validation/input_schemas/V45_outcome_label_dictionary_template.tsv`
3. verified GSM-to-subject/timepoint map
4. expression-processing provenance or author-provided processed expression
5. intake preflight result
6. subject-map sanity result
7. response-column audit result, if any pharmacodynamic-only context run is also
   planned

## Frozen Analysis Choices To Fill

| Field | Pre-fill / required choice |
|---|---|
| cohort ID | `gse228330_ocrelizumab_pbmc` |
| therapy | ocrelizumab |
| therapy class | anti-CD20 / B-cell depletion |
| primary role | secondary mechanism-domain stress test |
| primary feature | locked V22 early-change scalar, unchanged, only if verified baseline + early on-treatment pairs exist |
| context features | pharmacodynamic module trajectories from `PHARMACODYNAMIC_ONLY_PREREGISTRATION_V45.md` |
| outcome | from frozen outcome-label dictionary |
| success interpretation | secondary support for anti-CD20 transferability, not primary validation |
| failure interpretation | anti-CD20 transferability not supported; does not kill DMF primary lead |
| confounders | V32/V44/V45 batch, immune-tone, steroid, composition diagnostics where metadata allow |
| forbidden analyses | no threshold tuning, no feature selection, no post-hoc response definition, no baseline-only rescue claim |

## Analysis Budget

Pre-specify exactly which analyses will run:

1. context-only pharmacodynamic trajectory summary;
2. locked V22 scalar vs outcome if paired early samples and labels are usable;
3. confounder/batch diagnostic report;
4. effect-size and CI reporting;
5. no additional feature search.

If any required input is missing, mark the corresponding analysis
`unscoreable_before_analysis`.

## Outcome Interpretation Grid

| Result | Interpretation |
|---|---|
| raw positive, diagnostics clean | secondary support that anti-CD20 shares the monitoring axis; requires independent replication |
| raw positive, batch/immune-tone flagged | technically non-specific; do not count as clean support |
| null/negative, adequate paired n and clean diagnostics | anti-CD20 transferability not supported in this cohort |
| null/negative, underpowered or metadata-poor | inconclusive; use effect size/CI for future design |
| subject map fails | no paired-delta outcome analysis allowed |
| labels ambiguous | no outcome analysis allowed until dictionary is frozen |

## Machine-Readable Template

`docs/validation/input_schemas/V45_gse228330_outcome_addendum_template.tsv`

This template should be copied into a cohort-specific finalized addendum only
after labels and mapping are received, terms are captured, and the dictionary is
frozen.
