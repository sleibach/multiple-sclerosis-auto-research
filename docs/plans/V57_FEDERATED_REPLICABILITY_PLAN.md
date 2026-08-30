# V57 Federated Replicability Gate Plan

Status: frozen before synthetic execution. Method characterization only.

## Problem

The anytime-valid mixture e-process tests whether the same-estimand global null
can be rejected. One exceptional independent site can cross that boundary. It
does not establish that the effect recurs in two or more sites.

## Frozen Estimand And Gate

- Input: a complete, predeclared family of `m = 4` distinct site records for
  the immutable V22 early-delta/NEDA-4 estimand.
- Replicability claim: effects in at least `r = 2` distinct evidence units.
- Alpha: `0.05`, evaluated once after all four records arrive.
- Test: Bonferroni partial-conjunction p-value
  `min(1, (m-r+1) * p_(r))`, where `p_(r)` is the r-th ordered valid one-sided
  site p-value.
- Pass: the partial-conjunction p-value is at most `0.05` and every record
  passes the existing estimand, harness, direction, uncertainty, and distinct
  evidence-unit checks.
- No interim replication claim, adaptive family size, site dropping, or choice
  among values of `r` is allowed.

The union-bound construction controls the partial-conjunction null without
requiring statistical independence among valid true-null p-values. It still
requires genuinely distinct biological evidence units: hidden participant,
center, biobank, source-study, or preprocessing overlap invalidates the
replication interpretation.

## Frozen Synthetic Fixtures

1. Two small p-values in four complete records must replicate.
2. One exceptional p-value with three null-compatible records must not.
3. Four null-compatible records must not.
4. An incomplete family must be invalid.
5. A duplicate independence group must be invalid.
6. A record missing effect uncertainty must be invalid.

No fixture is MS evidence. The existing sequential global-evidence process is
unchanged and remains a different claim.

## Frozen Null Calibration Extension

Before accepting the implementation, simulate `250,000` four-record families
per cell at seeds `57031-57033`. Test equicorrelated valid null p-values at
rho `0`, `0.5`, and `0.9` under both the global null and the least-favorable
partial-conjunction configuration with one arbitrarily nonnull p-value fixed
to zero. The unchanged validity gate is maximum rejection probability `0.055`.
This calibration checks implementation behavior; the union-bound proof, not
the simulation, supplies the arbitrary-dependence guarantee.
