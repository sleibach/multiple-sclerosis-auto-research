# Wave107 CD82 Multiplicity / Disease-Collapse Audit

## Bottom Line

Branch call: `CD82_PROVISIONAL_NICHE_BIOMARKER_SIGNAL_NOT_REOPENED`.

This audit implements the hostile methods review's core correction: do not
count multiple target modules from the same donor set as independent disease
replication, and do not call a context strong if it fails BH correction,
specificity controls, or estimable strict-model support.

## Disease-Collapsed Evidence

| disease_name | source_analysis | target_analysis | n_module_contexts | n_m3_perm_q_positive | n_strict_context_pass | n_provisional_context_pass | n_generic_context | fisher_m3_perm_p | fisher_q | stouffer_signed_m3_perm_p | stouffer_q | strict_disease_pass | provisional_disease_pass | specificity_calls |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Sjogren syndrome | sjogren_gland_epithelial | sjogren_gland_apc | 3 | 0 | 0 | 1 | 0 | 0.03415 | 0.05122 | 0.003335 | 0.005002 | False | True | SPECIFIC_PRIMARY_OVER_CONTROLS_M3 |
| Crohn disease | ibd_crohn_epithelial | ibd_crohn_myeloid | 3 | 1 | 0 | 0 | 3 | 0.0001451 | 0.0004352 | 7.007e-06 | 2.102e-05 | False | False | GENERIC_TARGET_ACTIVATION_COUPLING |
| ulcerative colitis | ibd_uc_epithelial | ibd_uc_myeloid | 3 | 0 | 0 | 0 | 0 | 0.7064 | 0.7064 | 0.3678 | 0.3678 | False | False | NO_PRIMARY_SIGNAL |
| Crohn disease | ibd_crohn_stromal | ibd_crohn_myeloid | 3 | 0 | 0 | 0 | 0 |  |  |  |  | False | False | NO_PRIMARY_SIGNAL |
| Sjogren syndrome | sjogren_gland_stromal | sjogren_gland_apc | 3 | 0 | 0 | 0 | 3 |  |  |  |  | False | False | GENERIC_TARGET_ACTIVATION_COUPLING_M7 |
| psoriasis | psoriasis_keratinocyte | psoriasis_skin_apc | 3 | 0 | 0 | 0 | 0 |  |  |  |  | False | False | NO_PRIMARY_SIGNAL |
| psoriasis | psoriasis_skin_stromal | psoriasis_skin_apc | 3 | 0 | 0 | 0 | 0 |  |  |  |  | False | False | NO_PRIMARY_SIGNAL |
| ulcerative colitis | ibd_uc_stromal | ibd_uc_myeloid | 3 | 0 | 0 | 0 | 0 |  |  |  |  | False | False | NO_PRIMARY_SIGNAL |

## Context-Level Evidence

