# Wave76 Adjusted Response-Specificity Stress Test

## Question

Does the Wave75 IFN/APC plus lysosomal/APC response-stratification signal
survive patient-level adjustment and target/generic specificity gates?

## Verdict

PARK_RESPONSE_SIGNAL_GENERIC_LIMITED

## Integrated Decision

| candidate | wave76_call | decision_reason | best_module | best_endpoint | ra_coef | ra_p | ra_target_generic_abs_ratio | ibd_coef | ibd_p | ibd_target_generic_abs_ratio | sign_stable | both_adjusted_p10 | both_ratio_ge2 | passes_wave76_specificity |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IFN_APC_lysosomal_APC_response_stratification | PARK_RESPONSE_SIGNAL_GENERIC_LIMITED | adjusted response signal replicates but does not beat generic inflammation by ratio >=2 in both datasets | lysosomal_apc__resid_inflammatory_nfkb | baseline_pre | 0.2887 | 0.07461 | 3.715 | 0.2604 | 0.03686 | 1.696 | True | True | False | False |

## Cross-Dataset Adjusted Convergence

| module | endpoint | ra_comparison | ra_n | ra_coef | ra_p | ra_fdr | ra_generic_coef | ra_target_generic_abs_ratio | ibd_cell_state | ibd_n | ibd_coef | ibd_p | ibd_fdr | ibd_generic_coef | ibd_target_generic_abs_ratio | sign_stable | both_adjusted_p10 | both_ratio_ge2 | passes_wave76_specificity | priority |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| lysosomal_apc__resid_inflammatory_nfkb | baseline_pre | good_vs_moderate_none | 42 | 0.2887 | 0.07461 | 0.3954 | 0.07772 | 3.715 | DC | 29 | 0.2604 | 0.03686 | 0.5048 | 0.1535 | 1.696 | True | True | False | False | 3 |
| lysosomal_apc | baseline_pre | good_vs_moderate_none | 42 | 0.2887 | 0.07461 | 0.3954 | 0.07772 | 3.715 | DC | 29 | 0.2604 | 0.03686 | 0.5048 | 0.1535 | 1.696 | True | True | False | False | 3 |
| ifn_lysosomal_apc_composite__resid_inflammatory_nfkb | baseline_pre | good_vs_moderate_none | 42 | 0.2565 | 0.1139 | 0.3954 | 0.07772 | 3.3 | DC | 29 | 0.1959 | 0.1082 | 0.5048 | 0.1535 | 1.276 | True | False | False | False | 1 |
| ifn_lysosomal_apc_composite | baseline_pre | good_vs_moderate_none | 42 | 0.2565 | 0.1139 | 0.3954 | 0.07772 | 3.3 | DC | 29 | 0.1959 | 0.1082 | 0.5048 | 0.1535 | 1.276 | True | False | False | False | 1 |
| ifn_apc__resid_inflammatory_nfkb | baseline_pre | good_vs_moderate_none | 42 | 0.2242 | 0.2349 | 0.4698 | 0.07772 | 2.885 | DC | 29 | 0.1315 | 0.4457 | 0.6934 | 0.1535 | 0.8562 | True | False | False | False | 1 |
| ifn_apc | baseline_pre | good_vs_moderate_none | 42 | 0.2242 | 0.2349 | 0.4698 | 0.07772 | 2.885 | DC | 29 | 0.1315 | 0.4457 | 0.6934 | 0.1535 | 0.8562 | True | False | False | False | 1 |
| lysosomal_apc__resid_inflammatory_nfkb | delta_post_minus_pre | good_vs_moderate_none | 42 | 0.3259 | 0.1264 | 0.3954 | -0.2766 | 1.178 | DC | 29 | -0.2035 | 0.08691 | 0.5048 | -0.01959 | 10.39 | False | False | False | False | 0 |
| lysosomal_apc | delta_post_minus_pre | good_vs_moderate_none | 42 | 0.3259 | 0.1264 | 0.3954 | -0.2766 | 1.178 | DC | 29 | -0.2035 | 0.08691 | 0.5048 | -0.01959 | 10.39 | False | False | False | False | 0 |
| ifn_lysosomal_apc_composite__resid_inflammatory_nfkb | delta_post_minus_pre | good_vs_moderate_none | 42 | 0.3031 | 0.1412 | 0.3954 | -0.2766 | 1.096 | DC | 29 | -0.1284 | 0.2898 | 0.6002 | -0.01959 | 6.556 | False | False | False | False | 0 |
| ifn_lysosomal_apc_composite | delta_post_minus_pre | good_vs_moderate_none | 42 | 0.3031 | 0.1412 | 0.3954 | -0.2766 | 1.096 | DC | 29 | -0.1284 | 0.2898 | 0.6002 | -0.01959 | 6.556 | False | False | False | False | 0 |
| ifn_apc__resid_inflammatory_nfkb | delta_post_minus_pre | good_vs_moderate_none | 42 | 0.2718 | 0.1932 | 0.4509 | -0.2766 | 0.9826 | DC | 29 | -0.03783 | 0.8075 | 0.9044 | -0.01959 | 1.932 | False | False | False | False | 0 |
| ifn_apc | delta_post_minus_pre | good_vs_moderate_none | 42 | 0.2718 | 0.1932 | 0.4509 | -0.2766 | 0.9826 | DC | 29 | -0.03783 | 0.8075 | 0.9044 | -0.01959 | 1.932 | False | False | False | False | 0 |

