# Wave53-H Treatment-Response Stratification Review

Status: completed and closed.

## Verdict

`NO_GO`.

No treatment-response biomarker survives the required V3 bar.

## Best Non-Promotable Signal

Baseline CD4 T-cell `ifn_apc` in RA anti-TNF response is the best hypothesis
only:

- Dataset: `GSE138746`.
- Nominal signal: p = `0.0076`.
- Within-scope FDR = `0.0687`.
- Generic-adjusted p = `0.0244`.
- Global baseline FDR = `0.7738`.
- Global generic-adjusted FDR = `0.9717`.
- Independent same-module replication count = `0`.
- Local files:
  - `results_v3/wave26_treatment_response_strict_audit/strict_baseline_response_audit.tsv`
  - `results_v3/wave26_treatment_response_strict_audit/prior_go_reconciliation.tsv`
  - `results_v3/wave26_treatment_response_strict_audit/summary.json`

## Therapy-Specific Calls

- Anti-TNF RA: best CD4 `ifn_apc` is hypothesis-only, not promotable.
- Tofacitinib UC: baseline marker-derived signals are underpowered and fail
  FDR; best ranked baseline `lipid_loader_repair` has p = `0.129`, FDR =
  `0.674`, `4R/6NR`.
- IL-17/IL-23 psoriasis: secukinumab signals are post-treatment-only and fail
  correction; lysosomal APC p = `0.022`, FDR = `0.199`, `4 pairs`.
- Anti-CD20 MS: ocrelizumab is metadata-only, not analyzed as a response
  biomarker.
- Fumarate MS: dimethyl fumarate `hif_nampt_metabolic` baseline fails,
  p = `0.266`, FDR = `0.674`, `5R/5NR`.
- Fingolimod MS: `ifn_apc` baseline fails, p = `0.199`, FDR = `0.997`,
  `5R/5NR`.
- Rituximab RA: lipid-loader baseline effect is too underpowered,
  `9R/3NR`, FDR = `0.110`, explicitly `NO_GO`.

## Conclusion

Do not reopen treatment-response stratification as V3 evidence. At most, RA
anti-TNF baseline CD4 `ifn_apc` can be parked as a prospective validation idea.

