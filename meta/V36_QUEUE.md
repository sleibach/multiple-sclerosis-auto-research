# V36 Queue - Two-Hour Autonomous Block

## Timing

- Block start UTC: 2026-06-07T18:27:35Z
- Target end UTC: 2026-06-07T20:27:35Z
- Timing source: real `date -u` system-clock reads.

## Iteration Log

### Iteration 1

- Start UTC: 2026-06-07T18:27:35Z
- End UTC: 2026-06-07T18:30:25Z
- Status: completed
- Item selected: Extend SAP AI Core client to SAP RPT and smoke test.
- Note: First V36 action. Verify credentials/OpenGWAS/client state, then add
  RPT support so the tabular lens can be used for structured hypothesis
  generation.
- Result: SAP RPT path added to `scripts/sap_ai_core_client.py` using
  `POST <deploymentUrl>/predict`; `sap-rpt-1-large` deployment
  `d61aae51af327bbc` smoke-passed with status `ok` and predicted the held-out
  toy row as `high` with confidence `0.96`. Access contract documented in
  `meta/SAP_AI_CORE_ACCESS_V30.md`.

### Iteration 2

- Start UTC: 2026-06-07T18:30:25Z
- End UTC: 2026-06-07T18:33:04Z
- Status: completed
- Item selected: RPT-driven structured-data hypothesis pass.
- Note: Build structured project tables for RPT masked-label/anomaly probing,
  collect RPT-surfaced tabular patterns, and ground them on real data before
  counting anything.
- Result: RPT masked-verdict pass completed over a 13-row compact lead table.
  RPT concordantly predicted T/B gate as `promising_followup`, complement/lipid
  and EBV as `negative_or_not_now`, down-ranked postpartum for missing
  response/null-tested data, and up-ranked metabolic/sterol plus lysosomal APC
  structurally. Grounding against V35/V32/V26 evidence produced no upgrades;
  the output sharpened data needs and failure gates in
  `docs/history/HYPOTHESIS_SLATE_V36.md`.

### Iteration 3

- Start UTC: 2026-06-07T18:33:04Z
- End UTC: 2026-06-07T18:37:36Z
- Status: completed
- Item selected: Expansive tri-source generation round.
- Note: Use Claude, Gemini, RPT output, and agent-native interpretation to
  generate broader hypotheses, consolidate/de-duplicate, then ground the
  executable subset.
- Result: Claude produced 8 valid JSON hypotheses; Gemini produced 8 JSON
  hypotheses inside a markdown fence and was parsed by the consolidation
  script. Grounded first executable subset: tofacitinib glycolytic-brake
  hypothesis is all-cell context only (`delta_glycolysis` AUC `0.95`, exact p
  `0.0317`, no Treg/T-cell-specific matrix); sterol/lysosomal coupling remains
  not supported as a unified bottleneck because lesion-edge lysosomal
  cholesterol is weak/non-significant despite strong Mixscale lysosomal APC
  coupling.

### Iteration 4

- Start UTC: 2026-06-07T18:37:36Z
- End UTC: 2026-06-07T18:40:04Z
- Status: completed
- Item selected: T/B compartment remodeling gate artifact audit.
- Note: Test whether the current top lead can be explained by composition or
  generic T-cell/B-cell abundance proxies in existing exact compartment data.
- Result: Simple count/fraction artifact did not explain away the gate:
  T/B-minus-non-T/B AUC gap remained positive after residualizing locked scores
  against baseline/delta compartment fractions (`0.158` -> `0.133`). The
  T-cell component attenuated strongly (`1.000` -> `0.650`), while B/plasma
  remained more stable (`0.950` -> `0.850`). Refined lead: B/plasma-like
  remodeling is the more robust compartmental carrier; T-cell component may be
  partly composition/sampling-sensitive.

### Iteration 5

- Start UTC: 2026-06-07T18:40:04Z
- End UTC: 2026-06-07T18:41:15Z
- Status: completed
- Item selected: Postpartum APC-arm imbalance MS-specificity.
- Note: Deepen reachable grounding for postpartum/MS specificity using local
  pregnancy and cross-disease APC-arm artifacts; specify remaining data need.
- Result: Local MS data supports pregnancy-phase HLA-II-minus-CD64 movement
  from pre-pregnancy to month 9 (paired delta `-1.168`, p `0.0432`) but has no
  postpartum samples or relapse labels. Cross-disease postpartum data shows
  HLA-II-minus-CD64 rebound in healthy/SLE/RA contexts, not MS-specificity.
  Verdict remains high-priority data acquisition, not a finding.

### Iteration 6

- Start UTC: 2026-06-07T18:41:15Z
- End UTC: 2026-06-07T18:42:32Z
- Status: completed
- Item selected: Remaining V35 shortlist deepening.
- Note: Revisit metabolic/sterol, lysosomal, complement/lipid, and EBV/IFN
  after RPT and generation outputs; identify any executable heavier analysis or
  confirm blocked/null status.
