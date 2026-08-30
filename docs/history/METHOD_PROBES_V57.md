# V57 Unexhausted-Method Exploration

Status: cumulative V57 synthesis. Held-data results, synthetic method behavior,
and external method proposals are kept separate throughout.

## Executive Verdict

V57 audited 30 analytical method families and completed 47 substantive
execution items beyond setup and synthesis. It did **not** discover a cure, a
better MS treatment, a therapeutic target, or an externally validated
biomarker. The broad held-public-data search remains exhausted under the V41
boundary.

It did find three useful, previously unexhausted routes:

1. **Privacy-preserving, multi-site validation of the frozen V22 monitoring
   rule.** A data owner can run pinned code locally, return a redacted and
   hash-attested aggregate, and contribute a valid same-estimand site record to
   an anytime-valid evidence accumulator. The small-site discrete-p-value
   behavior is now directly calibrated.
2. **A direction-resolving human functional-experiment route for progression.**
   Bidirectional CRISPRi/a in donor-replicated human iPSC microglia can precede
   crossed-donor glia organoid/assembloid confirmation. Synthetic design work
   specifies efficacy, safety, context, batch, variance, and model-escalation
   gates. This is an experiment proposal, not evidence for a target.
3. **Conditional combinatorial screening.** D-optimal pair selection can save
   resources only when prespecified descriptors predict interaction structure
   out of sample. A random-pair comparator and independent confirmation remain
   mandatory.

The held-data probes mostly returned corrected nulls or transport failures.
That is decision-useful: alternative mathematics did not extract a hidden,
replicable MS signal from the same information. Progress now requires new,
well-designed data or code-to-data access, not another unconstrained public-
data feature search.

## Epistemic Separation

| Result class | What it can establish | What it cannot establish |
|---|---|---|
| Held, non-quarantined data | A bounded property or null in the analyzed cohorts | External MS validation or causal treatment effect |
| Seeded synthetic method test | Operating characteristics of a fixed procedure under stated generators | MS biology, a real effect size, or an empirical sample-size guarantee |
| External method context | Feasibility and precedent for an experiment | A project-grounded finding or target |
| Model proposal | A candidate criticism or method idea | Evidence of any kind until separately tested |

## Held-Data Method Probes

| Method | Grounded outcome | Consequence |
|---|---|---|
| Environment invariance / worst-environment risk | Pooled weighted AUC `0.6722` (`p=0.0322`), but worst environment AUC `0.5111`; stringent stability failed | Do not describe the V22 association as environment-invariant |
| Class-conditional conformal prediction | Coverage was high, but only 6/43 predictions were singletons; singleton correctness was null-compatible (`p=0.236`) | Abstention is implementable but not transport-ready |
| Paired scalar optimal transport | No response-specific feature survived patient-level max-T and sensitivity gates | Distribution shifts did not rescue a response signal |
| Formal compositional CLR change | No subtype passed raw, residualized, corrected, and disease-direction gates across seeds | No response-specific composition claim |
| Joint multivariate state geometry | No compartment passed the joint geometry gate across cell-subsampling seeds | No hidden multivariate response geometry established |
| Cluster-free neighborhood DA | One residualized neighborhood nominally reached `p=0.048`, but failed raw (`p=0.156`) and cross-seed gates | Honest corrected null |
| Multivariate transport displacement fields | Best corrected p `0.5165`; raw/adjusted direction unstable | Honest corrected null |
| Persistent 0D topology | Frozen cell-count threshold left 4 non-remitting and 0 remitting patients | Not estimable; threshold was not weakened |
| Hierarchical partial pooling | Worse leave-one-cohort log score under all 12 priors; reference null `p=0.375` | Formal hierarchy is not ready for these data |
| Donor-state-module tensor model | Tensor AUC `0.670` versus additive `0.686`; max-model `p=0.168`, gain `p=0.492` | No reproducible interaction gain |
| Outcome-blind shift preflight | No cohort was concordantly OOD; GSE235357 was MMD-only across seeds | Retain as a prospective warning, not evidence adjustment |
| V22 specification curve | All 26 prespecified adjustments retained positive direction; broad joint adjustment AUC `0.656`, `p=0.163` | Supports direction robustness, not universal confounder independence |
| Cross-environment partial conjunction | At-least-two-environment p `0.464` (dependence-valid), `0.299` (independence sensitivity) | Cross-environment recurrence is not established |
| V22 leave-one-gene-out influence | Pooled family passes, cohort minimum AUC `0.68` | No single-gene collapse, but no external recurrence |
| Measurement invariance | Both frozen modules failed gene-edge concordance, exact identity nulls, and bootstrap stability | Treat modules as predictive summaries, not invariant latent constructs |
| Matched competitive module null | V22 AUC `0.822`; matched-null p `0.0196-0.0340` across settings | Weakens a broad arbitrary-module explanation; matching remains imperfect |
| Mechanism-boundary selective inference | Boundary survives max-six-pair correction (`p` about `0.027`) | The bounded layer-transfer claim survives this selection audit |
| Missing-label partial identification | Universal AUC at least `0.60` through 2 missing labels, or 3 with audited class prevalence; 4 can lower it to `0.433` | Returned packages need bounds, not favorable imputation |
| Successor non-superiority | Best observed successor delta `-0.078`, but family upper bound `+0.189` | No observed gain, but superiority is not formally excluded |
| Functional trajectories | Later common timepoints have only 1-2 patients per arm | Blocked on longitudinal data; no curve was fit |

