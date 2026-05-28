# GSE282122 MIF/CD74 Anti-TNF Remission Interaction

Random seed: `20260528`

## Dataset

Local V3 paired IBD anti-TNF pseudobulk:
`results_v3/wave67_gse282122_myeloid_pseudobulk/paired_module_deltas.tsv`.

The test asks whether `mif_cd74_receptor_state` behaves as a treatment-response
or remission biomarker after controlling for baseline target score, IFN/APC
module delta, baseline inflammation score, and Crohn versus UC.

## Result

Dynamic response is adverse for a "remission lowers MIF/CD74" hypothesis:

- Major monocyte/macrophage: remission is associated with a larger post-treatment
  increase in `mif_cd74_receptor_state`, adjusted delta
  `0.4840720173619233`, adjusted p `0.03473492719224309`.
- Major DC: same direction but not adjusted-significant, adjusted delta
  `0.1954004175949041`, adjusted p `0.21222452353534355`.

Baseline prediction is weaker and conflicted:

- Major monocyte/macrophage lower baseline `mif_cd74_receptor_state` predicts
  remission after adjustment, logit coefficient `-4.088480806349443`, p
  `0.009857151903175113`.
- The raw baseline remission-versus-nonremission difference is not significant:
  Hedges g `-0.38734765558900636`, raw p `0.22965575235386465`.
- Several fine-cell logit fits emitted perfect-separation/convergence warnings;
  those rows should not be used as strong evidence.

## Interpretation

This does not rescue MIF/CD74 as a Tier 1 stratification biomarker. The dynamic
and baseline signals point in different directions: remission is associated with
increased post-treatment MIF/CD74 state, while lower baseline state may predict
remission in one adjusted monocyte/macrophage model. Treat this as an
IBD-specific response-state complication, not a clean cross-autoimmune
stratification result.

## Trace

- Script: `scripts/tier0_mif_cd74_gse282122_remission_interaction.py`
- Outputs:
  - `mif_cd74_remission_interaction.tsv`
  - `mif_cd74_baseline_predictive.tsv`
  - `summary.json`