- Result: No upgrades. Metabolic/sterol remains context-supported but not
  intervention-grade; lysosomal APC remains perturbation-coupled but not a
  proven bottleneck; complement/lipid remains donor-aware downgraded; EBV/IFN
  and generated rare-B-cell variants require EBV-stratified B-cell/APC data;
  neuropeptide B-cell and Treg-senescence variants lack required held metadata.

### Iteration 7

- Start UTC: 2026-06-07T18:42:32Z
- End UTC: 2026-06-07T18:46:12Z
- Status: completed
- Item selected: Deep multi-pass cross-examination of top grounded hypotheses.
- Note: Use Claude and Gemini with higher budget to attack the refined T/B
  gate and postpartum acquisition lead; ground concrete criticisms where held
  data allows.
- Result: Gemini produced usable critiques; Claude output was empty in this
  round and was not counted. Grounding showed the T/B gap is positive but
  bootstrap-fragile (raw gap bootstrap mean `0.145`, 95% CI `0.000-0.285`,
  p(gap <= 0) `0.0402`), B/plasma-only AUC `0.95` matches T/B mean AUC `0.95`,
  and MS pregnancy HLA-II/CD64 arms are separable (Spearman `0.022`). Lead
  interpretation refined, no upgrade.

### Iteration 8

- Start UTC: 2026-06-07T18:46:12Z
- End UTC: 2026-06-07T18:47:17Z
- Status: completed
- Item selected: Heavier analyses now affordable.
- Note: Use larger permutation/bootstrap or broader scans for the leading
  hypotheses where executable; start with exact/randomization hardening of the
  refined B/plasma carrier.
- Result: Exhaustive 31-combination compartment scan completed. T-cell alone
  had raw AUC `1.000`, B/plasma alone AUC `0.950`, and T/B mean AUC `0.950`.
  Many multi-compartment combinations reached AUC `1.000`, adding an overfit
  warning rather than an upgrade. Future validation must pre-specify B/plasma
  and T-cell components separately.

### Iteration 9

- Start UTC: 2026-06-07T18:47:17Z
- End UTC: 2026-06-07T18:48:14Z
- Status: completed
- Item selected: Generate next executable V36 backlog items.
- Note: The seeded backlog has been worked once; create further executable
  strict-grounding items to continue the 120-minute block.
- Result: Added follow-up executable items for B/plasma-specific module
  decomposition, cross-disease B/plasma proxy scout, and RPT second pass with
  refined B/plasma/T-cell split.

### Iteration 10

- Start UTC: 2026-06-07T18:48:14Z
- End UTC: 2026-06-07T18:49:15Z
- Status: completed
- Item selected: B/plasma-specific module decomposition.
- Note: Decompose the refined top lead to identify whether B/plasma
  discrimination is driven by IFN/APC, HLA-II, receptor, or count/fraction
  components.
- Result: B/plasma-like discrimination is carried by `delta_IFN_APC` /
  locked signed score (AUC `0.950`, exact p `0.0317`), not HLA-II alone
  (AUC `0.700`), receptor genes alone (AUC `0.750`), or baseline abundance.
  Mechanistic carrier refined to B/plasma IFN/APC dynamic remodeling.

### Iteration 11

- Start UTC: 2026-06-07T18:49:15Z
- End UTC: 2026-06-07T18:50:57Z
- Status: completed
- Item selected: Cross-disease response-cohort B/plasma proxy scout.
- Note: Search held response cohorts for B/plasma proxy genes or deconvolution
  features that can independently test the refined B/plasma carrier.
- Result: Blocked for independent replication with held data. `GSE253006` is
  the only saved compartment-resolved paired response cohort; MS IFN-beta and
  V22/V23 ledgers contain locked module scores but no B/plasma marker or
  deconvolution score sufficient to test the refined B/plasma carrier.

### Iteration 12

- Start UTC: 2026-06-07T18:50:57Z
- End UTC: 2026-06-07T18:54:28Z
- Status: completed
- Item selected: RPT second pass with refined B/plasma/T-cell split.
- Note: Update structured table with V36 refined features and ask RPT for
  masked verdict/carrier predictions after new groundings.
- Result: RPT refined carrier pass completed over 10 rows. RPT classified
  T-cell raw, B/plasma locked score, B/plasma IFN/APC delta, receptor-only, and
  T/B mean as `promising_but_unreplicated`, and classified B/plasma HLA-II-only
  as `weak_or_unbounded`. Grounding overrides RPT where needed: B/plasma IFN/APC
  remains the best real-data carrier, T-cell remains composition-sensitive, and
  no carrier is upgraded without independent replication.

### Iteration 13

- Start UTC: 2026-06-07T18:54:28Z
- End UTC: 2026-06-07T18:56:40Z
- Status: completed
- Item selected: Gene-level B/plasma IFN/APC driver analysis.
- Note: Test whether the B/plasma IFN/APC carrier is broad module remodeling or
  dominated by one/few genes in the n=9 exact compartment data.
