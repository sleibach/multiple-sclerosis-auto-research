# Wave106 CD82 Specificity / Confounder Audit

## Bottom Line

Branch call: `CD82_SIGNAL_PARTLY_GENERIC_OR_CONTEXT_LIMITED`.

This test asks whether CD82's matched-niche signal is specific to myeloid
lipid/lysosomal modules or whether it is better explained as generic target
APC/inflammatory activation.

## Context Summary

| source_analysis | target_analysis | disease_name | wave105_robust_context | specificity_call | primary_positive_m3_count | control_positive_m3_count | primary_positive_m7_count | control_positive_m7_count | best_primary_modules_m3 | best_control_modules_m3 | best_primary_modules_m7 | best_control_modules_m7 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ibd_crohn_epithelial | ibd_crohn_myeloid | Crohn disease | True | GENERIC_TARGET_ACTIVATION_COUPLING | 3 | 2 | 0 | 0 | lysosomal_apc;lipid_loader_repair;complement_phagocytosis | ifn_apc;hla_ii_apc |  |  |
| sjogren_gland_epithelial | sjogren_gland_apc | Sjogren syndrome | True | SPECIFIC_PRIMARY_OVER_CONTROLS_M3 | 1 | 0 | 0 | 1 | lysosomal_apc |  |  | ifn_apc |
| sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | False | GENERIC_TARGET_ACTIVATION_COUPLING_M7 | 0 | 1 | 1 | 1 |  | hif_nampt_metabolic | lysosomal_apc | hif_nampt_metabolic |
| ibd_crohn_stromal | ibd_crohn_myeloid | Crohn disease | False | NO_PRIMARY_SIGNAL | 0 | 1 | 0 | 2 |  | inflammatory_nfkb |  | ifn_apc;inflammatory_nfkb |
| ibd_uc_epithelial | ibd_uc_myeloid | ulcerative colitis | False | NO_PRIMARY_SIGNAL | 0 | 0 | 0 | 0 |  |  |  |  |
| ibd_uc_stromal | ibd_uc_myeloid | ulcerative colitis | False | NO_PRIMARY_SIGNAL | 0 | 0 | 0 | 0 |  |  |  |  |
| psoriasis_keratinocyte | psoriasis_skin_apc | psoriasis | False | NO_PRIMARY_SIGNAL | 0 | 0 | 0 | 0 |  |  |  |  |
| psoriasis_skin_stromal | psoriasis_skin_apc | psoriasis | False | NO_PRIMARY_SIGNAL | 0 | 0 | 0 | 0 |  |  |  |  |

## Top Tests

