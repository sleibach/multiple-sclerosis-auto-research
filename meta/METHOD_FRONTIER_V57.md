# V57 Unexhausted Method Frontier

## Scope

V41's discovery-exhaustion result remains binding. This map does not reopen an
unconstrained search for MS targets. It separates genuinely unused analytical
dimensions from methods already tested, and defines bounded probes that can
fail cleanly on held data.

The machine-readable audit is
`analysis/v57_method_frontier/method_coverage.tsv`.

## Selection Rule

Methods were ranked on five pre-outcome criteria:

1. orthogonality to prior project analyses;
2. feasibility on held, non-quarantined data;
3. ability to answer a decision-relevant question;
4. availability of a patient/cohort-level null and multiplicity control; and
5. low dependence on an unavailable external input.

Methods that merely repackage a completed analysis were assigned priority
zero. A new mathematical name is not a new research dimension when the
estimand and information used are unchanged.

## Highest-Priority Executable Dimensions

| Rank | Dimension | Why it is genuinely new here | Bounded V57 probe | Promotion gate |
|---:|---|---|---|---|
| 1 | Environment stability and worst-environment risk | Prior work pooled or compared cohorts but did not require a stable effect in every predeclared environment | Evaluate the frozen monitoring score across four held cohorts with within-cohort label permutations and leave-one-environment-out checks | Corrected null, direction consistency, and useful worst-environment performance |
| 2 | Class-conditional conformal prediction | The project has confidence intervals and power maps, but no prediction-set abstention mechanism | Leave one cohort out, calibrate by outcome class on the others, and measure coverage plus singleton accuracy | Coverage lower bound and singleton decisions both clear their predeclared gates |
| 3 | Distribution-level optimal transport | Prior module work emphasized means and scalar deltas | Measure paired pre/post changes in complete cell-score distributions and test response specificity at the patient level | max-T correction, technical-depth sensitivity, and disease-direction consistency |
| 4 | Compositional log-ratio analysis | Cell-composition confounding was audited by proxies and counts, not by a formal closed-composition estimand | Test paired myeloid subtype CLR changes in responder versus nonresponder patients | raw and residualized max-T results plus cross-disease direction agreement |
| 5 | Hierarchical partial pooling | Fixed-effect summaries can hide or exaggerate heterogeneity at small n | Fit a prior-sensitive cohort hierarchy only if it adds calibrated out-of-cohort predictions | leave-one-cohort predictive improvement under multiple defensible priors |
| 6 | Tensor donor-state-time interactions | Existing analyses flatten donor, state, and time into separate tables | Cross-validated low-rank reconstruction of response-linked interactions | held-out-donor gain over additive baselines and permutation family control |
| 7 | Topological state geometry | Linear modules can miss stable branching or loop structure | Donor-bootstrap persistence summaries with label permutations | stable topology and corrected outcome association |
| 8 | Sequential acquisition design | Existing power and value-of-information work ranks cohorts, but not adaptive assay choices | Convert current uncertainty into an explicit next-sample/assay policy | robustness to cost and arrival assumptions |

## Important but Currently Blocked Dimensions

| Dimension | Specific blocker | Required input |
|---|---|---|
| Target-trial emulation | No accessible individual-level longitudinal treatment, disability, censoring, and baseline-confounder data with a defensible time zero | Longitudinal MS clinical IPD with treatment strategy and disability outcomes |
| Causal mediation | Treatment, molecular mediator, and clinical outcome do not coexist in the same people at adequate timepoints | Paired baseline/early molecular data plus later outcome in one cohort |
| Spatial neighborhood inference | Held progressive-lesion spatial material does not provide a clean common-slide reconstruction with donor replication | Raw coordinates/counts and donor/slide metadata for chronic-active lesions |
| Formal single-cell differential abundance in MS response | The held treatment-response single-cell atlas is IBD, not MS | Paired, response-labelled MS single-cell data |
| Decision-curve analysis | No externally validated score threshold or agreed clinical action/harm ratio | External validation and clinician-specified decision consequences |

## Dimensions Not Worth Running Now

- High-dimensional gene selection, weak label modeling, and missing-modality
  imputation would create more researcher freedom than information at current
  sample sizes.
- Repeating joint multi-view inference, recurrence mining, network centrality,
  association-network control, or protective-direction genetics would repeat
  completed V40/V41/V53 work without a new modality.
- Structure prediction remains useful context for modality fit but is not a
  source of grounded biological evidence and is not a substitute for target
  direction.

## Early Probe Status

- Environment stability: completed; a pooled association was detectable, but
  worst-environment discrimination was near chance. The stringent stability
  gate failed.
- Class-conditional conformal prediction: completed; empirical set coverage
  was high, but informative singleton predictions were sparse and not above
  the stratified null. The transport-ready gate failed.
- Distribution-level optimal transport: completed; no cell-state/module
  feature survived the patient-level max-T and sensitivity gates.
- Compositional log-ratio analysis: predeclared next; result pending.

## Decision Consequence

The current frontier is not another broad feature search. It is methods that
challenge transportability, distribution shape, and composition using
patient/cohort-level units. A null from these methods narrows the rational
next step toward new MS-specific longitudinal data rather than more
re-expression of the same public signal.
