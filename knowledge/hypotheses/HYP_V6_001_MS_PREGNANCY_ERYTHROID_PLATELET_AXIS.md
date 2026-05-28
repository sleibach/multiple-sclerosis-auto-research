# HYP_V6_001 - MS Pregnancy Erythroid / Platelet Axis

Status: alive  
Tier: Tier -1  
Opened: 2026-05-28 20:51 CEST

## Hypothesis

In MS pregnancy PBMC at month 9, the apparent IFN/APC increase is partly a
hematologic composition state involving erythroid, platelet, and neutrophil
signals; this state may mark endothelial/coagulation/innate priming relevant to
postpartum relapse risk rather than APC activation.

## Opening Evidence

From `results/pregnancy_dimension/gse17410_ms_sensitivity/`:

- erythroid marker month-9 versus pre delta `2.791872935925154`, Hedges g
  `1.3560227945307173`, Welch p `0.009582015527605712`;
- platelet marker delta `0.8206577388359371`, Hedges g
  `1.031401084388657`, p `0.043306961443473554`;
- neutrophil marker delta `0.3145609478083351`, Hedges g
  `1.1330365830564075`, p `0.02622644650507269`;
- all-composition residualization reduces IFN/APC delta from
  `0.6358630063022481` to `0.09491044766501967`.

## Why This Is Tier -1

The original IFN/APC therapeutic interpretation weakened, but the absorbed
composition signal is large, coherent, and biologically plausible in pregnancy.

## First Independent Checks

- Search for MS pregnancy/postpartum blood datasets with relapse annotations.
- Test whether platelet/neutrophil/erythroid modules rise before postpartum
  immune rebound in RA/SLE/healthy pregnancy datasets.
- Check whether the signal is technical blood fraction contamination by
  comparing hemoglobin/platelet genes against sample quality markers.
