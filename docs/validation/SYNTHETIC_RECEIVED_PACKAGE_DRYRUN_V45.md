# Synthetic Received-Package Dry Run V45

Status: synthetic intake-state dry run. No biological claim and no real data
read.

## Purpose

`scripts/v45_synthetic_received_package_dryrun.py` exercises the first-24h
received-package path end to end on a synthetic blocked fixture. It verifies
that a package with receipt and quarantine recorded but data-use terms blocked
cannot become scoring-ready.

The dry run uses only synthetic operator-gate metadata and does not inspect
expression matrices, outcomes, sample phenotypes, quarantined data, or any real
Gafson files.

## Command

```bash
.venv/bin/python scripts/v45_synthetic_received_package_dryrun.py \
  --outdir analysis/v45_synthetic_received_package_dryrun
```

## Synthetic Case

- cohort id: `gafson_dmf_2018`
- passed gates: `receipt_log`, `quarantine_path`
- blocked gate: `data_use_terms`
- remaining gates: `todo`
- expected decision: `harness_ready=no`, `may_score_now=0`

## Current Result

- overall status: `PASS`
- received-status updater harness-ready state: `no`
- received-status updater blocker: `terms not approved for preflight`
- state-machine validator status: `PASS`
- decision-tree routes allowed to score now: `0`

## Machine-Readable Outputs

- `analysis/v45_synthetic_received_package_dryrun/synthetic_received_package_dryrun_summary.json`
- `analysis/v45_synthetic_received_package_dryrun/synthetic_gafson_first_24h_operator_status.tsv`
- `analysis/v45_synthetic_received_package_dryrun/received_status_updater/received_data_triage_status.proposed.tsv`
- `analysis/v45_synthetic_received_package_dryrun/state_machine_validator/route_state_validation.tsv`
- `analysis/v45_synthetic_received_package_dryrun/received_package_decision_tree/received_package_decision_tree.tsv`

## Interpretation Boundary

A `PASS` means the operational route correctly remains blocked and non-scoring
when a required data-use terms gate is not approved. It does not mean any real
package has arrived, any cohort is harness-ready, or any validation has
occurred.
