# Wave89 Psoriasis GSE85034 Response Validation

Question: do the Wave86/Wave87 parked IL1B/LAMP3 anti-TNF nonresponse genes replicate in baseline lesional skin from psoriasis patients treated with adalimumab?

Analysis call: `WEAK_DIRECTIONAL_THIRD_DISEASE_SUPPORT_ONLY`.

## Treatment/Response Counts

| treatment | n_subjects | n_baseline_ls | n_week16 | n_pasi75 | n_pasi75_responders | n_pasi75_nonresponders |
| --- | --- | --- | --- | --- | --- | --- |
| ADA | 15 | 15 | 14 | 14 | 9 | 5 |
| MTX | 15 | 14 | 15 | 13 | 3 | 10 |

## Primary Gene Cross-System View

| gene | treatment | n_subjects | n_pasi75_responders | n_pasi75_nonresponders | effect_responder_minus_non | hedges_g_responder_minus_non | auc_high_score_nonresponse | p | spearman_score_vs_pct_pasi_improvement | psoriasis_adalimumab_support_call | cross_system_call |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IL1B | ADA | 14 | 9 | 5 | -0.796 | -0.6325 | 0.5556 | 0.394 | 0.08132 | PSORIASIS_ADA_SAME_DIRECTION_WEAK | PARK_CROSS_SYSTEM_ANTITNF_RESISTANCE_GENE |
| IL1B | ALL | 27 | 12 | 15 | 0.1229 | 0.1033 | 0.4389 | 0.7823 | 0.07877 | CONTROL_ARM | PARK_CROSS_SYSTEM_ANTITNF_RESISTANCE_GENE |
| IL1B | MTX | 13 | 3 | 10 | 1.37 | 1.318 | 0.2333 | 0.292 | 0.07143 | CONTROL_ARM | PARK_CROSS_SYSTEM_ANTITNF_RESISTANCE_GENE |
| LAMP3 | ADA | 14 | 9 | 5 | 0.2757 | 0.496 | 0.3556 | 0.2968 | 0.2484 | NO_PSORIASIS_ADA_SUPPORT | PARK_CROSS_SYSTEM_ANTITNF_RESISTANCE_GENE |
| LAMP3 | ALL | 27 | 12 | 15 | 0.1861 | 0.2772 | 0.45 | 0.4552 | -0.03847 | CONTROL_ARM | PARK_CROSS_SYSTEM_ANTITNF_RESISTANCE_GENE |
| LAMP3 | MTX | 13 | 3 | 10 | -0.05784 | -0.06687 | 0.6333 | 0.8884 | -0.5604 | CONTROL_ARM | PARK_CROSS_SYSTEM_ANTITNF_RESISTANCE_GENE |

## Top Adalimumab Gene Tests

| feature | n_subjects | n_pasi75_responders | n_pasi75_nonresponders | hedges_g_responder_minus_non | auc_high_score_nonresponse | p | fdr_within_treatment | nonresponse_high_direction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LPL | 14 | 9 | 5 | -2.209 | 0.9556 | 0.01111 | 0.4998 | True |
| NFKBIA | 14 | 9 | 5 | 1.157 | 0.1778 | 0.03297 | 0.7418 | False |
| APOE | 14 | 9 | 5 | 0.7924 | 0.2222 | 0.08558 | 0.8145 | False |
| MERTK | 14 | 9 | 5 | -0.7528 | 0.7111 | 0.1267 | 0.8145 | True |
| LAMP2 | 14 | 9 | 5 | -0.9351 | 0.7778 | 0.1393 | 0.8145 | True |
| TREM1 | 14 | 9 | 5 | -0.8591 | 0.7333 | 0.1455 | 0.8145 | True |
| CTSB | 14 | 9 | 5 | -0.8159 | 0.7111 | 0.1853 | 0.8145 | True |
| IFI30 | 14 | 9 | 5 | -0.6432 | 0.6889 | 0.2911 | 0.8145 | True |
| LAMP3 | 14 | 9 | 5 | 0.496 | 0.3556 | 0.2968 | 0.8145 | False |
| C1QC | 14 | 9 | 5 | -0.6369 | 0.6889 | 0.3035 | 0.8145 | True |
| CD44 | 14 | 9 | 5 | -0.5602 | 0.7556 | 0.3705 | 0.8145 | True |
| CXCR4 | 14 | 9 | 5 | -0.5871 | 0.6444 | 0.3731 | 0.8145 | True |
| CCL3 | 14 | 9 | 5 | -0.5383 | 0.6667 | 0.3867 | 0.8145 | True |
| ACSL1 | 14 | 9 | 5 | 0.4198 | 0.4222 | 0.3925 | 0.8145 | False |
| IL1B | 14 | 9 | 5 | -0.6325 | 0.5556 | 0.394 | 0.8145 | True |
| SPP1 | 14 | 9 | 5 | -0.6407 | 0.5556 | 0.4052 | 0.8145 | True |
| CXCL10 | 14 | 9 | 5 | 0.3867 | 0.3778 | 0.4072 | 0.8145 | False |
| CCL4 | 14 | 9 | 5 | -0.4597 | 0.6667 | 0.4123 | 0.8145 | True |
| C1QB | 14 | 9 | 5 | -0.4958 | 0.6889 | 0.4193 | 0.8145 | True |
| C1QA | 14 | 9 | 5 | -0.3254 | 0.6 | 0.4433 | 0.8145 | True |
| HLA-DRB1 | 14 | 9 | 5 | -0.4205 | 0.6222 | 0.4535 | 0.8145 | True |
| CXCL8 | 14 | 9 | 5 | -0.5175 | 0.5333 | 0.4547 | 0.8145 | True |
| PLIN2 | 14 | 9 | 5 | -0.321 | 0.5333 | 0.4718 | 0.8145 | True |
| GPNMB | 14 | 9 | 5 | 0.3127 | 0.4222 | 0.5055 | 0.8145 | False |
| CTSS | 14 | 9 | 5 | -0.3195 | 0.6222 | 0.514 | 0.8145 | True |
| TNF | 14 | 9 | 5 | -0.2841 | 0.6 | 0.5155 | 0.8145 | True |
| HLA-DPB1 | 14 | 9 | 5 | -0.2798 | 0.6444 | 0.5748 | 0.8145 | True |
| TREM2 | 14 | 9 | 5 | 0.3748 | 0.4222 | 0.5767 | 0.8145 | False |
| STAT1 | 14 | 9 | 5 | 0.3013 | 0.4 | 0.5831 | 0.8145 | False |
| LAMP1 | 14 | 9 | 5 | -0.2965 | 0.5667 | 0.6055 | 0.8145 | True |

