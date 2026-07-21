# V54 Queue: Toward Halting MS Progression

Status: in-progress

V54 applies the mature toolkit to progression-specific, source-audited questions
without reopening the V41 public-data discovery boundary or weakening the
project's evidence standard.

## Timing

- Block start UTC: 2026-07-21T20:58:30Z
- Active target: 6h cumulative active time
- Projected target UTC if this interval stays continuous: 2026-07-22T02:58:30Z
- Active session intervals:
  - 2026-07-21T20:58:30Z - 2026-07-21T21:02:06Z (0h03m36s active)
  - 2026-07-21T21:02:06Z - OPEN
- Cumulative completed active runtime: 0h03m36s
- Wall-clock span: open

## Environment And Boundaries

- OpenGWAS authentication: POST-only checker passed HTTP 200 for `/gwasinfo`
  and `/tophits`; token expiry decoded locally as 2026-07-24 08:00 UTC.
- SAP AI Core health: Claude, Gemini, and RPT smoke-passed; AlphaFold and both
  structural/provenance gates remain available.
- Remote: `main` aligned with `origin/main` at block start (`5d538329`).
- V41 discovery-exhaustion boundary remains in force.
- V22/V42 locked rule and pre-registration remain immutable.
- Progression claims require source/batch audit before disease-stage or lesion
  localization is interpreted.

## Backlog

