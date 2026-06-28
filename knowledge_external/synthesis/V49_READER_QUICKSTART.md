# V49/V50 Reader Quickstart

Status: navigation only. This quickstart routes common V49/V50 questions to the
right artifact. It does not add evidence or change any finding.

## Start Here

| question | read this first | why |
|---|---|---|
| What did V49 change overall? | `V49_CONTENT_HANDOFF.md` | Compact handoff across hygiene, gap closure, validation routing, import packets, closures, and source terms. |
| Is the repo pushable now? | `meta/V49_REWRITE_PUSH_HANDOFF.md` | Records the history rewrite, remote removal, force-push step, and clone re-sync commands. |
| Why do old V3 files still reference purged paths? | `meta/V49_PURGED_ARTIFACT_REFERENCE_AUDIT.md` | Separates historical provenance references from live rerun dependencies after large-cache purge. |
| Where is the populated convergence/contradiction matrix? | `knowledge_external/synthesis/CONVERGENCE_CONTRADICTION_V48.md`; pointer: `docs/knowledge/CONVERGENCE_CONTRADICTION_V48.md` | The substantive rows stay in the segregated external tree; the docs pointer provides public routing and V49 counts without duplicating external claims into grounded trees. |
| Did V49 fully close the 11 high-priority gaps? | `V49_GAP_CLOSURE_COMPLETENESS_AUDIT.md` | Direct TSV-derived audit: 11 high-priority gaps became 0, with 5 new corroboration-context rows and 6 insufficient-overlap closures. |
| Do all relationship rows carry required provenance? | `V49_RELATIONSHIP_PROVENANCE_AUDIT.md` | Row-level audit showing all 23 relationship rows carry grounded artifact, source, class, marker, relationship class, and row-status fields. |
| Which corroborations are strongest? | `V49_CORROBORATION_STRENGTH_TIERS.md` | Tiers the 7 convergence rows so source-specific biological context is not conflated with method/governance context or overcounted shared-source rows. |
| Which V48 convergence gaps were closed? | `V49_RELATIONSHIP_DELTA_NOTE.md` | Summarizes the matrix delta and decision-relevant interpretation. |
| Which external agreements count as independent source clusters? | `V49_SOURCE_INDEPENDENCE_DELTA.md` | Prevents counting `7` rows as `7` independent corroborations; the correct source-cluster count is `5`. |
| Are there contradictions? | `V49_ZERO_CONTRADICTION_CAVEAT.md` | Explains why `0` current contradiction rows is not the same thing as consensus. |
| Which future contradictions should be watched? | `V49_CONTRADICTION_SURVEILLANCE_SHORTLIST.md` | Lists the rows where same-definition future sources could create real tension. |
| If a future contradiction appears, where does it route? | `V49_CONTRADICTION_ROUTING_AUDIT.md` | Confirms every surveillance row has a future-grounding route and safe non-overriding action. |
| What exact evidence would make a future contradiction real? | `V49_CONTRADICTION_EVIDENCE_TYPES.md` | Defines required evidence types, minimum fields, and non-triggers for the 7 surveillance rows. |
| Is the V22 validation path already covered? | `V49_VALIDATION_READY_ROW_CROSSCHECK.md` | Shows the primary V22 and confounder/batch guardrails are covered by V42/V44. |
| Which rows need source-specific intake? | `V49_SOURCE_SPECIFIC_IMPORT_PACKETS.md` | Defines acceptance gates for ZMIZ1, chr1 KIF21B/GPR25, and coupled APC-axis records. |
| How do those import packets relate to the future-grounding queue? | `V49_IMPORT_PACKET_QUEUE_RECONCILIATION.md` | Maps broad generated queue rows to stricter V49 field gates. |
| Which rows should stay closed unless a narrow trigger appears? | `V49_CONTEXT_ONLY_CLOSURE_GUARDRAIL.md` | Prevents broad context sources from reopening seven low-actionability rows. |
| Why are the 16 insufficient-overlap rows closed rather than unresolved? | `V49_INSUFFICIENT_OVERLAP_CAUSE_SUMMARY.md` | Groups the 16 rows into no-direct-corroboration, general-context-not-signal-specific, and resource-can-queue-future-check causes with concrete future triggers. |
| Did V49 change the comparator matrix? | `V49_COMPARATOR_MATRIX_REVIEW.md` | Shows no new resource-level comparator rows are warranted from V49 source domains. |
| Which resource candidates are still absent? | `V49_ABSENT_RESOURCE_INTAKE_CANDIDATES.md` | Lists future metadata-only intake candidates with acceptance gates. |
| Are absent resources safe to use now? | `V49_ABSENT_RESOURCE_ROUTING_AUDIT.md` | Confirms candidate resources are metadata-only, require source-terms review, and are not usable validation data yet. |
| What are the source-terms follow-ups? | `V49_SOURCE_TERMS_FOLLOWUP.md` | Separates metadata-only current use from fuller-reuse terms/access review. |
| What happened to the V48 unresolved handoff? | `V49_UNRESOLVED_ACTION_RECONCILIATION.md` | Marks V48 rows as covered, narrowed, closed-unless-triggered, or unchanged after V49. |

