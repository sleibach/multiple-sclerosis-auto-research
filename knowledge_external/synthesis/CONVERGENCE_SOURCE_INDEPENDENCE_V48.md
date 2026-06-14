# V48 Convergence Source-Independence Matrix

Status: synthesis/navigation only. This matrix prevents overcounting multiple rows from the same external source as independent corroborations.

- matrix rows: `23`
- decision relationship rows: `7`
- decision canonical sources: `5`
- convergence rows: `7`
- convergence canonical sources: `5`

## Decision Relationship Source Clusters

| relationship | grounded finding | external record | canonical source | source class | boundary |
|---|---|---|---|---|---|
| `converges` | MS-UC is strongest tested genome-wide genetics comparator | `claim.nature.ms_uc_greater_genetic_correlation_context.2026-06-14` | https://www.nature.com/articles/s41467-021-25768-0 | `shared_source_cluster` | A shared canonical source is one external source cluster, not multiple independent corroborations. |
| `converges` | Layer-specific autoimmune transfer-validity map | `claim.ms_ibd.treatment_transfer_caution_context.2026-06-14` | https://www.nature.com/articles/s41467-021-25768-0 | `shared_source_cluster` | A shared canonical source is one external source cluster, not multiple independent corroborations. |
| `converges` | Mucosal IBD early IFN/APC downshift validates while baseline fallback fails | `claim.frontiers.uc_tofacitinib_mhc_stat1_context.2026-06-14` | https://pmc.ncbi.nlm.nih.gov/articles/PMC9152176 | `single_row_source` | A shared canonical source is one external source cluster, not multiple independent corroborations. |
| `converges` | UC genetics vs treatment-response layer split | `claim.ms_ibd.treatment_transfer_caution_context.2026-06-14` | https://www.nature.com/articles/s41467-021-25768-0 | `shared_source_cluster` | A shared canonical source is one external source cluster, not multiple independent corroborations. |
| `converges` | First-principles druggability discipline changed target interpretation | `claim.open_targets.direction_tractability_context.2026-06-14` | https://www.annualreviews.org/content/journals/10.1146/annurev-biodatasci-102523-103838 | `single_row_source` | A shared canonical source is one external source cluster, not multiple independent corroborations. |
| `converges` | Tool-robust but simple V22 scalar | `claim.probast_tripod.prediction_model_validation_context.2026-06-14` | https://pubmed.ncbi.nlm.nih.gov/30596875 | `shared_source_cluster` | A shared canonical source is one external source cluster, not multiple independent corroborations. |
| `converges` | MHC overlap is distinct-signal, not simple shared biology | `claim.plos.ms_mhc_independent_effects_context.2026-06-14` | https://pmc.ncbi.nlm.nih.gov/articles/PMC3836799 | `single_row_source` | A shared canonical source is one external source cluster, not multiple independent corroborations. |

## Interpretation

- Current V48 convergence rows are useful corroborating context, but source independence is counted by canonical source URL, not row count.
- If multiple rows share one canonical source, treat them as one source cluster for independence accounting.
- This matrix does not change any grounded finding or evidence grade.
