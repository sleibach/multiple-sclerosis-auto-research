# Wave80 CD58/CD2-Axis Deepening

## Question

Can `CD58` be reframed from a weak myeloid-module target into a
defensible cross-autoimmune CD2/CD58 immune-synapse intervention?

## Verdict

PARK_CD58_CD2_AXIS_PRIOR_ART_OR_IBD_LIMITED

## Integrated Decision

| candidate | wave80_call | ms_anchor | ra_full_tcell_adjusted_coef | ra_full_tcell_adjusted_p | wave79_ibd_response_p | wave79_ibd_target_generic_abs_ratio | wave79_ra_response_p | wave79_ra_target_generic_abs_ratio | generic_autoimmune_prior_art | direction_conflict | decision_reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CD58_CD2_axis | PARK_CD58_CD2_AXIS_PRIOR_ART_OR_IBD_LIMITED | 1 | 0.87 | 0.008714 | 0.1732 | 1.623 | 0.002978 | 11.71 | 1 | 1 | MS genetics and RA CD58 signal survive T-cell adjustment, but IBD replication, direction, or prior art block promotion |

## RA CD58 Models With T-Cell Adjustment

| endpoint | model_name | n | response_coef | response_p | t_cell_coef | t_cell_p | effmem_t_coef | effmem_t_p | model_status | formula | response_fdr |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| baseline_pre | generic_only | 42 | 0.9104 | 0.002978 |  |  |  |  | ok | y ~ good_response + pre_generic + C(pathotype) + C(biologic) + inflammatory_score + das28_score | 0.01743 |
| baseline_pre | generic_plus_t_cell | 42 | 0.8859 | 0.006975 | -0.06419 | 0.8204 |  |  | ok | y ~ good_response + pre_generic + pre_t_cell + C(pathotype) + C(biologic) + inflammatory_score + das28_score | 0.01743 |
| baseline_pre | generic_plus_t_cell_plus_effmem | 42 | 0.87 | 0.008714 | -0.2419 | 0.5377 | 0.3035 | 0.5088 | ok | y ~ good_response + pre_generic + pre_t_cell + pre_effmem_t + C(pathotype) + C(biologic) + inflammatory_score + das28_score | 0.01743 |
| delta_post_minus_pre | generic_only | 42 | 0.7433 | 0.08006 |  |  |  |  | ok | y ~ good_response + pre_cd58 + pre_generic + delta_generic + C(pathotype) + C(biologic) + inflammatory_score + das28_score | 0.1201 |
| delta_post_minus_pre | generic_plus_t_cell | 42 | 0.5809 | 0.1729 | -0.7577 | 0.08868 |  |  | ok | y ~ good_response + pre_cd58 + pre_generic + delta_generic + pre_t_cell + delta_t_cell + C(pathotype) + C(biologic) + inflammatory_score + das28_score | 0.2074 |
| delta_post_minus_pre | generic_plus_t_cell_plus_effmem | 42 | 0.515 | 0.2616 | -0.3873 | 0.5626 | -0.6049 | 0.438 | ok | y ~ good_response + pre_cd58 + pre_generic + delta_generic + pre_t_cell + delta_t_cell + pre_effmem_t + delta_effmem_t + C(pathotype) + C(biologic) + inflammatory_score + das28_score | 0.2616 |

## RA Module Coverage

| module | n_present | genes_present |
| --- | --- | --- |
| t_cell_score | 12 | CD2;CD3D;CD3E;CD3G;CD4;CD8A;CD8B;IL7R;CCR7;SELL;LTB;CD27 |
| effector_memory_t_cell_score | 9 | CD2;CD8A;GZMB;PRF1;NKG7;GNLY;CCL5;CXCR3;KLRD1 |
| generic_inflammatory_nfkb | 9 | IL1B;TNF;CXCL8;CCL2;CCL3;CCL4;NFKBIA;TREM1;OSM |

## Wave79 CD58 Evidence

