# V54 Progression Weaker-Effect Power Extension

Status: frozen before simulation on 2026-07-22T01:21:28Z.

## Purpose And Boundary

The transport reference at analyzable `n=450` was established under a latent
molecular HR of `1.7`. This extension asks how large a clean, balanced,
site-aware cohort would need to be if the true association were weaker. It is
seeded synthetic method behavior only, not an empirical effect estimate or a
universal recruitment target.

## Frozen Grid

- analyzable sample sizes: `450`, `600`, `900`, `1,200`, `1,500`;
- event probabilities before ascertainment: `0.15`, `0.30`;
- molecular HR per latent SD: `1.0`, `1.2`, `1.3`, `1.5`, `1.7`;
- independent seeds: `55301`, `55303`, `55309`;
- `600` cohorts per seed/cell;
- balanced random three-site assignment;
- site baseline HRs `1.50`, `1.00`, `0.67` and assay scales
  `0.50`, `1.00`, `2.00` with fixed offsets;
- score reliability `0.70` and 10% independent score missingness;
- complete event observation and no competing event/switch/dropout process.

The only inferential route is outcome-blind within-site score standardization
plus site-stratified Cox. The naive pooled route is computed by the shared
generator but excluded from power planning.

## Frozen Decision Rules

Null calibration uses the strict-cell plus ten-cell family-maximum rule at
alpha `0.05`. A non-null cell counts only a significant **positive-direction**
call. Minimum analyzable N requires aggregate positive-call probability at
least `0.80` and every seed at least `0.75`, and is reported only if the guarded
null family calibrates.

Conditional gross enrollment applies the already-established `690/450`
inflation under 10% loss at each of molecular, clinical, and site-usable stages,
rounded upward to a multiple of three. It is labeled conditional and not used
when the analyzable minimum is not reached.

## Interpretation

`not_reached` means only that the frozen grid through 1,500 is insufficient.
It does not prove a weaker effect absent. A real package must rerun the design
from blinded event yield, missingness, reliability, site allocation, and
ascertainment metadata.
