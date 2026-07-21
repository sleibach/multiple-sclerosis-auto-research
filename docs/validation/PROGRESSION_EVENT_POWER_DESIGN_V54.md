# V54 Progression-Event Power Design

## Scope

`scripts/v54_progression_event_power_design.py` is a synthetic, pre-data study-
design simulator for a future frozen molecular association with a binary
progression event. It does not reuse V43 treatment-response power as progression
power and does not estimate an MS effect from held data.

The simulator varies:

- participant count;
- progression-event rate;
- assumed odds ratio per latent molecular-score standard deviation;
- molecular missingness;
- one versus repeated molecular measurements;
- per-measurement reliability;
- outcome label noise;
- alpha and random seeds.

It calibrates the logistic intercept to the requested marginal event rate,
simulates noisy repeated molecular measurements, fits a single pre-specified
logistic Wald test, requires positive direction for non-null effects, and counts
cohorts with fewer than five events or non-events as inconclusive. Three seeds
are required. Wilson intervals and per-seed ranges quantify simulation error.

## Default Run

```bash
.venv/bin/python scripts/v54_progression_event_power_design.py
```

The default is an assumption grid, not a recommended cohort specification.
After a package arrives but before any score is viewed, rerun with the package's
blinded event rate, missingness, and repeat structure:

```bash
.venv/bin/python scripts/v54_progression_event_power_design.py \
  --sample-sizes 60,80,100,120,160,200,240,320 \
  --event-rates 0.12 \
  --odds-ratios 1.0,1.25,1.5,2.0 \
  --missing-rates 0.18 \
  --molecular-repeats 2 \
  --measurement-reliability 0.70 \
  --replicates-per-seed 2000 \
  --output-dir analysis/<package>_blinded_progression_power
```

An event rate may be calculated from blinded outcome labels, but no expression
score or outcome-by-score relationship may be viewed first.

## Interpretation Boundary

The minimum-N table reports when a *specified synthetic effect* reaches 80%
conclusive probability under the simulated model. The true effect is unknown;
event definitions and longitudinal dependence vary; covariate estimation and
competing risks are not represented in the default model. Therefore:

- `not_reached` means only that the simulated grid through its largest N was
  insufficient for that assumption;
- a reached N is not a universal recruitment target;
- no synthetic power result is evidence about MS biology;
- a cohort-specific pre-registration must define endpoint, censoring,
  covariates, repeated-measures handling, and multiplicity separately.

The outputs are under `analysis/v54_progression_event_power_design/` and are
permanently labeled synthetic.
