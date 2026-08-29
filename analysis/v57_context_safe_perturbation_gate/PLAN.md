# V57 Context-Safe Perturbation Gate Plan

Status: predeclared seeded synthetic method characterization. It contains no
biological observation or MS claim.

## Threat Model

A perturbation can look beneficial on average while reversing in a donor
subtype. The existing leave-one-donor-out check may miss a harmful minority if
the majority effect is strong. This test uses a prespecified, outcome-blind
binary donor context; no subgroup may be discovered after outcomes are seen.

## Frozen Simulation

- Candidates: 24: four uniform broad rescues, four subgroup-reversal effects,
  four efficacy tradeoffs, four toxic pseudo-rescues, and eight nulls.
- Outcomes, guides, covariance, noise scales, and base gate follow commit
  `5c407480`.
- In subgroup-reversal candidates, the majority donor context receives the
  broad positive effect and the minority context receives a broad negative
  effect. The pooled mean remains favorable.
- Minority context: nearest integer to one-third of donors, assigned before
  outcomes.
- Donor counts: `12`, `16`, `24`.
- Effect scales: `0.80`, `1.00`.
- Seeds: `57101`, `57102`, `57103`.
- Screens per cell: `1,000` (`18,000` total).

## Methods

1. **Pooled replicated gate:** the existing partial-conjunction, simultaneous
   viability, leave-one-donor-out, and guide-replication rule.
2. **Context-safe gate:** the pooled gate plus, in each prespecified donor
   context, a simultaneous one-sided lower bound on average efficacy above the
   non-harm margin `-0.25` and a simultaneous viability lower bound above
   `-0.50`. Bounds use alpha `0.05 / (24 * 2)` within each outcome family.

## Frozen Success Criteria

At donors `>=16`, every seed and effect cell must meet:

- probability of selecting any subgroup-reversal candidate `<=0.05`;
- probability of selecting at least one uniform broad rescue `>=0.80`;
- precision for uniform broad rescues `>=0.90`;
- reversal promotion below the pooled gate;
- true uniform-rescue probability no more than `0.10` below the pooled gate.

If the context-safe gate passes only at a larger donor count, that is the
design result. If it cannot retain power while controlling reversals, the
method fails and a richer hierarchical design is required. No margin or gate
will change after simulation.
