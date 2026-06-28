# V50 Remaining Source Search Packet

Status: future search/navigation only. This packet defines narrow search routes
for the remaining V50 rows that still lack same-definition external records. It
does not add evidence, assert convergence, or create a contradiction.

Primary sources:

- `knowledge_external/synthesis/V50_INSUFFICIENT_OVERLAP_DIAGNOSIS.md`
- `knowledge_external/synthesis/CONVERGENCE_CONTRADICTION_V50.md`
- `knowledge_external/synthesis/V50_ZERO_CONTRADICTION_SPECIFICITY_AUDIT.md`

## Scope

Do not broaden this into generic MS literature searching. The remaining useful
source search is narrow:

1. T/B-readable early IFN/APC/STAT1 monitoring state.
2. EBV/IFN APC imprint specificity against autoimmune comparators.

Broad disease-course, drug-label, or EBV-risk sources are not sufficient. They
were already shown to produce insufficient overlap.

## Search Packet A: T/B-Readable Early IFN/APC/STAT1 Monitoring State

Minimum acceptable source:

- MS treatment-response or relapse-response transcriptomic or single-cell data;
- compartment-resolved, sorted-cell, single-cell, or deconvolution-readable T,
  B, and APC/monocyte/myeloid signals;
- early timepoint after therapy or acute treatment;
- IFN/APC/STAT1/HLA-II readout reported or raw data accessible;
- response or clinical-state label sufficient to compare module behavior.

Suggested queries:

| route | query |
|---|---|
| PubMed / Europe PMC | `"multiple sclerosis" "treatment response" "STAT1" "B cells" transcriptome` |
| PubMed / Europe PMC | `"multiple sclerosis" "interferon" "HLA" "B cells" "treatment response"` |
| PubMed / Europe PMC | `"multiple sclerosis" "single-cell" "treatment response" "interferon" "B cell"` |
| GEO / OmicsDI | `"multiple sclerosis" "treatment response" "CD19" "CD4" expression` |
| GEO / OmicsDI | `"multiple sclerosis" "early treatment" "PBMC" "STAT1"` |
| Supplement mining | `"multiple sclerosis" "baseline" "on-treatment" "B cell" "RNA-seq"` |

Reject source hits if:

- they report only a drug mechanism label;
- they are not MS or not treatment/relapse response;
- they contain no compartment-readable data;
- they do not include IFN/APC/STAT1/HLA-II readouts or raw data from which those
  can be scored;
- they have no timing or response/state label.

## Search Packet B: EBV/IFN APC Imprint Specificity

Minimum acceptable source:

- EBV-stratified or EBV-reactive immune expression data;
- MS plus controls and at least one non-MS autoimmune comparator, or a design
  that can test autoimmune specificity directly;
- APC/IFN/HLA-II or B-cell antigen-presentation readouts;
- raw or module-scoreable expression data, or explicit same-definition
  comparison;
- sufficient metadata to avoid collapsing EBV relevance into MS specificity.

Suggested queries:

| route | query |
|---|---|
| PubMed / Europe PMC | `"EBV" "multiple sclerosis" "autoimmune comparator" "interferon" transcriptome` |
| PubMed / Europe PMC | `"EBV" "multiple sclerosis" "B cell" "antigen presentation" "single-cell"` |
| PubMed / Europe PMC | `"EBNA1" "multiple sclerosis" "systemic lupus" "interferon"` |
| GEO / OmicsDI | `"EBV" "multiple sclerosis" "RNA-seq" "autoimmune"` |
| GEO / OmicsDI | `"EBV" "B cell" "multiple sclerosis" "single cell"` |
| Supplement mining | `"GlialCAM" "EBNA1" "transcriptome" "autoimmune"` |

Reject source hits if:

- they establish EBV risk only, without expression/state data;
- they lack non-MS autoimmune specificity controls;
- they report molecular mimicry without APC/IFN expression readouts;
- they are preprints without usable data and no clear source status;
- they cannot distinguish MS specificity from general autoimmune or antiviral
  immune activation.

## Acceptance Checklist For Any Hit

Before creating a new external record or relationship row:

1. Record source URL, citation, date accessed, and source terms status.
2. State the exact grounded finding the source could test.
3. State whether the source is a same-definition test, a partial overlap, or
   context only.
4. If it appears to contradict a grounded finding, route through
   `knowledge_external/synthesis/V50_ZERO_CONTRADICTION_SPECIFICITY_AUDIT.md`
   before adding any contradiction row.
5. If it is groundable on data, route it to a future grounding queue rather than
   treating the source as evidence.

## Decision

This packet keeps the next external search narrow enough to be useful. The
remaining rows should not be reopened by generic EBV-risk, drug-label, or broad
MS biomarker sources.
