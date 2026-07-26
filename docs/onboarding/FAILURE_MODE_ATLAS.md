# Why Good-Looking Research Leads Fail

Failures are part of the project’s evidence, not an embarrassing appendix. This
atlas helps newcomers distinguish **why** a route failed, what remains true,
and what kind of new input could change the verdict.

A closed interpretation is not the same as irrelevant biology. “Not a target,”
“not specific,” “not validated,” and “not identifiable with these data” are
different outcomes.

## The Pattern Across Failures

The project formally compared 20 killed, closed, parked, or decoupled items. It
did **not** find one universal reason MS leads fail.

The strongest bounded pattern was context or axis dependence among cross-axis
transfer failures: all four such rows carried that pattern, versus 1.4 expected
under random assignment (`p=0.007224`). Direction/modality constraints were
common in target-like routes but only suggestive in this small frame
(`p=0.077657`). These are project-specific failure patterns and practical
prefilters, not universal laws of MS. `[F01]`

## A Quick Decoder

| verdict | plain meaning | what remains possible |
|---|---|---|
| `wrong or unresolved direction` | We do not know how to change the route beneficially, or the apparent protective action is hard to deliver. | Direction-specific causal and functional evidence could reopen it. |
| `causal entity unresolved` | The associated region is real, but the responsible gene or signal is not identified. | Signal-specific cell-relevant evidence could separate candidates. |
| `context-dependent` | A relationship does not transfer cleanly across disease, therapy, tissue, cell, or stage. | A bounded use in the right context may remain. |
| `not specific` | Broad immune tone, source, composition, or another process can produce a similar pattern. | A source-balanced, discriminating test may recover a narrower claim. |
| `complexity did not help` | A larger model fit more detail but did not improve fair held-out behavior. | New independent data may justify a new development test, not a post-hoc rescue. |
| `validation missing or weak` | Internal evidence exists, but no untouched compatible cohort has tested it decisively. | Frozen external validation can pass, fail, or remain inconclusive. |
| `data design cannot answer` | Required people, timing, outcome, compartment, or provenance are absent. | Acquire the missing design; do not substitute a convenient proxy. |
| `category error` | A monitor, association, structure, or model proposal was being asked to prove a target or treatment effect. | Keep the bounded use and test the missing causal layer separately. |

## Failure Mode 1: The Direction Is Wrong Or Hard To Deliver

### The tempting shortcut

> The locus is associated and the protein class is familiar, so inhibit it.

### What actually fails

Genetics can imply that protection requires **more**, restored, or context-
specific function. An inhibitor then acts in the wrong direction. Even when the
sign is known, the relevant cell/state and feasible delivery may remain
unresolved.

### Project examples

- The chr1 KIF21B/GPR25 region remains biologically real but therapeutically
  closed by causal-gene ambiguity and an apparent restoration/up-function
  requirement. `[G03, G05]`
- PTGER4’s familiar receptor biology did not rescue conflicting signals and
  disease directions. `[G04]`

### What would change the answer

Signal-specific causal assignment, allele-aligned functional direction in the
relevant cell/state, and an assay showing that a feasible modality produces the
required sign rather than its opposite.

### Useful outsider input

Gain/restoration modalities, direction-matched assay design, targeted delivery,
or a falsification test that compares increase and decrease rather than assuming
inhibition.

## Failure Mode 2: The Region Is Real, But The Causal Entity Is Not

### The tempting shortcut

> Pick the nearest or most drug-like gene at an associated locus.

### What actually fails

A locus can contain several genes and association signals. Expression support,
protein class, and a pocket can all be true while the causal gene remains
unknown. Acting on the wrong gene converts real genetics into a false target.

### Project examples

- GPR25 was demoted after denser immune-QTL and direction review; chr1 biology
  was not declared irrelevant. `[G03, G05]`
- PTGER4 could not be reduced to one clean shared MS-UC signal. `[G04]`
- ZMIZ1 is a supported opposite-direction cross-disease warning, not a target
  nomination. `[G02]`

### What would change the answer

Fine-mapped, signal-specific evidence that joins disease association to a
cell-relevant molecular effect with aligned alleles and a therapeutic sign.

### Useful outsider input

Causal-graph comparison, fine-mapping uncertainty propagation, allele
harmonization audits, or experimental designs that discriminate genes at the
same locus.

## Failure Mode 3: The Relationship Depends On Context

### The tempting shortcut

> It appears in another disease, therapy, tissue, or cell, so it should transfer
> to MS.

### What actually fails

The same pathway can have different directions or roles across diseases and
states. A module that recurs as context may not predict response, identify a
target, or transfer to a new compartment.

### Project examples

- ZMIZ1 pointed in opposite MS and Crohn directions. `[G02]`
- The coupled APC architecture recurred, but adding it did not improve the
  locked monitoring score. `[D01-D02]`
- The V22 score was bounded rather than a broad cross-therapy rule. `[M02]`

### What would change the answer

A predeclared transfer test with matched measurement, outcome, timing, cell or
tissue, treatment context, and an explicit interaction or heterogeneity model.

### Useful outsider input

Domain-adaptation diagnostics, transportability analysis, hierarchical models,
or study designs that make context the variable under test rather than noise to
remove.

## Failure Mode 4: The Signal Is Not Specific Enough

### The tempting shortcut

> The named module moved, so the named mechanism caused the outcome.

### What actually fails

