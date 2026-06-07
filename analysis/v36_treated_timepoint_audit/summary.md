# V36 Treated-Timepoint Audit

Status: **completed_sparse_trajectory_audit**.

- Patients total: `11`.
- Timepoints present: `W0, W16, W24, W48, W8`.

AUC by compartment and timepoint:

| Compartment | Timepoint | n | responders | AUC | Exact p |
|---|---|---:|---:|---:|---:|
| `b_plasma_like` | `W0` | 11 | 5 | 0.500 | 1.0000 |
| `b_plasma_like` | `W16` | 2 | 1 |  |  |
| `b_plasma_like` | `W24` | 1 | 0 |  |  |
| `b_plasma_like` | `W48` | 1 | 1 |  |  |
| `b_plasma_like` | `W8` | 8 | 4 | 1.000 | 0.0286 |
| `epithelial_like` | `W0` | 11 | 5 | 0.533 | 0.9307 |
| `epithelial_like` | `W16` | 2 | 1 |  |  |
| `epithelial_like` | `W24` | 1 | 0 |  |  |
| `epithelial_like` | `W48` | 1 | 1 |  |  |
| `epithelial_like` | `W8` | 8 | 4 | 1.000 | 0.0286 |
| `myeloid_apc_like` | `W0` | 11 | 5 | 0.633 | 0.5368 |
| `myeloid_apc_like` | `W16` | 2 | 1 |  |  |
| `myeloid_apc_like` | `W24` | 1 | 0 |  |  |
| `myeloid_apc_like` | `W48` | 1 | 1 |  |  |
| `myeloid_apc_like` | `W8` | 8 | 4 | 1.000 | 0.0286 |
| `stromal_endothelial_like` | `W0` | 11 | 5 | 0.567 | 0.7922 |
| `stromal_endothelial_like` | `W16` | 2 | 1 |  |  |
| `stromal_endothelial_like` | `W24` | 1 | 0 |  |  |
| `stromal_endothelial_like` | `W48` | 1 | 1 |  |  |
| `stromal_endothelial_like` | `W8` | 8 | 4 | 0.875 | 0.1143 |
| `t_cell_like` | `W0` | 11 | 5 | 0.567 | 0.7922 |
| `t_cell_like` | `W16` | 2 | 1 |  |  |
| `t_cell_like` | `W24` | 1 | 0 |  |  |
| `t_cell_like` | `W48` | 1 | 1 |  |  |
| `t_cell_like` | `W8` | 8 | 4 | 1.000 | 0.0286 |

Interpretation:

- W8 is the only post-baseline timepoint with enough mixed responder status
  for a minimally interpretable early-monitoring check.
- Later timepoints are sparse/imbalanced and should be treated as
  trajectory context only, not validation.
