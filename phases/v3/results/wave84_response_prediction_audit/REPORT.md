# Wave84 Response-Prediction Audit

## Question

Does a frozen baseline lysosomal/APC response state improve out-of-sample
anti-TNF response prediction beyond generic inflammation and available
clinical/pathotype covariates?

## Verdict

PARK_STRATIFICATION_WEAK_PREDICTIVE_SIGNAL

## Decision

| candidate | wave84_call | decision_reason | primary_module | ra_delta_auc | ra_augmented_auc | ra_delta_auc_perm_p | ra_delta_auc_boot_ci_low | ibd_delta_auc | ibd_augmented_auc | ibd_delta_auc_perm_p | ibd_delta_auc_boot_ci_low | both_delta_positive | both_coef_positive | both_perm_support | both_perm_trend | both_boot_ci_excludes_zero | both_auc_ge_060 | uc_stress_best_delta_auc | legacy_rows |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| lysosomal_APC_baseline_antiTNF_response_stratification | PARK_STRATIFICATION_WEAK_PREDICTIVE_SIGNAL | direction and added AUC are stable, but permutation p-values are trend-level and bootstrap CIs include zero | lysosomal_apc__resid_inflammatory_nfkb | 0.07018 | 0.7368 | 0.122 | -0.04925 | 0.1587 | 0.726 | 0.116 | -0.05055 | True | True | False | True | False | True | 0.4333 | 30 |

## Primary RA/IBD Added-AUC Comparisons

| dataset | response_definition | module | baseline_auc | augmented_auc | delta_auc | baseline_average_precision | augmented_average_precision | baseline_brier | augmented_brier | target_coef | target_coef_positive | n_perm | delta_auc_perm_p | perm_mean_delta_auc | delta_auc_boot_ci_low | delta_auc_boot_ci_high |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GSE198520_RA_synovium_antiTNF | good_vs_moderate_none | lysosomal_apc__resid_inflammatory_nfkb | 0.6667 | 0.7368 | 0.07018 | 0.533 | 0.5585 | 0.2353 | 0.2101 | 1.021 | True | 499 | 0.122 | 0.002582 | -0.04925 | 0.1763 |
| GSE198520_RA_synovium_antiTNF | good_vs_moderate_none | lysosomal_apc | 0.6667 | 0.7388 | 0.07212 | 0.533 | 0.5586 | 0.2353 | 0.2095 | 1.06 | True | 0 |  |  |  |  |
| GSE198520_RA_synovium_antiTNF | good_vs_moderate_none | ifn_lysosomal_apc_composite__resid_inflammatory_nfkb | 0.6667 | 0.7329 | 0.06628 | 0.533 | 0.5756 | 0.2353 | 0.2138 | 0.9993 | True | 0 |  |  |  |  |
| GSE198520_RA_synovium_antiTNF | good_vs_moderate_none | ifn_lysosomal_apc_composite | 0.6667 | 0.7329 | 0.06628 | 0.533 | 0.5743 | 0.2353 | 0.2134 | 1.044 | True | 0 |  |  |  |  |
| GSE198520_RA_synovium_antiTNF | good_vs_moderate_none | ifn_apc__resid_inflammatory_nfkb | 0.6667 | 0.7173 | 0.05068 | 0.533 | 0.5776 | 0.2353 | 0.2252 | 0.8021 | True | 0 |  |  |  |  |
| GSE198520_RA_synovium_antiTNF | good_vs_moderate_none | ifn_apc | 0.6667 | 0.7135 | 0.04678 | 0.533 | 0.5752 | 0.2353 | 0.2249 | 0.8432 | True | 0 |  |  |  |  |
| GSE282122_IBD_DC_antiTNF | remission_vs_nonremission | lysosomal_apc__resid_inflammatory_nfkb | 0.5673 | 0.726 | 0.1587 | 0.4859 | 0.6943 | 0.241 | 0.2126 | 0.8722 | True | 499 | 0.116 | 0.01446 | -0.05055 | 0.3922 |
| GSE282122_IBD_DC_antiTNF | remission_vs_nonremission | lysosomal_apc | 0.5673 | 0.7212 | 0.1538 | 0.4859 | 0.6904 | 0.241 | 0.2125 | 0.9408 | True | 0 |  |  |  |  |
| GSE282122_IBD_DC_antiTNF | remission_vs_nonremission | ifn_lysosomal_apc_composite__resid_inflammatory_nfkb | 0.5673 | 0.6827 | 0.1154 | 0.4859 | 0.6283 | 0.241 | 0.2297 | 0.7804 | True | 0 |  |  |  |  |
| GSE282122_IBD_DC_antiTNF | remission_vs_nonremission | ifn_lysosomal_apc_composite | 0.5673 | 0.6875 | 0.1202 | 0.4859 | 0.6295 | 0.241 | 0.2295 | 0.8173 | True | 0 |  |  |  |  |
| GSE282122_IBD_DC_antiTNF | remission_vs_nonremission | ifn_apc__resid_inflammatory_nfkb | 0.5673 | 0.6442 | 0.07692 | 0.4859 | 0.5589 | 0.241 | 0.2516 | 0.4035 | True | 0 |  |  |  |  |
| GSE282122_IBD_DC_antiTNF | remission_vs_nonremission | ifn_apc | 0.5673 | 0.6394 | 0.07212 | 0.4859 | 0.5619 | 0.241 | 0.2515 | 0.4087 | True | 0 |  |  |  |  |

