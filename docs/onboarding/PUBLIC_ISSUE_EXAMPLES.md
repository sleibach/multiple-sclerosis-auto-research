# Public Issue Examples: Ready, Repairable, Closed, And Unsafe

These fictional examples show how to submit and review research-direction
ideas. They are communication fixtures, not actual proposals, analyses, or
scientific results. No named test below has run.

Reviewers grade the proposal, not the contributor. A strong issue is ready for
triage, not scientifically supported. A rejected form may still contain a
useful observation that can be reformulated safely. `[E01-E03]`

## Example 1: Strong And Ready For Triage

### Submitted issue

**Title:** Add a fail-closed source/outcome overlap diagnostic before any
returned monitoring-cohort interpretation

```markdown
Problem addressed:
A candidate outside validation package could have response labels aligned with
site, source, or processing batch. A score/outcome association would then be
hard to separate from acquisition structure. [M04, C02, A01]

Bounded question:
Before the frozen monitoring analysis is interpreted, does every included
source/batch stratum provide enough outcome overlap to estimate the planned
association without extrapolating outside observed support?

Prediction:
If source and outcome are sufficiently separable, the pre-specified overlap
diagnostic will pass and the frozen analysis can proceed to its ordinary
interpretation grid. If not, the package becomes non-identifiable for the
primary biological interpretation.

Required data:
- sample-to-person map;
- response label and its source definition;
- baseline and early sample IDs;
- source, site, processing batch, and collection dates;
- inclusion and quality flags; and
- permitted-use statement.

Independent unit:
Person. Repeated samples remain linked and are not counted independently.

Fair challenge:
Report source/outcome cross-tabs, overlap diagnostics, and a label-permutation
control that preserves source structure. Freeze any numeric warning or refusal
rule before viewing the molecular score/outcome association.

Drop or narrow rule:
If the primary outcome has no adequate within-source support, do not issue a
biological pass/fail verdict. Return “not identifiable under source overlap”
and name the missing strata.

Prior route changed:
This operationalizes the source-confounding lesson rather than claiming that
adjustment always repairs it. [C02]

Decision changed:
Determines whether a returned package is interpretable, requires a source-
balanced replication, or must be refused for the primary claim.
```

### Review response

```markdown
Workflow: Received for triage
Evidence: No new evidence grade

Why:
The issue states one bounded diagnostic question, the person-level unit,
required fields, an alternative explanation, a fail-closed outcome, and the
project decision it changes.

Next check:
Confirm compatibility with the frozen validation plan and define the diagnostic
without inspecting any outside outcome association. Ready-for-triage does not
mean the monitoring signal is supported or that a package will pass.
```

### Why this form works

- It improves interpretation eligibility rather than changing the locked
  biological rule.
- It permits “not identifiable” instead of forcing a positive or negative
  result.
- It names the independent unit and preserves pairing.
- It distinguishes a method safeguard from MS evidence.

## Example 2: Useful Insight, Design Repair Needed

### Initial issue

**Title:** Use network controllability to find the master switch in the APC
axis

```markdown
The APC system is coupled, so a controllability algorithm should identify the
best target. We should rank nodes and test the top one.
```

### Why this version cannot run

The grounded result is repeated co-movement, not a validated causal network.
The issue assumes edges, dynamics, intervention direction, and a “master
switch” before specifying observations that could distinguish them. It also
turns a method ranking into target evidence. `[D01-D02, M05]`

### Repair request

```markdown
Workflow: Design repair
Evidence: No grade yet

Useful part:
Control theory may help formalize which perturbations distinguish drivers,
readouts, feedback, and shared hidden causes.

Please add:
1. at least two competing directed system diagrams compatible with the current
   co-movement;
2. direction-resolved perturbations and time-resolved readouts that make the
   diagrams predict different outcomes;
3. the relevant cell/state and intervention sign;
4. a held-out functional result rather than a topology-only score; and
5. a result that rejects controllability as useful in this setting.

Important limit:
A centrality or controllability rank will remain a proposal lens until real
perturbation data discriminate the causal structures.
```

### Repaired issue

