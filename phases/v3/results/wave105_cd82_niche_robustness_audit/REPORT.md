# Wave105 CD82 Niche Robustness Audit

## Bottom Line

Branch call: `REOPEN_CD82_ROBUST_NICHE_SIGNAL`.

This audit stress-tests the Wave104 CD82 matched-niche signal with a fixed
covariate model grid, empirical permutation p-values (`2000` permutations),
and leave-one-donor-out sign stability. Direct CD82 therapeutic promotion is
already blocked by sidecar prior art; the only question here is whether CD82
remains useful as a tissue-niche mechanism/biomarker branch.

## Robustness Summary

| source_analysis | target_analysis | disease_name | target_module | robust_positive | robust_negative | m3_slope | m3_p | m3_perm_p | m3_loo_positive_fraction | m4_slope | m4_p | model_signs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ibd_crohn_epithelial | ibd_crohn_myeloid | Crohn disease | lysosomal_apc | True | False | 1.211 | 0.00349 | 0.001999 | 1 |  |  | M0_raw:+;M1_case:+;M2_target_inflammation:+;M3_source_target_inflammation:+;M5_adaptive_wave104_like:+;M6_target_context_excluding_outcome:+ |
| ibd_crohn_epithelial | ibd_crohn_myeloid | Crohn disease | lipid_loader_repair | True | False | 0.6412 | 0.02362 | 0.01599 | 1 |  |  | M0_raw:+;M1_case:+;M2_target_inflammation:+;M3_source_target_inflammation:+;M5_adaptive_wave104_like:+;M6_target_context_excluding_outcome:+ |
| sjogren_gland_epithelial | sjogren_gland_apc | Sjogren syndrome | lysosomal_apc | True | False | 0.4259 | 0.03835 | 0.04548 | 1 | 0.5669 | 0.004331 | M0_raw:+;M1_case:+;M2_target_inflammation:+;M3_source_target_inflammation:+;M4_ifn_hla_extension:+;M5_adaptive_wave104_like:+;M6_target_context_excluding_outcome:+ |
| ibd_crohn_epithelial | ibd_crohn_myeloid | Crohn disease | complement_phagocytosis | True | False | 1.055 | 0.04268 | 0.04298 | 1 |  |  | M0_raw:+;M1_case:+;M2_target_inflammation:+;M3_source_target_inflammation:+;M5_adaptive_wave104_like:-;M6_target_context_excluding_outcome:- |
| sjogren_gland_epithelial | sjogren_gland_apc | Sjogren syndrome | complement_phagocytosis | False | False | 0.621 | 0.0613 | 0.05647 | 1 | 0.869 | 0.01852 | M0_raw:+;M1_case:+;M2_target_inflammation:+;M3_source_target_inflammation:+;M4_ifn_hla_extension:+;M5_adaptive_wave104_like:+;M6_target_context_excluding_outcome:+ |
| ibd_uc_epithelial | ibd_uc_myeloid | ulcerative colitis | lipid_loader_repair | False | False | 0.1518 | 0.2554 | 0.2729 | 1 |  |  | M0_raw:+;M1_case:+;M2_target_inflammation:+;M3_source_target_inflammation:+;M5_adaptive_wave104_like:+;M6_target_context_excluding_outcome:+ |
| sjogren_gland_epithelial | sjogren_gland_apc | Sjogren syndrome | lipid_loader_repair | False | False | 0.2281 | 0.3882 | 0.4288 | 1 | 0.3373 | 0.2601 | M0_raw:+;M1_case:+;M2_target_inflammation:+;M3_source_target_inflammation:+;M4_ifn_hla_extension:+;M5_adaptive_wave104_like:-;M6_target_context_excluding_outcome:- |
| ibd_uc_epithelial | ibd_uc_myeloid | ulcerative colitis | complement_phagocytosis | False | False | -0.1121 | 0.5923 | 0.5757 | 0.08333 |  |  | M0_raw:-;M1_case:-;M2_target_inflammation:+;M3_source_target_inflammation:-;M5_adaptive_wave104_like:+;M6_target_context_excluding_outcome:+ |
| ibd_uc_epithelial | ibd_uc_myeloid | ulcerative colitis | lysosomal_apc | False | False | 0.01063 | 0.9604 | 0.9615 | 0.5833 |  |  | M0_raw:+;M1_case:+;M2_target_inflammation:+;M3_source_target_inflammation:+;M5_adaptive_wave104_like:+;M6_target_context_excluding_outcome:+ |
| ibd_crohn_stromal | ibd_crohn_myeloid | Crohn disease | complement_phagocytosis | False | False |  |  |  |  |  |  | M0_raw:-;M1_case:-;M2_target_inflammation:-;M5_adaptive_wave104_like:-;M6_target_context_excluding_outcome:- |
| ibd_crohn_stromal | ibd_crohn_myeloid | Crohn disease | lipid_loader_repair | False | False |  |  |  |  |  |  | M0_raw:+;M1_case:+;M2_target_inflammation:-;M5_adaptive_wave104_like:-;M6_target_context_excluding_outcome:- |
| ibd_crohn_stromal | ibd_crohn_myeloid | Crohn disease | lysosomal_apc | False | False |  |  |  |  |  |  | M0_raw:+;M1_case:-;M2_target_inflammation:-;M5_adaptive_wave104_like:+;M6_target_context_excluding_outcome:+ |
| ibd_uc_stromal | ibd_uc_myeloid | ulcerative colitis | complement_phagocytosis | False | False |  |  |  |  |  |  | M0_raw:-;M1_case:-;M2_target_inflammation:+;M5_adaptive_wave104_like:+;M6_target_context_excluding_outcome:+ |
| ibd_uc_stromal | ibd_uc_myeloid | ulcerative colitis | lipid_loader_repair | False | False |  |  |  |  |  |  | M0_raw:+;M1_case:-;M2_target_inflammation:+;M5_adaptive_wave104_like:-;M6_target_context_excluding_outcome:- |
| ibd_uc_stromal | ibd_uc_myeloid | ulcerative colitis | lysosomal_apc | False | False |  |  |  |  |  |  | M0_raw:+;M1_case:-;M2_target_inflammation:-;M5_adaptive_wave104_like:+;M6_target_context_excluding_outcome:+ |
| psoriasis_keratinocyte | psoriasis_skin_apc | psoriasis | complement_phagocytosis | False | False |  |  |  |  |  |  | M0_raw:+;M1_case:+;M5_adaptive_wave104_like:+;M6_target_context_excluding_outcome:+ |
| psoriasis_keratinocyte | psoriasis_skin_apc | psoriasis | lipid_loader_repair | False | False |  |  |  |  |  |  | M0_raw:-;M1_case:-;M5_adaptive_wave104_like:+;M6_target_context_excluding_outcome:+ |
| psoriasis_keratinocyte | psoriasis_skin_apc | psoriasis | lysosomal_apc | False | False |  |  |  |  |  |  | M0_raw:+;M1_case:-;M5_adaptive_wave104_like:+;M6_target_context_excluding_outcome:+ |
| psoriasis_skin_stromal | psoriasis_skin_apc | psoriasis | complement_phagocytosis | False | False |  |  |  |  |  |  | M0_raw:-;M1_case:-;M5_adaptive_wave104_like:-;M6_target_context_excluding_outcome:- |
| psoriasis_skin_stromal | psoriasis_skin_apc | psoriasis | lipid_loader_repair | False | False |  |  |  |  |  |  | M0_raw:-;M1_case:-;M5_adaptive_wave104_like:-;M6_target_context_excluding_outcome:- |
| psoriasis_skin_stromal | psoriasis_skin_apc | psoriasis | lysosomal_apc | False | False |  |  |  |  |  |  | M0_raw:-;M1_case:-;M5_adaptive_wave104_like:-;M6_target_context_excluding_outcome:- |
| sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | complement_phagocytosis | False | False |  |  |  |  |  |  | M0_raw:+;M1_case:+;M2_target_inflammation:+;M5_adaptive_wave104_like:+;M6_target_context_excluding_outcome:+ |
| sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | lipid_loader_repair | False | False |  |  |  |  |  |  | M0_raw:+;M1_case:+;M2_target_inflammation:-;M5_adaptive_wave104_like:-;M6_target_context_excluding_outcome:- |
| sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | lysosomal_apc | False | False |  |  |  |  |  |  | M0_raw:+;M1_case:+;M2_target_inflammation:+;M5_adaptive_wave104_like:+;M6_target_context_excluding_outcome:+ |