- Result: B/plasma gene driver scan completed. `STAT1` alone had oriented AUC
  `1.000`, exact p `0.0159`, and leave-one-out minimum AUC `1.000`; `IRF1`,
  `GBP1`, and `ISG15` moved in the same responder-associated downshift
  direction but did not independently clear exact p <= `0.05`. Interpretation:
  carrier sharpens to B/plasma IFN/STAT remodeling, not HLA-II-only or
  receptor-only, but remains n=9 and post-hoc.

### Iteration 14

- Start UTC: 2026-06-07T18:56:40Z
- End UTC: 2026-06-07T18:58:22Z
- Status: completed
- Item selected: Timepoint and responder-leverage sensitivity for B/plasma
  IFN/STAT carrier.
- Note: Test whether the B/plasma IFN/STAT result is driven by the single W48
  responder or another high-leverage patient/timepoint.
- Result: Internal sensitivity strengthened the refined carrier. Excluding the
  W48 responder (`TOF_009`) left the locked B/plasma score at AUC `0.938`
  (exact p `0.0571`) and STAT1 downshift at AUC `1.000` (exact p `0.0286`).
  Leave-one-out minimum AUC was `0.933` for locked B/plasma score and `1.000`
  for STAT1. Still internal robustness only, not external validation.

### Iteration 15

- Start UTC: 2026-06-07T18:58:22Z
- End UTC: 2026-06-07T18:59:50Z
- Status: completed
- Item selected: Cross-compartment STAT1/IFN specificity scan.
- Note: Test whether STAT1/IFN downshift is B/plasma-specific or a generic
  compartment-wide response feature.
- Result: STAT1 downshift is not B/plasma-specific: B/plasma and myeloid-like
  compartments both had STAT1 AUC `1.000` (exact p `0.0159`), and other
  compartments were high. Locked score was strongest in T-cell (AUC `1.000`)
  and B/plasma (AUC `0.950`). Interpretation weakened from B/plasma-specific
  STAT1 carrier to broad IFN/STAT downshift with candidate T-cell/B-plasma
  compartmental readouts.

### Iteration 16

- Start UTC: 2026-06-07T18:59:50Z
- End UTC: 2026-06-07T19:01:37Z
- Status: completed
- Item selected: Same-compartment random/module negative control for IFN/STAT
  signal.
- Note: Test whether locked IFN/STAT performance is exceptional relative to
  random matched gene modules available in the exact compartment matrix.
- Result: Genome-wide random null was impossible from the exact compartment
  artifact, which contains only locked genes. A limited same-size locked-gene
  combo null found the IFN/STAT four-gene set was not exceptional in B/plasma
  (`5/15` same-size combos matched/beat it; empirical p `0.3333`) or other
  compartments. This blocks a narrow STAT1/IRF1/GBP1/ISG15 module claim.

### Iteration 17

- Start UTC: 2026-06-07T19:01:37Z
- End UTC: 2026-06-07T19:04:39Z
- Status: completed
- Item selected: Refined tri-source generation after specificity audit.
- Note: Ask Claude/Gemini, and use RPT table context, for new executable tests
  now that the T/B lead has been narrowed to broad IFN/APC remodeling with
  specificity limits.
- Result: Claude returned 10 concrete JSON analyses. Gemini failed the long
  prompt by `MAX_TOKENS`, then returned 6 usable analyses from a compact prompt.
  Convergent next tests: B/plasma-versus-myeloid IFN/STAT correlation,
  leave-one-gene module dependence, global IFN/steroid residualization where
  markers exist, and within-B/plasma composition if cell-level artifacts are
  accessible.

### Iteration 18

- Start UTC: 2026-06-07T19:04:39Z
- End UTC: 2026-06-07T19:06:53Z
- Status: completed
- Item selected: B/plasma-vs-myeloid IFN independence and leave-one-gene module
  dependence.
- Note: Ground the strongest executable two-lineage proposals from Iteration
  17 on exact compartment data.
- Result: B/plasma IFN/STAT and myeloid IFN/STAT were highly rank-correlated
  (Spearman rho `0.900`, p `0.0009`). B/plasma response separation collapsed
  after residualizing against myeloid (AUC `0.650`, exact p `0.5556`). The
  four-gene score did not collapse when omitting STAT1, GBP1, or ISG15, although
  single STAT1 was strongest. Interpretation: demote B/plasma-independent
  mechanism; current lead is broad cross-compartment IFN remodeling with T/B
  readable outputs.

### Iteration 19

- Start UTC: 2026-06-07T19:06:53Z
- End UTC: 2026-06-07T19:09:01Z
- Status: completed
- Item selected: Steroid/global inflammatory marker coverage and residualization
  check.
- Note: Test whether available exact-matrix markers permit glucocorticoid or
  global inflammatory confound residualization; run where coverage exists.
