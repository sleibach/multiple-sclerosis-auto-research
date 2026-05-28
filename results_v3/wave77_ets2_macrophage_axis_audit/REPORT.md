# Wave77 ETS2 Macrophage-Axis Audit

## Question

Does the locally surfaced ETS2 macrophage/gene-desert axis survive as a
cross-autoimmune/MS therapeutic or stratification route?

## Verdict

NO_GO_ETS2_LOCAL_AUDIT

## Integrated Decision

| candidate | wave77_call | gate_count | gate_cross_disease_local_breadth | gate_ms_white_matter_anchor | gate_target_resolution_not_no_go | gate_treatment_response_support | gate_direct_perturbation_support | gate_foundation_model_support | gate_druggable_route_not_blocked | broad_positive_diseases | wave62_call | decision_reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ETS2_macrophage_gene_desert_axis | NO_GO_ETS2_LOCAL_AUDIT | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | Crohn disease;ulcerative colitis | NO_GO_WAVE62_TARGET_RESOLUTION | ETS2 has known AS/UC/Crohn macrophage/genetic signal but fails MS anchor, treatment-response, perturbation, and druggable-route gates in local V3 data |

## Broad Cell-State ETS2 Summary

| disease_name | tested_contexts | positive_contexts | negative_contexts | best_effect | best_p | best_fdr | positive_compartments |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ulcerative colitis | 3 | 2 | 0 | 1.972 | 0.0002169 | 0.05209 | colon epithelial;colon myeloid |
| Crohn disease | 3 | 1 | 0 | 1.519 | 0.004807 | 0.176 | colon myeloid |
| psoriasis | 3 | 0 | 0 | -0.7909 | 0.1562 | 0.5172 |  |
| type 1 diabetes mellitus | 5 | 0 | 0 | -0.3646 | 0.1657 | 0.6023 |  |
| Sjogren syndrome | 3 | 0 | 0 | -0.28 | 0.2805 | 0.8751 |  |

## Top Broad ETS2 Context Rows

| analysis | disease_name | compartment | role | delta_log2_cpm | p | fdr | nominal_positive | nominal_negative |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ibd_uc_myeloid | ulcerative colitis | colon myeloid | myeloid_apc | 1.972 | 0.0002169 | 0.05209 | True | False |
| ibd_crohn_myeloid | Crohn disease | colon myeloid | myeloid_apc | 1.519 | 0.004807 | 0.176 | True | False |
| ibd_uc_epithelial | ulcerative colitis | colon epithelial | tissue_resident | 0.6928 | 0.03443 | 0.299 | True | False |
| psoriasis_keratinocyte | psoriasis | skin keratinocyte | tissue_resident | -0.7909 | 0.1562 | 0.5172 | False | False |
| t1d_beta_cell | type 1 diabetes mellitus | pancreatic beta cell | tissue_resident | 0.2954 | 0.1657 | 0.7824 | False | False |
| t1d_ductal_cell | type 1 diabetes mellitus | pancreatic ductal cell | tissue_resident | -0.3512 | 0.2351 | 0.6023 | False | False |
| ibd_uc_stromal | ulcerative colitis | colon stromal | tissue_resident | 0.3229 | 0.2743 | 0.6638 | False | False |
| sjogren_gland_stromal | Sjogren syndrome | salivary gland stromal/endothelial | tissue_resident | -0.2412 | 0.2805 | 0.8751 | False | False |
| ibd_crohn_epithelial | Crohn disease | colon epithelial | tissue_resident | 0.3055 | 0.3464 | 0.6228 | False | False |
| psoriasis_skin_apc | psoriasis | skin APC | myeloid_apc | -0.7144 | 0.3639 | 0.7779 | False | False |
| t1d_endothelial_cell | type 1 diabetes mellitus | pancreatic endothelial cell | tissue_resident | -0.3646 | 0.3656 | 0.716 | False | False |
| sjogren_gland_apc | Sjogren syndrome | salivary gland APC | myeloid_apc | -0.28 | 0.4048 | 0.9622 | False | False |
| ibd_crohn_stromal | Crohn disease | colon stromal | tissue_resident | 0.1748 | 0.5661 | 0.8624 | False | False |
| t1d_stellate_cell | type 1 diabetes mellitus | pancreatic stellate cell | tissue_resident | 0.2104 | 0.7139 | 0.9139 | False | False |
| psoriasis_skin_stromal | psoriasis | skin stromal | tissue_resident | -0.1132 | 0.8126 | 0.9412 | False | False |
| sjogren_gland_epithelial | Sjogren syndrome | salivary gland epithelial | tissue_resident | -0.1232 | 0.8371 | 0.951 | False | False |
| t1d_acinar_cell | type 1 diabetes mellitus | pancreatic acinar cell | tissue_resident | 0.000674 | 0.9978 | 0.9988 | False | False |

