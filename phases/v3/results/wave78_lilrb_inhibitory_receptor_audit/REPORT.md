# Wave78 LILRB Inhibitory-Receptor Family Audit

## Question

Does any LILRB-family inhibitory receptor survive as a target-level
cross-autoimmune/MS intervention point after adjusted treatment-response
specificity, MS guardrails, genetics, model-direction, and intervention
route checks?

## Verdict

PARK_LILRB_DIRECTIONALLY_UNRESOLVED

## Integrated Decision

| gene | wave78_call | gate_count | gate_breadth_ge3_diseases | gate_adjusted_ra_ibd_response_specific | gate_ms_positive_anchor | gate_ms_nonnegative_guardrail | gate_cross_disease_genetics | gate_foundation_model_direction | gate_direct_perturbation | gate_nonblocked_intervention_route | positive_disease_count | positive_diseases | ms_delta_log2 | ms_p | ms_fdr | qtl_strong_h4_disease_count | qtl_strong_h4_diseases | wave62_call | best_response_endpoint | ra_response_p | ibd_response_p | ra_target_generic_abs_ratio | ibd_target_generic_abs_ratio | direction_model_call | wave70_call | wave37_call | decision_reason | is_lilrb_target |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LILRB4 | PARK_LILRB_DIRECTIONALLY_UNRESOLVED | 2 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 |  | -0.05671 | 0.8864 | 0.9842 | 2 | Psoriasis;RA |  | baseline_pre | 0.859 | 0.008191 | 0.4543 | 5.187 | NO_GO_MODEL_DIRECTION_SCREEN | NO_GO_INSUFFICIENT_CONVERGENCE |  | some target-level signal exists but MS, specificity, model direction, or intervention route is insufficient | True |
| LILRB5 | NO_GO_LILRB_LOCAL_AUDIT | 2 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0 |  | -0.8825 | 0.5157 | 0.9345 | 0 |  |  |  |  |  |  |  |  |  |  | does not pass target-level local gates | True |
| LILRB1 | PARK_LILRB_DIRECTIONALLY_UNRESOLVED | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 2 | Crohn disease;ulcerative colitis | -0.248 | 0.3035 | 0.9075 | 0 |  |  | baseline_pre | 0.5066 | 0.1118 | 4.743 | 2.409 | NO_GO_MODEL_DIRECTION_SCREEN | NO_GO_INSUFFICIENT_CONVERGENCE |  | some target-level signal exists but MS, specificity, model direction, or intervention route is insufficient | True |
| LILRB2 | PARK_LILRB_DIRECTIONALLY_UNRESOLVED | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 2 | Crohn disease;ulcerative colitis | -0.7297 | 0.007784 | 0.8345 | 2 | Crohn;T1D |  | delta_post_minus_pre | 0.5608 | 0.008671 | 0.7112 | 43.97 | NO_GO_MODEL_DIRECTION_SCREEN | NO_GO_INSUFFICIENT_CONVERGENCE |  | some target-level signal exists but MS, specificity, model direction, or intervention route is insufficient | True |
| LILRB3 | PARK_LILRB_DIRECTIONALLY_UNRESOLVED | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 2 | Crohn disease;ulcerative colitis | -0.377 | 0.504 | 0.9299 | 0 |  |  | delta_post_minus_pre | 0.1542 | 0.1344 | 6.732 | 13.57 | NO_GO_MODEL_DIRECTION_SCREEN | NO_GO_INSUFFICIENT_CONVERGENCE |  | some target-level signal exists but MS, specificity, model direction, or intervention route is insufficient | True |
| FCGR2B | NO_GO_LILRB_LOCAL_AUDIT | 3 | 0 | 1 | 0 | 1 | 1 | 0 | 0 | 0 | 0 |  | 0.3744 | 0.5996 | 0.9467 | 4 | AS;Crohn;SLE;UC | NO_GO_WAVE62_TARGET_RESOLUTION | baseline_pre | 0.001639 | 0.01444 | 12.6 | 4.746 | MODEL_OPPOSING_BUT_BLOCKED_COMPARATOR | NO_GO_BLOCKED_OR_BROAD_CLASS |  | does not pass target-level local gates | False |
| LAIR1 | NO_GO_LILRB_LOCAL_AUDIT | 2 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 1 | type 1 diabetes mellitus | -0.2811 | 0.1069 | 0.8989 | 2 | Celiac;RA |  | baseline_pre | 0.2231 | 0.2093 | 6.222 | 2.239 | NO_GO_MODEL_DIRECTION_SCREEN | NO_GO_INSUFFICIENT_CONVERGENCE |  | does not pass target-level local gates | False |
| CD300LF | NO_GO_LILRB_LOCAL_AUDIT | 2 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 1 | psoriasis | -0.09912 | 0.709 | 0.9669 | 2 | Crohn;RA |  | baseline_pre | 0.5184 | 0.7217 | 2.981 | 0.6119 | NO_GO_LOW_TOKEN_SUPPORT | NO_GO_INSUFFICIENT_CONVERGENCE |  | does not pass target-level local gates | False |
| CD300A | NO_GO_LILRB_LOCAL_AUDIT | 2 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 |  | -0.3453 | 0.07661 | 0.8989 | 2 | Celiac;T1D |  | baseline_pre | 0.348 | 0.396 | 4.146 | 1.196 | NO_GO_LOW_TOKEN_SUPPORT | NO_GO_INSUFFICIENT_CONVERGENCE |  | does not pass target-level local gates | False |
| INPP5D | NO_GO_LILRB_LOCAL_AUDIT | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |  | -0.3038 | 0.0944 | 0.8989 | 0 |  | NO_GO_WAVE62_TARGET_RESOLUTION | delta_post_minus_pre | 0.01134 | 0.0825 | 3.374 | 1.194 | NO_GO_MODEL_DIRECTION_SCREEN | NO_GO_INSUFFICIENT_CONVERGENCE |  | does not pass target-level local gates | False |

