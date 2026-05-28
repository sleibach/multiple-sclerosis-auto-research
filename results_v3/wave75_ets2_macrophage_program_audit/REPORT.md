# Wave75 ETS2 Inflammatory Macrophage Program Audit

## Question

Does local V3 evidence support `ETS2` as a promotable cross-autoimmune inflammatory macrophage intervention point rather than a generic/published inflammatory macrophage program?

## Verdict

PARK_IBD_MYELOID_PROGRAM_NOT_PROMOTABLE

## Integrated Decision

| candidate | wave75_call | gate_count | broad_direct_ets2_support | broad_program_support | specificity_vs_generic_modules | ms_support | ibd_response_support | ra_response_support | target_resolved_genetics | foundation_model_support | broad_direct_positive_disease_count | broad_program_positive_disease_count | specificity_pass_context_count | target_support_source_count | decision_blockers |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ETS2_inflammatory_macrophage_program | PARK_IBD_MYELOID_PROGRAM_NOT_PROMOTABLE | 2 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 3 | 1 | 1 | ETS2-labeled program does not beat generic inflammatory/APC comparators; no MS white-matter ETS2/program support; Wave62 target-resolution remains no-go; no replicated treatment-response support; no Geneformer/foundation reopener |

## Direct ETS2 Evidence

| source | metric | effect | p | fdr | support | details |
| --- | --- | --- | --- | --- | --- | --- |
| broad_h5ad_gene_summary | cross_disease_expression | 1.972 | 0.0002169 | 0.05209 | True | positive_diseases=Crohn disease;ulcerative colitis; negative_diseases=; fdr10_contexts=1 |
| GSE111972_MS_white_matter | MS_case_minus_control_expression | -0.06076 | 0.8649 | 0.9802 | False | direct ETS2 in MS white matter signature |
| wave62_opentargets_target_resolution | target_resolved_genetics | 1.229 |  |  | False | call=NO_GO_WAVE62_TARGET_RESOLUTION; strong_l2g=; relevant_qtl=AS;UC; ms_l2g=0.0 |
| wave57_geneformer_intervention | foundation_model_perturbation |  |  |  | False | ETS2 absent from output or below token/support threshold |
| wave69d_geneformer_remission_centroid | foundation_model_perturbation |  |  |  | False | ETS2 absent from output or below token/support threshold |
| GSE282122_raw_DC | IBD_antiTNF_remission_delta | -0.1139 | 0.5205 | 1 | False | negative effect means remission moves down relative to non-remission |
| GSE282122_raw_Mono_macro | IBD_antiTNF_remission_delta | -0.6527 | 0.06486 | 0.9671 | False | negative effect means remission moves down relative to non-remission |
| GSE282122_paired_DC | IBD_antiTNF_paired_post_minus_pre | -0.01836 | 0.8147 | 1 | False | negative effect means treatment pharmacodynamically lowers ETS2 |
| GSE282122_paired_Mono_macro | IBD_antiTNF_paired_post_minus_pre | 0.03031 | 0.8278 | 1 | False | negative effect means treatment pharmacodynamically lowers ETS2 |
| GSE282122_integrated_ | IBD_integrated_gene_rank | 1.885 | 0.9671 |  | False | cell_state=Mono_macro; call=DESCRIPTIVE_GENE_SIGNAL; paired_fdr=1.0 |
| GSE282122_integrated_ | IBD_integrated_gene_rank | 0.987 | 1 |  | False | cell_state=DC; call=DESCRIPTIVE_GENE_SIGNAL; paired_fdr=1.0 |

## Module Definitions

| module | class | genes | n_genes |
| --- | --- | --- | --- |
| ets2_direct | candidate | ETS2 | 1 |
| ets2_macrophage_program | candidate | ETS2;IL1B;IL6;TNF;PTGS2;CCL2;CCL3;CCL4;CXCL8;TNFAIP3;NFKBIA;ICAM1;MMP9 | 13 |
| ap1_ets_immediate_early | candidate | ETS2;FOS;FOSB;JUN;JUNB;JUND;EGR1;DUSP1;DUSP2 | 9 |
| generic_nfkb_tnf | specificity_comparator | TNF;IL6;CXCL8;NFKBIA;TNFAIP3;CCL2;CCL3;CCL4;IL1B | 9 |
| interferon_apc | specificity_comparator | STAT1;IRF1;CXCL10;IFI30;HLA-DRA;HLA-DRB1;CD74;GBP1;ISG15 | 9 |
| lysosome_apc | specificity_comparator | IFI30;CTSD;CTSB;CTSS;CTSL;LAMP1;LAMP2;TPP1;CD74;HLA-DRA | 10 |

