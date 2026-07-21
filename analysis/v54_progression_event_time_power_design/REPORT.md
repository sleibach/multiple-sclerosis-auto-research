# V54 Progression Event-Time And Covariate Power Design

All outputs are seeded synthetic method behavior. They are not biological
evidence and do not estimate MS progression rates or effects.

The frozen grid generated 90,000 unique
synthetic cohorts and 180,000 route evaluations.
Each cohort was tested unadjusted and stratified by source x treatment.

## Null Calibration

The stratified route had median null pass rate `0.046`
and maximum `0.065`.
The maximum is 49/750 (Wilson 95% CI `0.050-0.085`). Across 40 null cells, the Binomial reference
probability of a maximum at least this large is `0.776`.

Under deliberate
score-source-treatment confounding, the unadjusted route had median
`0.089` and maximum
`0.191`. These are simulation
calibration results, not cohort facts.

## Adjusted Planning Thresholds

The table reports the first simulated N at which aggregate conclusive
probability is at least 0.80 and every seed is at least 0.75.

| confounding | dropout | event probability | HR / latent SD | minimum N | power at N=320 |
|---:|---:|---:|---:|---:|---:|
| 0.0 | 0.00 | 0.15 | 1.5 | not_reached | 0.601 |
| 0.0 | 0.00 | 0.15 | 2.0 | 240 | 0.936 |
| 0.0 | 0.00 | 0.30 | 1.5 | 320 | 0.867 |
| 0.0 | 0.00 | 0.30 | 2.0 | 120 | 1.000 |
| 0.0 | 0.25 | 0.15 | 1.5 | not_reached | 0.549 |
| 0.0 | 0.25 | 0.15 | 2.0 | 240 | 0.945 |
| 0.0 | 0.25 | 0.30 | 1.5 | 320 | 0.825 |
| 0.0 | 0.25 | 0.30 | 2.0 | 120 | 0.996 |
| 0.8 | 0.00 | 0.15 | 1.5 | not_reached | 0.463 |
| 0.8 | 0.00 | 0.15 | 2.0 | 320 | 0.884 |
| 0.8 | 0.00 | 0.30 | 1.5 | not_reached | 0.744 |
| 0.8 | 0.00 | 0.30 | 2.0 | 160 | 0.993 |
| 0.8 | 0.25 | 0.15 | 1.5 | not_reached | 0.415 |
| 0.8 | 0.25 | 0.15 | 2.0 | 320 | 0.817 |
| 0.8 | 0.25 | 0.30 | 1.5 | not_reached | 0.685 |
| 0.8 | 0.25 | 0.30 | 2.0 | 160 | 0.987 |

A reached N is conditional on the generator and is not a universal
recruitment target. A real package must rerun this route while blinded
using its event count, follow-up, censoring, missingness, source/treatment
structure, endpoint adjudication, and frozen analysis budget.
