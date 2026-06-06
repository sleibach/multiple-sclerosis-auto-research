# Convergence Check 38: LILRB Inhibitory-Receptor Family Route

Timestamp: 2026-05-27 17:37 CEST

## Inputs Integrated

- Local Wave78 audit:
  - `scripts/v3_wave78_lilrb_family_target_audit.py`
  - `phases/v3/results/wave78_lilrb_family_target_audit/`
- Prior-art/translational sidecar:
  - `phases/v3/subagents/wave78a_lilrb_prior_art_feasibility.md`

## What Each Track Believes

Local target-level track:

- `LILRB1/2/3/4` show IBD anti-TNF response associations, but no receptor
  survives target-level convergence.
- Local call: `NO_GO_LILRB_TARGET_LEVEL_CONVERGENCE`.

Family-specificity track:

- The strongest disease-state LILRB signals are not receptor-family-specific.
- In same disease/compartment contexts, activating LILRA paralogs are stronger,
  so the LILRB signal looks like a generic inflamed myeloid/APC family readout.

MS track:

- `LILRB2`, the best prior local falsification target, is nominally lower in MS
  white matter: delta `-0.730`, p `0.00778`.
- That is wrong-direction for a suppression/antagonism route and insufficient
  for an agonism route because IBD remission is associated with receptor
  decrease.

Response track:

- IBD response is real:
  - `LILRB1` mono/macrophage adjusted delta `-1.035`, p `0.000937`.
  - `LILRB4` mono/macrophage adjusted delta `-1.476`, p `0.000730`.
  - `LILRB2` DC adjusted delta `-0.884`, p `0.00505`.
- RA does not replicate the same suppression-response direction.

Foundation-model track:

- Wave70-C remains no-go or ambiguous for LILRB genes.
- `LILRB2` has deletion-toward-remission support in some UC contexts, but not
  enough context breadth and no RA/MS/genetic convergence.

Prior-art/translational track:

- Call: `PARK_DIRECTIONALITY`.
- Tolerogenic autoimmune use points toward agonism/induction of ILT3/ILT4 or
  HLA-G/LILRB pathways.
- Oncology development points toward antagonist/depletion of LILRB2/LILRB1/2
  or LILRB4.
- Both directions are prior-art crowded; generic autoimmune agonism is blocked
  by ILT3-Fc/targeted-immunotolerance patents, while antagonist/depleter routes
  are biologically risky for autoimmunity.

## Agreement

- The LILRB family is biologically real and druggable by biologics.
- It does not currently produce a V3-valid cross-autoimmune/MS therapeutic
  mechanism.
- Directionality is the decisive problem: the same receptor class can plausibly
  mean compensatory tolerance, pathogenic plasma-cell biology, or generic
  myeloid activation depending on cell state.

## Decision

Do not promote `LILRB1/2/3/4`.

Close the inhibitory-checkpoint route unless a future branch opens a
cell-selective SLE plasmablast/plasma-cell hypothesis with a distinct delivery
or depletion modality.

## Next Forcing Question

Move to a target-first shortlist that is not just a myeloid marker family:
`CD58`, `SPNS1`, `P4HB`, and `SEL1L3` from the Wave75 targetability scout are
the next candidates to falsify.
