# V57 V22 Gene-Influence Audit Plan

## Question

Is the bounded V22 cohort-pair association carried by one constituent gene, or
does it remain after every single frozen-module gene is omitted in turn?

This is a sensitivity audit of the immutable rule. The locked rule is not
changed, refit, or replaced, and no deletion score is a candidate rule.

## Frozen analysis

- Cohorts: the existing bounded pair `GSE235357` and
  `GSE253006_TOF_exact`; no fresh or quarantined data.
- Recompute cohort-wise gene z-scores with the original V22 expression loaders.
- Evaluate the original score plus deletion of each unique gene in the frozen
  IFN/APC and HLA-II modules. `HLA-DRA`, which belongs to both modules, is
  removed from both simultaneously.
- Preserve the locked therapy-class formula in each cohort.
- Primary pooled scale: outcome-blind within-cohort score percentiles, preventing
  cross-platform score-scale differences from determining pooled rank.
- Secondary: raw pooled AUC and cohort-specific AUCs.

## Null and decision gate

- Enumerate every response-label assignment preserving each cohort's sample
  size and responder count.
- For each assignment, calculate the minimum pooled percentile AUC across all
  leave-one-gene-out scores. The exact family p-value compares the observed
  weakest deletion to this intersection null.
- The no-single-gene-dominance gate requires all three:
  1. every deletion pooled percentile AUC is at least `0.70`;
  2. maximum AUC loss versus the intact score is at most `0.10`;
  3. the exact family minimum-AUC p-value is below `0.05`.

## Boundary

Passing would show feature-level robustness within the same bounded data, not
external replication, mechanistic specificity, or clinical validation. Failing
would expose dependence or insufficient precision and must not be hidden by
choosing a favorable deletion.
