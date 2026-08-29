# V57 V22 Specification-Curve Plan

Status: frozen before computation on 2026-08-29 UTC.

## Scope

This is a robustness audit of the immutable V22 score, not a rule change and
not an independent validation. It uses every already-frozen adjustment in the
V32 confounder audit: 23 single-confounder specifications and the three named
joint risk sets. No specification may be removed after results are read.

The specifications share subjects, outcome labels, and score values. Their
counts therefore describe sensitivity to analytical choices; they are not 26
independent confirmations and will not be meta-analysed as such.

## Frozen summaries

For each specification record:

1. adjusted AUC and stratified-permutation p-value;
2. confidence interval and attenuation from the raw locked-score AUC;
3. leave-one-out AUC for confounder(s) alone and locked score plus
   confounder(s);
4. incremental leave-one-out AUC from adding the locked score;
5. the original V32 verdict.

The aggregate audit uses these predeclared gates:

- **direction robust:** adjusted AUC > 0.50 in at least 90% of specifications;
- **practical-discrimination robust:** adjusted AUC >= 0.60 in at least 80%;
- **permutation-support robust:** p <= 0.05 in at least 80%;
- **incremental-CV robust:** locked-plus-confounder leave-one-out AUC exceeds
  confounder-only AUC in at least 80%;
- **fully robust:** all four aggregate gates pass.

Nominal p-values are reported as stress-test diagnostics. No multiplicity
claim is made because the question is robustness across prespecified
adjustments, not discovery among them. The least favorable specification and
the full range are mandatory outputs.
