# V57 Trial-to-Trial Transport Method Verification

## Synthetic-Only Boundary

Every result here comes from seeded synthetic trials. This characterizes a
method and is not biological or treatment evidence about MS.

## Scale

- Synthetic trial pairs: 2,250
- Seeds: 57061, 57062, 57063
- Source/target participants per pair: 800/800

## Gates

| Gate | Passed across all seeds |
|---|---|
| Covariate shift recovered with adequate overlap | False |
| Hidden target modifier produces detectable incompatibility | True |
| Positivity failure is rejected | True |

Verdict: **TRIAL_TRANSPORT_HARNESS_NOT_VERIFIED**.

If verified, this method is worth applying only inside an approved controlled
environment holding harmonized source and target randomized trial IPD. It can
test whether measured population composition accounts for a trial difference;
it cannot prove exchangeability, repair endpoint mismatch, or infer an MS
effect from synthetic data.
