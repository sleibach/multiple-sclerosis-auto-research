# Outbound Request Packet Integrity V45

Status: request-packet operations guard. No biological claim.

## Purpose

`scripts/v45_outbound_request_packet_integrity.py` checks all live outbound
request packets listed in the external blocker board. It verifies:

- every route has a request-packet path;
- every packet exists and is non-empty;
- each packet includes send-approval / sent-copy guard language;
- each packet has `To:` and `Subject:` fields;
- each packet is hashed with SHA-256 for transfer/audit integrity.

The guard does not send requests, mark requests as sent, receive data, inspect
private data, or run any validation harness.

## Command

Live:

```bash
.venv/bin/python scripts/v45_outbound_request_packet_integrity.py \
  --outdir analysis/v45_outbound_request_packet_integrity/live
```

Synthetic regression:

```bash
.venv/bin/python scripts/v45_outbound_request_packet_integrity.py \
  --synthetic-case missing_packet \
  --expect-status FAIL \
  --outdir analysis/v45_outbound_request_packet_integrity/synthetic_missing_packet
```

## Current Result

Live status: `PASS`.

- routes checked: `4`;
- packets hashed: `4`;
- hard issues: `0`;
- soft issues: `0`.

Synthetic missing-packet regression: expected `FAIL` with `1` hard issue. It
also reports the displaced real packet as a soft unmapped-packet issue in that
synthetic fixture.

## Machine-Readable Outputs

Live:

- `analysis/v45_outbound_request_packet_integrity/live/outbound_request_packet_manifest.tsv`
- `analysis/v45_outbound_request_packet_integrity/live/outbound_request_packet_issues.tsv`
- `analysis/v45_outbound_request_packet_integrity/live/outbound_request_packet_integrity_summary.json`

Synthetic regression:

- `analysis/v45_outbound_request_packet_integrity/synthetic_missing_packet/outbound_request_packet_manifest.tsv`
- `analysis/v45_outbound_request_packet_integrity/synthetic_missing_packet/outbound_request_packet_issues.tsv`
- `analysis/v45_outbound_request_packet_integrity/synthetic_missing_packet/outbound_request_packet_integrity_summary.json`

## Interpretation Boundary

A `PASS` means the outbound request packet set is internally complete and
hashable. It does not mean requests have been sent, data have been received, any
route is harness-ready, or any biological validation has occurred.
