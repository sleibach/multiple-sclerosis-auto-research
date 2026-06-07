# V36 W8 Treated IFN Confounder Residualization

Status: **completed_w8_treated_state_stress_test**.

- W8 patients: `8`.
- Compartments tested: `5`.
- Confounders tested: `9`.

| Compartment | Raw AUC | Strongest attenuator | Residualized AUC | Exact p | Attenuation |
|---|---:|---|---:|---:|---:|
| `b_plasma_like` | 1.000 | `delta_stat1_axis` | 0.625 | 0.6857 | 0.375 |
| `epithelial_like` | 1.000 | `delta_t_cell_composition` | 0.625 | 0.6857 | 0.375 |
| `myeloid_apc_like` | 1.000 | `delta_stat1_axis` | 0.688 | 0.4857 | 0.312 |
| `stromal_endothelial_like` | 0.875 | `delta_t_cell_composition` | 0.562 | 0.8857 | 0.312 |
| `t_cell_like` | 1.000 | `delta_t_cell_composition` | 0.750 | 0.3429 | 0.250 |

Interpretation:

- This tests the W8 treated-state readout directly, not the baseline-to
  treated locked delta score.
- Strong attenuation under STAT1-axis or IFN-suppression panels means the
  readout is a generic IFN-axis state rather than an orthogonal T/B marker.
