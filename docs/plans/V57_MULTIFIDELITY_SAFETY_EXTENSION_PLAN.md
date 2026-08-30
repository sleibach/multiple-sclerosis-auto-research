# V57 Multifidelity Safety-Power Extension Plan

Status: predeclared remediation after the primary 2D-to-3D gate failed its
hidden-harm safety check. Synthetic method characterization only.

## Fixed Parent Result

The corrected parent design passed six of seven checks. In the hidden-harm
scenario, any 3D scale-up occurred in 83.0% of screens, but the prespecified
safety-discordance path identified the reason in only 13.9%. Generic
incremental information is not an adequate substitute for explicitly detecting
context harm.

## Unchanged Components

This extension keeps unchanged:

- the 12 candidates and hidden-harm data generator;
- the 2D and 3D effect sizes and variance;
- exact train/test batch balancing;
- the 0.20 safety margin;
- the 2.64 simultaneous candidate-family critical value;
- the two-panel requirement that 2D benefit and 3D harm replicate;
- 500 screens per seed and the three parent seeds.

Only training and held-out donor-pair counts vary over the frozen grid:

`12/8`, `12/12`, `16/12`, `16/16`, `20/16`, `24/20`, `32/24`, `40/32`.

## Passing Boundary

The first design point is eligible only if all three seeds have safety-specific
scale-up probability at least 0.80. Mean performance alone cannot pass. If no
point passes, the safety path remains unresolved and the 3D route must be sized
from empirical blinded variance rather than this synthetic model.

No biological inference follows from a passing design point.
