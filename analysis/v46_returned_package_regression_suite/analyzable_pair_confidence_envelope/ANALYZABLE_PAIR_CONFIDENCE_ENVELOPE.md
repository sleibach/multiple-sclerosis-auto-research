# Analyzable-Pair Confidence Envelope V46

Status: validation-readiness planning artifact. No validation result and no biological claim.

This artifact maps response-labeled analyzable-pair counts to allowed
pass/fail/inconclusive wording using the V43 synthetic power map and V45
analyzable-pair bands. It reads no returned scores or private labels.

Overall status: `PASS`.
Envelope bands: `7`; representative power rows: `35`; lint failures: `0`.

| Band | Min group n | Large clean pass range | Moderate noisy immune pass range | Allowed conclusion boundary |
|---|---:|---:|---:|---|
| `no_mapped_response_groups` | `0_or_single_class` | `0.417-0.917` | `0.000-0.500` | No response-validation conclusion is available because mapped responder and nonresponder groups are absent. |
| `below_planning_floor` | `1-9` | `0.417-0.917` | `0.000-0.500` | The labeled return is below the V45 planning floor; no pass, fail, kill, or response-predictive language is allowed. |
| `gafson_sized_effect_estimate_only` | `10-14` | `0.500-0.583` | `0.333-0.333` | This small return supplies an effect-size and uncertainty estimate only; it does not validate or kill the rule. |
| `small_to_mid_caution` | `15-29` | `0.417-0.667` | `0.083-0.333` | This return is in a small-to-mid planning band; the V42 class, CI width, and diagnostics bound any conclusion. |
| `minimum_decision_grade` | `30-59` | `0.667-0.917` | `0.167-0.500` | This cohort reaches the minimum decision-grade planning band only under clean-effect assumptions; diagnostics remain decisive. |
| `preferred_decision_grade` | `60-80` | `0.750-0.917` | `0.000-0.083` | This cohort is in the preferred planning range; interpretation follows the frozen V42 grid and diagnostic caveats. |
| `beyond_simulated_grid` | `>80` | `0.417-0.917` | `0.000-0.500` | This return exceeds the V43 simulated grid; apply the frozen V42 grid but do not quote a simulated power rate without extending the grid. |

## Synthetic Route Examples

| Case | Min group n | Confidence band | Required wording |
|---|---:|---|---|
| `gafson_small_complete` | `12` | `gafson_sized_effect_estimate_only` | This small return supplies an effect-size and uncertainty estimate only; it does not validate or kill the rule. |
| `gafson_partial_return` | `6` | `below_planning_floor` | The labeled return is below the V45 planning floor; no pass, fail, kill, or response-predictive language is allowed. |
| `karolinska_small_secondary` | `7` | `below_planning_floor` | The labeled return is below the V45 planning floor; no pass, fail, kill, or response-predictive language is allowed. |
| `gse228330_context_no_labels` | `0` | `no_mapped_response_groups` | No response-validation conclusion is available because mapped responder and nonresponder groups are absent. |

## Boundary

This table constrains interpretation only. It does not change the locked V22 rule,
the frozen V42 pre-registration, or any V43/V45 simulation result. Simulated
rates are planning evidence about method behavior, not biological evidence.
