# Wave75 Response-State Stratification Audit

## Question

Does the recurrent IFN/APC plus lysosomal/APC state predict anti-TNF
response across RA synovium and IBD myeloid/DC datasets better than a
generic inflammatory module?

## Verdict

REOPEN_RESPONSE_STRATIFICATION

## Integrated Decision

| candidate | wave75_call | decision_reason | best_module | best_endpoint | ra_effect | ra_p | ibd_effect | ibd_p | direction_stable | both_nominal_p10 | one_nominal_other_trend |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IFN_APC_lysosomal_APC_response_stratification | REOPEN_RESPONSE_STRATIFICATION | RA and IBD response associations are directionally stable and nominal in both datasets | lysosomal_apc | baseline_pre | 1.018 | 0.001127 | 0.8878 | 0.02039 | True | True | True |

## Cross-Dataset Convergence

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
| hla_ii_apc__resid_ifn_apc_inflammatory_nfkb | delta_post_minus_pre | moderate_good_vs_none | 0.4089 | 0.1114 | 0.2255 | DC | 1.265 | 0.00121 | 0.03327 | True | False | True | 4 |
| lysosomal_apc__resid_ifn_apc_inflammatory_nfkb | delta_post_minus_pre | moderate_good_vs_none | -0.4128 | 0.1959 | 0.333 | DC | -0.9869 | 0.0111 | 0.06991 | True | False | True | 4 |
| ifn_apc | delta_post_minus_pre | moderate_good_vs_none | -0.5345 | 0.02887 | 0.08724 | DC | -0.4626 | 0.2139 | 0.399 | True | False | False | 2 |
| lysosomal_apc__resid_ifn_apc_inflammatory_nfkb | baseline_pre | good_vs_moderate_none | 0.475 | 0.1409 | 0.2662 | DC | 0.6363 | 0.09855 | 0.2557 | True | False | False | 2 |
| lysosomal_apc__resid_inflammatory_nfkb | delta_post_minus_pre | moderate_good_vs_none | -0.3753 | 0.209 | 0.3417 | DC | -1.094 | 0.005623 | 0.04842 | True | False | False | 2 |
| ifn_lysosomal_apc_composite__resid_inflammatory_nfkb | delta_post_minus_pre | moderate_good_vs_none | -0.2779 | 0.3099 | 0.4621 | DC | -0.8986 | 0.02084 | 0.09839 | True | False | False | 2 |
| hla_ii_apc__resid_ifn_apc_inflammatory_nfkb | baseline_pre | moderate_good_vs_none | -0.2596 | 0.3147 | 0.4652 | DC | -0.6638 | 0.06611 | 0.2007 | True | False | False | 2 |
| hla_ii_apc__resid_inflammatory_nfkb | delta_post_minus_pre | moderate_good_vs_none | 0.2033 | 0.445 | 0.607 | Mono_macro | 1.065 | 0.006146 | 0.04842 | True | False | False | 2 |
| ifn_apc__resid_inflammatory_nfkb | delta_post_minus_pre | moderate_good_vs_none | -0.167 | 0.5129 | 0.6507 | DC | -0.4667 | 0.2103 | 0.3972 | True | False | False | 2 |
| inflammatory_nfkb | delta_post_minus_pre | moderate_good_vs_none | -0.7559 | 0.002493 | 0.04238 | Mono_macro | -0.2145 | 0.5633 | 0.7421 | True | False | False | 1 |
| inflammatory_nfkb | baseline_pre | moderate_good_vs_none | 0.7036 | 0.009973 | 0.05846 | DC | 0.3282 | 0.3703 | 0.5776 | True | False | False | 1 |
| mif_cd74_receptor_state__resid_ifn_apc_inflammatory_nfkb | baseline_pre | good_vs_moderate_none | 0.7078 | 0.01618 | 0.07294 | Mono_macro | -0.7848 | 0.04261 | 0.1575 | False | False | False | 1 |
| lipid_loader_repair__resid_ifn_apc_inflammatory_nfkb | baseline_pre | good_vs_moderate_none | -0.8426 | 0.01631 | 0.07294 | DC | 0.5424 | 0.1376 | 0.2999 | False | False | False | 1 |
| hla_ii_apc | baseline_pre | good_vs_moderate_none | 0.5301 | 0.09272 | 0.1946 | Mono_macro | -0.2704 | 0.4787 | 0.6572 | False | False | False | 1 |
| lipid_loader_repair__resid_ifn_apc_inflammatory_nfkb | delta_post_minus_pre | good_vs_moderate_none | 0.4496 | 0.1428 | 0.2667 | DC | -1.5 | 0.0003014 | 0.0253 | False | False | False | 1 |
| hla_ii_apc__resid_inflammatory_nfkb | baseline_pre | good_vs_moderate_none | 0.4501 | 0.1502 | 0.2775 | Mono_macro | -0.2968 | 0.4325 | 0.6339 | False | False | False | 1 |
| lipid_loader_repair | delta_post_minus_pre | moderate_good_vs_none | -0.3613 | 0.2 | 0.3334 | DC | -1.176 | 0.004306 | 0.04575 | True | False | False | 1 |
| mif_cd74_receptor_state__resid_ifn_apc_inflammatory_nfkb | delta_post_minus_pre | moderate_good_vs_none | -0.3287 | 0.2438 | 0.3838 | Mono_macro | 1.236 | 0.002008 | 0.03679 | False | False | False | 1 |
| hla_ii_apc | delta_post_minus_pre | good_vs_moderate_none | -0.2275 | 0.4632 | 0.6201 | Mono_macro | 1.034 | 0.007638 | 0.05636 | False | False | False | 1 |
| mif_cd74_receptor_state | baseline_pre | good_vs_moderate_none | 1.09 | 0.0005732 | 0.03112 | Mono_macro | -0.4601 | 0.24 | 0.4295 | False | False | False | 0 |
| mif_cd74_receptor_state__resid_inflammatory_nfkb | baseline_pre | good_vs_moderate_none | 1.042 | 0.0009152 | 0.03112 | Mono_macro | -0.4825 | 0.2159 | 0.399 | False | False | False | 0 |
| mif_cd74_receptor_state | delta_post_minus_pre | moderate_good_vs_none | -0.6025 | 0.025 | 0.08205 | Mono_macro | 1.099 | 0.005056 | 0.04775 | False | False | False | 0 |
| lipid_loader_repair__resid_inflammatory_nfkb | baseline_pre | good_vs_moderate_none | -0.6537 | 0.05506 | 0.14 | DC | 0.2963 | 0.4219 | 0.6292 | False | False | False | 0 |
| lipid_loader_repair | baseline_pre | good_vs_moderate_none | -0.5061 | 0.1282 | 0.2476 | DC | 0.5627 | 0.1417 | 0.3049 | False | False | False | 0 |
| mif_cd74_receptor_state__resid_inflammatory_nfkb | delta_post_minus_pre | moderate_good_vs_none | -0.4011 | 0.1397 | 0.2662 | Mono_macro | 1.129 | 0.004084 | 0.04575 | False | False | False | 0 |
| lipid_loader_repair__resid_inflammatory_nfkb | delta_post_minus_pre | good_vs_moderate_none | 0.4032 | 0.1897 | 0.3295 | DC | -1.218 | 0.002164 | 0.03679 | False | False | False | 0 |