A gene-expression label is an interpretation, not proof of a unique mechanism.
Broad immune tone, cell mixture, processing batch, tissue source, or treatment
context can create overlapping patterns.

### Project examples

- Broad immune tone attenuated the monitoring score, so it remains partially
  confounded rather than a pure APC/HLA-II mechanism. `[M04]`
- Brain-bank/source imbalance weakened one microglia partition and now requires
  source-balanced replication. `[C01-C02]`

### What would change the answer

Overlap-aware design, balanced sources, negative-control modules, direct rather
than proxy metadata, and a test where the proposed mechanism and broad-context
alternative predict different results.

### Useful outsider input

Batch/source overlap metrics, causal missingness models, negative-control
selection, deconvolution audits, or fail-closed rules for non-identifiable
contrasts.

## Failure Mode 5: More Complexity Fits, But Does Not Validate

### The tempting shortcut

> Add more genes, latent factors, interactions, or a more powerful model.

### What actually fails

In tiny datasets, flexibility increases the number of ways to obtain an
attractive internal result. If improvement does not survive a fair holdout or
null that includes model selection, complexity has not added evidence.

### Project examples

- Coupled-axis and flexible multifeature variants did not improve the simple
  locked scalar. `[D02]`
- A broad patient-level simulator could not be validated. `[D03]`
- Joint inference recovered known structure but no unexpected candidate passed
  recurrence plus the held-out-modality gate. `[D04]`

### What would change the answer

A model frozen before an independent cohort and a null pipeline that repeats
the same search/selection process. Any new model needs a new untouched test.

### Useful outsider input

Selective-inference controls, nested validation, search-aware permutation,
minimum-description-length comparisons, or explicit abstention under small
samples.

## Failure Mode 6: The Result Has Not Met External Validation

### The tempting shortcut

> Many internal stress tests are equivalent to replication.

### What actually fails

Repeated views of the same people and outcomes share information. Tool
robustness can reveal implementation fragility, but it cannot measure transport
to new people, sites, platforms, or outcome processes.

### Project example

The APC/HLA-II score is internally supported and tool-robust within a bounded
19-person evidence set, yet remains provisional until a correctly structured
independent cohort runs the unchanged rule. `[M01, M03, A01]`

### What would change the answer

The frozen external test. A pass raises confidence, a fail narrows or closes the
lead, and a wide interval can remain honestly inconclusive.

### Useful outsider input

Cohort access, holder-side execution, small-sample uncertainty, label-quality
audits, or a design that extracts useful effect intervals without converting an
inconclusive result into success.

## Failure Mode 7: The Data Design Cannot Identify The Question

### The tempting shortcut

> Use the closest available dataset or outcome.

### What actually fails

Some questions require a specific order of measurement and unit of
independence. A cross-sectional stage label cannot show molecular prediction of
later disability. Postmortem morphology, relapse, PBMC, or a different score
cannot silently replace longitudinal progression data.

### Project examples

- The held corpus has no longitudinal molecular-to-confirmed-disability
  progression package. `[P01, P03, P05]`
- No fresh monitoring cohort is validation-ready merely from repository
  metadata; Gafson and Karolinska still have access/label requirements. `[A04]`

### What would change the answer

Acquire the exact missing people × time × outcome × modality design with
provenance and permitted use, or run the frozen calculation at the data holder.

### Useful outsider input

Metadata recovery, cohort contacts, privacy-preserving execution, study design,
or a formal proof of which reduced outputs remain sufficient.

## Failure Mode 8: The Question Asks One Evidence Type To Prove Another

### The tempting shortcuts

- A monitoring score identifies a target.
- A predicted pocket establishes druggability.
- Literature agreement changes a grounded result.
- Two models agreeing makes a mechanism likely.
- A synthetic power result estimates MS biology.

### What actually fails

Each input can be useful in its own lane, but none supplies the missing causal,
experimental, external-validation, or clinical layer. `[M05, E01-E03, A03]`

### What would change the answer

Name the missing layer and test it directly: causal perturbation, experimental
structure/binding, independent cohort, clinical-utility study, or real-data
grounding.

### Useful outsider input

Evidence graphs, argument mapping, interface safeguards, or test plans that make
category transitions explicit and prevent a contextual input from being
reported as a conclusion.

## Failure Modes Often Combine

A lead may be real at one level and blocked at several later levels. The chr1
route combines causal-gene uncertainty, hard direction, and weak modality fit.
The monitoring route combines internal support, immune-tone bounds, tiny
samples, and missing external validation. Progression work combines plausible
states with an absent longitudinal outcome design.

Do not ask only “Is the lead alive?” Ask:

1. What exact statement survived?
2. At which evidence transition did it fail?
3. Is the blocker analytical, data, causal, directional, experimental, or
   clinical?
4. What observation would directly remove that blocker?
5. What result would close the route more firmly?

## Before Re-Proposing A Closed Route

- Name the route and its documented failure reason.
- Show which assumption or evidence has changed.
- Preserve any surviving bounded biology.
- Test the required direction, context, and specificity before tractability.
- Include the failed/null outcome in the plan.
- Do not substitute a new model, citation, or structure for the missing evidence
  layer.

Use the [worked transformations](IDEA_TRANSFORMATIONS.md) to rewrite a proposal
and the [triage rubric](IDEA_TRIAGE_RUBRIC.md) to decide whether it is runnable,
data-gated, repairable, or still closed.
