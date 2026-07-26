# Plain-Language Glossary

This glossary is orientation for reading the repository, not a collection of
new project findings. Definitions are intentionally short. Where a term has a
special project meaning, that boundary is stated explicitly.

If you arrived through a gene name or search snippet and need its current
project status, use [Find By Term](FIND_BY_TERM.md).

## MS And Immune Biology

**Multiple sclerosis (MS)**  
An immune-mediated disease involving injury in the central nervous system,
including damage to myelin and nerve fibers. This is background orientation,
not a causal model established by this project. `[B01]`

**Central nervous system (CNS)**  
The brain and spinal cord. The project distinguishes CNS-resident or
CNS-associated measurements from measurements in peripheral blood.

**Cerebrospinal fluid (CSF)**

Fluid around the brain and spinal cord. Paired blood and CSF measurements can
help distinguish a central nervous system association from a broad peripheral
immune association; an unpaired comparison cannot answer the same question.
`[P01, P03]`

**Myelin**  
Insulating material around nerve fibers. Damage to myelin is part of the
background description of MS, but this project did not directly model myelin
repair.

**Relapse**  
An episode of inflammatory disease activity. Relapse activity is not
interchangeable with disability progression. `[B02]`

**Progression**  
Disability accumulating and remaining confirmed over time. Studying it requires
repeated outcome measurements; a static disease-stage label is not the same
thing. `[B02, P01, P03]`

**RRMS / SPMS / PPMS**

Common disease-course labels: relapsing-remitting MS, secondary progressive MS,
and primary progressive MS. A label describes a clinical course category; by
itself it is not a timed measurement of disability progression. `[B02, P01]`

**PIRA (progression independent of relapse activity)**

A way of defining confirmed disability accumulation that is not attributed to
nearby relapse activity under a specified timing rule. The exact rule and
adjudication must come from the study protocol; this project does not treat the
acronym alone as a usable outcome. `[A02]`

**Confirmed disability**  
A disability change that remains present under a defined confirmation rule at
later assessment. The progression program requires repeated, timed outcomes
rather than treating a one-time measurement as progression. `[A02]`

**Immune-mediated**  
Involving immune processes. It does not mean that one immune pathway explains
all disease activity or progression.

**Antigen-presenting cell (APC)**  
An immune cell that displays molecular fragments to other immune cells. In this
repository, “APC” often names a gene-expression state or module, not a direct
cell-count measurement.

**Antigen presentation / HLA-II**  
Cellular machinery used to display molecular fragments to immune cells. HLA-II
genes contribute to the live monitoring score and recurring APC context. Their
presence in a score does not make HLA-II a validated target. `[M01, D01, M05]`

**Interferon (IFN) and STAT1**  
Signals and response machinery associated with broad immune activation states.
They matter here because broad IFN/STAT1/immune tone can overlap with the
APC/HLA-II score. `[M04]`

**MIF / CD74**

Gene and protein labels that appear in the recurring coupled APC architecture.
The project uses “MIF/CD74” as supported context; it did not establish either
component as a target. `[D01]`

**Oxidative phosphorylation (OXPHOS)**

A cellular energy-producing process and module label used in the progression
work. The foamy-morphology OXPHOS pattern was downgraded after stronger
multiplicity and donor checks. `[P04]`

**Microglia**  
Immune-related cells resident in the CNS. The exact CD44/CXCR4 candidate is
microglia-compatible and must not be silently transferred to PBMC or whole
blood. `[P06]`

**PBMC**  
Peripheral blood mononuclear cells, a mixed set of immune cells isolated from
blood. PBMC data cannot automatically answer a microglia- or CNS-specific
question.

**Compartment**  
The cell type, tissue, or biological location in which a measurement is made.
The same genes can have different meaning across compartments.

## Measurements And Study Design

**Cohort**  
A group of people or samples studied under a defined design. Two analyses of
the same cohort are not two independent replications.

**Baseline**  
A measurement taken before the treatment-relative change being studied.

**Early on-treatment sample**  
A measurement taken after treatment begins but before the later response
outcome. The exact allowed timing belongs to the frozen validation plan.

**Paired samples**  
Two or more measurements from the same person. Pairing must be preserved;
treating them as unrelated samples loses the within-person change design.

**Response label**  
The pre-defined outcome category against which a score is tested. A useful
validation package needs a sample-to-person map and a person-level response
label. `[A01, A04]`

**NEDA-4 (No Evidence of Disease Activity-4)**

A composite treatment-outcome label used by the intended external validation
cohort. Its exact components, assessment window, and source definition must be
supplied with the cohort; the project will not reconstruct or tune them after
seeing molecular data. `[A01, A04]`

**Dimethyl fumarate (DMF)**

The MS treatment used in the intended external monitoring validation. A cohort
on another therapy may be scientifically useful, but it cannot silently replace
the preregistered DMF primary validation. `[A01, A04]`

