# V38 Queue - Four-Hour Autonomous Block

## Timing

- Block start UTC: 2026-06-08T20:30:23Z
- Target end UTC: 2026-06-09T00:30:23Z
- Timing source: real `date -u` system-clock reads.

## Integrity Rules

- Mode: unconventional question generation with unchanged evidence gate.
- No model/RPT output is evidence; it only prioritizes grounded tests.
- No locked-rule edits.
- OpenGWAS POST only; token expires 2026-06-19 and is near enough to flag.
- Commit each clean iteration.

## Backlog

| Priority | Workstream | Item | Status | Resume Note |
|---:|---|---|---|---|
| 1 | B | Adversarial inversion of bounded V22/V23 monitoring signal | done | First adversarial target completed: inversion narrowed but did not kill the bounded scalar. |
| 2 | A | Failure-structure meta-analysis across killed/closed leads | done | V37 closed/negative frame analyzed: dominant families are evidence-resolution failure (7/20), context/axis dependence (5/20), direction/modality constraint (5/20), and specificity/control failure (4/20). |
| 3 | E | RPT-led structured mining over V37 score table and lead matrices | done | RPT matched 5/6 masked V37 action classes; only contradiction was bounded scalar predicted as data-gated follow-up, sharpening operational-priority wording without evidence demotion. |
| 4 | C | Unpublishable-but-true exclusion/non-replication list | done | Ledger written with 16 exclusions/non-replications: 13 negative-established, 2 supported exclusions, 1 data-gated not-established. |
| 5 | D | Cross-scale/control-systems reframing | done | Baseline load weak; dynamic/treated-state framing supported but set-point result is supervised/in-sample and needs fresh validation. |
| 6 | B | Adversarial inversion of coupled APC architecture | done | Global immune tone is strong, but row-centering does not erase core APC edges; coupling is tone-loaded mechanistic context, not a predictive successor. |
| 7 | B | Adversarial inversion of MS-UC genetic backdrop | done | V21 MS-UC rg survives recorded MHC/sample-overlap inversion, with caveat that the reference panel was already effectively MHC-free. |
| 8 | A/D | Failure-structure follow-up: hard-protective-direction constraint | done | Direction/modality constraints affect 8/20 closed/negative items and 5/6 target-like items; mandatory early prefilter for future target leads. |
| 9 | B/C | Adversarial inversion of layer-transfer map | done | Matrix-grounded: 4/4 key diseases have heterogeneous axis placements and 8/8 non-artifact cells are axis-specific. |
| 10 | A/C | V36 exploratory fragility map | done | V36 promotion failures cluster around multiplicity, confounder/composition, therapy specificity, small-n power, and missing decisive modalities/metadata. |
| 11 | B/D/E | Multi-lineage proposal pass plus tone-residual scalar grounding | done | Claude/Gemini proposed next tests; grounded tone-residual scalar test shows broad tone alone does not reproduce the scalar response signal. |
| 12 | A/C | Failure-vs-fragility concordance audit | done | Gate-level comparison shows maps are complementary: V38 captures direction/modality and marker-not-driver; V36 captures overfit/power/technical fragility. |
| 13 | B | Layer-map heterogeneity permutation null | done | Simple 4/4 heterogeneity is not exceptional under random placement-label reassignment; layer-map evidence should rest on disagreement-cell specificity. |
| 14 | D | Structured V37-to-V38 delta ledger | done | Wrote 8-item delta ledger: four strengthened-and-narrowed, no demotions, plus new prefilter/negative/fragility methodological ledgers. |
| 15 | E | Tool-lens contribution ledger | done | RPT/Claude/Gemini contributed prioritization/proposals only; no model/RPT output upgraded evidence. |

## Iteration Log

### Iteration 1

- Start UTC: 2026-06-08T20:30:23Z
- Resume UTC after interruption: 2026-06-09T04:16:56Z
- End UTC: 2026-06-09T04:21:54Z
- Status: completed
- Item selected: Workstream B, adversarial inversion of the bounded monitoring
  signal.
- Planned grounding: verify environment/tooling, read V37/V28/V32/V22/V23
  artifacts, build artifact/inversion tests from existing summary tables, and
  write the first V38 report section.
