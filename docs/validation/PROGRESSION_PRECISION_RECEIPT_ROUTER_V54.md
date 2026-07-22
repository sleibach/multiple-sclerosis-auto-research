# V54 Progression Precision Receipt Router

Status: additive blinded planning tool. It changes no endpoint, primary model,
locked rule, or pre-registration.

## Purpose

The V54 synthetic grids distinguish global sign transport from individually
precise estimates at every site. This router prevents a returned package from
being described with the stronger term merely because its total enrollment is
large. It reads aggregate design metadata only; effect estimates, p-values,
individual outcomes, and molecular values are forbidden.

## Routes

| route | bounded alignment | meaning |
|---|---|---|
| `TESTED_SIGN_REFERENCE_REQUIRES_COHORT_SIMULATION` | predeclared HR-1.7 planning assumption, balanced 3-site design, N>=450, event fraction>=0.30, minimum 26 events/site | eligible to rerun sign-transport simulation; not transport evidence |
| `TESTED_PRECISION_REFERENCE_REQUIRES_COHORT_SIMULATION` | predeclared HR-1.5 planning assumption and either balanced N>=1,800/min 102 events/site or 60/30/10 N>=3,000/min 137 events/site, event fraction>=0.30 | eligible to rerun every-site-precision simulation; not precision evidence |
| `VALID_OUTSIDE_TESTED_REFERENCE_REPARAMETERIZE` | valid aggregate metadata outside those cells | freeze and run a package-specific simulation; no reference-alignment claim |
| `FAIL_CLOSED` | malformed/inconsistent counts, declared allocation not matching blinded counts, forbidden information, prior access, or no frozen assumption | no planning interpretation |

The numeric values are synthetic reference-cell descriptors, not universal
cutoffs. Meeting them cannot substitute for the cohort-specific simulation,
site-stratified primary model, signed site estimates, leave-site-out analysis,
or observed confidence intervals.

## Machine Check

```bash
.venv/bin/python scripts/v54_progression_precision_receipt_router.py
```

Eleven synthetic declarations test two precision alignments, one sign alignment,
three valid reparameterization routes, and five fail-closed routes. No patient
data or biological claim is involved.
