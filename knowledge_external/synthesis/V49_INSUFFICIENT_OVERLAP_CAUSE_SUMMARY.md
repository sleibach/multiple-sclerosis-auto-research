# V49 Insufficient-Overlap Cause Summary

Status: external-layer synthesis; source:
`knowledge_external/synthesis/convergence_contradiction_v48.tsv`. This file is
classed as external context and does not alter any grounded finding.

Purpose: close the interpretive ambiguity around the `16` relationship rows
classified as `insufficient-overlap` in
`knowledge_external/synthesis/convergence_contradiction_v48.tsv`. These are not
open high-priority gaps. They are closed relationship assessments where the
external source does not directly corroborate or contradict the grounded
finding.

## Cause Counts

| insufficient-overlap cause | rows | meaning |
|---|---:|---|
| `NO_DIRECT_EXTERNAL_CORROBORATION` | `11` | The external source is relevant context but does not assert, test, or refute the project-specific finding. |
| `GENERAL_CONTEXT_NOT_LOCUS_CORROBORATION` | `3` | The source supports a broad framing but not the specific locus, direction, layer, or mechanism. |
| `RESOURCE_CAN_QUEUE_FUTURE_CHECK` | `2` | The external resource may contain relevant records, but the current resource-level metadata is not itself a source-specific claim. |

Operational interpretation: none of these `16` rows should be treated as
contradictions, and none should be upgraded to corroboration without a future
source-specific import or real-data grounding step. They remain useful because
they identify exactly what kind of evidence would be needed to change the
relationship class.

## Row-Level Closure

| grounded finding | cause | future trigger |
|---|---|---|
| Bounded APC/HLA-II early treatment-response monitoring scalar | `NO_DIRECT_EXTERNAL_CORROBORATION` | Validate with the frozen V42/V44 harness on a paired labeled DMF cohort; do not use label context as validation. |
| V22 scalar is immune-tone bounded, not steroid/composition artifact | `NO_DIRECT_EXTERNAL_CORROBORATION` | Use the V42/V44 confounder and batch diagnostics when real validation data arrive. |
| Coupled APC remodeling architecture | `NO_DIRECT_EXTERNAL_CORROBORATION` | Import specific CD74, MIF, HLA, and APC-axis external records only as segregated future-grounding context before comparing them to V26. |
| T/B-readable early IFN/APC/STAT1 monitoring state | `NO_DIRECT_EXTERNAL_CORROBORATION` | Ground only in paired response data with compartment-resolved or deconvolved readouts. |
| Postpartum HLA-II/CD64 APC-arm imbalance | `NO_DIRECT_EXTERNAL_CORROBORATION` | Acquire true postpartum MS immune trajectory data with relapse-window timing. |
| ZMIZ1 opposite-direction MS/Crohn decoupling | `RESOURCE_CAN_QUEUE_FUTURE_CHECK` | Create a future-grounding task only after importing specific ZMIZ1 records with source snapshots and hashes. |
| chr1 KIF21B/GPR25 locus resolves to real biology but hard target | `RESOURCE_CAN_QUEUE_FUTURE_CHECK` | Import specific GWAS Catalog associations only as future-grounding records before comparison. |
| PTGER4 mixed shared/distinct signal closes naive transfer | `GENERAL_CONTEXT_NOT_LOCUS_CORROBORATION` | Leave PTGER4 closed unless signal-specific external data are imported and grounded. |
| No validated broad immune-state simulator from held data | `NO_DIRECT_EXTERNAL_CORROBORATION` | Do not reopen simulator claims without a held-out perturbation dataset and frozen split. |
| Coupled-axis successor rule does not beat scalar | `NO_DIRECT_EXTERNAL_CORROBORATION` | Keep V27 negative-established unless a future external cohort is tested with the frozen scalar and any pre-locked successor under a preregistered comparison. |
| Locked V7 general cross-disease baseline fallback killed | `NO_DIRECT_EXTERNAL_CORROBORATION` | Keep the V7 fallback killed unless a predefined external dataset directly tests the baseline-fallback rule. |
| Crohn downstream IFN/APC convergence exceeds genetic proximity | `GENERAL_CONTEXT_NOT_LOCUS_CORROBORATION` | Import or acquire Crohn response datasets before using Crohn as a downstream response-monitoring comparator. |
| RA pregnancy comparator but blood APC treatment-response nontransfer | `NO_DIRECT_EXTERNAL_CORROBORATION` | Use RA pregnancy data only for pregnancy-timing hypotheses unless paired MS treatment-response data directly test transfer. |
| EBV/IFN APC imprint downgraded by specificity control | `NO_DIRECT_EXTERNAL_CORROBORATION` | Reopen only with EBV-stratified expression data and predefined specificity controls. |
| GPR25 demoted from protected favorite | `GENERAL_CONTEXT_NOT_LOCUS_CORROBORATION` | Keep GPR25 demoted unless signal-specific direction and tractability evidence is imported and grounded. |
| No load-bearing invariant found in V26 | `NO_DIRECT_EXTERNAL_CORROBORATION` | Do not promote an invariant unless it passes the project's cross-modality null-tested invariant gate. |

## Decision Rule

Future sessions should not reopen an insufficient-overlap row merely because an
external source is thematically related. Reclassification requires one of:

- a source-specific external record that directly matches the grounded finding's
  locus, mechanism, direction, disease layer, or prediction;
- a new rerunnable grounding analysis under the project's evidence gate;
- a true contradiction, explicitly tagged as a tension and queued for grounding
  rather than accepted as overriding evidence.
