# V57 Two-Stage Context Confirmation Plan

Status: predeclared seeded synthetic method characterization. No generated
observation is biological or MS evidence.

## Why a Second Stage

Simultaneous context bounds on all 24 discovery candidates were too
conservative. This design separates broad discovery from independent
confirmation so multiplicity-heavy screening does not share data with a
context-safety decision.

## Frozen Threat Model

- 24 candidates: four uniform broad rescues, four context-harm candidates,
  four efficacy tradeoffs, four toxic pseudo-rescues, and eight nulls.
- Context-harm candidates improve three efficacy outcomes in both contexts but
  reverse the fourth, neural-support placeholder, in the minority context.
- The donor context is binary, balanced in confirmation, fixed before outcomes,
  and never inferred from response.
- Discovery uses 12 donors, the committed pooled replicated gate, and nominates
  at most four passing candidates ranked by the minimum mean efficacy outcome.
- Confirmation uses fresh donors and no discovery observations.
- Confirmation donors per context: `4`, `6`, `8` (total `8`, `12`, `16`).
- Effect scales: `0.80`, `1.00`; seeds `57201`, `57202`, `57203`; `1,000`
  synthetic screens per cell (`18,000` total).

## Frozen Confirmation Rule

For every nominated candidate, require in each donor context:

1. simultaneous one-sided lower bounds for **each** of four efficacy outcomes
   above non-harm margin `-0.25`;
2. a simultaneous viability lower bound above `-0.50`.

Use alpha `0.05 / (4 candidates * 2 contexts * 5 outcomes)` regardless of how
many candidates are nominated. No efficacy endpoint can compensate for harm in
another. Only candidates passing every bound in both contexts are confirmed.

## Frozen Success Criteria

At confirmation sample sizes `>=6` donors per context, every seed/effect cell
must have:

- probability of confirming any context-harm candidate `<=0.05`;
- probability of confirming at least one uniform rescue `>=0.80`;
- uniform-rescue precision `>=0.90`;
- context-harm confirmation below its discovery nomination probability;
- uniform-rescue probability no more than `0.10` below discovery nomination.

The smallest passing confirmation panel is the method result. Failure is
retained without margin or multiplicity changes.