## Verified Validation and Acquisition Methods

All rows in this section characterize methods, mostly on seeded synthetic data.
They do not add biological evidence.

| Method | Verification result | Operational use |
|---|---|---|
| Value-of-information portfolio | Eight packages x 21 methods; no universal winner, four two-package Pareto strategies | Match the request to the decision rather than naming one best dataset |
| Anytime-valid mixture e-process | 1.8M sequences; null crossing `1.254%-1.299%` by 20, strong alternative `99.946%-99.960%` | Accumulate independent, same-estimand site evidence without peeking |
| Discrete small-site e-process | Additional 1.8M sequences/21.6M site arrivals; null crossing `0.325%-0.394%`, effect `0.9` crossing `96.901%-97.043%` by 12 | Confirms calibration for exact and V42 plus-one permutation p-values |
| Tied-score small-site e-process | 900k sequences/10.8M arrivals with five score levels; null crossing `0.146%-0.220%`, effect `0.9` crossing `92.666%-93.014%` | Extends calibration to exact conditional tied-rank tests; response-dependent preprocessing remains excluded |
| Correlated-site stress test | Naive null crossing rose to `8.214%`; known-cluster maximum-p collapse limited it to `0.088%` but strong power fell as low as `2.99%` | Require auditable dependence clusters; test a more efficient valid cluster p-value |
| Bonferroni dependence-cluster remediation | Null crossing `0.186%-0.564%` and large gain over maximum-p, but minimum strong crossing `65.732%` failed the `75%` gate | Valid fallback, not verified as the routine cluster rule |
| Averaged cluster e-values | Null crossing `0.238%-0.644%` and beats Bonferroni, but three independent high-correlation clusters reach only `69.502%` strong crossing | Information-count limitation; size independent clusters rather than trying more transforms |
| Independent dependence-cluster sizing | Three clusters fail (`69.518%` minimum strong crossing); four first pass (`81.782%`, null max `0.434%`) | Conditional planning boundary: count independent clusters, not nominal sites |
| Clustered federated combiner | 7/7 synthetic fixtures pass; refuses too few clusters, incomplete overlap review, absent attestation, assignment errors, oversized clusters, and split source groups | Operationalizes known dependence without changing the independent-site combiner |
| Code-to-data executor | Valid synthetic packet passed 254 schema checks; tampered metric and leaked paired table failed | Run the frozen V42 rule behind a data-owner boundary |
| Federated site combiner | Valid attested aggregate passed; duplicate independence group, harness mismatch, and missing uncertainty failed | Combine only independent sites with identical estimand, rule, direction, and retained effect uncertainty |
| Effect-size-preserving federated schema | AUC, AUC CI, Hedges' g, and p-value now survive owner export through both combiners; regression `87/87` | Prevent a significance-only evidence path; no pooled effect is inferred |
| Causal-design router | 7/7 synthetic declarations correctly routed or refused | Prevent causal language when time zero, assignment, overlap, or outcomes are inadequate |
| Trial transport envelope | Fixed scale-stable guard eligible through synthetic shift `0.50`, fails at `0.75-1.00` | Predeclare when randomized-effect transport must abstain |
| Prospective batch allocation | Outcome-aware blinded-lab layout reduced response/batch coupling; outcome-blind covariate balance did not | Require outcome-stratified technical allocation when labels can be held by an independent allocator |
| Label/measurement integrity | 2.1M perturbations robust through reliability `0.50`; two label-pair swaps can reduce AUC to `0.433` | Audit label provenance and score reliability before interpretation |