## Module Tests

| dataset | disease | tissue | treatment | feature_class | feature | n_subjects | n_pasi75_responders | n_pasi75_nonresponders | mean_score_responder | mean_score_nonresponder | effect_responder_minus_non | hedges_g_responder_minus_non | auc_high_score_response | auc_high_score_nonresponse | p | t | spearman_score_vs_pct_pasi_improvement | spearman_p | nonresponse_high_direction | fdr_within_treatment |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GSE85034 | psoriasis | skin_lesional_baseline | ADA | module | lysosomal_apc | 14 | 9 | 5 | 0.3281 | 0.6477 | -0.3197 | -1.017 | 0.2222 | 0.7778 | 0.1237 | -1.771 | -0.433 | 0.122 | True | 0.6707 |
| GSE85034 | psoriasis | skin_lesional_baseline | ADA | module | complement_phagocytosis | 14 | 9 | 5 | -0.03619 | 0.243 | -0.2792 | -0.5138 | 0.3556 | 0.6444 | 0.3865 | -0.9234 | -0.1956 | 0.5028 | True | 0.6707 |
| GSE85034 | psoriasis | skin_lesional_baseline | ADA | module | mif_cd74_receptor_state | 14 | 9 | 5 | 0.1206 | 0.4004 | -0.2798 | -0.3358 | 0.3333 | 0.6667 | 0.4257 | -0.8289 | -0.4286 | 0.1263 | True | 0.6707 |
| GSE85034 | psoriasis | skin_lesional_baseline | ADA | module | inflammatory_nfkb | 14 | 9 | 5 | 0.2426 | 0.5678 | -0.3252 | -0.5534 | 0.4667 | 0.5333 | 0.4539 | -0.8191 | -0.04176 | 0.8873 | True | 0.6707 |
| GSE85034 | psoriasis | skin_lesional_baseline | ADA | module | lipid_loader_repair | 14 | 9 | 5 | -0.1085 | -0.0373 | -0.07118 | -0.3302 | 0.4 | 0.6 | 0.4791 | -0.731 | 0.002198 | 0.9941 | True | 0.6707 |
| GSE85034 | psoriasis | skin_lesional_baseline | ADA | module | hla_ii_apc | 14 | 9 | 5 | 0.169 | 0.3171 | -0.1481 | -0.154 | 0.3778 | 0.6222 | 0.7264 | -0.3582 | -0.367 | 0.1967 | True | 0.8475 |
| GSE85034 | psoriasis | skin_lesional_baseline | ADA | module | ifn_apc | 14 | 9 | 5 | 0.4414 | 0.4214 | 0.01992 | 0.02465 | 0.6 | 0.4 | 0.9594 | 0.05213 | -0.1121 | 0.7028 | False | 0.9594 |
| GSE85034 | psoriasis | skin_lesional_baseline | ALL | module | inflammatory_nfkb | 27 | 12 | 15 | 0.3528 | 0.2462 | 0.1066 | 0.1977 | 0.6278 | 0.3722 | 0.5855 | 0.5529 | 0.131 | 0.5149 | False | 0.9969 |
| GSE85034 | psoriasis | skin_lesional_baseline | ALL | module | hla_ii_apc | 27 | 12 | 15 | 0.03139 | 0.09461 | -0.06322 | -0.07809 | 0.4278 | 0.5722 | 0.844 | -0.1995 | -0.1902 | 0.342 | True | 0.9969 |
| GSE85034 | psoriasis | skin_lesional_baseline | ALL | module | complement_phagocytosis | 27 | 12 | 15 | -0.05898 | -0.09064 | 0.03166 | 0.0658 | 0.4611 | 0.5389 | 0.8587 | 0.1798 | -0.105 | 0.6021 | False | 0.9969 |
| GSE85034 | psoriasis | skin_lesional_baseline | ALL | module | lipid_loader_repair | 27 | 12 | 15 | -0.08356 | -0.09688 | 0.01332 | 0.05211 | 0.4889 | 0.5111 | 0.887 | 0.1435 | -0.05892 | 0.7703 | False | 0.9969 |
| GSE85034 | psoriasis | skin_lesional_baseline | ALL | module | mif_cd74_receptor_state | 27 | 12 | 15 | 0.07132 | 0.08752 | -0.0162 | -0.0239 | 0.4556 | 0.5444 | 0.9527 | -0.06022 | -0.1072 | 0.5947 | True | 0.9969 |
| GSE85034 | psoriasis | skin_lesional_baseline | ALL | module | lysosomal_apc | 27 | 12 | 15 | 0.3344 | 0.3352 | -0.0008284 | -0.002092 | 0.4444 | 0.5556 | 0.9953 | -0.005957 | -0.2278 | 0.2532 | True | 0.9969 |
| GSE85034 | psoriasis | skin_lesional_baseline | ALL | module | ifn_apc | 27 | 12 | 15 | 0.3477 | 0.3467 | 0.0009965 | 0.001535 | 0.5333 | 0.4667 | 0.9969 | 0.003947 | -0.0864 | 0.6683 | False | 0.9969 |
| GSE85034 | psoriasis | skin_lesional_baseline | MTX | module | inflammatory_nfkb | 13 | 3 | 10 | 0.6832 | 0.08535 | 0.5978 | 1.308 | 0.8667 | 0.1333 | 0.1736 | 1.827 | 0.1703 | 0.578 | False | 0.4574 |
| GSE85034 | psoriasis | skin_lesional_baseline | MTX | module | hla_ii_apc | 13 | 3 | 10 | -0.3813 | -0.01664 | -0.3647 | -0.5234 | 0.3 | 0.7 | 0.2407 | -1.265 | -0.5385 | 0.05763 | True | 0.4574 |
| GSE85034 | psoriasis | skin_lesional_baseline | MTX | module | ifn_apc | 13 | 3 | 10 | 0.06662 | 0.3093 | -0.2427 | -0.4571 | 0.5333 | 0.4667 | 0.2807 | -1.147 | -0.1923 | 0.5291 | True | 0.4574 |
| GSE85034 | psoriasis | skin_lesional_baseline | MTX | module | lipid_loader_repair | 13 | 3 | 10 | -0.008816 | -0.1267 | 0.1179 | 0.3639 | 0.5667 | 0.4333 | 0.3577 | 0.9625 | -0.03297 | 0.9149 | False | 0.4574 |
| GSE85034 | psoriasis | skin_lesional_baseline | MTX | module | complement_phagocytosis | 13 | 3 | 10 | -0.1273 | -0.2575 | 0.1301 | 0.3295 | 0.5 | 0.5 | 0.3693 | 0.9363 | -0.2527 | 0.4048 | False | 0.4574 |
| GSE85034 | psoriasis | skin_lesional_baseline | MTX | module | lysosomal_apc | 13 | 3 | 10 | 0.3534 | 0.179 | 0.1744 | 0.389 | 0.5667 | 0.4333 | 0.3921 | 0.9091 | -0.4341 | 0.1383 | False | 0.4574 |
| GSE85034 | psoriasis | skin_lesional_baseline | MTX | module | mif_cd74_receptor_state | 13 | 3 | 10 | -0.07656 | -0.06895 | -0.007614 | -0.01437 | 0.4333 | 0.5667 | 0.981 | -0.02539 | -0.4011 | 0.1744 | True | 0.981 |

## Guardrails

- GSE85034 has only 30 subjects total and the adalimumab arm is small; this is a third-disease stress test, not a standalone classifier.
- PASI75 is reconstructed from GEO PASI fields; no hidden responder labels were inferred.
- Subject 28 lacks a baseline `LS` sample and is excluded from baseline-lesional response tests.
- A positive result would still not overcome IL1B/LAMP3 prior-art and targetability blocks without an intervention handle.
