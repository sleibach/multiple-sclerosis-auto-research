# POWER MAP V43

Status: synthetic method-characterization only. These simulations do not provide biological evidence about MS.

## Simulation Scale

- Synthetic cohorts: `9408`.
- Replicates per parameter cell: `12`.
- Bootstrap replicates per synthetic cohort: `300`.
- Parameter grid: n per response group `10,15,20,30,45,60,80`; true effect size `0,0.25,0.50,0.75,1.00,1.25,1.50`; label noise `0,0.10`; baseline SD `0.5,1.0`; confounder structures `none,immune_tone,composition,steroid`.
- Full synthetic subject-level data: purged from Git in V49
  (`analysis/v43_method_validation/synthetic/power_simulation_subjects.tsv.gz`)
  because it was a seeded, reproducible cache above the repository size ceiling.
  Regenerate it with `scripts/v43_method_validation_simulations.py` if
  subject-level synthetic rows are needed again.

## V49 Post-Purge Sufficiency Check

The subject-level power-simulation cache is intentionally absent after V49. The
method-characterization conclusions below remain backed by the committed
aggregate outputs:

- `analysis/v43_method_validation/power_simulation_cohort_results.tsv`: `9409`
  lines including header, matching `9408` synthetic cohorts.
- `analysis/v43_method_validation/power_map_summary.tsv`: `785` lines including
  header.
- `analysis/v43_method_validation/v43_method_validation_summary.json`: retained
  compact run summary with seed and headline rates.

This is sufficient to preserve the V43 power-map conclusions and audit trail.
It is not sufficient to re-run subject-level diagnostics without regenerating
the purged synthetic cache.

## Headline

- Null false-positive rate across all null cells: `0.016`.
- Gafson-small cells (`10-15` per group) mean conclusive rate: `0.578`.
- Minimum n for 80% pass probability at effect size 0.75, no label noise, no confounder: not reached up to 80 per group.
- Minimum n for 80% pass probability at effect size 1.00, no label noise, no confounder: 30 per group (pass_rate 0.92).
- Minimum n for 80% pass probability at effect size 0.75 with 10% label noise and immune-tone structure: not reached up to 80 per group.

Interpretation: a tiny Gafson-sized cohort can produce a useful effect estimate, but it is unlikely to settle the rule unless the true effect is large and labels are clean. A validation intended to settle the question should target at least the first n-per-group cell above, and preferably exceed it to preserve power under label noise/confounding.

## Machine-Readable Outputs

- `analysis/v43_method_validation/power_simulation_cohort_results.tsv`
- `analysis/v43_method_validation/power_map_summary.tsv`