## Broad Disease Cell-State Summary

| gene | contexts_tested | positive_contexts | negative_contexts | positive_disease_count | positive_diseases | negative_disease_count | negative_diseases | best_context | best_disease | best_delta_log2_cpm | best_p | best_fdr |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LILRB2 | 4 | 2 | 0 | 2 | Crohn disease;ulcerative colitis | 0 |  | ibd_crohn_myeloid | Crohn disease | 1.383 | 0.0003013 | 0.0707 |
| LILRB1 | 11 | 2 | 0 | 2 | Crohn disease;ulcerative colitis | 0 |  | ibd_crohn_myeloid | Crohn disease | 1.269 | 0.006744 | 0.2023 |
| LILRB3 | 14 | 2 | 0 | 2 | Crohn disease;ulcerative colitis | 0 |  | ibd_uc_myeloid | ulcerative colitis | 1.687 | 0.006776 | 0.2006 |
| LAIR1 | 14 | 2 | 2 | 1 | type 1 diabetes mellitus | 2 | Crohn disease;ulcerative colitis | ibd_crohn_myeloid | Crohn disease | -0.8834 | 0.004651 | 0.1738 |
| CD300LF | 8 | 1 | 0 | 1 | psoriasis | 0 |  | psoriasis_skin_apc | psoriasis | 2.246 | 0.03292 | 0.7297 |
| FCGR2B | 12 | 0 | 1 | 0 |  | 1 | ulcerative colitis | ibd_uc_stromal | ulcerative colitis | -1.934 | 0.008869 | 0.2055 |
| LILRB5 | 6 | 0 | 1 | 0 |  | 1 | ulcerative colitis | ibd_uc_myeloid | ulcerative colitis | -3.237 | 0.01699 | 0.2764 |
| LILRB4 | 10 | 0 | 0 | 0 |  | 0 |  | t1d_ductal_cell | type 1 diabetes mellitus | 0.3285 | 0.046 | 0.4708 |
| INPP5D | 16 | 0 | 0 | 0 |  | 0 |  | psoriasis_skin_stromal | psoriasis | 0.7026 | 0.07523 | 0.5993 |
| CD300A | 13 | 0 | 0 | 0 |  | 0 |  | psoriasis_keratinocyte | psoriasis | -0.28 | 0.08039 | 0.4328 |

## MS White-Matter Rows

| gene | mean_case | mean_control | delta_log2 | hedges_g | welch_t | p | fdr | ms_positive_anchor | ms_nominal_down | ms_nonnegative_guardrail |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LILRB2 | 8.555 | 9.284 | -0.7297 | -1.34 | -3.111 | 0.007784 | 0.8345 | False | True | False |
| CD300A | 11.09 | 11.43 | -0.3453 | -0.7766 | -1.875 | 0.07661 | 0.8989 | False | False | True |
| INPP5D | 13.09 | 13.4 | -0.3038 | -0.7287 | -1.765 | 0.0944 | 0.8989 | False | False | True |
| LAIR1 | 11.94 | 12.22 | -0.2811 | -0.7152 | -1.696 | 0.1069 | 0.8989 | False | False | True |
| LILRB1 | 10.96 | 11.21 | -0.248 | -0.4629 | -1.071 | 0.3035 | 0.9075 | False | False | True |
| LILRB3 | 8.754 | 9.13 | -0.377 | -0.2821 | -0.6816 | 0.504 | 0.9299 | False | False | True |
| LILRB5 | 4.584 | 5.467 | -0.8825 | -0.2793 | -0.6628 | 0.5157 | 0.9345 | False | False | True |
| FCGR2B | 8.952 | 8.578 | 0.3744 | 0.2224 | 0.5339 | 0.5996 | 0.9467 | False | False | True |
| CD300LF | 8.814 | 8.913 | -0.09912 | -0.1661 | -0.3823 | 0.709 | 0.9669 | False | False | True |
| LILRB4 | 11.78 | 11.83 | -0.05671 | -0.06277 | -0.1455 | 0.8864 | 0.9842 | False | False | True |

## QTL Colocalization Summary

| gene | qtl_coloc_rows | max_h4 | strong_h4_disease_count | strong_h4_diseases | ms_max_h4 | myeloid_relevant_rows |
| --- | --- | --- | --- | --- | --- | --- |
| FCGR2B | 18 | 0.9991 | 4 | AS;Crohn;SLE;UC | 0 | 0 |
| LILRB2 | 2 | 0.9956 | 2 | Crohn;T1D | 0 | 0 |
| LAIR1 | 3 | 0.9956 | 2 | Celiac;RA | 0 | 0 |
| LILRB4 | 2 | 0.9946 | 2 | Psoriasis;RA | 0 | 0 |
| CD300A | 3 | 0.9913 | 2 | Celiac;T1D | 0 | 0 |
| CD300LF | 2 | 0.9884 | 2 | Crohn;RA | 0 | 0 |

## Adjusted RA/IBD Response Convergence

