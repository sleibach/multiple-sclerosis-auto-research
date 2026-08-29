# V57 V22 Gene-Influence Audit

## Result

- Full predeclared no-single-gene-dominance gate: **PASS**.
- Intact pooled cohort-percentile AUC: `0.822`.
- Weakest deletion: `CXCL10`, AUC `0.800`.
- Maximum AUC loss: `0.022`.
- Exact intersection-null p-value: `0.008062` across `31,752`
  responder-count-preserving assignments.
- Weakest cohort-specific result: omission of
  `CXCL10` in
  `GSE235357`, AUC
  `0.680`.

| omitted gene | pooled percentile AUC | loss vs intact | pooled raw AUC |
|---|---:|---:|---:|
| CXCL10 | 0.800 | 0.022 | 0.800 |
| GBP1 | 0.822 | 0.000 | 0.833 |
| HLA-DPA1 | 0.822 | 0.000 | 0.811 |
| HLA-DPB1 | 0.822 | 0.000 | 0.811 |
| HLA-DRA | 0.822 | 0.000 | 0.811 |
| HLA-DRB1 | 0.822 | 0.000 | 0.811 |
| ISG15 | 0.822 | 0.000 | 0.811 |
| STAT1 | 0.822 | 0.000 | 0.811 |
| CD74 | 0.844 | -0.022 | 0.811 |
| HLA-DQB1 | 0.844 | -0.022 | 0.822 |
| IRF1 | 0.844 | -0.022 | 0.856 |
| HLA-DQA1 | 0.867 | -0.044 | 0.833 |

## Interpretation boundary

This is a complete, selection-corrected leave-one-gene-out sensitivity analysis
on the same two bounded cohorts. It neither modifies the immutable score nor
creates a successor. Even a pass would only exclude dependence on one listed
gene as a sufficient explanation in these data; it would not establish
mechanism, cross-environment recurrence, transportability, or clinical value.
The cohort-specific minimum below 0.70 is retained explicitly: pooled
leave-one-gene-out robustness does not repair the formal partial-conjunction
failure or establish that the association recurs independently in both
environments.
