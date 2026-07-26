# Routes For Different Kinds Of Collaborators

The open problems are cross-disciplinary by design. This page maps familiar
skills to bounded research tasks. It does not imply that a method is useful
before testing; every route ends at the same evidence gate.

Start with the [two-minute explanation](MS_RESEARCH_EXPLAINED.md#the-two-minute-version),
then choose the route closest to how you think.

For a larger prompt bank, continue to
[question starters by discipline](QUESTION_STARTERS_BY_DISCIPLINE.md).

## Software And Infrastructure Engineers

**Best-fit problems:**
[2 · cohort access](OPEN_PROBLEMS_FOR_COLLABORATORS.md#problem-2-remove-dependence-on-one-hard-to-access-cohort),
[7 · prospective new information](OPEN_PROBLEMS_FOR_COLLABORATORS.md#problem-7-learn-from-new-data-without-reopening-the-same-search), and
[8 · safe monitoring workflow](OPEN_PROBLEMS_FOR_COLLABORATORS.md#problem-8-make-a-monitoring-result-useful-without-calling-it-a-target).

**What you can bring:** deterministic ingestion, schema and provenance checks,
privacy-preserving execution, reproducible environments, audit trails,
fail-closed interfaces, and testing strategies for messy incoming packages.

**A strong first contribution:** Define one realistic incoming-data failure
(wrong IDs, partial labels, duplicate people, mismatched timepoints, or batch
confounding) and add a synthetic fixture proving the pipeline rejects it or
reports it safely.

**Avoid:** treating a clean software run as biological validation; quietly
coercing bad input; or making an invalid cohort fit the expected schema.

## Statisticians And Machine-Learning Researchers

**Best-fit problems:**
[1 · small-cohort validation](OPEN_PROBLEMS_FOR_COLLABORATORS.md#problem-1-validate-a-small-cohort-signal-without-fooling-ourselves),
[6 · early confound detection](OPEN_PROBLEMS_FOR_COLLABORATORS.md#problem-6-detect-confounding-before-an-exciting-result-is-interpreted), and
[7 · prospective new information](OPEN_PROBLEMS_FOR_COLLABORATORS.md#problem-7-learn-from-new-data-without-reopening-the-same-search).

**What you can bring:** exact or permutation inference, small-sample
uncertainty, hierarchical/meta-analytic design, calibration, domain-shift
diagnostics, informative missingness, selective-inference controls, and
prospective holdout design.

**A strong first contribution:** Take one proposed method and write its estimand,
null, exchangeability assumptions, holdout unit, testing budget, and behavior
under the actual expected sample size before fitting anything.

**Avoid:** optimizing cross-validation on the same tiny cohort; reporting only
the best model; assuming a p-value resolves transportability; or treating a
new encoding as independent evidence.

## Data Engineers, Curators, And Stewards

**Best-fit problems:**
[2 · cohort access](OPEN_PROBLEMS_FOR_COLLABORATORS.md#problem-2-remove-dependence-on-one-hard-to-access-cohort),
[3 · progression movie](OPEN_PROBLEMS_FOR_COLLABORATORS.md#problem-3-build-the-movie-needed-to-study-progression), and
[6 · source confounding](OPEN_PROBLEMS_FOR_COLLABORATORS.md#problem-6-detect-confounding-before-an-exciting-result-is-interpreted).

**What you can bring:** accession verification, sample-person-time mapping,
ontology alignment, data-use constraints, metadata recovery, quality lineage,
site/source balance audits, and federated execution plans.

**A strong first contribution:** Produce a verified candidate manifest that
answers pairing, labels, outcome definition, gene coverage, provenance, access,
and use terms. An honest “not validation-ready” verdict is useful.

**Avoid:** raw hit-count lists; assuming a paper's outcome exists at sample
level; counting longitudinal data without the required outcome; or erasing
source/site fields during harmonization.

## Systems, Control, And Network Researchers

**Best-fit problems:**
[4 · restoration direction](OPEN_PROBLEMS_FOR_COLLABORATORS.md#problem-4-act-when-the-needed-direction-is-restore-function) and
[5 · coupled-system control](OPEN_PROBLEMS_FOR_COLLABORATORS.md#problem-5-test-a-coupled-system-without-inventing-a-multi-target-story).

**What you can bring:** identifiability analysis, competing causal graphs,
controllability under uncertainty, sparse intervention design, feedback versus
readout separation, and experiments that maximize discrimination among system
models.

**A strong first contribution:** Draw two or three competing graphs for the
coupled APC architecture and identify the smallest intervention/readout set
that would reject at least one graph.

**Avoid:** equating correlation with an edge, centrality with control, or a
coupled module with a useful multi-drug combination. `[D01, D02]`

## Protein, Chemistry, And Modality Engineers

**Best-fit problem:**
[4 · restoration direction](OPEN_PROBLEMS_FOR_COLLABORATORS.md#problem-4-act-when-the-needed-direction-is-restore-function).

**What you can bring:** direction-matched functional assays, gain/restoration
modalities, targeted delivery, protein engineering, controllable regulation,
and explicit modality failure analysis.

**A strong first contribution:** For one closed route, state the unresolved
causal gene, required functional sign, target cell/state, measurable readout,
delivery assumption, and an experiment that would falsify modality fit.

**Avoid:** “protein class equals druggable,” “predicted pocket equals target,”
or defaulting to inhibition when the protective direction appears to require
more function. `[G02-G04]`

## Designers And Human-Factors Researchers

**Best-fit problem:**
[8 · safe monitoring workflow](OPEN_PROBLEMS_FOR_COLLABORATORS.md#problem-8-make-a-monitoring-result-useful-without-calling-it-a-target).

**What you can bring:** uncertainty communication, abstention and invalid-input
states, audit-friendly interactions, misuse prevention, accessibility, and
workflow simulations that expose how a provisional result could be overread.

**A strong first contribution:** Prototype all four states—pass, fail,
inconclusive, and invalid input—and test whether a user can accurately state
what the score does **not** establish.

**Avoid:** a green/red treatment recommendation, hidden intervals, target-like
language, or a success-only demo. `[M05, A01]`

## Privacy, Security, And Federated-Data Specialists

**Best-fit problems:**
[2 · cohort access](OPEN_PROBLEMS_FOR_COLLABORATORS.md#problem-2-remove-dependence-on-one-hard-to-access-cohort) and
[3 · progression movie](OPEN_PROBLEMS_FOR_COLLABORATORS.md#problem-3-build-the-movie-needed-to-study-progression).

**What you can bring:** holder-side execution, minimal sufficient outputs,
attested containers, privacy budgets, data-use compliant logs, and protocols
that preserve blinding while allowing the frozen harness to run.

**A strong first contribution:** Specify the minimum fields and aggregate
outputs that permit the preregistered test without transferring row-level data,
including how identity, pairing, and batch diagnostics remain auditable.

**Avoid:** privacy transformations that destroy pairing, timing, outcome, or
confounder fields; or claiming a federated result is independent when the rule
was tuned against holder feedback.

## Clinicians And Disease Experts

**Best-fit problems:**
[1 · monitoring validation](OPEN_PROBLEMS_FOR_COLLABORATORS.md#problem-1-validate-a-small-cohort-signal-without-fooling-ourselves),
[2 · cohort access](OPEN_PROBLEMS_FOR_COLLABORATORS.md#problem-2-remove-dependence-on-one-hard-to-access-cohort), and
[3 · progression design](OPEN_PROBLEMS_FOR_COLLABORATORS.md#problem-3-build-the-movie-needed-to-study-progression).

**What you can bring:** outcome-definition critique, treatment/steroid context,
visit and confirmation logic, clinically meaningful failure modes, cohort
contacts, and corrections where computational abstractions misrepresent care or
disease course.

**A strong first contribution:** Audit whether the proposed outcome and timing
answer the claimed question, and identify clinical processes that could make
missingness, switching, or source informative.

**Avoid:** relaxing the evidence bar because a mechanism is plausible, or
converting a molecular association into patient advice.

## Science Communicators And Educators

**Best-fit work:** all eight problems, as a comprehension and misuse audit.

**What you can bring:** jargon detection, mental-model testing, layered
explanations, information design, and tests of whether readers preserve status
and negatives after skimming.

**A strong first contribution:** Give the onboarding to a new reader and test
whether they can recover the one live lead, no-target verdict, progression data
wall, and one valid contribution path without prompting.

**Avoid:** removing the caveat that carries the evidence grade, hiding negatives
for narrative flow, or replacing a precise boundary with motivational language.

## A Route For Any Discipline

If none of these labels fits, choose a puzzle and answer five questions:

1. What assumption from your field might this project be making unknowingly?
2. What observable prediction changes if that assumption is wrong?
3. What data could distinguish the alternatives?
4. What null, confounder, or holdout prevents an attractive false answer?
5. What result would make you drop your own idea?

Then use the [research-direction template](HOW_TO_CONTRIBUTE_IDEAS.md#copy-ready-idea-template).
The project values unfamiliar methods precisely when they become fair,
falsifiable tests.