- Result: OpenGWAS verified HTTP 200; token expires `2026-06-19 12:28 UTC`.
  Gemini, Claude, and RPT smoke-passed. Claude/Gemini generated proposal-only
  inversion candidates. Grounding in `scripts/v38_adversarial_monitoring_inversion.py`
  showed adversarial inversion narrows but does not kill the V37 scalar claim:
  bounded AUC `0.811` vs primary-all AUC `0.547`; DMF-only AUC `0.720`, exact
  p `0.155`; exact tofacitinib-only AUC `0.950`, exact p `0.0159`; V32
  immune-tone adjustment AUC `0.656`, p `0.163`; threshold transfer weak
  (`0.667` and `0.600` accuracy). Report updated in
  `docs/history/UNCONVENTIONAL_FINDINGS_V38.md`.

### Iteration 2

- Start UTC: 2026-06-09T04:22:36Z
- End UTC: 2026-06-09T04:24:43Z
- Status: completed
- Item selected: Workstream A, failure-structure meta-analysis across
  killed/closed leads.
- Planned grounding: use `docs/reports/FINDINGS_SCORES_V37.tsv` as the
  closed/negative item frame, annotate failure modes from committed artifact
  summaries, count recurrent structures, and update the V38 report.
- Result: `scripts/v38_failure_structure_meta.py` analyzed 20 V37
  closed/negative/decoupling items. There is no single universal failure law.
  Dominant families: evidence-resolution failure `7/20`, context/axis
  dependence `5/20`, direction/modality constraint `5/20`, specificity/control
  failure `4/20`. V38 report updated.

### Iteration 3

- Start UTC: 2026-06-09T04:25:16Z
- End UTC: 2026-06-09T04:27:45Z
- Status: completed
- Item selected: Workstream E, RPT-led structured mining over V37 score table
  and V38 failure-mode annotations.
- Planned grounding: construct a compact tabular payload from V37/V38 tables,
  let RPT classify masked rows, then compare RPT-surfaced patterns against
  actual scored-table/failure-family counts.
- Result: `scripts/v38_rpt_structural_mining.py` built a V37/V38 feature table
  and masked six edge items. RPT matched the artifact-derived action class for
  `5/6` rows. The single contradiction was the bounded scalar, predicted as
  `data_gated_followup` rather than `external_validation_priority`, reinforcing
  that its priority is operational/clinical and not evidence-grade inflation.

### Iteration 4

- Start UTC: 2026-06-09T04:28:25Z
- End UTC: 2026-06-09T04:29:59Z
- Status: completed
- Item selected: Workstream C, unpublishable-but-true exclusion and
  non-replication ledger.
- Planned grounding: extract negative-established and supported exclusion
  statements from V37/V38 tables and source artifacts; distinguish rigorous
  exclusions from merely data-gated unknowns.
- Result: `scripts/v38_exclusion_ledger.py` wrote 16 decision-useful
  exclusions/non-replications. Counts: 13 negative-established, 2 supported
  exclusions, 1 data-gated not-established. V38 report updated.

### Iteration 5

- Start UTC: 2026-06-09T04:30:29Z
- End UTC: 2026-06-09T04:38:58Z
- Status: completed
- Item selected: Workstream D, cross-scale/control-systems reframing.
- Planned grounding: use held baseline/treated/delta module score tables to
  test whether response is better framed as movement toward an immune set-point
  or as generic baseline/delta magnitude.
- Result: `scripts/v38_control_system_reframing.py` tested 54 scalar features
  from the V32 subject-level table (`n=19`, responders/non-responders `10/9`).
  Baseline-load features were weak (best AUC `0.667`, exact p `0.243`);
  early dynamic/control action retained the best simple scalar
  (`locked_signed_score` AUC `0.811`, exact p `0.022`) but not after
  within-family max-AUC correction (`p=0.190`) or all-feature BH (`q=0.397`).
  Treated-state/set-point proximity was interesting (treated IFN/HLA-II/STAT1/
  metabolic proximity AUC `0.867`, Monte Carlo p `0.0098`) but supervised and
  in-sample. Report updated; no new rule promoted.

