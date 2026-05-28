# Wave87 Inflammatory Anti-TNF Nonresponse Circuit Audit

Question: after the residual lysosomal/APC response score failed external validation, can the Wave86 generic inflammatory nonresponse genes yield a V3-grade cross-autoimmune target or central node?

Decision: `NO_REOPEN_INFLAMMATORY_ANTITNF_NONRESPONSE_CIRCUIT_AS_V3_TARGET`.

## Candidate Rank

| gene | modules | wave86_call | central_node_score | wave87_call | prior_or_route_blocker | nonresponse_high_contexts | nominal_nonresponse_contexts_p_lt_0_05 | fdr10_nonresponse_contexts | median_auc_high_score_nonresponse | direct_h5ad_positive_p05_disease_count | direct_h5ad_positive_p05_diseases | direct_h5ad_negative_p05_disease_count | ms_wm_support | n_diseases_genetic_ge_0_25 | diseases_genetic_ge_0_25 | wave62_call | geneformer_strong_context_count | geneformer_support_contexts |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TREM1 | inflammatory_nfkb | GENE_LEVEL_ANTITNF_NONRESPONSE_ANCHOR | 19 | PARK_ANTI_TNF_ANCHOR_BUT_NOT_BROAD_CROSS_DISEASE | PARK_RECEPTOR_ROUTE_BUT_NO_LOCAL_MS_OR_GENETIC_ANCHOR | 4 | 3 | 3 | 0.8826 | 2 | Crohn disease;ulcerative colitis | 0 | MS_WM_NULL_OR_WEAK | 0 |  |  | 0 |  |
| CD44 | mif_cd74_receptor_state | GENE_LEVEL_ANTITNF_NONRESPONSE_ANCHOR | 16.5 | NO_GO_PRIOR_ROUTE_OR_DRUGGABILITY_BLOCKED | BLOCKED_ADHESION_MATRIX_PRIOR_ART_AND_BROAD_BIOLOGY | 4 | 3 | 3 | 0.7995 | 2 | Crohn disease;ulcerative colitis | 0 | MS_WM_POSITIVE_NOMINAL | 3 | AITD;SLE;T1D | NO_GO_WAVE62_TARGET_RESOLUTION | 0 |  |
| CXCL8 | inflammatory_nfkb | GENE_LEVEL_ANTITNF_NONRESPONSE_ANCHOR | 14 | NO_GO_PRIOR_ROUTE_OR_DRUGGABILITY_BLOCKED | BLOCKED_GENERIC_NEUTROPHIL_CHEMOKINE_LOW_MS_ANCHOR | 4 | 3 | 3 | 0.8849 | 2 | type 1 diabetes mellitus;ulcerative colitis | 0 | MS_WM_NULL_OR_WEAK | 0 |  |  | 1 | IBD_myeloid |
| IL1B | inflammatory_nfkb | GENE_LEVEL_ANTITNF_NONRESPONSE_ANCHOR | 13 | NO_GO_PRIOR_ROUTE_OR_DRUGGABILITY_BLOCKED | BLOCKED_GENERIC_IL1_INFLAMMATION_AND_EXISTING_IL1_BLOCKADE | 4 | 3 | 3 | 0.8974 | 2 | Crohn disease;ulcerative colitis | 0 | MS_WM_NULL_OR_WEAK | 0 |  |  | 0 |  |
| CCL4 | inflammatory_nfkb | GENE_LEVEL_ANTITNF_NONRESPONSE_ANCHOR | 12 | NO_GO_PRIOR_ROUTE_OR_DRUGGABILITY_BLOCKED | BLOCKED_BROAD_CHEMOKINE_REDUNDANCY | 4 | 3 | 3 | 0.8694 | 1 | ulcerative colitis | 0 | MS_WM_NULL_OR_WEAK | 0 |  |  | 0 |  |
| CCL3 | inflammatory_nfkb | GENE_LEVEL_ANTITNF_NONRESPONSE_ANCHOR | 12 | NO_GO_PRIOR_ROUTE_OR_DRUGGABILITY_BLOCKED | BLOCKED_BROAD_CHEMOKINE_REDUNDANCY | 4 | 3 | 3 | 0.8479 | 1 | ulcerative colitis | 0 | MS_WM_NULL_OR_WEAK | 0 |  |  | 0 |  |
| CCL2 | inflammatory_nfkb | GENE_LEVEL_ANTITNF_NONRESPONSE_ANCHOR | 12 | NO_GO_PRIOR_ROUTE_OR_DRUGGABILITY_BLOCKED | BLOCKED_BROAD_CHEMOKINE_REDUNDANCY_AND_PRIOR_ART | 4 | 3 | 2 | 0.825 | 0 |  | 1 | MS_WM_NULL_OR_WEAK | 5 | AS;Crohn;Psoriasis;RA;UC | NO_GO_WAVE62_TARGET_RESOLUTION | 0 |  |
| ACSL1 | lipid_loader_repair | GENE_LEVEL_ANTITNF_NONRESPONSE_ANCHOR | 11.5 | NO_GO_PRIOR_ROUTE_OR_DRUGGABILITY_BLOCKED | BLOCKED_AS_TARGET_DEMOTED_TO_MARKER_AFTER_MODULE_ADJUSTMENT | 4 | 3 | 2 | 0.8218 | 2 | Crohn disease;ulcerative colitis | 2 | MS_WM_NULL_OR_WEAK | 0 |  |  | 0 |  |
| IFI30 | ifn_apc;lysosomal_apc | GENE_LEVEL_ANTITNF_NONRESPONSE_ANCHOR | 11.5 | NO_GO_PRIOR_ROUTE_OR_DRUGGABILITY_BLOCKED | NO_GO_DIRECT_ANTIGEN_PROCESSING_HOST_DEFENSE_AND_POOR_DRUGGABILITY | 4 | 3 | 2 | 0.7945 | 1 | ulcerative colitis | 0 | MS_WM_NULL_OR_WEAK | 0 |  | PARK_MS_TARGET_RESOLVED_NO_CROSS_DISEASE_MODULE | 0 |  |
| GBP1 | ifn_apc | GENE_LEVEL_ANTITNF_NONRESPONSE_ANCHOR | 11 | NO_GO_PRIOR_ROUTE_OR_DRUGGABILITY_BLOCKED | NO_GO_IFN_RESPONSE_MARKER_NOT_DRUGGABLE_CONTROLLER | 4 | 2 | 2 | 0.732 | 2 | Crohn disease;ulcerative colitis | 0 | MS_WM_NULL_OR_WEAK | 0 |  |  | 0 |  |
| OSM | inflammatory_nfkb | GENE_LEVEL_ANTITNF_NONRESPONSE_ANCHOR | 10 | NO_GO_PRIOR_ROUTE_OR_DRUGGABILITY_BLOCKED | BLOCKED_OSM_OSMR_IBD_RA_PRIOR_ART_AND_MS_DIRECTION_AMBIGUITY | 4 | 2 | 2 | 0.8146 | 2 | Crohn disease;ulcerative colitis | 0 | MS_WM_NULL_OR_WEAK | 0 |  |  | 0 |  |
| LAMP3 | lysosomal_apc | GENE_LEVEL_ANTITNF_NONRESPONSE_ANCHOR | 10 | NO_GO_PRIOR_ROUTE_OR_DRUGGABILITY_BLOCKED | NO_GO_MARKER_STATE_NOT_INTERVENTION_POINT | 4 | 2 | 2 | 0.7589 | 1 | Crohn disease | 0 | MS_WM_NULL_OR_WEAK | 0 |  |  | 0 |  |
| STAT1 | ifn_apc | GENE_LEVEL_ANTITNF_NONRESPONSE_ANCHOR | 8.5 | NO_GO_PRIOR_ROUTE_OR_DRUGGABILITY_BLOCKED | BLOCKED_GENERIC_IFN_TRANSCRIPTION_AXIS | 4 | 2 | 1 | 0.6445 | 2 | Crohn disease;ulcerative colitis | 0 | MS_WM_NULL_OR_WEAK | 0 |  | NO_GO_WAVE62_TARGET_RESOLUTION | 0 |  |
| SPP1 | lipid_loader_repair | GENE_LEVEL_ANTITNF_NONRESPONSE_ANCHOR | 8 | NO_GO_PRIOR_ROUTE_OR_DRUGGABILITY_BLOCKED | BLOCKED_OSTEOPONTIN_CD44_PRIOR_ART_AND_WEAK_MS_SINGLE_GENE | 4 | 2 | 2 | 0.7854 | 0 |  | 1 | MS_WM_NULL_OR_WEAK | 0 |  |  | 0 |  |
| CXCL10 | ifn_apc | GENE_LEVEL_ANTITNF_NONRESPONSE_ANCHOR | 8 | NO_GO_PRIOR_ROUTE_OR_DRUGGABILITY_BLOCKED | BLOCKED_GENERIC_IFN_CHEMOKINE_AXIS | 4 | 2 | 2 | 0.728 | 0 |  | 0 | MS_WM_NULL_OR_WEAK | 0 |  |  | 0 |  |