- Result: V32 subject-level confounders were available for `GSE253006_TOF_exact`.
  Glucocorticoid residualization did not explain B/plasma or T-cell readouts
  (AUCs stayed `0.950` and `1.000`), but residualizing against `delta_stat1_axis`
  collapsed B/plasma (AUC `0.600`) and T-cell (AUC `0.500`). Interpretation:
  not steroid artifact in held scores, but STAT1/IFN-axis dependent.

### Iteration 20

- Start UTC: 2026-06-07T19:09:01Z
- End UTC: 2026-06-07T19:11:07Z
- Status: completed
- Item selected: Baseline-versus-delta decomposition for compartment readouts.
- Note: Test whether the refined readouts are monitoring dynamics or baseline
  stratification using exact compartment baseline and treated scores.
- Result: Monitoring interpretation strengthened. Baseline IFN/APC was null or
  weak across compartments (`0.500` in B/plasma, `0.550` in T cell), while
  treated IFN/APC reached AUC `1.000` in B/plasma, T cell, myeloid, and
  epithelial compartments. The lead is broad on-treatment IFN/APC/STAT1-axis
  state, not baseline subtype.

### Iteration 21

- Start UTC: 2026-06-07T19:11:07Z
- End UTC: 2026-06-07T19:12:49Z
- Status: completed
- Item selected: Treated-timepoint trajectory and sample-timing audit.
- Note: Test whether treated IFN/APC dominance reflects W8 monitoring or mixed
  later timepoint structure.
- Result: W8 is the only interpretable post-baseline timepoint with mixed
  responder labels (`n=8`, `4` responders). At W8, IFN/APC AUC was `1.000`
  in B/plasma, T-cell, myeloid, and epithelial compartments (exact p `0.0286`).
  Later trajectory claims are blocked by sparse/imbalanced W16/W24/W48 data.

### Iteration 22

- Start UTC: 2026-06-07T19:12:49Z
- End UTC: 2026-06-07T19:14:54Z
- Status: completed
- Item selected: Raw cell-level B/plasma subcluster feasibility check.
- Note: Determine whether existing raw GSE253006 data can test within-B/plasma
  subcluster composition versus within-cell remodeling without rebuilding a
  heavy single-cell pipeline.
- Result: Lightweight raw B/plasma substate audit completed. Within-substate
  IFN/APC scores dominated fraction features: `delta_ifn_apc_plasma_like`,
  `treated_ifn_apc_b_like`, and `treated_ifn_apc_plasma_like` all reached AUC
  `1.000` (exact p `0.0159`), while B/plasma substate fraction deltas were weak
  (`0.600`). Supports within-substate IFN remodeling over simple B/plasma
  composition, but not B/plasma specificity.

### Iteration 23

- Start UTC: 2026-06-07T19:14:54Z
- End UTC: 2026-06-07T19:16:48Z
- Status: completed
- Item selected: V36 interim ranked-slate synthesis after lead refactoring.
- Note: Consolidate the many grounding results into the current ranked slate
  and identify the next executable item for the remaining block.
- Result: Interim synthesis written. Current best wording: early W8
  on-treatment IFN/APC/STAT1-axis monitoring state, broad across compartments,
  readable in T/B compartments, not baseline subtype, not glucocorticoid
  explained, not B/plasma-specific, and still single-cohort/unreplicated.

### Iteration 24

- Start UTC: 2026-06-07T19:16:48Z
- End UTC: 2026-06-07T19:18:10Z
- Status: completed
- Item selected: W8 treated IFN/APC subject-level confounder residualization.
- Note: Test whether treated W8 IFN/APC readout survives V32 confounder
  residualization, not just locked delta score residualization.
- Result: W8 treated IFN/APC attenuated under V32 confounders. B/plasma and
  myeloid raw AUCs `1.000` fell to `0.625` and `0.688` after
  `delta_stat1_axis` residualization; T-cell fell to `0.750` after
  `delta_t_cell_composition`. Interpretation: early monitoring signal remains
  STAT1/composition-conditioned, not orthogonal.

### Iteration 25

- Start UTC: 2026-06-07T19:18:10Z
- End UTC: 2026-06-07T19:19:34Z
- Status: completed
- Item selected: V32 module specificity comparison for exact tofacitinib cohort.
- Note: Compare IFN/APC/STAT1 readouts with non-IFN V32 modules in
  `GSE253006_TOF_exact`.
- Result: V32 module scan completed over 28 numeric features. `delta_IFN_APC`,
  `delta_glycolysis`, `delta_stat1_axis`, and `locked_signed_score` tied at AUC
  `0.950` (exact p `0.0317`). Baseline IFN/STAT features were weak/null.
  Interpretation: dynamic monitoring supported; signal is IFN/STAT-led but
  metabolically coupled, not IFN-exclusive.

### Iteration 26