### Iteration 6

- Start UTC: 2026-06-09T04:39:44Z
- End UTC: 2026-06-09T04:44:12Z
- Status: completed
- Item selected: Workstream B, adversarial inversion of coupled APC
  architecture.
- Planned grounding: use V26/V27 coupled-axis and module-dependency outputs to
  test whether the claimed coupling survives controls for broad immune tone,
  composition, and scalar-response covariance.
- Result: `scripts/v38_coupled_architecture_inversion.py` tested V26 module
  matrices after row-wise global-tone centering. Core modules are strongly
  tone-loaded (median abs correlation with row mean `0.854`), so the inversion
  partly succeeds. But core APC edges did not collapse: `13/32` retained abs r
  >= `0.5` and permutation p < `0.05`, with `10/32` also BH q < `0.10`.
  V27 remains the predictive constraint: coupled features did not beat the V22
  scalar. Report updated as tone-loaded coupled architecture, not pure APC
  invariant and not a successor rule.

### Iteration 7

- Start UTC: 2026-06-09T04:45:21Z
- End UTC: 2026-06-09T04:47:05Z
- Status: completed
- Item selected: Workstream B, adversarial inversion of MS-UC genetic backdrop.
- Planned grounding: use recorded V21 LDSC full and MHC-excluded rg outputs to
  test whether the MS-UC backdrop is MHC/sample-overlap dominated or otherwise
  unsupported outside the primary LDSC run.
- Result: `scripts/v38_rg_backdrop_inversion.py` parsed committed V21 LDSC
  results only. MS-UC full rg remained `0.3342` (`p=4.8771e-14`), no-MHC rg was
  identical, and recorded intercepts did not strongly support a
  sample-overlap/confounding inversion. The caveat remains important: the
  no-MHC run is not an independent MHC-containing-reference sensitivity because
  the active LDSC panel already had zero chr6:25-34 Mb SNPs. Report updated.

### Iteration 8

- Start UTC: 2026-06-09T04:47:38Z
- End UTC: 2026-06-09T04:48:55Z
- Status: completed
- Item selected: Workstream A/D, hard-protective-direction constraint follow-up.
- Planned grounding: use the V38 failure-mode table to quantify how often
  direction/modality constraints recur, separating restoration/up-function
  target problems from opposite-direction transfer and unresolved-direction
  genetics.
- Result: `scripts/v38_direction_modality_prefilter.py` found direction/modality
  constraints in `8/20` closed/negative items overall and `5/6` target-like
  genetics/nomination items. Hard restoration/up-function/agonism was `2/20`,
  so it is not a universal law, but the target-like recurrence is strong enough
  to make direction-matched modality a mandatory early prefilter. Report updated.

### Iteration 9

- Start UTC: 2026-06-09T04:49:52Z
- End UTC: 2026-06-09T04:51:26Z
- Status: completed
- Item selected: Workstream B/C, adversarial inversion of the layer-transfer
  map.
- Planned grounding: use V8-V12 placement/disagreement matrices and transfer
  reports to test whether transfer-validity claims are axis-specific and
  evidence-backed, or merely narrative disease-proximity assertions.
- Result: `scripts/v38_layer_transfer_inversion.py` parsed V8/V11 matrices. All
  four key comparator diseases are heterogeneous across axes, and all eight
  non-artifact disagreement cells had axis-specific placement plus
  compartment/causality/independence evidence. The narrative-similarity
  inversion is not supported; the map remains a warning/triage framework, not
  an intervention claim. Report updated.

### Iteration 10

- Start UTC: 2026-06-09T04:52:16Z
- End UTC: 2026-06-09T04:54:34Z
- Status: completed
- Item selected: Workstream A/C, V36 exploratory fragility map.
- Planned grounding: parse V36 summary artifacts and machine-readable outputs
  to classify which exploratory hypothesis classes repeatedly fail under
  multiplicity, confounder, compartment, timepoint, or data-specificity stress.
- Result: `scripts/v38_v36_fragility_map.py` aggregated 13 selected V36
  machine-readable artifacts. Promotion failed mostly at multiplicity/overfit,
  composition/confounder, therapy-branch, small-n power, and missing
  modality/metadata gates. The narrow survivor remains B/plasma-like IFN/APC
  remodeling as an internal carrier, still single-cohort and validation-gated.
  Report updated.

