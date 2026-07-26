# Frequently Asked Questions

This page gives short answers for new readers. Bracketed IDs point to the
[claim-source contract](CLAIM_SOURCE_MATRIX_V55.md), where each statement is
bounded by its controlling project artifacts and a forbidden overread.

## The Project In One Minute

### What is this repository trying to do?

It is an autonomous computational research project that tests questions about
multiple sclerosis (MS) against data and keeps the results rerunnable. Its
long-term motivation is meaningful MS impact, especially disability
progression. Its current evidence does **not** contain a cure, an established
drug target, or a progression mechanism. `[E01, P01, P02]`

### What is the strongest live result?

A fixed score based on early changes in APC/HLA-II-related blood expression is
the one live clinical lead. It may be useful for **monitoring** whether biology
changes after treatment. It has encouraging but small internal evidence and
still needs a correctly structured independent cohort. It is not yet a
validated biomarker or clinical tool. `[M01-M04, A01]`

### Does that score tell doctors which treatment to prescribe?

No. A monitoring signal can describe a treatment-associated change without
identifying a causal drug target, proving efficacy, or selecting the right
treatment for a person. `[M05]`

### Did the project find a way to halt MS progression?

No. It found that the held data lack the longitudinal molecular and confirmed-
disability measurements needed to answer that question properly. That is a
data boundary, not evidence that progression biology does not exist. `[P01-P05]`

## Evidence And Trust

### What does “grounded” mean here?

It means the result was produced by a committed analysis that can be rerun on
data available to the project. Grounding does not automatically mean external
validation, causality, clinical usefulness, or high certainty; those are
separate questions. `[E01]`

### What does “provisional” mean?

There is some internal evidence, but a decisive outside test is still missing.
The live monitoring score is provisional for exactly this reason. `[E01, M01]`

### How is literature or database knowledge handled?

Outside-source material lives in a separate knowledge area with source and
status attached. It can provide context or motivate a future test, but a
citation alone cannot become evidence produced by this project or alter a
rerunnable result. `[E02]`

### Are Claude, Gemini, or RPT treated as scientific authorities?

No. Models can suggest questions, identify confusing wording, or challenge an
analysis. Their output counts only as a proposal until the project checks it
against artifacts or real data. Model agreement is not biological evidence.
`[E03]`

### Are AlphaFold structures experimental evidence?

No. They are confidence-scored predictions stored as outside-source context.
They can inform which structural questions or assays are worth considering,
but they cannot establish target tractability or override the genetics
direction. See the [evidence-class definitions](../knowledge/EPISTEMIC_CLASSES.md).

### Does “statistically significant” mean clinically useful?

No. Statistical separation in a small internal dataset does not establish
transportability, clinical utility, treatment selection, or patient benefit.
The monitoring result still requires frozen external validation. `[M01, M03,
A01]`

## What Was Tried

### Why were several genetics leads closed or demoted?

The main problems were not simply weak association. They included uncertainty
about the causal gene, opposite directions across diseases, and a protective
direction that appears to require restoring or increasing function rather than
ordinary inhibition. A familiar protein class or predicted pocket does not
solve those direction problems. `[G02-G05]`

### Is ZMIZ1 a closed lead?

Not in the same sense as a closed target route. The supported result is a
**decoupling warning**: the same expression-increasing direction was associated
with higher MS risk and lower Crohn risk. That makes simple cross-disease target
transfer unsafe; it does not prove ZMIZ1 irrelevant. `[G02]`

### What happened to KIF21B and GPR25?

The chr1 region still appears biologically real, but causal-gene uncertainty
and an apparent restoration or up-function requirement keep it therapeutically
closed. GPR25 was specifically demoted after denser immune-QTL and direction
review. `[G03, G05]`

### Why did a more complicated model not replace the simple score?

In the held small datasets, coupled-axis features and flexible multifeature
models did not improve the locked scalar under the project’s validation rules.
That is a bounded negative: it does not prove that complexity can never help
with genuinely new and larger data. `[D01-D02]`

### Did the patient simulator work?

No. The held data could not support broad patient-level prediction or
unseen-pathway simulation. Bounded directional modeling may still be useful,
but the proposed simulator was not validated. `[D03]`

### Did joint analysis of all the held data find a hidden target?

No. It recovered known APC and immune-tone structure, but zero of 22 unexpected
candidates passed the combined recurrence and held-out-modality gate. The
reported 0.127 upper bound applies to that assembled corpus and testing gate;
it is not a universal biological effect limit or a ban on analyzing new data.
`[D04-D05]`

## Progression

### Why distinguish relapse from progression?

A relapse is an episode of inflammatory activity; progression concerns
disability accumulating and remaining over time. They can be related, but they
are not interchangeable outcomes and require different study designs. `[B02]`

### Why can’t cross-sectional brain data settle progression?

Snapshots can identify cell states or lesion-associated differences, but they
do not show that an earlier molecular state predicts later confirmed disability
in the same people. The needed “movie” includes repeated molecular measurement,
repeated disability outcomes, timing, and provenance. `[P01, P03, P05]`

### Is the CD44/CXCR4 microglia result a progression biomarker?

