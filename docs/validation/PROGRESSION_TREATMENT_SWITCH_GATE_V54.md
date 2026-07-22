# V54 Progression Treatment-Switch Receipt Gate

Status: additive blind-committed guard. It does not alter a locked rule,
endpoint, or frozen progression analysis.

## Purpose

The V54 synthetic estimand audit showed that treatment-policy and censor-at-
switch routes can diverge materially and that joint molecular-state/progression-
risk switching invalidates direct prognostic interpretation under both. This
gate requires the estimands and switch metadata to be frozen before molecular
scores or individual outcomes are accessed.

## Required Declaration

The declaration binds a package ID to exact protocol, treatment, switch-date,
switch-reason, indication/context, and censoring sources. It must specify:

- whether switching occurred and a blinded aggregate switch count;
- one primary estimand (`treatment_policy` or `censor_at_switch`) and the other
  as its mandatory frozen sensitivity;
- retention of post-switch outcomes for the treatment-policy route;
- a pre-specified IPCW route and joint score/risk-dependence sensitivity for
  censor-at-switch interpretation;
- complete switch reasons with an explicit unknown category;
- source/treatment/indication adjustment and competing-event handling;
- no prior score/outcome access, post-result estimand selection, site/subject
  exclusion, or endpoint redefinition after switching.

Unknown switch reasons fail closed. A declared absence of switching must agree
with a zero aggregate count; the dual-estimand plan remains frozen in case the
receipt changes after data reconciliation.

## Decisions

- `PASS_NO_OBSERVED_SWITCH_DUAL_PLAN`: complete blind plan and zero switches.
- `PASS_SWITCH_SENSITIVITY_REQUIRED`: switches are present and both frozen
  estimands plus all dependence sensitivities are ready.
- `FAIL_CLOSED`: incomplete/mismatched metadata, unknown reasons, prior access,
  one-estimand-only reporting, or post-result selection.

Passing establishes process readiness only. It does not establish independent
switching, a treatment effect, molecular prognosis, or progression biology.

## Machine Check

```bash
.venv/bin/python scripts/v54_progression_treatment_switch_gate.py
```

For a quarantined package, supply `--declaration`, `--output-dir`, and
`--fail-on-error`. The default ten synthetic declarations test two valid and
eight fail-closed routes; they contain no patient data.
