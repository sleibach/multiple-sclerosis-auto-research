# V57 Trial-to-Trial Transport Method Verification: Frozen Plan

Status: **frozen before simulation outcomes**

## Motivation and Boundary

An untested progression-research method is to transport a randomized effect
from one trial population into the covariate distribution of another trial,
then compare the transported estimate with the second randomized result. That
can distinguish population-composition explanations from residual phenotype-
specific effect heterogeneity when assumptions and overlap are adequate.

This V57 analysis uses seeded synthetic data only. It tests method behavior;
it is not evidence about any MS treatment, trial, subgroup, or mechanism.

## Synthetic Trials

Each replicate has 800 source-trial and 800 target-trial participants, four
baseline covariates, 1:1 randomized treatment, and a binary endpoint. Three
predeclared scenarios are generated:

1. `covariate_shift_only`: baseline distributions differ, while the full
   outcome and treatment-effect model is shared;
2. `hidden_target_modifier`: the target trial has an additional unmeasured
   phenotype-level treatment modifier unavailable to source standardization;
3. `positivity_failure`: the target covariate distribution lies largely
   outside source support.

The coefficients are fixed in committed code before outcomes are generated.

## Estimators

- Fit source-versus-target sampling odds from baseline covariates.
- Estimate the transported randomized effect by inverse-odds weighting.
- Fit a source outcome model with treatment-by-covariate interactions and
  standardize both treatment states over target covariates.
- Use an augmented/doubly robust estimate as the primary transported result.
- Compare it with the target trial's randomized risk difference only in the
  synthetic verification.

## Fail-Closed Overlap Gate

A replicate is overlap-eligible only when all hold:

- source sampling-weight effective sample size >= 30% of source n;
- maximum sampling weight <= 20; and
- maximum absolute source-versus-target weighted standardized mean difference
  <= 0.10.

No transported causal interpretation is allowed when overlap fails.

## Scale and Stability

- 250 replicates per scenario under each of seeds 57061, 57062, and 57063;
  2,250 synthetic trial pairs total.
- Every row and report is stored under
  `analysis/v57_trial_transport/synthetic/` and marked synthetic.

## Method-Behavior Gates

- Covariate shift: overlap passes in >= 90% of replicates and absolute mean
  doubly robust error is <= 0.03.
- Hidden modifier: among overlap-eligible replicates, >= 80% show absolute
  transported-versus-target-randomized discrepancy > 0.08.
- Positivity failure: the overlap gate rejects >= 90% of replicates.
- All three seed-specific summaries must retain the same pass/fail verdict.

Passing these gates makes a controlled-data trial-transport analysis
technically worth pursuing. It does not show that the needed exchangeability
assumption holds in real progression trials.