| item | status | note |
|---|---|---|
| Progression-data inventory and semantic contract | done | Seven datasets/packages audited; only cross-sectional PPMS-vs-SPMS and small-n lesion-state proxies are testable. No held transcriptomic dataset has longitudinal disability outcomes. |
| CD44/CXCR4 progressive-stage re-analysis | done | 44 source/tissue-compatible donors; 300k nulls. CD44/CXCR4 beta 0.343, CI -0.253 to 0.938, max-T p=0.787; same direction but inconclusive. No module passed the portable stage gate. |
| Frozen source/tissue-balanced stage-test plan | done | Amsterdam WM plus UK GM, donor-equal inference, five pre-existing modules, three-seed 300k null, BH plus max-T, and cross-source direction gate fixed before execution. |
| Smoldering-lesion / chronic-active microglia probe | done | Three exact active/inactive donor pairs plus 54 samples/21 donors and 300k wild nulls. No orthogonally supported module; receptor and lipid inconclusive, others not supported. |
| GSE279972 lysosomal morphology specificity audit | done | Fully adjusted beta 0.517, CI 0.199 to 0.834, wild p=0.00861, max-variant p=0.0453; all 21 LODO coefficients positive. Bounded foamy-morphology association only, not progression or target evidence. |
| Relapsing-to-progressive transition proxy audit | done | Seven datasets audited: 5 verified subject maps, 2 repeated transcriptomes, but 0 time-varying stage and 0 repeated disability/conversion. Transition is not identifiable; this is not a biological null. |
| Progression-specific module panel | done | No orthogonally supported module. OXPHOS is lower in foamy morphology (max-module p=0.0357) but direction-discordant across chronic-active pairs; resolution and MOCCI are inconclusive. |
| OXPHOS-versus-lysosomal foamy-state coupling sensitivity | done | Both survive mutual adjustment: OXPHOS beta -0.562, max-endpoint p=0.0114; lysosomal beta 0.463, max-endpoint p=0.0518; all LODO directions stable. Morphology-only. |
| CNS-intrinsic versus peripheral APC separation | done | No eligible compartment pair. GSE228330 baseline has RRMS n=10/SPMS n=5 and subtype/activity confounding (Fisher p=0.01698), plus no verified map, processed matrix, batch/composition, or disability. Localization is not identifiable, not a peripheral null. |
| Progression intervention-direction map | done | Sequential audit of 9 states: 0 pass the progression-specific gate, 0 target revisits. V53 context supplies 0 replicated selective control nodes, 0 additive-pair passes, and 0 consensus causal orientations. |
| AlphaFold progression-axis context | done | Not eligible: no candidate reached progression association, pathogenic direction, causal specificity, and selective perturbation gates. Structure was deliberately not used as target decoration. |
| Multi-lineage adversarial progression review | done | All 12 objections grounded. Two changed the morphology evidential grade; zero changed progression/target verdicts. Independent lenses added value through a real downgrade, not a new positive lead. |
| Macnair source-by-stage interaction review check | done | Five modules, 44 donors, 300k reduced-model wild nulls. No interaction passes. CD44/CXCR4 source effects are nearly equal but imprecise; lysosomal heterogeneity is inconclusive. |
| Global post-result morphology multiplicity audit | done | Holm across all 12 sequential follow-up tests. Only a partial resident-adjusted variant passes; fully adjusted lysosomal and both mutual-adjustment endpoints fail. Claim-level morphology wording downgraded to exploratory. |
| Foamy donor/lesion estimand and influence audit | done | Only 6/21 donors and 3/43 donor-lesion blocks vary in morphology. Donor-FE OXPHOS is direction-retained but null/unstable; lysosomal reverses near zero. Pooled inference is substantially between-donor or unresolved. |
| Progression power calibration and assumption audit | done | Null calibration acceptable: maximum 0.060 has Wilson 0.049-0.073, no lower bound >0.05, 48-cell reference max-tail p=0.895. Label-noise sensitivity completed without empirical-MS interpretation. |
| Multi-lineage objection disposition table | done | Complete artifact-traced table and four agreement clusters committed; model assertions remain proposal-only external records. |
| Progression-cohort acquisition specification | done | Three-role contract (longitudinal progression, paired compartment, functional direction) with 64 unique required fields and fail-closed intake actions. No powered sample size inferred from held data. |
| Progression package eligibility validator | done | Six synthetic role fixtures: 3 complete P1/P2/P3 pass, 3 malformed packages fail closed. Real source paths must exist; pass means inventory-ready only. |
| Progression-event power design skeleton | done | 288k synthetic cohorts/3 seeds/192 cells; null FPR median 0.043, max 0.060. Only 7/24 non-null scenarios reached 80%; OR 1.25/1.5 not by n=240. Assumption-labeled, not empirical. |
| Progression power label-noise sensitivity | done | 576k additional synthetic cohorts. Scenarios reaching 80% fall 7/24 -> 4/24 -> 3/24 at 0/5/10% symmetric label error; endpoint adjudication is a hard design requirement. |
| Progression power covariate/event-time extension | done | 90k synthetic cohorts/180k route evaluations. Stratified null median 0.046/max 0.0653 (40-cell max-tail 0.776); deliberate-confounding unadjusted null median 0.0887/max 0.1907. PHReg reference check passes. |
| Progression P1/P2 blinded preregistration template | done | Frozen process contract covers endpoint/timepoint, censoring, covariates, P2 interaction, missingness, multiplicity, and pass/fail/inconclusive semantics before score access. |
| Progression validator malformed-input expansion | done | Eight synthetic malformed/path fixtures added. They exposed and fixed a bug where nonexistent source paths were logged but did not fail `field_gate_pass`; all 14 total regressions now pass. |
| Progression outcome semantic checker | done | Twelve synthetic declarations: valid CDP/PIRA/P2 pass; nine proxy, incomplete, unconfirmed, or unblinded declarations fail closed. Method behavior only. |
| Joint foamy-state lesion-stratum transport sensitivity | done | Classes 2/3 eligible; NAWM ineligible (4 foamy donors). Neither endpoint passes within-stratum family gates; OXPHOS same-direction but imprecise, lysosomal reverses in class 2. Pooled state is not stratum-portable. |
| Foamy morphology-by-lesion heterogeneity test | done | Direct class-3-minus-class-2 interactions: OXPHOS beta 0.115, max-family p=0.940; lysosomal beta 0.004, p=1.000; LODO signs unstable. No heterogeneity support, but wide CIs do not establish homogeneity. |
| GSE228330 progression metadata request addendum | done | Ready-unsent 29-field addendum requests subject map, a/s definition, age, disability/PIRA components, relapse/steroid/treatment, MRI, composition, batch/QC, and matrix. Context-only unless full role gate passes. |
| V37 progression evidence-grade delta | done | Artifact-checked 18-item delta: 12 V37 items carried, 6 post-V37 additions; 2 method-strengthened, 3 progression-narrowed, 1 negative reinforced, and no target/progression promotion. |
| Combined P1/P2 intake gate orchestrator | done | Nine synthetic cross-gate fixtures pass: valid P1/P2 and additive metadata accepted; component failures, role/endpoint/package mismatch, and prior score access fail closed. |
| P2 compartment-interaction power design | done | 288k synthetic cohorts/576k route evaluations. Direct interaction is calibrated with perfect composition, or noisy composition when no imbalance exists; noisy adjustment under true imbalance remains invalid. Trusted adjusted scenarios reach 80% in 27/36 cells; independent OLS reference check passes. |
| Event-time assumption robustness | done | 225k synthetic cohorts/675k window evaluations. Four censoring families calibrate; joint score/event-risk censoring is invalid (null median 0.544, max 0.795, all spurious-negative). Crossing effects are detected only 0.127-0.157 overall at n=320/event=0.30 despite opposite window recovery. Four numerical references pass. |
| Progression endpoint adjudication fixtures | done | Eleven synthetic CDP/PIRA fixtures pass: confirmed, transient, missing/mistimed confirmation, relapse/steroid exclusion, component discordance, switch censoring, and invalid baseline. CDP and PIRA remain distinct. |
| Progression cohort candidate role matrix | todo | Apply only metadata/semantic contracts to known candidates; no score access and no cohort counted eligible without verification. |
| Event-time receipt diagnostics contract | done | Additive blind metadata gate requires complete censoring dates/reasons, source-treatment strata, IPCW/worst-case/joint-dependence sensitivities, and time-variation diagnostics. Eight synthetic fixtures pass expected fail-closed behavior. |
| P2 composition measurement acceptance contract | done | Direct linked measurements pass eligibility; proxies require a blinded direct-reference subset, reported reliability, rerun null calibration, and sensitivity-only interpretation. Expression-derived proxy alone fails. Nine synthetic fixtures pass. |
| V54 consolidated regression suite | todo | One command for progression scripts, semantic/intake gates, numerical references, provenance/structure, and claim consistency. |
| Cumulative V54 progression report | todo | Maintain `docs/history/PROGRESSION_FRONTIER_V54.md` with supported/null/inconclusive outcomes and no target inflation. |
| V54 regression, provenance, structure, size, RAG, and clean close | todo | Run all gates, rebuild retrieval index, commit and push each clean iteration. |

