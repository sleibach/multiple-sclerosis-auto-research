# V54 Progression Confirmation-Provenance Receipt Gate

Status: additive blind receipt guard. It changes no endpoint definition,
locked rule, pre-registration, or primary model.

## Purpose

The 230,400-cohort synthetic confirmation audit showed that molecular-score-
linked missed or false confirmation can manufacture strong null associations.
A derived CDP/PIRA label alone is therefore insufficient. Before any molecular
score or individual outcome is opened, the package must declare the raw
candidate and confirmation records and the process that created them.

## Required Declaration

- package and endpoint-declaration identity;
- protocol and confirmation-process source documents;
- exact candidate-worsening date, confirmation date, confirmation-status, and
  unconfirmed-reason fields;
- protocol confirmation interval and visit tolerance;
- site/source-specific status and reason dictionaries;
- confirmation assessor status of either `blinded` or
  `molecular_score_not_computed`; `unknown` fails closed;
- retention of confirmed, transient, late-valid, missing-confirmation, and
  censored candidates rather than a favorable-label-only extract;
- explicit separation of missing confirmation from confirmed absence;
- a frozen audit of score association with confirmation/missingness process;
- confirmation that the declaration was fixed before score/outcome access and
  that post-result event reclassification is forbidden.

## Decisions

| decision | meaning |
|---|---|
| `PASS_CONFIRMATION_PROVENANCE_GATE` | process fields are available and frozen; proceed to other gates |
| `FAIL_CLOSED` | confirmation-dependent progression inference is not permitted |

Passing does not prove adjudication unbiased. It makes the process auditable;
the pre-specified process-association control still decides whether event-time
inference remains valid.

## Machine Check

```bash
.venv/bin/python scripts/v54_progression_confirmation_provenance_gate.py
```

The default regression uses ten labeled synthetic declarations: two safe
process routes and eight fail-closed variants. It contains no patient data and
makes no progression or biological claim.
