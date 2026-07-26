# MS Research, Explained

**Audience:** curious engineers, designers, scientists from other fields, and
systems thinkers. No medical background is assumed.

**What this page is:** an accessible map of work already recorded in this
repository. It introduces no new scientific claim. Bracketed IDs such as
`[M01]` point to the bounded claim contract in
[the claim-source matrix](CLAIM_SOURCE_MATRIX_V55.md).

## Read The Status Before The Claim

| plain-language status | what it means here |
|---|---|
| **Project-grounded** | The project can rerun the analysis on data it holds. This does not automatically mean independently validated or clinically useful. |
| **Live, provisional** | There is bounded internal support and a fixed next test, but outside confirmation is still missing. |
| **Supported context** | Useful for interpretation inside a stated scope; not necessarily a biomarker, cause, or target. |
| **Negative or closed** | A tested route failed, was downgraded, or needs specifically named new evidence before it should reopen. |
| **Data blocked** | The required design or data is absent. That is not proof that the underlying biology is absent. |
| **Outside-source context** | Material read from literature or public resources and kept in a separate layer. It can orient questions but is not project evidence. |

The formal evidence-handling policy is in
[EPISTEMIC_CLASSES.md](../knowledge/EPISTEMIC_CLASSES.md). `[E01, E02]`

![Research terrain showing the live monitoring route beside supported context, closed genetics routes, negative systems results, and progression data gaps.](visuals/RESEARCH_MAP_V55.svg)

[Open all seven visuals with full text equivalents](VISUAL_INDEX.md).

---

## The Two-Minute Version

### What Problem Are We Working On?

Multiple sclerosis, or MS, involves immune-mediated injury in the central
nervous system, including damage to myelin and nerve fibers. This sentence is
medical orientation, not a result discovered by this project. `[B01 |
Background orientation]`

Two outcomes are easy to blur together:

- A **relapse** is an episode of inflammatory disease activity.
- **Progression** is disability accumulating over time.

They are related, but they are not interchangeable, and people do not all
follow one universal path. The project ultimately cares about halting
progression, the harder question. `[B02 | Supported boundary]`

### What Kind Of Project Is This?

This is an autonomous computational research program. Its central discipline
is simple: a result earns project status only when it can be traced to data and
analysis stored or reproducible here. Literature and AI models can suggest
questions, but they cannot turn a suggestion into evidence. `[E01, E02, E03 |
Governance]`

That discipline produces many negative results. Those are not hidden. A
closed route is decision-useful because it tells the next contributor what
not to assume and what exact evidence would be needed to reopen it.

### What Has It Found?

There is **one live clinical lead**, and it is provisional: an early-treatment
score based on changes in antigen-presentation genes, called the scope-limited
(“bounded”) APC/HLA-II score. It may help monitor whether a person's immune state is
changing soon after treatment. It is not a drug target, treatment selector,
clinical test, or cure. It still needs an independent, mechanically
pre-registered validation. `[M01, M05, A01 | Live, provisional]`

The score produced mixed results across therapies and datasets. Within its
small 19-person evidence set it survived several statistical stress tests,
and added model complexity did not improve it. Broader immune state also
attenuated the signal, so its interpretation is deliberately bounded. `[M02,
M03, M04, D02 | Live, provisional]`

The project also established useful context and closures:

- MS and ulcerative colitis had the strongest genome-wide genetic relationship
  among the autoimmune comparators tested here, but this is known context, not
  a transferable target. `[G01 | Robust context]`
- ZMIZ1 is a supported direction-decoupling warning: the same expression
  direction pointed oppositely in MS and Crohn. It is not a promoted target or
  a closed biological result. `[G02 | Supported decoupling]`
- KIF21B/GPR25 and PTGER4 target routes closed or were demoted because the
  causal gene or required therapeutic direction remained unresolved or hard to
  achieve. A structurally drug-like protein is not enough when protection
  appears to require restoring or increasing function. `[G03, G04, G05 |
  Closed or demoted]`
