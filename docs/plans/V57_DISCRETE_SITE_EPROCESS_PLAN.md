# V57 Discrete Small-Site E-Process Calibration Plan

Status: **frozen before simulation outcomes**

## Purpose and Boundary

The V57 federated accumulator was calibrated with continuous beta-distributed
p-values. Future V22 sites instead contribute a finite-sample, one-sided AUC
permutation p-value. This probe tests whether the unchanged mixture e-process
retains optional-stopping calibration and useful power when site p-values are
discrete and small-sample.

This is seeded synthetic method characterization. It is not MS evidence and it
does not add any cohort to the evidence accumulator.

## Fixed Design

- independent site arrivals: 12;
- responder/non-responder counts, cycled in order:
  `(4,5)`, `(5,5)`, `(6,6)`, `(7,7)`, `(8,8)`, `(10,10)`;
- standardized score effects: `0.0`, `0.5`, and `0.9`;
- seeds: `57121`, `57122`, `57123`;
- sequences per seed/effect/p-value mode: `100,000`;
- p-value modes:
  1. exact one-sided tie-free Mann-Whitney tail;
  2. the frozen V42 approximation `(1 + Binomial(10000, p_exact)) / 10001`;
- unchanged calibrators: `k * p^(k - 1)` for
  `k in {0.25, 0.50, 0.75}`;
- unchanged mixture boundary: `20`.

The exact null rank-sum distribution is computed combinatorially for every
class split. Alternative scores are generated from independent unit-variance
normal distributions with the fixed standardized mean difference. Individual
synthetic sequences are not stored.

## Method-Behavior Gate

The operational extension passes only if, in both p-value modes and every
seed:

1. null probability of ever crossing by arrival 12 is at most `0.055`;
2. mean one-step e-factor under the null is at most `1.01` at every site
   design; and
3. effect `0.9` crosses by arrival 12 in at least `0.80` of sequences.

Effect `0.5` is descriptive. Failure does not permit changing the calibrator,
threshold, arrival count, p-value method, or effect grid in this run. Future
use still requires independent sites, the identical frozen estimand and
harness, locked-positive direction, and valid site-level p-values.
