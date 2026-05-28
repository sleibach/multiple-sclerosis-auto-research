# Wave133 Closure-Hygiene Correction

## Bottom Line

Branch call: `HYGIENE_CORRECTION_REOPENS_ROUTE`.

This wave corrects the two hostile-review hygiene defects: Wave122 now uses the
real Wave55 genetics file, and both Wave122/Wave128 are rerun with exact
gene-symbol closure matching rather than substring matching.

## Wave122 Corrected Top Rows

| gene | call | fresh_score | support_channels | ms | broad_cell_state | response | genetics | perturbation_or_model | modality | ms_delta_log2 | ms_p | ms_fdr | broad_positive_disease_count | response_contexts | strong_l2g_disease_count | strong_qtl_coloc_disease_count | wave55_genetic_disease_count | blocker_flag | blocker_text | would_have_been_substring_closed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DAP | TESTABLE_FRESH_ROUTE | 6.1 | 3 | True | True | False | True | False | False | 0.3933 | 0.008069 | 0.8345 | 3 | 0 | 0 | 0 | 5 | False |   NO_REOPEN_INSUFFICIENT_CONVERGENCE candidate lacks direct perturbation or model support  | False |
| NCF2 | NO_GO_FRESH_SCAN | 4.9 | 4 | True | False | False | True | True | True | 0.5994 | 0.01942 | 0.8373 | 2 | 0 | 2 | 1 | 3 | True |   NO_REOPEN_BLOCKED_BRANCH NOX2 host-defense/CGD directionality risk NO_GO_WAVE62_TARGET_RESOLUTION | False |
| CXCR2 | NO_GO_FRESH_SCAN | 4.6 | 4 | False | True | False | True | True | True | 0.8298 | 0.3775 | 0.9141 | 3 | 0 | 0 | 1 | 5 | True |   PARK_PRIOR_ART_OR_HOST_DEFENSE_PENALIZED chemokine/neutrophil route prior audited and infection-risk broad NO_GO_WAVE62_TARGET_RESOLUTION | False |
| CBX3 | NO_GO_FRESH_SCAN | 4.3 | 2 | True | True | False | False | False | False | 0.3505 | 0.01659 | 0.8373 | 4 | 0 | 0 | 0 | 0 | False |      | False |
| FMNL2 | NO_GO_FRESH_SCAN | 4.3 | 2 | True | True | False | False | False | False | 0.4117 | 0.03238 | 0.8507 | 4 | 0 | 0 | 0 | 1 | False |   NO_REOPEN_INSUFFICIENT_CONVERGENCE candidate lacks direct perturbation or model support  | False |
| TNFAIP8L1 | NO_GO_FRESH_SCAN | 4.3 | 2 | True | True | False | False | False | False | 0.4563 | 0.008562 | 0.8349 | 4 | 0 | 0 | 0 | 0 | False |      | False |
| CUL2 | NO_GO_FRESH_SCAN | 4.2 | 2 | True | False | False | True | False | False | 0.3506 | 0.03077 | 0.8507 | 1 | 0 | 0 | 0 | 3 | False |      | False |
| MSRA | NO_GO_FRESH_SCAN | 4.2 | 2 | True | False | False | True | False | False | 0.5151 | 0.04996 | 0.8769 | 1 | 0 | 0 | 0 | 3 | False |      | False |
| PTPN22 | NO_GO_FRESH_SCAN | 4.2 | 2 | True | False | False | True | False | False | 0.8195 | 0.03134 | 0.8507 | 1 | 0 | 0 | 0 | 9 | False |      | False |
| APOC1 | NO_GO_FRESH_SCAN | 4.1 | 2 | True | True | False | False | False | False | 0.8063 | 0.03335 | 0.8507 | 3 | 0 | 0 | 0 | 0 | False |      | False |
| AQR | NO_GO_FRESH_SCAN | 4.1 | 2 | True | True | False | False | False | False | 0.2576 | 0.04593 | 0.8735 | 3 | 0 | 0 | 0 | 0 | False |      | False |
| CHI3L1 | NO_GO_FRESH_SCAN | 4.1 | 2 | True | True | False | False | False | False | 2.007 | 0.004613 | 0.8345 | 3 | 0 | 0 | 0 | 0 | False |      | False |
| CRTAP | NO_GO_FRESH_SCAN | 4.1 | 2 | True | True | False | False | False | False | 0.3844 | 0.04989 | 0.8769 | 3 | 0 | 0 | 0 | 0 | False |      | False |
| CXCL9 | NO_GO_FRESH_SCAN | 4.1 | 2 | True | True | False | False | False | False | 2.554 | 0.03099 | 0.8507 | 3 | 0 | 0 | 0 | 0 | False |      | False |
| IGF2BP2 | NO_GO_FRESH_SCAN | 4.1 | 2 | False | True | False | True | False | False | -0.1546 | 0.8807 | 0.9832 | 3 | 0 | 0 | 0 | 3 | False |      | False |
| LTA4H | NO_GO_FRESH_SCAN | 4.1 | 2 | True | True | False | False | False | False | 0.8088 | 0.006357 | 0.8345 | 3 | 0 | 0 | 0 | 0 | False |      | False |
| NCK1 | NO_GO_FRESH_SCAN | 4.1 | 2 | True | True | False | False | False | False | 0.445 | 0.005556 | 0.8345 | 3 | 0 | 0 | 0 | 0 | False |      | False |
| NFIA | NO_GO_FRESH_SCAN | 4.1 | 2 | False | True | False | True | False | False | 0.03641 | 0.8647 | 0.9802 | 3 | 0 | 0 | 0 | 4 | False |      | False |
| PFKFB3 | NO_GO_FRESH_SCAN | 4.1 | 2 | False | True | False | True | False | False | -0.4547 | 0.1561 | 0.8989 | 3 | 0 | 0 | 0 | 3 | False |      | False |
| PLEK2 | NO_GO_FRESH_SCAN | 4.1 | 2 | True | True | False | False | False | False | 3.046 | 0.007379 | 0.8345 | 3 | 0 | 0 | 0 | 0 | False |      | False |
| PPIL3 | NO_GO_FRESH_SCAN | 4.1 | 2 | True | True | False | False | False | False | 0.6072 | 0.01829 | 0.8373 | 3 | 0 | 0 | 0 | 1 | False |      | False |
| PPP3CA | NO_GO_FRESH_SCAN | 4.1 | 2 | True | True | False | False | False | False | 0.3663 | 0.03434 | 0.8507 | 3 | 0 | 0 | 0 | 0 | False |      | False |
| PTPRC | NO_GO_FRESH_SCAN | 4.1 | 2 | False | True | False | True | False | False | -0.1131 | 0.4868 | 0.926 | 3 | 0 | 0 | 0 | 3 | False |      | False |
| SNX10 | NO_GO_FRESH_SCAN | 4.1 | 2 | True | True | False | False | False | False | 0.7124 | 0.01274 | 0.8349 | 3 | 0 | 0 | 0 | 0 | False |      | False |
| TNFAIP3 | NO_GO_FRESH_SCAN | 4.1 | 2 | False | True | False | True | False | False | 0.3284 | 0.3607 | 0.9141 | 3 | 0 | 0 | 0 | 9 | False |      | False |
| ADCY3 | NO_GO_FRESH_SCAN | 4 | 2 | True | False | False | True | False | False | 0.9418 | 0.005839 | 0.8345 | 0 | 0 | 0 | 0 | 5 | False |      | False |
| IL6R | NO_GO_FRESH_SCAN | 4 | 2 | True | False | False | True | False | False | 0.3662 | 0.03844 | 0.8516 | 0 | 0 | 0 | 0 | 5 | False |      | False |
| ABHD2 | NO_GO_FRESH_SCAN | 3.9 | 2 | True | True | False | False | False | False | 0.7082 | 0.003244 | 0.8345 | 2 | 0 | 0 | 0 | 0 | False |      | False |
| ACAP1 | NO_GO_FRESH_SCAN | 3.9 | 2 | False | True | False | True | False | False | 0.1056 | 0.8901 | 0.9842 | 2 | 0 | 0 | 0 | 3 | False |      | False |
| BTF3 | NO_GO_FRESH_SCAN | 3.9 | 2 | True | True | False | False | False | False | 0.3048 | 0.0168 | 0.8373 | 2 | 0 | 0 | 0 | 0 | False |      | False |

