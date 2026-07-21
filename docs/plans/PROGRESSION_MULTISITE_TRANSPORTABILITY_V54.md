# V54 Progression Multi-Site Transportability Plan

Status: frozen before simulation on 2026-07-21T23:54:43Z.

## Boundary

This seeded synthetic audit asks when a multi-site progression association is
transportable rather than a pooled site artifact. It is method behavior only,
not an empirical estimate of site heterogeneity, disability progression, or a
molecular effect in MS. It does not change any locked rule or pre-registration.

## Fixed Generator

Each cohort has three sites with baseline hazard multipliers `0.6, 1.0, 1.8`.
Total sample size is `180, 300, 450`, allocated either equally or in proportions
`0.6, 0.3, 0.1`. Cumulative event probability is `0.15` or `0.30`. The observed
molecular score has reliability 0.70 and 10% independent missingness.

Two site/score structures are fixed:

1. `balanced_score`: latent score mean zero at every site;
2. `hazard_aligned_score`: site means `-0.8, 0.0, 0.8`, deliberately aligning
   score with the ordered site baseline hazards so unstratified pooling is
   confounded under the null.

Four molecular-effect patterns are fixed across the three sites:

| pattern | site HRs per latent SD | purpose |
|---|---|---|
| null | 1.0, 1.0, 1.0 | type-I calibration |
| homogeneous | 1.7, 1.7, 1.7 | truly transportable association |
| one_site_only | 1.7, 1.0, 1.0 | context-specific association |
| one_site_reversed | 1.7, 1.7, 0.6 | adverse directional heterogeneity |

Independent progression frailty is included. Event times are proportional
exponential over a unit horizon. Three fixed seeds and 400 replicates per cell
are used.

## Frozen Analyses

For each replicate run:

1. a pooled unstratified Cox score test, retained as an artifact diagnostic;
2. a site-stratified Cox score test, the only global route eligible for
   interpretation;
3. three site-specific score/information estimates;
4. three leave-one-site-out fixed-effect score tests;
5. a score-test one-step Cochran-style heterogeneity statistic with two degrees
   of freedom.

The implementation must pass independent `statsmodels.PHReg` references for
pooled and site-stratified score/Hessian calculations. Report site event counts,
signed site estimates, leave-site-out results, heterogeneity, and three-seed
rates.

## Frozen Decisions

- Null calibration uses the Wilson-lower-bound plus fixed-family maximum rule.
  A pooled route that fails under hazard-aligned score is an expected site-
  confounding failure, not a biological result.
- A homogeneous effect is **transport-supported** in a replicate only if the
  site-stratified global test is positive at alpha 0.05, every site estimate is
  positive, every leave-one-site-out test is positive at alpha 0.05, no site
  has fewer than 10 events, and heterogeneity p is at least 0.05.
- `one_site_only` and `one_site_reversed` are negative controls for the
  transport gate. Their transport-pass rate is false transport, even if the
  pooled global test is significant.
- A design is ready only if homogeneous transport-pass probability is at least
  0.80 in aggregate and 0.75 in every seed, while both heterogeneous patterns
  have false-transport probability at most 0.05.
- No site is dropped, merged, or relabeled after seeing results. A future
  cohort must predeclare sites/batches and pass leave-site-out checks; pooling
  cannot substitute for transport.

Every artifact must state that it contains synthetic method behavior only.
