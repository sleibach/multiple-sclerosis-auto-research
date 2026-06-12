# Outbound Request Packets V45

Status: ready-to-send drafts. These files are not sent records.

When a request is actually sent, copy the exact sent text to:

```text
docs/validation/outbound_requests/<cohort>_sent_YYYY-MM-DD.md
```

and update:

- `docs/validation/OUTBOUND_DATA_REQUEST_TRACKER_V45.md`
- `analysis/v45_outbound_data_requests/request_tracker.tsv`

No received file should be opened before quarantine placement, checksum, intake
preflight, and any required cohort-specific preregistration addendum.

## Ready Packets

| Priority | Packet | Role |
|---:|---|---|
| 1 | `gafson_dmf_ready_to_send_V45.md` | Primary V22/V42 DMF PBMC/NEDA validation target |
| 2 | `karolinska_dmf_ready_to_send_V45.md` | Parallel secondary DMF label path |
| 3 | `gse228330_ocrelizumab_ready_to_send_V45.md` | Optional outcome-label request; otherwise context-only |
