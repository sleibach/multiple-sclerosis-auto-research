# V36 Baseline-Versus-Delta Decomposition

Status: **completed_monitoring_vs_baseline_audit**.

- Patients: `9`.
- Compartments: `5`.

| Compartment | Feature | AUC | Exact p |
|---|---|---:|---:|
| `b_plasma_like` | `treated_IFN_APC` | 1.000 | 0.0159 |
| `b_plasma_like` | `locked_delta_score` | 0.950 | 0.0317 |
| `b_plasma_like` | `treated_HLAII` | 0.900 | 0.0635 |
| `b_plasma_like` | `hla_delta_score` | 0.700 | 0.4127 |
| `b_plasma_like` | `baseline_HLAII` | 0.550 | 0.9048 |
| `b_plasma_like` | `baseline_IFN_APC` | 0.500 | 1.0000 |
| `epithelial_like` | `treated_IFN_APC` | 1.000 | 0.0159 |
| `epithelial_like` | `treated_HLAII` | 0.950 | 0.0317 |
| `epithelial_like` | `locked_delta_score` | 0.900 | 0.0635 |
| `epithelial_like` | `hla_delta_score` | 0.800 | 0.1905 |
| `epithelial_like` | `baseline_HLAII` | 0.650 | 0.5556 |
| `epithelial_like` | `baseline_IFN_APC` | 0.500 | 1.0000 |
| `myeloid_apc_like` | `treated_IFN_APC` | 1.000 | 0.0159 |
| `myeloid_apc_like` | `locked_delta_score` | 0.800 | 0.1905 |
| `myeloid_apc_like` | `baseline_IFN_APC` | 0.650 | 0.5556 |
| `myeloid_apc_like` | `treated_HLAII` | 0.650 | 0.5556 |
| `myeloid_apc_like` | `hla_delta_score` | 0.600 | 0.7302 |
| `myeloid_apc_like` | `baseline_HLAII` | 0.550 | 0.9048 |
| `stromal_endothelial_like` | `treated_IFN_APC` | 0.900 | 0.0635 |
| `stromal_endothelial_like` | `locked_delta_score` | 0.750 | 0.2857 |
| `stromal_endothelial_like` | `baseline_HLAII` | 0.650 | 0.5556 |
| `stromal_endothelial_like` | `treated_HLAII` | 0.650 | 0.5556 |
| `stromal_endothelial_like` | `hla_delta_score` | 0.550 | 0.9048 |
| `stromal_endothelial_like` | `baseline_IFN_APC` | 0.500 | 1.0000 |
| `t_cell_like` | `treated_IFN_APC` | 1.000 | 0.0159 |
| `t_cell_like` | `locked_delta_score` | 1.000 | 0.0159 |
| `t_cell_like` | `treated_HLAII` | 0.800 | 0.1905 |
| `t_cell_like` | `baseline_HLAII` | 0.650 | 0.5556 |
| `t_cell_like` | `baseline_IFN_APC` | 0.550 | 0.9048 |
| `t_cell_like` | `hla_delta_score` | 0.550 | 0.9048 |

Interpretation:

- If baseline features match or beat delta, the readout is closer to
  stratification than monitoring.
- If delta/treatment features dominate, the monitoring interpretation is
  better supported.
