# CIITA Selective Approaches

Status: parked  
V4 tier: Tier 0  
Last updated: 2026-05-28

## V3 History

CIITA/MHC-II regulation appeared in V3 perturbation and antigen-presentation
decoupling discussions but was not matured due to host-defense and modality
concerns.

## V4 Recalibration Question

Can selective CIITA pathway modulation decouple pathogenic antigen presentation
from broad host-defense suppression?

## Current V4 Contribution

Verdict: **Demotion was prior-art-driven but V4 contribution exists.**

V4 contribution:

Selective suppression of pathogenic `CIITA`/MHC-II/`CD74`
antigen-presentation output while sparing broad IFN/JAK antiviral signaling,
potentially via transcriptional co-regulator routes rather than direct JAK/STAT
blockade.

Prior-art grade: `P1 high crowding`, not target-invalidating.

## Recalibration Evidence

Local V3 support:

- `phases/v3/results/wave14_gsk3b_ciita_perturbation/wave14_verdict.json`:
  `Gsk3b_KO` reduces CIITA/MHC-II/CD74 mean log2FC `-1.856`, generic IFN mean
  log2FC `-0.483`, selectivity ratio `3.84`. Ruxolitinib is the broad
  IFN/JAK-collapse control.
- `phases/v3/results/wave15_perturbation_drug_response/ranked_direct_perturbations.tsv`:
  `Med16_KO` suppresses target module `-3.1395`, generic IFN `-0.7979`,
  selectivity score `2.3051`; `RFX5` CRISPRi is weaker but target-selective.
- `phases/v3/results/wave17_mediator_kinase_route/route_verdict.json`:
  CDK8/CDK19 translational route was parked because pharmacologic phenocopy of
  MED16 selectivity was not proven.

Prior-art context:

- CIITA is the master regulator of MHC-II expression; broad CIITA loss is
  immunologically dangerous.
- IFN-gamma/JAK/STAT induction of CIITA/MHC-II is established macrophage
  biology.
- MHC-II antigen presentation is deeply implicated in autoimmunity.

Therefore novelty cannot be "CIITA/MHC-II matters"; it must be selective
modulation that decouples pathogenic antigen-presentation output from broad
IFN/JAK blockade.

## Key Cautions

- Direct CIITA targeting is not currently a practical drug modality.
- Broad CIITA loss or JAK inhibition is not acceptable as the V4 mechanism.
- Mouse macrophage evidence must be translated into human APC-relevant systems.

## Next Tier 0 Test

Run a focused selectivity audit comparing `MED16`, `GSK3B`, `RFX5`, `CDK8`,
`CDK19`, and `CCNC` across V3 perturbation tables plus accessible external
perturbation data.

Advance only if an intervention-class candidate shows:

- CIITA/MHC-II/CD74 suppression at least `2x` stronger than generic IFN genes.
- No strong stress/toxicity induction.
- Evidence in human myeloid/APC-relevant cells, not only mouse macrophage or
  cancer Perturb-seq.
- A plausible modality route distinct from broad JAK inhibition.

## V4 Tier 0 Audit

Audit completed: `analysis/tier_0_triage/ciita_mediator_selectivity/decision.json`.

Call: `PARK_ALIVE_PENDING_PHARMACOLOGIC_PHENOCOPY`.

Result: selective CIITA/MHC-II/CD74 decoupling remains biologically plausible,
but the only strong benchmark is non-druggable `MED16`. `GSK3B` is partial and
pleiotropic; `RFX5/CIITA` are not practical direct modalities; and local
CDK8/CDK19 genetic evidence does not phenocopy `MED16`.

Interpretation: keep the branch as a priority Tier 0 parked mechanism, but do
not advance to Tier 1 without a pharmacologic or human APC perturbation dataset
showing target-module suppression at least 2x stronger than generic IFN without
stress/toxicity.
