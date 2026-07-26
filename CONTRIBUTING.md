# Contributing To MS Auto-Research

This repository welcomes research directions, data leads, methods, code,
documentation, visual design, and falsification tests. You do not need a
medical background. You do need to preserve the boundary between an idea, a
rerunnable result, a provisional finding, and outside-source context.

This project is research, not medical advice. Do not submit patient-specific
recommendations or personal health information. Read the
[`Patient And Public Safety`](docs/onboarding/PATIENT_AND_PUBLIC_SAFETY.md)
boundary before submitting any health-adjacent question or data lead.

## Fast Routes

| I want to… | start here |
|---|---|
| Understand the current state | [`docs/onboarding/README.md`](docs/onboarding/README.md) |
| Find a problem matching my skills | [`docs/onboarding/COLLABORATOR_ROUTES.md`](docs/onboarding/COLLABORATOR_ROUTES.md) |
| Pick a bounded starter task | [`docs/onboarding/STARTER_CONTRIBUTIONS.md`](docs/onboarding/STARTER_CONTRIBUTIONS.md) |
| Propose a research direction | [`docs/onboarding/HOW_TO_CONTRIBUTE_IDEAS.md`](docs/onboarding/HOW_TO_CONTRIBUTE_IDEAS.md) or the **Research direction** issue form |
| See how ideas are triaged | [`docs/onboarding/IDEA_TRIAGE_RUBRIC.md`](docs/onboarding/IDEA_TRIAGE_RUBRIC.md) |
| Avoid repeating a closed route | [`docs/onboarding/LEAD_STATUS_CARDS.md`](docs/onboarding/LEAD_STATUS_CARDS.md) and [`docs/onboarding/MYTHS_AND_ACTUAL_FINDINGS.md`](docs/onboarding/MYTHS_AND_ACTUAL_FINDINGS.md) |
| Inspect formal evidence classes | [`docs/knowledge/EPISTEMIC_CLASSES.md`](docs/knowledge/EPISTEMIC_CLASSES.md) |
| Check the live project state | [`meta/CURRENT_STATUS.md`](meta/CURRENT_STATUS.md) |

## Before You Change Anything

1. Read the nearest existing artifact and its status.
2. Identify whether your change is communication, method/software, grounded
   analysis, synthetic method testing, outside-source context, or a proposal.
3. Find the nearest negative, demoted, or closed route and explain why your work
   is different.
4. Decide what would make your own idea fail.
5. Confirm that required data are lawfully usable and that no reserved or
   quarantined cohort will be read outside its frozen test.

Finishing an analysis does not automatically create a finding. Evidence grade
and interpretation must follow the project's existing gates.

## Contribution Types

### Research-direction idea

Use the issue form or the copy-ready idea template. At minimum include:

- current boundary and relevant claim IDs;
- observable prediction and competing explanation;
- required data and verified access path;
- primary null or negative control;
- holdout, multiplicity, small-sample, and confound plan;
- decision consequence for pass, fail, and inconclusive; and
- a drop condition.

An idea remains a proposal until grounded on data. Model agreement, literature
plausibility, or a predicted structure does not change that.

### Documentation or visualization

Start with the dedicated
[`Contribute Documentation Or A Visual`](docs/onboarding/CONTRIBUTE_DOCUMENTATION_OR_VISUAL.md)
route.

- Trace every scientific statement to an existing bounded claim or source
  artifact.
- Keep provisional, supported, negative/closed, data-blocked, and outside-
  context language distinct.
- Preserve negatives prominently.
- Add alt text and a full text equivalent for substantive visuals.
- Use SVG or small self-contained files; do not add heavy media.
- Do not simplify away the caveat that determines the evidence grade.

Run the onboarding checks listed below.

### Method, software, or infrastructure

Use the
[`Contribute A Method`](docs/onboarding/CONTRIBUTE_A_METHOD.md) evaluation
contract for a new analytical method.