- Start UTC: 2026-06-07T19:19:34Z
- End UTC: 2026-06-07T19:22:05Z
- Status: completed
- Item selected: Focused two-lineage cross-exam of updated conservative lead.
- Note: Ask Claude/Gemini for fatal weaknesses and executable tests after V36
  refactored the lead to broad early IFN/metabolic remodeling.
- Result: Claude returned 5 concrete weaknesses; Gemini required compact prompt
  after `MAX_TOKENS` and returned 3. Most issues were already grounded or require
  external validation/steroid-dose metadata. New executable item: glycolysis
  decoupling from IFN/STAT.

### Iteration 27

- Start UTC: 2026-06-07T19:22:05Z
- End UTC: 2026-06-07T19:24:22Z
- Status: completed
- Item selected: Glycolysis decoupling from IFN/STAT.
- Note: Test whether `delta_glycolysis` retains response signal after
  residualizing against IFN/STAT and vice versa in V32 exact tofacitinib data.
- Result: Glycolysis collapsed after residualization against IFN/APC+STAT1
  (AUC `0.600`, exact p `0.7302`). IFN/APC retained more residual signal after
  glycolysis adjustment (AUC `0.850`, exact p `0.1111`). Interpretation:
  glycolysis is coupled context, not independent mechanism; IFN/STAT is primary
  in held data.

### Iteration 28

- Start UTC: 2026-06-07T19:24:22Z
- End UTC: 2026-06-07T19:27:08Z
- Status: completed
- Item selected: Technical metadata and batch-confounding feasibility check.
- Note: Determine whether held GSE253006 metadata contains batch/capture/date or
  QC fields sufficient to test Claude's batch-confounding critique.
- Result: Batch metadata fields were absent (no lane/capture date/chemistry
  batch/ambient RNA/per-sample processing batch). Raw-matrix QC residualization
  was possible; mitochondrial fraction attenuated W8 IFN/APC readouts
  substantially (B/plasma AUC `1.000` -> `0.688`, myeloid `1.000` -> `0.562`,
  T-cell `1.000` -> `0.750`). Added serious QC validation requirement.

### Iteration 29

- Start UTC: 2026-06-07T19:27:08Z
- End UTC: 2026-06-07T19:28:30Z
- Status: completed
- Item selected: Validation requirement update for refactored V36 lead.
- Note: Translate V36 caveats into concrete future-cohort/harness requirements.
- Result: Added V36 refactored-lead addendum to
  `docs/validation/VALIDATION_READINESS_V27.md`, preserving locked V22 primary
  rule but requiring timing, baseline/treated/delta, STAT1, glycolysis,
  compartment, substate, and technical-QC audits in future validation.

### Iteration 30

- Start UTC: 2026-06-07T19:28:30Z
- End UTC: 2026-06-07T19:30:06Z
- Status: completed
- Item selected: Updated RPT pass over refactored slate.
- Note: Use tabular lens after V36 demotions to prioritize any remaining
  untested patterns; ground output only if executable.
- Result: RPT kept broad early W8 IFN/STAT monitoring as `validation_priority`
  (confidence `0.950`) but over-prioritized B/plasma substate and glycolysis
  relative to grounded demotions. Grounded evidence overrides RPT. No new
  promoted item.

### Iteration 31

- Start UTC: 2026-06-07T19:30:06Z
- End UTC: 2026-06-07T19:31:34Z
- Status: completed
- Item selected: Refactored validation cohort/data scout from held V24
  inventory.
- Note: Re-read V24 scout outputs and identify candidates matching the stricter
  V36 spec: baseline + W8-like early sample, response labels, expression,
  batch/QC/steroid metadata, and compartment support if possible.
- Result: V24 inventory reinterpreted under V36. Best target remains Gafson et
  al. 2018 DMF PBMC RNA-seq, now with added required request fields:
  steroid/glucocorticoid exposure, batch/run metadata, QC metrics, and
  cell-count/deconvolution covariates.

### Iteration 32

- Start UTC: 2026-06-07T19:31:34Z
- End UTC: 2026-06-07T19:33:29Z
- Status: completed
- Item selected: Multiplicity stress test across V36 generated compartment
  features.
- Note: Estimate how surprising the best AUCs are after scanning many
  compartment/feature combinations in the held cohort.
- Result: Exact max-AUC null across 76 generated patient-level features found
  observed max AUC `1.000`, but empirical p for max AUC >= observed was `0.5000`
  and 70.6% of permutations had max AUC >= `0.95`. This downgrades all
  V36-derived perfect-AUC feature claims to exploratory prioritization only.

### Iteration 33

- Start UTC: 2026-06-07T19:33:29Z
- End UTC: 2026-06-07T19:34:22Z
- Status: completed
- Item selected: Update final V36 ranking after multiplicity caveat.
- Note: Reflect exact max-AUC null in the top-line slate before continuing.
- Result: Updated ranking written. Primary target clarified as immutable
  V22/V23 bounded monitoring rule; V36-derived W8/compartment/substate features
  are secondary audits only after multiplicity control.

