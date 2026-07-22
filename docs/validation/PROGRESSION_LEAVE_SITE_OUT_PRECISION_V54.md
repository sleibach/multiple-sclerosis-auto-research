# V54 Progression Leave-Site-Out Precision Audit

Status: **no tested design is per-site precision-ready**.

## Boundary

This is a seeded synthetic method audit, not evidence about an MS molecular
effect or a universal sample-size requirement. The design was frozen before
simulation in `docs/plans/PROGRESSION_LEAVE_SITE_OUT_PRECISION_V54.md` and ran
from `scripts/v54_progression_leave_site_out_precision.py`.

## Result

The run generated 96,000 synthetic cohorts over three seeds, five effect
patterns, four total sample sizes (`450` to `1,500`), two event regimes, and
balanced versus 60/30/10 site allocation. Both the global-positive and strict-
precision null families calibrate. The strict-null maximum is `0.00083`, and
the maximum strict false-transport rate is `0.00083` in each context control.

No homogeneous design reaches the frozen aggregate `0.80` plus every-seed
`0.75` precision rule. The best tested design is homogeneous HR 1.5,
`n=1,500`, 30% events, balanced sites:

- sign-based transport probability: `0.950`;
- strict every-site-CI probability: `0.740`;
- minimum-seed strict probability: `0.735`;
- median minimum site events: `85`;
- median widest site 95% CI half-width: `0.214` log-HR units.

The 60/30/10 version reaches only `0.593` strict precision despite `0.932`
sign-based transport. At 15% events, HR 1.5 strict precision is `0.337`
balanced and `0.309` imbalanced at `n=1,500`. Homogeneous HR 1.3 reaches at
most `0.222`.

## Interpretation

The earlier synthetic transport result is not retracted: it demonstrated that
a positive global association can retain direction under site omission. This
audit shows that direction stability is materially weaker than precise
site-by-site estimation. An `n=450`, 30%-event balanced design may support the
former under a strong HR-1.7 assumption, but it cannot be represented as
individually precise at every site.

Even 85 median events at the weakest site leave the HR-1.5 precision design
just below the frozen gate. That number is descriptive under this generator,
not a clinical cutoff. A separately frozen extension above `n=1,500` is needed
to locate the conditional boundary; HR 1.3 remains far from precision-ready.

Future reports must distinguish three claims: positive pooled association,
sign-transport under site omission, and every-site precision. Only the last
supports a statement that each contributing site estimates the same positive
association with a confidence interval excluding the null.