## Adjusted Model Rows

| dataset | cell_state | endpoint | comparison | module | n | response_coef | response_p | response_fdr | generic_response_coef | target_generic_abs_ratio | model_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | delta_post_minus_pre | good_vs_moderate_none | inflammatory_nfkb | 42 | -0.2766 | 0.03572 | 0.3954 | -0.2766 | 1 | ok |
| GSE282122_IBD_myeloid_antiTNF | DC | baseline_pre | remission_vs_nonremission | lysosomal_apc__resid_inflammatory_nfkb | 29 | 0.2604 | 0.03686 | 0.5048 | 0.1535 | 1.696 | ok |
| GSE282122_IBD_myeloid_antiTNF | DC | baseline_pre | remission_vs_nonremission | lysosomal_apc | 29 | 0.2604 | 0.03686 | 0.5048 | 0.1535 | 1.696 | ok |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | baseline_pre | moderate_good_vs_none | inflammatory_nfkb | 42 | 0.2088 | 0.06817 | 0.3954 | 0.2088 | 1 | ok |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | baseline_pre | good_vs_moderate_none | lysosomal_apc__resid_inflammatory_nfkb | 42 | 0.2887 | 0.07461 | 0.3954 | 0.07772 | 3.715 | ok |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | baseline_pre | good_vs_moderate_none | lysosomal_apc | 42 | 0.2887 | 0.07461 | 0.3954 | 0.07772 | 3.715 | ok |
| GSE282122_IBD_myeloid_antiTNF | DC | delta_post_minus_pre | remission_vs_nonremission | lysosomal_apc | 29 | -0.2035 | 0.08691 | 0.5048 | -0.01959 | 10.39 | ok |
| GSE282122_IBD_myeloid_antiTNF | DC | delta_post_minus_pre | remission_vs_nonremission | lysosomal_apc__resid_inflammatory_nfkb | 29 | -0.2035 | 0.08691 | 0.5048 | -0.01959 | 10.39 | ok |
| GSE282122_IBD_myeloid_antiTNF | DC | baseline_pre | remission_vs_nonremission | ifn_lysosomal_apc_composite__resid_inflammatory_nfkb | 29 | 0.1959 | 0.1082 | 0.5048 | 0.1535 | 1.276 | ok |
| GSE282122_IBD_myeloid_antiTNF | DC | baseline_pre | remission_vs_nonremission | ifn_lysosomal_apc_composite | 29 | 0.1959 | 0.1082 | 0.5048 | 0.1535 | 1.276 | ok |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | baseline_pre | good_vs_moderate_none | ifn_lysosomal_apc_composite__resid_inflammatory_nfkb | 42 | 0.2565 | 0.1139 | 0.3954 | 0.07772 | 3.3 | ok |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | baseline_pre | good_vs_moderate_none | ifn_lysosomal_apc_composite | 42 | 0.2565 | 0.1139 | 0.3954 | 0.07772 | 3.3 | ok |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | delta_post_minus_pre | good_vs_moderate_none | lysosomal_apc__resid_inflammatory_nfkb | 42 | 0.3259 | 0.1264 | 0.3954 | -0.2766 | 1.178 | ok |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | delta_post_minus_pre | good_vs_moderate_none | lysosomal_apc | 42 | 0.3259 | 0.1264 | 0.3954 | -0.2766 | 1.178 | ok |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | delta_post_minus_pre | good_vs_moderate_none | ifn_lysosomal_apc_composite__resid_inflammatory_nfkb | 42 | 0.3031 | 0.1412 | 0.3954 | -0.2766 | 1.096 | ok |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | delta_post_minus_pre | good_vs_moderate_none | ifn_lysosomal_apc_composite | 42 | 0.3031 | 0.1412 | 0.3954 | -0.2766 | 1.096 | ok |
| GSE282122_IBD_myeloid_antiTNF | Mono_macro | delta_post_minus_pre | remission_vs_nonremission | inflammatory_nfkb | 29 | -0.3389 | 0.1668 | 0.6002 | -0.3389 | 1 | ok |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | delta_post_minus_pre | good_vs_moderate_none | ifn_apc__resid_inflammatory_nfkb | 42 | 0.2718 | 0.1932 | 0.4509 | -0.2766 | 0.9826 | ok |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | delta_post_minus_pre | good_vs_moderate_none | ifn_apc | 42 | 0.2718 | 0.1932 | 0.4509 | -0.2766 | 0.9826 | ok |
| GSE282122_IBD_myeloid_antiTNF | Mono_macro | delta_post_minus_pre | remission_vs_nonremission | lysosomal_apc | 29 | -0.1396 | 0.2055 | 0.6002 | -0.3389 | 0.4119 | ok |
| GSE282122_IBD_myeloid_antiTNF | Mono_macro | delta_post_minus_pre | remission_vs_nonremission | lysosomal_apc__resid_inflammatory_nfkb | 29 | -0.1396 | 0.2055 | 0.6002 | -0.3389 | 0.4119 | ok |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | baseline_pre | good_vs_moderate_none | ifn_apc__resid_inflammatory_nfkb | 42 | 0.2242 | 0.2349 | 0.4698 | 0.07772 | 2.885 | ok |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | baseline_pre | good_vs_moderate_none | ifn_apc | 42 | 0.2242 | 0.2349 | 0.4698 | 0.07772 | 2.885 | ok |
| GSE282122_IBD_myeloid_antiTNF | Mono_macro | baseline_pre | remission_vs_nonremission | lysosomal_apc__resid_inflammatory_nfkb | 29 | 0.1571 | 0.2854 | 0.6002 | -0.112 | 1.403 | ok |
| GSE282122_IBD_myeloid_antiTNF | Mono_macro | baseline_pre | remission_vs_nonremission | lysosomal_apc | 29 | 0.1571 | 0.2854 | 0.6002 | -0.112 | 1.403 | ok |
| GSE282122_IBD_myeloid_antiTNF | DC | delta_post_minus_pre | remission_vs_nonremission | ifn_lysosomal_apc_composite | 29 | -0.1284 | 0.2898 | 0.6002 | -0.01959 | 6.556 | ok |
| GSE282122_IBD_myeloid_antiTNF | DC | delta_post_minus_pre | remission_vs_nonremission | ifn_lysosomal_apc_composite__resid_inflammatory_nfkb | 29 | -0.1284 | 0.2898 | 0.6002 | -0.01959 | 6.556 | ok |
| GSE282122_IBD_myeloid_antiTNF | Mono_macro | baseline_pre | remission_vs_nonremission | ifn_apc | 29 | -0.1555 | 0.3215 | 0.6002 | -0.112 | 1.389 | ok |
| GSE282122_IBD_myeloid_antiTNF | Mono_macro | baseline_pre | remission_vs_nonremission | ifn_apc__resid_inflammatory_nfkb | 29 | -0.1555 | 0.3215 | 0.6002 | -0.112 | 1.389 | ok |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | baseline_pre | moderate_good_vs_none | lysosomal_apc | 42 | 0.1586 | 0.3526 | 0.5878 | 0.2088 | 0.7595 | ok |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | baseline_pre | moderate_good_vs_none | lysosomal_apc__resid_inflammatory_nfkb | 42 | 0.1586 | 0.3526 | 0.5878 | 0.2088 | 0.7595 | ok |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | delta_post_minus_pre | moderate_good_vs_none | ifn_apc__resid_inflammatory_nfkb | 42 | 0.1661 | 0.4149 | 0.5878 | -0.07902 | 2.102 | ok |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | delta_post_minus_pre | moderate_good_vs_none | ifn_apc | 42 | 0.1661 | 0.4149 | 0.5878 | -0.07902 | 2.102 | ok |
| GSE282122_IBD_myeloid_antiTNF | DC | baseline_pre | remission_vs_nonremission | inflammatory_nfkb | 29 | 0.1535 | 0.4257 | 0.6934 | 0.1535 | 1 | ok |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | baseline_pre | moderate_good_vs_none | ifn_lysosomal_apc_composite__resid_inflammatory_nfkb | 42 | 0.1335 | 0.4332 | 0.5878 | 0.2088 | 0.6395 | ok |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | baseline_pre | moderate_good_vs_none | ifn_lysosomal_apc_composite | 42 | 0.1335 | 0.4332 | 0.5878 | 0.2088 | 0.6395 | ok |
| GSE282122_IBD_myeloid_antiTNF | DC | baseline_pre | remission_vs_nonremission | ifn_apc__resid_inflammatory_nfkb | 29 | 0.1315 | 0.4457 | 0.6934 | 0.1535 | 0.8562 | ok |
| GSE282122_IBD_myeloid_antiTNF | DC | baseline_pre | remission_vs_nonremission | ifn_apc | 29 | 0.1315 | 0.4457 | 0.6934 | 0.1535 | 0.8562 | ok |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | delta_post_minus_pre | moderate_good_vs_none | ifn_lysosomal_apc_composite__resid_inflammatory_nfkb | 42 | 0.1432 | 0.4759 | 0.5878 | -0.07902 | 1.812 | ok |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | delta_post_minus_pre | moderate_good_vs_none | ifn_lysosomal_apc_composite | 42 | 0.1432 | 0.4759 | 0.5878 | -0.07902 | 1.812 | ok |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | baseline_pre | good_vs_moderate_none | inflammatory_nfkb | 42 | 0.07772 | 0.509 | 0.5878 | 0.07772 | 1 | ok |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | delta_post_minus_pre | moderate_good_vs_none | inflammatory_nfkb | 42 | -0.07902 | 0.574 | 0.5878 | -0.07902 | 1 | ok |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | baseline_pre | moderate_good_vs_none | ifn_apc__resid_inflammatory_nfkb | 42 | 0.1085 | 0.582 | 0.5878 | 0.2088 | 0.5195 | ok |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | baseline_pre | moderate_good_vs_none | ifn_apc | 42 | 0.1085 | 0.582 | 0.5878 | 0.2088 | 0.5195 | ok |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | delta_post_minus_pre | moderate_good_vs_none | lysosomal_apc | 42 | 0.1126 | 0.5878 | 0.5878 | -0.07902 | 1.426 | ok |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | delta_post_minus_pre | moderate_good_vs_none | lysosomal_apc__resid_inflammatory_nfkb | 42 | 0.1126 | 0.5878 | 0.5878 | -0.07902 | 1.426 | ok |
| GSE282122_IBD_myeloid_antiTNF | Mono_macro | baseline_pre | remission_vs_nonremission | inflammatory_nfkb | 29 | -0.112 | 0.6641 | 0.8919 | -0.112 | 1 | ok |
| GSE282122_IBD_myeloid_antiTNF | Mono_macro | delta_post_minus_pre | remission_vs_nonremission | ifn_apc__resid_inflammatory_nfkb | 29 | 0.06793 | 0.683 | 0.8919 | -0.3389 | 0.2005 | ok |
| GSE282122_IBD_myeloid_antiTNF | Mono_macro | delta_post_minus_pre | remission_vs_nonremission | ifn_apc | 29 | 0.06793 | 0.683 | 0.8919 | -0.3389 | 0.2005 | ok |
| GSE282122_IBD_myeloid_antiTNF | Mono_macro | delta_post_minus_pre | remission_vs_nonremission | ifn_lysosomal_apc_composite | 29 | -0.03999 | 0.7326 | 0.8919 | -0.3389 | 0.118 | ok |
| GSE282122_IBD_myeloid_antiTNF | Mono_macro | delta_post_minus_pre | remission_vs_nonremission | ifn_lysosomal_apc_composite__resid_inflammatory_nfkb | 29 | -0.03999 | 0.7326 | 0.8919 | -0.3389 | 0.118 | ok |
| GSE282122_IBD_myeloid_antiTNF | DC | delta_post_minus_pre | remission_vs_nonremission | ifn_apc | 29 | -0.03783 | 0.8075 | 0.9044 | -0.01959 | 1.932 | ok |
| GSE282122_IBD_myeloid_antiTNF | DC | delta_post_minus_pre | remission_vs_nonremission | ifn_apc__resid_inflammatory_nfkb | 29 | -0.03783 | 0.8075 | 0.9044 | -0.01959 | 1.932 | ok |
| GSE282122_IBD_myeloid_antiTNF | DC | delta_post_minus_pre | remission_vs_nonremission | inflammatory_nfkb | 29 | -0.01959 | 0.8994 | 0.9686 | -0.01959 | 1 | ok |
| GSE282122_IBD_myeloid_antiTNF | Mono_macro | baseline_pre | remission_vs_nonremission | ifn_lysosomal_apc_composite__resid_inflammatory_nfkb | 29 | 0.0007994 | 0.9951 | 0.9951 | -0.112 | 0.00714 | ok |
| GSE282122_IBD_myeloid_antiTNF | Mono_macro | baseline_pre | remission_vs_nonremission | ifn_lysosomal_apc_composite | 29 | 0.0007994 | 0.9951 | 0.9951 | -0.112 | 0.00714 | ok |

## Frozen Gate

- RA baseline models adjust for generic inflammatory NF-kB score, pathotype,
  biologic, baseline tissue inflammatory score, and baseline DAS28.
- RA delta models also adjust for baseline target module and delta generic
  inflammatory NF-kB score.
- IBD baseline models adjust for generic inflammatory NF-kB score, disease
  label, and baseline inflammation score within cell state.
- IBD delta models also adjust for baseline target module and delta generic
  inflammatory NF-kB score.
- A survivor requires same sign, adjusted p <= 0.10 in RA and IBD DC, and
  target/generic absolute response-coefficient ratio >= 2 in both datasets.
