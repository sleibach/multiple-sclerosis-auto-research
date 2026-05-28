# Convergence Check 85 - Wave131 Class-Route Forcing

## Question

After Wave130 ruled out an MS treatment-response rescue for IL1B/LAMP3 and
lipid-lysosomal modules, do any least-bad intervention classes reopen as
target-search routes?

## Classes Tested

- `eicosanoid_receptors`
- `retinoid_vdr_rxr`
- `MED16_MEDIATOR_MODULE`
- `GALC_LYSOSOMAL_SPHINGOLIPID`

## Result

Branch call:

- `NO_CLASS_ROUTE_REOPENED_AFTER_WAVE130`

Gate summary:

- `eicosanoid_receptors`: 4/8 gates, no reopen.
- `retinoid_vdr_rxr`: 3/8 gates, no reopen.
- `MED16_MEDIATOR_MODULE`: 4/8 gates, no reopen.
- `GALC_LYSOSOMAL_SPHINGOLIPID`: 4/8 gates, no reopen.

## Interpretation

Reachable chemical matter is not enough. These classes fail because the missing
gates are the decisive ones: target-resolution genetics, MS anchor/response
rescue, prior-art freedom, direction/safety, and specificity.

This preserves a strict boundary between:

- plausible immunology classes, and
- a V3 therapeutic nomination.

## Decision

Do not reopen any Gibbs sidecar class route. The next forcing question is the
last Wave83 route parked rather than no-go: `GPR183_EBI2_OXYSTEROL_NICHE`,
checked against later GPR183 closure waves.

## Reproducibility

- Script: `scripts/v3_wave131_class_route_forcing_audit.py`
- Output: `results_v3/wave131_class_route_forcing_audit/`
- Seed: `20260527`
