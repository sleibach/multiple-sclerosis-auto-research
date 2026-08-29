# V57 Prospective Balanced-Batch Design Plan

## Question

Can prospective constrained randomization reduce the response-correlated batch
risk identified in V43-V45, before any expression data are generated?

This is synthetic method characterization only. It does not alter the V22 rule,
the V42 preregistration, or the existing post-data V44 batch guard.

## Frozen design before simulation

- 60 synthetic patients, each with one baseline and one early-treatment sample.
- Six equal-capacity processing batches; both samples from a patient remain in
  the same batch.
- Three cohort structures: approximately independent covariates,
  site-response coupling, and an imbalanced rare-site setting.
- Three allocation methods:
  - capacity-constrained random allocation;
  - outcome-blind constrained allocation balancing site, sex, and age stratum;
  - outcome-aware constrained allocation adding the finalized response label.
- The outcome-aware layout is only an admissible prospective option when labels
  are finalized before laboratory processing and the laboratory remains blinded.
  It is not a post-data correction and cannot be used to exclude samples.
- Constrained layouts are selected from 5,000 seeded capacity-valid candidates.
- Method behavior is evaluated under 20,000 seeded synthetic technical-null
  replicates per scenario, allocation method, and seed. Technical batch-by-time
  effects and patient noise are generated independently of response.

## Metrics and gate

- Pair split rate must equal zero.
- Each batch must contain equal baseline and early sample counts.
- Report maximum standardized batch imbalance for response and design
  covariates.
- Report the synthetic technical-null frequency of raw AUC >= 0.70. This is a
  stress metric, not the frozen V42 pass criterion.
- The method-level gate passes only if outcome-aware constrained allocation
  reduces median response imbalance and does not increase pooled raw-AUC>=0.70
  frequency relative to capacity-constrained random allocation.
- The outcome-blind branch is reported separately and is not claimed to balance
  response unless its observed synthetic results show that indirectly.

## Interpretation boundary

Synthetic results describe prospective design behavior, not MS biology and not
validation evidence. A favorable result supports adding constrained laboratory
allocation to the specification of a future cohort; it does not rehabilitate or
validate the monitoring signal.
