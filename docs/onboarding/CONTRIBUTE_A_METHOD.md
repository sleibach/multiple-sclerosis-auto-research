# Contribute A Computational Or Analytical Method

A new method is valuable when it makes a project decision more reliable,
identifies a failure earlier, or distinguishes explanations the current design
cannot separate. Novelty, complexity, benchmark reputation, or model confidence
does not make a biological claim true.

This guide turns a method idea into a fair evaluation plan. Model and tool
output remains proposal-only until a real, eligible run supports a bounded
result. Seeded synthetic data may test method behavior but never supplies MS
biology. `[E01-E03, A03]`

## Step 1: Name The Method Role

Choose one:

| method role | legitimate question | non-solution to avoid |
|---|---|---|
| Diagnostic | Can it detect source, batch, leakage, overlap failure, or unusable input before interpretation? | Calling a diagnostic pass biological validation. `[C02]` |
| Estimator | Can it estimate the same bounded effect with better calibrated uncertainty or less bias? | Selecting the estimator with the strongest favorable result. |
| Predictor | Can it transport to an untouched independent unit under a frozen target? | Refitting and evaluating on the same tiny labels. `[M03, D02]` |
| Causal-structure test | Can it discriminate competing causal graphs under signed interventions? | Turning co-movement or graph rank into a target. `[D01]` |
| Power/design tool | Can it map when a fixed future test is informative? | Treating simulated effects as MS estimates. `[A03]` |
| Ingestion or validation guard | Can it reject malformed, unauthorized, or non-identifiable packages mechanically? | Quietly coercing input to make the run proceed. `[A01-A04]` |
| Search or prioritization lens | Can it order tests while controlling the search family? | Treating rank, agreement, or novelty as evidence. `[D04-D05, E03]` |
| Communication/decision tool | Can it prevent overreading and support abstention? | Treating better presentation as clinical utility. `[M01, M05]` |

Write one sentence:

```text
This method changes the decision to ______________________________
by distinguishing __________________ from ________________________.
```

## Step 2: Fix The Target Before The Method

Specify:

```markdown
Population or data scope:
Independent unit:
Input available before the outcome:
Primary outcome or diagnostic target:
Estimand or prediction target:
Allowed exclusions:
Decision threshold, if already frozen:
Result classes: pass / fail / inconclusive / invalid / data-blocked
```

Do not let the method choose a more favorable outcome, time window, cohort,
gene set, or subgroup. If the target is developmental rather than frozen,
separate development from a truly untouched evaluation.

## Step 3: Choose A Fair Baseline

The baseline should answer the same question with the same inputs and
independent unit.

Good baselines include:

- the existing locked scalar when proposing a monitoring successor;
- a simple source/batch contingency diagnostic before a complex domain model;
- a fixed conventional estimator before a flexible learner;
- an intercept-only or pre-specified clinical baseline where appropriate;
- a simpler causal graph that makes a rival prediction; or
- the existing schema/guard behavior for an infrastructure contribution.

Do not compare a new method with a deliberately weak baseline, give it extra
fields, or tune only the new method on the held-out set. In the bounded
monitoring data, tested complexity did not improve the scalar; a new method
must face that result rather than assume complexity wins. `[M03, D02]`

## Step 4: Protect Independence

Name the unit that must not cross development and evaluation:

- person, not sample;
- donor, not cell;
- site or source, when transport across acquisition matters;
- cohort, for outside validation;
- data type, for cross-modal prediction; or
- time block, when future prediction is claimed.

State how repeated units, family relationships, shared source material, and
duplicate studies are detected. A random sample split is invalid when samples
from one person or cells from one donor appear on both sides.

## Step 5: Pre-Specify The Null And Search Family

Describe what chance should preserve:

```markdown
Null operation:
Structure preserved: pairing / donor / source / time / correlation / class size
Number of candidate features/models/tests:
Correction or family-wise control:
Primary versus sensitivity analyses:
Seed policy and replicate count, if stochastic:
```

A null that destroys all realistic structure can make an ordinary artifact
look exceptional. A correction applied only after selecting the best method
does not control the original search.

## Step 6: Run A Leakage And Confound Audit

At minimum, test:

