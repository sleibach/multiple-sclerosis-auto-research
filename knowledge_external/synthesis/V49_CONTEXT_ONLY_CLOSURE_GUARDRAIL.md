# V49 Context-Only Closure Guardrail

Status: synthesis/navigation only. This document extracts the low-actionability
rows from `V49_INSUFFICIENT_OVERLAP_TRIAGE.md` so future sessions do not reopen
them just because a broad contextual source exists.

Boundary: these rows remain not corroborated by the paired source. The listed
trigger is the minimum condition for reopening the row; absent that trigger, the
safe action is to leave the grounded project conclusion unchanged.

## Summary

- low-actionability/context-only closures: `7`
- rows with a narrow signal-specific data trigger: `3`
- rows requiring a new frozen/preregistered validation design: `3`
- rows requiring a new null-tested invariant candidate: `1`

## Closure Rules

| grounded finding | closure class | do not reopen for | reopen only if this arrives | why |
|---|---|---|---|---|
| PTGER4 mixed shared/distinct signal closes naive transfer | `closed_unless_signal_specific_data_arrive` | General MS/IBD transfer-caution literature, pathway summaries, or broad target lists. | PTGER4-specific fine-mapping, QTL, or treatment-transfer data with direction and disease-layer definitions that directly address the mixed-signal failure mode. | General treatment-transfer caution is context only; the project already closed naive transfer for this signal. |
| No validated broad immune-state simulator from held data | `closed_unless_new_perturbation_validation_data_arrive` | Curated MS gene/resource databases, simulator enthusiasm, or perturbation-resource metadata. | A held-out perturbation or response dataset plus a frozen split suitable for simulator validation. | Resource metadata cannot repair the held-out simulator validation failure. |
| Coupled-axis successor rule does not beat scalar | `closed_unless_preregistered_external_comparison_arrives` | Treatment labels, mechanism summaries, or in-sample coupled-axis performance. | A preregistered external scalar-versus-successor comparison using the immutable V22 scalar and any pre-locked successor under V27/V42-style rules. | The current project result is negative-established; a treatment label cannot evaluate predictive superiority. |
| Locked V7 general cross-disease baseline fallback killed | `closed_unless_same_failure_mode_dataset_arrives` | Generic prediction-model guidance or broad cross-disease plausibility arguments. | A predefined external dataset directly matching the cross-disease baseline-fallback rule and failure-mode comparison. | General validation guidance supports caution but does not test the specific killed rule. |
| RA pregnancy comparator but blood APC treatment-response nontransfer | `context_only_until_ms_or_ra_response_transfer_data` | RA/SLE pregnancy transcriptome context alone. | Paired MS/RA treatment-response transfer data, not pregnancy timing data alone. | Pregnancy transcriptomes can inform timing hypotheses but do not test blood APC treatment-response transfer. |
| GPR25 demoted from protected favorite | `closed_unless_direction_and_tractability_evidence_arrive` | External nomination of GPR25 as a putative gene or broad locus listing. | GPR25-specific direction, QTL, fine-mapping, and tractability evidence that resolves the V19 demotion reason. | A putative-gene nomination is not direction-matched target evidence. |
| No load-bearing invariant found in V26 | `closed_until_null_tested_invariant_candidate_exists` | General biomarker heterogeneity context or claims that invariants are biologically plausible. | A predefined invariant candidate with cross-modality data sufficient for null/permutation testing. | General heterogeneity context is not an invariant-search replication. |

## Operating Rule

If a future session encounters a source for one of these rows, apply this
decision rule before adding work:

1. Does the source satisfy the row-specific reopen trigger above?
2. Does it preserve direction, cohort, data type, and validation design where
   the trigger requires those details?
3. Can the resulting action be routed through a frozen or pre-specified
   comparison rather than a post-hoc rescue?

If any answer is no, keep the row context-only and do not add a relationship
matrix row or discovery task.

