# V36 Therapy-Branch Evidence Map

This table consolidates held V22/V36 evidence by therapy context. It does
not change locked rules; it clarifies which secondary branch should be
reported for each therapy class in future validation.

## Branch Summary

| therapy | branch | n_rows | max_auc | min_p |
| --- | --- | --- | --- | --- |
| adalimumab | locked scalar | 1 | 0.5111 | 0.9439 |
| dimethyl_fumarate | locked scalar | 1 | 0.72 | 0.2979 |
| fingolimod | locked scalar | 1 | 0.6 | 0.7993 |
| interferon-beta | CD74/receptor-state dynamics | 3 | 0.7222 | 0.00735 |
| interferon-beta | HLA-II competence/induction | 4 | 0.75 | 0.00025 |
| interferon-beta | IFN/APC/STAT1 dynamics | 1 | 0.7153 | 0.04206 |
| methotrexate | CD74/receptor-state dynamics | 1 | 0.9 | 0.02448 |
| methotrexate | IFN/APC/STAT1 dynamics | 1 | 0.6 | 0.3462 |
| tofacitinib | locked scalar | 1 | 1 | 0.03393 |

## Evidence Rows

| source_table | cohort | disease | therapy | context | candidate_feature | branch | auc | p_value | effect | status | caveat |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| validation_ledger_v22_ms_dmt | GSE235357 | MS | dimethyl_fumarate | locked V22/V23 MS DMT validation | delta_HLAII - delta_IFN_APC | locked scalar | 0.72 | 0.2979 | 0.6512 | pass | small held cohort; primary rule pre-specified |
| validation_ledger_v22_ms_dmt | GSE250453 | MS | fingolimod | locked V22/V23 MS DMT validation | delta_HLAII - delta_IFN_APC | locked scalar | 0.6 | 0.7993 | 0.1502 | fail | small held cohort; primary rule pre-specified |
| validation_ledger_v22_cross_disease | GSE85034_ADA | psoriasis | adalimumab | locked V22 cross-disease stress | -delta_IFN_APC | locked scalar | 0.5111 | 0.9439 | 0.04421 | fail | cross-disease; tofacitinib exact all-cell approximation caveated |
| validation_ledger_v22_cross_disease | GSE253006_TOF | ulcerative_colitis | tofacitinib | locked V22 cross-disease stress | -delta_IFN_APC | locked scalar | 1 | 0.03393 | 1.522 | pass | cross-disease; tofacitinib exact all-cell approximation caveated |
| gse85034_mtx_feature_tests | GSE85034_MTX | psoriasis | methotrexate | out-of-domain skin stress test | negative_delta_RECEPTOR | CD74/receptor-state dynamics | 0.9 | 0.02448 | 1.092 | post_hoc_stress_only | not bounded validation domain; 3 responders |
| gse85034_mtx_feature_tests | GSE85034_MTX | psoriasis | methotrexate | out-of-domain skin stress test | locked_signed_score | IFN/APC/STAT1 dynamics | 0.6 | 0.3462 | 0.1654 | post_hoc_stress_only | not bounded validation domain; 3 responders |
| gse24427_ifnb_timepoint_tests | GSE24427_month_1 | MS | interferon-beta | longitudinal relapse-free timing audit | delta__hla_ii_without_cd74 | HLA-II competence/induction | 0.75 | 0.02008 | 1.009 | exploratory_context | older IFN-beta cohort; therapy-specific branch only |
| gse24427_ifnb_timepoint_tests | GSE24427_month_1 | MS | interferon-beta | longitudinal relapse-free timing audit | delta__cd74_alone | CD74/receptor-state dynamics | 0.7222 | 0.03696 | 0.9276 | exploratory_context | older IFN-beta cohort; therapy-specific branch only |
| gse24427_ifnb_timepoint_tests | GSE24427_second_injection | MS | interferon-beta | longitudinal relapse-free timing audit | delta__ifn_apc | IFN/APC/STAT1 dynamics | 0.7153 | 0.04206 | 0.3362 | exploratory_context | older IFN-beta cohort; therapy-specific branch only |
| gse138064_ifnb_dose_hour_tests | GSE138064_stable_hour_4 | MS | interferon-beta | dose/hour complete-vs-partial responder audit | delta__receptor_only_cd74_cd44_cxcr4 | CD74/receptor-state dynamics | 0.6935 | 0.00735 | 0.6084 | exploratory_context | complete-vs-partial labels; repeated dose/hour rows |
| gse138064_ifnb_dose_hour_tests | GSE138064_stable_8MU | MS | interferon-beta | dose/hour complete-vs-partial responder audit | delta__receptor_only_cd74_cd44_cxcr4 | CD74/receptor-state dynamics | 0.6875 | 0.01075 | 0.6556 | exploratory_context | complete-vs-partial labels; repeated dose/hour rows |
| gse138064_ifnb_dose_hour_tests | GSE138064_all | MS | interferon-beta | dose/hour complete-vs-partial responder audit | baseline__hla_ii_without_cd74 | HLA-II competence/induction | 0.6853 | 0.00025 | 0.6992 | exploratory_context | complete-vs-partial labels; repeated dose/hour rows |
| gse138064_ifnb_dose_hour_tests | GSE138064_stable_8MU | MS | interferon-beta | dose/hour complete-vs-partial responder audit | baseline__hla_ii_without_cd74 | HLA-II competence/induction | 0.6845 | 0.0107 | 0.8198 | exploratory_context | complete-vs-partial labels; repeated dose/hour rows |
| gse138064_ifnb_dose_hour_tests | GSE138064_stable_hour_4 | MS | interferon-beta | dose/hour complete-vs-partial responder audit | baseline__hla_ii_without_cd74 | HLA-II competence/induction | 0.6592 | 0.02475 | 0.6436 | exploratory_context | complete-vs-partial labels; repeated dose/hour rows |

## Interpretation

IFN-beta held artifacts repeatedly emphasize HLA-II competence and CD74/receptor dynamics, whereas tofacitinib emphasizes IFN/APC/STAT1 downshift; MTX/ADA psoriasis skin are out-of-domain and do not support a universal scalar.
