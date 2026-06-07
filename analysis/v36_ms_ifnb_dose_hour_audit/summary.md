# V36 MS IFN-beta Dose/Hour Audit

This re-tests the held `GSE138064` IFN-beta artifact with AUC and a
fixed-seed label-permutation null, complementing the prior Welch-only
summary.

## Top Features

| subset | feature | n | n_complete | n_partial | auc_high_score_complete | auc_permutation_p | hedges_g_complete_minus_partial | welch_p |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stable_hour_4 | delta__receptor_only_cd74_cd44_cxcr4 | 52 | 24 | 28 | 0.6935 | 0.00735 | 0.6084 | 0.03276 |
| stable_8MU | delta__receptor_only_cd74_cd44_cxcr4 | 52 | 24 | 28 | 0.6875 | 0.01075 | 0.6556 | 0.01801 |
| all | baseline__hla_ii_without_cd74 | 133 | 48 | 85 | 0.6853 | 0.00025 | 0.6992 | 0.0001001 |
| stable_8MU | baseline__hla_ii_without_cd74 | 52 | 24 | 28 | 0.6845 | 0.0107 | 0.8198 | 0.004169 |
| stable_hour_4 | baseline__hla_ii_without_cd74 | 52 | 24 | 28 | 0.6592 | 0.02475 | 0.6436 | 0.01998 |
| stable_all_dose | delta__receptor_only_cd74_cd44_cxcr4 | 103 | 48 | 55 | 0.6557 | 0.0031 | 0.5101 | 0.01029 |
| stable_all_dose | baseline__hla_ii_without_cd74 | 103 | 48 | 55 | 0.653 | 0.0036 | 0.6279 | 0.001505 |
| stable_16MU | delta__cd74_alone | 51 | 24 | 27 | 0.6497 | 0.0341 | 0.556 | 0.04814 |
| stable_hour_24 | baseline__hla_ii_without_cd74 | 51 | 24 | 27 | 0.6466 | 0.0394 | 0.5885 | 0.03555 |
| all | delta__receptor_only_cd74_cd44_cxcr4 | 133 | 48 | 85 | 0.6363 | 0.00425 | 0.38 | 0.03223 |
| stable_hour_24 | delta__receptor_only_cd74_cd44_cxcr4 | 51 | 24 | 27 | 0.625 | 0.0627 | 0.4302 | 0.1211 |
| stable_8MU | baseline__ifn_apc | 52 | 24 | 28 | 0.625 | 0.0633 | 0.2324 | 0.394 |

## Full Table

