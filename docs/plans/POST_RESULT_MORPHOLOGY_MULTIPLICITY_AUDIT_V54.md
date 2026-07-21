# V54 Post-Result Morphology Multiplicity Audit

Status: frozen after the two-lineage critique and before execution. This audit
can only reduce the evidential grade of the sequential morphology analyses.

## Problem

Separate local family corrections were used as the foamy-morphology result
generated successive sensitivities. Those corrections are valid for their
declared local questions but do not control the family-wise error rate across
the complete post-result sequence. Calling the pooled OXPHOS/lysosomal state
robust without auditing that sequence would understate selection risk.

## Frozen Sequential Family

The family contains every inferential endpoint fitted after the first frozen
lesion panels generated the morphology follow-ups:

1. four lysosomal specificity variants (`base`, `resident_adjusted`,
   `mims_adjusted`, `resident_and_mims_adjusted`);
2. two mutually adjusted endpoints (`oxphos`, `lysosomal_unique`);
3. four eligible lesion-stratum transport endpoints (two modules in class 2
   and class 3); and
4. two class-3-minus-class-2 interaction endpoints.

This is exactly 12 tests. The preceding frozen six-module and five-module
lesion panels are not reclassified as post-result tests; they already used
their own prospective family gates. No additional morphology model may be
added to or removed from this audit because of its p-value.

## Frozen Correction

Read each endpoint's committed aggregate donor-wild p-value from its result
table and apply Holm's step-down correction across all 12. Holm is valid under
arbitrary dependence and therefore does not require pretending that null draws
from models with different samples, strata, and design matrices form one
exchangeable max-T matrix. Also report simple Bonferroni p-values as a
transparent sensitivity.

The audit does not refit models, redefine scores, or inspect new biology.

## Interpretation

- A claim-level result retains `post_result_family_supported` status only if
  the specific inferential endpoint needed for that claim has Holm p at most
  0.05 and all original local gates still pass.
- The lysosomal specificity claim requires the fully adjusted model, not a
  more favorable partial-adjustment variant.
- The separable two-endpoint state requires both mutually adjusted endpoints.
- A result failing the global family is downgraded to
  `exploratory_post_result_association`; it is not erased, but it cannot be
  described as robust or gate-passing evidence.

Regardless of correction, no morphology result is progression, disability,
causal, target, or therapeutic-direction evidence.

