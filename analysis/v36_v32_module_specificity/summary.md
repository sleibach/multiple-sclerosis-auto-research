# V36 V32 Module Specificity

Status: **completed_subject_level_module_specificity_scan**.

- Patients: `9`.
- V32 numeric features tested: `28`.
- Top feature: `delta_IFN_APC` (AUC `0.950`, exact p `0.0317`).

Top module features:

| Rank | Feature | AUC | Exact p | Direction in responders |
|---:|---|---:|---:|---|
| 1 | `delta_IFN_APC` | 0.950 | 0.0317 | lower |
| 2 | `delta_glycolysis` | 0.950 | 0.0317 | lower |
| 3 | `delta_stat1_axis` | 0.950 | 0.0317 | lower |
| 4 | `locked_signed_score` | 0.950 | 0.0317 | higher |
| 5 | `delta_ifn_suppression_inverse_isg` | 0.900 | 0.0635 | lower |
| 6 | `delta_t_cell_composition` | 0.900 | 0.0635 | lower |
| 7 | `delta_b_cell_composition` | 0.850 | 0.1111 | lower |
| 8 | `delta_HLAII` | 0.800 | 0.1905 | lower |
| 9 | `baseline_monocyte_myeloid_composition` | 0.800 | 0.1905 | lower |
| 10 | `delta_monocyte_myeloid_composition` | 0.800 | 0.1905 | lower |
| 11 | `delta_immunometabolism_hif_nampt` | 0.750 | 0.2857 | lower |
| 12 | `delta_general_inflammatory_tone` | 0.750 | 0.2857 | lower |

IFN/STAT-related feature ranks:

| Feature | Rank | AUC | Exact p |
|---|---:|---:|---:|
| `delta_IFN_APC` | 1 | 0.950 | 0.0317 |
| `delta_stat1_axis` | 3 | 0.950 | 0.0317 |
| `delta_ifn_suppression_inverse_isg` | 5 | 0.900 | 0.0635 |
| `baseline_IFN_APC` | 15 | 0.600 | 0.7302 |
| `baseline_stat1_axis` | 21 | 0.600 | 0.7302 |
| `baseline_ifn_suppression_inverse_isg` | 28 | 0.500 | 1.0000 |

Interpretation:

- This is a subject-level module scan over V32 panels in the exact
  tofacitinib cohort.
- If many non-IFN modules tie the IFN/STAT modules, the response state is
  broad immune/metabolic remodeling rather than IFN-specific.
- Exact p-values are discrete at n=9 and should be interpreted as ranking
  and stress-testing, not validation.
