# Wave108 MFGE8-Like Debris-Opsonin Safety-Window Model

## Bottom Line

Branch call: `MFGE8_LOCAL_OPSONIN_NO_THEORETICAL_SAFETY_WINDOW`.

This is a simulation-only stress test. It does not show that MFGE8 works in MS.
It quantifies what must be true for a local MFGE8-like opsonin to be plausible:
debris uptake must improve while viable-neuron/oligodendrocyte bystander uptake
and inflammatory lipid overload remain bounded.

## Safety Window Summary

| selectivity_debris_over_viable | n_safe_dose_affinity_points | safe_fraction | min_safe_debris_affinity | max_safe_dose | best_p10_debris_clearance_gain | best_p90_viable_lost | best_p90_cytokine_fold |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 0 |  |  | 1.535 | 0.9919 | 0.7986 |
| 1.334 | 0 | 0 |  |  | 1.522 | 0.9725 | 0.785 |
| 1.778 | 0 | 0 |  |  | 1.52 | 0.9623 | 0.7828 |
| 2.371 | 0 | 0 |  |  | 1.532 | 0.8624 | 0.8381 |
| 3.162 | 0 | 0 |  |  | 1.525 | 0.7939 | 0.7947 |
| 4.217 | 0 | 0 |  |  | 1.531 | 0.9349 | 0.7916 |
| 5.623 | 0 | 0 |  |  | 1.521 | 0.8283 | 0.7615 |
| 7.499 | 0 | 0 |  |  | 1.53 | 0.7576 | 0.7753 |
| 10 | 0 | 0 |  |  | 1.504 | 0.3461 | 0.8159 |
| 13.34 | 0 | 0 |  |  | 1.517 | 0.3384 | 0.7867 |
| 17.78 | 0 | 0 |  |  | 1.596 | 0.3104 | 0.8123 |
| 23.71 | 0 | 0 |  |  | 1.496 | 0.3193 | 0.7885 |
| 31.62 | 0 | 0 |  |  | 1.518 | 0.3069 | 0.7491 |
| 42.17 | 0 | 0 |  |  | 1.515 | 0.1689 | 0.7848 |
| 56.23 | 0 | 0 |  |  | 1.496 | 0.1037 | 0.828 |
| 74.99 | 0 | 0 |  |  | 1.519 | 0.1547 | 0.773 |
| 100 | 0 | 0 |  |  | 1.548 | 0.07588 | 0.8041 |
| 133.4 | 0 | 0 |  |  | 1.525 | 0.07048 | 0.7726 |
| 177.8 | 0 | 0 |  |  | 1.522 | 0.09447 | 0.7746 |
| 237.1 | 0 | 0 |  |  | 1.501 | 0.05837 | 0.7544 |
| 316.2 | 0 | 0 |  |  | 1.515 | 0.04632 | 0.8042 |
| 421.7 | 0 | 0 |  |  | 1.534 | 0.0438 | 0.803 |
| 562.3 | 0 | 0 |  |  | 1.581 | 0.04557 | 0.7784 |
| 749.9 | 0 | 0 |  |  | 1.545 | 0.04623 | 0.77 |
| 1000 | 0 | 0 |  |  | 1.538 | 0.0383 | 0.8092 |

## Best Safe Parameter Points

_No parameter point passed the safety window._

## Assumptions

- State variables are normalized, not fitted to wet-lab kinetics.
- Safety window requires p10 debris-clearance gain >= 2.0, p90 viable loss <=
  5%, and p90 cytokine proxy <= 1.20 across parameter uncertainty.
- Opsonin action is local; systemic exposure is not modeled and remains a
  blocker.
- The model treats viable bystander recognition as the decisive unknown. If an
  engineered molecule cannot make viable-cell affinity much lower than debris
  affinity, the route fails before efficacy testing.

## Interpretation

The output is useful only as a wet-lab design constraint. A pass means an
engineered-local MFGE8-like molecule has a theoretical safety window worth
testing ex vivo. It is not evidence of clinical efficacy, target engagement, or
novelty.

## Reproducibility

- Script: `scripts/v3_wave108_mfge8_debris_opsonin_safety_window_model.py`
- Wave54 gate matrix: `results_v3/wave54_mfge8_debris_opsonin_audit/decision_matrix.tsv`
- Grid output: `results_v3/wave108_mfge8_debris_opsonin_safety_window_model/mfge8_safety_window_grid.tsv`
- Summary output: `results_v3/wave108_mfge8_debris_opsonin_safety_window_model/mfge8_selectivity_summary.tsv`
- Seed: `20260527`
