# CONVERGENCE_CHECK_37

Timestamp: 2026-05-27 17:24 CEST

## Inputs Integrated

- Wave75 response-state stratification:
  - `scripts/v3_wave75_response_state_stratification.py`
  - `phases/v3/results/wave75_response_state_stratification/`
- Wave76 adjusted response-specificity stress test:
  - `scripts/v3_wave76_adjusted_response_specificity.py`
  - `phases/v3/results/wave76_adjusted_response_specificity/`
- Wave77 local `ETS2` target audit:
  - `scripts/v3_wave77_ets2_macrophage_axis_audit.py`
  - `phases/v3/results/wave77_ets2_macrophage_axis_audit/`
- Subagent reports:
  - `phases/v3/subagents/wave75a_perturbation_first_controller_hunt.md`
  - `phases/v3/subagents/wave75c_cross_disease_targetability_scout.md`
  - `phases/v3/subagents/wave75g_hostile_critique.md`

## What Each Track Believes

Response-state track:

- A pretreatment lysosomal/APC state separates anti-TNF responders in RA and
  IBD DCs.
- The raw signal is real enough to reopen the biomarker/readout branch:
  RA effect `1.018`, p `0.00113`, FDR `0.0319`; IBD DC effect `0.888`,
  p `0.0204`, FDR `0.0984`.
- After adjustment, the signal remains nominal but is generic-limited:
  RA coefficient `0.289`, p `0.0746`, target/generic ratio `3.72`; IBD DC
  coefficient `0.260`, p `0.0369`, target/generic ratio `1.70`.
- Call: `PARK_RESPONSE_SIGNAL_GENERIC_LIMITED`.

ETS2 track:

- Direct `ETS2` is strong in IBD myeloid contexts and RA baseline response,
  but fails MS, perturbation, foundation-model, target-resolution, and
  intervention-route gates.
- Wave77 call: `NO_GO_ETS2_LOCAL_AUDIT`.
- This independently confirms the prior Wave75 ETS2 program audit.

Perturbation-first subagent track:

- No immediate finding.
- MED16 is a non-druggable benchmark.
- The only bounded target family worth a response-direction audit is the
  LILRB inhibitory-receptor family (`LILRB2`, `LILRB1`, `LILRB4`).

Targetability scout:

- No promotable target.
- A separate strict follow-up shortlist remains: `CD58`, `SPNS1`, `P4HB`,
  `SEL1L3`; `IFI30` is benchmark only.

Hostile critique:

- The main risk is still proxy-satisficing.
- Required next evidence must be target-level, beat generic controls, and
  include modality plus guardrail checks.

## Agreement

- Generic inflammatory/APC programs are repeatedly reproducible but not enough
  for the V3 therapeutic-discovery bar.
- The strongest surviving route is no longer "find another module score"; it
  is target-level response-direction testing with explicit generic controls.
- A response-state signal may become a biomarker or trial-enrichment readout,
  but it is not an intervention claim.

## Disagreement

- The response-state track sees useful stratification signal.
- The intervention track has not yet identified a target that explains or
  controls that state without collapsing into broad inflammation.
- The ETS2/macrophage-regulatory branch supplies breadth in IBD but fails the
  MS and druggability requirements.

## Decision

No `FINDING_V3.md`.

Proceed to Wave78: LILRB inhibitory-receptor family target-level audit.

Pass criteria for Wave78:

- at least one LILRB-family member has target-level support in MS or a clear
  non-negative MS guardrail;
- response-direction support in both RA and IBD after generic-inflammatory
  adjustment;
- evidence that the effect is receptor-specific rather than merely myeloid
  abundance;
- no blocking directionality problem for agonism/inhibition;
- plausible intervention route and no immediate prior-art block.

Fail criteria:

- signal restricted to one disease;
- no MS guardrail;
- response association lost after generic controls;
- directionality ambiguous between pathogenic and resolving myeloid states;
- no realistic target-level intervention route.