## MS White-Matter ETS2

| gene | mean_case | mean_control | delta_log2 | hedges_g | welch_t | p | fdr |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ETS2 | 13.03 | 13.09 | -0.06076 | -0.07563 | -0.1739 | 0.8649 | 0.9802 |

## Wave62 Target Resolution

| gene | approved_name | wave62_score | wave62_call | manual_blocker | prior_context_blocker | max_l2g_score | best_l2g_disease | strong_l2g_disease_count | strong_l2g_diseases | supporting_l2g_disease_count | supporting_l2g_diseases | ms_max_l2g_score | ms_l2g_study_loci | strong_qtl_coloc_disease_count | strong_qtl_coloc_diseases | relevant_qtl_coloc_disease_count | relevant_qtl_coloc_diseases | myeloid_qtl_coloc_disease_count | max_qtl_h4 | ms_max_qtl_h4 | ms_max_relevant_qtl_h4 | ms_relevant_qtl_biosamples | direction_proxy_values | local_positive_disease_count | local_negative_disease_count | local_positive_diseases | ms_wm_delta_log2 | ms_wm_p | ms_wm_fdr | in_lipid_lysosomal_myeloid_neighborhood | residual_retained_disease_count | strict_core_covariate_surviving_disease_count | wave34_call | gwas_catalog_trait_count | chembl_target_id | druggable_activity_count | wave34a_call | wave34a_direction | wave34a_route_reason | wave55_score | wave55_genetic_diseases_ge_0_25 | wave61_best_call | wave61_best_manual_blocker | wave61_best_target_suppression | wave61_best_selectivity |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ETS2 | ETS proto-oncogene 2, transcription factor | 1.229 | NO_GO_WAVE62_TARGET_RESOLUTION |  |  | 0.2342 | Psoriasis | 0 |  | 0 |  | 0 |  | 2 | AS;UC | 2 | AS;UC | 2 | 0.9946 | 0 | 0 |  | AS:CD14-positive, CD16-negative classical monocyte:-0;AS:CD14-positive, CD16-negative classical monocyte:-0.0397;UC:CD14-positive, CD16-negative classical monocyte:-0.00998;UC:CD14-positive, CD16-negative classical monocyte:-0.0107;UC:CD14-positive, CD16-negative classical monocyte:-0.0138;UC:CD14-positive, CD16-negative classical monocyte:-0.0143;UC:CD14-positive, CD16-negative classical monocyte:-0.0187;UC:CD14-positive, CD16-negative classical monocyte:-0.0197;UC:CD14-positive, CD16-negative classical monocyte:-0.0549;UC:CD14-positive, CD16-negative classical monocyte:-0.171;UC:CD14-positive, CD16-negative classical monocyte:0.0905 | 2 | 0 | Crohn disease;ulcerative colitis | -0.06076 | 0.8649 | 0.9802 | False | 0 | 0 |  | 0 |  | 0 |  |  |  | 0 |  | NO_GO_WAVE61_GUARDRAIL |  | 0 | -0.01443 |

## GSE282122 IBD Anti-TNF ETS2

