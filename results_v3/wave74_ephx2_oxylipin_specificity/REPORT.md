# Wave74-A EPHX2/Oxylipin Specificity Audit

## Question

Can existing local metabolomics, expression, response, and target-resolution data resolve an `EPHX2` soluble epoxide hydrolase EpFA/diol mechanism rather than generic lipid disturbance?

## Verdict

**NO_GO**

available data do not resolve an EPHX2-specific mechanism over generic lipid/inflammatory disturbance

Promotion requires target-level `EPHX2` support plus cross-disease biochemical specificity and independent response/replication support. Those gates are intentionally strict.

## Final Gate

| candidate | wave74_call | decision_reason | specific_supportive_disease_count | specific_normalizing_treatment_hit_count | ratio_proxy_support_count | target_support_source_count | ephx2_module_support_context_count | ephx2_response_module_support_count | specificity_pass_context_count | cross_disease_specific_biochemistry | paired_diol_epfa_ratio_proxy | target_level_ephx2_support | specificity_vs_generic_modules | independent_response_replication |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EPHX2_sEH_epoxy_fatty_acid_diol_mechanism | NO_GO | available data do not resolve an EPHX2-specific mechanism over generic lipid/inflammatory disturbance | 1 | 1 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

## Metabolite Specificity

| category | tier | match_count | tested_disease_count | supportive_disease_count | supportive_diseases | normalizing_treatment_hit_count | fdr10_feature_count | best_feature |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| epoxy_fatty_acid_epfa | ephx2_specific | 6 | 2 | 0 |  | 0 | 0 | ST002470\|UC\|UC_week0_modsev_vs_mild\|Glycidyl linoleate\|g=-0.443\|p=0.331\|fdr=0.609 |
| diol_sEH_product | ephx2_specific | 13 | 4 | 1 | UC | 1 | 1 | ST002470\|UC\|UC_week12_inactive_vs_week0_modsev\|9,10-DiHOME\|g=-0.622\|p=0.0417\|fdr=0.0931 |
| eet_dhet_named | ephx2_specific | 0 | 0 | 0 |  | 0 | 0 |  |
| hete_hydroxy_eicosanoid | adjacent_oxylipin | 8 | 2 | 0 |  | 2 | 1 | ST002470\|UC\|UC_week12_inactive_vs_week0_modsev\|15-HETE\|g=-0.796\|p=0.0113\|fdr=0.0325 |
| oxo_oxylipin | adjacent_oxylipin | 28 | 1 | 1 | T1D | 0 | 0 | ST000422\|T1D\|T1D_vs_control\|3alpha,7alpha,12beta-Trihydroxy-11-oxo-5beta-cholan-24-oic acid\|g=0.561\|p=0.0351\|fdr=0.526 |
| linoleate_pool | substrate_pool | 190 | 6 | 0 |  | 0 | 50 | ST003328\|MS_model\|PMS_SV_vs_PMS_untreated\|CE 18:2\|g=-6.11\|p=1.33e-11\|fdr=2.25e-10 |
| arachidonate_pool | substrate_pool | 109 | 7 | 0 |  | 0 | 20 | ST003328\|MS_model\|PMS_SV_vs_PMS_untreated\|CE 20:4\|g=-5.69\|p=5.36e-12\|fdr=1.13e-10 |

## Diol/EpFA Ratio Proxy

| study_id | disease | contrast | contrast_type | is_treatment_or_improvement | mean_diol_effect | n_diol_features | mean_epfa_effect | n_epfa_features | diol_minus_epfa_effect_proxy | ratio_proxy_supports_ephx2 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ST000422 | T1D | T1D_vs_control | disease_control | False | 0.1258998556345902 | 4 | 0.19776215321574075 | 4 | -0.07186229758115056 | False |
| ST000899 | Crohn | Crohn_vs_control | disease_control | False | -0.13462298868863715 | 2 |  | 0 |  | False |
| ST000899 | UC | UC_vs_control | disease_control | False | 0.6445404900116971 | 2 |  | 0 |  | False |
| ST002470 | UC | UC_week0_modsev_vs_mild | severity | False | -0.21983968982619545 | 2 | -0.4434136668195522 | 1 | 0.22357397699335674 | False |
| ST002470 | UC | UC_week12_inactive_vs_week0_modsev | treatment_or_improvement_shift | True | -0.4452049573303598 | 2 | -0.1049338713090867 | 1 | -0.3402710860212731 | False |
| ST002949 | AS | AS_vs_control | disease_control | False | 0.1950005055186936 | 1 |  | 0 |  | False |

## Direct EPHX2 Evidence

