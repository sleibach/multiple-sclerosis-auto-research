# Wave84 Stratification-First Audit

## Question

Does the lipid-lysosomal/myeloid state stratify treatment response across
independent autoimmune datasets strongly enough to support a biomarker-guided
claim?

## Verdict

This wave does not produce a therapeutic target. It tests whether a
stratification route is more defensible than direct target nomination.

## Module Calls

| module | wave84_call | n_tissue_nominal_auc60 | n_tissue_support_datasets | n_blood_nominal_auc60 | tissue_direction_conflict | blood_tissue_direction_contradiction | best_tissue_system | best_tissue_adjusted_effect | best_tissue_adjusted_p | best_tissue_oriented_auc | best_blood_system | best_blood_adjusted_effect | best_blood_adjusted_p |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| lysosomal_apc__resid_inflammatory_nfkb | PARK_TISSUE_STRATIFICATION_SIGNAL | 2 | 2 | 0 | False | False | RA_synovium_antiTNF | 0.2707 | 0.03441 | 0.6862 |  |  |  |
| ifn_lysosomal_apc_composite | PARK_TISSUE_STRATIFICATION_SIGNAL | 2 | 2 | 0 | False | False | RA_synovium_antiTNF | 0.246 | 0.05812 | 0.6569 |  |  |  |
| mif_cd74_receptor_state | NO_GO_TISSUE_SIGNAL_BLOOD_CONTRADICTION | 2 | 2 | 0 | True | False | IBD_Mono_macro_antiTNF | -0.4575 | 0.003528 | 0.8173 | RA_blood_CD4_T_cell_antiTNF | 0.1831 | 0.2478 |
| lipid_loader_repair | NO_GO_TISSUE_SIGNAL_BLOOD_CONTRADICTION | 2 | 2 | 0 | True | False | RA_synovium_antiTNF | -0.2199 | 0.02902 | 0.7057 | RA_blood_CD4_T_cell_antiTNF | 0.1297 | 0.1771 |
| lysosomal_apc | NO_GO_TISSUE_SIGNAL_BLOOD_CONTRADICTION | 2 | 2 | 1 | False | True | RA_synovium_antiTNF | 0.2707 | 0.03441 | 0.6862 | RA_blood_CD14_monocyte_antiTNF | -0.2819 | 0.03895 |
| hla_ii_apc__resid_ifn_apc_inflammatory_nfkb | NO_GO_STRATIFICATION_NOT_REPLICATED | 2 | 1 | 0 | False | False | IBD_Mono_macro_antiTNF | -0.424 | 0.0009406 | 0.8798 |  |  |  |
| hla_ii_apc | NO_GO_STRATIFICATION_NOT_REPLICATED | 1 | 1 | 0 | False | False | IBD_Mono_macro_antiTNF | -0.4814 | 0.00192 | 0.8317 | RA_blood_CD4_T_cell_antiTNF | 0.2258 | 0.2539 |
| ifn_lysosomal_apc_composite__resid_inflammatory_nfkb | NO_GO_STRATIFICATION_NOT_REPLICATED | 1 | 1 | 0 | False | False | RA_synovium_antiTNF | 0.246 | 0.05812 | 0.6569 |  |  |  |
| ifn_apc__resid_inflammatory_nfkb | NO_GO_STRATIFICATION_NOT_REPLICATED | 0 | 0 | 0 | False | False | RA_synovium_antiTNF | 0.2213 | 0.1457 | 0.6355 |  |  |  |
| ifn_apc | NO_GO_STRATIFICATION_NOT_REPLICATED | 0 | 0 | 0 | False | False | RA_synovium_antiTNF | 0.2213 | 0.1457 | 0.6355 | RA_blood_CD4_T_cell_antiTNF | 0.1978 | 0.1955 |
| inflammatory_nfkb | NO_GO_STRATIFICATION_NOT_REPLICATED | 0 | 0 | 0 | False | False | IBD_DC_antiTNF | 0.1218 | 0.46 | 0.6587 | RA_blood_CD4_T_cell_antiTNF | 0.1618 | 0.2485 |
| complement_phagocytosis | NO_GO_STRATIFICATION_NOT_REPLICATED | 0 | 0 | 1 | False | False |  |  |  |  | RA_blood_CD14_monocyte_antiTNF | -0.2622 | 0.02712 |

