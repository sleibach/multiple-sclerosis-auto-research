# V54 Progression Leave-Site-Out Precision Plan

Status: frozen before simulation on 2026-07-22T01:42:02Z.

## Boundary

This seeded synthetic audit characterizes when a multi-site molecular
association is individually precise at every site rather than merely retaining
the same sign. It estimates no MS effect, event rate, site distribution, or
biological transportability. It changes no locked rule or pre-registration.

## Frozen Generator

- total analyzable N: `450`, `600`, `900`, `1,500`;
- cumulative event probability: `0.15` or `0.30`;
- three sites with baseline hazard multipliers `0.6/1.0/1.8`;
- balanced or `60/30/10` site allocation;
- score reliability `0.70`, 10% independent missingness, and deliberately
  different assay scales `0.5/1/2` plus offsets;
- blind within-site standardization and site-stratified inference;
- three fixed seeds and 400 cohorts per seed/cell.

Five fixed effect patterns are evaluated: null; homogeneous HR `1.3`;
homogeneous HR `1.5`; HR `1.5` at one site only; and HR `1.5/1.5/0.667`
across sites. The last two are false-transport controls.

## Frozen Precision Gate

For every replicate, compute site-specific score/information one-step log-HR
estimates and approximate 95% confidence intervals, the global site-stratified
test, all three leave-one-site-out estimates/intervals, and the fixed-effect
heterogeneity test.

The existing sign transport gate requires a positive significant global test,
positive estimates at all sites, positive significant leave-one-site-out
tests, at least ten events per site, and no detected heterogeneity. The stricter
precision gate additionally requires the lower 95% confidence bound to exceed
zero at **every individual site**. A design is precision-ready only if this
strict pass rate is at least `0.80` aggregate and `0.75` in every seed, while
both context controls pass at most `0.05`.

Null calibration precedes readiness interpretation. Invalid null families are
excluded rather than described as powered. Report minimum site events and the
widest site CI half-width descriptively; do not turn a simulated median into a
universal clinical cutoff.
