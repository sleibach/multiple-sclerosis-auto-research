# V54 Progression-Event Power Design

All outputs are synthetic method behavior, not biological evidence.

The default grid simulated 288,000 cohorts across 192 cells and 3 seeds. Median null false-positive rate was `0.043` and the maximum grid-cell null rate was `0.060`.

The grid models one frozen standardized molecular predictor of a binary
progression event. It is deliberately generic: a received cohort must replace
the assumed event rate, missingness, reliability, and analysis route before any
score is viewed.

## Minimum N Under Explicit Assumptions

`minimum_n_by_assumption.tsv` reports the first simulated sample size with
aggregate conclusive probability >=0.80 and every seed >=0.75. `not_reached`
means the default grid through n=240 did not meet that method-design threshold.

| event rate | OR / latent SD | missing | repeats | minimum n | power at n=240 |
|---:|---:|---:|---:|---:|---:|
| 0.15 | 1.25 | 0.00 | 1 | not_reached | 0.167 |
| 0.15 | 1.25 | 0.00 | 2 | not_reached | 0.189 |
| 0.15 | 1.25 | 0.20 | 1 | not_reached | 0.139 |
| 0.15 | 1.25 | 0.20 | 2 | not_reached | 0.155 |
| 0.30 | 1.25 | 0.00 | 1 | not_reached | 0.241 |
| 0.30 | 1.25 | 0.00 | 2 | not_reached | 0.283 |
| 0.30 | 1.25 | 0.20 | 1 | not_reached | 0.212 |
| 0.30 | 1.25 | 0.20 | 2 | not_reached | 0.254 |
| 0.15 | 1.50 | 0.00 | 1 | not_reached | 0.445 |
| 0.15 | 1.50 | 0.00 | 2 | not_reached | 0.509 |
| 0.15 | 1.50 | 0.20 | 1 | not_reached | 0.357 |
| 0.15 | 1.50 | 0.20 | 2 | not_reached | 0.439 |
| 0.30 | 1.50 | 0.00 | 1 | not_reached | 0.651 |
| 0.30 | 1.50 | 0.00 | 2 | not_reached | 0.723 |
| 0.30 | 1.50 | 0.20 | 1 | not_reached | 0.555 |
| 0.30 | 1.50 | 0.20 | 2 | not_reached | 0.608 |
| 0.15 | 2.00 | 0.00 | 1 | 240 | 0.875 |
| 0.15 | 2.00 | 0.00 | 2 | 240 | 0.903 |
| 0.15 | 2.00 | 0.20 | 1 | not_reached | 0.759 |
| 0.15 | 2.00 | 0.20 | 2 | 240 | 0.834 |
| 0.30 | 2.00 | 0.00 | 1 | 160 | 0.970 |
| 0.30 | 2.00 | 0.00 | 2 | 120 | 0.975 |
| 0.30 | 2.00 | 0.20 | 1 | 160 | 0.931 |
| 0.30 | 2.00 | 0.20 | 2 | 160 | 0.957 |

These values cannot be used as a universal progression cohort target. The
true effect is unknown, event definitions differ, and the model omits many
real longitudinal complexities. The durable output is the parameterized
interface and calibrated null, to be rerun on the blinded receipt inventory.
