# Wave85 External GEO Anti-TNF Validation

Decision call: `WEAK_EXTERNAL_DIRECTIONAL_SUPPORT_NOT_STRATIFICATION_GRADE`.

Primary endpoint: baseline `lysosomal_apc__resid_inflammatory_nfkb`; the Wave84-expected direction is higher score in responders.

Important independence guardrail: `GSE14580_UC_Leuven_baseline` and `GSE16879_UC_Leuven_baseline` share GSM accessions and are not counted as independent validation cohorts.

## Primary Cohort Results

| cohort | overlap_group | n_patients | n_responders | n_nonresponders | effect_responder_minus_non | hedges_g_responder_minus_non | auc_high_score_response | p | fdr_all_tests | direction_matches_wave84 | supportive_nominal | supportive_strong |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GSE16879_Crohn_all_Leuven_baseline | Leuven_GSE16879_Crohn_all | 37 | 20 | 17 | -0.105 | -0.2758 | 0.5029 | 0.3909 | 0.6304 | False | False | False |
| GSE16879_Crohn_colitis_Leuven_baseline | Leuven_GSE16879_Crohn_colitis | 19 | 12 | 7 | -0.1441 | -0.3664 | 0.4405 | 0.45 | 0.6702 | False | False | False |
| GSE14580_UC_Leuven_baseline | Leuven_GSE14580_GSE16879_UC_overlap | 24 | 8 | 16 | 0.1335 | 0.3197 | 0.5469 | 0.5236 | 0.7119 | True | False | False |
| GSE16879_UC_Leuven_baseline | Leuven_GSE14580_GSE16879_UC_overlap | 24 | 8 | 16 | 0.1335 | 0.3197 | 0.5469 | 0.5236 | 0.7119 | True | False | False |
| GSE12251_UC_ACT1_baseline | ACT1_GSE12251_UC | 22 | 12 | 10 | -0.0942 | -0.2606 | 0.4667 | 0.5364 | 0.7119 | False | False | False |
| GSE16879_all_IBD_Leuven_baseline | Leuven_GSE16879_all_IBD | 61 | 28 | 33 | -0.0539 | -0.1412 | 0.4957 | 0.5898 | 0.7373 | False | False | False |
| GSE16879_Crohn_ileitis_Leuven_baseline | Leuven_GSE16879_Crohn_ileitis | 18 | 8 | 10 | 0.01388 | 0.03219 | 0.65 | 0.9484 | 0.9621 | True | False | False |

## Primary Meta Summary

| meta_scope | n_cohorts | n_overlap_groups | weighted_mean_hedges_g | positive_direction_cohorts | negative_direction_cohorts | supportive_nominal_cohorts | supportive_strong_cohorts | median_auc | min_auc | max_auc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| all_tested_cohorts | 7 | 6 | -0.07604 | 3 | 4 | 0 | 0 | 0.5029 | 0.4405 | 0.65 |
| independent_overlap_groups_best_abs_effect | 6 | 6 | -0.1285 | 2 | 4 | 0 | 0 | 0.4993 | 0.4405 | 0.65 |

## All Module Tests