## V50 Sharper-Source Routing

| question | read this first | why |
|---|---|---|
| What did V50 add beyond V49? | `V50_CONTENT_HANDOFF.md` | Compact handoff for the V50 source-specific corroborations, non-corroborations, and zero-contradiction caveat. |
| Which V49 insufficient-overlap rows were worth sharpening? | `V50_INSUFFICIENT_OVERLAP_DIAGNOSIS.md` | Diagnoses the 16 insufficient-overlap rows by source-specificity gap, project-specific novelty, resource-metadata limitation, or context-only status. |
| What is the updated V50 convergence/contradiction result? | `CONVERGENCE_CONTRADICTION_V50.md` | Reassesses high-priority rows after adding source-specific DMF, ZMIZ1, chr1, coupled APC, EBV, Crohn, and PTGER4 records. |
| Which V50 records are now future grounding tasks? | `FUTURE_GROUNDING_QUEUE_V50.md` | Routes all 18 V50 sharper records into immediate non-OpenGWAS tasks, blocked-data routes, or context-only records. |
| Did V50 validate the locked V22 scalar externally? | `V50_CONTENT_HANDOFF.md`; detail: `CONVERGENCE_CONTRADICTION_V50.md` | No. V50 sharpened DMF validation context but did not find an external source that independently tests the frozen V22 scalar or confounder audit. |
| Which V50 genetics rows are strongest? | `CONVERGENCE_CONTRADICTION_V50.md` | ZMIZ1 opposite-direction and PTGER4 transfer-caution rows now have source-specific GWAS Catalog support; future allele-harmonized reruns remain separate tasks. |
| What is safe to run while OpenGWAS is expired? | `FUTURE_GROUNDING_QUEUE_V50.md` | Lists three immediate non-OpenGWAS routes based on public GWAS Catalog records, and blocks OpenGWAS-dependent refresh until renewal. |

## Minimal Resume Path

If resuming V49/V50 with little context, read in this order:

1. `meta/V50_QUEUE.md`
2. `knowledge_external/synthesis/V50_CONTENT_HANDOFF.md`
3. `knowledge_external/synthesis/CONVERGENCE_CONTRADICTION_V50.md`
4. `knowledge_external/synthesis/FUTURE_GROUNDING_QUEUE_V50.md`
5. `knowledge_external/synthesis/V50_INSUFFICIENT_OVERLAP_DIAGNOSIS.md`
6. `knowledge_external/synthesis/V49_CONTENT_HANDOFF.md`
7. `knowledge_external/synthesis/V49_UNRESOLVED_ACTION_RECONCILIATION.md`
8. `meta/V49_REWRITE_PUSH_HANDOFF.md`
9. `meta/V49_PURGED_ARTIFACT_REFERENCE_AUDIT.md`

## Boundary Reminder

All artifacts named here are navigation, synthesis, source-intake, or queue
controls. They do not convert external source context into project evidence.
Grounded findings remain in the normal project findings/report/history trees.
