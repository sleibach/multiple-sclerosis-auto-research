# V36 DMF Power Attenuation Sensitivity

Responder scores are moved toward the nonresponder mean before bootstrap
sampling. This shows how strongly validation size depends on the small
`GSE235357` effect estimate being representative.

| attenuation_fraction | n_per_group | total_n | median_auc | power_one_sided_p_lt_0_05 | power_auc_ge_0_70 |
| --- | --- | --- | --- | --- | --- |
| 1 | 20 | 40 | 0.725 | 0.7598 | 0.6083 |
| 1 | 30 | 60 | 0.7222 | 0.8973 | 0.6225 |
| 1 | 40 | 80 | 0.7219 | 0.9591 | 0.6368 |
| 1 | 50 | 100 | 0.7216 | 0.9836 | 0.6462 |
| 1 | 75 | 150 | 0.7214 | 0.9979 | 0.674 |
| 1 | 100 | 200 | 0.7213 | 0.9997 | 0.6989 |
| 0.75 | 20 | 40 | 0.725 | 0.7688 | 0.6105 |
| 0.75 | 30 | 60 | 0.7222 | 0.8947 | 0.6233 |
| 0.75 | 40 | 80 | 0.7212 | 0.9541 | 0.6381 |
| 0.75 | 50 | 100 | 0.7208 | 0.9839 | 0.6461 |
| 0.75 | 75 | 150 | 0.7211 | 0.9982 | 0.6711 |
| 0.75 | 100 | 200 | 0.72 | 0.9997 | 0.6925 |
| 0.5 | 20 | 40 | 0.685 | 0.6247 | 0.4461 |
| 0.5 | 30 | 60 | 0.6833 | 0.7713 | 0.4223 |
| 0.5 | 40 | 80 | 0.6819 | 0.857 | 0.4018 |
| 0.5 | 50 | 100 | 0.6808 | 0.9164 | 0.3795 |
| 0.5 | 75 | 150 | 0.6814 | 0.9809 | 0.3467 |
| 0.5 | 100 | 200 | 0.68 | 0.9952 | 0.3209 |
| 0.25 | 20 | 40 | 0.64 | 0.4632 | 0.2988 |
| 0.25 | 30 | 60 | 0.6422 | 0.5821 | 0.2431 |
| 0.25 | 40 | 80 | 0.6406 | 0.6785 | 0.2069 |
| 0.25 | 50 | 100 | 0.6416 | 0.7572 | 0.1731 |
| 0.25 | 75 | 150 | 0.6411 | 0.8848 | 0.1265 |
| 0.25 | 100 | 200 | 0.64 | 0.9447 | 0.09267 |

## Interpretation

The planning conclusion is conservative: if the Gafson/fresh-cohort effect
is materially weaker than the observed n=5/5 template, sample size needs
rise quickly and may exceed ordinary public-cohort sizes. This reinforces
that a small fresh cohort should be treated as directional evidence unless
the effect is large and covariates are well measured.