## Progression Functional-Experiment Route

The untried route is not another association scan. It is a direction-resolving
human experiment:

1. CRISPRi and CRISPRa perturb both directions in donor-replicated human iPSC
   microglia or a simple microglia-neural co-culture.
2. Evaluate prespecified efficacy, neural-support/myelin, viability, guide
   coherence, context, batch, and negative-control endpoints.
3. Escalate only candidates for which a crossed-donor 3D glial model adds
   reproducible information or detects a replicated hidden harm.
4. Confirm in an independent model and donor set before any target claim.

The source-specific external method records are under
`knowledge_external/records/`. They remain separately classed, non-grounded
context rather than project evidence.

### Synthetic Design Boundaries

| Design question | Result |
|---|---|
| Can a donor-replicated multi-outcome gate control false promotion? | Yes; 8 donors was underpowered, and 12 was the first tested high-precision passing point |
| Do 9-11 donors suffice? | No point passed the complete gate; 11 narrowly missed the sensitivity-loss constraint |
| Does independent context confirmation prevent context-harm promotion? | Yes, but the initial design confirmed only `0-6.4%` of uniform rescues because viability precision dominated |
| What orthogonal safety precision is needed in the tested generator? | 12 donors/context, 3 guides, and 2 viability wells/guide was the least-resource passing point |
| Can donor count adapt without looking at effects? | A 96-df blinded pilot with a grid through 48/context passed all checks through `1.5x` noise |
| When should 3D replace or supplement 2D? | A 12/8 split detects complementary information and rejects redundancy/batch artifacts, but not hidden-harm safety reliably |
| What tested panel detects hidden 3D harm? | First all-seed pass at 32 training + 24 held-out donor pairs; mean `0.840`, minimum `0.826` |
| Does leave-one-donor improve the multifidelity gate? | Sensitivity stayed high, but the parent already rejected the constructed leverage artifact; added protection not demonstrated |
| Do negative controls control assay-wide artifacts? | Naive rule failed FWER `0.2438-0.2498`; finite-sample eight-test correction passed at 12/8 with FWER `<=0.0388` and artifact power `>=0.961` |
| Can D-optimal pair selection reduce a combinatorial screen? | Only when prespecified descriptors encode true interaction structure out of sample; random comparator remains required |

All donor counts above are conditional synthetic reference points. A real
experiment first needs blinded technical-replicate and donor-level variance;
the design must then adapt without viewing candidate effects.

## Independent-Lens Contribution

Claude and Gemini received only a generic multifidelity design, not repository
data. Their outputs were stored as non-grounded model records. Grounding had
three outcomes:

- leave-one-donor stability was useful as a sensitivity but did not reveal a
  material parent failure;
- their negative-control suggestion exposed an invalid naive family threshold
  and led to the verified finite-sample correction;
- errors-in-variables analysis remains blocked on blinded empirical technical-
  replicate variance.

RPT was smoke-tested but not used substantively because this critique did not
have a defensible tabular prediction input. Agreement among models was never
treated as evidence.

## Ranked Dedicated-Run Shortlist

### 1. Privacy-Preserving Same-Estimand Validation

**Why first:** it directly addresses the current bottleneck: relevant cohorts
may exist behind transfer restrictions. The executor, redaction verifier,
attestation, site schema, duplicate-dependence checks, exact estimand binding,
and discrete e-process are now implemented.

**Next test:** send the pinned code-to-data packet to one eligible Gafson,
Karolinska, or equivalent data owner. Before combination, independently verify
cohort eligibility, label definition, treatment/timepoint match, batch and
confounder diagnostics, and independence group. An author-run aggregate stays
less reproducible than data-in-hand and must be labeled accordingly.

### 2. Direction-Resolving Human Microglia-to-3D Functional Program

**Why second:** progression target direction cannot be resolved by another
public association scan. Bidirectional perturbation can distinguish inhibition
from restoration, while crossed-donor 3D confirmation tests neural-support and
myelin consequences that a microglia-only readout cannot.

