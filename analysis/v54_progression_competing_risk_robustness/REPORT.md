# V54 Progression Competing-Risk Robustness

All outputs are seeded synthetic method behavior, not biological evidence.

The audit generated 129,600 unique cohorts.

| mechanism | null cells | median | maximum | Wilson CI | max-tail | verdict |
|---|---:|---:|---:|---:|---:|---|
| independent | 12 | 0.051 | 0.063 | 0.051-0.079 | 0.243 | STRICT CELL FLAG; FAMILY-COMPATIBLE |
| joint_score_progression_risk | 12 | 0.067 | 0.119 | 0.102-0.139 | 0.000 | INVALID |
| none | 6 | 0.052 | 0.056 | 0.044-0.070 | 0.724 | calibrated |
| progression_risk_dependent | 12 | 0.050 | 0.057 | 0.045-0.071 | 0.877 | calibrated |
| score_dependent | 12 | 0.050 | 0.061 | 0.049-0.076 | 0.474 | calibrated |

Only mechanisms passing both frozen calibration criteria enter `calibrated_power_thresholds.tsv`. A mechanism may fail the strict single-cell Wilson rule while remaining compatible with the predeclared family-maximum reference; that is reported as inconclusive and excluded from power, not equated with directional invalidity. A competing event is not automatically bias, but joint dependence on molecular state and latent progression risk can invalidate ordinary death censoring.
