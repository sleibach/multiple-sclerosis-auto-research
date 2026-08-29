# V57 V22 Successor Non-Superiority Plan

Status: frozen before computation on 2026-08-29 UTC.

## Question

Can the project exclude a practically meaningful predictive improvement from
the fixed-score V27/V28 successors, or has it only failed to detect one?

The distinction follows equivalence/non-inferiority logic: non-significance is
not evidence of practical equivalence. The fixed meaningful-improvement margin
is `candidate AUC - locked AUC >= +0.05`, inherited unchanged from the V27
successor gate. It is not selected for this audit.

## Frozen analysis

- Primary set: the 19-subject bounded immune-remodeling set.
- Sensitivity: all 43 primary plus exact-UC subjects.
- Candidates: receptor control, three V27 coupled scores, and the three V28
  adjacent dynamic scores. The V28 fitted ridge model is excluded because a
  valid bootstrap would require nested refitting and its predictions were not
  committed; fixed and fitted estimands are not mixed.
- Paired resampling: `200,000` bootstrap datasets per seed, sampling subjects
  with replacement within cohort-by-outcome strata so locked and candidate
  scores remain paired.
- Seeds: `57091, 57092, 57093`.
- For each candidate, estimate the one-sided 95% upper percentile bound on AUC
  difference.
- For family control, calculate the best candidate difference inside each
  bootstrap replicate and its one-sided 95% upper bound.

The family is demonstrably non-superior only if the family-maximum upper bound
is below `+0.05` in every seed. Otherwise the correct verdict is
`NO_OBSERVED_IMPROVEMENT_BUT_MEANINGFUL_GAIN_NOT_EXCLUDED`.

This is a reanalysis of held data, not validation, a successor search, or a
change to V22.