| subset | feature | n | n_complete | n_partial | auc_high_score_complete | auc_permutation_p | hedges_g_complete_minus_partial | welch_p |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| all | baseline__hla_ii_without_cd74 | 133 | 48 | 85 | 0.6853 | 0.00025 | 0.6992 | 0.0001001 |
| all | baseline__ifn_apc | 133 | 48 | 85 | 0.5667 | 0.1002 | 0.2311 | 0.1773 |
| all | baseline__receptor_only_cd74_cd44_cxcr4 | 133 | 48 | 85 | 0.5363 | 0.2507 | 0.1172 | 0.518 |
| all | delta__cd74_alone | 133 | 48 | 85 | 0.6069 | 0.01965 | 0.4158 | 0.01987 |
| all | delta__hla_ii_without_cd74 | 133 | 48 | 85 | 0.5892 | 0.0451 | 0.3141 | 0.07372 |
| all | delta__ifn_apc | 133 | 48 | 85 | 0.5142 | 0.3876 | 0.06681 | 0.7044 |
| all | delta__receptor_only_cd74_cd44_cxcr4 | 133 | 48 | 85 | 0.6363 | 0.00425 | 0.38 | 0.03223 |
| all | locked_style_score | 133 | 48 | 85 | 0.5404 | 0.2222 | 0.1321 | 0.4694 |
| all | negative_delta_ifn_apc | 133 | 48 | 85 | 0.4858 | 0.6144 | -0.06681 | 0.7044 |
| all | negative_delta_receptor | 133 | 48 | 85 | 0.3637 | 0.9959 | -0.38 | 0.03223 |
| stable_16MU | baseline__hla_ii_without_cd74 | 51 | 24 | 27 | 0.6049 | 0.1016 | 0.4425 | 0.1071 |
| stable_16MU | baseline__ifn_apc | 51 | 24 | 27 | 0.5185 | 0.4153 | 0.2174 | 0.4231 |
| stable_16MU | baseline__receptor_only_cd74_cd44_cxcr4 | 51 | 24 | 27 | 0.4352 | 0.7896 | -0.2717 | 0.343 |
| stable_16MU | delta__cd74_alone | 51 | 24 | 27 | 0.6497 | 0.0341 | 0.556 | 0.04814 |
| stable_16MU | delta__hla_ii_without_cd74 | 51 | 24 | 27 | 0.5941 | 0.125 | 0.3942 | 0.1513 |
| stable_16MU | delta__ifn_apc | 51 | 24 | 27 | 0.5278 | 0.3702 | 0.1491 | 0.5893 |
| stable_16MU | delta__receptor_only_cd74_cd44_cxcr4 | 51 | 24 | 27 | 0.6204 | 0.0689 | 0.3219 | 0.2564 |
| stable_16MU | locked_style_score | 51 | 24 | 27 | 0.5231 | 0.3911 | 0.1169 | 0.673 |
| stable_16MU | negative_delta_ifn_apc | 51 | 24 | 27 | 0.4722 | 0.6366 | -0.1491 | 0.5893 |
| stable_16MU | negative_delta_receptor | 51 | 24 | 27 | 0.3796 | 0.9337 | -0.3219 | 0.2564 |
| stable_8MU | baseline__hla_ii_without_cd74 | 52 | 24 | 28 | 0.6845 | 0.0107 | 0.8198 | 0.004169 |
| stable_8MU | baseline__ifn_apc | 52 | 24 | 28 | 0.625 | 0.0633 | 0.2324 | 0.394 |
| stable_8MU | baseline__receptor_only_cd74_cd44_cxcr4 | 52 | 24 | 28 | 0.494 | 0.5338 | -0.07171 | 0.7929 |
| stable_8MU | delta__cd74_alone | 52 | 24 | 28 | 0.5074 | 0.4687 | 0.07118 | 0.7967 |
| stable_8MU | delta__hla_ii_without_cd74 | 52 | 24 | 28 | 0.4955 | 0.5232 | -0.05789 | 0.8358 |
| stable_8MU | delta__ifn_apc | 52 | 24 | 28 | 0.4449 | 0.7511 | -0.1871 | 0.4948 |
| stable_8MU | delta__receptor_only_cd74_cd44_cxcr4 | 52 | 24 | 28 | 0.6875 | 0.01075 | 0.6556 | 0.01801 |
| stable_8MU | locked_style_score | 52 | 24 | 28 | 0.5506 | 0.2703 | 0.1044 | 0.7071 |
| stable_8MU | negative_delta_ifn_apc | 52 | 24 | 28 | 0.5551 | 0.2539 | 0.1871 | 0.4948 |
| stable_8MU | negative_delta_receptor | 52 | 24 | 28 | 0.3125 | 0.9899 | -0.6556 | 0.01801 |
| stable_all_dose | baseline__hla_ii_without_cd74 | 103 | 48 | 55 | 0.653 | 0.0036 | 0.6279 | 0.001505 |
| stable_all_dose | baseline__ifn_apc | 103 | 48 | 55 | 0.5727 | 0.1031 | 0.2294 | 0.2346 |
| stable_all_dose | baseline__receptor_only_cd74_cd44_cxcr4 | 103 | 48 | 55 | 0.4621 | 0.744 | -0.149 | 0.4504 |
| stable_all_dose | delta__cd74_alone | 103 | 48 | 55 | 0.5792 | 0.0858 | 0.3223 | 0.102 |
| stable_all_dose | delta__hla_ii_without_cd74 | 103 | 48 | 55 | 0.5413 | 0.2401 | 0.168 | 0.3889 |
| stable_all_dose | delta__ifn_apc | 103 | 48 | 55 | 0.4924 | 0.5512 | -0.01425 | 0.9419 |
| stable_all_dose | delta__receptor_only_cd74_cd44_cxcr4 | 103 | 48 | 55 | 0.6557 | 0.0031 | 0.5101 | 0.01029 |
| stable_all_dose | locked_style_score | 103 | 48 | 55 | 0.5352 | 0.2729 | 0.1062 | 0.5896 |
| stable_all_dose | negative_delta_ifn_apc | 103 | 48 | 55 | 0.5076 | 0.4513 | 0.01425 | 0.9419 |
| stable_all_dose | negative_delta_receptor | 103 | 48 | 55 | 0.3443 | 0.9972 | -0.5101 | 0.01029 |
| stable_hour_24 | baseline__hla_ii_without_cd74 | 51 | 24 | 27 | 0.6466 | 0.0394 | 0.5885 | 0.03555 |
| stable_hour_24 | baseline__ifn_apc | 51 | 24 | 27 | 0.5648 | 0.2192 | 0.1932 | 0.4798 |
| stable_hour_24 | baseline__receptor_only_cd74_cd44_cxcr4 | 51 | 24 | 27 | 0.4568 | 0.7059 | -0.161 | 0.5639 |
| stable_hour_24 | delta__cd74_alone | 51 | 24 | 27 | 0.5941 | 0.1272 | 0.3989 | 0.1529 |
| stable_hour_24 | delta__hla_ii_without_cd74 | 51 | 24 | 27 | 0.5556 | 0.2481 | 0.2494 | 0.3607 |
| stable_hour_24 | delta__ifn_apc | 51 | 24 | 27 | 0.5015 | 0.4958 | 0.06887 | 0.8025 |
| stable_hour_24 | delta__receptor_only_cd74_cd44_cxcr4 | 51 | 24 | 27 | 0.625 | 0.0627 | 0.4302 | 0.1211 |
| stable_hour_24 | locked_style_score | 51 | 24 | 27 | 0.5293 | 0.3603 | 0.1666 | 0.5385 |
| stable_hour_24 | negative_delta_ifn_apc | 51 | 24 | 27 | 0.4985 | 0.5115 | -0.06887 | 0.8025 |
| stable_hour_24 | negative_delta_receptor | 51 | 24 | 27 | 0.375 | 0.939 | -0.4302 | 0.1211 |
| stable_hour_4 | baseline__hla_ii_without_cd74 | 52 | 24 | 28 | 0.6592 | 0.02475 | 0.6436 | 0.01998 |
| stable_hour_4 | baseline__ifn_apc | 52 | 24 | 28 | 0.5804 | 0.1679 | 0.2557 | 0.3429 |
| stable_hour_4 | baseline__receptor_only_cd74_cd44_cxcr4 | 52 | 24 | 28 | 0.4673 | 0.656 | -0.1323 | 0.6327 |
| stable_hour_4 | delta__cd74_alone | 52 | 24 | 28 | 0.5699 | 0.1983 | 0.2804 | 0.3076 |
| stable_hour_4 | delta__hla_ii_without_cd74 | 52 | 24 | 28 | 0.5119 | 0.4448 | 0.09307 | 0.7352 |
| stable_hour_4 | delta__ifn_apc | 52 | 24 | 28 | 0.4911 | 0.5485 | -0.0533 | 0.8463 |
| stable_hour_4 | delta__receptor_only_cd74_cd44_cxcr4 | 52 | 24 | 28 | 0.6935 | 0.00735 | 0.6084 | 0.03276 |
| stable_hour_4 | locked_style_score | 52 | 24 | 28 | 0.5104 | 0.4513 | 0.08778 | 0.7531 |
| stable_hour_4 | negative_delta_ifn_apc | 52 | 24 | 28 | 0.5089 | 0.4579 | 0.0533 | 0.8463 |
| stable_hour_4 | negative_delta_receptor | 52 | 24 | 28 | 0.3065 | 0.9931 | -0.6084 | 0.03276 |

## Interpretation

The strongest signals are HLA-II baseline or HLA-II-related IFN-beta
competence signals, not the broad locked-style scalar. This independently
supports therapy-branch interpretation for IFN-beta.
