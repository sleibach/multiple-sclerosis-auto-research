# CONVERGENCE_CHECK_40

Timestamp: 2026-05-27 17:44 CEST

## Inputs Integrated

- Wave79 targetability shortlist audit:
  - `scripts/v3_wave79_targetability_shortlist_audit.py`
  - `results_v3/wave79_targetability_shortlist_audit/`
- Wave79 sidecar:
  - `subagents_v3/wave79_targetability_prior_art_directionality.md`
- Wave80 CD58/CD2-axis deepening:
  - `scripts/v3_wave80_cd58_cd2_axis_deepening.py`
  - `results_v3/wave80_cd58_cd2_axis_deepening/`

## What The Tracks Now Believe

Targetability shortlist:

- `P4HB`, `SPNS1`, and `SEL1L3` are closed for V3 therapeutic promotion.
- `CD58` is the only partial survivor from Wave79.

CD58 local evidence:

- MS genetics are strong:
  - MS L2G `0.951`.
  - Crohn/MS strong-H4 QTL support.
- Broad cell-state recurrence exists:
  - Crohn disease, T1D, UC.
  - APC/myeloid positive diseases: Crohn disease and UC.
- RA anti-TNF response is real and not explained by simple T-cell admixture:
  - baseline generic-only coefficient `0.910`, p `0.00298`.
  - after T-cell adjustment coefficient `0.886`, p `0.00697`.
  - after T-cell plus effector-memory adjustment coefficient `0.870`,
    p `0.00871`.
- IBD replication remains weak:
  - p `0.173`, target/generic ratio `1.62`.

Prior-art/direction:

- Published MS genetics support `CD58` biology but point toward increased
  CD58/restored CD2 engagement and Treg support.
- Alefacept/CD58-Ig/CD2-directed intervention is already psoriasis/T1D
  autoimmune prior art and has mixed blockade/depletion/agonism biology.
- Therefore `CD58` cannot be promoted as a novel target.

## Agreement

- Expression recurrence plus target reachability is no longer an efficient
  route in this workspace.
- The next branch must start from perturbation or clinical response, not from
  another expression-ranked candidate list.
- `CD58` can be retained only as a biomarker/stratification comparator.

## Disagreement Or Tension

- `CD58` has unusually strong MS genetic support, but the therapeutic direction
  is not clear.
- RA supports baseline high `CD58` in good responders; IBD does not replicate
  strongly.
- If CD58 is causal, the likely mechanism may be immune-synapse/Treg/memory-T
  biology, not the original lipid-lysosomal myeloid module.

## Decision

No `FINDING_V3.md`.

Do not promote:

- `CD58`
- `SPNS1`
- `P4HB`
- `SEL1L3`

Next branch:

- Wave81 perturbation-first rescue.
- Search existing real perturbation, foundation-model, and response-direction
  outputs for targets with:
  - direct perturbation evidence;
  - cross-disease or MS anchor;
  - non-conflicted intervention direction;
  - feasible modality.

Do not run another broad expression-targetability re-rank unless the candidate
comes with an independent perturbation or clinical-response anchor.
