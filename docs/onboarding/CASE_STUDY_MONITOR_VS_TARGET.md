# Case Study: A Useful Monitor Is Not A Drug Target

The project's one live clinical lead measures an early treatment-related
change. It may eventually help tell whether a person's immune biology is moving
into a favorable state. It does not identify which molecule should be blocked,
activated, restored, or replaced.

This page explains that distinction using the existing V22 monitoring result.
It adds no new scientific claim. `[M01-M05]`

## The Short Version

The locked V22 rule compares a person's baseline sample with an early sample
after treatment. It combines changes in antigen-presentation and inflammatory
immune modules into one score. In a small, bounded evidence set, higher scores
were associated with response in some eligible treatment contexts and not in
others. The rule remains provisional and awaits independent validation.
`[M01-M04]`

That can support a future question such as:

> Is treatment already moving this person's measured immune state in the
> direction associated with later response?

It cannot answer:

> Which protein should we drug to treat MS?

An instrument reading can be useful without being the control knob.

## Gauge Versus Control Knob

Consider a heating system:

- A thermometer reports temperature.
- A valve changes fuel flow.
- A thermostat uses the thermometer to decide when to change the valve.

The thermometer may predict whether the room will reach the desired
temperature. That does not mean heating the thermometer will warm the room.

The V22 score is closer to the thermometer than the valve. It observes a
multi-gene immune-state change after treatment. It does not establish that any
one measured gene is the cause of response or a safe intervention point.
`[M05]`

The analogy is deliberately limited. Immune systems are not simple heating
systems, and the score may reflect several coupled processes. The point is only
that **measurement and intervention require different evidence**.

## What The Rule Actually Does

For the relevant MS treatment class, the frozen feature is:

```text
early HLA-II module change - early IFN/APC module change
```

Each change is calculated within the same person:

```text
first eligible on-treatment score - pretreatment baseline score
```

The modules, time window, pairing rule, feature direction, outcome choice, and
pass/fail logic were fixed before held-out application. No coefficient is fit
inside a validation cohort. `[M01-M03]`

This design asks about **early monitoring after treatment begins**. It does not
ask who should receive treatment at baseline. It also does not claim broad
transfer across every therapy, tissue, disease, or outcome.

## What The Held Evidence Says

The locked rule produced mixed results: the small MS dimethyl-fumarate cohort
passed its bounded rule, while an MS fingolimod cohort and psoriasis
adalimumab cohort did not. A small ulcerative-colitis tofacitinib result was
supportive but remained exploratory because of module and compartment limits.
`[M02]`

Across the bounded 19-person confounder-audit set, the score survived the
tested baseline, steroid-response-signature, and simple cell-composition
adjustments. Broader metabolic, inflammatory, and STAT1/immune-tone adjustment
attenuated it. Direct steroid exposure metadata were not available. `[M03-M04]`

The honest status is therefore:

- one **provisional early-treatment monitor**;
- internally stress-tested but still tiny;
- mixed across contexts;
- bounded by broader immune tone; and
- not externally validated for clinical use. `[M01-M04]`

## The Two Evidence Ladders

“Ladder” means a sequence of distinct evidence requirements. It is not a
numeric score, and completing an earlier monitoring step does not automatically
advance an intervention claim.

### Monitoring Ladder

```text
fixed measurement
    -> association with later response
        -> independent replication without retuning
            -> prospective decision study
                -> evidence that using the result improves care
```

The project is between the association and independent-replication steps.

### Target Ladder

```text
disease-relevant mechanism
    -> causal intervention node
        -> protective direction
            -> selective perturbation
                -> benefit and safety in relevant models
                    -> clinical testing
```

The V22 association does not fill this ladder. It observes a changing system;
it does not isolate a causal node or intervention direction. `[M05]`

## Why Module Genes Are Not Automatically Targets

The score contains genes involved in HLA-II antigen presentation and
interferon/APC state. A gene can contribute to a useful readout for several
reasons:

