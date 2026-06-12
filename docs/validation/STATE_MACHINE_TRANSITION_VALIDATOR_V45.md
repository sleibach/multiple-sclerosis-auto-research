# State-Machine Transition Validator V45

Status: operational integrity guard. No biological claim.

Purpose: validate that the live V45 acquisition and validation-readiness boards
do not imply impossible route transitions before any received cohort is scored.
This guard is read-only: it does not inspect expression matrices, outcomes,
quarantined data, or run a validation harness.

## Command

Live board check:

```bash
.venv/bin/python scripts/v45_state_machine_validator.py \
  --outdir analysis/v45_state_machine_validator/live \
  --expect-status PASS
```

Synthetic impossible-state regression:

```bash
.venv/bin/python scripts/v45_state_machine_validator.py \
  --synthetic-case impossible \
  --outdir analysis/v45_state_machine_validator/synthetic_impossible \
  --expect-status FAIL
```

## Inputs

The live check joins these machine-readable boards:

- `analysis/v45_received_data_triage/received_data_triage_status.tsv`
- `analysis/v45_external_blocker_board/external_blocker_board.tsv`
- `analysis/v45_followup_due_board/live_template/followup_due_board.tsv`
- `analysis/v45_readiness_status_dashboard/readiness_status_dashboard_summary.json`

## Checks

The validator currently flags hard violations when:

- a triage route is missing from the external-blocker board;
- a route is marked harness-ready before checksum, metadata preflight, subject
  map, outcome dictionary, or required addendum gates pass;
- post-receipt gates are marked complete while the route still has no received
  validation data;
- sent-state disagrees between triage and follow-up boards;
- `request_sent=yes` is paired with `not_sent_ready`;
- an external-send blocker is paired with `request_sent=yes` or
  `harness_ready=yes`;
- dashboard harness-ready counts or headline state disagree with route boards.

## Current Result

Current live status: `PASS`.

Current synthetic impossible-state status: `FAIL`, as expected by regression.

Machine-readable outputs:

- `analysis/v45_state_machine_validator/live/route_state_validation.tsv`
- `analysis/v45_state_machine_validator/live/state_machine_violations.tsv`
- `analysis/v45_state_machine_validator/live/state_machine_validator_summary.json`
- `analysis/v45_state_machine_validator/synthetic_impossible/route_state_validation.tsv`
- `analysis/v45_state_machine_validator/synthetic_impossible/state_machine_violations.tsv`
- `analysis/v45_state_machine_validator/synthetic_impossible/state_machine_validator_summary.json`

## Interpretation Boundary

A live `PASS` means the current operational boards are internally consistent
with the V45 state machine. It does not mean:

- a cohort has been received;
- a frozen harness is ready to run;
- a validation result exists;
- any biological or clinical claim has been made.

The synthetic impossible-state run is method behavior only. It proves the guard
detects a deliberately impossible state; it is not evidence about MS biology or
about any real cohort.
