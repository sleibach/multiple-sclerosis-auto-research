# Convergence Check 2 - Hour 4

Timestamp: 2026-05-26 22:12 UTC

## Track Beliefs

Expression/cell-state track:

- Raw cross-disease IFN/HLA/CD74/APC recurrence is real.
- It is too generic to support a central causal mechanism without stronger
  controls.
- `LIPA` is not a pan-autoimmune myeloid node; it is a compartment-specific
  epithelial/ductal/keratinocyte stress/repair marker.

Perturbation track:

- Mixscale CRISPRi strongly validates IFNGR/JAK/STAT/RFX5 control of the
  antigen-presentation transition.
- This validates wiring, not therapeutic selectivity.
- No valid named-gene State foundation-model output exists yet.

Genetics track:

- HLA/MHC and some IFN-regulatory loci support broad autoimmunity.
- No non-MHC candidate among CD74, LIPA, IFI30, CIITA/RFX5, NAMPT has
  cross-disease causal anchoring sufficient for the V3 DoD.
- `OSMR` and `IRF1` remain visible in local OpenTargets-style tables and deserve
  a pivot pass.

Intervention track:

- Broad IFNGR/JAK/STAT is too broad and prior-arted.
- CD74/MIF, CTSS, CIITA/MHC-II, PDE4/cAMP, IFI30, and LIPA/LAL have prior-art
  or directionality barriers.
- PDE4/cAMP is tractable for local UC/skin experiments but current L1000 audit
  does not support it as a strong reversal candidate.

## Agreement

All tracks agree that no current candidate meets the V3 target bar.

The shared raw state remains useful as a map, not as a therapeutic claim.

## Disagreement

The only residual disagreement is whether a biomarker/stratification finding
could be valuable enough. Under the user-specified V3 DoD, it is not enough
because the task requires a central mechanism/intervention point with genetic,
foundation-model/perturbation, cell-state, and novelty support.

## Next Forcing Question

Does a tissue-licensing axis upstream of the lipid-lysosomal and IFN/APC states,
especially `OSM/OSMR` or complement/C1q, have:

- stronger cross-disease genetics;
- reproducible tissue/cell-state signal;
- perturbation evidence;
- a tractable selective intervention point;
- less blocking prior art than CD74/LIPA/NAMPT?

## Decision

Pivot to `OSM/OSMR` and complement/C1q in parallel. Keep `IRF1` as a positive
control and prior-art stress test, not as the default answer.