## Per-Iteration Notes

- 2026-07-21T20:58:30Z: V54 block started from clean, synchronized
  `main` at `5d538329`. The initial backlog prioritizes a semantic inventory
  before any stage claim so cross-sectional/source-confounded data cannot be
  misread as evidence about progression.
- 2026-07-21T21:02:06Z: Resumed immediately after a health-check interruption.
  The OpenGWAS POST-only check completed successfully (HTTP 200); no idle gap
  was charged to active time.
- 2026-07-21T21:05:04Z: Progression semantic inventory completed over seven
  held datasets/packages. Two bounded questions are executable; four decisive
  questions are blocked or non-identifiable. The first real-data test is a
  source-overlap-restricted PPMS-versus-SPMS module comparison, not a
  transition, progression-rate, or treatment-benefit claim.
- 2026-07-21T21:05:04Z: Froze `PROGRESSION_STAGE_TEST_V54.md`. The design
  prevents source/tissue mixing, uses only five pre-existing modules, and
  requires cross-source directional agreement plus HC3, permutation, BH, and
  max-T gates.
- 2026-07-21T21:07:04Z: Iteration 1 ready for commit: inventory, semantic
  contract, cumulative report, and frozen stage-test plan pass provenance,
  structural, syntax, whitespace, and size/path guards. Active time accrued
  through this checkpoint: 0h08m34s; the resumed interval remains open.
- 2026-07-21T21:10:15Z: Completed the frozen source/tissue-balanced stage
  test on 44 donors with 300,000 three-seed nulls. No module passed. CD44/CXCR4
  and IFN/APC were same-direction across Amsterdam and UK but statistically
  inconclusive; HLA, MIF, and lysosomal effects were direction-discordant. No
  progression, target, or therapeutic claim was upgraded.
- 2026-07-21T21:17:30Z: Completed the frozen two-dataset lesion-state test.
  No module passed the orthogonal-context gate. CD44/CXCR4 was positive in all
  three active/inactive pairs but null in the 21-donor morphology cohort;
  lysosomal state passed the morphology family-wise gate but was not consistent
  across active-edge donors. The isolated lysosomal result is queued for a
  composition-specificity sensitivity and is not a progression or target lead.
- 2026-07-21T21:18:29Z: Iteration 3 ready for verification and commit. Active
  time accrued through this checkpoint: 0h19m59s; the resumed interval remains
  open.
- 2026-07-21T21:22:27Z: The frozen post-result lysosomal morphology
  specificity audit completed. Its fully adjusted association survived 300,000
  donor-wild nulls, max-variant correction, three-seed stability, and all 21
  leave-one-donor fits. It remains strictly bounded to foamy morphology because
  the adjustments are transcript-state proxies and the chronic-active-edge
  dataset did not supply directional replication. Active time accrued through
  this checkpoint: 0h23m57s; the resumed interval remains open.
