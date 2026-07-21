# V54 Progression Event-Time Assumption Robustness

All results are seeded synthetic method behavior, not biological evidence.

The audit generated 225,000 unique synthetic cohorts and 675,000 window evaluations.

## Whole-Follow-Up Null Calibration

| censoring mechanism | cells | median null | maximum null | Wilson CI | family max-tail | frozen verdict |
|---|---:|---:|---:|---:|---:|---|
| administrative_only | 6 | 0.051 | 0.057 | 0.047-0.070 | 0.497 | calibrated |
| event_risk_dependent | 6 | 0.039 | 0.053 | 0.043-0.066 | 0.875 | calibrated |
| independent | 6 | 0.048 | 0.056 | 0.045-0.069 | 0.641 | calibrated |
| joint_score_event_risk | 6 | 0.544 | 0.795 | 0.774-0.815 | 0.000 | INVALID |
| score_dependent | 6 | 0.053 | 0.057 | 0.047-0.070 | 0.497 | calibrated |

## Boundary

Only censoring families passing the frozen null rule are eligible for power interpretation. Early and late windows are diagnostics, not post-hoc replacement analyses. A whole-follow-up null under a crossing effect cannot establish absence when the window diagnostics recover opposite signs.

See `nph_diagnostic_snapshot.tsv` for the fixed n=320, pre-censoring event-probability 0.30 comparison.
