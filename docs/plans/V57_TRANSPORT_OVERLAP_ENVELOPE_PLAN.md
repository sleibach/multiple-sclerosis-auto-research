# V57 Trial-Transport Overlap Envelope: Frozen Plan

Status: **frozen before simulation outcomes**

## Purpose

The V57 candidate transport harness failed because two variance-shift
scenarios did not meet the fixed overlap gate. This analysis does not alter
that gate or outcome. It maps the range of synthetic population shift for
which the candidate diagnostic remains eligible.

## Fixed Grid

- source and target `n`: 2,400 each;
- seeds: 57111, 57112, 57113;
- 300 replicates per seed and severity;
- severity `lambda`: 0, 0.25, 0.50, 0.75, 1.00;
- target means interpolate from zero to `(0.35,-0.25,0.20,0.30)`;
- target standard deviations interpolate from one to
  `(1.40,0.70,1.30,0.75)`.

Only covariates and sampling weights are generated. No outcomes, treatments,
or biological quantities are simulated.

## Unchanged Candidate Guard

Quadratic sampling odds are overlap-eligible only when:

- weight effective sample fraction is at least 0.30;
- 99th-percentile-to-median weight ratio is no greater than 12; and
- maximum weighted first/second-moment standardized difference is no greater
  than 0.10.

The envelope endpoint is the largest severity at which every seed has at
least 90% eligible replicates. Report each component's failure rate and do not
interpolate beyond the tested grid.

## Boundary

This is synthetic method behavior, not evidence about any real trial or MS.
Real eligibility must be computed from approved, harmonized participant-level
covariates and cannot be inferred from a trial name or aggregate table.