## Broad h5ad Module Summary

| module | module_class | tested_context_count | positive_context_count | negative_context_count | positive_fdr10_context_count | positive_disease_count | negative_disease_count | positive_diseases | negative_diseases | best_positive_context |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ets2_direct | candidate | 17 | 3 | 0 | 3 | 2 | 0 | Crohn disease;ulcerative colitis |  | ibd_uc_myeloid\|ulcerative colitis\|colon myeloid\|effect=1.97\|p=0.000217\|fdr=0.00079 |
| ets2_macrophage_program | candidate | 17 | 11 | 3 | 11 | 3 | 1 | Crohn disease;type 1 diabetes mellitus;ulcerative colitis | psoriasis | ibd_uc_myeloid\|ulcerative colitis\|colon myeloid\|effect=1.42\|p=2.61e-07\|fdr=3.21e-06 |
| ap1_ets_immediate_early | candidate | 17 | 0 | 5 | 0 | 0 | 2 |  | psoriasis;ulcerative colitis |  |
| generic_nfkb_tnf | specificity_comparator | 17 | 11 | 1 | 11 | 3 | 1 | Crohn disease;type 1 diabetes mellitus;ulcerative colitis | psoriasis | ibd_uc_myeloid\|ulcerative colitis\|colon myeloid\|effect=1.64\|p=3.42e-05\|fdr=0.000184 |
| interferon_apc | specificity_comparator | 17 | 15 | 0 | 15 | 5 | 0 | Crohn disease;Sjogren syndrome;psoriasis;type 1 diabetes mellitus;ulcerative colitis |  | t1d_beta_cell\|type 1 diabetes mellitus\|pancreatic beta cell\|effect=1.82\|p=0.00013\|fdr=0.000552 |
| lysosome_apc | specificity_comparator | 17 | 6 | 0 | 6 | 2 | 0 | psoriasis;type 1 diabetes mellitus |  | t1d_beta_cell\|type 1 diabetes mellitus\|pancreatic beta cell\|effect=1.1\|p=0.00237\|fdr=0.00691 |

## Specificity Versus Generic Modules

