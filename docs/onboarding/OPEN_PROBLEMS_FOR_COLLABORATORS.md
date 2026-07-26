# Open Problems For Collaborators

This board turns the project's current evidence boundary into concrete puzzles
for smart contributors who may know little medicine but know methods, systems,
data, measurement, software, or experimental design.

It introduces no biological finding. Every scientific premise carries a claim
ID from the [V55 source contract](CLAIM_SOURCE_MATRIX_V55.md). Proposed
directions on this page have **zero finding status** until they are tested.

Before choosing a route, scan the [known non-solutions](KNOWN_NON_SOLUTIONS.md)
so the proposal changes a failed assumption rather than repeating it.

## Pick A Puzzle

| # | open problem | current boundary | outside perspective most useful |
|---:|---|---|---|
| 1 | Validate a signal in a tiny cohort without fooling ourselves | Live, provisional; external test missing `[M01, A01, A03]` | small-sample statistics, decision theory, sequential design, uncertainty communication |
| 2 | Remove dependence on one hard-to-access cohort | Data/access blocked `[A04]` | data discovery, privacy-preserving collaboration, metadata engineering, federated analysis |
| 3 | Build the “movie” needed to study progression | No suitable longitudinal molecular-to-disability data `[P01, P03, A02]` | longitudinal design, measurement science, causal inference, survival/event-time methods |
| 4 | Act when protection seems to require restoring function | Genetics routes closed on direction `[G02-G04]` | control theory, protein engineering, modality design, inverse problems |
| 5 | Test a coupled immune system without inventing a multi-target story | Coupled context supported; added complexity failed `[D01, D02]` | system identification, network control, perturbation design, sparse models |
| 6 | Detect source and immune-tone confounding before interpretation | Two concrete confounding lessons `[M04, C02]` | adversarial validation, domain shift, causal diagrams, batch diagnostics |
| 7 | Learn from new data without reopening an exhausted same-corpus search | Joint held-corpus search reached a boundary `[D04, D05]` | prospective test design, dataset shift, cross-modal holdout, information value |
| 8 | Turn a monitor into a useful workflow without calling it a target | Monitoring is not intervention evidence `[M05, A01]` | human factors, clinical decision support design, calibration, failure-safe interfaces |

## Problem 1: Validate A Small-Cohort Signal Without Fooling Ourselves

**Plain question:** How can a fixed monitoring score receive a decisive and
honest external test when the available cohort may be small?

**What is known.** The fixed APC/HLA-II early-change score is the project's one
live research lead. Its internal evidence set has 19 people, and broader immune
tone attenuates it. A frozen preregistration specifies pass, fail, and
inconclusive outcomes. `[M01, M03, M04, A01]`

**Why it is hard.** Seeded method simulations show that a small cohort can
produce a useful effect estimate yet remain inconclusive unless the true effect
is large and labels are clean. Those simulations characterize method behavior;
they are not estimates of MS biology or a prediction of the real cohort.
`[A03 | Synthetic method evidence only]`

**Already tried.** The rule was locked, flexible models were compared, null and
confounder tests were run, a power map was simulated, and outcome
interpretations were fixed before external data access. `[M03, M04, A01, A03]`

**Useful contributions.** Bring a method that can be specified before labels
are seen and that reports effect size and uncertainty without silently changing
the rule. Examples include small-sample confidence methods, calibration-aware
decision analysis, valid meta-analysis across cohorts with matching
measurements and outcome definitions, or a design that separates “estimate the
effect” from “declare the rule passed.”

**A valuable idea must specify:** the estimand, required sample fields, how
pairing is preserved, the null, what happens under missingness, the number of
tests, and what result would count as failure.

**Known non-solutions:** adding features to the same 19 people; selecting a
subgroup after seeing outcomes; moving the threshold; calling repeated
reanalysis an independent replication; treating an inconclusive interval as a
pass. `[D02, A01]`

**Controlling artifacts:**
[Finding V22](../findings/FINDING_V22.md),
[Robustness Map V28](../workups/treatment_response/ROBUSTNESS_MAP_V28.md),
[Confounder Audit V32](../workups/treatment_response/CONFOUNDER_AUDIT_V32.md),
[Preregistration V42](../validation/PREREGISTRATION_V42.md), and
[Power Map V43](../validation/POWER_MAP_V43.md).

## Problem 2: Remove Dependence On One Hard-To-Access Cohort

**Plain question:** Can we obtain or construct a legitimate independent test
without pretending that an unlabeled or mismatched dataset is suitable?

