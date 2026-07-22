# V54 Progression Site-Score Harmonization Plan

Status: frozen before simulation on 2026-07-22T00:06:17Z.

## Boundary

This seeded synthetic audit tests whether site-specific assay scale can defeat
multi-site transport and whether a blinded within-site normalization restores
the intended estimand. It is method behavior only, not evidence about MS,
assay platforms, site quality, progression, or a molecular effect. It does not
change a locked rule or pre-registration.

## Fixed Generator

Three sites retain the baseline hazard multipliers `0.6, 1.0, 1.8` and score
offsets `-0.8, 0.0, 0.8`. Total sample size is `180, 300, 450`, allocation is
balanced or `60/30/10`, and cumulative event probability is `0.15` or `0.30`.
The true within-site molecular state has reliability 0.70 before site scaling,
with 10% independent score missingness.

Assay scale patterns are:

1. `uniform`: `1.0, 1.0, 1.0`;
2. `moderate`: `0.7, 1.0, 1.4`;
3. `severe`: `0.5, 1.0, 2.0`.

Molecular-effect patterns are `null` (`1.0,1.0,1.0`), `homogeneous`
(`1.7,1.7,1.7`), and `one_site_reversed` (`1.7,1.7,0.6`). Independent
progression frailty is included. Three fixed seeds and 400 replicates per cell
are used.

## Frozen Routes And Decisions

Both routes stratify the Cox score test by site:

- `global_scale`: globally standardize the received score once;
- `within_site_scale`: standardize score within each predeclared site using
  all score-available participants, without reading outcomes.

For each route report null calibration, global association, signed site
estimates, leave-site-out tests, heterogeneity, minimum site events, and the
same full transport gate used in the prior multi-site audit. Within-site
standardization is eligible only when site labels and the transformation are
frozen before outcome-score inspection.

- Null calibration uses the Wilson lower-bound and fixed-family maximum rule.
- A homogeneous effect is transport-supported only under the complete prior
  gate: positive global test, every site estimate positive, every leave-site-
  out test positive, at least 10 events/site, and heterogeneity p at least 0.05.
- The reversed effect is a negative control; transport pass above 0.05 fails a
  design.
- A harmonization gain requires at least 0.10 absolute transport-pass increase
  over global scaling in aggregate and every seed, without a null-calibration
  failure or reversed-effect false transport above 0.05.
- No outcome-driven site merging, batch correction, transform selection, or
  exclusion is allowed. A transformation cannot rescue an unknown site map.

All outputs must state that they are synthetic method behavior only.
