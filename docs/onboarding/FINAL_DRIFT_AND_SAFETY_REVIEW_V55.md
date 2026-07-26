# Final Cross-Page Drift And Safety Review

Status: communication-quality review; no scientific claim or status change.

This review asks whether the expanded public layer still tells one consistent,
safe story after many independently useful pages were added.

## Scope

The review covers:

- all reader pages registered in the plain-language and source-coverage maps;
- every Markdown page in `docs/onboarding/` plus the root README and
  contribution guide;
- all eight SVG visuals and their text equivalents;
- the live research-direction issue form; and
- the claim-source contract that controls public wording.

It checks status drift, medical-advice ambiguity, personal-data handling,
stale current-state counts, broken local links and anchors, and contribution
routes that end without a safe next step.

## Corrections Made

### “Clinical lead” removed from the controlling claim row

The reader pages already used **one live research lead**, but the M01 row in
the machine-readable claim contract still said **one live clinical lead**.
That wording could imply clinical readiness. The row now says **one live
research lead** while retaining the same provisional status, sources, allowed
scope, and forbidden overreads. No evidence changed. `[M01]`

### Root mission made current

The root README described the repository only as a search for a novel target.
That was the program's starting objective, but it no longer describes the
whole preserved record or the current boundary. The opening now says the
program began with that target search and retains supported, provisional,
negative, closed, and data-blocked results. It still makes no target claim.

### “Prove a near-match cannot substitute” narrowed

The one-page collaborator brief used “prove” for an access task. It now asks
contributors to **document precisely** why a near-match cannot answer the same
question. This avoids implying that a repository audit establishes a universal
impossibility.

### Current-state task summaries refreshed

The live queue's task table still described the initial five-visual and
11-page audit scopes. It now separates those early milestones from the current
eight-visual, full-reader-layer checks. Dated per-iteration notes remain
unchanged because they accurately record what existed at those times.

## Status-Drift Review

High-risk terms were searched across public pages, the issue form, root README,
and contribution guide. Uses of “validated biomarker,” “clinical lead,”
“treatment selector,” “treatment recommendation,” “prove,” and progression
claims were read in context.

After the M01 correction:

- the live monitor remains internally supported and outside-validation
  pending, not clinical; `[M01-M05]`
- coupled APC language remains context rather than target evidence; `[D01-D02]`
- CD44/CXCR4 remains an identity-only future candidate; `[P03-P06]`
- the progression result remains a data/design boundary rather than absent
  biology; `[P01-P02]`
- predicted structures and outside sources remain context; and `[E02]`
- model agreement remains proposal prioritization only. `[E03]`

Quoted unsafe examples remain only where the page immediately labels and
repairs them. Search hits alone therefore are not counted as drift.

## Medical-Advice And Privacy Review

The root contribution guide, onboarding landing page, live issue form, public
examples, response templates, workshop materials, and safety page all state
that the repository cannot:

- interpret a person's symptoms, scans, or laboratory results;
- recommend, stop, switch, or select treatment;
- predict an individual's response or progression;
- accept personal health records or identifying participant data; or
- provide urgent medical help.

The safe alternative is consistently a general research question, public
metadata/access route, method, documentation improvement, or privacy-safe
aggregate description. Unsafe examples are explicitly fictional and no
patient-level analysis is offered.

## Navigation And Contribution Loops

The public Markdown link graph was checked for dead ends:

- every public page has at least one outbound local route;
- every public page except the root README has at least one inbound route;
- all 17 configured high-value routes meet their one- or two-hop target; and
- data, method, documentation/visual, adversarial challenge, safety, status,
  and general-idea routes return contributors to review or evidence guidance.

The issue form contains ten elements with nine unique input IDs. YAML parsing
passes and every input is required. The form asks for the same bounded test
card used by the onboarding exercises.

## Current Machine Results

The final numbers below are generated after this review is added and are
refreshed with the release checks:

| check | result |
|---|---|
| Onboarding traceability and local links | `PASS` |
| Plain-language thresholds and acronym inventory | `PASS` |
| Claim/source coverage | `PASS` |
| Core route depth | `PASS` |
| Provenance segregation | `PASS` |
| Structural-prediction segregation | `PASS` |
| Browser rendering and constrained-width delivery | `PASS` |
| Tracked `tmp/` paths or files over 50 MB | none |

These checks establish consistency and delivery properties. They do not prove
human comprehension, scientific correctness beyond the controlling artifacts,
or clinical safety of a tool. No human newcomer comprehension session has yet
been reported.

## Maintainer Rule

When a scientific source changes, update the claim row first and use source
coverage to find every affected page. When only communication changes, retain
the same claim IDs and evidence status. Never “fix” a comprehension problem by
making the science sound stronger.

Continue with the [maintainer release checklist](MAINTAINER_RELEASE_CHECKLIST_V55.md),
[source-coverage map](SOURCE_COVERAGE_V55.md), or
[patient/public safety boundary](PATIENT_AND_PUBLIC_SAFETY.md).
