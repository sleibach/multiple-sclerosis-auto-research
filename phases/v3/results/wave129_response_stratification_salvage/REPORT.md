# Wave129 Response/Stratification Salvage

## Bottom Line

Branch call: `BIOMARKER_ONLY_SIGNAL_EXISTS`.

This wave separates response biomarkers from target nominations. A gene can
have useful anti-TNF nonresponse stratification value while remaining invalid as
a direct therapeutic target.

## Decisions

| gene | modules | call | biomarker_candidate | target_nomination_allowed | target_closed_or_prior | cross_system | ibd_fdr_contexts_ge2 | ra_fdr10 | predictive_auc_ge_0_75 | effect_abs_g_ge_1 | ms_context_trend | weighted_mean_hedges_g_responder_minus_non | median_auc_high_score_nonresponse | fdr10_nonresponse_contexts | fdr_ra | ra_replication_call | cross_system_call | ms_delta_log2 | ms_p | wave122_call |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IL1B | inflammatory_nfkb | BIOMARKER_STRATIFICATION_CANDIDATE_NOT_TARGET | True | False | True | True | True | True | True | True | False | -1.695 | 0.8974 | 3 | 0.09947 | RA_BASELINE_DIRECTIONAL_REPLICATION | PARK_CROSS_SYSTEM_ANTITNF_RESISTANCE_GENE |  |  |  |
| LAMP3 | lysosomal_apc | BIOMARKER_STRATIFICATION_CANDIDATE_NOT_TARGET | True | False | True | True | True | True | True | True | False | -1.097 | 0.7589 | 2 | 0.02614 | RA_BASELINE_DIRECTIONAL_REPLICATION | PARK_CROSS_SYSTEM_ANTITNF_RESISTANCE_GENE |  |  |  |
| TREM1 | inflammatory_nfkb | NO_STRATIFICATION_SALVAGE | False | False | True | False | True | True | True | True | False | -1.629 | 0.8826 | 3 | 0.09947 | NO_RA_BASELINE_REPLICATION | IBD_RESTRICTED_OR_UNRESOLVED_ANTITNF_RESISTANCE_GENE | 0.1492 | 0.7752 | NO_GO_FRESH_SCAN |
| LAMP2 | lysosomal_apc | NO_STRATIFICATION_SALVAGE | False | False | False | False | True | True | True | True | False | -1.068 | 0.835 | 3 | 0.02638 | NO_RA_BASELINE_REPLICATION | IBD_RESTRICTED_OR_UNRESOLVED_ANTITNF_RESISTANCE_GENE | 0.1348 | 0.2874 | NO_GO_FRESH_SCAN |
| CD44 | mif_cd74_receptor_state | NO_STRATIFICATION_SALVAGE | False | False | True | False | True | True | True | True | False | -1.305 | 0.7995 | 3 | 0.02614 | NO_RA_BASELINE_REPLICATION | IBD_RESTRICTED_OR_UNRESOLVED_ANTITNF_RESISTANCE_GENE |  |  |  |
| CCL2 | inflammatory_nfkb | NO_STRATIFICATION_SALVAGE | False | False | True | False | True | True | True | True | False | -1.41 | 0.825 | 2 | 0.04175 | NO_RA_BASELINE_REPLICATION | IBD_RESTRICTED_OR_UNRESOLVED_ANTITNF_RESISTANCE_GENE | 0.04905 | 0.9065 | NO_GO_FRESH_SCAN |
| NFKBIA | inflammatory_nfkb | NO_STRATIFICATION_SALVAGE | False | False | False | False | False | True | False | False | False | -0.6615 | 0.6687 | 1 | 0.02638 | NO_RA_BASELINE_REPLICATION | IBD_RESTRICTED_OR_UNRESOLVED_ANTITNF_RESISTANCE_GENE | 0.2903 | 0.3094 | NO_GO_FRESH_SCAN |
| CTSB | lysosomal_apc | NO_STRATIFICATION_SALVAGE | False | False | True | False | False | True | False | False | False | -0.7232 | 0.6583 | 1 | 0.09947 | NO_RA_BASELINE_REPLICATION | IBD_RESTRICTED_OR_UNRESOLVED_ANTITNF_RESISTANCE_GENE | -0.06 | 0.8141 | NO_GO_FRESH_SCAN |
| STAT1 | ifn_apc | NO_STRATIFICATION_SALVAGE | False | False | False | False | False | True | False | False | False | -0.6552 | 0.6445 | 1 | 0.04175 | NO_RA_BASELINE_REPLICATION | IBD_RESTRICTED_OR_UNRESOLVED_ANTITNF_RESISTANCE_GENE | 0.5379 | 0.1363 | NO_GO_FRESH_SCAN |
| CXCL8 | inflammatory_nfkb | NO_STRATIFICATION_SALVAGE | False | False | False | False | True | False | True | True | False | -1.702 | 0.8849 | 3 | 0.603 | RA_BASELINE_SAME_DIRECTION_WEAK | IBD_RESTRICTED_OR_UNRESOLVED_ANTITNF_RESISTANCE_GENE | -0.088 | 0.8091 | NO_GO_FRESH_SCAN |
| CCL4 | inflammatory_nfkb | NO_STRATIFICATION_SALVAGE | False | False | False | False | True | False | True | True | False | -1.533 | 0.8694 | 3 |  | NO_RA_BASELINE_REPLICATION | IBD_RESTRICTED_OR_UNRESOLVED_ANTITNF_RESISTANCE_GENE | -0.09812 | 0.8114 | NO_GO_FRESH_SCAN |
| CCL3 | inflammatory_nfkb | NO_STRATIFICATION_SALVAGE | False | False | False | False | True | False | True | True | False | -1.391 | 0.8479 | 3 |  | NO_RA_BASELINE_REPLICATION | IBD_RESTRICTED_OR_UNRESOLVED_ANTITNF_RESISTANCE_GENE | -0.2101 | 0.5505 | NO_GO_FRESH_SCAN |
| ACSL1 | lipid_loader_repair | NO_STRATIFICATION_SALVAGE | False | False | True | False | True | False | True | True | False | -1.328 | 0.8218 | 2 | 0.6816 | NO_RA_BASELINE_REPLICATION | IBD_RESTRICTED_OR_UNRESOLVED_ANTITNF_RESISTANCE_GENE |  |  |  |
| OSM | inflammatory_nfkb | NO_STRATIFICATION_SALVAGE | False | False | False | False | True | False | True | True | False | -1.431 | 0.8146 | 2 | 0.603 | RA_BASELINE_SAME_DIRECTION_WEAK | IBD_RESTRICTED_OR_UNRESOLVED_ANTITNF_RESISTANCE_GENE | 0.07623 | 0.859 | NO_GO_FRESH_SCAN |
| IFI30 | ifn_apc;lysosomal_apc | NO_STRATIFICATION_SALVAGE | False | False | True | False | True | False | True | False | False | -0.9749 | 0.7945 | 2 | 0.839 | NO_RA_BASELINE_REPLICATION | IBD_RESTRICTED_OR_UNRESOLVED_ANTITNF_RESISTANCE_GENE | 0.2102 | 0.3799 | NO_GO_FRESH_SCAN |
| SPP1 | lipid_loader_repair | NO_STRATIFICATION_SALVAGE | False | False | True | False | True | False | True | True | False | -1.234 | 0.7854 | 2 | 0.7569 | NO_RA_BASELINE_REPLICATION | IBD_RESTRICTED_OR_UNRESOLVED_ANTITNF_RESISTANCE_GENE |  |  |  |
| GBP1 | ifn_apc | NO_STRATIFICATION_SALVAGE | False | False | False | False | True | False | False | False | True | -0.845 | 0.732 | 2 | 0.2859 | NO_RA_BASELINE_REPLICATION | IBD_RESTRICTED_OR_UNRESOLVED_ANTITNF_RESISTANCE_GENE | 0.4914 | 0.06818 | NO_GO_FRESH_SCAN |
| CXCL10 | ifn_apc | NO_STRATIFICATION_SALVAGE | False | False | False | False | True | False | False | False | True | -0.8556 | 0.728 | 2 | 0.8823 | RA_BASELINE_SAME_DIRECTION_WEAK | IBD_RESTRICTED_OR_UNRESOLVED_ANTITNF_RESISTANCE_GENE | 1.083 | 0.09617 | NO_GO_FRESH_SCAN |
| CXCR4 | mif_cd74_receptor_state | NO_STRATIFICATION_SALVAGE | False | False | False | False | False | False | False | False | False | -0.7992 | 0.7138 | 1 | 0.1262 | NO_RA_BASELINE_REPLICATION | IBD_RESTRICTED_OR_UNRESOLVED_ANTITNF_RESISTANCE_GENE | 0.3121 | 0.3177 | NO_GO_FRESH_SCAN |
| TNF | inflammatory_nfkb | NO_STRATIFICATION_SALVAGE | False | False | False | False | False | False | False | False | False | -0.6903 | 0.7106 | 1 |  | NO_RA_BASELINE_REPLICATION | IBD_RESTRICTED_OR_UNRESOLVED_ANTITNF_RESISTANCE_GENE | 0.06707 | 0.8723 | NO_GO_FRESH_SCAN |
| HLA-DRB1 | hla_ii_apc;ifn_apc;mif_cd74_receptor_state | NO_STRATIFICATION_SALVAGE | False | False | False | False | False | False | False | False | True | -0.5089 | 0.6982 | 1 | 0.1765 | NO_RA_BASELINE_REPLICATION | IBD_RESTRICTED_OR_UNRESOLVED_ANTITNF_RESISTANCE_GENE | 0.5469 | 0.05777 | NO_GO_FRESH_SCAN |
| IRF1 | ifn_apc | NO_STRATIFICATION_SALVAGE | False | False | False | False | False | False | False | False | False | -0.5844 | 0.6434 | 1 | 0.7569 | NO_RA_BASELINE_REPLICATION | IBD_RESTRICTED_OR_UNRESOLVED_ANTITNF_RESISTANCE_GENE | -0.0304 | 0.9223 | NO_GO_FRESH_SCAN |
| APOE | lipid_loader_repair | NO_STRATIFICATION_SALVAGE | False | False | False | False | False | False | False | False | False | -0.4744 | 0.625 | 1 | 0.5512 | RA_BASELINE_SAME_DIRECTION_WEAK | IBD_RESTRICTED_OR_UNRESOLVED_ANTITNF_RESISTANCE_GENE | 0.3729 | 0.1202 | NO_GO_FRESH_SCAN |
| CTSS | lysosomal_apc | NO_STRATIFICATION_SALVAGE | False | False | False | False | False | False | False | False | False | -0.3122 | 0.5363 | 1 | 0.1234 | NO_RA_BASELINE_REPLICATION | IBD_RESTRICTED_OR_UNRESOLVED_ANTITNF_RESISTANCE_GENE | 0.1899 | 0.1407 | NO_GO_FRESH_SCAN |
| MERTK | complement_phagocytosis;lipid_loader_repair | NO_STRATIFICATION_SALVAGE | False | False | True | False | False | False | False | False | False | -0.3859 | 0.5264 | 1 | 0.7569 | NO_RA_BASELINE_REPLICATION | IBD_RESTRICTED_OR_UNRESOLVED_ANTITNF_RESISTANCE_GENE | 0.2471 | 0.4293 | NO_GO_FRESH_SCAN |

## Interpretation

The robust response signal is biomarker-like. It does not rescue a V3 target
nomination because the strongest replicated genes are already closed, crowded,
or marker-only. However, it may define a patient stratum for future analysis.

## Reproducibility

- Script: `scripts/v3_wave129_response_stratification_salvage.py`
- Output: `results_v3/wave129_response_stratification_salvage/response_stratification_salvage_decisions.tsv`
- Seed: `20260527`