| gene | endpoint | ra_comparison | ra_coef | ra_p | ra_fdr | ra_generic_coef | ra_target_generic_abs_ratio | ibd_cell_state | ibd_coef | ibd_p | ibd_fdr | ibd_generic_coef | ibd_target_generic_abs_ratio | sign_stable | both_p10 | both_ratio_ge2 | response_specificity_pass | priority |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FCGR2B | baseline_pre | good_vs_moderate_none | -0.9793 | 0.001639 | 0.06557 | 0.07772 | 12.6 | DC | -0.7287 | 0.01444 | 0.1155 | 0.1535 | 4.746 | True | True | True | True | 7 |
| INPP5D | delta_post_minus_pre | good_vs_moderate_none | 0.9331 | 0.01134 | 0.1512 | -0.2766 | 3.374 | Mono_macro | 0.4047 | 0.0825 | 0.275 | -0.3389 | 1.194 | True | True | False | False | 3 |
| LAIR1 | baseline_pre | good_vs_moderate_none | 0.4835 | 0.2231 | 0.7429 | 0.07772 | 6.222 | Mono_macro | 0.2507 | 0.2093 | 0.4152 | -0.112 | 2.239 | True | False | True | False | 1 |
| LILRB1 | baseline_pre | good_vs_moderate_none | 0.3687 | 0.5066 | 0.977 | 0.07772 | 4.743 | Mono_macro | 0.2698 | 0.1118 | 0.344 | -0.112 | 2.409 | True | False | True | False | 1 |
| LILRB2 | delta_post_minus_pre | good_vs_moderate_none | -0.1967 | 0.5608 | 0.977 | -0.2766 | 0.7112 | DC | -0.8612 | 0.008671 | 0.08671 | -0.01959 | 43.97 | True | False | False | False | 1 |
| LILRB4 | baseline_pre | moderate_good_vs_none | 0.09485 | 0.859 | 1 | 0.2088 | 0.4543 | Mono_macro | 0.5807 | 0.008191 | 0.08671 | -0.112 | 5.187 | True | False | False | False | 1 |
| LILRB1 | delta_post_minus_pre | good_vs_moderate_none | -4.586e-16 | 0.965 | 1 | -0.2766 | 1.658e-15 | Mono_macro | -0.6899 | 0.008194 | 0.08671 | -0.3389 | 2.036 | True | False | False | False | 1 |
| INPP5D | baseline_pre | good_vs_moderate_none | 0.6644 | 0.03601 | 0.3601 | 0.07772 | 8.549 | DC | -0.1215 | 0.5597 | 0.7524 | 0.1535 | 0.7911 | False | False | False | False | 0 |
| LILRB4 | delta_post_minus_pre | good_vs_moderate_none | 0.4343 | 0.06204 | 0.4856 | -0.2766 | 1.57 | Mono_macro | -0.7631 | 0.00576 | 0.08671 | -0.3389 | 2.252 | False | False | False | False | 0 |
| LAIR1 | delta_post_minus_pre | good_vs_moderate_none | 0.5476 | 0.0846 | 0.4856 | -0.2766 | 1.98 | Mono_macro | -0.2192 | 0.2515 | 0.4573 | -0.3389 | 0.6469 | False | False | False | False | 0 |
| LILRB3 | delta_post_minus_pre | moderate_good_vs_none | -0.532 | 0.1542 | 0.7429 | -0.07902 | 6.732 | DC | 0.2659 | 0.1344 | 0.384 | -0.01959 | 13.57 | False | False | False | False | 0 |
| LILRB3 | baseline_pre | moderate_good_vs_none | -0.5479 | 0.2374 | 0.7429 | 0.2088 | 2.625 | Mono_macro | 0.5267 | 0.02931 | 0.1675 | -0.112 | 4.704 | False | False | False | False | 0 |
| FCGR2B | delta_post_minus_pre | moderate_good_vs_none | -0.4213 | 0.2786 | 0.7429 | -0.07902 | 5.332 | DC | 0.2316 | 0.2799 | 0.4868 | -0.01959 | 11.83 | False | False | False | False | 0 |
| CD300A | baseline_pre | good_vs_moderate_none | -0.3222 | 0.348 | 0.7567 | 0.07772 | 4.146 | DC | 0.1837 | 0.396 | 0.6599 | 0.1535 | 1.196 | False | False | False | False | 0 |
| CD300A | delta_post_minus_pre | good_vs_moderate_none | -0.4068 | 0.3594 | 0.7567 | -0.2766 | 1.471 | DC | 0.5077 | 0.05879 | 0.2352 | -0.01959 | 25.92 | False | False | False | False | 0 |
| CD300LF | baseline_pre | good_vs_moderate_none | -0.2317 | 0.5184 | 0.977 | 0.07772 | 2.981 | Mono_macro | 0.06851 | 0.7217 | 0.8018 | -0.112 | 0.6119 | False | False | False | False | 0 |
| LILRB2 | baseline_pre | moderate_good_vs_none | -0.1866 | 0.6572 | 1 | 0.2088 | 0.894 | Mono_macro | 0.4418 | 0.01937 | 0.1291 | -0.112 | 3.946 | False | False | False | False | 0 |
| CD300LF | delta_post_minus_pre | moderate_good_vs_none | -0.1451 | 0.7369 | 1 | -0.07902 | 1.836 | Mono_macro | 0.2439 | 0.218 | 0.4152 | -0.3389 | 0.7197 | False | False | False | False | 0 |

## RA Adjusted Models

