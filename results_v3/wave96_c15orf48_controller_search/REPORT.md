# Wave96 C15ORF48 Controller Search

Random seed: `20260527`.

## Question

Can the C15ORF48-positive autoimmune mitochondrial/inflammatory-brake
state be converted into a druggable controller or intervention point?

## Anchor Contexts

Strict C15ORF48-positive contexts: `4`.
Trend C15ORF48-positive contexts: `7`.

Strict contexts:

| analysis | disease_name | compartment | role | c15_delta_log2_cpm | c15_p | c15_fdr |
| --- | --- | --- | --- | --- | --- | --- |
| ibd_crohn_myeloid | Crohn disease | colon myeloid | myeloid_apc | 3.882 | 0.0006135 | 0.08481 |
| ibd_uc_myeloid | ulcerative colitis | colon myeloid | myeloid_apc | 4.446 | 2.948e-05 | 0.02875 |
| t1d_stellate_cell | type 1 diabetes mellitus | pancreatic stellate cell | tissue_resident | 3.093 | 0.01543 | 0.3164 |
| t1d_endothelial_cell | type 1 diabetes mellitus | pancreatic endothelial cell | tissue_resident | 3.209 | 0.001372 | 0.1205 |

## Verdict

Reopened controller candidates: `0`.
Parked proximal candidates: `92`.

## Call Counts

| wave96_call | n |
| --- | --- |
| NO_GO_C15_CONTROLLER_SEARCH | 25066 |
| PARK_C15_COSTATE_MARKER_NO_MODALITY | 79 |
| NO_GO_PRIOR_OR_BLOCKER | 17 |
| PARK_C15_PROXIMAL_INTERVENTION_CANDIDATE | 13 |

## Top Ranked Rows

