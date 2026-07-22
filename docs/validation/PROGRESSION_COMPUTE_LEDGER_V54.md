# V54 Progression Compute Ledger

Status: **complete; unlike computational units are intentionally not summed**.

This ledger reads committed V54 summary artifacts. It separates unique
model-fit synthetic cohorts, lightweight enrollment-planning Monte Carlo
draws, repeated route evaluations, held-data randomization draws, and gate
fixtures. None is patient evidence, and a larger count is not a stronger
biological result.

| category | count rows | total within category | interpretation |
|---|---:|---:|---|
| `analysis_route_evaluations` | 10 | 3,875,400 | Multiple methods/estimands applied to cohorts already counted elsewhere. |
| `held_data_randomization_replicates` | 9 | 2,700,000 | Permutation/wild-bootstrap null draws over held observations. |
| `model_fit_synthetic_cohorts` | 19 | 3,348,600 | Unique synthetic cohorts plus explicitly disjoint calibration cohorts; method behavior only. |
| `planning_monte_carlo_replicates` | 1 | 122,805,000 | Lightweight enrollment/loss/event draws; not fitted cohort analyses. |
| `synthetic_gate_fixtures` | 18 | 187 | Software decision fixtures, not cohorts. |

A grand total is deliberately undefined because summing these units
would double-count route reuse and conflate lightweight draws with
model fitting. Row-level provenance is in
`analysis/v54_progression_compute_ledger/compute_ledger.tsv`.

## Rebuild

```bash
.venv/bin/python scripts/v54_progression_compute_ledger.py
```