## Top Individual Context Tests

| dataset | system | module | n | n_responders | adjusted_effect_responder_minus_non | adjusted_p | adjusted_fdr | oriented_auc | oriented_high_vs_low_response_rate_diff | direction | covariates |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GSE282122 | IBD_Mono_macro_antiTNF | hla_ii_apc__resid_ifn_apc_inflammatory_nfkb | 29 | 13 | -0.424 | 0.0009406 | 0.05079 | 0.8798 | 0.7286 | lower_in_responders | baseline_inflammation_score;Disease |
| GSE282122 | IBD_Mono_macro_antiTNF | hla_ii_apc | 29 | 13 | -0.4814 | 0.00192 | 0.05185 | 0.8317 | 0.4524 | lower_in_responders | baseline_inflammation_score;Disease |
| GSE282122 | IBD_Mono_macro_antiTNF | mif_cd74_receptor_state | 29 | 13 | -0.4575 | 0.003528 | 0.0635 | 0.8173 | 0.3143 | lower_in_responders | baseline_inflammation_score;Disease |
| GSE198520 | RA_synovium_antiTNF | mif_cd74_receptor_state | 46 | 19 | 0.3262 | 0.02258 | 0.2103 | 0.7018 | 0.3913 | higher_in_responders | pre_score_inflammatory_nfkb;pathotype;biologic;inflammatory_score;das28_score |
| GSE138746 | RA_blood_CD14_monocyte_antiTNF | complement_phagocytosis | 78 | 37 | -0.2622 | 0.02712 | 0.2103 | 0.646 | 0.1795 | lower_in_responders | drug |
| GSE198520 | RA_synovium_antiTNF | lipid_loader_repair | 46 | 19 | -0.2199 | 0.02902 | 0.2103 | 0.7057 | 0.2174 | lower_in_responders | pre_score_inflammatory_nfkb;pathotype;biologic;inflammatory_score;das28_score |
| GSE198520 | RA_synovium_antiTNF | lysosomal_apc__resid_inflammatory_nfkb | 46 | 19 | 0.2707 | 0.03441 | 0.2103 | 0.6862 | 0.3043 | higher_in_responders | pre_score_inflammatory_nfkb;pathotype;biologic;inflammatory_score;das28_score |
| GSE198520 | RA_synovium_antiTNF | lysosomal_apc | 46 | 19 | 0.2707 | 0.03441 | 0.2103 | 0.6862 | 0.3043 | higher_in_responders | pre_score_inflammatory_nfkb;pathotype;biologic;inflammatory_score;das28_score |
| GSE282122 | IBD_DC_antiTNF | lysosomal_apc | 29 | 13 | 0.2287 | 0.03533 | 0.2103 | 0.7115 | 0.3143 | higher_in_responders | baseline_inflammation_score;Disease |
| GSE138746 | RA_blood_CD14_monocyte_antiTNF | lysosomal_apc | 78 | 37 | -0.2819 | 0.03895 | 0.2103 | 0.6394 | 0.1795 | lower_in_responders | drug |
| GSE282122 | IBD_DC_antiTNF | hla_ii_apc__resid_ifn_apc_inflammatory_nfkb | 29 | 13 | -0.2296 | 0.04706 | 0.231 | 0.6779 | 0.1762 | lower_in_responders | baseline_inflammation_score;Disease |
| GSE198520 | RA_synovium_antiTNF | ifn_lysosomal_apc_composite | 46 | 19 | 0.246 | 0.05812 | 0.2414 | 0.6569 | 0.2174 | higher_in_responders | pre_score_inflammatory_nfkb;pathotype;biologic;inflammatory_score;das28_score |
| GSE198520 | RA_synovium_antiTNF | ifn_lysosomal_apc_composite__resid_inflammatory_nfkb | 46 | 19 | 0.246 | 0.05812 | 0.2414 | 0.6569 | 0.2174 | higher_in_responders | pre_score_inflammatory_nfkb;pathotype;biologic;inflammatory_score;das28_score |
| GSE282122 | IBD_DC_antiTNF | lysosomal_apc__resid_inflammatory_nfkb | 29 | 13 | 0.1923 | 0.06808 | 0.2626 | 0.6635 | 0.1762 | higher_in_responders | baseline_inflammation_score;Disease |
| GSE282122 | IBD_DC_antiTNF | ifn_lysosomal_apc_composite | 29 | 13 | 0.1769 | 0.08805 | 0.317 | 0.6683 | 0.3143 | higher_in_responders | baseline_inflammation_score;Disease |
| GSE282122 | IBD_DC_antiTNF | lipid_loader_repair | 29 | 13 | 0.1257 | 0.09986 | 0.337 | 0.6827 | 0.1762 | higher_in_responders | baseline_inflammation_score;Disease |
| GSE282122 | IBD_DC_antiTNF | ifn_lysosomal_apc_composite__resid_inflammatory_nfkb | 29 | 13 | 0.1556 | 0.1159 | 0.368 | 0.6298 | 0.3143 | higher_in_responders | baseline_inflammation_score;Disease |
| GSE138746 | RA_blood_PBMC_antiTNF | complement_phagocytosis | 79 | 38 | -0.2275 | 0.1431 | 0.3935 | 0.5802 | 0.1397 | lower_in_responders | drug |
| GSE198520 | RA_synovium_antiTNF | ifn_apc__resid_inflammatory_nfkb | 46 | 19 | 0.2213 | 0.1457 | 0.3935 | 0.6355 | 0.2174 | higher_in_responders | pre_score_inflammatory_nfkb;pathotype;biologic;inflammatory_score;das28_score |
| GSE198520 | RA_synovium_antiTNF | ifn_apc | 46 | 19 | 0.2213 | 0.1457 | 0.3935 | 0.6355 | 0.2174 | higher_in_responders | pre_score_inflammatory_nfkb;pathotype;biologic;inflammatory_score;das28_score |
| GSE138746 | RA_blood_CD4_T_cell_antiTNF | lipid_loader_repair | 78 | 37 | 0.1297 | 0.1771 | 0.4555 | 0.6018 | 0.2308 | higher_in_responders | drug |
| GSE138746 | RA_blood_CD4_T_cell_antiTNF | ifn_apc | 78 | 37 | 0.1978 | 0.1955 | 0.4758 | 0.5893 | 0.1795 | higher_in_responders | drug |
| GSE282122 | IBD_DC_antiTNF | hla_ii_apc | 29 | 13 | -0.1795 | 0.2071 | 0.4758 | 0.5673 | 0.0381 | lower_in_responders | baseline_inflammation_score;Disease |
| GSE138746 | RA_blood_PBMC_antiTNF | lysosomal_apc | 79 | 38 | -0.2019 | 0.2115 | 0.4758 | 0.5738 | 0.1904 | lower_in_responders | drug |
| GSE138746 | RA_blood_CD4_T_cell_antiTNF | mif_cd74_receptor_state | 78 | 37 | 0.1831 | 0.2478 | 0.5078 | 0.5709 | 0.1795 | higher_in_responders | drug |
| GSE138746 | RA_blood_CD4_T_cell_antiTNF | inflammatory_nfkb | 78 | 37 | 0.1618 | 0.2485 | 0.5078 | 0.5913 | 0.1795 | higher_in_responders | drug |
| GSE138746 | RA_blood_CD4_T_cell_antiTNF | hla_ii_apc | 78 | 37 | 0.2258 | 0.2539 | 0.5078 | 0.5801 | 0.07692 | higher_in_responders | drug |
| GSE282122 | IBD_Mono_macro_antiTNF | lysosomal_apc__resid_inflammatory_nfkb | 29 | 13 | 0.1399 | 0.2749 | 0.5301 | 0.6202 | 0.3143 | higher_in_responders | baseline_inflammation_score;Disease |
| GSE198520 | RA_synovium_antiTNF | hla_ii_apc | 46 | 19 | 0.1444 | 0.2931 | 0.5459 | 0.6023 | 0.1304 | higher_in_responders | pre_score_inflammatory_nfkb;pathotype;biologic;inflammatory_score;das28_score |
| GSE282122 | IBD_Mono_macro_antiTNF | lipid_loader_repair | 29 | 13 | 0.152 | 0.3287 | 0.5584 | 0.5962 | 0.0381 | higher_in_responders | baseline_inflammation_score;Disease |

