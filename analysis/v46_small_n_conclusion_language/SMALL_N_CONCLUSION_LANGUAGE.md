# Small-N Conclusion Language V46

Status: validation-readiness infrastructure. No validation result and no biological claim.

This table converts the frozen V42 interpretation grid, V43/V45 power
planning, and V45 analyzable-pair bands into allowed report wording for
underpowered or partial returned packages. It does not read expression
data, private labels, locked-rule metrics, AUCs, or returned scores.

Generated rows: `6` language bands and `4` synthetic route examples.

## Language Bands

| Band | Min group n | Safe class | Required sentence | Forbidden language |
|---|---:|---|---|---|
| `context_only_or_labels_needed` | `0_or_no_two_label_groups` | `CONTEXT_ONLY_OR_LABELS_NEEDED` | This return is context-only because paired response labels are absent or not mapped; no response-validation result is available. | validated; failed; passed; killed; response-predictive; AUC-based conclusion |
| `below_planning_floor` | `1-9` | `BELOW_V45_PLANNING_FLOOR` | This return is below the V45 planning floor and cannot support pass, fail, or kill language; it is useful only for acquisition repair planning. | clean pass; directional pass; adequate-power fail; kill; validated; clinically useful |
| `small_provisional_effect_size` | `10-14` | `INCONCLUSIVE_SMALL_COHORT` | This small cohort supplies an effect-size and uncertainty estimate; it does not validate or kill the rule. | clean validation; adequate-power kill; clinical readiness; definitive failure from wide CI |
| `small_to_mid_caution` | `15-29` | `INCONCLUSIVE_SMALL_COHORT` | The cohort remains in a small-to-mid planning band; any conclusion is bounded by CI width, diagnostics, and the V42 grid. | breakthrough; clinical deployment; broad DMT generalization; post-hoc rescue by secondary analyses |
| `minimum_decision_grade_caution` | `30-59` | `MINIMUM_DECISION_GRADE_CAUTION` | This cohort reaches the minimum decision-grade planning band only under clean-effect assumptions; the V42 grid and diagnostics determine interpretation. | clinical readiness; unbounded cross-therapy claim; ignoring batch/confounder caveats |
| `preferred_decision_grade` | `60+` | `ELIGIBLE_FOR_PREREGISTERED_INTERPRETATION` | This cohort is in the preferred planning range; interpretation follows the frozen V42 grid and diagnostic caveats. | clinical threshold established; baseline stratifier established; all-MS-DMT generalization |

## Route Examples

The examples use V45 synthetic analyzable-pair cases for method-planning only.

| Case | Route | Min group n | Language band | Required sentence |
|---|---|---:|---|---|
| `gafson_small_complete` | `gafson_dmf_2018` | `12` | `small_provisional_effect_size` | This small cohort supplies an effect-size and uncertainty estimate; it does not validate or kill the rule. |
| `gafson_partial_return` | `gafson_dmf_2018` | `6` | `below_planning_floor` | This return is below the V45 planning floor and cannot support pass, fail, or kill language; it is useful only for acquisition repair planning. |
| `karolinska_small_secondary` | `karolinska_dmf_ros_2019` | `7` | `below_planning_floor` | This return is below the V45 planning floor and cannot support pass, fail, or kill language; it is useful only for acquisition repair planning. |
| `gse228330_context_no_labels` | `gse228330_ocrelizumab_pbmc` | `0` | `context_only_or_labels_needed` | This return is context-only because paired response labels are absent or not mapped; no response-validation result is available. |

## Boundary

This artifact constrains wording only. It does not change `LOCKED_RULE_V22.md`,
the V42 pre-registration, the V42 pass/fail thresholds, or any returned score.
When all gates pass, the V42 interpretation grid remains authoritative.
