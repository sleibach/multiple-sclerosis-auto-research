# V54 Progression Event-Time Assumption Gate

Status: additive blind-committed receipt guard. It does not modify the frozen
V54 P1/P2 pre-registration or any locked rule.

## Purpose

The V54 synthetic assumption audit established two method boundaries:

1. a source-by-treatment-stratified Cox score test can remain null-calibrated
   under administrative, independent, score-dependent, or event-risk-only
   censoring in the fixed generator, but fails severely when censoring jointly
   depends on molecular state and latent event risk;
2. a single whole-follow-up coefficient can average away an early-positive,
   late-negative association.

This gate translates those method results into a package-handling rule. It
checks only blinded metadata and the frozen analysis declaration. Passing it is
not evidence that censoring is independent, proportional hazards holds, or a
molecular state predicts progression.

## Required Receipt Metadata

A P1 event-time package must declare, before molecular scores and individual
outcomes are viewed:

- package identifier and protocol/data-dictionary sources;
- follow-up time origin and administrative horizon;
- exact event, last-observation, censoring-date, and censoring-reason fields;
- a complete reason dictionary, including explicit unknown, disability/
  progression-related, treatment-toxicity, death, and administrative classes;
- whether nonadministrative, unknown, or outcome-related censoring is present,
  based only on blinded aggregate counts;
- death/competing-event and treatment-switch rules;
- the frozen source-by-treatment stratification;
- a joint score/event-risk censoring sensitivity, worst-case bounds, and an
  IPCW route fixed before score access whenever nonadministrative loss exists;
- a proportionality/time-variation diagnostic and protocol-defined cut basis;
- an explicit ban on substituting window p-values for a direct time-varying
  coefficient.

The actual aggregate censoring counts and reasons must be retained in the
quarantined receipt audit. A declaration that merely says “dropout adjusted” is
insufficient.

## Decisions

| decision | conditions | permitted interpretation |
|---|---|---|
| `PASS_STANDARD_PLUS_DIAGNOSTICS` | administrative censoring only; all fields and diagnostics frozen blind | frozen whole-follow-up route may run with mandatory diagnostics |
| `PASS_SENSITIVITY_REQUIRED` | documented nonadministrative loss, no unknown or outcome-related reasons, and IPCW + worst-case + joint-dependence sensitivities frozen blind | primary result cannot arbitrate without the frozen sensitivity panel |
| `FAIL_CLOSED` | unknown/outcome-related loss, absent dates/reason mapping, unfrozen sensitivity, score/outcome access before freeze, or post-hoc window substitution | no confirmatory progression interpretation |

Unknown or disability-related dropout fails closed because observed metadata
cannot prove the joint score/event-risk mechanism absent. The rule does not
claim every such cohort is biased; it states that the frozen Cox result alone
cannot adjudicate it.

## Machine Check

Run the synthetic regression:

```bash
.venv/bin/python scripts/v54_progression_event_time_assumption_gate.py
```

For a real quarantined package:

```bash
.venv/bin/python scripts/v54_progression_event_time_assumption_gate.py \
  --declaration path/to/blind_event_time_declaration.json \
  --output-dir path/to/event_time_gate --fail-on-error
```

The default regression contains eight clearly labeled synthetic declarations:
two eligible cases and six fail-closed cases. It tests method behavior only and
contains no patient data or biological evidence.

## Boundary

Passing establishes only that event-time inference has the minimum blind
metadata and pre-specified diagnostics required to be interpretable. It does
not establish independent censoring, a proportional effect, progression
association, causal biology, or a route to halting MS.
