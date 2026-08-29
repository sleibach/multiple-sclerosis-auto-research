# V57 Multi-Criterion Perturbation Gate Plan

Status: predeclared method-characterization plan. All generated observations
are seeded synthetic data and cannot support a biological or MS claim.

## Decision Problem

A direction-resolving human-cell perturbation pilot needs a rule that does not
promote a candidate merely because an average molecular score improves while
other functions or viability worsen. The method must also generalize across
donors and guides.

## Frozen Simulation

- Candidate perturbations per screen: `24`.
- Candidate truth classes: four broad rescues, four narrow one-endpoint
  effects, four two-benefit/two-harm tradeoffs, four toxic pseudo-rescues, and
  eight nulls.
- Efficacy outcomes: four equally scaled, benefit-oriented outcomes standing
  for inflammatory state, debris handling, lipid/oxidative stress, and neural
  support. These labels are experimental-design placeholders, not simulated
  MS biology.
- Safety outcome: viability, benefit-oriented so negative values indicate
  harm.
- Independent guides per perturbation: `3`.
- Donor counts: `4`, `6`, `8`, and `12`.
- Broad-rescue effect scales: `0.60`, `0.80`, and `1.00` standardized units.
- Seeds: `57061`, `57062`, and `57063`.
- Screens per donor/effect/seed cell: `500` (`18,000` total).
- Correlated donor, perturbation-by-donor, guide, and measurement noise are
  generated explicitly. Guide means are computed within donor before any
  candidate-level inference.

## Comparator: Averaged Endpoint

For each candidate, average the four efficacy outcomes within donor, run a
one-sided t test against zero, and require Bonferroni `p <= 0.05 / 24`. Require
only the observed mean viability to exceed `-0.50`. This is a multiplicity-
controlled but compensatory rule: a large benefit can mask a harmful efficacy
dimension or uncertainty around viability.

## Candidate Gate: Replicated Broad Rescue

A candidate passes only if all criteria hold:

1. Partial-conjunction evidence for benefit in at least three of four efficacy
   outcomes, using `p_PC = min(1, 2 * p_(3))`, then Bonferroni across 24
   candidates at family alpha `0.05`.
2. A simultaneous one-sided viability lower confidence bound exceeds the
   non-inferiority margin `-0.50`, using alpha `0.05 / 24`.
3. The minimum leave-one-donor-out average efficacy effect is positive.
4. At least two of three guide-specific average efficacy effects are positive.

No threshold will be changed after observing simulation results.

## Evaluation Gates

The candidate method is useful only if, in every seed at donors `>=8` and
effect scale `>=0.80`:

- false-promotion probability (any non-broad candidate selected) is `<=0.05`;
- probability of selecting at least one true broad rescue is `>=0.80`;
- broad-rescue selection precision is `>=0.90`;
- the method reduces false promotion versus the averaged endpoint without
  reducing probability of at least one true rescue by more than `0.10`.

The result will be reported as method behavior only. A pass specifies a future
screen decision rule; it does not nominate a perturbation, mechanism, or
treatment.
