# Convergence Check 102 - CUX1 Prior-Art Demotion

Timestamp: 2026-05-28 09:41 CEST

## Current Candidate

Wave153-Wave155 identified a reproducible CUX1-associated suppression pattern
in `GSE129487` human synovial fibroblasts:

- CUX1 siRNA is directionally negative across induced interface contexts.
- The strongest gene-level non-STAT subset is ELR+ chemokines:
  `CXCL1`, `CXCL2`, `CXCL3`, `CXCL8`, plus context-dependent `ICAM1`.

## Prior-Art Check

This is not novel as a rheumatoid-fibroblast mechanism.

Verified closest prior work:

- Slowikowski et al., PNAS 2020, DOI `10.1073/pnas.1912702117`, PubMed
  `32079724`.
- Title: "CUX1 and IkappaBzeta (NFKBIZ) mediate the synergistic inflammatory
  response to TNF and IL-17A in stromal fibroblasts."
- The public study page states that the authors performed time-series,
  dose-response, and gene-silencing transcriptomics in human synovial
  fibroblasts and found CUX1/NF-kappaB regulation of `CXCL1`, `CXCL2`, and
  `CXCL3`, independent of `LIFR`, `STAT3`, `STAT4`, and `ELF3`.
- JCI review "Fibroblast pathology in inflammatory diseases" separately
  summarizes CUX1 involvement in `CXCL1`, `CXCL2`, `CXCL3`, and `CXCL8`.

Search queries used:

- `"CUX1" "CXCL1" "CXCL2" "CXCL8" fibroblast`
- `"CUX1" "CXCL8" "CXCL1"`
- `"CUX1" "synovial fibroblasts"`

## Integration

Wave155 independently reproduces and extends the published CUX1 pattern inside
this session's cross-autoimmune interface-module framing, but it cannot be
claimed as a novel target discovery.

The remaining potentially useful angle is not "CUX1 is a new RA fibroblast
target"; it is:

- whether the CUX1/NFKBIZ/ELR+ chemokine fibroblast program is a shared
  cross-autoimmune interface state beyond RA, and
- whether a tractable intervention can selectively interrupt pathological
  interface-cell ELR+ chemokine output without broad JAK/STAT or CXCR1/2
  blockade.

## Next Forcing Question

Does the CUX1/NFKBIZ ELR+ chemokine program reproduce across non-RA autoimmune
interface datasets from Wave152 and prior V3 atlases strongly enough to justify
a stratification biomarker or intervention search?