State what method behavior is being tested. Add focused tests and failure
fixtures. Synthetic data may test software, power, or false-positive behavior,
but must be seeded, labeled synthetic, segregated, and never described as MS
biology.

Do not change a locked rule or frozen preregistration to make a test pass. An
additive diagnostic committed while blind to validation data must be clearly
identified as such.

### Grounded analysis

A grounded result needs:

- committed code and exact inputs;
- a rerunnable command;
- real outputs, effect sizes, and uncertainty;
- null/permutation or appropriate negative controls;
- holdout/cross-validation appropriate to the unit of independence;
- multiple-testing control across the actual search;
- source, batch, composition, and other plausible confound checks;
- an honest negative/inconclusive path; and
- a bounded interpretation that does not outrun the design.

Therapeutic claims additionally require causal-gene confidence, functional
direction, relevant cell/state, modality fit, delivery assumptions, and
direction-matched validation. A protein class or structural pocket is not
enough.

### Dataset or cohort lead

Do not submit only a paper title or accession. Verify as much as possible:

- disease, treatment, and comparator;
- same-person pairing and timepoints;
- exact response or repeated confirmed-disability outcome;
- sample-to-person mapping;
- modality and required gene/feature coverage;
- site, source, batch, treatment, steroid, and timing metadata;
- access tier, data-use terms, and holder contact; and
- whether this repository already used the cohort.

Start with metadata and lawful access details. Never attach protected patient
data to an issue or pull request.

### Outside-source knowledge

Outside literature, database annotations, and predicted structures belong only
in the segregated external-knowledge tree and must follow
[`docs/knowledge/EPISTEMIC_CLASSES.md`](docs/knowledge/EPISTEMIC_CLASSES.md).
Every record needs its source, access date, relationship to project findings,
and explicit non-project-evidence marker. It cannot alter a grounded finding,
locked rule, or preregistration.

## Repository Safety

Never commit:

- API keys, service credentials, bearer tokens, or `.env`;
- personal, protected, controlled-access, or license-restricted data;
- files under a `tmp/` path;
- downloaded model weights or caches;
- files over 50 MB; or
- real validation data reserved for a frozen analysis outside its approved
  quarantine and execution path.

OpenGWAS integrations use POST only. Credentials are read from the ignored
environment file and must never enter logs, fixtures, documentation, or git.

## Local Verification

For onboarding or public documentation changes, run:

```bash
python3 scripts/v55_onboarding_audit.py --fail-on-error
python3 scripts/v55_onboarding_audit.py --synthetic-check --fail-on-error
python3 scripts/v55_plain_language_audit.py --fail-on-error
python3 scripts/v55_source_coverage.py --fail-on-error
python3 scripts/v47_provenance_gate.py audit
python3 scripts/v51_structural_prediction_gate.py audit
python3 scripts/v55_visual_render_regression.py --fail-on-error
```

For other code, run the narrowest relevant test plus any owning regression
suite. In every case:

```bash
git diff --check
git status --short
```

Confirm there is no tracked file over 50 MB and no tracked `tmp/` path before
pushing. The onboarding workflow reruns the public-layer checks without
secrets.

## Pull Requests

Keep a pull request bounded to one coherent contribution. Use the repository
template and include:

- the problem and current boundary;
- changed files and why;
- epistemic impact: none, proposal, method-only, grounded result, or outside
  context;
- source artifacts and claim IDs;
- tests and exact commands;
- negative, failure, or residual-risk result;
- data/permission statement; and
- explicit confirmation that no scientific status was silently upgraded.

Generated outputs should be committed only when they are small, deterministic,
necessary to audit the claim or method, and clearly labeled. Do not commit a
successful-looking output while omitting a failing or null companion result.

## How Review Ends

A review should produce one explicit disposition:

- ready to merge;
- needs a named design or evidence repair;
- needs a verified data-access step;
- ready for an external frozen test;
- duplicates a closed route without addressing it;
- parked because no outcome changes a decision; or
- out of scope/unsafe.

A merged proposal is still a proposal. Only a completed, appropriately
controlled analysis can change the project's evidence record.