| gene | wave79_call | gate_count | gate_ms_anchor | gate_ms_nonnegative_guardrail | gate_breadth_ge3 | gate_apc_myeloid_ge2 | gate_adjusted_ra_ibd_response_specific | gate_genetics_or_target_resolution | gate_residual_survival | gate_model_or_perturbation | gate_modality | gate_prior_not_blocked | positive_disease_count | positive_diseases | apc_myeloid_positive_disease_count | apc_myeloid_positive_diseases | non_target_positive_disease_count | ms_delta_log2 | ms_p | ms_fdr | ms_max_l2g_score | qtl_strong_h4_disease_count | qtl_strong_h4_diseases | best_response_endpoint | ra_response_p | ibd_response_p | ra_target_generic_abs_ratio | ibd_target_generic_abs_ratio | strict_residual_surviving_disease_count | foundation_rows | foundation_supportive_text | foundation_do_not_promote_text | chembl_activity_count | modality_strength | wave62_call | wave39_call | wave21_call | wave71_call | decision_reason | is_target_gene |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CD58 | PARK_TARGETABILITY_SHORTLIST_NODE | 8 | 1 | 1 | 1 | 1 | 0 | 1 | 0 | 1 | 1 | 1 | 3 | Crohn disease;type 1 diabetes mellitus;ulcerative colitis | 2 | Crohn disease;ulcerative colitis | 1 | 0.1798 | 0.3111 | 0.9095 | 0.9514 | 2 | Crohn;MS | baseline_pre | 0.002978 | 0.1732 | 11.71 | 1.623 | 0 | 0 | 0 | 0 | 0 | surface_biologic_possible | PARK_MS_TARGET_RESOLVED_NO_CROSS_DISEASE_MODULE |  |  | NO_REOPEN_INSUFFICIENT_CONVERGENCE | partial support remains but one or more critical targetability gates fail | True |

## Wave79 Adjusted RA/IBD Convergence Row

| gene | endpoint | ra_comparison | ra_coef | ra_p | ra_fdr | ra_generic_coef | ra_target_generic_abs_ratio | ibd_cell_state | ibd_coef | ibd_p | ibd_fdr | ibd_generic_coef | ibd_target_generic_abs_ratio | sign_stable | both_p10 | both_ratio_ge2 | response_specificity_pass | priority |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CD58 | baseline_pre | good_vs_moderate_none | 0.9104 | 0.002978 | 0.05955 | 0.07772 | 11.71 | Mono_macro | 0.1818 | 0.1732 | 0.6413 | -0.112 | 1.623 | True | False | False | False | 1 |
| CD58 | delta_post_minus_pre | good_vs_moderate_none | 0.7433 | 0.08006 | 0.2669 | -0.2766 | 2.687 | Mono_macro | 0.2535 | 0.3284 | 0.702 | -0.3389 | 0.7481 | True | False | False | False | 1 |

## Wave62 CD58 Target Resolution

