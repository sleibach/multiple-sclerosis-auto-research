# V36 Technical QC / Batch Feasibility

Status: **completed_metadata_limited_qc_screen**.

- Samples with raw QC computed: `23`.
- Submission dates in SOFT: `Jan 11 2024`.
- Instrument models in SOFT: `Illumina NextSeq 500`.
- Unique data-processing strings: `1`.
- No lane, capture-date, chemistry-batch, ambient RNA, or per-sample
  processing-batch field was present in the held SOFT metadata.

W8 IFN/APC residualization against raw-matrix QC features:

| Compartment | Strongest QC attenuator | Raw AUC | Residualized AUC | Attenuation |
|---|---|---:|---:|---:|
| `b_plasma_like` | `median_pct_mito` | 1.000 | 0.688 | 0.312 |
| `epithelial_like` | `mean_pct_mito` | 1.000 | 0.688 | 0.312 |
| `myeloid_apc_like` | `mean_pct_mito` | 1.000 | 0.562 | 0.438 |
| `stromal_endothelial_like` | `mean_pct_mito` | 0.875 | 0.562 | 0.312 |
| `t_cell_like` | `mean_pct_mito` | 1.000 | 0.750 | 0.250 |

Interpretation:

- True batch confounding cannot be fully tested because batch/lane/capture
  metadata are absent.
- Basic raw-matrix QC residualization is a partial technical-artifact
  screen, not a substitute for batch metadata.
