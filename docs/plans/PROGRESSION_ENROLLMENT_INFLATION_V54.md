# V54 Progression Enrollment-Inflation Plan

Status: frozen before simulation on 2026-07-22T00:20:10Z.

## Boundary

This seeded synthetic design audit translates the existing V54 prospective
reference into gross-enrollment requirements under data loss. It tests study-
planning behavior only. It does not estimate an MS effect, observed event rate,
dropout rate, or universal sample size, and it changes no locked rule or frozen
pre-registration.

## Fixed Reference Targets

The prior multisite audit found transport only in the assumption-labeled
balanced `n=450`, event-probability `0.30` design. This audit therefore retains,
rather than re-optimizes:

- at least 450 analyzable participants overall;
- at least 150 analyzable participants at each of three sites;
- at least 135 confirmed progression events overall;
- at least 10 confirmed events at each site.

An analyzable participant has an available molecular score and retained
endpoint follow-up. A confirmed event additionally has the fixed synthetic
event probability and survives confirmation loss. The factors are independent
in this planning generator; departures from independence require the existing
informative-attendance and event-time sensitivity gates.

## Frozen Grid

Equal site quotas are simulated over:

- nonterminal follow-up loss: `0.0`, `0.1`, `0.2`;
- molecular-score missingness: `0.0`, `0.1`, `0.2`;
- event-confirmation loss: `0.0`, `0.1`, `0.2`;
- latent event probability among retained participants: `0.15`, `0.30`;
- gross enrollment per site: 150 through 800 in steps of 5;
- three fixed seeds and 5,000 replicates per cell.

For each scenario, the minimum gross enrollment is the first candidate at
which the 95% Wilson lower bound for joint-target attainment is at least 90%
in **every** seed. Failure by 2,400 total enrollees is reported as outside the
searched range, not impossible.

A separate passive-recruitment stress test fixes 10% loss in each channel and
event probability 0.30, then compares balanced, `45/35/20`, and `60/30/10`
site shares. It finds the gross total needed to clear count/event floors but
labels every unequal allocation `OUTSIDE_TESTED_BALANCED_REFERENCE` regardless
of assurance. Over-enrollment cannot establish transport under an allocation
the prior audit did not validate.

## Frozen Verdicts

- `REFERENCE_COUNTS_REACHED_WITHIN_GRID`: every seed reaches 90% assurance.
- `REFERENCE_COUNTS_NOT_REACHED_WITHIN_GRID`: at least one seed remains below
  90% at the maximum enrollment.
- `OUTSIDE_TESTED_BALANCED_REFERENCE`: passive unequal recruitment may clear
  arithmetic floors but cannot inherit the balanced transport result.

All output must state that it is seeded synthetic planning behavior only.
