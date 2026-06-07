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
- Status: in_progress
- Item selected: Deep multi-pass cross-examination of top grounded hypotheses.
- Note: Use Claude and Gemini with higher budget to attack the refined T/B
  gate and postpartum acquisition lead; ground concrete criticisms where held
  data allows.

## Backlog

| Priority | Item | Status | Current Result / Resume Note |
|---:|---|---|---|
| 1 | Extend client to SAP RPT + smoke test | done | `sap-rpt-1-large` smoke-passed through `rpt-smoke`; access documented. |
| 2 | RPT-driven structured-data hypothesis pass | done | RPT added prioritization value but no data-grounded upgrades; see `analysis/v36_rpt_structured_pass/` and slate. |
| 3 | Expansive tri-source generation round | done | 16 model hypotheses consolidated; first executable subset grounded with no upgrades. |
| 4 | T/B compartment remodeling gate artifact audit | done | Survives simple count/fraction residualization, but T-cell component attenuates; B/plasma is more robust. |
| 5 | Postpartum APC-arm imbalance MS-specificity | done | Pregnancy-phase MS movement grounded; postpartum relapse-window test blocked by missing data. |
| 6 | Metabolic/sterol, lysosomal, complement/lipid, EBV/IFN deepening | done | No upgrades; generated variants remain blocked/proposal-only without new data. |
| 7 | Deep multi-pass cross-examination | in_progress | Claude/Gemini adversarial rounds for top grounded hypotheses; ground concrete proposals. |
| 8 | Heavier analyses now affordable | todo | Larger permutation/module scans or pooled tests where executable. |

## Timing Rule

Each iteration must append its measured start and end UTC from `date -u`.
Continue chaining until cumulative measured active time is at least 120 minutes,
unless all backlog items are done/blocked or external termination occurs.
