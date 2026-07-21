# V54 Progression Visit-Schedule Robustness

All outputs are seeded synthetic method behavior, not biological evidence.

The audit generated 172,800 unique cohorts and 691,200 route evaluations.

| route | attendance | median null | maximum null | max-tail | verdict |
|---|---|---:|---:|---:|---|
| detected_visit_time | complete | 0.039 | 0.054 | 0.997 | calibrated |
| detected_visit_time | independent_20pct | 0.037 | 0.060 | 0.712 | calibrated |
| detected_visit_time | joint_score_progression_risk_20pct | 0.100 | 0.165 | 0.000 | INVALID |
| detected_visit_time | score_dependent_20pct | 0.067 | 0.158 | 0.000 | INVALID |
| midpoint_imputed_time | complete | 0.039 | 0.054 | 0.997 | calibrated |
| midpoint_imputed_time | independent_20pct | 0.040 | 0.062 | 0.522 | calibrated |
| midpoint_imputed_time | joint_score_progression_risk_20pct | 0.099 | 0.165 | 0.000 | INVALID |
| midpoint_imputed_time | score_dependent_20pct | 0.067 | 0.158 | 0.000 | INVALID |

Only observed route/attendance pairs passing the frozen strict calibration rule enter the power table. Oracles are diagnostics only. Sparse schedules and absent confirmation may lower ascertainment without creating type-I bias; informative attendance may instead invalidate the route. Neither is biological evidence.
