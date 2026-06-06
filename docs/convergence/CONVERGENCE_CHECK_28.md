# Convergence Check 28

Timestamp: 2026-05-27 15:47 CEST.

## Current Question

Does the strongest available cell-resolved anti-TNF perturbation dataset support
the lipid-lysosomal/APC myeloid module as an intervention axis?

## New Evidence

Wave67 `GSE282122` myeloid pseudobulk audit:

- Input: Zenodo `14007626` `myeloid_final.h5ad`, 30,858 cells x 33,075 genes,
  paired manifest with 110 samples.
- Primary states: `Mono_macro` and `DC`.
- Primary target modules: `lipid_loader_repair`, `lysosomal_apc`,
  `complement_phagocytosis`.
- Generic controls: `ifn_apc`, `inflammatory_nfkb`, `tnf_autocrine_nfkb`.
- Primary paired support after cell-count thresholds: 43 paired biopsy
  state-level comparisons, 29 patients.

Gate results:

- `lipid_loader_repair` is null in both major states:
  - `DC`: all-pair delta 0.0086, FDR 1.0, target/generic ratio 0.101.
  - `Mono_macro`: all-pair delta -0.0075, FDR 1.0, target/generic ratio 0.041.
- `lysosomal_apc` has weak positive paired deltas but fails specificity and
  response interaction:
  - `DC`: all-pair delta 0.144, FDR 0.708, target/generic ratio 1.686,
    adjusted remission-interaction FDR 1.0.
  - `Mono_macro`: all-pair delta 0.122, FDR 0.836, target/generic ratio 0.674.
- `complement_phagocytosis` does not pass:
  - `DC`: all-pair delta 0.0587, FDR 1.0.
  - `Mono_macro`: CD and UC effects have opposite directions.
- No target module has generic-adjusted remission-interaction FDR <= 0.10.

Non-target observation:

- HLA-II/MIF-CD74-like modules have the strongest raw paired signals:
  - `DC hla_ii_apc` in CD: raw p 0.000333, global FDR 0.103.
  - `DC hla_ii_apc` in remission: raw p 0.000201, global FDR 0.103.

## Agreement

- The cell-resolved perturbation dataset agrees with Wave65 that broad
  treatment-response signatures are not enough to nominate the lipid-lysosomal
  module.
- Unlike Wave65 bulk synovium, Wave67 resolves myeloid/DC states directly. The
  negative result therefore has substantially higher mechanistic weight.
- Ceramide/glycosphingolipid biochemical hints from Wave66 do not translate
  into a detectable anti-TNF lipid-loader module perturbation in IBD myeloid
  states.

## Disagreement

- Cross-sectional cell-state recurrence still suggests a shared inflammatory
  myeloid state.
- Perturbation data suggest that the treatment-responsive controller, if any,
  may sit in antigen-presentation/CD74/HLA-II biology or another gene-level
  program, not in the pre-specified lipid-lysosomal module.

## Decision

Demote the lipid-lysosomal/APC module from therapeutic intervention-axis status
under current evidence.

Next forcing question:

Which individual genes or regulatory programs inside `GSE282122` myeloid/DC
states show reproducible anti-TNF paired movement or remission-associated
movement, and do any intersect with cross-autoimmune genetic target-resolution
evidence from Wave62?