| gene | approved_name | wave62_score | wave62_call | manual_blocker | prior_context_blocker | max_l2g_score | best_l2g_disease | strong_l2g_disease_count | strong_l2g_diseases | supporting_l2g_disease_count | supporting_l2g_diseases | ms_max_l2g_score | ms_l2g_study_loci | strong_qtl_coloc_disease_count | strong_qtl_coloc_diseases | relevant_qtl_coloc_disease_count | relevant_qtl_coloc_diseases | myeloid_qtl_coloc_disease_count | max_qtl_h4 | ms_max_qtl_h4 | ms_max_relevant_qtl_h4 | ms_relevant_qtl_biosamples | direction_proxy_values | local_positive_disease_count | local_negative_disease_count | local_positive_diseases | ms_wm_delta_log2 | ms_wm_p | ms_wm_fdr | in_lipid_lysosomal_myeloid_neighborhood | residual_retained_disease_count | strict_core_covariate_surviving_disease_count | wave34_call | gwas_catalog_trait_count | chembl_target_id | druggable_activity_count | wave34a_call | wave34a_direction | wave34a_route_reason | wave55_score | wave55_genetic_diseases_ge_0_25 | wave61_best_call | wave61_best_manual_blocker | wave61_best_target_suppression | wave61_best_selectivity |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CD58 | CD58 molecule | 3.448 | PARK_MS_TARGET_RESOLVED_NO_CROSS_DISEASE_MODULE |  |  | 0.9514 | MS | 1 | MS | 1 | MS | 0.9514 | b019fe75b51b088838b09c72216af801;60eccbb51a18714ae52e2d150431c093;255d4d28fee11d6c5a0a4fb1d35becf0 | 2 | Crohn;MS | 2 | Crohn;MS | 1 | 0.9968 | 0.9945 | 0.9945 | CD14-positive, CD16-negative classical monocyte;blood plasma;lymphoblastoid cell line | Crohn:blood plasma:0.0326;MS:CD14-positive, CD16-negative classical monocyte:-0;MS:CD14-positive, CD16-negative classical monocyte:-0.0555;MS:blood plasma:-0;MS:blood plasma:-0.0555;MS:lymphoblastoid cell line:-0;MS:lymphoblastoid cell line:-0.0555;MS:lymphoblastoid cell line:0.0555;MS:lymphoblastoid cell line:0.163;MS:lymphoblastoid cell line:0.293 | 3 | 0 | Crohn disease;type 1 diabetes mellitus;ulcerative colitis | 0.1798 | 0.3111 | 0.9095 | False | 0 | 0 | PARK_GENETIC_CELL_STATE_NOT_CURRENTLY_DRUGGABLE | 5 |  | 0 |  |  |  | 17 | MS;PBC;SLE |  |  | 0 | 0 |

## Wave62 CD58 QTL/Coloc Rows

| disease | trait_from_source | variant_id | rs_ids | beta | qtl_study_type | biosample_name | h4 | risk_qtl_direction_proxy | biosample_relevant | biosample_myeloid |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MS | Multiple sclerosis | 1_116558335_A_G | rs1335532 | -0.1633 | sqtl | esophagus squamous epithelium | 0.9121 | -0.1633 | False | False |
| MS | Multiple sclerosis | 1_116558335_A_G | rs1335532 | -0.1633 | sqtl | CD14-positive, CD16-negative classical monocyte | 0.9218 | -0 | True | True |
| MS | Multiple sclerosis | 1_116558335_A_G | rs1335532 | -0.1633 | sqtl | lymphoblastoid cell line | 0.8995 | -0 | True | False |
| MS | Multiple sclerosis | 1_116558335_A_G | rs1335532 | -0.1633 | tuqtl | upper lobe of left lung | 0.8978 | -0 | False | False |
| MS | Multiple sclerosis | 1_116558335_A_G | rs1335532 | -0.1633 | tuqtl | lymphoblastoid cell line | 0.9071 | -0 | True | False |
| MS | Multiple sclerosis | 1_116558335_A_G | rs1335532 | -0.1633 | eqtl | lymphoblastoid cell line | 0.9158 | -0 | True | False |
| MS | Multiple sclerosis | 1_116558335_A_G | rs1335532 | -0.1633 | eqtl | esophagus squamous epithelium | 0.9778 | -0 | False | False |
| MS | Multiple sclerosis | 1_116558335_A_G | rs1335532 | -0.1633 | eqtl | lymphoblastoid cell line | 0.9671 | -0 | True | False |
| MS | Multiple sclerosis | 1_116558335_A_G | rs1335532 | -0.1633 | eqtl | lymphoblastoid cell line | 0.9703 | -0 | True | False |
| MS | Multiple sclerosis | 1_116558335_A_G | rs1335532 | -0.1633 | eqtl | lymphoblastoid cell line | 0.9882 | 0.1633 | True | False |
| MS | Multiple sclerosis | 1_116558335_A_G | rs1335532 | -0.1633 | eqtl | esophagus squamous epithelium | 0.9776 | -0 | False | False |
| MS | Multiple sclerosis | 1_116558335_A_G | rs1335532 | -0.1633 | eqtl | lymphoblastoid cell line | 0.9924 | 0.1633 | True | False |
| MS | Multiple sclerosis | 1_116558335_A_G | rs1335532 | -0.1633 | pqtl | blood plasma | 0.9807 | -0 | True | False |
| MS | Multiple sclerosis | 1_116561593_A_G | rs2300747 | -0.05553 | tuqtl | lymphoblastoid cell line | 0.8766 | 0.05553 | True | False |
| MS | Multiple sclerosis | 1_116561593_A_G | rs2300747 | -0.05553 | tuqtl | upper lobe of left lung | 0.3967 | -0.05553 | False | False |
| MS | Multiple sclerosis | 1_116561593_A_G | rs2300747 | -0.05553 | sqtl | esophagus squamous epithelium | 0.8121 | -0.05553 | False | False |
| MS | Multiple sclerosis | 1_116561593_A_G | rs2300747 | -0.05553 | sqtl | lymphoblastoid cell line | 0.8327 | -0.05553 | True | False |
| MS | Multiple sclerosis | 1_116561593_A_G | rs2300747 | -0.05553 | sqtl | CD14-positive, CD16-negative classical monocyte | 0.8872 | -0.05553 | True | True |
| MS | Multiple sclerosis | 1_116561593_A_G | rs2300747 | -0.05553 | pqtl | blood plasma | 0.9213 | -0.05553 | True | False |
| MS | Multiple sclerosis | 1_116561593_A_G | rs2300747 | -0.05553 | eqtl | lymphoblastoid cell line | 0.881 | 0.05553 | True | False |

