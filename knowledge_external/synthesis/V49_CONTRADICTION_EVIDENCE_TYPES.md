# V49 Contradiction Evidence-Type Map

Status: external-layer routing synthesis; source:
`knowledge_external/synthesis/V49_CONTRADICTION_SURVEILLANCE_SHORTLIST.md`.
This file is navigation/control content only and does not alter any grounded
finding.

Purpose: define what exact future source or data type would be required before
a surveillance row could become a real contradiction. The current V49 state
remains `0` contradiction rows.

## Evidence-Type Requirements

| priority | grounded finding | evidence type required for a real contradiction | minimum fields required | non-triggers |
|---:|---|---|---|---|
| 1 | Bounded APC/HLA-II early treatment-response monitoring scalar | Paired baseline/early-treatment response cohort under the frozen V42/V44 harness. | sample IDs, paired timepoints, treatment class, response/NEDA label, module genes, frozen preprocessing route, batch metadata. | DMF mechanism summaries, unpaired cohorts, unlabeled expression, or post-hoc threshold changes. |
| 2 | V22 scalar is immune-tone bounded, not steroid/composition artifact | Direct confounder metadata showing the score's apparent validation is explained away under prespecified diagnostics. | steroid exposure, cell counts or deconvolution inputs, batch fields, paired labels, raw and adjusted V22 results. | General steroid biology, cell-composition plausibility, or missing metadata. |
| 3 | ZMIZ1 opposite-direction MS/Crohn decoupling | Source-specific variant/QTL/disease record preserving allele and effect-direction mapping across MS and Crohn. | variant ID, effect allele, phenotype, effect direction, ancestry/population, mapping to project locus, source snapshot/hash. | gene-only disease association or directionless catalog entries. |
| 4 | chr1 KIF21B/GPR25 locus resolves to real biology but hard target | Signal-specific record showing intervention-favorable direction and tractability for the same locus signal. | variant/signal ID, causal-gene evidence, direction of effect, tractability class, safety/biology rationale, comparison to V19 fields. | broad gene nomination, pathway plausibility, or association without direction. |
| 5 | MHC overlap is distinct-signal, not simple shared biology | Fine-mapping or colocalization source showing the same causal HLA signal under matched variant definition. | credible set or posterior, lead variant mapping, comparator phenotype, LD ancestry, posterior shared-causal evidence. | broad HLA association, same-region overlap, or unmatched ancestry fine-mapping. |
| 6 | EBV/IFN APC imprint downgraded by specificity control | EBV-stratified expression or immune data with predefined MS-vs-autoimmune/control specificity panels. | EBV status/timing, MS/control/comparator labels, APC/IFN readout, specificity-control panel, frozen test definition. | EBV risk epidemiology alone or expression without specificity controls. |
| 7 | No load-bearing invariant found in V26 | Predefined invariant candidate tested across modalities with null/permutation and cross-modality replication. | invariant definition before fitting, modalities included, null model, permutation count, cross-modality holdout result, multiple-testing accounting. | literature plausibility, one-modality recurrence, or model-generated invariant suggestions. |

## Routing Rule

If a future source appears to satisfy a row above, route it through the
segregated source-intake controls first. Then run the named grounding route.
Until that route produces a rerunnable result, the row remains surveillance
only.

## Practical Decision

This map narrows future contradiction handling from "a source disagrees" to
"a source or dataset contains the exact fields needed to test the same claim."
That keeps broad reviews, labels, and directionless databases from being
overread as contradictions.
