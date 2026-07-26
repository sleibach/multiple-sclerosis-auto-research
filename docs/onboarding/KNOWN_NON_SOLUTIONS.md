# Known Non-Solutions: Search Before You Propose

This is a compact stop-and-repair index for ideas the project has already
tested, bounded, or rejected in their current form. It keeps dead ends visible
so a contributor can change the missing assumption instead of repeating the
same route.

A row closes only the shortcut stated. It does not declare a gene, pathway,
method, or broader biological question universally irrelevant. A route may
reopen only with the specific evidence in the last column. `[E01, G03-G05,
D02-D05, P01-P06]`

## How To Use This Page

1. Search for the gene, method, data type, or claim in your idea.
2. Read the **why it fails** column before refining the proposal.
3. If you have the named reopening evidence, state exactly how it changes the
   prior assumption.
4. If you do not, choose a different open problem rather than relabeling the
   same shortcut.
5. Use the [status decoder](STATUS_DECODER.md): “closed in current form” is not
   the same as “biology absent.”

## Monitoring And Validation Shortcuts

| do not re-propose unchanged | why it fails here | what would make it genuinely new |
|---|---|---|
| “The APC/HLA-II monitor is the drug target.” | An early readout of treatment-related change does not identify a causal control point or beneficial intervention direction. `[M05, D01]` | Direction-resolved perturbation in the relevant cell state, followed by an outcome test. |
| “Use the score to choose a treatment at baseline.” | The locked object is an early change from baseline, not a before-treatment selector or comparison among drugs. `[M01-M02]` | A separately pre-specified baseline decision study with treatment alternatives and decision-impact outcomes. |
| “Call it a validated biomarker because internal checks were strong.” | The evidence set is 19 people; repeated internal stress tests do not create an independent cohort. `[M01, M03, A01]` | Mechanical execution of the frozen rule on an eligible outside cohort. |
| “Tune the genes, threshold, labels, or exclusions when validation data arrive.” | Looking at outcomes before fixing those choices makes the outside test another development analysis. `[A01]` | Run the existing frozen plan unchanged; any new rule must start a separate development-and-validation cycle. |
| “A pass in one small outside cohort makes it a clinical tool.” | One association test does not establish clinical utility, treatment selection, benefit, or safe decision use. `[M01, M05, A01, A03]` | Further independent replication and a prospective decision-impact study with defined actions and harms. |
| “The score should generalize across drugs and diseases.” | Results were mixed across therapies and cohorts; the bounded support does not supply a universal response rule. `[M02]` | A prospectively specified transport test with matching time, outcome, tissue, and rule. |
| “The score is a pure APC/HLA-II mechanism.” | Broader immune tone weakened the association; the current interpretation is partially confounded and bounded. `[M04]` | Independent replication with richer state and composition measurements that separates the score without changing it. |
| “The steroid question is settled.” | The tested glucocorticoid-response proxy did not explain the score, but direct timed steroid exposure was unavailable. `[M04]` | Direct exposure and timing metadata analyzed under a pre-specified adjustment. |
| “A more complex learner must beat the scalar.” | Tested flexible and coupled alternatives did not improve fair behavior in the same small data. `[M03, D02]` | New independent development data, a frozen new model, and a distinct untouched validation set. |
| “An unlabeled longitudinal treatment dataset is validation-ready.” | Paired measurements without a verified person-level response outcome cannot test the frozen claim. `[A01, A04]` | A sample-person map, paired baseline/early times, outcome labels and definitions, module coverage, provenance, and permitted use. |

## Genetics, Structure, And Target Shortcuts

| do not re-propose unchanged | why it fails here | what would make it genuinely new |
|---|---|---|
| “MS and ulcerative colitis share genetics, so transfer a target.” | Genome-wide relationship does not establish the same causal gene, cell state, effect direction, or useful intervention at a locus. `[G01-G02]` | Signal-specific MS causal evidence with cell, allele, direction, and modality aligned. |
| “A shared autoimmune locus has one therapeutic direction.” | ZMIZ1 showed opposite disease-risk directions for the same expression-increasing direction. `[G02]` | MS-specific, signal- and cell-specific causal direction plus a matching functional assay. |
| “Choose the nearest or most drug-like gene at chr1.” | The region appears real, but causal-gene assignment remains unresolved; GPR25 was demoted after denser review. `[G03, G05]` | Fine-mapped signal-specific evidence linking the MS association to one gene and relevant-cell molecular effect. |
| “GPR25 is a receptor with a pocket, so inhibit it.” | Protein class and predicted geometry do not resolve the causal gene, and the protective implication points toward hard restoration or up-function logic. `[G03, G05]` | Causal assignment plus a feasible direction-matched gain/restoration modality in the relevant cell state. |
| “A predicted structure proves druggability.” | Predicted geometry is outside-source context, not experimental structure, causal evidence, beneficial direction, selectivity, delivery, or safety. `[G03, E01-E02]` | Experimental corroboration may improve structural confidence, but target status still needs causal and direction-matched functional evidence. |
| “Default to inhibition because most drugs inhibit.” | A familiar modality is useless or harmful if protection requires more or restored function. `[G03-G05]` | Compare increase and decrease experimentally under an allele-aligned, cell-specific functional readout. |
| “PTGER4 is familiar and druggable, so ignore the genetics conflict.” | Multiple signals and disease directions prevent a clean shared MS-ulcerative-colitis target interpretation. `[G04]` | Signal-specific cell-type molecular-genetics evidence with an MS-favorable direction and matching modality. |
| “A wrong-direction or demoted gene is biologically irrelevant.” | Therapeutic closure can preserve useful regional or cross-disease biology. `[G02-G05]` | Do not seek generic relevance; supply the exact causal, directional, and functional evidence needed for intervention. |

