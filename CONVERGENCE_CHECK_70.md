# Convergence Check 70

Timestamp: 2026-05-28 07:30 CEST

## LRRC61 Prefilter

`LRRC61` is a useful example of why breadth alone is insufficient:

- four nominal broad positive diseases;
- no MS anchor;
- no target genetics;
- no response support;
- no modality;
- CRISPR row has only two guides and no p/FDR values.

## Decision

Close `LRRC61` by prefilter. Continue route selection only for candidates with
evidence beyond broad expression recurrence.