## Robust Or Direction-Conflict Tests

| source_analysis | target_analysis | disease_name | target_module | robust_positive | robust_negative | m3_slope | m3_p | m3_perm_p | m3_loo_positive_fraction | m4_slope | m4_p | model_signs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ibd_crohn_epithelial | ibd_crohn_myeloid | Crohn disease | lysosomal_apc | True | False | 1.211 | 0.00349 | 0.001999 | 1 |  |  | M0_raw:+;M1_case:+;M2_target_inflammation:+;M3_source_target_inflammation:+;M5_adaptive_wave104_like:+;M6_target_context_excluding_outcome:+ |
| ibd_crohn_epithelial | ibd_crohn_myeloid | Crohn disease | lipid_loader_repair | True | False | 0.6412 | 0.02362 | 0.01599 | 1 |  |  | M0_raw:+;M1_case:+;M2_target_inflammation:+;M3_source_target_inflammation:+;M5_adaptive_wave104_like:+;M6_target_context_excluding_outcome:+ |
| sjogren_gland_epithelial | sjogren_gland_apc | Sjogren syndrome | lysosomal_apc | True | False | 0.4259 | 0.03835 | 0.04548 | 1 | 0.5669 | 0.004331 | M0_raw:+;M1_case:+;M2_target_inflammation:+;M3_source_target_inflammation:+;M4_ifn_hla_extension:+;M5_adaptive_wave104_like:+;M6_target_context_excluding_outcome:+ |
| ibd_crohn_epithelial | ibd_crohn_myeloid | Crohn disease | complement_phagocytosis | True | False | 1.055 | 0.04268 | 0.04298 | 1 |  |  | M0_raw:+;M1_case:+;M2_target_inflammation:+;M3_source_target_inflammation:+;M5_adaptive_wave104_like:-;M6_target_context_excluding_outcome:- |

