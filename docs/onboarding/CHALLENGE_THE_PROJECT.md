# Challenge The Project: A Guide To Useful Adversarial Critique

The project should be easy to challenge. A trustworthy claim is not protected
from criticism; it is stated precisely enough that a better explanation or
fairer test can defeat or narrow it.

This page invites strong counterarguments from newcomers and specialists. A
challenge does not need to agree with the project. It does need to identify the
exact claim, source, rival explanation, and observation that would distinguish
them. Criticism itself is not evidence; a valid rerunnable countertest can
change evidence. `[E01-E03]`

## What You May Challenge

You may challenge any of these:

- the scope or grade of a positive or provisional result;
- whether a confounder was measured or adjusted adequately;
- whether the independent unit, holdout, or null was fair;
- whether uncertainty or multiplicity was handled correctly;
- whether a closure is too broad or its reopening evidence is wrong;
- whether a target direction follows from the genetics;
- whether a data-coverage boundary overlooked a usable source;
- whether an onboarding simplification distorts the controlling artifact;
- whether code, data lineage, or a generated report is reproducible; or
- whether the current decision follows from the evidence.

Challenges to negative and closed findings are as welcome as challenges to the
live lead. The goal is not to defend a preferred conclusion. It is to make the
repository change when a stronger, eligible test warrants change.

## Choose One Challenge Type

| type | plain question | useful output |
|---|---|---|
| Claim-scope challenge | Does the wording reach beyond the population, time, compartment, outcome, or validation level tested? | A narrower replacement sentence tied to the same source. |
| Confound challenge | Could source, batch, baseline, broad immune tone, composition, timing, or observation process create the pattern? | A rival model and an overlap-aware test that may attenuate or invalidate interpretation. |
| Independence challenge | Are repeated samples, donors, sites, cohorts, or data types being counted as more independent than they are? | A corrected unit and rerun or uncertainty calculation. |
| Null challenge | Does the null preserve the structure that could generate a chance result? | A stricter, pre-specified null and family-wise correction. |
| Validation challenge | Is an internal split, resampling exercise, or reused cohort being described as outside confirmation? | A corrected label and genuinely independent test requirement. |
| Direction challenge | Does the proposed intervention sign match the allele-aligned protective direction in the relevant cell/state? | A sign-resolved causal and functional test. |
| Closure challenge | Was only one route tested while the wording closes a broader space? | Exact surviving scope and specific reopening evidence. |
| Coverage challenge | Does a supposedly missing dataset actually exist and meet every required field? | A verified package map, permissions, and eligibility table. |
| Decision challenge | Does the recommended next action follow from effect, uncertainty, value, and resource constraints? | An alternative decision rule with explicit costs and change conditions. |
| Reproducibility challenge | Can the recorded number be regenerated from committed code and allowed data? | A minimal failing case, corrected run, and affected-artifact list. |

## The Adversarial Challenge Card

Copy this form:

```markdown
### Exact claim challenged
<quote one sentence, status, claim ID, and link to controlling artifact>

### Why this is the strongest challenge
<one rival explanation or methodological defect, not a list of possibilities>

### Competing predictions
Under the current interpretation, we should observe: <directional prediction>
Under my rival interpretation, we should observe: <different prediction>

### Required data and independent unit
<people/donors/sites/cohorts/data types, fields, timing, source, permissions>

### Fair countertest
<fixed feature/estimand, comparator or null, holdout, confound checks,
multiplicity, and uncertainty>

### Failure conditions
My challenge fails if: <result retaining the current bounded claim>
The current claim narrows or fails if: <result favoring the rival>
The test is non-identifiable if: <overlap/data/design failure>

### Status consequence
<exact wording/status that should change under each eligible outcome>

### Prior work not being repeated
<known non-solution, previous sensitivity analysis, or closure already checked>
```

The card must permit the challenge to fail. “Try more methods until one
disagrees” is not adversarial validation; it is another flexible search.

## Four High-Value Challenge Targets

### 1. The provisional monitoring signal

**Current bounded position:** the fixed APC/HLA-II early-change score has small-
cohort internal support, mixed transport, and immune-tone attenuation; it
awaits frozen outside validation. It is not a target or clinical tool. `[M01-
M05, A01]`

Useful challenges include:

- a direct exposure or state variable missing from the confound audit;
- evidence that source, time, or response labels are not separable;
- a unit-of-independence error;
- a test showing the apparent transport depends on one therapy or definition;
  or
- a reproducible mismatch between the locked rule and its implementation.

