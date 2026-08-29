# V57 Mechanism-Boundary Selective-Inference Plan

Status: frozen before computation on 2026-08-29 UTC.

## Question

Would the observed bounded-pair AUC remain unusual if any favorable pair among
the four held treatment environments could have been selected after viewing
outcomes?

This is a deliberately adverse selection audit. It does not assert that V23's
mechanism boundary was outcome-selected; it quantifies the strongest version
of that vulnerability using the exact held cohort family.

## Frozen analysis

- Cohorts and patient rows are exactly those in the V57 environment audit.
- Selected pair: `GSE235357` plus `GSE253006_TOF_exact`.
- Primary candidate family: all six two-cohort subsets.
- Sensitivity family: every subset of size 2-4 (11 subsets).
- Primary estimand: pooled raw locked-score AUC, matching the bounded analysis.
- Scale sensitivity: pooled within-cohort score-percentile AUC.
- Null: permute labels independently within each cohort, preserving every
  cohort's sample size and outcome count.
- `200,000` permutations for each seed `57101, 57102, 57103`.
- In every permutation record the selected-pair statistic, the maximum across
  all six pairs, and the maximum across all 11 subsets.

The boundary is selection-robust only if the max-six-pair p-value is <=0.05 in
every seed for both raw and percentile estimands. Failure does not refute the
mechanistic rationale; it means held outcomes cannot distinguish that rationale
from favorable subset selection and external preregistered validation remains
necessary.

Only aggregate cohort-combination results are committed. No participant-level
permutation or label output is persisted.
