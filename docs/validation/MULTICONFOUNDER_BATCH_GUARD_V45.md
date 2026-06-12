# V45 Multi-Confounder Batch-Guard Stress Test

## Status

Synthetic method-characterization only. These results are not biological
evidence about MS. No locked rule, threshold, or frozen pre-registration was
changed, and no real Gafson data were read.

## Question

V44 showed that the additive batch diagnostic prevented response-correlated
batch from being reported as a clean validation. V45 stress-tested a harder
case: multiple technical or peri-treatment covariates acting together.

The test asked two questions:

1. Can interacting technical structures still create a clean synthetic-null
   pass after the existing individual-feature V44 guard?
2. Would a naive joint technical residualization guard improve the result?

## Simulation

Script:

- `scripts/v45_multiconfounder_batch_guard_simulation.py`

Outputs:

- `analysis/v45_multiconfounder_batch_guard/summary.json`
- `analysis/v45_multiconfounder_batch_guard/multiconfounder_batch_guard_summary.tsv`
- `analysis/v45_multiconfounder_batch_guard/multiconfounder_batch_guard_metrics.tsv`
- `analysis/v45_multiconfounder_batch_guard/multiconfounder_worst_cases.tsv`
- `analysis/v45_multiconfounder_batch_guard/synthetic/multiconfounder_subjects.tsv.gz`

Scale:

- `5,600` seeded synthetic cohorts.
- `336,000` synthetic subjects.
- `80` replicates per truth / scenario / severity cell.
- `7` scenarios:
  `independent_technical`, `batch_only`, `distributed_weak_technical`,
  `batch_plus_depth`, `batch_plus_steroid`, `immune_tone_plus_batch`,
  `normalization_plus_depth`.

## Headline Results

| Metric | Result |
|---|---:|
| Worst synthetic-null raw primary pass rate | `0.8625` |
| Worst synthetic-null acceptable pass after existing individual guard | `0.0125` |
| Worst synthetic-null acceptable pass after naive joint guard | `0.1000` |

Interpretation:

- The existing V44 individual-feature guard remained specific under these
  multi-confounder synthetic nulls.
- A naive joint residualization guard was **not** better; it allowed a higher
  worst-case synthetic-null clean pass rate and should not be adopted as a
  tightening without further calibration.

## Conservative-Sensitivity Cost

The existing guard is deliberately conservative. In planted-signal synthetic
cohorts with strong technical pathology, it often downgraded raw positives to
technically non-specific:

- `normalization_plus_depth`, severity `1.00`: raw planted pass `1.0000`,
  individual-guard acceptable pass `0.0000`.
- `batch_plus_steroid`, severity `1.00`: raw planted pass `0.9875`,
  individual-guard acceptable pass `0.0000`.
- even `independent_technical` planted cohorts at severity `0.00` had raw pass
  `0.9625` but individual-guard acceptable pass `0.2750`, showing that auditing
  many technical fields can create chance diagnostic flags in small cohorts.

This does **not** mean the primary V22 score changes. It means the diagnostic
guard is a specificity-preserving downgrade mechanism: a raw biological-looking
pass with technical flags should be reported as non-specific until resolved or
replicated, not discarded as impossible.

## Decision

No harness rule change is made here.

Supported additive conclusions:

1. Keep the V44 batch diagnostic as a required pre-data report.
2. Do not add naive joint technical residualization as a pass/fail modifier.
3. Add a follow-up calibration task: quantify whether permutation/FDR-calibrated
   diagnostic flags can reduce chance over-flagging while preserving the strong
   synthetic-null protection.

## Medical-Team Implication

For Gafson or any replacement cohort, technical metadata are not optional. A
small validation cohort can look positive under technical confounding, and the
guard appropriately prevents those positives from being interpreted as clean.
The cost is that a real positive in a technically imbalanced cohort may become
inconclusive, which is preferable to over-calling a validation.

