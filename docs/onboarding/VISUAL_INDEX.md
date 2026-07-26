# Visual Guide To The Research Frontier

All visuals are static, web-lightweight SVG files. They include an embedded
`title` and `desc`, use text and symbols in addition to color, and have a full
text equivalent below. The SVGs contain no controls or keyboard interactions.

## Small Screen And Print Rule

At phone, tablet-column, and portrait-print widths, all seven diagrams fit their
containers but their embedded labels become too small for direct reading. Use
the visible **Text equivalent** in each section as the complete content; open
the SVG directly only for zooming or a larger view. The measured review is in
[Narrow-Screen And Print Review V55](RESPONSIVE_PRINT_REVIEW_V55.md).

## 1. The Research Terrain

“Terrain” is a navigation aid, not a biological landscape. Card position and
distance do not encode causal proximity, effect size, or priority; the written
status and source references carry the meaning.

![Four-lane map of genetics, treatment monitoring, systems modeling, and progression. The one monitoring lead is live but provisional; genetics routes are context or closed; systems analysis contains supported context and negative results; progression is blocked by missing longitudinal data.](visuals/RESEARCH_MAP_V55.svg)

**Text equivalent:** Genetics produced robust MS-UC context and ZMIZ1
decoupling, while KIF21B/GPR25 and PTGER4 routes closed on direction or
evidence. Treatment monitoring contains the one live provisional APC/HLA-II
score, bounded by small n, mixed generalization, and immune tone. Systems work
supports coupled APC context but found no complexity gain; the broad simulator
failed its validation gate; and no unexpected joint signal passed the
held-out-modality gate. Progression has no established marker or target and
requires a longitudinal molecular-to-confirmed-disability cohort. The two open
edges are a frozen independent monitoring validation and correctly designed
progression data. `[G01-G05, M01-M04, D01-D05, P01, P02, P06, A01, A02]`

[Open the SVG directly](visuals/RESEARCH_MAP_V55.svg) ·
[Read the layered narrative](MS_RESEARCH_EXPLAINED.md)

## 2. The One Live Monitoring Lead

![Five-step flow from baseline and early-treatment paired samples through a fixed APC/HLA-II change score to a blind response-label test. Bounded evidence and confounder limits are shown beside a blocked inference to a drug target, followed by pass, fail, and inconclusive validation outcomes.](visuals/MONITORING_LEAD_V55.svg)

**Text equivalent:** The locked analysis compares baseline with an early sample
from the same person, computes a fixed APC/HLA-II delta, and compares one score
with a fixed response outcome without refitting. The pooled internal set has
`n=19`, AUC `0.811`, and permutation `p=0.008`; results were mixed across
therapies, and broad immune tone attenuated the score. It may monitor early
immune remodeling. It does not identify a target, choose treatment, prove
benefit, or answer progression. A frozen external test can pass, fail, or be
inconclusive. `[M01-M05, A01]`

[Open the SVG directly](visuals/MONITORING_LEAD_V55.svg) ·
[Read the source finding](../findings/FINDING_V22.md)

## 3. Evidence Lanes

The lanes are provenance categories, not biological pathways or a ranking of
importance. Material can move from an outside-source question to a new project
test only by creating and running that test; authority does not cross with the
idea.

![Two evidence lanes. Project-held data and rerunnable analysis can produce supported, provisional, negative, or data-bound conclusions. Literature, databases, and model suggestions can enter a future-test queue but cannot transfer authority directly into a project conclusion.](visuals/EVIDENCE_LANES_V55.svg)

**Text equivalent:** Project-grounded describes provenance, not whether a
result is positive. A rerunnable analysis can support a bounded statement,
justify a provisional next test, establish a negative, or identify a data
boundary. Outside-source and model material remains separate context. It can be
converted into a falsifiable future test, but cannot directly support a project
conclusion. `[E01-E03]`

[Open the SVG directly](visuals/EVIDENCE_LANES_V55.svg) ·
[Read the formal evidence policy](../knowledge/EPISTEMIC_CLASSES.md)

## 4. Relapse Versus Progression

The snapshot/movie language distinguishes cross-sectional from linked,
time-ordered measurement. It does not assume smooth disease change or make
repeated observation sufficient for causal inference.

![Schematic timeline separating discrete relapse events from repeated confirmed-disability measurements. A lower flow contrasts held snapshots and partial evidence roles with the required longitudinal molecular and disability movie, and lists prohibited proxy substitutions.](visuals/RELAPSE_VS_PROGRESSION_V55.svg)

**Text equivalent:** Relapse asks when an episode of inflammatory activity
occurred. Progression asks whether disability accumulated and remained
confirmed over time. They are related but not interchangeable. The held corpus
mostly provides snapshots or partial roles and cannot identify the transition.
The required design follows the same people with compatible molecular state,
repeated confirmed disability, event timing, and treatment/source/quality
provenance. Relapse, postmortem morphology, PBMC substitution, or an
outcome-chosen score cannot replace that design. `[B02, P01-P06, A02]`

[Open the SVG directly](visuals/RELAPSE_VS_PROGRESSION_V55.svg) ·
[Read the progression frontier](../history/PROGRESSION_FRONTIER_V54.md)

## 5. Open Problems For Collaborators

![Eight cards invite work on small-cohort validation, cohort access, longitudinal progression data, restoration-direction therapies, coupled-system control points, early confound detection, prospective new-data tests, and safe monitoring workflows. Each card names useful expertise and a known non-solution.](visuals/OPEN_PROBLEM_BOARD_V55.svg)

