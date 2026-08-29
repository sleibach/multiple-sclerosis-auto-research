# V57 Multi-Criterion Positive-Region Plan

Status: predeclared seeded synthetic method test; no biological evidence.

## Purpose

The original 500-screen sweep passed at 12 donors, while the higher-precision
9-11 sweep showed that a near-threshold design can fail the frozen sensitivity
criterion. This positive-control extension tests whether the apparent
12-donor boundary is stable at higher Monte Carlo precision.

## Frozen Design

- Parent generator and gate: commit `5c407480`.
- No changed effect, noise, endpoint, viability, guide, multiplicity, or
  selection parameter.
- Donor counts: `12`, `14`, and `16`.
- Effect scales: `0.80` and `1.00`.
- Seeds: `57061`, `57062`, and `57063`.
- Synthetic screens per cell: `2,000` (`36,000` total).
- The same five checks and all-seed/all-effect requirement apply.

## Decision

The smallest donor count passing all 30 checks is the first high-precision
tested positive design point. If 12 fails, the earlier low-precision pass is
superseded as method characterization. This does not estimate biological power
or assert that any useful perturbation exists.
