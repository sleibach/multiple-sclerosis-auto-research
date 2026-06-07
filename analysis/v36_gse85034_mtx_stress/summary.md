# V36 GSE85034 MTX Stress Test

This is a caveated cross-disease stress test of the immutable V22 dynamic
IFN/APC feature in the unused GSE85034 methotrexate arm. It is psoriasis
lesional skin, not MS blood/CSF and not the bounded immune-remodeling
validation setting; it therefore cannot upgrade or kill the V22/V23 lead.

## Cohort

- Paired labeled subjects: `13`.
- PASI75 responders/nonresponders: `3` / `10`.
- Feature: baseline lesional skin to week 1; outcome PASI75 at week 16.
- IFN/APC genes present: `STAT1;IRF1;CXCL10;GBP1;ISG15;CD74;HLA-DRA`.
- HLA-II genes present: `HLA-DRA;HLA-DRB1;HLA-DPA1;HLA-DPB1;HLA-DQB1`.
- receptor genes present: `CD74;CD44;CXCR4`.

## Feature Tests

| feature | n | n_responders | n_nonresponders | auc_high_score_response | exact_auc_p | mean_responder | mean_nonresponder | hedges_g_responder_minus_non | welch_p |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| locked_signed_score | 13 | 3 | 10 | 0.6 | 0.3462 | 0.0301 | -0.03986 | 0.1654 | 0.7634 |
| delta_IFN_APC | 13 | 3 | 10 | 0.4 | 0.7133 | -0.0301 | 0.03986 | -0.1654 | 0.7634 |
| delta_HLAII | 13 | 3 | 10 | 0.3 | 0.8566 | -0.3547 | 0.1014 | -0.6868 | 0.181 |
| negative_delta_RECEPTOR | 13 | 3 | 10 | 0.9 | 0.02448 | 0.3715 | -0.2176 | 1.092 | 0.008399 |

## Interpretation

The result is recorded as a stress test only. A positive metric would show
that early dynamic immune-remodeling information is not unique to the
tofacitinib artifact, while a negative metric would be unsurprising because
methotrexate psoriasis skin is outside the V23 bounded domain. Either way,
the primary validation target remains the pre-specified V22/V23 monitoring
rule in a fresh MS DMT cohort with steroid, QC, batch, timing, and cell
composition metadata.