Use the [data-source contribution checklist](CONTRIBUTE_A_DATA_SOURCE.md) to
verify a candidate before counting it as usable.

**What is known.** An audited multi-repository search found no fresh public,
ready-to-run primary validation cohort. Gafson, a candidate external cohort,
remains an access request. Karolinska, a second candidate, has useful
longitudinal data but lacks the public patient-level response mapping required
by the frozen test. This is a verified access boundary, not a claim that no
cohort exists anywhere. `[A04]`

**Why it is hard.** A dataset counts only if it has paired baseline and early
samples, compatible genes, response labels, subject mapping, and enough
provenance to diagnose batch and confounding. “Longitudinal” alone is not
enough.

**Already tried.** GEO, publication supplements, and multiple public
repositories were audited; candidate access tiers were checked; Gafson and
Karolinska request packets and mechanical arrival handling were prepared.
`[A04]`

**Useful contributions.** Find a specific cohort and verify every required
field; design a federated run in which data never leave the holder; propose a
privacy-preserving exchange of only preregistered sufficient outputs; or map
the exact governance path from author-held labels to a blind harness run.

**A valuable idea must specify:** accession or holder, treatment, timepoints,
outcome definition, sample-to-subject map, gene coverage, access terms, and how
the locked rule can run without tuning.

**Known non-solutions:** counting raw repository hits; using a cohort without
response labels; substituting another disease or late tissue result as primary
MS validation; describing an unsent request as acquired data. `[A04]`

**Controlling artifacts:**
[Alternative Cohort Scout V44](../validation/ALT_COHORT_SCOUT_V44.md) and
[Karolinska Label Request V45](../validation/KAROLINSKA_DMF_LABEL_REQUEST_V45.md).

## Problem 3: Build The “Movie” Needed To Study Progression

“Movie” is shorthand for linked, repeated molecular and disability
measurements in the same people. It does not assume progression is smooth or
that repeated measurement alone identifies a cause.

**Plain question:** What is the smallest feasible longitudinal design that can
connect a molecular state to confirmed disability accumulation rather than to
relapse, static stage, or tissue source?

**What is known.** The held corpus has no usable longitudinal
molecular-to-confirmed-disability dataset. Seven datasets could not identify a
relapsing-to-progressive transition, and none of ten known packages filled all
three pre-defined roles: longitudinal progression, compatible biological
compartment, or functional direction. `[P01, P03, P05]`

**Why it is hard.** Progression requires repeated measurements in the same
people, event timing, confirmed disability, treatment history, attendance and
censoring information, and source/site provenance. A cross-sectional stage
label is a photograph, not a transition.

**Already tried.** The project audited available roles, tested bounded state
modules, downgraded confounded patterns, fixed an exact CD44/CXCR4 microglia
candidate identity, and built acquisition and fail-closed intake rules. It did
not establish a progression marker or target. `[P02, P04, P05, P06, A02]`

**Useful contributions.** Bring longitudinal measurement design, event-time
methods, informative-missingness diagnostics, joint molecular/clinical models,
or a concrete dataset that satisfies the acquisition fields. A useful data
fusion idea must preserve time, person, compartment, and outcome identity.

**A valuable idea must specify:** repeated molecular compartment, confirmed
disability definition, visit schedule, event-time handling, treatment and
switches, missingness/censoring, source/site effects, and a held-out test.

**Known non-solutions:** relapse count alone; cross-sectional disease stage;
postmortem morphology alone; applying a microglia score to PBMC or whole blood;
choosing proxy genes or thresholds after disability outcomes are visible.
`[P03, P05, P06]`

**Controlling artifacts:**
[Progression Frontier V54](../history/PROGRESSION_FRONTIER_V54.md),
[Cohort Acquisition Spec V54](../validation/PROGRESSION_COHORT_ACQUISITION_SPEC_V54.md), and
[P1 Candidate Handoff V54](../validation/PROGRESSION_P1_CANDIDATE_STATE_HANDOFF_V54.md).

## Problem 4: Act When The Needed Direction Is “Restore Function”

**Plain question:** If protection appears to require more or restored function,
what intervention modality could deliver that direction in the right cell and
state?

**What is known.** ZMIZ1 provides a supported warning that shared autoimmune
genetics can point in opposite directions; it is not a promoted target or a
closed biological result. The KIF21B/GPR25 and PTGER4 target routes did close:
their obstacles include causal-gene uncertainty, conflicting directions, or a
protective implication on the difficult up-function side. Predicted structure
can inform geometry but cannot decide causal direction or make a route
actionable. `[G02, G03, G04]`

