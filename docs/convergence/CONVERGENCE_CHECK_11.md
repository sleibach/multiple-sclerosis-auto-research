# Convergence Check 11 - Upstream Niche-Driver Audit

Timestamp: 2026-05-27 07:44 UTC

## What Each Track Now Believes

- Cross-disease cell-state track: the recurrent signal remains an
  IFN/HLA-II/CD74/GILT antigen-presentation transition with lipid-lysosomal and
  receptor/checkpoint neighborhoods.
- Target/intervention track: direct markers, enzyme neighbors, PTPN2
  restoration, target-first druggability, and now static upstream
  ligand/receptor axes do not supply a selective therapeutic claim.
- Modeling/guardrail track: broad IFN/JAK suppression can move the module, but
  the effect is not selective enough to count as a new intervention point.

## Agreement

Corrected Wave30 agrees with prior waves:

- `IFNG_IFNGR_JAK_STAT1_CIITA` is the most defensible state driver, not a new
  selective target.
- `MIF_CD74_CXCR4_CD44` is a strong neighborhood/biomarker axis, but V3
  residual and novelty gates block a therapy claim.
- `LILRB_HLA_INHIBITORY_MYLOID_CHECKPOINT` and `SPP1_CD44_INTEGRIN_RETENTION`
  are real local neighborhoods but lack target causality, therapeutic format
  maturity, or directionally clean selectivity.

## Disagreement Or Weakness

The first Wave30 run was wrong enough to reject: it counted broad `ifn_apc`
module recurrence as support for every candidate annotated to IFN biology. This
would have made generic inflammatory pathways look artificially convergent. The
script was reformulated to separate candidate-specific breadth from global
module breadth.

## Next Forcing Question

A static ligand/receptor audit is exhausted as a rescue route. The remaining
non-redundant question is whether a dynamic transition controller exists that
can decouple HLA-II/CD74 antigen presentation from generic IFN/JAK host-defense
collapse. If not, the session should pivot outside the current module rather
than keep retesting its neighborhoods.
