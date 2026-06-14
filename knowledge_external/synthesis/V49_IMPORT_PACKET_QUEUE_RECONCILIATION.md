# V49 Import-Packet Queue Reconciliation

Status: queue/navigation only. This document reconciles the V49
source-specific import packets with the generated V48 future-grounding queue.
It does not add external claims, relationship rows, or project evidence.

Boundary: `FUTURE_GROUNDING_QUEUE_V48.md` is generated from the relationship
matrix, so V49 does not hand-edit it. The reconciliation below is an overlay:
it maps existing generated queue rows to the stricter V49 import packets and
states the missing field-level acceptance gates.

## Summary

- V49 import packets reviewed: `3`
- generated queue rows already present: `3`
- broad queue rows needing V49 field-level overlay: `3`
- missing generated queue rows: `0`
- hand-edits made to generated future-grounding queue: `0`

## Reconciliation

| packet | generated queue row | generated action status | V49 overlay status | field-level gate now required |
|---|---|---|---|---|
| `V49_IMPORT_ZMIZ1_DIRECTION` | `V48_FG_008` | Present but broad: create a future-grounding task only after importing specific ZMIZ1 records with snapshots and hashes. | `overlay_required_before_intake` | Imported record must address ZMIZ1 specifically and include direction/effect or enough variant/dataset fields to recover direction. Generic gene-disease association is rejected or parked. |
| `V49_IMPORT_CHR1_KIF21B_GPR25_SIGNAL` | `V48_FG_009` | Present but broad: import specific GWAS Catalog associations before comparison. | `overlay_required_before_intake` | Imported record must be signal-specific and preserve variant, effect allele, direction/beta/OR where available, trait, study accession, publication, and source version/date. Catalog-level locus existence is rejected or parked. |
| `V49_IMPORT_COUPLED_APC_AXIS_RECORDS` | `V48_FG_005` | Present but broad: import CD74, MIF, HLA, and APC-axis records before comparing to V26. | `overlay_required_before_intake` | Imported record must contain source-specific CD74/MIF/HLA/IFN-APC axis, cell-state, compartment, interaction, or direction/state fields. Simple database presence is rejected or parked. |

## Queue Handling Decision

Do not edit `FUTURE_GROUNDING_QUEUE_V48.md` manually. It is generated from the
relationship matrix and should remain reproducible. Future sessions should read
the generated queue row first, then apply the V49 packet overlay before any
source-intake action.

## Operational Rule For Future Intake

For each of the three rows:

1. Start from the generated queue row (`V48_FG_005`, `V48_FG_008`, or
   `V48_FG_009`).
2. Apply the matching V49 import packet.
3. If the candidate source does not satisfy the packet's field-level gate, park
   or reject it.
4. Add no relationship-matrix row until the imported record has source,
   not-grounded marker, snapshot/date, and a source-specific overlap review.

