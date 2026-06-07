# V36 RPT Refined Carrier Pass

Status: **completed_as_prioritization_lens_only**.

RPT role: tabular carrier-prioritization lens. It is not biological
evidence; only the already-run real-data tests count as grounding.

- Rows: `10`
- Masked rows: refined V36 carrier candidates.
- Known labels: weak/unbounded scalar, bounded scalar, composition proxy,
  and blocked independent replication row.

| Row | RPT top prediction | Confidence | Grounded interpretation |
|---|---|---:|---|
| `V36_t_cell_raw` | `promising_but_unreplicated` | 0.730 | Raw AUC is strongest, but residualized AUC fell to 0.650; composition/sampling sensitivity remains. |
| `V36_b_plasma_locked` | `promising_but_unreplicated` | 0.880 | B/plasma locked score has AUC 0.950 and residualized AUC 0.850; promising carrier but unreplicated. |
| `V36_b_plasma_ifn_apc` | `promising_but_unreplicated` | 0.800 | B/plasma IFN/APC delta has AUC 0.950 and exact p 0.0317; best mechanistic carrier in held data. |
| `V36_b_plasma_hlaii_only` | `weak_or_unbounded` | 0.520 | HLA-II-only component is weaker (AUC 0.700), so scalar HLA-II alone is not the carrier. |
| `V36_b_plasma_receptor_only` | `promising_but_unreplicated` | 0.730 | Receptor-only component is weaker (AUC 0.750), so MIF/CD74 alone is not sufficient. |
| `V36_tb_mean` | `promising_but_unreplicated` | 0.920 | T/B mean matches B/plasma AUC but adds post-hoc combination risk. |

Grounded verdict:

- RPT should not upgrade any carrier.
- If RPT prioritizes B/plasma IFN/APC, it agrees with the real-data
  decomposition; the evidence remains n=9 and unreplicated.
- If RPT prioritizes T-cell raw, the artifact audit still overrides it
  because residualized T-cell performance attenuated sharply.
