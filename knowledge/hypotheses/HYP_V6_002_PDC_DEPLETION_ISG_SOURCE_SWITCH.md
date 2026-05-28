# HYP_V6_002 - pDC Depletion / ISG Source Switch

Status: alive  
Tier: Tier -1  
Opened: 2026-05-28 20:51 CEST

## Hypothesis

MS month-9 pregnancy PBMCs show an interferon-stimulated gene increase from a
non-pDC source or altered trafficking state, because pDC markers decrease while
ISG-only signal increases.

## Opening Evidence

From `GSE17410` sensitivity analysis:

- `isg_only` month-9 versus pre delta `0.8662848708925912`, Hedges g
  `1.1650466279097202`, p `0.02448853974034433`;
- `pdc_marker` delta `-0.23162111368749905`, Hedges g
  `-1.042671101753469`, p `0.03844814819175888`;
- IFN/APC remains after monocyte-only and monocyte+pDC residualization but not
  after all available composition markers.

## Tier -1 Interpretation

The contradiction between ISG increase and pDC marker decrease is not a discard.
It suggests source switching, tissue trafficking, or interferon exposure in
non-pDC populations.

## First Independent Checks

- Decompose ISG source in any pregnancy single-cell dataset with plasmacytoid
  DC, neutrophil, monocyte, and lymphocyte annotations.
- Compare with postpartum flare-prone diseases where late pregnancy interferon
  state and pDC trafficking have been measured.
