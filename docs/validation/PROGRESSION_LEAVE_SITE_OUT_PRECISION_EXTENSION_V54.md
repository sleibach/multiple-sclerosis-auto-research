# V54 Upper-Range Per-Site Precision Extension

Status: **conditional HR-1.5 boundary located; HR 1.3 not reached**.

## Boundary

This is the separately frozen follow-up to the completed n<=1,500 precision
grid. It contains seeded synthetic method behavior only. The HRs, event rates,
site allocations, and event counts are assumptions, not estimates from MS.

## Result

The extension generated 72,000 cohorts at total N `1,800`, `2,100`, and
`3,000`, retaining all five effect/control patterns and both event/allocation
regimes. Both null families calibrate. Maximum one-site-only false precision is
`0.00083`; the reversed-site control has zero strict passes.

For homogeneous HR 1.5 and 30% events:

| Total N | Allocation | Strict probability | Minimum seed | Median weakest-site events | Widest site CI half-width | Ready |
|---:|---|---:|---:|---:|---:|---|
| 1,800 | balanced | 0.832 | 0.830 | 102 | 0.195 | yes |
| 1,800 | 60/30/10 | 0.685 | 0.675 | 83 | 0.219 | no |
| 2,100 | balanced | 0.890 | 0.873 | 119 | 0.181 | yes |
| 2,100 | 60/30/10 | 0.772 | 0.758 | 96 | 0.203 | no |
| 3,000 | balanced | 0.930 | 0.923 | 170 | 0.151 | yes |
| 3,000 | 60/30/10 | 0.887 | 0.880 | 137 | 0.170 | yes |

No 15%-event design reaches readiness through `n=3,000`; the best is 0.741
with a minimum seed of 0.713. Homogeneous HR 1.3 also remains below the rule;
its best design is 0.658 at `n=3,000`, 30% events, balanced sites.

## Planning Meaning

Under this generator, balanced HR-1.5/30%-event precision first appears at
`n=1,800`, with a median 102 events at the weakest site and a widest-site CI
half-width near 0.195. Site imbalance delays readiness to `n=3,000`. These are
conditional lookup points, not universal cutoffs and not evidence that the
candidate score has HR 1.5.

The design implication is to plan and monitor blinded per-site event
information, not merely total enrollment. A future real package still must
pass endpoint, confirmation, attendance, competing-risk, treatment-switch,
site-scale, and provenance gates before this lookup is applicable.
