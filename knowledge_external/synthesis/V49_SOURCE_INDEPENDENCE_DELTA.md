# V49 Source-Independence Delta

Status: synthesis/navigation only. This note summarizes source-independence
accounting after V49 added convergence/context rows. It prevents row-count
corroboration from being overread as independent-source corroboration.

Boundary: external agreement remains context only. The grounded project
artifacts remain the evidence.

## Summary

- convergence/context rows: `7`
- canonical source clusters behind those rows: `5`
- largest shared-source cluster: `3` convergence/context rows from the same
  Nature MS/IBD source URL
- independent-source count to cite for convergence context: `5`, not `7`

## Source-Cluster Accounting

| canonical source cluster | convergence/context rows | rows | interpretation |
|---|---:|---|---|
| https://www.nature.com/articles/s41467-021-25768-0 | 3 | MS-UC genetics comparator; layer-specific transfer-validity map; UC genetics vs treatment-response layer split | One source cluster, not three independent external corroborations. |
| https://pmc.ncbi.nlm.nih.gov/articles/PMC9152176 | 1 | Mucosal IBD early IFN/APC downshift validates while baseline fallback fails | Single independent source cluster. |
| https://www.annualreviews.org/content/journals/10.1146/annurev-biodatasci-102523-103838 | 1 | First-principles druggability discipline changed target interpretation | Single independent source cluster; fuller reuse requires access/terms review. |
| https://pubmed.ncbi.nlm.nih.gov/30596875 | 1 | Tool-robust but simple V22 scalar | Single independent source cluster; method-context corroboration only. |
| https://pmc.ncbi.nlm.nih.gov/articles/PMC3836799 | 1 | MHC overlap is distinct-signal, not simple shared biology | Single independent source cluster. |

## Decision

When summarizing V49 convergence, say:

> V49 records `7` convergence/context rows backed by `5` canonical source
> clusters.

Do not say:

> V49 has `7` independent external corroborations.

That wording would overcount the shared Nature MS/IBD source cluster.

