# Research-Direction Idea Triage Rubric

This rubric makes the first review of a contributed idea transparent. It ranks
**what to test next**; it does not rank people, establish scientific truth, or
turn a proposal into a finding.

Use it after the contributor has completed the
[idea template](HOW_TO_CONTRIBUTE_IDEAS.md#copy-ready-idea-template). Worked
rewrites are in [Idea Transformations](IDEA_TRANSFORMATIONS.md).

## Why There Is No Single Total Score

A proposal can be novel and important but impossible to test. It can be easy to
run but repeat a route already closed. It can fit available data but lack a fair
null. Adding those qualities into one number would let strengths hide fatal
weaknesses.

The rubric therefore has:

1. **hard gates** that cannot be averaged away;
2. **separate axes** that stay visible; and
3. **an action class** describing what happens next.

## Step 1: Hard Gates

Mark each `pass`, `repair`, or `stop`.

| gate | pass condition | repair | stop condition |
|---|---|---|---|
| Evidence language | Proposal is labeled as a proposal and does not upgrade a project status. | Rewrite overclaiming language. | Requires treating literature, structure, or model output as project evidence. |
| Safety/scope | No diagnosis, treatment recommendation, patient-specific advice, or request for personal health details. | Remove unnecessary sensitive fields. | The contribution is principally medical advice or unsafe patient handling. |
| Locked analysis | Does not tune a locked rule or preregistered threshold after outcomes are visible. | Separate a future-development hypothesis from the untouched validation. | Requires changing the frozen external test to obtain success. `[A01]` |
| Data permission | Proposed data are public under compatible terms, legitimately held, or have a concrete lawful access path. | Clarify access and use terms. | Requires unauthorized access, ignored restrictions, or concealed provenance. |
| Duplicate/closure | Names the nearest prior route and addresses the documented failure reason. | Add the comparison and changed evidence. | Merely repeats a direction-, confounder-, validation-, or data-closed route. |
| Therapeutic direction | If therapeutic, causal entity, required functional sign, cell/state, modality, and delivery assumptions are explicit. | Resolve missing pieces before target language. | Defaults to inhibition or pocket/class precedent against an unresolved or restoration direction. `[G02-G04]` |
| Testability | At least one observable outcome could make the idea fail or narrow. | Add a discriminating prediction and drop rule. | Every possible result is defined as support. |

`repair` means return the idea with a specific request. `stop` means do not run
it in its current form. A stopped idea can return only if it directly resolves
the named issue.

## Step 2: Score Separate Axes

Use `0–3` on each axis. Record evidence for the score; do not score from tone,
credentials, model confidence, or length.

### A. Current-boundary fit

| score | rule |
|---:|---|
| 0 | Does not identify a current project boundary or addresses a solved/closed question without distinction. |
| 1 | Names a broad area but not the exact unresolved decision. |
| 2 | Names one current boundary and the nearest relevant claim IDs. |
| 3 | Shows precisely how the result would change the project's next decision. |

### B. Repo-relative novelty and non-duplication

This axis means “new relative to work already in this repository.” It is not a
literature-novelty claim.

| score | rule |
|---:|---|
| 0 | Repeats a documented route without addressing why it failed. |
| 1 | New wording, model, or dataset encoding but the same evidentiary test. |
| 2 | Changes a meaningful assumption, data source, comparator, or intervention direction. |
| 3 | Introduces a genuinely orthogonal, groundable frame and explains why prior tests did not cover it. |

### C. Falsifiability and discrimination

| score | rule |
|---:|---|
| 0 | No observable failure condition. |
| 1 | Prediction exists, but the main competing explanation predicts the same result. |
| 2 | Proposal and one competitor predict distinguishable outcomes; a drop rule is stated. |
| 3 | Multiple plausible explanations are separated by a minimal, precommitted test. |

### D. Data fitness and reachability

| score | rule |
|---:|---|
| 0 | Required design is absent or access is hypothetical. |
| 1 | Candidate source exists, but essential pairing, labels, fields, provenance, or terms are unverified. |
| 2 | Required fields and access path are verified; one bounded preparation step remains. |
| 3 | Data are lawfully reachable now and match person/sample/time/outcome/modality requirements without outcome-dependent repair. |

A score of `0` can still produce a valuable **data-request** action; it cannot
produce a grounded-analysis action. `[A04, P01-P05]`

### E. Error-control completeness

| score | rule |
|---:|---|
| 0 | No fair null, holdout, multiplicity, sample-size, or confound plan. |
| 1 | Some controls named, but major leakage or source/batch risk remains. |
| 2 | Primary estimand, null, holdout, correction, small-sample plan, and main confounders are fixed. |
| 3 | Controls are design-matched, failure thresholds are precommitted, and sensitivity cannot quietly become primary evidence. |

### F. Direction and modality fit

Score `N/A` for non-therapeutic ideas.

| score | rule |
|---:|---|
| 0 | Functional direction is wrong or ignored. |
| 1 | Direction named, but causal entity, cell/state, modality, or delivery is unresolved. |
| 2 | Direction and modality are compatible in principle; a functional test is specified. |
| 3 | A direction-matched assay can distinguish desired modulation from the opposite and non-specific effects. |

Structure can inform this axis but cannot determine it alone.

### G. Decision value

| score | rule |
|---:|---|
| 0 | No outcome changes a project decision. |
| 1 | Positive result has a use, but null/inconclusive outcomes do not. |
| 2 | Pass and fail each change a named next step; inconclusive output estimates a data need. |
| 3 | The test efficiently resolves a high-cost uncertainty and prevents or justifies a specific external investment. |

### H. Implementation boundedness

| score | rule |
|---:|---|
| 0 | Open-ended search with no test budget or stopping point. |
| 1 | Broad work package with unspecified branching. |
| 2 | One resumable test with named inputs, outputs, budget, and stop condition. |
| 3 | Smallest viable discriminating test; code/artifact location and verification command are specified. |

## Step 3: Assign An Action Class

| action | required pattern | next step |
|---|---|---|
| `RUNNABLE_NOW` | All hard gates pass; falsifiability, data fitness, and error control each ≥2. | Freeze the test and run it. |
| `DESIGN_REPAIR` | No stop gate, but prediction, controls, or scope is incomplete. | Return a field-specific repair request. |
| `DATA_REQUEST` | Prediction and error plan are credible, but data fitness is 0–1. | Verify or request the exact missing package/fields. |
| `EXTERNAL_TEST` | Internally grounded route now needs an independent cohort, assay, or holder-side run. | Preserve frozen rule and execute externally. |
| `DUPLICATE_OR_CLOSED` | Nearest failure reason is not addressed. | Link the closure; state what evidence could reopen it. |
| `OUT_OF_SCOPE_OR_UNSAFE` | Safety, permission, medical-advice, or evidence-class gate stops. | Do not execute; explain the boundary. |
| `PARKED_LOW_VALUE` | Executable but no result would change a meaningful decision. | Record without consuming scarce analysis or data access. |

An action class is not an evidence grade. `RUNNABLE_NOW` means a fair test can
begin, not that the idea is likely true.

## Four Calibration Examples

### “Use an inhibitor because GPR25 is a GPCR”

- Hard gate: therapeutic direction `stop`.
- Novelty: `0–1`; it repeats the class-precedent route.
- Data/direction: unresolved causal gene and apparent restoration requirement.
- Action: `DUPLICATE_OR_CLOSED` until evidence addresses the actual closure.
  `[G03, G05]`

### “Run the frozen score at the data holder and return only preregistered outputs”

- Hard gates: can pass if permission, identity/pairing audit, and no tuning are
  explicit.
- Novelty: depends on whether the holder and package are real, not on the word
  “federated.”
- Data fitness: `1` before holder fields are verified, `2–3` after verification.
- Action: `DATA_REQUEST`, then `EXTERNAL_TEST`; never a finding at proposal
  stage. `[A01, A04]`

### “Add source-balance checks before interpreting a new cell-state result”

- Current-boundary fit: high because the project observed a concrete source-
  diagnosis entanglement.
- Falsifiability/error control: high only with overlap metrics and a fixed
  non-identifiability threshold.
- Action: `RUNNABLE_NOW` as method work when applied prospectively, not as a
  claim that adjustment always repairs bias. `[C02]`

### “Claude and Gemini agree on a mechanism”

- Evidence-language gate: repair if agreement is offered as support.
- Falsifiability/data fitness: score the concrete prediction, not the models.
- Action: `DESIGN_REPAIR` until a reachable real-data test exists. `[E03]`

## Review Record

Use the [TSV template](templates/IDEA_TRIAGE_SCORECARD_V55.tsv). Two reviewers
may score independently for high-cost proposals. Disagreement should be
resolved by naming the assumption or missing evidence, not by averaging scores.

Every review should end with:

- action class;
- strongest reason for that class;
- exact repair or next command;
- claim IDs and nearest closure consulted;
- what would change the decision; and
- confirmation that no proposal was promoted to a finding.