- 2026-07-21T21:24:47Z: Froze the transition-identifiability contract before
  execution. A valid transition dataset must link repeated transcriptomes,
  time-varying subtype/conversion status, repeated disability or adjudicated
  conversion, and treatment context to a verified subject ID. Relapse,
  pregnancy, pharmacodynamic, and same-death lesion repeats fail closed rather
  than serving as progression surrogates. Active time accrued: 0h26m17s.
- 2026-07-21T21:28:02Z: Executed the transition-identifiability gate over
  seven held datasets. Five have verified subject maps and two have repeated
  transcriptomes, but none measures time-varying stage or repeated disability/
  adjudicated conversion. GSE24427's two-year relapse follow-up is explicitly
  not substituted for disability progression. Active time accrued: 0h29m32s.
- 2026-07-21T21:31:02Z: Froze a second, non-overlapping progression-lesion
  family using only pre-existing project modules: OXPHOS, resolution/
  efferocytosis proxy, NRF2 antioxidant response, stress/cytotoxicity, and the
  signed MOCCI switch. Iron and senescence remain untested rather than receiving
  post hoc signatures. Active time accrued: 0h32m32s.
- 2026-07-21T21:34:50Z: Completed the five-module lesion panel. No module
  transferred through the orthogonal-context gate. A family-wise-significant
  OXPHOS decrease in foamy morphology reverses the majority chronic-active
  direction and remains morphology-bounded; resolution/efferocytosis and MOCCI
  are concordant but inconclusive. Active time accrued: 0h36m20s.
- 2026-07-21T21:37:04Z: Froze the post-result OXPHOS/lysosomal mutual-
  adjustment sensitivity. Two disjoint scores, two corrected endpoints,
  300,000 donor-wild nulls, and LODO stability will test separability without
  upgrading either morphology association. Active time accrued: 0h38m34s.
- 2026-07-21T21:39:15Z: Mutual adjustment retained 90.2% of the OXPHOS
  coefficient and 89.7% of the lysosomal coefficient; both pass the corrected
  donor-wild and LODO gates. This is a two-feature foamy transcript state in one
  cohort, not progression or intervention evidence. Active time accrued:
  0h40m45s.
- 2026-07-21T21:43:28Z: The frozen CNS-versus-peripheral eligibility audit
  found zero valid compartment pairs. GSE228330 baseline has 10 RRMS and 5 SPMS
  samples, with subtype/activity imbalance (Fisher `p=0.01698`) and no verified
  subject map, processed matrix, batch/composition fields, or disability
  trajectory. No peripheral expression test was run; the result is an
  identifiability boundary, not a biological null. Active time accrued:
  0h44m58s.
- 2026-07-21T21:47:09Z: Completed the frozen intervention-direction map over
  nine pre-existing states. Zero passes the first progression-specific gate;
  held V53 perturbations add zero replicated selective control nodes, zero
  corrected additive-pair passes, and zero consensus causal orientations.
  AlphaFold context is ineligible and was not used. Active time accrued:
  0h48m39s.
- 2026-07-21T21:50:28Z: The frozen lesion-stratum transport sensitivity found
  no corrected transport of either foamy-state endpoint across eligible classes
  2 and 3. OXPHOS retained its negative direction but was imprecise; lysosomal
  direction reversed in class 2. NAWM was ineligible with four foamy donors.
  This narrows the pooled morphology result without claiming a subgroup null.
  Active time accrued: 0h51m58s.
- 2026-07-21T21:53:58Z: A direct two-endpoint morphology-by-lesion interaction
  test found no supported heterogeneity (OXPHOS max-family `p=0.940`;
  lysosomal `p=1.000`; both LODO signs unstable). This avoids comparing
  subgroup p-values but does not establish homogeneity because intervals are
  wide. The pooled morphology state remains context-bounded and unresolved.
  Active time accrued: 0h55m28s.
- 2026-07-21T21:56:37Z: Completed the exact progression-cohort acquisition
  contract. It separates longitudinal disability/PIRA, paired-compartment, and
  functional-direction roles and defines 64 unique required fields with
  fail-closed actions. It explicitly forbids relapse, stage, morphology, or
  pharmacodynamics from substituting for disability progression. Active time
  accrued: 0h58m07s.
