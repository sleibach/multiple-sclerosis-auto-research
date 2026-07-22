# V54 Progression Weaker-Effect Planning Result

Status: seeded synthetic clean-reference method behavior. No value is an
empirical MS effect or universal cohort-size requirement.

## Result

The guarded within-site, site-stratified null family calibrates across ten
cells: maximum false-positive rate `0.0572`, Wilson lower bound `0.0474`, and
family-maximum tail `0.611`.

| event probability | latent HR / SD | minimum analyzable N | conditional gross N under 10% losses at each stage |
|---:|---:|---:|---:|
| 0.15 | 1.2 | not reached by 1,500 | not reached |
| 0.15 | 1.3 | 1,500 | 2,301 |
| 0.15 | 1.5 | 600 | 921 |
| 0.15 | 1.7 | 450 | 690 |
| 0.30 | 1.2 | not reached by 1,500 | not reached |
| 0.30 | 1.3 | 900 | 1,380 |
| 0.30 | 1.5 | 450 | 690 |
| 0.30 | 1.7 | 450 | 690 |

Minimum N requires aggregate positive-direction detection at least `0.80` and
every seed at least `0.75`. At `n=1,500`, HR `1.2` reaches only `0.529` at 15%
events and `0.789` at 30% events, so neither passes the fixed rule.

## Consequence

The prior `n=450` reference is adequate only for effects near the stronger end
of the frozen assumptions and high event yield. It must not be communicated as
a universal target. If the plausible latent association is around HR `1.3`, a
balanced clean design needs approximately 900 analyzable participants at 30%
events or 1,500 at 15% in this generator, before any additional inflation for
informative attendance or other departures.

## Reproduction

```bash
.venv/bin/python scripts/v54_progression_weaker_effect_power.py
```

The run generated 90,000 seeded synthetic cohorts. Configuration, seed-level
results, aggregate grid, null calibration, and minimum-N table are committed
under `analysis/v54_progression_weaker_effect_power/`.

## Boundary

The true effect, event rate, reliability, and ascertainment structure are
unknown. A real package must rerun this route while blinded. These simulations
do not show that a molecular state predicts progression or that any treatment
halts MS.