## Existing Cross-Dataset Summaries Used As Guardrails

Wave75 best cross-dataset response rows:

| module | endpoint | ra_best_comparison | ra_effect | ra_p | ra_fdr | ibd_best_cell_state | ibd_effect | ibd_p | ibd_fdr | direction_stable | both_nominal_p10 | one_nominal_other_trend | priority |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| lysosomal_apc | baseline_pre | good_vs_moderate_none | 1.018 | 0.001127 | 0.03194 | DC | 0.8878 | 0.02039 | 0.09839 | True | True | True | 7 |
| lysosomal_apc__resid_inflammatory_nfkb | baseline_pre | good_vs_moderate_none | 0.934 | 0.003074 | 0.04513 | DC | 0.7898 | 0.0392 | 0.1514 | True | True | True | 7 |
| ifn_lysosomal_apc_composite | baseline_pre | good_vs_moderate_none | 0.9078 | 0.004831 | 0.04513 | DC | 0.9478 | 0.01168 | 0.07092 | True | True | True | 7 |
| ifn_lysosomal_apc_composite__resid_inflammatory_nfkb | baseline_pre | good_vs_moderate_none | 0.832 | 0.009397 | 0.05846 | DC | 0.9103 | 0.01529 | 0.08964 | True | True | True | 7 |
| ifn_apc | baseline_pre | moderate_good_vs_none | 0.6771 | 0.01059 | 0.06001 | DC | 0.702 | 0.06062 | 0.2005 | True | True | True | 7 |
| ifn_lysosomal_apc_composite | delta_post_minus_pre | moderate_good_vs_none | -0.5896 | 0.02429 | 0.08205 | DC | -0.843 | 0.02957 | 0.1226 | True | True | True | 7 |
| lysosomal_apc | delta_post_minus_pre | moderate_good_vs_none | -0.6148 | 0.03158 | 0.09256 | DC | -1.061 | 0.008288 | 0.05636 | True | True | True | 7 |
| ifn_apc__resid_inflammatory_nfkb | baseline_pre | good_vs_moderate_none | 0.6878 | 0.03388 | 0.096 | DC | 0.6908 | 0.06487 | 0.2005 | True | True | True | 7 |

