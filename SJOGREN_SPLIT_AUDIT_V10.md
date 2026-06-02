# SJOGREN_SPLIT_AUDIT_V10

Status: V10 matched-compartment audit of Sjogren IFN/APC versus
lipid-lysosomal disagreement.

## Question

Is Sjogren's supported disagreement real or just a compartment artifact?

Supported V8 placements:

- `axis_01_ifn_apc`: `near/supported/medium`.
- `axis_04_lipid_lysosomal`: `far/supported/medium`.

## Data Source

Local V3 convergence table:

- `results_v3/cross_disease_cell_state_convergence.tsv`

Contexts:

- `sjogren_gland_epithelial`: salivary gland epithelial, `11` case donors and
  `14` controls.
- `sjogren_gland_apc`: salivary gland APC, `9` case donors and `13` controls.

## Module-Level Results

| Compartment | Module | Delta | Hedges g | p | FDR | Support |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| salivary gland epithelial | `hla_ii_apc` | `0.2037` | `1.034` | `0.0206` | `0.0914` | supportive |
| salivary gland epithelial | `mif_cd74_receptor_state` | `0.2070` | `1.075` | `0.0207` | `0.0914` | supportive |
| salivary gland epithelial | `ifn_apc` | `0.1495` | `0.844` | `0.0568` | `0.157` | trend |
| salivary gland APC | `mif_cd74_receptor_state` | `0.0992` | `0.747` | `0.0831` | `0.199` | trend |
| salivary gland APC | `ifn_apc` | `0.0832` | `0.687` | `0.101` | `0.235` | positive-null |
| salivary gland APC | `lipid_loader_repair` | `-0.1294` | `-0.774` | `0.0554` | `0.156` | negative trend |
| salivary gland epithelial | `lipid_loader_repair` | `-0.0166` | `-0.202` | `0.604` | `0.697` | null/negative |
| salivary gland APC | `lysosomal_apc` | `-0.0635` | `-0.307` | `0.434` | `0.555` | null/negative |
| salivary gland epithelial | `lysosomal_apc` | `-0.0516` | `-0.267` | `0.484` | `0.600` | null/negative |

## Artifact Audit

Compartment artifact:

- Partly mitigated. IFN/APC support is strongest in epithelial cells, but APC
  compartment also trends positive for MIF/CD74 and IFN/APC.
- Lipid-loader and lysosomal modules are negative or null in both epithelial
  and APC compartments.

Cohort artifact:

- Both compartments come from the same local Sjogren salivary gland atlas
  family used in V3.
- Donor counts are modest, so confidence remains medium at best.

Measurement-grade artifact:

- Both are cross-sectional donor mean module contrasts.
- No causal or longitudinal evidence.

## Mechanistic Interpretation

The Sjogren split survives first compartment audit as a biological candidate:

> Sjogren salivary gland disease shares MS-like antigen-presentation activation
> but not MS-like lipid-lysosomal / foamy myeloid repair-state biology.

This is a cleaner axis disagreement than the UC treatment-response versus
tissue-repair row because it compares distinct module families rather than
overlapping dynamic response evidence.

## MS Transfer Consequence

What may transfer:

- epithelial/barrier antigen-presentation mechanisms;
- MIF/CD74/HLA-II epithelial immune activation as a comparator for
  non-myeloid antigen-presentation states.

What should not transfer without new evidence:

- chronic-active lesion rim lipid-lysosomal/foamy myeloid biology;
- TREM2/APOE/LPL/GPNMB-like repair-state hypotheses from Sjogren salivary data.

## Falsifiable Prediction

In an independent Sjogren salivary single-cell or spatial dataset:

- HLA-II/CD74/IFN epithelial or APC antigen-presentation modules should be
  positive or enriched in disease.
- Lipid-loader / lysosomal repair modules should remain null or negative in
  myeloid/APC compartments after cell-type and donor adjustment.

Stop-loss:

- If matched myeloid compartments show a reproducible positive lipid-lysosomal
  repair module with Hedges g `>=0.5` and corrected p/FDR support, the V10
  split is downgraded to dataset artifact.

## Current Tier

Tier 1 biological disagreement candidate. It is not a therapeutic claim.
