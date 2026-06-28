# V50 EBV Specificity Source Search Results

Status: future search/navigation only. This file records a narrow source-search
pass for EBV/IFN APC imprint specificity. It does not add external records,
assert convergence, or alter the project's EBV specificity downgrade.

Search date: `2026-06-28`.

## Search Queries Run

| route | query |
|---|---|
| web / literature | `"EBV" "multiple sclerosis" "autoimmune comparator" "interferon" transcriptome` |
| web / literature | `"EBNA1" "multiple sclerosis" "systemic lupus" "interferon"` |
| web / literature | `"EBV" "multiple sclerosis" "B cell" "antigen presentation" "single-cell"` |
| web / literature | `"EBV" "multiple sclerosis" RNA-seq autoimmune comparator` |

## Candidate Hits

| candidate | source | overlap | decision |
|---|---|---|---|
| EBV reprograms anti-CNS B cells as antigen-presenting cells in MS | https://pmc.ncbi.nlm.nih.gov/articles/PMC12919047/ | Strong EBV/APC/B-cell overlap in MS, including antigen-presentation and activation context. | close context, but not a same-definition MS-versus-autoimmune-comparator specificity test. |
| EBV anti-CNS B-cell APC preprint / source record already represented in V50 | https://pubmed.ncbi.nlm.nih.gov/41727017/ | Same source family as the V50 EBV APC context record. | already represented as context; do not double count. |
| EBV-transformed B cells from SLE and MS differ in EBV lytic and latency marker expression | https://pmc.ncbi.nlm.nih.gov/articles/PMC13097320/ | Directly compares SLE and MS EBV-transformed B-cell context, but appears centered on lytic/latency markers rather than the project IFN/APC imprint. | promising future source candidate; requires detailed source review before any relationship row. |
| SLE and EBV interferon / anti-EBNA1 review context | https://pmc.ncbi.nlm.nih.gov/articles/PMC2885576/ | SLE EBV/IFN context supports the concern that EBV/IFN signatures are not MS-specific by default. | context only; does not test project modules. |
| EBNA1/GlialCAM MS cross-reactive B cells | https://pubmed.ncbi.nlm.nih.gov/35073561/ | Strong EBV-MS B-cell molecular mimicry source already represented in V50. | already represented as context; not a specificity-control rescue. |
| EBV infection and HLA-DR15 jointly drive MS by B-cell antigen presentation | https://www.cell.com/cell/fulltext/S0092-8674%2825%2901495-3 | Strong MS EBV/HLA/B-cell antigen-presentation context. | potential future source candidate; still needs autoimmune comparator or specificity design. |

## Result

No same-definition external source was found that tests the project's EBV/IFN
APC imprint against MS controls and non-MS autoimmune comparators under
comparable expression/module definitions.

The strongest search outcome is a refined future-source target: sources that
jointly measure EBV-positive or EBV-reactive B/APC states in MS and a comparator
autoimmune disease, with scoreable IFN/APC/HLA-II expression. Generic EBV-risk,
EBNA1 mimicry, or MS-only EBV APC sources are not enough.

## Decision

Keep the EBV/IFN APC imprint specificity row downgraded. Current external
sources support EBV relevance and EBV-linked B-cell/APC biology, but they do not
overturn the project's specificity-control result.
