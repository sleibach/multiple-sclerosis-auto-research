# Source Coverage And Maintenance Map

This page explains where newcomer material gets its authority. It is a
traceability map, not an additional evidence layer. Repeating a source across
many pages does not strengthen the underlying result or change its grade.
`[E01]`

## Coverage Result

Run:

```bash
python3 scripts/v55_source_coverage.py --fail-on-error
```

Current result: `PASS`.

| measure | result |
|---|---:|
| Reader-facing pages mapped | 43 |
| Bounded claim rows | 33 |
| Claim rows referenced by at least one reader page | 33 |
| Unique controlling artifacts | 33 |
| Controlling artifacts present | 33 |
| Missing reader pages | 0 |
| Missing controlling artifacts | 0 |

The machine-readable graph is under `analysis/v55_source_coverage/`:

- `claim_coverage.tsv` maps each claim ID to reader pages;
- `artifact_coverage.tsv` maps every controlling artifact to claims and pages;
- `document_coverage.tsv` shows the claim, source, and status breadth of each
  reader page; and
- `source_coverage_summary.json` records completeness and source groups.

## Why Page Coverage Differs

Different pages intentionally carry different evidence loads:

| page | bounded claims | controlling artifacts | purpose |
|---|---:|---:|---|
| Landing page | 3 | 4 | Fast orientation and the candid bottom line. |
| Collaborator brief | 31 | 32 | One-page status, open puzzles, shortcuts, and usable-idea anatomy. |
| Layered explanation | 30 | 28 | Broad account of the project arc and frontier. |
| FAQ | 29 | 28 | Direct answers to likely scope and evidence questions. |
| Failure-mode atlas | 25 | 26 | Why routes failed and what evidence could change each blocker. |
| Data-needed map | 20 | 21 | Minimum decisive packages and non-substitutable near-matches. |
| Research-evolution timeline | 31 | 31 | Promotions, bounds, demotions, nulls, and the present frontier in sequence. |
| Repository tour | 15 | 16 | Storage, authority, lifecycle, and safe navigation by evidence role. |
| Nulls and boundaries explainer | 19 | 21 | Decision differences among negative, closed, mixed, attenuated, inconclusive, invalid, and data-blocked outcomes. |
| Numbers-without-overreading guide | 9 | 9 | Effect, uncertainty, AUC, null tests, multiplicity, validation level, and project examples without threshold-to-truth upgrades. |
| Brain-bank confounding case study | 2 | 2 | How source-diagnosis entanglement narrowed one interpretation and changed the next study design. |
| Worked submission lifecycle | 2 | 2 | Fictional intake, repair, freeze, and five interpretation branches built around the real source-confound lesson. |
| Genetics-reversal case study | 3 | 4 | Why regional association, causal gene, protective direction, and workable modality are separate target gates. |
| Monitor-versus-target case study | 9 | 11 | Why an associated early-treatment readout and a causal intervention require different evidence ladders. |
| Progression snapshot-versus-movie case study | 9 | 10 | Why snapshots and partial longitudinal designs cannot identify molecular-to-confirmed-disability progression. |
| Confound-check quick reference | 3 | 3 | Detection, adjustment, interpretation, and fail-closed checks for source and immune-state alternatives. |
| Four-case learning path | 17 | 18 | Sequenced lessons on confounding, genetics-to-target, monitor-to-intervention, and snapshot-to-progression errors. |
| Collaborator workshop guide | 6 | 7 | A privacy-safe path from outsider observation through independent generation, boundary filtering, adversarial review, and issue submission. |
| Outside-context-to-test case study | 4 | 6 | How literature, database, and model context becomes a falsifiable future test without authority transfer. |
| Open-problem board | 26 | 25 | Boundaries, prior work, and useful next inputs. |
| Lead status cards | 26 | 25 | Route-by-route current status. |
| Visual text equivalents | 31 | 30 | Accessible linear equivalents for eight diagrams. |
| Glossary | 25 | 26 | Definitions that retain project-specific scope. |
| Worked transformations | 21 | 23 | Design examples tied to known errors and closures. |
| Myths versus findings | 27 | 26 | Common overreads corrected against source claims. |
| Contribution guide | 10 | 11 | Submission discipline rather than a scientific summary. |
| Contributor response lifecycle | 13 | 15 | Intake, hard gates, repair, action classes, grounding outcomes, and public closure without proposal promotion. |
| Review-response templates | 10 | 11 | Exact non-personal language for workflow actions and eligible grounded-result classes. |
| Status decoder | 22 | 22 | Separate workflow, test-validity, and evidence labels with allowed and forbidden transitions. |
| Known non-solutions | 31 | 30 | Searchable tested shortcuts paired with failure reasons and exact reopening evidence. |
| Question starters by discipline | 29 | 29 | Fifty-five prompts translate ten kinds of expertise into bounded, falsifiable contribution directions. |
| First idea in ten minutes | 28 | 29 | Timed path from one observation to data, rival explanation, fair challenge, drop rule, and decision. |
| Public issue examples | 12 | 14 | Fictional ready, repairable, duplicate/closed, and unsafe issue forms with bounded review responses. |
| Challenge the project | 22 | 20 | Adversarial claim, confound, independence, null, direction, closure, coverage, decision, and reproducibility countertests. |
| Contribute a data source | 23 | 24 | Role-specific eligibility, access, independent-unit, field, privacy, and honest status checks for cohort leads. |
| Contribute a method | 16 | 19 | Fixed estimand, fair baseline, independent unit, null, leakage, uncertainty, multiplicity, and drop-rule requirements for analytical proposals. |
| Contribute documentation or a visual | 16 | 17 | Meaning contract, bounded rewrites, status-aware visual semantics, accessibility, delivery, and comprehension checks. |
| Patient and public safety | 10 | 10 | No-medical-advice, no-personal-data boundary, privacy-safe alternatives, and maintainer response. |
| Find by term | 30 | 30 | Search-term and misconception route to bounded status, forbidden inference, and source-backed explanation. |
| V55 release notes | 25 | 23 | Public summary of the unchanged scientific state, added onboarding routes, checks, and human-test gap. |
| Invite collaborators | 26 | 25 | Shareable honest frontier, useful skill types, six puzzles, test-card anatomy, review outcomes, and safety boundary. |
| Starter contributions | 15 | 20 | Twelve bounded first tasks with expected output, completion criterion, evidence status, and non-solution. |
| Collaborator routes | 7 | 9 | Role-specific entry points, deliberately concise. |