### Iteration 11

- Start UTC: 2026-06-09T04:55:19Z
- End UTC: 2026-06-09T04:59:43Z
- Status: completed
- Item selected: Workstreams B/D/E, multi-lineage proposal pass for the next
  unconventional grounded test.
- Planned grounding: prompt Claude and Gemini with the V38 results so far and
  ask for concrete table-groundable remaining adversarial/unconventional tests;
  then select and run the highest-value executable test. Model proposals are
  not evidence.
- Result: Claude proposed a tone-stripped scalar inversion; Gemini produced a
  separate terse proposal list after increasing the token cap. Grounding in
  `scripts/v38_tone_residual_scalar.py` used the V32 bounded subject-level
  table. Broad-tone LOOCV prediction alone had AUC `0.589` (p `0.549`), while
  the tone-residual scalar had AUC `0.844` (p `0.0101`) versus raw scalar
  AUC `0.811` (p `0.0220`). This weakens the "scalar is merely broad immune
  tone" inversion but does not create a new locked rule. Report updated.

### Iteration 12

- Start UTC: 2026-06-09T05:00:25Z
- End UTC: 2026-06-09T05:01:45Z
- Status: completed
- Item selected: Workstream A/C, failure-vs-fragility concordance audit.
- Planned grounding: map V38 failure-family counts and V36 fragility-family
  counts onto a shared gate taxonomy, then test whether they are redundant or
  complementary views of the same project constraint structure.
- Result: `scripts/v38_failure_fragility_concordance.py` compared shared gate
  distributions rather than forcing a false item-level join. Jensen-Shannon
  divergence was `0.186` bits. The maps are complementary: V38 captures
  direction/modality and marker-not-driver target failures, while V36 captures
  multiplicity/overfit, power, technical, and exploratory-data fragility. Report
  updated.

### Iteration 13

- Start UTC: 2026-06-09T05:02:29Z
- End UTC: 2026-06-09T05:03:37Z
- Status: completed
- Item selected: Workstream B, layer-map heterogeneity permutation null.
- Planned grounding: permute placement labels across key disease-axis rows to
  test whether the simple "4/4 key diseases heterogeneous" statistic is itself
  exceptional, separate from the richer disagreement-cell evidence.
- Result: `scripts/v38_layer_heterogeneity_null.py` showed the simple
  heterogeneity statistic is not exceptional under random placement-label
  reassignment (`p=0.276` for `4/4` heterogeneous diseases; `p=0.147` for mean
  placement range). This narrows the layer-transfer claim: it should rest on the
  V11/V12 disagreement-cell evidence, not the heterogeneity count alone. Report
  updated.

### Iteration 14

- Start UTC: 2026-06-09T05:04:21Z
- End UTC: 2026-06-09T05:05:56Z
- Status: completed
- Item selected: Workstream D, structured V37-to-V38 delta ledger.
- Planned grounding: write a compact table of V37 conclusions affected by V38,
  with delta type, supporting V38 artifact, and whether the evidence grade
  changes.
- Result: `scripts/v38_delta_ledger.py` wrote
  `analysis/v38_delta_ledger/v37_v38_delta_ledger.tsv` and summary JSON.
  Ledger contains `8` delta items: four `strengthened_and_narrowed`, no
  demotions, and new operational/methodological negative ledgers. Report updated.

### Iteration 15

- Start UTC: 2026-06-09T05:06:51Z
- End UTC: 2026-06-09T05:07:56Z
- Status: completed
- Item selected: Workstream E, tool-lens contribution ledger.
- Planned grounding: write a compact ledger separating RPT/Claude/Gemini
  proposal value from data-grounded evidence, including whether any lens caused
  an evidence upgrade.
- Result: `scripts/v38_tool_lens_ledger.py` wrote the contribution ledger.
  RPT/Claude/Gemini added prioritization and test ideas, but no lens output was
  evidence and no lens upgraded a finding. SAP AI Core spend is not exposed by
  the local client outputs. Report updated.