**Why it is hard.** Most casual target discussions assume inhibition. A pocket
or known ligand is irrelevant if the required action is restoration, if the
causal gene is unresolved, or if the effect must occur only in a specific cell
state.

**Already tried.** Dense immune-QTL direction review, disease-direction
comparison, first-principles modality checks, and confidence-scored structure
context were applied. KIF21B/GPR25 and PTGER4 remained closed. `[G03, G04,
G05]`

**Useful contributions.** Propose a direction-matched modality or a decisive
experiment from protein engineering, targeted delivery, controllable gene
regulation, degradation-rescue logic, or systems control. The useful part is
not a platform name; it is a test showing the right functional sign in the
relevant cell state.

**A valuable idea must specify:** causal gene uncertainty, required sign,
affected cell/state, measurable functional readout, delivery assumptions,
off-direction risk, and an experiment that can falsify the modality fit.

**Known non-solutions:** “it is a GPCR, therefore druggable”; “AlphaFold shows a
structure, therefore target”; assuming inhibition; transferring direction from
another autoimmune disease. `[G02-G04]`

**Controlling artifacts:**
[chr1 Reevaluation V19](../workups/genetics/GENETICS_CHR1_REEVALUATION_V19.md) and
[Therapeutic Path V52](../reports/THERAPEUTIC_PATH_V52.md).

## Problem 5: Test A Coupled System Without Inventing A Multi-Target Story

**Plain question:** How can we tell whether a recurring coupled immune axis has
real control points, rather than merely correlated readouts?

**What is known.** HLA-II, IFN/APC, MIF/CD74-related state, IFN readout, and
lysosomal processing recur as a coupled architecture. Adding coupled features
did not improve the fixed monitoring score, and no component or combination is
a validated target. `[D01, D02]`

**Why it is hard.** Correlated nodes can reflect a shared upstream cause,
measurement redundancy, cell composition, or feedback. Network diagrams make
all four look like intervention logic.

**Already tried.** Latent/coupled structure, simple versus flexible prediction,
multi-node scoring, and perturbation checks were explored. Complexity did not
earn predictive improvement. `[D01, D02, D03]`

**Useful contributions.** Bring system identification, intervention design,
sparse control, causal discovery with explicit assumptions, or perturbation
selection that distinguishes upstream driver, downstream readout, and redundant
node. A minimal experiment that separates competing network topologies is more
valuable than a denser graph.

**A valuable idea must specify:** candidate causal graphs, interventions,
measurable responses, identifiability assumptions, negative controls, and what
observation would reject each graph.

**Known non-solutions:** ranking nodes by connectivity; treating co-movement as
causality; proposing a drug combination because two scores correlate; adding
features without held-out gain. `[D01-D03]`

**Controlling artifacts:**
[Deep Structure V26](../findings/DEEP_STRUCTURE_V26.md),
[Robustness Map V28](../workups/treatment_response/ROBUSTNESS_MAP_V28.md), and
[Therapeutic Path V52](../reports/THERAPEUTIC_PATH_V52.md).

## Problem 6: Detect Confounding Before An Exciting Result Is Interpreted

**Plain question:** Can we build diagnostics that identify when a biological
label is entangled with source, batch, composition, or broad immune state before
we narrate the pattern?

