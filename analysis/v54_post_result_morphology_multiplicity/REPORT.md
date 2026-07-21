# V54 Post-Result Morphology Multiplicity Audit

Verdict: **post_result_claims_downgraded_to_exploratory**.

The complete sequential family contains 12 post-result tests. Holm correction is applied to the committed aggregate donor-wild p-values and is valid under arbitrary dependence. It is intentionally broader than each original local family.

| family | endpoint | raw wild p | local-family p | Holm p (12) | local+global pass |
|---|---|---:|---:|---:|---|
| lysosomal_specificity | base | 0.00463 | 0.05962 | 0.05089 | false |
| lysosomal_specificity | resident_adjusted | 0.00121 | 0.00121 | 0.01448 | true |
| lysosomal_specificity | mims_adjusted | 0.01246 | 0.18894 | 0.09597 | false |
| lysosomal_specificity | resident_and_mims_adjusted | 0.00861 | 0.04526 | 0.08610 | false |
| mutual_adjustment | oxphos | 0.01066 | 0.01138 | 0.09597 | false |
| mutual_adjustment | lysosomal_unique | 0.01077 | 0.05183 | 0.09597 | false |
| lesion_stratum_transport | class_2:oxphos | 0.27708 | 0.81685 | 1.00000 | false |
| lesion_stratum_transport | class_2:lysosomal_unique | 0.94204 | 0.99999 | 1.00000 | false |
| lesion_stratum_transport | class_3:oxphos | 0.14845 | 0.16579 | 0.89072 | false |
| lesion_stratum_transport | class_3:lysosomal_unique | 0.29707 | 0.73910 | 1.00000 | false |
| lesion_class_interaction | oxphos | 0.78972 | 0.94039 | 1.00000 | false |
| lesion_class_interaction | lysosomal_unique | 0.98892 | 0.99993 | 1.00000 | false |

The fully adjusted lysosomal specificity endpoint has Holm `p=0.0861` and therefore does not retain the claim-level gate. The mutually adjusted OXPHOS and lysosomal endpoints have Holm `p=0.0960` and `p=0.0960`; the two-endpoint state also does not retain global family support.

One partial-adjustment specificity variant may pass globally, but it is not the fully adjusted endpoint required for the specificity claim. The pooled coefficients remain descriptive post-result associations; they must now be called exploratory rather than robust or gate-passing.

No conclusion about progression, disability, metabolic or lysosomal flux, causality, or intervention direction follows from this audit.
