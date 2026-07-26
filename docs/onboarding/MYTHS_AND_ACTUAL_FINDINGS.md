# Tempting Overreads vs What The Project Actually Found

This page is a misuse-prevention guide. The left-hand statements are not claims
made by the project; they are plausible but wrong upgrades a newcomer might
infer. The corrections on the right are bounded by the
[V55 claim-source contract](CLAIM_SOURCE_MATRIX_V55.md).

## The Live Monitoring Lead

### “The project has a validated MS biomarker.”

**What it actually found:** One fixed APC/HLA-II early-change score has bounded
internal support as a **provisional monitoring signal**. Its evidence set is
small, its generalization is mixed, broader immune tone attenuates it, and an
independent validation has not run. `[M01-M04]`

**What would change the status:** A pass under the frozen outside-validation
plan would strengthen the monitoring association. It would still not establish
clinical utility by itself. `[A01]`

### “The score can choose the right treatment.”

**What it actually found:** The score was evaluated as an early response-
monitoring signal. It has not shown that it selects among treatments, improves a
decision, or benefits patients. `[M01, M05]`

**What would be needed:** A separate prospective decision-impact design, after
independent validation, with an explicitly defined action and clinical outcome.

### “HLA-II/APC is the drug target.”

**What it actually found:** HLA-II/APC genes contribute to a score and recurring
immune architecture. A measurement that tracks treatment-associated change is
not evidence that directly increasing or decreasing that pathway will help.
`[M05, D01]`

**What would be needed:** Direction-resolved causal perturbation evidence in the
relevant cell/state, followed by outcome evidence. Monitoring alone cannot
supply this.

### “The score is either a steroid artifact or definitely independent of steroids.”

**What it actually found:** A tested glucocorticoid-response proxy did not
explain the score, but direct steroid-exposure metadata were unavailable. The
project can reject the tested proxy explanation, not every possible steroid
effect. `[M04]`

**What would be needed:** Direct, timed steroid-exposure metadata in a compatible
external cohort, analyzed under a pre-specified adjustment.

### “The signal is a pure APC/HLA-II mechanism.”

**What it actually found:** Broader metabolic, inflammatory, and STAT1/immune-
tone adjustment attenuated the result. The honest interpretation is partially
confounded or immune-tone bounded, not a pure mechanism. `[M04]`

**What would be needed:** Replication with richer state and composition
measurements showing separable predictive value without changing the locked
score.

### “A more sophisticated model should outperform the simple score.”

**What it actually found:** Tested flexible, coupled-axis, receptor-only, and
generic dynamic alternatives did not improve validated performance and were
often less stable in the small data. `[M03, D02]`

**What it does not mean:** Simplicity is universally superior. It means model
complexity did not earn an upgrade in these data. New data could support a new,
separately frozen model.

## Genetics And Targets

### “MS and ulcerative colitis share genetics, so an ulcerative-colitis target should work in MS.”

**What it actually found:** Ulcerative colitis was the strongest genome-wide
comparator among the diseases tested here. That is useful, low-novelty context,
not a target-transfer rule. `[G01]`

**Why the shortcut fails:** Shared genome-wide architecture does not establish
the same causal gene, cell state, effect direction, or therapeutic modality at a
particular locus.

### “A shared autoimmune locus points in the same therapeutic direction.”

**What it actually found:** At ZMIZ1, an expression-increasing direction aligned
with higher MS risk but lower Crohn risk. This is a concrete decoupling warning.
`[G02]`

**What would be needed:** Signal-specific, cell-specific causal direction in MS;
another disease's direction cannot substitute.

### “GPR25 is a GPCR with a predicted structure, so it is an obvious target.”

**What it actually found:** GPR25 was demoted after denser immune-QTL and
direction review. At the chr1 region, causal-gene uncertainty remains and the
protective implication points toward hard restoration or up-function logic.
Predicted structure informs geometry; it does not resolve those issues. `[G03,
G05]`

**What would reopen it:** Signal-specific causal-gene resolution plus a feasible
modality that produces the required sign in the relevant cell/state.

### “PTGER4 is druggable, so the genetics conflict is a detail.”

**What it actually found:** Multiple signals and conflicting disease directions
closed PTGER4 as a simple shared target. Pharmacological familiarity cannot
repair causal ambiguity. `[G04]`

**What would reopen it:** Signal-specific cell-type QTL evidence with a
direction favorable for MS and a matching modality.

### “A wrong-direction locus is scientifically useless.”

**What it actually found:** Wrong or unresolved direction can close a
therapeutic route while preserving useful biology and a decision rule for where
not to spend. `[G02-G05]`

**Why this matters:** A negative target verdict can be robust and useful even
when relevance or novelty is modest.

## Systems, Models, And Computation

### “The coupled APC axis is a validated multi-target intervention.”

