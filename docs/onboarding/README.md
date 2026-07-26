# Start Here: Understand And Contribute To The MS Research

This layer is for smart readers without a medical background. It explains the
project's current evidence state without changing it, makes negative and closed
routes visible, and turns the remaining frontier into testable collaborator
puzzles.

V55 is communication and onboarding only. It introduces no scientific claim.

## Choose Your Route

### I Have Two Minutes

1. Read [the two-minute version](MS_RESEARCH_EXPLAINED.md#the-two-minute-version).
2. Scan [the research terrain](visuals/RESEARCH_MAP_V55.svg).
3. Remember the bottom line: one provisional monitoring lead awaits independent
   validation; no intervention-grade target or progression mechanism has been
   established. `[M01, M05, P02]`

### I Have Fifteen Minutes

1. Read [the layered explanation](MS_RESEARCH_EXPLAINED.md#the-fifteen-minute-version).
2. Use the [visual guide](VISUAL_INDEX.md) for the monitoring lead, evidence
   lanes, relapse/progression distinction, and collaborator board.
3. Check [the lead status cards](LEAD_STATUS_CARDS.md) before following an
   attractive route.

### I Want To Contribute An Idea

1. Choose one of the eight
   [open problems](OPEN_PROBLEMS_FOR_COLLABORATORS.md#pick-a-puzzle).
2. Read its known non-solutions.
3. Use [the contribution guide and idea template](HOW_TO_CONTRIBUTE_IDEAS.md).
4. Open a research-direction issue using the repository issue form. A useful
   idea names a prediction, data, null or holdout, correction, and a condition
   that would make us drop it.

### I Am Reviewing Scientific Evidence

Start with the source artifacts rather than onboarding prose:

- [Authoritative scored findings](../reports/FINDINGS_REPORT_V37.md)
- [Therapeutic path](../reports/THERAPEUTIC_PATH_V52.md)
- [Joint-inference boundary](../history/JOINT_INFERENCE_V41.md)
- [Progression frontier](../history/PROGRESSION_FRONTIER_V54.md)
- [V55 claim-source contract](CLAIM_SOURCE_MATRIX_V55.md)
- [Machine-readable claim rows](ONBOARDING_CLAIM_SOURCES_V55.tsv)

## Visual Overview

![Four-lane research map showing the live provisional monitoring lead, supported context, closed genetics routes, negative systems results, progression data gaps, and two open validation/data edges.](visuals/RESEARCH_MAP_V55.svg)

[Open the accessible visual index and text equivalents](VISUAL_INDEX.md).

## Find The Right Page

| need | page |
|---|---|
| Understand MS, the project, and the honest frontier | [MS Research, Explained](MS_RESEARCH_EXPLAINED.md) |
| See every major route at a glance | [Visual Guide](VISUAL_INDEX.md) |
| Choose a cross-disciplinary puzzle | [Open Problems](OPEN_PROBLEMS_FOR_COLLABORATORS.md) |
| Find where my discipline fits | [Collaborator Routes](COLLABORATOR_ROUTES.md) |
| Get a short answer to a scope or evidence question | [FAQ](FAQ.md) |
| Turn a broad thought into a fair test | [Worked Idea Transformations](IDEA_TRANSFORMATIONS.md) |
| Submit a falsifiable idea | [How To Contribute Ideas](HOW_TO_CONTRIBUTE_IDEAS.md) |
| Decode terms | [Glossary](GLOSSARY.md) |
| Prevent common overreads | [Myths vs Actual Findings](MYTHS_AND_ACTUAL_FINDINGS.md) |
| Check one route's status | [Lead Status Cards](LEAD_STATUS_CARDS.md) |
| Inspect accessibility | [Accessibility Audit](ACCESSIBILITY_AUDIT_V55.md) |
| Inspect machine traceability | [Onboarding Audit Summary](../../analysis/v55_onboarding_audit/onboarding_audit_summary.json) |

## Evidence Promise

- Every scientific statement in this layer maps to a bounded claim row and
  committed source artifact.
- Status is always part of the statement: project-grounded, provisional,
  supported context, negative/closed, or data blocked.
- Outside-source context and model suggestions remain separate from project
  evidence.
- Missing data are not described as absent biology.
- Monitoring, mechanism, target, clinical benefit, and progression are not
  collapsed into one claim.

The automated V55 onboarding audit checks this boundary. Its current committed
result is `PASS` across all expected pages, visuals, claim references, local
links, semantic SVG metadata, size limits, and palette contrast.

## Automated Integrity Checks

The public onboarding layer has a secret-free continuous check at
`.github/workflows/onboarding-integrity.yml`. It runs on relevant pushes and
pull requests and can also be launched manually. The same checks can be run
locally:

```bash
python3 scripts/v55_onboarding_audit.py --fail-on-error
python3 scripts/v55_onboarding_audit.py --synthetic-check --fail-on-error
python3 scripts/v47_provenance_gate.py audit
python3 scripts/v51_structural_prediction_gate.py audit
python3 scripts/v55_visual_render_regression.py --fail-on-error
```

These commands test communication traceability, evidence-class separation,
static visual accessibility, and rendering. They do not validate a scientific
claim.
