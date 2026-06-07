# V36 Glycolysis-IFN Decoupling

Status: **completed_subject_level_decoupling_test**.

- Patients: `9`.
- Raw glycolysis AUC: `0.950`.
- Glycolysis residualized against IFN/APC + STAT1 AUC: `0.600`.
- IFN/APC residualized against glycolysis AUC: `0.850`.

| Test | AUC | Exact p |
|---|---:|---:|
| `glycolysis_raw` | 0.950 | 0.0317 |
| `ifn_apc_raw` | 0.950 | 0.0317 |
| `stat1_axis_raw` | 0.950 | 0.0317 |
| `ifn_apc_resid_glycolysis` | 0.850 | 0.1111 |
| `stat1_resid_glycolysis` | 0.800 | 0.1905 |
| `glycolysis_resid_stat1` | 0.700 | 0.4127 |
| `glycolysis_resid_ifn_apc` | 0.600 | 0.7302 |
| `glycolysis_resid_ifn_and_stat1` | 0.600 | 0.7302 |

Module correlations:

| Feature A | Feature B | Spearman | Pearson |
|---|---|---:|---:|
| `delta_glycolysis` | `delta_IFN_APC` | 0.967 | 0.798 |
| `delta_glycolysis` | `delta_stat1_axis` | 0.983 | 0.782 |
| `delta_glycolysis` | `delta_ifn_suppression_inverse_isg` | 0.883 | 0.424 |
| `delta_IFN_APC` | `delta_stat1_axis` | 0.983 | 0.985 |
| `delta_IFN_APC` | `delta_ifn_suppression_inverse_isg` | 0.933 | 0.843 |
| `delta_stat1_axis` | `delta_ifn_suppression_inverse_isg` | 0.900 | 0.837 |

Interpretation:

- If glycolysis residualized against IFN/STAT collapses, glycolysis is not
  an independent component of the response signal.
- If IFN/APC residualized against glycolysis remains high, IFN/APC is the
  more primary readout in this held data.
