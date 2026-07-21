# V54 Progression-Lesion State Test Plan

Status: frozen before the V54 lesion-state implementation is run. This tests a
pre-existing module family in two held lesion resources; it is not an open gene
scan and cannot establish clinical progression.

## Question

Do pre-existing microglial/APC module states show consistent direction in:

1. chronic-active versus chronic-inactive lesion-edge immune pseudobulks in
   GSE180759; and
2. foamy versus non-foamy MS white-matter samples in GSE279972 after deposited
   lesion class and B-cell/APC composition adjustment?

These are related but non-identical pathology contexts. Agreement is
orthogonal consistency, not replication of one estimand and not evidence that
the state drives disability accumulation.

## Frozen Module Family

Primary:

- `receptor_cd44_cxcr4`: `CD44`, `CXCR4`.

Secondary:

- `hla_regulatory`: `CIITA`, `RFX5`.
- `ifn_apc_unique`: `STAT1`, `IRF1`, `CXCL10`, `GBP1`.
- `lysosomal_unique`: `CTSS`, `CTSB`, `CTSD`, `LAMP1`, `LAMP2`, `LAMP3`.
- `complement_phagocytosis`: `C1QA`, `C1QB`, `C1QC`, `C3`, `ITGAM`,
  `ITGB2`, `TYROBP`, `AIF1`.
- `lipid_repair`: `APOE`, `LPL`, `TREM2`, `ABCA1`, `ABCG1`, `SPP1`,
  `LGALS3`, `GPNMB`.

Adjustment-only composition module:

- `b_apc_composition`: `CD79A`, `MS4A1`, `CD74`, `HLA-DRA`, `HLA-DPA1`,
  `HLA-DPB1`.

No gene or module will be added because of the V54 outcome.

## GSE180759 Frozen Analysis

- Stream deposited counts and compute donor x pathology x cell-type
  pseudobulk `log2(CPM + 1)` values.
- Restrict the primary analysis to deposited `immune` bins with at least 20
  nuclei; cells are never inferential replicates.
- Standardize each gene over eligible immune pseudobulks, then average genes
  into frozen modules.
- Primary contrast: paired chronic-active minus chronic-inactive lesion edge.
- Use all eligible paired donors and enumerate every paired sign flip exactly.
- Report paired differences, directions, exact two-sided p-values, BH q-values,
  and max-T family-wise p-values across six modules.
- Periplaque and lesion-core contrasts are descriptive sensitivities when fewer
  than three paired donors remain.

## GSE279972 Frozen Analysis

- Stream all 109 raw count files from the already checksummed archive; compute
  `log2(CPM + 1)` for frozen genes.
- Restrict to MS samples with deposited `foamy` or `non_foamy` morphology.
- Standardize genes across the eligible 54 samples and form frozen modules.
- For each module, fit `module ~ foamy + deposited broad lesion class +
  b_apc_composition`.
- Use donor-clustered covariance and a three-seed, 300,000-replicate donor-wild
  null. Apply BH and max-T control across six modules.
- Report leave-one-donor coefficient ranges.

## Calling And Interpretation

No module becomes a progression finding or target from these data. A module is
called `orthogonally_consistent_needs_data` only if:

- every eligible GSE180759 paired donor has the same active-minus-inactive
  direction;
- the adjusted GSE279972 foamy coefficient has that direction;
- its GSE279972 donor-wild p is at most 0.05, BH q at most 0.10, and max-T p at
  most 0.10; and
- leave-one-donor GSE279972 coefficients retain direction.

The GSE180759 exact p-value cannot be below 0.25 with three pairs, so even a
directionally consistent result is explicitly `needs_data`, never supported.
Failure of direction or corrected GSE279972 gates is `not_supported`; wide or
sparse results are `inconclusive`.
