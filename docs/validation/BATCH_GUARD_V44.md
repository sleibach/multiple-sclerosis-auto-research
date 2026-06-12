# BATCH_GUARD_V44: Additive Batch-Diagnostic Hardening

Date: 2026-06-12

Status: synthetic method-characterization and blind harness hardening. This is
not biological evidence and does not change the immutable V22 rule or V42
primary thresholds.

## Why This Was Needed

V43 identified response-correlated batch as the main false-positive pathology
for the frozen validation harness: in synthetic null cohorts, severe
response-correlated batch effects produced a primary null pass rate up to
`0.40`.

V44 therefore adds a **diagnostic guard**, not a new score:

- the primary V22 score is still computed exactly as pre-registered;
- the primary V22 verdict is still reported first;
- technical metadata are audited separately;
- a primary pass with a batch-risk flag is interpreted as technically
  non-specific until the batch issue is resolved.

## Harness Change

Updated script:

- `scripts/v42_gafson_validation_harness.py`

New additive behavior:

- carries optional technical metadata into `paired_module_deltas.tsv`;
- writes `batch_diagnostic_metrics.tsv`;
- adds `batch_guard_flag` to `validation_summary.json`;
- does not alter module definitions, expression preprocessing, score
  orientation, primary metrics, or pass/fail thresholds.

Technical metadata fields audited if supplied:

`batch`, `lane`, `flowcell`, `run`, `sequencing_batch`, `processing_batch`,
`capture_batch`, `library_batch`, `collection_date`, `processing_date`, `rin`,
`rqn`, `sequencing_depth`, `percent_mapped`, `steroid_exposure`.

For each available metadata feature the harness reports:

- response association (`metadata_auc`);
- association with the locked score (`spearman_with_locked`);
- residualized locked-score AUC and attenuation when stable;
- verdict: `BATCH_RISK_FLAG`, `NO_BATCH_RISK_FLAG`,
  `UNDERPOWERED_FOR_RESIDUALIZATION`, `UNSCOREABLE`, or
  `UNINFORMATIVE_SINGLE_LEVEL`.

## Synthetic Validation Scale

Script:

- `scripts/v44_batch_guard_simulation.py`

Inputs:

- V43 synthetic robustness subjects:
  `analysis/v43_method_validation/synthetic/robustness_simulation_subjects.tsv.gz`

Outputs:

- `analysis/v44_batch_guard/batch_guard_cohort_metrics.tsv`
- `analysis/v44_batch_guard/batch_guard_summary.tsv`
- `analysis/v44_batch_guard/batch_guard_envelope.tsv`
- `analysis/v44_batch_guard/summary.json`

Scale:

- `1,860` synthetic cohorts.
- Same V43 robustness grid and seeds.
- Synthetic data only; no real Gafson data read.

## Result

For the exact high-risk V43 pathology, response-correlated batch:

| Truth | Severity | Primary pass rate | Batch-risk flag rate | Guarded acceptable pass rate |
|---|---:|---:|---:|---:|
| Null | 0.00 | 0.000 | 0.100 | 0.000 |
| Null | 0.25 | 0.000 | 0.833 | 0.000 |
| Null | 0.50 | 0.067 | 1.000 | 0.000 |
| Null | 0.75 | 0.200 | 1.000 | 0.000 |
| Null | 1.00 | 0.400 | 1.000 | 0.000 |
| Planted | 0.00 | 0.900 | 0.067 | 0.833 |
| Planted | 0.25 | 0.967 | 0.667 | 0.300 |
| Planted | 0.50 | 0.967 | 1.000 | 0.000 |
| Planted | 0.75 | 1.000 | 1.000 | 0.000 |
| Planted | 1.00 | 1.000 | 1.000 | 0.000 |

Headline:

- maximum null primary pass rate under response-correlated batch: `0.40`;
- maximum null guarded acceptable pass rate under response-correlated batch:
  `0.00`;
- absolute reduction in worst-case synthetic batch false-positive risk: `0.40`.

## Interpretation

The guard does what it is supposed to do: it prevents a response-correlated
batch artifact from being reported as a clean validation.

It is deliberately conservative. Under planted signal plus moderate
response-correlated batch (`severity=0.25`), the primary synthetic pass rate is
`0.967`, but the guarded acceptable pass rate falls to `0.300`. This means a
real positive Gafson result with response-correlated batch should not be
discarded as biology-free, but it also cannot be called clean validation until
the batch structure is resolved or replicated.

## Trust Envelope Delta

Compared with V43, the batch guard changes interpretation rather than primary
performance:

- response-correlated batch is no longer allowed to produce a clean pass;
- any non-trivial response-correlated batch structure downgrades the result to
  non-specific/inconclusive;
- clean validation now requires the real data to show no meaningful
  response-correlated technical structure.

For Gafson, the practical rule is:

> A raw pass plus `batch_guard_flag=false` is interpretable as a clean technical
> validation result. A raw pass plus `batch_guard_flag=true` is a technically
> non-specific positive that requires batch resolution or independent
> replication before it can strengthen the lead.