| source_analysis | target_analysis | disease_name | outcome_module | outcome_class | model | covariate_mode | n | slope | p | positive_nominal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ibd_crohn_stromal | ibd_crohn_myeloid | Crohn disease | inflammatory_nfkb | control | M0_raw | none | 12 | 1.329 | 4.29e-06 | True |
| ibd_crohn_stromal | ibd_crohn_myeloid | Crohn disease | hif_nampt_metabolic | control | M0_raw | none | 12 | 0.7251 | 7.773e-05 | True |
| ibd_crohn_epithelial | ibd_crohn_myeloid | Crohn disease | ifn_apc | control | M3_base_inflammation | fixed | 12 | 1.697 | 0.0003109 | True |
| ibd_crohn_epithelial | ibd_crohn_myeloid | Crohn disease | hla_ii_apc | control | M3_base_inflammation | fixed | 12 | 1.7 | 0.0005287 | True |
| ibd_crohn_stromal | ibd_crohn_myeloid | Crohn disease | inflammatory_nfkb | control | M7_broad_nonoutcome_context | fixed | 12 | 0.8312 | 0.00161 | True |
| ibd_crohn_epithelial | ibd_crohn_myeloid | Crohn disease | lysosomal_apc | primary | M3_base_inflammation | fixed | 12 | 1.211 | 0.00349 | True |
| sjogren_gland_epithelial | sjogren_gland_apc | Sjogren syndrome | ifn_apc | control | M7_broad_nonoutcome_context | fixed | 22 | 0.4156 | 0.004329 | True |
| sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | hif_nampt_metabolic | control | M3_base_inflammation | fixed | 22 | 0.7707 | 0.005529 | True |
| sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | hif_nampt_metabolic | control | M0_raw | none | 22 | 0.8158 | 0.006193 | True |
| sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | lysosomal_apc | primary | M0_raw | none | 22 | 0.8413 | 0.00637 | True |
| sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | lysosomal_apc | primary | M7_broad_nonoutcome_context | fixed | 22 | 0.5629 | 0.01213 | True |
| ibd_crohn_stromal | ibd_crohn_myeloid | Crohn disease | ifn_apc | control | M7_broad_nonoutcome_context | fixed | 12 | 0.5279 | 0.01935 | True |
| ibd_crohn_epithelial | ibd_crohn_myeloid | Crohn disease | lipid_loader_repair | primary | M3_base_inflammation | fixed | 12 | 0.6412 | 0.02362 | True |
| ibd_crohn_stromal | ibd_crohn_myeloid | Crohn disease | complement_phagocytosis | primary | M0_raw | none | 12 | -0.3233 | 0.0244 | False |
| sjogren_gland_epithelial | sjogren_gland_apc | Sjogren syndrome | hla_ii_apc | control | M7_broad_nonoutcome_context | fixed | 22 | -0.3019 | 0.02573 | False |
| ibd_crohn_stromal | ibd_crohn_myeloid | Crohn disease | inflammatory_nfkb | control | M3_base_inflammation | fixed | 12 | 0.6902 | 0.02639 | True |
| ibd_crohn_stromal | ibd_crohn_myeloid | Crohn disease | hla_ii_apc | control | M7_broad_nonoutcome_context | fixed | 12 | -0.5139 | 0.03493 | False |
| sjogren_gland_epithelial | sjogren_gland_apc | Sjogren syndrome | hif_nampt_metabolic | control | M7_broad_nonoutcome_context | fixed | 22 | -0.428 | 0.0365 | False |
| ibd_crohn_epithelial | ibd_crohn_myeloid | Crohn disease | lipid_loader_repair | primary | M0_raw | none | 12 | 0.5875 | 0.03682 | True |
| sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | hif_nampt_metabolic | control | M7_broad_nonoutcome_context | fixed | 22 | 0.4171 | 0.03781 | True |
| sjogren_gland_epithelial | sjogren_gland_apc | Sjogren syndrome | lysosomal_apc | primary | M3_base_inflammation | fixed | 22 | 0.4259 | 0.03835 | True |
| ibd_uc_stromal | ibd_uc_myeloid | ulcerative colitis | inflammatory_nfkb | control | M3_base_inflammation | fixed | 12 | -0.2023 | 0.0411 | False |
| ibd_crohn_epithelial | ibd_crohn_myeloid | Crohn disease | complement_phagocytosis | primary | M3_base_inflammation | fixed | 12 | 1.055 | 0.04268 | True |
| sjogren_gland_epithelial | sjogren_gland_apc | Sjogren syndrome | hla_ii_apc | control | M0_raw | none | 22 | -0.1804 | 0.04913 | False |
| ibd_crohn_epithelial | ibd_crohn_myeloid | Crohn disease | lysosomal_apc | primary | M0_raw | none | 12 | 0.7399 | 0.05183 | False |
| ibd_uc_stromal | ibd_uc_myeloid | ulcerative colitis | hif_nampt_metabolic | control | M3_base_inflammation | fixed | 12 | 0.1509 | 0.05752 | False |
| sjogren_gland_epithelial | sjogren_gland_apc | Sjogren syndrome | complement_phagocytosis | primary | M0_raw | none | 22 | 0.3182 | 0.05829 | False |
| sjogren_gland_epithelial | sjogren_gland_apc | Sjogren syndrome | complement_phagocytosis | primary | M3_base_inflammation | fixed | 22 | 0.621 | 0.0613 | False |
| ibd_crohn_epithelial | ibd_crohn_myeloid | Crohn disease | ifn_apc | control | M0_raw | none | 12 | 1.92 | 0.06827 | False |
| sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | ifn_apc | control | M0_raw | none | 22 | 0.3593 | 0.07226 | False |
| sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | complement_phagocytosis | primary | M7_broad_nonoutcome_context | fixed | 22 | 0.6519 | 0.08301 | False |
| psoriasis_skin_stromal | psoriasis_skin_apc | psoriasis | lipid_loader_repair | primary | M0_raw | none | 6 | -1.034 | 0.0864 | False |
| ibd_uc_epithelial | ibd_uc_myeloid | ulcerative colitis | ifn_apc | control | M0_raw | none | 12 | 0.6452 | 0.1004 | False |
| ibd_uc_stromal | ibd_uc_myeloid | ulcerative colitis | hif_nampt_metabolic | control | M0_raw | none | 12 | 0.4439 | 0.1007 | False |
| ibd_crohn_stromal | ibd_crohn_myeloid | Crohn disease | hla_ii_apc | control | M0_raw | none | 12 | -0.2841 | 0.1029 | False |
| ibd_uc_epithelial | ibd_uc_myeloid | ulcerative colitis | lipid_loader_repair | primary | M0_raw | none | 12 | 0.272 | 0.1045 | False |
| sjogren_gland_epithelial | sjogren_gland_apc | Sjogren syndrome | ifn_apc | control | M3_base_inflammation | fixed | 22 | 0.2606 | 0.1146 | False |
| ibd_uc_stromal | ibd_uc_myeloid | ulcerative colitis | complement_phagocytosis | primary | M7_broad_nonoutcome_context | fixed | 12 | 0.09698 | 0.1155 | False |
| ibd_uc_stromal | ibd_uc_myeloid | ulcerative colitis | lysosomal_apc | primary | M0_raw | none | 12 | 0.1633 | 0.1287 | False |
| ibd_uc_epithelial | ibd_uc_myeloid | ulcerative colitis | lysosomal_apc | primary | M0_raw | none | 12 | 0.3554 | 0.131 | False |
| ibd_crohn_stromal | ibd_crohn_myeloid | Crohn disease | lysosomal_apc | primary | M7_broad_nonoutcome_context | fixed | 12 | 0.1979 | 0.1319 | False |
| sjogren_gland_epithelial | sjogren_gland_apc | Sjogren syndrome | lysosomal_apc | primary | M0_raw | none | 22 | 0.2333 | 0.1488 | False |
| ibd_uc_stromal | ibd_uc_myeloid | ulcerative colitis | complement_phagocytosis | primary | M0_raw | none | 12 | -0.1832 | 0.1543 | False |
| sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | lysosomal_apc | primary | M3_base_inflammation | fixed | 22 | 0.3853 | 0.1614 | False |
| ibd_crohn_stromal | ibd_crohn_myeloid | Crohn disease | complement_phagocytosis | primary | M3_base_inflammation | fixed | 12 | -0.4154 | 0.1723 | False |
| psoriasis_skin_stromal | psoriasis_skin_apc | psoriasis | hla_ii_apc | control | M0_raw | none | 6 | 2.468 | 0.1789 | False |
| ibd_uc_stromal | ibd_uc_myeloid | ulcerative colitis | inflammatory_nfkb | control | M0_raw | none | 12 | 0.4986 | 0.1798 | False |
| sjogren_gland_epithelial | sjogren_gland_apc | Sjogren syndrome | hif_nampt_metabolic | control | M0_raw | none | 22 | 0.2083 | 0.1841 | False |
| ibd_crohn_epithelial | ibd_crohn_myeloid | Crohn disease | hif_nampt_metabolic | control | M0_raw | none | 12 | 1.373 | 0.1894 | False |
| sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | ifn_apc | control | M3_base_inflammation | fixed | 22 | 0.3095 | 0.1941 | False |
| sjogren_gland_epithelial | sjogren_gland_apc | Sjogren syndrome | ifn_apc | control | M0_raw | none | 22 | -0.1248 | 0.2126 | False |
| ibd_uc_epithelial | ibd_uc_myeloid | ulcerative colitis | hif_nampt_metabolic | control | M0_raw | none | 12 | 0.755 | 0.2157 | False |
| ibd_uc_epithelial | ibd_uc_myeloid | ulcerative colitis | inflammatory_nfkb | control | M0_raw | none | 12 | 0.9966 | 0.2244 | False |
| sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | hla_ii_apc | control | M3_base_inflammation | fixed | 22 | 0.2031 | 0.2458 | False |
| ibd_crohn_stromal | ibd_crohn_myeloid | Crohn disease | ifn_apc | control | M3_base_inflammation | fixed | 12 | 0.3819 | 0.247 | False |
| sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | inflammatory_nfkb | control | M0_raw | none | 22 | 0.3109 | 0.2471 | False |
| psoriasis_keratinocyte | psoriasis_skin_apc | psoriasis | hif_nampt_metabolic | control | M0_raw | none | 6 | -0.6334 | 0.2502 | False |
| ibd_uc_epithelial | ibd_uc_myeloid | ulcerative colitis | lipid_loader_repair | primary | M3_base_inflammation | fixed | 12 | 0.1518 | 0.2554 | False |
| ibd_uc_epithelial | ibd_uc_myeloid | ulcerative colitis | ifn_apc | control | M3_base_inflammation | fixed | 12 | 0.1993 | 0.2683 | False |
| ibd_uc_stromal | ibd_uc_myeloid | ulcerative colitis | ifn_apc | control | M3_base_inflammation | fixed | 12 | -0.1356 | 0.2799 | False |
| ibd_crohn_epithelial | ibd_crohn_myeloid | Crohn disease | hla_ii_apc | control | M0_raw | none | 12 | 0.807 | 0.2856 | False |
| ibd_crohn_epithelial | ibd_crohn_myeloid | Crohn disease | inflammatory_nfkb | control | M0_raw | none | 12 | 1.92 | 0.3004 | False |
| sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | complement_phagocytosis | primary | M0_raw | none | 22 | 0.3661 | 0.3008 | False |
| ibd_uc_stromal | ibd_uc_myeloid | ulcerative colitis | ifn_apc | control | M7_broad_nonoutcome_context | fixed | 12 | -0.1019 | 0.3034 | False |
| ibd_crohn_stromal | ibd_crohn_myeloid | Crohn disease | lipid_loader_repair | primary | M0_raw | none | 12 | 0.07493 | 0.3067 | False |
| psoriasis_skin_stromal | psoriasis_skin_apc | psoriasis | complement_phagocytosis | primary | M0_raw | none | 6 | -1.96 | 0.3158 | False |
| psoriasis_keratinocyte | psoriasis_skin_apc | psoriasis | ifn_apc | control | M0_raw | none | 6 | 0.9543 | 0.3204 | False |
| ibd_uc_stromal | ibd_uc_myeloid | ulcerative colitis | hif_nampt_metabolic | control | M7_broad_nonoutcome_context | fixed | 12 | 0.074 | 0.3426 | False |
| ibd_uc_stromal | ibd_uc_myeloid | ulcerative colitis | lysosomal_apc | primary | M7_broad_nonoutcome_context | fixed | 12 | 0.03221 | 0.3439 | False |
| ibd_uc_epithelial | ibd_uc_myeloid | ulcerative colitis | complement_phagocytosis | primary | M0_raw | none | 12 | -0.2716 | 0.3489 | False |
| sjogren_gland_epithelial | sjogren_gland_apc | Sjogren syndrome | lipid_loader_repair | primary | M0_raw | none | 22 | 0.13 | 0.3588 | False |
| sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | hla_ii_apc | control | M0_raw | none | 22 | -0.1764 | 0.364 | False |
| psoriasis_skin_stromal | psoriasis_skin_apc | psoriasis | inflammatory_nfkb | control | M0_raw | none | 6 | -1.713 | 0.3714 | False |
| ibd_uc_stromal | ibd_uc_myeloid | ulcerative colitis | inflammatory_nfkb | control | M7_broad_nonoutcome_context | fixed | 12 | -0.08595 | 0.3726 | False |
| sjogren_gland_epithelial | sjogren_gland_apc | Sjogren syndrome | lysosomal_apc | primary | M7_broad_nonoutcome_context | fixed | 22 | 0.1451 | 0.3742 | False |
| psoriasis_skin_stromal | psoriasis_skin_apc | psoriasis | lysosomal_apc | primary | M0_raw | none | 6 | -0.8926 | 0.3775 | False |
| ibd_uc_stromal | ibd_uc_myeloid | ulcerative colitis | ifn_apc | control | M0_raw | none | 12 | 0.1636 | 0.3858 | False |
| sjogren_gland_epithelial | sjogren_gland_apc | Sjogren syndrome | lipid_loader_repair | primary | M3_base_inflammation | fixed | 22 | 0.2281 | 0.3882 | False |
| ibd_crohn_epithelial | ibd_crohn_myeloid | Crohn disease | hif_nampt_metabolic | control | M3_base_inflammation | fixed | 12 | 0.3741 | 0.4006 | False |
| ibd_uc_stromal | ibd_uc_myeloid | ulcerative colitis | complement_phagocytosis | primary | M3_base_inflammation | fixed | 12 | 0.1173 | 0.4012 | False |

## Interpretation

Specificity requires primary lipid/lysosomal positive tests without parallel
positive control-module tests (`ifn_apc`, `inflammatory_nfkb`,
`hif_nampt_metabolic`, `hla_ii_apc`) in the same paired context. If controls
are also positive, CD82 is interpreted as a generic tissue activation marker.

## Reproducibility

- Script: `scripts/v3_wave106_cd82_specificity_confounder_audit.py`
- Input pairs: `results_v3/wave104_accessible_survivor_niche_controller_test/matched_niche_pairs.tsv`
- Wave105 robust contexts: `results_v3/wave105_cd82_niche_robustness_audit/cd82_robust_tests.tsv`
- Tests: `results_v3/wave106_cd82_specificity_confounder_audit/cd82_specificity_tests.tsv`
- Summary: `results_v3/wave106_cd82_specificity_confounder_audit/cd82_specificity_summary.tsv`
- Seed: `20260527`