## RA Response Tests

| dataset | cell_state | endpoint | comparison | module | n_group_a | n_group_b | effect_group_a_minus_b | p | fdr |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | baseline_pre | good_vs_moderate_none | mif_cd74_receptor_state | 19 | 27 | 1.09 | 0.0005732 | 0.03112 |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | baseline_pre | spearman_vs_delta_das28 | mif_cd74_receptor_state | 46 | 0 | -0.4809 | 0.000717 | 0.03112 |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | paired_change | moderate_good_responders | mif_cd74_receptor_state | 32 | 0 | -0.4651 | 0.0008089 | 0.03112 |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | paired_change | all_patients | mif_cd74_receptor_state | 46 | 0 | -0.3464 | 0.0008237 | 0.03112 |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | baseline_pre | good_vs_moderate_none | mif_cd74_receptor_state__resid_inflammatory_nfkb | 19 | 27 | 1.042 | 0.0009152 | 0.03112 |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | baseline_pre | good_vs_moderate_none | lysosomal_apc | 19 | 27 | 1.018 | 0.001127 | 0.03194 |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | baseline_pre | spearman_vs_delta_das28 | mif_cd74_receptor_state__resid_inflammatory_nfkb | 46 | 0 | -0.4554 | 0.001472 | 0.03575 |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | paired_change | all_patients | mif_cd74_receptor_state__resid_inflammatory_nfkb | 46 | 0 | -0.2901 | 0.001749 | 0.03716 |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | baseline_pre | moderate_good_vs_none | mif_cd74_receptor_state | 32 | 14 | 0.967 | 0.00247 | 0.04238 |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | delta_post_minus_pre | moderate_good_vs_none | inflammatory_nfkb | 32 | 14 | -0.7559 | 0.002493 | 0.04238 |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | baseline_pre | good_vs_moderate_none | lysosomal_apc__resid_inflammatory_nfkb | 19 | 27 | 0.934 | 0.003074 | 0.04513 |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | paired_change | moderate_good_responders | mif_cd74_receptor_state__resid_inflammatory_nfkb | 32 | 0 | -0.3631 | 0.00336 | 0.04513 |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | paired_change | moderate_good_responders | lysosomal_apc | 32 | 0 | -0.4258 | 0.003806 | 0.04513 |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | paired_change | moderate_good_responders | ifn_lysosomal_apc_composite | 32 | 0 | -0.4549 | 0.003853 | 0.04513 |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | baseline_pre | moderate_good_vs_none | lysosomal_apc | 32 | 14 | 0.8202 | 0.004291 | 0.04513 |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | paired_change | all_patients | hla_ii_apc | 46 | 0 | -0.2824 | 0.004558 | 0.04513 |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | baseline_pre | good_vs_moderate_none | ifn_lysosomal_apc_composite | 19 | 27 | 0.9078 | 0.004831 | 0.04513 |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | baseline_pre | moderate_good_vs_none | ifn_lysosomal_apc_composite | 32 | 14 | 0.7699 | 0.005223 | 0.04513 |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | paired_change | all_patients | ifn_apc | 46 | 0 | -0.3516 | 0.005425 | 0.04513 |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | paired_change | moderate_good_responders | ifn_apc | 32 | 0 | -0.4839 | 0.005592 | 0.04513 |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | paired_change | all_patients | ifn_lysosomal_apc_composite | 46 | 0 | -0.3211 | 0.005838 | 0.04513 |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | baseline_pre | spearman_vs_delta_das28 | mif_cd74_receptor_state__resid_ifn_apc_inflammatory_nfkb | 46 | 0 | -0.4003 | 0.00584 | 0.04513 |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | paired_change | good_responders | mif_cd74_receptor_state | 19 | 0 | -0.5405 | 0.006432 | 0.04716 |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | baseline_pre | spearman_vs_delta_das28 | lysosomal_apc | 46 | 0 | -0.3946 | 0.006658 | 0.04716 |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | baseline_pre | spearman_vs_delta_das28 | ifn_lysosomal_apc_composite | 46 | 0 | -0.3848 | 0.008276 | 0.05446 |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | baseline_pre | moderate_good_vs_none | mif_cd74_receptor_state__resid_inflammatory_nfkb | 32 | 14 | 0.8397 | 0.00833 | 0.05446 |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | baseline_pre | good_vs_moderate_none | ifn_lysosomal_apc_composite__resid_inflammatory_nfkb | 19 | 27 | 0.832 | 0.009397 | 0.05846 |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | paired_change | all_patients | lysosomal_apc | 46 | 0 | -0.2907 | 0.009835 | 0.05846 |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | baseline_pre | moderate_good_vs_none | inflammatory_nfkb | 32 | 14 | 0.7036 | 0.009973 | 0.05846 |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | baseline_pre | moderate_good_vs_none | ifn_apc | 32 | 14 | 0.6771 | 0.01059 | 0.06001 |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | paired_change | good_responders | inflammatory_nfkb | 19 | 0 | -0.3849 | 0.01102 | 0.06042 |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | delta_post_minus_pre | good_vs_moderate_none | inflammatory_nfkb | 19 | 27 | -0.8528 | 0.01181 | 0.06276 |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | paired_change | good_responders | ifn_lysosomal_apc_composite | 19 | 0 | -0.5718 | 0.01485 | 0.07294 |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | paired_change | moderate_good_responders | inflammatory_nfkb | 32 | 0 | -0.2561 | 0.01553 | 0.07294 |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | paired_change | nonresponders | hla_ii_apc__resid_ifn_apc_inflammatory_nfkb | 14 | 0 | -0.2101 | 0.01582 | 0.07294 |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | paired_change | good_responders | ifn_apc | 19 | 0 | -0.6377 | 0.01586 | 0.07294 |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | baseline_pre | good_vs_moderate_none | mif_cd74_receptor_state__resid_ifn_apc_inflammatory_nfkb | 19 | 27 | 0.7078 | 0.01618 | 0.07294 |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | baseline_pre | good_vs_moderate_none | lipid_loader_repair__resid_ifn_apc_inflammatory_nfkb | 19 | 27 | -0.8426 | 0.01631 | 0.07294 |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | paired_change | all_patients | ifn_lysosomal_apc_composite__resid_inflammatory_nfkb | 46 | 0 | -0.2218 | 0.01773 | 0.07485 |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | paired_change | moderate_good_responders | lysosomal_apc__resid_inflammatory_nfkb | 32 | 0 | -0.2821 | 0.01776 | 0.07485 |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | paired_change | good_responders | lysosomal_apc | 19 | 0 | -0.5059 | 0.01805 | 0.07485 |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | paired_change | nonresponders | hla_ii_apc__resid_inflammatory_nfkb | 14 | 0 | -0.3021 | 0.01862 | 0.07539 |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | paired_change | good_responders | mif_cd74_receptor_state__resid_inflammatory_nfkb | 19 | 0 | -0.3871 | 0.01967 | 0.07776 |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | baseline_pre | good_vs_moderate_none | ifn_apc | 19 | 27 | 0.7594 | 0.02112 | 0.08032 |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | paired_change | all_patients | hla_ii_apc__resid_inflammatory_nfkb | 46 | 0 | -0.214 | 0.02135 | 0.08032 |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | baseline_pre | moderate_good_vs_none | mif_cd74_receptor_state__resid_ifn_apc_inflammatory_nfkb | 32 | 14 | 0.7321 | 0.0221 | 0.08032 |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | baseline_pre | spearman_vs_delta_das28 | lysosomal_apc__resid_inflammatory_nfkb | 46 | 0 | -0.3347 | 0.02298 | 0.08032 |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | paired_change | all_patients | lysosomal_apc__resid_inflammatory_nfkb | 46 | 0 | -0.2116 | 0.02307 | 0.08032 |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | paired_change | all_patients | ifn_apc__resid_inflammatory_nfkb | 46 | 0 | -0.2321 | 0.02315 | 0.08032 |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | delta_post_minus_pre | moderate_good_vs_none | ifn_lysosomal_apc_composite | 32 | 14 | -0.5896 | 0.02429 | 0.08205 |

