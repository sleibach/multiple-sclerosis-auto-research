# How To Read Research Numbers Without Overreading

A number can be calculated correctly and still answer a narrower question than
its reader assumes. This guide explains the statistics used in this repository
without turning a threshold into truth or an internal result into external
validation.

It is a reading guide, not a new analysis and not medical advice. Project
examples retain the status assigned by their controlling artifacts.

## The Five Questions To Ask First

Before interpreting any metric, ask:

1. **What is the unit?** A person, donor, sample, cell, gene, locus, or cohort?
2. **What comparison produced it?** Which groups, times, sources, and
   exclusions?
3. **What uncertainty and null were used?** Were dependencies and the actual
   analysis pipeline represented?
4. **Was this the only test?** If not, how were selection and multiplicity
   handled?
5. **Where was it evaluated?** Training data, cross-validation, an internal
   holdout, another modality, or a genuinely independent cohort?

A precise decimal does not answer any of these questions by itself.

## Effect Size: How Much, In The Tested Scale

An **effect size** describes the size of an observed contrast or relationship.
Examples include a mean difference, odds ratio, correlation, regression
coefficient, standardized difference, or change in ranking performance.

Read an effect size with:

- its units and direction;
- the population and time window;
- the number of independent units;
- its confidence interval;
- its sensitivity to source, batch, composition, baseline, and other
  alternatives; and
- the outcome scale's practical meaning.

Do not assume a large standardized effect is clinically important, causal, or
portable. Standardization can make unlike scales comparable, but it does not
make the underlying designs equivalent.

## Confidence Interval: A Range Produced By A Procedure

A frequentist **95% confidence interval** comes from a procedure designed to
cover the true parameter in 95% of repeated comparable samples under its
assumptions. For one realized interval, it is not literally a 95% posterior
probability that the parameter lies inside unless a Bayesian model justifies
that statement.

Use an interval to ask:

- Is the estimate precise enough to distinguish decisions that matter?
- Does the interval include practically important benefit, harm, or no useful
  effect?
- Are the assumptions credible for the sample size and dependence structure?
- Was the interval computed after feature selection or repeated tuning that it
  does not account for?

An interval crossing zero does not prove no effect. It may mean the data cannot
distinguish the relevant possibilities. An interval excluding zero does not
establish causality, clinical value, or transport to another cohort.

## Sample Size: Count Independent Information, Not Rows

The symbol **n** should name the number of independent units relevant to the
claim. Ten thousand cells from eight donors do not create ten thousand
independent people. Repeated samples from one person add temporal information
but remain linked.

Always look for:

- number of people or donors;
- number of outcome events in each class;
- sites, cohorts, or batches represented;
- repeated measurements per unit;
- missingness and exclusions; and
- whether the holdout contains genuinely independent units.

Large row counts can coexist with weak donor-level evidence. Small n can also
produce a useful estimate, but its uncertainty and validation limits must stay
visible.

## AUC: Ranking, Not Accuracy Or Clinical Utility

The **area under the receiver-operating-characteristic curve (AUC)** measures
ranking discrimination across all possible thresholds. Under the standard
binary interpretation, it is the probability that a randomly selected positive
case receives a higher score than a randomly selected negative case, with tie
handling included.

AUC does **not** directly tell you:

- accuracy at one chosen threshold;
- how many positive predictions are correct;
- whether predicted probabilities are calibrated;
- whether one error type is more costly;
- whether the score improves a clinical decision; or
- whether performance transports to another cohort.

Class prevalence does not change the mathematical ranking definition, but it
strongly affects positive and negative predictive values and practical use.
Always report uncertainty and the evaluation design beside AUC.

### Project Example: The Provisional Monitor

The internal pooled evidence for the fixed APC/HLA-II monitoring score reports
`n=19`, AUC `0.811`, and permutation `p=0.008`. The allowed reading is that the
fixed score ranked response outcomes better than the specified label-null in
that small internal evidence set. It remains a provisional, immune-tone-bounded
monitor awaiting independent validation. It is not 81.1% accuracy, a treatment
selector, a target, or proof of benefit. `[M01, M03-M05, A01]`

## p-Value: Compatibility With A Specific Null

A **p-value** is the probability, under the specified null model and analysis
procedure, of obtaining a test statistic at least as extreme as the one
observed.

It is not:

- the probability that the null is true;
- the probability the result occurred “by chance” in a general sense;
- the probability the result will replicate;
- the effect size;
- a measure of clinical importance; or
- protection against an inappropriate design or unmeasured confounder.

The difference between `p=0.049` and `p=0.051` is not a switch from true to
false. A pre-specified threshold controls a decision rule under assumptions; it
does not create a natural boundary in biology.

## Permutation Test: Rebuild The Null, Do Not Just Shuffle Anything

A **permutation test** compares the observed statistic with values produced by
reassignments that should be exchangeable under the null. A valid permutation
must preserve the design's structure.

Examples of what may need preservation include:

- pairing within a person;
- donor-level clustering of cells;
- site or batch blocks;
- class counts;
- the full model-selection or feature-selection step; and
- any cross-validation split logic.

If labels are shuffled across units that were never exchangeable, the null is
too easy and the p-value can be misleading. If a feature was selected using the
real labels but selection is omitted from each permutation, selection bias is
not represented.

## Multiple Testing: The Search Is Part Of The Result

Testing many genes, modules, outcomes, subsets, thresholds, or model variants
creates many chances for an impressive-looking result. The **analysis count**
must include choices made by code and by the researcher.

