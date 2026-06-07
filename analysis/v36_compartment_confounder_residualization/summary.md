# V36 Compartment Confounder Residualization

Status: **completed_using_v32_subject_level_confounders**.

- Patients: `9`.
- Compartments tested: `3`.
- Confounders tested per compartment: `9`.

| Compartment | Raw AUC | Strongest attenuator | Residualized AUC | Exact p | Attenuation |
|---|---:|---|---:|---:|---:|
| `b_plasma_like` | 0.950 | `delta_stat1_axis` | 0.600 | 0.7302 | 0.350 |
| `myeloid_apc_like` | 0.800 | `delta_stat1_axis` | 0.550 | 0.9048 | 0.250 |
| `t_cell_like` | 1.000 | `delta_stat1_axis` | 0.500 | 1.0000 | 0.500 |

Interpretation:

- This reuses V32 cohort-level confounder scores and tests whether the
  compartment-level locked readouts survive one-confounder residualization.
- Because n=9, this is a sensitivity screen, not a definitive adjusted model.
- The lowest residualized AUC per compartment is the conservative stress test.
