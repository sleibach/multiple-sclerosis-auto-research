# V57 Tied-Score Site E-Process Calibration Plan

Status: **frozen before simulation outcomes**

## Purpose and Boundary

The discrete-site calibration assumes continuous scores. A data owner may
round exported or intermediate scores, producing ties. This probe tests the
unchanged federated e-process with exact conditional permutation p-values under
a deliberately coarse five-level score mechanism.

This is seeded synthetic method characterization. It is not MS evidence and
does not add a site to the evidence accumulator.

## Fixed Design

- 12 independent arrivals;
- class splits cycled in order: `(4,5)`, `(5,5)`, `(6,6)`, `(7,7)`, `(8,8)`,
  `(10,10)`;
- latent unit-variance normal score effects: `0.0`, `0.5`, `0.9`;
- latent scores collapsed into five levels using fixed standard-normal quintile
  cut points `-0.841621`, `-0.253347`, `0.253347`, `0.841621`;
- seeds `57131`, `57132`, `57133`;
- 50,000 sequences per seed/effect/p-value mode;
- exact conditional one-sided rank-sum p-value with midranks;
- V42 plus-one sensitivity `(1 + Binomial(10000, p_exact)) / 10001`;
- unchanged e-calibrators `k * p^(k-1)` for
  `k in {0.25, 0.50, 0.75}` and unchanged boundary `20`.

For each observed tie pattern, dynamic programming enumerates the exact number
of label allocations at every midrank sum. Individual synthetic sequences are
not retained.

## Method-Behavior Gate

Both p-value modes must satisfy in every seed:

1. null ever-crossing by arrival 12 at most `0.055`;
2. null mean e-factor at every site design at most `1.01`; and
3. effect `0.9` crossing by arrival 12 at least `0.75`.

Effect `0.5` is descriptive. No threshold, grid, score coarsening, or evidence
rule may change after outcomes. Passing supports tied-score calibration only
for a valid conditional permutation test; it cannot repair response-dependent
preprocessing or invalid site independence.