**What is known.** Broad immune tone attenuated the monitoring score. In a
microglia analysis, brain bank and disease label were strongly entangled
(Cramer's V 0.773), and source adjustment weakened an apparent localization.
These are bounded project lessons, not claims that every immune or brain-bank
result is invalid. `[M04, C01, C02]`

**Why it is hard.** Small studies may have no overlap between source and label,
making ordinary adjustment unstable or impossible. A model can predict the
label perfectly by learning acquisition history.

**Already tried.** Marker-based composition panels, steroid-response proxies,
immune-tone residualization, source fixed effects, wild bootstrap,
source-stratified permutation, and balance auditing were used. `[M04, C02]`

**Useful contributions.** Bring domain-adversarial diagnostics, overlap and
positivity checks, causal diagrams, negative controls, leave-source-out tests,
or a visual audit that fails before modeling when labels and source cannot be
separated.

**A valuable idea must specify:** the suspected confounder, how overlap is
measured, a failure threshold fixed before outcome analysis, what correction is
valid under that overlap, and when the only honest verdict is “not
identifiable.”

**Known non-solutions:** deleting the source column; adjusting after selecting
the most exciting result; assuming normalization removes design confounding;
claiming biology absent after a source-sensitive result fails. `[C02]`

**Controlling artifacts:**
[Confounder Audit V32](../workups/treatment_response/CONFOUNDER_AUDIT_V32.md) and
[Microglia Source-Balance Addendum V53](../validation/MS_MICROGLIA_SOURCE_BALANCE_ADDENDUM_V53.md).

## Problem 7: Learn From New Data Without Reopening The Same Search

**Plain question:** What prospective test can extract genuinely new information
instead of fitting another flexible story to the same assembled corpus?

**What is known.** Joint inference over 985 evidence rows, 71 entities, and 14
modalities recovered known APC/immune-tone structure. None of 22 unexpected
candidates passed both recurrence and held-out gates. The resulting 0.127 upper
bound is specific to that corpus and gate, not a universal biological ceiling.
`[D04, D05]`

**Why it is hard.** The more often a corpus is queried, the easier it is to
produce a plausible post-hoc pattern. A new algorithm on the same labels is not
automatically new evidence.

**Already tried.** Per-dimension probes, multi-view aggregation, source-
preserving nulls, modality holdout, recurrence meta-analysis, and a quantitative
exhaustion estimate were run. `[D04]`

**Useful contributions.** Propose a prospective split, a genuinely new modality
with a predicted outcome, a cross-site transport test, or a value-of-information
calculation that chooses which data to acquire. The proposal should be written
before the new outcome is observed.

**A valuable idea must specify:** what information is new, the frozen
prediction, correction across the search budget, the holdout unit, and how a
null changes the decision.

**Known non-solutions:** another unconstrained genome-wide scan on the held
corpus; using model agreement as validation; changing the candidate after
holdout failure; calling a re-encoded modality independent. `[D04, D05, E03]`

**Controlling artifact:** [Joint Inference V41](../history/JOINT_INFERENCE_V41.md).

## Problem 8: Make A Monitoring Result Useful Without Calling It A Target

**Plain question:** If external validation succeeds, what decision-support role
could the score safely play, and what evidence would that role require?

**What is known.** The score is a candidate early monitoring signal. It does
not identify a therapeutic mechanism, select the best drug, prove clinical
benefit, or answer progression. Independent validation would strengthen the
monitoring association without erasing those boundaries. `[M01, M05, A01]`

**Why it is hard.** Interfaces and narratives often convert a correlated score
into a recommendation. Small-cohort uncertainty, missing values, batch
warnings, and inconclusive results must remain visible to a user under pressure.

**Already tried.** The rule, ingestion behavior, confounder report, outcome
grid, and synthetic method checks were frozen before external data. `[A01]`

**Useful contributions.** Bring human-factors design, calibrated risk
communication, prediction models that can decline to decide when input is
uncertain, audit trails, or workflow simulation. Design for pass, fail,
inconclusive, and invalid-input states rather than only a successful demo.

**A valuable idea must specify:** intended user and decision, permitted claim,
minimum data quality, uncertainty display, abstention behavior, harm from false
positive and false negative, and the next validation needed before deployment.

**Known non-solutions:** a green/red clinical recommendation from the current
score; hiding confidence intervals; treating immune remodeling as efficacy;
allowing users to tune the threshold; using the tool for progression. `[M05,
A01]`

**Controlling artifacts:**
[Preregistration V42](../validation/PREREGISTRATION_V42.md) and
[Outcome Interpretation Grid V42](../validation/OUTCOME_INTERPRETATION_GRID_V42.md).

## What A Useful Direction Looks Like

A useful contribution can be one paragraph if it answers these questions:

1. **Which numbered problem does it address?**
2. **What is the proposed mechanism, method, dataset, or reframe?**
3. **What concrete prediction differs from the current alternatives?**
4. **What data are needed, and are they actually reachable?**
5. **What null, holdout, or correction prevents self-deception?**
6. **What result would make us drop the idea?**
7. **Which known non-solution does it avoid?**

Domain expertise is welcome but not required. Precision about assumptions and
failure is more useful than confidence. The project can evaluate an unfamiliar
method; it cannot evaluate an idea that has no observable prediction.

## Not In Scope

- Medical advice or patient-specific treatment recommendations.
- A new scientific claim presented without a runnable test.
- Reopening a closed lead because it is popular or structurally attractive.
- Treating literature, model output, or consensus as project evidence.
- Replacing missing progression data with a convenient proxy after outcomes
  are known.

The purpose of this board is not to make contribution easy by lowering the
bar. It is to make the real bar visible enough that a person from another field
can clear it.

## Continue

- [Turn a chosen problem into a testable submission](HOW_TO_CONTRIBUTE_IDEAS.md)
- [See what happens after submission](WHAT_HAPPENS_TO_YOUR_IDEA.md)
- [Return to the onboarding routes](README.md)
