# V50 Public Reader Path

Status: class-aware public navigation only. This guide tells a GitHub reader
where to start and how to avoid confusing project-grounded findings with
segregated external knowledge. It adds no external records, biological claims,
or relationship rows.

## If You Land On The GitHub README

Read in this order:

1. `README.md`
   - Purpose: broad project orientation.
   - Caution: the README is a landing page, not the full current state.
2. `meta/CURRENT_STATUS.md`
   - Purpose: live project state and canonical current-frontier narrative.
3. `docs/reports/FINDINGS_REPORT_V37.md`
   - Purpose: scored project findings, including positives, negatives, kills,
     and methodological results.
4. `docs/reports/FINDINGS_SCORES_V37.tsv`
   - Purpose: machine-readable scored findings table.
5. `docs/knowledge/EPISTEMIC_CLASSES.md`
   - Purpose: the rule separating grounded project outputs from external
     context.
6. `knowledge_external/INDEX.md`
   - Purpose: navigation into public external resources, external records,
     convergence/contradiction analyses, and source-routing artifacts.

## What Is Project-Grounded

Treat these areas as the rerunnable project corpus:

- `docs/reports/`
- `docs/findings/`
- `docs/history/`
- `docs/workups/`
- `docs/validation/`
- `docs/locked_rules/`
- `analysis/`
- `scripts/`

Even inside those areas, use the artifact's own evidence grade and limitations.
A provisional result is not a validated finding just because it is grounded.

## What Is External Context

Treat everything under `knowledge_external/` as external context unless a later
grounded project run explicitly tests it. External records and syntheses are
useful for:

- source discovery;
- public-resource comparison;
- convergence/contradiction surveillance;
- future grounding queues;
- provenance and source-terms navigation.

They are not project evidence.

## Quick Questions

| question | first artifact |
|---|---|
| What has the project actually established? | `docs/reports/FINDINGS_REPORT_V37.md` |
| What is the strongest validation lead? | `docs/validation/PREREGISTRATION_V42.md`; `docs/locked_rules/LOCKED_RULE_V22.md`; `docs/workups/treatment_response/CONFOUNDER_AUDIT_V32.md` |
| Is public-data discovery exhausted? | `docs/history/JOINT_INFERENCE_V41.md` |
| What external sources agree or disagree with the project? | `knowledge_external/synthesis/CONVERGENCE_CONTRADICTION_V50.md` |
| Did external sources validate the V22 scalar? | `knowledge_external/synthesis/V50_VALIDATION_CONTEXT_BOUNDARY_CARD.md` |
| Is there a public MS knowledgebase equivalent to this repo? | `knowledge_external/synthesis/V50_PUBLIC_MS_KB_POSITION_CARD.md` |
| What can be run while OpenGWAS is expired? | `knowledge_external/synthesis/V50_NEXT_SOURCE_PRIORITIZATION.md`; `scripts/v50_fetch_gwas_catalog_associations.py` |
| Which future treatment-response source would count as a contradiction? | `knowledge_external/synthesis/V50_V22_V32_CONTRADICTION_TRIGGER_PACKET.md` |

## Interpretation Rules

Use these rules when reading the repository:

1. Grounded project artifacts are the evidence.
2. External records are context, routes, or future-grounding candidates.
3. External convergence raises confidence only as independent context; it is not
   validation.
4. External contradiction raises a flag; it does not override a grounded result.
5. Locked rules and pre-registrations are immutable unless a later artifact
   explicitly says an additive blind tightening was made.
6. Synthetic data tests method behavior only, never MS biology.
7. OpenGWAS-dependent work is disabled while the token is expired.

## Minimal Five-Minute Path

For a new technical reader:

1. Read the V37 executive summary:
   `docs/reports/FINDINGS_REPORT_V37.md`.
2. Read the current validation plan:
   `docs/validation/PREREGISTRATION_V42.md`.
3. Read the external boundary:
   `docs/knowledge/EPISTEMIC_CLASSES.md`.
4. Read the V50 content handoff:
   `knowledge_external/synthesis/V50_CONTENT_HANDOFF.md`.
5. Read the public-source position card:
   `knowledge_external/synthesis/V50_PUBLIC_MS_KB_POSITION_CARD.md`.

That path gives the current project state, the validation lead, and the
grounded/external boundary without requiring the reader to reconstruct V1-V50.

## Decision

Future public-facing summaries should link this path rather than duplicating
external claims in grounded files. If a reader wants source context, send them
to `knowledge_external/`; if they want project evidence, send them to the
grounded reports, workups, locked rules, validation docs, analysis outputs, and
scripts.