## Primary Model Metrics

| dataset | response_definition | model_name | target_feature | fit_status | n | n_positive | n_negative | auc | average_precision | brier | balanced_accuracy_0_5 | full_model_target_coef |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GSE198520_RA_synovium_antiTNF | good_vs_moderate_none | generic_clinical_baseline |  | ok | 46 | 19 | 27 | 0.6667 | 0.533 | 0.2353 | 0.6491 |  |
| GSE198520_RA_synovium_antiTNF | good_vs_moderate_none | generic_plus_lysosomal_apc__resid_inflammatory_nfkb | pre_score_lysosomal_apc__resid_inflammatory_nfkb | ok | 46 | 19 | 27 | 0.7368 | 0.5585 | 0.2101 | 0.694 | 1.021 |
| GSE198520_RA_synovium_antiTNF | good_vs_moderate_none | generic_plus_lysosomal_apc | pre_score_lysosomal_apc | ok | 46 | 19 | 27 | 0.7388 | 0.5586 | 0.2095 | 0.694 | 1.06 |
| GSE198520_RA_synovium_antiTNF | good_vs_moderate_none | generic_plus_ifn_lysosomal_apc_composite__resid_inflammatory_nfkb | pre_score_ifn_lysosomal_apc_composite__resid_inflammatory_nfkb | ok | 46 | 19 | 27 | 0.7329 | 0.5756 | 0.2138 | 0.694 | 0.9993 |
| GSE198520_RA_synovium_antiTNF | good_vs_moderate_none | generic_plus_ifn_lysosomal_apc_composite | pre_score_ifn_lysosomal_apc_composite | ok | 46 | 19 | 27 | 0.7329 | 0.5743 | 0.2134 | 0.694 | 1.044 |
| GSE198520_RA_synovium_antiTNF | good_vs_moderate_none | generic_plus_ifn_apc__resid_inflammatory_nfkb | pre_score_ifn_apc__resid_inflammatory_nfkb | ok | 46 | 19 | 27 | 0.7173 | 0.5776 | 0.2252 | 0.6491 | 0.8021 |
| GSE198520_RA_synovium_antiTNF | good_vs_moderate_none | generic_plus_ifn_apc | pre_score_ifn_apc | ok | 46 | 19 | 27 | 0.7135 | 0.5752 | 0.2249 | 0.6491 | 0.8432 |
| GSE282122_IBD_DC_antiTNF | remission_vs_nonremission | generic_clinical_baseline |  | ok | 29 | 13 | 16 | 0.5673 | 0.4859 | 0.241 | 0.6587 |  |
| GSE282122_IBD_DC_antiTNF | remission_vs_nonremission | generic_plus_lysosomal_apc__resid_inflammatory_nfkb | pre_score_lysosomal_apc__resid_inflammatory_nfkb | ok | 29 | 13 | 16 | 0.726 | 0.6943 | 0.2126 | 0.6274 | 0.8722 |
| GSE282122_IBD_DC_antiTNF | remission_vs_nonremission | generic_plus_lysosomal_apc | pre_score_lysosomal_apc | ok | 29 | 13 | 16 | 0.7212 | 0.6904 | 0.2125 | 0.6274 | 0.9408 |
| GSE282122_IBD_DC_antiTNF | remission_vs_nonremission | generic_plus_ifn_lysosomal_apc_composite__resid_inflammatory_nfkb | pre_score_ifn_lysosomal_apc_composite__resid_inflammatory_nfkb | ok | 29 | 13 | 16 | 0.6827 | 0.6283 | 0.2297 | 0.5962 | 0.7804 |
| GSE282122_IBD_DC_antiTNF | remission_vs_nonremission | generic_plus_ifn_lysosomal_apc_composite | pre_score_ifn_lysosomal_apc_composite | ok | 29 | 13 | 16 | 0.6875 | 0.6295 | 0.2295 | 0.5962 | 0.8173 |
| GSE282122_IBD_DC_antiTNF | remission_vs_nonremission | generic_plus_ifn_apc__resid_inflammatory_nfkb | pre_score_ifn_apc__resid_inflammatory_nfkb | ok | 29 | 13 | 16 | 0.6442 | 0.5589 | 0.2516 | 0.5817 | 0.4035 |
| GSE282122_IBD_DC_antiTNF | remission_vs_nonremission | generic_plus_ifn_apc | pre_score_ifn_apc | ok | 29 | 13 | 16 | 0.6394 | 0.5619 | 0.2515 | 0.5817 | 0.4087 |
| GSE253006_UC_tofacitinib_marker | b_plasma_like_baseline_responder | generic_baseline |  | ok | 11 | 5 | 6 | 0 | 0.3161 | 0.3232 | 0 |  |
| GSE253006_UC_tofacitinib_marker | b_plasma_like_baseline_responder | generic_plus_lysosomal_apc | pre_score_lysosomal_apc | ok | 11 | 5 | 6 | 0.2 | 0.3633 | 0.3388 | 0.2667 | -0.3468 |
| GSE253006_UC_tofacitinib_marker | b_plasma_like_baseline_responder | generic_plus_ifn_apc | pre_score_ifn_apc | ok | 11 | 5 | 6 | 0.1333 | 0.3542 | 0.3588 | 0.2667 | 0.3675 |
| GSE253006_UC_tofacitinib_marker | epithelial_like_baseline_responder | generic_baseline |  | ok | 11 | 5 | 6 | 0 | 0.3161 | 0.3353 | 0.3333 |  |
| GSE253006_UC_tofacitinib_marker | epithelial_like_baseline_responder | generic_plus_lysosomal_apc | pre_score_lysosomal_apc | ok | 11 | 5 | 6 | 0.4333 | 0.5042 | 0.3541 | 0.5333 | 0.5251 |
| GSE253006_UC_tofacitinib_marker | epithelial_like_baseline_responder | generic_plus_ifn_apc | pre_score_ifn_apc | ok | 11 | 5 | 6 | 0 | 0.3161 | 0.4056 | 0.08333 | -0.007073 |
| GSE253006_UC_tofacitinib_marker | myeloid_apc_like_baseline_responder | generic_baseline |  | ok | 11 | 5 | 6 | 0.4 | 0.4352 | 0.3171 | 0.65 |  |
| GSE253006_UC_tofacitinib_marker | myeloid_apc_like_baseline_responder | generic_plus_lysosomal_apc | pre_score_lysosomal_apc | ok | 11 | 5 | 6 | 0.3333 | 0.4233 | 0.3585 | 0.3667 | -0.3082 |
| GSE253006_UC_tofacitinib_marker | myeloid_apc_like_baseline_responder | generic_plus_ifn_apc | pre_score_ifn_apc | ok | 11 | 5 | 6 | 0.3333 | 0.4176 | 0.334 | 0.45 | -0.4988 |
| GSE253006_UC_tofacitinib_marker | stromal_endothelial_like_baseline_responder | generic_baseline |  | ok | 10 | 4 | 6 | 0.5 | 0.4583 | 0.2772 | 0.625 |  |
| GSE253006_UC_tofacitinib_marker | stromal_endothelial_like_baseline_responder | generic_plus_lysosomal_apc | pre_score_lysosomal_apc | ok | 10 | 4 | 6 | 0.625 | 0.5792 | 0.2938 | 0.625 | 0.668 |
| GSE253006_UC_tofacitinib_marker | stromal_endothelial_like_baseline_responder | generic_plus_ifn_apc | pre_score_ifn_apc | ok | 10 | 4 | 6 | 0.5833 | 0.6071 | 0.2493 | 0.5833 | 0.6706 |
| GSE253006_UC_tofacitinib_marker | t_cell_like_baseline_responder | generic_baseline |  | ok | 11 | 5 | 6 | 0.2667 | 0.3866 | 0.2939 | 0.3667 |  |
| GSE253006_UC_tofacitinib_marker | t_cell_like_baseline_responder | generic_plus_lysosomal_apc | pre_score_lysosomal_apc | ok | 11 | 5 | 6 | 0.2667 | 0.3833 | 0.3164 | 0.3667 | 0.3668 |
| GSE253006_UC_tofacitinib_marker | t_cell_like_baseline_responder | generic_plus_ifn_apc | pre_score_ifn_apc | ok | 11 | 5 | 6 | 0.03333 | 0.3209 | 0.3497 | 0.08333 | 0.1027 |

