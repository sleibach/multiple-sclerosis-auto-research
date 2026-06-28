# V50 Relationship Glossary

Status: class-aware interpretation glossary only. This document does not add
external records, project findings, validation results, or rule changes. It
defines how to read relationship terms used in the V48-V50 external layer.

## Core Rule

Project-grounded artifacts remain the evidence. Segregated external records can
provide context, corroboration, contradiction surveillance, or future-grounding
routes, but they do not become project evidence unless a later committed
analysis tests them on data.

## Relationship Terms

| term | meaning in this repository | what it permits | what it does not permit |
|---|---|---|---|
| `converges` | A segregated external source aligns with a project-grounded finding under a comparable definition. | Treat as independent contextual corroboration; prioritize future grounding if testable. | Do not call it validation or replace the project artifact as evidence. |
| `externally corroborated context` | A convergence row where the external source is specific enough to matter, but still not rerun by the project. | Increase confidence in the grounded finding's plausibility and source relevance. | Do not claim clinical validation, target qualification, or effect-size confirmation. |
| `contradicts` | A source-specific external record disagrees with a project-grounded finding under a comparable definition and evidence type. | Flag a scientific tension and queue a future grounding test where possible. | Do not override the grounded finding just because an external source disagrees. |
| `insufficient overlap` | The external source and project finding do not match closely enough to classify as convergence or contradiction. | Close the row as non-actionable unless a sharper source appears. | Do not treat the absence of overlap as agreement, disagreement, or consensus. |
| `orthogonal` | The source is useful but addresses a different question, data type, or evidence level. | Use for navigation, background, or future source discovery. | Do not use as support for a project result. |
| `context only` | The source sharpens surrounding biology, methods, access, or validation risks but does not test the project claim. | Use to refine search, intake, or diagnostic plans. | Do not count as corroboration of the claim itself. |
| `validation` | A pre-specified project rule is run mechanically on eligible held-out or new data under the locked/pre-registered plan. | Can support a validation verdict if the plan's thresholds are met. | External literature similarity is never validation. |
| `future grounding` | A queued route for later testing an external claim or source-derived hypothesis on data. | Creates an executable task or data request. | Does not establish the claim now. |
| `same-definition trigger` | Minimum fields needed before a source can fairly converge with or contradict a specific project claim. | Prevents over-classifying broad literature as agreement or disagreement. | Does not force a row to become convergence/contradiction if key fields are absent. |
| `source-specific record` | An external record tied to a concrete paper, database row, API extraction, accession, or resource page. | Allows sharper comparison than broad resource metadata. | Still remains external context unless the project reruns/grounds it. |
| `resource metadata` | A catalog entry describing an external resource, registry, archive, or platform. | Helps readers choose where to look next. | Does not support biological claims. |
| `transport status` | Whether a source URL/API route is reachable. | Maintains navigation and route health. | HTTP `200` is not claim validation; HTTP failure is not claim falsification. |
| `no-claim language` | Deliberate wording that states boundaries and avoids turning context into evidence. | Keeps public summaries safe and readable. | Does not weaken the grounded finding; it prevents overstatement. |

## Practical Examples

| reader question | correct interpretation |
|---|---|
| A GWAS Catalog row has the same allele-direction pattern as a project genetics finding. | This is source-specific external corroboration after allele/reporting checks, but project-side harmonization is still needed before direction evidence is grounded. |
| A DMF paper reports PBMC treatment-response biology. | This is validation context for the V22 rule only if it does not apply the frozen scalar, endpoint, and threshold. |
| A steroid or cell-composition source shows those confounders matter in MS. | This strengthens the need for the V32/V42 diagnostic guard; it does not prove the locked V22 scalar survives or fails adjustment in a new cohort. |
| No source contradicts a project result. | This means no same-definition contradiction has been found, not that the literature universally agrees. |
| A registry or catalogue is public-facing. | Public-facing metadata does not mean participant-level data are publicly reusable. |

## Reader Decision Tree

1. Is the claim produced by a committed project analysis?
   - If yes, read the relevant grounded artifact and evidence grade.
   - If no, continue.
2. Is the claim stored under `knowledge_external/` with source and boundary
   labeling?
   - If yes, treat it as external context only.
   - If no, it should not be used.
3. Does the external source match the same definition and evidence type as a
   project finding?
   - If yes, it may be assessed as convergence or contradiction.
   - If no, classify as context, orthogonal, or insufficient overlap.
4. Can the source-derived claim be tested on reachable data?
   - If yes, queue a future grounding route.
   - If no, keep it as context and do not promote it.

## Provenance

This glossary summarizes interpretation rules from:

- `docs/knowledge/EPISTEMIC_CLASSES.md`
- `knowledge_external/synthesis/CONVERGENCE_CONTRADICTION_V48.md`
- `knowledge_external/synthesis/CONVERGENCE_CONTRADICTION_V50.md`
- `knowledge_external/synthesis/V50_V22_V32_CONTRADICTION_TRIGGER_PACKET.md`
- `knowledge_external/synthesis/V50_VALIDATION_CONTEXT_BOUNDARY_CARD.md`
- `knowledge_external/synthesis/V50_NO_CLAIM_LANGUAGE_AUDIT.md`
- `knowledge_external/synthesis/V50_PUBLIC_CITATION_CARD.md`

Date prepared: 2026-06-28.