### Iteration 34

- Start UTC: 2026-06-07T19:34:22Z
- End UTC: 2026-06-07T19:35:28Z
- Status: completed
- Item selected: Human-facing Gafson data request package.
- Note: Convert V36 validation requirements into a concise request artifact for
  the best low-barrier validation dataset.
- Result: Wrote `docs/validation/GAFSON_DATA_REQUEST_V36.md` with exact files
  and covariates to request, including V36 steroid, batch/QC, mitochondrial,
  ambient RNA, and cell-composition requirements.

### Iteration 35

- Start UTC: 2026-06-07T19:35:28Z
- End UTC: 2026-06-07T19:36:48Z
- Status: completed
- Item selected: Resume-state next-actions update for V36 refactored lead.
- Note: Ensure project resume state points to the correct next action after
  V36's demotions and validation-request artifact.
- Result: Updated `meta/NEXT_ACTIONS.md` and `meta/CURRENT_STATUS.md` with V36
  status: locked V22/V23 remains primary validation target; V36 perfect-AUC
  features are secondary audits after multiplicity control; Gafson request
  package and validation-readiness addendum are now canonical.

### Iteration 36

- Start UTC: 2026-06-07T19:36:48Z
- End UTC: 2026-06-07T19:42:27Z
- Status: completed
- Item selected: Continue autonomous V36 block with next executable
  self-generated item.
- Note: Block runtime remains below 120 minutes; select next grounded analysis
  after resume-state update.
- Result: Ran caveated `GSE85034_MTX` psoriasis-skin stress test. The primary
  locked IFN/APC feature did not reproduce (`AUC = 0.600`, exact p `0.346`,
  Hedges g `0.165`). The receptor-side feature was high (`AUC = 0.900`, exact
  p `0.0245`) but is hypothesis-generating only because it was not the frozen
  primary feature, the arm had only `3` responders, and the cohort is outside
  the bounded MS/JAK-STAT validation domain.

### Iteration 37

- Start UTC: 2026-06-07T19:43:17Z
- End UTC: 2026-06-07T19:44:37Z
- Status: completed
- Item selected: Continue autonomous V36 block with next executable
  self-generated item.
- Note: Test whether the out-of-domain MTX receptor-side observation recurs in
  GSE85034 ADA or GSE253006 tofacitinib artifacts, explicitly as a post-hoc
  exploratory feature with multiplicity caveats.
- Result: Receptor-side dynamics were direction- and context-dependent. MTX
  favored `-delta_RECEPTOR` (`AUC = 0.900`, exact p `0.0245`), ADA was null
  (`AUC = 0.444`, exact p `0.650` for the same orientation), and exact TOF
  compartments that looked strong favored `+delta_RECEPTOR` instead
  (`epithelial_like AUC = 1.000`, exact p `0.00794`; `stromal_endothelial_like
  AUC = 0.950`, exact p `0.0159`). No receptor successor rule is warranted.

### Iteration 38

- Start UTC: 2026-06-07T19:45:18Z
- End UTC: 2026-06-07T19:50:26Z
- Status: completed
- Item selected: Continue autonomous V36 block with next executable
  self-generated item.
- Note: Run a focused two-lineage proposal pass on the refactored V36 state,
  requesting only executable in-held tests; ground any concrete test that is
  possible with existing artifacts.
- Result: Claude and Gemini converged mostly on already-executed checks
  (multiplicity, confounder attenuation, receptor stability). Claude proposed a
  concrete T-vs-B/plasma concordance audit, which was grounded: locked signed
  score T-vs-B/plasma Spearman rho `0.883`, permutation p `0.00340`, but sign
  concordance only `0.667`; HLA-II and receptor deltas did not concord.
  Therefore T/B-readable wording is retained only as a qualitative descriptor of
  broad IFN/APC remodeling, not an independent mechanism.

### Iteration 39

- Start UTC: 2026-06-07T19:51:17Z
- End UTC: 2026-06-07T19:53:23Z
- Status: completed
- Item selected: Continue autonomous V36 block with next executable
  self-generated item.
- Note: Use held MS IFN-beta longitudinal artifacts to test whether the
  locked-style dynamic APC/HLA-II score behaves as an early monitoring signal
  across second-injection, month-1, and month-24 timepoints.
- Result: The locked-style combined score did not validate in `GSE24427`
  (`month_1 AUC = 0.576`, permutation p `0.280`). A therapy-specific month-1
  HLA-II/CD74 induction signal did appear (`delta__hla_ii_without_cd74 AUC =
  0.750`, permutation p `0.0201`; `delta__cd74_alone AUC = 0.722`,
  permutation p `0.0370`). This supports the V6/V7 therapy-branch framing, not
  a universal scalar rule.

### Iteration 40

