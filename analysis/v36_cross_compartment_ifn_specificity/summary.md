# V36 Cross-Compartment IFN Specificity

Status: **completed_specificity_scan**.

- Compartments tested: `5`.
- Patients per compartment: `9`.
- Top STAT1 compartment: `b_plasma_like` (AUC `1.000`, exact p `0.0159`).
- Top locked-score compartment: `t_cell_like` (AUC `1.000`, exact p `0.0159`).

STAT1 downshift by compartment:

| Compartment | AUC | Exact p |
|---|---:|---:|
| `b_plasma_like` | 1.000 | 0.0159 |
| `myeloid_apc_like` | 1.000 | 0.0159 |
| `epithelial_like` | 0.950 | 0.0317 |
| `stromal_endothelial_like` | 0.900 | 0.0635 |
| `t_cell_like` | 0.900 | 0.0635 |

Locked score by compartment:

| Compartment | AUC | Exact p |
|---|---:|---:|
| `t_cell_like` | 1.000 | 0.0159 |
| `b_plasma_like` | 0.950 | 0.0317 |
| `epithelial_like` | 0.900 | 0.0635 |
| `myeloid_apc_like` | 0.800 | 0.1905 |
| `stromal_endothelial_like` | 0.750 | 0.2857 |

Interpretation:

- If STAT1 downshift is high across many compartments, the B/plasma
  carrier is likely a compartment-resolved view of generic IFN response.
- If B/plasma is selectively high after comparison with other compartments,
  the carrier interpretation is more specific.