| gene | endpoint | comparison | n | response_coef | response_p | response_fdr | generic_response_coef | target_generic_abs_ratio | model_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FCGR2B | baseline_pre | good_vs_moderate_none | 42 | -0.9793 | 0.001639 | 0.06557 | 0.07772 | 12.6 | ok |
| FCGR2B | baseline_pre | moderate_good_vs_none | 42 | -0.865 | 0.008555 | 0.1512 | 0.2088 | 4.144 | ok |
| INPP5D | delta_post_minus_pre | good_vs_moderate_none | 42 | 0.9331 | 0.01134 | 0.1512 | -0.2766 | 3.374 | ok |
| INPP5D | baseline_pre | good_vs_moderate_none | 42 | 0.6644 | 0.03601 | 0.3601 | 0.07772 | 8.549 | ok |
| LILRB4 | delta_post_minus_pre | good_vs_moderate_none | 42 | 0.4343 | 0.06204 | 0.4856 | -0.2766 | 1.57 | ok |
| LAIR1 | delta_post_minus_pre | good_vs_moderate_none | 42 | 0.5476 | 0.0846 | 0.4856 | -0.2766 | 1.98 | ok |
| LAIR1 | delta_post_minus_pre | moderate_good_vs_none | 42 | 0.5351 | 0.08498 | 0.4856 | -0.07902 | 6.772 | ok |
| LILRB3 | delta_post_minus_pre | moderate_good_vs_none | 42 | -0.532 | 0.1542 | 0.7429 | -0.07902 | 6.732 | ok |
| LILRB3 | delta_post_minus_pre | good_vs_moderate_none | 42 | -0.5031 | 0.1817 | 0.7429 | -0.2766 | 1.819 | ok |
| INPP5D | delta_post_minus_pre | moderate_good_vs_none | 42 | 0.4486 | 0.2048 | 0.7429 | -0.07902 | 5.678 | ok |
| LAIR1 | baseline_pre | good_vs_moderate_none | 42 | 0.4835 | 0.2231 | 0.7429 | 0.07772 | 6.222 | ok |
| LILRB3 | baseline_pre | moderate_good_vs_none | 42 | -0.5479 | 0.2374 | 0.7429 | 0.2088 | 2.625 | ok |
| LAIR1 | baseline_pre | moderate_good_vs_none | 42 | 0.4664 | 0.2572 | 0.7429 | 0.2088 | 2.234 | ok |
| LILRB4 | delta_post_minus_pre | moderate_good_vs_none | 42 | 0.2571 | 0.262 | 0.7429 | -0.07902 | 3.254 | ok |
| FCGR2B | delta_post_minus_pre | moderate_good_vs_none | 42 | -0.4213 | 0.2786 | 0.7429 | -0.07902 | 5.332 | ok |
| INPP5D | baseline_pre | moderate_good_vs_none | 42 | 0.3217 | 0.3392 | 0.7567 | 0.2088 | 1.541 | ok |
| CD300A | baseline_pre | good_vs_moderate_none | 42 | -0.3222 | 0.348 | 0.7567 | 0.07772 | 4.146 | ok |
| FCGR2B | delta_post_minus_pre | good_vs_moderate_none | 42 | -0.391 | 0.3514 | 0.7567 | -0.2766 | 1.414 | ok |
| CD300A | delta_post_minus_pre | good_vs_moderate_none | 42 | -0.4068 | 0.3594 | 0.7567 | -0.2766 | 1.471 | ok |
| LILRB1 | baseline_pre | good_vs_moderate_none | 42 | 0.3687 | 0.5066 | 0.977 | 0.07772 | 4.743 | ok |
| CD300LF | baseline_pre | good_vs_moderate_none | 42 | -0.2317 | 0.5184 | 0.977 | 0.07772 | 2.981 | ok |
| LILRB2 | delta_post_minus_pre | good_vs_moderate_none | 42 | -0.1967 | 0.5608 | 0.977 | -0.2766 | 0.7112 | ok |
| LILRB2 | delta_post_minus_pre | moderate_good_vs_none | 42 | 0.1901 | 0.5618 | 0.977 | -0.07902 | 2.406 | ok |
| LILRB2 | baseline_pre | moderate_good_vs_none | 42 | -0.1866 | 0.6572 | 1 | 0.2088 | 0.894 | ok |
| LILRB2 | baseline_pre | good_vs_moderate_none | 42 | -0.1475 | 0.7166 | 1 | 0.07772 | 1.898 | ok |
| CD300A | delta_post_minus_pre | moderate_good_vs_none | 42 | 0.147 | 0.7348 | 1 | -0.07902 | 1.86 | ok |
| CD300LF | delta_post_minus_pre | moderate_good_vs_none | 42 | -0.1451 | 0.7369 | 1 | -0.07902 | 1.836 | ok |
| CD300LF | delta_post_minus_pre | good_vs_moderate_none | 42 | -0.1469 | 0.741 | 1 | -0.2766 | 0.5311 | ok |
| CD300A | baseline_pre | moderate_good_vs_none | 42 | -0.08241 | 0.8178 | 1 | 0.2088 | 0.3947 | ok |
| LILRB3 | baseline_pre | good_vs_moderate_none | 42 | -0.1025 | 0.8208 | 1 | 0.07772 | 1.318 | ok |
| LILRB4 | baseline_pre | moderate_good_vs_none | 42 | 0.09485 | 0.859 | 1 | 0.2088 | 0.4543 | ok |
| LILRB1 | baseline_pre | moderate_good_vs_none | 42 | 0.05913 | 0.9183 | 1 | 0.2088 | 0.2832 | ok |
| CD300LF | baseline_pre | moderate_good_vs_none | 42 | 0.03304 | 0.9293 | 1 | 0.2088 | 0.1583 | ok |
| LILRB4 | baseline_pre | good_vs_moderate_none | 42 | -0.03932 | 0.9393 | 1 | 0.07772 | 0.5059 | ok |
| LILRB1 | delta_post_minus_pre | good_vs_moderate_none | 42 | -4.586e-16 | 0.965 | 1 | -0.2766 | 1.658e-15 | ok |
| LILRB1 | delta_post_minus_pre | moderate_good_vs_none | 42 | 1.466e-16 | 0.9879 | 1 | -0.07902 | 1.855e-15 | ok |
| LILRB5 | baseline_pre | good_vs_moderate_none | 0 |  |  | 1 | 0.07772 |  | insufficient_rows_or_response_levels |
| LILRB5 | delta_post_minus_pre | good_vs_moderate_none | 0 |  |  | 1 | -0.2766 |  | insufficient_rows_or_response_levels |
| LILRB5 | baseline_pre | moderate_good_vs_none | 0 |  |  | 1 | 0.2088 |  | insufficient_rows_or_response_levels |
| LILRB5 | delta_post_minus_pre | moderate_good_vs_none | 0 |  |  | 1 | -0.07902 |  | insufficient_rows_or_response_levels |

