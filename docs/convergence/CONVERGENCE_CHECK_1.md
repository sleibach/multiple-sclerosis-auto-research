# Convergence Check 1

**Time:** 2026-05-26T18:20Z

## Inputs

- γ1 hostile review returned and warned ACSL1 may be an overfit marker rather than a causal target.
- `scripts/v2_cross_autoimmune_bulk.py` ran after fixing a psoriasis classifier bug.
- `scripts/v2_acsl_family_inventory.py` ran.
- `scripts/v2_acsl1_mechanistic_simulations.py` ran.

## Deepen Track Status

ACSL1 structural/pharmacology inventory:

- AlphaFold DB models exist for ACSL1/3/4/5/6 with high global confidence.
- ACSL1 sequence identity is high with ACSL6 (`0.675`) and ACSL5 (`0.611`) under a simple global-alignment identity metric, creating a selectivity risk.
- ChEMBL has ACSL1 activity records, including sub-micromolar records, but this does not establish CNS penetration or family selectivity.

ACSL1 mechanistic simulations:

- ODE safe-window rule: `>=20%` injury reduction with `<=20%` free-lipid increase and `<=20%` clearance-capacity drop.
- Fraction of parameter draws with any safe therapeutic window: `0.0`.
- Median injury reduction at 20% inhibition was only `0.010`; 20% inhibition satisfied the safety rule in `0.95` of draws but had little modeled efficacy.
- Stronger inhibition improved median injury index only weakly and violated safety through free-lipid/clearance penalties.
- ABM lesion-rim simulation worsened active area and inflammation as ACSL1 activity decreased.

Interpretation: these simulations do not prove ACSL1 inhibition is bad, but they directly expose the therapeutic-window problem. The prior target claim is weakened. A microglia-selective RNA modality would still have to show partial pathway rebalancing, not broad ACSL1 suppression.

## Broaden Track Status

Cross-autoimmune public bulk/cell-specific screen:

- `GSE97779` RA macrophages: ACSL1 up directionally but not significant; LDAM module is lower in RA synovial macrophages than cultured healthy macrophages, while inflammation and NAMPT are strongly higher. This comparison is heavily confounded by fresh synovial fluid versus cultured blood macrophages.
- `GSE13355` psoriasis: paired lesional skin has LDAM module up, but ACSL1 is strongly lower. This argues against ACSL1 as a pan-autoimmune marker.
- `GSE75214` IBD: ACSL1 is strongly higher in active UC/CD comparisons; LDAM module is positive in most active comparisons.
- `GSE32591` lupus nephritis: LDAM module is higher in kidney compartments, but ACSL1 is null.

Interpretation: pan-autoimmune evidence supports a broader inflammatory lipid/lysosomal myeloid module more than ACSL1 specifically. ACSL1 appears disease-context dependent.

## Integration Decision

Do not write a V2 ACSL1 therapeutic target finding. ACSL1 is demoted to:

> a human MS/IBD-enriched marker and possible perturbation candidate in lipid-loaded myeloid states, with an unresolved and potentially unfavorable therapeutic window.

Pivot direction:

1. Search for a successor node in the ACSL1-marked module that has stronger cross-autoimmune recurrence, druggability, and perturbation precedent.
2. Initial candidates from local screen: `NAMPT`, `CTSB`, `SPP1`, possibly extracellular NAMPT/NAD-axis rather than intracellular ACSL1.
3. Require not just expression recurrence but plausible therapeutic direction; for example, NAMPT has strong recurrence but intracellular inhibition may impair phagocytosis and NAD-dependent repair.

## Next Actions

- Wait for α1 and β1 reports.
- Quantitatively rank module genes across MS and non-MS autoimmune screens.
- Run novelty and therapeutic feasibility scan for the strongest successor node.
- If no successor survives, prepare `EXHAUSTION.md` rather than forcing a target claim.