## IBD Response Tests

| dataset | cell_state | endpoint | comparison | module | n_group_a | n_group_b | effect_group_a_minus_b | p | fdr |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GSE282122_IBD_myeloid_antiTNF | DC | paired_change | remission | hla_ii_apc__resid_ifn_apc_inflammatory_nfkb | 13 | 0 | 0.421 | 0.0002865 | 0.0253 |
| GSE282122_IBD_myeloid_antiTNF | DC | delta_post_minus_pre | remission_vs_nonremission | lipid_loader_repair__resid_ifn_apc_inflammatory_nfkb | 13 | 16 | -1.5 | 0.0003014 | 0.0253 |
| GSE282122_IBD_myeloid_antiTNF | DC | paired_change | remission | hla_ii_apc__resid_inflammatory_nfkb | 13 | 0 | 0.3588 | 0.0005191 | 0.0253 |
| GSE282122_IBD_myeloid_antiTNF | DC | paired_change | remission | mif_cd74_receptor_state__resid_ifn_apc_inflammatory_nfkb | 13 | 0 | 0.3163 | 0.0005953 | 0.0253 |
| GSE282122_IBD_myeloid_antiTNF | DC | delta_post_minus_pre | remission_vs_nonremission | hla_ii_apc__resid_ifn_apc_inflammatory_nfkb | 13 | 16 | 1.265 | 0.00121 | 0.03327 |
| GSE282122_IBD_myeloid_antiTNF | Mono_macro | paired_change | remission | hla_ii_apc__resid_ifn_apc_inflammatory_nfkb | 13 | 0 | 0.7686 | 0.001526 | 0.03327 |
| GSE282122_IBD_myeloid_antiTNF | Mono_macro | paired_change | remission | mif_cd74_receptor_state__resid_ifn_apc_inflammatory_nfkb | 13 | 0 | 0.6288 | 0.001557 | 0.03327 |
| GSE282122_IBD_myeloid_antiTNF | DC | paired_change | remission | hla_ii_apc | 13 | 0 | 0.3898 | 0.001566 | 0.03327 |
| GSE282122_IBD_myeloid_antiTNF | Mono_macro | delta_post_minus_pre | remission_vs_nonremission | mif_cd74_receptor_state__resid_ifn_apc_inflammatory_nfkb | 13 | 16 | 1.236 | 0.002008 | 0.03679 |
| GSE282122_IBD_myeloid_antiTNF | DC | delta_post_minus_pre | remission_vs_nonremission | lipid_loader_repair__resid_inflammatory_nfkb | 13 | 16 | -1.218 | 0.002164 | 0.03679 |
| GSE282122_IBD_myeloid_antiTNF | Mono_macro | delta_post_minus_pre | remission_vs_nonremission | hla_ii_apc__resid_ifn_apc_inflammatory_nfkb | 13 | 16 | 1.201 | 0.002607 | 0.03815 |
| GSE282122_IBD_myeloid_antiTNF | DC | paired_change | remission | mif_cd74_receptor_state__resid_inflammatory_nfkb | 13 | 0 | 0.268 | 0.002889 | 0.03815 |
| GSE282122_IBD_myeloid_antiTNF | Mono_macro | paired_change | remission | hla_ii_apc__resid_inflammatory_nfkb | 13 | 0 | 0.7367 | 0.003101 | 0.03815 |
| GSE282122_IBD_myeloid_antiTNF | Mono_macro | paired_change | remission | mif_cd74_receptor_state__resid_inflammatory_nfkb | 13 | 0 | 0.6041 | 0.003142 | 0.03815 |
| GSE282122_IBD_myeloid_antiTNF | Mono_macro | delta_post_minus_pre | remission_vs_nonremission | mif_cd74_receptor_state__resid_inflammatory_nfkb | 13 | 16 | 1.129 | 0.004084 | 0.04575 |
| GSE282122_IBD_myeloid_antiTNF | DC | delta_post_minus_pre | remission_vs_nonremission | lipid_loader_repair | 13 | 16 | -1.176 | 0.004306 | 0.04575 |
| GSE282122_IBD_myeloid_antiTNF | DC | paired_change | remission | mif_cd74_receptor_state | 13 | 0 | 0.292 | 0.004913 | 0.04775 |
| GSE282122_IBD_myeloid_antiTNF | Mono_macro | delta_post_minus_pre | remission_vs_nonremission | mif_cd74_receptor_state | 13 | 16 | 1.099 | 0.005056 | 0.04775 |
| GSE282122_IBD_myeloid_antiTNF | DC | delta_post_minus_pre | remission_vs_nonremission | lysosomal_apc__resid_inflammatory_nfkb | 13 | 16 | -1.094 | 0.005623 | 0.04842 |
| GSE282122_IBD_myeloid_antiTNF | Mono_macro | paired_change | remission | mif_cd74_receptor_state | 13 | 0 | 0.5863 | 0.005865 | 0.04842 |
| GSE282122_IBD_myeloid_antiTNF | Mono_macro | delta_post_minus_pre | remission_vs_nonremission | hla_ii_apc__resid_inflammatory_nfkb | 13 | 16 | 1.065 | 0.006146 | 0.04842 |
| GSE282122_IBD_myeloid_antiTNF | Mono_macro | paired_change | remission | hla_ii_apc | 13 | 0 | 0.7137 | 0.006266 | 0.04842 |
| GSE282122_IBD_myeloid_antiTNF | Mono_macro | delta_post_minus_pre | remission_vs_nonremission | hla_ii_apc | 13 | 16 | 1.034 | 0.007638 | 0.05636 |
| GSE282122_IBD_myeloid_antiTNF | DC | paired_change | remission | lipid_loader_repair__resid_ifn_apc_inflammatory_nfkb | 13 | 0 | -0.2149 | 0.008113 | 0.05636 |
| GSE282122_IBD_myeloid_antiTNF | DC | delta_post_minus_pre | remission_vs_nonremission | lysosomal_apc | 13 | 16 | -1.061 | 0.008288 | 0.05636 |
| GSE282122_IBD_myeloid_antiTNF | DC | delta_post_minus_pre | remission_vs_nonremission | hla_ii_apc__resid_inflammatory_nfkb | 13 | 16 | 0.9849 | 0.008882 | 0.05807 |
| GSE282122_IBD_myeloid_antiTNF | DC | delta_post_minus_pre | remission_vs_nonremission | lysosomal_apc__resid_ifn_apc_inflammatory_nfkb | 13 | 16 | -0.9869 | 0.0111 | 0.06991 |
| GSE282122_IBD_myeloid_antiTNF | DC | baseline_pre | remission_vs_nonremission | ifn_lysosomal_apc_composite | 13 | 16 | 0.9478 | 0.01168 | 0.07092 |
| GSE282122_IBD_myeloid_antiTNF | DC | baseline_pre | remission_vs_nonremission | ifn_lysosomal_apc_composite__resid_inflammatory_nfkb | 13 | 16 | 0.9103 | 0.01529 | 0.08964 |
| GSE282122_IBD_myeloid_antiTNF | DC | paired_change | nonremission | lipid_loader_repair__resid_ifn_apc_inflammatory_nfkb | 16 | 0 | 0.1754 | 0.01624 | 0.09202 |
| GSE282122_IBD_myeloid_antiTNF | DC | delta_post_minus_pre | remission_vs_nonremission | hla_ii_apc | 13 | 16 | 0.8945 | 0.01746 | 0.09573 |
| GSE282122_IBD_myeloid_antiTNF | DC | paired_change | remission | lipid_loader_repair | 13 | 0 | -0.2546 | 0.01811 | 0.09618 |
| GSE282122_IBD_myeloid_antiTNF | DC | paired_change | remission | lipid_loader_repair__resid_inflammatory_nfkb | 13 | 0 | -0.1954 | 0.01874 | 0.09653 |
| GSE282122_IBD_myeloid_antiTNF | DC | delta_post_minus_pre | remission_vs_nonremission | mif_cd74_receptor_state__resid_ifn_apc_inflammatory_nfkb | 13 | 16 | 0.851 | 0.01972 | 0.09839 |
| GSE282122_IBD_myeloid_antiTNF | DC | baseline_pre | remission_vs_nonremission | lysosomal_apc | 13 | 16 | 0.8878 | 0.02039 | 0.09839 |
| GSE282122_IBD_myeloid_antiTNF | DC | delta_post_minus_pre | remission_vs_nonremission | ifn_lysosomal_apc_composite__resid_inflammatory_nfkb | 13 | 16 | -0.8986 | 0.02084 | 0.09839 |
| GSE282122_IBD_myeloid_antiTNF | Mono_macro | paired_change | remission | lipid_loader_repair__resid_ifn_apc_inflammatory_nfkb | 13 | 0 | -0.2363 | 0.02408 | 0.1074 |
| GSE282122_IBD_myeloid_antiTNF | Mono_macro | delta_post_minus_pre | remission_vs_nonremission | lipid_loader_repair | 13 | 16 | -0.893 | 0.02456 | 0.1074 |
| GSE282122_IBD_myeloid_antiTNF | DC | paired_change | remission | lysosomal_apc | 13 | 0 | -0.236 | 0.02465 | 0.1074 |
| GSE282122_IBD_myeloid_antiTNF | DC | paired_change | remission | lysosomal_apc__resid_inflammatory_nfkb | 13 | 0 | -0.1962 | 0.02832 | 0.1204 |
| GSE282122_IBD_myeloid_antiTNF | DC | delta_post_minus_pre | remission_vs_nonremission | ifn_lysosomal_apc_composite | 13 | 16 | -0.843 | 0.02957 | 0.1226 |
| GSE282122_IBD_myeloid_antiTNF | DC | paired_change | all_patients | hla_ii_apc | 29 | 0 | 0.1838 | 0.03284 | 0.1329 |
| GSE282122_IBD_myeloid_antiTNF | DC | paired_change | remission | lysosomal_apc__resid_ifn_apc_inflammatory_nfkb | 13 | 0 | -0.18 | 0.03513 | 0.1389 |
| GSE282122_IBD_myeloid_antiTNF | DC | baseline_pre | remission_vs_nonremission | lysosomal_apc__resid_inflammatory_nfkb | 13 | 16 | 0.7898 | 0.0392 | 0.1514 |
| GSE282122_IBD_myeloid_antiTNF | DC | paired_change | all_patients | hla_ii_apc__resid_inflammatory_nfkb | 29 | 0 | 0.1585 | 0.04043 | 0.1527 |
| GSE282122_IBD_myeloid_antiTNF | Mono_macro | baseline_pre | remission_vs_nonremission | mif_cd74_receptor_state__resid_ifn_apc_inflammatory_nfkb | 13 | 16 | -0.7848 | 0.04261 | 0.1575 |
| GSE282122_IBD_myeloid_antiTNF | Mono_macro | paired_change | remission | lipid_loader_repair__resid_inflammatory_nfkb | 13 | 0 | -0.2263 | 0.0477 | 0.169 |
| GSE282122_IBD_myeloid_antiTNF | Mono_macro | paired_change | remission | lysosomal_apc__resid_inflammatory_nfkb | 13 | 0 | -0.2143 | 0.04773 | 0.169 |
| GSE282122_IBD_myeloid_antiTNF | DC | paired_change | nonremission | lipid_loader_repair__resid_inflammatory_nfkb | 16 | 0 | 0.1499 | 0.05464 | 0.1896 |
| GSE282122_IBD_myeloid_antiTNF | Mono_macro | delta_post_minus_pre | remission_vs_nonremission | lipid_loader_repair__resid_ifn_apc_inflammatory_nfkb | 13 | 16 | -0.6997 | 0.05836 | 0.1984 |
| GSE282122_IBD_myeloid_antiTNF | DC | baseline_pre | remission_vs_nonremission | ifn_apc | 13 | 16 | 0.702 | 0.06062 | 0.2005 |
| GSE282122_IBD_myeloid_antiTNF | Mono_macro | paired_change | all_patients | hla_ii_apc__resid_ifn_apc_inflammatory_nfkb | 29 | 0 | 0.293 | 0.06206 | 0.2005 |
| GSE282122_IBD_myeloid_antiTNF | Mono_macro | paired_change | remission | lysosomal_apc__resid_ifn_apc_inflammatory_nfkb | 13 | 0 | -0.206 | 0.06325 | 0.2005 |
| GSE282122_IBD_myeloid_antiTNF | Mono_macro | delta_post_minus_pre | remission_vs_nonremission | lipid_loader_repair__resid_inflammatory_nfkb | 13 | 16 | -0.7002 | 0.06376 | 0.2005 |
| GSE282122_IBD_myeloid_antiTNF | DC | baseline_pre | remission_vs_nonremission | ifn_apc__resid_inflammatory_nfkb | 13 | 16 | 0.6908 | 0.06487 | 0.2005 |
| GSE282122_IBD_myeloid_antiTNF | DC | baseline_pre | remission_vs_nonremission | hla_ii_apc__resid_ifn_apc_inflammatory_nfkb | 13 | 16 | -0.6638 | 0.06611 | 0.2007 |
| GSE282122_IBD_myeloid_antiTNF | Mono_macro | paired_change | nonremission | lipid_loader_repair | 16 | 0 | 0.1564 | 0.07905 | 0.2358 |
| GSE282122_IBD_myeloid_antiTNF | DC | baseline_pre | remission_vs_nonremission | mif_cd74_receptor_state__resid_ifn_apc_inflammatory_nfkb | 13 | 16 | -0.6186 | 0.08276 | 0.2384 |
| GSE282122_IBD_myeloid_antiTNF | DC | delta_post_minus_pre | remission_vs_nonremission | mif_cd74_receptor_state__resid_inflammatory_nfkb | 13 | 16 | 0.6151 | 0.08351 | 0.2384 |
| GSE282122_IBD_myeloid_antiTNF | Mono_macro | paired_change | all_patients | lysosomal_apc__resid_inflammatory_nfkb | 29 | 0 | -0.1189 | 0.08479 | 0.2384 |

