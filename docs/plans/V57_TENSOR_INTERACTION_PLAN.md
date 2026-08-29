# V57 Donor-State-Module Tensor Probe: Frozen Plan

Status: **frozen before outcome analysis**

## Question and Boundary

Does a low-rank donor-by-cell-state-by-module representation predict held-out
treatment response better than an additive state/module representation?

The held paired data are anti-TNF IBD myeloid data. This is a method probe and
cross-disease context only. It cannot establish an MS treatment mechanism.

## Tensor

- Use the audited Wave67 paired major-state module deltas.
- Patient is the inferential unit; multiple tissue sites are collapsed by the
  median.
- Require complete data for both `DC` and `Mono_macro` across all 11 fixed
  Wave67 modules.
- Tensor dimensions are patient x 2 states x 11 modules.

## Models

Every patient is held out once. All centering, scaling, decomposition, and
regression fitting use the other patients only.

1. `additive`: grand mean, one state contrast, and ten module contrasts
   against the final fixed module; fixed ridge penalty 1.0.
2. `tensor_hosvd`: outcome-blind higher-order SVD of the training tensor,
   retaining both state factors and the first two module factors; the four
   patient core coordinates enter the same fixed ridge regression.

No rank or penalty is selected from response performance.

## Null and Multiplicity

- Primary metric: sample-size-weighted mean of within-disease AUCs, preventing
  Crohn's/ulcerative-colitis composition from driving prediction.
- Generate 200,000 disease-stratified patient-label permutations preserving
  response counts, seed 57071.
- Recompute both complete leave-one-patient-out predictors for every label
  permutation. Representations remain label-invariant; ridge fits change.
- Correct the tensor AUC against the maximum AUC of the two models.
- Separately null-test tensor-minus-additive AUC gain.

## Promotion Gate

The tensor method merits a dedicated run only if:

1. weighted AUC >= 0.65;
2. max-model permutation FWER p <= 0.05;
3. tensor-minus-additive AUC >= 0.05 with permutation p <= 0.05; and
4. tensor AUC is >0.5 within both diseases.

Otherwise multiway compression has not extracted a reproducible interaction
from this held tensor.