No. A bounded MS-associated microglial state was reproduced, with an important
brain-bank/source caveat. The exact two-gene state is only a future
progression-candidate identity; progression prediction is untested, and blood
or substitute-gene proxies are not permitted. `[C01-C02, P06]`

### What was the “brain-bank lesson”?

In one partition, tissue source and diagnosis were strongly entangled, so a
source effect could resemble a disease effect. Adjustment weakened the result.
This teaches the pipeline to test source balance before interpreting a
localization claim; it does not make every brain-bank study invalid. `[C01-C02]`

## Validation And Data

### What external validation is planned for the monitoring score?

The plan is a mechanical run of a rule frozen before seeing the validation
data. It requires paired baseline and early-treatment measurements, the needed
genes, a compatible outcome, and adequate metadata. Pass, fail, and
inconclusive interpretations are precommitted. `[A01]`

### Why might a small validation cohort be inconclusive?

Seeded method simulations show that a very small cohort may produce a wide
uncertainty interval unless the true separation is large and labels are clean.
Those simulations characterize method behavior, not MS biology and not the
effect expected in Gafson. `[A03]`

### Is the Gafson cohort already in the repository?

No validation-ready Gafson package is counted as acquired. Gafson remains an
access path; Karolinska still requires response-label mapping. The project does
not count a cohort as usable until pairing, outcome labels, module-gene
coverage, provenance, and use terms are verified. `[A04]`

### Can a contributor send a dataset?

Yes, if they have the legal right to do so. Start with metadata and access/use
terms rather than transferring sensitive rows. The project needs to establish
people, pairing, timepoints, outcome definition, assay/gene coverage, source or
batch fields, and permitted use before analysis. See [How to contribute
ideas](HOW_TO_CONTRIBUTE_IDEAS.md).

### What if data cannot leave its institution?

A holder-side or federated run may be possible if the frozen calculation,
pairing, quality diagnostics, and sufficient aggregate outputs remain
auditable. This is an engineering direction, not evidence that a particular
restricted cohort is currently usable. See [Problem 2](OPEN_PROBLEMS_FOR_COLLABORATORS.md#problem-2-remove-dependence-on-one-hard-to-access-cohort).

## Nulls, Closures, And New Ideas

### Why publish negative results and dead ends?

They prevent repeated spending on routes already tested, reveal where an
interpretation failed, and make future ideas more precise. A well-controlled
negative can be more decision-useful than an attractive but unvalidated lead.
`[D02-D05, G03-G05, P02, P04]`

### Can a closed lead ever reopen?

Yes, but only with evidence that addresses the reason it closed. For example,
PTGER4 would need signal-specific, cell-type-relevant causal evidence with a
favorable MS direction; a new citation or a pocket prediction is not enough.
`[G04]`

### Does “public-data discovery is exhausted” mean no one should compute more?

No. It means unconstrained mining of the same assembled corpus is not the
rational next discovery step under the tested gate. Targeted validation,
quality work, method audits, and analysis of genuinely new data remain useful.
`[D04-D05]`

### What kind of outsider idea is useful?

One that changes an observable prediction and can be tested fairly. State the
claim, why it differs from tried work, the data needed, the null or comparator,
the main confounder, and the result that would make you abandon the idea. Start
with the [open-problem board](OPEN_PROBLEMS_FOR_COLLABORATORS.md) or the
[role routes](COLLABORATOR_ROUTES.md).

### What ideas are unlikely to help?

Examples include proposing a target from association alone, defaulting to
inhibition when genetics implies restoration, re-optimizing the locked score on
the validation cohort, calling a predicted structure experimental, replacing
progression with relapse, or using a model’s confidence as evidence. The
[myths page](MYTHS_AND_ACTUAL_FINDINGS.md) lists more common overreads.

## Safety And Participation

### Is this medical advice?

No. The repository is research software and documentation. It does not provide
individual diagnosis, prognosis, treatment choice, or instructions to change
medication. Medical decisions belong with qualified clinicians who know the
person and the full clinical context.

### Do I need medical training to contribute?

No. Engineering, statistics, data stewardship, systems thinking, chemistry,
privacy, design, and communication can all contribute. Domain expertise still
matters when defining clinical outcomes and interpreting biology. Use the
[collaborator routes](COLLABORATOR_ROUTES.md) to find a bounded starting point.

### How should I submit an idea?

Use the [copy-ready idea template](HOW_TO_CONTRIBUTE_IDEAS.md#copy-ready-idea-template)
or open a **Research direction** issue. A useful submission includes a
falsifiable prediction, reachable data, comparator/null, confounder plan,
decision consequence, provenance, and explicit failure condition.

### Where should I go next?

- Read the [two-minute explanation](MS_RESEARCH_EXPLAINED.md#the-two-minute-version).
- Scan the [visual guide](VISUAL_INDEX.md).
- Pick an [open problem](OPEN_PROBLEMS_FOR_COLLABORATORS.md).
- Check the [lead status cards](LEAD_STATUS_CARDS.md) before proposing a target.
- Use the [glossary](GLOSSARY.md) whenever a term is unclear.