| analysis | disease_name | compartment | role | candidate_module | candidate_effect | max_generic_comparator_effect | specificity_margin | specificity_pass |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ibd_uc_myeloid | ulcerative colitis | colon myeloid | myeloid_apc | ets2_direct | 1.972 | 1.641 | 0.3317 | True |
| sjogren_gland_stromal | Sjogren syndrome | salivary gland stromal/endothelial | tissue_resident | ets2_macrophage_program | 0.2345 | 0.2626 | -0.02807 | False |
| sjogren_gland_stromal | Sjogren syndrome | salivary gland stromal/endothelial | tissue_resident | ap1_ets_immediate_early | 0.1961 | 0.2626 | -0.06647 | False |
| ibd_uc_stromal | ulcerative colitis | colon stromal | tissue_resident | ets2_macrophage_program | 0.7899 | 0.8599 | -0.07001 | False |
| ibd_crohn_myeloid | Crohn disease | colon myeloid | myeloid_apc | ets2_direct | 1.519 | 1.631 | -0.112 | False |
| t1d_ductal_cell | type 1 diabetes mellitus | pancreatic ductal cell | tissue_resident | ets2_macrophage_program | 1.227 | 1.351 | -0.1244 | False |
| t1d_stellate_cell | type 1 diabetes mellitus | pancreatic stellate cell | tissue_resident | ets2_macrophage_program | 1.332 | 1.471 | -0.1391 | False |
| t1d_acinar_cell | type 1 diabetes mellitus | pancreatic acinar cell | tissue_resident | ets2_macrophage_program | 1.297 | 1.452 | -0.1549 | False |
| ibd_crohn_stromal | Crohn disease | colon stromal | tissue_resident | ets2_macrophage_program | 1.002 | 1.204 | -0.2025 | False |
| ibd_uc_myeloid | ulcerative colitis | colon myeloid | myeloid_apc | ets2_macrophage_program | 1.416 | 1.641 | -0.2246 | False |
| ibd_crohn_myeloid | Crohn disease | colon myeloid | myeloid_apc | ets2_macrophage_program | 1.404 | 1.631 | -0.2266 | False |
| t1d_endothelial_cell | type 1 diabetes mellitus | pancreatic endothelial cell | tissue_resident | ets2_macrophage_program | 1.244 | 1.514 | -0.2699 | False |
| sjogren_gland_apc | Sjogren syndrome | salivary gland APC | myeloid_apc | ets2_macrophage_program | 0.2137 | 0.5244 | -0.3107 | False |
| sjogren_gland_apc | Sjogren syndrome | salivary gland APC | myeloid_apc | ap1_ets_immediate_early | 0.09335 | 0.5244 | -0.431 | False |
| sjogren_gland_stromal | Sjogren syndrome | salivary gland stromal/endothelial | tissue_resident | ets2_direct | -0.2412 | 0.2626 | -0.5038 | False |
| ibd_uc_stromal | ulcerative colitis | colon stromal | tissue_resident | ets2_direct | 0.3229 | 0.8599 | -0.537 | False |
| sjogren_gland_epithelial | Sjogren syndrome | salivary gland epithelial | tissue_resident | ets2_macrophage_program | 0.1828 | 0.7609 | -0.5781 | False |
| t1d_beta_cell | type 1 diabetes mellitus | pancreatic beta cell | tissue_resident | ets2_macrophage_program | 1.116 | 1.821 | -0.7055 | False |
| ibd_uc_epithelial | ulcerative colitis | colon epithelial | tissue_resident | ets2_macrophage_program | 0.7566 | 1.521 | -0.7645 | False |
| ibd_crohn_epithelial | Crohn disease | colon epithelial | tissue_resident | ets2_macrophage_program | 0.6777 | 1.448 | -0.7699 | False |

_Showing 20 of 51 rows._

## MS White-Matter Module Tests

| dataset | module | n_genes_present | genes_present | mean_effect | median_effect | combined_z | combined_p | fdr | support_call |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GSE111972_MS_white_matter | ets2_direct | 1 | ETS2 | -0.06076 | -0.06076 | -0.1701 | 0.8649 | 0.8943 | NO_MS_MODULE_SUPPORT |
| GSE111972_MS_white_matter | ets2_macrophage_program | 13 | CCL2;CCL3;CCL4;CXCL8;ETS2;ICAM1;IL1B;IL6;MMP9;NFKBIA;PTGS2;TNF;TNFAIP3 | -0.0145 | -0.05822 | -0.1329 | 0.8943 | 0.8943 | NO_MS_MODULE_SUPPORT |
| GSE111972_MS_white_matter | ap1_ets_immediate_early | 9 | DUSP1;DUSP2;EGR1;ETS2;FOS;FOSB;JUN;JUNB;JUND | -0.09755 | -0.09494 | -0.7862 | 0.4318 | 0.8635 | NO_MS_MODULE_SUPPORT |
| GSE111972_MS_white_matter | generic_nfkb_tnf | 9 | CCL2;CCL3;CCL4;CXCL8;IL1B;IL6;NFKBIA;TNF;TNFAIP3 | 0.02978 | 0.04905 | 0.3269 | 0.7437 | 0.8943 | NO_MS_MODULE_SUPPORT |
| GSE111972_MS_white_matter | interferon_apc | 9 | CD74;CXCL10;GBP1;HLA-DRA;HLA-DRB1;IFI30;IRF1;ISG15;STAT1 | 0.3602 | 0.2891 | 3.41 | 0.0006492 | 0.001948 | MS_NOMINAL_POSITIVE |
| GSE111972_MS_white_matter | lysosome_apc | 10 | CD74;CTSB;CTSD;CTSL;CTSS;HLA-DRA;IFI30;LAMP1;LAMP2;TPP1 | 0.2121 | 0.2 | 3.635 | 0.0002782 | 0.001669 | NO_MS_MODULE_SUPPORT |

## IBD GSE282122 Anti-TNF Module Tests

