# Wave74 EPHX2 Direct Ratio Audit

## Question

Can the Wave66 raw metabolomics data test soluble epoxide hydrolase
activity directly with same-study epoxide/diol product-substrate ratios?

## Verdict

NO_GO_EPHX2_DIRECT_RATIO_UNAVAILABLE

## Integrated Decision

| candidate | wave74_call | ephx2_relevant_features | direct_epoxide_diol_pairs | direct_ratio_tests | direct_ratio_supportive_tests | proxy_diol_supportive_diseases | proxy_diol_supportive_disease_count | decision_reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EPHX2_soluble_epoxide_hydrolase | NO_GO_EPHX2_DIRECT_RATIO_UNAVAILABLE | 37 | 0 | 0 | 0 | T1D;UC | 2 | raw studies contain EPHX2-relevant epoxide or diol features, but no same-study same-site epoxide/diol pair for direct sEH activity ratio |

## EPHX2-Relevant Feature Inventory

| study_id | disease_label | feature_id | analysis_id | feature_label | ephx2_role | ephx2_family | site |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ST000899 | IBD | ME229669 | AN001464 | 12,13-DiHOME | diol | linoleate_epome_dihome | 12,13 |
| ST000899 | IBD | ME229670 | AN001464 | 12-HETE | other_oxylipin |  |  |
| ST000899 | IBD | ME229671 | AN001464 | HODE | other_oxylipin |  |  |
| ST000899 | IBD | ME229760 | AN001464 | 9,10-DiHOME | diol | linoleate_epome_dihome | 9,10 |
| ST002470 | UC | ME583599 | AN004032 | 11-HETE | other_oxylipin |  |  |
| ST002470 | UC | ME583600 | AN004032 | 12,13-DiHOME | diol | linoleate_epome_dihome | 12,13 |
| ST002470 | UC | ME583682 | AN004032 | 12-HEPE | other_oxylipin |  |  |
| ST002470 | UC | ME583601 | AN004032 | 12-HETE | other_oxylipin |  |  |
| ST002470 | UC | ME583602 | AN004032 | 13-HODE | other_oxylipin |  |  |
| ST002470 | UC | ME583603 | AN004032 | 15-HETE | other_oxylipin |  |  |
| ST002470 | UC | ME583617 | AN004032 | 9,10-DiHOME | diol | linoleate_epome_dihome | 9,10 |
| ST002949 | AS | ME763801 | AN004837 | 9,10-DiHOME | diol | linoleate_epome_dihome | 9,10 |
| ST000422 | T1D | ME142562 | AN000667 | 13S-hydroxy-9E,11Z-octadecadienoic acid | other_oxylipin |  |  |
| ST000422 | T1D | ME142590 | AN000667 | 5,6-DiHETrE | diol | arachidonate_eet_dhet | 5,6 |
| ST000422 | T1D | ME142743 | AN000667 | 5,6-DiHETrE | diol | arachidonate_eet_dhet | 5,6 |
| ST000422 | T1D | ME142719 | AN000667 | 8-Methoxy-13-hydroxy-9,11-octadecadienoic acid | other_oxylipin |  | 9,11 |
| ST000422 | T1D | ME142553 | AN000667 | 9,13-DiHOME(11) | diol | linoleate_epome_dihome | 9,13 |
| ST000422 | T1D | ME144467 | AN000668 | 13S-hydroxy-9E,11Z-octadecadienoic acid | other_oxylipin |  |  |
| ST000422 | T1D | ME146649 | AN000669 | 12-oxo-14,18-dihydroxy-9Z,13E,15Z-octadecatrienoic acid | diol | other_pufa_epoxide_diol | 14,18 |
| ST000422 | T1D | ME147097 | AN000669 | 14,15-EpETrE | epoxide | arachidonate_eet_dhet | 14,15 |
| ST000422 | T1D | ME147200 | AN000669 | 14,15-EpETrE | epoxide | arachidonate_eet_dhet | 14,15 |
| ST000422 | T1D | ME147595 | AN000669 | 20-Oxoheneicosanoic acid | other_oxylipin |  |  |
| ST000422 | T1D | ME147625 | AN000669 | 20-Oxoheneicosanoic acid | other_oxylipin |  |  |
| ST000422 | T1D | ME146922 | AN000669 | 8-Hydroxy-9,11-octadecadiynoic acid | other_oxylipin |  | 9,11 |
| ST000422 | T1D | ME146970 | AN000669 | 8-Hydroxy-9,11-octadecadiynoic acid | other_oxylipin |  | 9,11 |
| ST000422 | T1D | ME147411 | AN000669 | 9,13-DiHOME(11) | diol | linoleate_epome_dihome | 9,13 |
| ST000422 | T1D | ME147269 | AN000669 | Eicosanoyl-EA | other_oxylipin |  |  |
| ST000422 | T1D | ME147179 | AN000669 | N-Ethyl N-(2-hydroxy-ethyl) arachidonoyl amine | other_oxylipin |  |  |
| ST000422 | T1D | ME147224 | AN000669 | N-Ethyl N-(2-hydroxy-ethyl) arachidonoyl amine | other_oxylipin |  |  |
| ST000422 | T1D | ME147381 | AN000669 | 11Z-Eicosaenoyl-EA | other_oxylipin |  |  |
| ST000422 | T1D | ME148480 | AN000670 | 15,16-EpODE | epoxide | other_pufa_epoxide_diol | 15,16 |
| ST000422 | T1D | ME148529 | AN000670 | 9R-HOME(12E) | other_oxylipin |  |  |
| ST000422 | T1D | ME148542 | AN000670 | 9R-HOME(12E) | other_oxylipin |  |  |
| ST000422 | T1D | ME148563 | AN000670 | 9R-HOME(12E) | other_oxylipin |  |  |
| ST000422 | T1D | ME148566 | AN000670 | 9R-HOME(12E) | other_oxylipin |  |  |
| ST000422 | T1D | ME148568 | AN000670 | 9R-HOME(12E) | other_oxylipin |  |  |
| ST000422 | T1D | ME148570 | AN000670 | 9R-HOME(12E) | other_oxylipin |  |  |