## Genes Restored By Exact Closure In Wave122

| gene | call | fresh_score | support_channels | ms | broad_cell_state | response | genetics | perturbation_or_model | modality | ms_delta_log2 | ms_p | ms_fdr | broad_positive_disease_count | response_contexts | strong_l2g_disease_count | strong_qtl_coloc_disease_count | wave55_genetic_disease_count | blocker_flag | blocker_text | would_have_been_substring_closed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NAMPT-AS1 | NO_GO_FRESH_SCAN | 0.4 | 0 | False | False | False | False | False | False | 0 | 1 | 1 | 2 | 0 | 0 | 0 | 0 | False |      | True |
| ANXA10 | NO_GO_FRESH_SCAN | 0.2 | 0 | False | False | False | False | False | False | 0 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | False |      | True |
| CD93 | NO_GO_FRESH_SCAN | 0.2 | 0 | False | False | False | False | False | False | -0.8292 | 0.1389 | 0.8989 | 1 | 0 | 0 | 0 | 0 | False |      | True |
| PIMREG | NO_GO_FRESH_SCAN | 0.2 | 0 | False | False | False | False | False | False | 0 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | False |      | True |
| PRPSAP1 | NO_GO_FRESH_SCAN | 0.2 | 0 | False | False | False | False | False | False | -0.1117 | 0.495 | 0.9274 | 1 | 0 | 0 | 0 | 0 | False |      | True |
| PRPSAP2 | NO_GO_FRESH_SCAN | 0.2 | 0 | False | False | False | False | False | False | 0.2217 | 0.1953 | 0.8994 | 1 | 0 | 0 | 0 | 0 | False |      | True |
| ANXA11 | NO_GO_FRESH_SCAN | 0 | 0 | False | False | False | False | False | False | 0.1472 | 0.5207 | 0.9353 | 0 | 0 | 0 | 0 | 2 | False |      | True |
| ANXA13 | NO_GO_FRESH_SCAN | 0 | 0 | False | False | False | False | False | False | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | False |      | True |
| CD44-AS1 | NO_GO_FRESH_SCAN | 0 | 0 | False | False | False | False | False | False | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | False |      | True |
| CD44-DT | NO_GO_FRESH_SCAN | 0 | 0 | False | False | False | False | False | False | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | False |      | True |
| CD96 | NO_GO_FRESH_SCAN | 0 | 0 | False | False | False | False | False | False | -0.6118 | 0.6216 | 0.949 | 0 | 0 | 0 | 0 | 0 | False |      | True |
| CD99 | NO_GO_FRESH_SCAN | 0 | 0 | False | False | False | False | False | False | 0.09623 | 0.4281 | 0.9195 | 0 | 0 | 0 | 0 | 0 | False |      | True |
| CD99L2 | NO_GO_FRESH_SCAN | 0 | 0 | False | False | False | False | False | False | -0.07413 | 0.7246 | 0.9678 | 0 | 0 | 0 | 0 | 0 | False |      | True |
| CD99P1 | NO_GO_FRESH_SCAN | 0 | 0 | False | False | False | False | False | False | 0.5815 | 0.1426 | 0.8989 | 0 | 0 | 0 | 0 | 0 | False |      | True |
| CSPP1 | NO_GO_FRESH_SCAN | 0 | 0 | False | False | False | False | False | False | -0.04966 | 0.8439 | 0.9762 | 0 | 0 | 0 | 0 | 0 | False |      | True |
| DAB2IP | NO_GO_FRESH_SCAN | 0 | 0 | False | False | False | False | False | False | 0.3948 | 0.5248 | 0.9357 | 0 | 0 | 0 | 0 | 0 | False |      | True |
| FABP5P3 | NO_GO_FRESH_SCAN | 0 | 0 | False | False | False | False | False | False | -0.5397 | 0.6005 | 0.9467 | 0 | 0 | 0 | 0 | 0 | False |      | True |
| LYNX1 | NO_GO_FRESH_SCAN | 0 | 0 | False | False | False | False | False | False | 0.6661 | 0.08738 | 0.8989 | 0 | 0 | 0 | 0 | 0 | False |      | True |
| PSAPL1 | NO_GO_FRESH_SCAN | 0 | 0 | False | False | False | False | False | False | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | False |      | True |
| RPSAP58 | NO_GO_FRESH_SCAN | 0 | 0 | False | False | False | False | False | False | 0.1141 | 0.4293 | 0.9195 | 0 | 0 | 0 | 0 | 0 | False |      | True |
| RPSAP9 | NO_GO_FRESH_SCAN | 0 | 0 | False | False | False | False | False | False | 0.5493 | 0.3764 | 0.9141 | 0 | 0 | 0 | 0 | 0 | False |      | True |
| YWHAEP1 | NO_GO_FRESH_SCAN | 0 | 0 | False | False | False | False | False | False | 0.1208 | 0.8835 | 0.9842 | 0 | 0 | 0 | 0 | 0 | False |      | True |

