# V54 Lysosomal Morphology Specificity

Verdict: **SPECIFICITY_SURVIVES_TESTED_STATE_ADJUSTMENT**.

This post-result sensitivity re-tested the isolated GSE279972 lysosomal
association after adding pre-specified resident-microglia identity and
de-overlapped MIMS state covariates. It used donor-clustered intervals,
300,000 three-seed donor-wild nulls, max-variant control, and leave-one-donor
checks.

| model | beta | cluster CI | wild p | max-variant p | LODO min |
|---|---:|---:|---:|---:|---:|
| base | 0.493 | [0.176, 0.810] | 0.004627 | 0.05962 | 0.384 |
| resident_adjusted | 0.753 | [0.402, 1.105] | 0.001207 | 0.001207 | 0.620 |
| mims_adjusted | 0.372 | [0.088, 0.656] | 0.01246 | 0.1889 | 0.289 |
| resident_and_mims_adjusted | 0.517 | [0.199, 0.834] | 0.00861 | 0.04526 | 0.420 |

These covariates are expression-state proxies and can be biologically
entangled with foamy activation. The result therefore cannot establish
cell-composition independence, causal lysosomal biology, therapeutic
direction, or an effect on disability progression.