| cohort | module | n_patients | effect_responder_minus_non | hedges_g_responder_minus_non | auc_high_score_response | p | fdr_all_tests | direction_matches_wave84 | supportive_nominal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GSE16879_Crohn_colitis_Leuven_baseline | complement_phagocytosis | 19 | -0.3991 | -0.7102 | 0.3095 | 0.2362 | 0.4352 | False | False |
| GSE16879_Crohn_all_Leuven_baseline | complement_phagocytosis | 37 | -0.2238 | -0.387 | 0.3912 | 0.2561 | 0.4596 | False | False |
| GSE12251_UC_ACT1_baseline | complement_phagocytosis | 22 | -0.3253 | -0.4732 | 0.3833 | 0.2677 | 0.4685 | False | False |
| GSE16879_all_IBD_Leuven_baseline | complement_phagocytosis | 61 | -0.1559 | -0.25 | 0.4535 | 0.3148 | 0.5375 | False | False |
| GSE16879_Crohn_ileitis_Leuven_baseline | complement_phagocytosis | 18 | -0.1 | -0.1473 | 0.4375 | 0.7456 | 0.8846 | False | False |
| GSE14580_UC_Leuven_baseline | complement_phagocytosis | 24 | -0.04154 | -0.05655 | 0.5469 | 0.8862 | 0.9299 | False | False |
| GSE16879_UC_Leuven_baseline | complement_phagocytosis | 24 | -0.04154 | -0.05655 | 0.5469 | 0.8862 | 0.9299 | False | False |
| GSE12251_UC_ACT1_baseline | hla_ii_apc | 22 | -0.5767 | -0.7599 | 0.3 | 0.07265 | 0.1956 | False | False |
| GSE16879_Crohn_colitis_Leuven_baseline | hla_ii_apc | 19 | -0.4736 | -0.6376 | 0.3333 | 0.1645 | 0.3291 | False | False |
| GSE16879_all_IBD_Leuven_baseline | hla_ii_apc | 61 | -0.1735 | -0.2437 | 0.4524 | 0.3606 | 0.6011 | False | False |
| GSE14580_UC_Leuven_baseline | hla_ii_apc | 24 | -0.3192 | -0.4262 | 0.3516 | 0.4052 | 0.6304 | False | False |
| GSE16879_UC_Leuven_baseline | hla_ii_apc | 24 | -0.3192 | -0.4262 | 0.3516 | 0.4052 | 0.6304 | False | False |
| GSE16879_Crohn_all_Leuven_baseline | hla_ii_apc | 37 | -0.145 | -0.1936 | 0.4735 | 0.539 | 0.7119 | False | False |
| GSE16879_Crohn_ileitis_Leuven_baseline | hla_ii_apc | 18 | 0.08476 | 0.09453 | 0.6125 | 0.8501 | 0.9298 | True | False |
| GSE12251_UC_ACT1_baseline | ifn_apc | 22 | -0.8355 | -1.041 | 0.225 | 0.01899 | 0.08307 | False | False |
| GSE16879_all_IBD_Leuven_baseline | ifn_apc | 61 | -0.4794 | -0.6111 | 0.342 | 0.02396 | 0.0849 | False | False |
| GSE14580_UC_Leuven_baseline | ifn_apc | 24 | -0.7389 | -0.9594 | 0.2266 | 0.04058 | 0.1136 | False | False |
| GSE16879_UC_Leuven_baseline | ifn_apc | 24 | -0.7389 | -0.9594 | 0.2266 | 0.04058 | 0.1136 | False | False |
| GSE16879_Crohn_colitis_Leuven_baseline | ifn_apc | 19 | -0.6541 | -0.7388 | 0.3095 | 0.09118 | 0.2279 | False | False |
| GSE16879_Crohn_all_Leuven_baseline | ifn_apc | 37 | -0.4163 | -0.5055 | 0.3647 | 0.1154 | 0.2613 | False | False |
| GSE16879_Crohn_ileitis_Leuven_baseline | ifn_apc | 18 | -0.2292 | -0.2559 | 0.4625 | 0.6024 | 0.7398 | False | False |
| GSE12251_UC_ACT1_baseline | ifn_lysosomal_apc_composite | 22 | -0.7879 | -1.404 | 0.1 | 0.002333 | 0.01889 | False | False |
| GSE16879_all_IBD_Leuven_baseline | ifn_lysosomal_apc_composite | 61 | -0.4122 | -0.7182 | 0.316 | 0.008855 | 0.04808 | False | False |
| GSE16879_Crohn_colitis_Leuven_baseline | ifn_lysosomal_apc_composite | 19 | -0.683 | -1.17 | 0.1548 | 0.008928 | 0.04808 | False | False |
| GSE16879_Crohn_all_Leuven_baseline | ifn_lysosomal_apc_composite | 37 | -0.4331 | -0.7276 | 0.3147 | 0.02605 | 0.08684 | False | False |
| GSE14580_UC_Leuven_baseline | ifn_lysosomal_apc_composite | 24 | -0.4438 | -0.7679 | 0.2578 | 0.1232 | 0.2613 | False | False |
| GSE16879_UC_Leuven_baseline | ifn_lysosomal_apc_composite | 24 | -0.4438 | -0.7679 | 0.2578 | 0.1232 | 0.2613 | False | False |
| GSE16879_Crohn_ileitis_Leuven_baseline | ifn_lysosomal_apc_composite | 18 | -0.2224 | -0.3193 | 0.4375 | 0.519 | 0.7119 | False | False |
| GSE16879_Crohn_ileitis_Leuven_baseline | ifn_lysosomal_apc_composite__resid_inflammatory_nfkb | 18 | 0.08649 | 0.1654 | 0.65 | 0.7405 | 0.8846 | True | False |
| GSE14580_UC_Leuven_baseline | ifn_lysosomal_apc_composite__resid_inflammatory_nfkb | 24 | 0.05145 | 0.1357 | 0.4688 | 0.7856 | 0.887 | True | False |
| GSE16879_UC_Leuven_baseline | ifn_lysosomal_apc_composite__resid_inflammatory_nfkb | 24 | 0.05145 | 0.1357 | 0.4688 | 0.7856 | 0.887 | True | False |
| GSE12251_UC_ACT1_baseline | ifn_lysosomal_apc_composite__resid_inflammatory_nfkb | 22 | -0.03628 | -0.08714 | 0.475 | 0.8338 | 0.9264 | False | False |
| GSE16879_Crohn_colitis_Leuven_baseline | ifn_lysosomal_apc_composite__resid_inflammatory_nfkb | 19 | -0.03323 | -0.05898 | 0.5119 | 0.8938 | 0.9299 | False | False |
| GSE16879_all_IBD_Leuven_baseline | ifn_lysosomal_apc_composite__resid_inflammatory_nfkb | 61 | -0.01482 | -0.03223 | 0.5249 | 0.9034 | 0.9299 | False | False |
| GSE16879_Crohn_all_Leuven_baseline | ifn_lysosomal_apc_composite__resid_inflammatory_nfkb | 37 | -0.005637 | -0.01129 | 0.5471 | 0.9714 | 0.9714 | False | False |
| GSE16879_all_IBD_Leuven_baseline | inflammatory_nfkb | 61 | -0.8915 | -1.232 | 0.197 | 5.471e-06 | 0.000383 | False | False |
| GSE16879_Crohn_colitis_Leuven_baseline | inflammatory_nfkb | 19 | -1.432 | -3.446 | 0 | 8.867e-05 | 0.003103 | False | False |
| GSE12251_UC_ACT1_baseline | inflammatory_nfkb | 22 | -1.258 | -1.892 | 0.03333 | 0.000437 | 0.007647 | False | False |
| GSE16879_Crohn_all_Leuven_baseline | inflammatory_nfkb | 37 | -0.9597 | -1.299 | 0.1941 | 0.0006984 | 0.009778 | False | False |
| GSE14580_UC_Leuven_baseline | inflammatory_nfkb | 24 | -0.8889 | -1.177 | 0.1875 | 0.002588 | 0.01889 | False | False |

## Data And Processing

- GSE12251: baseline ulcerative-colitis colonic biopsies before infliximab; response is week-8 endoscopic/histologic healing; PubMed ID from GEO matrix: 19700435.
- GSE14580: baseline active ulcerative-colitis colonic biopsies before first infliximab; response is 4-6 week endoscopic/histologic healing; PubMed ID from GEO matrix: 19700435.
- GSE16879: baseline and post-infliximab IBD mucosal biopsies; this analysis uses baseline UC, Crohn colitis, and Crohn ileitis subsets; PubMed ID from GEO matrix: 19956723.
- GPL570 annotation downloaded from NCBI GEO and restricted to module genes.
- Series matrices are already globally scaled by original submitters; this script log2-transforms values where needed, collapses probes to genes by median, z-scores genes within each tested cohort, computes module means, and aggregates duplicate patient samples before testing.

## Interpretation Guardrail

This is a treatment-response biomarker validation attempt, not a drug-target claim. A positive result would only support patient stratification for anti-TNF response in inflamed intestinal tissue; it would not establish that lysosomal/APC biology causally mediates response.
