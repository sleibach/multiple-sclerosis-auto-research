# V36 B/Plasma Timepoint Sensitivity

Status: **completed_timepoint_and_leverage_audit**.

- Patients: `9`.
- W8-only patients after excluding W48 TOF_009: `8`.
- Locked score AUC all patients: `0.950`.
- Locked score AUC W8-only: `0.938`.
- STAT1 AUC excluding W48 TOF_009: `1.000`.
- Leave-one-out minimum locked-score AUC: `0.933`.
- Leave-one-out minimum STAT1 AUC: `1.000`.

| Subset | Feature | n | responders | AUC | Exact p |
|---|---|---:|---:|---:|---:|
| `all_patients` | `locked_signed_score` | 9 | 5 | 0.950 | 0.0317 |
| `all_patients` | `delta_IFN_APC` | 9 | 5 | 0.950 | 0.0317 |
| `all_patients` | `delta_STAT1` | 9 | 5 | 1.000 | 0.0159 |
| `all_patients` | `delta_IRF1` | 9 | 5 | 0.900 | 0.0635 |
| `w8_only` | `locked_signed_score` | 8 | 4 | 0.938 | 0.0571 |
| `w8_only` | `delta_IFN_APC` | 8 | 4 | 0.938 | 0.0571 |
| `w8_only` | `delta_STAT1` | 8 | 4 | 1.000 | 0.0286 |
| `w8_only` | `delta_IRF1` | 8 | 4 | 0.875 | 0.1143 |
| `exclude_tof_009_w48` | `locked_signed_score` | 8 | 4 | 0.938 | 0.0571 |
| `exclude_tof_009_w48` | `delta_IFN_APC` | 8 | 4 | 0.938 | 0.0571 |
| `exclude_tof_009_w48` | `delta_STAT1` | 8 | 4 | 1.000 | 0.0286 |
| `exclude_tof_009_w48` | `delta_IRF1` | 8 | 4 | 0.875 | 0.1143 |

Interpretation:

- Excluding the single W48 responder tests whether the signal is a
  long-treatment-time artifact.
- Leave-one-out minima test whether one patient is necessary for the
  separation.
- This is still internal sensitivity only; it does not replace external
  replication.
