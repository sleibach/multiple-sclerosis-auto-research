# V36 B/Plasma Substate Audit

Status: **completed_lightweight_raw_substate_audit**.

- Samples processed: `23`.
- Paired patients: `9`.
- Top feature: `delta_ifn_apc_plasma_like` (AUC `1.000`, exact p `0.0159`).

| Feature | n | AUC | Exact p |
|---|---:|---:|---:|
| `delta_ifn_apc_plasma_like` | 9 | 1.000 | 0.0159 |
| `treated_ifn_apc_b_like` | 9 | 1.000 | 0.0159 |
| `treated_ifn_apc_plasma_like` | 9 | 1.000 | 0.0159 |
| `delta_ifn_apc_b_like` | 9 | 0.950 | 0.0317 |
| `treated_ifn_apc_all_bplasma` | 9 | 0.950 | 0.0317 |
| `delta_frac_b_plasma` | 9 | 0.850 | 0.1111 |
| `delta_ifn_apc_all_bplasma` | 9 | 0.850 | 0.1111 |
| `delta_frac_b_like_within_bplasma` | 9 | 0.600 | 0.7302 |
| `delta_frac_plasma_like_within_bplasma` | 9 | 0.600 | 0.7302 |

Interpretation:

- This is a lightweight marker split, not a full single-cell clustering
  analysis.
- If fraction features dominate, B/plasma composition is the likely carrier.
- If within-substate IFN/APC features dominate, within-cell remodeling is
  better supported.