```markdown
Bounded question:
Can a minimal set of signed, time-resolved perturbations distinguish (a) one
upstream controller, (b) common-input co-response, and (c) feedback-coupled
readouts within the bounded APC architecture?

Directional prediction:
The three diagrams must predict different early and late responses under at
least one increase and one decrease perturbation.

Required data:
Cell-state-matched perturbation time series with intervention sign, dose,
replicate, source, and a functional readout not used to construct the graph.

Drop rule:
If the diagrams remain observationally equivalent under reachable
perturbations, do not nominate a control point; record a data/design boundary.

Decision:
Either justify a distinct perturbation experiment or stop converting the
coupled context into target language.
```

The revision is now a test design, not a target finding. It may still receive a
data request if the required perturbation package is unavailable.

## Example 3: Duplicate Of A Direction-Closed Route

### Submitted issue

**Title:** Reopen GPR25 because its predicted structure has a drug-like pocket

```markdown
GPR25 is a receptor and the structure looks tractable. We should screen
inhibitors and promote it over KIF21B.
```

### Review response

```markdown
Workflow: Duplicate or closed in current form
Evidence: Existing chr1 closure remains unchanged

Nearest prior route:
The chr1 region remains biologically real, but causal-gene assignment is
unresolved, GPR25 was demoted after denser review, and the protective direction
points toward restoration or increased function rather than default
inhibition. [G03, G05]

Why the new input does not reopen it:
Predicted geometry cannot choose the causal gene or reverse the genetically
required sign. An inhibitor screen begins from the same direction mismatch.

Evidence that could reopen the route:
Signal-specific causal assignment to GPR25, an MS-relevant cell/state effect,
and a feasible modality shown to produce the beneficial direction.

Important limit:
This closes the inhibitor-and-pocket argument, not every biological role for
GPR25 or the chr1 region.
```

### A genuinely new version would look different

It would bring causal and direction evidence, not a second structure viewer or
another list of ligands. If such evidence is not available, the honest
contribution may be an assay design that can discriminate increased from
decreased GPR25 function without claiming target status.

## Example 4: Unsafe Form, Safe Reformulation Possible

### Submitted issue

**Title:** Upload my records and tell me whether I should change MS treatment

```markdown
I can share my laboratory reports, scans, symptoms, and current medication.
Please calculate the APC/HLA-II score and tell me whether my treatment is
working or whether I should switch.
```

### Review response

```markdown
Workflow: Out of scope and unsafe
Evidence: No grade; no patient-level analysis will run

Boundary triggered:
This requests patient-specific medical advice and offers identifying health
information. The provisional score is not a clinical test, treatment selector,
or established decision tool. [M01, M05]

Do not submit:
Medical records, images, dates, medication details, identifiers, or any other
personal health information.

What can be retained safely:
The general research question “What evidence and interface safeguards would be
required before any independently validated monitor could support a clinical
workflow?” can be discussed without personal data or advice.

Important limit:
The repository cannot evaluate an individual's treatment and this reformulation
does not imply that the score will become clinically useful.
```

### Safe research-direction reformulation

```markdown
Bounded question:
For a hypothetical future independently validated monitor, which abstention,
uncertainty, confound-warning, and escalation states would prevent an interface
from presenting a monitoring association as treatment advice?

Method-only test:
Use fictional or synthetic interface fixtures to test comprehension and unsafe
overreads. Report interface behavior only; do not infer MS biology or clinical
benefit from synthetic users or data.
```

This reformulation can improve safety design. It cannot answer whether the
monitor works or whether any person should change treatment.

## What The Four Examples Teach

| example | workflow result | scientific consequence |
|---|---|---|
| Source-overlap diagnostic | Ready for triage | None until implemented and run; may improve result eligibility. |
| Network-control idea | Design repair, then possibly data request | No target; becomes a discriminating perturbation design. |
| GPR25 pocket argument | Duplicate/closed in current form | Existing bounded closure stays; exact reopening evidence is named. |
| Patient-specific request | Out of scope and unsafe | No analysis or advice; only a general method/safety question may remain. |

The workflow labels are not evidence grades. Use the
[status decoder](STATUS_DECODER.md), [response templates](REVIEW_RESPONSE_TEMPLATES.md),
and [ten-minute idea exercise](FIRST_IDEA_IN_TEN_MINUTES.md) for your own draft.
