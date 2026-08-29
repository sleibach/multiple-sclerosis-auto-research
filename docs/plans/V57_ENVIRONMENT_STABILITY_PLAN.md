# V57 Environment-Stability And Selective-Prediction Plan

Status: frozen before execution.

## Question

Does the immutable V22 signed score retain a directionally stable association
with response across the four held treatment environments, and can a
class-conditional uncertainty wrapper abstain honestly when one complete cohort
is held out?

This is a method probe around the existing score. It does not alter the score,
fit module coefficients, select genes, or validate a clinical biomarker.

## Inputs

Use each subject once:

1. `GSE235357` DMF in MS from
   `analysis/v22_locked_apc_hla_validation/paired_locked_scores_v22.tsv`.
2. `GSE250453` fingolimod in MS from the same file.
3. `GSE85034_ADA` adalimumab in psoriasis from
   `analysis/v22_locked_apc_hla_validation/paired_locked_scores_v22_cross_disease.tsv`.
4. `GSE253006_TOF_exact` tofacitinib in ulcerative colitis from
   `analysis/v23_apc_hla_monitoring/gse253006_exact_locked/gse253006_exact_paired_scores.tsv`.

The earlier approximate `GSE253006_TOF` row is excluded to prevent duplicate
use of the same subjects.

## Frozen Analyses

### Environment stability

- Primary direction is higher signed score in responders.
- Report per-cohort AUC, Hedges g, and an exact one-sided label-permutation p
  value preserving each cohort's responder count.
- Report the sample-size-weighted mean AUC, worst-cohort AUC, number of
  direction-consistent cohorts, and a stratified Monte Carlo permutation p
  value (`200,000` draws; seed `57001`).
- Report Cochran Q across Hedges-g effects as a descriptive heterogeneity test.
- The stringent stability gate requires all four cohort AUCs at least `0.55`,
  all four Hedges-g effects positive, weighted-AUC permutation p at most `0.05`,
  and heterogeneity p at least `0.10`.
- Failure means the association is not environment-stable in these held
  cohorts. Passing would justify a dedicated prospective transport study, not
  a causal claim.

### Leave-one-cohort-out class-conditional prediction sets

- Convert the score to an unlabeled within-cohort percentile rank. This leaves
  each cohort's score ordering unchanged and prevents therapy-class scale from
  dominating cross-cohort calibration.
- Hold out one entire cohort. Use all other cohorts as calibration data; fit no
  predictor.
- For candidate responder labels, nonconformity is negative score rank. For
  candidate nonresponder labels, nonconformity is positive score rank.
- Include candidate labels with conformal p value greater than primary
  `alpha=0.10`. Report `alpha=0.20` only as a predeclared sensitivity.
- Report empirical true-label coverage, singleton rate, singleton accuracy,
  empty-set rate, and both-label abstention rate by held-out cohort and pooled.
- Test pooled singleton correctness against `200,000` stratified held-out-label
  permutations preserving each cohort's class count.
- The wrapper is worth a dedicated validation run only if primary pooled
  coverage is at least `0.90`, no cohort coverage is below `0.80`, singleton
  rate is at least `0.20`, singleton accuracy is at least `0.70`, and its exact
  stratified permutation p is at most `0.05`.

Coverage guarantees require exchangeability; holding out whole cohorts is an
intentional stress test of that assumption. Empirical coverage here is method
behavior on four small environments, not a distribution-free guarantee for a
future MS cohort.

## Multiplicity And Interpretation

The environment-stability conjunction and the `alpha=0.10` prediction-set gate
are the two primary method questions. The `alpha=0.20` result is sensitivity
only. No gene, module, threshold, or cohort is selected from the results.