| dataset | test | cell_state | module | n_genes_present | genes_present | mean_effect | median_effect | combined_z | combined_p | expected_direction_support | fdr |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GSE282122 | paired_post_minus_pre_all | Mono_macro | ap1_ets_immediate_early | 9 | DUSP1;DUSP2;EGR1;ETS2;FOS;FOSB;JUN;JUNB;JUND | 0.224 | 0.1379 | 4.336 | 1.45e-05 | False | 0.0003479 |
| GSE282122 | paired_post_minus_pre_all | Mono_macro | ets2_macrophage_program | 13 | CCL2;CCL3;CCL4;CXCL8;ETS2;ICAM1;IL1B;IL6;MMP9;NFKBIA;PTGS2;TNF;TNFAIP3 | 0.1328 | 0.2385 | 2.812 | 0.004925 | False | 0.0394 |
| GSE282122 | paired_post_minus_pre_all | Mono_macro | generic_nfkb_tnf | 9 | CCL2;CCL3;CCL4;CXCL8;IL1B;IL6;NFKBIA;TNF;TNFAIP3 | 0.2174 | 0.2385 | 2.908 | 0.00364 | False | 0.0394 |
| GSE282122 | remission_delta_difference | Mono_macro | ap1_ets_immediate_early | 9 | DUSP1;DUSP2;EGR1;ETS2;FOS;FOSB;JUN;JUNB;JUND | 0.1994 | 0.3033 | 2.004 | 0.0451 | False | 0.2165 |
| GSE282122 | paired_post_minus_pre_all | Mono_macro | lysosome_apc | 10 | CD74;CTSB;CTSD;CTSL;CTSS;HLA-DRA;IFI30;LAMP1;LAMP2;TPP1 | 0.05919 | 0.04615 | 2.053 | 0.04007 | False | 0.2165 |
| GSE282122 | remission_delta_difference | Mono_macro | ets2_direct | 1 | ETS2 | -0.6527 | -0.6527 | -1.846 | 0.06486 | False | 0.2594 |
| GSE282122 | remission_delta_difference | DC | lysosome_apc | 10 | CD74;CTSB;CTSD;CTSL;CTSS;HLA-DRA;IFI30;LAMP1;LAMP2;TPP1 | -0.3887 | -0.4097 | -1.675 | 0.09385 | False | 0.3167 |
| GSE282122 | paired_post_minus_pre_all | DC | lysosome_apc | 10 | CD74;CTSB;CTSD;CTSL;CTSS;HLA-DRA;IFI30;LAMP1;LAMP2;TPP1 | 0.009804 | 0.02231 | 1.618 | 0.1056 | False | 0.3167 |
| GSE282122 | remission_delta_difference | DC | ap1_ets_immediate_early | 9 | DUSP1;DUSP2;EGR1;ETS2;FOS;FOSB;JUN;JUNB;JUND | 0.1207 | 0.08158 | 1.344 | 0.1789 | False | 0.4772 |
| GSE282122 | paired_post_minus_pre_all | DC | interferon_apc | 9 | CD74;CXCL10;GBP1;HLA-DRA;HLA-DRB1;IFI30;IRF1;ISG15;STAT1 | -0.1153 | -0.01123 | 1.24 | 0.2151 | False | 0.5161 |
| GSE282122 | remission_delta_difference | Mono_macro | ets2_macrophage_program | 13 | CCL2;CCL3;CCL4;CXCL8;ETS2;ICAM1;IL1B;IL6;MMP9;NFKBIA;PTGS2;TNF;TNFAIP3 | -0.2623 | -0.2243 | -1.108 | 0.268 | False | 0.5556 |
| GSE282122 | remission_delta_difference | Mono_macro | generic_nfkb_tnf | 9 | CCL2;CCL3;CCL4;CXCL8;IL1B;IL6;NFKBIA;TNF;TNFAIP3 | -0.3322 | -0.2435 | -1.085 | 0.2778 | False | 0.5556 |
| GSE282122 | paired_post_minus_pre_all | Mono_macro | interferon_apc | 9 | CD74;CXCL10;GBP1;HLA-DRA;HLA-DRB1;IFI30;IRF1;ISG15;STAT1 | -0.06416 | 0.02481 | 0.9722 | 0.331 | False | 0.611 |
| GSE282122 | remission_delta_difference | DC | generic_nfkb_tnf | 9 | CCL2;CCL3;CCL4;CXCL8;IL1B;IL6;NFKBIA;TNF;TNFAIP3 | -0.1379 | -0.1554 | -0.763 | 0.4455 | False | 0.7637 |
| GSE282122 | remission_delta_difference | Mono_macro | lysosome_apc | 10 | CD74;CTSB;CTSD;CTSL;CTSS;HLA-DRA;IFI30;LAMP1;LAMP2;TPP1 | -0.09902 | -0.1046 | -0.7024 | 0.4824 | False | 0.7719 |
| GSE282122 | remission_delta_difference | DC | ets2_direct | 1 | ETS2 | -0.1139 | -0.1139 | -0.6425 | 0.5205 | False | 0.7808 |
| GSE282122 | remission_delta_difference | DC | ets2_macrophage_program | 13 | CCL2;CCL3;CCL4;CXCL8;ETS2;ICAM1;IL1B;IL6;MMP9;NFKBIA;PTGS2;TNF;TNFAIP3 | -0.05923 | -0.1301 | -0.5442 | 0.5863 | False | 0.8277 |
| GSE282122 | remission_delta_difference | DC | interferon_apc | 9 | CD74;CXCL10;GBP1;HLA-DRA;HLA-DRB1;IFI30;IRF1;ISG15;STAT1 | -0.6222 | -0.2649 | -0.4626 | 0.6437 | False | 0.8582 |
| GSE282122 | remission_delta_difference | Mono_macro | interferon_apc | 9 | CD74;CXCL10;GBP1;HLA-DRA;HLA-DRB1;IFI30;IRF1;ISG15;STAT1 | -0.7606 | -0.7641 | -0.1799 | 0.8572 | False | 0.9104 |
| GSE282122 | paired_post_minus_pre_all | DC | ets2_direct | 1 | ETS2 | -0.01836 | -0.01836 | -0.2344 | 0.8147 | False | 0.9104 |

