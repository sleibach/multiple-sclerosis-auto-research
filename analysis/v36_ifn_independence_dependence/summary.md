# V36 IFN Independence and Gene Dependence

Status: **completed_grounding_of_two_lineage_proposals**.

- Patients: `9`.
- B/plasma vs myeloid IFN/STAT Pearson r: `0.597` (p `0.0900`).
- B/plasma vs myeloid IFN/STAT Spearman rho: `0.900` (p `0.0009`).
- B/plasma IFN/STAT AUC: `0.950` (exact p `0.0317`).
- Myeloid IFN/STAT AUC: `0.900` (exact p `0.0635`).
- B/plasma residual after myeloid AUC: `0.650` (exact p `0.5556`).

B/plasma leave-one-gene dependence:

| Score | Genes | AUC | Exact p |
|---|---|---:|---:|
| `full_ifn_stat` | `STAT1,IRF1,GBP1,ISG15` | 0.950 | 0.0317 |
| `omit_STAT1` | `IRF1,GBP1,ISG15` | 0.950 | 0.0317 |
| `omit_IRF1` | `STAT1,GBP1,ISG15` | 0.850 | 0.1111 |
| `omit_GBP1` | `STAT1,IRF1,ISG15` | 0.950 | 0.0317 |
| `omit_ISG15` | `STAT1,IRF1,GBP1` | 0.950 | 0.0317 |
| `single_STAT1` | `STAT1` | 1.000 | 0.0159 |
| `single_IRF1` | `IRF1` | 0.900 | 0.0635 |
| `single_GBP1` | `GBP1` | 0.850 | 0.1111 |
| `single_ISG15` | `ISG15` | 0.850 | 0.1111 |

Interpretation:

- High B/plasma-myeloid correlation would support a broad shared IFN
  remodeling interpretation.
- Collapse after residualizing B/plasma against myeloid would argue against
  B/plasma-independent signal.
- A leave-one-gene collapse would indicate a single-gene signature rather
  than a module.
