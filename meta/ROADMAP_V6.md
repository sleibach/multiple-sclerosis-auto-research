# V6 Roadmap

Started: 2026-05-28 20:51 CEST

## Reframe

V6 treats V5 negative and confounded results as hypothesis-generating substrate.
The V5 therapeutic demotions remain valid at Tier 1+, but their failure modes
are no longer endpoints. They are sources for Tier -1 exploration.

## Active Tracks

### Track A - Confounder Mining

Inputs:
- `results/pregnancy_dimension/gse17410_ms_sensitivity/`
- `analysis/tier_1_mechanism/mif_cd74_component_ms_pseudobulk/`
- `analysis/tier_1_mechanism/mif_cd74_gse282122_component_response/`

Question: Which adjusted-away covariates or component decompositions identify
new biology rather than nuisance?

Initial outputs expected:
- pregnancy hematologic-shift hypotheses;
- APC-state-controller hypotheses;
- treatment-response remodeling hypotheses.

### Track B - Negative-Result Mining

Inputs:
- V3/V4/V5 candidate demotions in `knowledge/candidates/`;
- decision files in `knowledge/decisions/`.

Question: For each demotion, what narrower hypothesis survives under Tier -1
rules even if the therapeutic target claim failed?

### Track C - Generative Pattern Mining

Inputs:
- existing result tables from pregnancy, MS lesion pseudobulk, GSE282122
  treatment response, and spatial/lipid-lysosomal module work.

Question: What loose but biologically interpretable effects meet Tier -1 entry
criteria and deserve first independent checks?

### Track D - Promotion Queue

By hour 6 active work, at least three Tier -1 hypotheses should have enough
specificity and independent support to attempt Tier 0 promotion.

## First Priority Hypotheses

1. MS late-pregnancy hematologic/endothelial axis: erythroid, platelet, and
   neutrophil shifts in `GSE17410` may be disease-relevant rather than nuisance.
2. pDC-depletion/ISG-source switch: MS month-9 ISG rises while pDC markers fall.
3. Postpartum T-cell trafficking readiness: `E-MTAB-12260` T-cell trafficking
   rises postpartum despite no T-cell IFN/APC replication.
4. APC-state-controller rather than CD74: CD74 is mostly a broad APC/size
   readout, implying upstream state controllers are the relevant intervention
   layer.
5. OPC CD74 lesion-stress state: residual CD74 signals in OPC contrasts may
   point to nonimmune lesion-compartment biology.
6. Anti-TNF HLA-II remodeling: remission-associated HLA-II behavior in
   GSE282122 is IFN/APC-coupled but receptor-only CD74/CD44/CXCR4 moves in the
   opposite raw direction.

## Milestones

- Hour 0-2: Tier -1 rulebook, hypothesis registry, reproducible initial pattern
  mining, and first subagent dispatch.
- Hour 2-6: generate at least twelve Tier -1 entries and identify at least
  three Tier 0 promotion attempts.
- Hour 6-12: run Tier 0/Tier 1 tests for top hypotheses, preferring
  independent datasets and dimensions over reusing the opening observation.
- Hour 12-16: attempt Tier 2 advancement on the strongest survivor or document
  why none has temporal/natural-experiment support.

## Stop Condition Reminder

Do not stop for single nulls. A Tier -1 null must produce refinements. V6 stops
only on Tier 4 breakthrough, external interruption, or true exhaustion after at
least sixteen active hours.
