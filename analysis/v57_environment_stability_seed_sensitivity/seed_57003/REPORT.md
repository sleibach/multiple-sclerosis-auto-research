# V57 Environment-Stability And Selective-Prediction Probe

This is a method-behavior analysis around the immutable V22 score. It is
not a new biomarker, target, treatment result, or causal finding.

## Environment Stability

| Cohort | n | AUC | Hedges g | Exact p |
|---|---:|---:|---:|---:|
| `GSE235357` | 10 | 0.720 | 0.651 | 0.1548 |
| `GSE250453` | 10 | 0.600 | 0.150 | 0.3452 |
| `GSE253006_TOF_exact` | 9 | 0.950 | 1.811 | 0.0159 |
| `GSE85034_ADA` | 14 | 0.511 | 0.044 | 0.5000 |

- Weighted mean AUC: `0.672` (stratified permutation p=`0.032130`).
- Worst-environment AUC: `0.511`.
- Cochran Q p: `0.3159`.
- Frozen stability verdict: **NOT_ENVIRONMENT_STABLE**.

## Selective Prediction

- Primary alpha: `0.1`.
- Pooled coverage: `0.953`.
- Worst-cohort coverage: `0.900`.
- Singleton rate: `0.140`.
- Singleton accuracy: `0.6666666666666666`.
- Singleton correctness stratified-null p: `0.234558`.
- Frozen selective-prediction verdict: **NOT_TRANSPORT_READY**.

Whole-cohort holdout deliberately violates any casual IID assumption. Failure is
evidence that an uncertainty wrapper calibrated on these source cohorts should not
be trusted to guarantee coverage in a new MS cohort. Passing would still require
prospective validation.
