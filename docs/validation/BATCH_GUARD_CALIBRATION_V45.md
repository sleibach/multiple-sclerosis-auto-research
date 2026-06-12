# V45 Batch Guard Calibration Pilot

## Status

Synthetic method-characterization only. This pilot does not change the frozen
V42/V44 validation harness or any interpretation threshold.

## Question

V45 multi-confounder stress testing showed that the existing V44 batch diagnostic
is highly specific but can over-flag planted signals when many technical fields
are audited. This pilot asks whether permutation/FDR-calibrated diagnostic flags
can recover sensitivity without allowing synthetic-null clean passes.

## Script And Outputs

Script:

- `scripts/v45_batch_guard_calibration.py`

Focused pilot command:

```bash
.venv/bin/python scripts/v45_batch_guard_calibration.py \
  --n-perm 50 \
  --scenarios independent_technical,batch_only,distributed_weak_technical \
  --max-replicates-per-cell 30
```

Outputs:

- `analysis/v45_batch_guard_calibration/summary.json`
- `analysis/v45_batch_guard_calibration/batch_guard_calibration_summary.tsv`
- `analysis/v45_batch_guard_calibration/batch_guard_calibrated_cohort_metrics.tsv`
- `analysis/v45_batch_guard_calibration/batch_guard_calibrated_feature_metrics.tsv`

Scale:

- `900` synthetic cohorts;
- `4,500` feature-level diagnostic tests;
- `50` permutations per feature-level response/correlation test;
- focused on the decision-critical scenarios:
  `independent_technical`, `batch_only`, and `distributed_weak_technical`.

## Result

| Metric | Existing V44 effect-only guard | Calibrated q<=0.10 | Calibrated q<=0.20 |
|---|---:|---:|---:|
| Worst synthetic-null acceptable pass | `0.0000` | `0.0000` | `0.0000` |
| Planted independent acceptable pass | `0.2333` | `0.9333` | `0.8667` |

Scenario-level behavior:

- synthetic-null batch-only and distributed-weak technical scenarios retained
  `0.0000` acceptable pass under q<=0.10;
- planted independent technical cohorts recovered from `0.2333` acceptable pass
  to `0.9333`;
- severe planted batch-only and distributed-technical scenarios remained mostly
  downgraded, as desired, because technical structure genuinely tracks the
  signal.

## Interpretation

Permutation/FDR calibration is promising as a way to reduce chance
over-flagging without weakening the false-positive guard. The q<=0.10 variant
looks better than q<=0.20 in this focused pilot because it recovers sensitivity
while preserving the null protection in the tested scenarios.

## Decision

No harness change is made from this pilot.

Before adopting a calibrated diagnostic, the project should:

1. optimize the implementation for full-grid runtime;
2. run all V45 multi-confounder scenarios;
3. vary seeds;
4. confirm worst synthetic-null acceptable pass remains <= `0.05`;
5. confirm planted technically clean acceptable pass improves reproducibly.

If those conditions hold, a future blind additive preregistration tightening can
replace the current effect-only diagnostic flag with a permutation/FDR-calibrated
diagnostic report. Until then, the current V44 guard remains the operative
pre-data diagnostic.

