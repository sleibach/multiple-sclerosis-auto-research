# CONVERGENCE_CHECK_V23_01

Timestamp: 2026-06-06 14:31 CEST

## Actions Completed

- Action 1 pooled the small cohorts.
- Action 2 characterized therapy-mechanism specificity.
- Action 3 resolved the GSE253006 tofacitinib module-approximation problem by
  exact raw 10x rescoring.
- Action 4 regenerated marker-derived compartments for GSE253006 exact-module
  testing.
- Action 5 sharpened clinical utility as early monitoring only.
- Action 6 decided not to lock a V23 successor rule without fresh held-out
  data.

## Convergence

The unbounded rule diverges:

- primary locked pooled AUC is only `0.547`.
- fingolimod and psoriasis adalimumab fail.

The bounded immune-remodeling/JAK-STAT monitor converges:

- MS dimethyl fumarate passes.
- exact UC tofacitinib passes all-cell and across multiple marker-derived
  compartments.
- pooled bounded set AUC is `0.811`, despite small n.

## Main Caveat

The bounded result is still underpowered and partly cross-disease. It is not
yet an MS clinical rule. The next decisive test is a larger paired MS DMT
cohort in a coherent immune-remodeling therapy class.

