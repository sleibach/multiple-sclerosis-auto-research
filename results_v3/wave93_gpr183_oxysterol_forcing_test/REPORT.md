# Wave93 GPR183/EBI2 Oxysterol-Niche Forcing Test

Question: can a druggable upstream oxysterol-guided niche controller rescue the lipid-lysosomal myeloid module after direct lipid-state genes failed?

Analysis call: `NO_GO_GPR183_NO_MS_RECEPTOR_OR_LIGAND_ANCHOR`.

## Integrated Decision

| candidate | wave93_call | gate_count | total_gates | hard_failures | ms_gpr183_positive | ms_ligand_module_positive | coherent_context_count | coherent_disease_count | gpr183_genetic_disease_count_max | response_support_systems | ibd_gpr183_direction | ibd_gpr183_min_p | ibd_gpr183_weighted_g | ra_gpr183_direction | ra_gpr183_min_p | ra_gpr183_weighted_g | psoriasis_ada_gpr183_support | chembl_human_activity | direct_ms_or_eae_prior_art | direct_prior_pmids |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GPR183_EBI2_oxysterol_niche | NO_GO_GPR183_NO_MS_RECEPTOR_OR_LIGAND_ANCHOR | 1 | 7 | MS_GPR183_receptor_anchor_positive;MS_ligand_module_positive;cross_disease_coherent_ligand_receptor_response_contexts_ge3;target_resolved_genetics_ge4_autoimmune_diseases;gene_level_response_support_ge2_systems;chembl_human_target_activity_present | False | False | 0 | 0 | 2 | 1 | nonresponse_high | 0.0008986 | -1.108 | responder_high_or_null | 0.02785 | 0.7061 | False | False | False |  |

## Gate Audit

| gate | pass | value |
| --- | --- | --- |
| MS_GPR183_receptor_anchor_positive | False | -0.1364089401905186 |
| MS_ligand_module_positive | False | 0.0710988186652243 |
| cross_disease_coherent_ligand_receptor_response_contexts_ge3 | False | 0 |
| target_resolved_genetics_ge4_autoimmune_diseases | False | 2 |
| gene_level_response_support_ge2_systems | False | 1 |
| chembl_human_target_activity_present | False | False |
| no_direct_ms_or_eae_prior_art | True |  |

## MS Target-Gene Rows

| gene | mean_case | mean_control | delta_log2 | hedges_g | welch_t | p | fdr | ms_anchor_call |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CH25H | 11.68 | 11.5 | 0.1827 | 0.1301 | 0.3166 | 0.7553 | 0.9708 | NO_MS_WM_UP_SIGNAL |
| CYP27A1 | 10.77 | 9.994 | 0.7784 | 0.9108 | 2.222 | 0.0404 | 0.8574 | MS_WM_UP_NOMINAL_OR_TREND |
| CYP7B1 | 1.157 | 2.358 | -1.201 | -0.5231 | -1.261 | 0.2229 | 0.8994 | MS_WM_NOT_UP_NEGATIVE_DIRECTION |
| GPR183 | 13.59 | 13.73 | -0.1364 | -0.1849 | -0.4417 | 0.6637 | 0.9566 | MS_WM_NOT_UP_NEGATIVE_DIRECTION |
| HSD3B7 | 7.694 | 7.17 | 0.5238 | 0.5014 | 1.209 | 0.2417 | 0.9005 | NO_MS_WM_UP_SIGNAL |

## Broad h5ad Target-Gene Summary

