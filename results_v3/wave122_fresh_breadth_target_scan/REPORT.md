# Wave122 Fresh Breadth-First Target Scan

## Bottom Line

Branch call: `NO_FRESH_ROUTE_FROM_LOCAL_SCAN`.

This scan restarts from local evidence products after the Wave110/Wave91/Wave95
survivor-map branch closed. It excludes closure-ledger genes and requires
multiple independent support channels before a route can be reopened.

## Top Candidates

| gene | call | fresh_score | support_channels | ms | broad_cell_state | response | genetics | perturbation_or_model | modality | ms_delta_log2 | ms_p | ms_fdr | broad_positive_disease_count | broad_positive_diseases | response_contexts | strong_l2g_disease_count | strong_qtl_coloc_disease_count | wave55_genetic_disease_count | blocker_flag | blocker_text |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NCF2 | NO_GO_FRESH_SCAN | 4.9 | 4 | True | False | False | True | True | True | 0.5994 | 0.01942 | 0.8373 | 2 | Crohn disease;ulcerative colitis | 0 | 2 | 1 | 0 | True |   NO_REOPEN_BLOCKED_BRANCH NOX2 host-defense/CGD directionality risk NO_GO_WAVE62_TARGET_RESOLUTION |
| CXCR2 | NO_GO_FRESH_SCAN | 4.6 | 4 | False | True | False | True | True | True | 0.8298 | 0.3775 | 0.9141 | 3 | Crohn disease;psoriasis;ulcerative colitis | 0 | 0 | 1 | 0 | True |   PARK_PRIOR_ART_OR_HOST_DEFENSE_PENALIZED chemokine/neutrophil route prior audited and infection-risk broad NO_GO_WAVE62_TARGET_RESOLUTION |
| CBX3 | NO_GO_FRESH_SCAN | 4.3 | 2 | True | True | False | False | False | False | 0.3505 | 0.01659 | 0.8373 | 4 | Crohn disease;psoriasis;type 1 diabetes mellitus;ulcerative colitis | 0 | 0 | 0 | 0 | False |      |
| FMNL2 | NO_GO_FRESH_SCAN | 4.3 | 2 | True | True | False | False | False | False | 0.4117 | 0.03238 | 0.8507 | 4 | Crohn disease;psoriasis;type 1 diabetes mellitus;ulcerative colitis | 0 | 0 | 0 | 0 | False |   NO_REOPEN_INSUFFICIENT_CONVERGENCE candidate lacks direct perturbation or model support  |
| TNFAIP8L1 | NO_GO_FRESH_SCAN | 4.3 | 2 | True | True | False | False | False | False | 0.4563 | 0.008562 | 0.8349 | 4 | Crohn disease;psoriasis;type 1 diabetes mellitus;ulcerative colitis | 0 | 0 | 0 | 0 | False |      |
| APOC1 | NO_GO_FRESH_SCAN | 4.1 | 2 | True | True | False | False | False | False | 0.8063 | 0.03335 | 0.8507 | 3 | Sjogren syndrome;type 1 diabetes mellitus;ulcerative colitis | 0 | 0 | 0 | 0 | False |      |
| AQR | NO_GO_FRESH_SCAN | 4.1 | 2 | True | True | False | False | False | False | 0.2576 | 0.04593 | 0.8735 | 3 | Crohn disease;psoriasis;ulcerative colitis | 0 | 0 | 0 | 0 | False |      |
| CHI3L1 | NO_GO_FRESH_SCAN | 4.1 | 2 | True | True | False | False | False | False | 2.007 | 0.004613 | 0.8345 | 3 | Crohn disease;type 1 diabetes mellitus;ulcerative colitis | 0 | 0 | 0 | 0 | False |      |
| CRTAP | NO_GO_FRESH_SCAN | 4.1 | 2 | True | True | False | False | False | False | 0.3844 | 0.04989 | 0.8769 | 3 | Crohn disease;type 1 diabetes mellitus;ulcerative colitis | 0 | 0 | 0 | 0 | False |      |
| CXCL9 | NO_GO_FRESH_SCAN | 4.1 | 2 | True | True | False | False | False | False | 2.554 | 0.03099 | 0.8507 | 3 | Sjogren syndrome;type 1 diabetes mellitus;ulcerative colitis | 0 | 0 | 0 | 0 | False |      |
| DAP | NO_GO_FRESH_SCAN | 4.1 | 2 | True | True | False | False | False | False | 0.3933 | 0.008069 | 0.8345 | 3 | Crohn disease;psoriasis;ulcerative colitis | 0 | 0 | 0 | 0 | False |   NO_REOPEN_INSUFFICIENT_CONVERGENCE candidate lacks direct perturbation or model support  |
| LTA4H | NO_GO_FRESH_SCAN | 4.1 | 2 | True | True | False | False | False | False | 0.8088 | 0.006357 | 0.8345 | 3 | Crohn disease;type 1 diabetes mellitus;ulcerative colitis | 0 | 0 | 0 | 0 | False |      |
| NCK1 | NO_GO_FRESH_SCAN | 4.1 | 2 | True | True | False | False | False | False | 0.445 | 0.005556 | 0.8345 | 3 | Crohn disease;type 1 diabetes mellitus;ulcerative colitis | 0 | 0 | 0 | 0 | False |      |
| PLEK2 | NO_GO_FRESH_SCAN | 4.1 | 2 | True | True | False | False | False | False | 3.046 | 0.007379 | 0.8345 | 3 | Crohn disease;type 1 diabetes mellitus;ulcerative colitis | 0 | 0 | 0 | 0 | False |      |
| PPIL3 | NO_GO_FRESH_SCAN | 4.1 | 2 | True | True | False | False | False | False | 0.6072 | 0.01829 | 0.8373 | 3 | Crohn disease;type 1 diabetes mellitus;ulcerative colitis | 0 | 0 | 0 | 0 | False |      |
| PPP3CA | NO_GO_FRESH_SCAN | 4.1 | 2 | True | True | False | False | False | False | 0.3663 | 0.03434 | 0.8507 | 3 | Crohn disease;type 1 diabetes mellitus;ulcerative colitis | 0 | 0 | 0 | 0 | False |      |
| SNX10 | NO_GO_FRESH_SCAN | 4.1 | 2 | True | True | False | False | False | False | 0.7124 | 0.01274 | 0.8349 | 3 | Crohn disease;type 1 diabetes mellitus;ulcerative colitis | 0 | 0 | 0 | 0 | False |      |
| ABHD2 | NO_GO_FRESH_SCAN | 3.9 | 2 | True | True | False | False | False | False | 0.7082 | 0.003244 | 0.8345 | 2 | Crohn disease;ulcerative colitis | 0 | 0 | 0 | 0 | False |      |
| BTF3 | NO_GO_FRESH_SCAN | 3.9 | 2 | True | True | False | False | False | False | 0.3048 | 0.0168 | 0.8373 | 2 | Sjogren syndrome;ulcerative colitis | 0 | 0 | 0 | 0 | False |      |
| CCNI | NO_GO_FRESH_SCAN | 3.9 | 2 | True | True | False | False | False | False | 0.4909 | 0.02088 | 0.8373 | 2 | Crohn disease;ulcerative colitis | 0 | 0 | 0 | 0 | False |      |
| CDV3 | NO_GO_FRESH_SCAN | 3.9 | 2 | True | True | False | False | False | False | 0.225 | 0.03659 | 0.8507 | 2 | Crohn disease;ulcerative colitis | 0 | 0 | 0 | 0 | False |      |
| DIAPH1 | NO_GO_FRESH_SCAN | 3.9 | 2 | True | True | False | False | False | False | 0.4328 | 0.03702 | 0.8507 | 2 | Crohn disease;ulcerative colitis | 0 | 0 | 0 | 0 | False |      |
| ERI1 | NO_GO_FRESH_SCAN | 3.9 | 2 | True | True | False | False | False | False | 0.589 | 0.00979 | 0.8349 | 2 | Crohn disease;psoriasis | 0 | 0 | 0 | 0 | False |      |
| IL2RG | NO_GO_FRESH_SCAN | 3.9 | 2 | True | True | False | False | False | False | 0.768 | 0.01702 | 0.8373 | 2 | Crohn disease;ulcerative colitis | 0 | 0 | 0 | 0 | False |      |
| ITGAV | NO_GO_FRESH_SCAN | 3.9 | 2 | True | True | False | False | False | False | 0.5619 | 0.01744 | 0.8373 | 2 | Crohn disease;ulcerative colitis | 0 | 0 | 0 | 0 | False |      |
| KRTCAP3 | NO_GO_FRESH_SCAN | 3.9 | 2 | True | True | False | False | False | False | 2.063 | 0.03731 | 0.8507 | 2 | type 1 diabetes mellitus;ulcerative colitis | 0 | 0 | 0 | 0 | False |      |
| LIMS1 | NO_GO_FRESH_SCAN | 3.9 | 2 | True | True | False | False | False | False | 0.5206 | 0.02049 | 0.8373 | 2 | Crohn disease;ulcerative colitis | 0 | 0 | 0 | 0 | False |      |
| PILRA | NO_GO_FRESH_SCAN | 3.9 | 2 | True | True | False | False | False | False | 0.3378 | 0.02925 | 0.8507 | 2 | Crohn disease;ulcerative colitis | 0 | 0 | 0 | 0 | False |      |
| SDC4 | NO_GO_FRESH_SCAN | 3.9 | 2 | True | True | False | False | False | False | 0.9586 | 0.02496 | 0.8472 | 2 | type 1 diabetes mellitus;ulcerative colitis | 0 | 0 | 0 | 0 | False |      |
| TRIQK | NO_GO_FRESH_SCAN | 3.9 | 2 | True | True | False | False | False | False | 0.6175 | 0.007379 | 0.8345 | 2 | Crohn disease;ulcerative colitis | 0 | 0 | 0 | 0 | False |      |

## Interpretation

`TESTABLE_FRESH_ROUTE` is not a finding. It means the candidate has enough
non-overlapping local evidence to justify a new strict forcing audit. Any top
candidate still requires target-specific biology, novelty, and translational
feasibility checks.

## Reproducibility

- Script: `scripts/v3_wave122_fresh_breadth_target_scan.py`
- Output: `results_v3/wave122_fresh_breadth_target_scan/fresh_breadth_target_rank.tsv`
- Seed: `20260527`
