# V54 Blinded Progression Information-Accrual Monitor

Status: frozen operational guard. It changes no locked rule, endpoint,
pre-registration, analysis threshold, or stopping boundary for efficacy.

## Purpose

This monitor tracks whether a prospective progression package has accumulated
the pre-specified amount of usable information while the molecular-outcome
relationship remains inaccessible. It can continue accrual, hold because
censoring/visit metadata are unresolved, or lock the package when the reference
count targets are reached. It can never stop early for apparent benefit, harm,
futility, effect direction, or significance.

## Inputs

A frozen plan declares the package ID, three site targets, total analyzable and
confirmed-event targets, minimum events per site, source, and blindness rules.
Each timestamped snapshot may contain only aggregate:

- enrolled and analyzable counts by site;
- confirmed-event counts by site;
- expected/completed visit counts and pending confirmations;
- counts with unknown visit/censoring reasons;
- follow-up completion status.

Molecular values, score strata, score-outcome associations, model coefficients,
directions, p-values, confidence intervals, and individual outcomes are
forbidden fields. The plan and snapshot package IDs must bind exactly.

## Decisions

- `CONTINUE_BLINDED_ACCRUAL`: one or more frozen count/follow-up targets remain
  incomplete, with no unresolved metadata blocker.
- `HOLD_UNRESOLVED_CENSORING_METADATA`: unknown visit/censoring reasons remain;
  no confirmatory handoff is permitted.
- `REFERENCE_INFORMATION_REACHED_LOCK_AND_HANDOFF`: total and every-site
  analyzable/event targets are met, follow-up is complete, no confirmations are
  pending, and metadata are resolved. Lock and execute the pre-registered
  analysis once; this is not evidence of an effect.
- `FAIL_CLOSED_PEEKING_OR_METADATA`: a forbidden efficacy field, malformed
  count, package mismatch, unfrozen plan, or efficacy/futility stopping
  authority is present.

The reference target can be replaced only by a separately committed,
cohort-specific blinded power plan made before score/outcome access. It cannot
be changed because accrual looks favorable or unfavorable.

## Machine Check

```bash
.venv/bin/python scripts/v54_progression_information_monitor.py
```

For a real quarantined package:

```bash
.venv/bin/python scripts/v54_progression_information_monitor.py \
  --plan path/to/frozen_information_plan.json \
  --snapshot path/to/blind_aggregate_snapshot.json \
  --output-dir path/to/information_monitor --fail-on-error
```

The default regression contains ten clearly labeled synthetic plan/snapshot
pairs spanning clean continuation, pending confirmation, site shortfall,
information lock, unknown-reason hold, and fail-closed peeking/malformed cases.
It tests software behavior only.
