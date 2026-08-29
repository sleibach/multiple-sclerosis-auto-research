# V57 V22 Measurement and Label Integrity Plan

Status: frozen before computation on 2026-08-29 UTC.

## Purpose and boundary

This audit asks how fragile the observed V22 discrimination is to plausible
score measurement error and outcome-label errors. It does not alter the locked
rule, estimate assay reliability, validate the rule, or provide biological
evidence. The held 19-subject score/outcome table is the fixed reference.

## Score measurement-error envelope

- reliability grid: `1.00, 0.95, 0.90, 0.80, 0.70, 0.60, 0.50`;
- seeds: `57001, 57002, 57003`;
- `50,000` independent perturbations per reliability, seed, and mode;
- modes:
  - `global`: Gaussian error variance is `var(score) * (1-r) / r`;
  - `cohort_scaled`: the same formula uses each cohort's observed score
    variance, retaining platform-scale heterogeneity;
- outcome labels and the locked score definition remain fixed;
- report the AUC median, 5th/95th percentiles, and probabilities of AUC
  `>0.50`, `>=0.60`, and `>=0.70` for every cell.

Predeclared practical reliability criterion: at reliability `>=0.80`, every
seed and both modes must have median AUC `>=0.70` and probability of AUC
`>=0.60` of at least `0.80`. This is an acquisition-quality sensitivity rule,
not a clinical threshold.

## Outcome-label integrity envelope

Enumerate every balance-preserving exchange between responder and
non-responder labels for `k=1,2,3` pairs. Report unrestricted exchanges and
the subset that preserves class counts within each cohort. For each `k`, report
the minimum, median, maximum, and fractions below AUC `0.60` and at or below
`0.50`.

Predeclared single-pair criterion: the observed result is adversarially
single-pair robust only if the minimum AUC after any one-pair exchange remains
`>=0.60`. This deliberately stringent check quantifies label-integrity
dependence; failure is not proof that any recorded label is wrong.

All generated perturbations are synthetic method stress tests. Aggregates and
configuration are committed; simulated rows are not biological observations.
