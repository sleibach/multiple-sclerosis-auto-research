# Route Packet Integrity Manifest V45

Status: operational integrity guard. No biological claim.

Purpose: hash the generated route-arrival command packets and verify that the
packet index, packet summary, and packet files are mutually consistent and fresh
relative to their source tracker/acquisition/generator inputs.

This guard is read-only. It does not inspect expression matrices, outcomes,
quarantined files, or run any validation harness.

## Commands

Live packet check:

```bash
.venv/bin/python scripts/v45_route_packet_integrity_manifest.py \
  --outdir analysis/v45_route_packet_integrity_manifest/live \
  --expect-status PASS
```

Synthetic missing-packet regression:

```bash
.venv/bin/python scripts/v45_route_packet_integrity_manifest.py \
  --synthetic-case missing_packet \
  --outdir analysis/v45_route_packet_integrity_manifest/synthetic_missing_packet \
  --expect-status FAIL
```

## Inputs

Packet outputs:

- `analysis/v45_route_arrival_packets/route_arrival_packet_index.tsv`
- `analysis/v45_route_arrival_packets/route_arrival_packet_summary.json`
- `analysis/v45_route_arrival_packets/*_arrival_packet.md`

Freshness sources:

- `scripts/v45_route_arrival_packet_generator.py`
- `analysis/v45_live_cohort_acquisition_index/live_cohort_acquisition_index.tsv`
- `analysis/v45_outbound_data_requests/request_tracker.tsv`

## Current Result

Current live status: `PASS`.

Current synthetic missing-packet status: `FAIL`, as expected by regression.

Machine-readable outputs:

- `analysis/v45_route_packet_integrity_manifest/live/route_packet_integrity_manifest.tsv`
- `analysis/v45_route_packet_integrity_manifest/live/route_packet_integrity_sources.tsv`
- `analysis/v45_route_packet_integrity_manifest/live/route_packet_integrity_violations.tsv`
- `analysis/v45_route_packet_integrity_manifest/live/route_packet_integrity_summary.json`
- `analysis/v45_route_packet_integrity_manifest/synthetic_missing_packet/route_packet_integrity_manifest.tsv`
- `analysis/v45_route_packet_integrity_manifest/synthetic_missing_packet/route_packet_integrity_sources.tsv`
- `analysis/v45_route_packet_integrity_manifest/synthetic_missing_packet/route_packet_integrity_violations.tsv`
- `analysis/v45_route_packet_integrity_manifest/synthetic_missing_packet/route_packet_integrity_summary.json`

## Interpretation Boundary

A live `PASS` means the generated route-arrival packets are present, hashable,
listed consistently in the packet index and packet summary, and not older than
the declared source inputs. It does not mean:

- any external route has been sent;
- a package has been received;
- a cohort is harness-ready;
- any biological or validation claim exists.

The synthetic missing-packet run is method behavior only. It proves that the
guard detects a deliberately impossible packet manifest; it is not evidence
about any real cohort.