**Expanded Disability Status Scale (EDSS)**

A clinical scale used in MS disability assessment. For progression analysis,
one EDSS value is insufficient: the value, date, and pre-specified confirmation
rule must be available across repeated assessments. `[A02]`

**Quality control (QC)**

Checks and flags used to determine whether samples, labels, timing, and measured
features are usable. Missing QC information is an ingestion limitation, not
evidence that a biological effect is absent.

**Molecular state**  
A compact description of measured biological features at a point in time. It
is an analytical representation, not necessarily a discrete natural state.

**Gene module**  
A fixed set of genes summarized together because they represent a biological
theme or a pre-specified feature. A module name is an interpretation aid, not
proof that every gene has one mechanism.

**Module score**  
A numerical summary of a gene module. Its exact formula matters; replacing
genes or normalization after viewing outcomes changes the test.

**Delta / early-change score**  
The difference between an early on-treatment measurement and baseline. The
V22 lead uses a fixed delta rather than a baseline-only selector. `[M01]`

**Monitoring signal**  
A measurement that may report whether biology is changing. It does not by
itself identify a causal mechanism, choose a treatment, establish benefit, or
show an effect on progression. `[M05]`

**Biomarker**  
A measurable indicator associated with a biological state or outcome. This
repository does not call the V22 score a validated clinical biomarker because
independent validation and clinical-utility evidence are missing. `[M01]`

**Therapeutic target**  
A biological entity or process for which changing function in a specified
direction is expected to improve an outcome. Association, structural
tractability, or monitoring value alone does not establish a target.

## Statistics And Validation

**AUC (area under the ROC curve)**  
A ranking measure for how often a score orders one outcome group above another.
`0.5` is chance ranking under the usual interpretation; `1.0` is perfect
ranking in the evaluated data. A high AUC in a tiny cohort can be uncertain or
overfit.

**Effect size**  
The magnitude of a difference or association. It is distinct from a p-value
and should be reported with uncertainty.

**Confidence interval (CI)**  
A range produced by a stated statistical procedure to express uncertainty in
an estimate. An interval can be wide enough that a study remains inconclusive.

**Null hypothesis / null model**  
A defined reference for what could occur without the proposed signal, often by
chance assignment or structure-preserving permutation.

**Permutation test**  
A test that repeatedly rearranges labels or assignments under a specified null
while preserving relevant data structure. It asks how unusual the observed
result is under that null.

**p-value**

The probability, under a specified null and analysis procedure, of a statistic
at least as extreme as the observed one. It is not the probability that the
null is true or that a result will replicate.

**Family-wise error rate (FWER)**

The probability of making at least one false rejection in a defined family of
tests under the correction's assumptions.

**False discovery rate (FDR)**

The expected fraction of false discoveries among the discoveries under the
chosen procedure and its assumptions.

**q-value**

Commonly, the smallest FDR level at which a test would be called significant
under the chosen procedure. It is not the probability that one finding is
false.

**Holdout**  
Data deliberately not used to construct or select a result, reserved for a
later test. A different encoding of the same labels is not automatically an
independent holdout.

**Cross-validation (CV)**

A procedure that repeatedly trains or selects on part of the data and evaluates
on another part. It helps estimate out-of-sample behavior but does not replace
an independent cohort.

**Multiple testing**  
The increased chance of apparently strong results when many hypotheses,
features, or models are tried. Corrections and a fixed analysis budget prevent
the most attractive result from being judged as if it were the only test.

**Confounder**  
A factor related to both the measured signal and outcome that can create or
distort their association. This project explicitly encountered broad immune
tone and source-label imbalance. `[M04, C02]`

**Batch effect**  
Variation caused by processing, platform, site, or acquisition conditions
rather than the intended biological contrast.

**Source imbalance**  
A design in which disease or outcome labels align with source, site, brain
bank, or another acquisition factor. If overlap is poor, a disease effect may
not be identifiable. `[C02]`

**Underpowered**  
Having too little information to reliably distinguish a plausible effect from
noise under a specified design. Underpowered does not mean the effect is absent
or present.

**Inconclusive**  
The data do not meet a pre-specified pass or fail interpretation. It is a valid
outcome, not permission to change the analysis until it passes. `[A01, A03]`

**Estimand**  
The exact quantity an analysis intends to estimate, including population,
outcome, time window, and comparison.

**Calibration**  
Agreement between predicted uncertainty or risk and observed behavior under a
defined evaluation. Good ranking and good calibration are different qualities.

## Genetics And Druggability

**Locus**  
A region of the genome associated with a trait. A locus can contain multiple
genes and signals, so “associated region” does not automatically identify the
causal gene.

**GWAS**  
A genome-wide association study testing genetic variants across the genome for
association with a trait. Association is not the same as mechanism.

