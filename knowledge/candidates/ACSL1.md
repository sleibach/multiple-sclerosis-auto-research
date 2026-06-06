# ACSL1

Status: demoted  
V4 tier: Tier 0  
Last updated: 2026-05-28

## V3 History

ACSL1 was proposed as a target in `docs/findings/FINDING.md` but later demoted after deeper
module-adjusted testing; it currently appears more like a lipid-myeloid marker
than a standalone intervention point.

## V4 Recalibration Question

Was ACSL1 demoted for evidence reasons, modality reasons, or prior-art reasons?

## Current V4 Contribution

None as a therapeutic target nomination.

ACSL1 remains useful as:
- a foamy/MIMS2-like MS lesion myeloid marker,
- a perturbation hypothesis for wet-lab microglia/myelin-debris assays,
- and a cautionary example for V4: a biologically plausible and novel target
  can still fail if it loses incremental value beyond the broader module and
  lacks a repair-safe direction of intervention.

## V4 Recalibration Verdict

Verdict 3: evidence-driven and modality-driven demotion holds.

The V4 prior-art standard does not rescue ACSL1 because ACSL1 was not mainly
demoted for prior art. The original `docs/findings/FINDING.md` had a narrow novelty claim:
ACSL1 as a foamy/MIMS2 chronic-active MS lesion microglial target hypothesis.
The later V3/V2 scrutiny weakened the target claim on its own terms:

1. ACSL1 lost incremental value after adjustment for the broader lipid/lysosomal
   myeloid module.
2. Cross-autoimmune recurrence was inconsistent and disease-context dependent.
3. Mechanistic simulations exposed the risk that ACSL1 lowering worsens
   lesion-rim dynamics or impairs lipid-buffering/repair functions.
4. Selective ACSL1 chemistry appears possible in principle, but no
   clinically validated CNS/microglia-engaged modality exists.
5. ACSL1 has high sequence identity to ACSL5/ACSL6, raising family/CNS
   selectivity risk, especially for ACSL6.

## Evidence Ledger

- `docs/findings/FINDING.md`: original positive ACSL1 hypothesis, based on foamy MS lesion
  proteomics, MIMS2-like snRNA validation, and directional MERFISH support.
- `docs/history/EXHAUSTION.md`: ACSL1 failed under heavier scrutiny; foamy proteomics
  coefficient fell from 0.366 (p 2.76e-05) to 0.124 (p 0.136) after adjustment
  for the broader lipid/lysosomal module; ABM lesion-rim simulation worsened
  active lesion area as ACSL1 activity was reduced under stated assumptions.
- `docs/convergence/CONVERGENCE_CHECK_1.md`: documented structural/pharmacology inventory,
  simulation weakening, and cross-autoimmune inconsistency.
- `subagents/alpha1_acsl1_deepening_report_2026-05-26.md`: ACSL1 selectivity
  is feasible in principle via Shionogi benzimidazole chemistry, but ACSL5/6
  similarity, CNS engagement, and repair safety remain unresolved.
- `subagents/beta1_cross_autoimmune_report_2026-05-26.md`: direct ACSL1 is not
  cleanly pan-autoimmune; the broader lipid-associated inflammatory myeloid
  module is more recurrent.
- `subagents/gamma1_hostile_review_2026-05-26.md`: ACSL1 may be an overfit
  marker and requires incremental-value, perturbation-rescue, selectivity, and
  repair-safety gates before target promotion.
- `results_v3/geneformer_broad_residual_delete/geneformer_broad_residual_summary.json`:
  ACSL1 deletion in the bounded Geneformer screen had no support contexts, no
  strong support contexts, and negative projection direction in 5 of 7 contexts.

## Next Tier 0 Test

Do not spend V4 Tier 0 target budget on ACSL1 unless new wet-lab perturbation or
larger spatial/protein data arrive.

Allowed future re-entry gates:
- human myelin-debris microglia/macrophage ACSL1 perturbation plus rescue shows
  at least 30% reduction in lipid-droplet/inflammatory injury while preserving
  myelin uptake, lysosomal acidification, oligodendrocyte support, and axonal
  survival;
- larger MS spatial/protein cohort shows ACSL1 adds injury or PRL information
  beyond `GPNMB/APOE/PLIN2/CTSD/NAMPT` and myeloid density;
- CNS/microglia-selective ACSL1 target engagement is demonstrated for a tool
  compound or RNA modality.
