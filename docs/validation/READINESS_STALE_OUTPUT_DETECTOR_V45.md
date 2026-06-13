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

- artifacts checked: `75`
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
- V47 provenance gate;
- V47 external knowledge index;
- V47 external record schema linter;
- operational handoff index;
- readiness status dashboard;
- generated-doc freshness linter;
- no-score-before-gates linter;
- synthetic received-package dry run;
- OpenGWAS token-expiry sentinel;
- V46 terms-governance matrix;
- V46 metric-format adapter;
- V46 partial-label classifier;
- V46 receipt-manifest schema linter;
- V46 package-manifest shape classifier;
- V46 safe-interpretation classifier;
- V46 returned-package command-order planner;
- V46 returned-package route-state matrix;
- V46 aggregate-only returned-package composition dry run;
- V46 unscoreable-return composition dry run;
- V46 returned-package regression suite;
- V46 safe-wording fixture linter;
- V46 result-report safe-class linter;
- V46 report-header metadata linter;
- V46 report-header repair-template coverage;
- V46 safe-class report-template readiness map;
- V46 operator transcript fixture;
- V46 small-n conclusion language table;
- V46 analyzable-pair confidence envelope;
- V46 safe-interpretation examples;
- V46 safe-interpretation example coverage linter;
- V46 return repair-request templates;
- V46 partial-label repair prioritization;
- V46 first-30-minute returned-package decision table;
- V46 first-30 repair-template coverage linter;
- V46 first-30 returned-package status-board dry run;
- V46 returned-package status-board schema linter;
- V46 status-board Markdown round-trip renderer;
- V46 returned-package preflight dry run;
- V46 returned-package state-transition validator;
- V46 returned-package handoff bundle manifest;
- V46 returned-package quickstart README;
- V46 quickstart drift fixture;
- V46 quickstart command coverage matrix;
- V46 returned-package operator pocket card;
- V46 returned-package documentation cross-link linter;
- V46 returned-package dependency graph;
- V46 external blocker aging audit;
- V46 operator smoke-test bundle;
- V46 SAP AI Core health check.

## Interpretation

`PASS` means these generated readiness outputs are fresh relative to their
declared sources by filesystem modification time. It does not mean data were
received or validated.
