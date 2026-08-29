# V57 Cross-Environment Partial-Conjunction Plan

Status: frozen before computation on 2026-08-29 UTC.

## Question

Does the immutable V22 score have evidence for a responder-higher association
in at least two of the four already-audited held environments, rather than only
a favorable pooled average or one strong cohort?

The method is partial-conjunction testing as introduced by Benjamini and Heller
(2008, Biometrics 64:1215-1222, DOI
`10.1111/j.1541-0420.2007.00984.x`). It is new to this repository. The input is
the four exact one-sided within-cohort AUC permutation p-values committed by the
V57 environment-stability probe. No cohort, direction, or endpoint is selected
after reading this analysis.

## Frozen tests

- Primary claim: association in at least `r=2` of `m=4` environments.
- Primary p-value: dependence-valid Bonferroni partial conjunction,
  `min(1, (m-r+1) * p_(r))`, where `p_(r)` is the r-th ordered exact p-value.
- Sensitivity: Fisher combination of the largest `m-r+1` p-values, valid under
  independence of the non-overlapping cohorts.
- Report both methods for `r=1,2,3,4`; `alpha=0.05`.
- A transport-replicability claim requires the primary `r=2` p-value <= 0.05
  and responder-higher observed AUC in at least two cohorts.

The four cohorts differ in disease and therapy context. Passing would support
cross-environment recurrence, not external MS validation or a clinical claim.
Failure means current held data cannot establish recurrence in two
environments; it does not prove absence.