## MS Module Context

| feature_type | feature | n_genes_present | genes_present | contrast | n_case | n_control | mean_case | mean_control | delta_log2 | hedges_g | welch_t | p | ols_beta_disease_ms | ols_p_disease_ms | ols_note | fdr |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| module | lipid_loader_repair | 11 | ACSL1,APOE,GPNMB,LPL,PLIN2,CD36,LIPA,FABP5,TREM2,MSR1,MERTK | MS_GM_vs_CON_GM | 5 | 5 | -0.3832 | -0.7591 | 0.3759 | 0.834 | 1.46 | 0.1904 | 0.5241 | 0.00117 | HC3 robust SE; covariates disease, region, age, sex | 0.6664 |
| module | interferon_apc | 11 | STAT1,IRF1,IRF7,CXCL10,IFI30,HLA-DRA,HLA-DRB1,CD74,GBP1,ISG15,IFI44L | MS_GM_vs_CON_GM | 5 | 5 | 0.004946 | -0.4388 | 0.4437 | 0.6608 | 1.157 | 0.2962 | 0.2316 | 0.3 | HC3 robust SE; covariates disease, region, age, sex | 0.6911 |
| module | lysosome_antigen_processing | 13 | IFI30,CTSD,CTSB,CTSS,CTSL,LAMP1,LAMP2,TPP1,HLA-DRA,HLA-DRB1,HLA-DPA1,HLA-DPB1,CD74 | MS_GM_vs_CON_GM | 5 | 5 | -0.3302 | -0.6196 | 0.2894 | 0.3948 | 0.691 | 0.5134 | 0.4378 | 0.1098 | HC3 robust SE; covariates disease, region, age, sex | 0.7188 |
| module | hif_nampt_metabolic | 8 | HIF1A,NAMPT,LDHA,SLC2A1,NFKBIA,IL1B,HK2,PFKFB3 | MS_GM_vs_CON_GM | 5 | 5 | -0.78 | -0.8014 | 0.02146 | 0.03788 | 0.06631 | 0.9491 | -0.0003218 | 0.9989 | HC3 robust SE; covariates disease, region, age, sex | 0.9491 |
| module | lipid_loader_repair | 11 | ACSL1,APOE,GPNMB,LPL,PLIN2,CD36,LIPA,FABP5,TREM2,MSR1,MERTK | MS_WM_vs_CON_WM | 10 | 11 | 0.5226 | 0.04417 | 0.4784 | 1.379 | 3.23 | 0.005282 | 0.5241 | 0.00117 | HC3 robust SE; covariates disease, region, age, sex | 0.01916 |
| module | lysosome_antigen_processing | 13 | IFI30,CTSD,CTSB,CTSS,CTSL,LAMP1,LAMP2,TPP1,HLA-DRA,HLA-DRB1,HLA-DPA1,HLA-DPB1,CD74 | MS_WM_vs_CON_WM | 10 | 11 | 0.4949 | -0.0182 | 0.5131 | 0.947 | 2.219 | 0.04134 | 0.4378 | 0.1098 | HC3 robust SE; covariates disease, region, age, sex | 0.09645 |
| module | interferon_apc | 11 | STAT1,IRF1,IRF7,CXCL10,IFI30,HLA-DRA,HLA-DRB1,CD74,GBP1,ISG15,IFI44L | MS_WM_vs_CON_WM | 10 | 11 | 0.218 | -0.000963 | 0.219 | 0.4583 | 1.098 | 0.2861 | 0.2316 | 0.3 | HC3 robust SE; covariates disease, region, age, sex | 0.468 |
| module | hif_nampt_metabolic | 8 | HIF1A,NAMPT,LDHA,SLC2A1,NFKBIA,IL1B,HK2,PFKFB3 | MS_WM_vs_CON_WM | 10 | 11 | 0.2692 | 0.4741 | -0.2048 | -0.3655 | -0.8611 | 0.4011 | -0.0003218 | 0.9989 | HC3 robust SE; covariates disease, region, age, sex | 0.468 |
| module | lipid_loader_repair | 11 | ACSL1,APOE,GPNMB,LPL,PLIN2,CD36,LIPA,FABP5,TREM2,MSR1,MERTK | MS_all_vs_CON_all | 15 | 16 | 0.2207 | -0.2069 | 0.4275 | 0.7743 | 2.194 | 0.0372 | 0.5241 | 0.00117 | HC3 robust SE; covariates disease, region, age, sex | 0.1302 |
| module | lysosome_antigen_processing | 13 | IFI30,CTSD,CTSB,CTSS,CTSL,LAMP1,LAMP2,TPP1,HLA-DRA,HLA-DRB1,HLA-DPA1,HLA-DPB1,CD74 | MS_all_vs_CON_all | 15 | 16 | 0.2199 | -0.2061 | 0.426 | 0.6407 | 1.807 | 0.08308 | 0.4378 | 0.1098 | HC3 robust SE; covariates disease, region, age, sex | 0.1939 |
| module | interferon_apc | 11 | STAT1,IRF1,IRF7,CXCL10,IFI30,HLA-DRA,HLA-DRB1,CD74,GBP1,ISG15,IFI44L | MS_all_vs_CON_all | 15 | 16 | 0.147 | -0.1378 | 0.2848 | 0.5365 | 1.525 | 0.1387 | 0.2316 | 0.3 | HC3 robust SE; covariates disease, region, age, sex | 0.2428 |
| module | hif_nampt_metabolic | 8 | HIF1A,NAMPT,LDHA,SLC2A1,NFKBIA,IL1B,HK2,PFKFB3 | MS_all_vs_CON_all | 15 | 16 | -0.08051 | 0.07547 | -0.156 | -0.1993 | -0.5685 | 0.5741 | -0.0003218 | 0.9989 | HC3 robust SE; covariates disease, region, age, sex | 0.6487 |

## Interpretation

- `IL1B`, `CXCL8`, and `TREM1` are the strongest external mucosal anti-TNF nonresponse anchors, but this evidence is treatment-response biology in IBD mucosa, not a cross-autoimmune therapeutic target.
- Local MS white-matter evidence does not support the inflammatory/NFKB/TNF single-gene branch: the inflammatory module is null while lipid-loader and lysosome/APC modules are stronger.
- The only available Geneformer support in this candidate set is `CXCL8` in IBD myeloid cells; most Wave86 leaders were not covered by the prior foundation-model perturbation tables.
- The branch therefore remains useful as a nonresponse-state comparator and trial-stratification warning, but not as a V3 finding.
