# V35 T/B Gate Independent-Cohort Feasibility Scout

## Question

Is there another held, paired, response-labeled, compartment-resolved cohort that
can independently replicate the V35 T/B compartment remodeling gate?

## Search Performed

- File inventory search over `analysis`, `results`, and `data/derived` for:
  `compartment`, `tofacitinib`, `response`, `locked`, `paired`, and
  `validation`.
- Text search over `docs`, `meta`, `analysis`, `results`, and `scripts` for:
  `GSE253006`, `tofacitinib`, `compartment`, `T/B`, `b_plasma`, `t_cell`,
  `paired`, and `response`.

## Result

Only one held response-labeled paired cohort has exact compartment-resolved
scores suitable for the T/B gate:

- `analysis/v23_apc_hla_monitoring/gse253006_exact_compartments/`

This is the same UC tofacitinib cohort used in V23 and V35 iterations 4 and 9.

Other held response artifacts are not suitable for an independent T/B gate
replication:

- `analysis/v22_locked_apc_hla_validation/*`: scalar locked-rule validation
  ledgers and paired scores, not compartment-resolved.
- `analysis/tier_0_triage/hyp_v6_006_gse138064_ms_ifnb_replication/` and
  `analysis/tier_0_triage/hyp_v6_006_gse24427_ms_ifnb_longitudinal/`: paired
  module deltas, not sorted/single-cell T/B compartments.
- `analysis/v27_coupled_axis/v27_paired_score_input.tsv`: coupled/scalar
  module input, not compartment-resolved.

## Verdict

Blocked for independent replication with currently held data. The T/B gate
remains internally stress-tested but single-cohort.

## Next Data/Test Needed

Acquire a paired baseline/early-treatment response cohort with either:

1. single-cell/CITE-seq data and responder labels, or
2. sorted T, B, myeloid/APC expression with responder labels, or
3. bulk data with validated T/B deconvolution sufficient for a pre-specified
   compartment gate.
