# Convergence Check 86 - Wave132 GPR183 Closure

## Question

Does the only Wave83 parked class route, `GPR183_EBI2_OXYSTEROL_NICHE`, remain
open after later GPR183 forcing tests and Wave130 MS treatment-response data?

## Result

Branch call:

- `NO_REOPEN_GPR183_AFTER_POST_WAVE130_AUDIT`

Evidence:

- Wave83 parked the route but did not promote it.
- Wave93 has an integrated row but no promotional call.
- Wave111: `NO_REOPEN_GPR183_SPATIAL_PROXY`.
- Wave112: `NO_REOPEN_GPR183_COMPARTMENT_FALLBACK`.
- Wave112 coherent compartment diseases: 0.
- Wave130 lipid-lysosomal MS response rescue: false.

## Decision

Close GPR183/EBI2 for the current V3 session. It remains biologically plausible
as oxysterol niche biology, but the route lacks coherent spatial/compartment
support, target-level genetics, and MS response rescue.

## Reproducibility

- Script: `scripts/v3_wave132_gpr183_post_wave130_closure.py`
- Output: `results_v3/wave132_gpr183_post_wave130_closure/`
- Seed: `20260527`
