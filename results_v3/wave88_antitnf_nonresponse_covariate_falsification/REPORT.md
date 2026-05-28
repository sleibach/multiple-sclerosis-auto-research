# Wave88 Anti-TNF Nonresponse Covariate Falsification

Question: does the Wave86 `IL1B/TREM1/CXCL8/OSM` inflammatory nonresponse circuit add response information beyond neutrophil, stromal/ulceration, epithelial depletion, generic inflammation, and IFN/APC proxies under leave-source-out validation?

Decision: `FALSIFY_CIRCUIT_ADDED_VALUE`.

Reason: added AUC beyond proxy baseline is <=0.05.

## Added Predictive Value

| test_feature | baseline_auc | augmented_auc | delta_auc | baseline_average_precision | augmented_average_precision | delta_average_precision | baseline_brier | augmented_brier | delta_brier |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IL1B | 0.8006 | 0.8128 | 0.01221 | 0.8534 | 0.8588 | 0.005449 | 0.1804 | 0.1744 | -0.006006 |
| TREM1 | 0.8006 | 0.8099 | 0.009302 | 0.8534 | 0.8582 | 0.004825 | 0.1804 | 0.1792 | -0.001209 |
| CXCL8 | 0.8006 | 0.8087 | 0.00814 | 0.8534 | 0.8572 | 0.003854 | 0.1804 | 0.1795 | -0.0008982 |
| circuit_il1b_trem1_cxcl8_osm | 0.8006 | 0.8076 | 0.006977 | 0.8534 | 0.8575 | 0.004153 | 0.1804 | 0.1787 | -0.001785 |
| il1b_lamp3_cross_system | 0.8006 | 0.8006 | 0 | 0.8534 | 0.8502 | -0.003174 | 0.1804 | 0.1793 | -0.001166 |
| LAMP3 | 0.8006 | 0.7936 | -0.006977 | 0.8534 | 0.8464 | -0.006948 | 0.1804 | 0.1845 | 0.004034 |
| OSM | 0.8006 | 0.7936 | -0.006977 | 0.8534 | 0.8495 | -0.003849 | 0.1804 | 0.185 | 0.004588 |

## Primary Circuit Proxy-Adjustment Effect

| feature | scope | n | raw_effect_nonresponse_minus_response | raw_hedges_g_nonresponse_minus_response | raw_p | residual_effect_after_proxies | residual_hedges_g_after_proxies | residual_p_after_proxies | abs_residual_to_raw_g_ratio | raw_fdr | residual_fdr |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| score_circuit_il1b_trem1_cxcl8_osm | pooled_primary_contexts | 83 | 1.156 | 1.536 | 4.771e-10 | 0.04942 | 0.1749 | 0.4252 | 0.1139 | 1.122e-08 | 1 |

## Held-Out Source Metrics

| source_group | n_test | n_nonresponders | auc | average_precision | brier | test_feature | model_name |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ACT1_GSE12251_UC | 22 | 10 | 0.9 | 0.898 | 0.1699 | circuit_il1b_trem1_cxcl8_osm | proxy_baseline |
| ACT1_GSE12251_UC | 22 | 10 | 0.9083 | 0.9028 | 0.1612 | circuit_il1b_trem1_cxcl8_osm | proxy_plus_circuit_il1b_trem1_cxcl8_osm |
| Leuven_GSE14580_UC | 24 | 16 | 0.8125 | 0.9083 | 0.1988 | circuit_il1b_trem1_cxcl8_osm | proxy_baseline |
| Leuven_GSE14580_UC | 24 | 16 | 0.8125 | 0.9083 | 0.2025 | circuit_il1b_trem1_cxcl8_osm | proxy_plus_circuit_il1b_trem1_cxcl8_osm |
| Leuven_GSE16879_Crohn_colitis | 19 | 7 | 1 | 1 | 0.09117 | circuit_il1b_trem1_cxcl8_osm | proxy_baseline |
| Leuven_GSE16879_Crohn_colitis | 19 | 7 | 1 | 1 | 0.08672 | circuit_il1b_trem1_cxcl8_osm | proxy_plus_circuit_il1b_trem1_cxcl8_osm |
| Leuven_GSE16879_Crohn_ileitis | 18 | 10 | 0.7 | 0.7724 | 0.263 | circuit_il1b_trem1_cxcl8_osm | proxy_baseline |
| Leuven_GSE16879_Crohn_ileitis | 18 | 10 | 0.7125 | 0.7745 | 0.2652 | circuit_il1b_trem1_cxcl8_osm | proxy_plus_circuit_il1b_trem1_cxcl8_osm |

## Permutation

| test_feature | observed_delta_auc | n_perm | perm_mean_delta_auc | perm_sd_delta_auc | perm_p_delta_auc_ge_observed |
| --- | --- | --- | --- | --- | --- |
| circuit_il1b_trem1_cxcl8_osm | 0.006977 | 199 | 0.001753 | 0.01741 | 0.26 |

## Guardrail

This remains bulk mucosal treatment-response modeling. A surviving proxy-adjusted association would still be a biomarker/pathotype hypothesis, not a causal circuit or intervention point.
