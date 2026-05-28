# Wave73 P2RX7 Stratification Test

## Question

Does the Wave72 broad purine metabolomics signal correspond to a cell-resolved `P2RX7/IL1B/NLRP3/CASP1` state that predicts treatment response beyond generic inflammatory modules?

## Verdict

PARK_P2RX7_STRATIFICATION_NEEDS_TARGET_LEVEL_DATA

This is not a therapeutic finding. The branch is closed or parked unless future target-level baseline/purine/protein data can link P2RX7 activity to responder biology.

## Integrated Decision

| candidate | wave73_call | gate_count | biochemical_purine_support | cellstate_broad_support | specificity_vs_generic_modules | ms_module_anchor | gse282122_response_support | ra_response_support | p2rx7_gene_level_anchor | wave72_supportive_diseases | broad_positive_diseases | broad_negative_diseases | ms_mean_effect | ms_combined_p | best_gse282122_response | ra_response_row | decision_reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P2RX7_purinergic_inflammasome_stratification | PARK_P2RX7_STRATIFICATION_NEEDS_TARGET_LEVEL_DATA | 2 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | AS;Crohn;RA;T1D;UC | Crohn disease;type 1 diabetes mellitus;ulcerative colitis |  | -0.21359586134899236 | 0.06082489025676918 | {'dataset': 'GSE282122', 'test': 'remission_delta_difference', 'cell_state': 'DC', 'module': 'p2rx7_inflammasome', 'n_genes_present': 7, 'genes_present': 'CASP1;GSDMD;IL1B;NLRP1;NLRP3;P2RX7;PYCARD', 'mean_effect': 0.08835910996782455, 'median_effect': 0.1191805558680366, 'combined_z': 1.2178491775059896, 'combined_p': 0.2232812923152514, 'expected_direction_support': False, 'fdr': 0.49868891297808166} | {'dataset': 'GSE198520_RA_synovium_antiTNF', 'module': 'p2rx7_inflammasome', 'n_patients': 46, 'mean_post_minus_pre': -0.1402342401403561, 'paired_t': -3.0587164347733724, 'paired_p': 0.0037367103192994674, 'good_vs_other_delta': -0.06332583144547949, 'good_vs_other_p': 0.5329247126716025, 'modgood_vs_none_delta': -0.06557797991227464, 'modgood_vs_none_p': 0.4909264566882204, 'expected_direction_support': False, 'paired_fdr': 0.01001200436706063, 'good_vs_other_fdr': 0.5929618047666811, 'modgood | biochemistry and cell-state support exist, but target-level validation is missing |

## Broad Cell-State Module Summary

| module | tested_context_count | positive_context_count | negative_context_count | positive_fdr10_context_count | positive_disease_count | negative_disease_count | positive_diseases | negative_diseases | specificity_pass_context_count | best_positive_context |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| p2rx7_inflammasome | 17 | 5 | 0 | 5 | 3 | 0 | Crohn disease;type 1 diabetes mellitus;ulcerative colitis |  | 0 | ibd_crohn_myeloid\|Crohn disease\|colon myeloid\|effect=1.42\|p=4.42e-06\|fdr=6.44e-05 |
| inflammasome_no_p2rx7 | 17 | 6 | 0 | 6 | 3 | 0 | Crohn disease;type 1 diabetes mellitus;ulcerative colitis |  | 0 | ibd_crohn_myeloid\|Crohn disease\|colon myeloid\|effect=1.39\|p=1.6e-05\|fdr=0.000169 |
| purinergic_adenosine | 17 | 6 | 0 | 6 | 4 | 0 | Crohn disease;psoriasis;type 1 diabetes mellitus;ulcerative colitis |  | 0 | ibd_uc_stromal\|ulcerative colitis\|colon stromal\|effect=0.824\|p=0.00916\|fdr=0.0267 |
| generic_nfkb_tnf | 17 | 10 | 2 | 10 | 3 | 1 | Crohn disease;type 1 diabetes mellitus;ulcerative colitis | psoriasis | 0 | t1d_acinar_cell\|type 1 diabetes mellitus\|pancreatic acinar cell\|effect=1.53\|p=1.61e-07\|fdr=7.7e-06 |
| interferon_apc | 17 | 15 | 0 | 15 | 5 | 0 | Crohn disease;Sjogren syndrome;psoriasis;type 1 diabetes mellitus;ulcerative colitis |  | 0 | t1d_beta_cell\|type 1 diabetes mellitus\|pancreatic beta cell\|effect=1.82\|p=0.00013\|fdr=0.000736 |
| lysosome_apc | 17 | 6 | 0 | 6 | 2 | 0 | psoriasis;type 1 diabetes mellitus |  | 0 | t1d_beta_cell\|type 1 diabetes mellitus\|pancreatic beta cell\|effect=1.1\|p=0.00237\|fdr=0.00806 |

## MS White-Matter Module Test

| dataset | module | n_genes_present | genes_present | mean_effect | median_effect | combined_z | combined_p | fdr | support_call |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GSE111972_MS_white_matter | p2rx7_inflammasome | 7 | CASP1;GSDMD;IL1B;NLRP1;NLRP3;P2RX7;PYCARD | -0.21359586134899236 | -0.2348280075935918 | -1.8747662347817755 | 0.06082489025676918 | 0.09123733538515377 | NO_MS_MODULE_SUPPORT |
| GSE111972_MS_white_matter | inflammasome_no_p2rx7 | 6 | CASP1;GSDMD;IL1B;NLRP1;NLRP3;PYCARD | -0.2555530111011738 | -0.2644394894730411 | -2.1083500625991225 | 0.035000720565992606 | 0.07000144113198521 | NO_MS_MODULE_SUPPORT |
| GSE111972_MS_white_matter | purinergic_adenosine | 7 | ADA;ADK;ADORA2A;ADORA2B;ENTPD1;NT5E;PNP | -0.5183488215174247 | -0.1387538147642857 | -1.130101937489248 | 0.2584332734415793 | 0.31011992812989514 | NO_MS_MODULE_SUPPORT |
| GSE111972_MS_white_matter | generic_nfkb_tnf | 8 | CCL2;CCL3;CCL4;CXCL8;IL6;NFKBIA;TNF;TNFAIP3 | 0.08898171709682057 | 0.0580606193590167 | 0.7361552945617156 | 0.46163619520218935 | 0.46163619520218935 | NO_MS_MODULE_SUPPORT |
| GSE111972_MS_white_matter | interferon_apc | 9 | CD74;CXCL10;GBP1;HLA-DRA;HLA-DRB1;IFI30;IRF1;ISG15;STAT1 | 0.3601715486328435 | 0.2891316379039903 | 3.4101734067492657 | 0.0006492158730231826 | 0.0019476476190695478 | MS_NOMINAL_POSITIVE |
| GSE111972_MS_white_matter | lysosome_apc | 10 | CD74;CTSB;CTSD;CTSL;CTSS;HLA-DRA;IFI30;LAMP1;LAMP2;TPP1 | 0.21206171033192261 | 0.20001789636929151 | 3.6347534342909946 | 0.00027824661756285774 | 0.0016694797053771464 | NO_MS_MODULE_SUPPORT |

## GSE282122 IBD Anti-TNF Response Rows

| dataset | test | cell_state | module | n_genes_present | genes_present | mean_effect | median_effect | combined_z | combined_p | expected_direction_support | fdr |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GSE282122 | remission_delta_difference | DC | p2rx7_inflammasome | 7 | CASP1;GSDMD;IL1B;NLRP1;NLRP3;P2RX7;PYCARD | 0.08835910996782455 | 0.1191805558680366 | 1.2178491775059896 | 0.2232812923152514 | False | 0.49868891297808166 |
| GSE282122 | paired_post_minus_pre_all | Mono_macro | p2rx7_inflammasome | 7 | CASP1;GSDMD;IL1B;NLRP1;NLRP3;P2RX7;PYCARD | 0.12456667027190751 | 0.1618435575527959 | 1.2040616483175381 | 0.22856575178162075 | False | 0.49868891297808166 |
| GSE282122 | paired_post_minus_pre_all | DC | p2rx7_inflammasome | 7 | CASP1;GSDMD;IL1B;NLRP1;NLRP3;P2RX7;PYCARD | -0.1059359246436427 | 0.0381657388260361 | -0.8875676427376286 | 0.3747733654055646 | False | 0.5611002608291743 |
| GSE282122 | remission_delta_difference | Mono_macro | p2rx7_inflammasome | 7 | CASP1;GSDMD;IL1B;NLRP1;NLRP3;P2RX7;PYCARD | -0.14213905732374216 | -0.2027477831590355 | -0.846191329451717 | 0.3974460180873318 | False | 0.5611002608291743 |

## RA Anti-TNF Module Rows

| dataset | module | n_patients | mean_post_minus_pre | paired_t | paired_p | good_vs_other_delta | good_vs_other_p | modgood_vs_none_delta | modgood_vs_none_p | expected_direction_support | paired_fdr | good_vs_other_fdr | modgood_vs_none_fdr |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GSE198520_RA_synovium_antiTNF | generic_nfkb_tnf | 46 | -0.1137101524455509 | -1.8858218997567655 | 0.06578372907860758 | -0.24920499018450387 | 0.06432515705082106 | -0.3099350948150058 | 0.0033539839945187465 | False | 0.0789404748943291 | 0.2018468972681733 | 0.02012390396711248 |
| GSE198520_RA_synovium_antiTNF | inflammasome_no_p2rx7 | 46 | -0.1410269758338589 | -3.0153318197466 | 0.004209471303950704 | -0.055350840215225294 | 0.5929618047666811 | -0.06492373135069868 | 0.5207949190808949 | False | 0.01001200436706063 | 0.5929618047666811 | 0.5207949190808949 |
| GSE198520_RA_synovium_antiTNF | interferon_apc | 46 | -0.4053020375539986 | -2.951635716512686 | 0.005006002183530315 | -0.55306238472064 | 0.0672822990893911 | -0.6117434487416423 | 0.011757083124399012 | False | 0.01001200436706063 | 0.2018468972681733 | 0.03527124937319704 |
| GSE198520_RA_synovium_antiTNF | lysosome_apc | 46 | -0.4054193455963314 | -2.317448501874221 | 0.02508544691651757 | -0.45949925092504823 | 0.2175028023386274 | -0.7561382147405546 | 0.024129242133987646 | False | 0.03762817037477636 | 0.3262542035079411 | 0.036193863200981474 |
| GSE198520_RA_synovium_antiTNF | p2rx7_inflammasome | 46 | -0.1402342401403561 | -3.0587164347733724 | 0.0037367103192994674 | -0.06332583144547949 | 0.5329247126716025 | -0.06557797991227464 | 0.4909264566882204 | False | 0.01001200436706063 | 0.5929618047666811 | 0.5207949190808949 |
| GSE198520_RA_synovium_antiTNF | purinergic_adenosine | 46 | 0.02662820105885122 | 0.49274528129897516 | 0.6245884014711058 | 0.16763192182786119 | 0.15440432925099865 | 0.2465805879343111 | 0.02089112165456218 | False | 0.6245884014711058 | 0.3088086585019973 | 0.036193863200981474 |