- Start UTC: 2026-06-07T19:54:12Z
- End UTC: 2026-06-07T19:56:07Z
- Status: completed
- Item selected: Continue autonomous V36 block with next executable
  self-generated item.
- Note: Use held `GSE138064` MS IFN-beta dose/hour artifact to test complete
  versus partial responder separation across baseline and dynamic APC-axis
  modules with AUC and permutation nulls.
- Result: Independent IFN-beta branch support. Complete responders had stronger
  baseline HLA-II (`all` AUC `0.685`, permutation p `0.000250`) and early
  receptor-state dynamics (`stable_hour_4 delta__receptor_only_cd74_cd44_cxcr4
  AUC = 0.693`, permutation p `0.00735`; `stable_8MU AUC = 0.688`,
  permutation p `0.0107`). This supports therapy-specific HLA-II/receptor
  interpretation for IFN-beta, not a universal scalar rule.

### Iteration 41

- Start UTC: 2026-06-07T19:56:51Z
- End UTC: 2026-06-07T19:57:58Z
- Status: completed
- Item selected: Continue autonomous V36 block with next executable
  self-generated item.
- Note: Consolidate held-cohort therapy-branch evidence into one auditable table
  separating IFN/APC downshift, HLA-II competence, receptor-state dynamics, and
  out-of-domain/null contexts.
- Result: Wrote therapy-branch evidence map. IFN-beta held artifacts repeatedly
  emphasize HLA-II competence and CD74/receptor dynamics; tofacitinib emphasizes
  IFN/APC/STAT1 downshift; DMF remains the locked MS DMT pass; fingolimod,
  adalimumab, and MTX psoriasis skin argue against unbounded transfer.

### Iteration 42

- Start UTC: 2026-06-07T19:58:45Z
- End UTC: 2026-06-07T19:59:40Z
- Status: completed
- Item selected: Continue autonomous V36 block with next executable
  self-generated item.
- Note: Run exact permutation and leave-one-subject sensitivity for the V22
  locked MS DMT cohorts, especially the DMF pass that remains the primary
  locked-rule support.
- Result: DMF locked score remains directionally supportive but fragile
  (`AUC = 0.720`, exact p `0.155`, LOO min AUC `0.650`). DMF `delta_HLAII` was
  slightly stronger (`AUC = 0.760`, exact p `0.111`). Fingolimod remains
  weak/null (`locked AUC = 0.600`, exact p `0.345`). Fresh validation remains
  mandatory.

### Iteration 43

- Start UTC: 2026-06-07T20:00:18Z
- End UTC: 2026-06-07T20:01:40Z
- Status: completed
- Item selected: Continue autonomous V36 block with next executable
  self-generated item.
- Note: Estimate validation sample-size requirements for a Gafson-style DMF
  cohort using the observed V22 DMF locked-score effect as an empirical template.
- Result: Empirical bootstrap power simulation from `GSE235357` DMF locked-score
  distributions. Under the observed effect template, `n=30` per response group
  gives approximate one-sided p<0.05 power `0.897`; `n=40-50` per group gives
  `0.957-0.981`. Smaller cohorts are directional but unlikely to settle the
  claim, especially after covariate adjustment.

### Iteration 44

- Start UTC: 2026-06-07T20:02:20Z
- End UTC: 2026-06-07T20:03:51Z
- Status: completed
- Item selected: Continue autonomous V36 block with next executable
  self-generated item.
- Note: Extend the DMF validation power estimate with attenuation sensitivity,
  so planning is not overconfident if the true effect is weaker than
  `GSE235357`.
- Result: Attenuation sensitivity showed p-value power alone is not enough.
  At half the observed separation, median AUC is about `0.68`; p<0.05 power can
  still exceed `0.90` at `n=50` per group, while AUC>=0.70 power remains only
  `0.379`. Future validation should pre-specify both significance and
  effect-size/clinical-utility floors.

### Iteration 45

- Start UTC: pending
- Status: todo
- Item selected: Continue autonomous V36 block with next executable
  self-generated item.
- Note: Block runtime remains below 120 minutes after Iteration 44.

## Backlog