Two common controls answer different questions:

- **Family-wise error rate (FWER):** controls the probability of at least one
  false rejection in a defined family.
- **False discovery rate (FDR):** controls the expected fraction of false
  discoveries among the discoveries under the method's assumptions.

A **q-value** is commonly interpreted as the smallest false-discovery-rate
level at which a test would be called significant under the chosen procedure.
It is not the probability that this one finding is false.

Correction does not repair outcome-driven choice of the test family. The family
and primary analysis should be defined before results are inspected whenever
the analysis is meant to support a confirmatory claim.

## Cross-Validation: Internal Generalization Under A Split Rule

**Cross-validation** repeatedly trains on part of a dataset and evaluates on
held-out portions. It can estimate internal generalization when every
data-dependent step occurs inside each training fold and the held-out unit
matches the claim.

Common leakage paths include:

- selecting genes once on the full dataset;
- normalizing with outcome-linked information from all samples;
- placing cells from one donor in both train and test folds;
- tuning many models against the same folds and reporting only the best; and
- using the final cross-validation result to rewrite the model, then calling
  the same result held out.

Cross-validation is not an independent cohort. Repeated cross-validation can
stabilize an internal estimate, but it does not reproduce changes in site,
platform, population, treatment practice, or measurement process.

## Holdout: Name What Was Actually Independent

“Held out” is incomplete unless the unit is stated:

- held-out samples may share people or batches;
- held-out donors test donor transport within a source;
- held-out sites test some site transport;
- held-out modalities test cross-view recurrence;
- held-out cohorts test a stronger form of external generalization.

The project uses held-out-modality gates in its joint-inference boundary. Zero
of 22 unexpected candidates passed the full recurrence plus held-out gate. That
is a corpus-specific search result, not proof that no future data or method can
find anything. `[D04, D05]`

## Upper Bound: Bound The Exact Quantity Named

An upper confidence bound applies only to the estimand and gate that generated
it. The V41 value `0.127` is a 95% upper bound on the corpus-specific rate of
unexpected candidates passing the defined joint gate after zero of 22 passed.
It is not a maximum MS effect size, a 12.7% chance that MS biology remains, or a
limit on all future computation. `[D04, D05]`

## Association Measure: Strength Is Not Causality

Statistics such as correlation, regression coefficients, and Cramer's V can
show that variables align. They do not identify which variable causes the
other, nor whether a third process generates both.

In the progression work, a discovery partition had Cramer's V `0.773` between
brain-bank source and diagnosis. That strong alignment was a warning that the
disease contrast could not be cleanly separated from acquisition source;
source-adjusted evidence attenuated. The number supports a confounding
diagnostic, not a claim that brain-bank source causes MS or that all brain-bank
data are invalid. `[C01, C02]`

## Statistical, Predictive, And Clinical Questions Are Different

Keep these questions separate:

| question | example evidence | what it does not answer |
|---|---|---|
| Is there an association under this design? | Effect estimate, uncertainty, null test | Cause, transport, or usefulness |
| Can a fixed score predict held-out outcomes? | Properly nested cross-validation or holdout performance | Clinical benefit or intervention mechanism |
| Does it transport? | Independent cohort with compatible inputs and outcome | Whether using it improves care |
| Does using it help people? | Prospective decision-impact or clinical study | Which molecular mechanism caused the signal |
| Is a node a therapeutic target? | Causal entity, functional direction, perturbation, selectivity, safety | Whether a monitoring score happens to include its gene |

Passing one row does not automatically pass the next.

## How To Read A Results Sentence

Use this template:

```text
In [population and design], [fixed measure] showed [effect and uncertainty]
against [specified null/comparator], evaluated by [holdout unit], after
[multiplicity/confound handling]. This supports [narrow claim]. It does not
establish [nearest tempting overread].
```

If any bracket is missing, ask for it before interpreting the decimal.

## Thresholds Are Decisions, Not Truth Machines

Thresholds are useful when fixed in advance and linked to a consequence. They
make decisions reproducible. They do not prove a mechanism, erase uncertainty,
or make two nearly identical estimates scientifically different.

The repository therefore preserves:

- the continuous estimate and interval;
- the exact null and correction;
- the number of independent units and tests;
- the validation level;
- confounder sensitivity; and
- pass, fail, inconclusive, invalid, and data-blocked interpretations.

## Reader Checklist

- [ ] The independent unit and sample count are explicit.
- [ ] The effect size and uncertainty are both present.
- [ ] AUC is not described as accuracy or clinical utility.
- [ ] The p-value is tied to a named null and procedure.
- [ ] Permutations preserve pairing, clustering, and selection.
- [ ] The full analysis count and correction are visible.
- [ ] Every data-dependent step is nested inside cross-validation.
- [ ] The holdout unit and degree of independence are named.
- [ ] Confounder and source sensitivity are reported.
- [ ] The result wording stops at the evidence level actually tested.

## Continue

- [How to read nulls, invalid inputs, and data boundaries](HOW_TO_READ_NULLS_AND_BOUNDARIES.md)
- [Why monitoring and intervention require different evidence](CASE_STUDY_MONITOR_VS_TARGET.md)
- [How source imbalance can narrow an interpretation](CASE_STUDY_BRAIN_BANK_CONFOUND.md)
- [The project's exact claim-source contract](CLAIM_SOURCE_MATRIX_V55.md)