| source | evidence_type | metric | effect | p | fdr | support | blocker |
| --- | --- | --- | --- | --- | --- | --- | --- |
| broad_h5ad_gene_summary | cross_disease_cell_state_expression | positive/negative_disease_count |  |  |  | False | positive_diseases=; negative_diseases=psoriasis;ulcerative colitis |
| broad_h5ad_gene_rank | integrated_existing_rank | discovery_priority_score | -7.915842031345719 | 0.3207974938864871 | 0.9120391943246274 | False | rank is not supportive |
| GSE111972_MS_white_matter | MS_case_minus_control_expression | delta_log2 | 0.7623702959601806 | 0.3207974938864871 | 0.9120391943246274 | False | nominal MS WM EPHX2 expression support absent |
| wave62_opentargets_target_resolution | target_level_genetics | wave62_score |  |  |  | False | EPHX2 absent from Wave62 target-resolution summary |
| GSE282122_raw_remission_response | IBD_antiTNF_response | raw_delta_remission_minus_non | -0.5966159655304609 | 0.1201218220122457 | 1.0 | False | no nominal responder-normalizing EPHX2 signal |
| GSE282122_paired_post_pre | IBD_antiTNF_response | mean_delta | 0.1873034198536875 | 0.2619943988350041 | 1.0 | False | no nominal responder-normalizing EPHX2 signal |
| GSE282122_integrated_rank | IBD_antiTNF_response | raw_delta_remission_minus_non | -0.5966159655304609 | 0.1201218220122457 | 1.0 | False | no nominal responder-normalizing EPHX2 signal |
| wave57_geneformer_intervention | foundation_model_perturbation | wave57_model_priority_score |  |  |  | False | EPHX2 absent or below token/support threshold |
| wave69d_geneformer_remission_centroid | foundation_model_perturbation | geneformer_remission_priority_score |  |  |  | False | EPHX2 absent or below token/support threshold |
| GSE198520_RA_synovium_antiTNF | RA_antiTNF_response | good_vs_other_delta | 0.2371687066622362 | 0.35342325461420776 | 0.35342325461420776 | False | no nominal responder-normalizing RA EPHX2 signal |

## Module Specificity

| module | tested_context_count | positive_support_context_count | negative_or_normalization_support_context_count | best_positive_effect | best_negative_effect | best_positive_context | best_negative_or_response_context |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ephx2_epoxide_hydrolase_axis | 23 | 1 | 2 | 0.757858352195102 | -0.9748279710983057 | broad_h5ad\|case_minus_control\|effect=0.758\|p=0.00246 | broad_h5ad\|case_minus_control\|effect=-0.975\|p=0.0119 |
| generic_lipid_handling | 23 | 3 | 1 | 0.7452267061104367 | -0.6529068857948515 | broad_h5ad\|case_minus_control\|effect=0.745\|p=0.00019 | GSE282122_IBD_antiTNF\|remission_delta_minus_nonremission_delta\|effect=-0.653\|p=1.11e-05 |
| inflammatory_nfkb_tnf | 23 | 12 | 1 | 1.695446920518662 | -0.7657644559210937 | broad_h5ad\|case_minus_control\|effect=1.7\|p=7.91e-07 | GSE282122_IBD_antiTNF\|remission_delta_minus_nonremission_delta\|effect=-0.766\|p=0.0174 |
| lysosomal_apc | 23 | 8 | 0 | 1.1821549849933812 | -0.4434268379190338 | broad_h5ad\|case_minus_control\|effect=1.18\|p=0.00151 |  |
| oxylipin_enzyme_adjacent | 23 | 4 | 1 | 0.706159983720455 | -0.45961051527644503 | broad_h5ad\|case_minus_control\|effect=0.706\|p=0.00916 | broad_h5ad\|case_minus_control\|effect=-0.46\|p=0.00154 |

## Specificity Margins

