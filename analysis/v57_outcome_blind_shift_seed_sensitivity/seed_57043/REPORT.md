# V57 Outcome-Blind Cohort-Shift Preflight

This diagnostic uses no response labels. It does not alter the frozen
score or validation thresholds and is not a biological finding.

| Cohort | n | Energy | Energy FWER p | MMD2 | MMD FWER p | Concordant OOD |
|---|---:|---:|---:|---:|---:|---|
| `GSE235357` | 10 | 0.549 | 0.1393 | 0.085 | 0.0775 | False |
| `GSE85034_ADA` | 14 | 0.418 | 0.3699 | 0.070 | 0.1272 | False |
| `GSE253006_TOF_exact` | 9 | 0.368 | 0.5116 | 0.003 | 0.7879 | False |
| `GSE250453` | 10 | 0.289 | 0.7829 | -0.001 | 0.8305 | False |

A flag means source-distribution transport is unsafe to assume; it
does not explain, invalidate, or rescue an outcome association. The
same outcome-blind diagnostic can be run before labels are opened in
a future eligible validation cohort.
