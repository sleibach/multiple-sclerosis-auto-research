# Partial-Label Repair Prioritization V46

Status: validation-readiness infrastructure. No validation result and no biological claim.

This generated table maps partial-label returned-package classes to the
pre-existing analyzable-pair confidence bands and safe repair-request templates.

Overall status: `PASS`; rows: `7`; lint failures: `0`.

| Case | Class | Priority | Confidence band | Primary template | Status |
|---|---|---|---|---|---|
| `full_small` | `FULL_LABELS_SMALL_COHORT` | `P3` | `gafson_sized_effect_estimate_only` | `batch_or_confounder_metadata_needed` | `PASS` |
| `partial_below_floor` | `PARTIAL_LABELS_BELOW_PLANNING_FLOOR` | `P1` | `below_planning_floor` | `below_planning_floor_labeled_pairs` | `PASS` |
| `context_no_labels` | `RESPONSE_LABELS_ABSENT_CONTEXT_ONLY` | `P0` | `no_mapped_response_groups` | `response_labels_absent_or_unmapped` | `PASS` |
| `partial_effect_size_only` | `PARTIAL_LABELS_EFFECT_SIZE_ONLY` | `P2` | `gafson_sized_effect_estimate_only` | `below_planning_floor_labeled_pairs` | `PASS` |
| `partial_limited_decision` | `PARTIAL_LABELS_LIMITED_DECISION_CAUTION` | `P3` | `small_to_mid_caution` | `batch_or_confounder_metadata_needed` | `PASS` |
| `single_class_block` | `SINGLE_CLASS_LABELS_BLOCK_RESPONSE_VALIDATION` | `P0` | `no_mapped_response_groups` | `response_labels_absent_or_unmapped` | `PASS` |
| `too_few_one_arm` | `PARTIAL_LABELS_TOO_FEW_OR_SINGLE_ARM` | `P0` | `below_planning_floor` | `below_planning_floor_labeled_pairs` | `PASS` |

Boundary: priorities are repair-routing priorities only. They do not
authorize pass/fail, AUC, effect-size, or clinical interpretation.
