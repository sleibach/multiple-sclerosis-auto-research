# V57 Overlapping-Neighborhood Differential Abundance

## Boundary

This is a held anti-TNF IBD method-feasibility result, not an MS biological
finding.

## Result

- Outcome-blind neighborhoods: 40
- Unique patients: 22
- Estimable compartment-neighborhood tests: 20
- Best single seed/analysis result: Mono_macro__N17 (max-T p=0.0483)
- Stable features passing every gate:
  none

Verdict: **NO_STABLE_RESPONSE_SPECIFIC_NEIGHBORHOOD**.

The isolated best residualized result (`Mono_macro__N17`, max-T p=0.0483)
did not pass its raw test (p=0.1560) and was not stable across count seeds. It
is therefore not a supported feature.

Only patient labels were permuted; cells were never treated as independent
outcome replicates. A response-labelled MS single-cell cohort is required for
an MS-specific neighborhood test.