**What it actually found:** Several APC/immune-state components recur together
as bounded mechanistic context. Co-movement does not identify control points,
causal edges, or a useful drug combination. `[D01]`

**What would be needed:** Perturbations that distinguish drivers, readouts,
feedback, and redundant nodes, with a direction-matched functional outcome.

### “The immune simulator can predict individual patients.”

**What it actually found:** A broad patient-level immune-state simulator could
not be validated for individual prediction or unseen-pathway simulation. `[D03]`

**What remains possible:** Bounded directional priors or method development,
clearly separated from patient prediction.

### “Public-data computation is exhausted forever.”

**What it actually found:** In the assembled held corpus, none of 22 unexpected
joint candidates passed recurrence plus held-out validation, with a corpus-
specific upper bound of 0.127 under that gate. `[D04]`

**What it means:** More unconstrained mining of the same assembled evidence is
not the rational discovery step. Genuinely new data, targeted validation, and
new prospective tests remain in scope. `[D05]`

### “AI models agreed, so the idea has independent evidence.”

**What it actually found:** Claude, Gemini, and RPT are proposal and critique
lenses. Agreement can prioritize a test; it is not evidence. `[E03]`

**What would change status:** The concrete proposal must be implemented and
tested on real data under the same evidence gate as any human idea.

### “Synthetic simulations prove the biological effect is large enough.”

**What they actually show:** Seeded synthetic cohorts characterize method power,
false positives, and robustness under chosen assumptions. They do not estimate
the real MS effect or predict the outcome of a specific external cohort. `[A03]`

**Proper use:** Plan sample size, interpret an inconclusive result, and expose
method failure conditions.

## Progression And CNS Results

### “The project found no progression biology.”

**What it actually found:** The held corpus lacks a usable longitudinal
molecular-to-confirmed-disability design. No portable progression marker,
transition, mechanism, target, or treatment effect was established **under that
coverage**. Missing design is not biological absence. `[P01-P03]`

**What would change the boundary:** Repeated molecular state and confirmed
disability in the same people, with timing, treatment, attendance, source, and
quality provenance. `[A02]`

### “CD44/CXCR4 is a progression biomarker or therapeutic target.”

**What it actually found:** An exact CD44/CXCR4 microglial state has bounded
identity support and is fixed as a candidate for the correct future progression
dataset. Progression prediction, causality, and target status are untested.
`[P06, C01]`

**Non-negotiable boundary:** Do not substitute PBMC, whole blood, other genes,
or outcome-chosen thresholds.

### “The brain-bank confound invalidates all microglia findings.”

**What it actually found:** One discovery partition had strong brain-bank/
disease imbalance and attenuated after source-aware checks. Other bounded
analyses supported the state identity. The lesson is to qualify and replicate,
not to discard every brain-bank result. `[C01, C02]`

**What would resolve it:** A source-balanced, donor-aware replication with the
same score fixed beforehand.

### “Lesion morphology established a progression mechanism.”

**What it actually found:** An initially interesting OXPHOS/lysosomal morphology
pattern was downgraded after global multiple-testing and within-donor checks.
It remains exploratory rather than a progression mechanism or target. `[P04]`

**What would be needed:** Orthogonal donor-aware replication plus a separate
functional-direction test.

## Evidence And External Knowledge

### “Published or consensus knowledge is automatically stronger than a rerunnable project result.”

**What the repository does:** Outside-source material is kept in a separate
context layer with provenance. Agreement can orient confidence and disagreement
can flag a tension, but neither silently changes a project-grounded result.
`[E02]`

**Why:** A citation and a rerunnable analysis answer different provenance
questions. The repository preserves both without letting one borrow the other's
authority.

### “No recorded external contradiction means the project matches consensus.”

**What it actually means:** The external catalog is incomplete and relationship
classification depends on sufficiently specific overlap. Zero contradictions
in a table is not evidence of universal consensus. `[E02]`

### “A closed lead should disappear from the public story.”

**What this project does:** Closed and negative routes stay visible because they
prevent repeated work, reveal failure modes, and state exactly what evidence
would reopen them. `[G03-G05, D02, D03, P04]`

## The Short Version

| tempting upgrade | bounded truth |
|---|---|
| monitor → target | A state indicator does not identify a control point. |
| association → cause | Direction and intervention evidence are separate. |
| internal robustness → independent validation | A new cohort is still required. |
| data missing → biology absent | The question may be unidentifiable here. |
| structure → druggability | Geometry does not solve causal gene or direction. |
| correlation network → control system | Perturbation and identifiability are required. |
| synthetic behavior → MS evidence | Simulation characterizes methods, not biology. |
| model agreement → evidence | Agreement only orders the grounding queue. |
| closed → irrelevant | Closure can preserve useful biology and stop-spending value. |

When in doubt, use the weaker statement and follow its claim ID to the source.
The repository's usefulness depends more on preserving these boundaries than on
making every result sound important.