_Showing 20 of 24 rows._

## RA GSE198520 Anti-TNF Module Tests

| dataset | module | n_patients | mean_post_minus_pre | paired_t | paired_p | good_vs_other_delta | good_vs_other_p | modgood_vs_none_delta | modgood_vs_none_p | expected_direction_support | paired_fdr | good_vs_other_fdr | modgood_vs_none_fdr |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GSE198520_RA_synovium_antiTNF | ap1_ets_immediate_early | 46 | -0.3409 | -2.586 | 0.01302 | -0.2381 | 0.3808 | -0.5072 | 0.03677 | False | 0.03763 | 0.3808 | 0.05515 |
| GSE198520_RA_synovium_antiTNF | ets2_direct | 46 | 0.09118 | 0.96 | 0.3422 | -0.2417 | 0.2187 | -0.104 | 0.5856 | False | 0.3422 | 0.2624 | 0.5856 |
| GSE198520_RA_synovium_antiTNF | ets2_macrophage_program | 46 | -0.1234 | -2.381 | 0.02158 | -0.1982 | 0.09346 | -0.1511 | 0.09713 | False | 0.03763 | 0.1869 | 0.1166 |
| GSE198520_RA_synovium_antiTNF | generic_nfkb_tnf | 46 | -0.113 | -2.142 | 0.03765 | -0.2187 | 0.06862 | -0.2487 | 0.005936 | False | 0.04518 | 0.1869 | 0.03527 |
| GSE198520_RA_synovium_antiTNF | interferon_apc | 46 | -0.4053 | -2.952 | 0.005006 | -0.5531 | 0.06728 | -0.6117 | 0.01176 | False | 0.03004 | 0.1869 | 0.03527 |
| GSE198520_RA_synovium_antiTNF | lysosome_apc | 46 | -0.4054 | -2.317 | 0.02509 | -0.4595 | 0.2175 | -0.7561 | 0.02413 | False | 0.03763 | 0.2624 | 0.04826 |

## Interpretation

- ETS2 direct expression is strongest in IBD myeloid contexts, especially UC and Crohn myeloid compartments.
- The ETS2-labeled macrophage program is intentionally compared against generic NF-kB/TNF, IFN/APC, and lysosomal/APC modules; specificity failure blocks promotion.
- Direct ETS2 modulation remains a transcription-factor modality problem even before prior-art review.
