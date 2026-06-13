# Readiness Stale-Output Detector V45

Status: infrastructure freshness check. No biological claim.

Script:

`scripts/v45_readiness_stale_output_detector.py`

Purpose: detect when generated readiness artifacts should be refreshed because
their source docs, trackers, scripts, or upstream summaries are newer than their
outputs.

## Command

```bash
.venv/bin/python scripts/v45_readiness_stale_output_detector.py \
  --outdir analysis/v45_readiness_stale_output_detector
```

## Current Result

- artifacts checked: `31`
- stale or missing: `0`
- overall status: `PASS`

Checked generated artifacts:

- collaborator path resolver;
- follow-up due board;
- follow-up message templates;
- send-log intake template;
- external blocker board;
- external blocker escalation matrix;
- follow-up escalation packets;
- outbound request packet integrity;
- route arrival packets;
- route packet integrity manifest;
- cross-route readiness linter;
- state-machine transition validator;
- received-package decision tree;
- current-action card;
- cold-start operator sequence;
- author-run bundle dry-run manifest;
- generated-checker registry;
- operational handoff index;
- readiness status dashboard;
- generated-doc freshness linter;
- no-score-before-gates linter;
- synthetic received-package dry run;
- OpenGWAS token-expiry sentinel;
- V46 terms-governance matrix;
- V46 metric-format adapter;
- V46 partial-label classifier;
- V46 safe-interpretation classifier;
- V46 returned-package command-order planner;
- V46 aggregate-only returned-package composition dry run;
- V46 external blocker aging audit;
- V46 operator smoke-test bundle.

## Interpretation

`PASS` means these generated readiness outputs are fresh relative to their
declared sources by filesystem modification time. It does not mean data were
received or validated.
