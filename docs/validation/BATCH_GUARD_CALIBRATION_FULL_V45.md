# Full-Grid Batch Guard Calibration V45

Status: synthetic method-characterization only. This does not change the frozen
V42/V44 validation harness, locked V22 rule, or interpretation thresholds.

## Purpose

The V45 focused calibration pilot suggested that permutation/FDR calibration
might reduce chance over-flagging while preserving synthetic-null protection.
This run asks whether that result holds across the full V45 multi-confounder
scenario grid.

## Method

Script:

- `scripts/v45_batch_guard_calibration.py`

Command:

```bash
.venv/bin/python scripts/v45_batch_guard_calibration.py \
  --n-perm 30 \
  --max-replicates-per-cell 40 \
  --outdir analysis/v45_batch_guard_calibration_full
```

Scale:

- all V45 multi-confounder scenarios;
- `2,800` synthetic cohorts;
- `14,000` feature-level diagnostic tests;
- `30` permutations per feature-level response/correlation test;
- output directory: `analysis/v45_batch_guard_calibration_full/`.

## Results

| Metric | Existing effect-only guard | Calibrated q<=0.10 | Calibrated q<=0.20 |
|---|---:|---:|---:|
| Worst synthetic-null acceptable pass | `0.025` | `0.400` | `0.125` |
| Planted independent acceptable pass | `0.300` | `0.950` | `0.950` |

The calibration recovered technically clean planted synthetic cohorts, but it
failed the false-positive gate on the full scenario grid.

Worst q<=0.10 synthetic-null cells:

| Scenario | Severity | Primary pass | Existing acceptable | q<=0.10 acceptable | q<=0.20 acceptable |
|---|---:|---:|---:|---:|---:|
| immune_tone_plus_batch | `1.00` | `0.475` | `0.025` | `0.400` | `0.125` |
| normalization_plus_depth | `1.00` | `0.825` | `0.000` | `0.250` | `0.000` |
| immune_tone_plus_batch | `0.75` | `0.175` | `0.000` | `0.175` | `0.100` |

## Verdict

The permutation/FDR-calibrated batch guard is **rejected as a replacement** for
the current V44 effect-threshold guard.

Reason: the full-grid run shows that the calibrated guard lets severe
immune-tone-plus-batch synthetic nulls pass as acceptable at rates up to
`0.400` for q<=0.10 and `0.125` for q<=0.20. That violates the V45 false-positive
gate. The focused pilot was informative but too narrow.

Current operational decision:

1. Keep the existing stricter V44/V45 effect-threshold batch guard as the
   primary pre-data diagnostic.
2. Do not adopt q-calibrated batch flags for validation pass/fail decisions.
3. If a future real cohort has a raw pass but marginal technical flags, report
   the calibrated diagnostic only as sensitivity context; it cannot rescue a
   technically non-specific result.
4. For future method work, any better calibration must be tested specifically
   against immune-tone-plus-batch and normalization-depth nulls before it is
   considered.

## Outputs

- `analysis/v45_batch_guard_calibration_full/summary.json`
- `analysis/v45_batch_guard_calibration_full/batch_guard_calibration_summary.tsv`
- `analysis/v45_batch_guard_calibration_full/batch_guard_calibrated_cohort_metrics.tsv`
- `analysis/v45_batch_guard_calibration_full/batch_guard_calibrated_feature_metrics.tsv`

