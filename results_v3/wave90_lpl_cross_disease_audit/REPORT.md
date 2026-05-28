# Wave90 LPL Cross-Disease Audit

Analysis call: `PARK_LPL_RESPONSE_MARKER_WITH_CASE_CONTROL_CONFLICT`.

## Response Direction Summary

| disease | dataset | response_context | direction | effect | p_or_min_p | call | nonresponse_high |
| --- | --- | --- | --- | --- | --- | --- | --- |
| IBD | GSE12251/GSE14580/GSE16879 | intestinal mucosa anti-TNF | nonresponse_high | -0.2045 | 0.2508 | IBD_RESPONSE_WEAK_DIRECTION | True |
| rheumatoid arthritis | GSE198520 | synovium anti-TNF | nonresponse_high | -0.3946 | 0.1578 | DIRECTION_ONLY | True |
| psoriasis | GSE85034 | lesional skin adalimumab | nonresponse_high | -2.209 | 0.01111 | NONRESPONSE_HIGH_TREND | True |

## MS Bulk Evidence

| evidence_channel | dataset | disease | tissue | gene | delta_case_minus_control | hedges_g_case_minus_control | p | fdr | call |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MS_GSE111972_bulk_wm_signature | GSE111972 | multiple sclerosis | white matter | LPL | 1.76 | 1.873 | 0.000622 | 0.7144 | MS_WM_UP |
| MS_GSE111972_lipid_loader_module | GSE111972 | multiple sclerosis | white matter | LPL_module_context | 0.4784 | 1.379 | 0.005282 | 0.01916 | MS_WM_MODULE_UP |

## Direct Single-Cell Case-Control LPL Rows

| disease | tissue | n_case_donors | n_control_donors | delta_case_minus_control | hedges_g_case_minus_control | p | fdr_lpl_across_direct_contexts | call |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Crohn disease | colon epithelial | 6 | 6 | 0.5798 | 1.719 | 0.02314 | 0.1389 | CASE_HIGH_NOMINAL_OR_TREND |
| Crohn disease | colon myeloid | 6 | 6 | 0.007413 | 0.5329 | 0.3632 | 0.7264 | NO_NOMINAL_CASE_CONTROL_SIGNAL |
| Sjogren syndrome | salivary gland APC | 9 | 13 | -0.02416 | -0.0669 | 0.8847 | 0.9368 | NO_NOMINAL_CASE_CONTROL_SIGNAL |
| Sjogren syndrome | salivary gland epithelial | 11 | 14 | 0.04752 | 0.3809 | 0.3445 | 0.7264 | NO_NOMINAL_CASE_CONTROL_SIGNAL |
| psoriasis | skin APC | 3 | 3 | -0.1232 | -3.704 | 0.01578 | 0.1389 | CONTROL_HIGH_NOMINAL_OR_TREND |
| psoriasis | skin keratinocyte | 3 | 3 | 0.003945 | 0.05679 | 0.9368 | 0.9368 | NO_NOMINAL_CASE_CONTROL_SIGNAL |
| rheumatoid arthritis | blood myeloid/APC | 18 | 18 | 0.0122 | 0.252 | 0.4463 | 0.7382 | NO_NOMINAL_CASE_CONTROL_SIGNAL |
| type 1 diabetes mellitus | pancreatic acinar cell | 5 | 18 | -0.01402 | -0.1418 | 0.6151 | 0.7382 | NO_NOMINAL_CASE_CONTROL_SIGNAL |
| type 1 diabetes mellitus | pancreatic beta cell | 3 | 19 | 0.1023 | 0.984 | 0.5158 | 0.7382 | NO_NOMINAL_CASE_CONTROL_SIGNAL |
| type 1 diabetes mellitus | pancreatic ductal cell | 5 | 19 | -0.024 | -0.1463 | 0.5909 | 0.7382 | NO_NOMINAL_CASE_CONTROL_SIGNAL |
| ulcerative colitis | colon epithelial | 6 | 6 | 0.4579 | 0.6829 | 0.2562 | 0.7264 | NO_NOMINAL_CASE_CONTROL_SIGNAL |
| ulcerative colitis | colon myeloid | 6 | 6 | 0.005779 | 1.007 | 0.1173 | 0.4693 | NO_NOMINAL_CASE_CONTROL_SIGNAL |

## Interpretation

- LPL is MS white-matter lesion-up and sits in the lipid-loader module.
- LPL response direction is not stable enough to promote as the cross-disease intervention node.
- Psoriasis adalimumab nonresponse-high LPL conflicts with psoriasis APC case-control LPL being lower in cases than controls in the direct h5ad donor comparison.
- LPL remains useful as a lipid-load/state marker and a clue toward lipid handling, but direct systemic LPL modulation is not a plausible autoimmune therapeutic route without a more selective tissue/cell-state handle.