## Model Grid

| source_analysis | target_analysis | disease_name | target_module | model | covariate_mode | covariate_count | n | slope | p | perm_p | loo_positive_fraction | covariates |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | lysosomal_apc | M1_case | fixed | 1 | 22 | 0.9096 | 0.002696 | 0.001499 | 1 | case_indicator |
| sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | lysosomal_apc | M5_adaptive_wave104_like | full_missingness_limited | 6 | 22 | 0.4997 | 0.003355 | 0.002499 | 1 | case_indicator;target_inflammatory_nfkb;target_hif_nampt_metabolic;target_ifn_apc;target_hla_ii_apc;target_lipid_loader_repair |
| sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | lysosomal_apc | M6_target_context_excluding_outcome | full_missingness_limited | 6 | 22 | 0.4997 | 0.003355 | 0.002499 | 1 | case_indicator;target_inflammatory_nfkb;target_hif_nampt_metabolic;target_ifn_apc;target_hla_ii_apc;target_lipid_loader_repair |
| ibd_crohn_epithelial | ibd_crohn_myeloid | Crohn disease | lysosomal_apc | M3_source_target_inflammation | fixed | 5 | 12 | 1.211 | 0.00349 | 0.001999 | 1 | case_indicator;target_inflammatory_nfkb;target_hif_nampt_metabolic;source_inflammatory_nfkb;source_hif_nampt_metabolic |
| ibd_uc_epithelial | ibd_uc_myeloid | ulcerative colitis | lipid_loader_repair | M5_adaptive_wave104_like | adaptive_top_8_of_12 | 8 | 12 | 0.2964 | 0.004002 | 0.002999 | 0.9167 | case_indicator;target_inflammatory_nfkb;target_hif_nampt_metabolic;source_inflammatory_nfkb;source_hif_nampt_metabolic;target_ifn_apc;source_ifn_apc;target_hla_ii_apc |
| ibd_uc_epithelial | ibd_uc_myeloid | ulcerative colitis | lipid_loader_repair | M6_target_context_excluding_outcome | adaptive_top_8_of_12 | 8 | 12 | 0.2964 | 0.004002 | 0.003998 | 0.9167 | case_indicator;target_inflammatory_nfkb;target_hif_nampt_metabolic;source_inflammatory_nfkb;source_hif_nampt_metabolic;target_ifn_apc;source_ifn_apc;target_hla_ii_apc |
| sjogren_gland_epithelial | sjogren_gland_apc | Sjogren syndrome | lysosomal_apc | M4_ifn_hla_extension | fixed | 9 | 22 | 0.5669 | 0.004331 | 0.003998 | 1 | case_indicator;target_inflammatory_nfkb;target_hif_nampt_metabolic;source_inflammatory_nfkb;source_hif_nampt_metabolic;target_ifn_apc;source_ifn_apc;target_hla_ii_apc;source_hla_ii_apc |
| sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | lysosomal_apc | M0_raw | none | 0 | 22 | 0.8413 | 0.00637 | 0.007996 | 1 |  |
| ibd_crohn_epithelial | ibd_crohn_myeloid | Crohn disease | lysosomal_apc | M5_adaptive_wave104_like | adaptive_top_8_of_12 | 8 | 12 | 1.063 | 0.01118 | 0.007996 | 0.9167 | case_indicator;target_inflammatory_nfkb;target_hif_nampt_metabolic;source_inflammatory_nfkb;source_hif_nampt_metabolic;target_ifn_apc;source_ifn_apc;target_hla_ii_apc |
| ibd_crohn_epithelial | ibd_crohn_myeloid | Crohn disease | lysosomal_apc | M6_target_context_excluding_outcome | adaptive_top_8_of_12 | 8 | 12 | 1.063 | 0.01118 | 0.009995 | 0.9167 | case_indicator;target_inflammatory_nfkb;target_hif_nampt_metabolic;source_inflammatory_nfkb;source_hif_nampt_metabolic;target_ifn_apc;source_ifn_apc;target_hla_ii_apc |
| ibd_crohn_epithelial | ibd_crohn_myeloid | Crohn disease | lipid_loader_repair | M5_adaptive_wave104_like | adaptive_top_8_of_12 | 8 | 12 | 1.061 | 0.01385 | 0.01099 | 0.9167 | case_indicator;target_inflammatory_nfkb;target_hif_nampt_metabolic;source_inflammatory_nfkb;source_hif_nampt_metabolic;target_ifn_apc;source_ifn_apc;target_hla_ii_apc |
| ibd_crohn_epithelial | ibd_crohn_myeloid | Crohn disease | lipid_loader_repair | M6_target_context_excluding_outcome | adaptive_top_8_of_12 | 8 | 12 | 1.061 | 0.01385 | 0.01099 | 0.9167 | case_indicator;target_inflammatory_nfkb;target_hif_nampt_metabolic;source_inflammatory_nfkb;source_hif_nampt_metabolic;target_ifn_apc;source_ifn_apc;target_hla_ii_apc |
| sjogren_gland_epithelial | sjogren_gland_apc | Sjogren syndrome | complement_phagocytosis | M4_ifn_hla_extension | fixed | 9 | 22 | 0.869 | 0.01852 | 0.01549 | 1 | case_indicator;target_inflammatory_nfkb;target_hif_nampt_metabolic;source_inflammatory_nfkb;source_hif_nampt_metabolic;target_ifn_apc;source_ifn_apc;target_hla_ii_apc;source_hla_ii_apc |
| ibd_crohn_epithelial | ibd_crohn_myeloid | Crohn disease | lipid_loader_repair | M3_source_target_inflammation | fixed | 5 | 12 | 0.6412 | 0.02362 | 0.01599 | 1 | case_indicator;target_inflammatory_nfkb;target_hif_nampt_metabolic;source_inflammatory_nfkb;source_hif_nampt_metabolic |
| ibd_crohn_epithelial | ibd_crohn_myeloid | Crohn disease | lipid_loader_repair | M2_target_inflammation | fixed | 3 | 12 | 0.6152 | 0.03261 | 0.03148 | 1 | case_indicator;target_inflammatory_nfkb;target_hif_nampt_metabolic |
| ibd_crohn_epithelial | ibd_crohn_myeloid | Crohn disease | lipid_loader_repair | M0_raw | none | 0 | 12 | 0.5875 | 0.03682 | 0.04048 | 1 |  |
| sjogren_gland_epithelial | sjogren_gland_apc | Sjogren syndrome | lysosomal_apc | M3_source_target_inflammation | fixed | 5 | 22 | 0.4259 | 0.03835 | 0.04548 | 1 | case_indicator;target_inflammatory_nfkb;target_hif_nampt_metabolic;source_inflammatory_nfkb;source_hif_nampt_metabolic |
| ibd_crohn_epithelial | ibd_crohn_myeloid | Crohn disease | complement_phagocytosis | M3_source_target_inflammation | fixed | 5 | 12 | 1.055 | 0.04268 | 0.04298 | 1 | case_indicator;target_inflammatory_nfkb;target_hif_nampt_metabolic;source_inflammatory_nfkb;source_hif_nampt_metabolic |
| ibd_uc_epithelial | ibd_uc_myeloid | ulcerative colitis | lysosomal_apc | M6_target_context_excluding_outcome | adaptive_top_8_of_12 | 8 | 12 | 0.04275 | 0.04623 | 0.03798 | 0.1667 | case_indicator;target_inflammatory_nfkb;target_hif_nampt_metabolic;source_inflammatory_nfkb;source_hif_nampt_metabolic;target_ifn_apc;source_ifn_apc;target_hla_ii_apc |
| ibd_uc_epithelial | ibd_uc_myeloid | ulcerative colitis | lysosomal_apc | M5_adaptive_wave104_like | adaptive_top_8_of_12 | 8 | 12 | 0.04275 | 0.04623 | 0.04198 | 0.1667 | case_indicator;target_inflammatory_nfkb;target_hif_nampt_metabolic;source_inflammatory_nfkb;source_hif_nampt_metabolic;target_ifn_apc;source_ifn_apc;target_hla_ii_apc |
| ibd_crohn_stromal | ibd_crohn_myeloid | Crohn disease | complement_phagocytosis | M0_raw | none | 0 | 12 | -0.3233 | 0.0244 | 0.01199 | 0 |  |
| ibd_uc_stromal | ibd_uc_myeloid | ulcerative colitis | complement_phagocytosis | M5_adaptive_wave104_like | full_missingness_limited | 7 | 12 | 0.06717 | 0.0472 | 0.05097 | 1 | case_indicator;target_inflammatory_nfkb;target_hif_nampt_metabolic;target_ifn_apc;target_hla_ii_apc;target_lipid_loader_repair;target_lysosomal_apc |
| ibd_uc_stromal | ibd_uc_myeloid | ulcerative colitis | complement_phagocytosis | M6_target_context_excluding_outcome | full_missingness_limited | 7 | 12 | 0.06717 | 0.0472 | 0.05397 | 1 | case_indicator;target_inflammatory_nfkb;target_hif_nampt_metabolic;target_ifn_apc;target_hla_ii_apc;target_lipid_loader_repair;target_lysosomal_apc |
| ibd_crohn_epithelial | ibd_crohn_myeloid | Crohn disease | lysosomal_apc | M0_raw | none | 0 | 12 | 0.7399 | 0.05183 | 0.04648 | 1 |  |
| sjogren_gland_epithelial | sjogren_gland_apc | Sjogren syndrome | complement_phagocytosis | M0_raw | none | 0 | 22 | 0.3182 | 0.05829 | 0.05947 | 1 |  |
| sjogren_gland_epithelial | sjogren_gland_apc | Sjogren syndrome | complement_phagocytosis | M3_source_target_inflammation | fixed | 5 | 22 | 0.621 | 0.0613 | 0.05647 | 1 | case_indicator;target_inflammatory_nfkb;target_hif_nampt_metabolic;source_inflammatory_nfkb;source_hif_nampt_metabolic |
| ibd_crohn_stromal | ibd_crohn_myeloid | Crohn disease | complement_phagocytosis | M1_case | fixed | 1 | 12 | -0.3016 | 0.06314 | 0.06447 | 0 | case_indicator |
| sjogren_gland_epithelial | sjogren_gland_apc | Sjogren syndrome | complement_phagocytosis | M1_case | fixed | 1 | 22 | 0.3009 | 0.06472 | 0.06147 | 1 | case_indicator |
| ibd_crohn_epithelial | ibd_crohn_myeloid | Crohn disease | lipid_loader_repair | M1_case | fixed | 1 | 12 | 0.5862 | 0.07126 | 0.07896 | 1 | case_indicator |
| psoriasis_skin_stromal | psoriasis_skin_apc | psoriasis | lipid_loader_repair | M0_raw | none | 0 | 6 | -1.034 | 0.0864 | 0.07846 |  |  |
| psoriasis_skin_stromal | psoriasis_skin_apc | psoriasis | lipid_loader_repair | M1_case | fixed | 1 | 6 | -1.009 | 0.08904 | 0.09195 |  | case_indicator |
| sjogren_gland_epithelial | sjogren_gland_apc | Sjogren syndrome | complement_phagocytosis | M2_target_inflammation | fixed | 3 | 22 | 0.2809 | 0.09416 | 0.09045 | 1 | case_indicator;target_inflammatory_nfkb;target_hif_nampt_metabolic |
| ibd_uc_epithelial | ibd_uc_myeloid | ulcerative colitis | lipid_loader_repair | M0_raw | none | 0 | 12 | 0.272 | 0.1045 | 0.1069 | 1 |  |
| ibd_crohn_epithelial | ibd_crohn_myeloid | Crohn disease | complement_phagocytosis | M2_target_inflammation | fixed | 3 | 12 | 0.7879 | 0.1076 | 0.1044 | 1 | case_indicator;target_inflammatory_nfkb;target_hif_nampt_metabolic |
| sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | lipid_loader_repair | M5_adaptive_wave104_like | full_missingness_limited | 6 | 22 | -0.4212 | 0.1132 | 0.1119 | 0 | case_indicator;target_inflammatory_nfkb;target_hif_nampt_metabolic;target_ifn_apc;target_hla_ii_apc;target_lysosomal_apc |
| sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | lipid_loader_repair | M6_target_context_excluding_outcome | full_missingness_limited | 6 | 22 | -0.4212 | 0.1132 | 0.1139 | 0 | case_indicator;target_inflammatory_nfkb;target_hif_nampt_metabolic;target_ifn_apc;target_hla_ii_apc;target_lysosomal_apc |
| psoriasis_skin_stromal | psoriasis_skin_apc | psoriasis | lipid_loader_repair | M5_adaptive_wave104_like | adaptive_top_2_of_6_missingness_limited | 2 | 6 | -1.031 | 0.1153 | 0.1299 |  | case_indicator;target_inflammatory_nfkb |
| psoriasis_skin_stromal | psoriasis_skin_apc | psoriasis | lipid_loader_repair | M6_target_context_excluding_outcome | adaptive_top_2_of_6_missingness_limited | 2 | 6 | -1.031 | 0.1153 | 0.1399 |  | case_indicator;target_inflammatory_nfkb |
| ibd_uc_epithelial | ibd_uc_myeloid | ulcerative colitis | lipid_loader_repair | M2_target_inflammation | fixed | 3 | 12 | 0.2096 | 0.1156 | 0.1219 | 1 | case_indicator;target_inflammatory_nfkb;target_hif_nampt_metabolic |
| ibd_uc_stromal | ibd_uc_myeloid | ulcerative colitis | lysosomal_apc | M0_raw | none | 0 | 12 | 0.1633 | 0.1287 | 0.1354 | 1 |  |
| ibd_uc_epithelial | ibd_uc_myeloid | ulcerative colitis | lysosomal_apc | M0_raw | none | 0 | 12 | 0.3554 | 0.131 | 0.1309 | 1 |  |
| sjogren_gland_epithelial | sjogren_gland_apc | Sjogren syndrome | lysosomal_apc | M5_adaptive_wave104_like | full | 12 | 22 | 0.2135 | 0.1413 | 0.1394 | 0.9545 | case_indicator;target_inflammatory_nfkb;target_hif_nampt_metabolic;source_inflammatory_nfkb;source_hif_nampt_metabolic;target_ifn_apc;source_ifn_apc;target_hla_ii_apc;source_hla_ii_apc;source_lipid_loader_repair;target_lipid_loader_repair;source_lysosomal_apc |
| sjogren_gland_epithelial | sjogren_gland_apc | Sjogren syndrome | lysosomal_apc | M6_target_context_excluding_outcome | full | 12 | 22 | 0.2135 | 0.1413 | 0.1439 | 0.9545 | case_indicator;target_inflammatory_nfkb;target_hif_nampt_metabolic;source_inflammatory_nfkb;source_hif_nampt_metabolic;target_ifn_apc;source_ifn_apc;target_hla_ii_apc;source_hla_ii_apc;source_lipid_loader_repair;target_lipid_loader_repair;source_lysosomal_apc |
| ibd_crohn_stromal | ibd_crohn_myeloid | Crohn disease | lysosomal_apc | M5_adaptive_wave104_like | full_missingness_limited | 6 | 12 | 0.1666 | 0.1437 | 0.1474 | 0.9167 | case_indicator;target_inflammatory_nfkb;target_hif_nampt_metabolic;target_ifn_apc;target_hla_ii_apc;target_lipid_loader_repair |
| ibd_crohn_stromal | ibd_crohn_myeloid | Crohn disease | lysosomal_apc | M6_target_context_excluding_outcome | full_missingness_limited | 6 | 12 | 0.1666 | 0.1437 | 0.1634 | 0.9167 | case_indicator;target_inflammatory_nfkb;target_hif_nampt_metabolic;target_ifn_apc;target_hla_ii_apc;target_lipid_loader_repair |
| sjogren_gland_epithelial | sjogren_gland_apc | Sjogren syndrome | lysosomal_apc | M0_raw | none | 0 | 22 | 0.2333 | 0.1488 | 0.1429 | 1 |  |
| sjogren_gland_epithelial | sjogren_gland_apc | Sjogren syndrome | lipid_loader_repair | M6_target_context_excluding_outcome | full | 12 | 22 | -0.3822 | 0.1529 | 0.1409 | 0.04545 | case_indicator;target_inflammatory_nfkb;target_hif_nampt_metabolic;source_inflammatory_nfkb;source_hif_nampt_metabolic;target_ifn_apc;source_ifn_apc;target_hla_ii_apc;source_hla_ii_apc;source_lipid_loader_repair;source_lysosomal_apc;target_lysosomal_apc |
| sjogren_gland_epithelial | sjogren_gland_apc | Sjogren syndrome | lipid_loader_repair | M5_adaptive_wave104_like | full | 12 | 22 | -0.3822 | 0.1529 | 0.1669 | 0.04545 | case_indicator;target_inflammatory_nfkb;target_hif_nampt_metabolic;source_inflammatory_nfkb;source_hif_nampt_metabolic;target_ifn_apc;source_ifn_apc;target_hla_ii_apc;source_hla_ii_apc;source_lipid_loader_repair;source_lysosomal_apc;target_lysosomal_apc |
| ibd_uc_stromal | ibd_uc_myeloid | ulcerative colitis | complement_phagocytosis | M0_raw | none | 0 | 12 | -0.1832 | 0.1543 | 0.1584 | 0 |  |
| ibd_crohn_epithelial | ibd_crohn_myeloid | Crohn disease | lysosomal_apc | M2_target_inflammation | fixed | 3 | 12 | 0.579 | 0.1577 | 0.1554 | 1 | case_indicator;target_inflammatory_nfkb;target_hif_nampt_metabolic |
| sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | lysosomal_apc | M2_target_inflammation | fixed | 3 | 22 | 0.3853 | 0.1614 | 0.1639 | 1 | case_indicator;target_inflammatory_nfkb;target_hif_nampt_metabolic |
| sjogren_gland_epithelial | sjogren_gland_apc | Sjogren syndrome | lysosomal_apc | M1_case | fixed | 1 | 22 | 0.2239 | 0.1627 | 0.1584 | 1 | case_indicator |
| ibd_crohn_epithelial | ibd_crohn_myeloid | Crohn disease | lysosomal_apc | M1_case | fixed | 1 | 12 | 0.5693 | 0.1716 | 0.1624 | 1 | case_indicator |
| ibd_crohn_stromal | ibd_crohn_myeloid | Crohn disease | complement_phagocytosis | M2_target_inflammation | fixed | 3 | 12 | -0.4154 | 0.1723 | 0.1609 | 0 | case_indicator;target_inflammatory_nfkb;target_hif_nampt_metabolic |
| psoriasis_skin_stromal | psoriasis_skin_apc | psoriasis | complement_phagocytosis | M5_adaptive_wave104_like | adaptive_top_2_of_7_missingness_limited | 2 | 6 | -2.829 | 0.1839 | 0.1634 |  | case_indicator;target_inflammatory_nfkb |
| psoriasis_skin_stromal | psoriasis_skin_apc | psoriasis | complement_phagocytosis | M6_target_context_excluding_outcome | adaptive_top_2_of_7_missingness_limited | 2 | 6 | -2.829 | 0.1839 | 0.1649 |  | case_indicator;target_inflammatory_nfkb |
| sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | complement_phagocytosis | M1_case | fixed | 1 | 22 | 0.4529 | 0.1864 | 0.1719 | 0.9545 | case_indicator |
| psoriasis_skin_stromal | psoriasis_skin_apc | psoriasis | lysosomal_apc | M6_target_context_excluding_outcome | adaptive_top_2_of_6_missingness_limited | 2 | 6 | -1.218 | 0.2063 | 0.2214 |  | case_indicator;target_inflammatory_nfkb |
| psoriasis_skin_stromal | psoriasis_skin_apc | psoriasis | lysosomal_apc | M5_adaptive_wave104_like | adaptive_top_2_of_6_missingness_limited | 2 | 6 | -1.218 | 0.2063 | 0.2224 |  | case_indicator;target_inflammatory_nfkb |
| psoriasis_skin_stromal | psoriasis_skin_apc | psoriasis | lysosomal_apc | M1_case | fixed | 1 | 6 | -1.038 | 0.2266 | 0.2104 |  | case_indicator |
| ibd_uc_epithelial | ibd_uc_myeloid | ulcerative colitis | lipid_loader_repair | M3_source_target_inflammation | fixed | 5 | 12 | 0.1518 | 0.2554 | 0.2729 | 1 | case_indicator;target_inflammatory_nfkb;target_hif_nampt_metabolic;source_inflammatory_nfkb;source_hif_nampt_metabolic |
| sjogren_gland_epithelial | sjogren_gland_apc | Sjogren syndrome | lipid_loader_repair | M4_ifn_hla_extension | fixed | 9 | 22 | 0.3373 | 0.2601 | 0.2729 | 1 | case_indicator;target_inflammatory_nfkb;target_hif_nampt_metabolic;source_inflammatory_nfkb;source_hif_nampt_metabolic;target_ifn_apc;source_ifn_apc;target_hla_ii_apc;source_hla_ii_apc |
| ibd_crohn_stromal | ibd_crohn_myeloid | Crohn disease | complement_phagocytosis | M5_adaptive_wave104_like | full_missingness_limited | 7 | 12 | -0.1336 | 0.2658 | 0.2599 | 0.1667 | case_indicator;target_inflammatory_nfkb;target_hif_nampt_metabolic;target_ifn_apc;target_hla_ii_apc;target_lipid_loader_repair;target_lysosomal_apc |
| ibd_crohn_stromal | ibd_crohn_myeloid | Crohn disease | complement_phagocytosis | M6_target_context_excluding_outcome | full_missingness_limited | 7 | 12 | -0.1336 | 0.2658 | 0.2834 | 0.1667 | case_indicator;target_inflammatory_nfkb;target_hif_nampt_metabolic;target_ifn_apc;target_hla_ii_apc;target_lipid_loader_repair;target_lysosomal_apc |
| ibd_uc_epithelial | ibd_uc_myeloid | ulcerative colitis | lipid_loader_repair | M1_case | fixed | 1 | 12 | 0.1875 | 0.2912 | 0.3293 | 1 | case_indicator |
| sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | complement_phagocytosis | M0_raw | none | 0 | 22 | 0.3661 | 0.3008 | 0.2904 | 0.9545 |  |
| ibd_crohn_stromal | ibd_crohn_myeloid | Crohn disease | lipid_loader_repair | M0_raw | none | 0 | 12 | 0.07493 | 0.3067 | 0.3238 | 1 |  |
| psoriasis_skin_stromal | psoriasis_skin_apc | psoriasis | complement_phagocytosis | M1_case | fixed | 1 | 6 | -1.996 | 0.3106 | 0.3243 |  | case_indicator |
| psoriasis_skin_stromal | psoriasis_skin_apc | psoriasis | complement_phagocytosis | M0_raw | none | 0 | 6 | -1.96 | 0.3158 | 0.3258 |  |  |
| ibd_uc_stromal | ibd_uc_myeloid | ulcerative colitis | lysosomal_apc | M5_adaptive_wave104_like | full_missingness_limited | 6 | 12 | 0.02671 | 0.3243 | 0.3058 | 0.9167 | case_indicator;target_inflammatory_nfkb;target_hif_nampt_metabolic;target_ifn_apc;target_hla_ii_apc;target_lipid_loader_repair |
| ibd_uc_stromal | ibd_uc_myeloid | ulcerative colitis | lysosomal_apc | M6_target_context_excluding_outcome | full_missingness_limited | 6 | 12 | 0.02671 | 0.3243 | 0.3408 | 0.9167 | case_indicator;target_inflammatory_nfkb;target_hif_nampt_metabolic;target_ifn_apc;target_hla_ii_apc;target_lipid_loader_repair |
| ibd_uc_epithelial | ibd_uc_myeloid | ulcerative colitis | complement_phagocytosis | M0_raw | none | 0 | 12 | -0.2716 | 0.3489 | 0.4113 | 0 |  |
| sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | lipid_loader_repair | M1_case | fixed | 1 | 22 | 0.2516 | 0.3529 | 0.3473 | 0.9545 | case_indicator |
| sjogren_gland_epithelial | sjogren_gland_apc | Sjogren syndrome | lipid_loader_repair | M0_raw | none | 0 | 22 | 0.13 | 0.3588 | 0.3798 | 1 |  |
| ibd_crohn_epithelial | ibd_crohn_myeloid | Crohn disease | complement_phagocytosis | M1_case | fixed | 1 | 12 | 0.652 | 0.3699 | 0.3618 | 1 | case_indicator |
| psoriasis_skin_stromal | psoriasis_skin_apc | psoriasis | lysosomal_apc | M0_raw | none | 0 | 6 | -0.8926 | 0.3775 | 0.3733 |  |  |
| sjogren_gland_epithelial | sjogren_gland_apc | Sjogren syndrome | lipid_loader_repair | M3_source_target_inflammation | fixed | 5 | 22 | 0.2281 | 0.3882 | 0.4288 | 1 | case_indicator;target_inflammatory_nfkb;target_hif_nampt_metabolic;source_inflammatory_nfkb;source_hif_nampt_metabolic |
| ibd_uc_stromal | ibd_uc_myeloid | ulcerative colitis | complement_phagocytosis | M2_target_inflammation | fixed | 3 | 12 | 0.1173 | 0.4012 | 0.3973 | 1 | case_indicator;target_inflammatory_nfkb;target_hif_nampt_metabolic |
| ibd_crohn_stromal | ibd_crohn_myeloid | Crohn disease | lipid_loader_repair | M2_target_inflammation | fixed | 3 | 12 | -0.1604 | 0.4077 | 0.4313 | 0 | case_indicator;target_inflammatory_nfkb;target_hif_nampt_metabolic |
| sjogren_gland_epithelial | sjogren_gland_apc | Sjogren syndrome | lipid_loader_repair | M1_case | fixed | 1 | 22 | 0.1078 | 0.4131 | 0.4298 | 1 | case_indicator |

