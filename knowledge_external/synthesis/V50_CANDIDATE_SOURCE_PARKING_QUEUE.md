# V50 Candidate Source Parking Queue

Status: parking queue only. These candidates were surfaced during V50 source
searches but did not meet the same-definition intake bar. Parking them prevents
both loss and overclaiming.

Inputs:

- `knowledge_external/synthesis/V50_TB_MONITORING_SOURCE_SEARCH_RESULTS.md`
- `knowledge_external/synthesis/V50_EBV_SPECIFICITY_SOURCE_SEARCH_RESULTS.md`

## Parking Rules

1. A parked source is not an external record.
2. A parked source is not convergence or contradiction.
3. A parked source can leave parking only after source review, source terms
   review, and same-definition overlap assessment.
4. If a parked source is groundable on data, it must route to a future
   grounding queue before any finding-level statement.

## Parked T/B Monitoring Candidates

| candidate | source | why parked | release condition |
|---|---|---|---|
| IFN-beta gene dysregulation correction in MS | https://pmc.ncbi.nlm.nih.gov/articles/PMC6945282/ | IFN-beta expression context, but not a T/B-readable early monitoring rule with response labels. | Release only if detailed review finds compartment-readable IFN/APC/STAT1 readouts and response/state labels. |
| Cladribine single-cell memory B-cell treatment-response context | https://pmc.ncbi.nlm.nih.gov/articles/PMC10710756/ | Single-cell B-cell treatment response, but not the V50 T/B IFN/APC/STAT1 state and not DMF. | Release as B-cell treatment-response context only if source review confirms usable compartment/state fields. |
| B-cell activity predicts response to glatiramer acetate or IFN beta-1a | https://www.neurology.org/doi/10.1212/NXI.0000000000000980 | B-cell response relevance, but same-definition IFN/APC/STAT1 module overlap not established. | Release only after full text/data review confirms module-scoreable expression and response labels. |
| HLA-DQB1 and immune phenotypes in IFN-beta failure | https://www.frontiersin.org/journals/immunology/articles/10.3389/fimmu.2021.628375/full | HLA/immune phenotype and treatment failure context, but not transcriptomic T/B/APC monitoring under project definitions. | Release only as treatment-failure immune-phenotype context, not as scalar validation. |

## Parked EBV Specificity Candidates

| candidate | source | why parked | release condition |
|---|---|---|---|
| EBV reprograms anti-CNS B cells as APC in MS | https://pmc.ncbi.nlm.nih.gov/articles/PMC12919047/ | Strong EBV/APC/B-cell overlap, but not a same-definition MS-plus-autoimmune-comparator expression test. | Release only if data allow project IFN/APC/HLA-II scoring and comparator specificity testing. |
| EBV-transformed B cells from SLE and MS differ in lytic/latency markers | https://pmc.ncbi.nlm.nih.gov/articles/PMC13097320/ | Cross-disease EBV B-cell context, but project IFN/APC imprint overlap is not established. | Release only after detailed source review confirms expression fields relevant to project specificity controls. |
| SLE EBV/interferon context | https://pmc.ncbi.nlm.nih.gov/articles/PMC2885576/ | Supports the risk that EBV/IFN biology is not MS-specific, but does not test project modules. | Release only as context if source review requires a SLE comparator background record. |
| EBV infection and HLA-DR15 B-cell antigen presentation in MS | https://www.cell.com/cell/fulltext/S0092-8674%2825%2901495-3 | Strong MS EBV/HLA/B-cell mechanism, but no accepted autoimmune comparator route yet. | Release only if source/data review confirms specificity controls or scoreable comparator data. |

## Decision

These candidates are worth preserving for future source review, but none should
be used in the V50 convergence/contradiction count.