- 2026-07-21T21:58:21Z: Completed a ready-unsent GSE228330 progression-metadata
  addendum and 29-field return schema. It requests the exact fields blocking
  pairing, subtype interpretation, progression, composition, and batch control;
  the cohort remains pharmacodynamic context unless the returned package passes
  the new role gate. Active time accrued: 0h59m51s.
- 2026-07-21T22:00:52Z: Implemented the progression-package inventory gate and
  verified six clearly labeled synthetic fixtures. Complete P1/P2/P3 inventories
  pass; missing outcome, pairing/composition/batch, or progression-prequalified
  functional fields fail closed. A pass is intake readiness only. Active time
  accrued: 1h02m22s.
- 2026-07-21T22:03:56Z: Completed a 288,000-cohort, three-seed synthetic
  progression-event power grid. Null FPR was calibrated (median `0.043`, maximum
  `0.060`). Only 7/24 non-null scenarios reached 80%; assumed OR 1.25/1.5 did
  not by `n=240`. This is method-design evidence only, not an empirical MS
  effect or universal N target. Active time accrued: 1h05m26s.
- 2026-07-21T22:10:32Z: Claude and Gemini independently returned six
  progression-method objections each. Their outputs were segregated as
  proposal-only external records. Multi-lineage agreement prioritizes
  the Macnair source-by-stage interaction; Claude also identified a substantive
  family-definition issue across the sequential morphology follow-ups. Both
  audits were frozen before execution. Active time accrued: 1h12m02s.
- 2026-07-21T22:16:23Z: Grounded the two priority review checks. No Macnair
  source-by-stage interaction passed the frozen five-module gate. The complete
  12-test post-result morphology family produced a substantive downgrade: the
  required fully adjusted lysosomal endpoint (Holm `p=0.0861`) and both
  mutually adjusted endpoints (each `p=0.0960`) fail global family control.
  Their coefficients remain descriptive, but V54 now labels them exploratory
  post-result morphology associations. Active time accrued: 1h17m53s.
- 2026-07-21T22:21:52Z: Replaced Gemini's invalid repeated-sample Fisher
  proposal with a frozen donor-estimand audit. Only 6/21 donors and 3/43
  donor-by-lesion blocks contain both morphology labels. In the six informative
  donors, OXPHOS retained direction but was null and LODO-unstable; lysosomal
  reversed near zero. The pooled morphology coefficients are substantially
  between-donor or unresolved. Active time accrued: 1h23m22s.
- 2026-07-21T22:25:22Z: Closed both simulation objections. The default null
  grid is acceptably calibrated: the 0.060 maximum is 90/1,500 (Wilson
  `0.049-0.073`), no cell's lower bound exceeds 0.05, and the 48-cell
  binomial-reference max-tail is `0.895`. A further 576,000 synthetic cohorts
  show material sensitivity to outcome error: 80%-passing scenarios decline
  from 7/24 to 4/24 at 5% and 3/24 at 10%. No rate is presented as an empirical
  MS or PIRA estimate. Active time accrued: 1h26m52s.
- 2026-07-21T22:28:14Z: Closed all 12 Claude/Gemini objections with an
  artifact-traced disposition table. Two concerns held strongly enough to
  change evidential grade, both narrowing the foamy morphology state; none
  changed a progression or target verdict. The independent review therefore
  added value through a substantive downgrade rather than a new positive lead.
  Model spend remains unavailable from the current AI Core response path.
  Active time accrued: 1h29m44s.
- 2026-07-21T22:33:22Z: Completed the blinded P1/P2 process contract and
  endpoint semantic gate. Three valid synthetic disability declarations pass;
  nine relapse/stage/morphology/pharmacodynamic proxy, incomplete,
  unconfirmed, interaction-free, or unblinded declarations fail closed. This
  is method behavior only and leaves no new progression claim. Active time
  accrued: 1h34m52s.
- 2026-07-21T22:36:49Z: Expanded the progression intake regression to 14
  synthetic fixtures. A new nonexistent-path case exposed a real validator
  defect: the issue was logged but did not enter the pass boolean. The logic is
  fixed, and duplicate, unknown-additive, unknown-substitution, missing-path,
  unverified, zero-nonmissing, and missing-column behavior now passes its
  permanent regression. Active time accrued: 1h38m19s.