## Module Gene Coverage

| module | n_defined | n_present | genes_present | genes_missing | dataset |
| --- | --- | --- | --- | --- | --- |
| ifn_apc | 8 | 8 | STAT1;IRF1;CXCL10;GBP1;CD74;IFI30;HLA-DRA;HLA-DRB1 |  | GSE198520_RA_synovium_antiTNF |
| hla_ii_apc | 7 | 7 | CD74;HLA-DRA;HLA-DRB1;HLA-DPA1;HLA-DPB1;CIITA;RFX5 |  | GSE198520_RA_synovium_antiTNF |
| lysosomal_apc | 7 | 7 | IFI30;CTSS;CTSB;CTSD;LAMP1;LAMP2;LAMP3 |  | GSE198520_RA_synovium_antiTNF |
| mif_cd74_receptor_state | 7 | 7 | CD74;CD44;CXCR4;HLA-DRA;HLA-DRB1;HLA-DPA1;HLA-DPB1 |  | GSE198520_RA_synovium_antiTNF |
| lipid_loader_repair | 12 | 12 | ACSL1;APOE;GPNMB;LPL;PLIN2;CD36;LIPA;FABP5;TREM2;MSR1;MERTK;SPP1 |  | GSE198520_RA_synovium_antiTNF |
| inflammatory_nfkb | 9 | 9 | IL1B;TNF;CXCL8;CCL2;CCL3;CCL4;NFKBIA;TREM1;OSM |  | GSE198520_RA_synovium_antiTNF |
| ifn_apc | 8 | 8 | STAT1;IRF1;CXCL10;GBP1;CD74;IFI30;HLA-DRA;HLA-DRB1 |  | GSE282122_IBD_myeloid_antiTNF |
| hla_ii_apc | 7 | 7 | CD74;HLA-DRA;HLA-DRB1;HLA-DPA1;HLA-DPB1;CIITA;RFX5 |  | GSE282122_IBD_myeloid_antiTNF |
| lysosomal_apc | 7 | 7 | IFI30;CTSS;CTSB;CTSD;LAMP1;LAMP2;LAMP3 |  | GSE282122_IBD_myeloid_antiTNF |
| mif_cd74_receptor_state | 7 | 7 | CD74;CD44;CXCR4;HLA-DRA;HLA-DRB1;HLA-DPA1;HLA-DPB1 |  | GSE282122_IBD_myeloid_antiTNF |
| lipid_loader_repair | 12 | 12 | ACSL1;APOE;GPNMB;LPL;PLIN2;CD36;LIPA;FABP5;TREM2;MSR1;MERTK;SPP1 |  | GSE282122_IBD_myeloid_antiTNF |
| inflammatory_nfkb | 9 | 9 | IL1B;TNF;CXCL8;CCL2;CCL3;CCL4;NFKBIA;TREM1;OSM |  | GSE282122_IBD_myeloid_antiTNF |

## Interpretation Guardrails

- RA GSE198520 is bulk synovium, not cell-resolved myeloid data.
- IBD GSE282122 is cell-resolved, but this analysis uses patient-collapsed
  pseudobulk module scores, not causal perturbation.
- Directionally unstable RA/IBD effects block a stratification claim even if
  one dataset has nominal p-values.
