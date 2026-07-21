# V54 Progressive-Stage Source-Interaction Audit

Verdict: **no_supported_source_tissue_interaction**.

The frozen five-module audit used 44 donor-level observations and 300,000 reduced-model wild-bootstrap replicates. No interaction is called progression because source and tissue are inseparable.

| module | Amsterdam beta | UK beta | UK-minus-Amsterdam interaction | 95% CI | wild p | max-T p | outcome |
|---|---:|---:|---:|---:|---:|---:|---|
| receptor_cd44_cxcr4 | 0.319 | 0.372 | 0.053 | -1.155 to 1.262 | 0.9281 | 1.0000 | interaction_not_supported |
| hla_regulatory | -0.205 | 0.379 | 0.584 | -0.700 to 1.868 | 0.3558 | 0.8745 | interaction_not_supported |
| mif_ligand | 0.222 | -0.173 | -0.395 | -1.694 to 0.903 | 0.5369 | 0.9739 | interaction_not_supported |
| ifn_apc_unique | 0.086 | 0.537 | 0.451 | -0.806 to 1.709 | 0.4630 | 0.9490 | interaction_not_supported |
| lysosomal_unique | -0.075 | 0.842 | 0.917 | -0.373 to 2.208 | 0.1529 | 0.5386 | interaction_inconclusive |

Per-source HC3 intervals and leave-one-donor influence ranges are in `source_effects_lodo.tsv`. Same-sign effects are descriptive; they do not become portable merely because the formal interaction is not supported.

This is a cross-sectional source/tissue sensitivity, not evidence about disability accumulation or a therapeutic control point.