## IBD Adjusted Models

| gene | cell_state | endpoint | n | response_coef | response_p | response_fdr | generic_response_coef | target_generic_abs_ratio | model_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LILRB4 | Mono_macro | delta_post_minus_pre | 29 | -0.7631 | 0.00576 | 0.08671 | -0.3389 | 2.252 | ok |
| LILRB4 | Mono_macro | baseline_pre | 29 | 0.5807 | 0.008191 | 0.08671 | -0.112 | 5.187 | ok |
| LILRB1 | Mono_macro | delta_post_minus_pre | 29 | -0.6899 | 0.008194 | 0.08671 | -0.3389 | 2.036 | ok |
| LILRB2 | DC | delta_post_minus_pre | 29 | -0.8612 | 0.008671 | 0.08671 | -0.01959 | 43.97 | ok |
| FCGR2B | DC | baseline_pre | 29 | -0.7287 | 0.01444 | 0.1155 | 0.1535 | 4.746 | ok |
| LILRB2 | Mono_macro | baseline_pre | 29 | 0.4418 | 0.01937 | 0.1291 | -0.112 | 3.946 | ok |
| LILRB3 | Mono_macro | baseline_pre | 29 | 0.5267 | 0.02931 | 0.1675 | -0.112 | 4.704 | ok |
| LILRB5 | DC | delta_post_minus_pre | 29 | 0.354 | 0.04493 | 0.2085 | -0.01959 | 18.07 | ok |
| LILRB5 | DC | baseline_pre | 29 | -0.3054 | 0.04692 | 0.2085 | 0.1535 | 1.989 | ok |
| CD300A | DC | delta_post_minus_pre | 29 | 0.5077 | 0.05879 | 0.2352 | -0.01959 | 25.92 | ok |
| LILRB5 | Mono_macro | delta_post_minus_pre | 29 | 0.3946 | 0.07631 | 0.275 | -0.3389 | 1.165 | ok |
| INPP5D | Mono_macro | delta_post_minus_pre | 29 | 0.4047 | 0.0825 | 0.275 | -0.3389 | 1.194 | ok |
| LILRB1 | Mono_macro | baseline_pre | 29 | 0.2698 | 0.1118 | 0.344 | -0.112 | 2.409 | ok |
| LILRB3 | DC | delta_post_minus_pre | 29 | 0.2659 | 0.1344 | 0.384 | -0.01959 | 13.57 | ok |
| FCGR2B | Mono_macro | baseline_pre | 29 | -0.4488 | 0.1597 | 0.403 | -0.112 | 4.008 | ok |
| LILRB4 | DC | baseline_pre | 29 | 0.2708 | 0.1626 | 0.403 | 0.1535 | 1.764 | ok |
| LILRB3 | Mono_macro | delta_post_minus_pre | 29 | -0.3844 | 0.1738 | 0.403 | -0.3389 | 1.134 | ok |
| LILRB2 | Mono_macro | delta_post_minus_pre | 29 | -0.3549 | 0.1813 | 0.403 | -0.3389 | 1.047 | ok |
| LILRB2 | DC | baseline_pre | 29 | 0.2285 | 0.2045 | 0.4152 | 0.1535 | 1.488 | ok |
| LAIR1 | Mono_macro | baseline_pre | 29 | 0.2507 | 0.2093 | 0.4152 | -0.112 | 2.239 | ok |
| CD300LF | Mono_macro | delta_post_minus_pre | 29 | 0.2439 | 0.218 | 0.4152 | -0.3389 | 0.7197 | ok |
| LAIR1 | Mono_macro | delta_post_minus_pre | 29 | -0.2192 | 0.2515 | 0.4573 | -0.3389 | 0.6469 | ok |
| FCGR2B | DC | delta_post_minus_pre | 29 | 0.2316 | 0.2799 | 0.4868 | -0.01959 | 11.83 | ok |
| CD300A | DC | baseline_pre | 29 | 0.1837 | 0.396 | 0.6599 | 0.1535 | 1.196 | ok |
| LILRB1 | DC | baseline_pre | 29 | 0.1489 | 0.441 | 0.7056 | 0.1535 | 0.9696 | ok |
| FCGR2B | Mono_macro | delta_post_minus_pre | 29 | 0.3104 | 0.4683 | 0.7204 | -0.3389 | 0.9161 | ok |
| CD300A | Mono_macro | delta_post_minus_pre | 29 | 0.1171 | 0.4914 | 0.728 | -0.3389 | 0.3455 | ok |
| LAIR1 | DC | delta_post_minus_pre | 29 | -0.1196 | 0.5455 | 0.7524 | -0.01959 | 6.107 | ok |
| INPP5D | DC | baseline_pre | 29 | -0.1215 | 0.5597 | 0.7524 | 0.1535 | 0.7911 | ok |
| CD300LF | DC | delta_post_minus_pre | 29 | 0.1517 | 0.5643 | 0.7524 | -0.01959 | 7.744 | ok |
| INPP5D | Mono_macro | baseline_pre | 29 | 0.1267 | 0.5858 | 0.7559 | -0.112 | 1.131 | ok |
| LILRB1 | DC | delta_post_minus_pre | 29 | 0.1332 | 0.6101 | 0.7626 | -0.01959 | 6.802 | ok |
| LILRB3 | DC | baseline_pre | 29 | 0.106 | 0.6317 | 0.7657 | 0.1535 | 0.6906 | ok |
| CD300A | Mono_macro | baseline_pre | 29 | 0.07754 | 0.6826 | 0.8018 | -0.112 | 0.6925 | ok |
| INPP5D | DC | delta_post_minus_pre | 29 | 0.07778 | 0.7203 | 0.8018 | -0.01959 | 3.971 | ok |
| CD300LF | Mono_macro | baseline_pre | 29 | 0.06851 | 0.7217 | 0.8018 | -0.112 | 0.6119 | ok |
| LAIR1 | DC | baseline_pre | 29 | 0.04352 | 0.8232 | 0.8899 | 0.1535 | 0.2835 | ok |
| LILRB4 | DC | delta_post_minus_pre | 29 | 0.03566 | 0.8907 | 0.9269 | -0.01959 | 1.821 | ok |
| LILRB5 | Mono_macro | baseline_pre | 29 | -0.02966 | 0.9038 | 0.9269 | -0.112 | 0.2649 | ok |
| CD300LF | DC | baseline_pre | 29 | -0.0006901 | 0.9988 | 0.9988 | 0.1535 | 0.004495 | ok |

