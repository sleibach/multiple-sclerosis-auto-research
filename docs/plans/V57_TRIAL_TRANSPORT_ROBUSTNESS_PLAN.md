# V57 Trial-Transport Robustness Audit: Frozen Plan

Status: **frozen before simulation outcomes**

## Reason

The primary V57 trial-transport harness failed. Its follow-up showed that the
absolute maximum-weight criterion becomes more likely to fail as the sample
grows even when effective sample size and weighted balance improve. That
failure remains recorded. This separate candidate audit asks whether a
scale-stable overlap diagnostic and nuisance-specification sensitivity can
produce a technically defensible future method.

All data in this audit are seeded and synthetic. No result is evidence about
MS, a treatment, or a real trial.

## Candidate Diagnostics

Fit both linear and linear-plus-quadratic sampling and outcome models. The
candidate primary overlap diagnostic uses quadratic sampling weights and
requires all of:

- effective sample size at least 30% of source `n`;
- 99th-percentile weight divided by median weight no greater than 12; and
- maximum weighted standardized difference across first and squared
  covariate moments no greater than 0.10.

This replaces a sample maximum with stable distributional summaries. It is a
candidate for future plans only and does not retroactively alter the primary
V57 gate.

## Six Scenarios

Use 2,400 source and 2,400 target participants, 150 replicates per scenario,
and seeds 57101, 57102, and 57103:

1. linear sampling and linear outcome models are correct;
2. sampling is nonlinear but the linear outcome model is correct;
3. sampling is linear but the outcome model is nonlinear;
4. both linear nuisance models are wrong, while quadratic models are correct;
5. an unmeasured target-only treatment modifier violates transportability;
6. target support is largely absent.

## Frozen Gates

Every seed must satisfy:

- scenarios 1-4: candidate overlap pass rate at least 90%;
- scenario 1: mean absolute error no greater than 0.03 for both linear and
  quadratic doubly robust estimators;
- scenarios 2-3: linear doubly robust mean absolute error no greater than
  0.03, testing one-correct-nuisance robustness;
- scenario 4: quadratic doubly robust mean absolute error no greater than
  0.03 and at least 25% relative improvement over the linear estimator;
- scenario 5: among overlap-eligible pairs, at least 80% have absolute
  quadratic-transport versus target-randomized discrepancy above 0.08; and
- scenario 6: at least 90% fail the overlap diagnostic.

The harness is verified only if every gate passes under every seed. A pass
would justify a controlled-data analysis contract, not a real causal claim.