- A coupled antigen-presentation and immune-tone architecture recurs across
  data already stored in this repository (“held data”), but it did not become a
  target or a better prediction rule. `[D01, D02 | Supported context plus
  negative]`
- A joint search across the assembled corpus recovered known immune structure
  but found no unexpected signal that passed held-out validation. This bounds
  further unconstrained mining of this corpus; it does not claim that all
  computation or all future public data are exhausted. `[D04, D05 | Corpus
  boundary]`

### What Is Still Missing?

For progression, the project lacks the crucial kind of dataset: repeated
molecular measurements connected to repeated, confirmed disability outcomes.
The held datasets are closer to still photographs than a movie, so they cannot
identify a relapsing-to-progressive transition. No progression biomarker,
mechanism, target, treatment effect, or way to halt MS was established. `[P01,
P02, P03 | Data blocked and negative]`

An exact two-gene microglial state, CD44/CXCR4, is fixed as a future candidate
for the right longitudinal dataset. Its identity is supported; progression
prediction is not. It must not be applied to blood-based datasets as a proxy or
treated as a target. `[P06, C01 | Live, data-gated]`

### Where Could A Fresh Mind Help?

The open frontier is not "name another MS gene." It is to help solve puzzles
such as:

1. How can a small-cohort monitoring signal be validated without fooling
   ourselves?
2. What data design can distinguish progression from relapse and static
   disease stage?
3. How should therapy be approached when genetics implies restoration rather
   than inhibition?
4. Can a coupled biological system be tested without converting correlation
   into a multi-target story?
5. How can source and batch confounding be detected before an exciting pattern
   is interpreted?

These are developed in the
[Open Problems for Collaborators](OPEN_PROBLEMS_FOR_COLLABORATORS.md). The
claim IDs above point directly to the controlling evidence.

---

## The Fifteen-Minute Version

### 1. The Research Question Has Two Layers

MS can produce episodes of inflammatory activity and also accumulating
disability. A treatment can affect one without this project having established
an effect on the other. Therefore the repository keeps three questions
separate: `[B02, M05]`

1. **Monitoring:** can a molecular measurement report an early treatment
   response?
2. **Mechanism or target:** does the measurement identify something that
   should be changed therapeutically?
3. **Progression:** does changing it prevent or slow confirmed disability
   accumulation?

The project has a provisional answer only to the first question. It has not
crossed the evidence gap to the second or third.

### 2. What "Grounded" Does And Does Not Mean

A project-grounded result has a data trail and rerunnable analysis. A
provisional result can be grounded internally while still lacking independent
validation. A negative result can be strongly grounded. Conversely, a
plausible literature statement or fluent model answer remains outside-source
context until the project tests it. `[E01, E02, E03]`

This distinction prevents three common errors:

- repeating the same analysis many ways and calling that an independent
  replication;
- converting association into causation or a drug target;
- interpreting missing data as proof that a biological process does not
  exist.

### 3. Research Arc One: Genetics Found Biology, Then Direction Closed Routes

The genetics program compared MS with other immune diseases and examined
specific loci. The strongest genome-wide comparator in the tested set was
ulcerative colitis. That gives a backdrop for shared immune biology, but it is
low-novelty context and does not transfer a therapy from one disease to the
other. `[G01 | Robust context]`

Locus-level results exposed why target selection is harder than finding a
statistical association:

- **ZMIZ1:** an expression-increasing direction aligned with higher MS risk
  but lower Crohn risk. Shared location did not mean shared therapeutic
  direction. `[G02 | Supported decoupling]`
- **KIF21B/GPR25 region:** the region appears biologically real, but the causal
  gene remains uncertain and the protective implication points toward hard
  restoration or up-function logic. Predicted structure did not reverse that
  directional problem. `[G03 | Closed on direction]`
- **PTGER4:** attractive receptor pharmacology could not resolve multiple
  genetic signals and conflicting disease directions. `[G04 | Closed on
  direction]`
- **GPR25:** an early favorite was demoted after denser immune-QTL and direction
  review. That does not prove irrelevance; it means the evidence does not
  support actionability. `[G05 | Closed on evidence]`