## Verified Prior-Art / Directionality Table

| source_type | claim | url | identifier | local_interpretation |
| --- | --- | --- | --- | --- |
| published_ms_genetics | CD58 protective allele is associated with increased CD58 expression and enhanced FOXP3/Treg function in MS-context samples. | https://pmc.ncbi.nlm.nih.gov/articles/PMC2664005/ | PNAS 2009 CD58 locus in MS | supports CD58 as MS biology, but direction is increased CD58/restored CD2 engagement rather than simple CD58 blockade |
| meta_analysis | 2024 meta-analysis reports CD58 SNP associations with MS risk and protective effects in several genetic models. | https://doi.org/10.1016/j.msard.2023.105411 | MSARD 2024 105411 | confirms non-novel MS genetic anchor |
| approved_drug_and_autoimmune_prior_art | Alefacept is a CD58/LFA-3-Ig fusion protein targeting CD2; approved/tested in psoriasis and other immune indications. | https://www.nejm.org/doi/full/10.1056/NEJM200107263450403 | NEJM 2001 psoriasis alefacept | blocks novelty for generic CD2/CD58 autoimmune intervention |
| clinical_trial | T1DAL tested alefacept in new-onset type 1 diabetes; 12-month primary 2h C-peptide endpoint missed, secondary 4h C-peptide/insulin/hypoglycemia endpoints favored alefacept. | https://clinicaltrials.gov/study/NCT00965458 | NCT00965458 | strong cross-autoimmune prior art and a plausible lead-indication precedent, not a novel MS mechanism |
| clinical_followup | T1DAL 24-month follow-up reported sustained C-peptide and clinical/immunologic effects after alefacept. | https://www.jci.org/articles/view/81722/sd/1 | JCI T1DAL 24-month follow-up | supports CD2 targeting as biologically active, but increases prior-art burden |
| trial_registry_search | ClinicalTrials.gov searches surfaced psoriasis, T1D, transplant, graft-versus-host, aplastic anemia, and skin-disease alefacept studies, but no registered MS alefacept trial in the search results used here. | https://clinicaltrials.gov/search?term=alefacept%20multiple%20sclerosis | ClinicalTrials.gov query 2026-05-27 | MS-specific trial novelty may remain, but generic autoimmune CD2/CD58 intervention is not novel |

## Interpretation

The strongest local `CD58` signal is compatible with immune-synapse biology,
but the intervention direction is conflicted. MS genetics and the classic
CD58 locus paper point toward higher CD58 expression and Treg support,
whereas the available drug precedent, alefacept, is a CD58-Ig/CD2-directed
agent that blocks CD2/CD58 interaction and depletes CD2-high memory T
cells. That is a plausible autoimmune mechanism, but it is already prior
art in psoriasis and T1D and does not rescue the weak IBD replication in
the local V3 analysis.
