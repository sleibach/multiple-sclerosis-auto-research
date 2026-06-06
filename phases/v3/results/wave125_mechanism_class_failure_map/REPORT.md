# Wave125 Mechanism-Class Failure Map

## Bottom Line

Branch call: `MECHANISM_FAILURE_MAP_COMPLETE`.

This wave maps why the top 300 Wave122 candidates fail, so the next pivot is
based on failure structure rather than another single-gene rank.

## Failure Modes

| failure_mode | count | fraction_top_n |
| --- | --- | --- |
| failure_response_absent | 297 | 0.99 |
| failure_no_modality | 280 | 0.9333 |
| failure_no_causal_channel | 274 | 0.9133 |
| failure_ms_not_fdr | 139 | 0.4633 |
| failure_marker_only | 36 | 0.12 |
| failure_safety_or_prior | 22 | 0.07333 |

## Mechanism Classes

| mechanism_class | n_top | best_gene | best_score | n_marker_only | n_safety_or_prior | n_no_causal_channel | n_no_modality | n_ms_not_fdr | n_response_absent | top_genes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ros_host_defense | 1 | NCF2 | 4.9 | 0 | 1 | 0 | 0 | 1 | 1 | NCF2 |
| chemokine_neutrophil | 5 | CXCR2 | 4.6 | 1 | 3 | 2 | 3 | 1 | 4 | CXCR2;CXCL9;CCL20;CCL2;CCL19 |
| other | 251 | TNFAIP8L1 | 4.3 | 22 | 13 | 235 | 237 | 116 | 251 | TNFAIP8L1;DAP;LTA4H;NCK1;PLEK2;PPP3CA;SNX10;ABHD2;CCNI;CDV3 |
| adhesion_matrix | 9 | FMNL2 | 4.3 | 5 | 0 | 9 | 9 | 6 | 9 | FMNL2;DIAPH1;ITGAV;LIMS1;SDC4;ITGB1;ITGA2;ITGA5;ITGB4 |
| intracellular_housekeeping | 9 | CBX3 | 4.3 | 5 | 0 | 9 | 9 | 9 | 9 | CBX3;AQR;PPIL3;BTF3;RPL17;MRPL30;CBX1;MRPL11;MRPL44 |
| ifn_antigen_processing | 16 | CRTAP | 4.1 | 1 | 5 | 10 | 13 | 3 | 14 | CRTAP;IFI30;ASAH1;CTSB;SP140;GALC;STAT3;IFITM2;IFITM3;NLRC5 |
| secreted_remodeling | 6 | CHI3L1 | 4.1 | 1 | 0 | 6 | 6 | 1 | 6 | CHI3L1;COL4A1;COL4A2;MMP15;MMP7;TIMP1 |
| lipid_apoe_apoc | 1 | APOC1 | 4.1 | 1 | 0 | 1 | 1 | 1 | 1 | APOC1 |
| lysosomal_protease | 2 | CTSL | 2.4 | 0 | 0 | 2 | 2 | 1 | 2 | CTSL;CTSC |

## Pivot Recommendations

| mechanism_class | n_top | best_gene | best_score | n_marker_only | n_safety_or_prior | n_no_causal_channel | n_no_modality | n_ms_not_fdr | n_response_absent | top_genes | pivot_recommendation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ros_host_defense | 1 | NCF2 | 4.9 | 0 | 1 | 0 | 0 | 1 | 1 | NCF2 | avoid_direct_targeting; use as stratification/readout only |
| chemokine_neutrophil | 5 | CXCR2 | 4.6 | 1 | 3 | 2 | 3 | 1 | 4 | CXCR2;CXCL9;CCL20;CCL2;CCL19 | avoid_direct_targeting; use as stratification/readout only |
| other | 251 | TNFAIP8L1 | 4.3 | 22 | 13 | 235 | 237 | 116 | 251 | TNFAIP8L1;DAP;LTA4H;NCK1;PLEK2;PPP3CA;SNX10;ABHD2;CCNI;CDV3 | search upstream druggable regulator, not class member |
| adhesion_matrix | 9 | FMNL2 | 4.3 | 5 | 0 | 9 | 9 | 6 | 9 | FMNL2;DIAPH1;ITGAV;LIMS1;SDC4;ITGB1;ITGA2;ITGA5;ITGB4 | requires perturbation data before reopening |
| intracellular_housekeeping | 9 | CBX3 | 4.3 | 5 | 0 | 9 | 9 | 9 | 9 | CBX3;AQR;PPIL3;BTF3;RPL17;MRPL30;CBX1;MRPL11;MRPL44 | requires perturbation data before reopening |
| ifn_antigen_processing | 16 | CRTAP | 4.1 | 1 | 5 | 10 | 13 | 3 | 14 | CRTAP;IFI30;ASAH1;CTSB;SP140;GALC;STAT3;IFITM2;IFITM3;NLRC5 | avoid_direct_targeting; use as stratification/readout only |
| secreted_remodeling | 6 | CHI3L1 | 4.1 | 1 | 0 | 6 | 6 | 1 | 6 | CHI3L1;COL4A1;COL4A2;MMP15;MMP7;TIMP1 | search upstream druggable regulator, not class member |
| lipid_apoe_apoc | 1 | APOC1 | 4.1 | 1 | 0 | 1 | 1 | 1 | 1 | APOC1 | low_priority_manual_review |
| lysosomal_protease | 2 | CTSL | 2.4 | 0 | 0 | 2 | 2 | 1 | 2 | CTSL;CTSC | search upstream druggable regulator, not class member |

## Interpretation

If the dominant failure is marker-only recurrence or absence of causal/
perturbational channels, more expression ranking will not solve the problem.
The next useful pivot must add a new modality or explicitly search upstream
drugged regulators of the recurring marker classes.

## Reproducibility

- Script: `scripts/v3_wave125_mechanism_class_failure_map.py`
- Output: `results_v3/wave125_mechanism_class_failure_map/mechanism_class_failure_summary.tsv`
- Seed: `20260527`
