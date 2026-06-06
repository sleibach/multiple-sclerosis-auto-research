# CONVERGENCE_CHECK_V7_01

Timestamp: 2026-05-28 23:11 CEST

## Validation State

The locked rule has been tested in six independent in-scope cohorts.

- Passes: `GSE16879`, `GSE73661_IFX`.
- Fails: `GSE12051`, `GSE12251`, `GSE138746_CD14`, `GSE8350`.

The pre-specified kill threshold is met for the locked cross-disease rule.

## Conserved-Component Status

The data resolve the IFN/APC-versus-HLA-II question only partially:

- For Class A anti-TNF in intestinal mucosa, the conserved component is dynamic
  IFN/APC downshift.
- Baseline IFN/APC is not a valid fallback.
- RA blood and sorted CD14 monocytes do not show the same predictor.

## Causal-Direction Status

Causality is not established. The paired IBD results support temporal ordering
of transcriptomic change before or near the response-assessment window, but
they do not separate causal downshift from early mucosal healing.

## Decision

Kill `HYP_V6_006` as a locked cross-disease treatment-response stratifier.
Open `HYP_V7_001` as a narrower Tier 0 hypothesis: mucosal IBD anti-TNF
response is marked by early IFN/APC downshift.

## Immediate Follow-Up

An exploratory `GSE73661` vedolizumab W0-to-W6 analysis also shows a strong
IFN/APC downshift association with response: AUC `0.889`, Hedges g `1.286`,
N `24`. Because vedolizumab is Class C under the locked V7 rule, this does not
rescue or modify the locked validation. It changes the biological interpretation
of `HYP_V7_001`: the live signal is likely a **mucosal response/healing
plasticity marker**, not an anti-TNF-specific stratifier.
