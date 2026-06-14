# V48 Model-Lens Usage Boundary

Status: governance/navigation only. This card explains how Claude, Gemini, and
RPT may be used in this repository. It is not model output, not biological
evidence, and not a project finding.

## Rule

Models and tabular predictors are proposal lenses only.

- They may propose analyses, critique assumptions, suggest source-search routes,
  or identify possible inconsistencies.
- They may not establish a biological claim.
- They may not validate, weaken, override, or alter a grounded project finding.
- They may not change a locked rule, pre-registration, validation threshold, or
  evidence grade.
- Their output remains external-unverifiable context until a concrete proposal
  is grounded by a committed project analysis.

## Allowed Uses

| lens | allowed use | required follow-up |
|---|---|---|
| Claude | Generate or critique hypotheses, review text for hidden assumptions, propose concrete checks. | Convert proposals into executable project analyses or source-intake tasks. |
| Gemini | Independent critique and second-lineage proposal generation. | Ground any concrete proposal before reporting it as held or failed. |
| RPT | Structured/tabular pattern proposal over already-segregated tables. | Treat surfaced patterns as queue items until checked against real project data or classed external sources. |

## Forbidden Shortcuts

| shortcut | why forbidden |
|---|---|
| Treating model agreement as evidence. | Agreement prioritizes work; it does not establish truth. |
| Promoting a model-generated source summary into a project finding. | The model is not the source and the source is not project-grounded. |
| Using model confidence to rank evidence strength. | Confidence is not calibrated to the project evidence gate. |
| Letting a model revise a locked rule or validation plan. | Locked artifacts are immutable except through explicitly allowed blind tightenings. |
| Feeding model output into grounded trees as if it were rerunnable analysis. | It would collapse the epistemic-class boundary. |

## Current Tooling Status

Use `knowledge_external/catalogs/indexes/V48_AI_CORE_TOOLING_HEALTH.md` for the
current route health:

- Claude: smoke-passes through the SAP AI Core client.
- Gemini: smoke-passes through the SAP AI Core client.
- RPT: smoke-passes through the dedicated `rpt-smoke` route; do not use generic
  `smoke --model rpt`.

## Required Verification

After any model-assisted task:

```bash
python3 scripts/v47_provenance_gate.py audit --fail-on-error
python3 scripts/v48_governance_preflight.py
```

If a model proposes an external source or claim, intake it through the
segregated external-record process. If it proposes a data analysis, run the
analysis and report the data-grounded result, not the model opinion.

## Boundary

- This card does not authorize model output as evidence.
- It does not add a model-generated claim.
- It does not change any grounded artifact.
- It exists so public readers and future sessions can distinguish proposal
  generation from evidence.

