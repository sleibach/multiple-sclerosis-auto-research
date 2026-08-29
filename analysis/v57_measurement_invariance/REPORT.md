# V57 Cross-Environment Measurement-Invariance Result

## Result

- Global two-module gate: **FAIL**.
- Cohorts: GSE235357 n=10, GSE253006_TOF_exact n=9.
- Patient uncertainty: 30,000 seeded bootstrap
  resamples per module; only aggregate intervals retained.

| module | genes | edge concordance | gene-label p | minimum bootstrap CI low | primary pass |
|---|---:|---:|---:|---:|---|
| IFN_APC | 7 | 0.015 | 0.467063 | -0.322 | False |
| HLAII | 6 | -0.445 | 0.991667 | -0.463 | False |
| UNION_EXPLORATORY | 12 | 0.167 | 0.132480 | -0.214 | not_applicable |

## Interpretation

The test asks whether the same frozen names behave as a comparable multigene
measurement across environments. It does not retest outcome performance. A
failure prevents upgrading the bounded association to a shared latent
APC/HLA-II construct from these cohorts alone; it does not erase the empirical
within-cohort score associations. Different tissue, treatment, and platform are
inseparable from environment here, so the result localizes a transportability
problem rather than identifying its cause.
