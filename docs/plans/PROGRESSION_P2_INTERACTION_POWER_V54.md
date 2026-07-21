# V54 P2 Compartment-Interaction Power Plan

Status: frozen synthetic method plan, committed before execution. This plan
uses no received or held biological values and cannot establish compartment
localization or an MS progression effect.

## Question

Under what explicit assumptions can a future P2 package detect that the same
frozen molecular state has a different confirmed-disability association in
CNS/CSF versus blood, using a direct compartment-by-outcome interaction?

Separate significance in one compartment and non-significance in another is
prohibited. The direct interaction is the only confirmatory P2 estimand.

## Synthetic Generator

Each cohort has balanced progression-event groups and molecular scores in blood
and CNS/CSF. The generator varies:

- subjects per outcome group per compartment: `10, 15, 20, 30, 50, 80`;
- design: paired subjects or independent unpaired compartment samples;
- true CNS-minus-blood outcome effect: `0.0, 0.4, 0.7, 1.0` standardized units;
- paired residual compartment correlation: `0.0, 0.5, 0.8`;
- extra outcome-associated CNS composition imbalance: `0.0, 0.5`;
- composition-measure reliability: `1.0, 0.7`;
- three seeds and 250 cohorts per seed/cell;
- two-sided alpha `0.05`, with positive interaction required under non-null
  simulations.

The score includes a fixed composition contribution. In the imbalance regime,
outcome-associated composition differs more strongly in CNS/CSF than blood,
creating a deliberate false-localization risk if composition is ignored.
Reliability values are design stresses, not empirical estimates for MS data.

## Frozen Analyses

For paired subjects, the interaction is estimated by regressing within-subject
`CNS minus blood` score on outcome group. The adjusted route adds the paired
composition difference. Subject-level differencing is mandatory; treating the
two compartments as independent is not permitted.

For unpaired data, one model includes outcome, compartment, and their direct
interaction. The adjusted route adds measured composition and its compartment
interaction. The coefficient of outcome-by-compartment is the only tested
localization effect.

Each generated cohort is evaluated by both unadjusted and composition-adjusted
routes. Fits require positive residual degrees of freedom and nonsingular
information. The V54 eligibility floor of at least 10 independent subjects per
outcome group per compartment is represented but is not assumed powered.

## Frozen Evaluation

- Under a zero true interaction, any `p <= 0.05` is a false localization pass.
- Under a positive interaction, a pass requires `p <= 0.05` and a positive
  coefficient.
- Wilson intervals and per-seed ranges quantify simulation uncertainty.
- A scenario reaches the planning threshold at the first group size with
  aggregate pass probability at least `0.80` and every seed at least `0.75`.
- Null calibration is reported separately by design, composition imbalance,
  composition reliability, and analysis route.
- The adjusted route is not declared safe from its median alone: maxima,
  intervals, and the pattern across null cells are inspected.

## Interpretation Boundary

The simulation assumes a continuous score, balanced binary outcome, measured
composition with known reliability, and correctly specified linear interaction.
It omits irregular visit time, outcome misclassification, treatment/source
structure, and cell-state measurement error beyond the declared terms. Any
sample-size result is conditional method behavior, not a universal P2 target.
A real package must rerun the design from blinded metadata and must first pass
the P1 semantic gate.
