# V57 Hierarchical Environment Model: Frozen Plan

Status: **frozen before outcome analysis**

## Question

Does a normal-normal cohort hierarchy predict an unseen environment better
than a no-heterogeneity model for the already frozen V22 score association?

This tests method utility, not a new biomarker or biological mechanism.

## Data and Effect

- Four audited held cohorts from the V57 environment-stability probe.
- One Hedges-g score/response effect and its sampling variance per cohort.
- No gene, module, threshold, sign, or cohort is selected from outcomes.

## Model

For cohort `e`:

```text
observed_g[e] ~ Normal(theta[e], sampling_variance[e])
theta[e] ~ Normal(mu, tau^2)
mu ~ Normal(0, mu_sd^2)
tau ~ HalfNormal(tau_scale)
```

The posterior is evaluated by deterministic integration over `tau` from 0 to
3. Leave one complete cohort out, fit on the other three, and score the held
effect under the posterior predictive distribution.

## Comparator and Primary Estimand

The comparator is the same model fixed at `tau=0`. The primary estimand is
the sum of leave-one-cohort-out log predictive-density differences:

`hierarchical log score - tau=0 log score`.

Positive values favor partial pooling with heterogeneity.

## Prior Sensitivity

Evaluate all 12 combinations:

- `mu_sd`: 0.5, 1.0, 2.0;
- `tau_scale`: 0.25, 0.5, 1.0, 2.0.

The reference prior is `mu_sd=1.0`, `tau_scale=0.5`; it is not selected from
the result.

## Null

Generate 20,000 within-cohort response-label permutations preserving each
cohort's response count, seed 57051. Recompute Hedges g and its variance, then
repeat the reference-prior leave-one-cohort comparison. The one-sided null
p-value asks how often an apparent hierarchical predictive gain at least as
large occurs without a score/response relationship.

## Promotion Gate

Recommend a dedicated hierarchical transport study only if:

1. every one of the 12 prior settings improves total LOO log score by at
   least 2.0;
2. the reference-prior gain has permutation p <= 0.05; and
3. no held-out cohort has a reference-prior predictive deficit worse than
   -1.0 log unit relative to `tau=0`.

Otherwise the method is not ready on the current four-environment evidence.
