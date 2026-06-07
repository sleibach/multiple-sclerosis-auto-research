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
- Status: in_progress
- Item selected: W8 treated IFN/APC subject-level confounder residualization.
- Note: Test whether treated W8 IFN/APC readout survives V32 confounder
  residualization, not just locked delta score residualization.

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
| 23 | W8 treated IFN/APC subject-level confounder residualization | in_progress | Residualize W8 treated IFN/APC against V32 confounders. |

## Timing Rule

Each iteration must append its measured start and end UTC from `date -u`.
Continue chaining until cumulative measured active time is at least 120 minutes,
unless all backlog items are done/blocked or external termination occurs.
