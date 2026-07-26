# Starter Contributions With Clear Done Criteria

These are bounded ways to help without first mastering the whole repository.
Each task produces a reviewable artifact. None creates a scientific finding by
being completed or merged.

Choose a task because its **question** matches your skill, not because its tool
is fashionable. Read [Patient And Public Safety](PATIENT_AND_PUBLIC_SAFETY.md)
before handling any data-adjacent task.

## Quick Picker

| I can contribute… | start with | expected status |
|---|---|---|
| 30 minutes of careful reading | Task 1 or 2 | Communication feedback |
| Accessibility or visual design | Task 3 | Communication repair |
| Documentation or technical writing | Task 4 | Communication repair |
| Data engineering or schema design | Task 5 or 6 | Method behavior only |
| Statistics or causal inference | Task 7 or 8 | Method/proposal until a valid run |
| Dataset search or research operations | Task 9 | Access candidate only |
| Systems or experimental design | Task 10 | Test proposal only |
| Reproducible software | Task 11 | Infrastructure behavior only |
| Adversarial review | Task 12 | Challenge proposal only |

## Task 1: Run The Two-Minute Comprehension Check

- **Time:** 20-30 minutes
- **Useful skills:** careful reading; no domain expertise required

**Do:** Read only the two-minute route, then answer Q01-Q06 in the
[comprehension test kit](COMPREHENSION_TEST_KIT.md) without opening other
pages.

**Submit:** Which question failed, the exact phrase that produced your answer,
and the page or wording you expected to find.

**Done when:** The feedback identifies a reproducible comprehension gap rather
than simply saying the page is long or difficult.

**Do not:** Supply personal medical experience or search outside sources for
the “right” answer. This tests the documentation, not the reader.

## Task 2: Produce A Falsifiable Test Card

- **Time:** 20-40 minutes
- **Useful skills:** any discipline that can name a rival explanation

**Do:** Follow [Your First Idea In Ten Minutes](FIRST_IDEA_IN_TEN_MINUTES.md),
then score the draft with Q13-Q15 in the comprehension kit.

**Submit:** Observation, bounded question, directional prediction, independent
unit, minimum data, rival challenge, fail-closed checks, drop rule, and decision.

**Done when:** At least one plausible outcome makes you drop or narrow the
idea.

**Do not:** Start with a favorite method and retrofit a problem, or treat the
test card as evidence.

## Task 3: Audit One Visual Without Using Color

- **Time:** 30-60 minutes
- **Useful skills:** accessibility, information design, screen-reader use

**Do:** Choose one of the [eight visuals](VISUAL_INDEX.md). Review the rendered
graphic and its text equivalent in grayscale or without vision.

**Submit:** Whether status, reading order, uncertainty, and the “does not mean”
boundary survive; include one concrete repair if not.

**Done when:** Another reader can identify the same status and forbidden
overread without relying on hue or spatial layout alone.

**Do not:** Improve visual drama by making the provisional lead look like the
end of a success funnel.

## Task 4: Rewrite One Dense Passage Under A Meaning Contract

- **Time:** 30-60 minutes
- **Useful skills:** technical writing, editing, translation across disciplines

**Do:** Use [Contribute Documentation Or A Visual](CONTRIBUTE_DOCUMENTATION_OR_VISUAL.md)
to freeze the statement, claim ID, source, status, caveat, and dangerous
overread before editing.

**Submit:** Before/after text plus the unchanged meaning contract and audit
results.

**Done when:** The revision is easier to parse and preserves every distinction
that controls evidence status.

**Do not:** Remove the caveat, sample size, uncertainty, or closed-route scope
to make the sentence smoother.

## Task 5: Add A Synthetic Independent-Unit Leakage Fixture

- **Time:** 1-3 hours
- **Useful skills:** Python, testing, data engineering

**Do:** Create a small seeded, explicitly synthetic package where person-level
train/test separation passes and sample-level splitting leaks repeated visits.
Use it to test an existing validator or propose a focused failing test.

**Submit:** Seeded generator, expected pass/fail behavior, exact command, and
lightweight output.

**Done when:** The guard rejects the leaking split and accepts the correctly
grouped split across more than one seed.

**Status:** Method behavior only; no MS biology. `[A03, E01]`

**Do not:** Report synthetic performance as evidence that the monitoring score
works.

## Task 6: Exercise A Returned-Package Edge Case

- **Time:** 1-3 hours
- **Useful skills:** schemas, validation, privacy, data pipelines

**Do:** Choose one safe package shape: missing early timepoint, partial labels,
aggregate-only metrics, inconsistent person mapping, response-correlated batch,
or forbidden use terms. Use synthetic metadata only.

**Submit:** Fixture, expected intake status, refusal or warning message, and
test proving the pipeline fails closed.