| context | response_mode | ephx2_axis_effect | ephx2_axis_p | generic_lipid_effect | inflammatory_effect | lysosomal_apc_effect | specificity_margin | specificity_pass |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| broad_h5ad\|ibd_crohn_epithelial\|Crohn disease\|colon epithelial\|tissue_resident | False | -0.07587328262519401 | 0.4638942998373802 | 0.7452267061104367 | 0.7781903299965292 | 0.8687770708012587 | -0.9446503534264526 | False |
| broad_h5ad\|t1d_acinar_cell\|type 1 diabetes mellitus\|pancreatic acinar cell\|tissue_resident | False | 0.01851346133642573 | 0.38057639901792895 | 0.42257838527617847 | 1.3782933965104458 | 0.7043662911895336 | -1.35977993517402 | False |
| GSE282122_IBD_antiTNF\|remission_delta_minus_nonremission_delta\|Mono_macro | True | -0.11802086112031958 | 0.08191138211377504 | -0.32612188602829645 | -0.7657644559210937 | -0.03323425822146913 | -0.647743594800774 | False |
| GSE282122_IBD_antiTNF\|remission_delta_minus_nonremission_delta\|DC | True | 0.042500891347213084 | 0.7312279288141001 | -0.6529068857948515 | -0.4489268128185425 | -0.3247927973775549 | -0.6954077771420646 | False |
| GSE282122_IBD_antiTNF\|paired_post_minus_pre_all\|Mono_macro | True | 0.1554327688448199 | 0.01608151107643492 | -0.11282328827334558 | 0.1126488112108844 | 0.06667686650807893 | -0.26825605711816547 | False |
| GSE282122_IBD_antiTNF\|paired_post_minus_pre_all\|DC | True | 0.1351955720850482 | 0.036872037471950614 | -0.08682132279259883 | -0.21189723992251364 | 0.01898866473782367 | -0.3470928120075618 | False |
| GSE111972_MS_white_matter\|MS_case_minus_control | False | 0.1951260267248538 | 0.6210451934657115 | 0.36821157698900164 | 0.19873257216957416 | 0.24249862200951403 | -0.17308555026414785 | False |
| broad_h5ad\|t1d_stellate_cell\|type 1 diabetes mellitus\|pancreatic stellate cell\|tissue_resident | False | 0.2434895582714538 | 0.7609821588314225 | -0.07651523133024495 | 1.3516063060732944 | 0.6200575232640595 | -1.1081167478018406 | False |
| broad_h5ad\|t1d_endothelial_cell\|type 1 diabetes mellitus\|pancreatic endothelial cell\|tissue_resident | False | 0.6139332695089481 | 0.1831073916214535 | 0.09809347646969603 | 1.2601076046498303 | 0.5993486527083839 | -0.6461743351408822 | False |
| broad_h5ad\|t1d_ductal_cell\|type 1 diabetes mellitus\|pancreatic ductal cell\|tissue_resident | False | 0.757858352195102 | 0.0024621671977672873 | 0.24126477953127506 | 1.272288048722874 | 0.5899866188518691 | -0.514429696527772 | False |
| broad_h5ad\|t1d_beta_cell\|type 1 diabetes mellitus\|pancreatic beta cell\|tissue_resident | False | 0.25747951064321584 | 0.5362476162064462 | 0.2657150221458953 | 1.3701958697703813 | 1.1821549849933812 | -1.1127163591271656 | False |
| broad_h5ad\|sjogren_gland_stromal\|Sjogren syndrome\|salivary gland stromal/endothelial\|tissue_resident | False | -0.15256605494862216 | 0.2717006055453951 | -0.12719432185172316 | 0.2239090398646971 | 0.003953070333233466 | -0.37647509481331926 | False |

_Showing 12 of 23 rows._

## Generic Lipid-Class Context

| metabolite_class | n_diseases_tested | n_supportive_diseases_p10_abs_g35 | supportive_diseases | n_normalizing_treatment_or_improvement_hits | gate_call |
| --- | --- | --- | --- | --- | --- |
| phosphatidylcholine | 6 | 3 | AS,Crohn,UC | 2 | DESCRIPTIVE_OR_WEAK |
| ceramide | 6 | 3 | MS_model,RA,SLE | 1 | DESCRIPTIVE_OR_WEAK |
| glycosphingolipid | 5 | 3 | MS_model,RA,UC | 0 | DESCRIPTIVE_OR_WEAK |
| lysophosphatidylcholine | 6 | 2 | MS_model,RA | 1 | DESCRIPTIVE_OR_WEAK |
| phosphatidylglycerol | 3 | 2 | MS_model,SLE | 1 | DESCRIPTIVE_OR_WEAK |
| eicosanoid_oxylipin | 5 | 2 | MS_model,RA | 0 | DESCRIPTIVE_OR_WEAK |
| acylcarnitine | 4 | 2 | Crohn,UC | 0 | DESCRIPTIVE_OR_WEAK |
| phosphatidylethanolamine | 6 | 2 | Crohn,MS_model | 0 | DESCRIPTIVE_OR_WEAK |
| fatty_acid | 6 | 1 | RA | 1 | DESCRIPTIVE_OR_WEAK |
| sterol | 4 | 1 | MS_model | 1 | DESCRIPTIVE_OR_WEAK |
| phosphatidylserine | 4 | 1 | MS_model | 1 | DESCRIPTIVE_OR_WEAK |
| sphingomyelin | 6 | 1 | MS_model | 0 | DESCRIPTIVE_OR_WEAK |

_Showing 12 of 17 rows._

## Interpretation

- The audit separates direct EpFA/diol/EET/DHET evidence from adjacent HETE/oxo oxylipins and broad linoleate/arachidonate substrate pools.
- Broad lipid and inflammatory modules are carried as explicit comparators; they are not treated as EPHX2 evidence.
- The decisive promotion blocker is target-level `EPHX2` convergence: available expression/genetics/response data do not independently support EPHX2 as the causal target.
