# V57 Trial-Transport Sample-Size Remediation

## Synthetic-Only Boundary

This follow-up holds the failed primary gate fixed and varies only synthetic
trial size. It is not MS or treatment evidence.

## Result

- Synthetic trial pairs: 2,400
- Sizes per source and target trial: 800, 1200, 1600, 2400
- Seeds: 57061, 57062, 57063
- Smallest size passing the unchanged gate under every seed:
  none

Verdict: **TRANSPORT_REMAINS_UNVERIFIED**.

At n=2400 per trial, mean absolute error cleared 0.03 under every
seed, but the absolute maximum-weight component failed in
21.5%-29.0%
of replicates while weighted-SMD failure was
0.0%-0.5%.
The unchanged primary guard is therefore not rescued: its sample-maximum
criterion becomes more likely to encounter an extreme observation as n grows.

Even a synthetic pass establishes only that the estimator can behave as
designed under known models. Real trial transport must fail closed for poor
overlap, endpoint mismatch, or unjustified source-to-target exchangeability.
