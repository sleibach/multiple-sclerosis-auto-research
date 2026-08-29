# V57 Paired Single-Cell Distribution-Transport Plan

Status: frozen before execution.

## Question

Do paired treatment samples contain responder-associated changes in the full
within-cell distribution of fixed APC-axis module scores that were missed by
pseudobulk means?

The held data are GSE282122 paired pre/post anti-TNF myeloid cells from IBD.
This is a method-feasibility and cross-disease context test. It cannot establish
an MS mechanism, biomarker, or treatment target.

## Frozen Inputs And Units

- Cell object:
  `data/raw_v3/wave67_gse282122_myeloid/myeloid_final.h5ad`.
- Pair contract:
  `phases/v3/results/wave67_gse282122_myeloid_pseudobulk/paired_module_deltas.tsv`.
- Primary annotated states: `DC` and `Mono_macro`.
- Fixed modules: `ifn_apc`, `hla_ii_apc`, `mif_cd74_receptor_state`,
  `lysosomal_apc`, and `inflammatory_nfkb`, using the already committed Wave67
  definitions.
- A site-state pair is eligible only when pre and post samples are in the same
  recorded batch and each side has at least `50` cells.
- The inferential unit is the patient. Multiple tissue sites are collapsed by
  the median within patient, state, and module.

## Cell Scores And Transport

For each cell and module, calculate the mean of `log1p(10,000 * gene_count /
cell_total_count)` over present module genes. For each eligible paired
site-state:

1. calculate the one-dimensional Wasserstein-1 distance between pre and post
   cell-score distributions;
2. subtract each distribution's own median and calculate centered
   Wasserstein-1 distance, the primary shape-remodeling metric;
3. retain absolute mean-score shift as a location covariate;
4. calculate centered Wasserstein distance of log library size as a technical
   control;
5. retain absolute change in the recorded inflammation score.

## Frozen Tests

- Primary family: centered Wasserstein distance for five modules by two cell
  states (`10` tests).
- Compare remission with non-remission at patient level using a Welch-style
  studentized mean difference.
- Permute remission labels within disease (`CD`, `UC`) using `200,000` seeded
  draws (`57011`). For every draw retain the maximum absolute statistic across
  the ten tests; report max-T family-wise p values.
- Sensitivity: residualize centered distance against disease, centered library-
  size transport, absolute module mean shift, and absolute inflammation-score
  change before the same stratified max-T test.
- Report disease-specific effect directions. A feature is eligible for a
  dedicated follow-up only if raw and residualized max-T p are at most `0.10`,
  the pooled direction agrees in CD and UC, and each tested outcome group has at
  least three patients.
- Total uncentered Wasserstein distance is descriptive only.

The permutation operates on patient labels, never cells or tissue-site rows.
Cell count therefore does not create false inferential replication.

## Interpretation

- A pass means a distribution-level IBD treatment-response feature merits
  independent replication and a later MS-specific test.
- A fail means this method did not recover a response-specific distributional
  effect in the held paired atlas under the fixed family and controls.
- Neither outcome changes V22, V41, or any locked/pre-registered rule.
