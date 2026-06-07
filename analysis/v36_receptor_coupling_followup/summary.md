# V36 Receptor/Coupling Follow-Up

The MTX stress test produced a high post-hoc `negative_delta_RECEPTOR`
metric. This script checks recurrence in already-held ADA and TOF paired
score artifacts. It is explicitly exploratory and cannot alter the locked
V22 rule.

| cohort | source | feature | n | n_responders | n_nonresponders | auc_high_score_response | exact_auc_p | hedges_g_responder_minus_non | welch_p |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GSE85034_MTX | hypothesis_source | delta_RECEPTOR | 13 | 3 | 10 | 0.1 | 0.986 | -1.092 | 0.008399 |
| GSE253006_TOF_all_cell_approx | recurrence_check | delta_RECEPTOR | 9 | 5 | 4 | 0.8 | 0.09524 | 1.121 | 0.0935 |
| GSE253006_TOF_exact_b_plasma_like | recurrence_check | delta_RECEPTOR | 9 | 5 | 4 | 0.75 | 0.1429 | 0.9824 | 0.1505 |
| GSE253006_TOF_exact_epithelial_like | recurrence_check | delta_RECEPTOR | 9 | 5 | 4 | 1 | 0.007937 | 1.555 | 0.03011 |
| GSE253006_TOF_exact_myeloid_apc_like | recurrence_check | delta_RECEPTOR | 9 | 5 | 4 | 0.75 | 0.1429 | 0.812 | 0.274 |
| GSE253006_TOF_exact_stromal_endothelial_like | recurrence_check | delta_RECEPTOR | 9 | 5 | 4 | 0.95 | 0.01587 | 1.681 | 0.026 |
| GSE253006_TOF_exact_t_cell_like | recurrence_check | delta_RECEPTOR | 9 | 5 | 4 | 0.6 | 0.3651 | 0.1944 | 0.7617 |
| GSE85034_ADA | recurrence_check | delta_RECEPTOR | 14 | 9 | 5 | 0.5556 | 0.3986 | 0.07194 | 0.894 |
| GSE85034_MTX | hypothesis_source | locked_signed_score | 13 | 3 | 10 | 0.6 | 0.3462 | 0.1654 | 0.7634 |
| GSE253006_TOF_all_cell_approx | recurrence_check | locked_signed_score | 9 | 5 | 4 | 1 | 0.007937 | 1.522 | 0.03393 |
| GSE253006_TOF_exact_b_plasma_like | recurrence_check | locked_signed_score | 9 | 5 | 4 | 0.95 | 0.01587 | 1.487 | 0.05323 |
| GSE253006_TOF_exact_epithelial_like | recurrence_check | locked_signed_score | 9 | 5 | 4 | 0.9 | 0.03175 | 1.42 | 0.06192 |
| GSE253006_TOF_exact_myeloid_apc_like | recurrence_check | locked_signed_score | 9 | 5 | 4 | 0.8 | 0.09524 | 1.228 | 0.09421 |
| GSE253006_TOF_exact_stromal_endothelial_like | recurrence_check | locked_signed_score | 9 | 5 | 4 | 0.75 | 0.1429 | 0.9458 | 0.1727 |
| GSE253006_TOF_exact_t_cell_like | recurrence_check | locked_signed_score | 9 | 5 | 4 | 1 | 0.007937 | 1.27 | 0.06502 |
| GSE85034_ADA | recurrence_check | locked_signed_score | 14 | 9 | 5 | 0.5111 | 0.5 | 0.04421 | 0.9439 |
| GSE85034_MTX | hypothesis_source | negative_delta_RECEPTOR | 13 | 3 | 10 | 0.9 | 0.02448 | 1.092 | 0.008399 |
| GSE253006_TOF_all_cell_approx | recurrence_check | negative_delta_RECEPTOR | 9 | 5 | 4 | 0.2 | 0.9444 | -1.121 | 0.0935 |
| GSE253006_TOF_exact_b_plasma_like | recurrence_check | negative_delta_RECEPTOR | 9 | 5 | 4 | 0.25 | 0.9048 | -0.9824 | 0.1505 |
| GSE253006_TOF_exact_epithelial_like | recurrence_check | negative_delta_RECEPTOR | 9 | 5 | 4 | 0 | 1 | -1.555 | 0.03011 |
| GSE253006_TOF_exact_myeloid_apc_like | recurrence_check | negative_delta_RECEPTOR | 9 | 5 | 4 | 0.25 | 0.9048 | -0.812 | 0.274 |
| GSE253006_TOF_exact_stromal_endothelial_like | recurrence_check | negative_delta_RECEPTOR | 9 | 5 | 4 | 0.05 | 0.9921 | -1.681 | 0.026 |
| GSE253006_TOF_exact_t_cell_like | recurrence_check | negative_delta_RECEPTOR | 9 | 5 | 4 | 0.4 | 0.7222 | -0.1944 | 0.7617 |
| GSE85034_ADA | recurrence_check | negative_delta_RECEPTOR | 14 | 9 | 5 | 0.4444 | 0.6503 | -0.07194 | 0.894 |

## Interpretation

The receptor-side observation is not a stable, same-orientation successor
rule across artifacts. Some exact TOF compartments show high positive
`delta_RECEPTOR` AUCs, while MTX showed high `negative_delta_RECEPTOR`.
That direction/context instability blocks any upgrade. If receptor/coupling
biology is revisited, it should be a separately locked hypothesis tested in
fresh data, not a post-hoc substitute for the V22 IFN/APC rule.
