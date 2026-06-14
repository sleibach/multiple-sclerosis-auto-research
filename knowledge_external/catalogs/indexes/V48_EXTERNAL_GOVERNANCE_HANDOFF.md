# V48 External-Governance Handoff

Status: external-knowledge governance/navigation only. This handoff is not biological evidence and does not change any grounded finding, locked rule, or pre-registration.

## Current State

- External records: `39`.
- Direct V48 external convergences with grounded findings: `2`.
- V48 external contradictions flagged: `0`.
- V37 scored findings covered by direct external convergence: `2` of `32`.
- V37 scored findings with context-only external rows: `10` of `32`.
- V37 scored findings without a V48 external relationship row: `20` of `32`.
- Source-terms metadata present: `8` of `39`; missing terms remain optional review targets, not failures.
- Governance preflight: `20` checks, `0` failures at the latest V48 run.

## Required Command

Run this after any external record, external synthesis, external index, or V48 governance script changes:

```bash
.venv_v3_py312/bin/python scripts/v48_governance_preflight.py
```

Then run the provenance gate directly after preflight output generation:

```bash
.venv_v3_py312/bin/python scripts/v47_provenance_gate.py audit
```

Both must pass before committing.

## Navigation

| artifact | purpose |
|---|---|
| `knowledge_external/INDEX.md` | Public external-layer navigation entrypoint. |
| `knowledge_external/synthesis/CONVERGENCE_CONTRADICTION_V48.md` | Populated V48 relationship analysis. |
| `knowledge_external/synthesis/V37_FINDING_EXTERNAL_COVERAGE_V48.md` | V37 scored-finding coverage against V48 external relationship rows. |
| `knowledge_external/catalogs/indexes/V48_GOVERNANCE_NAVIGATION.md` | Generated list of governance controls and latest summaries. |
| `knowledge_external/catalogs/indexes/SOURCE_TERMS_COVERAGE_V48.md` | Source-terms metadata coverage and conservative reuse notes. |
| `knowledge_external/synthesis/FUTURE_GROUNDING_QUEUE_V48.md` | Future grounding tasks from V48 relationship rows. |

## Boundary Rules

- Grounded project artifacts remain the evidence.
- External convergence is corroborating context, not evidence.
- External contradiction is a tension flag and future-grounding task, not an override.
- External records and generated external syntheses stay under `knowledge_external/`.
- Generated JSON summaries belong under `knowledge_external/catalogs/indexes/`, not directly under `knowledge_external/synthesis/`, so the provenance gate does not misclassify them as live records.
- `knowledge/.index` intentionally does not ingest `knowledge_external`; the external layer has its own navigation index.

## When Adding External Knowledge

1. Add or update the live external record under `knowledge_external/records/` or `knowledge_external/catalogs/resources/`.
2. Ensure every record has source, epistemic class, relationship tag, date accessed, and `NOT_PROJECT_GROUNDED`.
3. Regenerate affected indexes or syntheses.
4. Run `scripts/v48_governance_preflight.py`.
5. Run `scripts/v47_provenance_gate.py audit`.
6. Commit only after both pass.

## Known Gaps

- Most records still lack explicit `source_terms`; this is tracked as optional coverage, not a blocker.
- No external contradiction records are live yet; use `knowledge_external/templates/contradiction_intake_template.json.template` if one is added.
- V48 has not tried to force an external relationship for every V37 finding; no-overlap rows are intentionally recorded as absence of linked context, not as a negative biological result.
