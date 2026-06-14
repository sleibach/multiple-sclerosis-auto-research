# V49 Content Handoff

Status: synthesis/navigation only. This handoff summarizes the V49 external
knowledge-layer content after the repository hygiene fix. It does not add
evidence, change grounded findings, alter locked rules, or modify
pre-registrations.

Boundary: project artifacts remain the evidence. V49 external-layer outputs
only classify source-context relationships, future intake routes, validation
readiness routing, and closure guardrails.

## What V49 Changed

| area | V49 result | artifact | practical consequence |
|---|---|---|---|
| Oversized Git history | Tracked large tmp/cache/generated files were purged from history; ignore rules now block recurrence. | `.gitignore`, `meta/V49_QUEUE.md` | Repo is pushable after the human re-adds `origin`, force-pushes rewritten `main`, and re-syncs clones. |
| Purged-path references | Remaining references to purged paths were audited. They are historical provenance or live historical-script rerun dependencies, not push blockers. | `meta/V49_PURGED_ARTIFACT_REFERENCE_AUDIT.md` | Old V3 scripts that name purged caches need regenerated local inputs before rerun; old reports were not rewritten. |
| High-priority convergence gaps | The `11` V48 high-priority gaps were closed; matrix now has `23` relationship rows: `7` corroboration-context, `0` contradiction, `16` insufficient-overlap/context. | `V49_RELATIONSHIP_DELTA_NOTE.md`; `CONVERGENCE_CONTRADICTION_V48.md` | The external layer is no longer mostly skeleton for high-priority findings. |
| Validation-facing rows | `7` validation-facing/high-actionability rows were crosschecked; `2` primary V22 rows are already covered by V42/V44, `2` secondary rows by V44, and `3` require source-specific import instead of validation harness work. | `V49_VALIDATION_READY_ROW_CROSSCHECK.md` | No new validation-harness work is needed now; wait for blind data or run source-intake packets. |
| Source-specific import routes | Three narrow future intake packets were defined: ZMIZ1 direction, chr1 KIF21B/GPR25 signal, and coupled APC-axis records. | `V49_SOURCE_SPECIFIC_IMPORT_PACKETS.md` | Future source intake must be signal-specific and direction-preserving where relevant; broad database presence is insufficient. |
| Context-only closures | Seven low-actionability rows now have explicit do-not-reopen rules and minimum reopen triggers. | `V49_CONTEXT_ONLY_CLOSURE_GUARDRAIL.md` | Future sessions should not reopen broad context rows without the named narrow data trigger. |
| Source-domain/access review | Eight V49-added source domains were reviewed; none need parking for current metadata-only use, but Annual Reviews requires parking before fuller reuse and PMC rows need source-specific terms review before table/figure reuse. | `V49_NEW_SOURCE_DOMAIN_REVIEW.md` | Current use is safe; deeper source extraction has named terms/access prerequisites. |

## What V49 Did Not Change

- No grounded biological finding was revised.
- No contradiction was asserted against a grounded finding.
- No locked rule, validation threshold, or pre-registration was edited.
- No external source was treated as project evidence.
- No source-context row was promoted to validation.

## Decision-Relevant Takeaways

1. The strongest V49 content gain is not a new result; it is cleaner external
   relationship classification. The high-priority gaps now have either
   corroboration context, insufficient-overlap closure, validation routing, or a
   specific import packet.
2. The V22 validation path remains mechanically ready. V49 confirmed that the
   validation-facing rows are already covered by V42/V44 and require data, not
   new harness design.
3. Several tempting external-context rows should stay closed. EBV risk does not
   rescue the EBV/IFN APC imprint, GPR25 nomination does not undo demotion, and
   general treatment-transfer or biomarker-context sources do not reopen killed
   rules.
4. The zero-contradiction count should be interpreted narrowly. It means no
   imported record directly contradicted a project finding under the V48/V49
   rules; it does not mean external consensus exists.

## Open Actions To Carry Forward

| priority | action | source artifact | blocker or next input |
|---|---|---|---|
| high | Run frozen primary V22 validation when blind paired DMF/NEDA or equivalent data arrive. | `V49_VALIDATION_READY_ROW_CROSSCHECK.md` | Validation cohort, labels, module coverage, metadata. |
| high | Use the ZMIZ1 source-specific import packet before any future ZMIZ1 external comparison. | `V49_SOURCE_SPECIFIC_IMPORT_PACKETS.md` | ZMIZ1-specific source records with direction/effect or a route to recover it. |
| high | Use the chr1 KIF21B/GPR25 import packet before any future locus comparison. | `V49_SOURCE_SPECIFIC_IMPORT_PACKETS.md` | Signal-specific association/fine-mapping/QTL records preserving direction fields. |
| medium | Use the coupled APC-axis import packet before comparing MSGD or other resources to V26 architecture. | `V49_SOURCE_SPECIFIC_IMPORT_PACKETS.md` | Source-specific CD74/MIF/HLA/IFN-APC or APC-axis records. |
| medium | Keep low-actionability rows closed unless their named trigger appears. | `V49_CONTEXT_ONLY_CLOSURE_GUARDRAIL.md` | Narrow row-specific data trigger. |
| medium | Review Annual Reviews access/terms before any full-text or detailed-method extraction from that row. | `V49_NEW_SOURCE_DOMAIN_REVIEW.md` | Human/source-terms review if deeper reuse is needed. |

## Reader Route

Use this order when resuming V49/V50 external-knowledge work:

1. `meta/V49_REWRITE_PUSH_HANDOFF.md` for the required rewritten-history push.
2. `meta/V49_PURGED_ARTIFACT_REFERENCE_AUDIT.md` for post-purge rerun boundaries.
3. `V49_RELATIONSHIP_DELTA_NOTE.md` for what changed.
4. `V49_VALIDATION_READY_ROW_CROSSCHECK.md` for validation routing.
5. `V49_SOURCE_SPECIFIC_IMPORT_PACKETS.md` for future source intake.
6. `V49_CONTEXT_ONLY_CLOSURE_GUARDRAIL.md` for rows that should stay closed.
7. `V49_NEW_SOURCE_DOMAIN_REVIEW.md` before deeper reuse of V49-added sources.
