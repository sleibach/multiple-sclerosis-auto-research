# Convergence Check 32 - Wave70 Closure

Timestamp: 2026-05-27 16:33 CEST

## Inputs

- Wave70-A prior-art/translational audit:
  `phases/v3/subagents/wave70a_fc_ros_prior_art_feasibility.md`.
- Wave70-B computational scout:
  `phases/v3/subagents/wave70b_fc_ros_computational_scout.md` and
  `phases/v3/results/wave70b_fc_ros_computational_scout/`.
- Wave70 local matrix:
  `phases/v3/results/wave70_fc_ros_resolution_matrix/`.
- Wave70-C Geneformer directionality screen:
  `phases/v3/results/wave70c_inhibitory_receptor_geneformer_direction/`.

## Agreement

All Wave70 tracks agree that no Fc/ROS-resolution candidate should be promoted.

- Prior-art/translational audit: the obvious target classes are clinically
  saturated, broad, directionally ambiguous, or delivery-limited.
- Local computational scout: `LILRB2` is the strongest falsification target but
  lacks genetics, RA replication, and direct perturbation evidence.
- Geneformer directionality screen: model support concentrates on blocked
  `FCGR2A`/`NCF1`/NOX biology; less-blocked inhibitory receptors and `INPP5D`
  do not reach the reopener threshold.

## Key Quantitative Points

- `LILRB2`:
  - `GSE282122` DC remission adjusted beta `-0.949`, FDR `0.0191`.
  - Wave68 adjusted delta `-0.884`, FDR `0.0224`.
  - broad h5ad recurrence: Crohn/UC myeloid, 2 positive compartments, 1 FDR10.
  - Wave70-C: 0 strong support contexts, 2 support contexts, 1 opposing
    context, 4 contexts with token support; call `NO_GO_MODEL_DIRECTION_SCREEN`.
- `INPP5D`:
  - RA anti-TNF paired delta `-0.386`, FDR `0.0294`.
  - Wave70-C: 1 support context, no strong support, only 1 token-supported
    context; call `NO_GO_MODEL_DIRECTION_SCREEN`.
- Blocked comparators:
  - `NCF1`: Wave70-C 2 strong support contexts, 3 support contexts.
  - `FCGR2A`: Wave70-C 2 strong support contexts, 3 support contexts.
  - `CYBB`: Wave70-C 1 strong support context, 2 support contexts.

## Self-Critique

The temptation is to rescue `LILRB2` because it is less blocked than Fc/NOX
nodes and has a plausible inhibitory-receptor story. That would be proxy
satisficing. Its support is a local IBD treatment-response expression state
plus broad Crohn/UC recurrence, not a cross-autoimmune target mechanism. The
foundation-model deletion signal is neither strong nor directionally clean.

The temptation is also to promote `INPP5D` because the prior-art sidecar says
SHIP1 activation is the only bounded fail-fast route. The local evidence does
not justify promotion: RA pharmacodynamic movement and an unresolved mouse
efferocytosis trend are not disease-causal, and the Geneformer screen lacks
token support.

## Decision

Close the Fc/ROS-resolution branch as a target-nomination route.

Next forcing question: outside Fc/ROS, does any prior V3 branch contain an
unblocked central node with cross-disease breadth, perturbation support, and
tractable intervention potential? If not, search for a new mechanism rather
than continuing local variants of Fc/NOX biology.
