# Wave86 External GEO Anti-TNF Gene Driver Decomposition

Question: which gene-level component of the Wave85 generic inflammatory/IFN-high nonresponse signal is most stable across independent anti-TNF mucosal contexts?

Primary independent contexts counted in the rank: ACT1 UC (`GSE12251`), Leuven UC (`GSE14580`), Leuven Crohn colitis (`GSE16879`), and Leuven Crohn ileitis (`GSE16879`). The duplicate UC representation inside `GSE16879` and the combined GSE16879 summaries are retained only as overlap/sensitivity outputs.

## Gene Meta Rank

| gene | modules | n_primary_contexts | n_primary_overlap_groups | nonresponse_high_contexts | responder_high_contexts | nominal_nonresponse_contexts_p_lt_0_05 | fdr10_nonresponse_contexts | weighted_mean_hedges_g_responder_minus_non | median_auc_high_score_nonresponse | min_p | best_context | best_context_p | best_context_effect | meta_rank_score | call |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IL1B | inflammatory_nfkb | 4 | 4 | 4 | 0 | 3 | 3 | -1.695 | 0.8974 | 6.005e-05 | GSE16879_Crohn_colitis_Leuven_baseline | 6.005e-05 | -1.594 | 24.59 | GENE_LEVEL_ANTITNF_NONRESPONSE_ANCHOR |
| CXCL8 | inflammatory_nfkb | 4 | 4 | 4 | 0 | 3 | 3 | -1.702 | 0.8849 | 6.652e-07 | GSE16879_Crohn_colitis_Leuven_baseline | 6.652e-07 | -1.706 | 24.59 | GENE_LEVEL_ANTITNF_NONRESPONSE_ANCHOR |
| TREM1 | inflammatory_nfkb | 4 | 4 | 4 | 0 | 3 | 3 | -1.629 | 0.8826 | 3.486e-05 | GSE12251_UC_ACT1_baseline | 3.486e-05 | -1.541 | 24.51 | GENE_LEVEL_ANTITNF_NONRESPONSE_ANCHOR |
| CCL4 | inflammatory_nfkb | 4 | 4 | 4 | 0 | 3 | 3 | -1.533 | 0.8694 | 0.0003529 | GSE16879_Crohn_colitis_Leuven_baseline | 0.0003529 | -1.715 | 24.4 | GENE_LEVEL_ANTITNF_NONRESPONSE_ANCHOR |
| CCL3 | inflammatory_nfkb | 4 | 4 | 4 | 0 | 3 | 3 | -1.391 | 0.8479 | 8.39e-05 | GSE16879_Crohn_colitis_Leuven_baseline | 8.39e-05 | -1.63 | 24.24 | GENE_LEVEL_ANTITNF_NONRESPONSE_ANCHOR |
| CD44 | mif_cd74_receptor_state | 4 | 4 | 4 | 0 | 3 | 3 | -1.305 | 0.7995 | 0.0005175 | GSE16879_Crohn_colitis_Leuven_baseline | 0.0005175 | -1.622 | 24.1 | GENE_LEVEL_ANTITNF_NONRESPONSE_ANCHOR |
| CCL2 | inflammatory_nfkb | 4 | 4 | 4 | 0 | 3 | 2 | -1.41 | 0.825 | 0.0001606 | GSE16879_Crohn_colitis_Leuven_baseline | 0.0001606 | -1.656 | 22.74 | GENE_LEVEL_ANTITNF_NONRESPONSE_ANCHOR |
| ACSL1 | lipid_loader_repair | 4 | 4 | 4 | 0 | 3 | 2 | -1.328 | 0.8218 | 0.0004432 | GSE12251_UC_ACT1_baseline | 0.0004432 | -1.446 | 22.65 | GENE_LEVEL_ANTITNF_NONRESPONSE_ANCHOR |
| IFI30 | ifn_apc;lysosomal_apc | 4 | 4 | 4 | 0 | 3 | 2 | -0.9749 | 0.7945 | 0.01215 | GSE12251_UC_ACT1_baseline | 0.01215 | -0.9976 | 22.27 | GENE_LEVEL_ANTITNF_NONRESPONSE_ANCHOR |
| OSM | inflammatory_nfkb | 4 | 4 | 4 | 0 | 2 | 2 | -1.431 | 0.8146 | 0.0002321 | GSE12251_UC_ACT1_baseline | 0.0002321 | -1.527 | 20.75 | GENE_LEVEL_ANTITNF_NONRESPONSE_ANCHOR |
| SPP1 | lipid_loader_repair | 4 | 4 | 4 | 0 | 2 | 2 | -1.234 | 0.7854 | 8.237e-05 | GSE16879_Crohn_colitis_Leuven_baseline | 8.237e-05 | -1.573 | 20.52 | GENE_LEVEL_ANTITNF_NONRESPONSE_ANCHOR |
| LAMP3 | lysosomal_apc | 4 | 4 | 4 | 0 | 2 | 2 | -1.097 | 0.7589 | 0.005744 | GSE16879_Crohn_colitis_Leuven_baseline | 0.005744 | -1.461 | 20.36 | GENE_LEVEL_ANTITNF_NONRESPONSE_ANCHOR |
| CXCL10 | ifn_apc | 4 | 4 | 4 | 0 | 2 | 2 | -0.8556 | 0.728 | 0.004406 | GSE14580_UC_Leuven_baseline | 0.004406 | -1.075 | 20.08 | GENE_LEVEL_ANTITNF_NONRESPONSE_ANCHOR |
| GBP1 | ifn_apc | 4 | 4 | 4 | 0 | 2 | 2 | -0.845 | 0.732 | 0.007833 | GSE12251_UC_ACT1_baseline | 0.007833 | -1.132 | 20.08 | GENE_LEVEL_ANTITNF_NONRESPONSE_ANCHOR |
| CXCR4 | mif_cd74_receptor_state | 4 | 4 | 4 | 0 | 2 | 1 | -0.7992 | 0.7138 | 0.0134 | GSE16879_Crohn_colitis_Leuven_baseline | 0.0134 | -1.177 | 18.51 | GENE_LEVEL_ANTITNF_NONRESPONSE_ANCHOR |
| STAT1 | ifn_apc | 4 | 4 | 4 | 0 | 2 | 1 | -0.6552 | 0.6445 | 0.03486 | GSE14580_UC_Leuven_baseline | 0.03486 | -0.9199 | 18.3 | GENE_LEVEL_ANTITNF_NONRESPONSE_ANCHOR |
| C1QB | complement_phagocytosis | 4 | 4 | 4 | 0 | 0 | 0 | -0.5141 | 0.6375 | 0.1173 | GSE16879_Crohn_colitis_Leuven_baseline | 0.1173 | -0.8741 | 12.65 | NO_GENE_LEVEL_CONVERGENCE |
| GPNMB | lipid_loader_repair | 4 | 4 | 4 | 0 | 0 | 0 | -0.494 | 0.6547 | 0.0594 | GSE16879_Crohn_colitis_Leuven_baseline | 0.0594 | -0.8689 | 12.65 | NO_GENE_LEVEL_CONVERGENCE |
| HLA-DPA1 | hla_ii_apc;mif_cd74_receptor_state | 4 | 4 | 4 | 0 | 0 | 0 | -0.4779 | 0.656 | 0.2333 | GSE14580_UC_Leuven_baseline | 0.2333 | -0.6402 | 12.63 | NO_GENE_LEVEL_CONVERGENCE |
| HLA-DPB1 | hla_ii_apc;mif_cd74_receptor_state | 4 | 4 | 4 | 0 | 0 | 0 | -0.4444 | 0.646 | 0.1344 | GSE12251_UC_ACT1_baseline | 0.1344 | -0.6197 | 12.59 | NO_GENE_LEVEL_CONVERGENCE |

