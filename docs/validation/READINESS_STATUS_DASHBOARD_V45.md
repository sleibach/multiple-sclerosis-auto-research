# Readiness Status Dashboard V45

Status: generated operational dashboard. No biological claim.

Script:

`scripts/v45_readiness_status_dashboard.py`

Purpose: aggregate the current V45 operational/readiness state across existing
tracker, triage, precommit, path-resolution, follow-up, and handoff outputs.
This is a read-only status summary. It does not run validation and does not mark
any cohort scoreable.

External blocker board:

`docs/validation/EXTERNAL_BLOCKER_BOARD_V45.md`

Generated checker registry:

`docs/validation/GENERATED_CHECKER_REGISTRY_V45.md`

Validation state machine:

`docs/validation/VALIDATION_STATE_MACHINE_V45.md`

Stale-output detector:

`docs/validation/READINESS_STALE_OUTPUT_DETECTOR_V45.md`

## Command

```bash
.venv/bin/python scripts/v45_readiness_status_dashboard.py \
  --outdir analysis/v45_readiness_status_dashboard
```

## Current Headline

`READY_AWAITING_EXTERNAL_DATA`

Meaning:

- internal guardrails are currently passing;
- collaborator package links resolve;
- pre-receipt handoff state is complete for the not-received lifecycle;
- no cohort is harness-ready;
- all current live request paths still need external acquisition action.

## Current Dashboard

Generated outputs:

- `analysis/v45_readiness_status_dashboard/readiness_status_dashboard.tsv`
- `analysis/v45_readiness_status_dashboard/readiness_status_dashboard_summary.json`
- `analysis/v45_readiness_status_dashboard/READINESS_STATUS_DASHBOARD.md`

Current key metrics:

- outbound tracker: `4/4` rows ready, `0` marked sent;
- received-data triage: `0/3` cohorts harness-ready;
- precommit readiness: `PASS`;
- collaborator path resolution: `PASS`, `168` links resolved, `0` missing;
- follow-up board: `4` `not_sent_ready` rows;
- external blocker board: `4` `external_send_or_author_approval` rows;
- scored-lifecycle handoff negative control: `EXPECTED_FAIL` until real harness outputs exist.

## Interpretation Boundary

The dashboard can support operational statements about readiness and blockers.
It cannot support biological or clinical-validation claims.
