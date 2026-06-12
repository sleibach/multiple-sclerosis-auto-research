# V45 Pharmacodynamic-Only Cohort Preregistration Skeleton

## Status

Preparation artifact. This applies to open longitudinal treatment cohorts that
lack response/remission/NEDA labels, such as `GSE228330`. It does not validate
the V22 rule and cannot be used to claim response prediction.

## Purpose

Define what may and may not be done with open pharmacodynamic cohorts while
response-labeled validation data are delayed.

Allowed uses:

- module coverage and platform feasibility checks;
- longitudinal pharmacodynamic trajectory summaries;
- batch/QC and timepoint-diagnostic harness exercise;
- therapy-mechanism context for interpreting future response validation.

Forbidden uses:

- response validation;
- AUC, responder/nonresponder, remission, relapse, or NEDA claims without
  sample-mapped clinical labels;
- post-hoc labeling by subtype/status as if it were response;
- tuning the V22 rule or any successor rule.

## Candidate Example: GSE228330

V45 record-level audit:

- `docs/validation/GSE228330_OUTCOME_SCOUT_V45.md`
- `analysis/v45_gse228330_outcome_scout/`

Verified:

- PBMC expression;
- ocrelizumab / anti-CD20;
- baseline, 2-week, and 6-month timepoints;
- 44 public expression samples.

Blocker:

- no public responder, NEDA, relapse, or EDSS-change labels mapped to samples.

Therefore `GSE228330` is pharmacodynamic context only unless author-provided
clinical outcomes are obtained.

## Frozen Pharmacodynamic Questions

These may be answered without response labels:

1. Are V22 IFN/APC, HLA-II, and receptor genes represented on the platform?
2. What is the direction and magnitude of early and later treatment-associated
   module change?
3. Are module changes dominated by one timepoint, subtype/status group, or
   technical batch?
4. Does the therapy produce a module shift that would make future response
   validation technically feasible?

These must be reported descriptively and without clinical-response language.

## Required Input Schema

Schema file:

- `docs/validation/input_schemas/V45_pharmacodynamic_only_schema.tsv`

Required fields:

- `sample_id`
- `subject`
- `timepoint`
- exact treatment-relative time if available
- expression matrix or platform feature matrix
- therapy name/class
- batch/QC metadata where available

Optional but useful:

- disease subtype/status;
- prior therapy;
- steroid exposure;
- infection;
- cell counts/fractions.

## Fixed Analyses

1. Run module gene coverage only.
2. Compute module scores using the frozen V22 module definitions if coverage
   passes.
3. Summarize paired within-subject deltas by timepoint:
   baseline to early, baseline to later.
4. Report batch/QC associations with module deltas.
5. Report receptor-only trajectory separately.
6. Do not compute response-prediction metrics.

## Output Template

Every pharmacodynamic-only run should write:

- `module_gene_coverage.tsv`
- `paired_pharmacodynamic_module_deltas.tsv`
- `timepoint_summary.tsv`
- `batch_qc_diagnostic_summary.tsv`
- `pharmacodynamic_context_summary.md`

Required language:

> This cohort lacks sample-mapped response labels. Results are pharmacodynamic
> context only and do not validate or falsify the locked V22 treatment-response
> rule.

## Upgrade Path To Validation

A pharmacodynamic-only cohort can be upgraded to response validation only if the
following are obtained before analysis:

1. sample-mapped response/remission/NEDA/relapse labels;
2. clinical outcome definition and assessment window;
3. subject-to-sample map across timepoints;
4. batch/QC and confounder metadata sufficient for V42/V44 diagnostics.

If upgraded, write a cohort-specific preregistration addendum before scoring the
response labels.