Not useful: training another flexible model on the same 19 people, moving the
threshold after looking, or citing model agreement. `[M03, D02, E03]`

### 2. The direction-closed genetics routes

**Current bounded position:** chr1 KIF21B/GPR25 remains biologically relevant
but causally and directionally unresolved for intervention; GPR25 was demoted,
and PTGER4 lacks a clean shared direction. `[G02-G05]`

Useful challenges include:

- allele-aligned, signal-specific evidence assigning the causal gene;
- a relevant-cell effect that reverses the recorded functional sign;
- a feasible gain/restoration modality with a falsifiable assay; or
- proof that the closure wording extends beyond the route actually tested.

Not useful: nearest-gene reasoning, a pocket viewer, known ligands, or default
inhibition without direction evidence.

### 3. The progression data boundary

**Current bounded position:** the held collection lacks repeated compatible
molecular measurements linked to later repeated confirmed disability; no
progression biomarker, transition mechanism, target, treatment effect, or halt
strategy was established. `[P01-P06, A02]`

Useful challenges include:

- a legally usable dataset that meets every fixed longitudinal field;
- a valid design showing that an existing package actually identifies the
  transition rather than static stage, relapse, or morphology;
- a better treatment of attendance, censoring, source, and repeated outcomes;
  or
- evidence that the “no result established” wording accidentally claims
  biological absence.

Not useful: substituting a blood score for microglia, a one-time stage label
for progression, or a relapse endpoint for confirmed disability. `[B02, P01-
P06]`

### 4. The same-corpus discovery boundary

**Current bounded position:** zero of 22 unexpected candidates passed the
recurrence-plus-held-out-data-type gate; the 0.127 upper bound applies to that
corpus and gate, so new data are favored over unconstrained re-mining. `[D04-
D05]`

Useful challenges include:

- a demonstrated error in candidate counting, recurrence, correction, or
  held-out prediction;
- an alternative prospectively fixed joint model with a stricter null and the
  same independent holdout;
- proof that a data type treated as held out was not independent; or
- a genuinely new public dataset, rather than a reformat of the same evidence.

Not useful: interpreting 0.127 as an MS effect-size ceiling or searching the
same labels until a candidate appears.

## Challenges Based On Outside Sources

An outside paper, database, or expert consensus may expose a tension, but it
does not override a rerunnable result by authority. Use it this way:

1. cite the exact outside statement and source;
2. classify whether it truly overlaps the project claim;
3. identify differences in population, definition, compartment, time, or
   method;
4. derive competing predictions on reachable data; and
5. queue the countertest without importing the outside claim as a finding.

“The literature disagrees” is a flag. “Under the literature's definition, the
same held data should show X rather than Y” is the beginning of a test. `[E02]`

## Challenges Based On Models

A model may help articulate a fatal weakness, generate a rival graph, or find
ambiguous wording. Save the concrete challenge, not the model's confidence or
persona. Then verify every premise against artifacts and data. Agreement among
models can order review but cannot make the challenge true. `[E03]`

## How The Project Should Respond

Every challenge should receive:

1. the exact claim and controlling artifact the reviewer thinks it addresses;
2. a workflow status: ready, design repair, data request, duplicate/closed, or
   out of scope;
3. the strongest reason for that status;
4. the current evidence grade, explicitly unchanged while no eligible run has
   completed;
5. the exact countertest or missing input;
6. the result that would change the claim; and
7. a public closure after the challenge is tested or stopped.

If the challenge survives a valid run, update the controlling finding or
workup first. The onboarding source graph then identifies every plain-language
page that must change. Do not quietly edit only the public summary.

## What Does Not Count As A Challenge

- “A famous researcher says otherwise.”
- “Two models agree.”
- “This method is newer.”
- “The p-value should have been significant.”
- “The result feels biologically implausible.”
- “Try enough normalizations and select the strongest.”
- “The closed route might still work somehow.”
- “No data means anything is possible.”

Each may motivate a question, but none supplies a discriminating prediction or
eligible countertest.

## Submit The Challenge

Before submitting:

- read the [known non-solutions](KNOWN_NON_SOLUTIONS.md);
- find the claim in the [source matrix](CLAIM_SOURCE_MATRIX_V55.md);
- complete the challenge card;
- check the [status decoder](STATUS_DECODER.md); and
- use the repository research-direction issue form.

The best challenge may strengthen a bounded conclusion, narrow it, expose an
artifact, reopen a route with genuinely new evidence, or save the project from
an unnecessary analysis. All are valuable outcomes when the test is fair.