## Decision Rule

`REOPEN_CD82_ROBUST_NICHE_SIGNAL` requires robust positive CD82 niche coupling
in at least two diseases with no robust negative disease. A robust positive
requires positive signs through M0-M3, M3 nominal p < 0.05, M3 permutation
p < 0.05, M3 leave-one-out positive fraction >= 0.85, and supportive or
underpowered M4 behavior.

## Interpretation Guardrail

Even a robust matched-niche correlation is not causal. It can reflect shared
tissue severity, therapy, donor composition, or unmeasured batch. Given CD82
prior art in colitis/NLRP3 and RA synovial fibroblasts, a positive result would
support a biomarker/mechanism branch, not a therapeutic target claim.

## Reproducibility

- Script: `scripts/v3_wave105_cd82_niche_robustness_audit.py`
- Input pairs: `results_v3/wave104_accessible_survivor_niche_controller_test/matched_niche_pairs.tsv`
- Model grid: `results_v3/wave105_cd82_niche_robustness_audit/cd82_model_grid_tests.tsv`
- Robustness summary: `results_v3/wave105_cd82_niche_robustness_audit/cd82_robustness_summary.tsv`
- Robust tests: `results_v3/wave105_cd82_niche_robustness_audit/cd82_robust_tests.tsv`
- Seed: `20260527`
- Permutations per model: `2000`