## UC Tofacitinib Orthogonal Stress Test

| dataset | response_definition | module | baseline_auc | augmented_auc | delta_auc | target_coef | n | note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GSE253006_UC_tofacitinib_marker | b_plasma_like_baseline_responder | lysosomal_apc | 0 | 0.2 | 0.2 | -0.3468 | 11 | small orthogonal stress test; not a primary anti-TNF replication dataset |
| GSE253006_UC_tofacitinib_marker | b_plasma_like_baseline_responder | ifn_apc | 0 | 0.1333 | 0.1333 | 0.3675 | 11 | small orthogonal stress test; not a primary anti-TNF replication dataset |
| GSE253006_UC_tofacitinib_marker | epithelial_like_baseline_responder | lysosomal_apc | 0 | 0.4333 | 0.4333 | 0.5251 | 11 | small orthogonal stress test; not a primary anti-TNF replication dataset |
| GSE253006_UC_tofacitinib_marker | epithelial_like_baseline_responder | ifn_apc | 0 | 0 | 0 | -0.007073 | 11 | small orthogonal stress test; not a primary anti-TNF replication dataset |
| GSE253006_UC_tofacitinib_marker | myeloid_apc_like_baseline_responder | lysosomal_apc | 0.4 | 0.3333 | -0.06667 | -0.3082 | 11 | small orthogonal stress test; not a primary anti-TNF replication dataset |
| GSE253006_UC_tofacitinib_marker | myeloid_apc_like_baseline_responder | ifn_apc | 0.4 | 0.3333 | -0.06667 | -0.4988 | 11 | small orthogonal stress test; not a primary anti-TNF replication dataset |
| GSE253006_UC_tofacitinib_marker | stromal_endothelial_like_baseline_responder | lysosomal_apc | 0.5 | 0.625 | 0.125 | 0.668 | 10 | small orthogonal stress test; not a primary anti-TNF replication dataset |
| GSE253006_UC_tofacitinib_marker | stromal_endothelial_like_baseline_responder | ifn_apc | 0.5 | 0.5833 | 0.08333 | 0.6706 | 10 | small orthogonal stress test; not a primary anti-TNF replication dataset |
| GSE253006_UC_tofacitinib_marker | t_cell_like_baseline_responder | lysosomal_apc | 0.2667 | 0.2667 | 5.551e-17 | 0.3668 | 11 | small orthogonal stress test; not a primary anti-TNF replication dataset |
| GSE253006_UC_tofacitinib_marker | t_cell_like_baseline_responder | ifn_apc | 0.2667 | 0.03333 | -0.2333 | 0.1027 | 11 | small orthogonal stress test; not a primary anti-TNF replication dataset |

