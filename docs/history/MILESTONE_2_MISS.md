# Milestone 2 Miss - Hour 4 Checkpoint

Timestamp: 2026-05-26 22:12 UTC

Run start: 2026-05-26 18:41 UTC

## Required Milestone

Hour 4 target:

- Cross-disease shared genes and shared cell states enumerated with statistics.
- First-pass central-node candidates ranked.
- Foundation-model perturbation predictions initiated.

## What Was Met

Shared cell states and genes were enumerated.

Key raw cross-disease state statistics:

- `mif_cd74_receptor_state`: tested in 8 diseases; 3 strong; 6
  supportive-or-strong; supporting diseases include Crohn disease, Hashimoto
  thyroiditis, MS, Sjogren syndrome, T1D, and UC.
- `ifn_apc`: tested in 8 diseases; 2 strong; 4 supportive-or-strong.
- `mixscale_validated_ifng_readout`: tested in 7 diseases; 3 strong; 4
  supportive-or-strong.
- `lipid_loader_repair`: tested in 6 diseases; 1 strong; 2
  supportive-or-strong; directionally mixed.

Central candidates were ranked and then stress-tested:

- Broad IFN/HLA/CD74 transition: raw 7/8 supportive-or-strong diseases, but only
  4/56 target-module tests retained nominal support after same-sample IFN
  residualization, with no residual FDR support.
- Residual CD74/HLA receptor-state: demoted to biomarker-only after wave-4
  scout. MS white-matter microglia is the only credible residual signal.
- `LIPA` lipid-lysosomal lane: demoted after wave-4 scout and local residual
  testing. Positive signals are epithelial/ductal/keratinocyte-restricted and
  contradicted in Crohn/UC myeloid compartments.
- HIF/NAMPT/NF-kB metabolic inflammation: demoted to IBD/T1D-heavy backup, not
  pan-autoimmune.
- PDE4/cAMP local CIITA-gate intervention: tractable hypothesis, but weak
  L1000 support and prior-art crowded.

Post-critique status file:

- `phases/v3/results/post_critique_candidate_status.tsv`

## What Was Missed

No central-node candidate currently survives enough scrutiny to initiate
foundation-model perturbation as a serious V3 finding.

Foundation-model status:

- State named-gene output is blocked by incomplete `adata_real.h5ad`.
- Local size at independent gate check: 5,619,356,404 bytes.
- HDF5 stored EOF: 9,112,404,896 bytes.
- Existing State outputs remain anonymous `FEATURE_n` tables and cannot support
  named-gene perturbation claims.
- The download was resumed and remains active, but State cannot be counted as
  named-gene evidence until the file opens and the State parsing script yields
  named genes.
- Mixscale CRISPRi remains the only valid named-gene perturbation backbone.

## Reason For Miss

The raw breadth signal was real but generic. Stronger operationalizations
changed the conclusion:

- IFN/APC recurrence mostly collapsed under IFN residualization.
- CD74/HLA residual signal was too narrow and prior-arted.
- `LIPA` had directionally inconsistent cell-compartment effects.
- PDE4/cAMP was tractable but not supported by current L1000 reversal hits.

The milestone was missed because promoting any of these candidates would be
proxy-satisficing.

## Pivot

Next pivot: abandon single-gene rescue of the V2 lipid-lysosomal module and
search for a higher-level cross-disease tissue-licensing node with:

- better genetics than CD74/LIPA;
- direction-stable cell-state expression across diseases;
- plausible intervention selectivity;
- perturbation evidence beyond generic IFN shutdown.

Priority families for hour 4-6:

1. `OSM/OSMR` stromal-myeloid inflammatory tissue-licensing axis.
2. complement/C1q resident-myeloid phagocytic axis.
3. `IRF1` / IFN-adjacent licensing, but only if it can pass non-generic
   residual and prior-art controls.

No finding is claimed at this checkpoint.
