# V54 Foamy Morphology-By-Lesion Heterogeneity Plan

Status: frozen before interaction coefficients were inspected.

## Trigger And Boundary

The frozen lesion-stratum transport test did not pass and showed a nominal
lysosomal direction difference between eligible lesion classes 2 and 3. This
follow-up tests the interaction directly rather than inferring heterogeneity
from different subgroup p-values.

The follow-up is triggered by the same data and is therefore a post-result
characterization, not independent confirmation. A passing interaction would
require replication before becoming a portable finding.

## Frozen Model

Use only lesion classes 2 and 3, which passed the pre-score transport
eligibility gate. For each fixed endpoint (OXPHOS and lysosomal unique state),
fit:

`endpoint ~ foamy + lesion_class_3 + foamy:lesion_class_3 + B/APC composition +
resident microglia identity + de-overlapped MIMS + other endpoint`

The interaction is class-3-minus-class-2 foamy-effect heterogeneity. It is
two-sided; no direction is pre-claimed.

Inference uses donor-clustered 95% confidence intervals, 300,000 donor-wild
residual sign-flip nulls over three fixed seeds under the no-interaction model,
maximum-statistic correction across both endpoints, and leave-one-donor
direction stability.

## Frozen Gate

An interaction is `POST_RESULT_HETEROGENEITY_SUPPORTED` only if:

1. the clustered confidence interval excludes zero;
2. donor-wild `p <= 0.05`;
3. two-endpoint max-family `p <= 0.10`; and
4. every estimable leave-one-donor interaction retains the observed sign.

Otherwise it is `HETEROGENEITY_NOT_SUPPORTED`. Non-passage does not establish
homogeneity or equivalence. Neither outcome is progression, flux, causal,
target, or treatment evidence.