| gene | wave96_call | wave96_score | critical_gate_count | support_gate_count | c15_trend_positive_context_count | c15_trend_positive_disease_count | c15_trend_negative_context_count | c15_state_pearson_r | donor_case_positive_context_count | donor_case_positive_disease_count | donor_case_median_spearman | ms_delta_log2 | ms_p | wave62_strong_qtl_coloc_disease_count | wave55_n_genetic_diseases_ge_0_25 | chembl_activity_count | w68_remission_adjusted_fdr | w37_screen_call | wave96_reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GBP1 | NO_GO_C15_CONTROLLER_SEARCH | 20.9 | 4 | 1 | 3 | 3 | 0 | 0.2004 | 4 | 3 | 0.6 | 0.4914 | 0.06818 | 0 | 0 | 0 | 0.01712 |  | insufficient C15 state proximity or donor-level co-state support; failures=gate_c15_contrast_state;gate_genetics |
| CXCL9 | NO_GO_C15_CONTROLLER_SEARCH | 17.61 | 4 | 1 | 4 | 4 | 0 | 0.3057 | 0 | 0 | -0.3354 | 2.554 | 0.03099 | 0 | 0 | 0 | 0.01857 | KO_IMPAIRS_EFFEROCYTOSIS_POSITIVE_REGULATOR | insufficient C15 state proximity or donor-level co-state support; failures=gate_donor_costate;gate_genetics |
| CBX3 | NO_GO_C15_CONTROLLER_SEARCH | 18.31 | 4 | 0 | 5 | 3 | 0 | -0.09698 | 2 | 1 | 0.3 | 0.3505 | 0.01659 | 0 | 0 | 4 |  | UNRESOLVED | insufficient C15 state proximity or donor-level co-state support; failures=gate_c15_contrast_state;gate_genetics |
| IFI30 | NO_GO_C15_CONTROLLER_SEARCH | 18.28 | 3 | 3 | 2 | 2 | 0 | 0.3887 | 1 | 1 | 0.1 | 0.2102 | 0.3799 | 3 | 0 | 0 | 0.02368 | UNRESOLVED | insufficient C15 state proximity or donor-level co-state support; failures=gate_c15_contrast_state;gate_modality |
| PTPN2 | NO_GO_C15_CONTROLLER_SEARCH | 20.85 | 3 | 2 | 3 | 3 | 0 | 0.6751 | 4 | 3 | 0.6455 | -0.005942 | 0.9844 | 5 | 9 | 1279 |  | UNRESOLVED | insufficient C15 state proximity or donor-level co-state support; failures=gate_c15_contrast_state;gate_ms_anchor |
| NCF2 | NO_GO_C15_CONTROLLER_SEARCH | 20.09 | 3 | 2 | 2 | 2 | 0 | 0.7945 | 6 | 3 | 0.7826 | 0.5994 | 0.01942 | 1 | 3 | 0 | 0.02012 | UNRESOLVED | insufficient C15 state proximity or donor-level co-state support; failures=gate_c15_contrast_state;gate_modality |
| ARHGAP31 | NO_GO_C15_CONTROLLER_SEARCH | 18.97 | 3 | 2 | 2 | 2 | 0 | 0.7351 | 3 | 2 | 0.4 | -0.1575 | 0.5702 | 3 | 2 | 0 | 0.007838 | UNRESOLVED | insufficient C15 state proximity or donor-level co-state support; failures=gate_c15_contrast_state;gate_modality |
| STAT4 | NO_GO_C15_CONTROLLER_SEARCH | 18.53 | 3 | 2 | 2 | 2 | 0 | 0.5142 | 2 | 2 | 0.3584 | 0.8684 | 0.4607 | 7 | 9 | 0 | 0.007838 | UNRESOLVED | insufficient C15 state proximity or donor-level co-state support; failures=gate_c15_contrast_state;gate_modality |
| SP140 | NO_GO_C15_CONTROLLER_SEARCH | 17.69 | 3 | 2 | 2 | 2 | 0 | 0.5944 | 1 | 1 | 0.2907 | -0.08676 | 0.7262 | 3 | 6 | 0 | 0.04687 | UNRESOLVED | insufficient C15 state proximity or donor-level co-state support; failures=gate_c15_contrast_state;gate_modality |
| CD80 | NO_GO_C15_CONTROLLER_SEARCH | 14.69 | 3 | 2 | 1 | 1 | 0 | 0.8451 | 1 | 1 | 0.4559 | -0.2206 | 0.8621 | 3 | 2 | 0 | 0.03159 | UNRESOLVED | insufficient C15 state proximity or donor-level co-state support; failures=gate_c15_contrast_state;gate_modality |
| DCLRE1B | NO_GO_C15_CONTROLLER_SEARCH | 8.905 | 3 | 2 | 2 | 1 | 1 | -0.2976 | 1 | 1 | 0.3714 | 0.8296 | 0.03066 | 5 | 2 | 0 | 0.03729 | UNRESOLVED | insufficient C15 state proximity or donor-level co-state support; failures=gate_c15_contrast_state;gate_modality |
| HLA-DRB1 | NO_GO_C15_CONTROLLER_SEARCH | 8.876 | 3 | 2 | 3 | 1 | 0 | -0.5621 | 0 | 0 |  | 0.5469 | 0.05777 | 0 | 0 | 105 | 0.007838 |  | insufficient C15 state proximity or donor-level co-state support; failures=gate_c15_contrast_state;gate_donor_costate;gate_genetics |
| IFITM2 | NO_GO_C15_CONTROLLER_SEARCH | 22.82 | 3 | 1 | 7 | 4 | 0 | 0.1608 | 3 | 2 | 0.3143 | -0.5241 | 0.2031 | 0 | 1 | 0 | 0.01398 | UNRESOLVED | insufficient C15 state proximity or donor-level co-state support; failures=gate_c15_contrast_state;gate_ms_anchor;gate_genetics |
| TMEM167A | NO_GO_C15_CONTROLLER_SEARCH | 21.61 | 3 | 1 | 5 | 4 | 0 | 0.05389 | 4 | 3 | 0.6545 | -0.05936 | 0.7753 | 0 | 0 | 0 | 0.01278 |  | insufficient C15 state proximity or donor-level co-state support; failures=gate_c15_contrast_state;gate_ms_anchor;gate_genetics |
| TIMP1 | NO_GO_C15_CONTROLLER_SEARCH | 19.96 | 3 | 1 | 5 | 3 | 0 | 0.2298 | 2 | 2 | 0.4 | -0.5837 | 0.4152 | 0 | 0 | 0 | 0.02305 | UNRESOLVED | insufficient C15 state proximity or donor-level co-state support; failures=gate_c15_contrast_state;gate_ms_anchor;gate_genetics |
| IFITM3 | NO_GO_C15_CONTROLLER_SEARCH | 19.85 | 3 | 1 | 6 | 4 | 0 | -0.3249 | 1 | 1 | 0.02857 | -0.4945 | 0.2965 | 0 | 0 | 0 | 0.02955 | UNRESOLVED | insufficient C15 state proximity or donor-level co-state support; failures=gate_c15_contrast_state;gate_ms_anchor;gate_genetics |
| VMP1 | NO_GO_C15_CONTROLLER_SEARCH | 19.46 | 3 | 1 | 3 | 3 | 0 | -0.02134 | 4 | 3 | 0.6571 | -0.2229 | 0.2881 | 1 | 0 | 0 | 0.02357 | UNRESOLVED | insufficient C15 state proximity or donor-level co-state support; failures=gate_c15_contrast_state;gate_modality;gate_genetics |
| KCNJ2 | NO_GO_C15_CONTROLLER_SEARCH | 18.84 | 3 | 1 | 3 | 3 | 0 | 0.6713 | 2 | 2 | 0.2052 | 0.002426 | 0.9931 | 0 | 1 | 23 | 0.01202 | UNRESOLVED | insufficient C15 state proximity or donor-level co-state support; failures=gate_c15_contrast_state;gate_ms_anchor;gate_genetics |
| LTA4H | NO_GO_C15_CONTROLLER_SEARCH | 18.77 | 3 | 1 | 3 | 3 | 0 | 0.8862 | 4 | 2 | 0.6571 | 0.8088 | 0.006357 | 0 | 0 | 0 | 0.01462 | UNRESOLVED | insufficient C15 state proximity or donor-level co-state support; failures=gate_c15_contrast_state;gate_modality;gate_genetics |
| PSMB8 | NO_GO_C15_CONTROLLER_SEARCH | 18.42 | 3 | 1 | 4 | 4 | 0 | 0.2076 | 4 | 2 | 0.6273 | 0.2543 | 0.2663 | 0 | 0 | 689 | 0.04048 | UNRESOLVED | insufficient C15 state proximity or donor-level co-state support; failures=gate_c15_contrast_state;gate_ms_anchor;gate_genetics |
| CFP | NO_GO_C15_CONTROLLER_SEARCH | 17.5 | 3 | 1 | 3 | 3 | 0 | 0.7476 | 1 | 1 | -0.2091 | -2.298 | 0.0365 | 0 | 0 | 0 | 0.09156 | UNRESOLVED | insufficient C15 state proximity or donor-level co-state support; failures=gate_c15_contrast_state;gate_ms_anchor;gate_genetics |
| SP110 | NO_GO_C15_CONTROLLER_SEARCH | 17.31 | 3 | 1 | 3 | 3 | 0 | 0.1571 | 2 | 2 | 0.3143 | -0.2597 | 0.3345 | 2 | 1 | 0 |  | UNRESOLVED | insufficient C15 state proximity or donor-level co-state support; failures=gate_c15_contrast_state;gate_modality |
| IL2RG | NO_GO_C15_CONTROLLER_SEARCH | 17.05 | 3 | 1 | 2 | 2 | 0 | 0.5266 | 2 | 2 | 0.2571 | 0.768 | 0.01702 | 0 | 0 | 0 | 0.09085 | UNRESOLVED | insufficient C15 state proximity or donor-level co-state support; failures=gate_c15_contrast_state;gate_modality;gate_genetics |
| SLC44A1 | NO_GO_C15_CONTROLLER_SEARCH | 17.03 | 3 | 1 | 2 | 2 | 0 | 0.5156 | 2 | 2 | 0.5429 | 0.416 | 0.06655 | 0 | 0 | 0 | 0.01238 | UNRESOLVED | insufficient C15 state proximity or donor-level co-state support; failures=gate_c15_contrast_state;gate_modality;gate_genetics |
| NMI | NO_GO_C15_CONTROLLER_SEARCH | 16.79 | 3 | 1 | 3 | 3 | 0 | -0.1044 | 5 | 3 | 0.7 | -0.1367 | 0.537 | 0 | 0 | 0 | 0.03612 | UNRESOLVED | insufficient C15 state proximity or donor-level co-state support; failures=gate_c15_contrast_state;gate_ms_anchor;gate_genetics |

## Interpretation Guardrail

C15ORF48 co-state evidence is not causality. A candidate can only be
reopened here if the C15 contrast vector, donor-level co-state validation,
MS anchoring, modality, and independent support channels agree. Otherwise
the output is a branch map for the next forcing test.

## Output Files

- `results_v3/wave96_c15orf48_controller_search/c15orf48_anchor_contexts.tsv`
- `results_v3/wave96_c15orf48_controller_search/contrast_state_rank_all.tsv`
- `results_v3/wave96_c15orf48_controller_search/pre_donor_controller_rank.tsv`
- `results_v3/wave96_c15orf48_controller_search/donor_level_c15_costate_correlations.tsv`
- `results_v3/wave96_c15orf48_controller_search/donor_level_c15_costate_summary.tsv`
- `results_v3/wave96_c15orf48_controller_search/c15orf48_controller_candidate_rank.tsv`
- `results_v3/wave96_c15orf48_controller_search/summary.json`
- `results_v3/wave96_c15orf48_controller_search/REPORT.md`