## Wave128 Exact-Closure Top Rows

| gene | call | passed_gates | gate_count | failed_gates | substring_closed_in_original_logic | wave55_score | genetic_diseases | ms_genetic_association | ms_wm_delta_log2 | ms_wm_p | strict_residual_disease_count | max_clinical_score | max_literature_score | foundation_recommendation | wave34_call | primary_blocker | corrected_wave122_call |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SP140 | NO_REOPEN_GENETICS_FIRST_ROUTE | 8 | 11 | strict_ms_local_nominal;residual_support_ge2;druggability_or_modality | False | 26 | AS;Crohn;MS;Psoriasis;RA;UC | 0.7594 | -0.08676 | 0.7262 | 0 | 0 | 0.5046 |  | PARK_GENETIC_CELL_STATE_NOT_CURRENTLY_DRUGGABLE |  | NO_GO_FRESH_SCAN |
| IL7R | NO_REOPEN_GENETICS_FIRST_ROUTE | 7 | 11 | strict_ms_local_nominal;residual_support_ge2;perturbation_or_model_support;druggability_or_modality | False | 26 | AITD;Crohn;MS;PBC;Psoriasis;SLE;T1D | 0.7886 | -0.6537 | 0.5725 | 1 | 0 | 0.8422 | do_not_promote | PARK_GENETIC_CELL_STATE_NOT_CURRENTLY_DRUGGABLE | no_target_resolved_coloc_or_mr | NO_GO_FRESH_SCAN |
| PRDM1 | NO_REOPEN_GENETICS_FIRST_ROUTE | 7 | 11 | ms_genetic_anchor;strict_ms_local_nominal;residual_support_ge2;druggability_or_modality | False | 23 | AS;Crohn;Psoriasis;RA;SLE;UC | 0 | -0.04114 | 0.9031 | 0 | 0 | 0.7571 |  | PARK_GENETIC_CELL_STATE_NOT_CURRENTLY_DRUGGABLE |  | NO_GO_FRESH_SCAN |
| CCL20 | NO_REOPEN_GENETICS_FIRST_ROUTE | 7 | 11 | ms_genetic_anchor;strict_ms_local_nominal;residual_support_ge2;druggability_or_modality | False | 22 | AS;Crohn;Psoriasis;RA;UC | 0 | 1.147 | 0.06111 | 0 | 0 | 0.7951 |  | PARK_GENETIC_CELL_STATE_NOT_CURRENTLY_DRUGGABLE | no_target_resolved_coloc_or_mr | NO_GO_FRESH_SCAN |
| GALC | NO_REOPEN_GENETICS_FIRST_ROUTE | 7 | 11 | strict_ms_local_nominal;residual_support_ge2;druggability_or_modality;coloc_or_mr_grade | False | 21 | AS;Crohn;MS;SLE;UC | 0.5501 | 0.1898 | 0.4547 | 0 | 0 | 0.05826 |  | PARK_GENETIC_CELL_STATE_NOT_CURRENTLY_DRUGGABLE |  | NO_GO_FRESH_SCAN |
| CXCR2 | NO_REOPEN_GENETICS_FIRST_ROUTE | 7 | 11 | ms_genetic_anchor;strict_ms_local_nominal;residual_support_ge2;coloc_or_mr_grade | False | 15 | AS;Crohn;Psoriasis;RA;UC | 0 | 0.8298 | 0.3775 | 0 | 0.4853 | 0.5063 |  | PARK_GENETIC_CELL_STATE_NOT_CURRENTLY_DRUGGABLE |  | NO_GO_FRESH_SCAN |
| CD40 | NO_REOPEN_GENETICS_FIRST_ROUTE | 6 | 11 | local_cellstate_ge3_no_negative;strict_ms_local_nominal;residual_support_ge2;not_prior_art_crowded;wave34_not_no_go | False | 24 | AITD;AS;Crohn;MS;Psoriasis;RA;SLE;UC | 0.7293 | -0.5446 | 0.05403 | 0 | 0.1733 | 0.9167 |  | NO_GO_WAVE34_GENETICS_EXPRESSION_DRUGGABILITY |  | NO_GO_FRESH_SCAN |
| STAT4 | NO_REOPEN_GENETICS_FIRST_ROUTE | 6 | 11 | local_cellstate_ge3_no_negative;strict_ms_local_nominal;residual_support_ge2;not_prior_art_crowded;wave34_not_no_go | False | 24 | AITD;Celiac;Crohn;MS;PBC;RA;SLE;Sjogren;T1D | 0.6556 | 0.8684 | 0.4607 | 0 | 0 | 0.9286 |  | NO_GO_WAVE34_GENETICS_EXPRESSION_DRUGGABILITY |  | NO_GO_FRESH_SCAN |
| BACH2 | NO_REOPEN_GENETICS_FIRST_ROUTE | 6 | 11 | local_cellstate_ge3_no_negative;strict_ms_local_nominal;residual_support_ge2;druggability_or_modality;wave34_not_no_go | False | 23 | AITD;AS;Celiac;Crohn;MS;Psoriasis;RA;SLE;T1D;UC | 0.7231 | -1.248 | 0.2981 | 0 | 0 | 0.7256 |  | NO_GO_WAVE34_GENETICS_EXPRESSION_DRUGGABILITY |  | NO_GO_FRESH_SCAN |
| INAVA | NO_REOPEN_GENETICS_FIRST_ROUTE | 6 | 11 | local_cellstate_ge3_no_negative;strict_ms_local_nominal;residual_support_ge2;druggability_or_modality;wave34_not_no_go | False | 23 | AS;Celiac;Crohn;MS;Psoriasis;RA;UC | 0.6677 | 0 | 1 | 0 | 0 | 0.06795 |  | NO_GO_WAVE34_GENETICS_EXPRESSION_DRUGGABILITY |  | NO_GO_FRESH_SCAN |
| PUS10 | NO_REOPEN_GENETICS_FIRST_ROUTE | 6 | 11 | local_cellstate_ge3_no_negative;strict_ms_local_nominal;residual_support_ge2;druggability_or_modality;wave34_not_no_go | False | 23 | AS;Celiac;Crohn;MS;Psoriasis;RA;UC | 0.5872 | -0.18 | 0.5667 | 0 | 0 | 0.07202 |  | NO_GO_WAVE34_GENETICS_EXPRESSION_DRUGGABILITY |  | NO_GO_FRESH_SCAN |
| SPRED2 | NO_REOPEN_GENETICS_FIRST_ROUTE | 6 | 11 | local_cellstate_ge3_no_negative;strict_ms_local_nominal;residual_support_ge2;druggability_or_modality;wave34_not_no_go | False | 23 | Celiac;Crohn;MS;Psoriasis;RA;SLE | 0.6799 | -0.2835 | 0.2238 | 0 | 0 | 0.1815 |  | NO_GO_WAVE34_GENETICS_EXPRESSION_DRUGGABILITY |  | NO_GO_FRESH_SCAN |
| TAGAP | NO_REOPEN_GENETICS_FIRST_ROUTE | 6 | 11 | local_cellstate_ge3_no_negative;strict_ms_local_nominal;residual_support_ge2;druggability_or_modality;wave34_not_no_go | False | 23 | AITD;AS;Celiac;Crohn;MS;Psoriasis;RA;T1D;UC | 0.7691 | 0.455 | 0.2565 | 0 | 0 | 0.2202 |  | NO_GO_WAVE34_GENETICS_EXPRESSION_DRUGGABILITY |  | NO_GO_FRESH_SCAN |
| IL12B | NO_REOPEN_GENETICS_FIRST_ROUTE | 6 | 11 | local_cellstate_ge3_no_negative;strict_ms_local_nominal;residual_support_ge2;not_prior_art_crowded;wave34_not_no_go | False | 22.5 | AITD;AS;Celiac;Crohn;MS;PBC;Psoriasis;RA;SLE;T1D;UC | 0.6699 | 0.2347 | 0.8363 | 0 | 0.9948 | 0.6837 |  | NO_GO_WAVE34_GENETICS_EXPRESSION_DRUGGABILITY |  | NO_GO_FRESH_SCAN |
| ANKRD55 | NO_REOPEN_GENETICS_FIRST_ROUTE | 6 | 11 | local_cellstate_ge3_no_negative;strict_ms_local_nominal;residual_support_ge2;druggability_or_modality;wave34_not_no_go | False | 22 | AITD;AS;Celiac;Crohn;MS;Psoriasis;RA;SLE;T1D;UC | 0.7108 | -0.2482 | 0.8214 | 0 | 0 | 0.2235 |  | NO_GO_WAVE34_GENETICS_EXPRESSION_DRUGGABILITY |  | NO_GO_FRESH_SCAN |
| ELMO1 | NO_REOPEN_GENETICS_FIRST_ROUTE | 6 | 11 | local_cellstate_ge3_no_negative;strict_ms_local_nominal;residual_support_ge2;druggability_or_modality;wave34_not_no_go | False | 22 | AITD;Celiac;Crohn;MS;PBC;Psoriasis;RA | 0.5109 | -0.266 | 0.1156 | 0 | 0 | 0.6876 |  | NO_GO_WAVE34_GENETICS_EXPRESSION_DRUGGABILITY |  | NO_GO_FRESH_SCAN |
| JAZF1 | NO_REOPEN_GENETICS_FIRST_ROUTE | 6 | 11 | local_cellstate_ge3_no_negative;strict_ms_local_nominal;residual_support_ge2;druggability_or_modality;wave34_not_no_go | False | 22 | AS;Crohn;MS;Psoriasis;RA;SLE;T1D;UC | 0.4559 | -0.5308 | 0.03951 | 0 | 0 | 0.3084 |  | NO_GO_WAVE34_GENETICS_EXPRESSION_DRUGGABILITY |  | NO_GO_FRESH_SCAN |
| IL12A | NO_REOPEN_GENETICS_FIRST_ROUTE | 6 | 11 | local_cellstate_ge3_no_negative;strict_ms_local_nominal;residual_support_ge2;not_prior_art_crowded;wave34_not_no_go | False | 21.5 | Celiac;MS;PBC;SLE;Sjogren | 0.7515 | -0.9143 | 0.4433 | 0 | 0.9865 | 0.4358 |  | NO_GO_WAVE34_GENETICS_EXPRESSION_DRUGGABILITY |  | NO_GO_FRESH_SCAN |
| CARMIL1 | NO_REOPEN_GENETICS_FIRST_ROUTE | 6 | 11 | ms_genetic_anchor;strict_ms_local_nominal;residual_support_ge2;druggability_or_modality;coloc_or_mr_grade | False | 21 | Celiac;Psoriasis;RA;SLE;T1D;UC | 0 | 0 | 1 | 0 | 0 | 0 |  | PARK_GENETIC_CELL_STATE_NOT_CURRENTLY_DRUGGABLE |  | NO_GO_FRESH_SCAN |
| DAP | NO_REOPEN_GENETICS_FIRST_ROUTE | 6 | 11 | ms_genetic_anchor;residual_support_ge2;perturbation_or_model_support;druggability_or_modality;coloc_or_mr_grade | False | 20 | AS;Crohn;Psoriasis;RA;UC | 0 | 0.3933 | 0.008069 | 0 | 0 | 0.1322 | do_not_promote | PARK_GENETIC_CELL_STATE_NOT_CURRENTLY_DRUGGABLE | no_target_resolved_coloc_or_mr | TESTABLE_FRESH_ROUTE |
| ADCY3 | NO_REOPEN_GENETICS_FIRST_ROUTE | 6 | 11 | ms_genetic_anchor;local_cellstate_ge3_no_negative;residual_support_ge2;druggability_or_modality;coloc_or_mr_grade | False | 15 | AS;Crohn;Psoriasis;RA;UC | 0 | 0.9418 | 0.005839 | 0 | 0 | 0.1491 |  | PARK_GENETIC_CELL_STATE_NOT_CURRENTLY_DRUGGABLE |  | NO_GO_FRESH_SCAN |
| CCDC88B | NO_REOPEN_GENETICS_FIRST_ROUTE | 6 | 11 | ms_genetic_anchor;strict_ms_local_nominal;residual_support_ge2;druggability_or_modality;coloc_or_mr_grade | False | 13 | Crohn;PBC;Psoriasis;RA | 0 | -0.4485 | 0.01371 | 0 | 0 | 0.07118 |  | PARK_GENETIC_CELL_STATE_NOT_CURRENTLY_DRUGGABLE |  | NO_GO_FRESH_SCAN |
| BANK1 | NO_REOPEN_GENETICS_FIRST_ROUTE | 5 | 11 | ms_genetic_anchor;local_cellstate_ge3_no_negative;strict_ms_local_nominal;residual_support_ge2;druggability_or_modality;wave34_not_no_go | False | 22 | AS;Crohn;Psoriasis;RA;SLE;UC | 0 | -1.328 | 0.2391 | 0 | 0 | 0.7954 |  | NO_GO_WAVE34_GENETICS_EXPRESSION_DRUGGABILITY |  | NO_GO_FRESH_SCAN |
| CDKAL1 | NO_REOPEN_GENETICS_FIRST_ROUTE | 5 | 11 | ms_genetic_anchor;local_cellstate_ge3_no_negative;strict_ms_local_nominal;residual_support_ge2;druggability_or_modality;wave34_not_no_go | False | 22 | AS;Crohn;Psoriasis;RA;T1D;UC | 0 | -0.6895 | 0.4021 | 0 | 0 | 0.1308 |  | NO_GO_WAVE34_GENETICS_EXPRESSION_DRUGGABILITY |  | NO_GO_FRESH_SCAN |
| IRF4 | NO_REOPEN_GENETICS_FIRST_ROUTE | 5 | 11 | ms_genetic_anchor;local_cellstate_ge3_no_negative;strict_ms_local_nominal;residual_support_ge2;druggability_or_modality;wave34_not_no_go | False | 22 | AITD;Celiac;Crohn;Psoriasis;RA;SLE;T1D | 0 | 0.04445 | 0.9107 | 0 | 0 | 0.8519 |  | NO_GO_WAVE34_GENETICS_EXPRESSION_DRUGGABILITY |  | NO_GO_FRESH_SCAN |
| TNFSF15 | NO_REOPEN_GENETICS_FIRST_ROUTE | 5 | 11 | ms_genetic_anchor;local_cellstate_ge3_no_negative;strict_ms_local_nominal;residual_support_ge2;druggability_or_modality;wave34_not_no_go | False | 22 | AITD;AS;Celiac;Crohn;PBC;Psoriasis;RA;SLE;T1D;UC | 0 | 0.3944 | 0.7557 | 0 | 0 | 0.4794 |  | NO_GO_WAVE34_GENETICS_EXPRESSION_DRUGGABILITY |  | NO_GO_FRESH_SCAN |
| HHEX | NO_REOPEN_GENETICS_FIRST_ROUTE | 5 | 11 | local_cellstate_ge3_no_negative;strict_ms_local_nominal;residual_support_ge2;druggability_or_modality;coloc_or_mr_grade;wave34_not_no_go | False | 21 | AS;Crohn;MS;Psoriasis;T1D;UC | 0.681 | 0.004266 | 0.9916 | 0 | 0 | 0.2134 |  | NO_GO_WAVE34_GENETICS_EXPRESSION_DRUGGABILITY |  | NO_GO_FRESH_SCAN |
| PRKCB | NO_REOPEN_GENETICS_FIRST_ROUTE | 5 | 11 | ms_genetic_anchor;local_cellstate_ge3_no_negative;strict_ms_local_nominal;residual_support_ge2;coloc_or_mr_grade;wave34_not_no_go | False | 21 | AS;Crohn;PBC;Psoriasis;RA;SLE;UC | 0 | 0.206 | 0.4904 | 0 | 0.4256 | 0.3989 |  | NO_GO_WAVE34_GENETICS_EXPRESSION_DRUGGABILITY |  | NO_GO_FRESH_SCAN |
| RGS1 | NO_REOPEN_GENETICS_FIRST_ROUTE | 5 | 11 | local_cellstate_ge3_no_negative;strict_ms_local_nominal;residual_support_ge2;druggability_or_modality;coloc_or_mr_grade;wave34_not_no_go | False | 21 | Celiac;MS;Psoriasis;SLE;T1D | 0.7618 | -0.04253 | 0.8978 | 0 | 0 | 0.3112 |  | NO_GO_WAVE34_GENETICS_EXPRESSION_DRUGGABILITY |  | NO_GO_FRESH_SCAN |
| GATA3 | NO_REOPEN_GENETICS_FIRST_ROUTE | 5 | 11 | local_cellstate_ge3_no_negative;strict_ms_local_nominal;residual_support_ge2;druggability_or_modality;coloc_or_mr_grade;wave34_not_no_go | False | 20 | AITD;Crohn;MS;Psoriasis;RA;T1D | 0.679 | -0.6133 | 0.6068 | 0 | 0 | 0.4757 |  | NO_GO_WAVE34_GENETICS_EXPRESSION_DRUGGABILITY |  | NO_GO_FRESH_SCAN |

## Wave128 Genes Restored By Exact Closure

_No rows._

## Interpretation

This audit fixes a real methodological defect. A corrected route can only be
accepted if it becomes `TESTABLE_FRESH_ROUTE` in Wave122 or
`REOPEN_GENETICS_FIRST_ROUTE` in Wave128. Parked or no-go rows are not V3
therapeutic claims.

## Reproducibility

- Script: `scripts/v3_wave133_closure_hygiene_correction.py`
- Outputs: `results_v3/wave133_closure_hygiene_correction/`
- Seed: `20260527`
