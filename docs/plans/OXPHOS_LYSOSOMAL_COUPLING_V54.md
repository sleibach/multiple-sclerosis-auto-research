# V54 OXPHOS-Lysosomal Foamy-State Coupling Sensitivity

Status: frozen after the second-panel result and before this sensitivity is
executed.

## Purpose And Boundary

GSE279972 showed a higher fixed lysosomal score and a lower frozen OXPHOS score
in foamy samples after lesion/state adjustment. This post-result sensitivity
asks whether each morphology coefficient persists when the other score is
entered as an additional covariate.

The analysis is confined to one foamy-morphology cohort. It cannot provide
progression, causal, flux, disability, target, or therapeutic-direction
evidence regardless of outcome.

## Frozen Models

Both models use the same 54 samples from 21 donors and adjust:

- deposited broad lesion class;
- B/APC composition;
- resident-microglia identity;
- de-overlapped MIMS state.

The two frozen endpoints are:

1. OXPHOS outcome, adding the fixed lysosomal score as a covariate;
2. lysosomal outcome, adding the frozen OXPHOS score as a covariate.

No genes overlap between the two scores. The unadjusted-for-each-other
coefficients must exactly reproduce their committed V54 source analyses before
the sensitivity is accepted.

## Inference

- donor-clustered 95% confidence intervals;
- three fixed seeds x 100,000 donor-wild residual sign flips under each null;
- max-endpoint family-wise control across both models;
- leave-one-donor direction stability;
- attenuation reported as the mutual-adjusted coefficient divided by the
  committed base coefficient.

An endpoint `survives` only if its mutual-adjusted CI excludes zero, donor-wild
p <= 0.05, max-endpoint p <= 0.10, and every leave-one-donor coefficient keeps
the observed direction. Persistence means only that the transcript associations
are separable under the tested model; it does not establish independent biology.
