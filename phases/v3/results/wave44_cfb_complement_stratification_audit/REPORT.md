# Wave44 CFB Complement Stratification Audit

## Result

CFB is a strong comparator route, not a V3 finding. It has broad local tissue recurrence, CFB druggability, and residual signal in Crohn/stromal contexts, but no MS anchor, no target-resolved causal genetic package, no favorable perturbation/model support, and heavy factor-B inhibitor prior art/trial crowding. A biomarker-selected CFB-high autoimmune subgroup remains plausible only as a clinical-repurposing hypothesis outside this V3 claim.

## Failed Gates

- no_MS_anchor_or_positive_MS_lesion_direction
- no_target_resolved_coloc_or_mr
- foundation_or_model_support_marked_do_not_promote
- strict_core_residual_survival_only_Crohn_stromal
- factor_B_inhibition_prior_art_and_trial_crowding
- systemic_complement_host_defense_safety

## Wave34 CFB Row

| gene | wave34_score | wave34_call | failed_gates | gwas_catalog_trait_count | gwas_catalog_min_p | gwas_catalog_traits | local_positive_disease_count | local_negative_disease_count | positive_diseases | residual_retained_disease_count | ms_anchor | ms_wm_delta_log2 | ms_wm_p | genetics_ready_score | ot_n_diseases_score_ge_0_5 | gtex_n_relevant_tissues_with_significant_cis_eqtl | druggable_activity_count | chembl_target_id | chembl_pref_name | chembl_target_type | chembl_best_nM | clinicaltrials_autoimmune_count | europepmc_autoimmune_hit_count | perturbation_or_model_support | foundation_rescue_recommendation | foundation_real_perturbation_alignment_call | manual_blocker_class | manual_blocker_text_wave34 | proxy_call | primary_blocker |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CFB | 23.5 | NO_GO_GENETIC_DRUGGABLE_PRIOR_ART_BLOCKED | gate_not_prior_art_blocked | 10 | 2.0000000000000003e-165 | Crohn's disease (Tractor method with European ancestry);Extraintestinal manifestations in inflammatory bowel disease (ocular manifestations);Inflammatory bowel disease;Inflammatory bowel disease (Tractor method with European ancestry);Inflammatory bowel disease x sex interaction (2df);Primary sclerosing cholangitis (MTAG);Rheumatoid arthritis or type 1 diabetes;Systemic lupus erythematosus;Type 1 diabetes and autoimmune thyroid diseases;Ulcerative colitis | 4.0 | 0.0 | Crohn disease;psoriasis;type 1 diabetes mellitus;ulcerative colitis | 4.0 | False | -0.9822682065524936 | 0.2868607768107353 | 0.0 | 0.0 | 0.0 | 341.0 | CHEMBL5731 | Complement factor B | SINGLE PROTEIN | 1.0 | 32.0 | 2567.0 | True | do_not_promote_from_foundation_model | model_only_no_real_perturbation_alignment |  |  | NO_GO_CAUSAL_PROXY | no_target_resolved_coloc_or_mr |

## Residual CFB Row

| gene | selection_reasons | discovery_priority_score | broad_positive_disease_count | broad_negative_disease_count | broad_ms_positive_nominal | ms_wm_delta_log2 | ms_wm_p | in_lipid_lysosomal_myeloid_neighborhood | raw_positive_analysis_count | raw_positive_disease_count | raw_negative_analysis_count | retained_positive_analysis_count | retained_positive_disease_count | non_ibd_retained_positive_analysis_count | non_ibd_retained_positive_disease_count | strict_core_covariate_surviving_analysis_count | strict_core_covariate_surviving_disease_count | strict_core_covariate_surviving_analyses | raw_positive_analyses | top_retained_tests | residual_gate_priority_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CFB | four_disease_low_contradiction;top_rank | 25.004597697631812 | 4.0 | 0.0 | False | -0.9822682065524936 | 0.2868607768107353 | False | 7 | 4 | 0 | 7 | 4 | 4 | 2 | 1 | 1 | ibd_crohn_stromal:Crohn disease | psoriasis_skin_stromal:0.214,p=0.0056;ibd_crohn_epithelial:0.406,p=0.0071;ibd_crohn_stromal:0.419,p=0.0079;ibd_uc_epithelial:0.567,p=0.02;t1d_stellate_cell:0.927,p=0.025;psoriasis_keratinocyte:0.628,p=0.035;t1d_ductal_cell:1.15,p=0.044 | t1d_stellate_cell\|core_lysosomal_lipid:0.754,p=2.5e-05;t1d_stellate_cell\|lipid_loader_repair:0.794,p=0.00081;psoriasis_skin_stromal\|inflammatory_nfkb:0.213,p=0.0039;psoriasis_skin_stromal\|hif_nampt_metabolic:0.215,p=0.0048;ibd_crohn_stromal\|lysosomal_apc:0.42,p=0.0077;ibd_uc_epithelial\|complement_phagocytosis:0.542,p=0.0081;ibd_crohn_epithelial\|complement_phagocytosis:0.391,p=0.0089;ibd_crohn_epithelial\|lysosomal_apc:0.358,p=0.0093 | 15 |

## Prior-Art Query Counts

| query | europepmc_hit_count |
| --- | --- |
| "complement factor B" AND ("multiple sclerosis" OR "rheumatoid arthritis" OR "lupus" OR "inflammatory bowel" OR psoriasis) | 1148 |
| "factor B inhibitor" AND (autoimmune OR "multiple sclerosis" OR lupus OR "inflammatory bowel") | 190 |
| iptacopan AND (autoimmune OR "multiple sclerosis" OR lupus OR "inflammatory bowel" OR psoriasis) | 300 |
| "CFB" AND ("biomarker" OR "stratification") AND autoimmune | 662 |

| query | clinicaltrials_count |
| --- | --- |
| complement factor B autoimmune | 1 |
| factor B inhibitor autoimmune | 1 |
| iptacopan autoimmune | 1 |
| iptacopan multiple sclerosis | 0 |
| CFB multiple sclerosis | 1 |