| dataset | test | cell_state | effect | p | fdr | n_patients | interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GSE282122_IBD_myeloid_antiTNF | remission_delta_difference | Mono_macro | -0.6527 | 0.06486 | 0.9671 |  | negative effect means ETS2 decreases more in remission than non-remission |
| GSE282122_IBD_myeloid_antiTNF | remission_delta_difference | DC | -0.1139 | 0.5205 | 1 |  | negative effect means ETS2 decreases more in remission than non-remission |
| GSE282122_IBD_myeloid_antiTNF | paired_post_minus_pre_all | DC | -0.01836 | 0.8147 | 1 | 29 | negative effect means ETS2 drops after anti-TNF |
| GSE282122_IBD_myeloid_antiTNF | paired_post_minus_pre_all | Mono_macro | 0.03031 | 0.8278 | 1 | 29 | negative effect means ETS2 drops after anti-TNF |

## GSE198520 RA Anti-TNF ETS2

| dataset | test | comparison | n_case | n_control | mean_case | mean_control | hedges_g_case_minus_control | t | p | n | mean_delta | median_delta | fdr |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GSE198520_RA_synovium_antiTNF | baseline_pre | good_vs_moderate_none | 19 | 27 | 0.4757 | -0.4695 | 0.9577 | 3.512 | 0.001048 |  |  |  | 0.005241 |
| GSE198520_RA_synovium_antiTNF | delta_post_minus_pre | good_vs_moderate_none | 19 | 27 | -0.08795 | 0.3315 | -0.3712 | -1.251 | 0.2187 |  |  |  | 0.4278 |
| GSE198520_RA_synovium_antiTNF | baseline_pre | moderate_good_vs_none | 32 | 14 | 0.04714 | -0.3677 | 0.3836 | 1.142 | 0.2661 |  |  |  | 0.4278 |
| GSE198520_RA_synovium_antiTNF | paired_post_minus_pre_all | all |  |  |  |  |  | 0.96 | 0.3422 | 46 | 0.1582 | 0.2749 | 0.4278 |
| GSE198520_RA_synovium_antiTNF | delta_post_minus_pre | moderate_good_vs_none | 32 | 14 | 0.1033 | 0.2838 | -0.1574 | -0.5509 | 0.5856 |  |  |  | 0.5856 |

## Perturbation Evidence

| source | candidate | n_evidence_records | sources | best_direct_selectivity_score | best_direct_target_suppression | best_direct_target_vs_ifn_margin | direct_evidence_calls | gse162463_mhcii_low_gate_rank_if_available | nomination_strength | nomination_priority | gene_symbol | n_sgrna | median_efficient_lfc | median_noneater_lfc | median_efficient_minus_noneater_lfc | s1_median_efficient_lfc | s3_median_efficient_lfc | s1_median_noneater_lfc | s3_median_noneater_lfc | efficient_consistent_positive | noneater_consistent_positive | efficient_p_wilcoxon | noneater_p_wilcoxon | contrast_p_wilcoxon | modules | tracked_candidate | efficient_fdr | noneater_fdr | contrast_fdr | screen_call |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| results_v3/wave15_perturbation_drug_response/candidate_level_synthesis.tsv | ETS2 | 1 | Mixscale_CRISPRi | -0.01443 | 0 | 0 | null_or_wrong_direction |  | not_nominated | 6 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| results_v3/wave37_gse212008_crispr_efferocytosis_screen/gene_level_screen_scores.tsv |  |  |  |  |  |  |  |  |  |  | ETS2 | 4 | 0.2367 | -0.02122 | 0.1432 | 0.2417 | 0.1474 | -0.03023 | 0.05421 | False | False | 0.875 | 0.875 | 0.625 |  | False | 1 | 1 | 0.9971 | UNRESOLVED |

## Geneformer/Foundation Rows

_No rows._

## Interpretation

ETS2 is a credible inflammatory macrophage biology axis in IBD/AS-like
contexts, but the local V3 data do not support a promotable MS-containing
cross-autoimmune intervention claim. The decisive local blocker is not
absence of biology; it is absence of MS anchor, response specificity,
direct useful perturbation, and a non-broad druggable route.