**Text equivalent:** The board contains eight puzzles:

1. Obtain an honest answer from a small validation cohort.
2. Break dependence on one inaccessible cohort.
3. Build the missing progression movie.
4. Design modalities for restoration rather than default inhibition.
5. Identify real control points in a coupled system.
6. Detect source, batch, and immune-tone confounding before interpretation.
7. Test genuinely new information prospectively.
8. Design a monitoring workflow that preserves uncertainty and does not become
   a treatment recommendation.

Every useful idea must name a prediction, data, null or holdout, correction,
failure condition, and known dead end avoided.

[Open the SVG directly](visuals/OPEN_PROBLEM_BOARD_V55.svg) ·
[Read all eight problem statements](OPEN_PROBLEMS_FOR_COLLABORATORS.md)

## 6. How The Research Changed Its Mind

![Six-row timeline connecting each candidate or question to a harder test and its current verdict. Genetics routes narrow or close, one monitoring signal remains provisional, systems complexity produces nulls, joint inference establishes a corpus boundary, validation engineering adds readiness rather than biology, and progression work ends at a bounded candidate plus missing longitudinal data.](visuals/RESEARCH_EVOLUTION_V55.svg)

**Text equivalent:** Cross-disease genetics produced MS-UC context and a ZMIZ1
direction warning while PTGER4 closed and GPR25 was demoted. The locked
APC/HLA-II score survived statistical and confounder testing as one provisional,
immune-tone-bounded monitor, not a target. Coupled APC architecture remained
supported context, while added complexity and a broad simulator failed their
predictive bars. Joint inference returned known structure but zero of 22
unexpected candidates passed the held-out-modality gate, bounding further mining of the held
corpus. Preregistration and synthetic checks improved validation readiness
without adding biological evidence. Progression work downgraded a morphology
pattern, retained CD44/CXCR4 by identity only, and exposed the missing
longitudinal molecular-to-confirmed-disability design. The open moves are frozen
monitoring validation and correctly designed progression data. `[G01-G05,
M01-M05, D01-D05, A01-A04, C01-C02, P01-P06]`

[Open the SVG directly](visuals/RESEARCH_EVOLUTION_V55.svg) ·
[Read the source-linked timeline](RESEARCH_EVOLUTION_TIMELINE.md)

## 7. How An Idea Reaches A Decision

The journey is an evidence workflow, not a disease mechanism or a guarantee of
progress. Real projects may loop back to repair data or narrow a claim; a clean
workflow can still end in a null, closure, or data boundary.

![Five-step evidence path from a bounded question through eligibility, identification, precommitment, and a rerunnable test. Invalid inputs and missing designs exit early. Valid tests can yield supported but bounded, mixed or inconclusive, or negative or closed outcomes, each with a different next action.](visuals/EVIDENCE_JOURNEY_V55.svg)

**Text equivalent:** Start with an exact claim, prediction, and drop rule. Check
that permissions, pairing, timing, labels, mappings, and coverage make the
inputs eligible. Then ask whether the design can separate the intended claim
from source, timing, outcome, and proxy alternatives. If inputs fail, the
result is invalid or unscoreable, not a biological null. If the design cannot
identify the claim, the result is data blocked, not absent biology. For a valid
question, freeze the feature, split, outcome, null, correction, and decision
rules before running the rerunnable test. A supported result keeps the scope and
any provisional status. A mixed, attenuated, or inconclusive result is narrowed
or used to repair/size the next test. A negative or closed result stops the
tested route unless genuinely new reopening evidence arrives. Every outcome
retains provenance, scope, uncertainty, and a concrete decision. `[E01, A01,
P01]`

[Open the SVG directly](visuals/EVIDENCE_JOURNEY_V55.svg) ·
[Read how to interpret non-positive outcomes](HOW_TO_READ_NULLS_AND_BOUNDARIES.md) ·
[Read how to submit a testable idea](HOW_TO_CONTRIBUTE_IDEAS.md)

## Status Encoding

No status depends on color alone:

| status | text/symbol treatment | visual treatment |
|---|---|---|
| Live or test next | `LIVE`, `PROVISIONAL`, or a filled-circle marker | blue, heavier border |
| Supported context | `SUPPORTED` or check marker | green border |
| Closed | `CLOSED`, `DEMOTED`, or cross marker | red border |
| Negative result | `NEGATIVE` or minus marker | purple border |
| Data or interpretation boundary | `DATA GAP`, `DATA BOUND`, or hatched-square marker | amber border and hatch where space permits |

Color improves scanning but never supplies the category by itself.

## Accessibility Notes

- SVG dimensions use a `viewBox`, so they scale without raster blur.
- Each file has `role="img"`, `aria-labelledby`, a non-empty title, and a
  detailed description.
- The lowest-contrast normal text has at least `6.12:1` contrast against its background;
  primary text is at least `13.99:1` across status fills.
- Status-border contrast against fills ranges from `5.41:1` to `7.19:1`.
- The long-form text equivalents on this page preserve meaning if SVG reading
  order is poor in a specific assistive technology.
- At constrained screen and portrait-print widths, the text equivalents are
  required because scaled embedded labels fall below the delivery threshold.
- The diagrams are static. There are no focusable controls, hover-only content,
  animation, or time limits.

See [Accessibility Audit V55](ACCESSIBILITY_AUDIT_V55.md) for the scoped review
and residual limitations.