## Direct Epoxide/Diol Pair Inventory

_No rows._

## Direct Ratio Contrasts

_No rows._

## Proxy Feature Contrasts

These rows are provenance only. Diol-only or epoxide-only features do not
support a target-level EPHX2 claim.

| study_id | disease | contrast | contrast_type | feature_id | feature_label | ephx2_role | ephx2_family | site | n_case | n_control | hedges_g_case_minus_control | p | fdr_within_study_contrast |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ST000422 | T1D | T1D_vs_control | disease_control | ME146649 | 12-oxo-14,18-dihydroxy-9Z,13E,15Z-octadecatrienoic acid | diol | other_pufa_epoxide_diol | 14,18 | 70 | 67 | 0.1357 | 0.4271 | 0.6589 |
| ST000422 | T1D | T1D_vs_control | disease_control | ME142590 | 5,6-DiHETrE | diol | arachidonate_eet_dhet | 5,6 | 30 | 30 | 0.5587 | 0.03251 | 0.5006 |
| ST000422 | T1D | T1D_vs_control | disease_control | ME142743 | 5,6-DiHETrE | diol | arachidonate_eet_dhet | 5,6 | 30 | 30 | 0.3796 | 0.1417 | 0.6589 |
| ST000422 | T1D | T1D_vs_control | disease_control | ME142553 | 9,13-DiHOME(11) | diol | linoleate_epome_dihome | 9,13 | 30 | 30 | 0.09511 | 0.7103 | 0.7753 |
| ST000422 | T1D | T1D_vs_control | disease_control | ME147411 | 9,13-DiHOME(11) | diol | linoleate_epome_dihome | 9,13 | 75 | 75 | 0.114 | 0.4839 | 0.6589 |
| ST000422 | T1D | T1D_vs_control | disease_control | ME147097 | 14,15-EpETrE | epoxide | arachidonate_eet_dhet | 14,15 | 69 | 66 | 0.1485 | 0.3881 | 0.6589 |
| ST000422 | T1D | T1D_vs_control | disease_control | ME147200 | 14,15-EpETrE | epoxide | arachidonate_eet_dhet | 14,15 | 66 | 63 | 0.1595 | 0.3651 | 0.6589 |
| ST000422 | T1D | T1D_vs_control | disease_control | ME148480 | 15,16-EpODE | epoxide | other_pufa_epoxide_diol | 15,16 | 90 | 89 | 0.2195 | 0.1425 | 0.6589 |
| ST000422 | T1D | T1D_vs_control | disease_control | ME147381 | 11Z-Eicosaenoyl-EA | other_oxylipin |  |  | 71 | 66 | 0.1492 | 0.3836 | 0.6589 |
| ST000422 | T1D | T1D_vs_control | disease_control | ME142562 | 13S-hydroxy-9E,11Z-octadecadienoic acid | other_oxylipin |  |  | 30 | 30 | 0.878 | 0.001324 | 0.08039 |
| ST000422 | T1D | T1D_vs_control | disease_control | ME144467 | 13S-hydroxy-9E,11Z-octadecadienoic acid | other_oxylipin |  |  | 60 | 60 | 0.1609 | 0.3769 | 0.6589 |
| ST000422 | T1D | T1D_vs_control | disease_control | ME147595 | 20-Oxoheneicosanoic acid | other_oxylipin |  |  | 64 | 62 | 0.1644 | 0.3557 | 0.6589 |
| ST000422 | T1D | T1D_vs_control | disease_control | ME147625 | 20-Oxoheneicosanoic acid | other_oxylipin |  |  | 68 | 67 | 0.1585 | 0.3565 | 0.6589 |
| ST000422 | T1D | T1D_vs_control | disease_control | ME146922 | 8-Hydroxy-9,11-octadecadiynoic acid | other_oxylipin |  | 9,11 | 70 | 67 | 0.1395 | 0.4142 | 0.6589 |
| ST000422 | T1D | T1D_vs_control | disease_control | ME146970 | 8-Hydroxy-9,11-octadecadiynoic acid | other_oxylipin |  | 9,11 | 73 | 72 | 0.1334 | 0.4212 | 0.6589 |
| ST000422 | T1D | T1D_vs_control | disease_control | ME142719 | 8-Methoxy-13-hydroxy-9,11-octadecadienoic acid | other_oxylipin |  | 9,11 | 30 | 30 | 0.1853 | 0.47 | 0.6589 |
| ST000422 | T1D | T1D_vs_control | disease_control | ME148529 | 9R-HOME(12E) | other_oxylipin |  |  | 90 | 89 | 0.2951 | 0.04922 | 0.6011 |
| ST000422 | T1D | T1D_vs_control | disease_control | ME148542 | 9R-HOME(12E) | other_oxylipin |  |  | 90 | 89 | 0.3006 | 0.04521 | 0.5766 |
| ST000422 | T1D | T1D_vs_control | disease_control | ME148563 | 9R-HOME(12E) | other_oxylipin |  |  | 90 | 89 | 0.1326 | 0.3746 | 0.6589 |
| ST000422 | T1D | T1D_vs_control | disease_control | ME148566 | 9R-HOME(12E) | other_oxylipin |  |  | 90 | 89 | 0.1727 | 0.2479 | 0.6589 |
| ST000422 | T1D | T1D_vs_control | disease_control | ME148568 | 9R-HOME(12E) | other_oxylipin |  |  | 90 | 89 | 0.1176 | 0.4309 | 0.6589 |
| ST000422 | T1D | T1D_vs_control | disease_control | ME148570 | 9R-HOME(12E) | other_oxylipin |  |  | 90 | 89 | 0.1595 | 0.2857 | 0.6589 |
| ST000422 | T1D | T1D_vs_control | disease_control | ME147269 | Eicosanoyl-EA | other_oxylipin |  |  | 75 | 75 | 0.1182 | 0.4679 | 0.6589 |
| ST000422 | T1D | T1D_vs_control | disease_control | ME147179 | N-Ethyl N-(2-hydroxy-ethyl) arachidonoyl amine | other_oxylipin |  |  | 67 | 63 | 0.1553 | 0.3766 | 0.6589 |
| ST000422 | T1D | T1D_vs_control | disease_control | ME147224 | N-Ethyl N-(2-hydroxy-ethyl) arachidonoyl amine | other_oxylipin |  |  | 67 | 68 | 0.1405 | 0.4131 | 0.6589 |
| ST000899 | Crohn | Crohn_vs_control | disease_control | ME229669 | 12,13-DiHOME | diol | linoleate_epome_dihome | 12,13 | 20 | 20 | -0.1103 | 0.7245 | 0.84 |
| ST000899 | Crohn | Crohn_vs_control | disease_control | ME229760 | 9,10-DiHOME | diol | linoleate_epome_dihome | 9,10 | 20 | 20 | -0.1589 | 0.6128 | 0.7504 |
| ST000899 | Crohn | Crohn_vs_control | disease_control | ME229670 | 12-HETE | other_oxylipin |  |  | 20 | 20 | 0.2608 | 0.4057 | 0.5522 |
| ST000899 | Crohn | Crohn_vs_control | disease_control | ME229671 | HODE | other_oxylipin |  |  | 20 | 20 | -1.033 | 0.002382 | 0.00737 |
| ST000899 | UC | UC_vs_control | disease_control | ME229669 | 12,13-DiHOME | diol | linoleate_epome_dihome | 12,13 | 20 | 20 | 0.5593 | 0.08031 | 0.3774 |
| ST000899 | UC | UC_vs_control | disease_control | ME229760 | 9,10-DiHOME | diol | linoleate_epome_dihome | 9,10 | 20 | 20 | 0.7298 | 0.02483 | 0.2674 |
| ST000899 | UC | UC_vs_control | disease_control | ME229670 | 12-HETE | other_oxylipin |  |  | 20 | 20 | 0.3686 | 0.2424 | 0.5735 |
| ST000899 | UC | UC_vs_control | disease_control | ME229671 | HODE | other_oxylipin |  |  | 20 | 20 | 0.3367 | 0.2852 | 0.6115 |
| ST002470 | UC | UC_week0_modsev_vs_mild | severity | ME583600 | 12,13-DiHOME | diol | linoleate_epome_dihome | 12,13 | 22 | 10 | -0.2223 | 0.5566 | 0.7703 |
| ST002470 | UC | UC_week0_modsev_vs_mild | severity | ME583617 | 9,10-DiHOME | diol | linoleate_epome_dihome | 9,10 | 22 | 10 | -0.2174 | 0.5792 | 0.7808 |
| ST002470 | UC | UC_week0_modsev_vs_mild | severity | ME583599 | 11-HETE | other_oxylipin |  |  | 18 | 9 | -0.1938 | 0.6363 | 0.8228 |
| ST002470 | UC | UC_week0_modsev_vs_mild | severity | ME583682 | 12-HEPE | other_oxylipin |  |  | 15 | 8 | 0.3505 | 0.4137 | 0.6671 |
| ST002470 | UC | UC_week0_modsev_vs_mild | severity | ME583601 | 12-HETE | other_oxylipin |  |  | 22 | 10 | 0.1864 | 0.648 | 0.8289 |
| ST002470 | UC | UC_week0_modsev_vs_mild | severity | ME583602 | 13-HODE | other_oxylipin |  |  | 22 | 10 | -0.5945 | 0.1781 | 0.4581 |
| ST002470 | UC | UC_week0_modsev_vs_mild | severity | ME583603 | 15-HETE | other_oxylipin |  |  | 22 | 10 | 0.193 | 0.6142 | 0.8013 |
| ST002470 | UC | UC_week12_inactive_vs_week0_modsev | treatment_or_improvement_shift | ME583600 | 12,13-DiHOME | diol | linoleate_epome_dihome | 12,13 | 18 | 22 | -0.2687 | 0.3636 | 0.4958 |
| ST002470 | UC | UC_week12_inactive_vs_week0_modsev | treatment_or_improvement_shift | ME583617 | 9,10-DiHOME | diol | linoleate_epome_dihome | 9,10 | 18 | 22 | -0.6217 | 0.04166 | 0.09306 |
| ST002470 | UC | UC_week12_inactive_vs_week0_modsev | treatment_or_improvement_shift | ME583599 | 11-HETE | other_oxylipin |  |  | 16 | 18 | -0.3511 | 0.3004 | 0.4436 |
| ST002470 | UC | UC_week12_inactive_vs_week0_modsev | treatment_or_improvement_shift | ME583682 | 12-HEPE | other_oxylipin |  |  | 6 | 15 | -0.271 | 0.5405 | 0.668 |
| ST002470 | UC | UC_week12_inactive_vs_week0_modsev | treatment_or_improvement_shift | ME583601 | 12-HETE | other_oxylipin |  |  | 18 | 22 | -0.529 | 0.09488 | 0.1776 |
| ST002470 | UC | UC_week12_inactive_vs_week0_modsev | treatment_or_improvement_shift | ME583602 | 13-HODE | other_oxylipin |  |  | 18 | 22 | -0.2222 | 0.486 | 0.6132 |
| ST002470 | UC | UC_week12_inactive_vs_week0_modsev | treatment_or_improvement_shift | ME583603 | 15-HETE | other_oxylipin |  |  | 18 | 22 | -0.7958 | 0.0113 | 0.03252 |
| ST002949 | AS | AS_vs_control | disease_control | ME763801 | 9,10-DiHOME | diol | linoleate_epome_dihome | 9,10 | 119 | 109 | 0.195 | 0.1449 | 0.1449 |

## Interpretation Guardrail

A direct EPHX2 activity claim requires matched epoxide substrate and diol
product features in the same study, ideally the same chromatographic
analysis, with sample-level ratios. Product-only DiHOME or DHET features
are treated as weak biochemical proxies and cannot promote the branch.
