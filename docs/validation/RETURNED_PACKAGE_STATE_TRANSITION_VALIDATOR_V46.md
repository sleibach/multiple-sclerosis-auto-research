# Returned-Package State-Transition Validator V46

Status: synthetic/software readiness only. No validation result and no biological claim.

Purpose: freeze and test the returned-package state machine from receipt through terms, format, completeness/schema, label coverage, safe-class assignment, and report readiness. This is a guard against premature score reading or result wording when a real author-returned package arrives.

## Current Run

Command:

```bash
.venv/bin/python scripts/v46_returned_package_state_transition_validator.py --outdir analysis/v46_returned_package_state_transition_validator --fail-on-error
```

Result:

- overall status: `PASS`
- synthetic scenarios: `8`
- states: `19`
- allowed edges: `25`
- scenario transition rows: `56`
- lint checks: `79`
- lint failures: `0`
- forbidden shortcut checks: `14`
- premature score paths: `0`
- premature report paths: `0`

## Boundary

The validator allows clean result-report states only after:

1. receipt is logged without interpreting package content;
2. terms permit the returned-package route;
3. aggregate format is canonical or normalized through the adapter;
4. redaction/completeness gate passes;
5. aggregate schema validation passes;
6. analyzable-pair and response-label coverage are classified;
7. the V46 safe-interpretation class is assigned.

Blocked paths may reach only `REPAIR_REQUEST_READY` or `RESTRICTED_LANGUAGE_READY`. Those states do not permit score interpretation.

## Outputs

- `analysis/v46_returned_package_state_transition_validator/returned_package_state_transition_summary.json`
- `analysis/v46_returned_package_state_transition_validator/returned_package_states.tsv`
- `analysis/v46_returned_package_state_transition_validator/returned_package_allowed_transitions.tsv`
- `analysis/v46_returned_package_state_transition_validator/returned_package_state_transition_scenarios.tsv`
- `analysis/v46_returned_package_state_transition_validator/returned_package_state_transition_lint.tsv`
- `analysis/v46_returned_package_state_transition_validator/RETURNED_PACKAGE_STATE_TRANSITION_VALIDATOR.md`

The script reads no real cohort data, returned scores, expression matrices, labels, or quarantined packages.