| source_analysis | target_analysis | disease_name | target_module | m3_slope | m3_p | m3_perm_p | m3_perm_q_all_contexts | m4_estimable | specificity_call | strict_context_pass | provisional_context_pass |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ibd_crohn_epithelial | ibd_crohn_myeloid | Crohn disease | lysosomal_apc | 1.211 | 0.00349 | 0.001999 | 0.01799 | False | GENERIC_TARGET_ACTIVATION_COUPLING | False | False |
| ibd_crohn_epithelial | ibd_crohn_myeloid | Crohn disease | lipid_loader_repair | 0.6412 | 0.02362 | 0.01599 | 0.07196 | False | GENERIC_TARGET_ACTIVATION_COUPLING | False | False |
| ibd_crohn_epithelial | ibd_crohn_myeloid | Crohn disease | complement_phagocytosis | 1.055 | 0.04268 | 0.04298 | 0.1016 | False | GENERIC_TARGET_ACTIVATION_COUPLING | False | False |
| sjogren_gland_epithelial | sjogren_gland_apc | Sjogren syndrome | lysosomal_apc | 0.4259 | 0.03835 | 0.04548 | 0.1016 | True | SPECIFIC_PRIMARY_OVER_CONTROLS_M3 | False | True |
| sjogren_gland_epithelial | sjogren_gland_apc | Sjogren syndrome | complement_phagocytosis | 0.621 | 0.0613 | 0.05647 | 0.1016 | True | SPECIFIC_PRIMARY_OVER_CONTROLS_M3 | False | False |
| ibd_uc_epithelial | ibd_uc_myeloid | ulcerative colitis | lipid_loader_repair | 0.1518 | 0.2554 | 0.2729 | 0.4093 | False | NO_PRIMARY_SIGNAL | False | False |
| sjogren_gland_epithelial | sjogren_gland_apc | Sjogren syndrome | lipid_loader_repair | 0.2281 | 0.3882 | 0.4288 | 0.5513 | True | SPECIFIC_PRIMARY_OVER_CONTROLS_M3 | False | False |
| ibd_uc_epithelial | ibd_uc_myeloid | ulcerative colitis | complement_phagocytosis | -0.1121 | 0.5923 | 0.5757 | 0.6477 | False | NO_PRIMARY_SIGNAL | False | False |
| ibd_uc_epithelial | ibd_uc_myeloid | ulcerative colitis | lysosomal_apc | 0.01063 | 0.9604 | 0.9615 | 0.9615 | False | NO_PRIMARY_SIGNAL | False | False |
| ibd_crohn_stromal | ibd_crohn_myeloid | Crohn disease | complement_phagocytosis |  |  |  |  | False | NO_PRIMARY_SIGNAL | False | False |
| ibd_crohn_stromal | ibd_crohn_myeloid | Crohn disease | lipid_loader_repair |  |  |  |  | False | NO_PRIMARY_SIGNAL | False | False |
| ibd_crohn_stromal | ibd_crohn_myeloid | Crohn disease | lysosomal_apc |  |  |  |  | False | NO_PRIMARY_SIGNAL | False | False |
| ibd_uc_stromal | ibd_uc_myeloid | ulcerative colitis | complement_phagocytosis |  |  |  |  | False | NO_PRIMARY_SIGNAL | False | False |
| ibd_uc_stromal | ibd_uc_myeloid | ulcerative colitis | lipid_loader_repair |  |  |  |  | False | NO_PRIMARY_SIGNAL | False | False |
| ibd_uc_stromal | ibd_uc_myeloid | ulcerative colitis | lysosomal_apc |  |  |  |  | False | NO_PRIMARY_SIGNAL | False | False |
| psoriasis_keratinocyte | psoriasis_skin_apc | psoriasis | complement_phagocytosis |  |  |  |  | False | NO_PRIMARY_SIGNAL | False | False |
| psoriasis_keratinocyte | psoriasis_skin_apc | psoriasis | lipid_loader_repair |  |  |  |  | False | NO_PRIMARY_SIGNAL | False | False |
| psoriasis_keratinocyte | psoriasis_skin_apc | psoriasis | lysosomal_apc |  |  |  |  | False | NO_PRIMARY_SIGNAL | False | False |
| psoriasis_skin_stromal | psoriasis_skin_apc | psoriasis | complement_phagocytosis |  |  |  |  | False | NO_PRIMARY_SIGNAL | False | False |
| psoriasis_skin_stromal | psoriasis_skin_apc | psoriasis | lipid_loader_repair |  |  |  |  | False | NO_PRIMARY_SIGNAL | False | False |
| psoriasis_skin_stromal | psoriasis_skin_apc | psoriasis | lysosomal_apc |  |  |  |  | False | NO_PRIMARY_SIGNAL | False | False |
| sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | complement_phagocytosis |  |  |  |  | False | GENERIC_TARGET_ACTIVATION_COUPLING_M7 | False | False |
| sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | lipid_loader_repair |  |  |  |  | False | GENERIC_TARGET_ACTIVATION_COUPLING_M7 | False | False |
| sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | lysosomal_apc |  |  |  |  | False | GENERIC_TARGET_ACTIVATION_COUPLING_M7 | False | False |

## Decision Rule

`CD82_REOPENED_AFTER_MULTIPLICITY_COLLAPSE` would require strict disease pass
in at least two diseases. Strict pass requires context-level BH-corrected
permutation support, estimable positive M4, specificity over control modules,
and no generic target-activation coupling.

## Interpretation

If this audit downgrades CD82, CD82 remains usable only as a provisional
matched-niche biomarker/readout for ex vivo mechanism experiments. It is not a
target and not an indirect intervention nomination.

## Reproducibility

- Script: `scripts/v3_wave107_cd82_multiplicity_disease_collapse_audit.py`
- Wave105 context summary: `results_v3/wave105_cd82_niche_robustness_audit/cd82_robustness_summary.tsv`
- Wave105 model grid: `results_v3/wave105_cd82_niche_robustness_audit/cd82_model_grid_tests.tsv`
- Wave106 specificity summary: `results_v3/wave106_cd82_specificity_confounder_audit/cd82_specificity_summary.tsv`
- Context output: `results_v3/wave107_cd82_multiplicity_disease_collapse_audit/cd82_context_multiplicity.tsv`
- Disease output: `results_v3/wave107_cd82_multiplicity_disease_collapse_audit/cd82_disease_collapsed_evidence.tsv`
- Seed: `20260527`