**General lesson:** "Can a molecule bind this protein?" is not enough. The
required question is "Can the available modality change the right function in
the direction genetics requires, in the relevant cell and state?" `[G03,
G04]`

### 4. Research Arc Two: A Bounded Monitoring Signal Survived, With Caveats

The live score measures the change from baseline to an early on-treatment
sample in a fixed set of antigen-presentation genes. In plain language, it is
closer to a dashboard indicator of immune remodeling than a steering control
for treatment. The metaphor is limited: a dashboard reading can correlate
with response without explaining the mechanism. `[M01, M05]`

Its evidence is encouraging but small and bounded:

- In the pooled 19-person evidence set, the fixed score reached AUC 0.811 with
  permutation `p=0.008`. `[M03]`
- Alternative implementations gave similar conclusions, while more flexible
  models were unstable and did not improve validated performance. `[M03,
  D02]`
- The rule did not work uniformly across all tested therapies or diseases.
  `[M02]`
- Tested steroid-response and simple marker-composition panels did not explain
  it. After adjustment for broad metabolic, inflammatory, and STAT1/immune
  state, the same score weakened to AUC 0.656 with `p=0.163`. Direct steroid
  metadata were not available. `[M04]`

The honest label is therefore **live, provisional, and immune-tone bounded**.
The next test is already frozen: apply the locked rule to a properly paired
external cohort without tuning it after outcomes are visible. A pass, fail, or
inconclusive result will be interpreted by rules already fixed before the data
are seen. `[A01]`

### 5. Research Arc Three: More Complexity Did Not Create A Better Answer

Across held data, HLA-II antigen presentation, IFN/APC state, MIF/CD74-related
state, an interferon readout, and lysosomal processing repeatedly moved as a
coupled architecture. This is supported as bounded mechanistic context. It is
not a validated causal network or intervention recipe. `[D01]`

Adding those coupled features did not improve the simple monitoring scalar.
A broader patient-level simulator also could not be validated for individual
prediction or unseen-pathway simulation. These are real negative results, not
unfinished positive claims. `[D02, D03]`

Finally, a joint multi-modal analysis assembled 985 rows, 71 entities, and 14
modalities. It recovered known APC/immune-tone structure, but none of 22
unexpected candidates passed both recurrence and held-out-modality gates. The
corpus-specific 95% upper bound for a hidden extractable candidate under that
gate was 0.127. This number is a search-boundary estimate, not a biological
effect-size limit. `[D04, D05]`

### 6. Research Arc Four: Progression Exposed A Data-Design Wall

The progression program audited seven datasets and ten known packages. None
contained the complete chain needed to test progression properly: repeated
molecular state, a changing clinical stage or treatment context, and repeated
confirmed-disability outcomes. None qualified for all three pre-defined dataset
roles: longitudinal progression, compatible biological compartment, or
functional direction. `[P01, P03, P05]`

Several apparent signals weakened under harder checks:

- A CD44/CXCR4-high microglial state reproduced in bounded MS comparisons,
  but one discovery partition was strongly imbalanced by brain bank. The
  disease label and brain-bank source were strongly entangled (Cramer's V
  0.773), and source-adjusted evidence attenuated. `[C01, C02]`
- A morphology-linked OXPHOS/lysosomal pattern was downgraded after global
  multiple-testing and within-donor checks. `[P04]`
- No tested module became a portable progression-stage marker, and no
  intervention candidate cleared the direction and evidence gates. `[P02]`

The result is not "progression biology is absent." It is "the held design
cannot identify the transition or establish a progression target." That
difference is central. `[P01, P02, P03]`

The exact CD44/CXCR4 microglia score remains frozen as an identity-only
candidate for a future longitudinal, microglia-compatible cohort. It cannot be
silently replaced by a blood proxy, another gene pair, or a threshold chosen
after seeing disability outcomes. `[P06, A02]`

### 7. Where The Walls Actually Are

| wall | why it matters | what would move it |
|---|---|---|
| **Independent validation is missing** `[A01]` | Internal robustness cannot substitute for a new cohort. | Paired baseline and early-treatment samples with compatible genes and a fixed response outcome, analyzed under the preregistration. |
| **Progression needs a movie, not snapshots** `[P01, P03]` | Cross-sectional disease labels cannot identify within-person disability transition. | Repeated molecular and confirmed-disability measurements with time and provenance. |
| **Therapeutic direction is unfavorable or uncertain** `[G02-G05]` | Inhibition is not useful when protection may require restoring function, and a binding pocket cannot decide direction. | Signal-specific causal-gene resolution plus a feasible, direction-matched modality. |
| **Immune tone can masquerade as specificity** `[M04]` | A predictive score may summarize broad state rather than one mechanism. | External validation with pre-specified confounder reporting and richer metadata. |
| **Source can masquerade as disease** `[C02]` | Brain bank, site, or acquisition effects can align with labels. | Source-balanced donor replication and diagnostics fixed before interpretation. |
| **The same corpus has a search ceiling** `[D04, D05]` | Flexible mining can manufacture structure after the obvious signal is extracted. | Genuinely new data or a targeted test fixed independently of outcomes. |

### 8. The Candid Bottom Line

The project has **not** produced a cure, progression-stopping mechanism,
intervention-grade target, clinical biomarker, or validated treatment
selector. `[M01, M05, P02]`

It has produced:

- one bounded monitoring signal worth an independent frozen validation;
- several reproducible biological contexts and decouplings;
- a documented set of attractive routes that failed direction, specificity,
  validation, or data-design tests;
- a precise progression-data request rather than an overclaimed progression
  result; and
- reusable infrastructure for testing incoming cohorts without post-hoc rule
  changes. `[M01-M05, G01-G05, D01-D05, P01-P06, A01, A02]`

The most defensible near-term impact is monitoring and stratification
research. The target-level and progression-stopping prize requires new,
correctly designed evidence. `[D05, P01, A01, A02]`

---

## Go Deeper

| question | start here |
|---|---|
| What is the complete scored state of the project? | [Findings Report V37](../reports/FINDINGS_REPORT_V37.md) |
| What is the honest therapeutic path? | [Therapeutic Path V52](../reports/THERAPEUTIC_PATH_V52.md) |
| What exactly supports and limits the monitoring score? | [Finding V22](../findings/FINDING_V22.md), [Robustness Map V28](../workups/treatment_response/ROBUSTNESS_MAP_V28.md), [Confounder Audit V32](../workups/treatment_response/CONFOUNDER_AUDIT_V32.md) |
| Why did joint public-data mining stop? | [Joint Inference V41](../history/JOINT_INFERENCE_V41.md) |
| What did the progression program establish? | [Progression Frontier V54](../history/PROGRESSION_FRONTIER_V54.md), [V54 Run Summary](../history/V54_RUN_SUMMARY.md) |
| What was the brain-bank confounding lesson? | [Microglia Source-Balance Addendum V53](../validation/MS_MICROGLIA_SOURCE_BALANCE_ADDENDUM_V53.md) |
| How are evidence types separated? | [Epistemic Classes](../knowledge/EPISTEMIC_CLASSES.md), [External Context Index](../../knowledge_external/INDEX.md) |
| What controls every sentence on this page? | [V55 Claim-Source Matrix](CLAIM_SOURCE_MATRIX_V55.md), [machine-readable rows](ONBOARDING_CLAIM_SOURCES_V55.tsv) |
| How can I propose a useful direction? | [Open Problems](OPEN_PROBLEMS_FOR_COLLABORATORS.md), [Contribution Guide](HOW_TO_CONTRIBUTE_IDEAS.md) |
| What do unfamiliar terms mean? | [Plain-Language Glossary](GLOSSARY.md) |

## A Useful Reading Habit

Whenever you encounter an exciting statement in this repository, ask four
questions:

1. What is its status?
2. What exact data and analysis support it?
3. What would falsify it?
4. Is it a monitoring association, a mechanism, a target, or a progression
   outcome?

That habit is more valuable to this project than domain vocabulary. It lets a
new collaborator contribute creative directions without accidentally turning
a bounded result into a larger claim.