- outcome-derived features or preprocessing;
- treatment, visit time, or site encoding the label;
- source/bank/batch aligned with outcome;
- repeated person or donor leakage;
- normalization fit on all data;
- missingness patterns revealing the outcome;
- broad immune state or composition explaining a supposedly specific score;
- hyperparameter or threshold selection on the evaluation set; and
- model selection across many attempts without accounting for the family.

If source and outcome have no meaningful overlap, a flexible adjustment is not
permission to extrapolate. Return non-identifiable. `[M04, C02]`

## Step 7: Report Method Behavior, Not A Victory Label

Report all of these:

- effect or performance estimate and uncertainty;
- independent unit and evaluation size;
- baseline under identical data and split;
- null/permutation result and correction family;
- calibration and abstention behavior where predictive;
- failure rates across seeds where stochastic;
- confound and leakage diagnostics;
- invalid/data-blocked cases;
- sensitivity results labeled secondary; and
- compute, dependencies, and deterministic reproduction command.

Do not select the best seed, fold, normalization, or sensitivity as the primary
answer. Small-sample cross-validation estimates can be unstable and are not an
outside cohort. `[M03, A03]`

## Step 8: Write The Drop Rule

Complete:

```text
The method is not worth advancing if ______________________________
because the simpler or rival explanation would be ________________.
```

Valid drop rules include:

- no improvement in pre-specified held-out behavior;
- gain disappears under person/donor/site-level splitting;
- calibration or false-positive control fails;
- performance depends on one source, seed, or unplanned subgroup;
- source/outcome overlap is insufficient for interpretation;
- the method cannot abstain outside support;
- a simpler baseline is equivalent within uncertainty; or
- the required fields are unavailable in the intended external setting.

“We will tune further” is not a drop rule.

## Real Data And Synthetic Data Have Different Jobs

| input | permitted conclusion | forbidden conclusion |
|---|---|---|
| Seeded synthetic data | Method power, false-positive behavior, robustness, ingestion behavior, or known failure recovery under stated assumptions. | The effect exists in MS, has the simulated size, or will validate externally. |
| Held real data | Bounded association or method behavior within its actual design and validation level. | Independent validation when the same people or labels were used for development. |
| New independent real data | Transport or validation under the pre-specified target and eligibility rules. | Clinical utility, mechanism, or target status unless separately tested. |

## Copy-Ready Method Proposal

Replace every angle-bracket prompt. The copied proposal must contain no
personal health information, credentials, private data, or claim that a method
plan is scientific evidence.

```markdown
### Method role and project decision
<role; exact decision changed>

### Distinction tested
<current interpretation versus strongest rival>

### Fixed target and independent unit
<population, inputs, outcome/estimand, exclusions, person/donor/site/cohort>

### Baseline
<same inputs, target, split, and budget>

### Development and untouched evaluation
<what may be tuned; what is frozen; what cannot cross the split>

### Null and multiplicity
<structure-preserving null, search family, correction>

### Leakage/confound checks
<source, batch, unit reuse, timing, preprocessing, missingness, immune tone>

### Uncertainty and abstention
<interval/calibration, out-of-support behavior, inconclusive rule>

### Drop rule
<result that stops or narrows the method>

### Output status
<method behavior only / bounded real-data result / future outside validation>

### Reproduction
<code path, environment, seed policy, expected lightweight outputs>

### Safety and evidence boundary
No personal/private data or credentials are included. This is a method
proposal or method-behavior test; no MS finding changes without a separate
eligible real-data run and bounded interpretation.
```

## Review Outcomes

- **Design repair:** target, baseline, independent unit, null, or drop rule is
  missing.
- **Data request:** the test is coherent but the required eligible package is
  unavailable.
- **Duplicate/closed:** it repeats flexible same-label fitting, unvalidated
  simulation, or another known non-solution without changed evidence.
- **Runnable after freeze:** target, inputs, split, search family, confound
  checks, and interpretation are fixed.
- **Method-only supported:** synthetic or software tests support behavior, not
  biology.
- **Bounded real-data result:** an eligible run supports only the stated method
  and data scope.

Use the [status decoder](STATUS_DECODER.md) and
[review-response templates](REVIEW_RESPONSE_TEMPLATES.md). Continue with
[question starters](QUESTION_STARTERS_BY_DISCIPLINE.md), the
[challenge guide](CHALLENGE_THE_PROJECT.md), or the general
[contribution guide](HOW_TO_CONTRIBUTE_IDEAS.md).
