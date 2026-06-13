# Safe-Interpretation Example Coverage Linter V46

Status: safe-class coverage governance. No validation result and no biological claim.

Overall status: `PASS`; safe classes: `12`; represented: `6`; explicit non-example reasons: `6`.

| Safe class | Coverage status | Example count | Reason |
|---|---|---:|---|
| `BLOCKED_TERMS_OR_RECEIPT_GATES` | `EXPLICIT_NON_EXAMPLE_REASON` | `0` | Covered by terms-governance, receipt-manifest, first-30 stop-route, and repair-template fixtures; no returned-package interpretation example is permitted. |
| `BLOCKED_REDACTION` | `EXPLICIT_NON_EXAMPLE_REASON` | `0` | Covered by author-run return gate and redaction precheck fixtures; no operator interpretation wording is allowed before redaction passes. |
| `BLOCKED_COMPLETENESS` | `EXPLICIT_NON_EXAMPLE_REASON` | `0` | Covered by unscoreable-return composition and repair-template fixtures; examples stop before safe interpretation when required outputs are missing. |
| `BLOCKED_RETURN_GATE` | `EXPLICIT_NON_EXAMPLE_REASON` | `0` | Covered by command-order and return-gate fixtures; no example should normalize a failed combined gate into result wording. |
| `BLOCKED_SCHEMA` | `EXPLICIT_NON_EXAMPLE_REASON` | `0` | Covered by receipt/schema and result-report linters; malformed aggregate outputs stop before example-card wording. |
| `BLOCKED_METADATA_CONTRADICTION` | `EXPLICIT_NON_EXAMPLE_REASON` | `0` | Covered by report-header metadata and metadata-contradiction guards; contradictory metadata blocks result review. |
| `CONTEXT_ONLY_OR_LABELS_NEEDED` | `EXAMPLE_CARD` | `1` |  |
| `BELOW_V45_PLANNING_FLOOR` | `EXAMPLE_CARD` | `1` |  |
| `INCONCLUSIVE_SMALL_COHORT` | `EXAMPLE_CARD` | `2` |  |
| `MINIMUM_DECISION_GRADE_CAUTION` | `EXAMPLE_CARD` | `1` |  |
| `CAUTION_BATCH_OR_CONFOUNDER` | `EXAMPLE_CARD` | `1` |  |
| `ELIGIBLE_FOR_PREREGISTERED_INTERPRETATION` | `EXAMPLE_CARD` | `1` |  |

Boundary: this linter only checks example coverage accounting. It does not
make blocked safe classes interpretable and does not read score values.
