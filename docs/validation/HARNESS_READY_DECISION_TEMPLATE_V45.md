# Harness-Ready Decision Template V45

Status: readiness decision template. No validation is run by this template.

Purpose: convert gate statuses into a binary decision about whether the frozen
harness may run.

Machine-readable template:

`docs/validation/input_schemas/V45_harness_ready_decision_template.tsv`

## Decision Rule

The harness may run only if every required gate is `PASS` or explicitly `NA` by
the applicable preregistration. Any `FAIL`, `TODO`, `UNKNOWN`, or unresolved
blocker means `harness_ready=no`.

For response-validation packages, `outcome_dictionary` and
`preregistration_or_addendum` are mandatory. For context-only packages,
response-validation gates are `NA`, and no response claim is allowed.

## Required Decision Fields

| Field | Meaning |
|---|---|
| `gate` | named gate from first-24h/status templates |
| `required_for_mode` | `yes`, `no`, or mode-specific condition |
| `status` | `PASS`, `FAIL`, `NA`, `TODO`, or `UNKNOWN` |
| `evidence_path` | file supporting status |
| `decision_effect` | how failure affects harness readiness |

## Final Decision Text

Use exactly one:

```text
harness_ready=yes; all required gates passed under the applicable frozen plan.
```

```text
harness_ready=no; [gate] is [status], so no validation has occurred.
```

## Guardrail

A favorable-looking partial metric cannot override a failed readiness gate. If
the harness was run before this decision was complete, report the run as
procedurally invalid.