## Wave70B Integrated Scout Rows

| gene | integrated_call | support_score_0_9 | manual_or_empirical_blocker | gse282122_best_cell_state | gse282122_adjusted_beta_remission | gse282122_adjusted_fdr | gse282122_response_call | wave68_adjusted_delta | wave68_adjusted_fdr | wave68_best_call | ms_gse111972_delta_log2 | ms_gse111972_p | ms_gse111972_fdr | ms_gse111972_call | broad_positive_compartments | broad_positive_fdr10_compartments | broad_negative_compartments | broad_negative_fdr10_compartments | positive_disease_count | positive_diseases | negative_disease_count | negative_diseases | ra_antitnf_mean_post_minus_pre | ra_antitnf_fdr | ra_antitnf_call | ra_response_adjusted_beta | ra_response_adjusted_fdr | ra_response_call | wave37_median_efficient_minus_noneater_lfc | wave37_screen_call | wave37_efferocytosis_direction | geneformer_sources | geneformer_support_contexts_max | geneformer_strong_support_contexts_max | ms_max_l2g_score | strong_qtl_coloc_disease_count | has_cross_autoimmune_genetics | has_any_druggability_flag_wave68 | call_priority |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LILRB2 | PARK_BLOCKED_OR_DIRECTIONALLY_UNRESOLVED | 4 | No local Wave68/Wave62 cross-autoimmune genetic anchor in this scout. | DC | -0.9486 | 0.01911 | remission_adjusted_down_fdr10 | -0.8842 | 0.02241 | DESCRIPTIVE_GENE_SIGNAL | -0.7297 | 0.007784 | 0.8345 | ms_down_nominal | 2 | 1 | 0 | 0 | 2 | Crohn disease;ulcerative colitis | 0 |  | -0.1359 | 0.2775 | null_or_weak | 0.1078 | 0.8943 | null_or_weak |  | not_present_in_wave37_mouse_screen | null_or_weak |  | 0 | 0 |  | 0 | False | False | 2 |
| LILRB4 | PARK_BLOCKED_OR_DIRECTIONALLY_UNRESOLVED | 3 | No local Wave68/Wave62 cross-autoimmune genetic anchor in this scout. | Mono_macro | -1.507 | 0.0167 | remission_adjusted_down_fdr10 | -1.476 | 0.01134 | DESCRIPTIVE_GENE_SIGNAL | -0.05671 | 0.8864 | 0.9842 | null_or_weak | 1 | 0 | 0 | 0 | 1 | type 1 diabetes mellitus | 0 |  | -0.02909 | 0.5352 | null_or_weak | -0.02495 | 0.9341 | null_or_weak | -0.4372 | UNRESOLVED | ko_impairment_trend |  | 0 | 0 |  | 0 | False | False | 2 |
| LILRB1 | PARK_BLOCKED_OR_DIRECTIONALLY_UNRESOLVED | 2 | No local Wave68/Wave62 cross-autoimmune genetic anchor in this scout. | Mono_macro | -1.075 | 0.01037 | remission_adjusted_down_fdr10 | -1.035 | 0.01202 | DESCRIPTIVE_GENE_SIGNAL | -0.248 | 0.3035 | 0.9075 | null_or_weak | 2 | 0 | 0 | 0 | 2 | Crohn disease;ulcerative colitis | 0 |  | -0.01185 | 0.4716 | null_or_weak | -0.01348 | 0.8943 | null_or_weak |  | not_present_in_wave37_mouse_screen | null_or_weak |  | 0 | 0 |  | 0 | False | False | 2 |
| CD300A | PARK_BLOCKED_OR_DIRECTIONALLY_UNRESOLVED | 1 | No local Wave68/Wave62 cross-autoimmune genetic anchor in this scout. | DC | 0.4478 | 0.3977 | null_or_weak |  |  | DESCRIPTIVE_GENE_SIGNAL | -0.3453 | 0.07661 | 0.8989 | null_or_weak | 0 | 0 | 0 | 0 | 0 |  | 0 |  | -0.225 | 0.287 | null_or_weak | -0.4041 | 0.8943 | null_or_weak | 1.338 | UNRESOLVED | ko_enhancement_trend |  | 0 | 0 |  | 0 | False | False | 2 |
| CD300LF | PARK_BLOCKED_OR_DIRECTIONALLY_UNRESOLVED | 1 | No local Wave68/Wave62 cross-autoimmune genetic anchor in this scout. | DC | 0.4623 | 0.6778 | null_or_weak |  |  | DESCRIPTIVE_GENE_SIGNAL | -0.09912 | 0.709 | 0.9669 | null_or_weak | 1 | 0 | 0 | 0 | 1 | psoriasis | 0 |  | -0.2821 | 0.1648 | null_or_weak | -0.1196 | 0.9251 | null_or_weak | -0.1802 | UNRESOLVED | null_or_weak | geneformer_pivot_panel;wave18_foundation_rescue_source | 1 | 1 |  | 0 | False | False | 2 |
| LAIR1 | PARK_BLOCKED_OR_DIRECTIONALLY_UNRESOLVED | 1 | No local Wave68/Wave62 cross-autoimmune genetic anchor in this scout. | DC | -0.3847 | 0.5097 | null_or_weak |  |  | DESCRIPTIVE_GENE_SIGNAL | -0.2811 | 0.1069 | 0.8989 | null_or_weak | 2 | 0 | 2 | 0 | 1 | type 1 diabetes mellitus | 2 | Crohn disease;ulcerative colitis | -0.3174 | 0.1349 | ra_antitnf_down_nominal | 0.5554 | 0.8943 | null_or_weak | 0.1628 | UNRESOLVED | null_or_weak |  | 0 | 0 |  | 0 | False | False | 2 |
| INPP5D | DESCRIPTIVE_SIGNAL_ONLY | 2 |  | Mono_macro | 0.3981 | 0.6008 | null_or_weak |  |  | DESCRIPTIVE_GENE_SIGNAL | -0.3038 | 0.0944 | 0.8989 | null_or_weak | 0 | 0 | 0 | 0 | 0 |  | 0 |  | -0.3864 | 0.02941 | ra_antitnf_down_fdr10 | -0.1771 | 0.8943 | null_or_weak | 0.4767 | UNRESOLVED | ko_enhancement_trend |  | 0 | 0 | 0 | 0 | False | False | 3 |

