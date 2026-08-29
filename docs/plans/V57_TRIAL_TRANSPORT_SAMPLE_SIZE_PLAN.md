# V57 Trial-Transport Sample-Size Remediation: Frozen Follow-Up

Status: **frozen after the primary n=800 harness failed, before this grid**

## Reason for Follow-Up

The primary synthetic verification retained the hidden-modifier and positivity
gates but failed its covariate-shift gate because overlap passed in only
84.8%-88.0% of replicates and mean absolute error was 0.038-0.044. This
follow-up does not relax or reinterpret that failure.

## Fixed Grid

- Reuse the exact `covariate_shift_only` data-generating process, estimator,
  overlap thresholds, and seeds from the primary plan.
- Equal source and target sizes: 800, 1,200, 1,600, and 2,400.
- 200 replicates per size under each of seeds 57061, 57062, and 57063.
- 2,400 additional synthetic trial pairs total.

## Gate

At a candidate size, every seed must have:

- overlap pass rate >= 90%; and
- mean absolute doubly robust error <= 0.03 risk-difference units.

The smallest size passing both under all seeds is the method's synthetic
minimum for this scenario. If no size passes, the transport harness remains
unverified. This is method behavior only, never evidence about MS or a trial.