**Next test:** obtain blinded pilot variance in at least the efficacy,
viability, and neural-support endpoints, then run the frozen adaptive sizing and
negative-control gates. No gene or combination is nominated by V57.

### 3. Descriptor-Validated Combinatorial Perturbation Design

**Why third:** context dependence is a recurrent project failure mode and may
require combinations rather than single nodes. The method earns use only if
mechanism descriptors predict held-out interactions better than random pair
selection.

**Next test:** predeclare descriptors and a random-pair comparator on pilot
single-perturbation data, then hold out donors and pairs. If descriptor value
does not replicate, use random coverage instead.

### 4. Trial/IPD Causal and Transport Router

**Why fourth:** HERCULES/ToleDYNAMIC-style packages could answer progression
questions, but only if time zero, assignment, outcomes, modifiers, and overlap
support the claimed estimand.

**Next test:** run the metadata-only router before any outcomes are opened.
Use the fixed transport envelope only after the source trial effect is
reproduced and required modifiers are present.

### 5. V22 Integrity Suite

**Why fifth:** specification curves, selection correction, competitive module
nulls, label bounds, influence checks, shift diagnostics, and measurement-
architecture cautions make the eventual validation harder to fool.

**Next test:** execute these as prespecified diagnostics around, never as
changes to, the immutable V22 rule on an eligible unseen cohort.

## Methods That Did Not Earn a Dedicated Run

- Environment invariance, conformal singleton prediction, hierarchical
  pooling, tensor interactions, formal composition, neighborhood DA,
  distributional transport, multivariate geometry, and topology did not clear
  their held-data gates.
- A flexible successor cannot be called equivalent or inferior merely because
  no observed gain occurred; current uncertainty still permits a meaningful
  gain. This is not a reason to tune on the validation cohort.
- Measurement invariance failed, so the module labels should not be interpreted
  as identical latent constructs across environments.
- The initial multifidelity safety claim and naive negative-control threshold
  were rejected rather than patched post hoc.

## Honest Boundary

V57 improved the route to evidence, not the biological endpoint. It found no
new intervention-grade target and no computational substitute for longitudinal
MS disability-linked data or direction-resolving human experiments. The most
defensible move is now to use the privacy-preserving route to validate the one
live monitoring signal and to seek the small amount of blinded pilot data
needed to launch a rigorously gated human functional program.

## Reproducibility Map

The V57 claim/artifact regression passes `87/87` checks. It verifies the main
negative boundaries, held-data null verdicts, synthetic labels, parent-gate
failures, calibrated extensions, privacy/tamper behavior, federated dependence
guards, mandatory site uncertainty, and external-record class markers. Run:

```bash
.venv/bin/python scripts/v57_regression_suite.py
```

- frontier audit: `meta/METHOD_FRONTIER_V57.md` and
  `analysis/v57_method_frontier/`
- live execution log: `meta/V57_QUEUE.md`
- code-to-data: `docs/validation/CODE_TO_DATA_VALIDATION_V57.md`
- federated accumulation: `docs/validation/FEDERATED_EVIDENCE_ACCUMULATION_V57.md`
- federated effect-size schema:
  `docs/validation/FEDERATED_EFFECT_SIZE_SCHEMA_V57.md`
- discrete-site calibration: `docs/validation/DISCRETE_SITE_EPROCESS_V57.md`
- tied-score calibration: `docs/validation/TIED_SITE_EPROCESS_V57.md`
- dependent-site stress: `docs/validation/DEPENDENT_SITE_EPROCESS_V57.md`
- Bonferroni dependence remediation:
  `docs/validation/DEPENDENT_SITE_BONFERRONI_V57.md`
- cluster-e dependence remediation:
  `docs/validation/DEPENDENT_SITE_EVALUE_V57.md`
- independent-cluster count boundary:
  `docs/validation/DEPENDENCE_CLUSTER_COUNT_V57.md`
- clustered federated operation:
  `docs/validation/CLUSTERED_FEDERATED_EVIDENCE_V57.md`
- multifidelity gate: `docs/validation/MULTIFIDELITY_ESCALATION_V57.md`
- adversarial safeguards:
  `docs/validation/MULTIFIDELITY_ADVERSARIAL_SAFEGUARDS_V57.md`
- every numerical result: corresponding `analysis/v57_*` directory and
  committed `scripts/v57_*` implementation
