# V48 External Layer Reader Brief

Status: class-aware public navigation only. This brief explains how to read the
segregated external-knowledge layer; it does not add external records, assert
new convergence, or change grounded project findings.

## The Short Version

The repository has two different knowledge classes.

- Project-grounded findings are the rerunnable results in the normal project
  report, history, analysis, validation, and locked-rule trees.
- External-layer items are public literature, database, resource, or navigation records stored under `knowledge_external/`. They are explicitly `NOT_PROJECT_GROUNDED` unless a later committed project run grounds them on real data. Source: `docs/knowledge/EPISTEMIC_CLASSES.md`.

The external layer is useful for context, source discovery, and relationship
mapping. It is not evidence for a project conclusion.

## What The External Layer Can Do

- Show which public MS resources, datasets, catalogs, and literature routes
  exist.
- Record external context with source, access date, epistemic class, and the
  not-grounded marker.
- Compare external context against grounded project findings as convergence,
  contradiction, orthogonal context, or insufficient overlap.
- Queue external-verifiable items for future grounding without treating them as findings. Source: `docs/knowledge/EPISTEMIC_CLASSES.md`.
- Help public readers navigate the broader MS knowledge landscape while keeping
  the grounded project core separate.

## What The External Layer Cannot Do

- It cannot validate a project finding.
- It cannot override a grounded project result.
- It cannot modify a locked rule, pre-registration, or validation threshold.
- It cannot promote an external claim into evidence by repetition, citation
  count, model agreement, or source reputation.
- It cannot resolve a contradiction by deferring to an external source. A
  contradiction is a flagged tension and, where possible, a future grounding
  task.

## How To Interpret Convergence

When a segregated external source agrees with a rerunnable grounded finding,
the relationship is recorded as independent corroborating context. The project
artifact remains the evidence. The external agreement can raise confidence that
the grounded finding is aligned with outside knowledge, but it is not itself
proof.

Use:

- `knowledge_external/synthesis/CONVERGENCE_CONTRADICTION_V48.md`
- `knowledge_external/synthesis/CONVERGENCE_SOURCE_INDEPENDENCE_V48.md`
- `knowledge_external/synthesis/DECISION_RELEVANT_CONVERGENCES_V48.md`

## How To Interpret Contradiction

When an external source disagrees with a grounded finding, the relationship is
recorded as a tension. The external source does not override the grounded
finding. The correct response is source-specific overlap review and, if the
claim can be tested with reachable data, a queued future grounding task.

Use:

- `knowledge_external/synthesis/CONTRADICTION_READINESS_PLAYBOOK_V48.md`
- `knowledge_external/synthesis/CONTRADICTION_SURVEILLANCE_CHECKLIST_V48.md`
- `knowledge_external/synthesis/FUTURE_GROUNDING_QUEUE_V48.md`

## How To Intake A New External Source

New sources enter only through segregated external intake. Before any source can
be used in relationship mapping, it needs a source locator, source/access date,
epistemic class, source terms review where applicable, and the explicit
not-grounded marker.

Use:

- `docs/knowledge/EPISTEMIC_CLASSES.md`
- `knowledge_external/templates/HIGH_PRIORITY_SOURCE_INTAKE_CHECKLIST_V48.md`
- `knowledge_external/templates/README.md`
- `scripts/v47_provenance_gate.py`
- `scripts/v48_governance_preflight.py`

## Reader Checklist

Before treating a statement as established, ask:

1. Is it in a grounded project artifact, or only in `knowledge_external/`?
2. If it is external, does it have an epistemic class and source?
3. Is it marked `NOT_PROJECT_GROUNDED`? Source: `docs/knowledge/EPISTEMIC_CLASSES.md`.
4. Is the relationship to project findings convergence, contradiction,
   orthogonal context, or insufficient overlap?
5. If it is external-verifiable, is there a future grounding route? Source: `docs/knowledge/EPISTEMIC_CLASSES.md`.
6. Did the latest provenance/preflight gates pass?

If the answer is unclear, treat the item as context only.

## Boundary

- This brief is a navigation artifact, not biological evidence.
- It does not add new external records.
- It does not change any grounded result, locked rule, or validation plan.
- The provenance gate and governance preflight remain the executable authority
  for whether the external layer is structurally safe to use.
