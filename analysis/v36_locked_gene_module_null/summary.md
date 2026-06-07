# V36 Locked-Gene Module Null

Status: **completed_limited_empirical_null**.

Important limitation: the exact compartment matrix contains the locked
module genes, not a full transcriptome. This control compares the IFN/STAT
four-gene set against all same-size combinations of the available locked
genes; it is not a genome-wide random-gene null.

- Available genes: `6`.
- Combo size: `4`.
- Combos per compartment: `15`.
- IFN/STAT set: `STAT1, IRF1, GBP1, ISG15`.

| Compartment | IFN/STAT AUC | Empirical combo p | Same/better combos | Best combo | Best AUC |
|---|---:|---:|---:|---|---:|
| `b_plasma_like` | 0.950 | 0.3333 | 5/15 | `CD74,GBP1,IRF1,ISG15` | 0.950 |
| `epithelial_like` | 0.950 | 0.9333 | 14/15 | `CD74,GBP1,IRF1,STAT1` | 1.000 |
| `myeloid_apc_like` | 0.900 | 0.2000 | 3/15 | `CD74,GBP1,IRF1,STAT1` | 0.950 |
| `t_cell_like` | 0.800 | 0.7333 | 11/15 | `CD74,GBP1,HLA-DRA,IRF1` | 1.000 |
| `stromal_endothelial_like` | 0.550 | 1.0000 | 15/15 | `GBP1,HLA-DRA,ISG15,STAT1` | 0.900 |

Interpretation:

- If the IFN/STAT set sits near the top of this locked-gene combination
  null, the signal is not trivially reproduced by arbitrary locked genes.
- If many same-size combinations match or beat it, the apparent module
  specificity is weak within the measured gene set.