| Priority | Item | Status | Current Result / Resume Note |
|---:|---|---|---|
| 1 | Extend client to SAP RPT + smoke test | done | `sap-rpt-1-large` smoke-passed through `rpt-smoke`; access documented. |
| 2 | RPT-driven structured-data hypothesis pass | done | RPT added prioritization value but no data-grounded upgrades; see `analysis/v36_rpt_structured_pass/` and slate. |
| 3 | Expansive tri-source generation round | done | 16 model hypotheses consolidated; first executable subset grounded with no upgrades. |
| 4 | T/B compartment remodeling gate artifact audit | done | Survives simple count/fraction residualization, but T-cell component attenuates; B/plasma is more robust. |
| 5 | Postpartum APC-arm imbalance MS-specificity | done | Pregnancy-phase MS movement grounded; postpartum relapse-window test blocked by missing data. |
| 6 | Metabolic/sterol, lysosomal, complement/lipid, EBV/IFN deepening | done | No upgrades; generated variants remain blocked/proposal-only without new data. |
| 7 | Deep multi-pass cross-examination | done | Gemini critiques grounded; T/B and postpartum interpretations refined, no upgrade. |
| 8 | Heavier analyses now affordable | done | Exhaustive compartment-combination scan added overfit warning; no upgrade. |
| 9 | B/plasma-specific module decomposition | done | B/plasma IFN/APC delta carries signal; HLA-II/receptor/counts weaker. |
| 10 | Cross-disease response-cohort B/plasma proxy scout | done | Independent replication blocked with held data; only GSE253006 is compartment-resolved. |
| 11 | RPT second pass with refined B/plasma/T-cell split | done | RPT agrees carrier candidates are promising-but-unreplicated; no evidence upgrade. |
| 12 | Gene-level B/plasma IFN/APC driver analysis | done | Carrier sharpens to B/plasma IFN/STAT remodeling; STAT1 strongest but no STAT1-only promotion. |
| 13 | Timepoint and responder-leverage sensitivity for B/plasma IFN/STAT carrier | done | Not driven by W48 TOF_009 or one removable patient; still internal only. |
| 14 | Cross-compartment STAT1/IFN specificity scan | done | STAT1 downshift is broad, not B/plasma-specific; compartment specificity weakened. |
| 15 | Same-compartment random/module negative control for IFN/STAT signal | done | Limited locked-gene combo null blocks narrow IFN/STAT four-gene specificity claim. |
| 16 | Refined tri-source generation after specificity audit | done | Claude/Gemini generated concrete next tests; no evidence upgrade. |
| 17 | B/plasma-vs-myeloid IFN independence and leave-one-gene module dependence | done | B/plasma-independent mechanism demoted; broad IFN remodeling favored. |
| 18 | Steroid/global inflammatory marker coverage and residualization check | done | Glucocorticoid did not explain; delta STAT1-axis did. |
| 19 | Baseline-versus-delta decomposition for compartment readouts | done | Baseline weak/null; treated IFN/APC and delta dominate, supporting monitoring. |
| 20 | Treated-timepoint trajectory and sample-timing audit | done | W8 early monitoring supported; later trajectory blocked by sparse data. |
| 21 | Raw cell-level B/plasma subcluster feasibility check | done | Within-substate IFN/APC dominates B/plasma substate fractions; broad IFN dependence remains. |
| 22 | V36 interim ranked-slate synthesis after lead refactoring | done | Lead refactored to early W8 broad IFN/APC/STAT1 monitoring state. |
| 23 | W8 treated IFN/APC subject-level confounder residualization | done | W8 treated IFN/APC is STAT1/composition-conditioned, not orthogonal. |
| 24 | V32 module specificity comparison for exact tofacitinib cohort | done | IFN/STAT-led but glycolysis-tied; dynamic broad remodeling, not IFN-exclusive. |
| 25 | Focused two-lineage cross-exam of updated conservative lead | done | Glycolysis decoupling queued; several other issues external-data gated. |
| 26 | Glycolysis decoupling from IFN/STAT | done | Glycolysis is coupled context, not independent mechanism; IFN/STAT primary. |
| 27 | Technical metadata and batch-confounding feasibility check | done | Batch metadata absent; mito/QC attenuation adds validation requirement. |
| 28 | Validation requirement update for refactored V36 lead | done | V36 validation-readiness addendum added. |
| 29 | Updated RPT pass over refactored slate | done | RPT concordant for broad W8 state but over-promotes grounded-demoted variants. |
| 30 | Refactored validation cohort/data scout from held V24 inventory | done | Gafson remains best target with stricter V36 metadata request. |
| 31 | Multiplicity stress test across V36 generated compartment features | done | Perfect V36 feature AUCs are expected under post-hoc feature search; exploratory only. |
| 32 | Update final V36 ranking after multiplicity caveat | done | Locked V22/V23 remains primary; V36 features secondary audits only. |
| 33 | Human-facing Gafson data request package | done | Gafson request package written with V36 covariate/QC requirements. |
| 34 | Resume-state next-actions update for V36 refactored lead | done | `meta/NEXT_ACTIONS.md` and `meta/CURRENT_STATUS.md` updated for V36. |
| 35 | Continue autonomous V36 block with next executable self-generated item | done | GSE85034 MTX stress test complete: locked IFN/APC null out of domain; receptor-side signal hypothesis-generating only. |
| 36 | Receptor/coupling stress-test follow-up from GSE85034 MTX | done | Direction/context instability blocks receptor successor rule; keep as mechanistic prompt only. |

## Timing Rule

Each iteration must append its measured start and end UTC from `date -u`.
Continue chaining until cumulative measured active time is at least 120 minutes,
unless all backlog items are done/blocked or external termination occurs.