**Done when:** The package cannot silently become analyzable and the output
distinguishes invalid, data-blocked, and biological negative.

**Do not:** Coerce fields or invent labels to make a package pass. `[A01-A04]`

## Task 7: Challenge A Confounder With A Fair Design

- **Time:** 1-2 hours for the proposal
- **Useful skills:** statistics, causal inference, domain adaptation

**Do:** Pick source, batch, broad immune tone, cell composition, timing, or
missingness. State the attractive claim and rival as two models that predict a
different observable outcome under a valid overlap design.

**Submit:** Estimand, independent unit, overlap requirement, primary diagnostic,
structure-preserving null, uncertainty, and the result that makes the claim
non-identifiable.

**Done when:** The challenge could weaken the attractive interpretation and
does not assume adjustment can repair absent support.

**Do not:** Call residual association causal after covariate adjustment.
`[M04, C02]`

## Task 8: Design A Small-Cohort Validation Alternative

- **Time:** 1-3 hours for the design
- **Useful skills:** sequential design, Bayesian design, calibration, decision
theory

**Do:** Preserve the frozen monitoring rule and outcome. Propose how a small
outside cohort can yield pass, fail, inconclusive, invalid, and data-blocked
outputs with calibrated uncertainty.

**Submit:** Cohort-size regime, fixed estimand, independent unit, interval or
decision rule, confound diagnostics, analysis budget, and simulation-only
evaluation plan.

**Done when:** The design extracts information without tuning the locked score
or turning inconclusive into support.

**Do not:** Change the genes, threshold, outcome, or exclusions after seeing
outside labels. `[M01-M04, A01, A03]`

## Task 9: Verify A Cohort Lead From Metadata

- **Time:** 1-4 hours
- **Useful skills:** literature/repository search, access operations, metadata

**Do:** Follow [Contribute A Data Source](CONTRIBUTE_A_DATA_SOURCE.md). Verify
person-level pairing, baseline/early timing, response or repeated-confirmed-
disability outcome, sample mapping, feature coverage, source/batch fields,
access tier, and use terms.

**Submit:** Permanent source links, access date, field-by-field eligibility,
independence from prior cohorts, and the exact missing field if unusable.

**Done when:** The lead has an honest access/eligibility status rather than a
paper-title claim.

**Do not:** Upload participant rows or count a cohort usable because the paper
mentions “response” or “progression.” `[A01-A04, P01]`

## Task 10: Turn Coupling Into A Discriminating Perturbation Design

- **Time:** 1-3 hours for the design
- **Useful skills:** control systems, experimental design, network science

**Do:** Draw at least two causal diagrams compatible with the observed coupled
APC context. Identify signed, timed perturbations that make them predict
different functional readouts.

**Submit:** Competing diagrams, intervention sign, cell/state, early and late
predictions, functional holdout, and a result that leaves the diagrams
observationally equivalent.

**Done when:** The proposal tests causality rather than ranking graph nodes.

**Do not:** Call centrality, controllability, or co-movement a target.
`[D01-D02]`

## Task 11: Reproduce One Public-Layer Check From A Clean Clone

- **Time:** 30-90 minutes
- **Useful skills:** reproducibility, continuous integration, developer experience

**Do:** Run one documented onboarding, rendering, source, provenance, or
structural gate in a clean environment without secrets.

**Submit:** Environment, exact command, output summary, runtime, missing
dependency if any, and whether the failure message points to a repair.

**Done when:** Another maintainer can reproduce the same pass or actionable
failure without private configuration.

**Do not:** Disable a failing gate or commit downloaded weights, caches, `tmp/`
files, or files over 50 MB.

## Task 12: Write The Strongest Countertest

- **Time:** 30-90 minutes
- **Useful skills:** skeptical review, red teaming, philosophy of science

**Do:** Use [Challenge The Project](CHALLENGE_THE_PROJECT.md). Target one exact
claim, closure, boundary, or decision and cite its controlling source.

**Submit:** Strongest rival, competing predictions, eligible data, fair
countertest, challenge-failure condition, and exact status consequence.

**Done when:** Both the original claim and the challenge can lose.

**Do not:** Use outside authority, model consensus, method novelty, or flexible
re-search as the countertest. `[E01-E03]`

## Submit Or Ask For Repair

Start with the root [contribution guide](../../CONTRIBUTING.md) and the live
research-direction issue form. If the task produces only documentation or
code, a focused pull request can be more appropriate than a research-direction
issue. State explicitly that scientific evidence status is unchanged.

Review grades the contribution, not the contributor. A useful partial result
can be returned with one named repair rather than forced into “accepted” or
“rejected.”

See [Contribution Examples By Type](CONTRIBUTION_EXAMPLES_BY_TYPE.md) for
ready-versus-repair patterns covering data, methods, visuals, and challenges.