## Systems, Models, And Search Shortcuts

| do not re-propose unchanged | why it fails here | what would make it genuinely new |
|---|---|---|
| “The coupled APC axis is a validated multi-target therapy.” | Repeated co-movement does not identify drivers, feedback, redundancy, useful combinations, or beneficial directions. `[D01-D02]` | Prospective perturbations that discriminate competing causal graphs and predict a held-out functional result. |
| “Add the coupled features to improve the monitoring rule.” | Tested coupled-axis and flexible additions did not improve the locked scalar in the bounded data. `[D02]` | New development data and a separately frozen successor with independent validation; never retune the locked rule. |
| “The immune simulator predicts individual patients or unseen pathways.” | The broad simulator could not be validated for those claims on held data. `[D03]` | A separately specified model with prospective or genuinely held-out individual-level validation. |
| “Run another unconstrained search over the same assembled corpus.” | Zero of 22 unexpected joint candidates passed recurrence plus the held-out-data-type gate. `[D04-D05]` | Genuinely new data or a targeted test fixed before analysis, not another flexible search on the same labels. |
| “The 0.127 bound is a biological effect ceiling.” | It is a corpus- and gate-specific upper bound on unexpected candidates, not an effect-size limit in MS. `[D04]` | A new corpus can support its own prospectively defined calibration; it cannot reinterpret the old number. |
| “AI models agree, so the idea has independent evidence.” | Claude, Gemini, and RPT generate and challenge proposals; shared wording or confidence is not a data test. `[E03]` | Implement the concrete prediction on real data under the ordinary evidence gate. |
| “Synthetic cohorts prove the MS effect exists.” | Seeded simulations characterize method behavior under chosen assumptions, not MS biology or a future cohort's result. `[A03]` | Biological evidence requires eligible real observations; simulations remain useful for power and failure-envelope design. |
| “Outside consensus overrides a rerunnable project result.” | Literature and database context have separate provenance and cannot silently borrow the grounded result's authority. `[E01-E02]` | A specific outside claim may motivate a distinct groundable test; only that run can change project evidence. |

## Progression And Compartment Shortcuts

| do not re-propose unchanged | why it fails here | what would make it genuinely new |
|---|---|---|
| “A static disease-stage contrast measures progression.” | Progression requires change and confirmation over time; a one-time stage label cannot identify the transition. `[B02, P01-P03]` | Repeated compatible molecular state before repeated confirmed-disability outcomes in the same people. |
| “Relapse activity can stand in for disability progression.” | The outcomes are related but not interchangeable. `[B02]` | Use a pre-defined confirmed-disability outcome with relapse timing retained as a separate variable. |
| “A treatment-response score is a progression marker.” | Early pharmacodynamic monitoring and later disability accumulation are different claims and time scales. `[M05, P01-P03]` | A separate fixed longitudinal test connecting an eligible molecular state to later confirmed disability. |
| “Apply CD44/CXCR4 to blood or substitute similar genes.” | Only the exact two-gene identity in a compatible microglial compartment transfers; progression prediction is untested. `[P06]` | The exact score in a microglia-compatible, longitudinal, source-qualified package with fixed outcomes. |
| “CD44/CXCR4 is already a progression target.” | The bounded result concerns state identity, not progression specificity, causality, beneficial direction, or intervention. `[C01, P06]` | First test progression prediction, then obtain separate direction-resolved functional evidence. |
| “The foamy OXPHOS/lysosomal pattern is a progression mechanism.” | The pattern was downgraded after global multiplicity and within-donor checks. `[P04]` | Orthogonal donor-aware replication followed by a distinct functional-direction test. |
| “The brain-bank imbalance invalidates every microglia result.” | One partition was strongly source-sensitive; the bounded lesson is qualification and source-balanced replication, not universal rejection. `[C01-C02]` | Repeat the fixed contrast in source-balanced donors with source and diagnosis jointly represented. |
| “No compatible progression dataset means no progression biology.” | The held corpus lacks the required design; missing coverage is not biological absence. `[P01-P05]` | Acquire a package meeting the fixed progression, compartment, and functional-direction roles. |
| “A near-match can substitute for whichever progression role is missing.” | None of ten known packages filled the complete role chain, and relapse, morphology, blood, and static stage answer different questions. `[P01-P05, A02]` | Meet each role's required compartment, timing, outcome, source, and functional evidence without post-outcome substitution. |

## Fast Duplicate Check

Before submitting, answer **no** to every shortcut below:

- Does the idea turn a monitor into a target?
- Does it treat internal robustness as outside validation?
- Does it tune a frozen rule after outcomes are visible?
- Does it pick a gene from proximity, protein class, or pocket shape alone?
- Does it default to inhibition without checking the protective direction?
- Does it turn co-movement into a causal control system?
- Does it call a model, simulation, or outside source evidence?
- Does it treat a static stage, relapse, morphology, or blood score as
  longitudinal progression?
- Does it interpret missing data as absent biology?
- Does it erase the stated scope of a closure?

If any answer is yes, use the last column of the relevant table to repair the
idea. If the repair needs unavailable data, say so directly and submit a data-
acquisition direction rather than an unsupported biological claim.

## Where To Go Next

- Choose an unresolved puzzle on the
  [open-problem board](OPEN_PROBLEMS_FOR_COLLABORATORS.md).
- Read the fuller explanation in the
  [failure-mode atlas](FAILURE_MODE_ATLAS.md).
- Check the current [lead status cards](LEAD_STATUS_CARDS.md).
- Turn your repair into a [testable contribution](HOW_TO_CONTRIBUTE_IDEAS.md).
- See how reviewers route it in the
  [contributor lifecycle](WHAT_HAPPENS_TO_YOUR_IDEA.md).
