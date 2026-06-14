# V48 Source-Domain Independence Rollup

Status: provenance/navigation only. This rollup summarizes source-domain and canonical-source concentration for V48 matrix rows; it does not validate external claims.

- V48 matrix rows represented: `12`
- source domains represented: `6`
- canonical source clusters represented: `7`
- decision relationship rows: `2`
- decision canonical source clusters: `1`
- domains with convergence rows: `1`
- domains with contradiction rows: `0`

## Domains

| domain | rows | canonical clusters | decision rows | convergence | contradiction | insufficient overlap | relationship counts | independence classes | boundary |
|---|---:|---:|---:|---:|---:|---:|---|---|---|
| www.nature.com | 3 | 1 | 2 | 2 | 0 | 1 | `converges:2;insufficient-overlap:1` | `not_decision_relationship:1;shared_source_cluster:2` | Decision-relevant convergence is present, but the domain contributes one canonical source cluster; do not count multiple rows as independent corroborations. |
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
