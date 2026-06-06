# V27 Build Queue

Session objective: construct and fairly evaluate fixed coupled APC-axis representations against the immutable V22 scalar rule, then prepare a frozen validation harness for future fresh cohorts.

## Queue

| Step | Status | Action | Output |
|---|---|---|---|
| 1 | completed | Verify OpenGWAS token, read V26/V22/V23 state, check for fresh cohort quarantine need. | Console preflight; no Gafson/NEDA fresh cohort found. |
| 2 | completed | Define coupled-axis representations before response comparison. | `docs/workups/treatment_response/COUPLED_AXIS_V27.md` |
| 3 | completed | Run parameter-count-aware scalar-vs-coupled comparison with cross-validation-style fixed-feature evaluation and response-label permutation null. | `analysis/v27_coupled_axis/` |
| 4 | completed | Decide whether `LOCKED_RULE_V27.md` is warranted. | Not warranted; no lock written. |
| 5 | completed | Prepare future validation harness and data-format spec. | `scripts/v27_apply_locked_rules.py`, `docs/validation/VALIDATION_READINESS_V27.md` |
| 6 | completed | Update resume state, README, session log, RAG index, commit. | checkpoint commit |

## Guardrails

- `docs/locked_rules/LOCKED_RULE_V22.md` is immutable.
- No fresh Gafson/NEDA cohort is present; if one appears in a future run it must be quarantined before any rule work.
- V27 uses `delta_RECEPTOR` (`CD74`, `CD44`, `CXCR4`) as the only available MIF/CD74 receptor-state proxy in V22/V23 paired-score tables.
- Coupled features are fixed from V22/V26 biology and are not fit to response labels.
- A successor lock requires a coupled feature to beat the V22 scalar in the bounded domain after multi-feature label-permutation null accounting.