Wave76 adjusted specificity rows:

| module | endpoint | ra_comparison | ra_n | ra_coef | ra_p | ra_fdr | ra_generic_coef | ra_target_generic_abs_ratio | ibd_cell_state | ibd_n | ibd_coef | ibd_p | ibd_fdr | ibd_generic_coef | ibd_target_generic_abs_ratio | sign_stable | both_adjusted_p10 | both_ratio_ge2 | passes_wave76_specificity | priority |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| lysosomal_apc__resid_inflammatory_nfkb | baseline_pre | good_vs_moderate_none | 42 | 0.2887 | 0.07461 | 0.3954 | 0.07772 | 3.715 | DC | 29 | 0.2604 | 0.03686 | 0.5048 | 0.1535 | 1.696 | True | True | False | False | 3 |
| lysosomal_apc | baseline_pre | good_vs_moderate_none | 42 | 0.2887 | 0.07461 | 0.3954 | 0.07772 | 3.715 | DC | 29 | 0.2604 | 0.03686 | 0.5048 | 0.1535 | 1.696 | True | True | False | False | 3 |
| ifn_lysosomal_apc_composite__resid_inflammatory_nfkb | baseline_pre | good_vs_moderate_none | 42 | 0.2565 | 0.1139 | 0.3954 | 0.07772 | 3.3 | DC | 29 | 0.1959 | 0.1082 | 0.5048 | 0.1535 | 1.276 | True | False | False | False | 1 |
| ifn_lysosomal_apc_composite | baseline_pre | good_vs_moderate_none | 42 | 0.2565 | 0.1139 | 0.3954 | 0.07772 | 3.3 | DC | 29 | 0.1959 | 0.1082 | 0.5048 | 0.1535 | 1.276 | True | False | False | False | 1 |
| ifn_apc__resid_inflammatory_nfkb | baseline_pre | good_vs_moderate_none | 42 | 0.2242 | 0.2349 | 0.4698 | 0.07772 | 2.885 | DC | 29 | 0.1315 | 0.4457 | 0.6934 | 0.1535 | 0.8562 | True | False | False | False | 1 |
| ifn_apc | baseline_pre | good_vs_moderate_none | 42 | 0.2242 | 0.2349 | 0.4698 | 0.07772 | 2.885 | DC | 29 | 0.1315 | 0.4457 | 0.6934 | 0.1535 | 0.8562 | True | False | False | False | 1 |
| lysosomal_apc__resid_inflammatory_nfkb | delta_post_minus_pre | good_vs_moderate_none | 42 | 0.3259 | 0.1264 | 0.3954 | -0.2766 | 1.178 | DC | 29 | -0.2035 | 0.08691 | 0.5048 | -0.01959 | 10.39 | False | False | False | False | 0 |
| lysosomal_apc | delta_post_minus_pre | good_vs_moderate_none | 42 | 0.3259 | 0.1264 | 0.3954 | -0.2766 | 1.178 | DC | 29 | -0.2035 | 0.08691 | 0.5048 | -0.01959 | 10.39 | False | False | False | False | 0 |

