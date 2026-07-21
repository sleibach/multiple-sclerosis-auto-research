# V54 Progression-Event Label-Noise Sensitivity

All cohorts are seeded synthetic method-design data, not MS evidence.

The sensitivity adds 576,000 cohorts at 5% and 10% symmetric outcome-label noise while preserving every other default-grid parameter. Scenarios reaching the frozen 80% criterion fall from 7/24 at zero noise to 4/24 at 5% and 3/24 at 10%.

| event rate | OR | missing | repeats | n at 0% | n at 5% | n at 10% | power n=240: 0% / 5% / 10% |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.15 | 1.25 | 0.00 | 1 | not_reached | not_reached | not_reached | 0.167 / 0.136 / 0.107 |
| 0.15 | 1.25 | 0.00 | 2 | not_reached | not_reached | not_reached | 0.189 / 0.145 / 0.123 |
| 0.15 | 1.25 | 0.20 | 1 | not_reached | not_reached | not_reached | 0.139 / 0.091 / 0.075 |
| 0.15 | 1.25 | 0.20 | 2 | not_reached | not_reached | not_reached | 0.155 / 0.123 / 0.105 |
| 0.15 | 1.50 | 0.00 | 1 | not_reached | not_reached | not_reached | 0.445 / 0.345 / 0.262 |
| 0.15 | 1.50 | 0.00 | 2 | not_reached | not_reached | not_reached | 0.509 / 0.351 / 0.269 |
| 0.15 | 1.50 | 0.20 | 1 | not_reached | not_reached | not_reached | 0.357 / 0.253 / 0.192 |
| 0.15 | 1.50 | 0.20 | 2 | not_reached | not_reached | not_reached | 0.439 / 0.327 / 0.223 |
| 0.15 | 2.00 | 0.00 | 1 | 240 | not_reached | not_reached | 0.875 / 0.711 / 0.576 |
| 0.15 | 2.00 | 0.00 | 2 | 240 | not_reached | not_reached | 0.903 / 0.793 / 0.639 |
| 0.15 | 2.00 | 0.20 | 1 | not_reached | not_reached | not_reached | 0.759 / 0.602 / 0.451 |
| 0.15 | 2.00 | 0.20 | 2 | 240 | not_reached | not_reached | 0.834 / 0.663 / 0.516 |
| 0.30 | 1.25 | 0.00 | 1 | not_reached | not_reached | not_reached | 0.241 / 0.197 / 0.162 |
| 0.30 | 1.25 | 0.00 | 2 | not_reached | not_reached | not_reached | 0.283 / 0.235 / 0.180 |
| 0.30 | 1.25 | 0.20 | 1 | not_reached | not_reached | not_reached | 0.212 / 0.162 / 0.122 |
| 0.30 | 1.25 | 0.20 | 2 | not_reached | not_reached | not_reached | 0.254 / 0.195 / 0.164 |
| 0.30 | 1.50 | 0.00 | 1 | not_reached | not_reached | not_reached | 0.651 / 0.531 / 0.435 |
| 0.30 | 1.50 | 0.00 | 2 | not_reached | not_reached | not_reached | 0.723 / 0.605 / 0.504 |
| 0.30 | 1.50 | 0.20 | 1 | not_reached | not_reached | not_reached | 0.555 / 0.441 / 0.339 |
| 0.30 | 1.50 | 0.20 | 2 | not_reached | not_reached | not_reached | 0.608 / 0.532 / 0.444 |
| 0.30 | 2.00 | 0.00 | 1 | 160 | 240 | 240 | 0.970 / 0.931 / 0.845 |
| 0.30 | 2.00 | 0.00 | 2 | 120 | 160 | 240 | 0.975 / 0.957 / 0.893 |
| 0.30 | 2.00 | 0.20 | 1 | 160 | 240 | not_reached | 0.931 / 0.853 / 0.755 |
| 0.30 | 2.00 | 0.20 | 2 | 160 | 240 | 240 | 0.957 / 0.903 / 0.802 |

No OR 1.25 or 1.5 scenario reaches 80% by n=240 at any noise level. At 15% events, all OR 2.0 scenarios also fall below the criterion once 5% label noise is introduced. At 30% events and OR 2.0, 5% noise moves minimum N to 160-240; 10% noise leaves one 20%-missingness, one-repeat scenario below 80% even at n=240.

The practical pre-data implication is an adjudication requirement, not a biological claim: endpoint provenance and likely misclassification must be specified before a received cohort's blinded power calculation. These synthetic error rates are not estimates of real PIRA label quality.
