# V49 Unresolved Action Reconciliation

Status: work-queue/navigation only. This document reconciles the generated
V48 unresolved coverage handoff with V49 content artifacts. It does not edit the
generated handoff, add relationship rows, or change grounded findings.

Boundary: `UNRESOLVED_EXTERNAL_COVERAGE_HANDOFF_V48.md` remains the generated
handoff. This V49 overlay tells future sessions which rows are now covered by a
more specific V49 artifact, narrowed, closed unless a trigger appears, or still
unchanged.

## Summary

- V48 handoff actions reviewed: `23`
- covered by validation/readiness crosscheck: `4`
- narrowed by source-specific import packets: `3`
- closed unless the V49 context-only trigger appears: `7`
- unchanged / keep original V48 action: `9`

## Reconciliation Table

| handoff id | item | V49 status | V49 artifact | next action |
|---|---|---|---|---|
| `V48_HO_001` | MS-UC is strongest tested genome-wide genetics comparator | `unchanged_keep_v48_action` | `FUTURE_GROUNDING_QUEUE_V48.md` | Optional refresh only if summary-statistic inputs are imported and hashed. |
| `V48_HO_002` | Layer-specific autoimmune transfer-validity map | `unchanged_keep_v48_action` | `FUTURE_GROUNDING_QUEUE_V48.md` | Ground specific transfer claims only in predefined patient-level or pharmacovigilance data. |
| `V48_HO_003` | Bounded APC/HLA-II early treatment-response monitoring scalar | `covered_by_validation_crosscheck` | `V49_VALIDATION_READY_ROW_CROSSCHECK.md` | Wait for blind paired validation data and run the frozen V42/V44 harness. |
| `V48_HO_004` | V22 scalar is immune-tone bounded, not steroid/composition artifact | `covered_by_validation_crosscheck` | `V49_VALIDATION_READY_ROW_CROSSCHECK.md` | Apply frozen V42/V44 confounder and batch diagnostics when validation data arrive. |
| `V48_HO_005` | Coupled APC remodeling architecture | `narrowed_by_import_packet` | `V49_SOURCE_SPECIFIC_IMPORT_PACKETS.md`; `V49_IMPORT_PACKET_QUEUE_RECONCILIATION.md` | Use the coupled APC-axis packet before any source comparison to V26. |
| `V48_HO_006` | T/B-readable early IFN/APC/STAT1 monitoring state | `covered_by_secondary_preregistration` | `V49_VALIDATION_READY_ROW_CROSSCHECK.md` | Wait for compartment-resolved paired response data; run the frozen V44 secondary harness. |
| `V48_HO_007` | Postpartum HLA-II/CD64 APC-arm imbalance | `covered_by_secondary_preregistration` | `V49_VALIDATION_READY_ROW_CROSSCHECK.md` | Wait for true MS postpartum trajectory data; run the frozen V44 secondary harness. |
| `V48_HO_008` | ZMIZ1 opposite-direction MS/Crohn decoupling | `narrowed_by_import_packet` | `V49_SOURCE_SPECIFIC_IMPORT_PACKETS.md`; `V49_IMPORT_PACKET_QUEUE_RECONCILIATION.md` | Use the ZMIZ1 direction packet before any source comparison. |
| `V48_HO_009` | chr1 KIF21B/GPR25 locus resolves to real biology but hard target | `narrowed_by_import_packet` | `V49_SOURCE_SPECIFIC_IMPORT_PACKETS.md`; `V49_IMPORT_PACKET_QUEUE_RECONCILIATION.md` | Use the chr1 KIF21B/GPR25 signal packet before any source comparison. |
| `V48_HO_010` | PTGER4 mixed shared/distinct signal closes naive transfer | `closed_unless_trigger_appears` | `V49_CONTEXT_ONLY_CLOSURE_GUARDRAIL.md` | Do not reopen without PTGER4 signal-specific direction and disease-layer data. |
| `V48_HO_011` | No validated broad immune-state simulator from held data | `closed_unless_trigger_appears` | `V49_CONTEXT_ONLY_CLOSURE_GUARDRAIL.md` | Do not reopen without a held-out perturbation/response dataset and frozen split. |
| `V48_HO_012` | Coupled-axis successor rule does not beat scalar | `closed_unless_trigger_appears` | `V49_CONTEXT_ONLY_CLOSURE_GUARDRAIL.md` | Do not reopen without a preregistered external scalar-versus-successor comparison. |
| `V48_HO_013` | Mucosal IBD early IFN/APC downshift validates while baseline fallback fails | `unchanged_keep_v48_action` | `FUTURE_GROUNDING_QUEUE_V48.md` | Optional only if paired mucosal response data are imported under a frozen test. |
| `V48_HO_014` | UC genetics vs treatment-response layer split | `unchanged_keep_v48_action` | `FUTURE_GROUNDING_QUEUE_V48.md` | Use disease-pair and treatment-pair specific data before transfer inference. |
| `V48_HO_015` | First-principles druggability discipline changed target interpretation | `unchanged_keep_v48_action` | `FUTURE_GROUNDING_QUEUE_V48.md` | Continue direction-matched tractability discipline; no new action needed. |
| `V48_HO_016` | Locked V7 general cross-disease baseline fallback killed | `closed_unless_trigger_appears` | `V49_CONTEXT_ONLY_CLOSURE_GUARDRAIL.md` | Do not reopen without a predefined dataset directly testing the killed fallback rule. |
| `V48_HO_017` | Tool-robust but simple V22 scalar | `unchanged_keep_v48_action` | `FUTURE_GROUNDING_QUEUE_V48.md` | Do not add complexity without preregistered external validation advantage. |
| `V48_HO_018` | Crohn downstream IFN/APC convergence exceeds genetic proximity | `unchanged_keep_v48_action` | `V49_INSUFFICIENT_OVERLAP_TRIAGE.md` | Needs Crohn paired response data before use as a monitoring comparator. |
| `V48_HO_019` | RA pregnancy comparator but blood APC treatment-response nontransfer | `closed_unless_trigger_appears` | `V49_CONTEXT_ONLY_CLOSURE_GUARDRAIL.md` | Use pregnancy context only unless paired MS/RA treatment-response transfer data arrive. |
| `V48_HO_020` | EBV/IFN APC imprint downgraded by specificity control | `unchanged_keep_v48_action` | `V49_INSUFFICIENT_OVERLAP_TRIAGE.md`; `V49_CONTRADICTION_SURVEILLANCE_SHORTLIST.md` | Needs EBV-stratified expression plus predefined specificity controls. |
| `V48_HO_021` | GPR25 demoted from protected favorite | `closed_unless_trigger_appears` | `V49_CONTEXT_ONLY_CLOSURE_GUARDRAIL.md` | Do not reopen without signal-specific direction and tractability evidence. |
| `V48_HO_022` | MHC overlap is distinct-signal, not simple shared biology | `unchanged_keep_v48_action` | `FUTURE_GROUNDING_QUEUE_V48.md`; `V49_CONTRADICTION_SURVEILLANCE_SHORTLIST.md` | Continue requiring signal-specific fine-mapping before interpreting shared biology. |
| `V48_HO_023` | No load-bearing invariant found in V26 | `closed_unless_trigger_appears` | `V49_CONTEXT_ONLY_CLOSURE_GUARDRAIL.md` | Do not promote an invariant without a predefined candidate passing cross-modality null tests. |

## Decision

Do not delete or hand-edit the generated V48 handoff. Use this V49 overlay as
the current routing layer. Rows marked covered or narrowed should start from the
named V49 artifact rather than the older broad action sentence.

