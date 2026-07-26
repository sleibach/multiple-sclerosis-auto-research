# Case Study: Turning Outside Context Into A Groundable Test

Literature, public databases, expert opinion, and AI models can reveal a useful
question. They cannot become project evidence merely because they sound
authoritative or agree with an existing result.

This page explains the repository's conversion path from outside context to a
rerunnable test. It introduces no external scientific claim and no new project
finding. `[E01-E03]`

## The Short Version

```text
outside observation
    -> source-preserved context record
        -> exact prediction
            -> eligible project data and fixed test
                -> rerunnable result with its own status
```

Authority does not transfer across the arrows. The outside item remains
outside context. If the project later runs a fair test, that new analysis has
its own provenance, result, uncertainty, and evidence grade. `[E01-E02]`

Models follow the same rule. Claude, Gemini, or RPT may suggest a blind spot,
but confidence, eloquence, and cross-model agreement only help prioritize a
question. They do not answer it. `[E03]`

## Why Separation Matters

Without separation, three errors become easy:

1. A citation can make an untested statement look rerunnable here.
2. Agreement with a project result can be described as validation even when
   populations, outcomes, timing, or measurements do not overlap.
3. A model-generated explanation can acquire the tone of evidence despite
   having no data-grounded test.

The repository prevents those upgrades by keeping outside material in its own
tree and attaching provenance to every item.

## Stage 1: Preserve The Source

Before interpreting an outside item, record:

- the claim or annotation in a faithful paraphrase;
- source URL, citation, or stable identifier;
- date accessed;
- source type and access constraints;
- why the project can or cannot test it;
- its relationship to existing project findings; and
- an explicit marker that it is not project-grounded.

Do not copy an outside claim into a finding, locked rule, validation result, or
grounded report. A source link is necessary provenance, not a truth stamp.
`[E02]`

## Stage 2: Classify The Relationship Honestly

Compare the outside item with the exact bounded project claim:

| relationship | plain meaning | allowed consequence |
|---|---|---|
| Converges | The outside source appears to agree at a sufficiently similar level. | Note independent agreement and prioritize scrutiny; do not call it project evidence. |
| Contradicts | The outside source appears to disagree at a sufficiently similar level. | Flag the tension and ask what population, definition, timing, or design could explain it. |
| Orthogonal | It addresses a different layer or question. | Keep as context; do not force agreement or conflict. |
| Insufficient overlap | The terms sound related but cannot be compared fairly. | Acquire a sharper source or stop the comparison. |

The project result remains controlled by its rerunnable artifacts. Outside
agreement does not upgrade its grade, and outside disagreement does not
silently override it. `[E01-E02]`

## Stage 3: Remove The Authority Words

Turn the outside statement into a proposal by removing phrases such as:

- “is known to”;
- “proves”;
- “the model confirms”;
- “experts agree”; or
- “the database says this is druggable.”

Replace them with:

```text
If this outside statement applies to the project's population, compartment,
timing, and outcome, then the following pre-specified pattern should appear...
```

This makes the actual bridge visible.

## Stage 4: Build A Discriminating Prediction

A groundable proposal needs:

1. **Exact population and unit:** person, donor, sample, locus, gene, or module.
2. **Measurement and time:** what is observed and when.
3. **Expected direction:** higher, lower, restoration, interaction, or no
   difference.
4. **Comparator:** what the proposed explanation must beat.
5. **Competing explanation:** source, batch, immune tone, cell mix, linkage,
   context, or another mechanism.
6. **Null and correction:** how chance and search multiplicity are controlled.
7. **Holdout:** what information cannot shape the proposal and then validate it.
8. **Drop rule:** the result that closes or narrows the idea.

If those cannot be stated, the item remains context rather than an executable
direction.

## Stage 5: Check Whether The Data Match The Verb

Before analysis, ask:

- Does a monitoring claim have paired early-treatment samples and later
  response labels?
- Does a progression claim have repeated molecular state and later confirmed
  disability?
- Does a target claim have causal-gene, direction, perturbation, and modality
  evidence?
- Does a localization claim compare compatible compartments under the same
  phenotype and timing?
- Does a confound claim have enough source/outcome overlap to separate them?

If the data do not identify the verb, the correct result is **data blocked** or
**not identifiable**, not a flexible proxy test. More mining of the same held
corpus is also bounded by the V41 decision unless genuinely new data or a
targeted precommitted validation question is present. `[D05]`

## Stage 6: Run And Record A New Result Separately

A valid future test must produce:

- committed code and inputs or a reproducible acquisition manifest;
- fixed feature, outcome, split, null, correction, and decision rule;
- complete eligible results, including nulls and failed contexts;
- effect and uncertainty;
- confound and sensitivity checks appropriate to the design; and
- a result status that does not exceed the design.

Only this new project analysis can become project-grounded. The original
literature, database, or model item remains outside context and keeps its
source.

## Three Procedural Examples

These examples illustrate conversion mechanics. They are not new biological
hypotheses or findings.

### A Model Suggests A Confound

**Unsafe:** “Two models agree that source drives the signal, so it is an
artifact.”

**Groundable:** “Before interpreting the disease contrast, cross-tabulate
diagnosis by source, quantify overlap, compare raw and source-aware effects,
and run leave-source-out sensitivity under a fixed rule.”

The model supplied a question. The data supply the verdict.

### A Database Calls A Protein Druggable

**Unsafe:** “The target is actionable because a database lists ligands or a
predicted structure contains a pocket.”

**Groundable:** “First resolve the disease signal to this gene and cell state,
then establish the protective direction and test a modality that creates that
direction.”

The annotation supplies tractability context. It does not supply disease
causality or therapeutic direction.

### A Paper Reports A Similar Biomarker

**Unsafe:** “The published marker validates our monitor.”

**Groundable:** “Check whether the paper used the same population, treatment,
time window, compartment, module, and clinical outcome. If an accessible
person-level package exists, run the frozen rule without retuning.”

Similar words do not guarantee the same estimand.

## Red Flags That Stop Authority Transfer

- No stable source or access date.
- Only a search-result snippet or model summary is available.
- The outside population, outcome, time, or compartment is unclear.
- Agreement depends on broad pathway names rather than the same direction and
  measurement.
- A contradiction is resolved by declaring the outside source “more trusted.”
- A model proposal is cited as if it ran an experiment.
- A predicted structure is described as experimental structure.
- The proposed project test uses the same data to generate and confirm the
  pattern.
- A literature mention is used to reopen a closed route without the named
  missing causal/directional evidence.

## Copy-Ready Context-To-Test Card

```text
Outside source and access date:
Faithful contextual claim:
Project claim it may relate to:
Relationship: converges / contradicts / orthogonal / insufficient overlap
Why authority does not transfer:
Exact groundable prediction:
Required data and current access:
Independent unit and timing:
Comparator and competing explanation:
Null, correction, and holdout:
Drop or narrow rule:
Possible result statuses:
What even a positive result would not establish:
```

Store the outside source in the separate context tree. Submit the proposed test
through the [contribution guide](HOW_TO_CONTRIBUTE_IDEAS.md); do not move the
source into the grounded tree.

## Trace The Policy

- [Epistemic classes](../knowledge/EPISTEMIC_CLASSES.md)
- [Outside-context index](../../knowledge_external/INDEX.md)
- [Contribution guide](HOW_TO_CONTRIBUTE_IDEAS.md)
- [Evidence-journey visual and text](VISUAL_INDEX.md#7-how-an-idea-reaches-a-decision)
- [Claim-source contract](CLAIM_SOURCE_MATRIX_V55.md), rows `E01-E03` and
  `D05`
