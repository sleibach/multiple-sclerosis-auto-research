# V54 Progression-Power Calibration And Label-Noise Sensitivity

Status: frozen after the two-lineage critique and before the additional
simulation runs. All results are synthetic method behavior, never MS evidence.

## Questions

1. Is the observed maximum null pass rate of `0.060` evidence that the frozen
   logistic Wald design is anti-conservative, or expected finite-simulation
   variation across many null cells?
2. How do symmetric 5% and 10% outcome-label error interact with 0% and 20%
   molecular missingness in the existing assumption grid?

## Frozen Calibration Audit

Use the committed default grid only. Report null-cell unconditional pass-rate
quantiles at 50%, 90%, 95%, 99%, and maximum, both aggregate (1,500 cohorts per
cell) and by seed (500 per cell). Also report pass rate conditional on a valid
fit. For the maximum aggregate cell, report its Wilson 95% interval and the
family-maximum tail probability under 48 independent `Binomial(1500, 0.05)`
cells. Independence is a reference calibration, not a claim that every design
cell has identical finite-sample behavior.

Calibration is acceptable if no aggregate cell's Wilson lower bound exceeds
0.05 and the observed maximum is not unusual under the 48-cell reference
(`p>=0.05`). Otherwise the design is labeled anti-conservative and cannot be
used without correction.

## Frozen Label-Noise Runs

Rerun the exact default 192-cell grid twice, changing only symmetric binary
outcome-label noise to `0.05` and `0.10`. Preserve:

- sample sizes `40,60,80,120,160,240`;
- event rates `0.15,0.30`;
- OR assumptions `1.0,1.25,1.5,2.0` per latent SD;
- missingness `0.0,0.20`;
- one and two molecular repeats;
- reliability `0.70` per repeat;
- alpha `0.05`;
- three seeds and 500 cohorts per seed/cell.

This adds 576,000 clearly labeled synthetic cohorts. Compare each noisy cell
with the matched no-noise cell, emphasizing n=240 and the minimum-N table.

## Interpretation Boundary

Symmetric label flips are an assumption sensitivity, not an estimate of PIRA
or disability-adjudication error. The GSE279972 lesion context cannot supply an
empirical progression-event variance or label-error model, so the request to
derive such parameters from it is semantically invalid. A received cohort must
provide its endpoint definition, adjudication process, missingness, event rate,
and repeat structure before the blinded design simulation is parameterized.