## Secondary Pharmacodynamic / Small Response Contexts

| dataset | system | module | n | effect_post_minus_pre | p | fdr | note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GSE183047 | psoriasis_secukinumab_myeloid_apc_like | complement_phagocytosis | 4 | -0.2299 | 0.06529 | 0.9747 | pharmacodynamic only; no responder/non-responder stratification |
| GSE183047 | psoriasis_secukinumab_myeloid_apc_like | hif_nampt_metabolic | 4 | -0.02834 | 0.6984 | 1 | pharmacodynamic only; no responder/non-responder stratification |
| GSE183047 | psoriasis_secukinumab_myeloid_apc_like | hla_ii_apc | 4 | -0.2072 | 0.525 | 1 | pharmacodynamic only; no responder/non-responder stratification |
| GSE183047 | psoriasis_secukinumab_myeloid_apc_like | ifn_apc | 4 | -0.2033 | 0.2437 | 0.9747 | pharmacodynamic only; no responder/non-responder stratification |
| GSE183047 | psoriasis_secukinumab_myeloid_apc_like | il17_keratinocyte_inflammation | 4 | -0.4989 | 0.1131 | 0.9747 | pharmacodynamic only; no responder/non-responder stratification |
| GSE183047 | psoriasis_secukinumab_myeloid_apc_like | inflammatory_nfkb | 4 | -0.07054 | 0.3345 | 1 | pharmacodynamic only; no responder/non-responder stratification |
| GSE183047 | psoriasis_secukinumab_myeloid_apc_like | lipid_loader_repair | 4 | -0.07469 | 0.5129 | 1 | pharmacodynamic only; no responder/non-responder stratification |
| GSE183047 | psoriasis_secukinumab_myeloid_apc_like | lysosomal_apc | 4 | -0.2083 | 0.01984 | 0.7427 | pharmacodynamic only; no responder/non-responder stratification |
| GSE183047 | psoriasis_secukinumab_myeloid_apc_like | mif_cd74_receptor_state | 4 | -0.2491 | 0.3981 | 1 | pharmacodynamic only; no responder/non-responder stratification |
| GSE183047 | psoriasis_secukinumab_myeloid_apc_like | mixscale_validated_ifng_readout | 4 | -0.1795 | 0.2265 | 0.9747 | pharmacodynamic only; no responder/non-responder stratification |
| GSE183047 | psoriasis_secukinumab_myeloid_apc_like | regulatory_dc_markers | 4 | -0.1828 | 0.1097 | 0.9747 | pharmacodynamic only; no responder/non-responder stratification |
| GSE253006 | UC_tofacitinib_stromal_endothelial_like | lipid_loader_repair | 4R/6NR | -0.07802 | 0.03529 | 0.9761 | UC tofacitinib marker-derived compartments; copied from existing V3 output |
| GSE253006 | UC_tofacitinib_stromal_endothelial_like | lipid_loader_repair | 4R/6NR | -0.05247 | 0.1291 | 0.9761 | UC tofacitinib marker-derived compartments; copied from existing V3 output |
| GSE253006 | UC_tofacitinib_myeloid_apc_like | mixscale_validated_ifng_readout | 5R/6NR | -0.07494 | 0.1499 | 0.9761 | UC tofacitinib marker-derived compartments; copied from existing V3 output |
| GSE253006 | UC_tofacitinib_myeloid_apc_like | mif_cd74_receptor_state | 5R/6NR | -0.07985 | 0.2552 | 0.9761 | UC tofacitinib marker-derived compartments; copied from existing V3 output |
| GSE253006 | UC_tofacitinib_t_cell_like | complement_phagocytosis | 5R/6NR | 0.02387 | 0.2569 | 0.9761 | UC tofacitinib marker-derived compartments; copied from existing V3 output |
| GSE253006 | UC_tofacitinib_stromal_endothelial_like | lysosomal_apc | 4R/6NR | 0.06362 | 0.2675 | 0.9761 | UC tofacitinib marker-derived compartments; copied from existing V3 output |
| GSE253006 | UC_tofacitinib_myeloid_apc_like | ifn_apc | 5R/6NR | -0.07032 | 0.2846 | 0.9761 | UC tofacitinib marker-derived compartments; copied from existing V3 output |
| GSE253006 | UC_tofacitinib_epithelial_like | lysosomal_apc | 5R/6NR | 0.04797 | 0.2854 | 0.9761 | UC tofacitinib marker-derived compartments; copied from existing V3 output |
| GSE253006 | UC_tofacitinib_myeloid_apc_like | mixscale_validated_ifng_readout | 5R/6NR | -0.0683 | 0.3051 | 0.9761 | UC tofacitinib marker-derived compartments; copied from existing V3 output |

## Interpretation

Tissue-level anti-TNF datasets provide the only plausible stratification signal.
Peripheral blood and small non-anti-TNF contexts do not cleanly replicate it.
Any downstream claim must therefore be restricted to tissue-resident inflammatory
myeloid/APC states and cannot be generalized to a blood biomarker or a direct
MS target from these data.

## Outputs

- `stratification_context_tests.tsv`
- `module_stratification_summary.tsv`
- `secondary_pharmacodynamic_or_small_response_contexts.tsv`
- `summary.json`