**QTL / eQTL**  
A genetic variant associated with a quantitative molecular feature; an eQTL is
associated with gene expression. Direction, tissue, cell type, and signal
identity matter when relating an eQTL to disease.

**Gene Expression Omnibus (GEO)**

A public archive commonly used to locate candidate molecular datasets. A GEO
listing does not make a cohort validation-ready; pairing, labels, gene coverage,
provenance, and use conditions still require verification. `[A04]`

**G protein-coupled receptor (GPCR)**

A protein-family label relevant to the early appeal of GPR25. In this project,
belonging to that family did not resolve the causal gene or the required
therapeutic direction. `[G03, G05]`

**Ulcerative colitis (UC) / MS-UC comparison**

UC was the strongest genome-wide genetic comparator to MS among the diseases
tested here. This is useful context, not evidence that UC causes MS or transfers
a treatment target. `[G01]`

**PTGER4**

A gene symbol for a route closed as a simple shared MS-UC target because signals
and disease directions conflicted. `[G04]`

**ZMIZ1**

A gene symbol used in the supported cross-disease decoupling result. The same
expression-increasing direction was associated with higher MS risk and lower
Crohn risk; this is a transfer warning, not a target nomination. `[G02]`

**Colocalization**  
A statistical assessment of whether two association patterns are compatible
with a shared causal signal. It does not prove a causal gene or therapeutic
effect.

**Causal-gene uncertainty**  
The unresolved question of which gene at an associated locus carries the
disease-relevant effect. This remains central at the KIF21B/GPR25 region.
`[G03]`

**Therapeutic direction**  
Whether protection appears to require decreasing, increasing, restoring, or
contextually changing a function. A modality is useful only if it can produce
the required sign in the relevant cell and state.

**Up-function / restoration**  
Increasing or recovering useful function rather than inhibiting it. These
directions are often harder to achieve and contributed to closure of the chr1
route. `[G03]`

**Druggability**  
Whether a biological route can plausibly be modulated with an appropriate
modality in the required direction. Protein class or a predicted pocket is
insufficient without causal, directional, cell-state, and delivery fit.

## Project Discipline

**Artificial intelligence (AI)**

Here, AI models are drafting, question-generating, and adversarial lenses. Their
confidence or agreement is not scientific evidence. `[E03]`

**RPT**

The project label for a tabular-model lens reached through SAP AI Core. Like the
language-model lenses, its output is proposal-only until checked against
artifacts or data. `[E03]`

**Scalable Vector Graphics (SVG)**

The lightweight vector format used for onboarding diagrams. SVG is a
communication format, not an evidence class or scientific result.

**HyperText Markup Language (HTML)**

The document format used for the responsive, print-designed collaborator
brief. HTML controls presentation here; it does not add an evidence layer or a
scientific result.

**Megabyte (MB)**

A unit of file size. The repository's 50 MB tracked-file guard is a hosting and
maintenance rule, not a scientific threshold.

**Locked rule**  
A feature set, calculation, and decision rule committed before the next test.
It cannot be tuned after the outcome is visible.

**Preregistration**  
A plan fixing data handling, analysis, tests, and interpretation before the
validation data are examined.

**Project-grounded**  
Produced by a rerunnable project analysis on held or reachable data. It can be
supported, provisional, negative, or data-bounded; the term does not mean
clinically validated. `[E01]`

**Provisional**  
Supported enough to justify a next test, but missing decisive independent
confirmation or another required evidence layer.

**Supported context**  
A bounded relationship useful for interpretation but not promoted to a
biomarker, cause, or target.

**Negative established / closed**  
A route that failed a fair test, was downgraded, or lacks the named evidence
needed to reopen. This is a result, not a hidden positive.

**Data blocked**  
The required data or design are absent. It must not be translated into “the
biology does not exist.” `[P01, P03]`

**External validation**  
A test on genuinely independent data under rules fixed before outcomes are
seen. It is stronger than repeated internal reanalysis.

**Outside-source context**  
Literature, database, expert, or model material kept separate from project
evidence. It can orient or propose a test but cannot directly support a project
conclusion. `[E02, E03]`

**Synthetic method evidence**  
Results from clearly labeled simulated data used to test power, false-positive
behavior, or software. They say how a method behaves under assumptions, not
what is biologically true in MS. `[A03]`

**Corpus boundary / exhaustion**  
A quantified decision that unconstrained mining of the assembled held corpus
did not produce an unexpected signal passing the held-out-modality gate.
It is not a ban on new data, targeted reanalysis, or future methods. `[D04,
D05]`

## Five Distinctions To Remember

1. **Relapse is not progression.**
2. **Monitoring is not a target.**
3. **Association is not cause.**
4. **Missing data are not absent biology.**
5. **Rerunnable here is not independently or clinically validated.**

Those five distinctions prevent most serious onboarding overreads.