- it may respond downstream of the true treatment mechanism;
- it may report the mix or state of cells present;
- it may be part of a coordinated immune program rather than its control point;
- its increase could be protective in one context and harmful in another; or
- it may correlate with response while direct perturbation has no benefit.

Therefore, “the gene is in the score” does not establish:

- that it causes treatment response;
- whether it should be increased or decreased;
- whether changing it reproduces the beneficial state;
- whether the effect is selective to MS biology; or
- whether intervention would be safe.

The project's coupled-axis work found recurring context around the score, but
adding that complexity did not improve the locked monitor. The architecture is
useful for interpretation and assay design, not a validated target list.
`[D01-D02, M05]`

## What Independent Validation Could Establish

The next valid package needs paired baseline and eligible early-treatment
samples, compatible response labels, sufficient frozen-module genes, and the
metadata required by the preregistration. The rule must run unchanged.
`[A01]`

### If It Passes

A clean pass would establish that the frozen score transported to that outside
cohort under the precommitted rules. It would strengthen the case for a larger
prospective monitoring-utility study.

It would still not establish:

- a drug target;
- baseline treatment selection;
- clinical benefit from acting on the score;
- a progression marker; or
- universal performance across therapies.

### If It Is Inconclusive

The effect estimate and confidence interval would inform the size of a later
study. Seeded method simulations show that a very small cohort may remain
inconclusive unless separation is large and labels are clean; those simulations
describe method behavior, not an expected MS effect. `[A03]`

### If It Fails

The result would be interpreted under the frozen failure grid. It could close
or further bound the monitoring claim. It would not prove that every module
gene or the broader immune biology is irrelevant.

## What Would Be Needed For A Target Claim

A separate target program would need evidence the monitoring study was not
designed to provide:

1. Resolve a causal node rather than a correlated readout.
2. Establish the direction that is protective in an MS-relevant cell state.
3. Perturb that node while measuring whether the proposed mechanism changes.
4. Separate desired effects from broad immune suppression or activation.
5. Replicate the perturbation in an independent, relevant system.
6. Demonstrate a plausible and safe modality for that direction.

That program could eventually involve a score component, a regulator upstream
of the score, or a different node entirely. The monitoring result alone does
not choose among them.

## Where Monitoring Could Still Matter Clinically

If independently validated and then shown useful in a prospective decision
study, an early monitor could help evaluate whether to continue or reconsider a
treatment before waiting for later clinical outcomes. That is meaningful
potential clinical value even though it is not a new drug. `[M01, M05]`

The sequence matters:

```text
external transport
    -> reliable assay
        -> decision threshold
            -> prospective utility
                -> clinical use
```

The project has not completed those steps. “Could help” is therefore the
correct future conditional, not a current clinical claim.

## A Checklist For Readout-Based Ideas

When a model, module, imaging feature, or blood marker predicts an outcome, ask:

1. Was it measured before the outcome and under a fixed rule?
2. Does it replicate outside the data that shaped it?
3. Is it a baseline selector, an on-treatment monitor, or an outcome measured
   after the fact?
4. Which confounders could move both the readout and the outcome?
5. Does the readout add information beyond those confounders?
6. What decision would use it, and has using it improved an outcome?
7. If someone calls it a target, where are the causal node, protective
   direction, perturbation, selectivity, and safety evidence?

Questions 1-6 evaluate a monitor. Question 7 begins a different evidence
program.

## Trace The Evidence

- [V22 finding](../findings/FINDING_V22.md)
- [Immutable V22 rule](../locked_rules/LOCKED_RULE_V22.md)
- [V28 robustness map](../workups/treatment_response/ROBUSTNESS_MAP_V28.md)
- [V32 confounder audit](../workups/treatment_response/CONFOUNDER_AUDIT_V32.md)
- [V42 preregistration](../validation/PREREGISTRATION_V42.md)
- [V52 therapeutic-path synthesis](../reports/THERAPEUTIC_PATH_V52.md)
- [Claim-source contract](CLAIM_SOURCE_MATRIX_V55.md), rows `M01-M05`, `A01`,
  and `A03`
