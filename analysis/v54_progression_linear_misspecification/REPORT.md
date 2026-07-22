# V54 Linear-Effect Misspecification Audit

Status: **FIXED_NONLINEAR_DIAGNOSTICS_ARE_NONRESCUING_MODEL_CHECKS**.

This is seeded synthetic method behavior only. It is not evidence that an MS
molecular state has a linear, threshold, saturated, U-shaped, or inverted-U
relationship with progression.

## Expected Diagnostic Comparisons

- `high_threshold`, n=180: linear `0.318`, expected diagnostic `0.194`, gain `-0.124`, materially missed `False`.
- `high_threshold`, n=320: linear `0.488`, expected diagnostic `0.353`, gain `-0.135`, materially missed `False`.
- `monotone_saturation`, n=180: linear `0.687`, expected diagnostic `0.543`, gain `-0.144`, materially missed `False`.
- `monotone_saturation`, n=320: linear `0.909`, expected diagnostic `0.828`, gain `-0.081`, materially missed `False`.
- `u_shaped_crossing`, n=180: linear `0.105`, expected diagnostic `0.637`, gain `0.532`, materially missed `False`.
- `u_shaped_crossing`, n=320: linear `0.105`, expected diagnostic `0.891`, gain `0.786`, materially missed `True`.
- `inverted_u`, n=180: linear `0.026`, expected diagnostic `0.032`, gain `0.006`, materially missed `False`.
- `inverted_u`, n=320: linear `0.027`, expected diagnostic `0.191`, gain `0.164`, materially missed `False`.

The primary remains one linear coefficient. The fixed threshold, saturated,
and linear-quadratic tests are multiplicity-controlled diagnostics. They can
flag a model class for a future, separately pre-registered study; they cannot
replace a failed primary model after outcomes are inspected.

## Calibration

All 5 method families are assessed under their fixed alpha;
`0` are invalid and
`0` have strict-cell but
family-compatible flags. Flagged families are excluded from any positive
performance claim.

## Boundary

The audit quantifies model behavior under fixed synthetic shapes. Even a clean
diagnostic advantage does not establish that shape in MS, validate a molecular
score, or identify a way to halt progression.
