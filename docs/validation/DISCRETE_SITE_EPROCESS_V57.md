# V57 Discrete Small-Site E-Process Calibration

Status: **synthetic method verification; no MS evidence accumulated**

## Question

The federated V57 evidence rule was calibrated with idealized continuous
p-values. Real V22 validation sites are small and return a discrete one-sided
AUC permutation p-value. Does the unchanged e-process remain calibrated and
useful under that operational p-value mechanism?

## Frozen Test

The pre-outcome plan is
[`V57_DISCRETE_SITE_EPROCESS_PLAN.md`](../plans/V57_DISCRETE_SITE_EPROCESS_PLAN.md).
It cycles responder/non-responder splits from `4/5` through `10/10` over 12
independent arrivals. It tests both exact one-sided Mann-Whitney tails and the
V42 10,000-permutation plus-one approximation at standardized effects `0`,
`0.5`, and `0.9`.

Three seeds and 100,000 sequences per seed/effect/mode produced 1.8 million
synthetic sequences and 21.6 million synthetic site arrivals. Individual
synthetic sequences were not retained.

## Result

| Quantity | Frozen gate | Observed range | Outcome |
|---|---:|---:|---|
| Null ever-crossing by arrival 12 | `<=0.055` | `0.00325-0.00394` | pass |
| Maximum one-site null mean e-factor | `<=1.01` | `0.99141` | pass |
| Effect `0.9` crossing by arrival 12 | `>=0.80` | `0.96901-0.97043` | pass |

The moderate effect `0.5`, which was descriptive, crossed by arrival 12 in
`0.38070-0.38441` of sequences. The exact and V42 Monte Carlo modes were
closely aligned. Discreteness was conservative here rather than anti-
conservative.

Verdict: **`DISCRETE_SITE_EPROCESS_VERIFIED`** for the tested site-size and
tie-free score regimes.

## What This Changes

The same-estimand federated route no longer rests only on a continuous-p-value
calibration. It has a direct small-site calibration matching the V42 plus-one
permutation mechanism. No calibrator, threshold, or evidence direction was
changed.

## What This Does Not Establish

- No external cohort contributed evidence.
- Synthetic effect sizes are not estimates of an MS effect.
- The test assumes independent sites, continuous scores without ties, and
  valid one-sided permutation p-values.
- It does not establish that an author-run package used the right samples,
  labels, preprocessing, or independence group.
- It does not replace cohort effect sizes, confidence intervals, confounder
  diagnostics, transport checks, or the V42 interpretation grid.

Tied scores and response-correlated preprocessing require either exact
conditional randomization or a separately validated p-value mechanism before
combination.

## Reproduce

```bash
.venv/bin/python scripts/v57_discrete_site_eprocess_probe.py
```

Outputs are under `analysis/v57_discrete_site_eprocess/`.
