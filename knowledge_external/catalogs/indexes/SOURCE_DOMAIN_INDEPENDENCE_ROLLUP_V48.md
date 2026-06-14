# V48 Source-Domain Independence Rollup

Status: provenance/navigation only. This rollup summarizes source-domain and canonical-source concentration for V48 matrix rows; it does not validate external claims.

- V48 matrix rows represented: `23`
- source domains represented: `9`
- canonical source clusters represented: `15`
- decision relationship rows: `7`
- decision canonical source clusters: `5`
- domains with convergence rows: `4`
- domains with contradiction rows: `0`

## Domains

| domain | rows | canonical clusters | decision rows | convergence | contradiction | insufficient overlap | relationship counts | independence classes | boundary |
|---|---:|---:|---:|---:|---:|---:|---|---|---|
| www.nature.com | 5 | 1 | 3 | 3 | 0 | 2 | `converges:3;insufficient-overlap:2` | `not_decision_relationship:2;shared_source_cluster:3` | Decision-relevant convergence is present, but the domain contributes one canonical source cluster; do not count multiple rows as independent corroborations. |
| pmc.ncbi.nlm.nih.gov | 4 | 4 | 2 | 2 | 0 | 2 | `converges:2;insufficient-overlap:2` | `not_decision_relationship:2;single_row_source:2` | Decision-relevant relationship is spread across multiple canonical source clusters; still external context, not project evidence. |
| pubmed.ncbi.nlm.nih.gov | 4 | 3 | 1 | 1 | 0 | 3 | `converges:1;insufficient-overlap:3` | `not_decision_relationship:3;shared_source_cluster:1` | Decision-relevant relationship is spread across multiple canonical source clusters; still external context, not project evidence. |
| www.annualreviews.org | 1 | 1 | 1 | 1 | 0 | 0 | `converges:1` | `single_row_source:1` | Decision-relevant convergence is present, but the domain contributes one canonical source cluster; do not count multiple rows as independent corroborations. |
| dailymed.nlm.nih.gov | 4 | 2 | 0 | 0 | 0 | 4 | `insufficient-overlap:4` | `not_decision_relationship:4` | Insufficient-overlap/resource context only; not external corroboration or contradiction. |
| ngdc.cncb.ac.cn | 2 | 1 | 0 | 0 | 0 | 2 | `insufficient-overlap:2` | `not_decision_relationship:2` | Insufficient-overlap/resource context only; not external corroboration or contradiction. |
| disgenet.com | 1 | 1 | 0 | 0 | 0 | 1 | `insufficient-overlap:1` | `not_decision_relationship:1` | Insufficient-overlap/resource context only; not external corroboration or contradiction. |
| www.ebi.ac.uk | 1 | 1 | 0 | 0 | 0 | 1 | `insufficient-overlap:1` | `not_decision_relationship:1` | Insufficient-overlap/resource context only; not external corroboration or contradiction. |
| www.nationalmssociety.org | 1 | 1 | 0 | 0 | 0 | 1 | `insufficient-overlap:1` | `not_decision_relationship:1` | Insufficient-overlap/resource context only; not external corroboration or contradiction. |

## Interpretation

- Decision rows are counted separately from canonical source clusters to prevent source overcounting.
- Current convergence is domain- and source-cluster concentrated; the grounded project artifact remains the evidence.
- Insufficient-overlap rows remain context/resource pointers, not corroboration.
- No row here changes a grounded finding, locked rule, validation plan, or V37 score.