## Wave70C Geneformer Direction Rows

| gene | contexts_tested | contexts_with_token_ge_3_cells | support_contexts | strong_support_contexts | opposing_contexts | strong_opposing_contexts | best_context | best_n_nonremission_cells_with_token | best_cosine_shift_z_vs_random | best_projection_minus_random | most_negative_context | most_negative_n_nonremission_cells_with_token | most_negative_cosine_shift_z_vs_random | most_negative_projection_minus_random | supporting_contexts | strong_supporting_contexts | opposing_context_names | strong_opposing_context_names | geneformer_direction_priority_score | route | wave70_call | wave70_score | evidence_count | manual_blocker | gse282122_support | broad_support | ms_support | ra_support | ra_response_support | genetics_support | eff_support | model_support | real_pert_support | wave68_best_call | wave68_min_adjusted_fdr | wave68_min_raw_fdr | wave68_min_paired_fdr | direction_model_call | direction_model_call_priority | directional_interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FCGR2B | 6 | 4 | 0 | 0 | 2 | 0 | GSE282122_DC_post_nonremission_to_remission | 4 | 0.1769 | -0.03452 | GSE282122_Mono_macro_post_nonremission_to_remission | 3 | -0.3782 | -0.01526 |  |  | GSE282122_Mono_macro_post_nonremission_to_remission;GSE282122_Mono_macro_post_nonremission_to_remission_UC_only |  | 4 | inhibitory Fc-gamma receptor comparator | NO_GO_BLOCKED_OR_BROAD_CLASS | -0.04108 | 2 | Fc_receptor_directionality_and_safety | False | False | False | True | False | True | False | False | False | DESCRIPTIVE_GENE_SIGNAL;PARK_GENETIC_PERTURBATION_INTERSECTION |  | 1 | 0.6911 | MODEL_OPPOSING_BUT_BLOCKED_COMPARATOR | 2 | token_deletion_moves_nonremission_cells_away_from_remission_centroid; restoration_or_agonism_direction |
| LILRB3 | 6 | 4 | 2 | 0 | 2 | 0 | GSE282122_Mono_macro_post_nonremission_to_remission_UC_only | 3 | 0.3852 | 0.02126 | GSE282122_DC_post_nonremission_to_remission_UC_only | 3 | -0.2226 | -0.007145 | GSE282122_Mono_macro_post_nonremission_to_remission_CD_only;GSE282122_Mono_macro_post_nonremission_to_remission_UC_only |  | GSE282122_DC_post_nonremission_to_remission_CD_only;GSE282122_DC_post_nonremission_to_remission_UC_only |  | 8 | myeloid inhibitory receptor | NO_GO_INSUFFICIENT_CONVERGENCE | 2 | 1 |  | True | False | False | False | False | False | False | False | False | DESCRIPTIVE_GENE_SIGNAL | 0.03843 | 0.6813 | 1 | NO_GO_MODEL_DIRECTION_SCREEN | 3 | no_clear_directional_model_support |
| LILRB1 | 6 | 2 | 1 | 1 | 0 | 0 | GSE282122_Mono_macro_post_nonremission_to_remission_UC_only | 4 | 0.6654 | 0.02495 | GSE282122_Mono_macro_post_nonremission_to_remission | 2 | -0.5802 | -0.02404 | GSE282122_Mono_macro_post_nonremission_to_remission_UC_only | GSE282122_Mono_macro_post_nonremission_to_remission_UC_only |  |  | 7.5 | myeloid inhibitory receptor | NO_GO_INSUFFICIENT_CONVERGENCE | 2 | 1 |  | True | False | False | False | False | False | False | False | False | DESCRIPTIVE_GENE_SIGNAL | 0.01202 | 0.6233 | 0.9872 | NO_GO_MODEL_DIRECTION_SCREEN | 3 | token_deletion_moves_nonremission_cells_toward_remission_centroid; suppression_or_antagonism_direction |
| LILRB2 | 6 | 4 | 2 | 0 | 1 | 0 | GSE282122_DC_post_nonremission_to_remission_UC_only | 4 | 0.3225 | 0.04986 | GSE282122_Mono_macro_post_nonremission_to_remission_CD_only | 5 | -0.326 | -0.03204 | GSE282122_DC_post_nonremission_to_remission_UC_only;GSE282122_Mono_macro_post_nonremission_to_remission_UC_only |  | GSE282122_Mono_macro_post_nonremission_to_remission_CD_only |  | 6.5 | myeloid inhibitory receptor | NO_GO_INSUFFICIENT_CONVERGENCE | 3 | 2 |  | True | True | False | False | False | False | False | False | False | DESCRIPTIVE_GENE_SIGNAL | 0.02241 | 0.997 | 1 | NO_GO_MODEL_DIRECTION_SCREEN | 3 | token_deletion_moves_nonremission_cells_toward_remission_centroid; suppression_or_antagonism_direction |
| INPP5D | 6 | 1 | 1 | 0 | 0 | 0 | GSE282122_DC_post_nonremission_to_remission_CD_only | 3 | 0.442 | 0.00748 | GSE282122_DC_post_nonremission_to_remission_CD_only | 3 | 0.442 | 0.00748 | GSE282122_DC_post_nonremission_to_remission_CD_only |  |  |  | 2.25 | SHIP1 inhibitory Fc/PI3K lipid phosphatase | NO_GO_INSUFFICIENT_CONVERGENCE | 1.283 | 1 |  | False | False | False | True | False | False | False | False | False | DESCRIPTIVE_GENE_SIGNAL |  | 1 | 0.9926 | NO_GO_MODEL_DIRECTION_SCREEN | 3 | token_deletion_moves_nonremission_cells_toward_remission_centroid; suppression_or_antagonism_direction |
| LILRB4 | 6 | 1 | 0 | 0 | 1 | 0 | GSE282122_DC_post_nonremission_to_remission_UC_only | 1 | 2.778 | -0.01262 | GSE282122_Mono_macro_post_nonremission_to_remission | 3 | -0.3215 | -0.002138 |  |  | GSE282122_Mono_macro_post_nonremission_to_remission |  | 1.75 | myeloid inhibitory receptor | NO_GO_INSUFFICIENT_CONVERGENCE | 1.5 | 1 |  | True | False | False | False | False | False | False | False | False | DESCRIPTIVE_GENE_SIGNAL | 0.01134 | 0.6233 | 1 | NO_GO_MODEL_DIRECTION_SCREEN | 3 | token_deletion_moves_nonremission_cells_away_from_remission_centroid; restoration_or_agonism_direction |
| LAIR1 | 6 | 1 | 0 | 0 | 0 | 0 | GSE282122_Mono_macro_post_nonremission_to_remission_UC_only | 6 | 0.3653 | -0.02174 | GSE282122_DC_post_nonremission_to_remission_CD_only | 1 | -0.4695 | 0.02276 |  |  |  |  | 0.25 | collagen-binding inhibitory receptor | NO_GO_INSUFFICIENT_CONVERGENCE | 1.5 | 1 |  | False | False | False | True | False | False | False | False | False | DESCRIPTIVE_GENE_SIGNAL |  | 0.9066 | 1 | NO_GO_MODEL_DIRECTION_SCREEN | 3 | no_clear_directional_model_support |
| CD300LF | 6 | 0 | 0 | 0 | 0 | 0 | GSE282122_DC_post_nonremission_to_remission_UC_only | 2 | 0.7842 | 0.03549 | GSE282122_DC_post_nonremission_to_remission | 2 | -0.913 | 0.005367 |  |  |  |  | 0 | CD300 inhibitory/immune receptor | NO_GO_INSUFFICIENT_CONVERGENCE | 0.5 | 0 |  | False | False | False | False | False | False | False | False | False | DESCRIPTIVE_GENE_SIGNAL |  | 1 | 1 | NO_GO_LOW_TOKEN_SUPPORT | 4 | insufficient_token_support |
| CD300A | 6 | 0 | 0 | 0 | 0 | 0 | GSE282122_DC_post_nonremission_to_remission_UC_only | 2 | 0.483 | 0.02496 | GSE282122_Mono_macro_post_nonremission_to_remission_UC_only | 1 | -0.0845 | 0.0116 |  |  |  |  | 0 | lipid-sensing inhibitory receptor | NO_GO_INSUFFICIENT_CONVERGENCE | 0 | 0 |  | False | False | False | False | False | False | False | False | False | DESCRIPTIVE_GENE_SIGNAL |  | 1 | 1 | NO_GO_LOW_TOKEN_SUPPORT | 4 | insufficient_token_support |

## Interpretation

A LILRB target can only be promoted if the target-level signal is not just
myeloid abundance or generic inflammation. The hard blockers are absent MS
anchor, inconsistent adjusted RA/IBD response specificity, no model-backed
direction, and uncertainty over whether agonism or inhibition would improve
the pathogenic state.