The landing page is not a substitute for the layered explanation. The claim
count makes that visible rather than letting a short summary appear complete.

## Most Reused Controlling Artifacts

The most reused record, `docs/reports/THERAPEUTIC_PATH_V52.md`, serves 40 of
the 43 reader pages and controls six live-lead, closed-direction, and
next-impact claims.

`docs/history/V54_RUN_SUMMARY.md` serves 39 pages and controls eight
progression, monitoring/target-boundary, and model-use claims.

`docs/reports/FINDINGS_REPORT_V37.md` serves 37 pages and controls eight
context, decoupling, closure, and governance claims.

`docs/findings/FINDING_V22.md` serves 34 pages;
`docs/history/PROGRESSION_FRONTIER_V54.md` serves 32;
`docs/validation/PREREGISTRATION_V42.md` serves 32.

This is **maintenance centrality**, not scientific importance. A heavily reused
artifact requires a wider communication review when it changes; it does not
gain evidentiary weight from being cited repeatedly.

## Source-Type Balance

The 33 controlling artifacts comprise:

| source group | artifacts |
|---|---:|
| Validation documents | 9 |
| History/run records | 7 |
| Workups | 5 |
| Analysis outputs | 5 |
| Findings | 2 |
| Reports | 2 |
| Knowledge governance | 1 |
| Locked rules | 1 |
| Outside-context governance | 1 |

The outside-context item governs separation; it does not supply biological
evidence. `[E02]`

## Maintenance Procedure

When a controlling artifact changes:

1. Review the affected row in `ONBOARDING_CLAIM_SOURCES_V55.tsv` first.
2. Change its plain-language statement, status, allowed scope, or forbidden
   overread only if the authoritative evidence actually changed.
3. Use `artifact_coverage.tsv` to find every affected reader page.
4. Update all affected wording while preserving page depth and purpose.
5. Run the onboarding, plain-language, provenance, structure, and browser
   checks before merging.

When a page changes without an evidence change, its claim IDs should remain
the same. If new scientific content cannot map to a bounded claim row, it does
not belong in onboarding until the source contract is updated from an
authoritative project artifact.

## Limits

- The graph checks presence and relationships, not whether prose faithfully
  paraphrases every nuance. Human source review still matters.
- A claim ID on a page does not make every nearby sentence correct.
- Source count is not evidence grade, novelty, effect size, or replication.
- The graph cannot substitute for independent validation of provisional work.

Continue with the [claim-source contract](CLAIM_SOURCE_MATRIX_V55.md) or the
[final drift and safety review](FINAL_DRIFT_AND_SAFETY_REVIEW_V55.md).
