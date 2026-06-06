# Convergence Check 18

Timestamp: 2026-05-27 11:20 UTC

## Trigger

Wave55 completed a live external genetics/druggability sweep across 12
autoimmune diseases using Open Targets, ChEMBL, Europe PMC, and local V3
cell-state/perturbation/foundation-model outputs.

## What Each Track Now Believes

- External genetics breadth: many canonical autoimmune genes recur across
  diseases. Among non-closed targets, `SP140`, `IL12A`, `IL7R`, `CD40`,
  `STAT4`, `BACH2`, `IL12B`, and `TAGAP` have broad Open Targets support.
- Local cross-disease cell-state track: `SP140` is the strongest Wave55
  reopener because it has local positive signal in Crohn disease, ulcerative
  colitis, psoriasis, and Sjogren syndrome with no negative local disease
  calls.
- MS-specific local track: no Wave55 candidate has a strict MS white-matter
  anchor after multiple-testing correction. `SP140` is near-null in the local
  MS compartment (delta -0.087, p 0.726, FDR 0.968).
- Perturbation/foundation-model track: no Wave55 reopener has direct real
  perturbation support in the available local perturbation tables.
- Druggability track: `IL12A` has modality precedent through the IL-12/23
  axis but looks prior-art-heavy and weakly local. `SP140` has no ChEMBL
  chemical matter in this sweep and must be considered an intervention-point
  problem, not an immediately druggable target.

## Agreement

All tracks agree that no Wave55 candidate is currently promotable under V3.
The recurring failure is target-resolved causality/intervention evidence, not
generic cross-disease association.

## Disagreement

- `SP140`: external genetics and local cross-disease cell states support a
  reopener; MS local signal, perturbation, and druggability do not.
- `IL12A`: genetics and modality precedent support a comparator; local module
  evidence and novelty do not.

## Next Forcing Question

Can `SP140` be converted from a cross-autoimmune association/cell-state marker
into a mechanistically grounded intervention hypothesis by showing one of:

1. target-resolved genetic causality/colocalization,
2. real perturbation or foundation-model-predicted rescue of the
   lipid-lysosomal inflammatory myeloid state,
3. a druggable upstream/downstream intervention point with lower prior-art
   blocking risk than IL-12/23 blockade?

## Decision

Run a targeted `SP140` audit next. Keep `IL12A` only as a comparator/control
for druggability and prior-art crowding.