| gene | tested_contexts | positive_contexts_p_lt_0_10 | negative_contexts_p_lt_0_10 | positive_disease_count | negative_disease_count | positive_diseases | negative_diseases | best_positive_context | best_negative_context |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CH25H | 13 | 1 | 1 | 1 | 1 | type 1 diabetes mellitus | psoriasis | t1d_stellate_cell\|type 1 diabetes mellitus\|pancreatic stellate cell\|delta=2.16\|p=0.0829 | psoriasis_skin_stromal\|psoriasis\|skin stromal\|delta=-0.673\|p=0.0882 |
| CYP27A1 | 17 | 2 | 3 | 1 | 2 | type 1 diabetes mellitus | Crohn disease;ulcerative colitis | t1d_endothelial_cell\|type 1 diabetes mellitus\|pancreatic endothelial cell\|delta=1.84\|p=0.0199 | ibd_uc_epithelial\|ulcerative colitis\|colon epithelial\|delta=-3.99\|p=0.000136 |
| CYP7B1 | 15 | 3 | 0 | 3 | 0 | Crohn disease;psoriasis;type 1 diabetes mellitus |  | t1d_endothelial_cell\|type 1 diabetes mellitus\|pancreatic endothelial cell\|delta=1.8\|p=0.0656 |  |
| GPR183 | 17 | 3 | 1 | 3 | 1 | Crohn disease;Sjogren syndrome;ulcerative colitis | psoriasis | ibd_crohn_epithelial\|Crohn disease\|colon epithelial\|delta=1.13\|p=0.0323 | psoriasis_skin_apc\|psoriasis\|skin APC\|delta=-1.25\|p=0.0496 |
| HSD3B7 | 17 | 3 | 1 | 2 | 1 | Crohn disease;type 1 diabetes mellitus | psoriasis | t1d_endothelial_cell\|type 1 diabetes mellitus\|pancreatic endothelial cell\|delta=1.74\|p=0.0733 | psoriasis_skin_stromal\|psoriasis\|skin stromal\|delta=-0.712\|p=0.00129 |

## IBD External Anti-TNF Gene-Level Meta

| system | gene | n_contexts | nonresponse_high_contexts | responder_high_contexts | nominal_nonresponse_contexts_p_lt_0_10 | weighted_mean_hedges_g_responder_minus_non | median_auc_high_expression_nonresponse | min_p |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IBD_external_antitnf | CCL17 | 4 | 2 | 2 | 0 | -0.04937 | 0.481 | 0.4102 |
| IBD_external_antitnf | CCL19 | 4 | 3 | 1 | 0 | -0.2598 | 0.5859 | 0.3182 |
| IBD_external_antitnf | CCL21 | 4 | 4 | 0 | 0 | -0.2278 | 0.5807 | 0.4492 |
| IBD_external_antitnf | CCL22 | 4 | 4 | 0 | 2 | -0.7515 | 0.7089 | 0.01115 |
| IBD_external_antitnf | CCR7 | 4 | 4 | 0 | 1 | -0.668 | 0.6888 | 0.06094 |
| IBD_external_antitnf | CD83 | 4 | 4 | 0 | 2 | -0.6847 | 0.6638 | 0.01499 |
| IBD_external_antitnf | CH25H | 4 | 4 | 0 | 1 | -0.368 | 0.5729 | 0.05744 |
| IBD_external_antitnf | CXCL13 | 4 | 4 | 0 | 1 | -0.7073 | 0.6724 | 0.007041 |
| IBD_external_antitnf | CXCR5 | 4 | 2 | 2 | 1 | -0.06822 | 0.5083 | 0.09898 |
| IBD_external_antitnf | CYP27A1 | 4 | 1 | 3 | 0 | 0.2645 | 0.4139 | 0.2079 |
| IBD_external_antitnf | CYP7B1 | 4 | 4 | 0 | 3 | -1.254 | 0.7971 | 0.002531 |
| IBD_external_antitnf | GPR183 | 4 | 4 | 0 | 2 | -1.108 | 0.7922 | 0.0008986 |
| IBD_external_antitnf | HSD3B7 | 4 | 1 | 3 | 0 | 0.1259 | 0.4375 | 0.4756 |
| IBD_external_antitnf | ITGAX | 4 | 4 | 0 | 1 | -0.4364 | 0.6515 | 0.09209 |
| IBD_external_antitnf | LAMP3 | 4 | 4 | 0 | 3 | -1.097 | 0.7589 | 0.005744 |
| IBD_external_antitnf | LTA | 4 | 3 | 1 | 1 | -0.2354 | 0.5946 | 0.09497 |
| IBD_external_antitnf | LTB | 4 | 2 | 2 | 0 | 0.001055 | 0.5164 | 0.202 |

## RA Baseline Anti-TNF Gene-Level Meta

