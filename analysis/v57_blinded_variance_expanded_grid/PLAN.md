# V57 Expanded Blinded-Variance Grid Plan

Status: predeclared seeded synthetic method characterization; no biological or
MS evidence.

## Frozen Remediation

The first blinded adaptation failed at high noise because a 48-df pilot was
uncertain and the 32-donor grid forced abstention. This extension changes only
those two design resources:

- pooled nuisance-variance residual degrees of freedom: `96`;
- donor grid per context: `12`, `16`, `20`, `24`, `32`, `40`, `48`.

Everything else is frozen from commit `25f0cdc4`: discovery, two-well
orthogonal viability assay, effects, noise multipliers, 90% upper confidence
limit, `ceil(12 * upper_multiplier^2)` rule, confirmation bounds, margins,
multiplicity, seeds (`57401`-`57403`), effects (`0.80`, `1.00`), and 500 screens
per cell.

## Decision

The same five success checks apply in every seed/effect/noise cell. Report the
selected sample-size distribution, abstention, and oracle gap. The method
passes only if all 120 checks pass. Added capacity is a resource tradeoff, not
a statistical relaxation; no candidate effect or outcome is visible during
adaptation.