- 2026-07-21T22:44:03Z: Completed the frozen 90,000-cohort progression
  event-time design with 180,000 route evaluations. The source/treatment-
  stratified null is compatible with nominal calibration (median 0.046,
  maximum 0.0653; 40-cell reference max-tail 0.776), while deliberate
  confounding inflates the unadjusted null median to 0.0887 and maximum to
  0.1907. Four PHReg numerical reference fixtures pass to 2.67e-15. This is
  synthetic method behavior only. Active time accrued: 1h45m33s.
- 2026-07-21T22:48:18Z: Completed an artifact-checked 18-item progression
  delta against V37. Twelve historical items retain their original relevance/
  novelty scores and are classified only for V54 scope; six post-V37 items are
  added without invented scores. No item becomes progression evidence or a
  target. Active time accrued: 1h49m48s.
- 2026-07-21T22:50:35Z: Combined inventory and endpoint semantics into one
  fail-closed intake decision. Nine synthetic fixtures bind package ID, role,
  endpoint, synthetic status, and score blindness; valid P1/P2 plus additive
  metadata pass, while every component or cross-gate mismatch fails. Active
  time accrued: 1h52m05s.
- 2026-07-21T22:52:30Z: Froze the P2 compartment-interaction power plan before
  simulation. It requires a direct paired or unpaired interaction, varies
  compartment correlation and composition imbalance/reliability, and forbids
  difference-of-significance localization. Active time accrued: 1h54m00s.
- 2026-07-21T22:57:28Z: Completed 288,000 unique synthetic P2 cohorts and
  576,000 direct-interaction route evaluations. Calibrated regimes reached the
  frozen 80% threshold in 27/36 non-null scenarios. Noisy composition
  adjustment under true imbalance was anti-conservative (null maximum
  `0.2227`) and is excluded from power interpretation; unadjusted imbalance was
  worse (maximum `0.5827`). Four independent `statsmodels` OLS fixtures pass
  to `2.22e-15`. Active time accrued: 1h58m58s.
- 2026-07-21T22:59:53Z: Froze the event-time assumption audit before
  simulation. It distinguishes proportional, early-only, late-only, and
  crossing effects and five censoring mechanisms, including a deliberately
  non-independent joint score/event-risk mechanism. Window-specific tests are
  diagnostic only and cannot replace the frozen whole-follow-up Cox route.
  Active time accrued: 2h01m23s.
- 2026-07-21T23:09:01Z: Completed 225,000 synthetic event-time cohorts and
  675,000 whole/early/late evaluations. Administrative, independent,
  score-dependent, and event-risk-only censoring pass the whole-follow-up null
  rule. Joint score/event-risk censoring is strongly anti-conservative (null
  median `0.544`, maximum `0.795`, all significant calls spurious-negative).
  Crossing effects are largely canceled in one coefficient despite opposite
  window signs. Four scalar/probability/PHReg reference checks pass to
  `2.94e-15`. Active time accrued: 2h10m31s.
- 2026-07-21T23:12:48Z: Converted the event-time failures into an additive,
  blinded receipt gate without editing the frozen P1/P2 pre-registration.
  Administrative-only and documented nonadministrative fixtures route as
  specified; unknown/outcome-related loss, missing dates or diagnostics,
  unblinding, and window-p-value substitution fail closed. All eight synthetic
  fixtures pass expected behavior. Active time accrued: 2h14m18s.
- 2026-07-21T23:13:52Z: Froze the synthetic CDP/PIRA adjudication regression
  before implementation. Ten edge-case families have predetermined decisions,
  including transient or discordant worsening, relapse/steroid exclusion,
  missing or mistimed confirmation, censoring before confirmation, and invalid
  baseline. Active time accrued: 2h15m22s.
- 2026-07-21T23:16:19Z: Implemented the parameterized endpoint processor and
  completed 11/11 synthetic regressions. A fixture-marker boolean identity bug
  was exposed and fixed before commit. Confirmed CDP is retained where the same
  worsening is PIRA-excluded by relapse; missing/mistimed confirmation and
  pre-confirmation censoring remain inconclusive rather than negative. Active
  time accrued: 2h17m49s.
- 2026-07-21T23:18:09Z: Implemented the P2 composition-method acceptance gate.
  Direct linked flow/CyTOF/CITE-seq/single-cell counts are eligible for
  cohort-specific calibration; proxies require a blinded direct-reference
  subset and an empirical null-calibration pass and remain sensitivity-only.
  Expression-derived proxies, missing linkage, outcome selection, and
  unresolved missingness fail. All 9 synthetic fixtures pass. Active time
  accrued: 2h19m39s.
