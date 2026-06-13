# Returned-Package State-Transition Validator V46

Status: synthetic/software readiness only. No validation result and no biological claim.

This validator freezes the allowed route from package receipt to report readiness.
It checks that a returned package cannot reach a report or score-reading state before
terms, format, completeness/schema, label coverage, and the V46 safe-interpretation
class have been resolved.

Overall status: `PASS`.
Synthetic scenarios: `8`; scenario transitions: `56`; lint failures: `0`.
Forbidden shortcut checks: `14`.

| Scenario | Terminal state | Score states before safe class | Report states before safe class |
|---|---|---:|---:|
| `batch_or_confounder_caution` | `REPORT_READY_WITH_CAUTION` | `0` | `0` |
| `labels_below_floor` | `RESTRICTED_LANGUAGE_READY` | `0` | `0` |
| `schema_blocked` | `REPAIR_REQUEST_READY` | `0` | `0` |
| `scored_canonical_clean` | `REPORT_READY` | `0` | `0` |
| `scored_noncanonical_clean` | `REPORT_READY` | `0` | `0` |
| `terms_blocked` | `REPAIR_REQUEST_READY` | `0` | `0` |
| `unknown_alias_branch_clean` | `REPORT_READY` | `0` | `0` |
| `unscoreable_completeness_block` | `REPAIR_REQUEST_READY` | `0` | `0` |

The validator intentionally permits only restricted-language or repair-request
states for blocked paths. Clean result reports are reachable only after
`SAFE_CLASS_ASSIGNED`.
