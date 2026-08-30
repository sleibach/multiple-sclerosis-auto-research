# V57 Blinded Variance-Adaptation Plan

Status: predeclared seeded synthetic method characterization. No generated
observation is biological or MS evidence.

## Purpose

The staged screen passed under one explicit variance model. A future assay's
variance is unknown. This extension tests whether a blinded internal pilot can
adapt confirmation sample size using nuisance variance only, without observing
candidate means, truth classes, or confirmation outcomes.

## Frozen Design

- Discovery and candidate nomination follow commit `d362861f`.
- Confirmation uses two orthogonal viability wells per guide, the passing
  assay architecture at commit `7b2d57bc`.
- True confirmation noise multipliers: `0.75`, `1.00`, `1.25`, `1.50`, applied
  to all efficacy and viability random components, not mean effects.
- A blinded pilot produces a pooled SD-multiplier estimate with `48` residual
  degrees of freedom. It is simulated from the exact chi-square sampling law
  and is independent of all candidate means/outcomes.
- Use the one-sided 90% upper confidence limit for the SD multiplier.
- Candidate donor counts per context: `12`, `16`, `20`, `24`, `32`.
- Select the smallest grid value at least `ceil(12 * upper_multiplier^2)`;
  abstain if this exceeds 32. No unblinded resizing is allowed.
- Effect scales: `0.80`, `1.00`; seeds `57401`, `57402`, `57403`; `500`
  synthetic screens per cell (`12,000` total).
- Frozen confirmation margins and family correction are unchanged.

## Comparators

1. Fixed 12 donors/context regardless of variance.
2. Blinded adaptive donor count.
3. Oracle donor count using the true multiplier in the same formula. The oracle
   is a method benchmark, not an executable design.

## Success Criteria

For every seed, effect, and true multiplier:

- adaptive context-harm confirmation `<=0.05`;
- adaptive probability of at least one uniform rescue `>=0.80`;
- adaptive uniform-rescue precision `>=0.90`;
- adaptive uniform-rescue probability no more than `0.10` below oracle;
- abstention probability `<=0.10`.

Report sample-size distribution and over/under-sizing relative to oracle. A
failure is retained; no confidence level, grid, multiplier, or threshold may
change after simulation.
