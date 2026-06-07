# V36 B/Plasma Gene Driver Scan

Status: **completed_gene_level_driver_audit**.

- Patients: `9` (`5` responders, `4` non-responders).
- Genes tested: `14` locked module genes.
- Genes with oriented AUC >= 0.9: `2`.
- Genes with exact oriented permutation p <= 0.05: `1`.

Top genes:

| Gene | Oriented AUC | Exact p | Direction in responders | LOO min AUC |
|---|---:|---:|---|---:|
| `STAT1` | 1.000 | 0.0159 | downshift | 1.000 |
| `IRF1` | 0.900 | 0.0635 | downshift | 0.867 |
| `GBP1` | 0.850 | 0.1111 | downshift | 0.800 |
| `ISG15` | 0.850 | 0.1111 | downshift | 0.800 |
| `CD74` | 0.800 | 0.1905 | downshift | 0.733 |
| `CD44` | 0.750 | 0.2857 | downshift | 0.667 |
| `CXCL10` | 0.750 | 0.2857 | downshift | 0.667 |
| `CXCR4` | 0.750 | 0.2857 | downshift | 0.667 |

Interpretation:

- This is a driver audit, not independent validation.
- A broad carrier would show multiple locked IFN/APC genes moving in
  the responder-associated direction rather than a single idiosyncratic
  gene dominating the score.
- Leave-one-out sensitivity is reported because n=9 makes single-patient
  leverage a major risk.
