# V54 Progression-Power Null Calibration Audit

All values characterize synthetic method behavior, not MS biology.

Verdict: **CALIBRATION_ACCEPTABLE**.

Across 48 aggregate null cells, the median false-pass rate was `0.043` and the maximum was `0.060` (90/1,500; Wilson 95% CI `0.049` to `0.073`). No cell's lower Wilson bound exceeded nominal 0.05.

Under a 48-cell Binomial(1500, 0.05) reference, a maximum at least this large has probability `0.895`. The observed maximum is therefore expected finite-grid variation, not evidence of anti-conservatism.

| quantile | aggregate unconditional | aggregate conditional-valid | seed unconditional | seed conditional-valid |
|---:|---:|---:|---:|---:|
| 0.50 | 0.043 | 0.043 | 0.042 | 0.043 |
| 0.90 | 0.053 | 0.053 | 0.056 | 0.056 |
| 0.95 | 0.053 | 0.053 | 0.060 | 0.060 |
| 0.99 | 0.058 | 0.058 | 0.065 | 0.065 |
| 1.00 | 0.060 | 0.060 | 0.068 | 0.068 |

The reference maximum assumes identically calibrated independent cells and is used only to contextualize Monte Carlo maxima. The per-cell Wilson gate is the fail-closed check. No alpha correction is required by this audit.