## Legacy Sensitivity Evidence

| dataset | evidence_type | context | module | effect_or_delta | p | fdr | auc_responder_high | interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GSE138746_RA_sorted_blood_antiTNF | baseline_response_sensitivity | CD4_T_cell\|adalimumab\|eular_responder_moderate_or_good_vs_none | ifn_apc | 0.5857 | 0.007628 | 0.6056 | 0.7515 | blood/sorted-compartment sensitivity; not primary tissue replication |
| GSE138746_RA_sorted_blood_antiTNF | baseline_response_sensitivity | CD4_T_cell\|adalimumab\|good_responder_vs_none | ifn_apc | 0.6829 | 0.01784 | 0.6056 | 0.7929 | blood/sorted-compartment sensitivity; not primary tissue replication |
| GSE138746_RA_sorted_blood_antiTNF | baseline_response_sensitivity | CD14_monocyte\|etanercept\|eular_responder_moderate_or_good_vs_none | lysosomal_apc | -0.4949 | 0.0273 | 0.6678 | 0.3043 | blood/sorted-compartment sensitivity; not primary tissue replication |
| GSE138746_RA_sorted_blood_antiTNF | baseline_response_sensitivity | CD14_monocyte\|all_anti_tnf_drug_adjusted\|eular_responder_moderate_or_good_vs_none | lysosomal_apc | -0.277 | 0.04291 | 0.7724 | 0.3665 | blood/sorted-compartment sensitivity; not primary tissue replication |
| GSE138746_RA_sorted_blood_antiTNF | baseline_response_sensitivity | PBMC\|adalimumab\|good_responder_vs_none | ifn_apc | 0.4568 | 0.0954 | 0.8091 | 0.6833 | blood/sorted-compartment sensitivity; not primary tissue replication |
| GSE138746_RA_sorted_blood_antiTNF | baseline_response_sensitivity | CD14_monocyte\|adalimumab\|good_responder_vs_none | ifn_apc | 0.4368 | 0.1047 | 0.8091 | 0.6869 | blood/sorted-compartment sensitivity; not primary tissue replication |
| GSE138746_RA_sorted_blood_antiTNF | baseline_response_sensitivity | CD14_monocyte\|all_anti_tnf_drug_adjusted\|good_responder_vs_none | lysosomal_apc | -0.2317 | 0.121 | 0.8091 | 0.3573 | blood/sorted-compartment sensitivity; not primary tissue replication |
| GSE138746_RA_sorted_blood_antiTNF | baseline_response_sensitivity | CD4_T_cell\|adalimumab\|eular_responder_moderate_or_good_vs_none | lysosomal_apc | 0.2475 | 0.1343 | 0.8091 | 0.6404 | blood/sorted-compartment sensitivity; not primary tissue replication |
| GSE138746_RA_sorted_blood_antiTNF | baseline_response_sensitivity | CD4_T_cell\|adalimumab\|good_responder_vs_none | lysosomal_apc | 0.2694 | 0.1837 | 0.8091 | 0.6515 | blood/sorted-compartment sensitivity; not primary tissue replication |
| GSE138746_RA_sorted_blood_antiTNF | baseline_response_sensitivity | PBMC\|all_anti_tnf_drug_adjusted\|eular_responder_moderate_or_good_vs_none | lysosomal_apc | -0.2173 | 0.1854 | 0.8091 | 0.4211 | blood/sorted-compartment sensitivity; not primary tissue replication |
| GSE138746_RA_sorted_blood_antiTNF | baseline_response_sensitivity | CD14_monocyte\|etanercept\|eular_responder_moderate_or_good_vs_none | ifn_apc | -0.3234 | 0.1907 | 0.8091 | 0.3862 | blood/sorted-compartment sensitivity; not primary tissue replication |
| GSE138746_RA_sorted_blood_antiTNF | baseline_response_sensitivity | CD4_T_cell\|all_anti_tnf_drug_adjusted\|good_responder_vs_none | ifn_apc | 0.2361 | 0.2089 | 0.8091 | 0.6074 | blood/sorted-compartment sensitivity; not primary tissue replication |
| GSE138746_RA_sorted_blood_antiTNF | baseline_response_sensitivity | PBMC\|etanercept\|good_responder_vs_none | lysosomal_apc | -0.3668 | 0.2098 | 0.8091 | 0.3992 | blood/sorted-compartment sensitivity; not primary tissue replication |
| GSE138746_RA_sorted_blood_antiTNF | baseline_response_sensitivity | CD4_T_cell\|all_anti_tnf_drug_adjusted\|eular_responder_moderate_or_good_vs_none | ifn_apc | 0.1874 | 0.2215 | 0.8207 | 0.5827 | blood/sorted-compartment sensitivity; not primary tissue replication |
| GSE138746_RA_sorted_blood_antiTNF | baseline_response_sensitivity | PBMC\|all_anti_tnf_drug_adjusted\|good_responder_vs_none | lysosomal_apc | -0.2116 | 0.2525 | 0.8207 | 0.4181 | blood/sorted-compartment sensitivity; not primary tissue replication |
| GSE138746_RA_sorted_blood_antiTNF | baseline_response_sensitivity | PBMC\|etanercept\|eular_responder_moderate_or_good_vs_none | ifn_apc | -0.2585 | 0.2613 | 0.8207 | 0.4142 | blood/sorted-compartment sensitivity; not primary tissue replication |
| GSE138746_RA_sorted_blood_antiTNF | baseline_response_sensitivity | CD14_monocyte\|adalimumab\|good_responder_vs_none | lysosomal_apc | -0.2238 | 0.3007 | 0.8546 | 0.3737 | blood/sorted-compartment sensitivity; not primary tissue replication |
| GSE138746_RA_sorted_blood_antiTNF | baseline_response_sensitivity | PBMC\|etanercept\|good_responder_vs_none | ifn_apc | -0.2526 | 0.3362 | 0.8552 | 0.4269 | blood/sorted-compartment sensitivity; not primary tissue replication |
| GSE138746_RA_sorted_blood_antiTNF | baseline_response_sensitivity | PBMC\|adalimumab\|eular_responder_moderate_or_good_vs_none | lysosomal_apc | -0.2294 | 0.339 | 0.8552 | 0.3918 | blood/sorted-compartment sensitivity; not primary tissue replication |
| GSE138746_RA_sorted_blood_antiTNF | baseline_response_sensitivity | CD14_monocyte\|etanercept\|good_responder_vs_none | lysosomal_apc | -0.21 | 0.356 | 0.8552 | 0.3816 | blood/sorted-compartment sensitivity; not primary tissue replication |
| GSE183047_psoriasis_secukinumab | pharmacodynamic_sensitivity_no_response_labels | myeloid_apc_like\|earliest_post_secukinumab_minus_pretreatment\|mean_score | lysosomal_apc | -0.2083 | 0.01984 | 0.7427 |  | pharmacodynamic only; no responder labels in local GEO metadata |
| GSE183047_psoriasis_secukinumab | pharmacodynamic_sensitivity_no_response_labels | myeloid_apc_like\|earliest_post_secukinumab_minus_pretreatment\|high_fraction | lysosomal_apc | -0.1128 | 0.08978 | 0.9747 |  | pharmacodynamic only; no responder labels in local GEO metadata |
| GSE183047_psoriasis_secukinumab | pharmacodynamic_sensitivity_no_response_labels | myeloid_apc_like\|earliest_post_secukinumab_minus_pretreatment\|mean_score | ifn_apc | -0.2033 | 0.2437 | 0.9747 |  | pharmacodynamic only; no responder labels in local GEO metadata |
| GSE183047_psoriasis_secukinumab | pharmacodynamic_sensitivity_no_response_labels | t_cell_like\|earliest_post_secukinumab_minus_pretreatment\|high_fraction | ifn_apc | -0.07101 | 0.2444 | 0.9747 |  | pharmacodynamic only; no responder labels in local GEO metadata |
| GSE183047_psoriasis_secukinumab | pharmacodynamic_sensitivity_no_response_labels | t_cell_like\|earliest_post_secukinumab_minus_pretreatment\|mean_score | ifn_apc | -0.08268 | 0.3217 | 1 |  | pharmacodynamic only; no responder labels in local GEO metadata |
| GSE183047_psoriasis_secukinumab | pharmacodynamic_sensitivity_no_response_labels | keratinocyte_like\|earliest_post_secukinumab_minus_pretreatment\|high_fraction | lysosomal_apc | 0.05846 | 0.3532 | 1 |  | pharmacodynamic only; no responder labels in local GEO metadata |
| GSE183047_psoriasis_secukinumab | pharmacodynamic_sensitivity_no_response_labels | keratinocyte_like\|earliest_post_secukinumab_minus_pretreatment\|mean_score | lysosomal_apc | 0.03649 | 0.4955 | 1 |  | pharmacodynamic only; no responder labels in local GEO metadata |
| GSE183047_psoriasis_secukinumab | pharmacodynamic_sensitivity_no_response_labels | keratinocyte_like\|earliest_post_secukinumab_minus_pretreatment\|mean_score | ifn_apc | -0.04821 | 0.6381 | 1 |  | pharmacodynamic only; no responder labels in local GEO metadata |
| GSE183047_psoriasis_secukinumab | pharmacodynamic_sensitivity_no_response_labels | myeloid_apc_like\|earliest_post_secukinumab_minus_pretreatment\|high_fraction | ifn_apc | -0.01528 | 0.6963 | 1 |  | pharmacodynamic only; no responder labels in local GEO metadata |
| GSE183047_psoriasis_secukinumab | pharmacodynamic_sensitivity_no_response_labels | keratinocyte_like\|earliest_post_secukinumab_minus_pretreatment\|high_fraction | ifn_apc | 0.01164 | 0.9076 | 1 |  | pharmacodynamic only; no responder labels in local GEO metadata |

## Guardrails

- This is not causal target evidence.
- Leave-one-out AUC estimates are high-variance at these sample sizes.
- The primary module was frozen from Wave76 before this prediction audit.
- UC tofacitinib and psoriasis secukinumab rows are stress tests, not
  anti-TNF replication.
- A positive added-AUC result would support only biomarker enrichment, not
  a new intervention point.
