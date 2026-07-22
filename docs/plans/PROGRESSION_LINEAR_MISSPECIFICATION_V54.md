# V54 Progression Linear-Effect Misspecification Plan

Status: frozen before simulation on 2026-07-22T00:40:26Z.

## Boundary

This seeded synthetic audit asks when one linear Cox score coefficient misses a
nonlinear risk shape. It tests method behavior only. It is not evidence that an
MS molecular state has any tested shape, and it changes no locked rule,
endpoint, or pre-registration.

## Fixed Generator

- sample sizes: `180` and `320`;
- administrative horizon: one normalized unit;
- cumulative event probability: `0.30` in every pattern after calibration;
- observed-score reliability: `0.70`, with 10% independent score missingness;
- patterns: null, linear (`HR 1.7` per latent SD), high-threshold (`HR 2.2`
  above latent z `0.674`), monotone saturation (`log(2.0)*tanh(1.5z)`),
  U-shaped crossing (`log(1.8)*(z^2-1)/sqrt(2)`), and its inverted-U sign;
- three fixed evaluation seeds and 3,000 cohorts per cell;
- three disjoint calibration seeds and 3,000 null cohorts per sample size.

## Frozen Tests

1. Primary: one standardized linear Cox score coefficient at alpha 0.05.
2. Fixed high-threshold diagnostic: observed standardized score above `0.674`.
3. Fixed saturated diagnostic: `tanh(1.5 * observed_z)`.
4. Fixed two-degree linear-plus-quadratic score-test omnibus.

The first asymptotic implementation was anti-conservative in four individual
method families, including the primary linear control. Before interpreting any
shape result, a disjoint seeded null bank was added. It fixes empirical p-value
cutoffs by sample size at alpha `0.05` for the primary, alpha `0.05/3` for each
individual diagnostic, and alpha `0.05` for the minimum p-value across all three
diagnostics. Evaluation seeds never contribute to those cutoffs.

`diagnostic_any` records whether the fixed minimum-p cutoff passes. The expected
diagnostic for each nonlinear generator is declared in advance: threshold for
high-threshold, saturated for saturation, and linear-quadratic for U/inverted-U.

A nonlinear pattern is classified as materially missed only if the primary
linear detection probability is below 0.50, the expected corrected diagnostic
is at least 0.80, and the expected diagnostic exceeds linear by at least 0.20 in
aggregate and every seed. Otherwise it is not called rescued.

Null families use the established strict-cell plus fixed-family-maximum rule.
Strict but family-compatible flags are reported and excluded. Diagnostics are
non-rescuing: they can establish a design warning and motivate a separately
pre-registered future model, but cannot replace a failed primary analysis after
outcome inspection.

Correction note: the empirical null bank is a method-calibration repair made
because the independent primary-null control failed before any nonlinear result
was accepted or committed. The failed asymptotic run is documented in the V54
queue; it is not used as evidence.

The first calibrated evaluation at 800 cohorts/seed remained Monte Carlo-
unstable (primary null seed rates 0.0688, 0.0488, and 0.0625 at `n=180`). The
evaluation was expanded to 3,000/seed with the disjoint bank and its thresholds
unchanged. This is a null-control precision increase, not shape selection.
