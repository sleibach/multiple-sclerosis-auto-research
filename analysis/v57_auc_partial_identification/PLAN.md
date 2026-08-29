# V57 AUC Partial-Identification Plan

Status: frozen before computation on 2026-08-29 UTC.

## Question

If a returned validation package contains locked V22 scores but one or more
clinical outcome labels cannot be linked, what AUC values remain logically
possible without pretending the labels are missing at random?

This follows the partial-identification principle described by Manski (2005,
International Journal of Approximate Reasoning 39:151-165, DOI
`10.1016/j.ijar.2004.10.006`): report the set allowed by observed information
rather than point-impute under an unsupported missingness assumption.

## Frozen probe

- Fixed reference: the 19 governed V32 subjects, immutable locked score, and
  observed complete-data AUC.
- For every possible missing-label subset of size `m=1,2,3,4,5`, enumerate all
  binary completions and calculate the sharp minimum and maximum AUC.
- Mode A, `no_prevalence_information`: any completion retaining both classes.
- Mode B, `known_total_responder_count`: completions must preserve a separately
  known cohort-wide responder total. This is only valid when that total comes
  from an audited external count, not inferred from unlinked rows.
- Commit aggregate bounds by `m`; do not persist participant-level missingness
  configurations.

## Frozen decision summary

For each mode and `m`, report the worst lower bound, median lower bound, median
width, and fraction of missingness patterns whose sharp lower bound remains at
least `0.60`. Define the maximum universally tolerable missing-label count as
the largest consecutive `m` from zero for which **every** pattern has lower
bound `>=0.60`.

This is method behavior around the observed score distribution, not validation,
not evidence that labels will be missing, and not permission to analyze a
partial package as if complete.
