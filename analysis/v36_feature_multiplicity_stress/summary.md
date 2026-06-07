# V36 Feature Multiplicity Stress Test

Status: **completed_exact_max_auc_null**.

- Patients: `9`.
- Features tested: `76`.
- Observed max AUC: `1.000`.
- Features at max AUC: `8`.
- Label permutations: `126`.
- Empirical p for max AUC >= observed max: `0.5000`.
- Fraction of permutations with max AUC >= 0.95: `0.7063`.

Top features:

| Rank | Feature | AUC |
|---:|---|---:|
| 1 | `bd_epithelial_like__treated_IFN_APC` | 1.000 |
| 2 | `bd_t_cell_like__locked_delta_score` | 1.000 |
| 3 | `substate__delta_ifn_apc_plasma_like` | 1.000 |
| 4 | `substate__treated_ifn_apc_plasma_like` | 1.000 |
| 5 | `bd_myeloid_apc_like__treated_IFN_APC` | 1.000 |
| 6 | `substate__treated_ifn_apc_b_like` | 1.000 |
| 7 | `bd_t_cell_like__treated_IFN_APC` | 1.000 |
| 8 | `bd_b_plasma_like__treated_IFN_APC` | 1.000 |
| 9 | `v32__delta_IFN_APC` | 0.950 |
| 10 | `bd_b_plasma_like__locked_delta_score` | 0.950 |
| 11 | `bd_epithelial_like__treated_HLAII` | 0.950 |
| 12 | `v32__delta_stat1_axis` | 0.950 |
| 13 | `substate__delta_ifn_apc_b_like` | 0.950 |
| 14 | `v32__delta_glycolysis` | 0.950 |
| 15 | `substate__treated_ifn_apc_all_bplasma` | 0.950 |

Interpretation:

- This controls only the post-hoc feature search within generated V36
  patient-level features; it does not replace external replication.
- If high max AUC is common under label permutations, perfect individual
  features must be treated as exploratory rather than validated.
