# Convergence Check 21

Timestamp: 2026-05-27 12:06 UTC

## Inputs

- Local Wave60:
  `results_v3/wave60_circuit_coupling_pivot/`.
- Wave60-R hostile review:
  `subagents_v3/wave60r_circuit_pivot_hostile_review.md`.

Wave60-P (`C15ORF48/MOCCI`) and Wave60-Q (`OSM/OSMR`) are still pending at
this checkpoint.

## What The Tracks Believe

Local circuit coupling:

- No circuit predictor passed the full reopener gate.
- `C15ORF48` has disease-up recurrence and nominal MS support, but does not
  pass cross-context residualized circuit coupling.
- `OSM` is IBD-skewed and fails MS/circuit-coupling gates.
- `OSMR` passes expression-coupling/disease-up gates but lacks MS and
  perturbation/model support.
- `GPNMB` is strongly coupled and MS-nominal but looks marker-like because the
  disease-up recurrence and perturbation gates fail.

Hostile methods review:

- Donor-level expression coupling is not promotable.
- The main failure modes are pseudo-replication, tissue non-comparability,
  module collinearity, weak residualization, and lack of perturbation or
  response validation.
- The next pivot should mine real perturbation/intervention evidence and use
  the lipid-lysosomal module only as a readout.

## Agreement

- The lipid-lysosomal/APC module is a recurrent disease-state readout, but it
  is not a sufficient target-discovery engine by itself.
- Single-gene expression, receptor expression, and donor-level coupling are
  too weak without perturbation, target engagement, or clinical response
  evidence.
- A valid therapeutic finding now needs intervention-level evidence.

## Decision

Close expression-only circuit coupling for V3 promotion.

Continue:

- external perturbation-first intervention mining;
- integrate Wave60-P/Q once returned, but do not allow them to promote
  `C15ORF48` or `OSM/OSMR` without real perturbation/response validation and a
  non-blocked prior-art delta.

## Next Forcing Question

Across public perturbation datasets already downloaded or reachable in this
environment, is there a named intervention that selectively reduces the V3
pathogenic module more than generic IFN/NF-kB/JAK/STAT suppression while
preserving repair/efferocytosis/viability guardrails?