| system | gene | n_contexts | nonresponse_high_contexts | responder_high_contexts | nominal_nonresponse_contexts_p_lt_0_10 | weighted_mean_hedges_g_responder_minus_non | median_auc_high_expression_nonresponse | min_p |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RA_baseline | CCL17 | 1 | 1 | 0 | 0 | -0.2526 | 0.567 | 0.4285 |
| RA_baseline | CCL19 | 1 | 1 | 0 | 0 | -0.2621 | 0.5893 | 0.3979 |
| RA_baseline | CCL21 | 1 | 0 | 1 | 0 | 0.614 | 0.3237 | 0.05286 |
| RA_baseline | CCL22 | 1 | 1 | 0 | 1 | -0.8112 | 0.7344 | 0.0212 |
| RA_baseline | CCR7 | 1 | 0 | 1 | 0 | 0.09307 | 0.4933 | 0.761 |
| RA_baseline | CD83 | 1 | 1 | 0 | 0 | -0.3026 | 0.5692 | 0.2582 |
| RA_baseline | CH25H | 1 | 1 | 0 | 1 | -0.6067 | 0.6429 | 0.06356 |
| RA_baseline | CXCL13 | 1 | 0 | 1 | 0 | 0.0747 | 0.4531 | 0.7707 |
| RA_baseline | CXCR5 | 1 | 1 | 0 | 0 | -0.1287 | 0.5335 | 0.7369 |
| RA_baseline | CYP27A1 | 1 | 1 | 0 | 1 | -0.6525 | 0.6562 | 0.02538 |
| RA_baseline | CYP7B1 | 1 | 1 | 0 | 0 | -0.3853 | 0.6161 | 0.3173 |
| RA_baseline | GPR183 | 1 | 0 | 1 | 0 | 0.7061 | 0.3371 | 0.02785 |
| RA_baseline | HSD3B7 | 1 | 0 | 1 | 0 | 0.5705 | 0.3683 | 0.1234 |
| RA_baseline | ITGAX | 1 | 1 | 0 | 0 | -0.3576 | 0.625 | 0.1908 |
| RA_baseline | LAMP3 | 1 | 1 | 0 | 1 | -0.9269 | 0.7857 | 0.002376 |

## Psoriasis Adalimumab Gene-Level Meta

| system | gene | n_contexts | nonresponse_high_contexts | responder_high_contexts | nominal_nonresponse_contexts_p_lt_0_10 | weighted_mean_hedges_g_responder_minus_non | median_auc_high_expression_nonresponse | min_p |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| psoriasis_ADA | CCL17 | 1 | 1 | 0 | 0 | -0.126 | 0.5778 | 0.8309 |
| psoriasis_ADA | CCL19 | 1 | 0 | 1 | 0 | 0.3689 | 0.4222 | 0.4067 |
| psoriasis_ADA | CCL21 | 1 | 1 | 0 | 0 | -0.2743 | 0.6 | 0.644 |
| psoriasis_ADA | CCL22 | 1 | 0 | 1 | 0 | 0.1972 | 0.5333 | 0.6711 |
| psoriasis_ADA | CCR7 | 1 | 0 | 1 | 0 | 0.1593 | 0.5111 | 0.7363 |
| psoriasis_ADA | CD83 | 1 | 0 | 1 | 0 | 0.3297 | 0.4222 | 0.5057 |
| psoriasis_ADA | CH25H | 1 | 0 | 1 | 0 | 0.02937 | 0.5556 | 0.9543 |
| psoriasis_ADA | CXCL13 | 1 | 1 | 0 | 0 | -0.5675 | 0.6 | 0.401 |
| psoriasis_ADA | CXCR5 | 1 | 0 | 1 | 0 | 0.009388 | 0.4444 | 0.9852 |
| psoriasis_ADA | CYP27A1 | 1 | 1 | 0 | 0 | -0.2014 | 0.5778 | 0.687 |
| psoriasis_ADA | CYP7B1 | 1 | 0 | 1 | 0 | 0.8119 | 0.2667 | 0.09351 |
| psoriasis_ADA | GPR183 | 1 | 1 | 0 | 0 | -0.06372 | 0.5556 | 0.8967 |
| psoriasis_ADA | HSD3B7 | 1 | 0 | 1 | 0 | 0.5902 | 0.3778 | 0.2473 |
| psoriasis_ADA | ITGAX | 1 | 1 | 0 | 0 | -0.332 | 0.6667 | 0.5084 |
| psoriasis_ADA | LAMP3 | 1 | 0 | 1 | 0 | 0.496 | 0.3556 | 0.2968 |
| psoriasis_ADA | LTA | 1 | 1 | 0 | 0 | -0.03972 | 0.5556 | 0.9401 |
| psoriasis_ADA | LTB | 1 | 0 | 1 | 0 | 0.257 | 0.4444 | 0.5515 |

