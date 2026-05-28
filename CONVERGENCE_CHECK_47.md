# Convergence Check 47: Psoriasis Anti-TNF Stress Test

Timestamp: 2026-05-27 19:10 CEST

## Forcing Question

Do `IL1B` and `LAMP3`, the only Wave86/Wave87 genes that survived from IBD
mucosa into RA synovium, also predict anti-TNF nonresponse in a third
autoimmune tissue system?

## Analysis Executed

Script:

- `scripts/v3_wave89_psoriasis_gse85034_response_validation.py`

Dataset:

- `GSE85034`, GPL10558 baseline lesional psoriasis skin with adalimumab and
  methotrexate treatment arms.

Endpoint:

- Week-16 PASI75 reconstructed from GEO PASI values.

Primary test:

- Baseline lesional-skin expression in the adalimumab arm.

## Result

Wave89 call:

- `WEAK_DIRECTIONAL_THIRD_DISEASE_SUPPORT_ONLY`

Treatment counts:

- Adalimumab: `14` evaluable subjects, `9` PASI75 responders, `5`
  nonresponders.
- Methotrexate: `13` evaluable subjects, `3` responders, `10` nonresponders.

Primary genes:

- `IL1B`: same nonresponse-high direction in adalimumab psoriasis, but weak:
  Hedges g `-0.6325`, AUC high-expression nonresponse `0.5556`, p `0.3940`.
- `LAMP3`: opposite direction in adalimumab psoriasis:
  Hedges g `0.4960`, AUC high-expression nonresponse `0.3556`, p `0.2968`.

Unexpected lead:

- `LPL` is the strongest adalimumab gene-level signal among the tested module
  genes:
  - Hedges g responder-minus-nonresponder `-2.2089`
  - AUC high-expression nonresponse `0.9556`
  - p `0.0111`
  - FDR across tested genes `0.4998`
- `lysosomal_apc` module is also nonresponse-high in adalimumab psoriasis:
  Hedges g `-1.017`, AUC `0.7778`, p `0.1237`.

## Convergence

Agree:

- IBD and psoriasis both contain a pretreatment tissue state in which
  inflammatory/lipid/lysosomal myeloid genes are higher in anti-TNF
  nonresponders.
- The specific single-gene anchor is not stable across diseases.

Disagree:

- `LAMP3` supports IBD/RA but reverses in psoriasis.
- `IL1B` supports IBD/RA but is weak in psoriasis.
- A broad inflammatory/IFN anti-TNF resistance claim is still blocked by
  Wave87 RA reversals.

## Decision

Do not promote `IL1B`/`LAMP3` as the cross-disease mechanism.

Reformulate the branch around the lipid-lysosomal myeloid state, with `LPL`
as a new falsifiable lead to test across existing MS/IBD/RA/psoriasis outputs.
The immediate question is whether `LPL` is:

1. a small-cohort psoriasis artifact,
2. a marker of lipid-loaded tissue macrophages,
3. a causal lipid-uptake amplifier with a tractable upstream/downstream
   intervention point.

## Self-Critique

- The adalimumab arm has only `14` evaluable subjects. The `LPL` effect is
  large but unstable until independently replicated.
- `LPL` FDR is not significant because many module genes were screened in a
  small arm. It is lead-generating only.
- `LPL` itself may be a poor drug target: systemic LPL inhibition would be
  metabolically dangerous, while activation may be directionally wrong if
  high lipid uptake is pathogenic.
- A better intervention point may be an upstream tissue cue or downstream lipid
  handling controller rather than LPL itself.
