# V35 Orthogonal-Context T/B Artifact Feasibility Check

## Question

Can held data test whether the V35 T/B compartment remodeling gate is a generic
lymphocyte/cellularity artifact by applying an analogous compartment comparison
in an orthogonal myeloid-dominant perturbation context?

## Files Inspected

- `phases/v3/results/mixscale/mixscale_module_effects_by_cell_type.tsv`
- `phases/v3/results/wave15_perturbation_drug_response/mixscale_selectivity_by_cell_type.tsv`
- `analysis/v26_deep_structure/treatment_pharmacodynamic_module_matrix.tsv`
- `analysis/v26_deep_structure/treatment_response_module_matrix.tsv`

## Result

Partially feasible only; no clean held-data falsification.

- Mixscale has per-cell-type perturbation module effects, but the cell types are
  cell lines such as `A549`, `BXPC3`, `HAP1`, `HT29`, `K562`, and `MCF7`, not
  immune T/B/myeloid compartments. It cannot test a T/B compartment artifact.
- V26 treatment pharmacodynamic matrices include marker compartments such as
  `t_cell_like` and `myeloid_apc_like`, but they are aggregated module summaries
  rather than patient-level paired response labels for an independent cohort.
- The only patient-level exact compartment response cohort remains
  `GSE253006` tofacitinib, already used for the T/B gate.

## Verdict

The model-raised artifact risk is valid, but currently not testable cleanly with
held data. The T/B gate remains replication-gated.

## Next Test

Acquire or build an independent response-labeled single-cell/sorted-cell cohort
with enough patient-level data to compare T/B versus myeloid/APC compartments
under the locked-rule delta. A useful orthogonal-context negative control would
be a myeloid-dominant perturbation/therapy where the pre-specified expectation
is that myeloid/APC compartments should dominate.
