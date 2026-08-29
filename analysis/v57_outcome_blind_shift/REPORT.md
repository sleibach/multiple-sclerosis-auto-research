# V57 Outcome-Blind Cohort-Shift Preflight

This diagnostic uses no response labels. It does not alter the frozen
score or validation thresholds and is not a biological finding.

| Cohort | n | Energy | Energy FWER p | MMD2 | MMD FWER p | Concordant OOD |
|---|---:|---:|---:|---:|---:|---|
| `GSE235357` | 10 | 0.549 | 0.1387 | 0.085 | 0.0779 | False |
| `GSE85034_ADA` | 14 | 0.418 | 0.3655 | 0.070 | 0.1288 | False |
| `GSE253006_TOF_exact` | 9 | 0.368 | 0.5080 | 0.003 | 0.7888 | False |
| `GSE250453` | 10 | 0.289 | 0.7834 | -0.001 | 0.8309 | False |

A flag means source-distribution transport is unsafe to assume; it
does not explain, invalidate, or rescue an outcome association. The
same outcome-blind diagnostic can be run before labels are opened in
a future eligible validation cohort.
