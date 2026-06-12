# HARNESS ROBUSTNESS V43

Status: synthetic method-characterization only. These stress tests define data-quality warning signs; they are not biological evidence.

## Simulation Scale

- Synthetic cohorts: `1860`.
- Replicates per pathology/severity/truth cell: `30`.
- Baseline planted effect: effect size `1.25`, `30` responders and `30` nonresponders.
- Full synthetic subject-level data: `analysis/v43_method_validation/synthetic/robustness_simulation_subjects.tsv.gz`.

## Trust Envelope

The harness is trustworthy when the received data package keeps the observed pathology severity inside the ranges below. The envelope requires both planted-signal recovery (`correct_rate >= 0.80`) and null false-positive control (`null pass rate <= 0.05`). Outside it, interpret Gafson as inconclusive or non-specific unless the issue can be resolved before running the frozen analysis.

| Pathology | Largest tested severity inside envelope | Criterion |
|---|---:|---|
| batch_response_correlated | 0.25 | planted_correct_rate>=0.80 and null_pass_rate<=0.05 |
| gene_id_loss | 0.25 | planted_correct_rate>=0.80 and null_pass_rate<=0.05 |
| label_swap | 0.0 | planted_correct_rate>=0.80 and null_pass_rate<=0.05 |
| missing_timepoints | 0.25 | planted_correct_rate>=0.80 and null_pass_rate<=0.05 |
| normalization_noise | 0.0 | planted_correct_rate>=0.80 and null_pass_rate<=0.05 |
| outlier_samples | 0.0 | planted_correct_rate>=0.80 and null_pass_rate<=0.05 |
| receptor_artifact | 1.0 | planted_correct_rate>=0.80 and null_pass_rate<=0.05 |

Worst null false-positive stress cells:

| Pathology | Severity | Null pass rate | Mean AUC |
|---|---:|---:|---:|
| batch_response_correlated | 1.0 | 0.400 | 0.675 |
| batch_response_correlated | 0.75 | 0.167 | 0.624 |
| batch_response_correlated | 0.5 | 0.067 | 0.562 |
| missing_timepoints | 0.4 | 0.033 | 0.518 |
| gene_id_loss | 0.25 | 0.033 | 0.498 |

## Machine-Readable Outputs

- `analysis/v43_method_validation/robustness_cohort_results.tsv`
- `analysis/v43_method_validation/robustness_summary.tsv`
- `analysis/v43_method_validation/robustness_envelope.tsv`
