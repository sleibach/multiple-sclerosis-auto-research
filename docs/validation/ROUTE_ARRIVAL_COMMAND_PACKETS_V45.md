# Route Arrival Command Packets V45

Status: acquisition/arrival operations packets. No biological claim.

Script:

`scripts/v45_route_arrival_packet_generator.py`

Purpose: generate first-action packets for each live route after data or
aggregate outputs arrive. The packets are derived from the live acquisition
index and outbound tracker, and repeat the hard stop that no scoring is allowed
before route-specific gates pass.

## Command

```bash
.venv/bin/python scripts/v45_route_arrival_packet_generator.py \
  --outdir analysis/v45_route_arrival_packets
```

## Current Packets

Index:

`analysis/v45_route_arrival_packets/route_arrival_packet_index.tsv`

Packets generated:

- `analysis/v45_route_arrival_packets/gafson_dmf_2018_arrival_packet.md`
- `analysis/v45_route_arrival_packets/karolinska_dmf_ros_2019_arrival_packet.md`
- `analysis/v45_route_arrival_packets/gse228330_ocrelizumab_pbmc_arrival_packet.md`
- `analysis/v45_route_arrival_packets/any_author_run_fallback_arrival_packet.md`

## Guardrail

These packets are arrival operations, not validation results. They do not allow
module scoring, response metrics, or interpretation before receipt, terms,
checksum, preflight, subject-map, label-dictionary, addendum, and/or author-run
return gates pass as applicable.