## Primary Context Tests For Top Genes

| cohort | gene | modules | n_patients | effect_responder_minus_non | hedges_g_responder_minus_non | auc_high_score_nonresponse | p | fdr_within_cohort |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GSE12251_UC_ACT1_baseline | ACSL1 | lipid_loader_repair | 22 | -1.446 | -1.99 | 0.9667 | 0.0004432 | 0.003324 |
| GSE14580_UC_Leuven_baseline | ACSL1 | lipid_loader_repair | 24 | -0.7283 | -0.7344 | 0.7031 | 0.04591 | 0.1377 |
| GSE16879_Crohn_colitis_Leuven_baseline | ACSL1 | lipid_loader_repair | 19 | -1.427 | -1.875 | 0.9405 | 0.00585 | 0.02393 |
| GSE16879_Crohn_ileitis_Leuven_baseline | ACSL1 | lipid_loader_repair | 18 | -0.7348 | -0.7326 | 0.6875 | 0.1098 | 0.8636 |
| GSE12251_UC_ACT1_baseline | CCL2 | inflammatory_nfkb | 22 | -0.6384 | -0.6766 | 0.65 | 0.1269 | 0.2121 |
| GSE14580_UC_Leuven_baseline | CCL2 | inflammatory_nfkb | 24 | -1.218 | -1.421 | 0.875 | 0.003644 | 0.03965 |
| GSE16879_Crohn_colitis_Leuven_baseline | CCL2 | inflammatory_nfkb | 19 | -1.656 | -2.692 | 0.9643 | 0.0001606 | 0.001446 |
| GSE16879_Crohn_ileitis_Leuven_baseline | CCL2 | inflammatory_nfkb | 18 | -0.9028 | -0.9403 | 0.775 | 0.04369 | 0.8636 |
| GSE12251_UC_ACT1_baseline | CCL3 | inflammatory_nfkb | 22 | -1.331 | -1.637 | 0.8833 | 0.0008736 | 0.004914 |
| GSE14580_UC_Leuven_baseline | CCL3 | inflammatory_nfkb | 24 | -0.9369 | -0.9913 | 0.8125 | 0.008081 | 0.06061 |
| GSE16879_Crohn_colitis_Leuven_baseline | CCL3 | inflammatory_nfkb | 19 | -1.63 | -2.565 | 0.9762 | 8.39e-05 | 0.0009439 |
| GSE16879_Crohn_ileitis_Leuven_baseline | CCL3 | inflammatory_nfkb | 18 | -0.4078 | -0.3852 | 0.65 | 0.4013 | 0.8636 |
| GSE12251_UC_ACT1_baseline | CCL4 | inflammatory_nfkb | 22 | -1.221 | -1.413 | 0.8833 | 0.004948 | 0.02234 |
| GSE14580_UC_Leuven_baseline | CCL4 | inflammatory_nfkb | 24 | -1.146 | -1.297 | 0.8555 | 0.002616 | 0.03965 |
| GSE16879_Crohn_colitis_Leuven_baseline | CCL4 | inflammatory_nfkb | 19 | -1.715 | -3.022 | 0.9881 | 0.0003529 | 0.002269 |
| GSE16879_Crohn_ileitis_Leuven_baseline | CCL4 | inflammatory_nfkb | 18 | -0.4466 | -0.4239 | 0.65 | 0.3576 | 0.8636 |
| GSE12251_UC_ACT1_baseline | CD44 | mif_cd74_receptor_state | 22 | -1.217 | -1.429 | 0.8333 | 0.004964 | 0.02234 |
| GSE14580_UC_Leuven_baseline | CD44 | mif_cd74_receptor_state | 24 | -0.8778 | -0.9146 | 0.7656 | 0.02036 | 0.0916 |
| GSE16879_Crohn_colitis_Leuven_baseline | CD44 | mif_cd74_receptor_state | 19 | -1.622 | -2.531 | 0.9524 | 0.0005175 | 0.002911 |
| GSE16879_Crohn_ileitis_Leuven_baseline | CD44 | mif_cd74_receptor_state | 18 | -0.4012 | -0.3787 | 0.6125 | 0.3951 | 0.8636 |
| GSE12251_UC_ACT1_baseline | CXCL8 | inflammatory_nfkb | 22 | -1.409 | -1.874 | 0.9417 | 0.000225 | 0.002422 |
| GSE14580_UC_Leuven_baseline | CXCL8 | inflammatory_nfkb | 24 | -1.152 | -1.308 | 0.8281 | 0.001845 | 0.03965 |
| GSE16879_Crohn_colitis_Leuven_baseline | CXCL8 | inflammatory_nfkb | 19 | -1.706 | -2.966 | 1 | 6.652e-07 | 2.994e-05 |
| GSE16879_Crohn_ileitis_Leuven_baseline | CXCL8 | inflammatory_nfkb | 18 | -0.6895 | -0.6808 | 0.6875 | 0.1548 | 0.8636 |
| GSE12251_UC_ACT1_baseline | IFI30 | ifn_apc;lysosomal_apc | 22 | -0.9976 | -1.106 | 0.8 | 0.01215 | 0.03738 |
| GSE14580_UC_Leuven_baseline | IFI30 | ifn_apc;lysosomal_apc | 24 | -0.895 | -0.9366 | 0.7891 | 0.02804 | 0.1051 |
| GSE16879_Crohn_colitis_Leuven_baseline | IFI30 | ifn_apc;lysosomal_apc | 19 | -1.034 | -1.118 | 0.8095 | 0.01766 | 0.05297 |
| GSE16879_Crohn_ileitis_Leuven_baseline | IFI30 | ifn_apc;lysosomal_apc | 18 | -0.7197 | -0.7151 | 0.675 | 0.1607 | 0.8636 |
| GSE12251_UC_ACT1_baseline | IL1B | inflammatory_nfkb | 22 | -1.569 | -2.34 | 0.9667 | 7.027e-05 | 0.001581 |
| GSE14580_UC_Leuven_baseline | IL1B | inflammatory_nfkb | 24 | -1.11 | -1.24 | 0.8281 | 0.002939 | 0.03965 |
| GSE16879_Crohn_colitis_Leuven_baseline | IL1B | inflammatory_nfkb | 19 | -1.594 | -2.411 | 0.9881 | 6.005e-05 | 0.0009439 |
| GSE16879_Crohn_ileitis_Leuven_baseline | IL1B | inflammatory_nfkb | 18 | -0.7566 | -0.758 | 0.7 | 0.1118 | 0.8636 |
| GSE12251_UC_ACT1_baseline | OSM | inflammatory_nfkb | 22 | -1.527 | -2.168 | 0.9583 | 0.0002321 | 0.002422 |
| GSE14580_UC_Leuven_baseline | OSM | inflammatory_nfkb | 24 | -0.6598 | -0.6571 | 0.6875 | 0.08893 | 0.2137 |
| GSE16879_Crohn_colitis_Leuven_baseline | OSM | inflammatory_nfkb | 19 | -1.562 | -2.289 | 0.9167 | 0.002771 | 0.01386 |
| GSE16879_Crohn_ileitis_Leuven_baseline | OSM | inflammatory_nfkb | 18 | -0.668 | -0.6567 | 0.7125 | 0.1494 | 0.8636 |
| GSE12251_UC_ACT1_baseline | TREM1 | inflammatory_nfkb | 22 | -1.541 | -2.251 | 1 | 3.486e-05 | 0.001569 |
| GSE14580_UC_Leuven_baseline | TREM1 | inflammatory_nfkb | 24 | -1.032 | -1.123 | 0.7891 | 0.01865 | 0.0916 |
| GSE16879_Crohn_colitis_Leuven_baseline | TREM1 | inflammatory_nfkb | 19 | -1.546 | -2.233 | 0.9762 | 0.0002169 | 0.001627 |
| GSE16879_Crohn_ileitis_Leuven_baseline | TREM1 | inflammatory_nfkb | 18 | -0.8752 | -0.9042 | 0.7375 | 0.07229 | 0.8636 |

## Interpretation Guardrail

This is a gene-level decomposition of bulk mucosal response data. It can nominate resistance-associated genes for prior-art and cell-state follow-up, but it does not prove that inhibiting or activating any gene would improve anti-TNF response.
