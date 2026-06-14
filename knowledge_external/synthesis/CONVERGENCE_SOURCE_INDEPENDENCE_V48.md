# V48 Convergence Source-Independence Matrix

Status: synthesis/navigation only. This matrix prevents overcounting multiple rows from the same external source as independent corroborations.

- matrix rows: `12`
- decision relationship rows: `2`
- decision canonical sources: `1`
- convergence rows: `2`
- convergence canonical sources: `1`

## Decision Relationship Source Clusters

| relationship | grounded finding | external record | canonical source | source class | boundary |
|---|---|---|---|---|---|
| `converges` | MS-UC is strongest tested genome-wide genetics comparator | `claim.nature.ms_uc_greater_genetic_correlation_context.2026-06-14` | https://www.nature.com/articles/s41467-021-25768-0 | `shared_source_cluster` | A shared canonical source is one external source cluster, not multiple independent corroborations. |
| `converges` | Layer-specific autoimmune transfer-validity map | `claim.ms_ibd.treatment_transfer_caution_context.2026-06-14` | https://www.nature.com/articles/s41467-021-25768-0 | `shared_source_cluster` | A shared canonical source is one external source cluster, not multiple independent corroborations. |

## Interpretation

- Current V48 convergence rows are useful corroborating context, but source independence is counted by canonical source URL, not row count.
- If multiple rows share one canonical source, treat them as one source cluster for independence accounting.
- This matrix does not change any grounded finding or evidence grade.
