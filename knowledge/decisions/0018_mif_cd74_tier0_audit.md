# Decision 0018: MIF/CD74 Stratification Tier 0 Audit

Date: 2026-05-28

## Decision

`MIF_CD74_STRATIFICATION` remains parked at Tier 0.

## Rationale

The V4 contribution is not broad MIF/CD74 therapeutic targeting. That is heavily
prior-arted and not novel. The surviving contribution is a predictive or
enrichment biomarker: a `CD74/CD44/CXCR4/HLA-II` receptor-state score that may
identify progressive-MS or other autoimmune patients likely to respond to
MIF/CD74-axis or APC-state modulation.

The local Tier 0 audit does not support promotion:

- MS white-matter microglia show nominal IFN-residual support:
  residual delta `0.45572407980566854`, Hedges g `1.247930189567055`,
  p `0.007887505384977308`, residual FDR `0.4417003015587293`.
- Sjogren epithelial residual support is weak and highly IFN-coupled:
  residual p `0.07344896860686509`, residual FDR `0.97363654262921`,
  target-vs-IFN R2 `0.9015149582126574`.
- No MIF/CD74 residual test survives FDR `<=0.10`.
- The available local IBD remission interaction table does not test
  `mif_cd74_receptor_state`.

## Next Valid Test

Run component-resolved residualization and treatment-response interaction:

- `CD74` alone;
- `CD74/CD44/CXCR4`;
- HLA-II-only;
- full `mif_cd74_receptor_state`.

Advance only if the predictive or residual signal is not explained by HLA-II
alone, generic `ifn_apc`, cell composition, or baseline inflammatory burden.

## Trace

- Script: `scripts/tier0_mif_cd74_stratification_audit.py`
- Outputs:
  - `analysis/tier_0_triage/mif_cd74_stratification/REPORT.md`
  - `analysis/tier_0_triage/mif_cd74_stratification/decision.json`
  - `analysis/tier_0_triage/mif_cd74_stratification/residual_evidence.tsv`
- Sidecar: Archimedes (`019e6e35-797c-7e23-9a0d-f96dce57dc88`)