## Target Resolution Rows

| source | gene | approved_name | wave55_score | wave62_score | wave62_call | n_diseases_genetic_ge_0_25 | diseases_genetic_ge_0_25 | strong_l2g_disease_count | strong_l2g_diseases | ms_wm_delta_log2 | ms_wm_p | druggable_activity_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| wave55_external_genetics | CYP7B1 | cytochrome P450 family 7 subfamily B member 1 | 8 |  |  | 1 | MS |  |  | -1.201 | 0.2229 |  |
| wave55_external_genetics | GPR183 | G protein-coupled receptor 183 | 8 |  |  | 2 | Psoriasis;SLE |  |  | -0.1364 | 0.6637 |  |
| wave55_external_genetics | CH25H | cholesterol 25-hydroxylase | 4 |  |  | 1 | UC |  |  | 0.1827 | 0.7553 |  |
| wave55_external_genetics | HSD3B7 | hydroxy-delta-5-steroid dehydrogenase, 3 beta- and steroid delta-isomerase 7 | 3 |  |  | 1 | Psoriasis |  |  | 0.5238 | 0.2417 |  |
| wave55_external_genetics | CYP27A1 | cytochrome P450 family 27 subfamily A member 1 | 2 |  |  | 0 |  |  |  | 0.7784 | 0.0404 |  |
| wave62_target_resolution | CH25H | cholesterol 25-hydroxylase | 4 | 1.318 | NO_GO_WAVE62_TARGET_RESOLUTION |  |  | 1 | UC | 0.1827 | 0.7553 | 0 |
| wave62_target_resolution | HSD3B7 | hydroxy-delta-5-steroid dehydrogenase, 3 beta- and steroid delta-isomerase 7 | 3 | 1.317 | NO_GO_WAVE62_TARGET_RESOLUTION |  |  | 0 |  | 0.5238 | 0.2417 | 0 |
| wave62_target_resolution | GPR183 | G protein-coupled receptor 183 | 8 | 1.241 | NO_GO_WAVE62_TARGET_RESOLUTION |  |  | 1 | Psoriasis | -0.1364 | 0.6637 | 0 |

## ChEMBL Target Query

| gene | query_url | chembl_query_error | chembl_hit_count |
| --- | --- | --- | --- |
| GPR183 | https://www.ebi.ac.uk/chembl/api/data/target/search.json?q=GPR183&limit=10 | URLError: <urlopen error [Errno 8] nodename nor servname provided, or not known> | 0 |
| CH25H | https://www.ebi.ac.uk/chembl/api/data/target/search.json?q=CH25H&limit=10 | URLError: <urlopen error [Errno 8] nodename nor servname provided, or not known> | 0 |
| CYP7B1 | https://www.ebi.ac.uk/chembl/api/data/target/search.json?q=CYP7B1&limit=10 | URLError: <urlopen error [Errno 8] nodename nor servname provided, or not known> | 0 |
| HSD3B7 | https://www.ebi.ac.uk/chembl/api/data/target/search.json?q=HSD3B7&limit=10 | URLError: <urlopen error [Errno 8] nodename nor servname provided, or not known> | 0 |
| CYP27A1 | https://www.ebi.ac.uk/chembl/api/data/target/search.json?q=CYP27A1&limit=10 | URLError: <urlopen error [Errno 8] nodename nor servname provided, or not known> | 0 |

## PubMed Closest Prior Art

_No rows._

## Guardrails

- Promotion requires receptor/ligand coherence, not only response genes.
- `EBI3` nomenclature is irrelevant here; EBI2 is `GPR183`.
- A response association is not treated as an intervention target unless MS anchoring and target-resolved genetics/druggability also survive.
- ChEMBL/PubMed/ClinicalTrials API failures, if any, are recorded in the corresponding TSVs rather than silently ignored.
