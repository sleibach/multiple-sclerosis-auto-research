# Received-Status Updater V45

Status: operational status-board utility. No data are received or analyzed by
this script.

Purpose: convert a filled first-24h operator gate-status TSV into a proposed
received-data triage board update, so package lifecycle state can be updated
mechanically without inspecting raw expression or outcome data.

## Command

Current pre-receipt check using the blank template:

```bash
.venv/bin/python scripts/v45_received_status_updater.py \
  --cohort-id gafson_dmf_2018 \
  --role primary_V22_V42_validation \
  --outdir analysis/v45_received_status_updater
```

Machine-readable outputs:

- `analysis/v45_received_status_updater/operator_gate_status_used.tsv`
- `analysis/v45_received_status_updater/received_data_triage_status.proposed.tsv`
- `analysis/v45_received_status_updater/received_status_update_summary.json`

## Current Result

The current run is intentionally pre-receipt. It reads the all-`todo` first-24h
operator template and proposes that `gafson_dmf_2018` remains
`harness_ready=no`.

| Metric | Value |
|---|---:|
| gates read | `14` |
| harness ready | `no` |
| current blocker | `receipt path/file inventory not recorded` |
| next action | `complete_or_repair_receipt_log` |
| canonical board overwritten | `no` |

## How To Use After Data Receipt

1. Copy `docs/validation/input_schemas/V45_first_24h_operator_status_template.tsv`
   into a non-sensitive received-package operations location.
2. Fill each gate status with one of the allowed lifecycle values, such as
   `PASS`, `todo`, `blocked`, or `not_applicable`.
3. Run this updater without `--write-board` first and inspect the proposed board.
4. Only after the proposed board is reviewed, rerun with `--write-board` if the
   update should replace `analysis/v45_received_data_triage/received_data_triage_status.tsv`.

## Status Mapping

| Operator gate | Board column |
|---|---|
| `receipt_log` | `data_received` |
| `quarantine_path` | `quarantined` |
| `data_use_terms` | `terms_captured` |
| `checksum_manifest` | `checksum_verified` |
| `intake_preflight` | `metadata_preflight_passed` |
| `subject_map_sanity` | `subject_map_passed` |
| `outcome_dictionary` | `outcome_dictionary_frozen` |
| `preregistration_or_addendum` | `addendum_committed` |

The updater preserves non-applicable gates. For example, exact primary Gafson
validation has `addendum_required=no`, so `addendum_committed` remains
`not_applicable` until a blind addendum is actually required.

## Guardrail

This utility reads only operator gate metadata. It does not:

- open raw expression matrices;
- inspect response labels;
- run the frozen harness;
- change locked rules, thresholds, or preregistrations;
- make a biological validation claim.

If the proposed board says `harness_ready=no`, the correct action is gate repair
or acquisition follow-up, not analysis.
