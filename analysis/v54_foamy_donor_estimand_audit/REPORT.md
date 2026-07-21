# V54 Foamy Morphology Donor-Estimand Audit

Verdict: **within_donor_estimand_not_supported**.

Only 6/21 donors contain both morphology labels and only 3/43 donor-by-lesion blocks contain both labels. A donor-by-lesion Fisher test would be invalid for these repeated, multi-category observations; the frozen audit instead uses donor fixed effects.

| endpoint | within-donor beta | HC3 CI | wild p | max-T p | informative LODO range | outcome |
|---|---:|---:|---:|---:|---:|---|
| oxphos | -0.184 | -1.941 to 1.573 | 0.5631 | 0.7189 | -1.614 to 0.422 | direction_retained_but_underpowered |
| lysosomal_unique | -0.057 | -1.884 to 1.770 | 0.8142 | 0.9385 | -0.390 to 1.256 | substantially_between_donor_or_unresolved |

The three same-donor, same-lesion blocks are descriptive only; the minimum possible exact two-sided sign p-value is 0.25. Direction matches by endpoint: oxphos 1/3, lysosomal_unique 2/3.

Donor-deletion changes for the earlier lesion interaction remain an influence diagnostic. A sign flip around an interaction already near zero does not establish donor-specific heterogeneity.

This audit cannot restore the global family gate or support progression, disability, causal, flux, target, or therapeutic claims.
