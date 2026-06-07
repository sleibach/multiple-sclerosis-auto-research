# V36 Gafson-Style DMF Power Simulation

Assumption: the observed `GSE235357` responder/nonresponder locked-score
distributions are an empirical template for a fresh DMF validation cohort.
This is a planning simulation, not evidence that the effect will replicate.

Observed AUC: `0.720` from `5` responders and `5` nonresponders.

| n_per_group | total_n | n_sim | median_auc | auc_ci_low | auc_ci_high | power_one_sided_p_lt_0_05 | power_auc_ge_0_70 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 8 | 16 | 20000 | 0.7344 | 0.4219 | 0.9688 | 0.4783 | 0.5806 |
| 10 | 20 | 20000 | 0.74 | 0.45 | 0.96 | 0.5418 | 0.6142 |
| 12 | 24 | 20000 | 0.7222 | 0.4722 | 0.9306 | 0.5915 | 0.5915 |
| 15 | 30 | 20000 | 0.7244 | 0.5067 | 0.9067 | 0.6721 | 0.59 |
| 20 | 40 | 20000 | 0.725 | 0.5375 | 0.8875 | 0.7774 | 0.6188 |
| 25 | 50 | 20000 | 0.7232 | 0.5568 | 0.872 | 0.8516 | 0.6054 |
| 30 | 60 | 20000 | 0.7222 | 0.5678 | 0.8556 | 0.8973 | 0.6266 |
| 40 | 80 | 20000 | 0.7219 | 0.5906 | 0.8413 | 0.9566 | 0.637 |
| 50 | 100 | 20000 | 0.7212 | 0.6032 | 0.828 | 0.981 | 0.6486 |

## Interpretation

At the observed effect size, small n=10-20 total cohorts are expected to be
directional but underpowered. A decisive fresh validation likely needs on
the order of `40-50` subjects per response group, or a stronger true effect
than the small GSE235357 template suggests.
